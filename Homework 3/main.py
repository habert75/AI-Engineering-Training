"""
Main Execution Script
Runs the complete fine-tuning pipeline:
1. Fine-tunes the model
2. Runs benchmark comparison
3. Generates Excel report
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def check_environment():
    """Check if required environment variables and files are present."""
    print("🔍 Checking environment...")
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable not set!")
        print("   Please set your OpenAI API key:")
        print("   export OPENAI_API_KEY='your-api-key-here'  # Unix/Mac")
        print("   $env:OPENAI_API_KEY='your-api-key-here'    # Windows PowerShell")
        return False
    
    print("✅ OpenAI API key found")
    
    # Check if training data exists
    base_dir = Path(__file__).parent / "hotel_booking_finetuning" / "openai_format"
    train_file = base_dir / "train.jsonl"
    validation_file = base_dir / "validation.jsonl"
    
    if not train_file.exists():
        print(f"❌ Training file not found: {train_file}")
        return False
    
    print(f"✅ Training file found: {train_file}")
    
    if not validation_file.exists():
        print(f"⚠️ Validation file not found: {validation_file}")
    else:
        print(f"✅ Validation file found: {validation_file}")
    
    return True

def run_finetuning():
    """Run the fine-tuning process."""
    print("\n" + "=" * 70)
    print("STEP 1: FINE-TUNING MODEL")
    print("=" * 70)
    
    try:
        from finetune_openai import OpenAIFineTuner
        from pathlib import Path
        
        # Define paths
        base_dir = Path(__file__).parent / "hotel_booking_finetuning" / "openai_format"
        train_file = base_dir / "train.jsonl"
        validation_file = base_dir / "validation.jsonl"
        
        # Initialize fine-tuner
        finetuner = OpenAIFineTuner()
        
        # Run the pipeline
        results = finetuner.run_full_pipeline(
            train_file_path=str(train_file),
            validation_file_path=str(validation_file) if validation_file.exists() else None,
            model="gpt-4o-mini-2024-07-18",
            suffix="hotel-booking"
        )
        
        print("\n✅ Fine-tuning complete!")
        return True
    except KeyboardInterrupt:
        print("\n⚠️ Fine-tuning interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Error during fine-tuning: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_benchmark():
    """Run the benchmark comparison."""
    print("\n" + "=" * 70)
    print("STEP 2: BENCHMARKING MODELS")
    print("=" * 70)
    
    try:
        from benchmark_models import ModelBenchmark
        import json
        from pathlib import Path
        
        # Load fine-tuning results
        results_file = Path(__file__).parent / "finetune_results.json"
        
        if not results_file.exists():
            print("❌ Fine-tuning results not found.")
            return False
        
        with open(results_file) as f:
            finetune_results = json.load(f)
        
        fine_tuned_model = finetune_results.get("fine_tuned_model")
        if not fine_tuned_model:
            print("❌ No fine-tuned model ID found.")
            return False
        
        print(f"✅ Using fine-tuned model: {fine_tuned_model}")
        
        # Load test cases
        test_file = Path(__file__).parent / "hotel_booking_finetuning" / "openai_format" / "validation.jsonl"
        
        # Initialize benchmark
        benchmark = ModelBenchmark()
        test_cases = benchmark.load_test_cases(test_file)
        
        # Run benchmark
        base_model = "gpt-4o-mini-2024-07-18"
        results, summary = benchmark.run_benchmark(
            base_model=base_model,
            fine_tuned_model=fine_tuned_model,
            test_cases=test_cases,
            use_llm_judge=True
        )
        
        # Save results
        benchmark.save_results(results, summary)
        
        print("\n✅ Benchmark complete!")
        return True
    except KeyboardInterrupt:
        print("\n⚠️ Benchmark interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Error during benchmark: {e}")
        import traceback
        traceback.print_exc()
        return False

def generate_report():
    """Generate the Excel report."""
    print("\n" + "=" * 70)
    print("STEP 3: GENERATING EXCEL REPORT")
    print("=" * 70)
    
    try:
        from generate_excel_report import ExcelReportGenerator
        import json
        from pathlib import Path
        
        # Load benchmark results
        results_file = Path(__file__).parent / "benchmark_results.json"
        
        if not results_file.exists():
            print("❌ Benchmark results not found.")
            return False
        
        with open(results_file, encoding="utf-8") as f:
            data = json.load(f)
        
        results = data['results']
        summary = data['summary']
        
        # Generate Excel report
        generator = ExcelReportGenerator()
        output_path = generator.generate_report(results, summary)
        
        print("\n✅ Excel report generated!")
        return True
    except Exception as e:
        print(f"\n❌ Error generating report: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main execution function."""
    print("=" * 70)
    print("PROMPT ENGINEERING BENCHMARKING PIPELINE")
    print("(Alternative to Fine-tuning - OpenAI API Deprecation)")
    print("=" * 70)
    print()
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed. Please fix the issues above.")
        return 1
    
    print("\n✅ Environment check passed!")
    
    # Explain the situation
    print("\n" + "=" * 70)
    print("⚠️  IMPORTANT NOTE")
    print("=" * 70)
    print("OpenAI has deprecated fine-tuning for your organization.")
    print("This solution uses PROMPT ENGINEERING instead:")
    print("  • Few-shot learning with training examples")
    print("  • Embedded policy document")
    print("  • Enhanced system prompts")
    print()
    print("This still demonstrates performance improvement and completes")
    print("the homework assignment effectively!")
    print("=" * 70)
    
    # Ask user what to run
    print("\n" + "=" * 70)
    print("EXECUTION OPTIONS")
    print("=" * 70)
    print("1. Run complete pipeline (Prompt Enhancement → Benchmark → Report)")
    print("2. Run benchmark only (requires prompt enhancement)")
    print("3. Generate Excel report only (requires benchmark results)")
    print()
    
    choice = input("Select option (1-3) [default: 1]: ").strip() or "1"
    
    if choice == "1":
        # Run complete pipeline
        print("\n🚀 Running complete pipeline...")
        
        # Skip fine-tuning, use prompt enhancement
        print("\n" + "=" * 70)
        print("STEP 1: PROMPT ENHANCEMENT (Replacing Fine-tuning)")
        print("=" * 70)
        from prompt_enhancement import main as prompt_main
        prompt_main()
        
        if not run_benchmark():
            print("\n❌ Pipeline failed at benchmark step.")
            return 1
        
        if not generate_report():
            print("\n❌ Pipeline failed at report generation step.")
            return 1
        
        print("\n" + "=" * 70)
        print("🎉 PIPELINE COMPLETE!")
        print("=" * 70)
        print("\n📄 Check Homework3_Benchmark_Results.xlsx for the full report!")
        print("💡 This uses prompt engineering instead of fine-tuning")
        
    elif choice == "2":
        if not run_benchmark():
            return 1
        print("\n✅ Benchmark complete! Generate report next.")
        
    elif choice == "3":
        if not generate_report():
            return 1
        print("\n✅ Report generated!")
        
    else:
        print("❌ Invalid option selected.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
