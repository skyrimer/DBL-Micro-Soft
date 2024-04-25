import json
import os

directory = r"C:\Users\User\Desktop\BDS\DBL Data Challenge\data\\"


def list_files():
    files_list = []
    files = os.listdir(directory)
    print("Files in the directory:")
    for file in files:
        print(file)
        files_list.append(file)
    return files_list


def read_file(file_name):
    data_to_append = []
    print(f">>> {file_name}")
    # Open the JSON file for reading
    with open(directory+file_name, 'r') as file:
        # Read the entire file content
        file_content = file.read()

        # Split the content into separate JSON objects
        json_objects = file_content.strip().split('\n')
        for item in json_objects:
            try:
                if "124476322" in item or "lufthansa" in item or "Lufthansa" in item:
                    temp = json.loads(item)
                    # print(temp)
                    data_to_append.append(temp)
            except Exception as e:
                continue
    return data_to_append


def write_to_file(data):
    with open(r"C:\Users\User\Desktop\BDS\DBL Data Challenge\airlines\lufthansa.json", 'a', encoding='utf-8') as file:
        for string in data:
            file.write(str(string) + '\n')


x = list_files()
for file_thing in x:
    y = read_file(file_thing)
    write_to_file(y)
