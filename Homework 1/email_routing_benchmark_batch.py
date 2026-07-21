"""
Non-interactive batch benchmarking script for automated testing.
Useful for running complete benchmarks without user interaction.
"""

import os
import json
from email_routing_benchmark import (
    call_gpt_model, create_zero_shot_prompt, create_one_shot_prompt,
    create_few_shot_prompt, TEST_EMAILS, is_correct_classification,
    export_to_excel, datetime, test_connection
)


def run_batch_benchmark():
    """Run non-interactive benchmark with automatic scoring."""
    
    results = []
    models = ["gpt-3.5-turbo", "gpt-4-turbo-preview"]
    techniques = ["zero-shot", "one-shot", "few-shot"]
    
    print("=" * 80)
    print("BATCH BENCHMARK (NON-INTERACTIVE MODE)")
    print("=" * 80)
    print(f"\nTesting {len(models)} models across {len(techniques)} techniques")
    print(f"Total test emails: {len(TEST_EMAILS)}\n")
    
    total_tests = len(models) * len(techniques) * len(TEST_EMAILS)
    current_test = 0
    
    for model in models:
        print(f"\n{'='*80}")
        print(f"Model: {model}")
        print(f"{'='*80}\n")
        
        for technique in techniques:
            print(f"\nTechnique: {technique.upper()}")
            print("-" * 40)
            
            for email in TEST_EMAILS:
                current_test += 1
                
                # Create prompt based on technique
                if technique == "zero-shot":
                    prompt = create_zero_shot_prompt(email["content"])
                elif technique == "one-shot":
                    prompt = create_one_shot_prompt(email["content"])
                else:  # few-shot
                    prompt = create_few_shot_prompt(email["content"])
                
                # Call the model
                print(f"[{current_test}/{total_tests}] {email['id']}... ", end="", flush=True)
                prediction = call_gpt_model(model, prompt)
                
                # Auto-score: 2 if correct, 0 if incorrect
                is_correct = is_correct_classification(prediction, email["expected_category"])
                quality_score = 2 if is_correct else 0
                
                print(f"{'✓' if is_correct else '✗'}")
                
                # Store result
                result = {
                    "model": model,
                    "technique": technique,
                    "email_id": email["id"],
                    "email_content": email["content"],
                    "expected_category": email["expected_category"],
                    "predicted_category": prediction,
                    "is_correct": is_correct,
                    "quality_score": quality_score,
                    "timestamp": datetime.now().isoformat()
                }
                results.append(result)
    
    return results


def save_json_results(results, filename="benchmark_results.json"):
    """Save results as JSON for further processing."""
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n✓ JSON results saved to: {filename}")


def main():
    """Main function."""
    print("\nStarting Batch Email Routing Benchmark...\n")
    
    # Test connection first
    if not test_connection():
        print("\n❌ Cannot proceed. Please fix the connection issue above.")
        return
    
    # Run batch benchmark
    results = run_batch_benchmark()
    
    print(f"\n{'='*80}")
    print(f"BATCH BENCHMARK COMPLETE")
    print(f"Total tests: {len(results)}")
    print(f"{'='*80}\n")
    
    # Save JSON results
    save_json_results(results)
    
    # Export to Excel
    output_file = export_to_excel(results)
    
    print("\nBatch benchmark complete! Results exported to Excel and JSON.")


if __name__ == "__main__":
    main()
