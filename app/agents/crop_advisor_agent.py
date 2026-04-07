from __future__ import annotations

from dataclasses import dataclass
from typing import List

from app.tools.crop_tools import get_top_crops


@dataclass
class CropRecommendation:
    crops: List[str]
    reasons: List[str]


class CropAdvisorAgent:
    def recommend(self, location: str, month: int, soil: str) -> CropRecommendation:
        crops, reasons = get_top_crops(location=location, month=month, soil=soil)
        return CropRecommendation(crops=crops, reasons=reasons)
