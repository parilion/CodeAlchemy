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
        if not chunks:
            return 0
        ids = [f"{self.project_id}-chunk-{i}" for i in range(len(chunks))]
        self.business_store.add(chunks, ids)
        return len(chunks)

    def query(self, question: str, n_results: int = 3) -> List[str]:
        business = self.business_store.query(question, n_results=n_results)
        general = self.general_store.query(question, n_results=n_results)
        seen = set()
        result = []
        for item in business + general:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result[:n_results]
