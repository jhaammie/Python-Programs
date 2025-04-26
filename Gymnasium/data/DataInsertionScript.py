import pandas as pd
import psycopg2
import re
import os
from glob import glob

# --- CONFIGURE THESE ---
DB_CONFIG = {
    "dbname":"gymnasium",
    "user":"postgres",
    "password":"password",
    "host":"localhost"
}

FOLDER_PATH = os.getcwd() + "/Gymnasium/data"  # Path where your Excel files are stored

# --- Define expected columns and possible alternatives ---
COLUMN_MAPPING = {
    'kommun': ['Kommun', 'kommun'],
    'skola': ['Skola', 'skola', 'Gymnasium'],
    'studievägskod': ['Studievägskod', 'studievägskod', 'StudieVagKod'],
    'studieväg': ['Studieväg', 'Studievag'],
    'antagningsgräns': ['Antagningsgräns', 'Antagningsgrans', 'antagningsgräns'],
    'median': ['Median', 'medianvärde', 'Medianvärde', 'median'],
    'antal_platser': ['AntalPlatser', 'Antal platser', 'Platser', 'antal platser', 'antal_platser'],
    'antagna': ['Antagna', 'Antagna elever', 'antagna', 'AntalAntagna'],
    'reserver': ['Reserver', 'reserver', 'Reserv', 'AntalReserver'],
    'lediga_platser': ['Lediga platser', 'Lediga', 'lediga platser', 'lediga_platser', 'AntalLedigaPlatser'],
}

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

# --- Helper function to standardize column names ---
def standardize_columns(df, file_path):
    col_map = {}
    for target_col, possible_names in COLUMN_MAPPING.items():
        for name in possible_names:
            if name in df.columns:
                col_map[target_col] = name
                break
        else:
            if target_col == 'organistionsform':
                col_map[target_col] = 'organistionsform'
            else:
                raise ValueError(f"❌ Error in file '{file_path}': Missing required column for '{target_col}'.")
    return col_map

# --- Process all Excel files ---
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
    
    # --- Standardize columns (strict checking) ---
    col_map = standardize_columns(df, file_path)
    
    # --- Insert each row ---
    for _, row in df.iterrows():
        data = {
            'år': år,
            'är_preliminär': är_preliminär,
            'kommun': row[col_map['kommun']],
            'skola': row[col_map['skola']],
            'organistionsform': row[col_map['organistionsform']] if 'organistionsform' in col_map else None,
            'studievägskod': row[col_map['studievägskod']],
            'studieväg': row[col_map['studieväg']],
            'antagningsgräns': row[col_map['antagningsgräns']],
            'median': row[col_map['median']],
            'antal_platser': row[col_map['antal_platser']],
            'antagna': row[col_map['antagna']],
            'reserver': row[col_map['reserver']],
            'lediga_platser': row[col_map['lediga_platser']],
        }
        try:
            if data['antal_platser'] == 'P':
                print(f"⚠️ Skipping row with P in 'antal_platser' in file '{file_path}'")
                continue
            cur.execute(insert_query, data)
        except psycopg2.Error as e:
            print(f"❌ Error inserting data from file '{file_path}': {row}")
            continue

# --- Commit and close ---
conn.commit()
cur.close()
conn.close()

print("✅ All files processed and data inserted successfully!")
