from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # PostgreSQL
    postgres_url: str
    postgres_user: str
    postgres_password: str
    postgres_db: str

    # Redis
    redis_url: str
    redis_password: str

    # ChromaDB
    chroma_host: str
    chroma_port: int
    chroma_token: str

    # Ollama
    ollama_url: str

    # LLM Providers
    openai_api_key: str
    anthropic_api_key: str

    # Auth
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiry_hours: int = 24

    # App
    environment: str = "development"
    log_level: str = "INFO"
    free_tier_queries_per_month: int = 50
    allowed_origins: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

@lru_cache
def get_settings() -> Settings:
    return Settings()