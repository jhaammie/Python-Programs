import pandas as pd
from db import InsertData

df = pd.read_excel('C:\\Users\\jhaan\\Downloads\\2023gothenburg.xlsx')

lst = ['1)', '2)', '3)', '4)', '5)', '6)', '7)']

for i, row in df.iterrows():
    print(i, row)
    schoolname = row.get(0)
    utbildning = row.get(1)

    antagningspoang_prelim = row.get(2)
    if pd.isna(antagningspoang_prelim):
        antagningspoang_prelim = None
    elif antagningspoang_prelim in lst:
        antagningspoang_prelim = int(antagningspoang_prelim[0]) * -1

    medelvarde_prelim = row.get(3)
    if pd.isna(medelvarde_prelim):
        medelvarde_prelim = None
    elif medelvarde_prelim in lst:
        medelvarde_prelim = int(medelvarde_prelim[0]) * -1

    antagningspoang_slut = row.get(4)
    if pd.isna(antagningspoang_slut):
        antagningspoang_slut = None
    elif antagningspoang_slut in lst:
        antagningspoang_slut = int(antagningspoang_slut[0]) * -1

    medelvarde_slut = row.get(5)
    if pd.isna(medelvarde_slut):
        medelvarde_slut = None
    elif medelvarde_slut in lst:
        medelvarde_slut = int(medelvarde_slut[0]) * -1

    antagningspoang_reserv = row.get(6)
    if pd.isna(antagningspoang_reserv):
        antagningspoang_reserv = None
    elif antagningspoang_reserv in lst:
        antagningspoang_reserv = int(antagningspoang_reserv[0]) * -1

    medelvarde_reserv = row.get(7)
    if pd.isna(medelvarde_reserv):
        medelvarde_reserv = None
    elif medelvarde_reserv in lst:
        medelvarde_reserv = int(medelvarde_reserv[0]) * -1

    InsertData(schoolname, utbildning, antagningspoang_prelim, medelvarde_prelim, antagningspoang_slut, medelvarde_slut, antagningspoang_reserv, medelvarde_reserv)
