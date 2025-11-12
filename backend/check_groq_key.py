"""
Script to verify Groq API key is configured correctly.
Run this to test your API key before starting the server.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ Loaded .env file from {env_path}")
else:
    print(f"❌ .env file not found at {env_path}")
    print("   Please create backend/.env with: GROQ_API_KEY=your_key_here")

# Check API key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("\n❌ GROQ_API_KEY not found in environment variables")
    print("   Make sure backend/.env contains: GROQ_API_KEY=your_key_here")
    exit(1)

# Check for common issues
api_key = api_key.strip()
if not api_key:
    print("\n❌ GROQ_API_KEY is empty")
    exit(1)

if api_key.startswith("your_") or api_key.startswith("YOUR_"):
    print("\n❌ GROQ_API_KEY appears to be a placeholder")
    print("   Please replace with your actual API key from https://console.groq.com/")
    exit(1)

if len(api_key) < 20:
    print(f"\n⚠️  GROQ_API_KEY seems too short ({len(api_key)} characters)")
    print("   Typical API keys are longer. Please verify your key.")

print(f"\n✅ GROQ_API_KEY found ({len(api_key)} characters)")

# Test API key with a simple request
try:
    from groq import Groq
    
    client = Groq(api_key=api_key)
    models = client.models.list()
    print("✅ API Key is valid! Successfully connected to Groq API")
    print(f"   Available models: {len(models.data)} models")
    
    # Check for llama-3.1 models
    model_names = [m.id for m in models.data]
    print(f"\n📋 Available models ({len(model_names)} total):")
    for model in model_names[:10]:  # Show first 10
        print(f"   - {model}")
    
    # Check for preferred models
    preferred_models = ["llama-3.1-8b-instant", "llama-3.1-70b-versatile", "mixtral-8x7b-32768"]
    available_preferred = [m for m in preferred_models if m in model_names]
    
    if available_preferred:
        print(f"\n✅ Preferred models available: {', '.join(available_preferred)}")
        print(f"   Using: {available_preferred[0]} (most stable)")
    else:
        print("\n⚠️  Preferred models not found in available models")
        print("   The code will try to use 'llama-3.1-8b-instant' first, then fallback to 'llama-3.1-70b-versatile'")
        
except ImportError:
    print("\n⚠️  groq package not installed")
    print("   Run: pip install groq")
except Exception as e:
    print(f"\n❌ Error testing API key: {e}")
    if "401" in str(e) or "invalid" in str(e).lower():
        print("   This means your API key is invalid or expired")
        print("   Get a new key from: https://console.groq.com/")
    exit(1)

print("\n🎉 All checks passed! Your Groq API key is configured correctly.")

