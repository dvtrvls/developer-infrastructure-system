from datetime import datetime
from rich.console import Console
from collections import deque


console = Console()

class AlertDispatcher:
    def __init__(self, max_logs=100):
        self.logs = deque(maxlen=max_logs)
        
    def dispatch(self, alert: dict):
        rule_name = alert["rule_name"]
        severity = alert["severity"]
        event = alert["event"]
        timestamp = event.get("timestamps", datetime.now().isoformat())
        source = event.get("source", "unknown")

        if event.get("type") == "metric":
            message = (
                f"cpu={event.get('cpu', '?')}%"
                f"memory={event.get("memory", '?')}%"
                f"disk={event.get("disk", '?')}%"
            )

        else:
            message = alert.get("message", "")

        styles = {
            "INFO": "cyan",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold red"
        }

        log_entry = {
            "rule_name": rule_name,
            "severity": severity,
            "source": source,
            "message": message,
            "timestamp": timestamp
        }
        self.logs.append(log_entry)

        style = styles.get(severity, "white")
        if alert['is_frequent']:
            console.print(["FREQUENT ERROR DETECTED"], style=styles["CRITICAL"])

        console.print(
            f"[ALERT] [{severity}] {rule_name} | {source} | {message} | {timestamp}",
            style=style
        )

    def search(self, keyword:str):
        return [log for log in self.logs if keyword.lower()  in log["message"].lower()]
    def filter_by_severity(self, severity: str):
        return [log for log in self.logs if log["severity"].lower() == severity.lower()]
    