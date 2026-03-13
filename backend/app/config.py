# -*- coding: utf-8 -*-
"""
Configuration Management
Load configuration from environment variables.
"""

import os
from pathlib import Path
from dotenv import load_dotenv


# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


class Config:
    """Application configuration."""
    
    # ==================== Database ====================
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./data/content_factory.db"
    )
    
    # ==================== AI Service ====================
    DASHSCOPE_API_KEY: str = os.getenv("DASHSCOPE_API_KEY", "")
    AI_MODEL: str = os.getenv("AI_MODEL", "qwen-plus")
    
    # ==================== AI Timeout (seconds) ====================
    AI_TEXT_TIMEOUT: int = int(os.getenv("AI_TEXT_TIMEOUT", "30"))
    AI_IMAGE_TIMEOUT: int = int(os.getenv("AI_IMAGE_TIMEOUT", "60"))
    
    # ==================== Retry Mechanism ====================
    AI_MAX_RETRIES: int = int(os.getenv("AI_MAX_RETRIES", "3"))
    AI_RETRY_BASE_DELAY: int = int(os.getenv("AI_RETRY_BASE_DELAY", "1"))
    
    # ==================== Prompt Cache ====================
    PROMPT_CACHE_ENABLED: bool = os.getenv(
        "PROMPT_CACHE_ENABLED", "true"
    ).lower() == "true"
    PROMPT_CACHE_TTL: int = int(os.getenv("PROMPT_CACHE_TTL", "300"))
    
    # ==================== Generation Parameters ====================
    AI_MAX_TOKENS: int = int(os.getenv("AI_MAX_TOKENS", "2000"))
    AI_TEMPERATURE: float = float(os.getenv("AI_TEMPERATURE", "0.7"))
    
    # ==================== Server ====================
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # ==================== Logging ====================
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def get_ai_timeout(cls, is_image: bool = False) -> int:
        """
        Get AI timeout by type.
        
        Args:
            is_image: True for image generation, False for text
        
        Returns:
            Timeout in seconds
        """
        return cls.AI_IMAGE_TIMEOUT if is_image else cls.AI_TEXT_TIMEOUT
    
    @classmethod
    def get_retry_delay(cls, attempt: int) -> int:
        """
        Get retry delay with exponential backoff.
        
        Args:
            attempt: Current attempt number (0-based)
        
        Returns:
            Delay in seconds
        """
        return cls.AI_RETRY_BASE_DELAY * (2 ** attempt)
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate required configuration.
        
        Returns:
            True if valid, raises ValueError otherwise
        """
        if not cls.DASHSCOPE_API_KEY:
            raise ValueError("DASHSCOPE_API_KEY is required")
        if not cls.DATABASE_URL:
            raise ValueError("DATABASE_URL is required")
        return True
    
    @classmethod
    def to_dict(cls) -> dict:
        """Convert configuration to dictionary (for debugging)."""
        return {
            "DATABASE_URL": cls.DATABASE_URL,
            "AI_MODEL": cls.AI_MODEL,
            "AI_TEXT_TIMEOUT": cls.AI_TEXT_TIMEOUT,
            "AI_IMAGE_TIMEOUT": cls.AI_IMAGE_TIMEOUT,
            "AI_MAX_RETRIES": cls.AI_MAX_RETRIES,
            "AI_RETRY_BASE_DELAY": cls.AI_RETRY_BASE_DELAY,
            "PROMPT_CACHE_ENABLED": cls.PROMPT_CACHE_ENABLED,
            "PROMPT_CACHE_TTL": cls.PROMPT_CACHE_TTL,
            "AI_MAX_TOKENS": cls.AI_MAX_TOKENS,
            "AI_TEMPERATURE": cls.AI_TEMPERATURE,
            "HOST": cls.HOST,
            "PORT": cls.PORT,
            "LOG_LEVEL": cls.LOG_LEVEL,
        }


# Global config instance
config = Config()
