from aiogram import Router, types
from filters.chat_type import ChatTypeFilter
from config import Messages
import re
router = Router()


@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]))
async def ban_spammers(message: types.Message) -> None:
    if message.text:
        text = message.text
    elif message.caption:
        text = message.caption
    for regex in Messages.ban_regexs:
        if re.search(r"" + regex, text, re.IGNORECASE):
            try:
                if await message.chat.ban(user_id=message.from_user.id, revoke_messages=False):
                    await message.reply(Messages.ban_message.format(
                        user_full_name=message.from_user.full_name,
                        ban_reason=re.escape(regex)))
                await message.delete()
            except Exception as err:
                await message.answer(str(err))
