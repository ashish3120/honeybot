import random

def generate_reply(text: str, conversation_history: list) -> str:
    """
    Generates a human-like, confused/cautious reply.
    Does NOT mention scams.
    """
    
    # Simple rule-based responses if context matches, otherwise random neutral questions
    
    text_lower = text.lower()
    
    if "otp" in text_lower or "code" in text_lower:
        return random.choice([
            "Wait, I didn't ask for any code. Why are you sending this?",
            "I haven't received any notification on my phone. Is this necessary?",
            "I'm a bit busy, can we do this later? What is the code for anyway?"
        ])
    
    if "link" in text_lower or "click" in text_lower:
        return random.choice([
            "My son told me not to click on random links. Can you just tell me here?",
            "The link isn't opening on my phone. What does it say?",
            "Is there another way? I don't feel comfortable with links."
        ])
        
    if "pay" in text_lower or "transfer" in text_lower or "money" in text_lower or "fees" in text_lower:
        return random.choice([
            "I don't have that much balance right now. Can I pay half?",
            "Which bank are you from? I have accounts in SBI and HDFC.",
            "Can you send me the account details again? I lost them."
        ])
        
    if "blocked" in text_lower or "suspended" in text_lower or "closed" in text_lower:
        return random.choice([
            "Oh no! My pension comes into that account. How do I fix it?",
            "But I just used my card this morning for groceries. Are you sure?",
            "I can't go to the branch today, it's too far. Can you help me here?"
        ])
    
    generic_replies = [
        "I'm sorry, I didn't quite catch that. Could you clarify?",
        "Is this official? I haven't gotten any letters about this.",
        "Wait, who is this speaking? I forget things easily.",
        "Can you wait a minute? I need to find my glasses.",
        "I'm a bit confused, why are you calling/messaging me now?",
        "My daughter usually handles these things, but she's not home.",
        "Please explain it simply, I'm not very good with technology.",
        "Can you please explain this in more detail?"
    ]
    
    return random.choice(generic_replies)
