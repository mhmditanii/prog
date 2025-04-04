import model
import controller
import tkinter as tk
from tkinter import messagebox 
from tkinter import *


# for the GUI we're using the following guides
# https://www.tutorialspoint.com/python/python_gui_programming.htm

def listing_button():
    messagebox.showinfo("Available Books", controller.list_books())

def add_book_button():
    new_window = tk.Toplevel()
    new_window.title("Add a Book")
    new_window.geometry("300x160")
    fields = ['Book Name', 'Author', 'Publication Year']
    entries = makeform(new_window, fields)
    submit_button = tk.Button(new_window, text="Submit", command=lambda: controller.book_collect_data(entries, new_window))
    submit_button.pack(pady=10)

def delete_book_button():
    new_window = tk.Toplevel()
    new_window.title("Delete a Book")
    new_window.geometry("300x120")
    row = tk.Frame(new_window)
    label = tk.Label(row, width=15, text="Book Name", anchor='w')
    entry = tk.Entry(row)
    row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
    label.pack(side=tk.LEFT)
    entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
    submit_button = tk.Button(new_window, text="Delete", command=lambda: controller.delete_and_close(entry, new_window))
    submit_button.pack(pady=10)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Book Library")
        self.geometry("300x200")
        list_button = tk.Button(self, text="List Available Books", command=listing_button)
        list_button.pack(pady=10)
        add_button = tk.Button(self, text="Add Book", command=add_book_button)
        add_button.pack(pady=10)
        delete_button = tk.Button(self, text="Delete Book", command=delete_book_button)
        delete_button.pack(pady=10)

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

