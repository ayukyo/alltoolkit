#!/usr/bin/env python3
"""Tests for polyglot_topology — topology functions."""

import importlib.util
import sys
import unittest
from pathlib import Path

# Load the module using importlib (the src/__init__.py is the main module file)
_spec = importlib.util.spec_from_file_location(
    "polyglot_topology",
    Path(__file__).parent.parent / "src" / "__init__.py"
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

TOOL_NAME = _mod.TOOL_NAME
TOOL_VERSION = _mod.TOOL_VERSION
ROTATION_ORDER = _mod.ROTATION_ORDER
FEATURE_VECTORS = _mod.FEATURE_VECTORS
NEIGHBORHOOD_GRAPH = _mod.NEIGHBORHOOD_GRAPH
BOUNDARY_LINES = _mod.BOUNDARY_LINES
load_rotation = _mod.load_rotation
save_rotation = _mod.save_rotation
_render_topology_map = _mod._render_topology_map
_compute_topological_metrics = _mod._compute_topological_metrics
topology = _mod.topology
compute_topology = _mod.compute_topology
format_topology = _mod.format_topology


class TestConstants(unittest.TestCase):
    def test_tool_name(self):
        self.assertEqual(TOOL_NAME, "polyglot-topology")

    def test_tool_version(self):
        self.assertEqual(TOOL_VERSION, "1.0.0")

    def test_rotation_order(self):
        self.assertEqual(ROTATION_ORDER, [
            "Rust", "Go", "Swift", "Kotlin",
            "TypeScript", "JavaScript", "Java", "C/C++",
        ])

    def test_feature_vectors_all_8(self):
        for lang in ROTATION_ORDER:
            self.assertIn(lang, FEATURE_VECTORS, f"{lang} missing")

    def test_neighborhood_graph_all_8(self):
        for lang in ROTATION_ORDER:
            self.assertIn(lang, NEIGHBORHOOD_GRAPH, f"{lang} missing from NEIGHBORHOOD_GRAPH")


class TestRenderMap(unittest.TestCase):
    def test_render_topology_map_returns_list(self):
        result = _render_topology_map("Rust")
        self.assertIsInstance(result, list)

    def test_render_topology_map_all_languages(self):
        for lang in ROTATION_ORDER:
            result = _render_topology_map(lang)
            self.assertIsInstance(result, list)
            self.assertTrue(len(result) > 0)

    def test_render_topology_map_contains_language_name(self):
        for lang in ROTATION_ORDER:
            result = _render_topology_map(lang)
            joined = "\n".join(result)
            self.assertIn(lang, joined)


class TestMetrics(unittest.TestCase):
    def test_compute_topological_metrics_returns_dict(self):
        result = _compute_topological_metrics("Rust")
        self.assertIsInstance(result, dict)

    def test_compute_topological_metrics_all_languages(self):
        for lang in ROTATION_ORDER:
            result = _compute_topological_metrics(lang)
            self.assertIn("neighbors", result)
            self.assertIn("distances", result)

    def test_compute_topological_metrics_has_signature(self):
        for lang in ROTATION_ORDER:
            result = _compute_topological_metrics(lang)
            self.assertIn("topological_signature", result)


class TestRotation(unittest.TestCase):
    ROTATION_FILE = str(Path(__file__).parent.parent.parent / "language_rotation.json")

    def _save(self):
        with open(self.ROTATION_FILE) as f:
            return f.read()

    def _restore(self, data):
        with open(self.ROTATION_FILE, "w") as f:
            f.write(data)

    def test_load_rotation_returns_dict(self):
        saved = self._save()
        try:
            cfg = load_rotation()
            self.assertIsInstance(cfg, dict)
        finally:
            self._restore(saved)


class TestTopologyMain(unittest.TestCase):
    ROTATION_FILE = str(Path(__file__).parent.parent.parent / "language_rotation.json")

    def _save(self):
        with open(self.ROTATION_FILE) as f:
            return f.read()

    def _restore(self, data):
        with open(self.ROTATION_FILE, "w") as f:
            f.write(data)

    def test_topology_returns_dict(self):
        saved = self._save()
        try:
            result = topology()
            self.assertIsInstance(result, dict)
        finally:
            self._restore(saved)

    def test_topology_has_language_and_map(self):
        saved = self._save()
        try:
            result = topology()
            self.assertIn("language", result)
            self.assertIn("topology_map", result)
            self.assertIn("next_language", result)
        finally:
            self._restore(saved)

    def test_topology_advances_rotation(self):
        saved = self._save()
        try:
            cfg_before = load_rotation()
            idx_before = cfg_before["current_index"]
            topology()
            cfg_after = load_rotation()
            self.assertEqual(cfg_after["current_index"], (idx_before + 1) % 8)
        finally:
            self._restore(saved)


class TestComputeTopology(unittest.TestCase):
    def test_compute_topology_returns_dict(self):
        result = compute_topology("Rust")
        self.assertIsInstance(result, dict)

    def test_compute_topology_all_languages(self):
        for lang in ROTATION_ORDER:
            result = compute_topology(lang)
            self.assertIn("language", result)
            self.assertIn("topology_map", result)

    def test_compute_topology_unknown_language_raises_valueerror(self):
        with self.assertRaises(ValueError):
            compute_topology("Brainfuck")


class TestFormatTopology(unittest.TestCase):
    def test_format_topology_returns_string(self):
        result = compute_topology("Go")
        txt = format_topology(result)
        self.assertIsInstance(txt, str)
        self.assertTrue(len(txt) > 0)


if __name__ == "__main__":
    unittest.main()
