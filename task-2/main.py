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
def open_file(access_type):
    try:
        file_path = find("library_data.json", os.getcwd())
        if file_path is None:
            raise FileNotFoundError("File not found!")
        current_file = open(file_path, access_type)
        return current_file
    except FileNotFoundError as error:
        print(f"{error}! Program will terminate!")
        quit()

def save_file(library_data):
    with open_file('w') as library:
        json.dump(library_data, library, indent = 4)

def list_books():
    with open_file('r') as library:
        library_data = json.load(library)
        for book in library_data.values():
            for details in book:  
                print(f"Title: {details['title']}")
                print(f"Author: {details['author']}")
                print(f"Year: {details['year']}")
                print('\n')

def add_book(book_details):
    with open_file('r') as library:
        library_data = load_data(library)
    if any(book_details[0] == book["title"] for books in library_data.values() for book in books):
        print("Book is already found!")
        return
    entry = {
        "title": book_details[0],
        "author": book_details[1],
        "year": book_details[-1]
    }
    author = book_details[1]
    if author in library_data:
        library_data[author].append(entry)
    else:
        library_data[author] = [entry]
    save_file(library_data)
    print("Book added successfully")



# Opening the file

list_books()
#add_book(("Zorba : The Greek", "Nikos Kazantzakis", 1946))
#print(data)
