"""In-memory database adapter with optional DynamoDB routing."""

import os
from datetime import datetime, timezone

USE_DYNAMODB = os.environ.get("USE_DYNAMODB", "false").lower() == "true"

# In-memory storage
_sessions: dict[str, dict] = {}
_feedback: dict[str, list[dict]] = {}


def put_session(session_id: str, data: dict) -> None:
    """Store a session by ID."""
    if USE_DYNAMODB:
        raise NotImplementedError("DynamoDB adapter not yet implemented")
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    _sessions[session_id] = data


def get_session(session_id: str) -> dict | None:
    """Retrieve a session by ID. Returns None if not found."""
    if USE_DYNAMODB:
        raise NotImplementedError("DynamoDB adapter not yet implemented")
    return _sessions.get(session_id)


def put_path_feedback(
    session_id: str, item_id: str, status: str, reaction: str | None = None
) -> None:
    """Record feedback for a path item."""
    if USE_DYNAMODB:
        raise NotImplementedError("DynamoDB adapter not yet implemented")
    if session_id not in _feedback:
        _feedback[session_id] = []
    _feedback[session_id].append(
        {
            "item_id": item_id,
            "status": status,
            "reaction": reaction,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )


def get_path_feedback(session_id: str) -> list[dict]:
    """Get all feedback entries for a session."""
    if USE_DYNAMODB:
        raise NotImplementedError("DynamoDB adapter not yet implemented")
    return _feedback.get(session_id, [])


def delete_session(session_id: str) -> None:
    """Delete a session and its associated feedback."""
    if USE_DYNAMODB:
        raise NotImplementedError("DynamoDB adapter not yet implemented")
    _sessions.pop(session_id, None)
    _feedback.pop(session_id, None)


def list_all_sessions() -> list[dict]:
    """List all sessions (for admin/debug use)."""
    if USE_DYNAMODB:
        raise NotImplementedError("DynamoDB adapter not yet implemented")
    return [
        {"session_id": sid, **data} for sid, data in _sessions.items()
    ]
