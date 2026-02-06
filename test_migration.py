import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
BASE_URL = "http://127.0.0.1:8001"

def test_migration():
    try:
        print("Testing Auth...")
        email = "test_migration@example.com"
        password = "password123"
        res = requests.post(f"{BASE_URL}/auth/signup", json={"email": email, "password": password})
        if res.status_code == 400:
             res = requests.post(f"{BASE_URL}/auth/token", data={"username": email, "password": password})
        
        res.raise_for_status()
        token = res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        print("Testing Chat with new SDK...")
        chat_res = requests.post(f"{BASE_URL}/chat", headers=headers, json={"message": "Hello! Add a task called 'Test New SDK' please."})
        chat_res.raise_for_status()
        reply = chat_res.json()
        print(f"Reply: {reply['reply']}")
        print(f"Refresh Needed: {reply['refresh']}")

        if reply['refresh']:
            print("Migration verified: Tool calling works with google-genai!")
        else:
            print("Warning: Tool calling might not have triggered. Check logs.")

    except Exception as e:
        print(f"Verification Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_migration()
