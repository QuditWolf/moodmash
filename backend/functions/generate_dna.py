"""DNA generation handler — creates taste archetype from session data."""

from backend.lib import ai, db


def handler(event: dict) -> dict:
    """Generate or retrieve the taste DNA for a session.

    Input:
        session_id: str — path parameter

    Returns:
        {archetype, vibe_summary, markers, radar_scores, cross_platform_insight}
    """
    session_id = event.get("session_id")
    if not session_id:
        return {"error": "session_id is required", "status_code": 400}

    session = db.get_session(session_id)
    if not session:
        return {"error": "Session not found", "status_code": 404}

    # Generate DNA if not already cached in session
    if "dna" not in session:
        taste_signals = session.get("taste_signals", {})
        dna = ai.generate_archetype(taste_signals)
        session["dna"] = dna
        db.put_session(session_id, session)

    dna = session["dna"]

    return {
        "archetype": dna["archetype"],
        "vibe_summary": dna["vibe_summary"],
        "markers": dna["markers"],
        "radar_scores": dna["radar_scores"],
        "cross_platform_insight": dna["cross_platform_insight"],
    }
