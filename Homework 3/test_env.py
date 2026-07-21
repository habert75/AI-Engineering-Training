"""
Quick test to verify .env file is loaded correctly
"""

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def test_env_loading():
    """Test if API key is loaded from .env file."""
    print("🔍 Testing .env file loading...")
    print("=" * 60)
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ OPENAI_API_KEY not found!")
        print("\n💡 Solution:")
        print("1. Make sure .env file exists in the project directory")
        print("2. Add your API key to .env:")
        print("   OPENAI_API_KEY=sk-your-actual-key-here")
        return False
    
    # Mask the key for security
    if api_key.startswith("sk-"):
        masked_key = api_key[:7] + "..." + api_key[-4:]
        print(f"✅ API key loaded successfully!")
        print(f"   Key: {masked_key}")
        print(f"   Length: {len(api_key)} characters")
        print(f"   Source: .env file")
    else:
        print(f"⚠️ API key found but format looks unusual")
        print(f"   Key starts with: {api_key[:10]}...")
    
    print("=" * 60)
    print("✅ .env file is working correctly!")
    return True

if __name__ == "__main__":
    import sys
    success = test_env_loading()
    sys.exit(0 if success else 1)
