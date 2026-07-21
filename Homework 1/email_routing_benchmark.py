"""
Airline Email Routing Benchmark - Prompt Engineering Optimization
Benchmarks 2 ChatGPT models (gpt-3.5-turbo, gpt-4-turbo-preview) using 
zero-shot, one-shot, and few-shot prompting techniques for email classification.
"""

import os
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Please set it in your .env file or environment variables.")
client = OpenAI(api_key=api_key)

# Define support categories
SUPPORT_CATEGORIES = {
    "Reservations & Ticketing": "Emails about changing names on tickets, correcting spelling errors, upgrading to business class, or canceling a booking for a voucher.",
    "Baggage & Lost & Found": "Emails about delayed baggage, damaged luggage, lost items left on the plane, or claims for reimbursement for emergency purchases.",
    "Refunds & Compensation": "Emails requesting monetary compensation (EU261 rules), refunds for canceled flights, or disputed credit card charges.",
    "Frequent Flyer Program (Loyalty)": "Emails about missing miles, redeeming points for flights, or status tier matching.",
    "Special Assistance": "Emails about wheelchair assistance, traveling with service animals, unaccompanied minors, or passengers needing extra oxygen/medical equipment."
}

# Test emails for benchmarking
TEST_EMAILS = [
    {
        "id": "email_001",
        "content": "I want to upgrade my ticket but my miles aren't showing up in my account.",
        "expected_category": "Frequent Flyer Program (Loyalty)"
    },
    {
        "id": "email_002",
        "content": "I need a refund because I can't find my booking confirmation anywhere.",
        "expected_category": "Reservations & Ticketing"
    },
    {
        "id": "email_003",
        "content": "My elderly father needs help but I need to change his ticket first.",
        "expected_category": "Reservations & Ticketing"
    },
    {
        "id": "email_004",
        "content": "I lost my bag and need compensation for the items inside.",
        "expected_category": "Baggage & Lost & Found"
    },
    {
        "id": "email_005",
        "content": "Can I use my points to pay for my wheelchair assistance fee?",
        "expected_category": "Special Assistance"
    },
    {
        "id": "email_006",
        "content": "I found someone else's medication in my suitcase after I got home.",
        "expected_category": "Baggage & Lost & Found"
    },
    {
        "id": "email_007",
        "content": "I want compensation but first I need to update my loyalty account details.",
        "expected_category": "Frequent Flyer Program (Loyalty)"
    },
    {
        "id": "email_008",
        "content": "My ticket says I'm upgraded to first class but I never requested this and don't want to pay extra.",
        "expected_category": "Reservations & Ticketing"
    },
    {
        "id": "email_009",
        "content": "I need to rebook my canceled flight using a voucher from a previous compensation.",
        "expected_category": "Reservations & Ticketing"
    },
    {
        "id": "email_010",
        "content": "Where do I report a missing item from my carry-on bag that I had during the flight?",
        "expected_category": "Baggage & Lost & Found"
    },
    {
        "id": "email_011",
        "content": "I was promised a refund in miles instead of money. How do I get those miles?",
        "expected_category": "Frequent Flyer Program (Loyalty)"
    },
    {
        "id": "email_012",
        "content": "My son needs oxygen during the flight and I need to change our seats to accommodate this.",
        "expected_category": "Special Assistance"
    },
    {
        "id": "email_013",
        "content": "Can I get a refund on the ticket I bought with miles?",
        "expected_category": "Reservations & Ticketing"
    },
    {
        "id": "email_014",
        "content": "I need special assistance but your website won't let me modify my existing reservation.",
        "expected_category": "Reservations & Ticketing"
    }
]

# One-shot example
ONE_SHOT_EXAMPLE = {
    "email": "I want to cancel my booking and get a voucher instead of a cash refund.",
    "category": "Reservations & Ticketing"
}

# Few-shot examples
FEW_SHOT_EXAMPLES = [
    {
        "email": "I want to cancel my booking and get a voucher instead of a cash refund.",
        "category": "Reservations & Ticketing"
    },
    {
        "email": "My bag was lost and I had to buy emergency clothes and toiletries. Can I be reimbursed?",
        "category": "Baggage & Lost & Found"
    },
    {
        "email": "I believe I'm eligible for compensation under EU261 for my delayed flight.",
        "category": "Refunds & Compensation"
    }
]


def create_zero_shot_prompt(email_content):
    """Create a zero-shot prompt for email classification."""
    categories_list = "\n".join([f"- {cat}" for cat in SUPPORT_CATEGORIES.keys()])
    
    prompt = f"""You are an email routing specialist for an airline. Your task is to classify incoming customer support emails into one of these categories:

{categories_list}

Email content:
{email_content}

Classify this email into one of the support categories above. Return ONLY the category name, nothing else."""
    
    return prompt


def create_one_shot_prompt(email_content):
    """Create a one-shot prompt for email classification."""
    categories_list = "\n".join([f"- {cat}" for cat in SUPPORT_CATEGORIES.keys()])
    
    prompt = f"""You are an email routing specialist for an airline. Your task is to classify incoming customer support emails into one of these categories:

{categories_list}

Example:
Email: {ONE_SHOT_EXAMPLE['email']}
Category: {ONE_SHOT_EXAMPLE['category']}

Now classify this email:
Email: {email_content}
Category:"""
    
    return prompt


def create_few_shot_prompt(email_content):
    """Create a few-shot prompt for email classification."""
    categories_list = "\n".join([f"- {cat}" for cat in SUPPORT_CATEGORIES.keys()])
    
    examples_text = "\n\n".join([
        f"Email: {ex['email']}\nCategory: {ex['category']}"
        for ex in FEW_SHOT_EXAMPLES
    ])
    
    prompt = f"""You are an email routing specialist for an airline. Your task is to classify incoming customer support emails into one of these categories:

{categories_list}

Examples:
{examples_text}

Now classify this email:
Email: {email_content}
Category:"""
    
    return prompt


def call_gpt_model(model_name, prompt):
    """Call OpenAI API with specified model."""
    try:
        # Use Completions API for instruct models, Chat API for chat models
        if "instruct" in model_name.lower():
            # For instruct models, use the Completions endpoint
            full_prompt = f"You are a helpful email routing specialist.\n\n{prompt}"
            response = client.completions.create(
                model=model_name,
                prompt=full_prompt,
                temperature=0.7,
                max_tokens=100,
                timeout=30
            )
            return response.choices[0].text.strip()
        else:
            # For chat models, use the Chat Completions endpoint
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful email routing specialist."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=100,
                timeout=30
            )
            return response.choices[0].message.content.strip()
    except Exception as e:
        error_msg = str(e)
        print(f"\nError calling {model_name}: {error_msg}")
        print("  Troubleshooting tips:")
        print("  1. Check your internet connection")
        print("  2. Verify your OpenAI API key is valid")
        print("  3. Check OpenAI's status: https://status.openai.com")
        print("  4. Try again in a few moments (may be rate limited)")
        return f"ERROR: {error_msg}"


def is_correct_classification(predicted, expected):
    """Check if the predicted category matches the expected category."""
    predicted_lower = predicted.lower().strip()
    expected_lower = expected.lower().strip()
    return predicted_lower in expected_lower or expected_lower in predicted_lower


def test_connection():
    """Test connection to OpenAI API."""
    print("\nTesting connection to OpenAI API...")
    try:
        # Try a simple call with minimal tokens
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'OK'"}
            ],
            temperature=0.5,
            max_tokens=10,
            timeout=15
        )
        print("✓ Connection successful!")
        print(f"  Model: {response.model}")
        print(f"  Usage: {response.usage.prompt_tokens} prompt tokens, {response.usage.completion_tokens} completion tokens")
        return True
    except Exception as e:
        print(f"✗ Connection failed: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Verify your internet connection is working")
        print("2. Check that your OpenAI API key is valid:")
        print("   - Go to https://platform.openai.com/account/api-keys")
        print("   - Create a new key if needed")
        print("3. Ensure your API key is correctly set in .env file")
        print("4. Check OpenAI's status: https://status.openai.com")
        print("5. Try using a different region/network if available")
        return False


def run_benchmark_interactive():
    """Run interactive benchmark with user input."""
    
    results = []
    models = ["gpt-3.5-turbo-instruct","gpt-3.5-turbo"]
    techniques = ["zero-shot", "one-shot", "few-shot"]
    
    print("=" * 80)
    print("AIRLINE EMAIL ROUTING BENCHMARK - PROMPT ENGINEERING OPTIMIZATION")
    print("=" * 80)
    print(f"\nTesting {len(models)} models across {len(techniques)} prompting techniques")
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
                print(f"[{current_test}/{total_tests}] Testing {email['id']}...", end=" ", flush=True)
                prediction = call_gpt_model(model, prompt)
                
                # Check if correct
                is_correct = is_correct_classification(prediction, email["expected_category"])
                
                print(f"Predicted: {prediction[:40]}... {'✓' if is_correct else '✗'}")
                
                # Get user feedback
                print(f"  Expected: {email['expected_category']}")
                user_score = input("  Enter quality score (0-2, or press Enter for auto): ").strip()
                
                if user_score == "":
                    if is_correct:
                        user_score = 2
                    else:
                        user_score = 0
                else:
                    try:
                        user_score = int(user_score)
                    except ValueError:
                        user_score = 1
                
                # Store result
                result = {
                    "model": model,
                    "technique": technique,
                    "email_id": email["id"],
                    "email_content": email["content"],
                    "expected_category": email["expected_category"],
                    "predicted_category": prediction,
                    "is_correct": is_correct,
                    "quality_score": user_score,
                    "timestamp": datetime.now().isoformat()
                }
                results.append(result)
                print()
    
    return results


def export_to_excel(results):
    """Export benchmark results to Excel with analysis."""
    
    # Create workbook with multiple sheets
    wb = openpyxl.Workbook()
    
    # Remove default sheet
    if 'Sheet' in wb.sheetnames:
        wb.remove(wb['Sheet'])
    
    # Sheet 1: Detailed Results
    ws_detailed = wb.create_sheet("Detailed Results", 0)
    
    # Add headers
    headers = [
        "Email ID", "Model", "Technique", "Expected Category", 
        "Predicted Category", "Correct", "Quality Score", "Email Content"
    ]
    ws_detailed.append(headers)
    
    # Style header row
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
    
    for cell in ws_detailed[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(wrap_text=True, vertical="center")
    
    # Add data
    for result in results:
        ws_detailed.append([
            result["email_id"],
            result["model"],
            result["technique"],
            result["expected_category"],
            result["predicted_category"][:40],
            "Yes" if result["is_correct"] else "No",
            result["quality_score"],
            result["email_content"][:100]
        ])
    
    # Adjust column widths
    ws_detailed.column_dimensions['A'].width = 12
    ws_detailed.column_dimensions['B'].width = 18
    ws_detailed.column_dimensions['C'].width = 12
    ws_detailed.column_dimensions['D'].width = 25
    ws_detailed.column_dimensions['E'].width = 25
    ws_detailed.column_dimensions['F'].width = 10
    ws_detailed.column_dimensions['G'].width = 10
    ws_detailed.column_dimensions['H'].width = 40
    
    # Sheet 2: Summary by Model and Technique
    ws_summary = wb.create_sheet("Summary Analysis", 1)
    
    # Calculate summary statistics
    summary_data = {}
    for result in results:
        key = (result["model"], result["technique"])
        if key not in summary_data:
            summary_data[key] = {
                "total": 0,
                "correct": 0,
                "total_score": 0,
                "quality_scores": []
            }
        
        summary_data[key]["total"] += 1
        if result["is_correct"]:
            summary_data[key]["correct"] += 1
        summary_data[key]["total_score"] += result["quality_score"]
        summary_data[key]["quality_scores"].append(result["quality_score"])
    
    # Add summary headers
    summary_headers = ["Model", "Technique", "Accuracy %", "Avg Quality Score", "Total Tests"]
    ws_summary.append(summary_headers)
    
    for cell in ws_summary[1]:
        cell.fill = header_fill
        cell.font = header_font
    
    # Add summary data
    for (model, technique), stats in sorted(summary_data.items()):
        accuracy = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
        avg_score = stats["total_score"] / stats["total"] if stats["total"] > 0 else 0
        
        ws_summary.append([
            model,
            technique,
            f"{accuracy:.1f}%",
            f"{avg_score:.2f}",
            stats["total"]
        ])
    
    ws_summary.column_dimensions['A'].width = 18
    ws_summary.column_dimensions['B'].width = 12
    ws_summary.column_dimensions['C'].width = 15
    ws_summary.column_dimensions['D'].width = 15
    ws_summary.column_dimensions['E'].width = 12
    
    # Sheet 3: Model Comparison
    ws_comparison = wb.create_sheet("Model Comparison", 2)
    
    models = sorted(set(r["model"] for r in results))
    techniques = sorted(set(r["technique"] for r in results))
    
    # Create comparison matrix for accuracy
    ws_comparison.append(["Model Accuracy Comparison (%)"] + techniques)
    
    for model in models:
        row = [model]
        for technique in techniques:
            model_tech_results = [r for r in results if r["model"] == model and r["technique"] == technique]
            if model_tech_results:
                accuracy = sum(1 for r in model_tech_results if r["is_correct"]) / len(model_tech_results) * 100
                row.append(f"{accuracy:.1f}%")
            else:
                row.append("N/A")
        ws_comparison.append(row)
    
    ws_comparison.column_dimensions['A'].width = 18
    for col in range(2, len(techniques) + 2):
        ws_comparison.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 15
    
    # Sheet 4: Analysis & Insights
    ws_analysis = wb.create_sheet("Analysis & Insights", 3)
    
    analysis_text = [
        ["BENCHMARK ANALYSIS & INSIGHTS"],
        [],
        ["Key Findings:"],
        []
    ]
    
    # Calculate best performing model/technique combination
    best_combo = max(summary_data.items(), 
                     key=lambda x: (x[1]["correct"] / x[1]["total"], x[1]["total_score"] / x[1]["total"]))
    best_model, best_technique = best_combo[0]
    best_stats = best_combo[1]
    best_accuracy = best_stats["correct"] / best_stats["total"] * 100
    best_score = best_stats["total_score"] / best_stats["total"]
    
    analysis_text.append([f"Best Combination: {best_model} + {best_technique}"])
    analysis_text.append([f"  • Accuracy: {best_accuracy:.1f}%"])
    analysis_text.append([f"  • Average Quality Score: {best_score:.2f}"])
    analysis_text.append([])
    
    # Model comparison
    model_stats = {}
    for (model, _), stats in summary_data.items():
        if model not in model_stats:
            model_stats[model] = {"correct": 0, "total": 0, "score": 0}
        model_stats[model]["correct"] += stats["correct"]
        model_stats[model]["total"] += stats["total"]
        model_stats[model]["score"] += stats["total_score"]
    
    analysis_text.append(["Model Performance:"])
    for model in sorted(model_stats.keys()):
        stats = model_stats[model]
        acc = stats["correct"] / stats["total"] * 100
        score = stats["score"] / stats["total"]
        analysis_text.append([f"  • {model}: {acc:.1f}% accuracy, {score:.2f} avg score"])
    
    analysis_text.append([])
    analysis_text.append(["Technique Effectiveness:"])
    
    technique_stats = {}
    for (_, technique), stats in summary_data.items():
        if technique not in technique_stats:
            technique_stats[technique] = {"correct": 0, "total": 0, "score": 0}
        technique_stats[technique]["correct"] += stats["correct"]
        technique_stats[technique]["total"] += stats["total"]
        technique_stats[technique]["score"] += stats["total_score"]
    
    for technique in sorted(technique_stats.keys()):
        stats = technique_stats[technique]
        acc = stats["correct"] / stats["total"] * 100
        score = stats["score"] / stats["total"]
        analysis_text.append([f"  • {technique}: {acc:.1f}% accuracy, {score:.2f} avg score"])
    
    # Add analysis to worksheet
    for row in analysis_text:
        ws_analysis.append(row)
    
    ws_analysis.column_dimensions['A'].width = 60
    
    # Save workbook
    output_file = "email_routing_benchmark_results.xlsx"
    wb.save(output_file)
    print(f"\n✓ Results exported to: {output_file}")
    return output_file


def main():
    """Main function."""
    print("\nStarting Email Routing Benchmark...")
    print("This will test 2 models with 3 prompting techniques on email classification.\n")
    
    # Test connection first
    if not test_connection():
        print("\n❌ Cannot proceed. Please fix the connection issue above.")
        return
    
    # Run interactive benchmark
    results = run_benchmark_interactive()
    
    print(f"\n{'='*80}")
    print(f"BENCHMARK COMPLETE")
    print(f"Total tests: {len(results)}")
    print(f"{'='*80}\n")
    
    # Export results
    export_to_excel(results)
    
    print("Benchmark complete! Check the Excel file for detailed analysis.")


if __name__ == "__main__":
    main()
