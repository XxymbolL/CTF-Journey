import psycopg2
import uuid
import os

db = psycopg2.connect(os.environ.get('DATABASE_URL'))
db.autocommit = True
with db.cursor() as cursor:
    print('Migrating database...')
    cursor.execute('CREATE TABLE IF NOT EXISTS students (id SERIAL PRIMARY KEY, username VARCHAR(255) UNIQUE NOT NULL, password TEXT NOT NULL)')

    cursor.execute('DROP TABLE IF EXISTS courses CASCADE')
    cursor.execute('CREATE TABLE IF NOT EXISTS courses (id VARCHAR(255) PRIMARY KEY, name VARCHAR(255) UNIQUE NOT NULL, full_name VARCHAR(255) NOT NULL, description TEXT, is_open BOOLEAN NOT NULL DEFAULT TRUE)')
    cursor.execute('INSERT INTO courses (id, name, full_name) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING', (str(uuid.uuid4()), 'DDP1', 'Foundations of Programming 1'))
    cursor.execute('INSERT INTO courses (id, name, full_name) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING', (str(uuid.uuid4()), 'CALC1', 'Calculus 1'))
    cursor.execute('INSERT INTO courses (id, name, full_name) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING', (str(uuid.uuid4()), 'DM1', 'Discrete Mathematics 1'))
    cursor.execute('INSERT INTO courses (id, name, full_name) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING', (str(uuid.uuid4()), 'LINALG', 'Linear Algebra'))
    cursor.execute('INSERT INTO courses (id, name, full_name) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING', (str(uuid.uuid4()), 'IDS', 'Intro to Digital Systems'))
    cursor.execute('INSERT INTO courses (id, name, full_name) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING', (str(uuid.uuid4()), 'SDA', 'Data Structures'))
    cursor.execute('INSERT INTO courses (id, name, full_name) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING', (str(uuid.uuid4()), 'DDP2', 'Foundations of Programming 2'))
    cursor.execute('INSERT INTO courses (id, name, full_name) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING', (str(uuid.uuid4()), 'ICO', 'Intro to Computer Organization'))
    cursor.execute('INSERT INTO courses (id, name, full_name) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING', (str(uuid.uuid4()), 'CALC2', 'Calculus 2'))
    cursor.execute('INSERT INTO courses (id, name, full_name) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING', (str(uuid.uuid4()), 'DM2', 'Discrete Mathematics 2'))
    cursor.execute('INSERT INTO courses (id, name, full_name, description, is_open) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING', (str(uuid.uuid4()), 'RIZZ', 'Rizzing 101', os.getenv('FLAG'), False))

    cursor.execute('DROP TABLE IF EXISTS student_courses')
    cursor.execute('CREATE TABLE IF NOT EXISTS student_courses (id SERIAL PRIMARY KEY, student_id INTEGER REFERENCES students (id) ON DELETE CASCADE, course_id VARCHAR(255) REFERENCES courses (id) ON DELETE CASCADE)')
