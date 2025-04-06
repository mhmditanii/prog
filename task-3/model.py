#asser.hussein@stud.th-deg.de
#robin.christ@stud.th-deg.de
#mohammad.itani@stud.th-deg.de

import os
import json
from tkinter import filedialog

default_file_name = "lib_default.json"
global_file_path = ""

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None

def load_data():
    with open_file('r') as current_file:
        return json.load(current_file)

def openFile():
    global global_file_path
    global_file_path = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title="Open file okay?",
                                          filetypes=[("JSON files", "*.json")]
                                        )

def createFile():
    global global_file_path
    global_file_path = filedialog.asksaveasfilename(
    initialdir=os.getcwd(),
    title="Save New File",
    defaultextension=".json",
    filetypes=[("JSON files", "*.json")])
    with open(global_file_path, 'w') as new_file:
        json.dump({}, new_file)

def open_file(access_type):
    try:
        if not global_file_path:
            file_path = find("lib_default.json", os.getcwd())
            if file_path is None:
                raise FileNotFoundError("File not found!")
        else:
            file_path = global_file_path
        current_file = open(file_path, access_type)
        return current_file
    except FileNotFoundError as error:
        print(f"{error}! Program will terminate!")
        quit()

def save_file(library_data):
    with open_file('w') as library:
        json.dump(library_data, library, indent=4)

