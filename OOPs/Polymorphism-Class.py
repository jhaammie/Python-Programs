
# Class Polymorphism

"""

Polymorphism (in OOPs) is concept that refers to the ability of a variable, function or object to take on multiple forms
Examples:
    Print()
    Type()

Creating subclasses within the main class and create instances/objects of them

Polymorphism is often used in Class methods,
where there are multiple classes with the same method name.

"""


# Creating new class called 'Shape'
class Shape:

    def area(self):
        print(self.area())

    def PrintArea(self):
        print(f"Area of {self.name} is {self.area()}")

    def __init__(self, name):
        self.name = name


# Making a subclass of shape called rectangle
class Rectangle(Shape):
    def __init__(self, length, width, name):
        super().__init__(name)
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width


# Making a subclass of shape called circle
class Circle(Shape):
    def __init__(self, radius, name):
        super().__init__(name)
        self.radius = radius

    def area(self):
        return self.radius * self.radius * 22 / 7


# Making a subclass of shape called triangle
class Triangle(Shape):
    def __init__(self, height, base, name):
        super().__init__(name)
        self.height = height
        self.base = base

    def area(self):
        return self.base * self.height / 2


# Creating objects of all the shapes
circle = Circle(9, 'circle')
rectangle = Rectangle(5, 9, 'rectangle')
triangle = Triangle(2, 8, 'triangle')

triangle.area()
rectangle.area()
circle.area()

# Printing the area
circle.PrintArea()
triangle.PrintArea()
rectangle.PrintArea()
