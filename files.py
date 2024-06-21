import os

FILE_DIRECTORY = 'product_info'
OUTPUT_FILE = "tropicanaData.txt"

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f_output:
    for filename in os.listdir(FILE_DIRECTORY):
        file_path = os.path.join(FILE_DIRECTORY, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            f_output.write(content + "\n")

with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
    print(f.read())
