import random

def generate_reply(text: str, conversation_history: list) -> str:
    """
    Optimized honeypot persona:
    - Mid-aged, low-tech, cooperative
    - Never exits conversation early
    - Keeps scammer engaged safely
    """

    text_lower = text.lower()
    turn_count = len(conversation_history)

    def hesitate(s):
        return random.choice([
            s,
            f"Um… {s}",
            f"Just a second… {s}",
            f"{s} I’m a bit confused."
        ])

    # ===== LATE STAGE (Turn 7+) — slow compliance, not exit =====
    if turn_count >= 7:
        return hesitate(random.choice([
            "I’m trying to do this correctly, please guide me step by step.",
            "I don’t want to make a mistake here. What should I do next?",
            "This is a bit stressful, but I want to finish it properly.",
            "Please explain once more, slowly."
        ]))

    # ===== OTP / PIN =====
    if any(x in text_lower for x in ["otp", "code", "pin", "password"]):
        return hesitate(random.choice([
            "I haven’t received any code yet. Does it come by SMS?",
            "What is this code used for exactly?",
            "Is it safe to share the code here?",
            "It says the code will expire. What should I do?"
        ]))

    # ===== LINK / APP =====
    if any(x in text_lower for x in ["link", "click", "download", "app", "apk"]):
        return hesitate(random.choice([
            "The link is opening very slowly on my phone.",
            "Is this the official website? It looks different.",
            "Do I need to download something to complete this?",
            "Can you tell me what will happen after I open the link?"
        ]))

    # ===== MONEY / PAYMENT =====
    if any(x in text_lower for x in ["pay", "transfer", "amount", "rs", "rupees", "fee"]):
        return hesitate(random.choice([
            "Why is there a charge for this?",
            "Which account should I send it to?",
            "Is this a one-time payment or recurring?",
            "I just want to be sure before sending money."
        ]))

    # ===== THREAT / URGENCY =====
    if any(x in text_lower for x in ["block", "suspend", "close", "urgent", "expire"]):
        return random.choice([
            "Please don’t block it, I use this account regularly.",
            "I’m worried now. What is the quickest way to fix this?",
            "Why is this happening suddenly?",
            "I want to resolve this today if possible."
        ])

    # ===== CONTINUITY =====
    if turn_count > 0:
        return random.choice([
            "You mentioned something earlier, can you explain that again?",
            "I’m still trying to understand what needs to be done.",
            "What is the next step from my side?",
            "I’m following, please continue."
        ])

    # ===== FIRST MESSAGE =====
    return random.choice([
        "Sorry, I didn’t understand this properly. Can you explain?",
        "What is this message about?",
        "Is this regarding my bank account?",
        "I’m a bit confused, can you clarify?"
    ])
