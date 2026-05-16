# app/alerts/thresholds.py

from app.alerts.rules import Rule

# --- The Key Pattern ---
# Every threshold rule MUST check event type first.
# If it's not a metric event, ignore it immediately.
# This prevents log events from crashing your numeric comparisons.

CPU_THRESHOLD = 90
MEMORY_THRESHOLD = 85
DISK_THRESHOLD = 80

THRESHOLD_RULES = [
    Rule(
        name="High CPU Usage",
        severity="WARNING",
        condition_fn=lambda e: (
            e.get("type") == "metric" and
            e.get("cpu", 0) > CPU_THRESHOLD
        )
    ),
    Rule(
        name="Critical CPU Usage",
        severity="CRITICAL",
        condition_fn=lambda e: (
            e.get("type") == "metric" and
            e.get("cpu", 0) > 95
        )
    ),
    Rule(
        name="High Memory Usage",
        severity="WARNING",
        condition_fn=lambda e: (
            e.get("type") == "metric" and
            e.get("memory", 0) > MEMORY_THRESHOLD
        )
    ),
    Rule(
        name="High Disk Usage",
        severity="WARNING",
        condition_fn=lambda e: (
            e.get("type") == "metric" and
            e.get("disk", 0) > DISK_THRESHOLD
        )
    ),
]