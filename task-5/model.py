#asser.hussein@stud.th-deg.de
#robin.christ@stud.th-deg.de
#mohammad.itani@stud.th-deg.de

import os
import json
from tkinter import filedialog
from json.decoder import JSONDecodeError


file_path = "lib_default.json"
library = []

def load_data():
    global library
    return library

def load_image():
    image_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open image okay?",
                                      filetypes=[("Image files", "*.webp *.png *.jpg *.jpeg"),("All files", "*.*")]
                                    )
    return image_path

def update_file_path():
    global file_path
    file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open file okay?", filetypes=[("JSON files", "*.json")])
    open_file()

def create_file():
    global file_path
    file_path = filedialog.asksaveasfilename(
    initialdir=os.getcwd(),
    title="Save New File",
    defaultextension=".json",
    filetypes=[("JSON files", "*.json")])
    with open(file_path, 'w') as new_file:
        json.dump({}, new_file)

def open_file():
    global file_path
    global library
    try:
        with open(file_path, 'r') as working_file:
            try:
                library = json.load(working_file)
            except JSONDecodeError:
                pass
    except IOError:
        print("Could not open/read file:", file_path)

def save_file():
    global file_path
    global library
    with open(file_path, 'w') as working_file:
        json.dump(library, working_file, indent=4)
