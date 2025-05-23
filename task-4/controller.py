#asser.hussein@stud.th-deg.de
#robin.christ@stud.th-deg.de
#mohammad.itani@stud.th-deg.de

import model
from tkinter import messagebox
from collections import Counter


def list_books():
    library_data = model.load_data()
    if not library_data:
        return []
    return library_data

def add_book(book_details):
    library_data = model.load_data()
    if not library_data:
        library_data = []
    for book in library_data:
        if book_details[0] == book["title"]:
            print("Book is already found!")
            return 
    entry = {
        "title": book_details[0].strip(),
        "author": book_details[1].strip(),
        "year": book_details[-1],
        "status": "Available"
    }
    library_data.append(entry)
    model.save_file(library_data)

def book_search(book_name):
    library_data = model.load_data()
    for book in library_data:
        if book_name.strip() == book["title"]:
            return book
    return None

def book_list_search(typed):
    if not typed:
        return
    library_data = model.load_data()
    found_books = []
    check_length = len(typed)
    for book in library_data:
        if book['title'][0:check_length].lower() == typed.lower():
            found_books.append(book)
    return found_books

def book_edit_status(book_name, status_options, var):
    library_data = model.load_data()
    status = status_options[var.get()]
    for book in library_data:
        if book["title"] == book_name:
            book["status"] = status
            model.save_file(library_data)

def delete_book(book_title):
    library_data = model.load_data() 
    for book in library_data:
        if book["title"] == book_title:
            book["status"] = "Deleted"
            model.save_file(library_data)
            print(f"Book '{book_title}' deleted successfully")
            return
    print(f"Book '{book_title}' was not found in the library!")

def book_collect_data(entries, window):
    book_info = []
    for entry in entries:
        book_info.append(entry.get())
    add_book(book_info)
    print("Book Added:", book_info)
    messagebox.showinfo("Success", "Book added successfully!")
    window.destroy()

def delete_and_close(entry, window):
    book_name = entry.get()
    delete_book(book_name)
    messagebox.showinfo("Success", f"Book '{book_name}' deleted successfully!")
    window.destroy()
