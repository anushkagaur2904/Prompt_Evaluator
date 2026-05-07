import re


# ─────────────────────────────────────────────
# INTENT DETECTION
# ─────────────────────────────────────────────
def detect_intent(prompt: str):

    p = prompt.lower()

    if any(k in p for k in [
        "explain",
        "define",
        "describe",
        "teach",
        "what is"
    ]):
        return "explanation"

    if any(k in p for k in [
        "write",
        "generate",
        "create",
        "draft"
    ]):

        if "email" in p:
            return "email"

        if "code" in p:
            return "code"

        if "essay" in p:
            return "essay"

        return "generation"

    if any(k in p for k in [
        "compare",
        "difference",
        "vs"
    ]):
        return "comparison"

    if any(k in p for k in [
        "summarize",
        "summary"
    ]):
        return "summary"

    return "general"


# ─────────────────────────────────────────────
# MAIN PROMPT EVALUATION
# ─────────────────────────────────────────────
def evaluate_prompt(prompt: str):

    words = prompt.split()
    length = len(words)

    prompt_lower = prompt.lower()

    # ───────── CLARITY
    clarity = 0.7

    if length >= 8:
        clarity += 0.1

    if any(x in prompt_lower for x in [
        "explain",
        "write",
        "generate",
        "create",
        "summarize",
        "compare"
    ]):
        clarity += 0.1

    if "," in prompt or "." in prompt:
        clarity += 0.1

    clarity = min(1.0, clarity)

    # ───────── SPECIFICITY

    specificity_terms = [
        w for w in words
        if len(w) > 6
        ]

    constraint_terms = [
        "bullet",
        "steps",
        "json",
        "table",
        "formal",
        "technical",
        "examples",
        "simple",
        "detailed",
        "professional"
    ]

    constraint_bonus = sum(
        1 for t in constraint_terms
        if t in prompt_lower
    )

    specificity = (
        (len(specificity_terms) * 0.08) +
        (constraint_bonus * 0.12)
    )

    # short prompts should not get huge specificity
    if length < 6:
        specificity *= 0.5

    specificity = min(1.0, max(0.2, specificity))

    

    # ───────── CONTEXT
    context = 0.5

    context_keywords = [
        "because",
        "for",
        "due to",
        "using",
        "with",
        "including",
        "regarding",
        "about"
    ]

    if any(k in prompt_lower for k in context_keywords):
        context += 0.3

    if length > 15:
        context += 0.2

    context = min(1.0, context)

    # ───────── INSTRUCTION QUALITY
    instruction = 0.5

    instruction_keywords = [
        "explain",
        "write",
        "generate",
        "analyze",
        "compare",
        "summarize",
        "list",
        "describe"
    ]

    if any(v in prompt_lower for v in instruction_keywords):
        instruction += 0.4

    formatting_words = [
        "bullet",
        "steps",
        "table",
        "json",
        "format"
    ]

    if any(v in prompt_lower for v in formatting_words):
        instruction += 0.1

    instruction = min(1.0, instruction)

    # ───────── AMBIGUITY

    ambiguity = 0.0

    vague_words = [
        "thing",
        "stuff",
        "something",
        "anything",
        "whatever",
        "etc",
        "and more"
    ]

    vague_count = sum(
        1 for w in vague_words
        if w in prompt_lower
    )

    ambiguity += vague_count * 0.15

    # vague / underspecified short prompts
    if length <= 3:
        ambiguity += 0.35

    elif length <= 6:
        ambiguity += 0.2

    # missing constraints
    constraint_words = [
        "steps",
        "examples",
        "bullet",
        "table",
        "json",
        "beginner",
        "advanced",
        "professional",
        "short",
        "detailed",
    ]

    if not any(w in prompt_lower for w in constraint_words):
        ambiguity += 0.15

    ambiguity = min(1.0, round(ambiguity, 2))

    # ───────── KEYWORD RELEVANCE
    important_words = [
        w.lower()
        for w in words
        if len(w) > 4
    ]

    unique_ratio = len(set(important_words)) / max(len(important_words), 1)

    keyword_relevance = min(1.0, unique_ratio)

    # ───────── FORMAT VALIDITY
    format_valid = 0.7

    if any(x in prompt_lower for x in [
        "bullet",
        "json",
        "steps",
        "table",
        "paragraph"
    ]):
        format_valid = 1.0

    # ───────── CONCISENESS
    conciseness = 1.0

    if length > 120:
        conciseness = 0.7

    if length > 250:
        conciseness = 0.5

    # ─────────────────────────────────────────
    # FINAL SCORES
    # ─────────────────────────────────────────
    scores = {
        "clarity": round(clarity, 2),
        "specificity": round(specificity, 2),
        "context": round(context, 2),
        "instruction": round(instruction, 2),
        "ambiguity": round(ambiguity, 2),
        "keyword_relevance": round(keyword_relevance, 2),
        "format_valid": round(format_valid, 2),
        "conciseness": round(conciseness, 2)
    }

    final_score = (
        clarity * 0.18 +
        specificity * 0.18 +
        context * 0.16 +
        instruction * 0.18 +
        keyword_relevance * 0.08 +
        format_valid * 0.12 +
        conciseness * 0.08 -
        ambiguity * 0.25
    )

    final_score = max(0, min(10, round(final_score * 10, 1)))

    return final_score, scores


# ─────────────────────────────────────────────
# ISSUE DETECTION
# ─────────────────────────────────────────────
def detect_issues(prompt: str, scores: dict):

    issues = []

    if scores["instruction"] < 0.6:
        issues.append(
            "Instruction could be clearer about expected output."
        )

    if scores["context"] < 0.5:
        issues.append(
            "Add more context or background details."
        )

    if scores["specificity"] < 0.45:
        issues.append(
            "Use more specific keywords or constraints."
        )

    if scores["clarity"] < 0.6:
        issues.append(
            "Simplify or restructure the wording."
        )

    if scores["ambiguity"] > 0.3:
        issues.append(
            "Prompt contains vague or ambiguous wording."
        )

    if not issues:
        issues.append(
            "Prompt is well-structured with good clarity."
        )

    return issues


# ─────────────────────────────────────────────
# MAIN ANALYZE FUNCTION
# ─────────────────────────────────────────────
def analyze(prompt: str):

    score, scores = evaluate_prompt(prompt)

    issues = detect_issues(prompt, scores)

    intent = detect_intent(prompt)

    prediction = "Excellent"

    if score < 8:
        prediction = "Good"

    if score < 6:
        prediction = "Average"

    if score < 4:
        prediction = "Weak"

    return {
        "score": score,
        "metrics": scores,
        "issues": issues,
        "intent": intent,
        "prediction": prediction
    }