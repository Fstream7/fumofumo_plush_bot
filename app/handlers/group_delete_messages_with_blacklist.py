from config import Messages
from aiogram import Router, types
from filters.chat_type import ChatTypeFilter
from aiogram.exceptions import TelegramBadRequest


router = Router()
router.message.filter(ChatTypeFilter(chat_type=["group", "supergroup"]))


@router.message()
async def group_delete_messages_with_blacklist(message: types.Message) -> None:
    if message.text:
        text = message.text
    elif message.caption:
        text = message.caption
    else:
        return None
    for word in Messages.blacklist_words:
        if word in text:
            try:
                await message.delete()
            except TelegramBadRequest as err:
                await message.reply(
                    f"Cannot delete message containing with blacklisted word, check bot admin rights. {str(err)}"
                )
                break
            await message.answer(Messages.blacklist_ban_message.format(user_full_name=message.from_user.full_name))
            break
