from pydantic import BaseModel
from typing import List, Optional


class EnhanceRequest(BaseModel):
    project_id: str
    modules: List[str]  # ["chat_assistant", "smart_search", ...]


class EnhanceResponse(BaseModel):
    project_id: str
    download_url: str
    injected_modules: List[str]
    analysis: dict


class TemplateGenRequest(BaseModel):
    requirement: str
    modules: List[str]


class TemplateGenResponse(BaseModel):
    project_id: str
    template_used: str
    download_url: str


class KnowledgeUploadResponse(BaseModel):
    chunks_added: int
    collection: str
