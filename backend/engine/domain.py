"""
Domain Detection Engine
Classifies the topic/domain of a prompt so template selection is domain-aware.
"""

DOMAIN_RULES = {
    "fiction": [
        "harry potter", "lord of the rings", "narnia", "game of thrones",
        "hobbit", "twilight", "hunger games", "percy jackson", "sherlock",
        "characters", "wizard", "dragon", "magic", "fantasy", "novel",
        "book", "character", "protagonist", "villain", "plot", "story",
        "author", "fiction", "literature", "poem", "poet"
    ],
    "science": [
        "photosynthesis", "evolution", "cell", "dna", "physics", "chemistry",
        "biology", "quantum", "gravity", "relativity", "atom", "molecule",
        "ecosystem", "organisms", "species", "genetics", "newton", "einstein",
        "scientific", "experiment", "hypothesis", "theorem"
    ],
    "computer_science": [
        "algorithm", "sorting", "binary search", "tree", "graph", "linked list",
        "code", "function", "python", "javascript", "api", "database", "sql",
        "machine learning", "neural network", "deep learning", "data structure",
        "programming", "software", "server", "deployment", "docker", "kubernetes",
        "stack", "queue", "recursion", "complexity", "array", "object"
    ],
    "history": [
        "world war", "revolution", "independence", "empire", "civilization",
        "ancient", "medieval", "renaissance", "colonization", "dynasty",
        "historical", "war of", "battle", "king", "queen", "president",
        "century", "decade", "timeline", "era", "colony", "treaty"
    ],
    "finance": [
        "stock", "market", "investment", "portfolio", "economy", "gdp",
        "inflation", "interest rate", "budget", "tax", "revenue", "profit",
        "loss", "crypto", "bitcoin", "trading", "shares", "mutual fund", "ipo"
    ],
    "health": [
        "disease", "symptom", "medicine", "doctor", "treatment", "diet",
        "exercise", "mental health", "nutrition", "vaccine", "virus", "health",
        "cancer", "diabetes", "heart", "surgery", "therapy", "hospital"
    ],
    "general": []  # fallback
}

def detect_domain(prompt: str) -> str:
    p = prompt.lower()
    scores = {domain: 0 for domain in DOMAIN_RULES}
    for domain, keywords in DOMAIN_RULES.items():
        if domain == "general":
            continue
        for kw in keywords:
            if kw in p:
                scores[domain] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "general"

def get_domain_label(domain: str) -> str:
    labels = {
        "fiction": "Fiction / Literature",
        "science": "Science",
        "computer_science": "Computer Science",
        "history": "History",
        "finance": "Finance / Economics",
        "health": "Health / Medicine",
        "general": "General"
    }
    return labels.get(domain, "General")
