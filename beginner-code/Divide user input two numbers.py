print("Please enter numbers you need to know are divisible by any other number you need. If you want to exit the program please enter a negetive number or 0 ")
od=int(input("Please enter your first number: "))
odd=int(input("Please enter your second number: "))
while od>0:
    while odd>0:
         if(od%odd)==0:
              print(str(od)+ " is divisible by " +str(odd))
              break
         else:
              print(str(od)+ " is not divisible by " + str(odd))
              break
    if odd<1: break
    od = int(input("Please enter your first number: "))
    odd = int(input("Please enter your second number: "))
print(" Alright, Goodbye!!!!!!!!!!!!!! ")
