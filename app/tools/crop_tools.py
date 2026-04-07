from __future__ import annotations

from typing import Dict, List, Tuple


CROP_DB: Dict[str, Dict[str, List[str]]] = {
    "kharif": {
        "loamy": ["rice", "maize", "cotton"],
        "sandy": ["millet", "groundnut", "pigeon pea"],
        "clay": ["rice", "sugarcane", "soybean"],
    },
    "rabi": {
        "loamy": ["wheat", "mustard", "chickpea"],
        "sandy": ["barley", "mustard", "lentil"],
        "clay": ["wheat", "linseed", "pea"],
    },
    "zaid": {
        "loamy": ["watermelon", "cucumber", "fodder maize"],
        "sandy": ["watermelon", "muskmelon", "sesame"],
        "clay": ["fodder maize", "sunflower", "okra"],
    },
}

WATER_NEED = {
    "rice": "high",
    "sugarcane": "high",
    "cotton": "medium",
    "maize": "medium",
    "soybean": "medium",
    "wheat": "medium",
    "barley": "low",
    "millet": "low",
    "groundnut": "low",
    "pigeon pea": "low",
    "mustard": "low",
    "chickpea": "low",
    "lentil": "low",
    "linseed": "low",
    "pea": "low",
    "watermelon": "medium",
    "muskmelon": "medium",
    "cucumber": "medium",
    "sesame": "low",
    "sunflower": "low",
    "okra": "medium",
    "fodder maize": "medium",
}


def season_from_month(month: int) -> str:
    if month in (6, 7, 8, 9):
        return "kharif"
    if month in (10, 11, 12, 1, 2):
        return "rabi"
    return "zaid"


def crop_water_need(crop: str) -> str:
    return WATER_NEED.get(crop, "medium")


def get_top_crops(location: str, month: int, soil: str) -> Tuple[List[str], List[str]]:
    season = season_from_month(month)
    soil_key = soil.lower().strip()
    candidates = CROP_DB.get(season, {}).get(soil_key, [])

    if not candidates:
        return [], [
            f"No crops mapped for soil '{soil}' in {season} season.",
            "Try loamy, sandy, or clay as soil type.",
        ]

    top = candidates[:3]
    reasons = [
        f"Season: {season} based on month {month}.",
        f"Soil match: {soil_key}.",
    ]
    return top, reasons
