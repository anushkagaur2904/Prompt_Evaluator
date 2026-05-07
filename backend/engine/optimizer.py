from engine.nlp import detect_intent


def generate_versions(prompt: str):

    return {
        "concise": {
            "title": "Concise Version",
            "content": f"""Write a concise response for:

{prompt}

Constraints:
- Keep it brief
- Use simple language
- Focus on main points""",

            "why": [
                "Reduced verbosity",
                "Focused on clarity",
                "Short response format"
            ]
        },

        "detailed": {
            "title": "Detailed Version",
            "content": f"""Provide a detailed response for:

{prompt}

Include:
- Background/context
- Key explanations
- Examples
- Important details""",

            "why": [
                "Expanded explanation",
                "Added supporting details",
                "Improved completeness"
            ]
        },

        "technical": {
            "title": "Technical Version",
            "content": f"""Provide a technical/professional response for:

{prompt}

Requirements:
- Precise terminology
- Structured format
- Analytical explanation""",

            "why": [
                "Improved precision",
                "Added technical depth",
                "Professional structure"
            ]
        }
    }


def optimize(prompt: str):

    intent = detect_intent(prompt)

    if intent == "email":
        main_suggestion = """
- Add a subject line
- Mention reason clearly
- Maintain professional tone
- Add polite closing
"""

    elif intent == "explanation":
        main_suggestion = """
- Add definitions
- Include examples
- Structure concepts clearly
- Add applications/use cases
"""

    elif intent == "code":
        main_suggestion = """
- Mention language/framework
- Include edge cases
- Request comments/documentation
- Define expected output
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