"""AI adapter with mock responses for local development."""

import os
import hashlib
import random

from backend.lib import archetypes as _archetypes

USE_MOCK = os.environ.get("USE_MOCK", "true").lower() == "true"


def generate_taste_profile(quiz_answers: dict) -> dict:
    """Generate a taste signals profile from quiz answers.

    Returns a dict with domain_scores, dominant_signals, archetype_key, and
    a style_tag.
    """
    if not USE_MOCK:
        raise NotImplementedError("Live AI adapter not yet implemented")

    archetype_key = _archetypes.match_archetype(quiz_answers)
    archetype = _archetypes.get_archetype(archetype_key)

    # Use radar_scores as domain_scores
    domain_scores = dict(archetype["radar_scores"])

    # Pick top 3 domains as dominant signals
    sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
    dominant_signals = [d[0] for d in sorted_domains[:3]]

    return {
        "domain_scores": domain_scores,
        "dominant_signals": dominant_signals,
        "archetype_key": archetype_key,
        "style_tag": archetype["name"],
    }


def generate_archetype(taste_signals: dict, quiz_answers: dict | None = None) -> dict:
    """Generate a full archetype profile from taste signals.

    Uses archetypes.py for canonical archetype data. Returns archetype name,
    vibe_summary, markers, radar_scores, and cross_platform_insight.
    """
    if not USE_MOCK:
        raise NotImplementedError("Live AI adapter not yet implemented")

    archetype_key = taste_signals.get("archetype_key")
    if not archetype_key or _archetypes.get_archetype(archetype_key) is None:
        # Fallback: re-derive from quiz_answers or use deterministic hash
        if quiz_answers:
            archetype_key = _archetypes.match_archetype(quiz_answers)
        else:
            archetype_key = _archetypes.ARCHETYPE_KEYS[0]

    archetype = _archetypes.get_archetype(archetype_key)

    return {
        "archetype": archetype["name"],
        "vibe_summary": archetype["vibe_summary"],
        "markers": archetype["markers"],
        "radar_scores": archetype["radar_scores"],
        "cross_platform_insight": archetype["cross_platform_insight"],
    }


def generate_growth_path(
    taste_signals: dict,
    mood: str,
    goal: str,
    time_available: int,
    content_items: list[dict],
) -> list[dict]:
    """Generate a sequenced growth path of 3-5 items.

    Filters content_items by mood_tags matching mood, filters by time, selects
    3-5 items, sequences as Absorb -> Create -> Reflect.
    """
    if not USE_MOCK:
        raise NotImplementedError("Live AI adapter not yet implemented")

    mood_lower = mood.lower().strip()
    dominant = taste_signals.get("dominant_signals", [])

    # Filter by mood tags
    mood_matched = []
    for item in content_items:
        item_tags = [t.lower() for t in item.get("mood_tags", [])]
        if mood_lower in item_tags or any(
            mood_lower in tag for tag in item_tags
        ):
            mood_matched.append(item)

    # If not enough mood matches, include items from dominant domains
    if len(mood_matched) < 3:
        for item in content_items:
            if item.get("domain", "").lower() in dominant and item not in mood_matched:
                mood_matched.append(item)
            if len(mood_matched) >= 8:
                break

    # If still not enough, just use all items
    if len(mood_matched) < 3:
        mood_matched = list(content_items)

    # Filter by time availability
    time_filtered = [
        item for item in mood_matched
        if item.get("time_minutes", 30) <= time_available
    ]

    if len(time_filtered) < 3:
        time_filtered = mood_matched  # relax time constraint

    # Deterministic seed for reproducibility within a session
    seed_str = f"{mood}|{goal}|{time_available}"
    rng = random.Random(hashlib.md5(seed_str.encode()).hexdigest())

    rng.shuffle(time_filtered)
    selected = time_filtered[:5]

    # Sequence as Absorb -> Create -> Reflect
    engagement_types = ["Absorb", "Create", "Reflect"]
    why_love_templates = {
        "Absorb": [
            "This hits different when you are in a {mood} mood — let it wash over you.",
            "Perfect for soaking in something meaningful without overthinking.",
            "You will find yourself nodding along — this resonates with your {domain} taste.",
        ],
        "Create": [
            "Time to channel your {mood} energy into something tangible.",
            "Your {archetype} side will love the creative challenge here.",
            "Making something is the best way to process what you are feeling.",
        ],
        "Reflect": [
            "Sit with this one. Your {archetype} energy means you will see layers others miss.",
            "This is where the growth happens — connecting dots between what you consumed and who you are.",
            "The kind of piece that changes meaning every time you revisit it.",
        ],
    }
    why_grows_templates = {
        "Absorb": [
            "Expands your {domain} palette in a direction you have not explored yet.",
            "Builds new neural pathways in your taste map — your DNA evolves with every listen/watch/read.",
        ],
        "Create": [
            "Shifts you from consumer to creator — the most powerful growth move.",
            "Forces you to articulate what you feel, which deepens your self-awareness.",
        ],
        "Reflect": [
            "Strengthens your ability to connect ideas across domains — a core {archetype} superpower.",
            "Deepens your understanding of why you like what you like — taste as self-knowledge.",
        ],
    }

    archetype_name = taste_signals.get("style_tag", "Midnight Philosopher")
    path_items = []

    for i, item in enumerate(selected):
        eng_type = engagement_types[i % len(engagement_types)]
        domain = item.get("domain", "music")

        love_options = why_love_templates[eng_type]
        grows_options = why_grows_templates[eng_type]

        why_love = rng.choice(love_options).format(
            mood=mood, domain=domain, archetype=archetype_name
        )
        why_grows = rng.choice(grows_options).format(
            domain=domain, archetype=archetype_name
        )

        path_items.append(
            {
                "id": item.get("id", f"item-{i}"),
                "title": item.get("title", "Untitled"),
                "creator": item.get("creator", "Unknown"),
                "domain": domain,
                "engagement_type": eng_type,
                "why_youll_love_it": why_love,
                "why_it_grows_you": why_grows,
                "external_link": item.get("external_link", ""),
                "time_minutes": item.get("time_minutes", 15),
            }
        )

    return path_items


def generate_analytics_insight(stats: dict) -> str:
    """Generate a natural-language insight from analytics stats."""
    if not USE_MOCK:
        raise NotImplementedError("Live AI adapter not yet implemented")

    items_done = stats.get("items_done", 0)
    items_skipped = stats.get("items_skipped", 0)
    domain_breakdown = stats.get("domain_breakdown", {})
    goal_alignment_pct = stats.get("goal_alignment_pct", 0)

    # Find top domain
    top_domain = "music"
    if domain_breakdown:
        top_domain = max(domain_breakdown, key=domain_breakdown.get)

    total = items_done + items_skipped
    if total == 0:
        return (
            "You have not started your growth path yet. Take the first step — "
            "even a 5-minute piece can shift your perspective."
        )

    completion_rate = items_done / total if total > 0 else 0

    if completion_rate > 0.8:
        return (
            f"You are crushing it — {items_done} items completed with serious "
            f"commitment. Your {top_domain} taste is evolving fast. You are "
            f"the kind of person who finishes what they start, and it shows "
            f"in your {goal_alignment_pct}% goal alignment."
        )
    elif completion_rate > 0.5:
        return (
            f"Solid progress with {items_done} items done. You are leaning "
            f"heavily into {top_domain}, which makes sense for your vibe. "
            f"Try branching out to balance your radar — growth happens at "
            f"the edges of your comfort zone."
        )
    else:
        return (
            f"You have been exploring but skipping a lot — {items_skipped} "
            f"skips versus {items_done} completions. That is okay, it means "
            f"we are still calibrating. The items you did finish were mostly "
            f"{top_domain} — let us lean into that and find your rhythm."
        )
