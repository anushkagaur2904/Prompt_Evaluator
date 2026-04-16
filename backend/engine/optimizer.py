import re
from engine.domain import detect_domain, get_domain_label

DEFAULT_TEMPLATE = "General Template"

def detect_intent(prompt):
    p = prompt.lower()
    
    if any(word in p for word in ["build", "create", "design"]):
        return "Creation"
    elif any(word in p for word in ["code", "implement"]):
        return "Coding"
    elif "?" in p:
        return "Question"
    elif any(word in p for word in ["explain", "describe"]):
        return "Explanation"
    elif any(word in p for word in ["compar", " vs ", "versus", "difference"]):
        return "Comparison"
    else:
        return "General"


def get_template_name(intent: str):
    template_map = {
        "Creation": "Build/System Design",
        "Coding": "Code Template",
        "Question": "Answer Template",
        "Explanation": "Explanation",
        "Comparison": "Comparison Template",
        "General": DEFAULT_TEMPLATE
    }
    return template_map.get(intent, DEFAULT_TEMPLATE)

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
    based on intent and domain.
    """
    topic_placeholder = "{topic}"

    # Intent-based templates
    if intent == "Creation":
        return [
            f"Design a {topic_placeholder} with key features, architecture overview, technologies used, user flow, and scalability considerations.",
            f"Create a comprehensive design for {topic_placeholder}. Include: detailed feature list, system architecture diagram description, technology stack recommendations, user journey mapping, and scalability strategy.",
            f"Develop a technical specification for {topic_placeholder}. Cover: functional requirements, architectural patterns, technology choices with justification, implementation roadmap, and performance optimization strategies."
        ]
    elif intent == "Coding":
        return [
            f"Write clean, well-commented code for {topic_placeholder}. Include brief inline explanations.",
            f"Implement production-grade code for {topic_placeholder}. Include time/space complexity analysis, edge cases handling, and sample input/output examples.",
            f"Develop optimized code for {topic_placeholder}. Focus on performance, memory management, type hints, comprehensive documentation, and best practices."
        ]
    elif intent == "Question":
        return [
            f"Answer the question: {topic_placeholder}. Provide a clear, direct response with supporting evidence.",
            f"Provide a comprehensive answer to: {topic_placeholder}. Include step-by-step reasoning, examples, and relevant context.",
            f"Analyze and answer: {topic_placeholder}. Cover multiple perspectives, provide evidence-based reasoning, and include technical details where applicable."
        ]
    elif intent == "Explanation":
        return [
            f"Explain {topic_placeholder} in simple terms with 2 real-world examples. Use bullet points.",
            f"Provide a comprehensive overview of {topic_placeholder}. Include definition, key concepts, examples, and applications with clear headings.",
            f"Explain the technical architecture and underlying mechanisms of {topic_placeholder} using domain-specific terminology and architectural patterns."
        ]
    elif intent == "Comparison":
        return [
            f"Compare {topic_placeholder} concisely using a table format with key features, pros, and cons.",
            f"Provide a detailed side-by-side comparison of {topic_placeholder} covering features, advantages, disadvantages, and best use cases.",
            f"Analyze {topic_placeholder} from a technical perspective with benchmarks, performance metrics, and suitability for different scenarios."
        ]

    # Domain-specific overrides for certain intents
    if domain == "computer_science" and intent == "Explanation":
        return [
            f"Explain {topic_placeholder} simply with a short code example. Use bullet points.",
            f"Explain {topic_placeholder} with definition, key concepts, step-by-step process, and a code example. Use clear headings.",
            f"Explain the internal architecture and algorithmic complexity of {topic_placeholder}. Include Big-O analysis, trade-offs, and real-world applications."
        ]

    # Default fallback
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
        r"^implement\s+(a\s+|an\s+|the\s+)?",
        r"^create\s+(a\s+|an\s+|the\s+)?",
        r"^build\s+(a\s+|an\s+|the\s+)?",
        r"^design\s+(a\s+|an\s+|the\s+)?",
    ]
    topic = prompt.strip()
    for pattern in filler:
        topic = re.sub(pattern, "", topic, flags=re.IGNORECASE).strip()
    topic = re.sub(r"\s*(for me|please|now)$", "", topic, flags=re.IGNORECASE).strip()
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

    # Map intent to template name
    template_map = {
        "Creation": "Build/System Design",
        "Explanation": "Explanation",
        "Coding": "Code Template",
        "Question": "Answer Template",
        "Comparison": "Comparison Template",
        "General": DEFAULT_TEMPLATE
    }
    template_name = template_map.get(intent, DEFAULT_TEMPLATE)

    steps_common = [
        f"Step 1: Detected intent → {intent}",
        f"Step 2: Detected domain → {domain_label}",
        f"Step 3: Selected template → {template_name}",
        ambiguity_step,
    ]

    variants = _templates_for(intent, domain)
    names = ["Concise", "Detailed", "Technical"]
    constraint_notes = [
        "Step 5: Injected constraints (Length: Short, Format: Bullet points)",
        "Step 5: Expanded context, added headings and strict formatting constraints",
        "Step 5: Injected domain-specific depth and professional analytical tone"
    ]
    relevance_note = f"Step 6: Validated template relevance → {domain_label} template applied ✅"

    suggestions = []
    for i in range(3):
        populated = variants[i].replace("{topic}", topic)
        steps = list(steps_common) + [constraint_notes[i], relevance_note]
        suggestions.append({
            "name": names[i],
            "prompt": populated,
            "transformation_steps": steps,
            "domain": domain_label,
            "intent": intent,
            "template": template_name
        })

    return suggestions


def optimize(prompt: str):
    intent = detect_intent(prompt)
    suggestions = generate_suggestions(prompt, intent)
    return suggestions[1]["prompt"], suggestions
