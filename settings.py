from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_ENV: str
    DATABASE_HOSTNAME: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PW: str
    DATABASE_NAME: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="forbid"
    )


settings = Settings()  # type: ignore
