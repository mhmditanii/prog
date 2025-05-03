#asser.hussein@stud.th-deg.de
#robin.christ@stud.th-deg.de
#mohammad.itani@stud.th-deg.de

import model
from tkinter import messagebox
from collections import Counter


def add_book(book_details):
    for book in model.library:
        if book_details[0] == book["title"]:
            print("Book is already found!")
            return 
    entry = {
        "title": book_details[0].strip(),
        "author": book_details[1].strip(),
        "year": book_details[-1],
        "status": "Available"
    }
    model.library.append(entry)
    model.save_file()

def book_list_search(typed):
    if not typed:
        return 
    found_books = []
    check_length = len(typed)
    for book in model.library:
        if book['title'][0:check_length].lower() == typed.lower():
            found_books.append(book)
    return found_books

def book_edit_status(book_name, status_options, var):
    status = status_options[var.get()]
    for book in model.library:
        if book["title"] == book_name:
            book["status"] = status
            model.save_file()

def delete_book(book_title):
    for book in model.library:
        if book["title"] == book_title:
            book["status"] = "Deleted"
            print(f"Book '{book_title}' deleted successfully")
            return
    print(f"Book '{book_title}' was not found in the library!")
    model.save_file()

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
