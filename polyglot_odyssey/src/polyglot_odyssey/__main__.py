"""
Polyglot Odyssey CLI

Usage:
    python -m polyglot_odyssey                        # advance + narrate
    python -m polyglot_odyssey --status              # show current state
    python -m polyglot_odyssey --history              # show journey log
    python -m polyglot_odyssey --state                # show raw JSON state
    python -m polyglot_odyssey --peek                 # peek next without advancing
    python -m polyglot_odyssey --peek 3              # peek N steps ahead
"""

import argparse
import sys
from pathlib import Path

from polyglot_odyssey import (
    STATE_FILE,
    OdysseyState,
    format_odyssey,
)


def cmd_status(state: OdysseyState) -> None:
    print()
    print("  ── Polyglot Odyssey: Current Status ──")
    print(f"  Current language : {state.last_language}")
    print(f"  Current index     : {state.current_index}")
    print(f"  Languages in tour : {', '.join(state.languages)}")
    print(f"  Total legs taken  : {state.total_legs}")
    print(f"  Last updated       : {state.updated_at}")
    print()


def cmd_history(state: OdysseyState) -> None:
    if not state.journey_log:
        print("  No journey legs recorded yet. Run without flags to begin!")
        return
    print()
    print("  ── Journey Log ──")
    for entry in state.journey_log[-10:]:  # last 10
        print(f"  Leg {entry.leg:03d}: {entry.from_lang} → {entry.to_lang}")
        print(f"           {entry.transition_story[:70]}...")
        print()
    if len(state.journey_log) > 10:
        print(f"  ... ({len(state.journey_log) - 10} earlier legs omitted)")
        print()


def cmd_peek(state: OdysseyState, steps: int = 1) -> None:
    rotation = state.languages
    try:
        pos = rotation.index(state.last_language)
    except ValueError:
        pos = -1
    print()
    print(f"  ── Next {steps} Stop{'s' if steps != 1 else ''} Ahead ──")
    for i in range(1, steps + 1):
        next_idx = (pos + i) % len(rotation)
        lang = rotation[next_idx]
        print(f"  {i}. {lang}")
    print()


def cmd_state(state: OdysseyState) -> None:
    import json
    data = {
        "languages": state.languages,
        "current_index": state.current_index,
        "last_language": state.last_language,
        "updated_at": state.updated_at,
        "total_legs": state.total_legs,
        "journey_log": [
            {
                "leg": e.leg,
                "from_lang": e.from_lang,
                "to_lang": e.to_lang,
                "transition_story": e.transition_story,
                "waypoints": e.waypoints,
                "timestamp": e.timestamp,
            }
            for e in state.journey_log
        ],
    }
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Polyglot Odyssey — Language Journey Tracker",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--status", action="store_true",
        help="Show current rotation status",
    )
    group.add_argument(
        "--history", action="store_true",
        help="Show journey log (last 10 legs)",
    )
    group.add_argument(
        "--state", action="store_true",
        help="Show raw state JSON",
    )
    group.add_argument(
        "--peek", nargs="?", const=1, type=int, metavar="N",
        help="Peek N stops ahead without advancing (default: 1)",
    )
    args = parser.parse_args()

    # Load state (do NOT auto-advance for info commands)
    state = OdysseyState.load(STATE_FILE)

    if args.status:
        cmd_status(state)
        return

    if args.history:
        cmd_history(state)
        return

    if args.state:
        cmd_state(state)
        return

    if args.peek is not None:
        cmd_peek(state, args.peek)
        return

    # Default: advance rotation and narrate
    if not STATE_FILE.exists():
        print(
            "WARNING: language_rotation.json not found. "
            "Bootstrapping from default state.",
            file=sys.stderr,
        )

    from_lang, to_lang, story, waypoints, leg = state.advance()
    state.save(STATE_FILE)

    output = format_odyssey(from_lang, to_lang, story, waypoints, leg)
    print(output)


if __name__ == "__main__":
    main()
