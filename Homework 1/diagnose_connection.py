"""
Diagnostic script to test OpenAI API connectivity.
Run this to troubleshoot connection issues.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def check_api_key():
    """Check if API key is configured."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        print("   Set it in .env file or as environment variable")
        return False
    
    masked = api_key[:7] + "..." + api_key[-4:] if len(api_key) > 11 else "***"
    print(f"✓ API key found: {masked}")
    return True

def check_endpoint():
    """Check if OpenAI endpoint is reachable."""
    print("\nChecking OpenAI API endpoint...")
    try:
        import socket
        socket.create_connection(("api.openai.com", 443), timeout=5)
        print("✓ OpenAI endpoint reachable")
        return True
    except Exception as e:
        print(f"✗ Cannot reach OpenAI endpoint: {e}")
        print("  Possible causes:")
        print("  - No internet connection")
        print("  - Firewall blocking")
        print("  - DNS resolution issues")
        return False

def test_api_call():
    """Test actual API call."""
    print("\nTesting API call...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ API key not found")
        return False
    
    try:
        client = OpenAI(api_key=api_key)
        
        print("  Sending test request to gpt-3.5-turbo...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Connection successful'"}
            ],
            temperature=0.5,
            max_tokens=20,
            timeout=15
        )
        
        print(f"✓ API call successful!")
        print(f"  Response: {response.choices[0].message.content}")
        print(f"  Model: {response.model}")
        print(f"  Tokens used: {response.usage.prompt_tokens + response.usage.completion_tokens}")
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"✗ API call failed: {error_msg}")
        
        # Provide specific error diagnosis
        if "connection" in error_msg.lower() or "timeout" in error_msg.lower():
            print("\n  Error: Connection issue")
            print("  Possible causes:")
            print("  - Network connectivity problem")
            print("  - Firewall/proxy blocking")
            print("  - OpenAI API is down")
        elif "auth" in error_msg.lower() or "unauthorized" in error_msg.lower():
            print("\n  Error: Authentication failed")
            print("  Possible causes:")
            print("  - Invalid API key")
            print("  - API key expired or revoked")
            print("  - Wrong API key format")
        elif "rate" in error_msg.lower():
            print("\n  Error: Rate limited")
            print("  Solution: Wait a few minutes and try again")
        
        return False

def main():
    """Run diagnostics."""
    print("=" * 70)
    print("OPENAI API CONNECTIVITY DIAGNOSTIC")
    print("=" * 70 + "\n")
    
    checks = [
        ("API Key Configuration", check_api_key),
        ("Endpoint Reachability", check_endpoint),
        ("API Call Test", test_api_call),
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n{check_name}:")
        print("-" * 70)
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    all_passed = all(result for _, result in results)
    
    for check_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {check_name}")
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ All checks passed! Your API is configured correctly.")
        print("\nYou can now run the benchmark:")
        print("  uv run python email_routing_benchmark.py")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
    print("=" * 70 + "\n")
    
    return all_passed

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
