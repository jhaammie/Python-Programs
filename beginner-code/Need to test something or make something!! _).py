
# Here I am defining a variable called ""Odev" and since I want the user's number to be a integer I wrote "int". I am also telling the user that if thier needs are over they can put a negitive integer.
odev=int(input("Please enter the numbers you want to know if they are odd or even. You can enter 0 or any negative number to exit: "))
# Using the while loop and saying that while our variable (odev) is bigger than 0 then we put a colon
while odev>0:
# Now we are saying that "if odev and 2 have a remainder it is = 0"
   if(odev % 2)==0:
# Now we are printing "(First we are converting into a string) So we write str(odev)  + (In chords) 'is Even'"
      print(str(odev)+ " is Even")
# Saying "or else"
   else:
# Now we are printing "(First we are converting into a string) So we write str(odev)  + (In chords) 'is Odd'"
      print(str(odev) + " is Odd")
# Here I am defining a variable called ""Odev" and since I want the user's number to be a integer I wrote "int". I am also telling the user that if thier needs are over they can put a negitive integer.
# So we wrote that again so that...
   odev = int(input("Please enter the numbers you want to know if they are odd or even. You can enter 0 or any negative number to exit: "))
# ...It prints "You decided to leave. Bye Bye ;)" just as you see below!;)
print ("You decided to leave. Bye Bye ;)")
