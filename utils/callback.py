import httpx
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

async def trigger_callback(session_id: str, total_messages: int, extracted_intelligence: dict, agent_notes: str = "Scam detected based on keywords."):
    """
    Sends the mandatory callback to GUVI endpoint.
    Designed to be run as a background task.
    """
    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": total_messages,
        "extractedIntelligence": extracted_intelligence,
        "agentNotes": agent_notes
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(CALLBACK_URL, json=payload, timeout=10.0)
            
        if response.status_code == 200:
            logger.info(f"Callback successful for session {session_id}")
        else:
            logger.error(f"Callback failed for session {session_id}: {response.status_code} - {response.text}")
            
    except Exception as e:
        logger.error(f"Callback error for session {session_id}: {str(e)}")
