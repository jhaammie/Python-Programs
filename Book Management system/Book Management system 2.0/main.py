
# Simple flask application
# Importing what I need
from flask import Flask, request
from flask_cors import CORS
from book import Book
from db import exists, insertbook, SortBooks
# Defining app
app = Flask(__name__)  # Creates an instance of app
CORS(app)  # Allows a web page to access restricted resources from a server on a domain different from the domain that served the web page


@app.route('/books/add', methods=["POST"])
def addBook():
    content = request.json
    a = content["title"]
    b = content["author"]

    if a is None or a.strip() == "":  # Strip() removes extra whitespaces and specified characters from the start and from the end of the strip irrespective of how the parameter is passed.
        return "Please enter a valid title", 400
    elif b is None or b.strip() == "":
        return "Please enter a valid author", 400
    book = Book(b.strip(), a.strip())

    if not exists(book.getTitle(), book.getAuthor()):
        insertbook(book.getTitle(), book.getAuthor())
        return "Book successfully added!"
    else:
        return "Book already exists", 400


@app.route('/books', methods=["GET"])
def getBooks():
    Newlst = []
    ConvertToJsonList(SortBooks(None), Newlst)
    return Newlst


@app.route('/books/sort', methods=["GET"])
def Sort():
    Newlst = []
    sortby = request.args.get('by')
    if sortby == 'author':
        sorting = SortBooks("author")
    elif sortby == 'title':
        # sortByTitle(CopyOfLst)
        sorting = SortBooks("title")
    else:
        return "Please enter a valid author or title", 400

    ConvertToJsonList(sorting, Newlst)
    return Newlst


# Creating function because it's common in both getBooks and Sort
def ConvertToJsonList(CopyOfLst, Newlst):
    for name, author, id in CopyOfLst:
        book = {"title": name, "author": author}
        Newlst.append(book)
    # Newlst.append(json.dumps([{"title": name, "author": author} for name, author, id in CopyOfLst]))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
