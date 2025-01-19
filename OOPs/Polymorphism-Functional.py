
# Functional Polymorphism

"""

Polymorphism (in OOPs) is concept that refers to the ability of a variable, function or object to take on multiple forms
Examples:
    Print()
    Type()

Functional polymorphism: Any function that accepts more than 1 kind of data type

"""


# Creating a class called Rectangle
class Rectangle:

    # Defining the 'init' function which will basically be run each time the class is initiated
    def __init__(self, length, width):

        # Defining the dimensions for the rectangle
        self.length = length
        self.width = width


# Creating a class called Circle
class Circle:

    def __init__(self, radius):
        self.radius = radius


# Creating a class called triangle
class Triangle:
    def __init__(self, height, base):
        self.height = height
        self.base = base


# Defining the function area, and giving it the parameter 'shape'
def area(shape):

    # Using the isinstance function to check if the requested shape is a circle
    if isinstance(shape, Circle):
        circle = shape
        print("Area of a circle: ", circle.radius * circle.radius * 22 / 7)

    # Using the isinstance function to check if the requested shape is a rectangle
    elif isinstance(shape, Rectangle):
        rectangle = shape
        print("Area of a rectangle: ", rectangle.length * rectangle.width)

    # Using the isinstance function to check if the requested shape is a triangle
    elif isinstance(shape, Triangle):
        triangle = shape
        print("Area of a triangle: ", triangle.base * triangle.height / 2)

    # If the shape is not a valid one (for this program)...
    else:
        print("I don't know this shape")


# Creating objects for each shape and putting in the arguments
circle = Circle(100)
rectangle = Rectangle(978, 11)
triangle = Triangle(98, 84)

# Calling the area function with all the data so the result will be printed
area(triangle)
area(circle)
area(rectangle)
