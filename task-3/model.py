import os
import json


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None

def load_data():
    with open_file('r') as current_file:
        return json.load(current_file)

def open_file(access_type):
    try:
        file_path = find("lib_default.json", os.getcwd())
        if file_path is None:
            raise FileNotFoundError("File not found!")
        current_file = open(file_path, access_type)
        return current_file
    except FileNotFoundError as error:
        print(f"{error}! Program will terminate!")
        quit()

def save_file(library_data):
    with open_file('w') as library:
        json.dump(library_data, library, indent=4)

