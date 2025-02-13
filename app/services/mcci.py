import httpx
from config import settings
from fastapi import HTTPException


class MCCIService:
    def __init__(self):
        self.settings = settings.Settings()
        self.headers = {
            "X-API-Key": self.settings.MCCI_API_KEY,
            "User-Agent": self.settings.USER_AGENT,
            "Content-Type": "application/json",
        }

    async def get_player_fishing_data(self, username: str):
        query = """
        query GetPlayerFishingData($username: String!) {
            playerByUsername(username: $username) {
                uuid
                username
                collections {
                    fish {
                        fish {
                            name
                            rarity
                            climate
                            collection
                            catchTime
                            elusive
                        }
                        weights {
                            weight
                            firstCaught
                        }
                    }
                }
                statistics {
                    commonFish: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_fish_common")
                    uncommonFish: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_fish_uncommon")
                    rareFish: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_fish_rare")
                    epicFish: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_fish_epic")
                    legendaryFish: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_fish_legendary")
                    mythicFish: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_fish_mythic")
                    averageFish: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_fish_average")
                    largeFish: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_fish_large")
                    massiveFish: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_fish_massive")
                    gargantuanFish: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_fish_gargantuan")
                    pearl1: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_pearl_1")
                    pearl2: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_pearl_2")
                    pearl3: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_pearl_3")
                    spiritSpirit: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_spirit_spirit")
                    spiritRefined: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_spirit_refined")
                    spiritPure: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_spirit_pure")
                    treasureCommon: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_treasure_common")
                    treasureUncommon: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_treasure_uncommon")
                    treasureRare: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_treasure_rare")
                    treasureEpic: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_treasure_epic")
                    treasureLegendary: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_treasure_legendary")
                    treasureMythic: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_treasure_mythic")
                    trashCommon: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_trash_common")
                    trashUncommon: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_trash_uncommon")
                    trashRare: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_trash_rare")
                    trashEpic: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_trash_epic")
                    trashLegendary: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_trash_legendary")
                    fish: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_fish")
                    trash: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_trash")
                    pearl: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_pearl")
                    treasure: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_treasure")
                    spirit: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_spirit")
                    any: rotationValue(rotation: LIFETIME, statisticKey: "fishing_catch_caught_any")
                    trophies: rotationValue(rotation: LIFETIME, statisticKey: "trophies_fishing")
                }
            }
        }
        """

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.settings.MCCI_API_URL,
                json={"query": query, "variables": {"username": username}},
                headers=self.headers,
            )

            for header, value in response.headers.items():
                if "x-ratelimit-remaining" in header.lower():
                    print(f"{header}: {value}")

            if response.status_code != 200:
                raise HTTPException(status_code=502, detail="API service unavailable")

            data = response.json()
            if errors := data.get("errors"):
                raise HTTPException(status_code=400, detail=errors[0]["message"])
            if not "playerByUsername" in data["data"]:
                raise HTTPException(status_code=404, detail="Player not found")
            return data["data"]["playerByUsername"]
