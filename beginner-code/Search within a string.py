# Write a program to ask user to input a paragraph. Then ask user to input the search word. Then search within the paragraph and find out how many times the search word has come

# Making up a variable called s and giving it the value 0
s=0
# Making a variable p and asking the user to input a random paragraph or sentence
p=input("Please enter a paragrapaph or a sentance: ")
# Now making another variable called sw and here I have asked the user to enter any word from the paragraph or sentence and the computer will searcch for that word from alphabet 0 to alphabet -1 and tell what it found
sw= input("Please enter a word from the paragraph you have entered to see how many times you have written that word: ")
# Making a variable sw1 and saying that "In this sentence the word is first found with a space on both sides on number "on number whatever the user has input, and lastly count so that the computer counts when or on what number it came
sw1=" "+sw+" "
print(" In this sentence the word " + str(sw) + " is first found with a space on both sides on number "+str(p.find(sw1)))
s=p.count(sw1)+s
# Making a variable sw2 and saying that "In this sentence the word is first found with a space on one side on number "on number whatever the user has input, and lastly count so that the computer counts when or on what number it came
sw2=sw+" "
print(" In this sentence the word " + str(sw) + " is first found with a space on one side on number " + str(p.find(sw2)))
s=p.count(sw2)+s
# Making a variable sw3 and saying that "In this sentence the word is first found with a full stop on number "on number whatever the user has input, and lastly count so that the computer counts when or on what number it came
sw3=sw+"."
print("In this sentence the word "+str(sw)+" is first found with a full stop on number  " + str(p.find(sw3)))
s=p.count(sw3)+s
# Making a variable sw4 and saying that "In this sentence the word is first found with a comma on number "on number whatever the user has input, and lastly count so that the computer counts when or on what number it came
sw4=sw+","
print("In this sentence the word "+str(sw)+" is first found with a comma on number "+str(p.find(sw4)))
s=p.count(sw4)+s
# Making a variable sw5 and saying that "In this sentence the word is first found with a semi colon on number "on number whatever the user has input, and lastly count so that the computer counts when or on what number it came
sw5=sw+";"
print("In this sentence the word "+str(sw)+" is first found with a semi colon on number  "+str(p.find(sw5)))
s=p.count(sw5)+s
# Making a variable sw6 and saying that "In this sentence the word is first found with a colon on number "on number whatever the user has input, and lastly count so that the computer counts when or on what number it came
sw6=sw+":"
print("In this sentence the word "+str(sw)+" is first found with a colon on number "+str(p.find(sw6)))
s=p.count(sw6)+s
# Making a variable sw7 and saying that "In this sentence the word is first found with a question mark on number "on number whatever the user has input, and lastly count so that the computer counts when or on what number it came
sw7=sw+"?"
print("In this sentence the word "+str(sw)+" is first found with a question mark on number "+str(p.find(sw7)))
s=p.count(sw7)+s
# Making a variable sw8 and saying that "In this sentence the word is first found with a explanation mark on number "on number whatever the user has input, and lastly count so that the computer counts when or on what number it came
sw8=sw+"!"
print("In this sentence the word "+str(sw)+" is first found with a explanation mark on number "+str(p.find(sw8)))
s=p.count(sw8)+s
# 2-Now if that variable does exist how many times does it exist or how many times does it come? So you use the function count again with the variables 'p'and'sw'
