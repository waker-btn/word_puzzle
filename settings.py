from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_ENV: str
    DATABASE_HOSTNAME: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PW: str
    DATABASE_NAME: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    RATE_LIMIT: str  # Format: "10/minute", "100/hour"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="forbid"
    )


settings = Settings()  # type: ignore
