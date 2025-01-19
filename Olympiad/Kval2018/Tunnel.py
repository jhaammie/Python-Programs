
# Writing a program based off of a question

"""

Context:

On the subway trains, there are seat groups with four seats each. Now a number of groups of
people come and want to sit down. Each group of people has size 1, 2, 3 or 4. Ideally, all the people in a
group would like to sit in the same four-seater group, thus not having to share. What is the minimum
four-seater groups are required for this to be possible?

"""

# Taking the user inputs
a1 = int(input("Please enter the number of single people: "))
a2 = int(input("Please enter the number of groups with 2 people: "))
a3 = int(input("Please enter the number of groups with 3 people: "))
a4 = int(input("Please enter the number of groups with 4 people: "))

# Starting with a4
# Because there are 4 people in each group and 4 seats in each set of seats it's the same number
print("The total number of four-seater groups needed for", a4, "number of 4 people groups is", a4)

# Continuing with a3
# Because there are 3 people in each group and 4 seats in each set of seats it's the same except for one extra seat left in each group
print("The total number of four-seater groups needed for", a3, "number of 3 people groups is", a3)
print("The remaining number of individual seats for each group is the same number of the groups of people ", a3)

# Continuing with a2
# If a2 is even
if a2 % 2 == 0:
    # Defining variables called Total Blocks and Empty seats
    TotalBlocks = a4 + a3 + a2/2
    EmptySeats = a3

    # if the value of a1 is smaller than the total number of empty seats then there will be no added blocks
    if a1 == range(0, EmptySeats):
        AddedBlocks = 0
    # If not
    else:

        # Defining the number of unseated people
        UnseatedPeople = a1 - EmptySeats

        # If the mod of unseated people and 4 is 0
        if UnseatedPeople % 4 == 0:

            # The total blocks occupied
            TotalBlocks = TotalBlocks + UnseatedPeople/4

        # If it's not
        else:

            # Defining 'x'
            x = UnseatedPeople//4 + 1

            # Total number of blocks
            TotalBlocks = TotalBlocks + x

# If the value of a2 is odd
else:

    # Total number of blocks till now
    TotalBlocks = a4 + a3 + a2//2 + 1

    # Empty seats till now
    EmptySeats = a3 + 2

    # If the value of a1 is smaller than the total number of empty seats
    if a1 == range(0, EmptySeats):

        # No extra blocks needed
        AddedBlocks = 0

    # If it's not
    else:

        # Total unseated people
        UnseatedPeople = a1 - EmptySeats

        # If the mod of unseated people and 4 is 0
        if UnseatedPeople % 4 == 0:

            # Total blocks
            TotalBlocks = TotalBlocks + UnseatedPeople/4

        # If mod is not 0
        else:

            # Defining 'x'
            x = UnseatedPeople // 4 + 1

            # Total Blocks
            TotalBlocks = TotalBlocks + x

# printing the result
print("Total blocks occupied by everyone: ", TotalBlocks)
