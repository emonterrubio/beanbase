from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/beanbase"
    clerk_secret_key: str = ""
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    sentry_dsn: str = ""
    allowed_origins: list[str] = ["http://localhost:3000"]
    environment: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()
