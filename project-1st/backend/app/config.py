from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    cors_origins: str = "http://localhost:5173"
    
    # Logging
    log_level: str = "INFO"
    
    # API Limits
    max_transcript_length: int = 100000  # characters
    api_timeout: int = 60  # seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert comma-separated CORS origins to list"""
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
