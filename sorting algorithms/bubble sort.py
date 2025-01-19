
# Bubble sort

"""

How Bubble Sort works
Example on wikipedia
Program

"""

# List of numbers
num = [8, 9, 2, -8, 100, 0]

for a in range(0, len(num)):
    for i in range(0, len(num)-a-1):
        print(num[i], num[i + 1])
        if num[i] > num[i+1]:
            extra = num[i]
            num[i] = num[i+1]
            num[i+1] = extra

print(num)






















"""            num[i] = num[i+1] + num[i]
            num[i+1] = num[i] - num[i+1]
            num[i] = num[i] - num[i+1]"""