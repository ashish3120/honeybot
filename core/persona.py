import random

def generate_reply(text: str, conversation_history: list) -> str:
    """
    Generates a human-like, confused/cautious reply.
    Does NOT mention scams.
    """
    
    # Simple rule-based responses if context matches, otherwise random neutral questions
    
    text_lower = text.lower()
    
    if "otp" in text_lower or "code" in text_lower:
        return "I didn't request any code. What is this for?"
    
    if "link" in text_lower or "click" in text_lower:
        return "I'm not comfortable clicking links. Can you tell me what it's about?"
        
    if "pay" in text_lower or "transfer" in text_lower or "money" in text_lower:
        return "Which account are you referring to? I have a few."
        
    if "blocked" in text_lower or "suspended" in text_lower:
        return "Why would it be blocked? I used it yesterday."
    
    generic_replies = [
        "I don't understand, can you explain?",
        "Who is this exactly?",
        "I didn't receive any official notification about this.",
        "Can you send me an email instead?",
        "I need to check with my bank first.",
        "This is very confusing.",
        "What is the urgency?",
        "Can you please explain this in more detail?" # Default safe reply
    ]
    
    return random.choice(generic_replies)
