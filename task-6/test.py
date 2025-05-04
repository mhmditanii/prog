import view1
import controller
import model
import tkinter as tk
from tkinter import ttk
from tkinter import *
from line_profiler import LineProfiler
import psutil
import os
import time
import pyocr
import pyocr.builders

file_name = "data_profiling.json"
model.file_path = file_name
with open(file_name, mode='w'):
    pass

lp = LineProfiler()
lp.add_function(model.save_file)
lp.add_function(model.open_file)

app = view1.App()

start_time = time.time()

ps = psutil.Process(os.getpid())
io_before = psutil.disk_io_counters()


@lp
def profiling():
    for i in range(1000):
        model.library.append({
            "title": f"book{i}",
            "author": f"author{i}",
            "year": 2000,
            "status": "Available"
        })
        model.save_file()

profiling()

@lp
def automated_ocr():
    image = app.image_loaded
    tool = app.tool
    full_text = tool.image_to_string(image, lang='eng', builder=pyocr.builders.TextBuilder())
    return full_text.strip()



app.load_image()

recognized_text = automated_ocr()
print("OCR Output:\n", recognized_text)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time taken to run the app with the generating function: {elapsed_time} seconds")

lp.print_stats()

io_after = psutil.disk_io_counters()
print("Bytes written:", io_after.write_bytes - io_before.write_bytes)
print("Bytes read:", io_after.read_bytes - io_before.read_bytes)

app.quit()
app.destroy()
