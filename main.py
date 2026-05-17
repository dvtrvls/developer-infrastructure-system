from app.monitoring.file_watcher import LogWatcher
from app.parsers.event_parser import EventRouter
from app.alerts.engine import AlertEngine
from app.alerts.dispatcher import AlertDispatcher
from app.core.event_bus import EventBus
from app.monitoring.system_monitor import SystemMonitor
from app.database.models import initialize_db
from app.database.repository import AlertRepository
from app.api.server import app as api_app
import threading
import uvicorn

def run_api():
    uvicorn.run(api_app, host="0.0.0.0", port=8000, log_level="warning")


def main():

    initialize_db()
    
    watcher = LogWatcher(r"C:\Users\dave lugasan\system_projects\developer-infrastructure-system\logs\fake_system.log")
    parser = EventRouter()
    engine = AlertEngine()
    dispatcher = AlertDispatcher()
    bus = EventBus()
    monitor = SystemMonitor()
    repo = AlertRepository()

    def run_log_watcher():
        for event in watcher.watch_log():
            bus.push(event)
    def run_system_monitor():
        for event in monitor.watch():
            bus.push(event)

    threading.Thread(target=run_log_watcher, daemon=True).start()
    threading.Thread(target=run_system_monitor, daemon=True).start()
    threading.Thread(target=run_api, daemon=True).start()

    print("System running — API at http://localhost:8000")
    print("Docs at http://localhost:8000/docs")

    for event in bus.listen():
        parsed = parser.process(event)
        alerts = engine.evaluate(parsed)
        for alert in alerts:
            dispatcher.dispatch(alert)
            repo.save(alert)
            

if __name__ == "__main__":
    main()