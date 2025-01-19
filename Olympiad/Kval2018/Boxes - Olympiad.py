
# Olympiad

"""

You've just helped a friend move, but unfortunately you're stuck at the wrong end
of a narrow corridor full of moving boxes. The corridor consists of N stacks of
moving boxes, where stack number i contains ai boxes. All boxes are the same size.
The only way to get out is to walk on top of the bars from bar 1 to bar N.
If you are on a bar, you can go to a nearby bar, but only if it is not higher than
the one you are standing on. If the stack you are standing on is at least
two boxes higher than a neighboring stack, you can also push down the topmost box
from the stack you are standing on to the neighboring stack.
This can be repeated any number of times. You are currently on stack 1.
Unfortunately, it may be impossible for you to get to stack N.
But luckily, you can add any number of extra boxes to stack 1 before you start walking.
Write a program that calculates how many extra cartons you need to
 add in order to get to stack N. The program must read in the number of stacks N,
 and then the height ai of each stack.
 The program should print the minimum number of extra cartons that need to be added.

"""

stacks = int(input("Stacks: "))
s = []

for a in range(stacks):
    num = int(input(f"Number of boxes in stack {a+1}: "))
    s.append(num)
SumOfExtraBoxes = 0
NewValue = 0
for i in range(len(s)-1, 0, -1):

    if s[i] > s[i-1]:
        s[i - 1] = NewValue
        SumOfExtraBoxes = SumOfExtraBoxes + s[i]-(s[i-1])
        NewValue = (s[i-1]) + SumOfExtraBoxes
    else:
        NewValue = s[i-1]
        MaxBoxes = (s[i-1] - s[i]) // 2

        if MaxBoxes >= SumOfExtraBoxes:
            SumOfExtraBoxes = 0
        else:
            SumOfExtraBoxes = SumOfExtraBoxes - MaxBoxes
    print(SumOfExtraBoxes)
