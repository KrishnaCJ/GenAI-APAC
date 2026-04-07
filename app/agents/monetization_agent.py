from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from app.tools.market_tools import get_profit_insights


@dataclass
class MonetizationInsight:
    options: List[Dict[str, object]]
    best_option: Dict[str, object] | None


class MonetizationAgent:
    def evaluate(self, location: str, month: int, crops: List[str]) -> MonetizationInsight:
        options = get_profit_insights(location=location, month=month, crops=crops)
        best = max(options, key=lambda item: item["expected_profit_inr"], default=None)
        return MonetizationInsight(options=options, best_option=best)
