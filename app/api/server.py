from fastapi import FastAPI, Request
from  app.api.routes import  alerts, metrics
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from  pathlib import Path
import os
from fastapi.middleware.cors import CORSMiddleware
from app.security.auth import is_authenticated
from app.api.routes import  alerts, metrics, auth as auth_router


APP_FOLDER = Path(__file__).parent.parent.parent
print(APP_FOLDER)

app = FastAPI(
    title="Developer Infrastructure System",
    description="Real-time monitoring and alerting api",
    version="1.0.0"
)
app.mount("/static", StaticFiles(directory=str(APP_FOLDER / "frontend")), name="static")

app.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])
app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])
app.include_router(auth_router.router, tags=["Auth"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # or ["http://localhost:3000"]
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
def serve_dashboard(request: Request):
    if not is_authenticated(request):
        return RedirectResponse("/login", status_code=302)
    return FileResponse(APP_FOLDER / "frontend" / "index.html")




