from typing import Optional
import yaml
from pydantic import SecretStr, BaseModel, model_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_extra_types.timezone_name import TimeZoneName
from os import path

file_path = path.join(path.dirname(__file__), 'messages.yml')
with open(file_path, "r", encoding="utf-8") as stream1:
    messages_kwargs = yaml.safe_load(stream1)


class Messages(BaseModel):
    welcome_message: str = None
    thanks_message: str = None
    thanks_sticker: list[str] = []
    new_member_message: str = None
    new_member_sticker: list[str] = []
    left_member_message: str = None
    left_member_sticker: list[str] = []
    ban_member_message: str = None
    ban_member_sticker: list[str] = []
    fumofumo_message: str = None
    fumofumo_fumos: list[object] = []


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: SecretStr
    ADMIN_CHAT_ID: Optional[int] = None
    LOG_LEVEL: str = "INFO"
    DATABASE_URI: Optional[SecretStr] = None
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[SecretStr] = None
    HASH_SALT: Optional[SecretStr] = Field("salt", max_length=16)
    TIMEZONE: TimeZoneName = "UTC"
    model_config = SettingsConfigDict(env_file='.env')

    @model_validator(mode="after")
    def validate_db_uri(self) -> "Settings":
        if self.DATABASE_URI is None:
            if (
                self.DATABASE_URI is None
                and self.POSTGRES_DB is not None
                and self.POSTGRES_USER is not None
                and self.POSTGRES_PASSWORD is not None
            ):
                self.DATABASE_URI = SecretStr(
                    f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD.get_secret_value()}@"
                    f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
                )
            else:
                self.DATABASE_URI = SecretStr("sqlite+aiosqlite:///db.sqlite")
        return self


Config = Settings()
Messages = Messages(**messages_kwargs)
