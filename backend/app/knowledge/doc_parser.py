from pathlib import Path
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocParser:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def parse(self, file_path: str) -> List[str]:
        path = Path(file_path)
        text = self._extract_text(path)
        if not text.strip():
            return []
        return self.splitter.split_text(text)

    def _extract_text(self, path: Path) -> str:
        suffix = path.suffix.lower()
        if suffix in (".txt", ".md"):
            return path.read_text(encoding="utf-8", errors="ignore")
        if suffix == ".pdf":
            try:
                import PyPDF2
                reader = PyPDF2.PdfReader(str(path))
                return "\n".join(page.extract_text() or "" for page in reader.pages)
            except Exception:
                return ""
        if suffix == ".docx":
            try:
                import docx
                doc = docx.Document(str(path))
                return "\n".join(p.text for p in doc.paragraphs)
            except Exception:
                return ""
        return ""
