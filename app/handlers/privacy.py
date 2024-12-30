from aiogram.filters import Command
from aiogram import Router, types

router = Router()


@router.message(Command("privacy"))
async def privacy(message: types.Message) -> None:
    privacy = """Privacy Policy
By sending messages to this bot in private chat, you agree to the following privacy policy
It can be viewed at any time by using the `/privacy` command in private chat with the bot.

Data Collection
Fumobot don't collect or save any received data.
All received messages in direct chat wih bot are forwarding to bot administrator and can be posted publicly
This data is only stored on Telegram servers, bot don't store them. Bot also sends your name and login for feedback.
If you do not want your account to be viewed on forwarding to channel, disable link for forwarding in
Telegram privacy settings or write in the message that you want to remain anonymous.
For /fumofumo command fumobot will get your user_id in Telegram for processing.


Contact
If you have any questions or concerns about this privacy policy, please contact the bot owner directly.
    """
    await message.reply(privacy)
