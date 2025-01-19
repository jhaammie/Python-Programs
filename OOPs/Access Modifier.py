
# Access Modifiers

"""

A class in python has 3 types of access modifiers:
        Public Access Modifier
        Private Access Modifier
        Protected Access Modifier

The super() function is used to access methods and properties of a
parent class.

"""


class Book:

    def __init__(self, title):
        self.title = title
        self._text = ""

    # Read is public
    def read(self):
        if len(self._text) == 0:

            # Accessing __write in its own class
            self.__write("Hey there!")
        print(f"I am reading the book: {self.title}")

    # __write is private
    def __write(self, text):
        # _text is protected

        # Accessing the protected variable inside the class
        self._text = text
        print(f"I am writing in the book: {self.title} = {self._text}")


class TextBook(Book):
    def __init__(self, title):
        super().__init__(title)

    def PrintText(self):

        # Accessing protected variable in child class
        print(self._text)


# Public
biologyTextBook = TextBook("biology 101")
biologyTextBook.read()
biologyTextBook.read()

# Protected
# Giving warning but letting it go anyway
print(biologyTextBook._text)

# Public function of child class that uses protected variable of parent
biologyTextBook.PrintText()

# Private: will throw error
biologyTextBook.__write("can i write?")
