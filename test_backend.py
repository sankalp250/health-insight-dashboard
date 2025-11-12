"""
Quick test script to verify backend is working.
Run this after starting the backend server.
"""
import requests
import json

BASE_URL = "http://localhost:8080"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/healthz")
        print(f"✅ Health check: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_vaccines():
    """Test vaccines endpoint"""
    print("\n🔍 Testing vaccines endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/vaccines?limit=5")
        data = response.json()
        print(f"✅ Vaccines endpoint: {data['total']} total records, {data['returned']} returned")
        if data['data']:
            print(f"   First record: {data['data'][0]['brand']} in {data['data'][0]['region']}")
        return True
    except Exception as e:
        print(f"❌ Vaccines endpoint failed: {e}")
        return False

def test_summary():
    """Test summary endpoint"""
    print("\n🔍 Testing summary endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/summary")
        data = response.json()
        print(f"✅ Summary endpoint: {len(data['kpis'])} KPIs")
        for kpi in data['kpis']:
            print(f"   - {kpi['label']}: {kpi['value']} {kpi['unit'] or ''}")
        return True
    except Exception as e:
        print(f"❌ Summary endpoint failed: {e}")
        return False

def test_ai_chat():
    """Test AI chat endpoint"""
    print("\n🔍 Testing AI chat endpoint...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/ai/chat",
            json={"query": "What is the total market size?"}
        )
        data = response.json()
        print(f"✅ AI Chat endpoint: {data.get('answer', 'No answer')[:100]}...")
        print(f"   Visualization: {data.get('visualization')}")
        print(f"   Confidence: {data.get('confidence', 0)}")
        return True
    except Exception as e:
        print(f"❌ AI Chat endpoint failed: {e}")
        print("   Note: This requires GROQ_API_KEY to be set in backend/.env")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🧪 Testing Health Insight Dashboard Backend")
    print("=" * 50)
    print("\n⚠️  Make sure the backend server is running!")
    print("   Run: cd backend && uvicorn app.main:app --reload --port 8000\n")
    
    results = []
    results.append(test_health())
    results.append(test_vaccines())
    results.append(test_summary())
    results.append(test_ai_chat())
    
    print("\n" + "=" * 50)
    if all(results):
        print("✅ All tests passed!")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    print("=" * 50)

