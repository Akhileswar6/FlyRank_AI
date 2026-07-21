import sqlite3
import os

DB_FILE = "tasks.db"

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        val = row[idx]
        if col[0] == 'done':
            val = bool(val)
        d[col[0]] = val
    return d

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = dict_factory
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL CHECK (done IN (0, 1))
        )
    ''')
    cursor.execute('SELECT COUNT(*) as count FROM tasks')
    count = cursor.fetchone()['count']
    if count == 0:
        example_tasks = [
            ("Buy groceries", 0),
            ("Finish assignment", 0),
            ("Clean the room", 1)
        ]
        cursor.executemany('INSERT INTO tasks (title, done) VALUES (?, ?)', example_tasks)
    conn.commit()
    conn.close()
