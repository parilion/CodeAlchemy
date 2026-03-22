from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import projects, enhance, templates, knowledge

app = FastAPI(title="AI赋能开发平台", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(enhance.router, prefix="/api/enhance", tags=["enhance"])
app.include_router(templates.router, prefix="/api/templates", tags=["templates"])
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["knowledge"])


@app.get("/health")
def health():
    return {"status": "ok"}
