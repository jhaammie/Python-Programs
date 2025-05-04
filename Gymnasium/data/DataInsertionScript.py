import pandas as pd
import psycopg2
import re
import os
from glob import glob
from dotenv import load_dotenv

load_dotenv()


def insert_data_from_excel():
    # --- CONFIGURE THESE ---
    DB_CONFIG = {
        "dbname":os.getenv("DB_NAME"),
        "user":os.getenv("DB_USER"),
        "password":os.getenv("DB_PASSWORD"),
        "host":os.getenv("DB_HOST"),
        "port":os.getenv("DB_PORT")
    }

    FOLDER_PATH = os.getcwd()  # Path where your Excel files are stored
    if os.path.normpath('gymnasium/data') not in os.path.normpath(FOLDER_PATH).lower():
        FOLDER_PATH = os.path.join(FOLDER_PATH, 'Gymnasium', 'data')
    if os.path.normpath('data') not in os.path.normpath(FOLDER_PATH).lower():
        FOLDER_PATH = os.path.join(FOLDER_PATH, 'data')

    # --- Define expected columns and possible alternatives ---
    COLUMN_MAPPING = {
        'kommun': ['Kommun', 'kommun'],
        'skola': ['Skola', 'skola', 'Gymnasium'],
        'studievägskod': ['Studievägskod', 'studievägskod', 'StudieVagKod'],
        'studieväg': ['Studieväg', 'Studievag'],
        'antagningsgräns': ['Antagningsgräns', 'Antagningsgrans', 'antagningsgräns'],
        'organistionsform': ['Organistionsform', 'organistionsform', 'Organistionsform'],
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
        insert into public.gymnasium (
            "år", "är_preliminär", kommun, skola, organistionsform,
            "studievägskod", "studieväg", "antagningsgräns", median,
            antal_platser, antagna, reserver, lediga_platser
        ) values (
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
                    continue
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
        år = int(year_match.group(1)) if year_match else 1900
        är_preliminär = True if 'prelim' in filename.lower() else False
        
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
                # --- Convert 'P' to -1 for specific columns ---
                if data['antagningsgräns'] == 'P':
                    data['antagningsgräns'] = -1
                if data['median'] == 'P':
                    data['median'] = -1
                if data['antal_platser'] == 'P':
                    data['antal_platser'] = -1
                if data['antagna'] == 'P':
                    data['antagna'] = -1
                if data['reserver'] == 'P':
                    data['reserver'] = -1
                if data['lediga_platser'] == 'P':
                    data['lediga_platser'] = -1
                cur.execute(insert_query, data)
            except psycopg2.Error as e:
                print(f"❌ Error inserting data from file '{file_path}': {data}, Error: {e}")
                break

    # --- Commit and close ---
    conn.commit()
    cur.close()
    conn.close()

    print("✅ All files processed and data inserted successfully!")

insert_data_from_excel()