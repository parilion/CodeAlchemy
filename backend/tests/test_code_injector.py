import pytest
import zipfile
from pathlib import Path
from app.services.code_injector import CodeInjector
from app.services.package_builder import PackageBuilder
from app.ai_modules.smart_search import SmartSearchModule
from app.ai_modules.smart_classify import SmartClassifyModule


def _create_minimal_spring_project(base_dir: Path) -> None:
    """创建最小化 Spring Boot 项目结构"""
    (base_dir / "pom.xml").write_text(
        "<project><artifactId>test</artifactId></project>",
        encoding="utf-8"
    )
    resources = base_dir / "src/main/resources"
    resources.mkdir(parents=True)
    (resources / "application.yml").write_text("server:\n  port: 8080\n", encoding="utf-8")


def test_injector_writes_smart_search_files(tmp_path):
    _create_minimal_spring_project(tmp_path)
    injector = CodeInjector(str(tmp_path))
    module = SmartSearchModule()
    injector.inject([module], project_analysis={"base_package": "com.example.app"})
    injected_file = tmp_path / "src/main/java/com/example/app/ai/SmartSearchService.java"
    assert injected_file.exists()
    content = injected_file.read_text(encoding="utf-8")
    assert "SmartSearchService" in content
    assert "com.example.app.ai" in content


def test_injector_appends_config_to_yml(tmp_path):
    _create_minimal_spring_project(tmp_path)
    injector = CodeInjector(str(tmp_path))
    injector.inject([SmartSearchModule()], project_analysis={"base_package": "com.example.app"})
    yml_content = (tmp_path / "src/main/resources/application.yml").read_text(encoding="utf-8")
    assert "ai:" in yml_content
    assert "server:" in yml_content  # 原有配置保留


def test_injector_does_not_duplicate_config(tmp_path):
    _create_minimal_spring_project(tmp_path)
    injector = CodeInjector(str(tmp_path))
    module = SmartSearchModule()
    injector.inject([module], project_analysis={"base_package": "com.example.app"})
    injector.inject([module], project_analysis={"base_package": "com.example.app"})  # 注入两次
    yml_content = (tmp_path / "src/main/resources/application.yml").read_text(encoding="utf-8")
    assert yml_content.count("ai:") == 1  # 只有一个 ai: 配置块


def test_injector_multiple_modules(tmp_path):
    _create_minimal_spring_project(tmp_path)
    injector = CodeInjector(str(tmp_path))
    injector.inject(
        [SmartSearchModule(), SmartClassifyModule()],
        project_analysis={"base_package": "com.example.app"}
    )
    assert (tmp_path / "src/main/java/com/example/app/ai/SmartSearchService.java").exists()
    assert (tmp_path / "src/main/java/com/example/app/ai/SmartClassifyService.java").exists()


def test_package_builder_creates_zip(tmp_path):
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    (project_dir / "Test.java").write_text("public class Test {}", encoding="utf-8")
    (project_dir / "sub").mkdir()
    (project_dir / "sub" / "Sub.java").write_text("public class Sub {}", encoding="utf-8")

    out_zip = tmp_path / "output.zip"
    builder = PackageBuilder()
    result_path = builder.build_zip(str(project_dir), str(out_zip))
    assert Path(result_path).exists()
    with zipfile.ZipFile(result_path, "r") as zf:
        names = zf.namelist()
    assert any("Test.java" in n for n in names)
    assert any("Sub.java" in n for n in names)
