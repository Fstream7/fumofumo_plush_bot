# fumofumo_plush_bot
Silly tg bot 

# How to setup

- `git clone https://github.com/Fstream/fumofumo_plush_bot`
- `cd fumofumo_plush_bot`
- `cp app/config.example.yml app/config.yml`
- *Fill in all the vars. To get media file_id just start a bot and send him any messages you want*

# Start with local python:
```
pip3 install -U -r requirements.txt
python3 app/main.py
```

# Run with docker
```
docker run --detach -v=$(pwd)/app/config.yml:app/config.yml ghcr.io/fstream7/fumofumo_plush_bot:main
```