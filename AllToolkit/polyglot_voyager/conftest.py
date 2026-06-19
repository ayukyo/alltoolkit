"""Conftest: ensure src/ is on the import path."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))
