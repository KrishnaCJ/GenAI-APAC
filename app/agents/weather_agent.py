from __future__ import annotations

from dataclasses import dataclass
from typing import List

from app.tools.weather_tools import get_weather_forecast


@dataclass
class WeatherSummary:
    location: str
    rainfall_mm_next_10d: float
    rain_risk: str
    daily_rain_prob: List[float]


class WeatherIntelligenceAgent:
    def analyze(self, location: str, month: int) -> WeatherSummary:
        forecast = get_weather_forecast(location=location, month=month, days=10)
        rainfall_mm_next_10d = sum(day["rain_mm"] for day in forecast)
        avg_rain_prob = sum(day["rain_prob"] for day in forecast) / len(forecast)
        rain_risk = "risky" if avg_rain_prob >= 0.5 else "safe"
        return WeatherSummary(
            location=location,
            rainfall_mm_next_10d=round(rainfall_mm_next_10d, 1),
            rain_risk=rain_risk,
            daily_rain_prob=[day["rain_prob"] for day in forecast],
        )
