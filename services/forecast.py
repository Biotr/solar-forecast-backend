import math


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
