from fastapi import APIRouter, Depends, HTTPException
from database.session import get_db
from schemas.fishing import PlayerFishData
from services.mcci import MCCIService
from crud.fishing import FishingCRUD
from datetime import datetime
from models.fishing import Player

router = APIRouter()


@router.get("/api/fishing/{username}", response_model=PlayerFishData)
async def get_fishing_data(
    username: str, db=Depends(get_db), mcci_service: MCCIService = Depends()
):
    crud = FishingCRUD(db)

    # Check cache first
    if crud.is_cache_valid(username):
        return _build_response_from_cache(crud, username)

    # Fetch fresh data
    try:
        data = await mcci_service.get_player_fishing_data(username)
        player = crud.cache_player_data(username, data)
        return _build_response(data, player)
    except HTTPException as e:
        if cached_data := crud.get_player(username):
            return _build_response_from_cache(crud, username)
        raise e


def _build_response_from_cache(crud: FishingCRUD, username: str):
    player = crud.get_player(username)
    records = crud.get_fish_records(player.uuid)

    return PlayerFishData(
        username=player.username,
        uuid=player.uuid,
        total_species=sum(1 for r in records if r.weights),
        total_catches=sum(len(r.weights) for r in records),
        last_updated=player.last_updated,
        fish_records=[
            {
                "fish_data": r.fish_data,
                "weights": r.weights,
            }
            for r in records
        ],
    )


def _build_response(raw_data: dict, player: Player):
    collections = raw_data.get("collections", {})
    fish_records = collections.get("fish", [])

    return PlayerFishData(
        username=player.username,
        uuid=player.uuid,
        total_species=sum(1 for record in fish_records if record["weights"]),
        total_catches=sum(len(record["weights"]) for record in fish_records),
        last_updated=datetime.now(),
        fish_records=[
            {
                "fish_data": record["fish"],
                "weights": record["weights"],
            }
            for record in fish_records
        ],
    )
