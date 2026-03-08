"""Data control handlers — GDPR-style data access and deletion."""

from backend.lib import db


def get_handler(event: dict) -> dict:
    """Return sanitized session data for the user.

    Input:
        session_id: str

    Returns:
        Sanitized session data (no raw vectors or internal keys).
    """
    session_id = event.get("session_id")
    if not session_id:
        return {"error": "session_id is required", "status_code": 400}

    session = db.get_session(session_id)
    if not session:
        return {"error": "Session not found", "status_code": 404}

    # Sanitize: return user-facing data only
    sanitized = {
        "session_id": session_id,
        "goal": session.get("goal", ""),
        "created_at": session.get("created_at", ""),
        "updated_at": session.get("updated_at", ""),
    }

    # Include taste profile summary (no raw vectors)
    taste = session.get("taste_signals", {})
    if taste:
        sanitized["taste_profile"] = {
            "style_tag": taste.get("style_tag", ""),
            "dominant_signals": taste.get("dominant_signals", []),
            "domain_scores": taste.get("domain_scores", {}),
        }

    # Include DNA if generated
    dna = session.get("dna")
    if dna:
        sanitized["dna"] = {
            "archetype": dna.get("archetype", ""),
            "vibe_summary": dna.get("vibe_summary", ""),
            "markers": dna.get("markers", []),
        }

    # Include feedback history
    feedback = db.get_path_feedback(session_id)
    if feedback:
        sanitized["feedback_history"] = feedback

    return sanitized


def delete_handler(event: dict) -> dict:
    """Delete all session data.

    Input:
        session_id: str

    Returns:
        {deleted: true}
    """
    session_id = event.get("session_id")
    if not session_id:
        return {"error": "session_id is required", "status_code": 400}

    session = db.get_session(session_id)
    if not session:
        return {"error": "Session not found", "status_code": 404}

    db.delete_session(session_id)

    return {"deleted": True}
