from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o-mini"
    llm_api_key: str = ""
    llm_base_url: str = ""
    chroma_persist_dir: str = "./chroma_db"
    upload_dir: str = "./uploads"
    output_dir: str = "./outputs"

    class Config:
        env_file = ".env"


settings = Settings()
