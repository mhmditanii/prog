import model
from tkinter import messagebox

def list_books(): 
    library_data = model.load_data() 
    if not library_data: 
        return "No books available." 
    book_list = "" 
    for book in library_data:
        book_list += f"Title: {book['title']}\n"
        book_list += f"Author: {book['author']}\n"
        book_list += f"Year: {book['year']}\n\n"
    return book_list

def add_book(book_details):
    library_data = model.load_data()
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
    model.save_file(library_data)
    print("Book added successfully")

def delete_book(book_name):
    library_data = model.load_data()
    for book in library_data:
        if book_name == book["title"]:
            library_data.remove(book)
            model.save_file(library_data)
            print(f"Book '{book_name}' deleted successfully")
            return
    print(f"Book '{book_name}' not found!")

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

