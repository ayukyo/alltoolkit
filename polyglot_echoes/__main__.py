#!/usr/bin/env python3
"""Polyglot Echoes CLI entry point."""
import sys
import json
from pathlib import Path

# Add the src directory to the path
_TOOL_DIR = Path(__file__).parent.resolve()
_SRC_DIR = _TOOL_DIR / "src"
sys.path.insert(0, str(_SRC_DIR))

from echoes import echoes, format_echo_report, run_tests, TOOL_NAME, TOOL_VERSION


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--json":
        result = echoes()
        print(json.dumps(result, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "--text":
        result = echoes()
        print(format_echo_report(result))
    else:
        result = echoes()
        print(format_echo_report(result))


if __name__ == "__main__":
    main()
