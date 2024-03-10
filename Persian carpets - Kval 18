
# Writing a program based off of a question

"""

During the IOI in Tehran last summer, an increased demand was noticed for Persian carpets,
especially those whose pattern consists of a check pattern with L × B squares
A rug's price is usually determined by the number of squares, so a typical customer wants a rug included
at least M squares and at most N squares. If there are several possible mats, the customer wants one
as square a mat as possible, i.e. it wants |L − B| is as small as possible.
Write a program that reads in the numbers M and N and prints the best choice of B and L

"""

import math


def ValOfbl(m):
    a = int(math.sqrt(m))
    for i in range(a, 0, -1):
        if m % i == 0:
            return i, int(m / i)


# Get user input for minimum and maximum squares
m = int(input("Min: "))
n = int(input("Max: "))

# Initialize l and b before calculating difference
l = m
b = 1
smallest_difference = l-b  # Initialize with a large difference

# Find option with the smallest difference
for a in range(m, n + 1):
    b, l = ValOfbl(a)
    current_difference = abs(l - b)
    if current_difference < smallest_difference:
        smallest_difference = current_difference
        smallest_l = l
        smallest_b = b
    if smallest_difference == 0:
        smallest_l = l
        smallest_b = b
        break

# Print only the option with the smallest difference
print("Option for you:", smallest_b, "x", smallest_l)



