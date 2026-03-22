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

SAMPLE_POM = """
<project>
  <dependencies>
    <dependency>
      <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
  </dependencies>
</project>
"""


def test_analyze_detects_controllers(tmp_path):
    ctrl_dir = tmp_path / "src/main/java/com/example/library/controller"
    ctrl_dir.mkdir(parents=True)
    (ctrl_dir / "BookController.java").write_text(SAMPLE_CONTROLLER)
    analyzer = CodeAnalyzer(str(tmp_path))
    result = analyzer.analyze()
    assert "BookController" in result["controllers"]


def test_analyze_detects_api_endpoints(tmp_path):
    ctrl_dir = tmp_path / "src/main/java/com/example/library/controller"
    ctrl_dir.mkdir(parents=True)
    (ctrl_dir / "BookController.java").write_text(SAMPLE_CONTROLLER)
    analyzer = CodeAnalyzer(str(tmp_path))
    result = analyzer.analyze()
    assert "/api/books" in result["api_endpoints"]


def test_analyze_detects_spring_boot(tmp_path):
    (tmp_path / "pom.xml").write_text(SAMPLE_POM)
    analyzer = CodeAnalyzer(str(tmp_path))
    result = analyzer.analyze()
    assert result["framework"] == "spring-boot"


def test_analyze_empty_project_returns_defaults(tmp_path):
    analyzer = CodeAnalyzer(str(tmp_path))
    result = analyzer.analyze()
    assert result["framework"] == "unknown"
    assert result["controllers"] == []
    assert result["api_endpoints"] == []


def test_analyze_detects_entities(tmp_path):
    entity_dir = tmp_path / "src/main/java/com/example/library/entity"
    entity_dir.mkdir(parents=True)
    (entity_dir / "Book.java").write_text(
        "@Entity\npublic class Book {\n    private Long id;\n}"
    )
    analyzer = CodeAnalyzer(str(tmp_path))
    result = analyzer.analyze()
    assert "Book" in result["entities"]


def test_analyze_detects_vue_frontend(tmp_path):
    vue_dir = tmp_path / "src/main/resources/static"
    vue_dir.mkdir(parents=True)
    (vue_dir / "App.vue").write_text("<template><div>Hello</div></template>")
    analyzer = CodeAnalyzer(str(tmp_path))
    result = analyzer.analyze()
    assert result["frontend_type"] == "vue"
