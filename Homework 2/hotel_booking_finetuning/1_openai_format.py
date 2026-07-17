import json

# Paths to your files
input_file_path = "data/input_output.txt"
jsonl_file_path = "openai_format/all.jsonl"


def transform_txt_to_jsonl(input_file, output_file):
    system_message = {"role": "system", "content": "You are a helpful hotel booking assistant expert on Lighthouse Jurmala hotel booking terms and conditions. You provide accurate and clear information to help guests understand the hotel's policies."}
    transformed_data = []

    with open(input_file, "r", encoding="utf-8") as file:
        while True:
            # Get the next two lines
            input_line = file.readline().strip()
            output_line = file.readline().strip()

            # If the lines are empty, we've reached the end of the file
            if not input_line or not output_line:
                break

            # Process the two lines
            user_message = {
                "role": "user",
                "content": input_line.replace("Input: ", ""),
            }
            assistant_message = {
                "role": "assistant",
                "content": output_line.replace("Output: ", ""),
            }

            transformed_data.append(
                {"messages": [system_message, user_message, assistant_message]}
            )

    with open(output_file, "w", encoding="utf-8") as outfile:
        for data in transformed_data:
            outfile.write(json.dumps(data) + "\n")


transform_txt_to_jsonl(input_file_path, jsonl_file_path)
print(f"Successfully converted {input_file_path} to {jsonl_file_path}")
