#!/usr/bin/env python3
"""Polyglot Quantum CLI entry point."""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from quantum import quantum, run_tests, TOOL_NAME, TOOL_VERSION


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        result = quantum()
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
