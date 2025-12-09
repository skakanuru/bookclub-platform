"""Application configuration settings."""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str

    # Google OAuth
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str

    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080  # 7 days

    # CORS
    frontend_url: str

    # Open Library API
    open_library_api_url: str = "https://openlibrary.org"

    # Cloudinary
    cloudinary_cloud_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str

    # Environment
    environment: str = "development"

    # App Settings
    buffer_percentage: float = 3.0  # Progress buffer for comment visibility
    max_group_members: int = 32
    max_comment_length: int = 1000
    max_avatar_size_mb: int = 2

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
