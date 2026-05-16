class Rule:
    def __init__(self, name, condition_fn, severity="INFO", alert_level=0, type="KEYWORD ERROR", category="SYSTEM PROBLEM", cooldown=10):
        self.name = name
        self.condition_fn = condition_fn # each rules has their own way to check if an error occured
        self.severity = severity
        self.alert_level =  alert_level
        self.category = category
        self.type = type
        self.cooldown = cooldown

    def matches(self, event: dict)-> bool:
        return self.condition_fn(event)
    

RULES = [

    # 🔴 SEVERITY-BASED
    Rule(
        name="Error Level Detected",
        condition_fn=lambda e: e.get("severity") == "ERROR",
        severity="CRITICAL",
        alert_level=3,
        type="SEVERITY",
        category="SYSTEM"
    ),
    Rule(
        name="Warning Level Detected",
        condition_fn=lambda e: e.get("severity") == "WARNING",
        severity="WARNING",
        alert_level=2,
        type="SEVERITY",
        category="SYSTEM"
    ),

    # ⚠️ PERFORMANCE / SYSTEM
    Rule(
        name="High CPU Usage",
        condition_fn=lambda e: "cpu usage high" in e.get("message", "").lower(),
        severity="WARNING",
        alert_level=2,
        type="KEYWORD",
        category="PERFORMANCE"
    ),
    Rule(
        name="Memory Issue",
        condition_fn=lambda e: "out of memory" in e.get("message", "").lower() or "memory usage high" in e.get("message", "").lower(),
        severity="CRITICAL",
        alert_level=3,
        type="KEYWORD",
        category="PERFORMANCE"
    ),
    Rule(
        name="Disk Full",
        condition_fn=lambda e: "disk full" in e.get("message", "").lower() or "disk almost full" in e.get("message", "").lower(),
        severity="CRITICAL",
        alert_level=3,
        type="KEYWORD",
        category="SYSTEM"
    ),

    # 🔐 SECURITY
    Rule(
        name="Failed Login Attempt",
        condition_fn=lambda e: "failed login" in e.get("message", "").lower(),
        severity="HIGH",
        alert_level=3,
        type="KEYWORD",
        category="SECURITY"
    ),
    Rule(
        name="Unauthorized Access",
        condition_fn=lambda e: "unauthorized" in e.get("message", "").lower() or "access denied" in e.get("message", "").lower(),
        severity="HIGH",
        alert_level=3,
        type="KEYWORD",
        category="SECURITY"
    ),
    Rule(
        name="Permission Issue",
        condition_fn=lambda e: "permission denied" in e.get("message", "").lower(),
        severity="MEDIUM",
        alert_level=2,
        type="KEYWORD",
        category="SECURITY"
    ),

    # 🌐 NETWORK
    Rule(
        name="Connection Timeout",
        condition_fn=lambda e: "timeout" in e.get("message", "").lower(),
        severity="MEDIUM",
        alert_level=2,
        type="KEYWORD",
        category="NETWORK"
    ),
    Rule(
        name="Connection Refused",
        condition_fn=lambda e: "connection refused" in e.get("message", "").lower(),
        severity="HIGH",
        alert_level=3,
        type="KEYWORD",
        category="NETWORK"
    ),
    Rule(
        name="Host Unreachable",
        condition_fn=lambda e: "host unreachable" in e.get("message", "").lower(),
        severity="HIGH",
        alert_level=3,
        type="KEYWORD",
        category="NETWORK"
    ),

    # 🗄️ DATABASE
    Rule(
        name="Database Connection Failed",
        condition_fn=lambda e: "database connection failed" in e.get("message", "").lower() or "db connection lost" in e.get("message", "").lower(),
        severity="CRITICAL",
        alert_level=3,
        type="KEYWORD",
        category="DATABASE"
    ),
    Rule(
        name="Query Timeout",
        condition_fn=lambda e: "query timeout" in e.get("message", "").lower(),
        severity="HIGH",
        alert_level=3,
        type="KEYWORD",
        category="DATABASE"
    ),
    Rule(
        name="Deadlock Detected",
        condition_fn=lambda e: "deadlock detected" in e.get("message", "").lower(),
        severity="CRITICAL",
        alert_level=3,
        type="KEYWORD",
        category="DATABASE"
    ),

    # 🧨 GENERIC FAILURES
    Rule(
        name="Generic Failure",
        condition_fn=lambda e: "failed" in e.get("message", "").lower(),
        severity="MEDIUM",
        alert_level=2,
        type="KEYWORD",
        category="SYSTEM"
    ),
    Rule(
        name="Exception Detected",
        condition_fn=lambda e: "exception" in e.get("message", "").lower(),
        severity="HIGH",
        alert_level=3,
        type="KEYWORD",
        category="SYSTEM"
    ),
    Rule(
        name="Service Crash",
        condition_fn=lambda e: "crash" in e.get("message", "").lower(),
        severity="CRITICAL",
        alert_level=3,
        type="KEYWORD",
        category="SYSTEM"
    ),

    # 📁 SOURCE-BASED
    Rule(
        name="Auth Log Monitoring",
        condition_fn=lambda e: e.get("source") == "auth.log",
        severity="INFO",
        alert_level=1,
        type="SOURCE",
        category="SECURITY"
    ),
    Rule(
        name="System Log Monitoring",
        condition_fn=lambda e: e.get("source") == "system.log",
        severity="INFO",
        alert_level=1,
        type="SOURCE",
        category="SYSTEM"
    ),
    Rule(
        name="Database Log Monitoring",
        condition_fn=lambda e: e.get("source") == "db.log",
        severity="INFO",
        alert_level=1,
        type="SOURCE",
        category="DATABASE"
    ),
]










