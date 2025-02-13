from sqlalchemy.orm import Session
from models.fishing import Player, FishRecord
from datetime import datetime, timedelta
from config.settings import Settings


class FishingCRUD:
    def __init__(self, db: Session):
        self.settings = Settings()
        self.db = db

    def get_player(self, username: str):
        return self.db.query(Player).filter(Player.username == username).first()

    def get_fish_records(self, player_uuid: str):
        return (
            self.db.query(FishRecord)
            .filter(FishRecord.player_uuid == player_uuid)
            .all()
        )

    def cache_player_data(self, username: str, data: dict):
        # Update or create player record
        player = self.get_player(username)
        now = datetime.now()

        if not player:
            player = Player(uuid=data["uuid"], username=username, last_updated=now)
            self.db.add(player)
        else:
            player.last_updated = now

        # Update fish records
        self.db.query(FishRecord).filter(FishRecord.player_uuid == player.uuid).delete()

        for record in data["collections"]["fish"]:
            fish_record = FishRecord(
                player_uuid=player.uuid,
                fish_data=record["fish"],
                weights=record["weights"],
                last_caught=datetime.now(),
            )
            self.db.add(fish_record)

        self.db.commit()
        return player

    def is_cache_valid(self, username: str):
        player = self.get_player(username)
        if not player:
            return False
        return (datetime.now() - player.last_updated).seconds < self.settings.CACHE_TTL
