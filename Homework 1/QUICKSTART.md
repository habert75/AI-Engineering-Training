# Quick Start Guide

## Setup Steps

### 1. Install Dependencies (using uv)
```bash
uv sync
```

If you don't have `uv` installed:
```bash
pip install uv
```

### 2. Set OpenAI API Key

Create a `.env` file in the project root directory (copy from `.env.example`):

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Then edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

**Alternative:** Set as environment variable:

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-your-key-here"
```

**Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=sk-your-key-here
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

### 3. Verify Setup
```bash
uv run python setup_verify.py
```

## Running the Benchmark

### Option 1: Interactive Mode (Recommended)
```bash
uv run python email_routing_benchmark.py
```
- Tests each email one by one
- Displays predictions and expected categories
- **Prompts you to rate quality** (0-2 scale)
- Generate Excel report with analysis

### Option 2: Batch Mode (Automated)
```bash
uv run python email_routing_benchmark_batch.py
```
- Runs automatically without interaction
- Auto-scores based on correctness (2 if correct, 0 if not)
- Generates Excel and JSON results
- Faster for full benchmarks

### Option 3: Analyze Results
```bash
uv run python analyze_results.py benchmark_results.json
```
- Generates detailed comparison report
- Shows model and technique performance
- Identifies best combinations

## Output Files

After running the benchmark, you'll get:

1. **email_routing_benchmark_results.xlsx** - Main results file with 4 sheets:
   - Detailed Results: Every test outcome
   - Summary Analysis: Accuracy and scores by model/technique
   - Model Comparison: Side-by-side accuracy matrix
   - Analysis & Insights: Key findings

2. **benchmark_results.json** (batch mode only) - Raw results in JSON format

## Expected Results

The benchmark will show:
- Which model performs better (GPT-3.5 vs GPT-4)
- Which prompting technique is most effective (zero/one/few-shot)
- Accuracy by support category
- Best combination for production use

## Typical Performance

Expected ranges:
- **Accuracy**: 60-90% depending on model and technique
- **Few-shot**: Generally 10-20% better than zero-shot
- **GPT-4**: Typically 5-15% better than GPT-3.5

## Using uv

`uv` is a fast Python package and project manager written in Rust.

**Basic commands:**
- `uv sync` - Install dependencies from pyproject.toml
- `uv run python script.py` - Run Python scripts with managed environment
- `uv add package` - Add new dependencies
- `uv remove package` - Remove dependencies

## Example Session

```
[1/48] Testing email_001... Predicted: Reservations & Ticketing [40...]... ✓
  Expected: Reservations & Ticketing
  Enter quality score (0-2, or press Enter for auto): 2

[2/48] Testing email_002... Predicted: Baggage & Lost & Found... ✓
  Expected: Baggage & Lost & Found
  Enter quality score (0-2, or press Enter for auto): 
```

## Troubleshooting

### "API key not found"
1. Make sure you've set the OPENAI_API_KEY environment variable
2. Restart your terminal/IDE
3. Check the key is valid and has credits

### "Model not available"
Use different models:
- Instead of `gpt-4-turbo-preview`: try `gpt-4`
- Instead of `gpt-3.5-turbo`: try `gpt-3.5-turbo-instruct`

### "Rate limit exceeded"
- Wait a minute or two before retrying
- Reduce number of models or tests
- Consider using batch mode with delays

## Cost Estimation

Approximate costs:
- Per complete benchmark: $2-5 USD
- Per test: $0.01-0.05 USD
- You can set spending limits in OpenAI console

## IMPORTANT Notes

1. **Rating Quality**: In interactive mode, your ratings affect results
   - 2 = Correct and clear
   - 1 = Partial or unclear
   - 0 = Incorrect or refused
   
2. **Temperature**: Set to 0.7 for fairness and reproducibility

3. **API Limits**: Different model versions may not be available in all regions

4. **Data Privacy**: Email content is sent to OpenAI API

---
For full documentation, see README.md
