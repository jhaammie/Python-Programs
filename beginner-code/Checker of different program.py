

import random
#def game
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
p1=input("Please enter your name (player 1): ")
p2=input("Please enter your name (player 2): ")
print ("Hello "+p1+ " you will start first")
print("Hi "+p2+" you will play next")
qp=input("If you want to play then type in 'p' and if you want to quit then type in 'q': ")
if qp == 'p' or qp == 'P':
    print(" ")
    chance=0
    totalp1=0
    totalp2=0
    playeridentifier=0
    while chance<10:
        playeridentifier=playeridentifier+1
        if ((playeridentifier%2)==0):
                print(color.RED+"We will play for " + p2)
                dice1=random.randrange(1, 7, 1)
                dice2=random.randrange(1, 7, 1)
                print ("The number you  got with Dice1 is "+ str(dice1)+ " and the number you got with dice2 is " + str (dice2))
                ds=dice1+dice2
                if (ds%2)==0:
                     totalp2 = totalp2 + 10
                     print("Cool so now your points have increased by 10")
                     print("Now your total is " + str(totalp2))
                else:
                     totalp2 = totalp2 - 5
                     print("Oh no! Better luck next time, you lost 5 points now your number of points is decreased by 5 ")
                     print("Now your total is " + str(totalp2))
                chance = chance + 1
                input("Press enter for next roll"+color.END)
                print(" ")
        else:
                 print(color.CYAN+"We will play for " + p1)
                 dice1 = random.randrange(1, 7, 1)
                 dice2 = random.randrange(1, 7, 1)
                 print("The number you  got with Dice1 is " + str(dice1) + " and the number you got with dice2 is " + str(dice2))
                 ds = dice1 + dice2
                 if (ds % 2) == 0:
                    totalp1 = totalp1 + 10
                    print("Cool so now your points have increased by 10")
                    print("Now your total is " + str(totalp1))
                 else:
                    totalp1 = totalp1 - 5
                    print("Oh no! Better luck next time, you lost 5 points now your number of points is decreased by 5 ")
                    print("Now your total is " + str(totalp1))
                 chance = chance + 1
                 input("Press enter for next roll"+color.END)
        print(" ")
    if totalp1>totalp2:
        print(color.BLUE+color.BOLD + "Congratulations " + p1)
    elif totalp2>totalp1:
        print(color.BLUE+color.BOLD +"Congratulations " + p2)
    else:
        print(color.BLUE+color.BOLD +"Oh seems like there is tie, Congrats both of you!!! ")
elif qp == 'q' or qp == 'Q':
    print("Ok, you decided to leave,Goodbye!! ")
else:
    print(" You are entering garbage, Dumbo!!!!!!!!!!")
    quit()

