# 3. Write a class for a library system that allows adding/removing books and searching by title.

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title):
        self.books.append(title)
        print("Book added:", title)

    def remove_book(self, title):
        if title in self.books:
            self.books.remove(title)
            print("Book removed:", title)
        else:
            print("Book not found")

    def search_book(self, title):
        if title in self.books:
            print("Book found:", title)
        else:
            print("Book not found")


library = Library()

library.add_book("Python Basics")
library.add_book("Learn JavaScript")

library.search_book("Python Basics")
library.remove_book("Learn JavaScript")
library.search_book("Learn JavaScript")