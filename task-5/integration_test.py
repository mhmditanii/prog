import unittest
import sys
import os
import random
import string

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import model
import controller
file_name = "test_file.json"

class integration_test(unittest.TestCase):

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

    def test_addingBook(self):
        controller.add_book(self.book_details_test)
        books = model.load_data()
        added_book = None

        for book in books:
            if (book['title'] == self.book_details_test[0] and book['author'] == self.book_details_test[1] and 
                book['year'] == self.book_details_test[2]):
                added_book = book
                break
        self.assertIsNotNone(added_book, "Book was not added to the model library")
        self.assertEqual(added_book['status'], "Available")

if __name__ == '__main__':
    unittest.main()


