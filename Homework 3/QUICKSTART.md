# Quick Start Guide - Homework 3

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
Using **uv** (recommended):
```bash
uv sync
```

Or using **pip** (alternative):
```bash
pip install -r requirements.txt
```

### Step 2: Set Your API Key
**Recommended: Use `.env` file** (automatically loaded):
```bash
# Copy and edit the .env file
cp .env.example .env

# Add your API key to .env:
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Alternative: Environment variable:**
```powershell
$env:OPENAI_API_KEY = "sk-your-api-key-here"
```

### Step 3: Run the Pipeline
Using **uv** (recommended):
```bash
uv run verify_setup.py   # Verify everything is ready
uv run main.py           # Run the complete pipeline
```

Or using **standard Python**:
```bash
python verify_setup.py   # Verify everything is ready
python main.py           # Run the complete pipeline
```

---

## 📋 What Will Happen?

1. **Fine-tuning** (~10-30 minutes)
   - Uploads your training data
   - Creates fine-tuning job
   - Waits for completion
   - Saves model ID

2. **Benchmarking** (~5-10 minutes)
   - Tests both models
   - Uses GPT-4 to evaluate responses
   - Calculates improvement scores

3. **Report Generation** (~1 minute)
   - Creates Excel file with 3 sheets
   - Color-coded results
   - Summary statistics

---

## 📊 Final Output

**File:** `Homework3_Benchmark_Results.xlsx`

This is your submission file containing:
- ✅ Summary statistics
- ✅ Detailed comparisons
- ✅ Score evaluations
- ✅ Improvement analysis

---

## 💡 Tips

- **Cost:** Expect $5-$15 total (depending on dataset size)
- **Time:** Allow 30-60 minutes for complete pipeline
- **Internet:** Stable connection required
- **API Credits:** Ensure you have sufficient credits

---

## ❓ Need Help?

1. Run `python verify_setup.py` to check for issues
2. Check [README.md](README.md) for detailed documentation
3. Review troubleshooting section in README

---

## 📝 What to Submit

Submit the generated file:
```
Homework3_Benchmark_Results.xlsx
```

This Excel file contains all required information:
- Model comparison
- Benchmark scores
- Performance evaluation

---

**That's it!** Simple and straightforward. 🎉
