from __future__ import annotations

from dataclasses import dataclass
from typing import List

from app.tools.crop_tools import crop_water_need


@dataclass
class Decision:
    recommendation: str
    reasoning: List[str]


class DecisionAgent:
    def decide(self, crops: List[str], rain_risk: str) -> Decision:
        if not crops:
            return Decision(
                recommendation="No strong crop match found. Try nearby district or adjust soil info.",
                reasoning=["No crop candidates from rules."],
            )

        water_hungry = [c for c in crops if crop_water_need(c) == "high"]
        drought_tolerant = [c for c in crops if crop_water_need(c) == "low"]

        if rain_risk == "risky" and drought_tolerant:
            pick = drought_tolerant[0]
            return Decision(
                recommendation=f"Based on higher rain risk, prefer {pick} over water-hungry crops.",
                reasoning=[
                    "Rain risk is elevated in the next 10 days.",
                    f"{pick} is more drought tolerant and safer in uncertain rainfall.",
                ],
            )

        pick = crops[0]
        return Decision(
            recommendation=f"Conditions look safe. Recommended crop: {pick}.",
            reasoning=[
                "Rain risk is manageable.",
                f"{pick} matches the season and soil profile.",
            ],
        )
