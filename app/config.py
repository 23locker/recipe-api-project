from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # PostgreSQL
    DATABASE_URL: str

    # MongoDB
    MONGODB_URL: str
    MONGODB_DB: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Redis
    REDIS_URL: str

    # env
    ENV: str = "prod"

    class Config:
        env_file = ".env"


settings = Settings()
