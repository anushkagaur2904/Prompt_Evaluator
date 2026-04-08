import re
try:
    import textstat
except ImportError:
    textstat = None

def calculate_clarity(text):
    if not text: return 0.0
    grammar_errors = len(re.findall(r"\b(is am|are is|does not has|their is)\b", text, re.IGNORECASE))
    if textstat:
        try:
            readability = textstat.flesch_reading_ease(text)
            r_norm = max(0, min(100, readability)) / 100.0
        except:
            r_norm = 0.5
    else:
        r_norm = 0.5
    return (1 / (1 + grammar_errors)) * r_norm

def calculate_specificity(text):
    words = text.split()
    total_words = len(words)
    if total_words == 0: return 0.0
    domain_keywords = ["ai", "api", "python", "javascript", "code", "database", "sql", "explain", "analyze", "evaluate", "optimize", "system", "architecture", "data"]
    matched = sum(1 for w in words if w.lower() in domain_keywords)
    return min(1.0, (matched / total_words) * 3)

def calculate_context(text):
    words = len(text.split())
    if words < 5: return 0.2
    if words < 15: return 0.5
    if words < 30: return 0.8
    return 1.0

def calculate_instruction(text):
    action_verbs = ["write", "explain", "create", "build", "analyze", "evaluate", "summarize", "list", "describe", "show"]
    matched = sum(1 for v in action_verbs if v in text.lower())
    return min(1.0, matched / 2.0)

def calculate_ambiguity(text):
    ambig = ["stuff", "things", "something", "sometimes", "maybe", "probably"]
    words = text.split()
    if not words: return 0.0
    matched = sum(1 for w in words if w.lower() in ambig)
    return min(1.0, matched / len(words))

def calculate_overall_score(c, s, k, u, a):
    w1, w2, w3, w4, w5 = 0.25, 0.20, 0.20, 0.20, -0.15
    score = (w1 * c) + (w2 * s) + (w3 * k) + (w4 * u) + (w5 * a)
    max_possible = 0.85
    final_score = max(0.0, min(10.0, (score / max_possible) * 10))
    return final_score

def analyze(prompt: str):
    c = calculate_clarity(prompt)
    s = calculate_specificity(prompt)
    k = calculate_context(prompt)
    u = calculate_instruction(prompt)
    a = calculate_ambiguity(prompt)
    score = calculate_overall_score(c, s, k, u, a)
    
    issues = []
    if c < 0.4: issues.append("Low clarity. Try shortening sentences or simplifying language.")
    if s < 0.3: issues.append("Too vague. Add domain-specific keywords.")
    if k < 0.4: issues.append("Missing context. Provide more background details.")
    if u < 0.5: issues.append("Unclear instructions. Start with action verbs (e.g., 'Evaluate').")
    if a > 0.1: issues.append("High ambiguity. Remove vague words ('stuff', 'things').")
    
    if len(issues) == 0 and score < 9:
        issues.append("Prompt is good but lacks structural constraints (e.g., word limit).")
        
    return {
        "score": round(score, 1),
        "metrics": {
            "clarity": round(c, 2),
            "specificity": round(s, 2),
            "context": round(k, 2),
            "instruction": round(u, 2),
            "ambiguity": round(a, 2)
        },
        "issues": issues,
        "response_prediction": {
            "type": "Code" if "code" in prompt.lower() or "function" in prompt.lower() else "Explanation",
            "confidence": 0.85
        }
    }
