from app.database.connection import get_connections


class AlertRepository:
    def save(self, alert: dict):
        event = alert["event"]
        conn = get_connections()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO alerts (rule_name, severity, source, message, timestamp, event_type)
            VALUES (?, ?, ?, ?, ?, ?)            
        """, (
            alert["rule_name"],
            alert["severity"],
            event.get("source", "unknown"),
            event.get("message", ""),
            event.get("timestamp", ""),
            event.get("type", "unknown")
        ))
        conn.commit()
        conn.close()
    def get_all(self)-> list:
        conn = get_connections()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alerts ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    def get_by_severity(self, severity: str) -> list:
        conn = get_connections()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM alerts WHERE severity = ? ORDER BY timestamp DESC",
            (severity, )
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    def get_recent(self, limit:int =50)-> list:
        conn = get_connections()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT ?", 
        (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for  row in rows]
