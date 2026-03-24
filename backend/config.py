"""应用配置：从环境变量加载"""

import os


class Settings:
    # DeepSeek API
    DEEPSEEK_API_KEY: str = os.environ.get("DEEPSEEK_API_KEY", "")

    # Database (PostgreSQL via Supabase)
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "")

    # JWT
    JWT_SECRET: str = os.environ.get("JWT_SECRET", "change-me-in-production")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_DAYS: int = 7

    # Google OAuth
    GOOGLE_CLIENT_ID: str = os.environ.get("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.environ.get("GOOGLE_CLIENT_SECRET", "")

    # CORS
    ALLOWED_ORIGINS: str = os.environ.get("ALLOWED_ORIGINS", "*")


settings = Settings()
