import os
import time
from datetime import datetime

class LogWatcher:
    def __init__(self, filepath:str, interval:int = 1):
        self.filepath = filepath
        self.interval = interval
    def watch_log(self):
        if not os.path.exists(self.filepath):
            open(self.filepath, "w").close()
        file = open(self.filepath, "r")
        file.seek(0, 2)
        last_pos = file.tell()
        while True:
            if not os.path.exists(self.filepath):
                print(f"File {self.filepath} deleted! Recreating ...")
                open(self.filepath, "w").close()   
            file.seek(last_pos)
            for line in file:
                yield {"source": os.path.basename(self.filepath), "raw_line": line.strip(), "timestamp": datetime.now().isoformat()}
            last_pos = file.tell()
            time.sleep(self.interval)

