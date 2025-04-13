#asser.hussein@stud.th-deg.de
#robin.christ@stud.th-deg.de
#mohammad.itani@stud.th-deg.de

import controller
import model
import tkinter as tk
from tkinter import ttk
from tkinter import *
import threading
from PIL import ImageTk, Image
import pyocr
import pyocr.builders



# layout inspired by "https://www.pythonguis.com/tutorials/use-tkinter-to-design-gui-layout/"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Book Library")
        self.geometry("900x800")
        
        # menu
        menu = Menu(self)
        self.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='New', command=self.create_new_file)
        filemenu.add_command(label='Open', command=self.open_new_file)

        # left side of the window
        left_frame = tk.Frame(self, width=400)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, expand=True, padx=10, pady=10)

        # search call back inspired by "https://www.geeksforgeeks.org/tracing-tkinter-variables-in-python/"
        self.search_var = StringVar()
    
        def search_callback(var,index, mode):
            found_books = controller.book_list_search(self.search_var.get())
            if not found_books: 
                self.update_search_results([])
            else:
                self.update_search_results(found_books)
        

        self.search_var.trace_add('write', search_callback)
        self.search_count_label = tk.Label(left_frame, text="Search Results: 0")
        self.search_count_label.pack()
        Label(left_frame, textvariable = self.search_var).pack(pady = 2)
        Entry(left_frame, textvariable = self.search_var).pack(pady = 5)
        self.search_listbox = tk.Listbox(left_frame, height=5)
        self.search_listbox.pack(fill=X, padx=6, pady=1)
        
        self.generate_button = tk.Button(left_frame, text="Generate 1 Million Book Entries",)
        self.generate_button.pack(pady=5)
        self.stop_button = tk.Button(left_frame, text="Stop Generation")
        self.stop_button.pack(pady=5)
        
        image_process_frame = tk.Frame(left_frame)
        image_process_frame.pack(fill=tk.BOTH, pady=4)
        self.image_canvas_frame = tk.Frame(image_process_frame, height=10, background="#ffffff", highlightbackground="#000000", bd=3, highlightthickness=2)
        self.image_canvas_frame.pack()
        self.image_canvas = Canvas(self.image_canvas_frame, height=420, bg="#f0f0f0")
        self.image_canvas.pack(fill='both', expand=TRUE)
        self.image_upload_button = tk.Button(image_process_frame, text="Upload Image", command=self.load_image)
        self.image_upload_button.pack(padx=2, pady=2)
        self.image_loaded_tk = NONE
        
        # key bindings to track mouse position and draw rectangle
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.rect_id = None
        self.text_label = tk.Label(left_frame, text="Text Selected: ", font=("Helvetica", 12))
        self.text_label.pack(pady=10)

        # Set up OCR tool (pyocr)
        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            raise Exception("No OCR tool found")
        self.tool = tools[0]  # Using the first available OCR tool (usually Tesseract)

        # Bind mouse events
        self.image_canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.image_canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.image_canvas.bind("<ButtonRelease-1>", self.on_button_release)




###########################################################################
        # right side of the window
        right_frame = tk.Frame(self)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        listbox_frame = tk.Frame(right_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)

        self.book_titles = controller.list_books()
        #self.book_titles = book_titles
        self.book_var = StringVar(value=[book["title"] for book in self.book_titles])
        self.lbox = tk.Listbox(listbox_frame, listvariable=self.book_var, height=15)
        self.lbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.lbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lbox.config(yscrollcommand=scrollbar.set)
        self.lbox.bind("<Double-1>", self.open_details_window)

        buttons_frame = tk.Frame(right_frame)
        buttons_frame.pack(fill=tk.X, pady=10)

        add_button = tk.Button(buttons_frame, text="Add Book", command=lambda: self.open_add_book())
        add_button.pack(side=tk.LEFT,padx=5)
        edit_button = tk.Button(buttons_frame, text="Edit", command=lambda: self.open_edit_window(self.lbox.get(tk.ANCHOR)))
        edit_button.pack(side=tk.LEFT, padx=5)
        delete_button = tk.Button(buttons_frame,text="Delete",command=lambda: controller.delete_book(self.lbox.get(tk.ANCHOR)))
        delete_button.pack(side=tk.LEFT, padx=5)
        self.total_books_label = tk.Label(buttons_frame, text=f"Total Books: {len(controller.list_books())}")
        self.total_books_label.pack(side=tk.RIGHT, padx=10)

    # function to refresh the book list whenever a new one is added
    def refresh_book_var(self):
        book_titles = controller.list_books()
        self.book_titles = book_titles
        self.book_var.set([book["title"] for book in book_titles])
        self.total_books_label.config(text=f"Total Books: {len(book_titles)}")

    def refresh_search_results(self, search_variable):
        book_titles = controller.book_list_search(search_variable)
        self.book_var.set(book_titles)
        self.total_books_label.config(text=f"Total Books: {len(book_titles)}")

    def open_details_window(self, event):
        self.book_titles = controller.list_books()
        selection = self.lbox.curselection()
        if not selection:
            return
        index = selection[0]
        book = self.book_titles[index]

        details_window = tk.Toplevel(self)
        details_window.title(f"Details: {book['title']}")

        tk.Label(details_window, text=f"Book Name: {book['title']}").pack(padx=10, pady=5)
        tk.Label(details_window, text=f"Author: {book['author']}").pack(padx=10, pady=5)
        tk.Label(details_window, text=f"Publication Year: {book['year']}").pack(padx=10, pady=5)
        tk.Label(details_window, text=f"Status: {book['status']}").pack(padx=10, pady=5)

    def update_search_results(self, found_books):
        self.search_listbox.delete(0, tk.END)
        for book in found_books:
            self.search_listbox.insert(tk.END, book["title"])
        self.search_count_label.config(text=f"Search Results: {len(found_books)}")

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
    
    def open_new_file(self):
        model.openFile(False)
        self.refresh_book_var()
   
    def create_new_file(self):
        model.createFile()
        self.refresh_book_var()

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

    def load_image(self):
        image_path = model.openFile(True)
        self.image_loaded = Image.open(image_path)
        print("DIMENSTIONS ", self.winfo_reqheight(), self.winfo_reqwidth())
        self.image_loaded = self.image_loaded.resize((self.image_canvas.winfo_reqwidth(), self.image_canvas.winfo_reqheight()))
        self.image_loaded_tk = ImageTk.PhotoImage(self.image_loaded)
        self.image_canvas.create_image(0, 0, anchor='nw', image=self.image_loaded_tk)
        print("UPLOADED SUCCESFULLY")

    def on_button_press(self, event):
        # When a new rectangle starts, delete the previous one
        if self.rect_id:
            self.image_canvas.delete(self.rect_id)
        
        # Store the initial position when the mouse button is pressed
        self.start_x = event.x
        self.start_y = event.y

        # Create a new placeholder rectangle (empty)
        self.rect = self.image_canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2)
        self.rect_id = self.rect  # Store the ID of the current rectangle

    def on_mouse_drag(self, event):
        self.image_canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
        
    def on_button_release(self, event):
        self.image_canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
        # Perform OCR on the selected area
        self.recognize_text_in_rectangle(self.start_x, self.start_y, event.x, event.y)

    def recognize_text_in_rectangle(self, x1, y1, x2, y2):
        # Crop the image based on the selected area
        cropped_image = self.image_loaded.crop((x1, y1, x2, y2))

        # Convert the cropped image to text using pyocr
        selected_text = self.tool.image_to_string(cropped_image, lang='eng', builder=pyocr.builders.TextBuilder())

        # Display the recognized text in the label
        self.text_label.config(text=f"Recognized Text: {selected_text.strip()}")
        self.search_var.set(selected_text.strip().lower())
