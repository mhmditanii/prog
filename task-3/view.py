import model
import controller
import tkinter as tk
from tkinter import messagebox 
from tkinter import *
from tkinter import ttk

def donothing():
    x = 3

#inspired by (https://tkdocs.com/tutorial/morewidgets.html)
def listing_button():
    list_window = tk.Toplevel()
    list_window.title("Available Books")
    list_window.geometry("480x380")

    def edit_button_pressed(book_name):
        new_window = tk.Toplevel()
        new_window.geometry("160x120")
        status_options = {1: "Available", 2: "Missing", 3: "Lent Out"}
        var = IntVar()
        for key, option in status_options.items():
            rb = Radiobutton(new_window, text=option, variable=var, value=key)
            rb.pack(anchor=W)
        
        def submit_and_close():
            controller.book_edit_status(book_name, status_options, var)
            new_window.destroy()

        submit_button = tk.Button(new_window, text="Submit", command=submit_and_close)
        submit_button.pack(pady=10)

    def delete_button_pressed(): 
        controller.delete_book(lbox.get(ANCHOR)) 

    book_titles = controller.list_book_titles()
    book_names = StringVar(value=book_titles)

    c = ttk.Frame(list_window, padding=(10, 10, 12, 0))

    c.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

    list_window.grid_columnconfigure(0, weight=1)
    list_window.grid_rowconfigure(0, weight=1)

    lbox = tk.Listbox(c, listvariable=book_names, height=15)
    lbl = ttk.Label(c, text="Edit/Delete Selected Item:")
    edit = ttk.Button(c, text='Edit', command= lambda: edit_button_pressed(lbox.get(ANCHOR)), default='active')
    delete = ttk.Button(c, text='Delete', command=delete_button_pressed, default='active')

    lbox.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W), padx=5, pady=5)
    lbl.grid(column=0, row=1, padx=10, pady=5)
    edit.grid(column=0, row=2, sticky=tk.EW, padx=10, pady=5)
    delete.grid(column=0, row=3, sticky=tk.EW, padx=10, pady=5)
    c.grid_columnconfigure(0, weight=1)

   #for i in range(0, len(book_names.get()), 2):
        #lbox.itemconfigure(i, background='#f0f0ff')

def add_book_button():
    new_window = tk.Toplevel()
    new_window.title("Add a Book")
    new_window.geometry("400x350")
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

