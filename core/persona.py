import random

def generate_reply(text: str, conversation_history: list) -> str:
    """
    Generates a human-like, confused/cautious reply.
    Uses conversation_history to understand context and avoid repetition.
    """
    
    text_lower = text.lower()
    turn_count = len(conversation_history)
    
    # helper for adding hesitation
    def hesitate(s):
        return random.choice([f"Um... {s}", f"{s}...", f"Wait, {s}", s])

    # 1. High frustration / Late stage
    if turn_count > 5:
        frustrated_responses = [
            "Look, I'm really getting confused here... Can we just talk on the phone?",
            "This is taking too long. I'm already late for my prayer meeting.",
            "I've told you before, I don't understand these things! Why are you keeping me?",
            "I'm going to have to ask my son to call you back, this is too much for me.",
            "My head is spinning with all this tech stuff. Please stop.",
            "Are you sure this is necessary? It feels very complicated.",
            "I think I'll just go to the bank tomorrow. This is too hard."
        ]
        return random.choice(frustrated_responses)

    # 2. Context-specific responses
    
    # OTP / Code
    if any(x in text_lower for x in ["otp", "code", "pin", "password"]):
        return hesitate(random.choice([
            "I didn't ask for any code... Why are you sending this?",
            "I haven't received any notification on my phone yet. Is it SMS?",
            "I'm a bit busy right now, can we do this later? What is the code for anyway?",
            "My son said never share codes. Is this safe?",
            "Where do I find this code? My messages are full of junk.",
            "Is it the 4 digit one or the 6 digit one? I have a few here.",
            "Wait, a message just popped up but it went away. Send it again?"
        ]))
    
    # Link / Click / App
    if any(x in text_lower for x in ["link", "click", "app", "download", "apk"]):
        return hesitate(random.choice([
            "My son told me not to click on random links... Can you just tell me here?",
            "The link isn't opening on my phone. It says 'Error'. What does it say?",
            "Is there another way? I really don't feel comfortable with links.",
            "Do I have to download something? My phone storage is full.",
            "I clicked it but nothing happened. Am I doing it wrong?",
            "Can't you just do it from your end? I'm not good with this.",
            "Is this the official website? It looks a bit different."
        ]))
        
    # Money / Payment / Bank / Fees
    if any(x in text_lower for x in ["pay", "transfer", "money", "fees", "rs", "rupees", "amount"]):
        return hesitate(random.choice([
            "I don't have that much balance right now... Can I pay half?",
            "Which bank are you from again? I have accounts in SBI and HDFC.",
            "Can you send me the account details again? I think I lost them.",
            "Is there a senior citizen discount? Usually I get one.",
            "My daily limit is low. Can I send it in two parts?",
            "I need to ask my husband before sending that much. He handles the finances.",
            "Why is there a fee? You said it was a refund earlier..."
        ]))
        
    # Threats / Urgent / Police / Blocked
    if any(x in text_lower for x in ["block", "suspend", "close", "police", "jail", "illegal", "urgent", "expire"]):
        return random.choice([
            "Oh no! My pension comes into that account... How do I fix it?",
            "But I just used my card this morning for groceries! Are you sure?",
            "I can't go to the branch today, it's raining. Can you help me here?",
            "Please don't block it! I have to pay my electricity bill tomorrow.",
            "This is very scaring me. Let me call my neighbor, he knows a lawyer.",
            "Why is this happening? I've been a loyal customer for 20 years!",
            " ok ok I am listening. Please don't do anything to my account."
        ])
    
    # General Agreement / "Okay" / "Yes" triggers
    if any(x in text_lower for x in ["ok", "okay", "listen", "understand", "wait"]):
        return random.choice([
            "Okay, I'm listening...",
            "I am trying to understand, beta. Go slowly.",
            "Yes, yes, I am here. Tell me.",
            "Okay but please hurry, my tea is getting cold.",
            "I am listening. What needs to be done?"
        ])

    # 3. Acknowledge continuity if history exists
    if turn_count > 0:
        continuity_replies = [
            "As I was saying, I'm still not quite sure about this...",
            "Can you repeat that part? I'm trying to write it down on paper.",
            "You still haven't explained why this is so urgent.",
            "Is there someone else I should be talking to? A manager maybe?",
            "I am finding this very difficult. Is there a simpler way?",
            "Hold on, my glasses fell down."
        ]
        return random.choice(continuity_replies)

    # 4. First-turn generic replies
    generic_replies = [
        "I'm sorry, I didn't quite catch that. Could you clarify?",
        "Is this official? I haven't gotten any letters about this in the post.",
        "Wait, who is this speaking? I forget things easily these days.",
        "Can you wait a minute? I need to find my reading glasses.",
        "I'm a bit confused, why are you calling/messaging me now?",
        "My daughter usually handles these things, but she's not home.",
        "Please explain it simply, I'm not very good with technology...",
        "Can you please explain this in more detail? I am old."
    ]
    
    return random.choice(generic_replies)
