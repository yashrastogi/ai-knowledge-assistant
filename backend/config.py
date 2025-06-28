"""Configuration management"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Google Gemini Configuration
    google_api_key: str = ""
    gemini_model: str = "gemini-pro"
    
    # HuggingFace Embeddings (Free - runs locally)
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_device: str = "cpu"
    
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
        env_file_encoding = "utf-8"
        case_sensitive = False


# Create global settings instance
# Look for .env file in backend directory
import os
from pathlib import Path

# Get the backend directory path
backend_dir = Path(__file__).parent
env_path = backend_dir / ".env"

# Load settings, explicitly passing env file path if it exists
if env_path.exists():
    settings = Settings(_env_file=str(env_path))
else:
    settings = Settings()
