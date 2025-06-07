import pandas as pd
import psycopg2
import re
import os
from glob import glob
from dotenv import load_dotenv
from utility import slug

load_dotenv()


def create_raw_table(cur, year, is_preliminary):
    table_name = f"gymnasium_{'prelim' if is_preliminary else 'final'}_{year}_raw"
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS public.{table_name} (
            id SERIAL PRIMARY KEY,
            raw_data JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    cur.execute(create_table_query)
    return table_name

def insert_raw_data_from_excel():
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

    # --- Prepare INSERT statements ---
    raw_insert_query = """
        INSERT INTO public.{table_name} (raw_data)
        VALUES (%(raw_data)s)
    """

    processed_insert_query = """
        INSERT INTO public.gymnasium (
            "år", "är_preliminär", kommun, skola, skola_slug, organistionsform,
            "studievägskod", "studieväg", studieväg_slug, "antagningsgräns", median,
            antal_platser, antagna, reserver, lediga_platser
        ) VALUES (
            %(år)s, %(är_preliminär)s, %(kommun)s, %(skola)s, %(skola_slug)s, %(organistionsform)s,
            %(studievägskod)s, %(studieväg)s, %(studieväg_slug)s, %(antagningsgräns)s, %(median)s,
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
        
        # --- Create raw table for this year and type ---
        raw_table_name = create_raw_table(cur, år, är_preliminär)
        
        # --- Read Excel file ---
        df = pd.read_excel(file_path)
        
        # --- Store raw data ---
        raw_data = df.to_dict(orient='records')
        cur.execute(raw_insert_query.format(table_name=raw_table_name), {'raw_data': raw_data})
        
        # --- Standardize columns (strict checking) ---
        col_map = standardize_columns(df, file_path)
        
        # --- Insert processed data ---
        for _, row in df.iterrows():
            skola_value = row[col_map['skola']]
            studievag_value = row[col_map['studieväg']]
            
            data = {
                'år': år,
                'är_preliminär': är_preliminär,
                'kommun': row[col_map['kommun']],
                'skola': skola_value,
                'skola_slug': slug(skola_value),
                'organistionsform': row[col_map['organistionsform']] if 'organistionsform' in col_map else None,
                'studievägskod': row[col_map['studievägskod']],
                'studieväg': studievag_value,
                'studieväg_slug': slug(studievag_value),
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
                cur.execute(processed_insert_query, data)
            except psycopg2.Error as e:
                print(f"❌ Error inserting data from file '{file_path}': {data}, Error: {e}")
                break

    # --- Commit and close ---
    conn.commit()
    cur.close()
    conn.close()

    print("✅ All files processed and data inserted successfully!")

insert_raw_data_from_excel()