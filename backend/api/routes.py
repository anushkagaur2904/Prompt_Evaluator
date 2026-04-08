from fastapi import APIRouter
from models.schemas import (
    PromptRequest, EvaluationResponse, OptimizationResponse,
    ModelComparisonResponse, ModelResponse, BehaviorStats, ApiStatusResponse
)
from engine.nlp import analyze
from engine.optimizer import optimize
from engine.behavior import analyze_behavior
from engine.llm_api import get_real_llm_responses, get_api_status

router = APIRouter()

@router.post("/analyze", response_model=EvaluationResponse)
def analyze_prompt(request: PromptRequest):
    result = analyze(request.prompt)
    return EvaluationResponse(
        original_prompt=request.prompt,
        score=result["score"],
        metrics=result["metrics"],
        issues=result["issues"],
        response_prediction=result.get("response_prediction", {"type": "Unknown", "confidence": 0.0})
    )

@router.post("/optimize", response_model=OptimizationResponse)
def optimize_prompt(request: PromptRequest):
    analyze_result_before = analyze(request.prompt)
    optimized_text, suggestions_data = optimize(request.prompt, analyze_result_before["metrics"])
    analyze_result_after = analyze(optimized_text)
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
