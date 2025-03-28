import tkinter as tk
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
        json.dump(library_data, library, indent=4)

def list_books():
    library_data = load_data()
    for book in library_data:
        print(f"Title: {book['title']}")
        print(f"Author: {book['author']}")
        print(f"Year: {book['year']}")
        print('\n')

def add_book(book_details):
    library_data = load_data()
    for book in library_data:
        if book_details[0] == book["title"]:
            print("Book is already found!")
            return 
    entry = {
        "title": book_details[0],
        "author": book_details[1],
        "year": book_details[-1]
    }
    library_data.append(entry)
    save_file(library_data)
    print("Book added successfully")

def delete_book(book_name):
    library_data = load_data()
    for book in library_data:
        if book_name == book["title"]:
            library_data.remove(book)
            save_file(library_data)
            print(f"Book '{book_name}' deleted successfully")
            return
    print(f"Book '{book_name}' not found!")

add_book(("test","test1", 1222))

delete_book("test")

list_books()
