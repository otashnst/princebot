import sqlite3
import os

DB_PATH = os.path.join("data", "database.db")

def create_tables():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT,
            phone TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_contact(user_id, full_name, phone):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO contacts (user_id, full_name, phone)
        VALUES (?, ?, ?)
    ''', (user_id, full_name, phone))
    conn.commit()
    conn.close()
import sqlite3
import os

DB_PATH = "data/database.db"

def create_tables():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS stickers (
            code TEXT PRIMARY KEY
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT,
            phone TEXT,
            sticker_code TEXT,
            FOREIGN KEY (sticker_code) REFERENCES stickers(code)
        )
    ''')
    conn.commit()
    conn.close()

def check_sticker_code_exists(code):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT code FROM stickers WHERE code = ?", (code,))
    result = c.fetchone()
    conn.close()
    return result is not None

def is_code_used(code):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE sticker_code = ?", (code,))
    result = c.fetchone()
    conn.close()
    return result is not None

def save_user(user_id, full_name, phone, sticker_code):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO users (user_id, full_name, phone, sticker_code)
        VALUES (?, ?, ?, ?)
    ''', (user_id, full_name, phone, sticker_code))
    conn.commit()
    conn.close()
