from pydantic import SecretStr, model_validator
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: SecretStr
    ADMIN_ID: Optional[int] = None
    LOG_LEVEL: str = "INFO"
    DATABASE_URI: Optional[str] = None
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[SecretStr] = None
    TZ: str = "UTC"

    @model_validator(mode="after")
    def validate_db_uri(self) -> "Settings":
        if self.DATABASE_URI is None:
            if (
                self.DATABASE_URI is None
                and self.POSTGRES_DB is not None
                and self.POSTGRES_USER is not None
                and self.POSTGRES_PASSWORD is not None
            ):
                self.DATABASE_URI = "postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}".format(
                    username=self.POSTGRES_USER,
                    password=self.POSTGRES_PASSWORD.get_secret_value(),
                    host=self.POSTGRES_HOST,
                    port=self.POSTGRES_PORT,
                    database=self.POSTGRES_DB,
                )
            else:
                self.DATABASE_URI = "sqlite+aiosqlite:///db.sqlite"
            return self


Config = Settings()
