import os
import motor.motor_asyncio
from datetime import datetime

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.prompt_evaluator
logs_collection = db.logs
dataset_collection = db.dataset
versions_collection = db.prompt_versions
feedback_collection = db.feedback

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


async def save_dataset_entry(prompt: str, expected_keywords: list = None, expected_format: str = None, ideal_length: int = 100, version: str = None):
    entry = {
        "prompt": prompt,
        "expected_keywords": expected_keywords or [],
        "expected_format": expected_format,
        "ideal_length": ideal_length,
        "version": version,
        "created_at": datetime.utcnow().isoformat()
    }
    try:
        await dataset_collection.insert_one(entry)
        return True
    except Exception as e:
        print(f"Failed to save dataset entry: {e}")
        return False


async def list_dataset_entries():
    try:
        cursor = dataset_collection.find({}).sort("created_at", -1)
        return [doc async for doc in cursor]
    except Exception as e:
        print(f"Failed to load dataset entries: {e}")
        return []


async def save_prompt_version(prompt: str, version: str, score: float, metrics: dict):
    entry = {
        "prompt": prompt,
        "version": version,
        "score": score,
        "metrics": metrics,
        "created_at": datetime.utcnow().isoformat()
    }
    try:
        await versions_collection.insert_one(entry)
        return True
    except Exception as e:
        print(f"Failed to save prompt version: {e}")
        return False


async def list_prompt_versions(prompt: str = None):
    query = {"prompt": prompt} if prompt else {}
    try:
        cursor = versions_collection.find(query).sort("created_at", -1)
        return [doc async for doc in cursor]
    except Exception as e:
        print(f"Failed to load prompt versions: {e}")
        return []


async def save_feedback(prompt: str, feedback: str, score: float = None, comment: str = None):
    entry = {
        "prompt": prompt,
        "feedback": feedback,
        "score": score,
        "comment": comment,
        "created_at": datetime.utcnow().isoformat()
    }
    try:
        await feedback_collection.insert_one(entry)
        return True
    except Exception as e:
        print(f"Failed to save feedback: {e}")
        return False


async def list_feedback():
    try:
        cursor = feedback_collection.find({}).sort("created_at", -1)
        return [doc async for doc in cursor]
    except Exception as e:
        print(f"Failed to load feedback: {e}")
        return []
