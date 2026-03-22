import pytest
import json
from unittest.mock import AsyncMock, MagicMock
from app.ai_modules.chat_assistant import ChatAssistantModule


@pytest.mark.asyncio
async def test_chat_assistant_query_mode():
    mock_llm = AsyncMock()
    mock_llm.chat.return_value = json.dumps(
        {"intent": "query", "entity": "Book", "condition": "author=张三"}
    )
    mock_km = MagicMock()
    module = ChatAssistantModule(llm=mock_llm, knowledge_manager=mock_km)
    result = await module.handle_query("查询作者是张三的所有图书")
    assert result["type"] == "query"
    assert "entity" in result
    assert result["entity"] == "Book"


@pytest.mark.asyncio
async def test_chat_assistant_rag_mode():
    mock_llm = AsyncMock()
    mock_llm.chat.return_value = "借书证办理需携带学生证。"
    mock_km = MagicMock()
    mock_km.query.return_value = ["借书证办理需携带学生证到图书馆前台。"]
    module = ChatAssistantModule(llm=mock_llm, knowledge_manager=mock_km)
    result = await module.handle_knowledge_qa("借书证怎么办理？")
    assert isinstance(result, str)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_chat_assistant_classify_intent_query():
    mock_llm = AsyncMock()
    mock_llm.chat.return_value = json.dumps({"intent": "query", "entity": "User"})
    mock_km = MagicMock()
    module = ChatAssistantModule(llm=mock_llm, knowledge_manager=mock_km)
    result = await module.classify_intent("查询用户列表")
    assert result["intent"] == "query"


def test_chat_assistant_get_inject_files():
    mock_llm = AsyncMock()
    mock_km = MagicMock()
    module = ChatAssistantModule(llm=mock_llm, knowledge_manager=mock_km)
    files = module.get_inject_files({"base_package": "com.example.library"})
    assert len(files) > 0
    assert any("ChatController" in k or "ChatController" in v for k, v in files.items())


def test_chat_assistant_get_config_snippet():
    mock_llm = AsyncMock()
    mock_km = MagicMock()
    module = ChatAssistantModule(llm=mock_llm, knowledge_manager=mock_km)
    snippet = module.get_config_snippet()
    assert "ai:" in snippet
    assert isinstance(snippet, str)


from app.ai_modules.smart_search import SmartSearchModule
from app.ai_modules.smart_classify import SmartClassifyModule
from app.ai_modules.collaborative_filter import CollaborativeFilterModule
from app.ai_modules.rag_retrieval import RagRetrievalModule


def test_smart_search_generates_inject_files():
    module = SmartSearchModule()
    files = module.get_inject_files({"base_package": "com.example.shop"})
    assert len(files) > 0
    assert any("SmartSearch" in k or "SmartSearch" in v for k, v in files.items())


def test_smart_search_config_snippet():
    module = SmartSearchModule()
    snippet = module.get_config_snippet()
    assert "ai:" in snippet


def test_smart_classify_generates_inject_files():
    module = SmartClassifyModule()
    files = module.get_inject_files({"base_package": "com.example.shop"})
    assert len(files) > 0
    assert any("Classify" in k or "Classify" in v for k, v in files.items())


def test_collaborative_filter_generates_inject_files():
    module = CollaborativeFilterModule()
    files = module.get_inject_files({"base_package": "com.example.shop"})
    assert len(files) > 0
    assert any("Recommend" in k or "Recommend" in v for k, v in files.items())


def test_rag_retrieval_generates_inject_files():
    module = RagRetrievalModule()
    files = module.get_inject_files({"base_package": "com.example.shop"})
    assert len(files) > 0
    assert any("Rag" in k or "Rag" in v or "rag" in k.lower() for k, v in files.items())


def test_all_modules_have_module_id():
    modules = [SmartSearchModule(), SmartClassifyModule(), CollaborativeFilterModule(), RagRetrievalModule()]
    for m in modules:
        assert m.MODULE_ID != ""
        assert m.MODULE_NAME != ""


def test_all_modules_config_snippet_contains_ai():
    modules = [SmartSearchModule(), SmartClassifyModule(), CollaborativeFilterModule(), RagRetrievalModule()]
    for m in modules:
        snippet = m.get_config_snippet()
        assert "ai:" in snippet
