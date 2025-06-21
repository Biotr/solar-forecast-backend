from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import math


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_summary(data: dict) -> dict:
    hourly_pressure = data["hourly"]["pressure_msl"]
    average_pressure = round(sum(hourly_pressure) / len(hourly_pressure), 0)

    hourly_temperature = data["hourly"]["temperature_2m"]
    max_temperature = max(hourly_temperature)
    min_temperature = min(hourly_temperature)

    daily_sunshine = data["daily"]["sunshine_duration"]
    average_sunshine = math.floor(sum(daily_sunshine) / len(daily_sunshine))

    week_avg_temperature = sum(hourly_temperature) / len(hourly_temperature)
    if week_avg_temperature < 5:
        temperature_status = "Cold"
    elif week_avg_temperature < 10:
        temperature_status = "Cool"
    elif week_avg_temperature < 17:
        temperature_status = "Mild"
    elif week_avg_temperature < 25:
        temperature_status = "Warm"
    else:
        temperature_status = "Hot"

    week_showers = sum(data["daily"]["showers_sum"])
    if week_showers == 0:
        showers_status = "no rainfall"
    elif week_showers < 11:
        showers_status = "light rainfall"
    elif week_showers < 31:
        showers_status = "moderate rainfall"
    else:
        showers_status = "heavy rainfall"

    return {
        "average_pressure": average_pressure,
        "max_temperature": max_temperature,
        "min_temperature": min_temperature,
        "average_sunshine_duration": average_sunshine,
        "weather_status": f"{temperature_status}, {showers_status}",
    }


def get_daily_forecast(data: dict, *, power: float, efficiency: float) -> dict:

    daily_energy = []
    days = len(data["time"])
    for day in range(0, days):
        energy = power * data["sunshine_duration"][day] / 3600 * efficiency
        daily_energy.append(round(energy, 1))

    return {
        "time": data["time"],
        "weather_code": data["weather_code"],
        "min_temperature": data["temperature_2m_min"],
        "max_temperature": data["temperature_2m_max"],
        "energy": daily_energy,
    }


def request_data(url: str) -> dict:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except:
        raise HTTPException(status_code=502, detail=f"Error fetching data from external service")


@app.get("/summary")
def summary(latitude: float, longitude: float) -> dict:
    if not (-90 < latitude < 90) or not (-180 < longitude < 180):
        raise HTTPException(status_code=422, detail="Langitude or longitude not in range")

    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=sunshine_duration,showers_sum&hourly=pressure_msl,temperature_2m"
    data = request_data(url)
    try:
        summary_data = get_summary(data)
    except KeyError as e:
        raise HTTPException(status_code=502, detail=f"Missing key in API data:{e}")

    return summary_data


@app.get("/dailyforecast")
def daily_forecast(latitude: float, longitude: float, power: float, efficiency: float) -> dict:

    if not (-90 < latitude < 90) or not (-180 < longitude < 180):
        raise HTTPException(status_code=422, detail="Langitude or longitude not in range")

    if efficiency > 1 or efficiency < 0:
        raise HTTPException(status_code=422, detail="Efficiency not in range")

    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weather_code,sunshine_duration,temperature_2m_min,temperature_2m_max"
    data = request_data(url)

    try:
        weather_data = get_daily_forecast(data["daily"], power=power, efficiency=efficiency)
    except KeyError as e:
        raise HTTPException(status_code=502, detail=f"Missing key in API data:{e}")

    return weather_data
