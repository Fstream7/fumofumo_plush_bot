# fumofumo_plush_bot
Silly telegram bot. Will welcome new users in the group and notify if someone has left. Users can propose posts to the channel with private messages.

[https://t.me/fumofumo_plush_bot](https://t.me/fumofumo_plush_bot)

[![Create and publish a Docker image](https://github.com/Fstream7/fumofumo_plush_bot/actions/workflows/deploy-image.yml/badge.svg?branch=main)](https://github.com/Fstream7/fumofumo_plush_bot/actions/workflows/deploy-image.yml)


## Used technologies
* Python 3.11 with asyncio, data validation and typing
* aiogram 3
* sqlalchemy asyncio wth SQLite for development or Postgres for production
* Docker and Docker Compose
* GitHub  workflow linter and build

## environment variables
### required:
- `TELEGRAM_BOT_TOKEN=Your_token`
### optional:
- `LOG_LEVEL=INFO` loglevel
- `ADMIN_CHAT_ID=238637902` To get ADMIN_CHAT_ID start bot and send him */id* command
### env for postgres (if they are not specified, then sqlite will be used):
- `POSTGRES_HOST` postgress db host
- `POSTGRES_PORT`  postgress db port
- `POSTGRES_DB` postgress db name
- `POSTGRES_USER` postgress db user
- `POSTGRES_PASSWORD` postgress db password

#### messages located in file app/messages.yml and can be redefined using docker volume. user_full_name will be replaced with user full name
#### To get sticker id start bot and send him /get_stickers_id command from admin. 
#### To add fumos to db start bot and send him /add_fumos command from admin. Send fumo images with names. Telegram allows sharing  stickers between bots, but each bot has a unique file_id for other media, so you have to re-upload them. 

## Run container
```bash
docker run -it --rm \
--env TELEGRAM_BOT_TOKEN="Your_token" \
--env ADMIN_CHAT_ID=238637902 \
ghcr.io/fstream7/fumofumo_plush_bot:main
```

## Run container in detach/daemon mode
```bash
docker run --detach --restart=always \
--env TELEGRAM_BOT_TOKEN="Your_token" \
--env ADMIN_CHAT_ID=238637902 \
--name fumofumo_plush_bot \
ghcr.io/fstream7/fumofumo_plush_bot:main
```

## Installation
1. Clone repo:
```bash
git clone git@github.com:Fstream7/fumofumo_plush_bot.git
```
2. Add env:
```bash
export TELEGRAM_BOT_TOKEN="Your_token"
export ADMIN_CHAT_ID=238637902
```
3. Run with local python
```bash
pip3 install requirements.txt
cd app/
alembic upgrade head
python main.py
```
Or with docker compose
```bash
# for development, with sqlite
docker compose -f docker-compose-dev.yml up
# for production, with postgres
docker compose -f docker-compose.yml up -d 
```

### Commands:
 * /id will return current chat id
 * /fumo will return random fumo face ᗜᴗᗜ
 * /fumofumo will return fumo of the day based on day and user id. 
### Admin commands:
 * /get_stickers_id FSM, will return given sticker id
 * /add_fumo FSM for adding fumos to db
 * /cancel exit from FSM
 * /list_fumos list fumos by name in db.