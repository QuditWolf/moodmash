"""MoodMash FastAPI application — local development server simulating Lambda handlers."""

import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.functions import (
    analytics,
    data_control,
    generate_dna,
    get_path,
    onboard,
    path_feedback,
)

app = FastAPI(
    title="MoodMash API",
    description="Taste DNA and Growth Path engine for culturally-rooted content discovery",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Pydantic request models
# ---------------------------------------------------------------------------


class OnboardRequest(BaseModel):
    quiz_answers: dict = Field(..., min_length=1, description="Quiz responses as key-value pairs")
    goal: str = Field(..., min_length=1, description="User's growth goal")


class PathRequest(BaseModel):
    session_id: str = Field(..., description="Session identifier")
    mood: str = Field(..., min_length=1, description="Current mood")
    goal: str = Field(default="", description="Goal for this path session")
    time_available: int = Field(default=30, ge=5, le=480, description="Minutes available")


class FeedbackRequest(BaseModel):
    session_id: str = Field(..., description="Session identifier")
    item_id: str = Field(..., description="Content item identifier")
    status: str = Field(..., pattern="^(done|skipped|saved)$", description="Item status")
    reaction: str | None = Field(default=None, description="Optional reaction")


# ---------------------------------------------------------------------------
# Helper to convert handler results into HTTP responses
# ---------------------------------------------------------------------------


def _respond(result: dict) -> dict:
    """Check handler result for errors and raise HTTPException if needed."""
    status_code = result.pop("status_code", None)
    error = result.get("error")
    if status_code and status_code >= 400:
        raise HTTPException(status_code=status_code, detail=error or "Unknown error")
    return result


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/health")
def health():
    mock_mode = os.environ.get("USE_MOCK", "true").lower() == "true"
    return {"status": "ok", "mock_mode": mock_mode}


@app.post("/api/onboard")
def api_onboard(body: OnboardRequest):
    event = {"quiz_answers": body.quiz_answers, "goal": body.goal}
    return _respond(onboard.handler(event))


@app.get("/api/dna/{session_id}")
def api_dna(session_id: str):
    event = {"session_id": session_id}
    return _respond(generate_dna.handler(event))


@app.post("/api/path")
def api_path(body: PathRequest):
    event = {
        "session_id": body.session_id,
        "mood": body.mood,
        "goal": body.goal,
        "time_available": body.time_available,
    }
    return _respond(get_path.handler(event))


@app.post("/api/path/{path_id}/feedback")
def api_feedback(path_id: str, body: FeedbackRequest):
    event = {
        "session_id": body.session_id,
        "item_id": body.item_id,
        "status": body.status,
        "reaction": body.reaction,
    }
    return _respond(path_feedback.handler(event))


@app.get("/api/analytics/{session_id}")
def api_analytics(session_id: str):
    event = {"session_id": session_id}
    return _respond(analytics.handler(event))


@app.get("/api/data/{session_id}")
def api_data_get(session_id: str):
    event = {"session_id": session_id}
    return _respond(data_control.get_handler(event))


@app.delete("/api/data/{session_id}")
def api_data_delete(session_id: str):
    event = {"session_id": session_id}
    return _respond(data_control.delete_handler(event))


# ---------------------------------------------------------------------------
# Lambda export (uncomment for deploy)
# ---------------------------------------------------------------------------
# from mangum import Mangum
# lambda_handler = Mangum(app)


# ---------------------------------------------------------------------------
# Local dev entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    host = os.environ.get("API_HOST", "0.0.0.0")
    port = int(os.environ.get("API_PORT", "8000"))
    uvicorn.run("backend.main:app", host=host, port=port, reload=True)
