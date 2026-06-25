from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://localhost:5432/beanbase"
    clerk_secret_key: str = ""
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    sentry_dsn: str = ""
    # Comma-separated; kept as str so pydantic-settings doesn't try JSON-decode
    allowed_origins: str = "http://localhost:3000"
    environment: str = "development"

    @property
    def allowed_origins_list(self) -> list:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]

    class Config:
        env_file = ".env"


settings = Settings()
