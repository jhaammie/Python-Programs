
p=input("Please enter a word that you are wondering is a palindrome or not: ")
l = len(p)
for a in range(l):
    if p[0]==p[-1]:
       print(p+" is a palindrome ")
       print(p+" is not a palindrome ")
