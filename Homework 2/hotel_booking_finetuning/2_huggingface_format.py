import json

# Paths to your files
input_file_path = "data/input_output.txt"
json_file_path = "huggingface_format/all.json"


def transform_txt_to_json(input_file, output_file):
    result = []

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

            result.append({"text": [user_message, assistant_message]})

    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(result, indent=2))


transform_txt_to_json(input_file_path, json_file_path)
print(f"Successfully converted {input_file_path} to {json_file_path}")
