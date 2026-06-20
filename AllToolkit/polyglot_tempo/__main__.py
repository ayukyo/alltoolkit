#!/usr/bin/env python3
"""
Polyglot Tempo CLI entry point.
Usage: python -m polyglot_tempo [--test|--analyze [language]]
"""

import sys
from polyglot_tempo.src.tempo import (
    analyze_tempo,
    format_tempo_report,
    load_rotation,
    run_tests,
)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--analyze":
        language = sys.argv[2] if len(sys.argv) > 2 else None
        if language:
            analysis = analyze_tempo(language)
            print(format_tempo_report(analysis))
        else:
            config = load_rotation()
            current = config["languages"][config["current_index"]]
            analysis = analyze_tempo(current)
            print(format_tempo_report(analysis))
    else:
        print("🎵 Polyglot Tempo v1.0.0")
        print("Usage:")
        print("  python -m polyglot_tempo --test           # Run test suite")
        print("  python -m polyglot_tempo --analyze        # Analyze current language")
        print("  python -m polyglot_tempo --analyze Rust   # Analyze specific language")


if __name__ == "__main__":
    main()