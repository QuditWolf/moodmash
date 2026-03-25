"""Path feedback handler — records user feedback on path items."""

from backend.lib import db

VALID_STATUSES = {"done", "skipped", "saved"}


def handler(event: dict) -> dict:
    """Record feedback for a path item.

    Input:
        session_id: str
        item_id: str
        status: str — one of done/skipped/saved
        reaction: str (optional) — emoji or text reaction

    Returns:
        {ok: true}
    """
    session_id = event.get("session_id")
    item_id = event.get("item_id")
    status = event.get("status")
    reaction = event.get("reaction")

    if not session_id:
        return {"error": "session_id is required", "status_code": 400}
    if not item_id:
        return {"error": "item_id is required", "status_code": 400}
    if status not in VALID_STATUSES:
        return {
            "error": f"status must be one of: {', '.join(VALID_STATUSES)}",
            "status_code": 400,
        }

    db.put_path_feedback(session_id, item_id, status, reaction)

    return {"ok": True}
