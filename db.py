import sqlite3
from config import DB_NAME

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS assignments (
        user_id TEXT,
        category TEXT,
        date TEXT,
        challenge TEXT,
        completed INTEGER DEFAULT 0,
        PRIMARY KEY (user_id, category, date)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS streaks (
        user_id TEXT PRIMARY KEY,
        count INTEGER,
        last_day TEXT
    )
    """)

    conn.commit()
    conn.close()