from db.requests import FumoCache
from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
from config import Config


def setup_scheduler(session: AsyncSession):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        FumoCache.update_fumo_ids_cache,
        CronTrigger(hour=0, minute=0, timezone=timezone(Config.TIMEZONE)),
        args=[session])
    scheduler.start()
    return scheduler
