"""
Quick debug script to verify Django session + CORS + CSRF setup.
Run this after logging in via the frontend to check if cookies are properly set.

Instructions:
1. Start Django: python manage.py runserver localhost:8000
2. Start TaskManagementFinal: npm run dev
3. Login via frontend (http://localhost:5173)
4. Open browser DevTools → Application → Cookies
5. Verify that both 'sessionid' and 'csrftoken' cookies are present
6. Copy the sessionid value and update SESSIONID_VALUE below
7. Run: python debug_session.py
"""

import requests
import json

# Configuration
API_BASE = "http://localhost:8000/api"
SESSIONID_VALUE = "YOUR_SESSIONID_HERE"  # Replace with value from browser cookies
CSRF_TOKEN = "YOUR_CSRFTOKEN_HERE"  # Replace with value from browser cookies

def test_with_session():
    """Test API endpoints using session credentials"""
    
    print("=" * 60)
    print("Testing TaskManagementFinal + Django Backend Communication")
    print("=" * 60)
    
    # Test 1: Check profile without session (should return authenticated: false)
    print("\n[TEST 1] GET /accounts/api/profile/ (no session)")
    resp = requests.get(f"{API_BASE}/accounts/api/profile/")
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.json()}")
    
    # Test 2: Login
    print("\n[TEST 2] POST /accounts/api/login/")
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    resp = requests.post(
        f"{API_BASE}/accounts/api/login/",
        json=login_data,
        allow_redirects=True
    )
    print(f"Status: {resp.status_code}")
    response_json = resp.json()
    print(f"Response: {json.dumps(response_json, indent=2)}")
    
    # Extract session cookie
    if 'Set-Cookie' in resp.headers:
        print(f"Set-Cookie header: {resp.headers['Set-Cookie']}")
    
    # Store session for next requests
    session = requests.Session()
    session.cookies.update(resp.cookies)
    
    # Test 3: Get profile with session
    print("\n[TEST 3] GET /accounts/api/profile/ (with session)")
    resp = session.get(f"{API_BASE}/accounts/api/profile/")
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.json()}")
    
    # Test 4: Get tasks with session
    print("\n[TEST 4] GET /api/tasks/ (with session)")
    resp = session.get(f"{API_BASE}/tasks/")
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        print(f"Tasks fetched: {len(resp.json())} tasks")
    else:
        print(f"Error: {resp.json()}")
    
    # Test 5: Get stats with session
    print("\n[TEST 5] GET /api/tasks/stats/ (with session)")
    resp = session.get(f"{API_BASE}/tasks/stats/")
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.json()}")
    
    print("\n" + "=" * 60)
    print("If all tests return 200 and show data, everything works!")
    print("=" * 60)

if __name__ == "__main__":
    test_with_session()
