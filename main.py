from fastapi import FastAPI
from pydantic import BaseModel
import nltk
from nltk.tokenize import word_tokenize
from pymongo import MongoClient
import os

nltk.download("punkt")

app = FastAPI()

# Intent recognition logic
intents = {
    "greeting": ["hello", "hi", "hey"],
    "farewell": ["bye", "goodbye", "see you"],
    "help": ["help", "assist", "support"],
    "thanks": ["thanks", "thank you"]
}

def detect_intent(text):
    words = word_tokenize(text.lower())
    for intent, keywords in intents.items():
        if any(word in words for word in keywords):
            return intent
    return "unknown"

# MongoDB Setup (Optional)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["ai_voice_assistant"]
collection = db["interactions"]

# Pydantic model for input validation
class TextRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "AI Voice Assistant API is running"}

@app.post("/process/")
def process_text(request: TextRequest):
    intent = detect_intent(request.text)
    response = {"input": request.text, "detected_intent": intent}

    # Store in DB
    collection.insert_one(response)
    return response
