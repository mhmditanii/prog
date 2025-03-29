import tkinter as tk
import os
import json
from tkinter import messagebox 
from tkinter import *

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
    if not library_data:
        return "No books available."
    book_list = ""
    for book in library_data:
        book_list += f"Title: {book['title']}\n"
        book_list += f"Author: {book['author']}\n"
        book_list += f"Year: {book['year']}\n\n"
    return book_list

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



# for the GUI we're using the following guide
# https://www.tutorialspoint.com/python/python_gui_programming.htm
def listing_button():
    messagebox.showinfo("Available Books", list_books())

def add_book_button():
    new_window = tk.Toplevel()
    new_window.title("Add a Book")
    new_window.geometry("300x160")
    
    fields = ['Book Name', 'Author', 'Publication Year']
    entries = makeform(new_window, fields)
    
    submit_button = tk.Button(new_window, text="Submit", command=lambda: book_collect_data(entries, new_window))
    submit_button.pack(pady=10)

def book_collect_data(entries, window):
    book_info = []
    for entry in entries:
        book_info.append(entry.get())
    add_book(book_info) 
    print("Book Added:", book_info)
    messagebox.showinfo("Success", "Book added successfully!")
    window.destroy()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Book Library")
        self.geometry("400x200")
        
        list_button = tk.Button(self, text="List Available Books", command=listing_button)
        list_button.pack(pady=10)
        
        add_button = tk.Button(self, text="Add Book", command=add_book_button)
        add_button.pack(pady=10)

def makeform(window, fields):
    entries = []
    for field in fields:
        row = tk.Frame(window)
        label = tk.Label(row, width=15, text=field, anchor='w')
        entry = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        label.pack(side=tk.LEFT)
        entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append(entry)
    return entries


app = App()
app.mainloop()
