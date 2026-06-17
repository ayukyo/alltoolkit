#!/usr/bin/env python3
"""
Tests for Polyglot Quantum — Language Quantum System Analyzer
Run with: python -m pytest polyglot_quantum/tests/ -v
"""
import json
import os
import sys
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any

import pytest

# Import from package
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from quantum import (
    TOOL_NAME,
    TOOL_VERSION,
    ROTATION_ORDER,
    QUANTUM_SYSTEMS,
    load_rotation,
    save_rotation,
    quantum,
    run_tests,
    compute_entanglement_strength,
    build_uncertainty_bar,
    build_wave_function_bar,
)


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def rotation_config(tmp_path: Path) -> str:
    """Create a temporary rotation config file and return its path."""
    config = {
        "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": 0,
        "last_language": "Rust",
        "updated_at": "2026-06-14T03:00:00+08:00",
    }
    path = tmp_path / "language_rotation.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f)
    return str(path)


@pytest.fixture
def rotation_config_index5(tmp_path: Path) -> str:
    """Create a rotation config at index 5 (JavaScript)."""
    config = {
        "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": 5,
        "last_language": "JavaScript",
        "updated_at": "2026-06-14T03:00:00+08:00",
    }
    path = tmp_path / "language_rotation.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f)
    return str(path)


@pytest.fixture
def rotation_config_last_index(tmp_path: Path) -> str:
    """Create a rotation config at last index (7 = C/C++)."""
    config = {
        "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": 7,
        "last_language": "C/C++",
        "updated_at": "2026-06-14T03:00:00+08:00",
    }
    path = tmp_path / "language_rotation.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f)
    return str(path)


@pytest.fixture
def rotation_config_index0_last(tmp_path: Path) -> str:
    """Create a rotation config at index 0, with save_rotation stubbed."""
    config = {
        "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": 0,
        "last_language": "Rust",
        "updated_at": "2026-06-14T03:00:00+08:00",
    }
    path = tmp_path / "language_rotation.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f)
    return str(path)


# ─────────────────────────────────────────────────────────────────────────────
# Module Constants Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestModuleConstants:
    def test_tool_name(self):
        assert TOOL_NAME == "polyglot-quantum"

    def test_tool_version(self):
        assert TOOL_VERSION == "1.0.0"

    def test_rotation_order_length(self):
        assert len(ROTATION_ORDER) == 8

    def test_rotation_order_sequence(self):
        expected = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]
        assert ROTATION_ORDER == expected

    def test_quantum_systems_has_8_entries(self):
        assert len(QUANTUM_SYSTEMS) == 8

    def test_quantum_systems_has_all_rotation_languages(self):
        for lang in ROTATION_ORDER:
            assert lang in QUANTUM_SYSTEMS, f"Missing {lang} in QUANTUM_SYSTEMS"


# ─────────────────────────────────────────────────────────────────────────────
# Quantum System Data Structure Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestQuantumSystemStructure:
    REQUIRED_FIELDS = {
        "wave_function", "ground_state", "excited_states",
        "uncertainty_principle", "decoherence_pattern",
        "entanglement_pairs", "hamiltonian", "uncertainty_product",
        "quantum_description", "quantum_glyph", "orbital_config",
        "superposition_cardinality", "collapse_mechanism",
        "measurement_disturbance",
    }

    def test_all_languages_have_required_fields(self):
        for lang in ROTATION_ORDER:
            entry = QUANTUM_SYSTEMS[lang]
            missing = self.REQUIRED_FIELDS - entry.keys()
            assert not missing, f"{lang} missing fields: {missing}"

    def test_wave_function_is_list_of_tuples(self):
        for lang in ROTATION_ORDER:
            wf = QUANTUM_SYSTEMS[lang]["wave_function"]
            assert isinstance(wf, list)
            for item in wf:
                assert isinstance(item, tuple)
                assert len(item) == 2
                assert isinstance(item[0], str)
                assert isinstance(item[1], float)
                assert 0.0 <= item[1] <= 1.0

    def test_wave_function_weights_sum_to_1(self):
        for lang in ROTATION_ORDER:
            wf = QUANTUM_SYSTEMS[lang]["wave_function"]
            total = sum(w for _, w in wf)
            assert 0.99 <= total <= 1.01, f"{lang} wave_function weights sum to {total}, not ~1.0"

    def test_excited_states_is_list_of_tuples(self):
        for lang in ROTATION_ORDER:
            es = QUANTUM_SYSTEMS[lang]["excited_states"]
            assert isinstance(es, list)
            assert len(es) > 0
            for item in es:
                assert isinstance(item, tuple)
                assert len(item) == 2
                assert isinstance(item[0], str)
                assert isinstance(item[1], str)

    def test_uncertainty_principle_has_required_fields(self):
        for lang in ROTATION_ORDER:
            up = QUANTUM_SYSTEMS[lang]["uncertainty_principle"]
            assert "dx" in up
            assert "dp" in up
            assert "description" in up

    def test_decoherence_pattern_has_required_fields(self):
        for lang in ROTATION_ORDER:
            dp = QUANTUM_SYSTEMS[lang]["decoherence_pattern"]
            assert "trigger" in dp
            assert "description" in dp
            assert "uncertainty_bits" in dp

    def test_entanglement_pairs_are_4tuples(self):
        for lang in ROTATION_ORDER:
            pairs = QUANTUM_SYSTEMS[lang]["entanglement_pairs"]
            assert isinstance(pairs, list)
            assert len(pairs) >= 2
            for p in pairs:
                assert len(p) == 4
                assert isinstance(p[0], str)  # language
                assert isinstance(p[1], str)  # bond name
                assert isinstance(p[2], (int, float))  # strength
                assert 0.0 <= p[2] <= 1.0
                assert isinstance(p[3], str)  # explanation

    def test_hamiltonian_has_required_fields(self):
        for lang in ROTATION_ORDER:
            h = QUANTUM_SYSTEMS[lang]["hamiltonian"]
            assert "operator" in h
            assert "description" in h
            assert "eigenvalue_label" in h

    def test_uncertainty_product_is_numeric(self):
        for lang in ROTATION_ORDER:
            up = QUANTUM_SYSTEMS[lang]["uncertainty_product"]
            assert isinstance(up, (int, float))
            assert up >= 0.0
            assert up <= 15.0

    def test_superposition_cardinality_is_positive_int(self):
        for lang in ROTATION_ORDER:
            sc = QUANTUM_SYSTEMS[lang]["superposition_cardinality"]
            assert isinstance(sc, int)
            assert sc >= 1

    def test_collapse_mechanism_is_nonempty_string(self):
        for lang in ROTATION_ORDER:
            cm = QUANTUM_SYSTEMS[lang]["collapse_mechanism"]
            assert isinstance(cm, str)
            assert len(cm) > 0

    def test_measurement_disturbance_is_nonempty_string(self):
        for lang in ROTATION_ORDER:
            md = QUANTUM_SYSTEMS[lang]["measurement_disturbance"]
            assert isinstance(md, str)
            assert len(md) > 0

    def test_quantum_description_is_nonempty_string(self):
        for lang in ROTATION_ORDER:
            qd = QUANTUM_SYSTEMS[lang]["quantum_description"]
            assert isinstance(qd, str)
            assert len(qd) > 20  # should be a substantial description

    def test_quantum_glyph_is_emoji(self):
        for lang in ROTATION_ORDER:
            glyph = QUANTUM_SYSTEMS[lang]["quantum_glyph"]
            assert isinstance(glyph, str)
            assert len(glyph) > 0

    def test_orbital_config_is_nonempty_string(self):
        for lang in ROTATION_ORDER:
            oc = QUANTUM_SYSTEMS[lang]["orbital_config"]
            assert isinstance(oc, str)
            assert len(oc) > 5

    def test_cpp_has_highest_uncertainty(self):
        all_up = {lang: QUANTUM_SYSTEMS[lang]["uncertainty_product"] for lang in ROTATION_ORDER}
        assert all_up["C/C++"] == max(all_up.values())

    def test_rust_has_lowest_uncertainty(self):
        all_up = {lang: QUANTUM_SYSTEMS[lang]["uncertainty_product"] for lang in ROTATION_ORDER}
        assert all_up["Rust"] == min(all_up.values())

    def test_all_uncertainty_products_unique(self):
        products = [QUANTUM_SYSTEMS[lang]["uncertainty_product"] for lang in ROTATION_ORDER]
        assert len(products) == len(set(products)), "All uncertainty_products should be unique"


# ─────────────────────────────────────────────────────────────────────────────
# Helper Function Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestHelperFunctions:

    def test_compute_entanglement_strength_basic(self):
        pairs = [
            ("Rust", "Memory Control Entanglement", 0.80, "explanation"),
            ("Swift", "Ownership Protocol Entanglement", 0.75, "explanation"),
        ]
        result = compute_entanglement_strength(pairs)
        assert "average_strength" in result
        assert "strongest_pair" in result
        assert result["average_strength"] == 0.775

    def test_compute_entanglement_strength_empty(self):
        result = compute_entanglement_strength([])
        assert result["average_strength"] == 0.0
        assert result["strongest_pair"] is None

    def test_build_uncertainty_bar_length(self):
        bar = build_uncertainty_bar(12.0)
        assert len(bar) == 20

    def test_build_uncertainty_bar_zero(self):
        bar = build_uncertainty_bar(0.0)
        assert len(bar) == 20
        assert all(c == "░" for c in bar)

    def test_build_uncertainty_bar_max(self):
        bar = build_uncertainty_bar(12.0)
        assert all(c == "█" for c in bar)

    def test_build_uncertainty_bar_mid(self):
        bar = build_uncertainty_bar(6.0)
        filled = bar.count("█")
        assert 0 < filled < 20

    def test_build_wave_function_bar_returns_string(self):
        wf = [("Systems Programming", 0.35), ("Memory Safety", 0.25)]
        result = build_wave_function_bar(wf)
        assert isinstance(result, str)
        assert len(result) > 0
        assert "Systems Programming" in result
        assert "35%" in result


# ─────────────────────────────────────────────────────────────────────────────
# Quantum Function Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestQuantumFunction:

    def test_quantum_returns_dict(self):
        result = quantum()
        assert isinstance(result, dict)

    def test_quantum_result_has_required_keys(self):
        result = quantum()
        required = {
            "tool", "version", "language", "quantum_glyph", "orbital_config",
            "wave_function", "ground_state", "excited_states",
            "uncertainty_principle", "decoherence_pattern",
            "entanglement_pairs", "entanglement_metrics",
            "hamiltonian", "uncertainty_product", "uncertainty_bar",
            "superposition_cardinality", "collapse_mechanism",
            "measurement_disturbance", "quantum_description",
            "wave_function_bar", "rotation_order", "next_language",
            "next_index", "timestamp",
        }
        missing = required - result.keys()
        assert not missing, f"Missing keys: {missing}"

    def test_quantum_tool_name_and_version(self):
        result = quantum()
        assert result["tool"] == "polyglot-quantum"
        assert result["version"] == "1.0.0"

    def test_quantum_language_is_valid(self):
        result = quantum()
        assert result["language"] in ROTATION_ORDER

    def test_quantum_next_language_is_valid(self):
        result = quantum()
        assert result["next_language"] in ROTATION_ORDER
        assert result["next_language"] != result["language"]

    def test_quantum_uncertainty_bar_length_20(self):
        result = quantum()
        assert len(result["uncertainty_bar"]) == 20

    def test_quantum_uncertainty_bar_contains_only_box_chars(self):
        result = quantum()
        assert all(c in "█░" for c in result["uncertainty_bar"])

    def test_quantum_wave_function_bar_is_string(self):
        result = quantum()
        assert isinstance(result["wave_function_bar"], str)
        assert len(result["wave_function_bar"]) > 0

    def test_quantum_entanglement_metrics_structure(self):
        result = quantum()
        em = result["entanglement_metrics"]
        assert "average_strength" in em
        assert "strongest_pair" in em

    def test_quantum_rotation_advances(self, rotation_config_index0_last):
        # Patch ROTATION_FILE
        import quantum as qm
        original = qm.ROTATION_FILE
        qm.ROTATION_FILE = rotation_config_index0_last
        try:
            with open(rotation_config_index0_last) as f:
                before = json.load(f)
            idx_before = before["current_index"]
            lang_before = before["languages"][idx_before]
            result = quantum()
            with open(rotation_config_index0_last) as f:
                after = json.load(f)
            assert after["current_index"] == (idx_before + 1) % 8
            assert result["language"] == lang_before
        finally:
            qm.ROTATION_FILE = original

    def test_quantum_rotation_wraps(self, rotation_config_last_index):
        import quantum as qm
        original = qm.ROTATION_FILE
        qm.ROTATION_FILE = rotation_config_last_index
        try:
            result = quantum()
            assert result["next_index"] == 0
            assert result["next_language"] == "Rust"
        finally:
            qm.ROTATION_FILE = original

    def test_quantum_returns_correct_language_at_index5(self, rotation_config_index5):
        import quantum as qm
        original = qm.ROTATION_FILE
        qm.ROTATION_FILE = rotation_config_index5
        try:
            result = quantum()
            assert result["language"] == "JavaScript"
        finally:
            qm.ROTATION_FILE = original


# ─────────────────────────────────────────────────────────────────────────────
# Round-Robin Sequence Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestRoundRobinSequence:

    def test_full_rotation_sequence(self, tmp_path: Path):
        """Test that all 8 languages are visited in correct order over a full cycle."""
        import quantum as qm
        config = {
            "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
            "current_index": 0,
            "last_language": "Rust",
            "updated_at": "2026-06-14T03:00:00+08:00",
        }
        path = tmp_path / "lang.json"
        with open(path, "w") as f:
            json.dump(config, f)
        original = qm.ROTATION_FILE
        qm.ROTATION_FILE = str(path)
        try:
            visited = []
            for i in range(8):
                qm.load_rotation.cache_clear() if hasattr(qm.load_rotation, 'cache_clear') else None
                result = quantum()
                visited.append(result["language"])
            assert visited == ROTATION_ORDER
        finally:
            qm.ROTATION_FILE = original

    def test_index_wraps_after_full_cycle(self, tmp_path: Path):
        """Test that index wraps back to 0 after a full 8-step cycle."""
        import quantum as qm
        config = {
            "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
            "current_index": 0,
            "last_language": "Rust",
            "updated_at": "2026-06-14T03:00:00+08:00",
        }
        path = tmp_path / "lang.json"
        with open(path, "w") as f:
            json.dump(config, f)
        original = qm.ROTATION_FILE
        qm.ROTATION_FILE = str(path)
        try:
            for _ in range(8):
                quantum()
            with open(path) as f:
                data = json.load(f)
            assert data["current_index"] == 0
        finally:
            qm.ROTATION_FILE = original


# ─────────────────────────────────────────────────────────────────────────────
# Uncertainty Product Ordering Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestUncertaintyOrdering:

    def test_cpp_highest_uncertainty(self):
        """C/C++ should have the highest uncertainty product (undefined behavior)."""
        up = {lang: QUANTUM_SYSTEMS[lang]["uncertainty_product"] for lang in ROTATION_ORDER}
        assert up["C/C++"] == max(up.values())

    def test_rust_lowest_uncertainty(self):
        """Rust should have the lowest uncertainty product (compile-time safety)."""
        up = {lang: QUANTUM_SYSTEMS[lang]["uncertainty_product"] for lang in ROTATION_ORDER}
        assert up["Rust"] == min(up.values())

    def test_js_second_highest(self):
        """JavaScript should have second-highest uncertainty (prototype + event loop)."""
        up = {lang: QUANTUM_SYSTEMS[lang]["uncertainty_product"] for lang in ROTATION_ORDER}
        sorted_langs = sorted(up, key=up.get, reverse=True)
        assert sorted_langs[0] == "C/C++"
        assert sorted_langs[1] == "JavaScript"

    def test_typescript_lowest_after_rust(self):
        """TypeScript should have low uncertainty (type erasure collapses cleanly)."""
        up = {lang: QUANTUM_SYSTEMS[lang]["uncertainty_product"] for lang in ROTATION_ORDER}
        assert up["TypeScript"] < up["Java"]
        assert up["TypeScript"] < up["Go"]

    def test_all_uncertainty_products_increasing_order(self):
        """Uncertainty products should be strictly ordered across the 8 languages."""
        up = {lang: QUANTUM_SYSTEMS[lang]["uncertainty_product"] for lang in ROTATION_ORDER}
        sorted_vals = sorted(up.values())
        assert len(sorted_vals) == len(set(sorted_vals)), "All uncertainty_product values must be unique"

    def test_superposition_cardinality_max_for_cpp(self):
        """C/C++ should have the maximum superposition cardinality."""
        sc = {lang: QUANTUM_SYSTEMS[lang]["superposition_cardinality"] for lang in ROTATION_ORDER}
        assert sc["C/C++"] == max(sc.values())

    def test_superposition_cardinality_min_for_rust(self):
        """Rust should have the minimum superposition cardinality."""
        sc = {lang: QUANTUM_SYSTEMS[lang]["superposition_cardinality"] for lang in ROTATION_ORDER}
        assert sc["Rust"] == min(sc.values())


# ─────────────────────────────────────────────────────────────────────────────
# Entanglement Pairs Validity Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestEntanglementPairs:

    def test_all_languages_have_at_least_2_entanglement_pairs(self):
        for lang in ROTATION_ORDER:
            pairs = QUANTUM_SYSTEMS[lang]["entanglement_pairs"]
            assert len(pairs) >= 2, f"{lang} should have at least 2 entanglement pairs"

    def test_entanglement_strengths_are_valid_floats(self):
        for lang in ROTATION_ORDER:
            for p in QUANTUM_SYSTEMS[lang]["entanglement_pairs"]:
                assert isinstance(p[2], (int, float))
                assert 0.0 <= p[2] <= 1.0

    def test_entangled_languages_are_in_rotation(self):
        for lang in ROTATION_ORDER:
            for p in QUANTUM_SYSTEMS[lang]["entanglement_pairs"]:
                assert p[0] in ROTATION_ORDER, f"{lang} entangled with {p[0]} which is not in ROTATION_ORDER"

    def test_no_language_is_entangled_with_itself(self):
        for lang in ROTATION_ORDER:
            for p in QUANTUM_SYSTEMS[lang]["entanglement_pairs"]:
                assert p[0] != lang, f"{lang} is entangled with itself"

    def test_rust_cpp_entanglement_exists(self):
        """Rust should be entangled with C/C++."""
        rust_pairs = [p[0] for p in QUANTUM_SYSTEMS["Rust"]["entanglement_pairs"]]
        assert "C/C++" in rust_pairs

    def test_ts_js_entanglement_is_strongest_for_ts(self):
        """TypeScript's strongest entanglement should be with JavaScript."""
        ts_pairs = QUANTUM_SYSTEMS["TypeScript"]["entanglement_pairs"]
        strongest = max(ts_pairs, key=lambda p: p[2])
        assert strongest[0] == "JavaScript"

    def test_swift_kotlin_entanglement_is_very_strong(self):
        """Swift↔Kotlin entanglement should be ≥ 0.85."""
        swift_pairs = {p[0]: p[2] for p in QUANTUM_SYSTEMS["Swift"]["entanglement_pairs"]}
        assert swift_pairs.get("Kotlin", 0) >= 0.85


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
