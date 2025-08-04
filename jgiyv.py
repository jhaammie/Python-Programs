"""
for i in range(1, 5):
    for a in range(1, i+1):
        print(a, end=" ")
    print()

"""

"""for i in range(1, 5):
    print()
    for a in range(5, i, -1):
        print("*", end="")
    print()"""


"""lst = []
num = int(input("Number:"))
lst.append(num)
while len(lst) < 10:
    num = int(input("Number:"))
    lst.append(num)
for i in range(0, len(lst)):
    a = sum(lst) / len(lst)

print(a)"""

def prema(num):
    num = abs(num)
    num = int(num)
    primefinder = 1
    for i in range(2, num):
        if num % i == 0:
            primefinder = 0
    if primefinder == 0:
        pass
    else:
        print(num, "is a prime")
    primefinder = 1
    return primefinder


num1 = int(input("Number 1: "))
num2 = int(input("Number 2: "))
for i in range(num1, num2+1):
    prema(i)










"""def prema(num):
    num = abs(num)
    num = int(num)
    primefinder = 1
    for i in range(2, num):
        if num % i == 0:
            print(num % i)
            primefinder = 0
        break
    if primefinder == 0:
        print(num, "is not a prime number")
    else:
        print(num, "is a prime")
    primefinder = 1
    return primefinder

prema(9)

"""
"""
num1 = int(input("Number 1: "))
num2 = int(input("Number 2: "))
for i in range(num1, num2+1):
    prema(i)
"""
