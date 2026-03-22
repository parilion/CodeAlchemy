import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from app.knowledge.doc_parser import DocParser
from app.knowledge.vector_store import VectorStore


def test_doc_parser_txt(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("这是一本关于借书的指南。\n借书需要借书证。\n" * 20, encoding="utf-8")
    parser = DocParser()
    chunks = parser.parse(str(f))
    assert len(chunks) > 0
    assert any("借书" in c for c in chunks)


def test_doc_parser_md(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("# 借书指南\n\n借书步骤如下：\n1. 出示借书证\n2. 扫描书籍\n" * 20, encoding="utf-8")
    parser = DocParser()
    chunks = parser.parse(str(f))
    assert len(chunks) > 0


def test_doc_parser_empty_file(tmp_path):
    f = tmp_path / "empty.txt"
    f.write_text("", encoding="utf-8")
    parser = DocParser()
    chunks = parser.parse(str(f))
    assert isinstance(chunks, list)


def test_vector_store_add_and_query():
    mock_collection = MagicMock()
    mock_collection.query.return_value = {
        "documents": [["借书需要借书证"]],
        "distances": [[0.1]]
    }
    store = VectorStore.__new__(VectorStore)
    store.collection = mock_collection
    store.add(["借书需要借书证"], ["doc-1"])
    results = store.query("借书证怎么办理", n_results=1)
    assert len(results) == 1
    assert results[0] == "借书需要借书证"
    mock_collection.add.assert_called_once_with(documents=["借书需要借书证"], ids=["doc-1"])


def test_vector_store_empty_query():
    mock_collection = MagicMock()
    mock_collection.query.return_value = {"documents": [[]], "distances": [[]]}
    store = VectorStore.__new__(VectorStore)
    store.collection = mock_collection
    results = store.query("不存在的内容", n_results=3)
    assert results == []
