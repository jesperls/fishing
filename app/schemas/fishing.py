from pydantic import BaseModel
from datetime import datetime


class FishRecordBase(BaseModel):
    fish_data: dict
    weights: list[dict]


class PlayerFishData(BaseModel):
    username: str
    uuid: str
    total_species: int
    total_catches: int
    last_updated: datetime
    fish_records: list[FishRecordBase]
