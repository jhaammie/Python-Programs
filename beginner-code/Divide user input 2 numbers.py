# Giving the user a message
print("Please enter the number you want to know is divisible by any number you want. If you want to leave just enter 0 or any negetive number ")
# Now asking the user to input their first number and forcing them to use only numbers
od=int(input("Please enter your first number: "))
# Now asking the user to input their second number and forcing them to use only numbers
odd=int(input("Please enter your second number: "))
# Using while loop
while od > 0:
# Using while loop again for the variable odd
    while odd > 0:
    # Now using if loop for the remainder of od and odd numbers coming from the user
        if(od % odd)==0:
# Making the variable od and odd strings by using str and saying it is divisible by what ever number they want
            print(str(od)+ " is divisible by " + str(odd))
# We are now using the break statement so that if the numbers are divisible it wont go infinite and will stop after saying it once
            break
# Saying or else print...
        else:
# ...Making the variable od and odd strings by using str and saying it is not divisible by what ever number they want
            print(str(od)+ " is not divisible by " + str(odd))
# Using the break statment so that if the numbers are not divisible it wont go infinte  and will stop after saying it once
            break
# If whatever number goes in the variable odd is smaller than one;BREAK
    if odd<1: break
# Printing: Please enter the number you want to know is divisible by any number you want. If you want to leave just enter 0 or any negetive number
    print ("Please enter the number you want to know is divisible by any number you want. If you want to leave just enter 0 or any negetive number ")
# Now asking the user to input their first number and forcing them to use only numbers
    od=int(input("Please enter your first number: "))
    # Now asking the user to input their second number and forcing them to use only numbers
    odd=int(input("Please enter your second number: "))
# As soon as the user inputs a negetive number or 0 Alright, Goodbye!!!!!!!!!! Will get printed
print(" Alright, Goodbye!!!!!!!!!!!!!! ")
