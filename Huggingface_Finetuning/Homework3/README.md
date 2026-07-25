# Homework 3 — Fine-tuning Benchmark

## What this does

Compares **google/gemma-4-E4B-it** (base) against the LoRA-adapted version
**habert75/autogen-gemma4-4bit-lora-adapter** (fine-tuned on hotel policies).

Two test sets:
| Set | # Questions | Purpose |
|---|---|---|
| **Hotel Policy** | 10 | Domain knowledge — FT model expected to score higher |
| **General / Moral** | 5  | Sanity check — both models should score similarly |

Output: `benchmark_results.xlsx` with:
- **Comparison** sheet — side-by-side answers + score per question
- **Summary** sheet — average scores by category and overall

## Run on RunPod (GPU)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run benchmark (takes ~5-10 min on L4)
python benchmark.py
```

## Run locally (CPU — slow)

```bash
pip install -r requirements.txt
python benchmark.py
# Expect ~5-10 min per question on CPU
```

## Scoring method

Each answer is scored by keyword matching against the hotel policy document.
Score = (keywords found / total keywords) × 100 %.

For general questions the keywords are common sense terms expected in a reasonable answer.

## Files

| File | Description |
|---|---|
| `benchmark.py` | Main benchmark script |
| `requirements.txt` | Python dependencies |
| `Hotel Booking terms.md` | Source hotel policy document |
| `benchmark_results.xlsx` | Generated after running benchmark.py |
| `Task.txt` | Original assignment |
| `instructions.txt` | Solution instructions |
