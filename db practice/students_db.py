import random
import psycopg2

# Establish SQLite database connection
conn = psycopg2.connect(
    dbname="university",
    user="postgres",
    password="password",
    host="localhost"
)

cursor = conn.cursor()
# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS Majors (
    major_id INTEGER PRIMARY KEY,
    major_name TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Students (
    student_id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    gender TEXT,
    major_id INTEGER,
    total_credits INTEGER,
    FOREIGN KEY (major_id) REFERENCES Majors(major_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Courses (
    course_id INTEGER PRIMARY KEY,
    course_name TEXT,
    credits INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INTEGER,
    course_id INTEGER,
    grade REAL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
)
''')

# Sample data generation
major_names = ['Computer Science', 'Mathematics', 'Physics', 'Biology', 'Chemistry']
course_names = [
    'Introduction to Programming', 'Calculus I', 'Physics Lab', 'Biology Basics',
    'Organic Chemistry', 'Data Structures', 'Discrete Mathematics', 'Linear Algebra',
    'Environmental Science', 'Thermodynamics'
]

# Populate Majors
for i in range(1, 6):
    cursor.execute('INSERT INTO Majors (major_id, major_name) VALUES (%s, %s)', (i, major_names[i - 1]))

# Populate Courses
for i in range(1, 11):
    cursor.execute(
        'INSERT INTO Courses (course_id, course_name, credits) VALUES (%s, %s, %s)',
        (i, course_names[i - 1], random.randint(2, 5))
    )

# Populate Students
for i in range(1, 51):
    cursor.execute(
        'INSERT INTO Students (student_id, name, age, gender, major_id, total_credits) VALUES (%s, %s, %s, %s, %s, %s)',
        (
            i,
            f"Student {i}",
            random.randint(18, 25),
            random.choice(['M', 'F']),
            random.randint(1, 5),
            random.randint(10, 120)
        )
    )

# Populate Enrollments
for i in range(1, 51):
    for _ in range(random.randint(1, 5)):  # Each student enrolls in 1 to 5 courses
        cursor.execute(
            'INSERT INTO Enrollments (student_id, course_id, grade) VALUES (%s, %s, %s)',
            (
                i,
                random.randint(1, 10),  # Random course
                round(random.uniform(2.0, 4.0), 2)  # Grade between 2.0 and 4.0
            )
        )

# Commit and close the connection
conn.commit()
conn.close()

print("Database populated with sample data!")