from db.requests import FumoCache
from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot, Dispatcher
from pytz import timezone
from config import Config
from handlers.group_quiz import quiz_start


def setup_scheduler(session: AsyncSession, bot: Bot, dp: Dispatcher) -> AsyncIOScheduler:
    """
    Here we set up scheduler jobs to periodically run.
    update_fumo_ids_cache - daily update fumo cache. So adding new fumos would affect only on next day result.
    quiz_start - start quiz in provided chat. Run every 12 hours with maximum delay of 10 hour to make it more random.
    """
    scheduler = AsyncIOScheduler()
    scheduler.start()
    scheduler.add_job(
        FumoCache.update_fumo_ids_cache,
        CronTrigger(hour=0, minute=0, timezone=timezone(Config.TIMEZONE)),
        args=[session])
    if Config.QUIZ_CHAT_ID:
        scheduler.add_job(
            quiz_start,
            CronTrigger(hour="8,20", minute="0", timezone=timezone(Config.TIMEZONE)),
            args=[session, bot, dp, Config.QUIZ_CHAT_ID, 36000])
    return scheduler
