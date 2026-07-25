from transformers import AutoTokenizer
from dotenv import load_dotenv, find_dotenv
import os
from datasets import Dataset
import pandas as pd

_ = load_dotenv(find_dotenv())  # read local .env file

API_TOKEN = os.environ.get("HF_TOKEN")
print(API_TOKEN)

# ----------------------------------------------------------
# Llama 3 - 8B - Instruct
# ----------------------------------------------------------
print("-----------------------------------------------------------")
print("Llama 3 - 8B Instruct")
print("-----------------------------------------------------------")
tokenizer = AutoTokenizer.from_pretrained(
    "meta-llama/Meta-Llama-3-8B-Instruct", token=API_TOKEN
)
print(tokenizer)


# Retrieve all tokens and their IDs
tokens = tokenizer.get_vocab()

# Convert to a DataFrame for easier viewing
tokens_df = pd.DataFrame(tokens.items(), columns=['Token', 'ID']).sort_values(by='ID')

# Display the DataFrame
tokens_df.reset_index(drop=True, inplace=True)
print(tokens_df)
tokens_df.to_csv("llama_3_instruct-tokens.csv", index=False)

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


chat = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I'm doing great. How can I help you today?"},
    {"role": "user", "content": "I'd like to show off how chat templating works!"},
]


print("----- Applied on data -----")
result = tokenizer.apply_chat_template(
    chat, tokenize=False, add_generation_prompt=False
)
print(result)

print("----- Applied on data + tokenized -----")
result = tokenizer.apply_chat_template(chat, tokenize=True, add_generation_prompt=False)
print(result)

print("----- Decoded -----")
decoded = tokenizer.decode(result)
print(decoded)

