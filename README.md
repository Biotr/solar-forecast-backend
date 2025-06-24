Solar Forecast API - its backend application mainly created for [solar-forecast-frontend](https://github.com/Biotr/solar-forecast-frontend). 
This backend provides weather and solar energy forecast data using the Open-Meteo API.
Built with FastAPI, it exposes two endpoints for use.

Base URL:
`https://solar-forecast-backend-91fr.onrender.com/`

Endpoints: <br/>
`/summary` - returns a 7-day weather overview for a given location.
Parameters:
| Name      | Type  | Range       |
| --------- | ----- | ----------- |
| latitude  | float | -90 to 90   |
| longitude | float | -180 to 180 |

Output:
| Name      | Type  |
| --------- | ----- |
| average_pressure |  int  |
| max_temperature | float |
| min_temperature |  float  |
| average_sunshine_duration | int |
| weather_status | str |

Example:
`https://solar-forecast-backend-91fr.onrender.com/summary?latitude=52.20&longitude=13.20`

Response:
```json
{
  "average_pressure": 1013,
  "max_temperature": 24.3,
  "min_temperature": 10.1,
  "average_sunshine_duration": 312,
  "weather_status": "Warm, light rainfall"
}
```
---

`/dailyforecast` - returns a 7-day forecast including min,max temperature and estimated solar energy production.
Energy is estimated as:
`energy = power × sunshine_duration (seconds) / 3600 × efficiency`

Parameters:
| Name      | Type  | Range       |
| --------- | ----- | ----------- |
| latitude  | float | -90 to 90   |
| longitude | float | -180 to 180 |
| efficiency  | float | 0 to 1   |
| power | float | 0> |

Output:
| Name      | Type  |
| --------- | ----- |
| time  | List[str] |
| weather_code | List[int] |
| min_temperature  | List[float] |
| max_temperature | List[float] |
| energy | List[float] |

Example:
`https://solar-forecast-backend-91fr.onrender.com/dailyforecast?latitude=32&longitude=12&power=2.5&efficiency=0.2`

Response:
```json
{
  "time": [
    "2025-06-22",
    "2025-06-23",
    "2025-06-24",
    "2025-06-25",
    "2025-06-26",
    "2025-06-27",
    "2025-06-28"
  ],
  "weather_code": [2, 1, 0, 0, 0, 0, 1],
  "min_temperature": [20.7, 21.6, 22.7, 24.4, 26, 24, 21.6],
  "max_temperature": [31.9, 33.5, 34.3, 36, 37.9, 35.8, 32.1],
  "energy": [6.5, 6.5, 6.5, 6.5, 6.7, 6.7, 6.7]
}
```

### ToDo
- implement power greater than zero, less than (?)
- change parameters validation with FastAPI Query


(not enough time)
