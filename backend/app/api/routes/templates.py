import uuid
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.models.schemas import TemplateGenRequest, TemplateGenResponse
from app.services.template_engine import TemplateEngine
from app.services.package_builder import PackageBuilder
from app.core.config import settings

router = APIRouter()


@router.post("/generate", response_model=TemplateGenResponse)
async def generate_from_template(req: TemplateGenRequest):
    project_id = str(uuid.uuid4())
    output_path = Path(settings.output_dir) / project_id

    engine = TemplateEngine()
    template_used = engine.generate(req.requirement, str(output_path), req.modules)

    zip_path = Path(settings.output_dir) / f"{project_id}-generated.zip"
    PackageBuilder().build_zip(str(output_path), str(zip_path))

    return TemplateGenResponse(
        project_id=project_id,
        template_used=template_used,
        download_url=f"/api/templates/download/{project_id}",
    )


@router.get("/download/{project_id}")
async def download_generated(project_id: str):
    out = Path(settings.output_dir) / f"{project_id}-generated.zip"
    if not out.exists():
        raise HTTPException(status_code=404, detail="Output not found")
    return FileResponse(str(out), filename=f"{project_id}-generated.zip")
