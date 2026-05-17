from app.database.connection import get_connections

def  initialize_db():
    conn = get_connections()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts
            (
        
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule_name TEXT NOT NULL,
                severity TEXT NOT NULL,
                source TEXT,
                message TEXT,
                timestamp TEXT NOT NULL, 
                event_type TEXT
           )
        """)
    conn.commit()
    conn.close()