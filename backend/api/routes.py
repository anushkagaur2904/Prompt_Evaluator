from fastapi import APIRouter, BackgroundTasks
from typing import Optional
from models.schemas import (
    PromptRequest, EvaluationResponse, OptimizationResponse,
    ModelComparisonResponse, ModelResponse, BehaviorStats, ApiStatusResponse,
    CompareResponse, ABTestRequest, ABTestResponse,
    DatasetEntry, FeedbackRequest
)
from engine.nlp import analyze, evaluate_prompt
from db.database import log_interaction, save_dataset_entry, list_dataset_entries, save_prompt_version, list_prompt_versions, save_feedback
from engine.optimizer import detect_intent, get_template_name
from engine.behavior import analyze_behavior
from engine.llm_api import get_real_llm_responses, get_api_status
from engine.security import detect_injection

router = APIRouter()

@router.post("/analyze", response_model=EvaluationResponse)
def analyze_prompt(request: PromptRequest):
    result = evaluate_prompt(
        request.prompt,
        expected_keywords=request.expected_keywords,
        expected_format=request.expected_format,
        ideal_length=request.ideal_length
    )
    regression_detected = False
    score_change = None
    if request.previous_score is not None:
        score_change = round(result["score"] - request.previous_score, 1)
        regression_detected = result["score"] < request.previous_score
    
    intent = detect_intent(request.prompt)
    template = get_template_name(intent)
    
    return EvaluationResponse(
        original_prompt=request.prompt,
        score=result["score"],
        metrics=result["metrics"],
        issues=result["issues"],
        response_prediction=result.get("response_prediction", {"type": "Unknown", "confidence": 0.0}),
        regression_detected=regression_detected,
        previous_score=request.previous_score,
        score_change=score_change,
        intent=intent,
        template=template
    )

@router.post("/optimize", response_model=OptimizationResponse)
def optimize_prompt(request: PromptRequest):
    analyze_result_before = evaluate_prompt(
        request.prompt,
        expected_keywords=request.expected_keywords,
        expected_format=request.expected_format,
        ideal_length=request.ideal_length
    )
    optimized_text, suggestions_data = optimize(request.prompt)
    analyze_result_after = evaluate_prompt(
        optimized_text,
        expected_keywords=request.expected_keywords,
        expected_format=request.expected_format,
        ideal_length=request.ideal_length
    )
    return OptimizationResponse(
        original_prompt=request.prompt,
        suggestions=suggestions_data,
        improved_prompt=optimized_text,
        score_before=analyze_result_before["score"],
        score_after=analyze_result_after["score"],
        metrics_before=analyze_result_before["metrics"],
        metrics_after=analyze_result_after["metrics"]
    )

@router.get("/api-status", response_model=ApiStatusResponse)
def api_status():
    return ApiStatusResponse(statuses=get_api_status())

@router.post("/compare-models", response_model=ModelComparisonResponse)
def compare_models(request: PromptRequest):
    responses = get_real_llm_responses(request.prompt)
    model_list = []

    for model_name, data in responses.items():
        response_text = data["text"]
        stats, labels = analyze_behavior(model_name, response_text)
        b_stats = BehaviorStats(**stats)
        model_list.append(ModelResponse(
            model_name=model_name,
            response_text=response_text,
            behavior_stats=b_stats,
            behavior_labels=labels,
            latency_ms=data.get("latency_ms", 0),
            source=data.get("source", "mock"),
            error=data.get("error")
        ))

    explanation = [
        "Groq (LLaMA) prioritizes inference speed with moderate detail — optimized for low-latency responses.",
        "Gemini excels at fast, strictly-structured output — trained for concise bullet-pointed answers.",
        "HuggingFace (Mistral) provides community-model flexibility — output quality varies by model selection."
    ]

    best_model = "Groq"
    best_score = -1
    for m in model_list:
        if m.source == "real":
            length = len(m.response_text)
            lat = m.latency_ms if m.latency_ms > 0 else 1
            score = (length / lat) * 100
            if score > best_score:
                best_score = score
                best_model = m.model_name

    rec = {
        "best_model": best_model,
        "reason": f"Based on your prompt, {best_model} provided the best trade-off between response detail and inference speed during our live benchmark."
    }

    return ModelComparisonResponse(
        original_prompt=request.prompt,
        models=model_list,
        explanation=explanation,
        recommendation=rec
    )


@router.post("/ab-test", response_model=ABTestResponse)
def ab_test(request: ABTestRequest):
    result_a = evaluate_prompt(
        request.prompt_a,
        expected_keywords=request.expected_keywords,
        expected_format=request.expected_format,
        ideal_length=request.ideal_length,
    )
    result_b = evaluate_prompt(
        request.prompt_b,
        expected_keywords=request.expected_keywords,
        expected_format=request.expected_format,
        ideal_length=request.ideal_length,
    )

    winner = "A" if result_a["score"] >= result_b["score"] else "B"
    regression_detected = result_b["score"] < result_a["score"]
    message = (
        f"Prompt {winner} performs better based on deterministic prompt metrics."
        if winner else "Comparison complete."
    )
    return ABTestResponse(
        prompt_a=request.prompt_a,
        prompt_b=request.prompt_b,
        metrics_a=result_a["metrics"],
        metrics_b=result_b["metrics"],
        issues_a=result_a["issues"],
        issues_b=result_b["issues"],
        score_a=result_a["score"],
        score_b=result_b["score"],
        winner=winner,
        regression_detected=regression_detected,
        message=message
    )


@router.post("/dataset")
async def add_dataset_entry(entry: DatasetEntry):
    success = await save_dataset_entry(
        prompt=entry.prompt,
        expected_keywords=entry.expected_keywords,
        expected_format=entry.expected_format,
        ideal_length=entry.ideal_length,
        version=entry.version,
    )
    return {"success": success}


@router.get("/dataset")
async def get_dataset_entries():
    return await list_dataset_entries()


@router.post("/prompt-history")
async def add_prompt_history(entry: DatasetEntry):
    success = await save_prompt_version(
        prompt=entry.prompt,
        version=entry.version or "v1",
        score=0.0,
        metrics={},
    )
    return {"success": success}


@router.get("/prompt-history")
async def get_prompt_history(prompt: Optional[str] = None):
    return await list_prompt_versions(prompt)


@router.post("/feedback")
async def add_feedback(feedback: FeedbackRequest):
    success = await save_feedback(
        prompt=feedback.prompt,
        feedback=feedback.feedback,
        score=feedback.score,
        comment=feedback.comment,
    )
    return {"success": success}

@router.post("/compare", response_model=CompareResponse)
def compare_endpoint(request: PromptRequest, background_tasks: BackgroundTasks):
    injection_result = detect_injection(request.prompt)
    is_malicious = injection_result["is_malicious"]
    reason = injection_result["reason"]

    responses = get_real_llm_responses(request.prompt)
    
    final_responses = {}
    final_scores = {}
    final_latencies = {}
    
    best_model = "Groq"
    best_score = -1

    for model_name, data in responses.items():
        response_text = data["text"]
        latency_ms = data.get("latency_ms", 0)
        
        stats, _ = analyze_behavior(model_name, response_text)
        
        avg_score = ((stats["verbosity"] + stats["structure"] + stats["creativity"] + stats["safety"]) / 4) * 10
        
        final_responses[model_name] = response_text
        final_scores[model_name] = round(avg_score, 1)
        final_latencies[model_name] = latency_ms

        length = len(response_text)
        lat = latency_ms if latency_ms > 0 else 1
        efficiency_score = (length / lat) * 100
        if efficiency_score > best_score and data.get("source") == "real":
            best_score = efficiency_score
            best_model = model_name

    regression_detected = False
    score_change = None
    if request.previous_score is not None:
        average_score = sum(final_scores.values()) / len(final_scores) if final_scores else 0
        score_change = round(average_score - request.previous_score, 1)
        regression_detected = average_score < request.previous_score

    background_tasks.add_task(
        log_interaction,
        prompt=request.prompt,
        responses=final_responses,
        scores=final_scores,
        latency=final_latencies,
        is_malicious=is_malicious
    )

    return CompareResponse(
        is_malicious=is_malicious,
        reason=reason,
        responses=final_responses,
        scores=final_scores,
        latency=final_latencies,
        best_model=best_model
        , regression_detected=regression_detected
        , previous_score=request.previous_score
        , score_change=score_change
    )
