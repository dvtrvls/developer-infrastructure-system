from app.alerts.rules import RULES

class AlertEngine:
    def __init__(self, rules=None):
        self.rules = rules if rules is not None else RULES
    def evaluate(self, event: dict)->list:
        fired = []
        for rule in self.rules:
            if rule.matches(event):
                fired.append({
                    "rule_name": rule.name,
                    "severity": rule.severity,
                    "alert_level": rule.alert_level,
                    "category": rule.category,
                    "type": rule.type,
                    "event": event            
                })
        return fired
