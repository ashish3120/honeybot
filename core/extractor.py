import re

def extract_intelligence(text: str) -> dict:
    """
    Extracts intelligence (UPI, URLs, Phone numbers, Keywords) from text with improved regex.
    """
    
    # Improved Regex patterns
    # UPI: Handles dots, dashes, and varied domain suffixes
    upi_pattern = r"[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}"
    
    # URLs: More comprehensive URL pattern including common phishing domains
    url_pattern = r"(https?://(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?://(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
    
    # Phone Numbers: Handles international formats, spaces, and dashes
    phone_pattern = r"(\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9})"
    
    # Bank Account Numbers: Typically 9-18 digits in India/international context
    bank_pattern = r"\b\d{9,18}\b"
    
    # Keywords to flag specifically for intelligence
    suspicious_keywords_list = [
        "pay", "transfer", "bank", "password", "pin", "cvv", "atm", 
        "manager", "verification", "kyc", "documents", "login", "update",
        "official", "department", "regulatory", "mandatory", "immediate"
    ]
    
    text_lower = text.lower()
    
    extracted = {
        "bankAccounts": list(set(re.findall(bank_pattern, text))),
        "upiIds": list(set(re.findall(upi_pattern, text))),
        "phishingLinks": list(set(re.findall(url_pattern, text))),
        "phoneNumbers": list(set([p.strip() for p in re.findall(phone_pattern, text) if len(re.sub(r'\D', '', p)) >= 10])),
        "suspiciousKeywords": list(set([k for k in suspicious_keywords_list if k in text_lower]))
    }
    
    return extracted
