import os
import json


# Function to save interview data locally
async def save_to_local(file_name: str, content: dict):
    # Define the directory path where the files will be stored
    local_dir = "interviews"  # This is the folder to store the files
    os.makedirs(local_dir, exist_ok=True)  # Create the directory if it doesn't exist

    file_path = os.path.join(local_dir, file_name)

    # Write the content as a JSON file
    with open(file_path, "w") as f:
        json.dump(content, f, indent=4)