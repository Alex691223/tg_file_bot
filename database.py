import sqlite3

def init_db():
    conn = sqlite3.connect("files.db")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            file_id TEXT,
            file_type TEXT,
            caption TEXT,
            category TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()
