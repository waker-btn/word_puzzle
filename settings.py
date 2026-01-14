from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_ENV: str = "production"
    # Railway provides DATABASE_URL, but also support individual variables
    DATABASE_URL: str | None = None
    DATABASE_HOSTNAME: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_USER: str = "postgres"
    DATABASE_PW: str = ""
    DATABASE_NAME: str = "word_puzzle"
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    RATE_LIMIT: str = "100/minute"  # Format: "10/minute", "100/hour"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()  # type: ignore
