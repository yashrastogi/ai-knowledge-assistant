"""Configuration management"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # OpenAI Configuration
    openai_api_key: str = ""
    openai_model: str = "gpt-4-turbo-preview"
    embedding_model: str = "text-embedding-3-small"
    
    # Vector Store Configuration
    vector_store_type: str = "faiss"
    vector_store_path: str = "./data/vector_store"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    log_level: str = "info"
    
    # CORS Configuration
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    
    # Agent Configuration
    max_iterations: int = 5
    agent_timeout: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create global settings instance
settings = Settings()
