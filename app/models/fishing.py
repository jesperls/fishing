from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database.session import Base


class Player(Base):
    __tablename__ = "players"

    uuid = Column(String, primary_key=True)
    username = Column(String, index=True)
    last_updated = Column(DateTime)

    fish_records = relationship("FishRecord", back_populates="player")
    statistics = relationship("Statistic", back_populates="player")


class FishRecord(Base):
    __tablename__ = "fish_records"

    id = Column(Integer, primary_key=True)
    player_uuid = Column(String, ForeignKey("players.uuid"))
    fish_data = Column(JSON)
    weights = Column(JSON)
    last_caught = Column(DateTime)

    player = relationship("Player", back_populates="fish_records")


class Statistic(Base):
    __tablename__ = "statistics"

    id = Column(Integer, primary_key=True)
    player_uuid = Column(String, ForeignKey("players.uuid"), index=True)
    key = Column(String, index=True, autoincrement=True)
    value = Column(Integer)

    player = relationship("Player", back_populates="statistics")
