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
