"""Entry point: python -m polyglot_semantics"""
from .src.semantics import (
    analyze_semantics,
    format_semantic_fingerprint,
    get_current_language,
    run_tests,
)

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        lang_info = get_current_language()
        profile = analyze_semantics(lang_info["current_language"])
        print(format_semantic_fingerprint(lang_info, profile))