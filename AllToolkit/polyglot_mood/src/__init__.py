"""Polyglot Mood core module."""
from .mood import (
    get_mood_profile,
    get_consecutive_mood,
    MoodProfile,
    MoodSpectrum,
    VibeCheck,
    LANGUAGE_MOODS,
    ROTATION_FILE,
    _compute_mood_shift,
    _compute_contrast,
    _build_transition_advice,
)

__all__ = [
    "get_mood_profile",
    "get_consecutive_mood",
    "MoodProfile",
    "MoodSpectrum",
    "VibeCheck",
    "LANGUAGE_MOODS",
    "ROTATION_FILE",
    "_compute_mood_shift",
    "_compute_contrast",
    "_build_transition_advice",
]