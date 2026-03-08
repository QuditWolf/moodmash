"""Convert quiz answers into structured taste signals — text-based, no embeddings."""
from __future__ import annotations
from typing import Any

QUESTION_DOMAIN_MAP = {
    "music_album": "music", "music_3am": "music", "music_relationship": "music",
    "film_feel": "films", "story_theme": "films", "story_time": "films",
    "visual_room": "art", "visual_artist": "art", "visual_color": "art",
    "creative_time": "creators", "creative_book": "books", "creative_goal": "books",
    "consume_discover": "creators", "consume_attention": "creators", "consume_changed": "books",
}

INTROSPECTION_SIGNALS = {
    "I feel it before I understand it": 0.9, "I analyze lyrics obsessively": 0.8,
    "My mood creates the playlist": 0.85, "Masaan (ghat scene)": 0.85,
    "Pather Panchali (rain)": 0.9, "Lootera (autumn)": 0.8,
    "Identity and belonging": 0.9, "Grief and acceptance": 0.85,
    "The ordinary made extraordinary": 0.8, "Watching a 1970s Bengali film": 0.85,
    "Reading an essay that changes perspective": 0.75, "Bare walls, one good print": 0.8,
    "The Ministry of Utmost Happiness": 0.8, "The Remains of the Day": 0.85,
    "A Gentleman in Moscow": 0.75, "A film scene I couldn't stop thinking about": 0.9,
    "An essay that reframed how I see myself": 0.85, "An album that defined a year": 0.8,
}

CULTURAL_SIGNALS = {
    "Morning Raga (Bhairav)": 0.95, "Indian Ocean - Kandisa": 0.9,
    "Old Bollywood classics": 0.85, "Tamil film score": 0.9,
    "Carnatic instrumental": 0.95, "Regional music is spiritual": 0.95,
    "Pather Panchali (rain)": 0.9, "Masaan (ghat scene)": 0.85,
    "Watching a 1970s Bengali film": 0.9, "Cultural inheritance": 0.95,
    "Maximalist Indian textiles": 0.85, "Sabyasachi (maximalist heritage)": 0.9,
    "Raw Mango (quiet luxury)": 0.8, "Zarina Hashmi (geometric meditation)": 0.85,
    "Dayanita Singh (intimate documentary)": 0.85, "Rajasthan block print saturation": 0.9,
    "The Ministry of Utmost Happiness": 0.85, "Why I Am Not a Hindu": 0.8,
    "Understand where I come from": 0.9,
}

AMBITION_SIGNALS = {
    "Build something that matters": 0.95, "Get technically excellent": 0.9,
    "Start something of my own": 0.9, "Zero to One": 0.85,
    "Atomic Habits": 0.8, "Show Your Work": 0.75,
    "A skill I learned that unlocked others": 0.8, "Learn a new skill": 0.8,
    "Plan what to make next": 0.75, "Get restless without a plan": 0.7,
}

AESTHETIC_SIGNALS = {
    "Bare walls, one good print": 0.9, "Gallery white, curated objects": 0.9,
    "Black and white always": 0.8, "Single color entire frame": 0.85,
    "Earth tones only": 0.75, "Hand-applied texture imperfection": 0.85,
    "Raw Mango (quiet luxury)": 0.9, "Zarina Hashmi (geometric meditation)": 0.85,
    "Dayanita Singh (intimate documentary)": 0.8, "Lo-fi Hindustani beats": 0.75,
    "Lootera (autumn)": 0.8, "Piranesi": 0.8,
}

def _score_dimension(all_answers: list[str], signal_map: dict[str, float]) -> float:
    scores = [signal_map[a] for a in all_answers if a in signal_map]
    if not scores:
        return 0.4
    return min(1.0, sum(scores) / len(scores) + 0.05 * len(scores))

def _compute_domain_scores(quiz_answers: dict[str, list[str]]) -> dict[str, float]:
    domain_counts: dict[str, int] = {}
    for q_id, answers in quiz_answers.items():
        domain = QUESTION_DOMAIN_MAP.get(q_id, "")
        if domain:
            domain_counts[domain] = domain_counts.get(domain, 0) + len(answers)
    total = sum(domain_counts.values()) or 1
    base_domains = ["music", "films", "books", "art", "creators"]
    return {d: min(1.0, domain_counts.get(d, 0) / total * 2.5 + 0.15) for d in base_domains}

def _extract_dominant_signals(all_answers: list[str], domain_scores: dict[str, float]) -> list[str]:
    signals = [f"{max(domain_scores, key=domain_scores.get)}-dominant"]
    introspection = _score_dimension(all_answers, INTROSPECTION_SIGNALS)
    cultural = _score_dimension(all_answers, CULTURAL_SIGNALS)
    ambition = _score_dimension(all_answers, AMBITION_SIGNALS)
    if introspection > 0.7:
        signals.append("introspection-seeker")
    elif ambition > 0.7:
        signals.append("ambition-driven")
    if cultural > 0.7:
        signals.append("culturally-rooted")
    elif cultural < 0.4:
        signals.append("globally-oriented")
    return signals[:3]

def analyze_quiz(quiz_answers: dict[str, list[str]]) -> dict[str, Any]:
    all_answers = [opt for answers in quiz_answers.values() for opt in answers]
    domain_scores = _compute_domain_scores(quiz_answers)
    return {
        "domain_scores": domain_scores,
        "dominant_signals": _extract_dominant_signals(all_answers, domain_scores),
        "introspection_depth": round(_score_dimension(all_answers, INTROSPECTION_SIGNALS), 3),
        "aesthetic_sensitivity": round(_score_dimension(all_answers, AESTHETIC_SIGNALS), 3),
        "cultural_rootedness": round(_score_dimension(all_answers, CULTURAL_SIGNALS), 3),
        "ambition_orientation": round(_score_dimension(all_answers, AMBITION_SIGNALS), 3),
        "consumption_breadth": round(min(1.0, len(quiz_answers) / 15.0), 3),
    }
