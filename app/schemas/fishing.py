from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict

class FishRecordBase(BaseModel):
    fish_data: Dict
    weights: List[Dict]

class StatisticBase(BaseModel):
    key: str
    value: int

class PlayerFishData(BaseModel):
    username: str
    uuid: str
    total_species: int
    total_catches: int
    last_updated: datetime
    fish_records: List[FishRecordBase]
    statistics: List[StatisticBase]
