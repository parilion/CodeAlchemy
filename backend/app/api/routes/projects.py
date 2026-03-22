from fastapi import APIRouter
from pathlib import Path
from app.core.config import settings

router = APIRouter()


@router.get("/")
async def list_projects():
    upload_dir = Path(settings.upload_dir)
    if not upload_dir.exists():
        return []
    return [
        {"project_id": d.name}
        for d in upload_dir.iterdir()
        if d.is_dir()
    ]
