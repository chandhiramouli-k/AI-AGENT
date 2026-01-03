import sqlite3

DB_NAME = "data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            date TEXT,
            reasoning TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_meeting(title, date, reasoning):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO meetings (title, date, reasoning) VALUES (?, ?, ?)", (title, date, reasoning))
    conn.commit()
    conn.close()

def get_all_meetings():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM meetings")
    rows = cursor.fetchall()
    conn.close()
    return rows

init_db()