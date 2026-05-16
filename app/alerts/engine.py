from app.alerts.rules import RULES
from collections import deque
from app.alerts.thresholds import THRESHOLD_RULES
import time

class AlertEngine:
    def __init__(self, rules=None, max_history_len=100):
        self.history = deque(maxlen=max_history_len)
        self.rules = rules if rules is not None else RULES + THRESHOLD_RULES
        self.last_fired = {}
    def evaluate(self, event: dict)->list:
        fired = []
        now = time.time()
        for rule in self.rules:
            if rule.matches(event):
                last = self.last_fired.get(rule.name, 0)
                cooldown = getattr(rule, "cooldown",  10)

                if (now - last) < cooldown:
                    continue

                self.last_fired[rule.name] = now

                log = {
                    "rule_name": rule.name,
                    "severity": rule.severity,
                    "alert_level": rule.alert_level,
                    "category": rule.category,
                    "type": rule.type,
                    "event": event,
                    "is_frequent": False,
                    "message": event["message"]        
                }
                if len(self.filter_by_rule(log["rule_name"])) > 25:
                    log["is_frequent"] = True

                fired.append(log)
                self.history.append(log)

        return fired
    
   
    def filter_by_rule(self, severity: str):
        return [event for event in self.history if event["rule_name"].lower() == severity.lower()]
