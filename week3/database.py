import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL", "postgres://postgres:dev@localhost:5432/tasks")

def get_db_connection():
    return psycopg.connect(DB_URL, row_factory=dict_row)

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
    ''')
    cursor.execute('SELECT COUNT(*) as count FROM tasks')
    count = cursor.fetchone()['count']
    if count == 0:
        example_tasks = [
            ("Buy groceries", False),
            ("Finish assignment", False),
            ("Clean the room", True)
        ]
        cursor.executemany('INSERT INTO tasks (title, done) VALUES (%s, %s)', example_tasks)
    conn.commit()
    conn.close()