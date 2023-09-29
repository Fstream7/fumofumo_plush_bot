# fumofumo_plush_bot
Silly telegram bot 

# How to setup

- `git clone https://github.com/Fstream/fumofumo_plush_bot`
- `cd fumofumo_plush_bot`
- `cp .env.example .env`
- *Fill in all the vars.

# Start with local python:
```
Create postgres database and fill all data
pip3 install -U -r requirements.txt
python3 app/main.py
```

# Run with docker
```
docker compose up
```