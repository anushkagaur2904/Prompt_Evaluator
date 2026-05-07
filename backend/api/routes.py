from fastapi import APIRouter
from models.schemas import PromptRequest

from engine.security import detect_injection
from engine.nlp import analyze
from engine.optimizer import optimize
from engine.llm_api import (
    get_real_llm_responses,
    get_api_status
)

from db.database import (
    save_prompt_version,
    list_prompt_versions,
    delete_prompt_version
)

router = APIRouter()


# ───────────────── API STATUS ─────────────────
@router.get("/api-status")
def api_status():
    return get_api_status()


# ───────────────── ANALYZE ─────────────────
@router.post("/analyze")
def analyze_prompt(request: PromptRequest):

    # ✅ SECURITY CHECK
    security = detect_injection(request.prompt)

    if security["is_malicious"]:

        return {
            "original_prompt": request.prompt,

            "blocked": True,

            "risk_level": security["risk_level"],

            "reason": security["reason"],

            "score": 0,

            "metrics": {
                "clarity": 0,
                "specificity": 0,
                "context": 0,
                "instruction": 0,
                "ambiguity": 1,
                "keyword_relevance": 0,
                "format_valid": 0,
                "conciseness": 0
            },

            "issues": [
                "Prompt blocked due to malicious or unsafe intent."
            ],

            "prediction": {
                "label": "Blocked",
                "confidence": 100
            },

            "intent": "blocked"
        }

    # ✅ NORMAL ANALYSIS
    analysis = analyze(request.prompt)

    return {
        "original_prompt": request.prompt,

        "blocked": False,

        "score": analysis["score"],

        "metrics": analysis["metrics"],

        "issues": analysis["issues"],

        "prediction": {
            "label": (
                "Excellent" if analysis["score"] >= 8 else
                "Good" if analysis["score"] >= 6 else
                "Average" if analysis["score"] >= 4 else
                "Poor"
            ),

            "confidence": round(analysis["score"] * 10, 1)
        },

        "intent": analysis["intent"]
    }


# ───────────────── OPTIMIZE ─────────────────
@router.post("/optimize")
def optimize_prompt(request: PromptRequest):

    # ✅ SECURITY CHECK
    security = detect_injection(request.prompt)

    if security["is_malicious"]:

        return {
            "blocked": True,

            "reason": "Optimization disabled for unsafe prompts.",

            "suggestions": []
        }

    # ✅ NORMAL OPTIMIZATION
    return optimize(request.prompt)


# ───────────────── COMPARE ─────────────────
@router.post("/compare")
def compare_models(request: PromptRequest):

    # ✅ SECURITY CHECK
    security = detect_injection(request.prompt)

    if security["is_malicious"]:

        return {
            "is_malicious": True,

            "reason": security["reason"],

            "responses": {},

            "best_model": "None"
        }

    # ✅ NORMAL COMPARISON
    llm_data = get_real_llm_responses(request.prompt)

    return {
        "is_malicious": False,

        "reason": "",

        "responses": llm_data["results"],

        "best_model": llm_data["best_model"]
    }

# ───────────────── A/B TEST ─────────────────
@router.post("/ab-test")
def ab_test(data: dict):

    prompt_a = data.get("prompt_a", "")
    prompt_b = data.get("prompt_b", "")

    if not prompt_a or not prompt_b:

        return {
            "success": False,
            "message": "Both prompts are required."
        }

    # analyze prompt A
    analysis_a = analyze(prompt_a)

    # analyze prompt B
    analysis_b = analyze(prompt_b)

    score_a = analysis_a["score"]
    score_b = analysis_b["score"]

    improvement = round(score_b - score_a, 1)

    return {

        "success": True,

        "prompt_a": prompt_a,
        "prompt_b": prompt_b,

        "score_a": score_a,
        "score_b": score_b,

        "issues_a": analysis_a["issues"],
        "issues_b": analysis_b["issues"],

        "regression_detected": score_b < score_a,

        "message": (
            f"Prompt B improved the score by {improvement}"
            if improvement > 0
            else "No improvement detected."
        )
    }

# ───────────────── FEEDBACK ─────────────────
@router.post("/feedback")
async def feedback(data: dict):

    prompt = data.get("prompt", "")
    feedback_type = data.get("feedback", "")
    score = data.get("score", None)
    comment = data.get("comment", "")

    print("Feedback received:")
    print({
        "prompt": prompt,
        "feedback": feedback_type,
        "score": score,
        "comment": comment
    })

    return {
        "success": True,
        "message": "Feedback submitted successfully."
    }

# ───────────────── SAVE PROMPT HISTORY ─────────────────
@router.post("/prompt-history")
async def save_prompt_history(data: dict):

    prompt = data.get("prompt", "")
    version = data.get("version", "Unknown")

    # analyze prompt to save score/metrics
    analysis = analyze(prompt)

    success = await save_prompt_version(
        prompt=prompt,
        version=version,
        score=analysis["score"],
        metrics=analysis["metrics"]
    )

    if success:

        return {
            "success": True,
            "message": "Prompt history saved successfully."
        }

    return {
        "success": False,
        "message": "Failed to save prompt history."
    }


# ───────────────── GET PROMPT HISTORY ─────────────────
@router.get("/prompt-history")
async def get_prompt_history(prompt: str = ""):

    history = await list_prompt_versions(prompt)

    cleaned_history = []

    for item in history:

        cleaned_history.append({
            "id": str(item.get("_id")),
            "prompt": item.get("prompt"),
            "version": item.get("version"),
            "score": item.get("score"),
            "timestamp": item.get("created_at")
            })

    return {
        "history": cleaned_history
    }

# ───────────────── DELETE PROMPT HISTORY ─────────────────
@router.delete("/prompt-history/{prompt_id}")
async def delete_history(prompt_id: str):

    success = await delete_prompt_version(prompt_id)

    if success:

        return {
            "success": True,
            "message": "Prompt deleted successfully."
        }

    return {
        "success": False,
        "message": "Failed to delete prompt."
    }