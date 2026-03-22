import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from app.core.llm_gateway import LLMGateway


@pytest.mark.asyncio
async def test_llm_gateway_chat_returns_string():
    gateway = LLMGateway(provider="openai", model="gpt-4o-mini", api_key="test-key")
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "hello"
    with patch("litellm.acompletion", new_callable=AsyncMock) as mock:
        mock.return_value = mock_response
        result = await gateway.chat([{"role": "user", "content": "test"}])
    assert isinstance(result, str)
    assert result == "hello"


@pytest.mark.asyncio
async def test_llm_gateway_unsupported_provider_raises():
    with pytest.raises(ValueError, match="Unsupported provider"):
        LLMGateway(provider="unknown", model="x", api_key="k")


def test_llm_gateway_supported_providers():
    """验证所有支持的 provider 都能实例化"""
    for provider in ("openai", "anthropic", "ollama", "tongyi"):
        gw = LLMGateway(provider=provider, model="test", api_key="k")
        assert gw.provider == provider
