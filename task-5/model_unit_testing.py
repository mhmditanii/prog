import unittest
import random
import sys
import os
import string
from pathlib import Path

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import model

file_name = "test_file.json"

class test_model(unittest.TestCase):

    def setUp(self):
        global file_name
        title_test = ''.join(random.choices(string.ascii_uppercase + string.digits, k=18))
        author_test = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)) 
        year_test = random.randint(1800,2025)
        self.book_details_test = [title_test,author_test,year_test]
        model.file_path = file_name
        with open(file_name, mode='a'): pass 

    def tearDown(self):
        try:
            os.remove(model.file_path)
        except FileNotFoundError:
            print(f"File '{model.file_path}' not found.")

    def test_createFile(self):
        model.create_file()
        name = model.file_path
        file_exist = False
        for root, dirs, files in os.walk(os.getcwd()):
            if os.path.basename(name) in files:
                file_exist = True
        self.assertTrue(file_exist, "File does not exist in the directory")

    # the way of comparison used is naive because there exist overhead for data structures and different writing conventions in .json files. 
    def test_saveFile(self):
        model.library.append(self.book_details_test)
        model.save_file()
        expected_size = sum(sys.getsizeof(item) for item in model.library) - 2
        self.assertEqual(os.stat(os.path.abspath(file_name)).st_size, expected_size)

    def test_loadImage(self):
        self.assertTrue(Path(model.load_image()).suffix in [".png", ".jpg", ".jpeg", ".webp"], "File loaded was not of type image")

if __name__ == '__main__':
    unittest.main()

