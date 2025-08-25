from pydantic import BaseModel, Field


class PositionRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class EnergyRequest(BaseModel):
    power: float = Field(..., gt=0)
    efficiency: float = Field(..., gt=0, le=1)
