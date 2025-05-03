import unittest
import sys
import os
import time
import tkinter as tk
from tkinter import ttk
from tkinter import *

file_name = "test_file.json"

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import model
import controller
import view1

class system_test(unittest.TestCase):

    def setUp(self):
        global file_name
        model.file_path = file_name
        with open(file_name, mode='a'):
            pass
        self.app = view1.App()

    def tearDown(self):
        if hasattr(self, 'app') and self.app:
            self.app.quit()
            self.app.destroy()
        try:
            os.remove(model.file_path)
        except FileNotFoundError:
            print(f"File '{model.file_path}' not found.")

    def test_add_book(self):
        initial_count = len(self.app.library)
        for widget in self.app.winfo_children():
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    if hasattr(child, 'winfo_children'):
                        for button in child.winfo_children():
                            if isinstance(button, tk.Button):
                                if hasattr(button, 'cget') and button.cget('text') == "Add Book":
                                    button.invoke()
                                    break

        self.test_add_book_helper()
        time.sleep(1)
        self.app.update()
        self.assertEqual(len(self.app.library), initial_count + 1, "Book should be added to library")
        book_titles = [book["title"] for book in self.app.library]
        self.assertIn("Test Book", book_titles, "Added book not found in library")
        total_books_text = self.app.total_books_label.cget("text")
        self.assertEqual(total_books_text, f"Total Books: {len(self.app.library)}",
                         "Total Books label not updated correctly")

    def test_add_book_helper(self):
        for window in self.app.winfo_children():
            if hasattr(window, 'title') and window.title() == "Add a Book":
                entries = []
                for frame in window.winfo_children():
                    if hasattr(frame, 'winfo_children'):
                        for widget in frame.winfo_children():
                            if hasattr(widget, 'insert') and hasattr(widget, 'get'):
                                entries.append(widget)
                if len(entries) >= 3:
                    entries[0].insert(0, "Test Book")
                    entries[1].insert(0, "Test Author")
                    entries[2].insert(0, "2023")
                for widget in window.winfo_children():
                    if hasattr(widget, 'cget') and hasattr(widget, 'invoke') and widget.cget('text') == "Submit":
                        widget.invoke()
                        break
                break

if __name__ == "__main__":
    unittest.main()

