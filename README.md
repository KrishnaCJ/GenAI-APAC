# Farm Guide Agent

A compact multi-agent farming guide designed for the GenAI Asia Pacific hackathon. It includes:

- Crop Advisor Agent: maps season + soil to best crops.
- Weather Intelligence Agent: provides rain risk and a safe/risky signal (mocked data).
- Decision Agent: merges the above into a final recommendation.
- Voice input and a "Today" advice card in the frontend.

## Project Structure

```
farm-guide-agent/
├── app/
│   ├── agents/
│   ├── tools/
│   ├── orchestrator.py
│   └── main.py
├── frontend/
├── Dockerfile
├── deploy.sh
├── requirements.txt
└── README.md
```

## Local Run

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

Open the frontend by serving the files in `frontend/` using any static server.

## Deploy to Cloud Run

```
export GCP_PROJECT_ID="your-project"
export GOOGLE_API_KEY="your-gemini-key"
./deploy.sh
```

## API

- `GET /health`
- `POST /api/recommend`

Sample request:

```
{
  "location": "Pune",
  "month": 7,
  "soil": "loamy"
}
```
