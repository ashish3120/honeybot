import re

def extract_intelligence(text: str) -> dict:
    """
    Extracts scam intelligence from text:
    - Bank names
    - UPI IDs
    - URLs
    - Phone numbers
    - Suspicious keywords / tactics
    """

    text_lower = text.lower()

    # =====================
    # REGEX PATTERNS
    # =====================

    # UPI ID (strict & reliable)
    upi_pattern = r"\b[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}\b"

    # URLs
    url_pattern = r"https?://[^\s]+|www\.[^\s]+"

    # Phone numbers (India + general)
    phone_pattern = r"\+?\d[\d\s\-()]{8,}\d"

    # Bank account numbers (India/global heuristic)
    bank_account_pattern = r"\b\d{9,18}\b"

    # Bank name extraction from UPI domain
    # Example: scammer.fraud@fakebank → fakebank
    bank_name_pattern = r"@[a-zA-Z0-9.\-_]*?([a-zA-Z]{3,})\b"

    # =====================
    # SUSPICIOUS KEYWORDS / TACTICS
    # =====================

    suspicious_keywords_list = [
        "otp", "one time password", "verify", "verification",
        "urgent", "immediately", "right now", "locked", "blocked",
        "suspended", "confirm", "kyc", "update",
        "account", "bank", "upi", "fraud"
    ]

    # =====================
    # EXTRACTION
    # =====================

    upi_ids = list(set(re.findall(upi_pattern, text)))
    phishing_links = list(set(re.findall(url_pattern, text)))
    phone_numbers = list(set([
        p.strip() for p in re.findall(phone_pattern, text)
        if len(re.sub(r"\D", "", p)) >= 10
    ]))
    bank_accounts = list(set(re.findall(bank_account_pattern, text)))

    # Extract bank names from UPI IDs
    bank_names = list(set([
        match.group(1)
        for upi in upi_ids
        for match in [re.search(bank_name_pattern, upi)]
        if match
    ]))

    suspicious_keywords = list(set([
        k for k in suspicious_keywords_list if k in text_lower
    ]))

    return {
        "bankAccounts": bank_accounts,
        "bankNames": bank_names,
        "upiIds": upi_ids,
        "phishingLinks": phishing_links,
        "phoneNumbers": phone_numbers,
        "suspiciousKeywords": suspicious_keywords
    }
