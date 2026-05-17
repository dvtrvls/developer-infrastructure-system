import time
from datetime import datetime
    

def generate_logs()-> dict:
    return {
        "raw_line": "[Error] hotdog",
        "source": "fake_log.log",
        "severity": "Unknown",
        "message": "hotdog",
        "event_type": "log",
        "timestamp": datetime.now().isoformat()

    }
if __name__ == "__main__":
    while True:
        event = generate_logs()
        print(f"[SIMULATED LOGS] {event}")
        time.sleep(2)