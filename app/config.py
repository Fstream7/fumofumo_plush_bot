import yaml
from pydantic import SecretStr, BaseModel
from pydantic_settings import BaseSettings
from typing import Optional

with open('messages.yml', 'r') as stream1:
    messages_kwargs = yaml.safe_load(stream1)


class messages(BaseModel):
    welcome_message: str = None
    thanks_message: str = None
    thanks_sticker: list[str] = []
    new_member_message: str = None
    new_member_sticker: list[str] = []
    left_member_message: str = None
    left_member_sticker: list[str] = []
    ban_regexs: list[str] = []
    ban_message: str = None


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: SecretStr
    ADMIN_CHAT_ID: Optional[int] = None
    LOG_LEVEL: str = "INFO"


Config = Settings()
Messages = messages(**messages_kwargs)
