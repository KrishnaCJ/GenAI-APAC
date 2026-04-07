from __future__ import annotations

import os
from typing import Dict

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.orchestrator import Orchestrator

load_dotenv()
app = FastAPI(title="Farm Guide Agent", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = Orchestrator()


class RecommendRequest(BaseModel):
    location: str = Field(..., min_length=2)
    month: int = Field(..., ge=1, le=12)
    soil: str = Field(..., min_length=3)


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "model": os.getenv("MODEL_NAME", "rules")}


@app.post("/api/recommend")
def recommend(payload: RecommendRequest) -> Dict:
    result = orchestrator.run(
        location=payload.location,
        month=payload.month,
        soil=payload.soil,
    )
    today_advice = _today_advice(result)
    return {"result": result, "today_advice": today_advice}


def _today_advice(result: Dict) -> str:
    rain_risk = result["weather"]["rain_risk"]
    if rain_risk == "risky":
        return "Today: Avoid sowing water-heavy crops. Keep soil dry and monitor rain."
    return "Today: Good day for sowing. Low rain expected in the next few days."
