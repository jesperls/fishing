from apscheduler.schedulers.asyncio import AsyncIOScheduler
from models.fishing import Player
from database.session import get_db
from crud.fishing import FishingCRUD
from services.mcci import MCCIService

scheduler = AsyncIOScheduler()


async def refresh_popular_players():
    """Background task to refresh top players periodically"""
    db = next(get_db())
    crud = FishingCRUD(db)
    mcci_service = MCCIService()

    players = db.query(Player).order_by(Player.last_updated.desc()).limit(5).all()

    for player in players:
        try:
            data = await mcci_service.get_player_fishing_data(player.username)
            crud.cache_player_data(player.username, data)
        except Exception as e:
            pass


def setup_scheduler():
    scheduler.add_job(refresh_popular_players, "cron", hour=3, timezone="UTC")
    scheduler.start()
