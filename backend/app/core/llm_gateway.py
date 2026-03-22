import litellm
from typing import List, Dict

SUPPORTED_PROVIDERS = {"openai", "anthropic", "ollama", "tongyi"}


class LLMGateway:
    def __init__(self, provider: str, model: str, api_key: str, base_url: str = ""):
        if provider not in SUPPORTED_PROVIDERS:
            raise ValueError(
                f"Unsupported provider: {provider}. Choose from {SUPPORTED_PROVIDERS}"
            )
        self.provider = provider
        self.model = model
        self.api_key = api_key
        self.base_url = base_url

    async def chat(self, messages: List[Dict[str, str]]) -> str:
        kwargs = {
            "model": self.model,
            "messages": messages,
            "api_key": self.api_key,
        }
        if self.base_url:
            kwargs["base_url"] = self.base_url
        response = await litellm.acompletion(**kwargs)
        return response.choices[0].message.content

    async def embed(self, text: str) -> List[float]:
        response = await litellm.aembedding(
            model=f"{self.provider}/text-embedding-3-small",
            input=[text],
            api_key=self.api_key,
        )
        return response.data[0]["embedding"]
