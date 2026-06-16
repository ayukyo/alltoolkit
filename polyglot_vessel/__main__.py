#!/usr/bin/env python3
"""
Entry point for polyglot_vessel module.
"""

import sys
import os
from pathlib import Path

# Ensure AllToolkit/ is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_vessel.src.vessel import generate_vessel_report, format_vessel_report, run_tests


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--report":
        report = generate_vessel_report()
        print(format_vessel_report(report))
    elif len(sys.argv) > 1 and sys.argv[1] == "--json":
        import json
        report = generate_vessel_report()
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        report = generate_vessel_report()
        print(format_vessel_report(report))
