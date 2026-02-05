import httpx
import asyncio
import os
import json
from dotenv import load_dotenv

# Load env vars
load_dotenv()
API_KEY = os.getenv("HONEYPOT_API_KEY", "default_secret_key")
BASE_URL = "http://localhost:8000"

async def test_normal_query():
    print("\n--- Testing Normal Query ---")
    async with httpx.AsyncClient() as client:
        payload = {
            "sessionId": "test-session-123",
            "message": {
                "text": "Hello, how are you?"
            },
            "conversationHistory": []
        }
        headers = {"x-api-key": API_KEY}
        
        try:
            response = await client.post(f"{BASE_URL}/honeypot", json=payload, headers=headers)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            assert response.status_code == 200
            assert response.json()["status"] == "success"
        except Exception as e:
            print(f"Test Failed: {e}")

async def test_scam_query():
    print("\n--- Testing Scam Query (Should trigger callback) ---")
    async with httpx.AsyncClient() as client:
        payload = {
            "sessionId": "scam-session-456",
            "message": {
                "text": "Your account is blocked. Please verify your UPI details immediately."
            },
            "conversationHistory": []
        }
        headers = {"x-api-key": API_KEY}
        
        try:
            response = await client.post(f"{BASE_URL}/honeypot", json=payload, headers=headers)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            assert response.status_code == 200
            assert response.json()["status"] == "success"
        except Exception as e:
            print(f"Test Failed: {e}")

async def test_auth_failure():
    print("\n--- Testing Auth Failure ---")
    async with httpx.AsyncClient() as client:
        payload = {"sessionId": "fail", "message": {"text": "hi"}}
        headers = {"x-api-key": "wrong-key"}
        
        response = await client.post(f"{BASE_URL}/honeypot", json=payload, headers=headers)
        print(f"Status: {response.status_code} (Expected 401)")
        assert response.status_code == 401
    
if __name__ == "__main__":
    print("Starting tests... Make sure the server is running!")
    # Simple check to see if we can connect, assuming user runs server separately or we run it in bg
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(test_normal_query())
    loop.run_until_complete(test_scam_query())
    loop.run_until_complete(test_auth_failure())
