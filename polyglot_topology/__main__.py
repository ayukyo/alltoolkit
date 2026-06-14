#!/usr/bin/env python3
"""Entry point for polyglot_topology module."""

import sys
import os

# Ensure parent (AllToolkit/) is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_topology.src import run_tests, topology, compute_topology, format_topology
import json


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--report":
        result = topology()
        print(format_topology(result))
    elif len(sys.argv) > 1 and sys.argv[1] == "--json":
        result = topology()
        print(json.dumps(result, indent=2))
    else:
        print("🗺️ Polyglot Topology v1.0.0")
        print("  🗺️  Map the topological structure of programming language design space.")
        print("")
        print("Usage:")
        print("  python -m polyglot_topology --test    # Run all tests")
        print("  python -m polyglot_topology --report # Human-readable report")
        print("  python -m polyglot_topology --json   # JSON output")