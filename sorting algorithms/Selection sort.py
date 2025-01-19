
num = [8, 9, 2, -8, 100, 0]

length = len(num)
for i in range(0, length):
    min = num[i]
    for j in range(i+1, length):
        current = num[j]

        if min > current:
            extra = num[j]
            num[j] = num[i]
            num[i] = extra
            min = current
print(num)
