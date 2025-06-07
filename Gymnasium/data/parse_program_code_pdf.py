import pdfplumber
import psycopg2
import os
from dotenv import load_dotenv
from psycopg2 import errors
from utility import slug

# Load environment variables
load_dotenv()

# === PDF parsing ===
pdf_path = os.getenv("PDF_PATH", "code_program_ver53.pdf")
programs = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                if row and len(row) >= 2:
                    name = row[0].strip()
                    code = row[1].strip()
                    program_slug = slug(name)
                    programs.append((code, name, program_slug))
                    
print("Parsed programs:", len(programs))

# === PostgreSQL insertion ===
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

cursor = conn.cursor()

# Create table if not exists
create_table_query = """
    CREATE TABLE IF NOT EXISTS study_programs (
        id SERIAL PRIMARY KEY,
        studievägskod TEXT UNIQUE NOT NULL,
        studieväg TEXT NOT NULL,
        studieväg_slug TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""

cursor.execute(create_table_query)
conn.commit()  # Ensure table creation is committed before further operations

# Truncate the table before inserting new data
cursor.execute("TRUNCATE TABLE study_programs RESTART IDENTITY")
cursor.execute("ALTER SEQUENCE study_programs_id_seq RESTART WITH 10000")

insert_query = """
    INSERT INTO study_programs (studievägskod, studieväg, studieväg_slug)
    VALUES (%s, %s, %s)
"""

try:
    for i, program in enumerate(programs):
        # Skip empty program codes
        if not program[0]:
            print(f"⚠️ Skipping program with empty code:")
            print(f"   Name: {program[1]}")
            print(f"   Slug: {program[2]}")
            print("---")
            continue
            
        # Create a savepoint before each insert
        savepoint_name = f"sp_{i}"
        cursor.execute(f"SAVEPOINT {savepoint_name}")
        
        try:
            cursor.execute(insert_query, program)
        except errors.UniqueViolation as e:
            print(f"❌ Conflict detected for program:")
            print(f"   Code: {program[0]}")
            print(f"   Name: {program[1]}")
            print(f"   Slug: {program[2]}")
            print(f"   Error: {str(e)}")
            print("---")
            # Roll back to the savepoint instead of the entire transaction
            cursor.execute(f"ROLLBACK TO SAVEPOINT {savepoint_name}")
            continue
            
    conn.commit()
    print("✅ Data insertion completed.")
except Exception as e:
    print("❌ Error during data insertion:", e)
    conn.rollback()
finally:
    cursor.close()
    conn.close()
