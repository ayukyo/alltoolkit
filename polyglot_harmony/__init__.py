"""
Polyglot Harmony — analyzes compatibility and synergy between consecutive languages in rotation.

This module reads language_rotation.json, identifies the current and next language,
and produces a detailed harmony report exploring their relationship across multiple dimensions:
- Syntax similarity
- Paradigm overlap
- Ecosystem interop
- Learning transfer

The output is a structured report designed for developers exploring language transitions.
"""

__version__ = "0.1.0"
__author__ = "AllToolkit"

from .src.harmony import analyze_harmony, get_consecutive_pair, HarmonyReport

__all__ = ["analyze_harmony", "get_consecutive_pair", "HarmonyReport"]