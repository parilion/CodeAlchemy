import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

from app.models.schemas import EnhanceRequest, EnhanceResponse
from app.services.code_analyzer import CodeAnalyzer
from app.services.code_injector import CodeInjector
from app.services.package_builder import PackageBuilder
from app.core.config import settings

router = APIRouter()

MODULE_REGISTRY = {}


def _get_module(module_id: str):
    from app.ai_modules.smart_search import SmartSearchModule
    from app.ai_modules.smart_classify import SmartClassifyModule
    from app.ai_modules.collaborative_filter import CollaborativeFilterModule
    from app.ai_modules.rag_retrieval import RagRetrievalModule
    registry = {
        "smart_search": SmartSearchModule,
        "smart_classify": SmartClassifyModule,
        "collaborative_filter": CollaborativeFilterModule,
        "rag_retrieval": RagRetrievalModule,
    }
    cls = registry.get(module_id)
    return cls() if cls else None


@router.post("/upload")
async def upload_project(file: UploadFile = File(...)):
    project_id = str(uuid.uuid4())
    upload_path = Path(settings.upload_dir) / project_id
    upload_path.mkdir(parents=True, exist_ok=True)
    zip_path = upload_path / file.filename
    content = await file.read()
    zip_path.write_bytes(content)
    src_path = upload_path / "src"
    src_path.mkdir(exist_ok=True)
    try:
        shutil.unpack_archive(str(zip_path), str(src_path))
    except Exception:
        pass  # 如果不是压缩文件，src 目录保持空
    return {"project_id": project_id}


@router.post("/", response_model=EnhanceResponse)
async def enhance_project(req: EnhanceRequest):
    project_path = Path(settings.upload_dir) / req.project_id / "src"
    if not project_path.exists():
        raise HTTPException(status_code=404, detail="Project not found")

    analysis = CodeAnalyzer(str(project_path)).analyze()
    modules = [m for m in (_get_module(mid) for mid in req.modules) if m is not None]
    CodeInjector(str(project_path)).inject(modules, analysis)

    out_path = Path(settings.output_dir) / f"{req.project_id}-enhanced.zip"
    PackageBuilder().build_zip(str(project_path), str(out_path))

    return EnhanceResponse(
        project_id=req.project_id,
        download_url=f"/api/enhance/download/{req.project_id}",
        injected_modules=req.modules,
        analysis=analysis,
    )


@router.get("/download/{project_id}")
async def download_enhanced(project_id: str):
    out = Path(settings.output_dir) / f"{project_id}-enhanced.zip"
    if not out.exists():
        raise HTTPException(status_code=404, detail="Output not found")
    return FileResponse(str(out), filename=f"{project_id}-enhanced.zip")
