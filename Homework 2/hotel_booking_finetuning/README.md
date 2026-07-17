# Hotel Booking Fine-tuning Dataset

## Overview

This project prepares a fine-tuning dataset for teaching language models about the Lighthouse Jurmala hotel's booking terms and conditions. The dataset is designed to help train models to accurately answer guest questions about hotel policies, cancellation rules, check-in procedures, and payment requirements.

## Dataset Description

The dataset consists of **74 question-answer pairs** covering comprehensive information about:

- **Booking Methods**: Email, website, and online reservation systems
- **Reservation Requirements**: Required guest information and credit card details
- **Payment Methods**: Accepted credit cards (American Express, Visa, MasterCard, Maestro)
- **High Season Policy**: Special requirements for July 1 - August 15 period
- **Guaranteed Reservations**: Credit card guarantees and prepayment options
- **Cancellation Policy**: 72-hour cancellation window and penalties
- **High Season Cancellation**: No-refund policy during peak season
- **Check-in/Check-out**: Standard times and procedures
- **Early Check-in/Late Check-out**: Availability and additional costs
- **Required Documentation**: ID requirements and credit card policies
- **Deposits**: Cash deposit alternatives (200 EUR)
- **Force Majeure**: Hotel cancellation rights and guest compensation

## Dataset Structure

### Source Data Format

The raw data is stored in `data/input_output.txt` with the following format:

```
Input: [Guest question]
Output: [Detailed answer based on hotel policy]
Input: [Next question]
Output: [Next answer]
...
```

### Output Formats

The dataset is converted into two industry-standard formats:

#### 1. OpenAI Format (JSONL)
Located in `openai_format/` directory:
- `all.jsonl` - Complete dataset
- `train.jsonl` - Training split (80%)
- `validation.jsonl` - Validation split (20%)

Structure:
```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful hotel booking assistant expert on Lighthouse Jurmala hotel booking terms and conditions."
    },
    {
      "role": "user",
      "content": "How can I make a booking at the hotel?"
    },
    {
      "role": "assistant",
      "content": "You can make a booking by writing a request to..."
    }
  ]
}
```

#### 2. HuggingFace Format (JSON)
Located in `huggingface_format/` directory:
- `all.json` - Complete dataset
- `train.json` - Training split (80%)
- `validation.json` - Validation split (20%)

Structure:
```json
{
  "text": [
    {
      "role": "user",
      "content": "How can I make a booking at the hotel?"
    },
    {
      "role": "assistant",
      "content": "You can make a booking by writing a request to..."
    }
  ]
}
```

## Usage Instructions

### Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses only standard library)

### Step 1: Prepare Data

The source data is already prepared in `data/input_output.txt`. This file contains 74 carefully crafted question-answer pairs based on the hotel's actual booking terms.

### Step 2: Generate OpenAI Format

```bash
python 1_openai_format.py
```

This will create `openai_format/all.jsonl` containing the full dataset in OpenAI's fine-tuning format.

### Step 3: Generate HuggingFace Format

```bash
python 2_huggingface_format.py
```

This will create `huggingface_format/all.json` containing the full dataset in HuggingFace's format.

### Step 4: Create Train/Validation Splits

```bash
python 3_train_validation_split.py
```

This will:
- Split both formats into 80% training and 20% validation sets
- Use random seed 42 for reproducibility
- Create train.jsonl and validation.jsonl (OpenAI format)
- Create train.json and validation.json (HuggingFace format)

Expected output:
- ~59 samples in training set
- ~15 samples in validation set

## File Structure

```
hotel_booking_finetuning/
├── data/
│   └── input_output.txt          # Source Q&A pairs
├── openai_format/
│   ├── all.jsonl                 # Complete OpenAI format dataset
│   ├── train.jsonl               # Training split
│   └── validation.jsonl          # Validation split
├── huggingface_format/
│   ├── all.json                  # Complete HuggingFace format dataset
│   ├── train.json                # Training split
│   └── validation.json           # Validation split
├── 1_openai_format.py            # OpenAI format converter
├── 2_huggingface_format.py       # HuggingFace format converter
├── 3_train_validation_split.py  # Train/validation splitter
└── README.md                     # This file
```

## Fine-tuning Recommendations

### OpenAI Models

Use the generated `openai_format/train.jsonl` and `openai_format/validation.jsonl` files with OpenAI's fine-tuning API:

```bash
openai api fine_tunes.create \
  -t "openai_format/train.jsonl" \
  -v "openai_format/validation.jsonl" \
  -m gpt-3.5-turbo \
  --suffix "hotel-booking-assistant"
```

### HuggingFace Models

Use the generated `huggingface_format/train.json` and `huggingface_format/validation.json` files with HuggingFace's Transformers library for fine-tuning models like:
- Mistral
- Llama 2/3
- Phi-2/3
- Gemma

## Dataset Quality

The dataset was carefully constructed to:
- ✅ Cover all aspects of the hotel's booking policy
- ✅ Provide accurate, detailed answers based on official terms
- ✅ Include common guest questions and edge cases
- ✅ Maintain consistent formatting and structure
- ✅ Use clear, professional language
- ✅ Include specific details (dates, amounts, email addresses, times)

## Source Material

The dataset is based on the official booking terms and conditions from Lighthouse Jurmala hotel, as documented in `Hotel Booking terms.md`.

## Use Cases

After fine-tuning, the model can be used for:
- Customer service chatbots
- Hotel booking assistants
- FAQ automation
- Guest inquiry handling
- Pre-arrival information systems
- Virtual hotel concierge services

## License

This dataset is prepared for educational purposes as part of AI Engineering coursework.

## Contact

For questions about this dataset preparation, refer to the course materials in:
`C:\Users\Admin\Documents\Training\AI Engineering\Homeworks\Homework2\3_data_preparation`
