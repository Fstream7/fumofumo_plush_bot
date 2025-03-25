from db.requests import FumoCache
from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot, Dispatcher
from pytz import timezone
from config import Config
from handlers.quiz import quiz_start


def setup_scheduler(session: AsyncSession, bot: Bot, dp: Dispatcher):
    """
    Here we set up scheduler jobs to periodically run.
    update_fumo_ids_cache - daily update fumo cache. So adding new fumos would affect only on next day result.
    quiz_start - start quiz in provided chat. Run every 2 hours with maximum delay of 1 hour to make it more random.
    """
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        FumoCache.update_fumo_ids_cache,
        CronTrigger(hour=0, minute=0, timezone=timezone(Config.TIMEZONE)),
        args=[session])
    if Config.QUIZ_CHAT_ID:
        scheduler.add_job(
            quiz_start,
            'interval',
            seconds=7200,
            args=[session, bot, dp, Config.QUIZ_CHAT_ID, 3600])
    scheduler.start()
    return scheduler
