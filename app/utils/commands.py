from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat
from config import Config


async def set_commands_for_admins(bot: Bot):
    """
    Set custom commands for admins
    """
    commands = [
        BotCommand(command='id', description='Get current chat id'),
        BotCommand(command='fumo', description='Get random fumo face ᗜᴗᗜ'),
        BotCommand(command='fumofumo', description='Get Fumo of the day based on day and user id. '),
        BotCommand(command='get_stickers_id', description='Get stickers file_id'),
        BotCommand(command='add_fumo', description='Add fumos to database'),
        BotCommand(command='cancel', description='Cancel any operations'),
        BotCommand(command='list_fumos', description='List fumos by name in db.'),
    ]
    scope = BotCommandScopeChat(chat_id=Config.ADMIN_CHAT_ID)
    await bot.set_my_commands(commands, scope)
