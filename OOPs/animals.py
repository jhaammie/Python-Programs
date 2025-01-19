"""
# Defining new class 'Animal'
class Animal:

    def __init__(self, name, NumberOfLegs, food):
        self.name = name
        self.NumberOfLegs = NumberOfLegs
        self.food = food

    def move(self):
        print(f'{self.name} can run')

    def eats(self):
        print(f'{self.name} eats {self.food}')


dog = Animal('dog', 4, 'dog food')
dog.move()
dog.eats()

cat = Animal('cat', 4, 'cat food')
cat.eats()

duck = Animal('Donald Duck', 2, 'bread crumbs')
duck.move()

"""

class Flowers:
    def __init__(self, ColourOfPetals, environment, name):
        self.name = name
        self.ColourOfPetals = ColourOfPetals
        self.environment = environment

    def CanPerformPhotosynthesis(self):
        lower = self.ColourOfPetals.lower()
        if lower == 'green':
            print(f"Yes, {self.name} can perform photosynthesis")
        else:
            print(f"No, {self.name} can't perform photosynthesis")

    def eat(self):
        print(f"{self.name} consumes nutrients from the soil and water")

    def grow(self):
        print(f"{self.name} grows in {self.environment}")

    def __str__(self):
        return f"{self.name}({self.ColourOfPetals})"


daisy = Flowers('White', 'Gardens', 'daisy')
RedRose = Flowers('Red', 'Rosebushes', 'Red roses')
GreenRose = Flowers('Green', 'Rosebushes', 'Green roses')
daisy.grow()
RedRose.CanPerformPhotosynthesis()
GreenRose.CanPerformPhotosynthesis()

print(RedRose)
