# In this program the user will input a number, sentence, or word and print whatever they wrote the other way around
# First we define a variable called empty_string so that we put the alphabets in a word format
empty_string=""
# Giving i a value because -1 will print the last alphabet in first place
i=-1
# Defining a variable called integers so that the computer gives instructions to the user on what to do
integers = input("Please enter a number, sentence, or a word: ")
# Below I am defining a variable called l and measuring the length of the number or word the user has input to reverse it
l=len(integers)
# Using the for loop to reverse
for v in range(l):
# You can add strings so we added the strings together
   empty_string = empty_string+integers[i]
# To reverse-1 will print the last alphabet first which is what we want so instead of doing i=i+1 we are doing i=i-1
   i=i-1
# Now so that it puts the reversed numbers in a word format you print empty_string
print (empty_string)
