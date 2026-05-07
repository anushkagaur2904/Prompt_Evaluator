from engine.nlp import detect_intent
import re


# ───────────────── KEYWORD EXTRACTION ─────────────────
def extract_keywords(prompt: str):

    words = re.findall(r"\b[a-zA-Z]{5,}\b", prompt)

    stopwords = {
        "explain",
        "describe",
        "provide",
        "using",
        "include",
        "write",
        "create",
        "generate",
        "about",
        "which",
        "their",
        "there",
        "these",
        "those",
        "would",
        "should",
        "could",
        "simple",
        "language",
        "detail",
        "detailed"
    }

    keywords = []

    for word in words:
        if word.lower() not in stopwords:
            keywords.append(word)

    return list(dict.fromkeys(keywords[:8]))


# ───────────────── PROMPT TYPE DETECTION ─────────────────
def detect_prompt_type(prompt: str):

    p = prompt.lower()

    if any(k in p for k in [
        "email",
        "mail",
        "letter"
    ]):
        return "email"

    if any(k in p for k in [
        "code",
        "python",
        "java",
        "api",
        "algorithm",
        "debug",
        "program"
    ]):
        return "technical"

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

    if any(k in p for k in [
        "explain",
        "describe",
        "definition",
        "what is"
    ]):
        return "educational"

    return "general"


# ───────────────── VERSION GENERATOR ─────────────────
def generate_versions(prompt: str):

    prompt_type = detect_prompt_type(prompt)

    keywords = extract_keywords(prompt)

    keyword_text = ", ".join(keywords)

    # ───────── CONCISE VERSION
    if prompt_type == "email":

        concise_content = f"""Write a short professional email.

Task:
{prompt}

Requirements:
- Keep response concise
- Maintain polite tone
- Use clear subject line
- Avoid unnecessary details"""

    elif prompt_type == "technical":

        concise_content = f"""Provide a concise technical explanation.

Topic:
{prompt}

Requirements:
- Focus on core concepts
- Use technical accuracy
- Keep explanation short
- Mention key technologies

Keywords:
{keyword_text}"""

    elif prompt_type == "educational":

        concise_content = f"""Explain the topic briefly in simple language.

Topic:
{prompt}

Requirements:
- Beginner-friendly explanation
- Use short bullet points
- Focus on important concepts
- Avoid unnecessary complexity"""

    elif prompt_type == "comparison":

        concise_content = f"""Provide a short comparison for:

{prompt}

Requirements:
- Mention key differences
- Use concise points
- Highlight practical usage"""

    else:

        concise_content = f"""Write a concise response for:

{prompt}

Constraints:
- Keep it brief
- Use simple language
- Focus on main points"""

    # ───────── DETAILED VERSION
    if prompt_type == "email":

        detailed_content = f"""Write a detailed professional email.

Task:
{prompt}

Include:
- Professional greeting
- Clear explanation
- Supporting context
- Polite closing
- Proper formatting"""

    elif prompt_type == "technical":

        detailed_content = f"""Provide a detailed technical explanation.

Topic:
{prompt}

Include:
- Architecture/workflow
- Key components
- Advantages and limitations
- Real-world examples
- Step-by-step explanation

Technical topics:
{keyword_text}"""

    elif prompt_type == "educational":

        detailed_content = f"""Provide a detailed educational explanation.

Topic:
{prompt}

Include:
- Definitions
- Core concepts
- Examples
- Real-world applications
- Structured bullet points"""

    elif prompt_type == "comparison":

        detailed_content = f"""Provide a detailed comparison.

Task:
{prompt}

Include:
- Similarities
- Differences
- Advantages/disadvantages
- Practical applications
- Summary conclusion"""

    else:

        detailed_content = f"""Provide a detailed response for:

{prompt}

Include:
- Background/context
- Key explanations
- Examples
- Important details"""

    # ───────── TECHNICAL VERSION
    if prompt_type == "technical":

        technical_content = f"""Provide an advanced technical explanation.

Topic:
{prompt}

Requirements:
- Use precise terminology
- Include implementation details
- Mention optimization techniques
- Discuss scalability/performance
- Include edge cases

Technical keywords:
{keyword_text}"""

    elif prompt_type == "educational":

        technical_content = f"""Provide a technically accurate explanation.

Topic:
{prompt}

Requirements:
- Explain underlying mechanisms
- Use structured formatting
- Include technical terminology
- Mention practical implementations"""

    elif prompt_type == "email":

        technical_content = f"""Write a highly professional business email.

Task:
{prompt}

Requirements:
- Formal business tone
- Professional structure
- Clear communication
- Concise and respectful wording"""

    else:

        technical_content = f"""Provide a technical/professional response for:

{prompt}

Requirements:
- Precise terminology
- Structured format
- Analytical explanation
- Include implementation insights"""

    return {
        "concise": {
            "title": "Concise Version",
            "content": concise_content,
            "why": [
                "Reduced verbosity",
                "Focused on clarity",
                "Short response format"
            ]
        },

        "detailed": {
            "title": "Detailed Version",
            "content": detailed_content,
            "why": [
                "Expanded explanation",
                "Added supporting details",
                "Improved completeness"
            ]
        },

        "technical": {
            "title": "Technical Version",
            "content": technical_content,
            "why": [
                "Improved precision",
                "Added technical depth",
                "Professional structure"
            ]
        }
    }


# ───────────────── MAIN OPTIMIZER ─────────────────
def optimize(prompt: str):

    intent = detect_intent(prompt)

    if intent == "email":

        main_suggestion = """
- Add a clear subject line
- Mention the reason professionally
- Maintain formal tone
- Add polite opening and closing
"""

    elif intent == "explanation":

        main_suggestion = """
- Add definitions
- Include examples
- Structure concepts clearly
- Mention practical applications
"""

    elif intent == "code":

        main_suggestion = """
- Mention language/framework
- Define expected output
- Include edge cases
- Request comments/documentation
"""

    elif intent == "comparison":

        main_suggestion = """
- Mention comparison criteria
- Include similarities and differences
- Use structured format/table
- Add conclusion
"""

    else:

        main_suggestion = """
- Improve clarity
- Add structure
- Include constraints
- Specify expected output
"""

    return {
        "original_prompt": prompt,
        "suggestions": generate_versions(prompt),
        "main_suggestion": main_suggestion
    }