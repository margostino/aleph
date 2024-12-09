import os

files_base_path = os.getenv("FILES_BASE_PATH")


def get_files_content():
    # fix this to only read ALL TXT files
    files = os.listdir(files_base_path)
    files_content = []
    for file in files:
        if file.endswith(".txt"):
            with open(f"{files_base_path}/{file}", "r", encoding="utf-8") as file:
                print(f"Reading file: {file}")
                file_content = file.read()
                files_content.append(file_content)
    return files_content
