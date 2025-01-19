od=1
odd=1
while od>0:
    print("Please enter numbers you need to know are divisible by any other number you need. If you want to exit the program please enter a negetive number or 0 ")
    od = int(input("Please enter your first number: "))
    odd = int(input("Please enter your second number: "))
    while odd>0:
        if(od%odd)==0:
              print(str(od)+ " is divisible by " +str(odd))
        else:
              print(str(od)+ " is not divisible by " + str(odd))
print(" Alright, Goodbye!!!!!!!!!!!!!! ")