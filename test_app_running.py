import requests

print("Testing Backend API...")
try:
    # Test backend root (should be 404, but server is running)
    r = requests.get('http://localhost:8001/', timeout=5)
    print(f"✓ Backend responding: Status {r.status_code}")
except Exception as e:
    print(f"✗ Backend error: {e}")

try:
    # Test backend docs (should be 200)
    r = requests.get('http://localhost:8001/docs', timeout=5)
    print(f"✓ Backend /docs: Status {r.status_code}")
except Exception as e:
    print(f"✗ Backend /docs error: {e}")

print("\nTesting Frontend...")
try:
    r = requests.get('http://localhost:3000/', timeout=5)
    print(f"✓ Frontend responding: Status {r.status_code}")
    if r.status_code == 200:
        print(f"✓ Frontend content length: {len(r.text)} bytes")
except Exception as e:
    print(f"✗ Frontend error: {e}")

print("\n" + "="*50)
print("SUMMARY:")
print("Backend: http://localhost:8001")
print("Frontend: http://localhost:3000")
print("="*50)
