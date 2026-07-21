"""
Prompt Enhancement Strategy (Alternative to Fine-tuning)
Since OpenAI fine-tuning is deprecated, we use advanced prompt engineering:
- Few-shot learning with examples from training data
- Domain-specific system prompts
- Embedded policy knowledge
"""

import json
import jsonlines
from pathlib import Path
from typing import List, Dict

class PromptEnhancer:
    def __init__(self):
        """Initialize the prompt enhancer."""
        self.training_examples = []
        self.policy_text = ""
        
    def load_training_data(self, train_file_path):
        """Load training examples for few-shot prompting."""
        print(f"📥 Loading training examples from: {train_file_path}")
        
        try:
            with jsonlines.open(train_file_path) as reader:
                for obj in reader:
                    if "messages" in obj:
                        messages = obj["messages"]
                        user_msg = next((m["content"] for m in messages if m["role"] == "user"), "")
                        assistant_msg = next((m["content"] for m in messages if m["role"] == "assistant"), "")
                        
                        if user_msg and assistant_msg:
                            self.training_examples.append({
                                "question": user_msg,
                                "answer": assistant_msg
                            })
            
            print(f"✅ Loaded {len(self.training_examples)} training examples")
            return True
        except Exception as e:
            print(f"❌ Error loading training data: {e}")
            return False
    
    def load_policy_document(self, policy_file_path):
        """Load the hotel booking policy document."""
        print(f"📄 Loading policy document from: {policy_file_path}")
        
        try:
            with open(policy_file_path, 'r', encoding='utf-8') as f:
                self.policy_text = f.read()
            
            print(f"✅ Loaded policy document ({len(self.policy_text)} characters)")
            return True
        except Exception as e:
            print(f"❌ Error loading policy document: {e}")
            return False
    
    def create_base_system_prompt(self):
        """Create the basic system prompt (no enhancement)."""
        return "You are a helpful hotel booking assistant expert on Lighthouse Jurmala hotel booking terms and conditions. You provide accurate and clear information to help guests understand the hotel's policies."
    
    def create_enhanced_system_prompt(self, include_policy=True, num_examples=3):
        """Create an enhanced system prompt with policy and few-shot examples."""
        
        prompt_parts = [
            "You are an expert hotel booking assistant for Lighthouse Jurmala hotel.",
            "You provide accurate, clear, and helpful information about hotel policies.",
            ""
        ]
        
        # Add policy document if available and requested
        if include_policy and self.policy_text:
            prompt_parts.extend([
                "=== HOTEL BOOKING POLICY ===",
                self.policy_text,
                "",
                "=== END OF POLICY ===",
                ""
            ])
        
        # Add few-shot examples
        if self.training_examples and num_examples > 0:
            prompt_parts.append("=== EXAMPLE Q&A ===")
            
            # Select diverse examples
            examples = self.training_examples[:num_examples]
            
            for i, example in enumerate(examples, 1):
                prompt_parts.extend([
                    f"Example {i}:",
                    f"Q: {example['question']}",
                    f"A: {example['answer']}",
                    ""
                ])
            
            prompt_parts.extend([
                "=== END OF EXAMPLES ===",
                "",
                "Based on the policy and examples above, answer questions accurately and helpfully."
            ])
        
        return "\n".join(prompt_parts)
    
    def save_enhanced_prompt_config(self, output_file="enhanced_prompt_config.json"):
        """Save the enhanced prompt configuration."""
        config = {
            "strategy": "Few-shot Learning + Policy Embedding",
            "base_system_prompt": self.create_base_system_prompt(),
            "enhanced_system_prompt": self.create_enhanced_system_prompt(),
            "num_training_examples": len(self.training_examples),
            "policy_length": len(self.policy_text),
            "note": "This replaces fine-tuning due to OpenAI API deprecation"
        }
        
        output_path = Path(__file__).parent / output_file
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Enhanced prompt config saved to: {output_path}")
        return output_path


def main():
    """Main execution function."""
    print("=" * 70)
    print("PROMPT ENHANCEMENT STRATEGY")
    print("(Alternative to Fine-tuning)")
    print("=" * 70)
    
    # Initialize enhancer
    enhancer = PromptEnhancer()
    
    # Load training data
    train_file = Path(__file__).parent / "hotel_booking_finetuning" / "openai_format" / "train.jsonl"
    enhancer.load_training_data(train_file)
    
    # Load policy document
    policy_file = Path(__file__).parent / "Hotel Booking terms.md"
    if policy_file.exists():
        enhancer.load_policy_document(policy_file)
    
    # Create and display prompts
    print("\n" + "=" * 70)
    print("BASE SYSTEM PROMPT")
    print("=" * 70)
    print(enhancer.create_base_system_prompt())
    
    print("\n" + "=" * 70)
    print("ENHANCED SYSTEM PROMPT (Preview - first 500 chars)")
    print("=" * 70)
    enhanced = enhancer.create_enhanced_system_prompt()
    print(enhanced[:500] + "..." if len(enhanced) > 500 else enhanced)
    
    # Save configuration
    enhancer.save_enhanced_prompt_config()
    
    print("\n✅ Prompt enhancement strategy ready!")
    print("   This will be used instead of fine-tuning for benchmarking.")


if __name__ == "__main__":
    main()
