from __future__ import annotations

from typing import Dict, List


PRICE_PER_QUINTAL: Dict[str, int] = {
    "rice": 2400,
    "maize": 2100,
    "cotton": 6200,
    "millet": 2500,
    "groundnut": 5500,
    "pigeon pea": 7000,
    "sugarcane": 350,
    "soybean": 4800,
    "wheat": 2300,
    "mustard": 5600,
    "chickpea": 5400,
    "barley": 1900,
    "lentil": 6200,
    "linseed": 6200,
    "pea": 4800,
    "watermelon": 1200,
    "cucumber": 1600,
    "muskmelon": 1400,
    "sesame": 8000,
    "sunflower": 5200,
    "okra": 3000,
    "fodder maize": 1500,
}

YIELD_PER_ACRE_QTL: Dict[str, float] = {
    "rice": 22.0,
    "maize": 18.0,
    "cotton": 8.5,
    "millet": 10.0,
    "groundnut": 9.0,
    "pigeon pea": 6.0,
    "sugarcane": 380.0,
    "soybean": 10.0,
    "wheat": 18.0,
    "mustard": 7.0,
    "chickpea": 7.5,
    "barley": 16.0,
    "lentil": 5.5,
    "linseed": 5.0,
    "pea": 6.0,
    "watermelon": 90.0,
    "cucumber": 80.0,
    "muskmelon": 70.0,
    "sesame": 4.5,
    "sunflower": 7.0,
    "okra": 40.0,
    "fodder maize": 120.0,
}

TREND_MULTIPLIER = {
    "up": 1.08,
    "flat": 1.0,
    "down": 0.92,
}


def _trend_for_crop(location: str, crop: str) -> str:
    seed = sum(ord(ch) for ch in f"{location.lower()}-{crop}")
    idx = seed % 3
    return ["up", "flat", "down"][idx]


def estimate_profit(location: str, crop: str, month: int) -> Dict[str, object]:
    base_price = PRICE_PER_QUINTAL.get(crop, 2000)
    base_yield = YIELD_PER_ACRE_QTL.get(crop, 8.0)
    seasonal_factor = 1.05 if month in (6, 7, 8, 9) else 1.0

    trend = _trend_for_crop(location, crop)
    price = base_price * TREND_MULTIPLIER[trend]
    profit = base_yield * price * seasonal_factor

    return {
        "crop": crop,
        "expected_profit_inr": int(round(profit, 0)),
        "trend": trend,
    }


def get_profit_insights(location: str, month: int, crops: List[str]) -> List[Dict[str, object]]:
    return [estimate_profit(location, crop, month) for crop in crops]
