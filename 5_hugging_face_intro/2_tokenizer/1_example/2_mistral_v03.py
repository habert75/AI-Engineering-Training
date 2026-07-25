from transformers import AutoTokenizer
from dotenv import load_dotenv, find_dotenv
import os
from datasets import Dataset
import pandas as pd

_ = load_dotenv(find_dotenv())  # read local .env file

API_TOKEN = os.environ.get("HF_TOKEN")
print(API_TOKEN)


# ----------------------------------------------------------
# Mistral 7B v0.3
# ----------------------------------------------------------
print("-----------------------------------------------------------")
print("Mistral 7B v0.3")
print("-----------------------------------------------------------")
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.3", token=API_TOKEN)
print(tokenizer)


# Retrieve all tokens and their IDs
tokens = tokenizer.get_vocab()

# Convert to a DataFrame for easier viewing
tokens_df = pd.DataFrame(tokens.items(), columns=['Token', 'ID']).sort_values(by='ID')

# Display the DataFrame
tokens_df.reset_index(drop=True, inplace=True)
print(tokens_df)
tokens_df.to_csv("mistral_v03-tokens.csv", index=False)

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


# Normal text
text = "Hello, how are you?"

print("----- Encode -----")
result = tokenizer.encode(text)
print(result)

print("----- Decoded -----")
decoded = tokenizer.decode(result)
print(decoded)

