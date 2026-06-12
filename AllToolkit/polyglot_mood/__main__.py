#!/usr/bin/env python3
"""
Polyglot Mood CLI entry point.
"""

import argparse
import json
import sys
from pathlib import Path

# Ensure src is on path
sys.path.insert(0, str(Path(__file__).parent))

from polyglot_mood.src.mood import (
    get_mood_profile,
    get_consecutive_mood,
    LANGUAGE_MOODS,
    ROTATION_FILE,
    MoodProfile,
    MoodSpectrum,
    VibeCheck,
)


def _print_profile(profile, vibe_check=None):
    print(f"╔{'═'*60}╗")
    print(f"║ 🌡️  {profile.language} — {profile.archetype:<46}║")
    print(f"╠{'═'*60}╣")
    print(f"║ \"{profile.tagline}\"")
    print(f"╠{'═'*60}╣")
    print(f"║ MOOD SPECTRUM")
    s = profile.spectrum
    bars = {}
    for axis, val in [("intensity", s.intensity), ("warmth", s.warmth),
                       ("discipline", s.discipline), ("creativity", s.creativity),
                       ("confidence", s.confidence)]:
        bar = "█" * int(val * 10) + "░" * (10 - int(val * 10))
        bars[axis] = bar
    print(f"║   intensity:  [{bars['intensity']}] {s.intensity:.2f}")
    print(f"║   warmth:     [{bars['warmth']}] {s.warmth:.2f}")
    print(f"║   discipline: [{bars['discipline']}] {s.discipline:.2f}")
    print(f"║   creativity:[{bars['creativity']}] {s.creativity:.2f}")
    print(f"║   confidence: [{bars['confidence']}] {s.confidence:.2f}")
    print(f"╠{'═'*60}╣")
    print(f"║ HAIKU")
    for line in profile.haiku.split("\n"):
        print(f"║   {line}")
    print(f"╠{'═'*60}╣")
    print(f"║ CODING TIPS")
    for tip in profile.coding_tips:
        print(f"║   • {tip}")
    print(f"╠{'═'*60}╣")
    print(f"║ EMOTIONAL TERRAIN")
    print(f"║   {profile.emotional_terrain}")
    if vibe_check:
        print(f"╠{'═'*60}╣")
        print(f"║ VIBE CHECK: {vibe_check.from_language} → {vibe_check.to_language}")
        print(f"║   shift: {vibe_check.mood_shift}")
        print(f"║   contrast: {vibe_check.contrast_score:.2f}")
        print(f"║   advice: {vibe_check.advice}")
    print(f"╚{'═'*60}╝")


def cmd_profile(args):
    profile = get_mood_profile(args.language, rotate=args.rotate)
    _print_profile(profile)
    if args.json:
        print(json.dumps({
            "language": profile.language,
            "archetype": profile.archetype,
            "tagline": profile.tagline,
            "spectrum": {
                "intensity": profile.spectrum.intensity,
                "warmth": profile.spectrum.warmth,
                "discipline": profile.spectrum.discipline,
                "creativity": profile.spectrum.creativity,
                "confidence": profile.spectrum.confidence,
            },
            "haiku": profile.haiku,
            "coding_tips": profile.coding_tips,
            "emotional_terrain": profile.emotional_terrain,
        }, indent=2))


def cmd_rotate(args):
    current_mood, vibe_check = get_consecutive_mood(rotate=True)
    _print_profile(current_mood, vibe_check)
    if args.json:
        data = {
            "current": {
                "language": current_mood.language,
                "archetype": current_mood.archetype,
                "spectrum": {
                    "intensity": current_mood.spectrum.intensity,
                    "warmth": current_mood.spectrum.warmth,
                    "discipline": current_mood.spectrum.discipline,
                    "creativity": current_mood.spectrum.creativity,
                    "confidence": current_mood.spectrum.confidence,
                },
                "haiku": current_mood.haiku,
                "coding_tips": current_mood.coding_tips,
            }
        }
        if vibe_check:
            data["vibe_check"] = {
                "from": vibe_check.from_language,
                "to": vibe_check.to_language,
                "mood_shift": vibe_check.mood_shift,
                "contrast_score": vibe_check.contrast_score,
                "advice": vibe_check.advice,
            }
        print(json.dumps(data, indent=2))


def cmd_list(args):
    print("Available languages and their archetypes:")
    for lang, data in LANGUAGE_MOODS.items():
        print(f"  {lang:12s} → {data['archetype']}")


def main():
    parser = argparse.ArgumentParser(prog="polyglot-mood")
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("profile", help="Show mood profile for a language")
    p.add_argument("language", help="Language name")
    p.add_argument("--no-rotate", dest="rotate", action="store_false",
                   help="Don't advance the rotation index")
    p.add_argument("--json", action="store_true", help="Output JSON")

    r = sub.add_parser("rotate", help="Rotate and show current language mood")
    r.add_argument("--json", action="store_true", help="Output JSON")

    l = sub.add_parser("list", help="List all languages and archetypes")

    args = parser.parse_args()

    if args.cmd == "profile":
        cmd_profile(args)
    elif args.cmd == "rotate":
        cmd_rotate(args)
    elif args.cmd == "list":
        cmd_list(args)
    else:
        # Default: rotate
        cmd_rotate(argparse.Namespace(json=False))


if __name__ == "__main__":
    main()