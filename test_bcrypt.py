from passlib.context import CryptContext
import os

print("Testing CryptContext...")
try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    print("CryptContext initialized.")
    h = pwd_context.hash("password123")
    print(f"Hash: {h}")
    v = pwd_context.verify("password123", h)
    print(f"Verify: {v}")
except Exception as e:
    print(f"Bcrypt Test Failed: {e}")
    import traceback
    traceback.print_exc()
