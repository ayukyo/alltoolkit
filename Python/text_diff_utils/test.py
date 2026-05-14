"""
Tests for Text Diff Utilities

Comprehensive test suite for all text diff utility functions.
"""

import unittest
from mod import (
    TextDiffUtils,
    DiffOperation,
    DiffBlock,
    lcs,
    lcs_length,
    levenshtein_distance,
    similarity_ratio,
    jaccard_similarity,
    diff_chars,
    diff_lines,
    unified_diff,
    highlight_diff,
    html_diff,
    diff_stats,
    side_by_side,
    find_changes
)


class TestLCS(unittest.TestCase):
    """Test Longest Common Subsequence functions."""

    def test_lcs_basic(self):
        """Test basic LCS computation."""
        # LCS can have multiple valid results of same length
        result = lcs("ABCBDAB", "BDCABA")
        self.assertEqual(len(result), 4)  # LCS length is 4
        # Verify it's a valid subsequence of both strings
        self.assertIn(result, ["BCBA", "BDAB", "BCAB"])  # All valid LCS
        
    def test_lcs_empty(self):
        """Test LCS with empty strings."""
        self.assertEqual(lcs("", ""), "")
        self.assertEqual(lcs("ABC", ""), "")
        self.assertEqual(lcs("", "ABC"), "")
        
    def test_lcs_identical(self):
        """Test LCS with identical strings."""
        self.assertEqual(lcs("hello", "hello"), "hello")
        
    def test_lcs_no_common(self):
        """Test LCS with no common characters."""
        self.assertEqual(lcs("abc", "xyz"), "")
        
    def test_lcs_single_char(self):
        """Test LCS with single common character."""
        result = lcs("abc", "cba")
        self.assertEqual(len(result), 1)  # Either 'b' or 'c' is valid
        self.assertIn(result, ["b", "c"])
        
    def test_lcs_length_basic(self):
        """Test LCS length computation."""
        self.assertEqual(lcs_length("ABCBDAB", "BDCABA"), 4)
        
    def test_lcs_length_empty(self):
        """Test LCS length with empty strings."""
        self.assertEqual(lcs_length("", ""), 0)
        self.assertEqual(lcs_length("ABC", ""), 0)
        
    def test_lcs_length_identical(self):
        """Test LCS length with identical strings."""
        self.assertEqual(lcs_length("hello", "hello"), 5)


class TestLevenshteinDistance(unittest.TestCase):
    """Test Levenshtein distance functions."""

    def test_levenshtein_basic(self):
        """Test basic Levenshtein distance computation."""
        self.assertEqual(levenshtein_distance("kitten", "sitting"), 3)
        
    def test_levenshtein_empty(self):
        """Test Levenshtein distance with empty strings."""
        self.assertEqual(levenshtein_distance("", ""), 0)
        self.assertEqual(levenshtein_distance("hello", ""), 5)
        self.assertEqual(levenshtein_distance("", "world"), 5)
        
    def test_levenshtein_identical(self):
        """Test Levenshtein distance with identical strings."""
        self.assertEqual(levenshtein_distance("same", "same"), 0)
        
    def test_levenshtein_single_char(self):
        """Test Levenshtein distance with single character changes."""
        self.assertEqual(levenshtein_distance("a", "b"), 1)  # substitution
        self.assertEqual(levenshtein_distance("a", "ab"), 1)  # insertion
        self.assertEqual(levenshtein_distance("ab", "a"), 1)  # deletion
        
    def test_levenshtein_case_sensitive(self):
        """Test that Levenshtein distance is case sensitive."""
        self.assertEqual(levenshtein_distance("Hello", "hello"), 1)


class TestSimilarity(unittest.TestCase):
    """Test similarity functions."""

    def test_similarity_ratio_identical(self):
        """Test similarity ratio with identical strings."""
        self.assertEqual(similarity_ratio("hello", "hello"), 1.0)
        
    def test_similarity_ratio_different(self):
        """Test similarity ratio with different strings."""
        # hello world vs hello earth
        # Levenshtein distance is 4 (world->earth = 4 substitutions)
        # total_len = 22, ratio = (22-4)/22 = 0.818...
        ratio = similarity_ratio("hello world", "hello earth")
        self.assertAlmostEqual(ratio, 18/22, places=5)
        
    def test_similarity_ratio_empty(self):
        """Test similarity ratio with empty strings."""
        self.assertEqual(similarity_ratio("", ""), 1.0)
        
    def test_similarity_ratio_no_similarity(self):
        """Test similarity ratio with completely different strings."""
        # For strings of equal length with all substitutions
        # abc vs xyz: distance = 3, total = 6, ratio = 0.5
        self.assertEqual(similarity_ratio("abc", "xyz"), 0.5)
        # For truly no overlap (one empty string)
        self.assertEqual(similarity_ratio("", "xyz"), 0.0)
        
    def test_jaccard_similarity_basic(self):
        """Test basic Jaccard similarity computation."""
        # hello bigrams: he, el, ll, lo (4)
        # hallo bigrams: ha, al, ll, lo (4)
        # intersection: ll, lo (2), union: he, el, ll, lo, ha, al (6)
        self.assertEqual(jaccard_similarity("hello", "hallo"), 2/6)
        
    def test_jaccard_similarity_identical(self):
        """Test Jaccard similarity with identical strings."""
        self.assertEqual(jaccard_similarity("hello", "hello"), 1.0)
        
    def test_jaccard_similarity_empty(self):
        """Test Jaccard similarity with empty strings."""
        self.assertEqual(jaccard_similarity("", ""), 1.0)
        
    def test_jaccard_similarity_ngram(self):
        """Test Jaccard similarity with different n-gram sizes."""
        self.assertEqual(jaccard_similarity("ab", "ab", ngram=1), 1.0)
        self.assertEqual(jaccard_similarity("abc", "abd", ngram=3), 0.0)


class TestDiffChars(unittest.TestCase):
    """Test character-level diff functions."""

    def test_diff_chars_basic(self):
        """Test basic character-level diff."""
        result = diff_chars("hello", "hallo")
        # Should show: h (equal), e->a (delete+insert), llo (equal)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], DiffBlock(DiffOperation.EQUAL, "h"))
        self.assertEqual(result[1], DiffBlock(DiffOperation.DELETE, "e"))
        self.assertEqual(result[2], DiffBlock(DiffOperation.INSERT, "a"))
        self.assertEqual(result[3], DiffBlock(DiffOperation.EQUAL, "llo"))
        
    def test_diff_chars_identical(self):
        """Test character diff with identical strings."""
        result = diff_chars("hello", "hello")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], DiffBlock(DiffOperation.EQUAL, "hello"))
        
    def test_diff_chars_insert_only(self):
        """Test character diff with only insertions."""
        result = diff_chars("", "hello")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], DiffBlock(DiffOperation.INSERT, "hello"))
        
    def test_diff_chars_delete_only(self):
        """Test character diff with only deletions."""
        result = diff_chars("hello", "")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], DiffBlock(DiffOperation.DELETE, "hello"))
        
    def test_diff_chars_complete_change(self):
        """Test character diff with complete string change."""
        result = diff_chars("abc", "xyz")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], DiffBlock(DiffOperation.DELETE, "abc"))
        self.assertEqual(result[1], DiffBlock(DiffOperation.INSERT, "xyz"))


class TestDiffLines(unittest.TestCase):
    """Test line-level diff functions."""

    def test_diff_lines_basic(self):
        """Test basic line-level diff."""
        result = diff_lines("a\nb\nc", "a\nx\nc")
        self.assertTrue(any(block.operation == DiffOperation.DELETE for block in result))
        self.assertTrue(any(block.operation == DiffOperation.INSERT for block in result))
        
    def test_diff_lines_identical(self):
        """Test line diff with identical texts."""
        result = diff_lines("a\nb\nc", "a\nb\nc")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].operation, DiffOperation.EQUAL)
        
    def test_diff_lines_insert_line(self):
        """Test line diff with line insertion."""
        result = diff_lines("a\nc", "a\nb\nc")
        self.assertTrue(any(block.operation == DiffOperation.INSERT for block in result))
        
    def test_diff_lines_delete_line(self):
        """Test line diff with line deletion."""
        result = diff_lines("a\nb\nc", "a\nc")
        self.assertTrue(any(block.operation == DiffOperation.DELETE for block in result))


class TestUnifiedDiff(unittest.TestCase):
    """Test unified diff output."""

    def test_unified_diff_basic(self):
        """Test basic unified diff generation."""
        diff = unified_diff("a\nb\nc", "a\nx\nc")
        self.assertIn("--- original", diff)
        self.assertIn("+++ modified", diff)
        self.assertIn("@@", diff)
        
    def test_unified_diff_empty(self):
        """Test unified diff with identical texts."""
        diff = unified_diff("hello", "hello")
        self.assertIn("--- original", diff)
        self.assertIn("+++ modified", diff)
        
    def test_unified_diff_filenames(self):
        """Test unified diff with custom filenames."""
        diff = unified_diff("a", "b", "file1.txt", "file2.txt")
        self.assertIn("--- file1.txt", diff)
        self.assertIn("+++ file2.txt", diff)
        
    def test_unified_diff_context(self):
        """Test unified diff with different context lines."""
        text1 = "\n".join(["line" + str(i) for i in range(10)])
        text2 = "\n".join(["line" + str(i) if i != 5 else "changed" for i in range(10)])
        diff1 = unified_diff(text1, text2, context_lines=1)
        diff2 = unified_diff(text1, text2, context_lines=3)
        # More context should produce more lines
        self.assertGreater(len(diff2), len(diff1))


class TestHighlightDiff(unittest.TestCase):
    """Test diff highlighting functions."""

    def test_highlight_diff_basic(self):
        """Test basic diff highlighting."""
        blocks = [
            DiffBlock(DiffOperation.EQUAL, "h"),
            DiffBlock(DiffOperation.DELETE, "e"),
            DiffBlock(DiffOperation.INSERT, "a"),
            DiffBlock(DiffOperation.EQUAL, "llo")
        ]
        result = highlight_diff(blocks)
        self.assertIn("\033[32m", result)  # Green for insert
        self.assertIn("\033[31m", result)  # Red for delete
        self.assertIn("h", result)
        self.assertIn("a", result)
        self.assertIn("llo", result)
        
    def test_highlight_diff_all_equal(self):
        """Test highlighting with no changes."""
        blocks = [DiffBlock(DiffOperation.EQUAL, "hello")]
        result = highlight_diff(blocks)
        self.assertNotIn("\033[32m", result)
        self.assertNotIn("\033[31m", result)


class TestHtmlDiff(unittest.TestCase):
    """Test HTML diff output."""

    def test_html_diff_basic(self):
        """Test basic HTML diff generation."""
        blocks = [
            DiffBlock(DiffOperation.EQUAL, "h"),
            DiffBlock(DiffOperation.DELETE, "e"),
            DiffBlock(DiffOperation.INSERT, "a"),
            DiffBlock(DiffOperation.EQUAL, "llo")
        ]
        result = html_diff(blocks)
        self.assertIn("diff-equal", result)
        self.assertIn("diff-delete", result)
        self.assertIn("diff-insert", result)
        self.assertIn("<span", result)
        self.assertIn("</span>", result)
        
    def test_html_diff_escaping(self):
        """Test HTML diff with special characters."""
        blocks = [DiffBlock(DiffOperation.EQUAL, "<script>alert('xss')</script>")]
        result = html_diff(blocks)
        self.assertIn("&lt;", result)
        self.assertIn("&gt;", result)
        self.assertNotIn("<script>", result)


class TestDiffStats(unittest.TestCase):
    """Test diff statistics functions."""

    def test_diff_stats_basic(self):
        """Test basic diff statistics."""
        blocks = [
            DiffBlock(DiffOperation.EQUAL, "h"),
            DiffBlock(DiffOperation.DELETE, "ello"),
            DiffBlock(DiffOperation.INSERT, "allo"),
        ]
        stats = diff_stats(blocks)
        self.assertEqual(stats["insertions"], 4)
        self.assertEqual(stats["deletions"], 4)
        self.assertEqual(stats["unchanged"], 1)
        self.assertEqual(stats["total"], 9)
        
    def test_diff_stats_empty(self):
        """Test diff statistics with empty blocks."""
        stats = diff_stats([])
        self.assertEqual(stats["insertions"], 0)
        self.assertEqual(stats["deletions"], 0)
        self.assertEqual(stats["unchanged"], 0)
        self.assertEqual(stats["total"], 0)
        
    def test_diff_stats_all_equal(self):
        """Test diff statistics with no changes."""
        blocks = [DiffBlock(DiffOperation.EQUAL, "hello world")]
        stats = diff_stats(blocks)
        self.assertEqual(stats["insertions"], 0)
        self.assertEqual(stats["deletions"], 0)
        self.assertEqual(stats["unchanged"], 11)
        self.assertEqual(stats["total"], 11)


class TestSideBySide(unittest.TestCase):
    """Test side-by-side comparison."""

    def test_side_by_side_basic(self):
        """Test basic side-by-side comparison."""
        result = side_by_side("a\nb", "x\ny")
        lines = result.split('\n')
        self.assertEqual(len(lines), 2)
        self.assertIn("a", lines[0])
        self.assertIn("x", lines[0])
        
    def test_side_by_side_different_lengths(self):
        """Test side-by-side with different text lengths."""
        result = side_by_side("a\nb\nc", "x\ny")
        lines = result.split('\n')
        self.assertEqual(len(lines), 3)
        
    def test_side_by_side_custom_width(self):
        """Test side-by-side with custom width."""
        result = side_by_side("hello", "world", width=10)
        lines = result.split('\n')
        self.assertEqual(len(lines[0]), 23)  # 10 + 3 (separator) + 10
        
    def test_side_by_side_custom_separator(self):
        """Test side-by-side with custom separator."""
        result = side_by_side("a", "b", separator=" || ")
        self.assertIn(" || ", result)


class TestFindChanges(unittest.TestCase):
    """Test find changes functions."""

    def test_find_changes_basic(self):
        """Test basic change finding."""
        changes = find_changes("hello world", "hello there")
        # There should be at least one change region
        self.assertGreaterEqual(len(changes), 1)
        # Verify changes were found (character-level diff may split differently)
        total_deleted = "".join(c[2] for c in changes)
        total_inserted = "".join(c[3] for c in changes)
        # Should have some deletions and insertions
        self.assertTrue(len(total_deleted) > 0 or len(total_inserted) > 0)
        
    def test_find_changes_multiple(self):
        """Test finding multiple changes."""
        changes = find_changes("abc def", "xyz uvw")
        self.assertGreaterEqual(len(changes), 1)
        
    def test_find_changes_none(self):
        """Test finding no changes."""
        changes = find_changes("hello", "hello")
        self.assertEqual(len(changes), 0)
        
    def test_find_positions(self):
        """Test that change positions are correct."""
        changes = find_changes("abc", "adc")
        self.assertEqual(len(changes), 1)
        start, end, deleted, inserted = changes[0]
        self.assertEqual(start, 1)
        self.assertEqual(deleted, "b")
        self.assertEqual(inserted, "d")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def test_unicode_support(self):
        """Test Unicode character support."""
        result = diff_chars("héllo", "hållo")
        self.assertTrue(len(result) > 0)
        self.assertTrue(any("é" in block.text or "å" in block.text for block in result))
        
    def test_very_long_string(self):
        """Test with very long strings."""
        text1 = "a" * 1000 + "b" * 1000
        text2 = "a" * 1000 + "c" * 1000
        result = diff_chars(text1, text2)
        stats = diff_stats(result)
        self.assertEqual(stats["deletions"], 1000)
        self.assertEqual(stats["insertions"], 1000)
        self.assertEqual(stats["unchanged"], 1000)
        
    def test_whitespace_handling(self):
        """Test whitespace handling in diffs."""
        result = diff_chars("hello world", "hello\tworld")
        self.assertTrue(len(result) > 0)
        
    def test_newline_handling(self):
        """Test newline handling in line diffs."""
        result = diff_lines("a\nb", "a\nb\n")
        # Both texts have same visible lines
        self.assertTrue(len(result) > 0)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience function exports."""

    def test_convenience_functions_exist(self):
        """Test that all convenience functions are exported."""
        self.assertTrue(callable(lcs))
        self.assertTrue(callable(lcs_length))
        self.assertTrue(callable(levenshtein_distance))
        self.assertTrue(callable(similarity_ratio))
        self.assertTrue(callable(jaccard_similarity))
        self.assertTrue(callable(diff_chars))
        self.assertTrue(callable(diff_lines))
        self.assertTrue(callable(unified_diff))
        self.assertTrue(callable(highlight_diff))
        self.assertTrue(callable(html_diff))
        self.assertTrue(callable(diff_stats))
        self.assertTrue(callable(side_by_side))
        self.assertTrue(callable(find_changes))
        
    def test_convenience_function_results(self):
        """Test that convenience functions return same results as class methods."""
        text1 = "hello"
        text2 = "hallo"
        
        self.assertEqual(lcs(text1, text2), TextDiffUtils.lcs(text1, text2))
        self.assertEqual(lcs_length(text1, text2), TextDiffUtils.lcs_length(text1, text2))
        self.assertEqual(levenshtein_distance(text1, text2), 
                        TextDiffUtils.levenshtein_distance(text1, text2))
        self.assertEqual(similarity_ratio(text1, text2), 
                        TextDiffUtils.similarity_ratio(text1, text2))


if __name__ == "__main__":
    unittest.main(verbosity=2)