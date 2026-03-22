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
                    zf.write(file, file.relative_to(root))
        return str(out)
