from transformers import AutoTokenizer
from dotenv import load_dotenv, find_dotenv
import os
from datasets import Dataset
import pandas as pd

_ = load_dotenv(find_dotenv())  # read local .env file

API_TOKEN = os.environ.get("HF_TOKEN")
print(API_TOKEN)


# ----------------------------------------------------------
# Mistral 7B v0.3 Instruct
# ----------------------------------------------------------
print("-----------------------------------------------------------")
print("Mistral 7B v0.3 Instruct")
print("-----------------------------------------------------------")
tokenizer = AutoTokenizer.from_pretrained(
    "mistralai/Mistral-7B-Instruct-v0.3", token=API_TOKEN
)
print(tokenizer)


# Retrieve all tokens and their IDs
tokens = tokenizer.get_vocab()

# Convert to a DataFrame for easier viewing
tokens_df = pd.DataFrame(tokens.items(), columns=['Token', 'ID']).sort_values(by='ID')

# Display the DataFrame
tokens_df.reset_index(drop=True, inplace=True)
print(tokens_df)
tokens_df.to_csv("mistral_v03_instruct-tokens.csv", index=False)

print("----- Model chat template -----")
print(tokenizer.chat_template)

print("bos_token: ")
print(tokenizer.bos_token_id)
print(tokenizer.bos_token)
print("eos_token: ")
print(tokenizer.eos_token_id)
print(tokenizer.eos_token)
print("pad_token: ")
print(tokenizer.pad_token_id)
print(tokenizer.pad_token)
print("unk_token: ")
print(tokenizer.unk_token_id)
print(tokenizer.unk_token)
print("cls_token: ")
print(tokenizer.cls_token_id)
print(tokenizer.cls_token)
print("mask_token: ")
print(tokenizer.mask_token_id)
print(tokenizer.mask_token)
print("sep_token: ")
print(tokenizer.sep_token_id)
print(tokenizer.sep_token)
print("additional_special_tokens: ")
print(tokenizer.special_tokens_map.get("additional_special_tokens"))
print("all_special_tokens: ")
print(tokenizer.all_special_tokens)

print("----- Padding -----")
print(tokenizer.padding_side)



chat = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What's the weather like in Paris?"},
    {
        "tool_calls": [
            {
                "id": "abcdefghi",
                "function": {
                    "name": "get_current_weather",
                    "arguments": {"location": "Paris, France", "format": "celsius"},
                }
            }
        ],
    },
    {
        "role": "tool_results", 
        "tool_call_id": "abcdefghi",
        "content": {
            "content": 22
        }
    },
    {
        "role": "assistant",
        "content": "The current temperature in Paris, France is 22 degrees Celsius.",
    },
    {"role": "user", "content": "What about San Francisco?"},
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get▁the▁current▁weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "format": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The temperature unit to use. Infer this from the users location.",
                    },
                },
                "required": ["location", "format"],
            },
        },
    }
]


print("----- Applied on data -----")
result = tokenizer.apply_chat_template(
    chat,
    tools=tools,
    tokenize=False, 
    add_generation_prompt=False
)
print(result)

print("----- Applied on data + tokenized -----")
result = tokenizer.apply_chat_template(chat, tools=tools, tokenize=True, add_generation_prompt=False)
print(result)

print("----- Decoded -----")
decoded = tokenizer.decode(result)
print(decoded)
