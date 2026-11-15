from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import logging
from web.routers import router
from config import Config

logging.basicConfig(level=Config.LOG_LEVEL)
app = FastAPI()
app.mount("/static", StaticFiles(directory="web/static"), name="static")
app.mount("/media", StaticFiles(directory="media/photos"), name="media")
app.include_router(router)
