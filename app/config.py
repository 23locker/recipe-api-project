from pydantic_settings import BaseSettings


class Settings:
    # PostgreSQL
    DATABASE_URL: str

    # MongoDB
    MONGODB_URL: str =
    MONGODB_DB: str =

    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Redis
    REDIS_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
