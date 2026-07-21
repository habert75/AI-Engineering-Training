# 🔄 Workflow Diagram

## Complete Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    HOMEWORK 3 SOLUTION                          │
│              GPT-4 Fine-tuning & Benchmarking                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STEP 0: SETUP                                                   │
├─────────────────────────────────────────────────────────────────┤
│ 1. uv sync  (or pip install -r requirements.txt)               │
│ 2. Create .env file with OPENAI_API_KEY=sk-your-key            │
│ 3. Run: uv run verify_setup.py                                  │
│ 4. Test: uv run test_env.py (optional)                          │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: FINE-TUNING (finetune_openai.py)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Input:  hotel_booking_finetuning/openai_format/               │
│          ├── train.jsonl                                        │
│          └── validation.jsonl                                   │
│                                                                 │
│  Process:                                                       │
│  1. Upload training file to OpenAI      ⏱ ~1 min              │
│  2. Upload validation file              ⏱ ~1 min              │
│  3. Create fine-tuning job              ⏱ ~1 min              │
│  4. Wait for completion                 ⏱ ~10-30 min          │
│                                                                 │
│  Output: finetune_results.json                                  │
│          ├── fine_tuned_model: "ft:gpt-4o-mini-...:..."       │
│          ├── job_id: "ftjob-..."                               │
│          ├── training_file_id: "file-..."                      │
│          └── validation_file_id: "file-..."                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: BENCHMARKING (benchmark_models.py)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Input:  finetune_results.json                                  │
│          validation.jsonl (test cases)                          │
│                                                                 │
│  Process: For each test case:                                   │
│  ┌────────────────────────────────────────────────┐            │
│  │ Question → Base Model → Response → Score       │            │
│  │            (gpt-4o-mini-2024-07-18)   ↓       │            │
│  │                                  LLM Judge     │            │
│  │                                  (GPT-4o-mini) │            │
│  └────────────────────────────────────────────────┘            │
│  ┌────────────────────────────────────────────────┐            │
│  │ Question → Fine-tuned Model → Response → Score │            │
│  │            (ft:gpt-4o-mini-...)        ↓       │            │
│  │                                  LLM Judge     │            │
│  │                                  (GPT-4o-mini) │            │
│  └────────────────────────────────────────────────┘            │
│                                                                 │
│  Metrics Calculated:                                            │
│  ├── Average base score                                         │
│  ├── Average fine-tuned score                                   │
│  ├── Average improvement                                        │
│  └── Improvement percentage                                     │
│                                                                 │
│  Output: benchmark_results.json                                 │
│          ├── summary (metrics)                                  │
│          ├── results (per-question details)                     │
│          └── timestamp                                          │
│                                                                 │
│  Time: ⏱ ~5-15 minutes                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: EXCEL REPORT (generate_excel_report.py)                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Input: benchmark_results.json                                  │
│                                                                 │
│  Process:                                                       │
│  ├── Create "Summary" sheet                                     │
│  │   ├── Model information                                      │
│  │   ├── Performance metrics                                    │
│  │   └── Key findings                                           │
│  │                                                              │
│  ├── Create "Detailed Results" sheet                            │
│  │   ├── All questions                                          │
│  │   ├── Expected vs actual responses                           │
│  │   ├── Scores (color-coded)                                   │
│  │   └── Improvement indicators                                 │
│  │                                                              │
│  └── Create "Score Comparison" sheet                            │
│      ├── Side-by-side scores                                    │
│      └── Visual comparison                                      │
│                                                                 │
│  Output: Homework3_Benchmark_Results.xlsx ⭐                    │
│                                                                 │
│  Time: ⏱ ~1 minute                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ 🎉 FINAL OUTPUT                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📄 Homework3_Benchmark_Results.xlsx                            │
│                                                                 │
│  ┌──────────────────────────────────────────────┐              │
│  │ Sheet 1: Summary                             │              │
│  │ ╔════════════════════════════════════════╗   │              │
│  │ ║ GPT-4 Fine-tuning Benchmark Results    ║   │              │
│  │ ╠════════════════════════════════════════╣   │              │
│  │ ║ Base Model:     gpt-4o-mini-2024-07-18 ║   │              │
│  │ ║ Fine-tuned:     ft:gpt-4o-mini-...     ║   │              │
│  │ ║                                         ║   │              │
│  │ ║ Avg Base Score:        7.2/10          ║   │              │
│  │ ║ Avg Fine-tuned Score:  8.9/10          ║   │              │
│  │ ║ Improvement:          +1.7 (23.6%)     ║   │              │
│  │ ╚════════════════════════════════════════╝   │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
│  ┌──────────────────────────────────────────────┐              │
│  │ Sheet 2: Detailed Results                    │              │
│  │ All questions with full responses            │              │
│  │ Color-coded scores                           │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
│  ┌──────────────────────────────────────────────┐              │
│  │ Sheet 3: Score Comparison                    │              │
│  │ Quick score overview                         │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
│  👉 SUBMIT THIS FILE! 👈                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 📊 Color Coding Legend

```
Score Visualization in Excel:

🟢 Green (8-10)   → Excellent response
🟡 Yellow (5-7)   → Good response
🔴 Red (0-4)      → Poor response
💚 Bright Green   → Improvement indicator
```

## 📁 File Structure

```
Homework 3/
│
├── 🔧 Setup & Configuration
│   ├── requirements.txt           # Dependencies
│   ├── .env.example              # API key template
│   └── verify_setup.py           # Verification script
│
├── 📜 Core Scripts
│   ├── main.py                   # Main execution
│   ├── finetune_openai.py       # Fine-tuning
│   ├── benchmark_models.py      # Benchmarking
│   └── generate_excel_report.py # Report generation
│
├── 📚 Documentation
│   ├── README.md                 # Full documentation
│   ├── QUICKSTART.md             # Quick guide
│   ├── IMPLEMENTATION_SUMMARY.md # Summary
│   └── WORKFLOW.md               # This file
│
├── 📊 Data
│   └── hotel_booking_finetuning/
│       └── openai_format/
│           ├── train.jsonl       # Training data
│           └── validation.jsonl  # Test data
│
└── 📈 Output (Generated)
    ├── finetune_results.json     # Fine-tuning output
    ├── benchmark_results.json    # Benchmark output
    └── Homework3_Benchmark_Results.xlsx ⭐ SUBMIT
```

## 🎮 Command Reference

### Quick Commands (using uv - recommended)

```bash
# Full pipeline
uv run main.py

# Individual steps
uv run finetune_openai.py
uv run benchmark_models.py
uv run generate_excel_report.py

# Verification
uv run verify_setup.py
```

### Alternative Commands (using standard Python)

```bash
# Full pipeline
python main.py

# Individual steps
python finetune_openai.py
python benchmark_models.py
python generate_excel_report.py

# Verification
python verify_setup.py
```

### Setup Commands

```bash
# Install dependencies with uv (recommended)
uv sync

# Or install with pip
pip install -r requirements.txt

# Set API key (Windows PowerShell)
$env:OPENAI_API_KEY = "sk-..."

# Set API key (Unix/Mac)
export OPENAI_API_KEY="sk-..."
```

## ⏱️ Timeline

```
Minute 0:  Start setup
Minute 5:  Dependencies installed, API key set
Minute 6:  Run main.py, select option 1
Minute 7:  Training data uploaded
Minute 8:  Validation data uploaded
Minute 9:  Fine-tuning job started
...
Minute 30: Fine-tuning complete
Minute 31: Benchmark started
Minute 35: All test cases evaluated
Minute 36: Excel report generated
Minute 37: 🎉 DONE! Submit the Excel file
```

## 💡 Pro Tips

1. **Run verify_setup.py first** - catches issues early
2. **Monitor costs** - check OpenAI dashboard during pipeline
3. **Backup results** - save JSON files for future reference
4. **Check Excel** - review all 3 sheets before submitting
5. **Document changes** - if you modify test cases

## 🔄 Restart Points

If something fails:

```
Failed at fine-tuning?
→ Fix issue, run: uv run finetune_openai.py

Failed at benchmark?
→ Fix issue, run: uv run benchmark_models.py

Need to regenerate Excel?
→ Run: uv run generate_excel_report.py
```

---

**Ready?** Let's get started! 🚀

```bash
uv sync                  # Install dependencies
uv run verify_setup.py   # Verify
uv run main.py           # Execute
```
