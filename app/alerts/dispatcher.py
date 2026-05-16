from datetime import datetime
from rich.console import Console

from datetime import datetime
from rich.console import Console

console = Console()

class AlertDispatcher:
    def dispatch(self, alert: dict):
        rule_name = alert["rule_name"]
        severity = alert["severity"]
        event = alert["event"]
        timestamp = event.get("timestamps", datetime.now().isoformat())
        source = event.get("sources", "unknown")
        message = event.get("message", "")

        styles = {
            "INFO": "cyan",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold red"
        }
        style = styles.get(severity, "white")

        console.print(
            f"[ALERT] [{severity}] {rule_name} | {source} | {message} | {timestamp}",
            style=style
        )
