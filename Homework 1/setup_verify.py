"""
Quick setup and configuration script for the Email Routing Benchmark.
"""

import os
import sys
import subprocess


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print("✓ Python version OK:", sys.version.split()[0])
    return True


def check_uv():
    """Check if uv is installed."""
    try:
        result = subprocess.run(["uv", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✓ uv installed: {version}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ uv not installed")
    print("\nInstalling uv:")
    print("  Run: pip install uv")
    print("  Or visit: https://github.com/astral-sh/uv#installation")
    return False


def check_dependencies():
    """Check if required packages are installed."""
    required_packages = {
        'openai': 'openai',
        'openpyxl': 'openpyxl'
    }
    
    missing = []
    for package, import_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"✓ {package} installed")
        except ImportError:
            print(f"❌ {package} not installed")
            missing.append(package)
    
    if missing:
        print(f"\nInstalling missing packages using uv: {', '.join(missing)}")
        try:
            subprocess.check_call(["uv", "sync"])
            print("✓ Dependencies installed")
        except FileNotFoundError:
            print("⚠ uv not found. Installing with pip instead...")
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
            print("✓ Dependencies installed (via pip)")
        return True
    return True


def check_openai_key():
    """Check if OpenAI API key is set."""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        masked_key = api_key[:7] + "..." + api_key[-4:] if len(api_key) > 11 else "***"
        print(f"✓ OPENAI_API_KEY found: {masked_key}")
        return True
    else:
        print("❌ OPENAI_API_KEY not set")
        print("\nTo set it:")
        if sys.platform == "win32":
            print("  PowerShell: $env:OPENAI_API_KEY=\"sk-...\"")
            print("  CMD: set OPENAI_API_KEY=sk-...")
        else:
            print("  Bash: export OPENAI_API_KEY=\"sk-...\"")
        return False


def main():
    """Run setup checks."""
    print("=" * 80)
    print("EMAIL ROUTING BENCHMARK - SETUP VERIFICATION")
    print("=" * 80 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("uv Installation", check_uv),
        ("Dependencies", check_dependencies),
        ("OpenAI API Key", check_openai_key)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"\nChecking {check_name}:")
        print("-" * 40)
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 80)
    if all_passed:
        print("✓ Setup verification complete! Ready to run benchmark.")
        print("\nRun with:")
        print("  Interactive mode: uv run python email_routing_benchmark.py")
        print("  Batch mode:       uv run python email_routing_benchmark_batch.py")
        print("  Analysis only:    uv run python analyze_results.py benchmark_results.json")
    else:
        print("❌ Setup verification failed. Please fix the issues above.")
        sys.exit(1)
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
