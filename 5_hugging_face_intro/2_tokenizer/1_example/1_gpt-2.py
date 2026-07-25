from transformers import AutoTokenizer
from dotenv import load_dotenv, find_dotenv
import os
from datasets import Dataset
import pandas as pd

_ = load_dotenv(find_dotenv())  # read local .env file

API_TOKEN = os.environ.get("HF_TOKEN")
print(API_TOKEN)


# -----------------------------------------------------------
# GPT2
# -----------------------------------------------------------
print("-----------------------------------------------------------")
print("GPT 2")
print("-----------------------------------------------------------")
tokenizer = AutoTokenizer.from_pretrained("openai-community/gpt2", token=API_TOKEN)
print(tokenizer)


# Retrieve all tokens and their IDs
tokens = tokenizer.get_vocab()

# Convert to a DataFrame for easier viewing
tokens_df = pd.DataFrame(tokens.items(), columns=['Token', 'ID']).sort_values(by='ID')

# Display the DataFrame
tokens_df.reset_index(drop=True, inplace=True)
print(tokens_df)
tokens_df.to_csv("gpt2-tokens.csv", index=False)

# NOTE: `tokenizer.default_chat_template` was removed in transformers v5.
# There is no longer a hardcoded fallback template; models without a chat
# template simply have `chat_template == None` (as is the case for GPT-2).
print("----- Current model chat template -----")
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

print("----- Applied on text -----")
result = tokenizer("What's the weather like in Paris? The current temperature in Paris, France is 22 degrees Celsius.")
print(result)

print("----- Decoded -----")
decoded = tokenizer.decode(result["input_ids"])
print(decoded)

# GPT-2 ships without a chat template. transformers <4.44 fell back to a
# built-in ChatML default; that fallback was removed, so set it explicitly
# here to reproduce the original behaviour of this demo.
if tokenizer.chat_template is None:
    tokenizer.chat_template = (
        "{% for message in messages %}"
        "{{'<|im_start|>' + message['role'] + '\n' + message['content'] + '<|im_end|>' + '\n'}}"
        "{% endfor %}"
        "{% if add_generation_prompt %}{{ '<|im_start|>assistant\n' }}{% endif %}"
    )

# Chat
chat = [
    {"role": "user", "content": "What's the weather like in Paris?"},
    {
        "role": "assistant",
        "content": "The current temperature in Paris, France is 22 degrees Celsius.",
    },
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
