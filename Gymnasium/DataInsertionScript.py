import pandas as pd
import psycopg2
import re
import os
from glob import glob

#PAPA CONFIGURED THIS HA HA
DB_CONFIG = {
    'dbname':"gymnasium",
    'user':"postgres",
    'password':"password",
    'host':"localhost",
    'port': 5432,
}

FOLDER_PATH = '.'  # Path where your Excel files are stored

# --- Connect to PostgreSQL ---
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

# --- Prepare INSERT statement ---
insert_query = """
    INSERT INTO public.gymnasium (
        "år", "är_preliminär", kommun, skola, organistionsform,
        "studievägskod", "studieväg", "antagningsgräns", median,
        antal_platser, antagna, reserver, lediga_platser
    ) VALUES (
        %(år)s, %(är_preliminär)s, %(kommun)s, %(skola)s, %(organistionsform)s,
        %(studievägskod)s, %(studieväg)s, %(antagningsgräns)s, %(median)s,
        %(antal_platser)s, %(antagna)s, %(reserver)s, %(lediga_platser)s
    )
"""

# --- Process all Excel files in the folder ---
excel_files = glob(os.path.join(FOLDER_PATH, '*.xlsx'))

for file_path in excel_files:
    print(f"Processing file: {file_path}")

    # --- Extract year and preliminary status from filename ---
    filename = os.path.basename(file_path)
    year_match = re.search(r'(\d{4})', filename)
    år = int(year_match.group(1)) if year_match else None
    är_preliminär = 'preliminär' in filename.lower()

    # --- Read Excel file ---
    df = pd.read_excel(file_path)

    # --- Insert each row ---
    for _, row in df.iterrows():
        data = {
            'år': år,
            'är_preliminär': är_preliminär,
            'kommun': row['Kommun'],
            'skola': row['Skola'],
            'organistionsform': row['Organistionsform'],
            'studievägskod': row['StudieVagKod'],
            'studieväg': row['Studievag'],
            'antagningsgräns': row['Antagningsgrans'],
            'median': row['Median'],
            'antal_platser': row['AntalPlatser'],
            'antagna': row['AntalAntagna'],
            'reserver': row['AntalReserver'],
            'lediga_platser': row['AntalLedigaPlatser'],
        }
        cur.execute(insert_query, data)

# --- Commit and close ---
conn.commit()
cur.close()
conn.close()

print("All files processed and data inserted successfully!")