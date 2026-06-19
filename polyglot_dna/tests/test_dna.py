#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for polyglot_dna module.
"""

import json
import os
import sys
import pytest
from pathlib import Path

# Build correct path to module
POLYGLOT_ROOT = Path(__file__).parent.parent.parent
ROTATION_FILE = str(POLYGLOT_ROOT / "language_rotation.json")

# Patch ROTATION_FILE before importing
import polyglot_dna
polyglot_dna.ROTATION_FILE = ROTATION_FILE

from polyglot_dna import (
    TOOL_NAME,
    TOOL_VERSION,
    LANGUAGE_DNA,
    GENE_NAMES,
    GENE_LEGENDS,
    NUCLEOTIDE_MEANING,
    COMPLEMENT,
    _normalize,
    _gap,
    _annotate_gene,
    generate_dna_sequence,
    compare_dna,
    compatibility_score,
    dna,
    load_rotation,
)


ROTATION_ORDER = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]


class TestModuleMetadata:
    """Test module constants."""

    def test_tool_name(self):
        assert TOOL_NAME == "polyglot-dna"

    def test_tool_version(self):
        assert TOOL_VERSION == "1.0.0"


class TestNucleotideConstants:
    """Test nucleotide and complement constants."""

    def test_complement_is_symmetric(self):
        for base, comp in COMPLEMENT.items():
            assert COMPLEMENT[comp] == base

    def test_complement_has_4_bases(self):
        assert set(COMPLEMENT.keys()) == {"A", "T", "G", "C"}


class TestLanguageDNA:
    """Test LANGUAGE_DNA data structure."""

    def test_all_8_languages_have_dna(self):
        for lang in ROTATION_ORDER:
            assert lang in LANGUAGE_DNA, f"{lang} missing DNA"

    def test_dna_sequences_have_correct_gene_count(self):
        for lang, seq in LANGUAGE_DNA.items():
            norm = _normalize(seq)
            assert len(norm) == len(GENE_NAMES) * 2, \
                f"{lang} has {len(norm)} nucleotides, expected {len(GENE_NAMES) * 2}"

    def test_gene_names_count(self):
        assert len(GENE_NAMES) == 10


class TestNormalize:
    """Test _normalize helper function."""

    def test_removes_dashes(self):
        assert _normalize("TC-GT-CT") == "TCGTCT"

    def test_preserves_nucleotides(self):
        assert _normalize("ACGT") == "ACGT"


class TestGap:
    """Test _gap helper function."""

    def test_returns_gene_at_position(self):
        seq = "TC-GT-CT-GC-AC"
        assert _gap(seq, 0) == "TC-"
        assert _gap(seq, 1) == "GT-"
        assert _gap(seq, 2) == "CT-"

    def test_last_gene(self):
        seq = "TC-GT-CT-GC-AC"
        assert _gap(seq, 4) == "AC"


class TestAnnotateGene:
    """Test _annotate_gene function."""

    def test_returns_dict(self):
        result = _annotate_gene("TC-GT-CT-GC-AC", 0)
        assert isinstance(result, dict)

    def test_returns_required_keys(self):
        result = _annotate_gene("TC-GT-CT-GC-AC", 0)
        assert "position" in result
        assert "nucleotide" in result
        assert "gene_name" in result
        assert "meaning" in result

    def test_position_matches_gene_index(self):
        result = _annotate_gene("TC-GT-CT-GC-AC", 2)
        assert result["position"] == 2

    def test_nucleotide_is_first_char(self):
        result = _annotate_gene("GT-", 0)
        assert result["nucleotide"] == "G"


class TestGenerateDNASequence:
    """Test generate_dna_sequence function."""

    def test_returns_dict(self):
        result = generate_dna_sequence("Rust")
        assert isinstance(result, dict)

    def test_returns_language(self):
        result = generate_dna_sequence("Go")
        assert result["language"] == "Go"

    def test_returns_dna_sequence(self):
        result = generate_dna_sequence("Swift")
        assert "dna_sequence" in result
        assert isinstance(result["dna_sequence"], str)

    def test_returns_normalized_sequence(self):
        result = generate_dna_sequence("Rust")
        assert "dna_normalized" in result
        assert "-" not in result["dna_normalized"]

    def test_returns_length_bp(self):
        result = generate_dna_sequence("Kotlin")
        assert result["length_bp"] == len(GENE_NAMES) * 2

    def test_returns_gene_count(self):
        result = generate_dna_sequence("TypeScript")
        assert result["gene_count"] == len(GENE_NAMES)

    def test_returns_genes_list(self):
        result = generate_dna_sequence("JavaScript")
        assert isinstance(result["genes"], list)
        assert len(result["genes"]) == len(GENE_NAMES)

    def test_gene_positions_are_sequential(self):
        result = generate_dna_sequence("Java")
        positions = [g["position"] for g in result["genes"]]
        assert positions == list(range(len(GENE_NAMES)))

    def test_gene_has_required_fields(self):
        result = generate_dna_sequence("C/C++")
        for gene in result["genes"]:
            assert all(k in gene for k in ["position", "nucleotide", "gene_name", "meaning"])

    def test_returns_helix_art(self):
        result = generate_dna_sequence("Rust")
        assert "helix_art" in result
        assert isinstance(result["helix_art"], str)

    def test_unknown_language_raises_value_error(self):
        with pytest.raises(ValueError) as excinfo:
            generate_dna_sequence("Python")
        assert "Python" in str(excinfo.value)


class TestCompareDNA:
    """Test compare_dna function."""

    def test_returns_dict(self):
        result = compare_dna("Rust", "Go")
        assert isinstance(result, dict)

    def test_returns_language_a_and_b(self):
        result = compare_dna("Swift", "Kotlin")
        assert result["language_a"] == "Swift"
        assert result["language_b"] == "Kotlin"

    def test_returns_similarity_score(self):
        result = compare_dna("Rust", "Go")
        assert "similarity_score" in result
        assert 0 <= result["similarity_score"] <= 1

    def test_returns_mutation_count(self):
        result = compare_dna("Rust", "Go")
        assert "mutation_count" in result
        assert isinstance(result["mutation_count"], int)

    def test_returns_mutations_list(self):
        result = compare_dna("Rust", "Go")
        assert isinstance(result["mutations"], list)

    def test_is_symmetric(self):
        ab = compare_dna("Rust", "Go")
        ba = compare_dna("Go", "Rust")
        assert ab["similarity_score"] == ba["similarity_score"]
        assert ab["mutation_count"] == ba["mutation_count"]

    def test_mutation_has_required_fields(self):
        result = compare_dna("Rust", "Go")
        for mutation in result["mutations"]:
            assert "position" in mutation
            assert "gene_index" in mutation
            assert "gene_name" in mutation
            assert "Rust_base" in mutation
            assert "Go_base" in mutation

    def test_same_language_has_zero_mutations(self):
        result = compare_dna("Rust", "Rust")
        assert result["mutation_count"] == 0
        assert result["similarity_score"] == 1.0

    def test_returns_summary(self):
        result = compare_dna("Rust", "Go")
        assert "summary" in result
        assert isinstance(result["summary"], str)


class TestCompatibilityScore:
    """Test compatibility_score function."""

    def test_returns_dict(self):
        result = compatibility_score("JavaScript", "TypeScript")
        assert isinstance(result, dict)

    def test_returns_from_and_to(self):
        result = compatibility_score("Go", "Rust")
        assert result["from"] == "Go"
        assert result["to"] == "Rust"

    def test_returns_similarity(self):
        result = compatibility_score("Go", "Rust")
        assert "similarity" in result

    def test_returns_difficulty(self):
        result = compatibility_score("Go", "Rust")
        assert "difficulty" in result
        assert isinstance(result["difficulty"], str)

    def test_difficulty_is_non_empty(self):
        for lang_a in ROTATION_ORDER:
            for lang_b in ROTATION_ORDER:
                result = compatibility_score(lang_a, lang_b)
                assert len(result["difficulty"]) > 0

    def test_returns_note(self):
        result = compatibility_score("JavaScript", "TypeScript")
        assert "note" in result
        assert isinstance(result["note"], str)


class TestDNAFunction:
    """Test dna() rotation-aware entry point."""

    def test_returns_dict(self):
        result = dna()
        assert isinstance(result, dict)

    def test_returns_language(self):
        result = dna()
        assert "language" in result

    def test_returns_rotation_advanced(self):
        result = dna()
        assert result.get("rotation_advanced") is True

    def test_returns_next_language(self):
        result = dna()
        assert "next_language" in result
        assert result["next_language"] in ROTATION_ORDER

    def test_advances_rotation(self):
        config_before = load_rotation()
        idx_before = config_before["current_index"]
        dna()
        config_after = load_rotation()
        expected = (idx_before + 1) % len(config_before["languages"])
        assert config_after["current_index"] == expected


class TestGeneLegends:
    """Test GENE_LEGENDS data structure."""

    def test_all_gene_positions_have_legends(self):
        for i in range(len(GENE_NAMES)):
            assert i in GENE_LEGENDS, f"Gene position {i} missing legend"

    def test_each_legend_has_meaning_for_each_base(self):
        for gene_idx, legend in GENE_LEGENDS.items():
            for base in ["A", "C", "T", "G"]:
                assert base in legend, f"Gene {gene_idx} missing base {base}"
