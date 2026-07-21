"""
Setup Verification Script
Checks if all requirements are met before running the pipeline
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python version: {version.major}.{version.minor}.{version.micro}")
        print("   Required: Python 3.8 or higher")
        return False

def check_dependencies():
    """Check if required packages are installed."""
    print("\n📦 Checking dependencies...")
    
    required_packages = {
        'openai': 'openai',
        'jsonlines': 'jsonlines',
        'openpyxl': 'openpyxl',
        'dotenv': 'python-dotenv'
    }
    
    all_installed = True
    
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name if import_name != 'dotenv' else 'dotenv')
            print(f"   ✅ {package_name}")
        except ImportError:
            print(f"   ❌ {package_name} - NOT INSTALLED")
            all_installed = False
    
    return all_installed

def check_api_key():
    """Check if OpenAI API key is set."""
    print("\n🔑 Checking OpenAI API key...")
    
    # Try to load from .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except:
        pass
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("   ❌ OPENAI_API_KEY not found")
        print("\n   Set your API key using one of these methods:")
        print("   1. Create a .env file with: OPENAI_API_KEY=your-key-here")
        print("   2. Set environment variable:")
        print("      Windows PowerShell: $env:OPENAI_API_KEY='your-key-here'")
        print("      Unix/Mac: export OPENAI_API_KEY='your-key-here'")
        return False
    elif api_key.startswith("sk-") and len(api_key) > 20:
        # Mask the key
        masked_key = api_key[:7] + "..." + api_key[-4:]
        print(f"   ✅ API key found: {masked_key}")
        return True
    else:
        print(f"   ⚠️ API key found but format looks unusual")
        print(f"      Key: {api_key[:10]}...")
        return True

def check_dataset():
    """Check if dataset files exist."""
    print("\n📁 Checking dataset files...")
    
    base_dir = Path(__file__).parent / "hotel_booking_finetuning" / "openai_format"
    
    files_to_check = [
        ("train.jsonl", True),
        ("validation.jsonl", False)
    ]
    
    all_required_exist = True
    
    for filename, required in files_to_check:
        file_path = base_dir / filename
        if file_path.exists():
            # Count lines
            with open(file_path) as f:
                line_count = sum(1 for _ in f)
            print(f"   ✅ {filename} ({line_count} examples)")
        else:
            status = "❌" if required else "⚠️"
            print(f"   {status} {filename} - NOT FOUND")
            if required:
                all_required_exist = False
    
    return all_required_exist

def check_disk_space():
    """Check available disk space."""
    print("\n💾 Checking disk space...")
    
    try:
        import shutil
        total, used, free = shutil.disk_usage(Path(__file__).parent)
        
        free_gb = free / (1024**3)
        print(f"   Free space: {free_gb:.2f} GB")
        
        if free_gb < 1:
            print("   ⚠️ Low disk space - may cause issues")
            return False
        else:
            print("   ✅ Sufficient disk space")
            return True
    except:
        print("   ⚠️ Could not check disk space")
        return True

def test_openai_connection():
    """Test connection to OpenAI API."""
    print("\n🔌 Testing OpenAI API connection...")
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Simple test: list models
        models = client.models.list()
        print("   ✅ Successfully connected to OpenAI API")
        print(f"   ✅ API is responsive")
        return True
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        print("\n   Possible issues:")
        print("   - Invalid API key")
        print("   - No internet connection")
        print("   - OpenAI API is down")
        print("   - Insufficient API credits")
        return False

def main():
    """Run all checks."""
    print("=" * 70)
    print("SETUP VERIFICATION")
    print("=" * 70)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("API Key", check_api_key),
        ("Dataset Files", check_dataset),
        ("Disk Space", check_disk_space),
        ("OpenAI Connection", test_openai_connection)
    ]
    
    results = {}
    
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"   ❌ Error during {check_name} check: {e}")
            results[check_name] = False
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    all_passed = all(results.values())
    
    for check_name, passed in results.items():
        status = "✅" if passed else "❌"
        print(f"{status} {check_name}")
    
    print("\n" + "=" * 70)
    
    if all_passed:
        print("🎉 All checks passed! You're ready to run the pipeline.")
        print("\nNext step: python main.py")
        return 0
    else:
        print("⚠️ Some checks failed. Please fix the issues above before proceeding.")
        
        # Provide specific guidance
        if not results.get("Dependencies"):
            print("\n📦 Install dependencies: pip install -r requirements.txt")
        
        if not results.get("API Key"):
            print("\n🔑 Set your API key - see README.md for instructions")
        
        if not results.get("Dataset Files"):
            print("\n📁 Ensure dataset files are in hotel_booking_finetuning/openai_format/")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())
