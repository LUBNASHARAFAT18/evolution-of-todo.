import requests
import json

BASE_URL = "http://localhost:8000"

def test_signup_and_chat():
    try:
        # 1. Signup
        print("Testing Signup...")
        email = "test_verify@example.com"
        password = "password123"
        res = requests.post(f"{BASE_URL}/auth/signup", json={"email": email, "password": password})
        if res.status_code == 400 and "already registered" in res.text:
             # If already exists, login
             print("User already exists, logging in...")
             res = requests.post(f"{BASE_URL}/auth/token", data={"username": email, "password": password})
        
        res.raise_for_status()
        token = res.json()["access_token"]
        print("Auth Success!")

        # 2. Chat
        print("Testing Chat with Gemini...")
        headers = {"Authorization": f"Bearer {token}"}
        chat_res = requests.post(f"{BASE_URL}/chat", headers=headers, json={"message": "Hello, who are you and what can you do?"})
        chat_res.raise_for_status()
        print(f"Chat Reply: {chat_res.json()['reply']}")

        # 3. Test Tool Calling (Add Task)
        print("Testing Tool Calling (Add Task)...")
        tool_res = requests.post(f"{BASE_URL}/chat", headers=headers, json={"message": "Add a task to verify phase 3"})
        tool_res.raise_for_status()
        print(f"Tool Reply: {tool_res.json()['reply']}")
        print(f"Refresh Needed: {tool_res.json()['refresh']}")

        if tool_res.json()['refresh']:
            print("Successfully verified tool calling!")
        else:
            print("Warning: Tool calling might not have been triggered as expected.")

    except Exception as e:
        print(f"Verification Failed: {e}")

if __name__ == "__main__":
    test_signup_and_chat()
