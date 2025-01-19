
"""

Input title and author of the book and save in list
Option to view all books
Sort list of books on title or author

"""


class Book:

    def __init__(self, author, title):
        self.__author = author
        self.__title = title

    def getAuthor(self):
        print(self.__author)
        return self.__author

    def getTitle(self):
        print(self.__title)
        return self.__title

    def toJson(self):
        info = {
            "Title": self.__title,
            "Author": self.__author
        }
        return info

    def __str__(self):
        return f"Title: {self.__title}, Author: {self.__author}"

    def __eq__(self, other):
        return self.__title == other.__title and self.__author == other.__author
