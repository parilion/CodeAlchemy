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
                # 取 snippet 第一行作为判重 key（如 "ai:"）
                first_line = snippet.strip().split("\n")[0]
                if first_line not in original:
                    yml.write_text(original + "\n" + snippet, encoding="utf-8")
                return
