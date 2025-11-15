from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import Set, Tuple

class Settings(BaseSettings):

    """
    Application configuration and environment loader.

    - Fetches sensitive values from the .env by automatically validating .env variables using Pydantic at runtime (uvicorn main:app).
    - Stores global constants for file handling and language support.
    - Ensures consistent configuration usage across all modules.

    Defines a centralized configuration class that loads and validates environment variables (like API keys etc. )
    using Pydantic BaseSettings. Stores global constants for file handling and language support ennsuring consistent configuration usage across all modules.
    """

    
    GOOGLE_API_KEY: str = Field(..., description="Google API Key")
    GROQ_API_KEY: str = Field(..., description="Groq API Key")
    ELEVENLABS_API_KEY : str = Field(..., description="Elevenlabs API Key")
    ELEVENLABS_VOICE_ID : str = Field(..., description="Elevenlabs Voice ID")


    # Optional fields with default values

    MAX_FILE_SIZE: int = Field(default=10 * 1024 * 1024, description="Max file size in bytes")

    ALLOWED_EXTENSIONS: Set[str] = Field(default={".pdf", ".txt", ".docx"})

    SUPPORTED_LANGUAGES: Tuple[str, ...] = Field(
        default=("English", "Hindi", "Spanish", "French", "German", "Chinese", "Japanese", "Arabic")
    )


    # Configuration for loading settings from .env file

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    


"""
Creates and returns a single cached Settings instance, so only one instance of Settings is ever created. Avoids re-reading .env or recreating objects repeatedly. SINGLETON - only ONE instance of Settings will be created, subsequent calls return SAME object

"""

@lru_cache
def get_settings() -> Settings:
    return Settings()


