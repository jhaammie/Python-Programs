
from book import Book


def sortByTitle(books):
    for a in range(0, len(books)):
        for i in range(0, len(books) - a - 1):
            if books[i].getTitle() > books[i+1].getTitle():
                extra = books[i]
                books[i] = books[i + 1]
                books[i + 1] = extra


def sortByAuthor(books):
    for a in range(0, len(books)):
        smallest = books[a]

        for i in range(a+1, len(books)):
            current = books[i]
            if smallest.getAuthor() > current.getAuthor():
                extra = books[i]
                books[i] = books[a]
                books[a] = extra
