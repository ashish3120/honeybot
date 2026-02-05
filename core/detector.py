def is_scam(text: str) -> bool:
    """
    Detects if the message is a potential scam based on keywords.
    """
    scam_keywords = [
        "blocked", "suspended", "verify", "urgent", "kyc", "otp", 
        "upi", "refund", "account", "pan card", "adhaar", "limit",
        "update", "win", "lottery", "prize", "cashback", "reward",
        "pending", "expired", "deactivated", "malicious", "security",
        "verification", "click here", "unauthorized", "suspicious"
    ]
    
    text_lower = text.lower()
    for keyword in scam_keywords:
        if keyword in text_lower:
            return True
            
    return False
