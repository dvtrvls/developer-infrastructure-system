import sqlite3
import os 

DB_PATH = os.path.join("data","devops.db")

def get_connections():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn