"""
Unit tests for glob_pattern_utils module.

Run with: python -m pytest glob_pattern_utils_test.py -v
Or: python glob_pattern_utils_test.py
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from glob_pattern_utils.mod import (
    GlobPattern,
    match,
    filter_strings,
    expand_braces,
    translate,
    is_glob,
    escape,
    GlobMatcher,
    fnmatch_translate,
    glob_to_regex,
)


class TestGlobPattern(unittest.TestCase):
    """Test cases for GlobPattern class."""
    
    def test_wildcard_star(self):
        """Test * wildcard matching."""
        pattern = GlobPattern("*.txt")
        self.assertTrue(pattern.match("file.txt"))
        self.assertTrue(pattern.match("document.txt"))
        self.assertTrue(pattern.match(".txt"))  # Empty string before .txt
        self.assertFalse(pattern.match("file.py"))
        self.assertFalse(pattern.match("file.txt.bak"))
    
    def test_wildcard_question(self):
        """Test ? wildcard matching."""
        pattern = GlobPattern("file?.txt")
        self.assertTrue(pattern.match("file1.txt"))
        self.assertTrue(pattern.match("fileA.txt"))
        self.assertFalse(pattern.match("file.txt"))
        self.assertFalse(pattern.match("file12.txt"))
    
    def test_character_class(self):
        """Test character class [...]."""
        pattern = GlobPattern("[abc].txt")
        self.assertTrue(pattern.match("a.txt"))
        self.assertTrue(pattern.match("b.txt"))
        self.assertTrue(pattern.match("c.txt"))
        self.assertFalse(pattern.match("d.txt"))
        self.assertFalse(pattern.match("ab.txt"))
    
    def test_character_class_range(self):
        """Test character class with range [a-z]."""
        pattern = GlobPattern("[a-z].txt")
        self.assertTrue(pattern.match("a.txt"))
        self.assertTrue(pattern.match("m.txt"))
        self.assertTrue(pattern.match("z.txt"))
        self.assertFalse(pattern.match("A.txt"))
        self.assertFalse(pattern.match("1.txt"))
    
    def test_negated_character_class(self):
        """Test negated character class [!...]."""
        pattern = GlobPattern("[!abc].txt")
        self.assertFalse(pattern.match("a.txt"))
        self.assertFalse(pattern.match("b.txt"))
        self.assertFalse(pattern.match("c.txt"))
        self.assertTrue(pattern.match("d.txt"))
        self.assertTrue(pattern.match("1.txt"))
    
    def test_negated_character_class_caret(self):
        """Test negated character class [^...]."""
        pattern = GlobPattern("[^abc].txt")
        self.assertFalse(pattern.match("a.txt"))
        self.assertFalse(pattern.match("b.txt"))
        self.assertTrue(pattern.match("x.txt"))
    
    def test_brace_expansion(self):
        """Test brace expansion {a,b,c}."""
        pattern = GlobPattern("file.{txt,py,md}")
        self.assertTrue(pattern.match("file.txt"))
        self.assertTrue(pattern.match("file.py"))
        self.assertTrue(pattern.match("file.md"))
        self.assertFalse(pattern.match("file.js"))
        self.assertFalse(pattern.match("file"))
    
    def test_escape_character(self):
        """Test escape character backslash."""
        pattern = GlobPattern("file\\*.txt")
        self.assertTrue(pattern.match("file*.txt"))
        self.assertFalse(pattern.match("file_test.txt"))
        self.assertFalse(pattern.match("file.txt"))
    
    def test_escape_bracket(self):
        """Test escaping brackets."""
        pattern = GlobPattern("file\\[1\\].txt")
        self.assertTrue(pattern.match("file[1].txt"))
        self.assertFalse(pattern.match("file1.txt"))
    
    def test_case_sensitive(self):
        """Test case-sensitive matching."""
        pattern_sensitive = GlobPattern("FILE.txt", case_sensitive=True)
        self.assertTrue(pattern_sensitive.match("FILE.txt"))
        self.assertFalse(pattern_sensitive.match("file.txt"))
        
        pattern_insensitive = GlobPattern("FILE.txt", case_sensitive=False)
        self.assertTrue(pattern_insensitive.match("FILE.txt"))
        self.assertTrue(pattern_insensitive.match("file.txt"))
        self.assertTrue(pattern_insensitive.match("File.Txt"))
    
    def test_complex_pattern(self):
        """Test complex patterns with multiple wildcards."""
        pattern = GlobPattern("test_*/data_*.csv")
        self.assertTrue(pattern.match("test_001/data_123.csv"))
        self.assertTrue(pattern.match("test_backup/data_final.csv"))
        # Note: * matches empty string, so test_/data_.csv does match
        self.assertTrue(pattern.match("test_/data_.csv"))
    
    def test_multiple_question_marks(self):
        """Test multiple question mark wildcards."""
        pattern = GlobPattern("file???.txt")
        self.assertTrue(pattern.match("file123.txt"))
        self.assertTrue(pattern.match("fileABC.txt"))
        self.assertFalse(pattern.match("file12.txt"))
        self.assertFalse(pattern.match("file1234.txt"))


class TestMatchFunction(unittest.TestCase):
    """Test cases for the match() function."""
    
    def test_basic_match(self):
        """Test basic pattern matching."""
        self.assertTrue(match("*.py", "module.py"))
        self.assertTrue(match("test_?","test_1"))
        self.assertFalse(match("*.py", "module.js"))
    
    def test_case_insensitive(self):
        """Test case-insensitive matching."""
        self.assertTrue(match("*.PY", "module.py", case_sensitive=False))
        self.assertFalse(match("*.PY", "module.py", case_sensitive=True))


class TestFilterStrings(unittest.TestCase):
    """Test cases for filter_strings() function."""
    
    def test_filter_files(self):
        """Test filtering files by extension."""
        files = ["main.py", "test.txt", "utils.py", "readme.md", "config.py"]
        result = filter_strings("*.py", files)
        self.assertEqual(result, ["main.py", "utils.py", "config.py"])
    
    def test_filter_empty(self):
        """Test filtering with no matches."""
        files = ["main.py", "test.py"]
        result = filter_strings("*.txt", files)
        self.assertEqual(result, [])
    
    def test_filter_pattern_with_question(self):
        """Test filtering with ? wildcard."""
        files = ["file1.txt", "file12.txt", "file.txt", "fileA.txt"]
        result = filter_strings("file?.txt", files)
        self.assertEqual(result, ["file1.txt", "fileA.txt"])


class TestExpandBraces(unittest.TestCase):
    """Test cases for expand_braces() function."""
    
    def test_single_brace(self):
        """Test single brace expansion."""
        result = expand_braces("file.{txt,py,md}")
        self.assertEqual(set(result), {"file.txt", "file.py", "file.md"})
    
    def test_multiple_braces(self):
        """Test multiple brace expansions."""
        result = expand_braces("{a,b}{1,2}")
        self.assertEqual(set(result), {"a1", "a2", "b1", "b2"})
    
    def test_no_braces(self):
        """Test pattern without braces."""
        result = expand_braces("file.txt")
        self.assertEqual(result, ["file.txt"])
    
    def test_nested_braces(self):
        """Test nested brace expansion."""
        result = expand_braces("{a,{b,c}}")
        self.assertEqual(set(result), {"a", "{b,c}"})
    
    def test_single_alternative(self):
        """Test single alternative in braces."""
        result = expand_braces("file.{txt}")
        self.assertEqual(result, ["file.txt"])


class TestTranslate(unittest.TestCase):
    """Test cases for translate() function."""
    
    def test_translate_star(self):
        """Test translating * wildcard."""
        regex = translate("*.txt")
        self.assertIn("[^/]*", regex)
        self.assertIn(".txt", regex)
    
    def test_translate_question(self):
        """Test translating ? wildcard."""
        regex = translate("file?.txt")
        self.assertIn(".", regex)


class TestIsGlob(unittest.TestCase):
    """Test cases for is_glob() function."""
    
    def test_is_glob_star(self):
        """Test detecting * in pattern."""
        self.assertTrue(is_glob("*.txt"))
    
    def test_is_glob_question(self):
        """Test detecting ? in pattern."""
        self.assertTrue(is_glob("file?.txt"))
    
    def test_is_glob_bracket(self):
        """Test detecting [...] in pattern."""
        self.assertTrue(is_glob("[abc].txt"))
    
    def test_is_glob_brace(self):
        """Test detecting {...} in pattern."""
        self.assertTrue(is_glob("{a,b}.txt"))
    
    def test_is_not_glob(self):
        """Test detecting no glob characters."""
        self.assertFalse(is_glob("file.txt"))
    
    def test_is_glob_escaped(self):
        """Test escaped glob characters."""
        self.assertFalse(is_glob("file\\*.txt"))  # Escaped *


 
class TestEscape(unittest.TestCase):
    """Test cases for escape() function."""
    
    def test_escape_star(self):
        """Test escaping * character."""
        self.assertEqual(escape("file*.txt"), "file\\*.txt")
    
    def test_escape_question(self):
        """Test escaping ? character."""
        self.assertEqual(escape("file?.txt"), "file\\?.txt")
    
    def test_escape_brackets(self):
        """Test escaping brackets."""
        self.assertEqual(escape("file[1].txt"), "file\\[1\\].txt")
    
    def test_escape_braces(self):
        """Test escaping braces."""
        self.assertEqual(escape("file{1}.txt"), "file\\{1\\}.txt")
    
    def test_escape_backslash(self):
        """Test escaping backslash."""
        self.assertEqual(escape("file\\path"), "file\\\\path")


class TestGlobMatcher(unittest.TestCase):
    """Test cases for GlobMatcher class."""
    
    def test_match_any(self):
        """Test match_any with multiple patterns."""
        matcher = GlobMatcher()
        matcher.add_pattern("*.py")
        matcher.add_pattern("*.txt")
        
        self.assertTrue(matcher.match_any("file.py"))
        self.assertTrue(matcher.match_any("file.txt"))
        self.assertFalse(matcher.match_any("file.md"))
    
    def test_match_all(self):
        """Test match_all with multiple patterns."""
        matcher = GlobMatcher()
        matcher.add_pattern("file*")
        matcher.add_pattern("*.py")
        
        self.assertTrue(matcher.match_all("file.py"))
        self.assertFalse(matcher.match_all("file.txt"))
        self.assertFalse(matcher.match_all("test.py"))
    
    def test_filter(self):
        """Test filtering with GlobMatcher."""
        matcher = GlobMatcher()
        matcher.add_pattern("*.py")
        matcher.add_pattern("*.txt")
        
        files = ["main.py", "test.txt", "readme.md", "utils.py"]
        result = matcher.filter(files)
        self.assertEqual(result, ["main.py", "test.txt", "utils.py"])
    
    def test_clear(self):
        """Test clearing patterns."""
        matcher = GlobMatcher()
        matcher.add_pattern("*.py")
        self.assertTrue(matcher.match_any("file.py"))
        
        matcher.clear()
        self.assertFalse(matcher.match_any("file.py"))


class TestFnmatchTranslate(unittest.TestCase):
    """Test cases for fnmatch_translate() function."""
    
    def test_fnmatch_basic(self):
        """Test basic fnmatch functionality."""
        self.assertTrue(fnmatch_translate("file.txt", "*.txt"))
        self.assertTrue(fnmatch_translate("file1.txt", "file?.txt"))
        self.assertFalse(fnmatch_translate("file.txt", "*.py"))


class TestGlobToRegex(unittest.TestCase):
    """Test cases for glob_to_regex() function."""
    
    def test_to_regex_basic(self):
        """Test converting glob to regex."""
        regex = glob_to_regex("*.py")
        self.assertTrue(regex.match("test.py"))
        self.assertFalse(regex.match("test.txt"))


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios."""
    
    def test_empty_pattern(self):
        """Test empty pattern matching."""
        pattern = GlobPattern("")
        self.assertTrue(pattern.match(""))
        self.assertFalse(pattern.match("a"))
    
    def test_empty_string_match(self):
        """Test matching empty string."""
        self.assertTrue(match("*", ""))
        self.assertFalse(match("?", ""))
        self.assertTrue(match("", ""))
    
    def test_special_characters(self):
        """Test matching special regex characters."""
        pattern = GlobPattern("file.txt")
        self.assertTrue(pattern.match("file.txt"))
        # The . should be treated literally in glob, not as regex wildcard
        # Actually in our implementation, . is literal since we escape it
    
    def test_star_star_globstar(self):
        """Test ** globstar pattern."""
        # ** matches anything including path separators
        pattern = GlobPattern("**/*.py")
        # **/ at start should match files at root level too
        self.assertTrue(pattern.match("test.py"))
        self.assertTrue(pattern.match("src/test.py"))
        self.assertTrue(pattern.match("src/lib/test.py"))
    
    def test_unicode_matching(self):
        """Test Unicode character matching."""
        pattern = GlobPattern("文件*.txt")
        self.assertTrue(pattern.match("文件1.txt"))
        self.assertTrue(pattern.match("文件测试.txt"))


class TestCharacterClasses(unittest.TestCase):
    """Test various character class patterns."""
    
    def test_digit_class(self):
        """Test digit character class."""
        pattern = GlobPattern("[0-9].txt")
        self.assertTrue(pattern.match("1.txt"))
        self.assertTrue(pattern.match("9.txt"))
        self.assertFalse(pattern.match("a.txt"))
    
    def test_multiple_ranges(self):
        """Test multiple ranges in character class."""
        pattern = GlobPattern("[a-zA-Z0-9].txt")
        self.assertTrue(pattern.match("a.txt"))
        self.assertTrue(pattern.match("Z.txt"))
        self.assertTrue(pattern.match("5.txt"))
        self.assertFalse(pattern.match("_.txt"))
    
    def test_bracket_in_class(self):
        """Test bracket character inside class."""
        pattern = GlobPattern("[[]")
        self.assertTrue(pattern.match("["))
    
    def test_hyphen_at_start(self):
        """Test hyphen at start of character class."""
        pattern = GlobPattern("[-a].txt")
        self.assertTrue(pattern.match("-.txt"))
        self.assertTrue(pattern.match("a.txt"))


def run_tests():
    """Run all tests and print summary."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())