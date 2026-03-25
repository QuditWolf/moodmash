"""Analytics handler — computes user progress stats and insights."""

from collections import Counter

from backend.lib import ai, db


def handler(event: dict) -> dict:
    """Generate analytics for a session.

    Input:
        session_id: str

    Returns:
        {radar_scores, goal_alignment_pct, items_done, items_skipped,
         domain_breakdown, pattern_insight, spotify_connected}
    """
    session_id = event.get("session_id")
    if not session_id:
        return {"error": "session_id is required", "status_code": 400}

    session = db.get_session(session_id)
    if not session:
        return {"error": "Session not found", "status_code": 404}

    completions = db.get_path_feedback(session_id)

    # Compute stats
    items_done = sum(1 for c in completions if c.get("status") == "done")
    items_skipped = sum(1 for c in completions if c.get("status") == "skipped")
    items_saved = sum(1 for c in completions if c.get("status") == "saved")

    # Domain distribution from completed items — we track item_id prefixes
    # Item IDs follow the pattern "domain-NNN"
    domain_counter = Counter()
    for c in completions:
        if c.get("status") == "done":
            item_id = c.get("item_id", "")
            # Extract domain from item_id prefix (e.g., "music-001" -> "music")
            parts = item_id.rsplit("-", 1)
            if len(parts) == 2:
                domain_counter[parts[0]] += 1
            else:
                domain_counter["unknown"] += 1

    domain_breakdown = dict(domain_counter)

    # Goal alignment: ratio of done vs total interactions
    total_interactions = items_done + items_skipped + items_saved
    goal_alignment_pct = round(
        (items_done / total_interactions * 100) if total_interactions > 0 else 0,
        1,
    )

    # Get radar scores from DNA if available
    radar_scores = {}
    if "dna" in session:
        radar_scores = session["dna"].get("radar_scores", {})
    elif "taste_signals" in session:
        radar_scores = session["taste_signals"].get("domain_scores", {})

    # Generate insight
    stats = {
        "items_done": items_done,
        "items_skipped": items_skipped,
        "domain_breakdown": domain_breakdown,
        "goal_alignment_pct": goal_alignment_pct,
    }
    pattern_insight = ai.generate_analytics_insight(stats)

    return {
        "radar_scores": radar_scores,
        "goal_alignment_pct": goal_alignment_pct,
        "items_done": items_done,
        "items_skipped": items_skipped,
        "domain_breakdown": domain_breakdown,
        "pattern_insight": pattern_insight,
        "spotify_connected": False,
    }
