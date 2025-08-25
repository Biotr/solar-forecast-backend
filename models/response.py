from typing import List

from pydantic import BaseModel


class SummaryResponse(BaseModel):
    average_pressure: int
    max_temperature: float
    min_temperature: float
    average_sunshine_duration: int
    weather_status: str


class DailyForecastResponse(BaseModel):
    time: List[str]
    weather_code: List[int]
    min_temperature: List[float]
    max_temperature: List[float]
    energy: List[float]
