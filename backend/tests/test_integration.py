import pytest
import zipfile
import shutil
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def _create_spring_project_zip(zip_path: Path) -> None:
    """创建最小化 Spring Boot 项目 ZIP"""
    tmp = zip_path.parent / "_tmp_proj"
    tmp.mkdir(exist_ok=True)

    ctrl_dir = tmp / "src/main/java/com/example/library/controller"
    ctrl_dir.mkdir(parents=True)
    (ctrl_dir / "BookController.java").write_text(
        'package com.example.library.controller;\n'
        'import org.springframework.web.bind.annotation.*;\n'
        '@RestController\n'
        '@RequestMapping("/api/books")\n'
        'public class BookController {\n'
        '    @GetMapping\n'
        '    public String list() { return "books"; }\n'
        '}\n',
        encoding="utf-8"
    )

    res_dir = tmp / "src/main/resources"
    res_dir.mkdir(parents=True)
    (res_dir / "application.yml").write_text(
        "server:\n  port: 8080\n",
        encoding="utf-8"
    )

    (tmp / "pom.xml").write_text(
        '<project><artifactId>library</artifactId>'
        '<dependencies><dependency>'
        '<artifactId>spring-boot-starter-web</artifactId>'
        '</dependency></dependencies></project>',
        encoding="utf-8"
    )

    with zipfile.ZipFile(str(zip_path), "w") as zf:
        for f in tmp.rglob("*"):
            if f.is_file():
                zf.write(f, f.relative_to(tmp))
    shutil.rmtree(str(tmp))


def test_health_endpoint():
    """基础健康检查"""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_list_projects_empty():
    """项目列表端点可访问"""
    resp = client.get("/api/projects/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_upload_project_returns_project_id(tmp_path):
    """上传项目返回项目ID"""
    zip_path = tmp_path / "test_project.zip"
    _create_spring_project_zip(zip_path)

    with open(zip_path, "rb") as f:
        resp = client.post(
            "/api/enhance/upload",
            files={"file": ("test_project.zip", f, "application/zip")}
        )

    assert resp.status_code == 200
    data = resp.json()
    assert "project_id" in data
    assert len(data["project_id"]) > 0


def test_enhance_nonexistent_project_returns_404():
    """增强不存在的项目返回404"""
    resp = client.post("/api/enhance/", json={
        "project_id": "nonexistent-project-12345",
        "modules": ["smart_search"]
    })
    assert resp.status_code == 404


def test_full_enhance_pipeline(tmp_path, monkeypatch):
    """完整流水线：上传 → 增强 → 验证下载URL"""
    # 临时配置上传/输出目录
    upload_dir = tmp_path / "uploads"
    output_dir = tmp_path / "outputs"
    upload_dir.mkdir()
    output_dir.mkdir()

    from app.core import config
    monkeypatch.setattr(config.settings, "upload_dir", str(upload_dir))
    monkeypatch.setattr(config.settings, "output_dir", str(output_dir))

    # Step 1: 上传项目
    zip_path = tmp_path / "project.zip"
    _create_spring_project_zip(zip_path)

    with open(zip_path, "rb") as f:
        upload_resp = client.post(
            "/api/enhance/upload",
            files={"file": ("project.zip", f, "application/zip")}
        )

    assert upload_resp.status_code == 200
    project_id = upload_resp.json()["project_id"]

    # Step 2: 执行增强（选择两个模块）
    enhance_resp = client.post("/api/enhance/", json={
        "project_id": project_id,
        "modules": ["smart_search", "smart_classify"]
    })

    assert enhance_resp.status_code == 200
    enhance_data = enhance_resp.json()
    assert "download_url" in enhance_data
    assert "analysis" in enhance_data
    assert enhance_data["project_id"] == project_id
    assert set(enhance_data["injected_modules"]) == {"smart_search", "smart_classify"}

    # Step 3: 验证增强后的文件已注入
    src_path = upload_dir / project_id / "src"
    smart_search_file = src_path / "src/main/java/com/example/library/ai/SmartSearchService.java"
    assert smart_search_file.exists(), f"SmartSearchService.java not found at {smart_search_file}"

    # Step 4: 验证 ZIP 包已生成
    zip_output = output_dir / f"{project_id}-enhanced.zip"
    assert zip_output.exists()


def test_template_generation(tmp_path, monkeypatch):
    """模板生成流水线"""
    output_dir = tmp_path / "outputs"
    output_dir.mkdir()

    from app.core import config
    monkeypatch.setattr(config.settings, "output_dir", str(output_dir))

    resp = client.post("/api/templates/generate", json={
        "requirement": "图书馆管理系统，需要图书借阅和归还功能",
        "modules": ["smart_search"]
    })

    assert resp.status_code == 200
    data = resp.json()
    assert data["template_used"] == "library"
    assert "download_url" in data
    assert "project_id" in data


def test_enhance_with_unknown_module_skips_gracefully(tmp_path, monkeypatch):
    """未知模块ID应被跳过，不报错"""
    upload_dir = tmp_path / "uploads"
    output_dir = tmp_path / "outputs"
    upload_dir.mkdir()
    output_dir.mkdir()

    from app.core import config
    monkeypatch.setattr(config.settings, "upload_dir", str(upload_dir))
    monkeypatch.setattr(config.settings, "output_dir", str(output_dir))

    zip_path = tmp_path / "project.zip"
    _create_spring_project_zip(zip_path)

    with open(zip_path, "rb") as f:
        upload_resp = client.post(
            "/api/enhance/upload",
            files={"file": ("project.zip", f, "application/zip")}
        )
    project_id = upload_resp.json()["project_id"]

    # 包含一个有效模块和一个无效模块
    enhance_resp = client.post("/api/enhance/", json={
        "project_id": project_id,
        "modules": ["smart_search", "nonexistent_module"]
    })
    assert enhance_resp.status_code == 200
