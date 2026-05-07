import re

SAFE_CONTEXTS = [
    "prevent",
    "protection",
    "awareness",
    "education",
    "research",
    "ethical hacking",
    "cybersecurity",
    "defense",
    "how to secure",
]

def detect_injection(prompt: str):

    text = prompt.lower()

    # ✅ allow educational/security contexts
    if any(ctx in text for ctx in SAFE_CONTEXTS):
        return {
            "is_malicious": False,
            "risk_level": "safe",
            "reason": "Educational/security context detected"
        }

    patterns = [

        # ───────── PROMPT INJECTION
        r"ignore previous instructions",
        r"override system",
        r"disregard rules",
        r"forget earlier instructions",
        r"reveal system prompt",

        # ───────── HACKING / MISUSE
        r"\bbypass\b",
        r"\bexploit\b",
        r"\bhack\b",
        r"\bsteal\b",
        r"extract .*password",
        r"get .*credentials",
        r"dump database",
        r"sql injection",
        r"ddos",
        r"ransomware",
        r"keylogger",

        # ───────── DATA EXFILTRATION
        r"reveal confidential",
        r"internal system",
        r"hidden instructions",
        r"private key",

        # ───────── JAILBREAK
        r"act as .*without restrictions",
        r"do anything now",
        r"no rules",
        r"developer mode",
    ]

    for pattern in patterns:

        if re.search(pattern, text):

            return {
                "is_malicious": True,
                "risk_level": "high",
                "reason": f"Detected unsafe pattern: '{pattern}'"
            }

    return {
        "is_malicious": False,
        "risk_level": "low",
        "reason": "No malicious intent detected"
    }