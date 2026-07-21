# Homework 3: GPT-4 Model Fine-tuning and Benchmarking

## 📋 Overview

This project implements a complete pipeline for fine-tuning OpenAI's GPT-4 model on hotel booking policy data and benchmarking the results against the base model.

### Project Structure

```
Homework 3/
├── main.py                         # Main execution script
├── finetune_openai.py             # Fine-tuning implementation
├── benchmark_models.py            # Benchmark comparison
├── generate_excel_report.py       # Excel report generator
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── hotel_booking_finetuning/      # Dataset directory
│   └── openai_format/
│       ├── train.jsonl           # Training data
│       └── validation.jsonl      # Validation/test data
└── Hotel Booking terms.md        # Source policy document
```

## 🎯 Objectives

1. **Fine-tune** GPT-4 model on hotel booking policy Q&A dataset
2. **Benchmark** the fine-tuned model against the base model
3. **Evaluate** performance improvements using LLM-as-judge methodology
4. **Report** results in a comprehensive Excel spreadsheet

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher (Python 3.12 recommended)
- **uv** (recommended) - [Install uv](https://docs.astral.sh/uv/getting-started/installation/) - See [UV_GUIDE.md](UV_GUIDE.md) for details
  - Or use pip as an alternative
- OpenAI API key with access to fine-tuning
- Sufficient API credits (fine-tuning costs depend on dataset size)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd "C:\Users\Admin\Documents\Training\AI Engineering\AI-Engineering-Training\Homework 3"
   ```

2. **Install dependencies using uv:**
   ```bash
   uv sync
   ```
   
   **Or using pip (alternative):**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your OpenAI API key:**
   
   **Recommended: Create a `.env` file** (already loaded automatically):
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your API key:
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```
   
   **Alternative: Set environment variable manually:**
   
   Windows PowerShell:
   ```powershell
   $env:OPENAI_API_KEY = "sk-your-api-key-here"
   ```
   
   Windows Command Prompt:
   ```cmd
   set OPENAI_API_KEY=sk-your-api-key-here
   ```
   
   Unix/Mac:
   ```bash
   export OPENAI_API_KEY='sk-your-api-key-here'
   ```

### Running the Complete Pipeline

Using uv (recommended):
```bash
uv run main.py
```

Or using standard Python:
```bash
python main.py
```

Select option `1` to run the complete pipeline:
- Fine-tune the model
- Run benchmark comparison
- Generate Excel report

## 📊 Pipeline Steps

### Step 1: Fine-tuning

The `finetune_openai.py` script:
1. Uploads training data to OpenAI
2. Uploads validation data (optional)
3. Creates a fine-tuning job
4. Monitors the job until completion
5. Saves the fine-tuned model ID

**Model Used:** `gpt-4o-mini-2024-07-18` (more cost-effective alternative to GPT-4)

**Expected Duration:** 10-30 minutes (depends on dataset size and queue)

### Step 2: Benchmarking

The `benchmark_models.py` script:
1. Loads test cases from validation set
2. Gets responses from both base and fine-tuned models
3. Evaluates responses using GPT-4 as a judge
4. Calculates performance metrics
5. Saves detailed results to JSON

**Evaluation Criteria:**
- Accuracy: Does it provide correct information?
- Completeness: Does it cover key points?
- Clarity: Is it well-structured?
- Relevance: Does it directly answer the question?

**Scoring:** 0-10 scale per response

### Step 3: Excel Report Generation

The `generate_excel_report.py` script creates a comprehensive Excel workbook with three sheets:

1. **Summary Sheet:**
   - Model information
   - Performance metrics
   - Key findings
   - Improvement analysis

2. **Detailed Results Sheet:**
   - Question-by-question comparison
   - Full responses from both models
   - Individual scores
   - Improvement per question
   - Color-coded performance

3. **Score Comparison Sheet:**
   - Side-by-side score comparison
   - Quick overview of all test cases

**Output File:** `Homework3_Benchmark_Results.xlsx`

## 📈 Understanding the Results

### Score Color Coding

- **Green (8-10):** Excellent response
- **Yellow (5-7):** Good response with minor issues
- **Red (0-4):** Poor or incorrect response
- **Bright Green (Improvement):** Fine-tuned model performed better

### Key Metrics

- **Average Base Score:** Performance of the base model
- **Average Fine-tuned Score:** Performance after fine-tuning
- **Average Improvement:** Absolute improvement in points
- **Improvement Percentage:** Relative improvement

### Expected Improvements

Fine-tuning should provide:
- More accurate policy information
- Consistent terminology usage
- Better handling of edge cases
- More contextually appropriate responses

## 🔧 Individual Script Usage

### Fine-tuning Only
```bash
uv run finetune_openai.py
```

### Benchmarking Only (after fine-tuning)
```bash
uv run benchmark_models.py
```

### Report Generation Only (after benchmarking)
```bash
uv run generate_excel_report.py
```

## 💰 Cost Considerations

### Fine-tuning Costs (approximate)
- Training: ~$0.008 per 1K tokens
- Validation: ~$0.008 per 1K tokens

### Inference Costs
- Base model: Standard API rates
- Fine-tuned model: ~$0.012 per 1K tokens

**Estimated Total Cost:** $5-$15 depending on dataset size and benchmark test cases

## 🐛 Troubleshooting

### Common Issues

1. **"API key not found"**
   - Ensure OPENAI_API_KEY is set correctly
   - Check for typos in the key

2. **"Training file not found"**
   - Verify the dataset exists in `hotel_booking_finetuning/openai_format/`
   - Check file paths are correct

3. **"Fine-tuning failed"**
   - Check API credits/billing
   - Verify data format is correct (JSONL with "messages" key)
   - Ensure minimum dataset size requirements

4. **"Rate limit exceeded"**
   - Add delays between API calls
   - Reduce benchmark test case count

5. **"uv command not found"**
   - Install uv: `pip install uv` or visit https://docs.astral.sh/uv/
   - Or use standard pip commands instead

## 📚 Dataset Information

**Dataset:** Hotel Booking Policy Q&A

**Format:** OpenAI Chat Completion format
```json
{
  "messages": [
    {"role": "system", "content": "System prompt"},
    {"role": "user", "content": "User question"},
    {"role": "assistant", "content": "Expected answer"}
  ]
}
```

**Training Set:** Questions about hotel booking terms, cancellation policies, payment methods, etc.

**Validation Set:** Held-out questions for benchmark evaluation

## 📝 Assignment Submission

The final deliverable is:

**File:** `Homework3_Benchmark_Results.xlsx`

This Excel file contains:
- Summary of model performance
- Detailed comparison of all test cases
- Scoring and evaluation metrics
- Visual indicators of improvement

## 🎓 Learning Outcomes

This project demonstrates:
1. ✅ Fine-tuning LLMs for domain-specific tasks
2. ✅ Evaluating model performance objectively
3. ✅ Using LLM-as-judge for automated evaluation
4. ✅ Comparing base vs fine-tuned models
5. ✅ Creating professional reports with data visualization

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review OpenAI documentation: https://platform.openai.com/docs/guides/fine-tuning
3. Verify all dependencies are installed correctly

## 📄 License

This is an educational project for AI Engineering Training coursework.

---

**Author:** AI Engineering Student  
**Course:** Homework 3 - Model Fine-tuning  
**Date:** 2026-07-20
