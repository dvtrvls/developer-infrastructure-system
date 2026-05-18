import psutil
from datetime import datetime
import time

class SystemMonitor:
    def __init__(self, interval: int = 2):
        self.interval = interval
    def read(self) -> dict:
        """ read current machine stats and return as a metric event"""
        return {
            "type": "metric",
            "source": "System Monitor",
            "cpu":psutil.cpu_percent(interval=1),
            "memory": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage("/").percent,
            "timestamp": datetime.now().isoformat()
        }
    def watch(self):
        while True:
            yield self.read()
            time.sleep(self.interval)
