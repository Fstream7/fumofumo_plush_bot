from typing import Optional
from os import path
import yaml
from pydantic import SecretStr, BaseModel, model_validator, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_extra_types.timezone_name import TimeZoneName

file_path = path.join(path.dirname(__file__), 'messages.yml')
with open(file_path, "r", encoding="utf-8") as stream1:
    messages_kwargs = yaml.safe_load(stream1)


class Messages(BaseModel):
    welcome_message: str
    propose_command_message: str
    propose_cant_edit_message: str
    propose_thanks_message: str
    propose_thanks_stickers: list[str]
    new_member_message: str
    new_member_stickers: list[str]
    left_member_message: str
    left_member_stickers: list[str]
    ban_member_message: str
    ban_member_stickers: list[str]
    fumofumo_message: str
    fumofumo_message_not_found: str
    privacy: str
    blacklist_words: list[str]
    blacklist_ban_message: str
    quiz_guess_message:  str
    quiz_success_message: str
    quiz_fail_message: str
    quiz_no_fumos_in_collection_message: str
    quiz_finish_animation_id: str
    quiz_finish_win_message: str
    quiz_finish_fail_message: str


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: SecretStr
    ADMIN_CHAT_ID: int
    LOG_LEVEL: str = "INFO"
    DATABASE_URI: Optional[SecretStr] = None
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[SecretStr] = None
    HASH_SALT: Optional[SecretStr] = SecretStr("salt")
    TIMEZONE: TimeZoneName = "UTC"
    QUIZ_CHAT_ID: Optional[int] = None
    model_config = SettingsConfigDict(env_file='.env')

    @field_validator("QUIZ_CHAT_ID", mode="before")
    @classmethod
    def empty_string_to_none(cls, input):
        """Convert empty fields from docker to None for Optional[int] values"""
        if input == '':
            return None
        return input

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
