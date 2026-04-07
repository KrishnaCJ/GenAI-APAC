from __future__ import annotations

from dataclasses import asdict
from typing import Dict

from app.agents.crop_advisor_agent import CropAdvisorAgent
from app.agents.decision_agent import DecisionAgent
from app.agents.monetization_agent import MonetizationAgent
from app.agents.weather_agent import WeatherIntelligenceAgent


class Orchestrator:
    def __init__(self) -> None:
        self.crop_agent = CropAdvisorAgent()
        self.weather_agent = WeatherIntelligenceAgent()
        self.decision_agent = DecisionAgent()
        self.monetization_agent = MonetizationAgent()

    def run(self, location: str, month: int, soil: str) -> Dict:
        crop_result = self.crop_agent.recommend(location=location, month=month, soil=soil)
        weather_result = self.weather_agent.analyze(location=location, month=month)
        decision = self.decision_agent.decide(crops=crop_result.crops, rain_risk=weather_result.rain_risk)
        monetization = self.monetization_agent.evaluate(
            location=location,
            month=month,
            crops=crop_result.crops,
        )

        return {
            "crop_advisor": asdict(crop_result),
            "weather": asdict(weather_result),
            "decision": asdict(decision),
            "monetization": asdict(monetization),
        }
