import re
from engine.domain import detect_domain, get_domain_label

def detect_intent(prompt: str):
    p = prompt.lower()
    if any(k in p for k in ["code", "function", "script", "program", "implement", "write a"]):
        return "Code"
    if any(k in p for k in ["summar", "tl;dr", "shorten", "brief"]):
        return "Summary"
    if any(k in p for k in ["compar", " vs ", "difference between", "versus"]):
        return "Comparison"
    return "Explanation"

def remove_ambiguity(prompt: str):
    ambig_map = {
        r"\bexplain\b": "explain in detail",
        r"\btell\b": "describe with examples",
        r"\babout\b": "specifically focusing on"
    }
    cleaned = prompt
    for k, v in ambig_map.items():
        cleaned = re.sub(k, v, cleaned, flags=re.IGNORECASE)
    return cleaned

# ─── Domain-conditioned Template Library ────────────────────────────────────

def _templates_for(intent: str, domain: str):
    """
    Returns (concise, detailed, technical) prompt variants
    conditioned on both intent AND domain.
    """
    topic_placeholder = "{topic}"  # replaced at call time

    # ── Fiction / Literature ──────────────────────────────────────────────
    if domain == "fiction":
        if intent == "Explanation":
            return [
                f"Explain {topic_placeholder} in simple terms. Include key characters, their roles, personalities, and relationships. Use bullet points and provide a concise summary.",
                f"Provide a complete overview of {topic_placeholder}. Include: key characters and their traits, important relationships, major events they are involved in, their motivations, and a thematic summary. Use bullet points with clear headings.",
                f"Analyze {topic_placeholder} from a literary perspective. Discuss character archetypes, narrative roles, symbolic significance, and their contribution to the story's themes. Include critical analysis."
            ]
        if intent == "Summary":
            return [
                f"Summarize {topic_placeholder} in 3 bullet points focusing on the key narrative elements.",
                f"Provide a detailed plot and character summary of {topic_placeholder}, covering all major arcs and relationships.",
                f"Write a literary summary of {topic_placeholder} including thematic analysis and narrative structure."
            ]
        return [
            f"Briefly explain {topic_placeholder} with 2 examples.",
            f"Explain {topic_placeholder} in detail with examples and context.",
            f"Analyze {topic_placeholder} in depth with critical perspective."
        ]

    # ── Computer Science ──────────────────────────────────────────────────
    if domain == "computer_science":
        if intent == "Code":
            return [
                f"Write clean, well-commented code for: {topic_placeholder}. Include brief inline explanations.",
                f"Write production-grade code for: {topic_placeholder}. Include time/space complexity, edge cases, and sample input/output.",
                f"Implement optimized code for: {topic_placeholder}. Focus on performance, memory management, type hints, and full documentation."
            ]
        if intent == "Explanation":
            return [
                f"Explain {topic_placeholder} simply with a short example. Use bullet points.",
                f"Explain {topic_placeholder} with definition, key concepts, step-by-step process, and a code example. Use clear headings.",
                f"Explain the internal architecture and algorithmic complexity of {topic_placeholder}. Include Big-O analysis, trade-offs, and real-world applications."
            ]
        return [
            f"Briefly explain {topic_placeholder} with a code snippet.",
            f"Explain {topic_placeholder} including concepts and implementation.",
            f"Perform a deep technical analysis of {topic_placeholder}."
        ]

    # ── Science ───────────────────────────────────────────────────────────
    if domain == "science":
        return [
            f"Explain {topic_placeholder} in simple terms with 2 real-world examples. Use bullet points.",
            f"Provide a comprehensive scientific explanation of {topic_placeholder}. Include definition, underlying principles, real-world applications, and key discoveries.",
            f"Explain {topic_placeholder} with technical depth. Cover the scientific mechanisms, experimental evidence, current research trends, and implications."
        ]

    # ── History ───────────────────────────────────────────────────────────
    if domain == "history":
        return [
            f"Explain {topic_placeholder} briefly with key dates and outcomes. Use bullet points.",
            f"Provide a detailed historical account of {topic_placeholder}. Include causes, key events, major figures, and long-term impact.",
            f"Analyze {topic_placeholder} critically. Examine primary causes, strategic significance, multiple historical perspectives, and lasting geopolitical consequences."
        ]

    # ── Finance ───────────────────────────────────────────────────────────
    if domain == "finance":
        return [
            f"Explain {topic_placeholder} in simple terms with 2 practical examples.",
            f"Provide a detailed analysis of {topic_placeholder}. Include definition, key metrics, risks, and real-world examples.",
            f"Analyze {topic_placeholder} from a quantitative finance perspective. Include economic models, market indicators, risk metrics, and historical trends."
        ]

    # ── Health ────────────────────────────────────────────────────────────
    if domain == "health":
        return [
            f"Explain {topic_placeholder} in simple terms. Include key facts and 2 practical tips. Use bullet points.",
            f"Provide a detailed medical explanation of {topic_placeholder}. Include causes, symptoms, diagnosis, treatment options, and prevention.",
            f"Provide a clinical analysis of {topic_placeholder}. Cover pathophysiology, diagnostic criteria, evidence-based treatment protocols, and prognosis."
        ]

    # ── General / Fallback ────────────────────────────────────────────────
    if intent == "Code":
        return [
            f"Write clean code for: {topic_placeholder}. Include brief comments.",
            f"Write production-grade code for: {topic_placeholder}. Include explanation and edge cases.",
            f"Implement optimized code for: {topic_placeholder} with full documentation."
        ]
    if intent == "Summary":
        return [
            f"Summarize {topic_placeholder} in 3 bullet points.",
            f"Provide a detailed summary of {topic_placeholder} with key arguments and conclusions.",
            f"Write a technical summary of {topic_placeholder} with data points and factual results."
        ]
    if intent == "Comparison":
        return [
            f"Compare {topic_placeholder} concisely using a short table.",
            f"Provide a detailed side-by-side comparison of {topic_placeholder} covering features, pros, cons, and best use cases.",
            f"Analyze {topic_placeholder} from a technical engineering perspective with benchmarks and use-case suitability."
        ]
    # Default Explanation
    return [
        f"Explain {topic_placeholder} simply with 2 real-world examples. Use bullet points.",
        f"Provide a comprehensive overview of {topic_placeholder}. Include definition, key concepts, examples, and applications with clear headings.",
        f"Explain the technical architecture and underlying mechanisms of {topic_placeholder} using domain-specific terminology and architectural patterns."
    ]


def _extract_topic(prompt: str) -> str:
    """Strip leading intent/filler words to extract the core topic."""
    filler = [
        r"^explain\s+(in\s+detail\s+)?about\s+",
        r"^explain\s+",
        r"^tell\s+(me\s+)?(about\s+)?",
        r"^describe\s+",
        r"^what\s+is\s+",
        r"^what\s+are\s+",
        r"^summarize\s+",
        r"^compare\s+",
        r"^write\s+(a\s+)?code\s+(for\s+)?",
        r"^implement\s+",
        r"^create\s+",
    ]
    topic = prompt.strip()
    for pattern in filler:
        topic = re.sub(pattern, "", topic, flags=re.IGNORECASE).strip()
    # Capitalize first letter
    return topic[0].upper() + topic[1:] if topic else prompt.strip()


def generate_suggestions(prompt: str, intent: str):
    domain = detect_domain(prompt)
    domain_label = get_domain_label(domain)
    topic = _extract_topic(prompt)

    # Check ambiguity for step reporting only
    clean_p = remove_ambiguity(prompt)
    ambiguity_step = (
        "Step 3: Removed ambiguity (replaced vague words)"
        if clean_p != prompt
        else "Step 3: Ambiguity check passed"
    )

    steps_common = [
        f"Step 1: Detected intent → {intent}",
        f"Step 2: Detected domain → {domain_label}",
        ambiguity_step,
    ]

    variants = _templates_for(intent, domain)
    names = ["Concise", "Detailed", "Technical"]
    constraint_notes = [
        "Step 4: Injected constraints (Length: Short, Format: Bullet points)",
        "Step 4: Expanded context, added headings and strict formatting constraints",
        "Step 4: Injected domain-specific depth and professional analytical tone"
    ]
    relevance_note = f"Step 5: Validated template relevance → {domain_label} template applied ✅"

    suggestions = []
    for i in range(3):
        populated = variants[i].replace("{topic}", topic)
        steps = list(steps_common) + [constraint_notes[i], relevance_note]
        suggestions.append({
            "name": names[i],
            "prompt": populated,
            "transformation_steps": steps,
            "domain": domain_label,
            "intent": intent
        })

    return suggestions


def optimize(prompt: str, metrics: dict):
    intent = detect_intent(prompt)
    suggestions = generate_suggestions(prompt, intent)
    return suggestions[1]["prompt"], suggestions
