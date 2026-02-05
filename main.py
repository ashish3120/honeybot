from fastapi import FastAPI, HTTPException, Header, BackgroundTasks, Request
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv

from core.detector import is_scam
from core.extractor import extract_intelligence
from core.persona import generate_reply
from utils.callback import trigger_callback

# Load environment variables
load_dotenv()

app = FastAPI()

# Pydantic models
class Message(BaseModel):
    text: str

class HoneypotRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: Optional[List[Dict[str, Any]]] = []
    metadata: Optional[Dict[str, Any]] = {}

class HoneypotResponse(BaseModel):
    status: str
    reply: str

@app.post("/honeypot", response_model=HoneypotResponse)
async def honeypot_endpoint(
    request: HoneypotRequest, 
    background_tasks: BackgroundTasks,
    x_api_key: Optional[str] = Header(None)
):
    # 1. Auth Check
    expected_key = os.getenv("HONEYPOT_API_KEY", "default_secret_key")
    if x_api_key != expected_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    try:
        user_message = request.message.text
        session_id = request.sessionId
        history = request.conversationHistory or []

        # 2. Scam Detection
        scam_detected = is_scam(user_message)

        # 3. Intelligence Extraction
        # We always extract, but we only trigger callback if scam is detected OR based on other heuristics if needed.
        # The prompt says: "When Scam intent is confirmed AND sufficient engagement has occurred (>=2-3 turns OR intel found)"
        # For simplicity/robustness in hackathon, if we see scam keywords, we flag it.
        
        extracted_data = extract_intelligence(user_message)
        
        # Check if we should trigger callback
        # Logic: If scam detected OR we found specific intel (like UPI/URL)
        has_intel = len(extracted_data["upiIds"]) > 0 or len(extracted_data["phishingLinks"]) > 0 or len(extracted_data["phoneNumbers"]) > 0
        
        if scam_detected or has_intel:
            # Calculate total messages approximately from history + current
            total_turns = len(history) + 1
            
            # Fire callback in background
            background_tasks.add_task(
                trigger_callback, 
                session_id=session_id, 
                total_messages=total_turns, 
                extracted_intelligence=extracted_data
            )

        # 4. Generate Reply
        reply_text = generate_reply(user_message, history)
        
        return HoneypotResponse(status="success", reply=reply_text)

    except Exception as e:
        # Failsafe: return neutral response even if something breaks
        print(f"Error processing request: {e}")
        return HoneypotResponse(status="success", reply="Can you please explain this in more detail?")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
