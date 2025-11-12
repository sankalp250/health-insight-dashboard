"""
Quick test for predictions endpoint.
Run this to verify predictions endpoint works.
"""
import requests
import json

BASE_URL = "http://localhost:8080"

def test_predictions():
    """Test predictions endpoint"""
    print("🔍 Testing predictions endpoint...")
    try:
        # Test without filters
        response = requests.get(f"{BASE_URL}/api/ai/predictions?years_ahead=2", timeout=5)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Predictions endpoint works!")
            print(f"   Predictions: {len(data.get('predictions', []))} items")
            print(f"   Method: {data.get('method', 'unknown')}")
            print(f"   Confidence: {data.get('confidence', 0)}")
            if data.get('predictions'):
                print(f"   First prediction: {data['predictions'][0]}")
            else:
                print(f"   Message: {data.get('ai_insight', 'No message')}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Backend is not running on port 8080")
        print("   Start backend with: cd backend && uvicorn app.main:app --reload --port 8080")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🧪 Testing Predictions Endpoint")
    print("=" * 50)
    print("\n⚠️  Make sure the backend server is running!")
    print("   Run: cd backend && uvicorn app.main:app --reload --port 8080\n")
    
    success = test_predictions()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Predictions endpoint is working!")
    else:
        print("❌ Predictions endpoint failed. Check the errors above.")
    print("=" * 50)

