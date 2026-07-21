# Airline Email Routing Benchmark - Prompt Engineering Optimization

## Overview
This solution benchmarks two ChatGPT models (GPT-3.5-turbo and GPT-4-turbo-preview) on their ability to classify airline customer support emails into appropriate specialized teams using different prompting techniques.

## Task Description
### Domain
**Airline Customer Support Email Routing** - Automatically route incoming emails from airline customers to specialized teams:
- **Reservations & Ticketing**: Name changes, upgrades, cancellations
- **Baggage & Lost & Found**: Delayed/damaged baggage, lost items, emergency purchases
- **Refunds & Compensation**: EU261 compensation claims, refunds
- **Frequent Flyer Program (Loyalty)**: Miles, points, status tier issues
- **Special Assistance**: Wheelchairs, service animals, medical equipment, unaccompanied minors

### Prompting Techniques Tested
1. **Zero-shot**: Direct instruction without examples
2. **One-shot**: Single example provided
3. **Few-shot**: Multiple examples (3) provided

## Installation

### Prerequisites
- Python 3.8+
- OpenAI API key with access to GPT models

### Setup

1. Install dependencies using uv:
```bash
uv sync
```

   If `uv` is not installed:
   ```bash
   pip install uv
   ```

2. Create a `.env` file with your OpenAI API key:
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your API key
   OPENAI_API_KEY=sk-your-actual-key-here
   ```
   
   Or set the environment variable directly (see QUICKSTART.md)

## Running the Benchmark

Execute the benchmark script:
```bash
python email_routing_benchmark.py
```

### Interactive Usage
The script will:
1. Test each email with each model and technique combination
2. Display the email content and expected category
3. Show the model's prediction
4. **Prompt you to rate the quality** of the prediction (0-2 scale):
   - **2**: Detailed, correct, coherent answer
   - **1**: Partial/low-effort answer with missing pieces
   - **0**: Incorrect or irrelevant response
5. Press Enter to use automatic scoring based on correctness
6. Save results to Excel when complete

## Output

The script generates **email_routing_benchmark_results.xlsx** with the following sheets:

### 1. Detailed Results
- Every individual test with full details
- Email content, expected category, predicted category
- Correctness and quality scores

### 2. Summary Analysis
- Accuracy percentage for each model/technique combination
- Average quality scores
- Total tests per combination

### 3. Model Comparison
- Matrix comparing accuracy across techniques for each model
- Side-by-side comparison of model performance

### 4. Analysis & Insights
- Best performing model/technique combination
- Overall model performance statistics
- Technique effectiveness analysis

## Benchmark Configuration

### Test Emails
8 test emails covering:
- Reservations & Ticketing (2 emails)
- Baggage & Lost & Found (2 emails)
- Refunds & Compensation (2 emails)
- Frequent Flyer Program (1 email)
- Special Assistance (1 email)

### Models Tested
- **gpt-3.5-turbo**: Faster, more efficient
- **gpt-4-turbo-preview**: More advanced reasoning

### Scoring Scale
Quality scores range from 0-2 per prompt:
- Correct classification with clear reasoning = 2 points
- Partial correct or unclear answer = 1 point
- Incorrect or refused response = 0 points

## Expected Output Structure

```
Results Summary:
├── Model Performance
│   ├── GPT-3.5: Accuracy %, Avg Score
│   └── GPT-4: Accuracy %, Avg Score
├── Technique Effectiveness
│   ├── Zero-shot: Accuracy %
│   ├── One-shot: Accuracy %
│   └── Few-shot: Accuracy %
└── Best Combination
    └── Model + Technique with highest accuracy
```

## Key Findings Expected

Based on prompt engineering research:
- **Few-shot** prompting typically outperforms zero-shot
- **GPT-4** generally shows better performance than GPT-3.5
- Domain-specific examples improve classification accuracy
- Few-shot prompting provides best balance of accuracy and cost

## Methodology Reference

This benchmark follows the evaluation framework from:
- Prompt Engineering Techniques: Materials from `aide-rdcz-5/2_promp_engineering/1_prompt_engineering/1_types/`
- Benchmarking Approach: Guide from `aide-rdcz-5/2_promp_engineering/2_benchmarking/manual/my_uncensored/`

## Customization

### Adding More Test Emails
Modify the `TEST_EMAILS` list in `email_routing_benchmark.py`:
```python
TEST_EMAILS = [
    {
        "id": "email_XXX",
        "content": "Your email content here",
        "expected_category": "Category Name"
    },
    ...
]
```

### Changing Models
Modify the `models` list in `run_benchmark_interactive()`:
```python
models = ["gpt-3.5-turbo", "gpt-4-turbo-preview"]  # Change as needed
```

### Adjusting Prompting Examples
Modify `ONE_SHOT_EXAMPLES` and `FEW_SHOT_EXAMPLES` dictionaries to test different examples.

## Cost Estimation

Approximate API call costs:
- Per test: ~0.01-0.05 USD (varies by model)
- Full benchmark (8 emails × 2 models × 3 techniques): ~$2-5 USD

## Troubleshooting

### "API key not found"
- Ensure OPENAI_API_KEY environment variable is set
- Verify the key is correct and account has available credits

### "Model not found"
- Check if models are available in your account region
- Consider using `gpt-3.5-turbo` and `gpt-4` instead

### "Rate limit exceeded"
- Add delays between requests
- Reduce number of parallel API calls

## Next Steps

1. Run the benchmark in interactive mode
2. Review the generated Excel file
3. Analyze results across models and techniques
4. Document findings about optimal prompting approach
5. Consider fine-tuning the best-performing model/technique combination for production use

## License
Homework submission for AI Engineering Training

---
**Generated**: 2024
**Domain**: Airline Customer Support Email Routing
**Models**: GPT-3.5-turbo, GPT-4-turbo-preview
**Techniques**: Zero-shot, One-shot, Few-shot
