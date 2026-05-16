# scripts/generate_metrics.py
import time
import random
from datetime import datetime

def generate_metric_event() -> dict:
    return {
        "type": "metric",
        "source": "system_monitor",
        "cpu": random.randint(50, 100),   # simulate spikes
        "memory": random.randint(40, 95),
        "disk": random.randint(30, 90),
        "timestamps": datetime.now().isoformat()
    }

if __name__ == "__main__":
    while True:
        event = generate_metric_event()
        print(f"[SIMULATED METRIC] {event}")
        time.sleep(2)