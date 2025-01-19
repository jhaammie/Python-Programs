


num = int(input("enter number of stars: "))

for row in range(0, num, 2):
    for i in range(row):
        print(" ", end="")
    for column in range(row, num):
        print('*', end="")
    print("")

"""
* * * * * * *
  * * * * *
    * * *
      *
"""
"""
num = int(input("enter number of stars: "))

for row in range(0, num, 2):

    for column in range(row, num):
        print('*', end=" ")
    print("")
"""
"""
num = int(input("enter number of rows: "))

for row in range(0, num):

    for column in range(0, row+1):
        print('*', end="")
    print("")
"""