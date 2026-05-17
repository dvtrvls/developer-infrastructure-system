from fastapi import APIRouter
import psutil
from datetime import datetime


router = APIRouter()

@router.get("/current")
def  get_current_metric():
    return {
        "timestamp": datetime.now().isoformat(),
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk":  psutil.disk_usage("/").percent
    }

@router.get("/cpu")
def get_cpu():
    return  {
        "timestamps": datetime.now().isoformat(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_count": psutil.cpu_count()
    }

@router.get("/memory")
def get_memory():
    mem = psutil.virtual_memory()
    return {
        "timestamp": datetime.now().isoformat(),
        "total_gb": round(mem.total / (1024 ** 3), 2),
        "used_gb": round(mem.used / (1024 ** 3), 2),
        "percent": mem.percent
    }

@router.get("/disk")
def get_disk():
    disk = psutil.disk_usage("/")
    return {
        "timestamp": datetime.now().isoformat(),
        "total_gb": round(disk.total / (1024**3), 2),
        "used_gb": round(disk.used / (1024**3), 2),
        "percent": disk.percent
    }
