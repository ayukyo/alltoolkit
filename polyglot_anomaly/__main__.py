#!/usr/bin/env python3
"""Entry point for polyglot_anomaly module."""

import sys
import os

# Ensure parent (AllToolkit/) is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_anomaly import run_tests, detect_anomalies, format_anomaly_report
import json


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--report":
        result = detect_anomalies()
        print(format_anomaly_report(result))
    elif len(sys.argv) > 1 and sys.argv[1] == "--json":
        result = detect_anomalies()
        print(json.dumps(result, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "--detect":
        lang = sys.argv[2] if len(sys.argv) > 2 else None
        result = detect_anomalies(lang)
        print(format_anomaly_report(result))
    else:
        result = detect_anomalies()
        print(format_anomaly_report(result))
