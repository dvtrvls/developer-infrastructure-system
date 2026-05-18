from fastapi import FastAPI
from  app.api.routes import  alerts, metrics
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from  pathlib import Path
import path
from fastapi.middleware.cors import CORSMiddleware

APP_FOLDER = Path(__file__).parent.parent


app = FastAPI(
    title="Developer Infrastructure System",
    description="Real-time monitoring and alerting api",
    version="1.0.0"
)
app.mount("/static", StaticFiles(directory="frontend"), name="static")
app.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])
app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {
        "status": "running",
        "message": "System is operational"
    }

@app.get("/")
def serve_dashboard():
    return FileResponse(path.join(APP_FOLDER, "frontend/index.html"))



