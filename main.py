from app.monitoring.file_watcher import LogWatcher
from app.parsers.basic_parser import BasicParser

def main():
    watcher = LogWatcher(r"C:\Users\dave lugasan\system_projects\developer-infrastructure-system\logs\fake_system.log")
    parser = BasicParser()
    for line in watcher.watch_log():
        parsed = parser.parse(line)
        print(parsed)

if __name__ == "__main__":
    main()
