"""Onboarding handler — processes quiz answers and creates a session."""

import hashlib
import uuid
from datetime import datetime, timezone

from backend.lib import ai, db


def handler(event: dict) -> dict:
    """Process onboarding quiz answers and create a new session.

    Input:
        quiz_answers: dict — user's quiz responses (at least 1 key)
        goal: str — user's stated growth goal

    Returns:
        {session_id, status}
    """
    quiz_answers = event.get("quiz_answers")
    goal = event.get("goal", "")

    # Validate
    if not quiz_answers or not isinstance(quiz_answers, dict) or len(quiz_answers) < 1:
        return {"error": "quiz_answers must be a dict with at least 1 key", "status_code": 400}

    if not goal or not isinstance(goal, str):
        return {"error": "goal must be a non-empty string", "status_code": 400}

    # Generate taste profile
    taste_signals = ai.generate_taste_profile(quiz_answers)

    # Create session
    session_id = str(uuid.uuid4())

    # Hash quiz answers for dedup — do NOT store raw answers (privacy)
    answers_str = "|".join(
        f"{k}={v}" for k, v in sorted(quiz_answers.items(), key=lambda x: x[0])
    )
    quiz_answers_hash = hashlib.sha256(answers_str.encode()).hexdigest()

    db.put_session(
        session_id,
        {
            "taste_signals": taste_signals,
            "goal": goal,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "quiz_answers_hash": quiz_answers_hash,
        },
    )

    return {"session_id": session_id, "status": "ok"}
