# Mock responses for Groq, DeepSeek, and HuggingFace
# Used as fallback when API keys are not configured

def generate_mock_responses(prompt: str):
    topic = prompt[:40] + "..." if len(prompt) > 40 else prompt

    # 1. Groq (LLaMA): Very fast, moderate detail, slightly informal
    groq = f"""Here's a quick overview of {topic}:

### Key Points
- Point 1: A concise but solid explanation of the core concept.
- Point 2: Covers the essential details without going overboard.
- Point 3: Practical takeaway you can use right away.

That's the gist of it! Let me know if you want me to dive deeper into any part."""

    # 2. Gemini: Concise, well-structured, fast
    gemini = f"""Here is a detailed explanation of {topic}.

**1. Overview**
It involves multiple components working together efficiently.

**2. Key Aspects**
* Focuses on structural integrity and performance.
* Requires careful consideration of edge cases.

In summary, {topic} is highly relevant for modern applications. Let me know if you need more details!"""

    # 3. HuggingFace (Mistral): Variable quality, community model behavior
    huggingface = f"""Regarding {topic}:

{topic} is an interesting subject. Here are some thoughts:
- It has several important aspects worth considering.
- The main idea can be broken down into simpler parts.
- There are different perspectives on this topic.

Overall, this is a topic that benefits from exploration and hands-on experience."""

    return {
        "Groq": groq,
        "Gemini": gemini,
        "HuggingFace": huggingface
    }
