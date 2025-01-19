

"""# 21 Hourglass Pattern

num = int(input("enter number of stars: "))

for row in range(0, num-1):
    for space in range(0, row):
        print(end="  ")
    for j in range(0, ((num-row)*2)-1):
        print("* ", end="")

    print("")


for i in range(1, num + 1):  #1
    for space in range(1, (num - i) + 1): # 1, (5-1) + 1
        print(end="  ")

    for j in range(0, ((i*2) - 1)):
        print("* ", end="")

    print()
"""

rows = int(input("Enter number of rows: "))

for i in range(1, rows + 1):
    for space in range(1, (rows - i) + 1):
        print(end=" ")

    for j in range(0, i):
        if i == rows or j == 0 or j == (i-1):
            print("*", end=" ")
        else:
            print(" ", end=" ")


# j 0 3 4 i 5 1 2
    print()

"""# 16 Hollow square (rectangle) pattern
num = int(input("enter number of rows and columns: "))  #5
for i in range(num):
    for j in range(num):
        # print("i: ", i, "j: ", j, end="  ")
        if i == 0 or i == num - 1 or j == 0 or j == num - 1:
            print("*", end=" ")
        else:
            print(" ", end=" ")
    print()
"""
"""# 18b reverse floyds triangle
num = int(input("enter number of rows: "))
i = int(0.5 * num * (num + 1))
for row in range(0, num):
    for column in range(0, row+1):
        print(f"{i:>5}", end=" ")
        i = i - 1
    print("")"""

"""# 18 Floyd's Triangle
i = 1
num = int(input("enter number of rows: "))
for row in range(0, num):
    for column in range(0, row+1):
        print(i, end=" ")
        i = i + 1
    print("")"""

"""#17 Number pyramid program
rows = int(input("Enter number of rows: "))

for i in range(1, rows + 1):
    for space in range(1, (rows - i) + 1):
        print(end=" ")

    for j in range(0, i):
        print(i, end=" ")

    print()"""

# 16 Hollow Square Pattern
"""
*****
*   *
*   *
*   *
*****

"""
"""width = int(input("Please enter a number: "))
length = width*2

for i in range(length):
    #print("*", end="")
    for a in range(width):
        print("*", end="\n")
"""

"""# 15 diamond

num = int(input("enter number of stars: "))

for i in range(1, num + 1):  #1
    for space in range(1, (num - i) + 1): # 1, (5-1) + 1
        print(end="  ")

    for j in range(0, ((i*2) - 1)):
        print("* ", end="")

    print()

for row in range(1, num):
    for space in range(0, row):
        print(end="  ")
    for j in range(0, ((num-row)*2)-1):
        print("* ", end="")

    print("")"""

"""
# 14 pyramid

    *
   ***
  *****
 *******
*********
"""
"""rows = int(input("Enter number of rows: ")) #5

for i in range(1, rows + 1):  #1
    for space in range(1, (rows - i) + 1): # 1, (5-1) + 1
        print(end="  ")

    for j in range(0, ((i*2) - 1)):
        print("* ", end="")

    print()"""

"""
# 13 inverted triangle

num = int(input("enter number of stars: "))

for row in range(0, num):

    for column in range(row, num):
        print('*', end="")
    print("")
"""
"""
# 12 right angle triangle
num = int(input("enter number of rows: "))

for row in range(0, num):

    for column in range(0, row+1):
        print('*', end="")
    print("")
"""
"""# 11 FizzBuzz
n = 50
for i in range(1, 51):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz", end=", ")
    elif i % 5 == 0:
        if i == 50:
            print("Buzz.")
        else:
            print("Buzz", end=", ")
    elif i % 3 == 0:
        print("Fizz", end=", ")
    else:
        print(i, end=", ")"""

"""# 9 Word Frequency Counter
sentence = "this is a test this is only a test, lala alice is dead in wonderland"
words = sentence.split()
dict = {}
for i in range(len(words)):
    if words[i] in dict:
        x = dict.get(words[i])
        dict[words[i]] = x+1
    else:
        dict[words[i]] = 1
    print("dict:", dict, "words[i]:", words[i], "i:", i)
print(dict)
"""

"""#6 Find Prime Numbers in a Range

for i in range(1, 51):
    if i%2 == 0:
        pass
    else:
        print(i)"""
"""
#5 Print number of vowels in given string
text = "hello world"
vowels = []
length = len(text)
for i in range(0, length):
    current = text[i]
    if current == 'a':
        vowels.append(current)
    elif current == 'e':
        vowels.append(current)
    elif current == 'i':
        vowels.append(current)
    elif current == 'o':
        vowels.append(current)
    elif current == 'u':
        vowels.append(current)
    else:
        pass
print(len(vowels))
"""
"""
#4 Print multiplication table
n = int(input("Please enter a number: "))
for i in range(1, 11):
    print(n, "times", i, "=", i*n)
"""
"""
#3 Find the Largest Number
numbers = [45, 67, 34, 89, 12, 78, 100]
max = numbers[0]
for i in range(len(numbers)):
    if max < numbers[i]:
        max = numbers[i]
    else:
        pass
print(max)
"""
"""
#2 Factorial calculation
n = 5
product = 1
for i in range(1, n+1):
    product = product * i
print(product)


#1 Sum of list of elements
numbers = [1, 2, 3, 4, 5]
sum = 0
for i in range(len(numbers)):
    sum = sum+numbers[i]

print(sum)
"""
