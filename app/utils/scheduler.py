from db.requests import update_fumo_ids_cache
from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


def setup_scheduler(session: AsyncSession):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(update_fumo_ids_cache, CronTrigger(hour=0, minute=0), args=[session])
    scheduler.start()
    return scheduler
