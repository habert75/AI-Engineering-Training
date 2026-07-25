"""
Test the fine-tuned Gemma-4-E4B hotel-policies adapter — no GPU required.

Usage:
    python test_adapter.py
    python test_adapter.py --prompt "What is the cancellation policy?"
    python test_adapter.py --interactive      # chat loop

Requirements (install once):
    pip install transformers peft accelerate sentencepiece torch
"""

import argparse
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

ADAPTER_REPO = "habert75/autogen-gemma4-4bit-lora-adapter"
BASE_MODEL   = "google/gemma-4-E4B-it"
HF_TOKEN     = os.environ.get("HF_TOKEN")

DEMO_QUESTIONS = [
    "What time is check-in and check-out?",
    "What is the cancellation policy?",
    "Are pets allowed in the hotel?",
    "How can I make a booking at the hotel?",
    "Is breakfast included in the room rate?",
]


def load_model():
    device = (
        "cuda" if torch.cuda.is_available()
        else "mps"  if (hasattr(torch.backends, "mps") and torch.backends.mps.is_available())
        else "cpu"
    )
    print(f"Device: {device}")

    load_kwargs = dict(token=HF_TOKEN)

    if device == "cuda":
        from transformers import BitsAndBytesConfig
        load_kwargs["quantization_config"] = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_quant_type="nf4",
        )
        load_kwargs["dtype"] = torch.bfloat16
        load_kwargs["device_map"] = "auto"
    else:
        # CPU / MPS: load in 32-bit (no bitsandbytes needed)
        load_kwargs["dtype"] = torch.float32
        if device == "mps":
            load_kwargs["device_map"] = {"": "mps"}
        # CPU: let accelerate place everything
        print("⚠️  No GPU found — loading in fp32. Expect slow responses (~1-5 min each).")

    print("Loading base model…")
    model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, **load_kwargs)

    print("Loading tokenizer…")
    tokenizer = AutoTokenizer.from_pretrained(ADAPTER_REPO, token=HF_TOKEN)

    print("Attaching LoRA adapter…")
    peft_kwargs = {"token": HF_TOKEN}
    if device == "cuda":
        peft_kwargs["device_map"] = "auto"
    model = PeftModel.from_pretrained(model, ADAPTER_REPO, **peft_kwargs)
    model.eval()

    print("✅ Model ready\n")
    return model, tokenizer, device


def generate(model, tokenizer, prompt, max_new_tokens=256):
    messages = [{"role": "user", "content": prompt}]
    formatted = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(formatted, return_tensors="pt")
    # Move inputs to the same device as the model's first parameter.
    target_device = next(model.parameters()).device
    inputs = {k: v.to(target_device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    generated = outputs[0][inputs["input_ids"].shape[1]:]
    return tokenizer.decode(generated, skip_special_tokens=True).strip()


def main():
    parser = argparse.ArgumentParser(description="Test fine-tuned Gemma hotel adapter")
    parser.add_argument("--prompt",      type=str, help="Single question to ask")
    parser.add_argument("--interactive", action="store_true", help="Start an interactive chat loop")
    parser.add_argument("--max-tokens",  type=int, default=256, help="Max tokens to generate")
    args = parser.parse_args()

    model, tokenizer, device = load_model()

    if args.prompt:
        print(f"❓ {args.prompt}")
        print(f"💬 {generate(model, tokenizer, args.prompt, args.max_tokens)}\n")

    elif args.interactive:
        print("💬 Interactive mode — type 'quit' to exit\n")
        while True:
            q = input("You: ").strip()
            if q.lower() in ("quit", "exit", "q"):
                break
            if q:
                print(f"Bot: {generate(model, tokenizer, q, args.max_tokens)}\n")

    else:
        # Default: run demo questions
        print("=" * 60)
        print("DEMO — Hotel Policy Questions")
        print("=" * 60)
        for q in DEMO_QUESTIONS:
            print(f"\n❓ {q}")
            print(f"💬 {generate(model, tokenizer, q, args.max_tokens)}")
            print("-" * 60)


if __name__ == "__main__":
    main()
