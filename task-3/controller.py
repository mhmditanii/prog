#asser.hussein@stud.th-deg.de
#robin.christ@stud.th-deg.de
#mohammad.itani@stud.th-deg.de

import model
from tkinter import messagebox
from collections import Counter

def list_books(): 
    library_data = model.load_data() 
    if not library_data: 
        return "No books available." 
    book_list = "" 
    for book in library_data:
        book_list += f"Title: {book['title']}\n"
        book_list += f"Author: {book['author']}\n"
        book_list += f"Year: {book['year']}\n"
        book_list += f"Status: {book['status']}\n\n"
    return book_list

def list_book_titles():
    library_data = model.load_data()
    if not library_data:
        return []
    return [book['title'] for book in library_data]

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
            return library_data, book
    return library_data, None

def book_list_search(typed):
    if not typed:
        return
    library_data = model.load_data()
    found_books = []
    typed_counter = Counter(typed.lower())
    for book in library_data:
        title_counter = Counter(book["title"].lower())
        if all(title_counter[char] >= count for char, count in typed_counter.items()):
            found_books.append(book)
    return found_books

def book_edit_status(book_name, status_options, var):
    library_data, found_book = book_search(book_name)
    status = status_options[var.get()]
    found_book["status"] = status
    model.save_file(library_data)


def delete_book(book_name):
    library_data, found_book = book_search(book_name)
    if not found_book:
        print(f"Book '{book_name}' was not found in the library!")
        return
    #library_data.remove(found_book)
    found_book["status"] = "Deleted"
    model.save_file(library_data)
    print(f"Book '{book_name}' deleted successfully")

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
