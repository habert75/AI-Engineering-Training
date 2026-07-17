import json
import random

# Set random seed for reproducibility
random.seed(42)

# Paths for OpenAI format
openai_all_file = "openai_format/all.jsonl"
openai_train_file = "openai_format/train.jsonl"
openai_val_file = "openai_format/validation.jsonl"

# Paths for HuggingFace format
hf_all_file = "huggingface_format/all.json"
hf_train_file = "huggingface_format/train.json"
hf_val_file = "huggingface_format/validation.json"

# Split ratio (80% train, 20% validation)
train_ratio = 0.8


def split_openai_format():
    """Split OpenAI JSONL format into train and validation sets"""
    # Read all data
    with open(openai_all_file, "r", encoding="utf-8") as f:
        data = [json.loads(line) for line in f]
    
    # Shuffle data
    random.shuffle(data)
    
    # Calculate split point
    split_idx = int(len(data) * train_ratio)
    
    # Split data
    train_data = data[:split_idx]
    val_data = data[split_idx:]
    
    # Write train data
    with open(openai_train_file, "w", encoding="utf-8") as f:
        for item in train_data:
            f.write(json.dumps(item) + "\n")
    
    # Write validation data
    with open(openai_val_file, "w", encoding="utf-8") as f:
        for item in val_data:
            f.write(json.dumps(item) + "\n")
    
    print(f"OpenAI format split: {len(train_data)} training samples, {len(val_data)} validation samples")


def split_huggingface_format():
    """Split HuggingFace JSON format into train and validation sets"""
    # Read all data
    with open(hf_all_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Shuffle data
    random.shuffle(data)
    
    # Calculate split point
    split_idx = int(len(data) * train_ratio)
    
    # Split data
    train_data = data[:split_idx]
    val_data = data[split_idx:]
    
    # Write train data
    with open(hf_train_file, "w", encoding="utf-8") as f:
        json.dump(train_data, f, indent=2)
    
    # Write validation data
    with open(hf_val_file, "w", encoding="utf-8") as f:
        json.dump(val_data, f, indent=2)
    
    print(f"HuggingFace format split: {len(train_data)} training samples, {len(val_data)} validation samples")


if __name__ == "__main__":
    print("Splitting datasets into train and validation sets...")
    split_openai_format()
    split_huggingface_format()
    print("Done!")
