from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from database.session import Base


class Player(Base):
    __tablename__ = "players"

    uuid = Column(String, primary_key=True)
    username = Column(String, index=True)
    last_updated = Column(DateTime)


class FishRecord(Base):
    __tablename__ = "fish_records"

    id = Column(Integer, primary_key=True)
    player_uuid = Column(String, ForeignKey("players.uuid"))
    fish_data = Column(JSON)
    weights = Column(JSON)
    last_caught = Column(DateTime)
