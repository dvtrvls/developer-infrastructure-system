from fastapi import FastAPI
from  app.api.routes import  alerts, metrics


app = FastAPI(
    title="Developer Infrastructure System",
    description="Real-time monitorinb and alerting api",
    version="1.0.0"
)

app.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])
app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])

@app.get("/health")
def health_check():
    return {
        "status": "running",
        "message": "System is operational"
    }





