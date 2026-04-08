import re

def analyze_verbosity(text: str, expected_words=100):
    words = text.split()
    total = len(words)
    v_score = total / expected_words
    return min(1.0, v_score)

def analyze_structure(text: str):
    points = 0
    if "-" in text or "*" in text: points += 0.3
    if "\n\n" in text: points += 0.3
    if re.search(r"^\d+\.", text, re.MULTILINE): points += 0.2
    if "#" in text: points += 0.2
    return min(1.0, points)

def analyze_creativity(text: str):
    words = [w.lower() for w in re.findall(r'\b\w+\b', text)]
    if not words: return 0.0
    unique = set(words)
    creativity = len(unique) / len(words)
    # usually ranges between 0.3 to 0.7. Scale it.
    score = (creativity - 0.3) / 0.4
    return max(0.0, min(1.0, score))

def analyze_safety(text: str):
    safety_terms = ["cannot", "sorry", "refuse", "safety", "policy", "guidelines", "violate", "illegal", "harmful"]
    count = sum(1 for term in safety_terms if term in text.lower())
    # 1.0 means highly safe/restrictive, 0.0 means unconstrained
    return min(1.0, count * 0.33)

def generate_behavior_labels(v, s, c, saf):
    labels = []
    if v > 0.8: labels.append("Detailed & Verbose")
    elif v < 0.4: labels.append("Concise")
    else: labels.append("Balanced Length")
    
    if s > 0.7: labels.append("Highly Structured")
    elif s < 0.3: labels.append("Informal / Unstructured")
    
    if saf > 0.5: labels.append("Cautious / Safe")
    
    if c > 0.7: labels.append("High Lexical Diversity")
    
    if not labels:
        labels.append("Standard / Predictable")
    
    return labels

def analyze_behavior(model_name: str, response_text: str):
    v = analyze_verbosity(response_text)
    s = analyze_structure(response_text)
    c = analyze_creativity(response_text)
    saf = analyze_safety(response_text)
    
    stats = {
        "verbosity": round(v, 2),
        "structure": round(s, 2),
        "creativity": round(c, 2),
        "safety": round(saf, 2)
    }
    
    labels = generate_behavior_labels(v, s, c, saf)
    
    return stats, labels
