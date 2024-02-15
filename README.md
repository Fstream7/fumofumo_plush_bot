# fumofumo_plush_bot
Silly telegram bot. Will welcome new users in the group and notify if someone has left. Users can propose posts to the channel with private messages.

## environment variables

- `TELEGRAM_BOT_TOKEN=Your_token`
- `LOG_LEVEL=INFO` #loglevel
- `ADMIN_CHAT_ID=238637902` #To get ADMIN_CHAT_ID start bot and send him /id command*

#### messages located in file app/messages.yml and can be redefined using docker volume. user_full_name will be replaced with user full name
#### To get sticker id start bot and send him /get_stickers_id command from admin. 

### Run with docker in test mode
```
docker run -it --rm \
--env TELEGRAM_BOT_TOKEN="Your_token" \
--env ADMIN_CHAT_ID=238637902 \
ghcr.io/fstream7/fumofumo_plush_bot:main
```

### Run with docker in detach/daemon mode
```
docker run --detach --restart=always \
--env TELEGRAM_BOT_TOKEN="Your_token" \
--env ADMIN_CHAT_ID=238637902 \
--name fumofumo_plush_bot \
ghcr.io/fstream7/fumofumo_plush_bot:main
```
 Or clone repo and use python/docker compose