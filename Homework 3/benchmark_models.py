"""
Model Benchmarking Script
Compares responses from base model vs enhanced prompt model
(Updated to use prompt engineering instead of fine-tuning due to OpenAI API deprecation)
"""

import os
import json
import time
from pathlib import Path
from openai import OpenAI
from typing import List, Dict, Any
import jsonlines
from dotenv import load_dotenv
from prompt_enhancement import PromptEnhancer

# Load environment variables from .env file
load_dotenv()

class ModelBenchmark:
    def __init__(self, api_key=None):
        """Initialize the OpenAI client."""
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.results = []
        self.prompt_enhancer = PromptEnhancer()
        
    def load_test_cases(self, test_file_path):
        """Load test cases from JSONL file."""
        print(f"📥 Loading test cases from: {test_file_path}")
        test_cases = []
        
        try:
            with jsonlines.open(test_file_path) as reader:
                for obj in reader:
                    if "messages" in obj:
                        # Extract the user question and expected answer
                        messages = obj["messages"]
                        system_msg = next((m["content"] for m in messages if m["role"] == "system"), "")
                        user_msg = next((m["content"] for m in messages if m["role"] == "user"), "")
                        assistant_msg = next((m["content"] for m in messages if m["role"] == "assistant"), "")
                        
                        if user_msg:
                            test_cases.append({
                                "system": system_msg,
                                "question": user_msg,
                                "expected_answer": assistant_msg
                            })
            
            print(f"✅ Loaded {len(test_cases)} test cases")
            return test_cases
        except Exception as e:
            print(f"❌ Error loading test cases: {e}")
            raise
    
    def get_model_response(self, model_id, system_prompt, user_question, temperature=0.3):
        """Get a response from a model."""
        try:
            response = self.client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_question}
                ],
                temperature=temperature,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠️ Error getting response from {model_id}: {e}")
            return f"ERROR: {str(e)}"
    
    def evaluate_response(self, expected, actual):
        """
        Simple evaluation of response quality.
        Returns a score from 0-10 based on:
        - Relevance (contains key information)
        - Accuracy (matches expected content)
        """
        if actual.startswith("ERROR:"):
            return 0
        
        # Basic scoring logic
        score = 5  # Base score
        
        # Check if key terms from expected answer appear in actual
        expected_lower = expected.lower()
        actual_lower = actual.lower()
        
        # Extract key phrases (simple approach)
        key_terms = set()
        for word in expected_lower.split():
            if len(word) > 4 and word.isalpha():
                key_terms.add(word)
        
        # Calculate match percentage
        matches = sum(1 for term in key_terms if term in actual_lower)
        if key_terms:
            match_percentage = matches / len(key_terms)
            score += match_percentage * 5  # Up to 5 additional points
        
        # Length similarity bonus (penalize too short or too long)
        len_ratio = len(actual) / max(len(expected), 1)
        if 0.5 <= len_ratio <= 2.0:
            score += 1
        
        return min(10, round(score, 1))
    
    def use_llm_judge(self, question, expected, actual):
        """
        Use GPT-4 as a judge to evaluate response quality.
        Returns a score from 0-10.
        """
        judge_prompt = f"""You are an expert evaluator. Compare the following two answers to the question and rate the quality of the "Actual Answer" on a scale of 0-10.

Question: {question}

Expected Answer: {expected}

Actual Answer: {actual}

Evaluate based on:
1. Accuracy: Does it provide correct information?
2. Completeness: Does it cover the key points?
3. Clarity: Is it clear and well-structured?
4. Relevance: Does it directly answer the question?

Respond with ONLY a number between 0 and 10, where:
- 0-3: Poor/Incorrect
- 4-6: Adequate but missing details
- 7-8: Good, mostly accurate
- 9-10: Excellent, comprehensive

Score (number only):"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": judge_prompt}],
                temperature=0.1,
                max_tokens=10
            )
            score_text = response.choices[0].message.content.strip()
            # Extract number
            score = float(''.join(c for c in score_text if c.isdigit() or c == '.'))
            return min(10, max(0, score))
        except Exception as e:
            print(f"⚠️ Error using LLM judge: {e}")
            return self.evaluate_response(expected, actual)
    
    def run_benchmark(self, base_model, enhanced_model_name, test_cases, use_llm_judge=True, 
                     base_prompt=None, enhanced_prompt=None):
        """Run benchmark comparing base prompt and enhanced prompt."""
        print("\n" + "=" * 60)
        print("🎯 Starting Model Benchmark")
        print("=" * 60)
        print(f"Base Model: {base_model} (standard prompt)")
        print(f"Enhanced Model: {base_model} (enhanced prompt with few-shot)")
        print(f"Test Cases: {len(test_cases)}")
        print(f"Evaluation Method: {'LLM Judge (GPT-4o-mini)' if use_llm_judge else 'Rule-based'}")
        print(f"Strategy: Prompt Engineering (Fine-tuning deprecated)")
        print("=" * 60)
        
        results = []
        total_base_score = 0
        total_enhanced_score = 0
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📝 Test Case {i}/{len(test_cases)}")
            print(f"Question: {test_case['question'][:80]}...")
            
            question = test_case['question']
            expected = test_case['expected_answer']
            
            # Use base prompt or enhanced prompt
            base_sys_prompt = base_prompt or test_case['system']
            enhanced_sys_prompt = enhanced_prompt or base_sys_prompt
            
            # Get responses from both prompt strategies
            print("  ⏳ Getting base prompt response...")
            base_response = self.get_model_response(base_model, base_sys_prompt, question)
            time.sleep(0.5)  # Rate limiting
            
            print("  ⏳ Getting enhanced prompt response...")
            enhanced_response = self.get_model_response(base_model, enhanced_sys_prompt, question)
            time.sleep(0.5)  # Rate limiting
            
            # Evaluate responses
            if use_llm_judge:
                enhanced_score = self.use_llm_judge(question, expected, enhanced_response)
                time.sleep(0.5)
            else:
                base_score = self.evaluate_response(expected, base_response)
                enhanced_score = self.evaluate_response(expected, enhanced_response)
            
            print(f"  📊 Base Prompt Score: {base_score}/10")
            print(f"  📊 Enhanced Prompt Score: {enhanced_score}/10")
            
            # Store results
            result = {
                "test_case_id": i,
                "question": question,
                "expected_answer": expected,
                "base_model": base_model + " (base prompt)",
                "base_response": base_response,
                "base_score": base_score,
                "finetuned_model": enhanced_model_name,
                "finetuned_response": enhanced_response,
                "finetuned_score": enhanced_score,
                "improvement": enhanced_score - base_score
            }
            results.append(result)
            
            total_base_score += base_score
            total_enhanced_score += enhanc
            
            total_base_score += base_score
            total_finetuned_score += finetuned_score
        enhanced_score = total_enhanced_score / len(test_cases)
        avg_improvement = avg_enhanced_score - avg_base_score
        improvement_percentage = (avg_improvement / avg_base_score * 100) if avg_base_score > 0 else 0
        
        summary = {
            "base_model": base_model + " (base prompt)",
            "finetuned_model": enhanced_model_name,
            "total_test_cases": len(test_cases),
            "avg_base_score": round(avg_base_score, 2),
            "avg_finetuned_score": round(avg_enhanced_score, 2),
            "avg_improvement": round(avg_improvement, 2),
            "improvement_percentage": round(improvement_percentage, 2),
            "method": "Prompt Engineering (Few-shot + Policy)"
        }
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 BENCHMARK SUMMARY")
        print("=" * 60)
        print(f"Average Base Prompt Score: {summary['avg_base_score']}/10")
        print(f"Average Enhanced Prompt Score: {summary['avg_finetuned_score']}/10")
        print(f"Average Improvement: {summary['avg_improvement']} points")
        print(f"Improvement Percentage: {summary['improvement_percentage']}%")
        print(f"Method: {summary['method']}
        print(f"Average Fine-tuned Score: {summary['avg_finetuned_score']}/10")
        print(f"Average Improvement: {summary['avg_improvement']} points")
        print(f"Improvement Percentage: {summary['improvement_percentage']}%")
        print("=" * 60)
        
        return results, summary
    
    def save_results(self, results, summary, output_file="benchmark_results.json"):
        """Save benchmark results to JSON file."""
        output_data = {
            "summary": summary,
            "results": results,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        output_path = Path(__file__).parent / output_file
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to: {output_path}")
        return output_path


def main():
    """Main execution function."""
    print("⚠️ Note: Using Prompt Engineering instead of Fine-tuning")
    print("   (OpenAI has deprecated fine-tuning for this organization)")
    print()
    
    # Initialize prompt enhancer
    enhancer = PromptEnhancer()
    
    # Load training data for few-shot examples
    train_file = Path(__file__).parent / "hotel_booking_finetuning" / "openai_format" / "train.jsonl"
    enhancer.load_training_data(str(train_file))
    
    # Load policy document
    policy_file = Path(__file__).parent / "Hotel Booking terms.md"
    if policy_file.exists():
        enhancer.load_policy_document(str(policy_file))
    
    # Create prompts
    base_prompt = enhancer.create_base_system_prompt()
    enhanced_prompt = enhancer.create_enhanced_system_prompt(include_policy=True, num_examples=5)
    
    # Load test cases (using validation set)
    test_file = Path(__file__).parent / "hotel_booking_finetuning" / "openai_format" / "validation.jsonl"
    
    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        return
    
    # Initialize benchmark
    benchmark = ModelBenchmark()
    test_cases = benchmark.load_test_cases(test_file)
    
    # Run benchmark with prompt engineering
    base_model = "gpt-4o-mini-2024-07-18"
    enhanced_model_name = base_model + " (Enhanced Prompt + Few-shot)"
    
    results, summary = benchmark.run_benchmark(
        base_model=base_model,
        enhanced_model_name=enhanced_model_name,
        test_cases=test_cases,
        use_llm_judge=True,
        base_prompt=base_prompt,
        enhanced_prompt=enhanced_prompt
    )
    
    # Save results
    benchmark.save_results(results, summary)
    
    print("\n🎉 Benchmark complete!")
    print("💡 This demonstrates performance improvement via prompt engineering")
    print("   instead of fine-tuning (due to OpenAI API deprecation)")


if __name__ == "__main__":
    main()
