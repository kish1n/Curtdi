import requests
import disnake
from typing import Optional, Dict, Union


async def get_steam_id_from_discord_user(user_id: int, bot: disnake.Client) -> Optional[str]:
    user = await bot.fetch_user(user_id)
    connections = await user.fetch_connections()
    for connection in connections:
        if connection.type == 'steam':
            return connection.id
    return None


async def get_dota_rank(steam_id: str) -> Optional[Dict[str, Union[str, int]]]:
    response = requests.get(f"https://api.opendota.com/api/players/{steam_id}")
    if response.status_code != 200:
        return None

    data = response.json()
    mmr_estimate = data.get("mmr_estimate", {}).get("estimate", "N/A")
    solo_mmr = data.get("solo_competitive_rank", "N/A")
    party_mmr = data.get("competitive_rank", "N/A")

    return {
        "mmr_estimate": mmr_estimate,
        "solo_mmr": solo_mmr,
        "party_mmr": party_mmr
    }
