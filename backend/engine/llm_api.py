import os
from dotenv import load_dotenv
import time
import requests

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")

def _is_valid(key: str, placeholder: str) -> bool:
    return bool(key) and key != placeholder

def _check_status():
    return {
        "Groq":        "connected" if _is_valid(GROQ_API_KEY, "gsk_") else "missing_key",
        "Gemini":      "connected" if _is_valid(GOOGLE_API_KEY, "your_google_gemini_key_here") else "missing_key",
        "HuggingFace": "connected" if _is_valid(HUGGINGFACE_API_KEY, "hf_") else "missing_key",
    }

def get_api_status():
    return _check_status()

# ─── Groq ────────────────────────────────────────────────────────────────────
def _call_groq(prompt: str):
    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)
    start = time.time()
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    latency_ms = round((time.time() - start) * 1000)
    return resp.choices[0].message.content.strip(), latency_ms

# ─── Gemini ──────────────────────────────────────────────────────────────────
def _call_gemini(prompt: str):
    from google import genai
    client = genai.Client(api_key=GOOGLE_API_KEY)
    start = time.time()
    resp = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    latency_ms = round((time.time() - start) * 1000)
    return resp.text.strip(), latency_ms

# ─── Hugging Face Inference API (huggingface_hub) ─────────────────────────────
def _call_huggingface(prompt: str):
    from huggingface_hub import InferenceClient
    client = InferenceClient(api_key=HUGGINGFACE_API_KEY)
    start = time.time()
    resp = client.chat_completion(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    latency_ms = round((time.time() - start) * 1000)
    return resp.choices[0].message.content.strip(), latency_ms


def get_real_llm_responses(prompt: str):
    """
    Calls real APIs for Groq, DeepSeek, HuggingFace.
    Falls back to mock gracefully if key is missing or call fails.
    """
    from engine.llm_mock import generate_mock_responses
    status = _check_status()
    mock_responses = generate_mock_responses(prompt)

    results = {}
    callers = {
        "Groq": _call_groq,
        "Gemini": _call_gemini,
        "HuggingFace": _call_huggingface,
    }

    for model_name, caller in callers.items():
        if status[model_name] == "connected":
            try:
                text, ms = caller(prompt)
                results[model_name] = {"text": text, "latency_ms": ms, "source": "real"}
            except Exception as e:
                results[model_name] = {"text": mock_responses[model_name], "latency_ms": 0, "source": "mock", "error": str(e)}
        else:
            results[model_name] = {"text": mock_responses[model_name], "latency_ms": 0, "source": "mock", "error": "API key not configured"}

    return results
