def detect_injection(prompt: str) -> dict:
    patterns = [
        "ignore previous instructions",
        "reveal system prompt",
        "bypass safety",
        "act as system",
        "act as admin"
    ]
    
    lower_prompt = prompt.lower()
    for p in patterns:
        if p in lower_prompt:
            return {
                "is_malicious": True,
                "reason": "Prompt injection detected"
            }
            
    return {
        "is_malicious": False,
        "reason": ""
    }
