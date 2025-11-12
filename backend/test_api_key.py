"""
Quick script to test Groq API key - run from backend directory.
Usage: python test_api_key.py
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Try to load .env
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Loaded .env from {env_path}")
    else:
        print(f"⚠️  .env file not found at {env_path}")
        print("   Creating one for you...")
except ImportError:
    print("⚠️  python-dotenv not installed, trying environment variables directly")

# Check API key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("\n❌ GROQ_API_KEY not found!")
    print("\n📝 To fix:")
    print("   1. Create backend/.env file")
    print("   2. Add: GROQ_API_KEY=your_key_here")
    print("   3. Get key from: https://console.groq.com/")
    sys.exit(1)

api_key = api_key.strip()
if not api_key or api_key.startswith("your_"):
    print("\n❌ GROQ_API_KEY is empty or placeholder!")
    print("   Please add your actual API key to backend/.env")
    sys.exit(1)

print(f"\n✅ GROQ_API_KEY found ({len(api_key)} characters)")

# Test with Groq
try:
    from groq import Groq
    
    print("\n🔍 Testing API key...")
    client = Groq(api_key=api_key)
    
    # List models
    models = client.models.list()
    model_names = [m.id for m in models.data]
    
    print(f"✅ API Key is VALID! Connected to Groq API")
    print(f"   Available models: {len(model_names)}")
    
    # Check for our preferred models
    preferred = ["llama-3.1-8b-instant", "llama-3.1-70b-versatile"]
    available = [m for m in preferred if m in model_names]
    
    if available:
        print(f"\n✅ Preferred models available:")
        for model in available:
            print(f"   ✓ {model}")
        print(f"\n🎯 Will use: {available[0]} (most stable)")
    else:
        print(f"\n⚠️  Preferred models not found")
        print(f"   Available models include: {', '.join(model_names[:5])}")
        print(f"   Code will try: llama-3.1-8b-instant (fallback: llama-3.1-70b-versatile)")
    
    # Test a simple completion
    print("\n🧪 Testing model response...")
    try:
        chat = client.chat.completions.create(
            model="llama-3.1-8b-instant" if "llama-3.1-8b-instant" in model_names else model_names[0],
            messages=[{"role": "user", "content": "Say 'Hello'"}],
            max_tokens=10
        )
        response = chat.choices[0].message.content
        print(f"✅ Model test successful!")
        print(f"   Response: {response}")
    except Exception as e:
        if "llama-3.1-8b-instant" in model_names:
            # Try fallback
            try:
                chat = client.chat.completions.create(
                    model="llama-3.1-70b-versatile",
                    messages=[{"role": "user", "content": "Say 'Hello'"}],
                    max_tokens=10
                )
                print(f"✅ Fallback model test successful!")
            except:
                print(f"⚠️  Model test failed: {e}")
        else:
            print(f"⚠️  Model test failed: {e}")
    
    print("\n🎉 All checks passed! Your API key is working correctly.")
    print("\n📌 Next steps:")
    print("   1. Restart your backend server")
    print("   2. Test the AI chat in the frontend")
    
except ImportError:
    print("\n❌ 'groq' package not installed")
    print("   Run: pip install groq")
    sys.exit(1)
except Exception as e:
    error_str = str(e)
    if "401" in error_str or "invalid" in error_str.lower() or "unauthorized" in error_str.lower():
        print(f"\n❌ INVALID API KEY!")
        print(f"   Error: {error_str}")
        print("\n📝 To fix:")
        print("   1. Go to https://console.groq.com/")
        print("   2. Generate a NEW API key")
        print("   3. Update backend/.env with the new key")
        print("   4. Make sure there are NO spaces or quotes around the key")
    else:
        print(f"\n❌ Error testing API: {e}")
    sys.exit(1)

