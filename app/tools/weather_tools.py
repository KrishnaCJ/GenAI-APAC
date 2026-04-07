from __future__ import annotations

from typing import Dict, List


def _seasonal_rain_profile(month: int) -> float:
    if month in (6, 7, 8, 9):
        return 0.6
    if month in (10, 11):
        return 0.35
    if month in (12, 1, 2):
        return 0.2
    return 0.25


def _mock_forecast(month: int, days: int) -> List[Dict[str, float]]:
    base_prob = _seasonal_rain_profile(month)
    forecast = []
    for i in range(days):
        rain_prob = min(0.9, max(0.05, base_prob + (0.05 if i % 3 == 0 else -0.03)))
        rain_mm = round(rain_prob * 8, 1)
        forecast.append({"rain_prob": rain_prob, "rain_mm": rain_mm})
    return forecast


def get_weather_forecast(location: str, month: int, days: int) -> List[Dict[str, float]]:
    base = _mock_forecast(month=month, days=days)
    location_bias = (sum(ord(ch) for ch in location.lower()) % 7) - 3
    adjusted = []
    for day in base:
        rain_prob = min(0.9, max(0.05, day["rain_prob"] + (location_bias * 0.01)))
        rain_mm = round(rain_prob * 8, 1)
        adjusted.append({"rain_prob": rain_prob, "rain_mm": rain_mm})
    return adjusted
