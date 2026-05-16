from app.monitoring.file_watcher import LogWatcher
from app.parsers.event_parser import EventRouter
from app.alerts.engine import AlertEngine
from app.alerts.dispatcher import AlertDispatcher
from scripts.generate_metrics import generate_metric_event
from app.core.event_bus import EventBus
from app.monitoring.system_monitor import SystemMonitor
import threading

def main():
    watcher = LogWatcher(r"C:\Users\dave lugasan\system_projects\developer-infrastructure-system\logs\fake_system.log")
    parser = EventRouter()
    engine = AlertEngine()
    dispatcher = AlertDispatcher()
    bus = EventBus()
    monitor = SystemMonitor()

    def run_log_watcher():
        for event in watcher.watch_log():
            bus.push(event)
    # def run_system_monitor():
    #     for event in monitor.watch():
    #         bus.push(event)

    threading.Thread(target=run_log_watcher, daemon=True).start()
    # threading.Thread(target=run_system_monitor, daemon=True).start()

    for event in bus.listen():
        parsed = parser.process(event)
        alerts = engine.evaluate(parsed)
        for alert in alerts:
            dispatcher.dispatch(alert)

if __name__ == "__main__":
    main()