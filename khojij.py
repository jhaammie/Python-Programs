
"""

Given two strings s and t, return true if s is a subsequence of t, or false otherwise.

A subsequence of a string is a new string that is formed from the original string by deleting some (can be none) of the characters without disturbing the relative positions of the remaining characters. (i.e., "ace" is a subsequence of "abcde" while "aec" is not).



Example 1:

Input: s = "abc", t = "ahbgdc"
Output: true
Example 2:

Input: s = "axc", t = "ahbgdc"
Output: false


Constraints:

0 <= s.length <= 100
0 <= t.length <= 104
s and t consist only of lowercase English letters.

"""
from numpy.ma.core import append

"""
s = 'abc'
t = 'ahbgdc'
CurrentIndex = 0
count = 0
for i in s:
    for x in range(CurrentIndex, len(t)):
        CurrentIndex += 1
        if i == t[x]:
            count += 1
            break

print(count==len(s))

"""

"""

Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:

Open brackets must be closed by the same type of brackets.
Open brackets must be closed in the correct order.
Every close bracket has a corresponding open bracket of the same type.
 

Example 1:

Input: s = "()"

Output: true

Example 2:

Input: s = "()[]{}"

Output: true

Example 3:

Input: s = "(]"

Output: false

Example 4:

Input: s = "([])"

Output: true

Example 5:

Input: s = "([)]"

Output: false

 

Constraints:

1 <= s.length <= 104
s consists of parentheses only '()[]{}'.


"""
"""def GetClosingBracket(a):
    if a == '(':
        return ')'
    elif a == '{':
        return '}'
    elif a == '[':
        return ']'

a = "([])"

# lifo...nisha calls it last in first out
# according to her whatever you put in the list last you remove it first
# also called stack again according to her
# to insert something in a stack, she performs a function called push
# to take the last inserted element out from the stack, she performs a function called pop
lst = []

for i in range(len(a)):
    if a[i] in ['(', '{', '[']:
        lst.append(a[i])
    else:
        x = GetClosingBracket(lst[-1])
        if a[i] == x:
            lst.pop()
        else:
            print("false")
            break
if len(lst) == 0:
    print("true")"""

"""
def moveZeros(nums):
    for i in range(len(nums)):
        if nums[i] == 0:
            nums.pop(i)
            nums.append(0)
    print(nums)

num = [0, 1, 2, 3, 0]
moveZeros(num)
"""
"""
def geteffectiveemail(a):
    l = a.split("@")
    localname = l[0]
    domainname = l[1]
    localname = localname.replace('.', '')
    localname = localname.split('+')[0]
    newemail = localname + '@' + domainname
    return newemail


lst =  ["a@leetcode.com","b@leetcode.com","c@leetcode.com"]
lstofemails = set()
for a in lst:
    newemail = geteffectiveemail(a)
    lstofemails.add(newemail)
print("lalal:", len(lstofemails))

"""


"""while i < length:
    if localname[i] == '.':
        localname = localname[:i] + localname[i + 1:]
        print(localname)
        length = length-1
    elif localname[i] == '+':
        localname = localname[:i]
        length = len(localname)
        print(localname)
    i = i + 1"""

"""

finalemail = ln + @ + dn
for every email in input list
write a function and call it 'geteffectiveemail'
i will get a list
i will convert list to set
output will be number of unique emails

= ["test.email+alex@leetcode.com","test.e.mail+bob.cathy@leetcode.com","testemail+david@lee.tcode.com"]
"""