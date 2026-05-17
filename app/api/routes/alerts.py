from fastapi import APIRouter, HTTPException
from app.database.repository import AlertRepository

router = APIRouter()
repo = AlertRepository()

@router.get("/")
def get_all_alerts():
    alerts = repo.get_all()
    return {"counts": len(alerts), "alerts": alerts}

@router.get("/recent")
def get_recent_alerts(limit: int = 50):
    alerts = repo.get_recent(limit)
    return {"counts": len(alerts), "alerts": alerts}

@router.get("/severity/{severity}")
def get_by_severity(severity: str):
    valid = ["INFO", "WARNING", "ERROR", "CRITICAL"]
    if severity.upper() not in valid:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid Severity. choose from {valid}"
        )
    alerts = repo.get_by_severity(severity.upper())
    return {"severity": severity.upper(), "count": len(alerts), "alerts": alerts}

@router.get("/stats")
def get_stats():
    alerts = repo.get_all()
    stats = {}
    for alert in alerts:
        sev = alert["severity"]
        stats[sev] = stats.get(sev, 0) + 1
    return {"total": len(alerts), "by_severity": stats} 

    