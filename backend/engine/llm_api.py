import os
import time
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")


# ─────────────────────────────────────────────
# API STATUS
# ─────────────────────────────────────────────
def get_api_status():
    return {
        "Groq": "connected" if GROQ_API_KEY else "missing_key",
        "Gemini": "connected" if GOOGLE_API_KEY else "missing_key",
        "HuggingFace": "connected" if HUGGINGFACE_API_KEY else "missing_key",
    }


# ─────────────────────────────────────────────
# GROQ
# ─────────────────────────────────────────────
def _call_groq(prompt):
    from groq import Groq

    client = Groq(api_key=GROQ_API_KEY)

    start = time.time()

    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=400
    )

    latency = int((time.time() - start) * 1000)

    text = resp.choices[0].message.content.strip()

    return text, latency


# ─────────────────────────────────────────────
# GEMINI
# ─────────────────────────────────────────────
def _call_gemini(prompt):

    import google.generativeai as genai

    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel("gemini-flash-latest")

    start = time.time()

    response = model.generate_content(prompt)

    latency = int((time.time() - start) * 1000)

    try:
        text = response.text.strip()

    except:
        try:
            text = response.candidates[0].content.parts[0].text.strip()
        except:
            text = "Unable to generate response."

    return text, latency


# ─────────────────────────────────────────────
# HUGGINGFACE
# ─────────────────────────────────────────────
def _call_hf(prompt):
    from huggingface_hub import InferenceClient

    client = InferenceClient(api_key=HUGGINGFACE_API_KEY)

    start = time.time()

    resp = client.chat_completion(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=400,
        temperature=0.7
    )

    latency = int((time.time() - start) * 1000)

    text = resp.choices[0].message.content.strip()

    return text, latency


# ─────────────────────────────────────────────
# RESPONSE QUALITY SCORING
# ─────────────────────────────────────────────
def evaluate_response(text: str, prompt: str = ""):

    if not text:
        return 2

    lower = text.lower()

    # ───────────────── ERRORS
    error_patterns = [
        "error generating",
        "quota",
        "rate limit",
        "api key",
        "failed",
        "cannot assist",
        "unable to",
        "no module named",
    ]

    if any(p in lower for p in error_patterns):
        return 2

    score = 5

    words = text.split()
    word_count = len(words)

    # ───────────────── RESPONSE LENGTH
    if word_count < 25:
        score -= 2

    elif word_count < 50:
        score -= 1

    elif 80 <= word_count <= 220:
        score += 1

    # ───────────────── STRUCTURE
    structure_keywords = [
        "summary",
        "example",
        "steps",
        "conclusion",
        "subject",
        "regards",
    ]

    structure_hits = sum(
        1 for k in structure_keywords
        if k in lower
    )

    if structure_hits >= 2:
        score += 1

    # ───────────────── FORMAT QUALITY
    if "\n" in text:
        score += 0.5

    if ":" in text:
        score += 0.5

    # ───────────────── PROMPT RELEVANCE
    if prompt:

        prompt_words = [
            w.lower()
            for w in prompt.split()
            if len(w) > 4
        ]

        response_words = lower.split()

        overlap = sum(
            1 for w in prompt_words
            if w in response_words
        )

        relevance_ratio = overlap / max(len(prompt_words), 1)

        if relevance_ratio > 0.7:
            score += 1

        elif relevance_ratio < 0.3:
            score -= 2

    # ───────────────── REPETITION CHECK
    unique_ratio = len(set(words)) / max(word_count, 1)

    if unique_ratio < 0.45:
        score -= 2

    elif unique_ratio < 0.6:
        score -= 1

    # ───────────────── GENERIC AI DETECTION
    generic_phrases = [
        "here is a detailed explanation",
        "it is important to note",
        "various aspects",
        "in conclusion",
        "this can be useful",
    ]

    generic_hits = sum(
        1 for p in generic_phrases
        if p in lower
    )

    if generic_hits >= 2:
        score -= 1

    # ───────────────── OVERLY VERBOSE
    if word_count > 400:
        score -= 1

    return max(1, min(round(score), 10))

# ─────────────────────────────────────────────
# MODEL COMPARISON
# ─────────────────────────────────────────────
def get_real_llm_responses(prompt):

    results = {}

    callers = {
        "Groq": _call_groq,
        "Gemini": _call_gemini,
        "HuggingFace": _call_hf,
    }

    for name, func in callers.items():

        try:
            text, latency = func(prompt)

            #score = evaluate_response(text)
            score = evaluate_response(text, prompt)
            
            results[name] = {
                "text": text,
                "latency_ms": latency,
                "score": score,
                "source": "real"
            }

        except Exception as e:

            print(f"{name} ERROR:", e)

            results[name] = {
                "text": f"Error generating response: {str(e)}",
                "latency_ms": 0,
                "score": 2,
                "source": "error",
                "error": str(e)
            }

    # ─────────────────────────────────────────────
    # SMART BEST MODEL SELECTION
    # ─────────────────────────────────────────────

    best_model = None
    best_rank = -999

    for model_name, item in results.items():

        score = float(item.get("score", 0))
        latency = item.get("latency_ms", 99999)

        text = item.get("text", "").lower()

        # strong penalty for failed/error responses
        if "error" in text:
            score -= 5

        # VERY SMALL latency effect
        latency_penalty = latency / 50000

        final_rank = score - latency_penalty

        if final_rank > best_rank:
            best_rank = final_rank
            best_model = model_name

    return {
        "results": results,
        "best_model": best_model
    }