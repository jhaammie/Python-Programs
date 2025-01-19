# In this program the user will enter a number of his/her choice and the computer will tell the LCM of those numbers
# Giving i the value 1 so that the counting starts from 1
i=1
# Defining the variable "s" for adding with another variable
s=0
# Asking the user (in an integer) to enter the numbers of number they want to add
num= int(input("Please enter the number of numbers you want to add: "))
# Using the "While loop" saying while "i" (Since we defined it) is smaller than "num+1" (We had defined that too)
while i<(num+1):
# Defining the varible "a" asking the user the numbers they want to add
    a = int(input("Please enter the number "+str(i)+ ": "))
# Defining a variable "s" and in that variable we add the other variable "s" and the variable "a"
    s=s+a
# Keep adding 1
    i=i+1
# Telling the user that the added value of the user's entered numbers
print ("The value of added numbers is: "+ str(s))

