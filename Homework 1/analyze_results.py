"""
Utility script for analyzing benchmark results and generating reports.
"""

import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment


def load_results(filename):
    """Load results from JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)


def generate_comparison_report(results):
    """Generate detailed comparison report."""
    
    print("\n" + "=" * 80)
    print("BENCHMARK ANALYSIS REPORT")
    print("=" * 80 + "\n")
    
    # Group by model
    models = set(r["model"] for r in results)
    techniques = set(r["technique"] for r in results)
    
    for model in sorted(models):
        print(f"\n{'─' * 80}")
        print(f"Model: {model.upper()}")
        print(f"{'─' * 80}")
        
        model_results = [r for r in results if r["model"] == model]
        
        total_correct = sum(1 for r in model_results if r["is_correct"])
        total_score = sum(r["quality_score"] for r in model_results)
        
        print(f"\nOverall Performance:")
        print(f"  • Total tests: {len(model_results)}")
        print(f"  • Correct: {total_correct} ({total_correct/len(model_results)*100:.1f}%)")
        print(f"  • Average quality score: {total_score/len(model_results):.2f}")
        
        print(f"\nBreakdown by Technique:")
        for technique in sorted(techniques):
            technique_results = [r for r in model_results if r["technique"] == technique]
            if technique_results:
                correct = sum(1 for r in technique_results if r["is_correct"])
                score = sum(r["quality_score"] for r in technique_results)
                print(f"  • {technique:12s}: {correct:2d}/{len(technique_results)} correct ({correct/len(technique_results)*100:5.1f}%), avg score: {score/len(technique_results):.2f}")
    
    # Cross-model comparison
    print(f"\n{'─' * 80}")
    print("CROSS-MODEL COMPARISON")
    print(f"{'─' * 80}\n")
    
    comparison_data = {}
    for model in sorted(models):
        model_results = [r for r in results if r["model"] == model]
        correct = sum(1 for r in model_results if r["is_correct"])
        accuracy = correct / len(model_results) * 100
        avg_score = sum(r["quality_score"] for r in model_results) / len(model_results)
        
        comparison_data[model] = {
            "accuracy": accuracy,
            "avg_score": avg_score,
            "correct": correct,
            "total": len(model_results)
        }
        
        print(f"{model:25s}: {accuracy:5.1f}% accuracy, {avg_score:.2f} avg score")
    
    # Best technique analysis
    print(f"\n{'─' * 80}")
    print("TECHNIQUE EFFECTIVENESS")
    print(f"{'─' * 80}\n")
    
    technique_data = {}
    for technique in sorted(techniques):
        technique_results = [r for r in results if r["technique"] == technique]
        correct = sum(1 for r in technique_results if r["is_correct"])
        accuracy = correct / len(technique_results) * 100
        avg_score = sum(r["quality_score"] for r in technique_results) / len(technique_results)
        
        technique_data[technique] = {
            "accuracy": accuracy,
            "avg_score": avg_score,
            "correct": correct,
            "total": len(technique_results)
        }
        
        print(f"{technique:15s}: {accuracy:5.1f}% accuracy, {avg_score:.2f} avg score")
    
    # Best combination
    print(f"\n{'─' * 80}")
    print("BEST COMBINATION")
    print(f"{'─' * 80}\n")
    
    best_combo = None
    best_score = -1
    
    for model in models:
        for technique in techniques:
            combo_results = [r for r in results 
                           if r["model"] == model and r["technique"] == technique]
            if combo_results:
                combo_score = sum(r["quality_score"] for r in combo_results) / len(combo_results)
                if combo_score > best_score:
                    best_score = combo_score
                    best_combo = (model, technique)
    
    if best_combo:
        model, technique = best_combo
        combo_results = [r for r in results 
                        if r["model"] == model and r["technique"] == technique]
        correct = sum(1 for r in combo_results if r["is_correct"])
        accuracy = correct / len(combo_results) * 100
        
        print(f"Best: {model} + {technique}")
        print(f"  • Accuracy: {accuracy:.1f}%")
        print(f"  • Average Quality Score: {best_score:.2f}")
    
    # Category-wise analysis
    print(f"\n{'─' * 80}")
    print("PERFORMANCE BY SUPPORT CATEGORY")
    print(f"{'─' * 80}\n")
    
    categories = set(r["expected_category"] for r in results)
    for category in sorted(categories):
        category_results = [r for r in results if r["expected_category"] == category]
        correct = sum(1 for r in category_results if r["is_correct"])
        accuracy = correct / len(category_results) * 100
        
        print(f"{category:35s}: {correct:2d}/{len(category_results)} ({accuracy:5.1f}%)")


def main():
    """Main function."""
    
    import sys
    
    if len(sys.argv) > 1:
        results_file = sys.argv[1]
    else:
        results_file = "benchmark_results.json"
    
    try:
        results = load_results(results_file)
        generate_comparison_report(results)
        print("\n" + "=" * 80)
        print("Report generation complete!")
        print("=" * 80 + "\n")
    except FileNotFoundError:
        print(f"Error: Results file '{results_file}' not found.")
        print("Run email_routing_benchmark_batch.py first to generate results.")


if __name__ == "__main__":
    main()
