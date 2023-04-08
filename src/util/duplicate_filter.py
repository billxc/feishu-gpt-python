
# Store the processed records in sqlite
import os
import sqlite3


DB_PATH = "data/processed_records.db"

def init_db():
    if not os.path.exists(DB_PATH):
        # create an empty database file
        open(DB_PATH, 'a').close()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS records (id text)''')
    conn.commit()
    conn.close()

def is_processed(id):
    init_db()
    records = {}
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM records")
    rows = c.fetchall()
    for row in rows:
        records[row[0]] = True
    if id in records:
        return True

def event_is_processed(event):
    return is_processed(event.event.message.message_id)

def mark_event_processed(event):
    set_processed(event.event.message.message_id)

def set_processed(id):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO records VALUES (?)", (id,))
    conn.commit()
    conn.close()