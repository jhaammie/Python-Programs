
# File type conversion
# Deleting user decided columns

"""

We need to download a csv file, convert it into an excel file and save it into a Google sheets
Before we convert it however, the user gets a choice to delete specific columns from the 
dataframe, and then we make the final version of our excel sheet.

"""

# Importing what modules I need
from pathlib import Path  # Provides functions and operations that help you with handling
# and manipulating paths. Also ensures that all file paths work
# the same way no matter the operating system
import pandas as pd  # Pandas assists with data manipulation and data structure


# CONVERTING FROM CSV TO XLSX FILE

# Creating a path to my file
PathToCsvFile = Path.home() / 'Downloads' / 'MyFile.csv'

# The with statements helps with exception handling, cleaner alternative to try-except-finally
with open(PathToCsvFile) as TheData:

    # Reading the csv file using the pandas read csv function
    data = pd.read_csv(TheData)

    # Creating a DataFrame containing given data
    # If not entered the 'index' and 'column' are 'None' by default
    df = pd.DataFrame(data)

    df.to_excel('MyFileOriginal.xlsx', sheet_name='sheet 1')

    # TRUNCATING THE DATA

    """
    
    Creating a while loop so that the user can delete as many of the columns as they like
    by entering the names and once they're done it will create a final file with all of
    those columns gone from the dataframe I've been removing the data from.
    
    """

    # Asking the user if they want to delete any columns or not.
    WantToDelete = input("Please enter 'yes' or 'no', would you like to delete a column? ")

    # If it's a 'yes' then so that the while loop can recognise it we're changing it to lower case
    lowercase = WantToDelete.lower()

    # If it's a 'yes' the while loop runs
    while lowercase == 'yes':

        # Asking the user which column they want to delete
        ColumnToDelete = input("Please enter which column you would like to delete: ")
        
        # Using the 'del' function to delete the column
        del df[ColumnToDelete]

        # Asking the user if they want to delete another column
        WantToDelete = input("Please enter 'yes' or 'no', would you like to delete a column? ")

        # Making it lowercase again for the next round
        lowercase = WantToDelete.lower()

    # If the user does not want to delete another column
    else:

        # Politely saying goodbye to the user
        print("Alright goodbye u piece of SHIT")

        # Creating an excel file plus sheet to save the new DataFrame into a spreadsheet
        df.to_excel('MyFileNew.xlsx', sheet_name='sheet 1')

        # Quiting the program
        quit()
