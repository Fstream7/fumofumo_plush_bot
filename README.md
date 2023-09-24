# fumofumo_plush_bot
Silly tg bot 

# How to setup

- `git clone https://github.com/Fstream/fumofumo_plush_bot`
- `cd fumofumo_plush_bot`
- `cp app/.env_example app/.env`
- *Fill in all the vars*

# Start with local python:
```
pip3 install -U -r requirements.txt
python3 app/main.py
```

# Run with docker
```
docker run --detach -v=$(pwd)/.env:/app/.env ghcr.io/fstream7/fumofumo_plush_bot:main
```