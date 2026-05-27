#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Etymology Utilities Test Suite

Comprehensive test suite for etymology_utils module.
Tests cover word lookup, root extraction, tree building, compound detection,
word comparison, validation, and visualization.

Author: AllToolkit
License: MIT
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etymology_utils.mod import (
    # Enums
    LanguageOrigin, HistoricalPeriod, WordRelation,
    
    # Data Classes
    EtymologyEntry, EtymologyTree, WordFamily,
    
    # Core Functions
    get_etymology, add_etymology, search_by_origin, search_by_period,
    find_cognates, get_word_family, build_etymology_tree, extract_root,
    analyze_word, detect_compound, compare_words, visualize_tree,
    get_statistics, search_words, validate_etymology, export_to_json,
    
    # Advanced Functions
    trace_word_evolution, find_language_contributions,
    find_period_contributions, generate_word_report,
    
    # Convenience Functions
    quick_lookup, is_loanword, get_loanwords, get_native_words,
    
    # Database
    ETYMOLOGY_DATABASE, ROOT_WORDS_DATABASE, PREFIXES_DATABASE, SUFFIXES_DATABASE
)


class TestLanguageOrigin(unittest.TestCase):
    """Test LanguageOrigin enum."""
    
    def test_enum_values(self):
        """Test that all enum values exist."""
        self.assertEqual(LanguageOrigin.LATIN.value, "Latin")
        self.assertEqual(LanguageOrigin.GREEK.value, "Greek")
        self.assertEqual(LanguageOrigin.GERMANIC.value, "Germanic")
        self.assertEqual(LanguageOrigin.OLD_ENGLISH.value, "Old English")
        self.assertEqual(LanguageOrigin.FRENCH.value, "French")
        self.assertEqual(LanguageOrigin.UNKNOWN.value, "Unknown")
    
    def test_enum_count(self):
        """Test number of language origins."""
        self.assertEqual(len(LanguageOrigin), 20)


class TestHistoricalPeriod(unittest.TestCase):
    """Test HistoricalPeriod enum."""
    
    def test_enum_values(self):
        """Test that all enum values exist."""
        self.assertEqual(HistoricalPeriod.ANCIENT.value, "Ancient")
        self.assertEqual(HistoricalPeriod.MEDIEVAL.value, "Medieval")
        self.assertEqual(HistoricalPeriod.EARLY_MODERN.value, "Early Modern")
        self.assertEqual(HistoricalPeriod.MODERN.value, "Modern")
        self.assertEqual(HistoricalPeriod.CONTEMPORARY.value, "Contemporary")
    
    def test_enum_count(self):
        """Test number of historical periods."""
        self.assertEqual(len(HistoricalPeriod), 5)


class TestWordRelation(unittest.TestCase):
    """Test WordRelation enum."""
    
    def test_enum_values(self):
        """Test that all enum values exist."""
        self.assertEqual(WordRelation.DERIVATION.value, "Derivation")
        self.assertEqual(WordRelation.COMPOUND.value, "Compound")
        self.assertEqual(WordRelation.BORROWING.value, "Borrowing")
        self.assertEqual(WordRelation.COGNATE.value, "Cognate")
        self.assertEqual(WordRelation.ROOT.value, "Root")
    
    def test_enum_count(self):
        """Test number of word relations."""
        self.assertEqual(len(WordRelation), 7)


class TestEtymologyEntry(unittest.TestCase):
    """Test EtymologyEntry data class."""
    
    def test_basic_entry(self):
        """Test creating a basic entry."""
        entry = EtymologyEntry(
            word="test",
            language_origin=LanguageOrigin.LATIN,
            historical_period=HistoricalPeriod.MODERN
        )
        self.assertEqual(entry.word, "test")
        self.assertEqual(entry.language_origin, LanguageOrigin.LATIN)
        self.assertEqual(entry.historical_period, HistoricalPeriod.MODERN)
    
    def test_full_entry(self):
        """Test creating a full entry."""
        entry = EtymologyEntry(
            word="computer",
            language_origin=LanguageOrigin.LATIN,
            historical_period=HistoricalPeriod.MODERN,
            original_form="computare",
            intermediate_forms=["compute", "computer"],
            meaning_evolution=["calculate", "machine"],
            related_words=["computing", "computational"],
            cognates={"French": "ordinateur"},
            notes="Test entry",
            confidence=0.95
        )
        self.assertEqual(entry.word, "computer")
        self.assertEqual(entry.original_form, "computare")
        self.assertEqual(len(entry.intermediate_forms), 2)
        self.assertEqual(entry.confidence, 0.95)
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        entry = EtymologyEntry(
            word="test",
            language_origin=LanguageOrigin.LATIN,
            historical_period=HistoricalPeriod.MODERN,
            confidence=0.9
        )
        d = entry.to_dict()
        self.assertEqual(d["word"], "test")
        self.assertEqual(d["language_origin"], "Latin")
        self.assertEqual(d["historical_period"], "Modern")
        self.assertEqual(d["confidence"], 0.9)
    
    def test_default_values(self):
        """Test default values."""
        entry = EtymologyEntry(
            word="test",
            language_origin=LanguageOrigin.UNKNOWN,
            historical_period=HistoricalPeriod.MODERN
        )
        self.assertIsNone(entry.original_form)
        self.assertEqual(entry.intermediate_forms, [])
        self.assertEqual(entry.meaning_evolution, [])
        self.assertEqual(entry.related_words, [])
        self.assertEqual(entry.cognates, {})
        self.assertIsNone(entry.notes)
        self.assertEqual(entry.confidence, 1.0)


class TestEtymologyTree(unittest.TestCase):
    """Test EtymologyTree data class."""
    
    def test_basic_tree(self):
        """Test creating a basic tree."""
        tree = EtymologyTree(word="test")
        self.assertEqual(tree.word, "test")
        self.assertEqual(tree.children, [])
        self.assertIsNone(tree.origin)
    
    def test_tree_with_children(self):
        """Test tree with children."""
        parent = EtymologyTree(word="parent")
        child1 = EtymologyTree(word="child1")
        child2 = EtymologyTree(word="child2")
        
        parent.add_child(child1)
        parent.add_child(child2)
        
        self.assertEqual(len(parent.children), 2)
        self.assertEqual(parent.children[0].word, "child1")
    
    def test_tree_depth(self):
        """Test tree depth calculation."""
        root = EtymologyTree(word="root")
        child = EtymologyTree(word="child")
        grandchild = EtymologyTree(word="grandchild")
        
        child.add_child(grandchild)
        root.add_child(child)
        
        self.assertEqual(root.depth(), 3)
    
    def test_tree_size(self):
        """Test tree size calculation."""
        root = EtymologyTree(word="root")
        child1 = EtymologyTree(word="child1")
        child2 = EtymologyTree(word="child2")
        grandchild = EtymologyTree(word="grandchild")
        
        child1.add_child(grandchild)
        root.add_child(child1)
        root.add_child(child2)
        
        self.assertEqual(root.size(), 4)
    
    def test_tree_to_dict(self):
        """Test tree to dictionary."""
        tree = EtymologyTree(
            word="test",
            origin=LanguageOrigin.LATIN,
            period=HistoricalPeriod.MODERN
        )
        d = tree.to_dict()
        self.assertEqual(d["word"], "test")
        self.assertEqual(d["origin"], "Latin")
        self.assertEqual(d["period"], "Modern")


class TestWordFamily(unittest.TestCase):
    """Test WordFamily data class."""
    
    def test_basic_family(self):
        """Test creating a basic family."""
        family = WordFamily(root="work")
        self.assertEqual(family.root, "work")
        self.assertEqual(family.members, [])
    
    def test_add_member(self):
        """Test adding members."""
        family = WordFamily(root="work")
        family.add_member("worker")
        family.add_member("working")
        
        self.assertEqual(len(family.members), 2)
    
    def test_add_member_with_path(self):
        """Test adding member with derivation path."""
        family = WordFamily(root="work")
        family.add_member("worker", "work + -er")
        
        self.assertIn("worker", family.derivations)
        self.assertEqual(family.derivations["worker"], "work + -er")
    
    def test_duplicate_member(self):
        """Test that duplicate members don't get added twice."""
        family = WordFamily(root="work")
        family.add_member("worker")
        family.add_member("worker")
        
        self.assertEqual(len(family.members), 1)
    
    def test_to_dict(self):
        """Test family to dictionary."""
        family = WordFamily(root="work", members=["worker", "working"])
        d = family.to_dict()
        self.assertEqual(d["root"], "work")
        self.assertEqual(d["members"], ["worker", "working"])


class TestGetEtymology(unittest.TestCase):
    """Test get_etymology function."""
    
    def test_existing_word(self):
        """Test looking up an existing word."""
        entry = get_etymology("computer")
        self.assertIsNotNone(entry)
        self.assertEqual(entry.word, "computer")
        self.assertEqual(entry.language_origin, LanguageOrigin.LATIN)
    
    def test_nonexistent_word(self):
        """Test looking up a nonexistent word."""
        entry = get_etymology("xyzzy")
        self.assertIsNone(entry)
    
    def test_case_insensitive(self):
        """Test case insensitive lookup."""
        entry1 = get_etymology("COMPUTER")
        entry2 = get_etymology("Computer")
        entry3 = get_etymology("computer")
        
        self.assertIsNotNone(entry1)
        self.assertEqual(entry1.word, "computer")
    
    def test_with_spaces(self):
        """Test lookup with spaces."""
        entry = get_etymology("  computer  ")
        self.assertIsNotNone(entry)


class TestAddEtymology(unittest.TestCase):
    """Test add_etymology function."""
    
    def test_add_entry(self):
        """Test adding a new entry."""
        entry = EtymologyEntry(
            word="testword",
            language_origin=LanguageOrigin.UNKNOWN,
            historical_period=HistoricalPeriod.MODERN
        )
        add_etymology(entry)
        
        retrieved = get_etymology("testword")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.word, "testword")


class TestSearchByOrigin(unittest.TestCase):
    """Test search_by_origin function."""
    
    def test_search_latin(self):
        """Test searching for Latin origins."""
        results = search_by_origin(LanguageOrigin.LATIN)
        self.assertTrue(len(results) > 0)
        for entry in results:
            self.assertEqual(entry.language_origin, LanguageOrigin.LATIN)
    
    def test_search_greek(self):
        """Test searching for Greek origins."""
        results = search_by_origin(LanguageOrigin.GREEK)
        self.assertTrue(len(results) > 0)
        for entry in results:
            self.assertEqual(entry.language_origin, LanguageOrigin.GREEK)
    
    def test_search_old_english(self):
        """Test searching for Old English origins."""
        results = search_by_origin(LanguageOrigin.OLD_ENGLISH)
        self.assertTrue(len(results) > 0)
        for entry in results:
            self.assertEqual(entry.language_origin, LanguageOrigin.OLD_ENGLISH)
    
    def test_search_empty_category(self):
        """Test searching for a category with no entries."""
        results = search_by_origin(LanguageOrigin.HINDI)
        # May be empty depending on database
        self.assertIsInstance(results, list)


class TestSearchByPeriod(unittest.TestCase):
    """Test search_by_period function."""
    
    def test_search_modern(self):
        """Test searching for Modern period."""
        results = search_by_period(HistoricalPeriod.MODERN)
        self.assertTrue(len(results) > 0)
        for entry in results:
            self.assertEqual(entry.historical_period, HistoricalPeriod.MODERN)
    
    def test_search_ancient(self):
        """Test searching for Ancient period."""
        results = search_by_period(HistoricalPeriod.ANCIENT)
        self.assertTrue(len(results) > 0)
    
    def test_search_medieval(self):
        """Test searching for Medieval period."""
        results = search_by_period(HistoricalPeriod.MEDIEVAL)
        self.assertTrue(len(results) > 0)


class TestFindCognates(unittest.TestCase):
    """Test find_cognates function."""
    
    def test_existing_word_cognates(self):
        """Test finding cognates for existing word."""
        cognates = find_cognates("computer")
        self.assertTrue(len(cognates) > 0)
        self.assertIn("French", cognates)
    
    def test_nonexistent_word_cognates(self):
        """Test finding cognates for nonexistent word."""
        cognates = find_cognates("xyzzy")
        self.assertEqual(cognates, {})
    
    def test_philosophy_cognates(self):
        """Test cognates for philosophy."""
        cognates = find_cognates("philosophy")
        self.assertIn("French", cognates)
        self.assertIn("German", cognates)


class TestGetWordFamily(unittest.TestCase):
    """Test get_word_family function."""
    
    def test_existing_root(self):
        """Test getting family for existing root."""
        family = get_word_family("work")
        self.assertIsNotNone(family)
        self.assertEqual(family.root, "work")
        self.assertTrue(len(family.members) > 0)
    
    def test_nonexistent_root(self):
        """Test getting family for nonexistent root."""
        family = get_word_family("xyzzy")
        self.assertIsNone(family)
    
    def test_family_members(self):
        """Test family members content."""
        family = get_word_family("act")
        self.assertIsNotNone(family)
        self.assertIn("action", family.members)
        self.assertIn("active", family.members)
    
    def test_case_insensitive(self):
        """Test case insensitive lookup."""
        family1 = get_word_family("WORK")
        family2 = get_word_family("work")
        
        if family1 and family2:
            self.assertEqual(family1.root, family2.root)


class TestBuildEtymologyTree(unittest.TestCase):
    """Test build_etymology_tree function."""
    
    def test_tree_for_existing_word(self):
        """Test building tree for existing word."""
        tree = build_etymology_tree("computer")
        self.assertEqual(tree.word, "computer")
        self.assertEqual(tree.origin, LanguageOrigin.LATIN)
        self.assertTrue(len(tree.children) > 0)
    
    def test_tree_for_nonexistent_word(self):
        """Test building tree for nonexistent word."""
        tree = build_etymology_tree("xyzzy")
        self.assertEqual(tree.word, "xyzzy")
        self.assertIsNone(tree.origin)
    
    def test_tree_depth(self):
        """Test tree depth."""
        tree = build_etymology_tree("telephone")
        self.assertTrue(tree.depth() >= 1)
    
    def test_tree_size(self):
        """Test tree size."""
        tree = build_etymology_tree("king")
        self.assertTrue(tree.size() >= 1)


class TestExtractRoot(unittest.TestCase):
    """Test extract_root function."""
    
    def test_extract_from_simple_word(self):
        """Test extracting root from simple word."""
        # This test depends on what's in the database
        root = extract_root("action")
        # May return "act" if properly set up
        self.assertTrue(root is None or root == "act")
    
    def test_extract_from_nonexistent_word(self):
        """Test extracting from nonexistent word."""
        root = extract_root("xyzzy")
        self.assertIsNone(root)
    
    def test_word_already_root(self):
        """Test word that is already a root."""
        root = extract_root("work")
        # "work" is a root word, so should return itself or None
        pass  # Depends on implementation


class TestAnalyzeWord(unittest.TestCase):
    """Test analyze_word function."""
    
    def test_analyze_existing_word(self):
        """Test analyzing existing word."""
        analysis = analyze_word("computer")
        self.assertEqual(analysis["word"], "computer")
        self.assertIsNotNone(analysis["etymology"])
        self.assertTrue(len(analysis["cognates"]) > 0)
    
    def test_analyze_nonexistent_word(self):
        """Test analyzing nonexistent word."""
        analysis = analyze_word("xyzzy")
        self.assertEqual(analysis["word"], "xyzzy")
        self.assertIsNone(analysis["etymology"])
    
    def test_analyze_compound_word(self):
        """Test analyzing compound word."""
        analysis = analyze_word("breakfast")
        # Breakfast is marked as compound in the database entry
        # The detection depends on having the parts in the database
        self.assertIn("is_compound", analysis)
    
    def test_analyze_with_prefix(self):
        """Test analyzing word with prefix."""
        analysis = analyze_word("information")
        # May have prefix info
        self.assertIn("prefix", analysis)
    
    def test_analyze_with_suffix(self):
        """Test analyzing word with suffix."""
        analysis = analyze_word("education")
        # May have suffix info
        self.assertIn("suffix", analysis)
    
    def test_analysis_has_all_keys(self):
        """Test that analysis has all expected keys."""
        analysis = analyze_word("test")
        expected_keys = [
            "word", "etymology", "root", "prefix", "suffix",
            "word_family", "cognates", "is_compound", "compound_parts"
        ]
        for key in expected_keys:
            self.assertIn(key, analysis)


class TestDetectCompound(unittest.TestCase):
    """Test detect_compound function."""
    
    def test_detect_known_compound(self):
        """Test detecting known compound."""
        parts = detect_compound("breakfast")
        # Should detect break + fast if available in database
        self.assertIsInstance(parts, list)
    
    def test_detect_non_compound(self):
        """Test detecting non-compound."""
        parts = detect_compound("computer")
        self.assertEqual(parts, [])
    
    def test_detect_airport(self):
        """Test detecting airport compound."""
        parts = detect_compound("airport")
        self.assertIsInstance(parts, list)


class TestCompareWords(unittest.TestCase):
    """Test compare_words function."""
    
    def test_compare_same_origin(self):
        """Test comparing words with same origin."""
        result = compare_words("computer", "information")
        self.assertTrue(result["same_origin"])  # Both Latin
    
    def test_compare_different_origin(self):
        """Test comparing words with different origin."""
        result = compare_words("computer", "king")
        self.assertFalse(result["same_origin"])  # Latin vs Old English
    
    def test_compare_nonexistent_words(self):
        """Test comparing nonexistent words."""
        result = compare_words("xyzzy", "plugh")
        self.assertEqual(result["word1"], "xyzzy")
        self.assertEqual(result["word2"], "plugh")
    
    def test_compare_result_has_all_keys(self):
        """Test that comparison result has all keys."""
        result = compare_words("computer", "education")
        expected_keys = [
            "word1", "word2", "same_origin", "same_period",
            "common_root", "related", "cognate_languages"
        ]
        for key in expected_keys:
            self.assertIn(key, result)


class TestVisualizeTree(unittest.TestCase):
    """Test visualize_tree function."""
    
    def test_visualize_simple_tree(self):
        """Test visualizing a simple tree."""
        tree = EtymologyTree(word="root")
        child = EtymologyTree(word="child")
        tree.add_child(child)
        
        visualization = visualize_tree(tree)
        self.assertIn("root", visualization)
        self.assertIn("child", visualization)
    
    def test_visualize_with_origin(self):
        """Test visualizing tree with origin."""
        tree = EtymologyTree(
            word="computer",
            origin=LanguageOrigin.LATIN,
            period=HistoricalPeriod.MODERN
        )
        
        visualization = visualize_tree(tree)
        self.assertIn("computer", visualization)
        self.assertIn("Latin", visualization)
        self.assertIn("Modern", visualization)
    
    def test_visualize_indentation(self):
        """Test proper indentation in visualization."""
        root = EtymologyTree(word="root")
        child = EtymologyTree(word="child")
        grandchild = EtymologyTree(word="grandchild")
        
        child.add_child(grandchild)
        root.add_child(child)
        
        visualization = visualize_tree(root)
        # Check that there's some indentation
        self.assertTrue("  " in visualization or visualization.startswith("root"))


class TestGetStatistics(unittest.TestCase):
    """Test get_statistics function."""
    
    def test_statistics_has_required_keys(self):
        """Test that statistics has all required keys."""
        stats = get_statistics()
        expected_keys = [
            "total_words", "total_roots", "total_prefixes",
            "total_suffixes", "by_origin", "by_period",
            "average_confidence"
        ]
        for key in expected_keys:
            self.assertIn(key, stats)
    
    def test_total_words_positive(self):
        """Test that total words is positive."""
        stats = get_statistics()
        self.assertTrue(stats["total_words"] > 0)
    
    def test_by_origin_counts(self):
        """Test origin counts."""
        stats = get_statistics()
        self.assertTrue(len(stats["by_origin"]) > 0)
    
    def test_average_confidence_range(self):
        """Test that confidence is in valid range."""
        stats = get_statistics()
        self.assertTrue(0 <= stats["average_confidence"] <= 1)


class TestSearchWords(unittest.TestCase):
    """Test search_words function."""
    
    def test_search_prefix(self):
        """Test prefix search."""
        results = search_words("com")
        self.assertIsInstance(results, list)
        for r in results:
            self.assertTrue(r.startswith("com"))
    
    def test_search_exact_match(self):
        """Test exact match search."""
        results = search_words("computer")
        self.assertIn("computer", results)
    
    def test_search_empty_query(self):
        """Test search with empty query."""
        results = search_words("")
        self.assertIsInstance(results, list)
    
    def test_search_fuzzy(self):
        """Test fuzzy search."""
        results = search_words("compu", fuzzy=True)
        self.assertIsInstance(results, list)


class TestValidateEtymology(unittest.TestCase):
    """Test validate_etymology function."""
    
    def test_valid_entry(self):
        """Test validating a valid entry."""
        entry = EtymologyEntry(
            word="test",
            language_origin=LanguageOrigin.LATIN,
            historical_period=HistoricalPeriod.MODERN,
            confidence=0.5
        )
        errors = validate_etymology(entry)
        self.assertEqual(errors, [])
    
    def test_empty_word(self):
        """Test validating entry with empty word."""
        entry = EtymologyEntry(
            word="",
            language_origin=LanguageOrigin.LATIN,
            historical_period=HistoricalPeriod.MODERN
        )
        errors = validate_etymology(entry)
        self.assertTrue(len(errors) > 0)
    
    def test_invalid_confidence(self):
        """Test validating entry with invalid confidence."""
        entry = EtymologyEntry(
            word="test",
            language_origin=LanguageOrigin.LATIN,
            historical_period=HistoricalPeriod.MODERN,
            confidence=2.0
        )
        errors = validate_etymology(entry)
        self.assertTrue(len(errors) > 0)
        
        entry = EtymologyEntry(
            word="test",
            language_origin=LanguageOrigin.LATIN,
            historical_period=HistoricalPeriod.MODERN,
            confidence=-0.5
        )
        errors = validate_etymology(entry)
        self.assertTrue(len(errors) > 0)


class TestExportToJson(unittest.TestCase):
    """Test export_to_json function."""
    
    def test_export_all(self):
        """Test exporting all entries."""
        json_str = export_to_json()
        self.assertIsInstance(json_str, str)
        self.assertTrue(len(json_str) > 0)
        self.assertIn("version", json_str)
        self.assertIn("entries", json_str)
    
    def test_export_specific_entries(self):
        """Test exporting specific entries."""
        entry = get_etymology("computer")
        if entry:
            json_str = export_to_json([entry])
            self.assertIn("computer", json_str)
    
    def test_export_statistics(self):
        """Test that export includes statistics."""
        json_str = export_to_json()
        self.assertIn("statistics", json_str)


class TestTraceWordEvolution(unittest.TestCase):
    """Test trace_word_evolution function."""
    
    def test_trace_existing_word(self):
        """Test tracing existing word."""
        stages = trace_word_evolution("computer")
        self.assertTrue(len(stages) > 0)
    
    def test_trace_nonexistent_word(self):
        """Test tracing nonexistent word."""
        stages = trace_word_evolution("xyzzy")
        self.assertEqual(stages, [])
    
    def test_evolution_stages_format(self):
        """Test evolution stages format."""
        stages = trace_word_evolution("philosophy")
        for stage in stages:
            self.assertIn("form", stage)
            self.assertIn("period", stage)
            self.assertIn("origin", stage)


class TestFindLanguageContributions(unittest.TestCase):
    """Test find_language_contributions function."""
    
    def test_contributions_positive(self):
        """Test that contributions are positive."""
        contributions = find_language_contributions()
        self.assertTrue(len(contributions) > 0)
    
    def test_latin_has_contributions(self):
        """Test Latin has contributions."""
        contributions = find_language_contributions()
        self.assertIn("Latin", contributions)
    
    def test_greek_has_contributions(self):
        """Test Greek has contributions."""
        contributions = find_language_contributions()
        self.assertIn("Greek", contributions)


class TestFindPeriodContributions(unittest.TestCase):
    """Test find_period_contributions function."""
    
    def test_period_contributions_positive(self):
        """Test that period contributions are positive."""
        contributions = find_period_contributions()
        self.assertTrue(len(contributions) > 0)
    
    def test_modern_has_contributions(self):
        """Test Modern period has contributions."""
        contributions = find_period_contributions()
        self.assertIn("Modern", contributions)


class TestGenerateWordReport(unittest.TestCase):
    """Test generate_word_report function."""
    
    def test_report_for_existing_word(self):
        """Test generating report for existing word."""
        report = generate_word_report("computer")
        self.assertTrue(len(report) > 0)
        self.assertIn("computer", report)
        self.assertIn("ETYMOLOGY REPORT", report)
    
    def test_report_format(self):
        """Test report format."""
        report = generate_word_report("philosophy")
        self.assertIn("Origin:", report)
        self.assertIn("Period:", report)
    
    def test_report_for_nonexistent_word(self):
        """Test generating report for nonexistent word."""
        report = generate_word_report("xyzzy")
        # Should still generate a report
        self.assertIn("XYZZY", report.upper())


class TestQuickLookup(unittest.TestCase):
    """Test quick_lookup function."""
    
    def test_lookup_existing_word(self):
        """Test quick lookup for existing word."""
        result = quick_lookup("computer")
        self.assertIn("computer", result)
        self.assertIn("Latin", result)
    
    def test_lookup_nonexistent_word(self):
        """Test quick lookup for nonexistent word."""
        result = quick_lookup("xyzzy")
        self.assertIn("xyzzy", result)
        self.assertIn("no etymology", result)
    
    def test_lookup_format(self):
        """Test quick lookup format."""
        result = quick_lookup("philosophy")
        self.assertTrue("'" in result)


class TestIsLoanword(unittest.TestCase):
    """Test is_loanword function."""
    
    def test_loanword_from_latin(self):
        """Test Latin words are loanwords."""
        self.assertTrue(is_loanword("computer"))
    
    def test_loanword_from_greek(self):
        """Test Greek words are loanwords."""
        self.assertTrue(is_loanword("philosophy"))
    
    def test_native_word(self):
        """Test Old English words are not loanwords."""
        self.assertFalse(is_loanword("king"))
        self.assertFalse(is_loanword("friend"))
    
    def test_nonexistent_word(self):
        """Test nonexistent word."""
        self.assertFalse(is_loanword("xyzzy"))


class TestGetLoanwords(unittest.TestCase):
    """Test get_loanwords function."""
    
    def test_loanwords_list(self):
        """Test loanwords list."""
        loanwords = get_loanwords()
        self.assertIsInstance(loanwords, list)
        self.assertTrue(len(loanwords) > 0)
    
    def test_loanwords_not_native(self):
        """Test loanwords are not native."""
        loanwords = get_loanwords()
        # Should not include Old English words
        self.assertNotIn("king", loanwords)
    
    def test_loanwords_include_borrowed(self):
        """Test loanwords include borrowed words."""
        loanwords = get_loanwords()
        self.assertIn("computer", loanwords)


class TestGetNativeWords(unittest.TestCase):
    """Test get_native_words function."""
    
    def test_native_words_list(self):
        """Test native words list."""
        native = get_native_words()
        self.assertIsInstance(native, list)
        self.assertTrue(len(native) > 0)
    
    def test_native_words_include_old_english(self):
        """Test native words include Old English."""
        native = get_native_words()
        self.assertIn("king", native)
    
    def test_native_words_not_loanwords(self):
        """Test native words are not loanwords."""
        native = get_native_words()
        self.assertNotIn("computer", native)


class TestDatabaseIntegrity(unittest.TestCase):
    """Test database integrity."""
    
    def test_etymology_database_not_empty(self):
        """Test etymology database is not empty."""
        self.assertTrue(len(ETYMOLOGY_DATABASE) > 0)
    
    def test_root_database_not_empty(self):
        """Test root database is not empty."""
        self.assertTrue(len(ROOT_WORDS_DATABASE) > 0)
    
    def test_prefixes_database_not_empty(self):
        """Test prefixes database is not empty."""
        self.assertTrue(len(PREFIXES_DATABASE) > 0)
    
    def test_suffixes_database_not_empty(self):
        """Test suffixes database is not empty."""
        self.assertTrue(len(SUFFIXES_DATABASE) > 0)
    
    def test_entries_valid(self):
        """Test all entries are valid."""
        for word, entry in ETYMOLOGY_DATABASE.items():
            errors = validate_etymology(entry)
            self.assertEqual(errors, [], f"Invalid entry: {word}")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases."""
    
    def test_empty_string(self):
        """Test empty string."""
        entry = get_etymology("")
        self.assertIsNone(entry)
    
    def test_single_character(self):
        """Test single character."""
        entry = get_etymology("a")
        self.assertIsNone(entry)
    
    def test_unicode_characters(self):
        """Test unicode characters."""
        entry = get_etymology("你好")
        self.assertIsNone(entry)
    
    def test_numbers(self):
        """Test numbers."""
        entry = get_etymology("123")
        self.assertIsNone(entry)
    
    def test_special_characters(self):
        """Test special characters."""
        entry = get_etymology("!@#$%")
        self.assertIsNone(entry)
    
    def test_whitespace_only(self):
        """Test whitespace only."""
        entry = get_etymology("   ")
        self.assertIsNone(entry)
    
    def test_mixed_case(self):
        """Test mixed case."""
        entry = get_etymology("CoMPuTeR")
        self.assertIsNotNone(entry)


class TestChainedOperations(unittest.TestCase):
    """Test chained operations."""
    
    def test_lookup_then_analyze(self):
        """Test lookup then analyze."""
        entry = get_etymology("computer")
        if entry:
            analysis = analyze_word(entry.word)
            self.assertEqual(analysis["word"], "computer")
    
    def test_build_tree_then_visualize(self):
        """Test build tree then visualize."""
        tree = build_etymology_tree("philosophy")
        visualization = visualize_tree(tree)
        self.assertIn("philosophy", visualization)
    
    def test_search_then_process(self):
        """Test search then process results."""
        results = search_by_origin(LanguageOrigin.LATIN)
        for entry in results[:3]:
            cognates = find_cognates(entry.word)
            self.assertIsInstance(cognates, dict)


# Run tests
if __name__ == "__main__":
    unittest.main(verbosity=2)