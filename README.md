# fumofumo_plush_bot
Silly telegram bot. Will welcome new users in the group and notify if someone has left. Users can propose posts to the channel with private messages.

[https://t.me/fumofumo_plush_bot](https://t.me/fumofumo_plush_bot)

[![Create and publish a Docker image](https://github.com/Fstream7/fumofumo_plush_bot/actions/workflows/deploy-image.yml/badge.svg?branch=main)](https://github.com/Fstream7/fumofumo_plush_bot/actions/workflows/deploy-image.yml)


## Used technology
* Python 3.11 with asyncio, data validation and typing
* aiogram 3.3 (Telegram Bot framework)
* Docker and Docker Compose (containerization)
* Github workflow linter and build

## environment variables

- `TELEGRAM_BOT_TOKEN=Your_token`
- `LOG_LEVEL=INFO` #loglevel
- `ADMIN_CHAT_ID=238637902` #To get ADMIN_CHAT_ID start bot and send him /id command*

#### messages located in file app/messages.yml and can be redefined using docker volume. user_full_name will be replaced with user full name
#### To get sticker id start bot and send him /get_stickers_id command from admin. 
#### To get images id start bot and send him /get_images_id command from admin. Images can be found at fumos_images dir. 
#### Most of the photos were taken from https://fumo.website/

## Run with docker in test mode
```
docker run -it --rm \
--env TELEGRAM_BOT_TOKEN="Your_token" \
--env ADMIN_CHAT_ID=238637902 \
ghcr.io/fstream7/fumofumo_plush_bot:main
```

## Run with docker in detach/daemon mode
```
docker run --detach --restart=always \
--env TELEGRAM_BOT_TOKEN="Your_token" \
--env ADMIN_CHAT_ID=238637902 \
--name fumofumo_plush_bot \
ghcr.io/fstream7/fumofumo_plush_bot:main
```
 Or clone repo and use python/docker compose


### Commands:
 * /id will return current chat id
 * /fumo will return random fumo face ᗜᴗᗜ
 * /fumofumo will return fumo of the day based on day and user id. 
### Admin commands:
 * /get_stickers_id FSM, will return given sticker id
 * /get_images_id FSM, will return given photo id
 * /cancel exit from FSM
