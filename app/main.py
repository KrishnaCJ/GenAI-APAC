from __future__ import annotations

import os
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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
    try:
        result = orchestrator.run(
            location=payload.location,
            month=payload.month,
            soil=payload.soil,
        )
        today_advice = _today_advice(result)
        return {"result": result, "today_advice": today_advice}
    except Exception as e:
        import traceback
        print(f"Error in orchestrator: {traceback.format_exc()}")
        return {"error": f"Failed to generate recommendation: {str(e)}"}


def _today_advice(result: Dict) -> str:
    rain_risk = result["weather"]["rain_risk"]
    if rain_risk == "risky":
        return "Today: Avoid sowing water-heavy crops. Keep soil dry and monitor rain."
    return "Today: Good day for sowing. Low rain expected in the next few days."


# Serve static frontend files with SPA fallback
frontend_path = Path(__file__).parent.parent / "frontend"

if not frontend_path.exists():
    print(f"WARNING: Frontend directory not found at {frontend_path}")
else:
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """Serve frontend files with SPA fallback to index.html"""
        # Prevent directory traversal attacks
        if ".." in full_path or full_path.startswith("/"):
            return {"error": "Invalid path"}, 400
        
        # Try to serve the actual file first
        file_path = frontend_path / full_path
        file_path = file_path.resolve()
        frontend_path_resolved = frontend_path.resolve()
        
        # Security check: ensure the file is within the frontend directory
        try:
            file_path.relative_to(frontend_path_resolved)
        except ValueError:
            # Path is outside frontend directory, deny access
            pass
        else:
            # Path is valid and within directory
            if file_path.is_file():
                return FileResponse(file_path)
        
        # Fallback to index.html for client-side routing
        index_file = frontend_path_resolved / "index.html"
        if index_file.is_file():
            return FileResponse(index_file, media_type="text/html")
        
        return {"error": "Frontend not found"}, 404
