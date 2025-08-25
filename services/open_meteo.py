import os

import httpx
from fastapi import HTTPException


async def request_data(latitude: float, longitude: float, daily: str = "", hourly="") -> dict:
    open_meteo_url = os.getenv("METEO_API_URL")

    daily = "&daily=" + daily if daily else ""
    hourly = "&hourly=" + hourly if hourly else ""
    url = f"{open_meteo_url}?latitude={latitude}&longitude={longitude}{daily}{hourly}"

    try:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error fetching data from external service. {e}")
