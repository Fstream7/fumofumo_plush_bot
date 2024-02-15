# fumofumo_plush_bot
Silly telegram bot 

# How to setup

- `git clone https://github.com/Fstream/fumofumo_plush_bot`
- `cd fumofumo_plush_bot`
- `cp .env.example .env`
- *Fill in all the vars. To get ADMIN_CHAT_ID start bot and send him /id command*
- *Optional - fill values in app/messages.py. To get sticker id start bot and send him any sticker from admin. user_full_name will be replaced with user full name*

# Start with local python:
```
pip3 install -U -r requirements.txt
cd app/
python3 main.py
```

# or run with docker
```
docker compose up
```