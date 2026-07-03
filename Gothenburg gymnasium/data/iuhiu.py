import tabula
tables = tabula.read_pdf(
    "C:/Users/jhaan/Downloads/ygiygiygyi.pdf",
    pages=2,
    multiple_tables=True,
    force_subprocess=True,
    encoding='latin1',  # or 'ISO-8859-1'
)
table = tables[0]

"""print(table)
columns = list(table)
print("columns: ", columns)
for i in columns:
    print (table[i])
"""
for i, j in table.iterrows():

    for col in table.columns:
        print("hhhhhh")
        print(table.at[i, col])

# I have to pick every table, and in that table, for every row, get data for every column
# Print row no, column no and value,

# the type of table is data frame btw