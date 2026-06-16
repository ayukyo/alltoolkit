#!/usr/bin/env python3
"""
Tests for polyglot_ecosystem_map module.
Run with: python -m pytest polyglot_ecosystem_map/tests/ -v
"""
import json
import os
import sys
import tempfile
import shutil
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
import polyglot_ecosystem_map as pem

from polyglot_ecosystem_map import (
    PARADIGM_VECTORS, ECOSYSTEMS, INFLUENCE_CHAINS, SYNERGY_PAIRS,
    _cosine_similarity, _ecosystem_distance, _influence_distance,
    calculate_relationship, find_ecosystem_neighbors,
    generate_ecosystem_map, get_rotation_state, rotate_and_update,
    _score_to_label,
)


class TestPolyglotEcosystemMap(unittest.TestCase):
    """Test suite for Polyglot Ecosystem Map."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.rotation_file = os.path.join(self.test_dir, "language_rotation.json")

        self.test_data = {
            "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
            "current_index": 0,
            "last_language": None,
            "updated_at": "2026-01-01T00:00:00+00:00",
        }
        with open(self.rotation_file, "w") as f:
            json.dump(self.test_data, f)
        
        # Monkey-patch the ROTATION_FILE in the module to use our test file
        # so get_rotation_state() finds the test file
        import polyglot_ecosystem_map as pem_module
        pem_module.ROTATION_FILE = self.rotation_file

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
        import polyglot_ecosystem_map as pem_module
        # Restore original path (it reads from module-level constant paths)
        # The actual rotation file is at the repo root

    # ── Cosine similarity ────────────────────────────────────────────────────

    def test_cosine_identical_vectors(self):
        sim = _cosine_similarity([1.0, 2.0, 3.0], [1.0, 2.0, 3.0])
        self.assertAlmostEqual(sim, 1.0, places=9)

    def test_cosine_orthogonal_vectors(self):
        sim = _cosine_similarity([1.0, 0.0], [0.0, 1.0])
        self.assertAlmostEqual(sim, 0.0, places=9)

    def test_cosine_negative(self):
        sim = _cosine_similarity([1.0, 0.0], [-1.0, 0.0])
        self.assertAlmostEqual(sim, -1.0, places=9)

    def test_cosine_zero_vector(self):
        sim = _cosine_similarity([0.0, 0.0], [1.0, 1.0])
        self.assertEqual(sim, 0.0)

    # ── Ecosystem distance ────────────────────────────────────────────────────

    def test_ecosystem_same_cluster(self):
        # Rust and Go are both in "systems"
        dist = _ecosystem_distance("Rust", "Go")
        self.assertEqual(dist, 0.0)

    def test_ecosystem_different_clusters(self):
        dist = _ecosystem_distance("Python", "Rust")
        self.assertGreater(dist, 0.0)

    def test_ecosystem_identical(self):
        dist = _ecosystem_distance("Rust", "Rust")
        self.assertEqual(dist, 0.0)

    # ── Influence distance ───────────────────────────────────────────────────

    def test_influence_direct(self):
        dist = _influence_distance("Java", "C/C++")
        self.assertEqual(dist, 0.2)  # 1 hop / 5.0

    def test_influence_chain(self):
        dist = _influence_distance("Kotlin", "C/C++")
        # Kotlin -> Java -> C/C++ = 2 hops = 0.4
        self.assertAlmostEqual(dist, 0.4, places=1)

    def test_influence_no_connection(self):
        # Lua and SQL are far apart in the influence chain
        dist = _influence_distance("Lua", "SQL")
        self.assertEqual(dist, 1.0)

    # ── Relationship calculation ─────────────────────────────────────────────

    def test_relationship_symmetric(self):
        rel_ab = calculate_relationship("Rust", "Go")
        rel_ba = calculate_relationship("Go", "Rust")
        self.assertAlmostEqual(rel_ab["relationship_score"], rel_ba["relationship_score"], places=1)

    def test_relationship_self_highest(self):
        rel_self = calculate_relationship("Rust", "Rust")
        rel_rust_go = calculate_relationship("Rust", "Go")
        self.assertGreaterEqual(rel_self["relationship_score"], rel_rust_go["relationship_score"])

    def test_relationship_score_range(self):
        for lang_a in list(PARADIGM_VECTORS.keys())[:5]:
            for lang_b in list(PARADIGM_VECTORS.keys())[:5]:
                rel = calculate_relationship(lang_a, lang_b)
                self.assertGreaterEqual(rel["relationship_score"], 0.0)
                self.assertLessEqual(rel["relationship_score"], 100.0)

    def test_relationship_has_required_fields(self):
        rel = calculate_relationship("Rust", "Go")
        for field in ["paradigm_similarity", "ecosystem_distance", "influence_distance",
                       "synergy_score", "relationship_score", "relationship_label"]:
            self.assertIn(field, rel)

    def test_relationship_label_valid(self):
        for lang in list(PARADIGM_VECTORS.keys())[:4]:
            rel = calculate_relationship(lang, "C/C++")
            self.assertIn(rel["relationship_label"], [
                "tightly coupled", "compatible", "neutral", "divergent", "foreign territory"
            ])

    # ── Score to label ───────────────────────────────────────────────────────

    def test_score_to_label_tightly_coupled(self):
        self.assertEqual(_score_to_label(85), "tightly coupled")
        self.assertEqual(_score_to_label(100), "tightly coupled")

    def test_score_to_label_compatible(self):
        self.assertEqual(_score_to_label(65), "compatible")

    def test_score_to_label_neutral(self):
        self.assertEqual(_score_to_label(45), "neutral")

    def test_score_to_label_divergent(self):
        self.assertEqual(_score_to_label(25), "divergent")

    def test_score_to_label_foreign(self):
        self.assertEqual(_score_to_label(5), "foreign territory")

    # ── Ecosystem neighbors ──────────────────────────────────────────────────

    def test_ecosystem_neighbors_count(self):
        neighbors = find_ecosystem_neighbors("Rust", top_n=3)
        self.assertEqual(len(neighbors), 3)

    def test_ecosystem_neighbors_sorted(self):
        neighbors = find_ecosystem_neighbors("Rust", top_n=5)
        scores = [n["relationship_score"] for n in neighbors]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_ecosystem_neighbors_has_scores(self):
        neighbors = find_ecosystem_neighbors("Rust", top_n=3)
        for n in neighbors:
            self.assertIn("relationship_score", n)
            self.assertIn("language_a", n)
            self.assertIn("language_b", n)

    # ── Ecosystem map ────────────────────────────────────────────────────────

    def test_ecosystem_map_has_required_fields(self):
        eco = generate_ecosystem_map("Rust")
        for field in ["current_language", "ecosystem_cluster", "influenced_by",
                       "neighbors", "paradigm_vector", "paradigm_labels"]:
            self.assertIn(field, eco)

    def test_ecosystem_map_cluster_correct(self):
        eco = generate_ecosystem_map("Rust")
        self.assertEqual(eco["ecosystem_cluster"], "systems")

    def test_ecosystem_map_paradigm_vector_length(self):
        eco = generate_ecosystem_map("Rust")
        self.assertEqual(len(eco["paradigm_vector"]), 5)
        self.assertEqual(len(eco["paradigm_labels"]), 5)

    def test_ecosystem_map_unknown_language(self):
        eco = generate_ecosystem_map("UnknownLang")
        self.assertEqual(eco["ecosystem_cluster"], "unknown")

    # ── Rotation state ────────────────────────────────────────────────────────

    def test_get_rotation_state_returns_dict(self):
        state = get_rotation_state()
        self.assertIsInstance(state, dict)

    def test_get_rotation_state_has_required_keys(self):
        state = get_rotation_state()
        self.assertIn("languages", state)
        self.assertIn("current_index", state)


if __name__ == "__main__":
    unittest.main(verbosity=2)
