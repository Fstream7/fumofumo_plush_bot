from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats
from config import Config


async def set_commands(bot: Bot) -> None:
    """
    Set commands for different chats
    """
    admin_commands = [
        BotCommand(command='id', description='Get current chat id'),
        BotCommand(command='fumo', description='Get random fumo face ᗜᴗᗜ'),
        BotCommand(command='fumofumo', description='Get Fumo of the day based on day and user id. '),
        BotCommand(command='get_stickers_id', description='Get stickers file_id'),
        BotCommand(command='add_fumo', description='Add fumos to database'),
        BotCommand(command='cancel', description='Cancel any operations'),
        BotCommand(command='list_fumos', description='List fumos by name in db.'),
        BotCommand(command='update_fumo_cache', description='Manually update fumo db cache.'),
        BotCommand(command='download_fumo_images', description='Download fumo images.'),
        BotCommand(command='import_fumo_images', description='Import fumo images.'),
    ]
    private_chat_commands = [
        BotCommand(command='fumo', description='Get random fumo face ᗜᴗᗜ'),
        BotCommand(command='fumofumo', description='Get Fumo of the day based on day and user id. '),
        BotCommand(command='privacy', description='Get privacy policy'),
    ]
    group_chat_commands = [
        BotCommand(command='fumo', description='Get random fumo face ᗜᴗᗜ'),
        BotCommand(command='fumofumo', description='Get Fumo of the day based on day and user id. '),
    ]
    await bot.set_my_commands(admin_commands, BotCommandScopeChat(chat_id=Config.ADMIN_CHAT_ID))
    await bot.set_my_commands(private_chat_commands, BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(group_chat_commands, BotCommandScopeAllGroupChats())
