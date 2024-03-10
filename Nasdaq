
# Importing json and requests.
import json
import requests

# Asking the user for which company they want the data for.
CompanyName = input("Please enter the name of the company: ")
lc = CompanyName.lower()

# Putting a start and end date for the time range of data I want.
StartDate = input("Please enter the start date: ")
EndDate = input("Please enter the end date: ")

# Using the URL
url = f"https://data.nasdaq.com/api/v3/datasets/WIKI/{lc}.json?start_date={StartDate}&end_date={EndDate}&order=asc&column_index=4&collapse=quarterly&transformation=rdiff"

# Getting the desired data in json format
request = requests.get(url)
print('request: ', request.text)

# Converting the json data file so that python can parse it.
data = json.loads(request.text)

# Parsing the data to all the data I need
parsing = data["dataset"]["data"]

# Setting a counter in order to extract the specific pieces of data I need in the coming loop
z = 0

# Writing a loop to extract the data I need using 'z'.
for i in parsing:

    # Extracting the data, 'z' is the counter to extract the specific piece of data.
    parsing = data["dataset"]["data"][z]

    # READ WHAT THE '*' DOES.
    # Printing the closing price. (The star gets rid of the brackets surrounding the data)
    print('Closing price: ', *parsing)

    # Moving the counter to ensure that the next time I run the loop the next set of data is used.
    z = z + 1

# Essentially the same thing as the last line however the seperator is now separating the last 2 lines
print("Closing price: ", *parsing, sep="\n")
