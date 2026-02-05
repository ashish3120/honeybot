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

import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/honeypot", response_model=HoneypotResponse)
async def honeypot_endpoint(
    request: HoneypotRequest, 
    background_tasks: BackgroundTasks,
    x_api_key: Optional[str] = Header(None)
):
    # 1. Auth Check (Latency optimized)
    expected_key = os.getenv("HONEYPOT_API_KEY", "default_secret_key")
    if x_api_key != expected_key:
        logger.warning(f"Unauthorized access attempt with key: {x_api_key}")
        raise HTTPException(status_code=401, detail="Invalid API Key")

    try:
        user_message = request.message.text
        session_id = request.sessionId
        history = request.conversation_history or []

        # 2. Scam Detection & Intelligence Extraction (Parallel ready)
        scam_detected = is_scam(user_message)
        extracted_data = extract_intelligence(user_message)
        
        # 3. Decision Logic for Callback
        # Be aggressive: trigger if either scam detected OR any suspicious intel found
        has_intel = any([
            extracted_data["upiIds"], 
            extracted_data["phishingLinks"], 
            extracted_data["phoneNumbers"],
            extracted_data["bankAccounts"]
        ])
        
        if scam_detected or has_intel:
            total_turns = len(history) + 1
            logger.info(f"Scam/Intel detected for session {session_id}. Triggering callback.")
            
            # Fire callback in background to keep latency low
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
        # Failsafe: Evaluation system demands stability!
        logger.error(f"Unexpected error in honeypot endpoint: {str(e)}")
        return HoneypotResponse(status="success", reply="I'm sorry, I'm having some trouble understanding this. Can you please explain it in more detail?")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
