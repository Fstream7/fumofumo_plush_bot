import logging
import re
from config import Messages
from curl_cffi import requests
from aiogram import Router, types
from filters.chat_type import ChatTypeFilter
from filters.admin import AdminFilter
from aiogram.filters import invert_f


router = Router()

router.message.filter(ChatTypeFilter(chat_type=["group", "supergroup"]), invert_f(AdminFilter()))


@router.message()
async def block_nft_spam(message: types.Message) -> None:
    """
    Delete any message contain link with NFT
    #todo make a list of such sites, to not parse them each time
    """
    if message.text:
        text = message.text
    elif message.caption:
        text = message.caption
    if sites := re.findall(r"https?://(?:www\.)?[\w\-]+\.io(?:/[\w\-./?%&=]*)?", text, re.IGNORECASE):
        headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/75.0.3770.100 Safari/537.36'
            )
        }
        for site in sites:
            logging.info(f"Checking site {site}")
            try:
                response = requests.get(site, headers=headers, timeout=10)
                response.raise_for_status()
                text_content = response.text.lower()
                if 'nft' in text_content:
                    await message.reply(Messages.nft_ban_message.format(user_full_name=message.from_user.full_name))
                    await message.delete()
                    break
            except requests.exceptions.RequestException as e:
                logging.error(f"Error accessing {site}: {e}")
                continue
