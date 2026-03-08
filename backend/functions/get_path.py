"""Growth path generation handler."""

import json
import uuid
from pathlib import Path

from backend.lib import ai, db

# Resolve content.json relative to project root
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_CONTENT_PATH = _PROJECT_ROOT / "knowledge-base" / "content.json"


def _load_content() -> list[dict]:
    """Load content items from knowledge base."""
    if not _CONTENT_PATH.exists():
        return []
    with open(_CONTENT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def handler(event: dict) -> dict:
    """Generate a growth path for the user.

    Input:
        session_id: str
        mood: str — current mood
        goal: str — what user wants from this session
        time_available: int — minutes available

    Returns:
        {path_id, items: [{id, title, creator, domain, engagement_type,
         why_youll_love_it, why_it_grows_you, external_link, time_minutes}]}
    """
    session_id = event.get("session_id")
    mood = event.get("mood", "")
    goal = event.get("goal", "")
    time_available = event.get("time_available", 30)

    if not session_id:
        return {"error": "session_id is required", "status_code": 400}
    if not mood:
        return {"error": "mood is required", "status_code": 400}

    session = db.get_session(session_id)
    if not session:
        return {"error": "Session not found", "status_code": 404}

    taste_signals = session.get("taste_signals", {})
    content_items = _load_content()

    if not content_items:
        return {"error": "Content library is empty", "status_code": 500}

    # Use session goal if not provided in request
    if not goal:
        goal = session.get("goal", "explore")

    path_items = ai.generate_growth_path(
        taste_signals=taste_signals,
        mood=mood,
        goal=goal,
        time_available=int(time_available),
        content_items=content_items,
    )

    path_id = str(uuid.uuid4())

    return {
        "path_id": path_id,
        "items": path_items,
    }
