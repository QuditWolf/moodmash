"""Archetype definitions and keyword-based matching logic.

Defines 8 Indian-cultural archetypes with full metadata and provides
a text-based matching function that scores quiz answers against each
archetype's trigger keywords — no embeddings or vector math required.
"""

from __future__ import annotations

import hashlib
from typing import Any

# ---------------------------------------------------------------------------
# Archetype catalogue
# ---------------------------------------------------------------------------

ARCHETYPES: dict[str, dict[str, Any]] = {
    "midnight_philosopher": {
        "name": "Midnight Philosopher",
        "vibe_summary": (
            "You chase depth over trend. Your playlists have more feelings "
            "than most people's journals. You are the one who pauses a film "
            "to sit with a scene before moving on — and your 2 AM reading "
            "sessions with Dostoevsky and Prateek Kuhad on loop are not a "
            "phase, they are a lifestyle."
        ),
        "markers": [
            "depth-seeker",
            "emotionally-literate",
            "late-night-thinker",
            "quality-over-quantity",
            "introspective-listener",
            "narrative-driven",
            "journals-after-consuming",
        ],
        "radar_scores": {
            "music": 0.70,
            "films": 0.85,
            "books": 0.95,
            "art": 0.60,
            "creators": 0.50,
        },
        "cross_platform_insight": (
            "Your taste graph reveals a pattern: you gravitate toward "
            "content that sits with ambiguity rather than resolving it. "
            "Your Spotify is acoustic playlists made at 1 AM, your "
            "Letterboxd is curated like a museum, and your Kindle "
            "highlights could fill a thesis."
        ),
        "trigger_keywords": [
            "introspective", "philosophical", "depth", "melancholic",
            "bengali film", "essay", "identity", "grief", "existential",
            "think deeply", "late night", "lo-fi", "acoustic",
            "dostoevsky", "manto", "literary fiction", "slow cinema",
            "poetry", "journaling", "pather panchali", "solitude",
            "meaning", "contemplative", "quiet", "reflection",
            "long-form", "books", "reading", "emotionally resonant",
        ],
    },
    "desi_renaissance_soul": {
        "name": "Desi Renaissance Soul",
        "vibe_summary": (
            "You move between Carnatic music and K-pop without blinking. "
            "You quote Mirza Ghalib and Hayao Miyazaki in the same breath. "
            "Your taste is a bridge between cultures — rooted in desi soil "
            "but reaching everywhere. Your friends call it chaotic; you know "
            "it is just range."
        ),
        "markers": [
            "multilingual-playlists",
            "culturally-rooted-explorer",
            "genre-bridger",
            "raga-to-lo-fi",
            "translation-reader",
            "history-podcast-while-cooking",
        ],
        "radar_scores": {
            "music": 0.85,
            "films": 0.80,
            "books": 0.75,
            "art": 0.70,
            "creators": 0.80,
        },
        "cross_platform_insight": (
            "Your YouTube recommendations are wild — one minute it is a "
            "Bharatanatyam recital, the next it is a video essay about Wes "
            "Anderson. You have sent at least ten different friends ten "
            "different genre recommendations this week, and every one landed."
        ),
        "trigger_keywords": [
            "diverse", "culture", "classical", "global", "multilingual",
            "carnatic", "hindustani", "world cinema", "regional music",
            "translation", "ghalib", "miyazaki", "raga", "folk",
            "broad taste", "everything", "all genres", "spiritual",
            "traditional", "roots", "heritage", "bollywood and arthouse",
            "indian classical", "cross-cultural", "fusion",
            "regional", "desi", "gharana",
        ],
    },
    "chai_minimalist": {
        "name": "Chai Minimalist",
        "vibe_summary": (
            "You believe in less but better. One perfect album on repeat, "
            "one film a week watched properly, one book at a time finished "
            "before the next. Your aesthetic is clean, intentional, and "
            "surprisingly warm — like cutting chai on a rainy Mumbai evening."
        ),
        "markers": [
            "curated-over-cluttered",
            "album-listener",
            "fewer-films-every-frame",
            "clean-desk-energy",
            "values-craft-over-trend",
            "analog-notebook-user",
        ],
        "radar_scores": {
            "music": 0.65,
            "films": 0.70,
            "books": 0.80,
            "art": 0.90,
            "creators": 0.55,
        },
        "cross_platform_insight": (
            "Your phone has three apps on the home screen. Your Goodreads "
            "is small but every rating is earned. You have strong opinions "
            "about font choices and colour palettes, and your room looks "
            "like a Pinterest board that actually gets lived in."
        ),
        "trigger_keywords": [
            "minimal", "simple", "clean", "less", "focused", "intentional",
            "curated", "design", "aesthetic", "craft", "quality",
            "one at a time", "finish before starting", "zen", "calm",
            "declutter", "wabi-sabi", "pottery", "handmade",
            "sabyasachi", "muji", "understated", "analog", "notebook",
            "deliberate", "selective",
        ],
    },
    "chaos_creative": {
        "name": "Chaos Creative",
        "vibe_summary": (
            "Your taste looks like a Jackson Pollock painting — no clear "
            "pattern, but somehow it all works. You jump from death metal "
            "to ghazals, from anime to arthouse, and every mashup you make "
            "is fire. Your creativity thrives in the beautiful chaos of it all."
        ),
        "markers": [
            "genre-fluid-everywhere",
            "meme-maker-remixer",
            "150-browser-tabs-energy",
            "underground-scout",
            "bored-by-mainstream",
            "creative-bursts",
            "sharing-oriented",
        ],
        "radar_scores": {
            "music": 0.90,
            "films": 0.65,
            "books": 0.50,
            "art": 0.85,
            "creators": 0.95,
        },
        "cross_platform_insight": (
            "Your Spotify Wrapped confuses the algorithm every year. Your "
            "Instagram story is a mood board that changes hourly. You have "
            "sent at least 200 reels to friends this month with 'this is so us'."
        ),
        "trigger_keywords": [
            "chaos", "eclectic", "mix", "random", "experimental",
            "mashup", "remix", "meme", "underground", "avant-garde",
            "weird", "genre-fluid", "everything at once", "no pattern",
            "spontaneous", "impulsive", "creative", "make things",
            "collage", "punk", "death metal", "ghazal", "anime",
            "absurd", "surreal", "unconventional",
        ],
    },
    "analog_futurist": {
        "name": "Analog Futurist",
        "vibe_summary": (
            "You collect vinyl and code generative art. You read paperbacks "
            "about AI ethics. You think the future should feel like a "
            "Satyajit Ray film — warm, human, and quietly revolutionary. "
            "Nostalgia and innovation are not opposites in your world; they "
            "are collaborators."
        ),
        "markers": [
            "nostalgic-but-forward",
            "tech-ethics-thinker",
            "synthwave-and-classical",
            "craftsmanship-old-and-new",
            "film-photography-aesthetic",
            "sci-fi-and-mythology",
        ],
        "radar_scores": {
            "music": 0.75,
            "films": 0.80,
            "books": 0.85,
            "art": 0.70,
            "creators": 0.65,
        },
        "cross_platform_insight": (
            "Your bookshelf has Asimov next to Tagore. Your Spotify has a "
            "playlist called 'Retro Future Vibes'. You have opinions about "
            "both typewriter fonts and neural networks, and you think that "
            "is perfectly normal."
        ),
        "trigger_keywords": [
            "retro", "vintage", "future", "analog", "nostalgia",
            "vinyl", "film photography", "generative art", "AI ethics",
            "sci-fi", "mythology", "synthwave", "satyajit ray",
            "tagore", "asimov", "tech", "old school", "cassette",
            "typewriter", "handwritten", "code", "build",
            "innovation", "tradition meets tech", "timeless",
        ],
    },
    "rhythm_seeker": {
        "name": "Rhythm Seeker",
        "vibe_summary": (
            "Music is not just something you listen to — it is how you "
            "process the world. You feel films through their soundtracks, "
            "choose books by their rhythm, and your mood is always one song "
            "away from shifting entirely. You judge cafes by their playlist "
            "and that is a valid life choice."
        ),
        "markers": [
            "music-is-primary",
            "knows-producers-not-just-artists",
            "emotional-regulation-via-playlists",
            "raga-and-beat-drop-fluent",
            "live-show-devotee",
            "sound-connects-all-media",
            "earphone-quality-opinions",
        ],
        "radar_scores": {
            "music": 0.98,
            "films": 0.60,
            "books": 0.45,
            "art": 0.55,
            "creators": 0.70,
        },
        "cross_platform_insight": (
            "Your Spotify is your diary. You have explained the difference "
            "between Hindustani and Carnatic to at least five people this "
            "year. When someone asks for a song recommendation, you ask "
            "three clarifying questions first."
        ),
        "trigger_keywords": [
            "music", "rhythm", "sound", "beats", "melody", "song",
            "playlist", "concert", "live show", "producer", "DJ",
            "raga", "taal", "hip-hop", "rap", "EDM", "electronic",
            "nucleya", "ar rahman", "amit trivedi", "anuv jain",
            "prateek kuhad", "shankar mahadevan", "berklee",
            "soundtrack", "bass", "earphones", "vinyl",
            "ambient", "lo-fi beats",
        ],
    },
    "the_storyteller": {
        "name": "The Storyteller",
        "vibe_summary": (
            "You live for narrative. A great story can come from a novel, "
            "a three-minute song, a documentary, or your grandmother's "
            "kitchen — and you treat them all with the same reverence. "
            "You do not just consume stories; you carry them, retell them, "
            "and let them reshape how you see the world."
        ),
        "markers": [
            "narrative-across-all-media",
            "character-arcs-over-plot",
            "literary-and-graphic-novels",
            "documentaries-as-often-as-dramas",
            "podcasts-about-people",
            "writes-even-just-for-themselves",
        ],
        "radar_scores": {
            "music": 0.55,
            "films": 0.90,
            "books": 0.95,
            "art": 0.60,
            "creators": 0.75,
        },
        "cross_platform_insight": (
            "Your Goodreads goal is aggressive and you are somehow ahead of "
            "schedule. Your Letterboxd reviews read like personal essays. "
            "You have recommended Manto to everyone you know and you will "
            "not stop until they read him."
        ),
        "trigger_keywords": [
            "story", "narrative", "book", "read", "character",
            "novel", "documentary", "film", "cinema", "screenplay",
            "manto", "arundhati roy", "jhumpa lahiri", "ruskin bond",
            "graphic novel", "podcast", "oral history", "memoir",
            "biography", "zoya akhtar", "vishal bhardwaj",
            "gulzar", "lyric", "folklore", "mythology",
            "write", "journal", "storytelling",
        ],
    },
    "digital_nomad": {
        "name": "Digital Nomad",
        "vibe_summary": (
            "You are plugged in, switched on, and always scanning the "
            "horizon. You found that artist on SoundCloud three months "
            "before they blew up. Your taste is shaped by algorithms but "
            "you bend them to your will — you are not the product, you "
            "are the curator. Your DMs are a recommendation engine."
        ),
        "markers": [
            "early-platform-adopter",
            "micro-trend-tracker",
            "content-as-self-expression",
            "threads-and-carousels-thinker",
            "tech-optimist-with-taste",
            "global-palette-local-heart",
            "rabbit-hole-discoverer",
        ],
        "radar_scores": {
            "music": 0.80,
            "films": 0.55,
            "books": 0.50,
            "art": 0.70,
            "creators": 0.95,
        },
        "cross_platform_insight": (
            "You have accounts on platforms most people have not heard of "
            "yet. Your Twitter is a curation feed, your Instagram is a "
            "portfolio, and your YouTube watch history is a masterclass in "
            "trend-spotting. You think in carousels."
        ),
        "trigger_keywords": [
            "tech", "digital", "online", "trend", "platform",
            "social media", "algorithm", "influencer", "creator",
            "content creation", "soundcloud", "youtube", "instagram",
            "twitter", "threads", "carousel", "early adopter",
            "startup", "hustle", "build something", "entrepreneurship",
            "side project", "viral", "growth", "community",
            "newsletter", "substack",
        ],
    },
}

ARCHETYPE_KEYS = list(ARCHETYPES.keys())


def _flatten_answers(quiz_answers: dict, questions: list | None = None) -> list[str]:
    """Extract all selected option text from quiz answers as lowercase tokens.

    Handles multiple answer formats:
    - ``{"q1": "option text", "q2": ["opt a", "opt b"]}``
    - ``[{"questionId": "q1", "selectedOptions": ["opt"]}]``
    - Nested section format ``{"section1": [...], "section2": [...]}``
    """
    tokens: list[str] = []

    def _add(value: Any) -> None:
        if isinstance(value, str):
            tokens.append(value.lower())
        elif isinstance(value, list):
            for item in value:
                _add(item)
        elif isinstance(value, dict):
            # Handle {"questionId": ..., "selectedOptions": [...]} format
            if "selectedOptions" in value:
                _add(value["selectedOptions"])
            else:
                for v in value.values():
                    _add(v)

    _add(quiz_answers)

    # Also include question titles if provided — they carry signal
    if questions:
        for q in questions:
            if isinstance(q, dict):
                title = q.get("title", "")
                if title:
                    tokens.append(title.lower())

    return tokens


def _score_archetype(tokens: list[str], trigger_keywords: list[str]) -> float:
    """Score how well a set of tokens matches an archetype's triggers.

    Uses substring matching so that "philosophical" matches trigger
    "philosophical" and "bengali film" matches a token containing
    "bengali film".  Returns a weighted score.
    """
    score = 0.0
    joined = " ".join(tokens)

    for keyword in trigger_keywords:
        kw = keyword.lower()
        # Exact word presence in any token
        if any(kw in t for t in tokens):
            score += 2.0
        # Partial presence in the joined string (weaker signal)
        elif kw in joined:
            score += 1.0

    return score


def match_archetype(
    quiz_answers: dict,
    questions: list | None = None,
) -> str:
    """Determine the best-matching archetype key from quiz answers.

    1. Flattens all selected options into lowercase tokens.
    2. Scores each archetype by keyword overlap with its trigger_keywords.
    3. Returns the key with the highest score.
    4. Tiebreaker: deterministic hash of the answer text selects among tied
       archetypes so the result is stable for the same input.
    """
    tokens = _flatten_answers(quiz_answers, questions)

    if not tokens:
        # No signal at all — fall back to deterministic hash
        raw = str(quiz_answers)
        h = int(hashlib.md5(raw.encode()).hexdigest(), 16)
        return ARCHETYPE_KEYS[h % len(ARCHETYPE_KEYS)]

    scores: dict[str, float] = {}
    for key, arch in ARCHETYPES.items():
        scores[key] = _score_archetype(tokens, arch["trigger_keywords"])

    max_score = max(scores.values())

    # Gather all archetypes tied at the top
    tied = [k for k, s in scores.items() if s == max_score]

    if len(tied) == 1:
        return tied[0]

    # Tiebreaker: deterministic hash of tokens selects among tied keys
    tie_str = "|".join(sorted(tokens))
    h = int(hashlib.md5(tie_str.encode()).hexdigest(), 16)
    return tied[h % len(tied)]


def get_archetype(key: str) -> dict[str, Any] | None:
    """Return full archetype data by key, or None if not found."""
    return ARCHETYPES.get(key)


def all_archetype_keys() -> list[str]:
    """Return ordered list of all archetype keys."""
    return list(ARCHETYPE_KEYS)
