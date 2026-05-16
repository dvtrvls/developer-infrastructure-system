from app.monitoring.file_watcher import LogWatcher
from app.parsers.basic_parser import BasicParser
from app.alerts.engine import AlertEngine
from app.alerts.dispatcher import AlertDispatcher

def main():
    watcher = LogWatcher(r"C:\Users\dave lugasan\system_projects\developer-infrastructure-system\logs\fake_system.log")
    parser = BasicParser()
    engine = AlertEngine()
    dispatcher = AlertDispatcher()

    for event in watcher.watch_log():
        parsed = parser.parse(event)
        alerts = engine.evaluate(parsed)
        for alert in alerts:
            dispatcher.dispatch(alert)

if __name__ == "__main__":
    main()