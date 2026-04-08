import os
import motor.motor_asyncio
from datetime import datetime

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.prompt_evaluator
logs_collection = db.logs

async def log_interaction(prompt: str, responses: dict, scores: dict, latency: dict, is_malicious: bool):
    interaction_doc = {
        "prompt": prompt,
        "responses": responses,
        "scores": scores,
        "latency": latency,
        "is_malicious": is_malicious,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    try:
        await logs_collection.insert_one(interaction_doc)
        print("Logged interaction successfully.")
    except Exception as e:
        print(f"Failed to log interaction: {e}")
