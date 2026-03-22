import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File

from app.models.schemas import KnowledgeUploadResponse
from app.knowledge.knowledge_manager import KnowledgeManager
from app.core.config import settings

router = APIRouter()


@router.post("/upload/{project_id}", response_model=KnowledgeUploadResponse)
async def upload_knowledge_doc(project_id: str, file: UploadFile = File(...)):
    tmp_dir = Path(settings.upload_dir) / "knowledge_docs"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    tmp_path = tmp_dir / f"{uuid.uuid4()}-{file.filename}"
    tmp_path.write_bytes(await file.read())

    km = KnowledgeManager(project_id=project_id)
    count = km.add_business_document(str(tmp_path))

    return KnowledgeUploadResponse(
        chunks_added=count,
        collection=f"business_{project_id}",
    )
