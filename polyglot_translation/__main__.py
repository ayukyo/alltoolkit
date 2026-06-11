#!/usr/bin/env python3
"""
Polyglot Translation — CLI entry point
"""

import json
import os
import sys
from pathlib import Path

# Add parent to path so the module imports cleanly
sys.path.insert(0, str(Path(__file__).parent))

from polyglot_translation import (
    ROTATION_FILE,
    get_current_language,
    advance_rotation,
    generate_card,
    format_card,
    run,
)

if __name__ == "__main__":
    print(run())