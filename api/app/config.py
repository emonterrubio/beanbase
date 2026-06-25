from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://localhost:5432/beanbase"
    clerk_secret_key: str = ""
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    sentry_dsn: str = ""
    allowed_origins: List[str] = ["http://localhost:3000"]
    environment: str = "development"

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_origins(cls, v):
        if isinstance(v, str):
            return [o.strip() for o in v.split(",") if o.strip()]
        return v

    class Config:
        env_file = ".env"


settings = Settings()
