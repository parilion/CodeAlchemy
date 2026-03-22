from typing import List
import chromadb


class VectorStore:
    def __init__(self, collection_name: str, persist_dir: str = "./chroma_db"):
        try:
            client = chromadb.PersistentClient(path=persist_dir)
        except Exception:
            client = chromadb.Client(
                chromadb.Settings(
                    chroma_db_impl="duckdb+parquet",
                    persist_directory=persist_dir,
                    anonymized_telemetry=False,
                )
            )
        self.collection = client.get_or_create_collection(collection_name)

    def add(self, documents: List[str], ids: List[str]) -> None:
        self.collection.add(documents=documents, ids=ids)

    def query(self, query_text: str, n_results: int = 3) -> List[str]:
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
        )
        docs = results.get("documents", [[]])
        return docs[0] if docs and docs[0] else []

    def delete_collection(self) -> None:
        self.collection.delete()
