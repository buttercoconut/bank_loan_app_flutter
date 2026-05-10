# Configuration for the FastAPI backend
# This file holds settings such as database URLs, secret keys, and other
# environment‑specific variables.

from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    # Database connection string (PostgreSQL)
    DATABASE_URL: str = Field(
        "postgresql://postgres:postgres@localhost:5432/loan_db",
        env="DATABASE_URL",
    )
    # Secret key for JWT or other token based auth
    SECRET_KEY: str = Field("super-secret-key", env="SECRET_KEY")
    # Algorithm used for JWT
    ALGORITHM: str = Field("HS256", env="ALGORITHM")
    # Token expiration in minutes
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
