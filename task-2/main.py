import tkinter as tk
import os
import json


# searches for the file and return None if file does not exist
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None

def load_data(current_file):
    return json.load(current_file)

# takes care of file handling errors
def open_file():
    try:
        file_path = find("library_data.json", os.getcwd())
        if file_path is None:
            raise FileNotFoundError("File not found!")
        current_file = open(file_path, "r+")
        return current_file
    except FileNotFoundError as error:
        print(f"{error}! Program will terminate!")
        quit()

def list_books(library_dict):
    for book in library_dict.values():
        for details in book:  
            print(f"Title: {details['title']}")
            print(f"Author: {details['author']}")
            print(f"Year: {details['year']}")
            print('\n')


# Opening and loading data
library = open_file()
data = load_data(library)

list_books(data)

#print(data)
