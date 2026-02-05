import re

def extract_intelligence(text: str) -> dict:
    """
    Extracts intelligence (UPI, URLs, Phone numbers, Keywords) from text.
    """
    
    # Regex patterns
    upi_pattern = r"[\w\.\-_]+@[\w\.\-_]+"
    url_pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+|www\.[-\w.]+"
    phone_pattern = r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
    
    # Keywords to flag specifically for intelligence
    suspicious_keywords_list = [
        "pay", "transfer", "bank", "password", "pin", "cvv", "atm", 
        "manager", "verification", "kyc", "documents"
    ]
    
    extracted = {
        "bankAccounts": [], # Regex for bank accounts is complex/varied, leaving empty as permitted
        "upiIds": re.findall(upi_pattern, text),
        "phishingLinks": re.findall(url_pattern, text),
        "phoneNumbers": re.findall(phone_pattern, text),
        "suspiciousKeywords": [k for k in suspicious_keywords_list if k in text.lower()]
    }
    
    return extracted
