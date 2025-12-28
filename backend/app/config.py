import os
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
    REDIS_URL: str = "redis://localhost:6380/0"

    # RabbitMQ
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"

    # env
    APP_ENV: str = "prod"

    class Config:
        @classmethod
        def env_file(cls):
            env = os.getenv("APP_ENV", "prod")
            if env == "test":
                return ".env.test"
            return ".env"


settings = Settings()
