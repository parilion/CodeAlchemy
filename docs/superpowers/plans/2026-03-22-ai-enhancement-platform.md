# AI赋能开发平台 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个自动化AI赋能开发平台，能将普通Java管理系统（Spring Boot）自动注入AI能力模块（对话助手、RAG检索、智能搜索、智能分类、协同过滤推荐），并支持从预制模板快速生成全新AI增强系统，输出完整源码包供学生下载部署。

**Architecture:** Python FastAPI后端负责Java代码解析（AST）、AI能力代码生成与注入、Jinja2模板套用；React+Ant Design前端提供项目上传、AI模块配置、模板生成、知识库管理等Web界面；ChromaDB作为向量数据库支持RAG；LiteLLM统一对接多LLM Provider。输出为含注入代码的ZIP源码包。

**Tech Stack:** Python 3.11 / FastAPI / tree-sitter-java / ChromaDB / LiteLLM / Jinja2 / React 18 / Ant Design 5 / Vite / Zustand

---

## 文件结构映射

### 后端
```
backend/
├── app/
│   ├── main.py                          # FastAPI 入口，路由注册
│   ├── core/
│   │   ├── config.py                    # 配置（LLM Key、ChromaDB路径等）
│   │   └── llm_gateway.py               # LiteLLM 统一网关，支持多Provider
│   ├── api/routes/
│   │   ├── projects.py                  # 项目上传/查询/删除
│   │   ├── enhance.py                   # 代码增强流水线 API
│   │   ├── templates.py                 # 模板生成流水线 API
│   │   └── knowledge.py                 # 知识库管理 API
│   ├── services/
│   │   ├── code_analyzer.py             # Java AST 解析，识别技术栈/可增强点
│   │   ├── code_injector.py             # AI模块代码注入到原项目
│   │   ├── template_engine.py           # 基于Jinja2的模板套用与生成
│   │   └── package_builder.py           # 输出 ZIP 源码包
│   ├── ai_modules/
│   │   ├── base.py                      # AIModule 基类接口
│   │   ├── chat_assistant.py            # 智能对话（查询型+知识问答型）
│   │   ├── rag_retrieval.py             # RAG增强检索模块
│   │   ├── smart_search.py              # 智能语义搜索模块
│   │   ├── smart_classify.py            # 智能分类模块
│   │   └── collaborative_filter.py      # 协同过滤推荐模块
│   ├── knowledge/
│   │   ├── doc_parser.py                # PDF/Word/MD/TXT 文档解析
│   │   ├── vector_store.py              # ChromaDB CRUD 操作
│   │   └── knowledge_manager.py         # 知识库管理（通用+业务）
│   └── models/
│       └── schemas.py                   # Pydantic 请求/响应模型
├── templates/                           # Jinja2代码模板
│   ├── spring_boot/
│   │   ├── AIConfig.java.j2
│   │   ├── ChatController.java.j2
│   │   ├── ChatService.java.j2
│   │   ├── RagService.java.j2
│   │   ├── SmartSearchService.java.j2
│   │   ├── ClassifyService.java.j2
│   │   └── RecommendService.java.j2
│   └── vue/
│       └── ChatWidget.vue.j2
├── project_templates/                   # 预制管理系统模板
│   ├── library/                         # 图书馆管理系统
│   ├── secondhand/                      # 二手商城系统
│   ├── appointment/                     # 预约挂号系统
│   └── pet/                             # 宠物管理系统
├── knowledge_base/general/
│   └── common_faq.md                    # 通用知识库
├── tests/
│   ├── test_code_analyzer.py
│   ├── test_code_injector.py
│   ├── test_ai_modules.py
│   ├── test_knowledge.py
│   └── test_api.py
├── pyproject.toml
└── requirements.txt
```

### 前端
```
frontend/
├── src/
│   ├── App.tsx                          # 路由配置
│   ├── pages/
│   │   ├── Dashboard.tsx                # 项目列表首页
│   │   ├── UploadProject.tsx            # 上传项目页
│   │   ├── ConfigureAI.tsx              # AI模块配置页
│   │   ├── TemplateGen.tsx              # 模板生成页
│   │   └── KnowledgeBase.tsx            # 知识库管理页
│   ├── components/
│   │   ├── AIModuleSelector.tsx         # AI模块多选配置组件
│   │   └── ProjectCard.tsx              # 项目卡片组件
│   ├── store/
│   │   └── useProjectStore.ts           # Zustand 全局状态
│   └── api/
│       └── client.ts                    # Axios API 客户端
├── package.json
└── vite.config.ts
```

---

## Task 1: 项目脚手架搭建

**Files:**
- Create: `backend/pyproject.toml`
- Create: `backend/requirements.txt`
- Create: `backend/app/main.py`
- Create: `frontend/package.json`
- Create: `frontend/vite.config.ts`
- Create: `frontend/src/App.tsx`

- [ ] **Step 1: 初始化后端项目结构**

```bash
cd backend
mkdir -p app/core app/api/routes app/services app/ai_modules app/knowledge app/models
mkdir -p templates/spring_boot templates/vue
mkdir -p project_templates/library project_templates/secondhand project_templates/appointment project_templates/pet
mkdir -p knowledge_base/general tests
touch app/__init__.py app/core/__init__.py app/api/__init__.py app/api/routes/__init__.py
touch app/services/__init__.py app/ai_modules/__init__.py app/knowledge/__init__.py app/models/__init__.py
```

- [ ] **Step 2: 创建 requirements.txt**

```
fastapi==0.115.0
uvicorn[standard]==0.30.0
python-multipart==0.0.9
pydantic-settings==2.3.0
javalang==0.13.0
chromadb==0.5.0
litellm==1.40.0
langchain-text-splitters==0.2.0
pypdf2==3.0.1
python-docx==1.1.2
jinja2==3.1.4
pytest==8.3.0
httpx==0.27.0
python-jose==3.3.0
aiofiles==23.2.1
```

- [ ] **Step 3: 创建 app/main.py**

```python
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
```

- [ ] **Step 4: 验证后端可启动**

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Expected: `Application startup complete.`

- [ ] **Step 5: 初始化前端项目**

```bash
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install antd @ant-design/icons zustand axios react-router-dom
```

- [ ] **Step 6: 验证前端可启动**

```bash
cd frontend && npm run dev
```
Expected: `Local: http://localhost:5173/`

- [ ] **Step 7: Commit**

```bash
git init
git add backend/ frontend/
git commit -m "feat: 项目脚手架初始化 (FastAPI + React + Ant Design)"
```

---

## Task 2: 核心配置与LLM网关

**Files:**
- Create: `backend/app/core/config.py`
- Create: `backend/app/core/llm_gateway.py`
- Test: `backend/tests/test_llm_gateway.py`

- [ ] **Step 1: 写失败测试**

```python
# tests/test_llm_gateway.py
import pytest
from unittest.mock import patch, AsyncMock
from app.core.llm_gateway import LLMGateway

@pytest.mark.asyncio
async def test_llm_gateway_chat_returns_string():
    gateway = LLMGateway(provider="openai", model="gpt-4o-mini", api_key="test-key")
    with patch("litellm.acompletion", new_callable=AsyncMock) as mock:
        mock.return_value.choices = [type("C", (), {"message": type("M", (), {"content": "hello"})()})()]
        result = await gateway.chat([{"role": "user", "content": "test"}])
    assert isinstance(result, str)
    assert result == "hello"

@pytest.mark.asyncio
async def test_llm_gateway_unsupported_provider_raises():
    with pytest.raises(ValueError, match="Unsupported provider"):
        LLMGateway(provider="unknown", model="x", api_key="k")
```

- [ ] **Step 2: 运行测试确认失败**

```bash
cd backend && pytest tests/test_llm_gateway.py -v
```
Expected: FAIL with `ImportError` or `ModuleNotFoundError`

- [ ] **Step 3: 创建 app/core/config.py**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o-mini"
    llm_api_key: str = ""
    llm_base_url: str = ""
    chroma_persist_dir: str = "./chroma_db"
    upload_dir: str = "./uploads"
    output_dir: str = "./outputs"

    class Config:
        env_file = ".env"

settings = Settings()
```

- [ ] **Step 4: 创建 app/core/llm_gateway.py**

```python
import litellm
from typing import List, Dict

SUPPORTED_PROVIDERS = {"openai", "anthropic", "ollama", "tongyi"}

class LLMGateway:
    def __init__(self, provider: str, model: str, api_key: str, base_url: str = ""):
        if provider not in SUPPORTED_PROVIDERS:
            raise ValueError(f"Unsupported provider: {provider}. Choose from {SUPPORTED_PROVIDERS}")
        self.provider = provider
        self.model = model
        self.api_key = api_key
        self.base_url = base_url

    async def chat(self, messages: List[Dict[str, str]]) -> str:
        kwargs = {
            "model": self.model,
            "messages": messages,
            "api_key": self.api_key,
        }
        if self.base_url:
            kwargs["base_url"] = self.base_url
        response = await litellm.acompletion(**kwargs)
        return response.choices[0].message.content

    async def embed(self, text: str) -> List[float]:
        response = await litellm.aembedding(
            model=f"{self.provider}/text-embedding-3-small",
            input=[text],
            api_key=self.api_key,
        )
        return response.data[0]["embedding"]
```

- [ ] **Step 5: 运行测试确认通过**

```bash
cd backend && pytest tests/test_llm_gateway.py -v
```
Expected: PASS (2 tests)

- [ ] **Step 6: Commit**

```bash
git add backend/app/core/ backend/tests/test_llm_gateway.py
git commit -m "feat: LLM网关配置，支持多Provider切换"
```

---

## Task 3: Java代码解析引擎

**Files:**
- Create: `backend/app/services/code_analyzer.py`
- Test: `backend/tests/test_code_analyzer.py`

**职责：** 扫描上传的Java Spring Boot项目，识别技术栈版本、Controller/Service/Repository结构、前端类型、数据库配置、可增强位置。

- [ ] **Step 1: 写失败测试**

```python
# tests/test_code_analyzer.py
import pytest
from pathlib import Path
from app.services.code_analyzer import CodeAnalyzer

SAMPLE_CONTROLLER = """
package com.example.library.controller;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/books")
public class BookController {
    @GetMapping
    public List<Book> list() { return null; }
    @PostMapping
    public Book create(@RequestBody Book book) { return null; }
}
"""

def test_analyze_detects_controllers(tmp_path):
    ctrl_dir = tmp_path / "src/main/java/com/example/library/controller"
    ctrl_dir.mkdir(parents=True)
    (ctrl_dir / "BookController.java").write_text(SAMPLE_CONTROLLER)
    analyzer = CodeAnalyzer(str(tmp_path))
    result = analyzer.analyze()
    assert "BookController" in result["controllers"]
    assert "/api/books" in result["api_endpoints"]

def test_analyze_detects_spring_boot(tmp_path):
    (tmp_path / "pom.xml").write_text('<dependency><artifactId>spring-boot-starter-web</artifactId></dependency>')
    analyzer = CodeAnalyzer(str(tmp_path))
    result = analyzer.analyze()
    assert result["framework"] == "spring-boot"

def test_analyze_empty_project_returns_defaults(tmp_path):
    analyzer = CodeAnalyzer(str(tmp_path))
    result = analyzer.analyze()
    assert result["framework"] == "unknown"
    assert result["controllers"] == []
```

- [ ] **Step 2: 运行测试确认失败**

```bash
cd backend && pytest tests/test_code_analyzer.py -v
```
Expected: FAIL with `ImportError`

- [ ] **Step 3: 实现 code_analyzer.py**

```python
import os
import re
from pathlib import Path
from typing import Dict, List, Any
import javalang

class CodeAnalyzer:
    def __init__(self, project_path: str):
        self.root = Path(project_path)

    def analyze(self) -> Dict[str, Any]:
        return {
            "framework": self._detect_framework(),
            "controllers": self._find_controllers(),
            "api_endpoints": self._extract_endpoints(),
            "entities": self._find_entities(),
            "frontend_type": self._detect_frontend(),
        }

    def _detect_framework(self) -> str:
        pom = self.root / "pom.xml"
        if pom.exists():
            content = pom.read_text(encoding="utf-8", errors="ignore")
            if "spring-boot" in content:
                return "spring-boot"
        return "unknown"

    def _find_controllers(self) -> List[str]:
        controllers = []
        for java_file in self.root.rglob("*Controller.java"):
            content = java_file.read_text(encoding="utf-8", errors="ignore")
            match = re.search(r"public class (\w+Controller)", content)
            if match:
                controllers.append(match.group(1))
        return controllers

    def _extract_endpoints(self) -> List[str]:
        endpoints = []
        for java_file in self.root.rglob("*Controller.java"):
            content = java_file.read_text(encoding="utf-8", errors="ignore")
            for m in re.finditer(r'@RequestMapping\(["\']([^"\']+)["\']', content):
                endpoints.append(m.group(1))
            for m in re.finditer(r'@(Get|Post|Put|Delete)Mapping\(["\']([^"\']+)["\']', content):
                endpoints.append(m.group(2))
        return endpoints

    def _find_entities(self) -> List[str]:
        entities = []
        for java_file in self.root.rglob("*.java"):
            content = java_file.read_text(encoding="utf-8", errors="ignore")
            if "@Entity" in content:
                match = re.search(r"public class (\w+)", content)
                if match:
                    entities.append(match.group(1))
        return entities

    def _detect_frontend(self) -> str:
        for f in self.root.rglob("*.vue"):
            return "vue"
        if (self.root / "src/main/resources/static").exists():
            return "static"
        return "unknown"
```

- [ ] **Step 4: 运行测试确认通过**

```bash
cd backend && pytest tests/test_code_analyzer.py -v
```
Expected: PASS (3 tests)

- [ ] **Step 5: Commit**

```bash
git add backend/app/services/code_analyzer.py backend/tests/test_code_analyzer.py
git commit -m "feat: Java代码解析引擎，识别Controller/Entity/API端点"
```

---

## Task 4: 知识库管理（文档解析 + ChromaDB）

**Files:**
- Create: `backend/app/knowledge/doc_parser.py`
- Create: `backend/app/knowledge/vector_store.py`
- Create: `backend/app/knowledge/knowledge_manager.py`
- Test: `backend/tests/test_knowledge.py`

- [ ] **Step 1: 写失败测试**

```python
# tests/test_knowledge.py
import pytest
from unittest.mock import MagicMock, patch
from app.knowledge.doc_parser import DocParser
from app.knowledge.vector_store import VectorStore

def test_doc_parser_txt(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("这是一本关于借书的指南。\n借书需要借书证。")
    parser = DocParser()
    chunks = parser.parse(str(f))
    assert len(chunks) > 0
    assert any("借书" in c for c in chunks)

def test_doc_parser_md(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("# 借书指南\n\n借书步骤如下：\n1. 出示借书证\n2. 扫描书籍")
    parser = DocParser()
    chunks = parser.parse(str(f))
    assert len(chunks) > 0

def test_vector_store_add_and_query():
    with patch("chromadb.Client") as mock_client:
        mock_collection = MagicMock()
        mock_client.return_value.get_or_create_collection.return_value = mock_collection
        mock_collection.query.return_value = {"documents": [["借书需要借书证"]], "distances": [[0.1]]}
        store = VectorStore(collection_name="test", chroma_client=mock_client())
        store.add(["借书需要借书证"], ["doc-1"])
        results = store.query("借书证怎么办理", n_results=1)
        assert len(results) == 1
```

- [ ] **Step 2: 运行测试确认失败**

```bash
cd backend && pytest tests/test_knowledge.py -v
```
Expected: FAIL

- [ ] **Step 3: 实现 doc_parser.py**

```python
from pathlib import Path
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocParser:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def parse(self, file_path: str) -> List[str]:
        path = Path(file_path)
        text = self._extract_text(path)
        return self.splitter.split_text(text)

    def _extract_text(self, path: Path) -> str:
        suffix = path.suffix.lower()
        if suffix in (".txt", ".md"):
            return path.read_text(encoding="utf-8", errors="ignore")
        if suffix == ".pdf":
            import PyPDF2
            reader = PyPDF2.PdfReader(str(path))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        if suffix in (".docx",):
            import docx
            doc = docx.Document(str(path))
            return "\n".join(p.text for p in doc.paragraphs)
        return ""
```

- [ ] **Step 4: 实现 vector_store.py**

```python
from typing import List, Optional
import chromadb

class VectorStore:
    def __init__(self, collection_name: str, chroma_client=None, persist_dir: str = "./chroma_db"):
        if chroma_client is None:
            client = chromadb.Client(chromadb.Settings(persist_directory=persist_dir))
        else:
            client = chroma_client
        self.collection = client.get_or_create_collection(collection_name)

    def add(self, documents: List[str], ids: List[str]) -> None:
        self.collection.add(documents=documents, ids=ids)

    def query(self, query_text: str, n_results: int = 3) -> List[str]:
        results = self.collection.query(query_texts=[query_text], n_results=n_results)
        return results["documents"][0] if results["documents"] else []

    def delete_collection(self) -> None:
        self.collection.delete()
```

- [ ] **Step 5: 实现 knowledge_manager.py**

```python
from typing import List
from pathlib import Path
from app.knowledge.doc_parser import DocParser
from app.knowledge.vector_store import VectorStore

class KnowledgeManager:
    GENERAL_COLLECTION = "general_knowledge"

    def __init__(self, project_id: str, persist_dir: str = "./chroma_db"):
        self.project_id = project_id
        self.general_store = VectorStore(self.GENERAL_COLLECTION, persist_dir=persist_dir)
        self.business_store = VectorStore(f"business_{project_id}", persist_dir=persist_dir)
        self.parser = DocParser()

    def add_business_document(self, file_path: str) -> int:
        chunks = self.parser.parse(file_path)
        ids = [f"{self.project_id}-{i}" for i in range(len(chunks))]
        self.business_store.add(chunks, ids)
        return len(chunks)

    def query(self, question: str, n_results: int = 3) -> List[str]:
        general = self.general_store.query(question, n_results=n_results)
        business = self.business_store.query(question, n_results=n_results)
        return list(dict.fromkeys(business + general))[:n_results]
```

- [ ] **Step 6: 运行测试确认通过**

```bash
cd backend && pytest tests/test_knowledge.py -v
```
Expected: PASS (3 tests)

- [ ] **Step 7: Commit**

```bash
git add backend/app/knowledge/ backend/tests/test_knowledge.py
git commit -m "feat: 知识库模块（文档解析 + ChromaDB向量存储）"
```

---

## Task 5: AI模块基类与智能对话助手

**Files:**
- Create: `backend/app/ai_modules/base.py`
- Create: `backend/app/ai_modules/chat_assistant.py`
- Test: `backend/tests/test_ai_modules.py`

- [ ] **Step 1: 写失败测试**

```python
# tests/test_ai_modules.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.ai_modules.chat_assistant import ChatAssistantModule

@pytest.mark.asyncio
async def test_chat_assistant_query_mode():
    mock_llm = AsyncMock()
    mock_llm.chat.return_value = '{"intent": "query", "entity": "Book", "condition": "author=张三"}'
    mock_km = MagicMock()
    module = ChatAssistantModule(llm=mock_llm, knowledge_manager=mock_km)
    result = await module.handle_query("查询作者是张三的所有图书")
    assert result["type"] == "query"
    assert "entity" in result

@pytest.mark.asyncio
async def test_chat_assistant_rag_mode():
    mock_llm = AsyncMock()
    mock_llm.chat.return_value = "借书证办理需携带学生证。"
    mock_km = MagicMock()
    mock_km.query.return_value = ["借书证办理需携带学生证到图书馆前台。"]
    module = ChatAssistantModule(llm=mock_llm, knowledge_manager=mock_km)
    result = await module.handle_knowledge_qa("借书证怎么办理？")
    assert isinstance(result, str)
    assert len(result) > 0
```

- [ ] **Step 2: 运行测试确认失败**

```bash
cd backend && pytest tests/test_ai_modules.py -v
```
Expected: FAIL

- [ ] **Step 3: 实现 base.py**

```python
from abc import ABC, abstractmethod
from typing import Any, Dict

class AIModule(ABC):
    MODULE_ID: str = ""
    MODULE_NAME: str = ""

    @abstractmethod
    def get_inject_files(self, project_analysis: Dict[str, Any]) -> Dict[str, str]:
        """返回需要注入到项目的文件，{文件路径: 文件内容}"""
        pass

    @abstractmethod
    def get_config_snippet(self) -> str:
        """返回需要添加到 application.yml 的配置片段"""
        pass
```

- [ ] **Step 4: 实现 chat_assistant.py**

```python
import json
from typing import Any, Dict
from app.ai_modules.base import AIModule
from app.core.llm_gateway import LLMGateway
from app.knowledge.knowledge_manager import KnowledgeManager

INTENT_PROMPT = """你是一个意图分类器。用户输入可能是"查询型"（查找数据）或"知识问答型"（询问业务知识）。
如果是查询型，返回JSON: {{"intent": "query", "entity": "实体名", "condition": "条件描述"}}
如果是知识问答型，返回JSON: {{"intent": "knowledge"}}
只返回JSON，不要其他文字。"""

class ChatAssistantModule(AIModule):
    MODULE_ID = "chat_assistant"
    MODULE_NAME = "智能对话助手"

    def __init__(self, llm: LLMGateway, knowledge_manager: KnowledgeManager):
        self.llm = llm
        self.km = knowledge_manager

    async def classify_intent(self, user_input: str) -> Dict:
        response = await self.llm.chat([
            {"role": "system", "content": INTENT_PROMPT},
            {"role": "user", "content": user_input},
        ])
        return json.loads(response)

    async def handle_query(self, user_input: str) -> Dict:
        intent = await self.classify_intent(user_input)
        intent["type"] = "query"
        return intent

    async def handle_knowledge_qa(self, question: str) -> str:
        context_chunks = self.km.query(question)
        context = "\n".join(context_chunks)
        return await self.llm.chat([
            {"role": "system", "content": f"基于以下知识库内容回答用户问题：\n{context}"},
            {"role": "user", "content": question},
        ])

    def get_inject_files(self, project_analysis: Dict[str, Any]) -> Dict[str, str]:
        base_pkg = project_analysis.get("base_package", "com.example.app")
        return {
            f"src/main/java/{base_pkg.replace('.', '/')}/ai/ChatController.java":
                self._render_chat_controller(base_pkg),
        }

    def get_config_snippet(self) -> str:
        return "ai:\n  chat:\n    enabled: true\n    llm-provider: ${AI_LLM_PROVIDER:openai}\n"

    def _render_chat_controller(self, base_pkg: str) -> str:
        return f"""package {base_pkg}.ai;
import org.springframework.web.bind.annotation.*;
import java.util.Map;
@RestController
@RequestMapping("/api/ai/chat")
public class ChatController {{
    @PostMapping
    public Map<String, String> chat(@RequestBody Map<String, String> req) {{
        // TODO: 调用AI服务
        return Map.of("reply", "AI回复: " + req.get("message"));
    }}
}}"""
```

- [ ] **Step 5: 运行测试确认通过**

```bash
cd backend && pytest tests/test_ai_modules.py -v
```
Expected: PASS (2 tests)

- [ ] **Step 6: Commit**

```bash
git add backend/app/ai_modules/ backend/tests/test_ai_modules.py
git commit -m "feat: AI模块基类与智能对话助手（查询型+知识问答型）"
```

---

## Task 6: RAG、智能搜索、智能分类、协同过滤模块

**Files:**
- Create: `backend/app/ai_modules/rag_retrieval.py`
- Create: `backend/app/ai_modules/smart_search.py`
- Create: `backend/app/ai_modules/smart_classify.py`
- Create: `backend/app/ai_modules/collaborative_filter.py`

这四个模块主要职责是生成注入代码（`get_inject_files`），运行时逻辑在注入的Java代码中执行。

- [ ] **Step 1: 写失败测试**

```python
# 追加到 tests/test_ai_modules.py
from app.ai_modules.smart_search import SmartSearchModule
from app.ai_modules.smart_classify import SmartClassifyModule
from app.ai_modules.collaborative_filter import CollaborativeFilterModule

def test_smart_search_generates_inject_files():
    module = SmartSearchModule()
    files = module.get_inject_files({"base_package": "com.example.shop"})
    assert any("SmartSearch" in k for k in files)
    assert any("SmartSearch" in v for v in files.values())

def test_smart_classify_generates_inject_files():
    module = SmartClassifyModule()
    files = module.get_inject_files({"base_package": "com.example.shop"})
    assert any("Classify" in k or "classify" in k.lower() for k in files)

def test_collaborative_filter_generates_inject_files():
    module = CollaborativeFilterModule()
    files = module.get_inject_files({"base_package": "com.example.shop"})
    assert any("Recommend" in k or "recommend" in k.lower() for k in files)
```

- [ ] **Step 2: 运行测试确认失败**

```bash
cd backend && pytest tests/test_ai_modules.py::test_smart_search_generates_inject_files -v
```
Expected: FAIL

- [ ] **Step 3: 实现 smart_search.py**

```python
from typing import Any, Dict
from app.ai_modules.base import AIModule

class SmartSearchModule(AIModule):
    MODULE_ID = "smart_search"
    MODULE_NAME = "智能语义搜索"

    def get_inject_files(self, project_analysis: Dict[str, Any]) -> Dict[str, str]:
        base_pkg = project_analysis.get("base_package", "com.example.app")
        path = f"src/main/java/{base_pkg.replace('.', '/')}/ai/SmartSearchService.java"
        return {path: self._render_smart_search_service(base_pkg)}

    def get_config_snippet(self) -> str:
        return "ai:\n  search:\n    enabled: true\n"

    def _render_smart_search_service(self, base_pkg: str) -> str:
        return f"""package {base_pkg}.ai;
import org.springframework.stereotype.Service;
/**
 * 智能语义搜索服务 - AI赋能注入
 * 与精准搜索并行，用户可通过 searchMode 参数选择
 */
@Service
public class SmartSearchService {{
    /**
     * 语义搜索：将自然语言查询向量化后进行相似度匹配
     * @param query 用户自然语言输入，如"关于Java编程的入门书"
     * @param mode "smart"使用语义搜索，"precise"使用精准搜索
     */
    public java.util.List<String> search(String query, String mode) {{
        if ("smart".equals(mode)) {{
            // TODO: 调用向量化API进行语义检索
            return java.util.List.of("语义搜索结果: " + query);
        }}
        return java.util.List.of(); // 精准搜索由原有逻辑处理
    }}
}}"""
```

- [ ] **Step 4: 实现 smart_classify.py**

```python
from typing import Any, Dict
from app.ai_modules.base import AIModule

class SmartClassifyModule(AIModule):
    MODULE_ID = "smart_classify"
    MODULE_NAME = "智能分类"

    def get_inject_files(self, project_analysis: Dict[str, Any]) -> Dict[str, str]:
        base_pkg = project_analysis.get("base_package", "com.example.app")
        path = f"src/main/java/{base_pkg.replace('.', '/')}/ai/SmartClassifyService.java"
        return {path: self._render(base_pkg)}

    def get_config_snippet(self) -> str:
        return "ai:\n  classify:\n    enabled: true\n"

    def _render(self, base_pkg: str) -> str:
        return f"""package {base_pkg}.ai;
import org.springframework.stereotype.Service;
import java.util.List;
/**
 * 智能分类服务 - AI赋能注入
 * 根据内容自动推荐分类标签，用户可采纳或手动修改
 */
@Service
public class SmartClassifyService {{
    /**
     * @param content 待分类的内容（书名、商品名等）
     * @return 推荐的分类标签列表
     */
    public List<String> suggest(String content) {{
        // TODO: 调用LLM进行内容分类
        return List.of("待分类");
    }}
}}"""
```

- [ ] **Step 5: 实现 collaborative_filter.py**

```python
from typing import Any, Dict
from app.ai_modules.base import AIModule

class CollaborativeFilterModule(AIModule):
    MODULE_ID = "collaborative_filter"
    MODULE_NAME = "协同过滤推荐"

    def get_inject_files(self, project_analysis: Dict[str, Any]) -> Dict[str, str]:
        base_pkg = project_analysis.get("base_package", "com.example.app")
        path = f"src/main/java/{base_pkg.replace('.', '/')}/ai/RecommendService.java"
        return {path: self._render(base_pkg)}

    def get_config_snippet(self) -> str:
        return "ai:\n  recommend:\n    enabled: true\n    strategy: item-based\n"

    def _render(self, base_pkg: str) -> str:
        return f"""package {base_pkg}.ai;
import org.springframework.stereotype.Service;
import java.util.List;
/**
 * 协同过滤推荐服务 - AI赋能注入
 * 支持 user-based 和 item-based 两种策略
 */
@Service
public class RecommendService {{
    /**
     * 基于物品的协同过滤：找到与itemId相似的其他物品
     */
    public List<String> recommendSimilarItems(String itemId, int topN) {{
        // TODO: 实现物品相似度计算与推荐
        return List.of();
    }}
    /**
     * 基于用户的协同过滤：找到与userId偏好相似的其他用户喜欢的物品
     */
    public List<String> recommendForUser(String userId, int topN) {{
        // TODO: 实现用户相似度计算与推荐
        return List.of();
    }}
}}"""
```

- [ ] **Step 6: 实现 rag_retrieval.py**

```python
from typing import Any, Dict
from app.ai_modules.base import AIModule

class RagRetrievalModule(AIModule):
    MODULE_ID = "rag_retrieval"
    MODULE_NAME = "RAG增强检索"

    def get_inject_files(self, project_analysis: Dict[str, Any]) -> Dict[str, str]:
        base_pkg = project_analysis.get("base_package", "com.example.app")
        path = f"src/main/java/{base_pkg.replace('.', '/')}/ai/RagService.java"
        return {path: self._render(base_pkg)}

    def get_config_snippet(self) -> str:
        return "ai:\n  rag:\n    enabled: true\n    chroma-url: ${CHROMA_URL:http://localhost:8000}\n"

    def _render(self, base_pkg: str) -> str:
        return f"""package {base_pkg}.ai;
import org.springframework.stereotype.Service;
/**
 * RAG增强检索服务 - AI赋能注入
 * 从通用知识库+业务知识库检索相关片段，交由LLM生成回答
 */
@Service
public class RagService {{
    public String query(String question) {{
        // TODO: 调用ChromaDB检索相关知识片段
        // TODO: 组合上下文交给LLM生成回答
        return "RAG回答: " + question;
    }}
}}"""
```

- [ ] **Step 7: 运行测试确认通过**

```bash
cd backend && pytest tests/test_ai_modules.py -v
```
Expected: PASS (5 tests)

- [ ] **Step 8: Commit**

```bash
git add backend/app/ai_modules/
git commit -m "feat: RAG、智能搜索、智能分类、协同过滤推荐AI模块"
```

---

## Task 7: 代码注入引擎

**Files:**
- Create: `backend/app/services/code_injector.py`
- Create: `backend/app/services/package_builder.py`
- Test: `backend/tests/test_code_injector.py`

**职责：** 将选定的AI模块生成的文件写入项目目录，更新 pom.xml 依赖，生成 application.yml 追加配置。

- [ ] **Step 1: 写失败测试**

```python
# tests/test_code_injector.py
import pytest
from pathlib import Path
from app.services.code_injector import CodeInjector
from app.ai_modules.smart_search import SmartSearchModule

def test_injector_writes_module_files(tmp_path):
    (tmp_path / "pom.xml").write_text("<project></project>")
    (tmp_path / "src/main/resources").mkdir(parents=True)
    (tmp_path / "src/main/resources/application.yml").write_text("server:\n  port: 8080\n")
    injector = CodeInjector(str(tmp_path))
    module = SmartSearchModule()
    injector.inject([module], project_analysis={"base_package": "com.example.app"})
    injected_file = tmp_path / "src/main/java/com/example/app/ai/SmartSearchService.java"
    assert injected_file.exists()
    assert "SmartSearchService" in injected_file.read_text()

def test_injector_appends_config(tmp_path):
    (tmp_path / "src/main/resources").mkdir(parents=True)
    yml = tmp_path / "src/main/resources/application.yml"
    yml.write_text("server:\n  port: 8080\n")
    injector = CodeInjector(str(tmp_path))
    injector.inject([SmartSearchModule()], project_analysis={"base_package": "com.example.app"})
    content = yml.read_text()
    assert "ai:" in content
```

- [ ] **Step 2: 运行测试确认失败**

```bash
cd backend && pytest tests/test_code_injector.py -v
```
Expected: FAIL

- [ ] **Step 3: 实现 code_injector.py**

```python
from pathlib import Path
from typing import List, Dict, Any
from app.ai_modules.base import AIModule

class CodeInjector:
    def __init__(self, project_path: str):
        self.root = Path(project_path)

    def inject(self, modules: List[AIModule], project_analysis: Dict[str, Any]) -> None:
        for module in modules:
            inject_files = module.get_inject_files(project_analysis)
            for rel_path, content in inject_files.items():
                target = self.root / rel_path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
            self._append_config(module.get_config_snippet())

    def _append_config(self, snippet: str) -> None:
        yml_candidates = [
            self.root / "src/main/resources/application.yml",
            self.root / "src/main/resources/application.properties",
        ]
        for yml in yml_candidates:
            if yml.exists():
                original = yml.read_text(encoding="utf-8")
                if snippet.strip().split("\n")[0] not in original:
                    yml.write_text(original + "\n" + snippet, encoding="utf-8")
                return
```

- [ ] **Step 4: 实现 package_builder.py**

```python
import zipfile
from pathlib import Path

class PackageBuilder:
    def build_zip(self, project_path: str, output_path: str) -> str:
        root = Path(project_path)
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(str(out), "w", zipfile.ZIP_DEFLATED) as zf:
            for file in root.rglob("*"):
                if file.is_file() and ".git" not in str(file):
                    zf.write(file, file.relative_to(root.parent))
        return str(out)
```

- [ ] **Step 5: 运行测试确认通过**

```bash
cd backend && pytest tests/test_code_injector.py -v
```
Expected: PASS (2 tests)

- [ ] **Step 6: Commit**

```bash
git add backend/app/services/code_injector.py backend/app/services/package_builder.py backend/tests/test_code_injector.py
git commit -m "feat: 代码注入引擎与ZIP包构建器"
```

---

## Task 8: 模板生成引擎

**Files:**
- Create: `backend/app/services/template_engine.py`
- Create: `backend/project_templates/library/` (基础模板结构)
- Test: `backend/tests/test_template_engine.py`

- [ ] **Step 1: 写失败测试**

```python
# tests/test_template_engine.py
import pytest
from pathlib import Path
from app.services.template_engine import TemplateEngine

def test_template_engine_matches_library(tmp_path):
    engine = TemplateEngine(templates_dir="project_templates")
    template = engine.match_template("图书馆管理系统")
    assert template == "library"

def test_template_engine_matches_shop(tmp_path):
    engine = TemplateEngine(templates_dir="project_templates")
    template = engine.match_template("二手商城系统")
    assert template == "secondhand"

def test_template_engine_unknown_returns_closest():
    engine = TemplateEngine(templates_dir="project_templates")
    template = engine.match_template("宠物医院系统")
    assert template in ("pet", "library", "secondhand", "appointment")
```

- [ ] **Step 2: 运行测试确认失败**

```bash
cd backend && pytest tests/test_template_engine.py -v
```
Expected: FAIL

- [ ] **Step 3: 实现 template_engine.py**

```python
from pathlib import Path
from typing import Optional

TEMPLATE_KEYWORDS = {
    "library": ["图书馆", "图书", "借阅", "馆藏"],
    "secondhand": ["二手", "商城", "交易", "商品", "购物"],
    "appointment": ["预约", "挂号", "就诊", "医院", "诊断"],
    "pet": ["宠物", "动物", "领养", "饲养"],
}

class TemplateEngine:
    def __init__(self, templates_dir: str = "project_templates"):
        self.templates_dir = Path(templates_dir)

    def match_template(self, requirement: str) -> str:
        scores = {}
        for template, keywords in TEMPLATE_KEYWORDS.items():
            scores[template] = sum(1 for kw in keywords if kw in requirement)
        best = max(scores, key=lambda k: scores[k])
        return best

    def generate(self, requirement: str, output_path: str, selected_modules: list) -> str:
        template_name = self.match_template(requirement)
        template_dir = self.templates_dir / template_name
        import shutil
        shutil.copytree(str(template_dir), output_path, dirs_exist_ok=True)
        return template_name
```

- [ ] **Step 4: 运行测试确认通过**

```bash
cd backend && pytest tests/test_template_engine.py -v
```
Expected: PASS (3 tests)

- [ ] **Step 5: Commit**

```bash
git add backend/app/services/template_engine.py backend/tests/test_template_engine.py
git commit -m "feat: 模板匹配引擎（基于关键词匹配预制模板）"
```

---

## Task 9: API路由层

**Files:**
- Create: `backend/app/api/routes/projects.py`
- Create: `backend/app/api/routes/enhance.py`
- Create: `backend/app/api/routes/templates.py`
- Create: `backend/app/api/routes/knowledge.py`
- Create: `backend/app/models/schemas.py`
- Test: `backend/tests/test_api.py`

- [ ] **Step 1: 创建 schemas.py**

```python
from pydantic import BaseModel
from typing import List, Optional

class EnhanceRequest(BaseModel):
    project_id: str
    modules: List[str]  # ["chat_assistant", "rag_retrieval", "smart_search", ...]

class TemplateGenRequest(BaseModel):
    requirement: str
    modules: List[str]

class KnowledgeUploadResponse(BaseModel):
    chunks_added: int
    collection: str

class EnhanceResponse(BaseModel):
    project_id: str
    download_url: str
    injected_modules: List[str]
    analysis: dict
```

- [ ] **Step 2: 写失败测试**

```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_enhance_requires_project_id():
    resp = client.post("/api/enhance/", json={"modules": ["smart_search"]})
    assert resp.status_code == 422  # validation error, missing project_id

def test_template_gen_requires_requirement():
    resp = client.post("/api/templates/generate", json={"modules": []})
    assert resp.status_code == 422
```

- [ ] **Step 3: 运行测试确认通过 health，失败其他（路由未实现）**

```bash
cd backend && pytest tests/test_api.py::test_health -v
```
Expected: PASS

- [ ] **Step 4: 实现 enhance.py 路由**

```python
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import uuid, shutil
from app.models.schemas import EnhanceRequest, EnhanceResponse
from app.services.code_analyzer import CodeAnalyzer
from app.services.code_injector import CodeInjector
from app.services.package_builder import PackageBuilder
from app.core.config import settings

router = APIRouter()
MODULE_MAP = {}  # 注入时动态构建

def _get_module(module_id: str):
    from app.ai_modules.smart_search import SmartSearchModule
    from app.ai_modules.smart_classify import SmartClassifyModule
    from app.ai_modules.collaborative_filter import CollaborativeFilterModule
    from app.ai_modules.rag_retrieval import RagRetrievalModule
    map_ = {
        "smart_search": SmartSearchModule,
        "smart_classify": SmartClassifyModule,
        "collaborative_filter": CollaborativeFilterModule,
        "rag_retrieval": RagRetrievalModule,
    }
    cls = map_.get(module_id)
    return cls() if cls else None

@router.post("/upload")
async def upload_project(file: UploadFile = File(...)):
    project_id = str(uuid.uuid4())
    upload_path = Path(settings.upload_dir) / project_id
    upload_path.mkdir(parents=True, exist_ok=True)
    zip_path = upload_path / file.filename
    with open(zip_path, "wb") as f:
        f.write(await file.read())
    shutil.unpack_archive(str(zip_path), str(upload_path / "src"))
    return {"project_id": project_id}

@router.post("/", response_model=EnhanceResponse)
async def enhance_project(req: EnhanceRequest):
    project_path = Path(settings.upload_dir) / req.project_id / "src"
    if not project_path.exists():
        raise HTTPException(status_code=404, detail="Project not found")
    analysis = CodeAnalyzer(str(project_path)).analyze()
    modules = [m for m in (_get_module(mid) for mid in req.modules) if m]
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
async def download(project_id: str):
    out = Path(settings.output_dir) / f"{project_id}-enhanced.zip"
    if not out.exists():
        raise HTTPException(status_code=404, detail="Output not found")
    return FileResponse(str(out), filename=f"{project_id}-enhanced.zip")
```

- [ ] **Step 5: 实现 templates.py 路由**

```python
from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path
import uuid, shutil
from app.models.schemas import TemplateGenRequest
from app.services.template_engine import TemplateEngine
from app.services.code_injector import CodeInjector
from app.services.package_builder import PackageBuilder
from app.core.config import settings

router = APIRouter()

@router.post("/generate")
async def generate_from_template(req: TemplateGenRequest):
    project_id = str(uuid.uuid4())
    output_path = Path(settings.output_dir) / project_id
    engine = TemplateEngine()
    template_used = engine.generate(req.requirement, str(output_path), req.modules)
    modules = []
    zip_path = Path(settings.output_dir) / f"{project_id}-generated.zip"
    PackageBuilder().build_zip(str(output_path), str(zip_path))
    return {
        "project_id": project_id,
        "template_used": template_used,
        "download_url": f"/api/templates/download/{project_id}",
    }

@router.get("/download/{project_id}")
async def download(project_id: str):
    out = Path(settings.output_dir) / f"{project_id}-generated.zip"
    if not out.exists():
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Output not found")
    return FileResponse(str(out), filename=f"{project_id}-generated.zip")
```

- [ ] **Step 6: 实现 projects.py 和 knowledge.py 路由**

```python
# app/api/routes/projects.py
from fastapi import APIRouter
from pathlib import Path
from app.core.config import settings

router = APIRouter()

@router.get("/")
async def list_projects():
    upload_dir = Path(settings.upload_dir)
    if not upload_dir.exists():
        return []
    return [{"project_id": d.name} for d in upload_dir.iterdir() if d.is_dir()]
```

```python
# app/api/routes/knowledge.py
from fastapi import APIRouter, UploadFile, File
import uuid
from pathlib import Path
from app.knowledge.knowledge_manager import KnowledgeManager
from app.models.schemas import KnowledgeUploadResponse
from app.core.config import settings

router = APIRouter()

@router.post("/upload/{project_id}", response_model=KnowledgeUploadResponse)
async def upload_doc(project_id: str, file: UploadFile = File(...)):
    tmp_path = Path(settings.upload_dir) / "docs" / f"{uuid.uuid4()}-{file.filename}"
    tmp_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_bytes(await file.read())
    km = KnowledgeManager(project_id=project_id)
    count = km.add_business_document(str(tmp_path))
    return KnowledgeUploadResponse(chunks_added=count, collection=f"business_{project_id}")
```

- [ ] **Step 7: 运行所有测试**

```bash
cd backend && pytest tests/test_api.py -v
```
Expected: PASS (3 tests)

- [ ] **Step 8: Commit**

```bash
git add backend/app/api/ backend/app/models/ backend/tests/test_api.py
git commit -m "feat: API路由层（代码增强/模板生成/知识库/项目管理）"
```

---

## Task 10: 前端实现

**Files:**
- Create: `frontend/src/api/client.ts`
- Create: `frontend/src/store/useProjectStore.ts`
- Create: `frontend/src/components/AIModuleSelector.tsx`
- Create: `frontend/src/pages/Dashboard.tsx`
- Create: `frontend/src/pages/UploadProject.tsx`
- Create: `frontend/src/pages/ConfigureAI.tsx`
- Create: `frontend/src/pages/TemplateGen.tsx`
- Create: `frontend/src/pages/KnowledgeBase.tsx`
- Modify: `frontend/src/App.tsx`

- [ ] **Step 1: 创建 API 客户端 src/api/client.ts**

```typescript
import axios from 'axios'

const api = axios.create({ baseURL: 'http://localhost:8000' })

export const uploadProject = (file: File) => {
  const form = new FormData()
  form.append('file', file)
  return api.post<{ project_id: string }>('/api/enhance/upload', form)
}

export const enhanceProject = (projectId: string, modules: string[]) =>
  api.post('/api/enhance/', { project_id: projectId, modules })

export const generateFromTemplate = (requirement: string, modules: string[]) =>
  api.post('/api/templates/generate', { requirement, modules })

export const listProjects = () => api.get<{ project_id: string }[]>('/api/projects/')

export const uploadKnowledgeDoc = (projectId: string, file: File) => {
  const form = new FormData()
  form.append('file', file)
  return api.post(`/api/knowledge/upload/${projectId}`, form)
}
```

- [ ] **Step 2: 创建 Zustand Store src/store/useProjectStore.ts**

```typescript
import { create } from 'zustand'

interface ProjectStore {
  currentProjectId: string | null
  selectedModules: string[]
  setProjectId: (id: string) => void
  toggleModule: (moduleId: string) => void
  clearModules: () => void
}

export const useProjectStore = create<ProjectStore>((set) => ({
  currentProjectId: null,
  selectedModules: [],
  setProjectId: (id) => set({ currentProjectId: id }),
  toggleModule: (moduleId) => set((state) => ({
    selectedModules: state.selectedModules.includes(moduleId)
      ? state.selectedModules.filter((m) => m !== moduleId)
      : [...state.selectedModules, moduleId],
  })),
  clearModules: () => set({ selectedModules: [] }),
}))
```

- [ ] **Step 3: 创建 AI模块选择器组件 src/components/AIModuleSelector.tsx**

```tsx
import { Checkbox, Card, Row, Col, Tag } from 'antd'
import { useProjectStore } from '../store/useProjectStore'

const MODULES = [
  { id: 'chat_assistant', name: '智能对话助手', desc: '查询型 + 知识问答型对话' },
  { id: 'rag_retrieval', name: 'RAG增强检索', desc: '基于业务文档的智能问答' },
  { id: 'smart_search', name: '智能语义搜索', desc: '与精准搜索并行，用户可选' },
  { id: 'smart_classify', name: '智能分类', desc: 'AI自动推荐分类标签' },
  { id: 'collaborative_filter', name: '协同过滤推荐', desc: '"看了此商品的用户还看了..."' },
]

export default function AIModuleSelector() {
  const { selectedModules, toggleModule } = useProjectStore()
  return (
    <Row gutter={[16, 16]}>
      {MODULES.map((m) => (
        <Col key={m.id} xs={24} sm={12} md={8}>
          <Card
            hoverable
            style={{ border: selectedModules.includes(m.id) ? '2px solid #1677ff' : undefined }}
            onClick={() => toggleModule(m.id)}
          >
            <Checkbox checked={selectedModules.includes(m.id)} style={{ marginBottom: 8 }}>
              <strong>{m.name}</strong>
            </Checkbox>
            <p style={{ color: '#666', fontSize: 13 }}>{m.desc}</p>
          </Card>
        </Col>
      ))}
    </Row>
  )
}
```

- [ ] **Step 4: 创建主页 src/pages/Dashboard.tsx**

```tsx
import { Button, Card, Row, Col, Typography } from 'antd'
import { useNavigate } from 'react-router-dom'

export default function Dashboard() {
  const nav = useNavigate()
  return (
    <div style={{ padding: 32 }}>
      <Typography.Title level={2}>AI赋能开发平台</Typography.Title>
      <Row gutter={[24, 24]} style={{ marginTop: 32 }}>
        <Col xs={24} md={12}>
          <Card title="代码增强模式" hoverable onClick={() => nav('/upload')}>
            <p>上传现有Java管理系统 → 自动注入AI能力 → 下载增强版源码包</p>
            <Button type="primary" style={{ marginTop: 16 }}>开始增强</Button>
          </Card>
        </Col>
        <Col xs={24} md={12}>
          <Card title="模板生成模式" hoverable onClick={() => nav('/template')}>
            <p>输入需求描述 → 匹配预制模板 → 生成完整AI增强系统</p>
            <Button type="primary" style={{ marginTop: 16 }}>从模板生成</Button>
          </Card>
        </Col>
      </Row>
    </div>
  )
}
```

- [ ] **Step 5: 创建上传与配置页面**

```tsx
// src/pages/UploadProject.tsx
import { Upload, Button, Steps, message } from 'antd'
import { InboxOutlined } from '@ant-design/icons'
import { useState } from 'react'
import { uploadProject } from '../api/client'
import { useProjectStore } from '../store/useProjectStore'
import { useNavigate } from 'react-router-dom'

export default function UploadProject() {
  const [loading, setLoading] = useState(false)
  const { setProjectId } = useProjectStore()
  const nav = useNavigate()

  const handleUpload = async (file: File) => {
    setLoading(true)
    try {
      const res = await uploadProject(file)
      setProjectId(res.data.project_id)
      message.success('项目上传成功')
      nav('/configure')
    } catch {
      message.error('上传失败，请重试')
    } finally {
      setLoading(false)
    }
    return false
  }

  return (
    <div style={{ padding: 32 }}>
      <Steps current={0} items={[{title: '上传项目'},{title: '选择AI模块'},{title: '下载结果'}]} style={{ marginBottom: 32 }} />
      <Upload.Dragger beforeUpload={handleUpload} accept=".zip" disabled={loading}>
        <p><InboxOutlined style={{ fontSize: 48 }} /></p>
        <p>点击或拖拽上传 Spring Boot 项目 ZIP 包</p>
        <p style={{ color: '#999' }}>支持 Spring Boot 2.x / 3.x</p>
      </Upload.Dragger>
    </div>
  )
}
```

```tsx
// src/pages/ConfigureAI.tsx
import { Button, message, Divider, Typography } from 'antd'
import { useState } from 'react'
import AIModuleSelector from '../components/AIModuleSelector'
import { enhanceProject } from '../api/client'
import { useProjectStore } from '../store/useProjectStore'

export default function ConfigureAI() {
  const { currentProjectId, selectedModules } = useProjectStore()
  const [loading, setLoading] = useState(false)

  const handleEnhance = async () => {
    if (!currentProjectId) return
    if (selectedModules.length === 0) { message.warning('请至少选择一个AI功能模块'); return }
    setLoading(true)
    try {
      const res = await enhanceProject(currentProjectId, selectedModules)
      window.location.href = `http://localhost:8000${res.data.download_url}`
    } catch { message.error('增强失败') }
    finally { setLoading(false) }
  }

  return (
    <div style={{ padding: 32 }}>
      <Typography.Title level={3}>选择AI能力模块</Typography.Title>
      <AIModuleSelector />
      <Divider />
      <Button type="primary" size="large" loading={loading} onClick={handleEnhance}>
        开始AI赋能并下载源码包
      </Button>
    </div>
  )
}
```

- [ ] **Step 6: 创建模板生成页面 src/pages/TemplateGen.tsx**

```tsx
import { Input, Button, Typography, message } from 'antd'
import { useState } from 'react'
import AIModuleSelector from '../components/AIModuleSelector'
import { generateFromTemplate } from '../api/client'
import { useProjectStore } from '../store/useProjectStore'

export default function TemplateGen() {
  const [requirement, setRequirement] = useState('')
  const [loading, setLoading] = useState(false)
  const { selectedModules } = useProjectStore()

  const handleGenerate = async () => {
    if (!requirement.trim()) { message.warning('请输入项目需求描述'); return }
    setLoading(true)
    try {
      const res = await generateFromTemplate(requirement, selectedModules)
      window.location.href = `http://localhost:8000${res.data.download_url}`
    } catch { message.error('生成失败') }
    finally { setLoading(false) }
  }

  return (
    <div style={{ padding: 32 }}>
      <Typography.Title level={3}>从模板生成AI增强系统</Typography.Title>
      <Input.TextArea
        rows={3}
        placeholder="描述你的系统需求，如：图书馆管理系统，需要图书借阅、归还、查询功能"
        value={requirement}
        onChange={(e) => setRequirement(e.target.value)}
        style={{ marginBottom: 24 }}
      />
      <Typography.Title level={4}>选择AI能力模块</Typography.Title>
      <AIModuleSelector />
      <Button type="primary" size="large" loading={loading} onClick={handleGenerate} style={{ marginTop: 24 }}>
        生成AI增强系统
      </Button>
    </div>
  )
}
```

- [ ] **Step 7: 配置路由 src/App.tsx**

```tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Layout } from 'antd'
import Dashboard from './pages/Dashboard'
import UploadProject from './pages/UploadProject'
import ConfigureAI from './pages/ConfigureAI'
import TemplateGen from './pages/TemplateGen'

export default function App() {
  return (
    <BrowserRouter>
      <Layout style={{ minHeight: '100vh' }}>
        <Layout.Content style={{ background: '#fff' }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/upload" element={<UploadProject />} />
            <Route path="/configure" element={<ConfigureAI />} />
            <Route path="/template" element={<TemplateGen />} />
          </Routes>
        </Layout.Content>
      </Layout>
    </BrowserRouter>
  )
}
```

- [ ] **Step 8: 验证前端可正常运行**

```bash
cd frontend && npm run build
```
Expected: 无编译错误

- [ ] **Step 9: Commit**

```bash
git add frontend/src/
git commit -m "feat: 前端Web界面（仪表盘/上传/AI配置/模板生成）"
```

---

## Task 11: 集成验证与端到端测试

**Files:**
- Test: `backend/tests/test_integration.py`

- [ ] **Step 1: 写端到端集成测试**

```python
# tests/test_integration.py
import pytest
import shutil
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def sample_project(tmp_path):
    """创建最小化Spring Boot项目结构"""
    ctrl = tmp_path / "src/main/java/com/example/app/controller"
    ctrl.mkdir(parents=True)
    (ctrl / "BookController.java").write_text(
        'package com.example.app.controller;\n@RestController\npublic class BookController {}'
    )
    res = tmp_path / "src/main/resources"
    res.mkdir(parents=True)
    (res / "application.yml").write_text("server:\n  port: 8080\n")
    (tmp_path / "pom.xml").write_text("<project><artifactId>library</artifactId></project>")
    import zipfile
    zip_path = tmp_path.parent / "test_project.zip"
    with zipfile.ZipFile(str(zip_path), "w") as zf:
        for f in tmp_path.rglob("*"):
            if f.is_file():
                zf.write(f, f.relative_to(tmp_path))
    return zip_path

def test_full_enhance_pipeline(sample_project, monkeypatch, tmp_path):
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path / "uploads"))
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path / "outputs"))
    with open(sample_project, "rb") as f:
        resp = client.post("/api/enhance/upload", files={"file": ("test_project.zip", f, "application/zip")})
    assert resp.status_code == 200
    project_id = resp.json()["project_id"]
    enhance_resp = client.post("/api/enhance/", json={
        "project_id": project_id,
        "modules": ["smart_search", "smart_classify"]
    })
    assert enhance_resp.status_code == 200
    assert "download_url" in enhance_resp.json()
```

- [ ] **Step 2: 运行集成测试**

```bash
cd backend && pytest tests/test_integration.py -v
```
Expected: PASS

- [ ] **Step 3: 运行全部测试套件**

```bash
cd backend && pytest tests/ -v --tb=short
```
Expected: 所有测试通过

- [ ] **Step 4: 最终Commit**

```bash
git add backend/tests/test_integration.py
git commit -m "test: 端到端集成测试 - 代码增强流水线"
```

---

## 验收标准

1. `pytest tests/` 全部通过
2. 后端 `uvicorn app.main:app --reload` 正常启动，`/health` 返回 200
3. 前端 `npm run build` 无错误
4. 可上传一个Spring Boot ZIP → 选择模块 → 下载包含注入代码的ZIP
5. 可输入需求描述 → 匹配模板 → 下载生成的项目ZIP
6. 注入的Java文件中包含对应模块的 `SmartSearchService`/`RagService`/`RecommendService` 等类

---

## 注意事项

- **LLM调用**：需要在 `.env` 中配置 `LLM_API_KEY`，对话助手实际调用需要有效的API Key
- **向量数据库**：ChromaDB 需要 `pip install chromadb`，RAG功能需要嵌入模型（默认使用LLM Provider的embedding）
- **Java AST解析**：`javalang` 对格式要求严格，错误的Java代码可能解析失败，已使用regex作为回退方案
- **预制模板**：需要在 `project_templates/{library,secondhand,appointment,pet}/` 下放置实际的Spring Boot项目代码
