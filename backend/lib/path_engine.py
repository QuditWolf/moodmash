"""Text-based path generation engine — no embeddings, pure keyword matching."""

from __future__ import annotations
import random
from typing import Any

MOOD_TAG_MAP = {
    "focused":     ["focused", "calm", "contemplative"],
    "exploratory": ["exploratory", "joyful", "energized"],
    "melancholic": ["melancholic", "introspective", "nostalgic"],
    "energized":   ["energized", "joyful", "rebellious"],
    "calm":        ["calm", "introspective", "contemplative"],
}

GOAL_GROWTH_MAP = {
    "Build something that matters":       ["creative_inspiration", "technical_skills", "goal_clarity"],
    "Get technically excellent":          ["technical_skills", "critical_thinking", "goal_clarity"],
    "Find what makes me happy":           ["emotional_awareness", "mindfulness", "self_expression"],
    "Start something of my own":          ["creative_inspiration", "goal_clarity", "communication"],
    "Understand where I come from":       ["cultural_roots", "emotional_awareness", "aesthetic_sense"],
    "Just inspire me and see what emerges": ["creative_inspiration", "aesthetic_sense", "self_expression"],
}

WHY_LOVE_TEMPLATES = {
    "music": [
        "Your taste map shows you feel music before you understand it — {title} by {creator} hits exactly that register.",
        "This matches the {mood} energy you're in. {creator}'s sound sits perfectly in your musical world.",
        "{title} is the kind of track that defines a season. Given your taste, this one's yours.",
    ],
    "films": [
        "{title} is exactly the kind of cinema you gravitate toward — it doesn't resolve, it resonates.",
        "Your film taste values stories that stay with you. {creator}'s work here will do exactly that.",
        "This one lives in the space between entertainment and experience — which is where you seem to like it.",
    ],
    "books": [
        "You pick books that reframe how you see things. {title} by {creator} will do that.",
        "Your reading pattern favors depth and honesty. This one delivers both.",
        "{title} isn't just a book — it's a lens. Given your taste, it'll fit naturally.",
    ],
    "art": [
        "Your visual world values restraint and intention. {creator}'s work speaks that language.",
        "This piece resonates with your aesthetic sensitivity — you'll find something new each time you look.",
        "{title} reflects the visual sensibility you've been cultivating.",
    ],
    "creators": [
        "You follow people obsessively, not channels. {creator} is one worth following deeply.",
        "Your discovery pattern values one person's full perspective over many opinions. {creator} delivers that.",
        "{title} by {creator} is the kind of content you mark, save, and come back to.",
    ],
    "exercise": [
        "This exercise matches how you process — through making, not just consuming.",
        "You tend to need to externalize things to understand them. This prompt is designed for that.",
        "Given your creative orientation, this is exactly the kind of thing that will unlock something.",
    ],
    "default": [
        "This matches your current taste profile and the energy you came in with.",
        "Selected for your specific combination of tastes — this one fits.",
    ],
}

WHY_GROW_TEMPLATES = {
    "emotional_awareness": [
        "This builds your capacity to sit with complexity — which is the core of emotional intelligence.",
        "Deepens your emotional vocabulary in a way that's invisible while it's happening.",
    ],
    "creative_inspiration": [
        "Will give you raw material your creative mind will be processing for days.",
        "Exposes you to a creative approach you haven't fully absorbed yet.",
    ],
    "cultural_roots": [
        "Connects you to a lineage of Indian creative thought that's worth knowing intimately.",
        "Part of the cultural inheritance you're still discovering — and this is a significant piece.",
    ],
    "technical_skills": [
        "Builds a specific capability that compounds. The skill unlocks the next skill.",
        "Practical and immediately applicable to where you want to go technically.",
    ],
    "self_expression": [
        "This is practice for finding your voice — low stakes, high output.",
        "Expression builds on expression. This adds to the archive of yourself.",
    ],
    "critical_thinking": [
        "Challenges a frame you might be taking for granted. That's where growth happens.",
        "Gives you a new analytical lens — one that applies well beyond this domain.",
    ],
    "mindfulness": [
        "Trains your attention without calling it meditation. You'll notice the difference later.",
        "Builds the capacity to be fully present with one thing — rare and worth developing.",
    ],
    "goal_clarity": [
        "Sharpens your sense of direction by showing you what commitment looks like in someone else.",
        "Will help crystallize what you actually want, not just what you think you should want.",
    ],
    "communication": [
        "Every great communicator is first a great observer. This trains observation.",
        "Strengthens your ability to translate internal experience into something others can receive.",
    ],
    "aesthetic_sense": [
        "Refines your visual vocabulary — the more you see with intention, the more you make with intention.",
        "Develops the eye. You'll start noticing things you used to walk past.",
    ],
}

def score_item(item: dict[str, Any], mood_tags: list[str], growth_tags: list[str], domain_scores: dict[str, float]) -> float:
    """Score a content item for relevance to current user context."""
    score = 0.0
    for tag in item.get("mood_tags", []):
        if tag in mood_tags:
            score += 2.0
    for tag in item.get("growth_tags", []):
        if tag in growth_tags:
            score += 2.0
    domain = item.get("domain", "")
    score += domain_scores.get(domain, 0.0) * 1.5
    return score


def pick_template(templates: list[str], item: dict[str, Any]) -> str:
    """Fill a template with item data."""
    t = random.choice(templates)
    return t.format(
        title=item.get("title", "this piece"),
        creator=item.get("creator", "the creator"),
        mood=item.get("mood_tags", ["this"])[0] if item.get("mood_tags") else "this",
        domain=item.get("domain", "this"),
    )


def generate_why_love(item: dict[str, Any]) -> str:
    domain = item.get("domain", "default")
    templates = WHY_LOVE_TEMPLATES.get(domain, WHY_LOVE_TEMPLATES["default"])
    return pick_template(templates, item)


def generate_why_grow(item: dict[str, Any], growth_tags: list[str]) -> str:
    for tag in item.get("growth_tags", []):
        if tag in growth_tags and tag in WHY_GROW_TEMPLATES:
            return random.choice(WHY_GROW_TEMPLATES[tag])
    all_tags = item.get("growth_tags", [])
    if all_tags and all_tags[0] in WHY_GROW_TEMPLATES:
        return random.choice(WHY_GROW_TEMPLATES[all_tags[0]])
    return "Adds a new perspective to your current growth direction."


def sequence_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Sort items: Absorb first, then Create, then Reflect last if possible."""
    order = {"absorb": 0, "create": 1, "reflect": 2}
    return sorted(items, key=lambda x: order.get(x.get("engagement_type", "absorb"), 0))


def generate_path(
    taste_signals: dict[str, Any],
    mood: str,
    goal: str,
    time_available: int,
    content_items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    mood_tags = MOOD_TAG_MAP.get(mood, [mood])
    growth_tags = GOAL_GROWTH_MAP.get(goal, ["creative_inspiration", "emotional_awareness"])
    domain_scores = taste_signals.get("domain_scores", {})

    # Score all items
    scored = [(score_item(item, mood_tags, growth_tags, domain_scores), item) for item in content_items]
    scored.sort(key=lambda x: x[0], reverse=True)

    # Select items within time budget
    selected = []
    total_time = 0
    for score, item in scored:
        item_time = item.get("time_minutes", 10)
        if total_time + item_time <= time_available:
            selected.append(item)
            total_time += item_time
        if len(selected) >= 5:
            break

    # Fallback: take top 3 regardless of time if nothing selected
    if not selected:
        selected = [item for _, item in scored[:3]]

    # Sequence: absorb → create → reflect
    selected = sequence_items(selected)

    # Annotate with explanations
    result = []
    for item in selected:
        annotated = dict(item)
        annotated["why_youll_love_it"] = generate_why_love(item)
        annotated["why_it_grows_you"] = generate_why_grow(item, growth_tags)
        result.append(annotated)

    return result
