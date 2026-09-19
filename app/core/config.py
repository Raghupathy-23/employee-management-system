from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Employee Management System API"
    environment: str = "development"
    database_url: str = ""
    secret_key: str = "change-me-in-development"
    access_token_expire_minutes: int = 30
    jwt_algorithm: str = "HS256"
    cors_origins: str = "http://localhost:5174,http://127.0.0.1:5174,http://localhost:5173,http://127.0.0.1:5173"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )

    @field_validator("environment", mode="before")
    @classmethod
    def normalize_environment(cls, value: str) -> str:
        return str(value).strip().lower()

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    def validate_runtime(self) -> None:
        if not self.database_url:
            raise RuntimeError("DATABASE_URL is not configured.")
        if self.environment in {"production", "staging"} and self.secret_key == "change-me-in-development":
            raise RuntimeError("SECRET_KEY must be changed outside development environments.")
        if self.access_token_expire_minutes <= 0:
            raise RuntimeError("ACCESS_TOKEN_EXPIRE_MINUTES must be greater than zero.")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
