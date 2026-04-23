#from fastapi import FastAPI
#from fastapi.middleware.cors import CORSMiddleware
#from dotenv import load_dotenv
#import os
#from api.routes import router as api_router
#print("GOOGLE KEY:", os.getenv("GOOGLE_API_KEY"))

# Load environment variables from the backend directory
#load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

#app = FastAPI(title="Prompt Evaluator API", version="1.0.0")

# Configure CORS
#app.add_middleware(
#    CORSMiddleware,
#    allow_origins=["*"],  # Adjust in production
#    allow_credentials=True,
#    allow_methods=["*"],
#    allow_headers=["*"],
#)

#app.include_router(api_router, prefix="/api")

#@app.get("/")
#def root():
#    return {"message": "Welcome to Prompt Evaluator API"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from api.routes import router as api_router

# ✅ LOAD ENV FIRST
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Now access variables
print("GOOGLE KEY:", os.getenv("GOOGLE_API_KEY"))

app = FastAPI(title="Prompt Evaluator API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to Prompt Evaluator API"}
