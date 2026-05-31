"""
Tests for dotenv_utils.
"""

import unittest
import sys
sys.path.insert(0, ".")
from mod import parse, serialize, load


class TestDotenvParse(unittest.TestCase):
    def test_basic_key_value(self):
        self.assertEqual(parse("FOO=bar"), {"FOO": "bar"})

    def test_multiple_pairs(self):
        result = parse("FOO=bar\nBAZ=qux\n")
        self.assertEqual(result, {"FOO": "bar", "BAZ": "qux"})

    def test_double_quoted_value(self):
        result = parse('FOO="hello world"')
        self.assertEqual(result, {"FOO": "hello world"})

    def test_single_quoted_value(self):
        result = parse("FOO='hello world'")
        self.assertEqual(result, {"FOO": "hello world"})

    def test_single_quote_preserves_content(self):
        result = parse("FOO='hello\\nworld'")
        self.assertEqual(result, {"FOO": "hello\\nworld"})

    def test_escape_newline(self):
        result = parse('FOO="hello\\nworld"')
        self.assertEqual(result, {"FOO": "hello\nworld"})

    def test_escape_tab(self):
        result = parse('FOO="hello\\tworld"')
        self.assertEqual(result, {"FOO": "hello\tworld"})

    def test_escape_backslash(self):
        result = parse('FOO="hello\\\\world"')
        self.assertEqual(result, {"FOO": "hello\\world"})

    def test_escape_double_quote(self):
        result = parse('FOO="hello\\"world"')
        self.assertEqual(result, {"FOO": 'hello"world'})

    def test_inline_comment(self):
        result = parse("FOO=bar # comment")
        self.assertEqual(result, {"FOO": "bar"})

    def test_full_line_comment(self):
        result = parse("# full line comment\nFOO=bar\n")
        self.assertEqual(result, {"FOO": "bar"})

    def test_empty_lines_ignored(self):
        result = parse("\n\nFOO=bar\n\n\n")
        self.assertEqual(result, {"FOO": "bar"})

    def test_empty_value(self):
        result = parse("FOO=")
        self.assertEqual(result, {"FOO": ""})

    def test_export_prefix(self):
        result = parse("export FOO=bar")
        self.assertEqual(result, {"FOO": "bar"})

    def test_variable_interpolation(self):
        result = parse("FOO=${BAR}")
        self.assertEqual(result, {"FOO": "${BAR}"})

    def test_multiline_continuation(self):
        result = parse("FOO=hello\\\nworld")
        self.assertEqual(result, {"FOO": "helloworld"})

    def test_missing_value_no_key(self):
        result = parse("=bar")
        self.assertEqual(result, {})


class TestDotenvSerialize(unittest.TestCase):
    def test_basic_serialize(self):
        result = serialize({"FOO": "bar"})
        self.assertEqual(result.strip(), "FOO=bar")

    def test_quoted_value_with_spaces(self):
        result = serialize({"FOO": "hello world"})
        self.assertEqual(result.strip(), 'FOO="hello world"')

    def test_quoted_value_with_newline(self):
        result = serialize({"FOO": "hello\nworld"})
        self.assertEqual(result.strip(), 'FOO="hello\\nworld"')

    def test_quoted_value_with_double_quote(self):
        result = serialize({"FOO": 'hello"world'})
        self.assertEqual(result.strip(), 'FOO="hello\\"world"')

    def test_escape_backslash_in_value(self):
        result = serialize({"FOO": "hello\\world"})
        self.assertIn("\\\\", result)

    def test_empty_value_no_quotes(self):
        result = serialize({"FOO": ""})
        self.assertEqual(result.strip(), "FOO=")


class TestDotenvRoundtrip(unittest.TestCase):
    def test_roundtrip(self):
        original = {"FOO": "bar", "BAZ": "hello world"}
        serialized = serialize(original)
        parsed = parse(serialized)
        self.assertEqual(parsed, original)

    def test_roundtrip_with_newlines(self):
        original = {"FOO": "hello\nworld"}
        serialized = serialize(original)
        parsed = parse(serialized)
        self.assertEqual(parsed, original)


class TestDotenvLoad(unittest.TestCase):
    def test_load_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            load("/nonexistent/path/.env")


if __name__ == "__main__":
    unittest.main()