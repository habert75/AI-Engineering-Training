from transformers import AutoTokenizer
from dotenv import load_dotenv, find_dotenv
import os
from datasets import Dataset
import pandas as pd

_ = load_dotenv(find_dotenv())  # read local .env file

API_TOKEN = os.environ.get("HF_TOKEN")
print(API_TOKEN)


# ----------------------------------------------------------
# Mistral 7B v0.3 Instruct - TOOL USE
# ----------------------------------------------------------
print("-----------------------------------------------------------")
print("Mistral 7B v0.3 Instruct - TOOL USE")
print("-----------------------------------------------------------")
tokenizer = AutoTokenizer.from_pretrained(
    "mistralai/Mistral-7B-Instruct-v0.3", token=API_TOKEN
)
print(tokenizer)

print("----- Model chat template -----")
print(tokenizer.chat_template)

tokenizer.chat_template = {
    "default": tokenizer.chat_template,
    "tool_use": "{{bos_token}}{% set user_messages = messages | selectattr('role', 'equalto', 'user') | list %}{% for message in messages %}{% if message['role'] == 'user' %}{% if message == user_messages[-1] %}{% if tools %}{{'[AVAILABLE_TOOLS]'+ tools|string + '[/AVAILABLE_TOOLS]'}}{% endif %}{{ '[INST]' + message['content'] + '[/INST]' }}{% else %}{{ '[INST]' + message['content'] + '[/INST]' }}{% endif %}{% elif message['role'] == 'assistant' %}{{ ' ' + message['content'] + ' ' + eos_token}}{% elif message['role'] == 'tool_results' %}{{'[TOOL_RESULTS]' + message['content']|string + '[/TOOL_RESULTS]'}}{% elif message['role'] == 'tool_calls' %}{{'[TOOL_CALLS]' + message['content']|string + eos_token}}{% endif %}{% endfor %}",
}

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


conversation = [
    {"role": "user", "content": "What's the weather like in Paris?"},
    {
        "role": "tool_calls",
        "content": [
            {
                "name": "get_current_weather",
                "arguments": {"location": "Paris, France", "format": "celsius"},
            }
        ],
    },
    {"role": "tool_results", "content": {"content": 22}},
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
result1 = tokenizer.apply_chat_template(
    conversation,
    chat_template="tool_use",
    tools=tools,
    tokenize=False,
    add_generation_prompt=True,
)
print(result1)

print("----- Applied on data + tokenized -----")
result = tokenizer.apply_chat_template(
    conversation,
    chat_template="tool_use",
    tools=tools,
    tokenize=True,
    add_generation_prompt=True,
)
print(result)

print("----- Decoded -----")
decoded = tokenizer.decode(result)
print(decoded)
