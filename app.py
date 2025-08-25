import os

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.request import EnergyRequest, PositionRequest
from models.response import DailyForecastResponse, SummaryResponse
from services.forecast import get_daily_forecast, get_summary
from services.open_meteo import request_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://solar-forecast-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/summary")
async def summary(position: PositionRequest = Depends()) -> SummaryResponse:

    latitude, longitude = position.latitude, position.longitude
    data = await request_data(latitude, longitude, daily="sunshine_duration,showers_sum", hourly="pressure_msl,temperature_2m")

    try:
        summary_data = get_summary(data)
    except KeyError as e:
        raise HTTPException(status_code=502, detail=f"Missing key in API data:{e}")

    return SummaryResponse(**summary_data)


@app.get("/dailyforecast")
async def daily_forecast(position: PositionRequest = Depends(), energy: EnergyRequest = Depends()) -> DailyForecastResponse:

    latitude, longitude = position.latitude, position.longitude
    data = await request_data(latitude, longitude, daily="weather_code,sunshine_duration,temperature_2m_min,temperature_2m_max")

    try:
        forecast_data = get_daily_forecast(data["daily"], power=energy.power, efficiency=energy.efficiency)
    except KeyError as e:
        raise HTTPException(status_code=502, detail=f"Missing key in API data:{e}")

    return DailyForecastResponse(**forecast_data)
