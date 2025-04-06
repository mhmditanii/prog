import controller
import model
import tkinter as tk
from tkinter import ttk
from tkinter import *

# layout inspired by "https://www.pythonguis.com/tutorials/use-tkinter-to-design-gui-layout/"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Book Library")
        self.geometry("700x400")
        
        # menu
        menu = Menu(self)
        self.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='Open')

        # left side of the window
        left_frame = tk.Frame(self, width=200)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        add_button = tk.Button(left_frame, text="Add Book", command=lambda: self.open_add_book())
        add_button.pack(pady=10)
        
        # search call back inspired by "https://www.geeksforgeeks.org/tracing-tkinter-variables-in-python/"
        search_var = StringVar()
        
        def search_callback(var,index, mode):
            found_books = controller.book_list_search(search_var.get())
            if not found_books: 
                self.update_search_results([])
            else:
                self.update_search_results(found_books)
        

        search_var.trace_add('write', search_callback)
        Label(left_frame, textvariable = search_var).pack(pady = 15)
        Entry(left_frame, textvariable = search_var).pack(pady = 15)
        self.search_listbox = tk.Listbox(left_frame, height=5)
        self.search_listbox.pack(fill=X, padx=6, pady=1)
        

        # right side of the window
        right_frame = tk.Frame(self)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        book_titles = controller.list_book_titles()
        self.book_var = StringVar(value=book_titles)
        self.lbox = tk.Listbox(right_frame, listvariable=self.book_var, height=15)
        self.lbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        buttons_frame = tk.Frame(right_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        edit_button = tk.Button(
            buttons_frame,
            text="Edit",
            command=lambda: self.open_edit_window(self.lbox.get(ANCHOR))
        )
        edit_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(
            buttons_frame,
            text="Delete",
            command=lambda: controller.delete_book(self.lbox.get(ANCHOR))
        )
        delete_button.pack(side=tk.LEFT, padx=5)
        
    # function to refresh the book list whenever a new one is added
    def refresh_book_var(self):
        self.book_var.set(controller.list_book_titles())
    
    def update_search_results(self, found_books):
        self.search_listbox.delete(0, tk.END)
        for book in found_books:
            self.search_listbox.insert(tk.END, book["title"])

    def open_add_book(self):
        new_window = tk.Toplevel(self)
        new_window.title("Add a Book")
        new_window.geometry("400x350")

        fields = ['Book Name', 'Author', 'Publication Year']
        entries = []
        for field in fields:
            row = tk.Frame(new_window)
            label = tk.Label(row, width=15, text=field, anchor='w')
            entry = tk.Entry(row)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            label.pack(side=tk.LEFT)
            entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            entries.append(entry)

        submit_button = tk.Button(
            new_window,
            text="Submit",
            command=lambda:( 
                    controller.book_collect_data(entries, new_window),
                   self.refresh_book_var() 
            )
        )
        submit_button.pack(pady=10)

    def open_edit_window(self, book_name):
        if not book_name:
            return
        new_window = tk.Toplevel(self)
        new_window.geometry("200x150")
        new_window.title(f"Edit: {book_name}")
        status_options = {1: "Available", 2: "Missing", 3: "Lent Out"}
        var = IntVar()
        for key, option in status_options.items():
            tk.Radiobutton(new_window, text=option, variable=var, value=key).pack(anchor=W)

        submit_button = tk.Button(
            new_window,
            text="Submit",
            command=lambda: (controller.book_edit_status(book_name, status_options, var), new_window.destroy())
        )
        submit_button.pack(pady=10)

