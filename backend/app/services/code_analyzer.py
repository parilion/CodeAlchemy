import re
from pathlib import Path
from typing import Dict, List, Any


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
            "base_package": self._detect_base_package(),
        }

    def _detect_framework(self) -> str:
        pom = self.root / "pom.xml"
        if pom.exists():
            content = pom.read_text(encoding="utf-8", errors="ignore")
            if "spring-boot" in content:
                return "spring-boot"
        build_gradle = self.root / "build.gradle"
        if build_gradle.exists():
            content = build_gradle.read_text(encoding="utf-8", errors="ignore")
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
            # @RequestMapping("/api/books")
            for m in re.finditer(r'@RequestMapping\s*\(\s*["\']([^"\']+)["\']', content):
                endpoints.append(m.group(1))
            # @GetMapping("/path") 等
            for m in re.finditer(r'@(?:Get|Post|Put|Delete|Patch)Mapping\s*\(\s*["\']([^"\']+)["\']', content):
                endpoints.append(m.group(1))
        return list(set(endpoints))

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
        for _ in self.root.rglob("*.vue"):
            return "vue"
        static = self.root / "src/main/resources/static"
        if static.exists():
            for _ in static.rglob("*.vue"):
                return "vue"
        templates = self.root / "src/main/resources/templates"
        if templates.exists():
            for _ in templates.rglob("*.html"):
                return "thymeleaf"
        return "unknown"

    def _detect_base_package(self) -> str:
        for java_file in self.root.rglob("*.java"):
            content = java_file.read_text(encoding="utf-8", errors="ignore")
            match = re.match(r"package\s+([\w.]+);", content.strip())
            if match:
                pkg = match.group(1)
                # 取前3段作为 base package
                parts = pkg.split(".")
                return ".".join(parts[:3]) if len(parts) >= 3 else pkg
        return "com.example.app"
