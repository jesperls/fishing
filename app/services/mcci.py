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
            if not data["data"] or data["data"]["playerByUsername"]:
                raise HTTPException(status_code=404, detail="Player not found")
            return data["data"]["playerByUsername"]
