from pydantic_settings import BaseSettings
from typing import List, Optional
import json
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sheets API Generator"
    API_V1_STR: str = "/api/v1"
    
    # Security
    JWT_SECRET_KEY: str = os.environ["JWT_SECRET_KEY"]
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # Next.js frontend
        "http://localhost:8000",  # FastAPI backend
    ]
    
    # Google OAuth
    GOOGLE_CREDENTIALS: str = os.environ["GOOGLE_CREDENTIALS"]  # JSON string from service account key
    
    # Database
    DATABASE_URL: str = os.environ["DATABASE_URL"]

    @property
    def google_credentials_dict(self) -> dict:
        """Parse Google credentials JSON string into dict"""
        return json.loads(self.GOOGLE_CREDENTIALS)

    class Config:
        env_file = None  # Disable .env file loading

settings = Settings() 