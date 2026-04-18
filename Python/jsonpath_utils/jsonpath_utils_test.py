"""
AllToolkit - JSONPath Utilities Tests

Comprehensive test suite covering all JSONPath functionality.
"""

import unittest
import json
from typing import Any, Dict, List

# Import the module
from mod import (
    JSONPath, JSONPathError, JSONPathSyntaxError,
    find, find_one, compile, validate,
    JSONPathLexer, JSONPathParser, JSONPathEvaluator,
    TokenType, Token
)


# =============================================================================
# Test Data
# =============================================================================

# Sample JSON data from JSONPath specification
SAMPLE_DATA = {
    "store": {
        "book": [
            {
                "category": "reference",
                "author": "Nigel Rees",
                "title": "Sayings of the Century",
                "price": 8.95
            },
            {
                "category": "fiction",
                "author": "Evelyn Waugh",
                "title": "Sword of Honour",
                "price": 12.99
            },
            {
                "category": "fiction",
                "author": "Herman Melville",
                "title": "Moby Dick",
                "isbn": "0-553-21311-3",
                "price": 8.99
            },
            {
                "category": "fiction",
                "author": "J. R. R. Tolkien",
                "title": "The Lord of the Rings",
                "isbn": "0-395-19395-8",
                "price": 22.99
            }
        ],
        "bicycle": {
            "color": "red",
            "price": 19.95
        }
    },
    "expensive": 10
}

ARRAY_DATA = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

NESTED_ARRAY = {
    "items": [
        {"id": 1, "tags": ["a", "b", "c"]},
        {"id": 2, "tags": ["d", "e"]},
        {"id": 3, "tags": ["f"]}
    ]
}

DEEP_NESTED = {
    "level1": {
        "level2": {
            "level3": {
                "level4": {
                    "value": "deep"
                }
            }
        }
    }
}


# =============================================================================
# Lexer Tests
# =============================================================================

class TestJSONPathLexer(unittest.TestCase):
    """Test JSONPath lexer/tokenizer."""
    
    def test_tokenize_root(self):
        """Test root token."""
        lexer = JSONPathLexer('$')
        tokens = lexer.tokenize()
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenType.ROOT)
        self.assertEqual(tokens[1].type, TokenType.EOF)
    
    def test_tokenize_current(self):
        """Test current node token."""
        lexer = JSONPathLexer('@')
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.CURRENT)
    
    def test_tokenize_dot(self):
        """Test dot token."""
        lexer = JSONPathLexer('$.name')
        tokens = lexer.tokenize()
        self.assertEqual(tokens[1].type, TokenType.DOT)
        self.assertEqual(tokens[2].type, TokenType.NAME)
        self.assertEqual(tokens[2].value, 'name')
    
    def test_tokenize_recursive(self):
        """Test recursive descent token."""
        lexer = JSONPathLexer('$..name')
        tokens = lexer.tokenize()
        self.assertEqual(tokens[1].type, TokenType.DOTDOT)
    
    def test_tokenize_bracket_index(self):
        """Test bracket index tokens."""
        lexer = JSONPathLexer('$[0]')
        tokens = lexer.tokenize()
        self.assertEqual(tokens[1].type, TokenType.LBRACKET)
        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertEqual(tokens[2].value, 0)
        self.assertEqual(tokens[3].type, TokenType.RBRACKET)
    
    def test_tokenize_bracket_string(self):
        """Test bracket with string."""
        lexer = JSONPathLexer('$["name"]')
        tokens = lexer.tokenize()
        self.assertEqual(tokens[2].type, TokenType.STRING)
        self.assertEqual(tokens[2].value, 'name')
    
    def test_tokenize_wildcard(self):
        """Test wildcard token."""
        lexer = JSONPathLexer('$.*')
        tokens = lexer.tokenize()
        self.assertEqual(tokens[2].type, TokenType.STAR)
    
    def test_tokenize_slice(self):
        """Test slice tokens."""
        lexer = JSONPathLexer('$[1:5]')
        tokens = lexer.tokenize()
        self.assertEqual(tokens[2].value, 1)
        self.assertEqual(tokens[3].type, TokenType.COLON)
        self.assertEqual(tokens[4].value, 5)
    
    def test_tokenize_union(self):
        """Test union tokens."""
        lexer = JSONPathLexer('$[0,1,2]')
        tokens = lexer.tokenize()
        self.assertEqual(tokens[2].value, 0)
        self.assertEqual(tokens[3].type, TokenType.COMMA)
        self.assertEqual(tokens[4].value, 1)
    
    def test_tokenize_filter(self):
        """Test filter tokens."""
        lexer = JSONPathLexer('$[?(@.price < 10)]')
        tokens = lexer.tokenize()
        self.assertEqual(tokens[2].type, TokenType.QUESTION)
        self.assertEqual(tokens[3].type, TokenType.LPAREN)
        self.assertEqual(tokens[4].type, TokenType.CURRENT)
    
    def test_tokenize_comparison_operators(self):
        """Test comparison operator tokens."""
        lexer = JSONPathLexer('$[?(@.x == @.y)]')
        tokens = lexer.tokenize()
        # Find == operator
        eq_tokens = [t for t in tokens if t.type == TokenType.EQ]
        self.assertEqual(len(eq_tokens), 1)
    
    def test_tokenize_logical_operators(self):
        """Test logical operator tokens."""
        lexer = JSONPathLexer('$[?(@.x > 0 && @.y < 10)]')
        tokens = lexer.tokenize()
        and_tokens = [t for t in tokens if t.type == TokenType.AND]
        self.assertEqual(len(and_tokens), 1)
    
    def test_tokenize_negative_index(self):
        """Test negative index."""
        lexer = JSONPathLexer('$[-1]')
        tokens = lexer.tokenize()
        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertEqual(tokens[2].value, -1)
    
    def test_tokenize_float(self):
        """Test float number."""
        lexer = JSONPathLexer('$[?(@.price == 8.95)]')
        tokens = lexer.tokenize()
        float_tokens = [t for t in tokens if t.type == TokenType.NUMBER and isinstance(t.value, float)]
        self.assertTrue(len(float_tokens) > 0)
    
    def test_tokenize_string_escapes(self):
        """Test string escape sequences."""
        lexer = JSONPathLexer('$["hello\\nworld"]')
        tokens = lexer.tokenize()
        self.assertEqual(tokens[2].value, 'hello\nworld')
    
    def test_tokenize_error_invalid_char(self):
        """Test error on invalid character."""
        lexer = JSONPathLexer('$#')
        with self.assertRaises(JSONPathSyntaxError):
            lexer.tokenize()
    
    def test_tokenize_error_unterminated_string(self):
        """Test error on unterminated string."""
        lexer = JSONPathLexer('$["unclosed')
        with self.assertRaises(JSONPathSyntaxError):
            lexer.tokenize()


# =============================================================================
# Parser Tests
# =============================================================================

class TestJSONPathParser(unittest.TestCase):
    """Test JSONPath parser."""
    
    def test_parse_root_only(self):
        """Test parsing root only."""
        lexer = JSONPathLexer('$')
        tokens = lexer.tokenize()
        parser = JSONPathParser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast), 1)
        self.assertIsInstance(ast[0], type(None).__class__.__bases__[0])  # RootNode
    
    def test_parse_child_dot(self):
        """Test parsing child accessor."""
        lexer = JSONPathLexer('$.store')
        tokens = lexer.tokenize()
        parser = JSONPathParser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast), 2)
        # Check second node is ChildNode
        from mod import ChildNode
        self.assertIsInstance(ast[1], ChildNode)
        self.assertEqual(ast[1].name, 'store')
    
    def test_parse_child_bracket(self):
        """Test parsing child with bracket."""
        lexer = JSONPathLexer('$["store"]')
        tokens = lexer.tokenize()
        parser = JSONPathParser(tokens)
        ast = parser.parse()
        from mod import ChildNode
        self.assertIsInstance(ast[1], ChildNode)
    
    def test_parse_index(self):
        """Test parsing array index."""
        lexer = JSONPathLexer('$[0]')
        tokens = lexer.tokenize()
        parser = JSONPathParser(tokens)
        ast = parser.parse()
        from mod import IndexNode
        self.assertIsInstance(ast[1], IndexNode)
        self.assertEqual(ast[1].index, 0)
    
    def test_parse_slice(self):
        """Test parsing slice."""
        lexer = JSONPathLexer('$[1:5]')
        tokens = lexer.tokenize()
        parser = JSONPathParser(tokens)
        ast = parser.parse()
        from mod import SliceNode
        self.assertIsInstance(ast[1], SliceNode)
        self.assertEqual(ast[1].start, 1)
        self.assertEqual(ast[1].end, 5)
    
    def test_parse_slice_full(self):
        """Test full slice."""
        lexer = JSONPathLexer('$[1:5:2]')
        tokens = lexer.tokenize()
        parser = JSONPathParser(tokens)
        ast = parser.parse()
        from mod import SliceNode
        self.assertEqual(ast[1].step, 2)
    
    def test_parse_wildcard_dot(self):
        """Test wildcard after dot."""
        lexer = JSONPathLexer('$.*')
        tokens = lexer.tokenize()
        parser = JSONPathParser(tokens)
        ast = parser.parse()
        from mod import WildcardNode
        self.assertIsInstance(ast[1], WildcardNode)
    
    def test_parse_wildcard_bracket(self):
        """Test wildcard in bracket."""
        lexer = JSONPathLexer('$[*]')
        tokens = lexer.tokenize()
        parser = JSONPathParser(tokens)
        ast = parser.parse()
        from mod import WildcardNode
        self.assertIsInstance(ast[1], WildcardNode)
    
    def test_parse_recursive(self):
        """Test recursive descent."""
        lexer = JSONPathLexer('$..price')
        tokens = lexer.tokenize()
        parser = JSONPathParser(tokens)
        ast = parser.parse()
        from mod import RecursiveNode, ChildNode
        self.assertIsInstance(ast[1], RecursiveNode)
        self.assertIsInstance(ast[2], ChildNode)
    
    def test_parse_union(self):
        """Test union expression."""
        lexer = JSONPathLexer('$[0,1,2]')
        tokens = lexer.tokenize()
        parser = JSONPathParser(tokens)
        ast = parser.parse()
        from mod import UnionNode
        self.assertIsInstance(ast[1], UnionNode)
        self.assertEqual(ast[1].indices, [0, 1, 2])
    
    def test_parse_filter(self):
        """Test filter expression."""
        lexer = JSONPathLexer('$[?(@.price < 10)]')
        tokens = lexer.tokenize()
        parser = JSONPathParser(tokens)
        ast = parser.parse()
        from mod import FilterNode
        self.assertIsInstance(ast[1], FilterNode)
    
    def test_parse_error_no_root(self):
        """Test error when no root."""
        lexer = JSONPathLexer('.name')
        tokens = lexer.tokenize()
        parser = JSONPathParser(tokens)
        with self.assertRaises(JSONPathSyntaxError):
            parser.parse()


# =============================================================================
# Basic Query Tests
# =============================================================================

class TestBasicQueries(unittest.TestCase):
    """Test basic JSONPath queries."""
    
    def test_root(self):
        """Test root query."""
        path = JSONPath('$')
        result = path.query(SAMPLE_DATA)
        self.assertEqual(result, [SAMPLE_DATA])
    
    def test_single_child(self):
        """Test single child accessor."""
        path = JSONPath('$.store')
        result = path.query(SAMPLE_DATA)
        self.assertEqual(result, [SAMPLE_DATA['store']])
    
    def test_nested_child(self):
        """Test nested child accessors."""
        path = JSONPath('$.store.bicycle')
        result = path.query(SAMPLE_DATA)
        self.assertEqual(result, [SAMPLE_DATA['store']['bicycle']])
    
    def test_child_bracket_string(self):
        """Test child accessor with bracket."""
        path = JSONPath('$["store"]["bicycle"]')
        result = path.query(SAMPLE_DATA)
        self.assertEqual(result, [SAMPLE_DATA['store']['bicycle']])
    
    def test_child_mixed_access(self):
        """Test mixing dot and bracket access."""
        path = JSONPath('$.store["bicycle"].color')
        result = path.query(SAMPLE_DATA)
        self.assertEqual(result, ['red'])
    
    def test_array_index(self):
        """Test array index accessor."""
        path = JSONPath('$.store.book[0]')
        result = path.query(SAMPLE_DATA)
        self.assertEqual(result, [SAMPLE_DATA['store']['book'][0]])
    
    def test_array_negative_index(self):
        """Test negative array index."""
        path = JSONPath('$.store.book[-1]')
        result = path.query(SAMPLE_DATA)
        self.assertEqual(result, [SAMPLE_DATA['store']['book'][3]])
    
    def test_array_index_on_simple_array(self):
        """Test index on simple array."""
        path = JSONPath('$[0]')
        result = path.query(ARRAY_DATA)
        self.assertEqual(result, [1])
    
    def test_missing_child_empty_result(self):
        """Test missing child returns empty."""
        path = JSONPath('$.nonexistent')
        result = path.query(SAMPLE_DATA)
        self.assertEqual(result, [])
    
    def test_missing_index_empty_result(self):
        """Test missing index returns empty."""
        path = JSONPath('$[100]')
        result = path.query(ARRAY_DATA)
        self.assertEqual(result, [])


# =============================================================================
# Wildcard Tests
# =============================================================================

class TestWildcardQueries(unittest.TestCase):
    """Test wildcard queries."""
    
    def test_wildcard_on_dict(self):
        """Test wildcard on dictionary."""
        path = JSONPath('$.store.*')
        result = path.query(SAMPLE_DATA)
        self.assertEqual(len(result), 2)
        self.assertIn(SAMPLE_DATA['store']['book'], result)
        self.assertIn(SAMPLE_DATA['store']['bicycle'], result)
    
    def test_wildcard_on_array(self):
        """Test wildcard on array."""
        path = JSONPath('$.store.book[*]')
        result = path.query(SAMPLE_DATA)
        self.assertEqual(len(result), 4)
    
    def test_wildcard_with_bracket(self):
        """Test wildcard in bracket."""
        path = JSONPath('$[*]')
        result = path.query(ARRAY_DATA)
        self.assertEqual(result, ARRAY_DATA)
    
    def test_wildcard_nested(self):
        """Test nested wildcard."""
        path = JSONPath('$.store.book[*].author')
        result = path.query(SAMPLE_DATA)
        expected = ['Nigel Rees', 'Evelyn Waugh', 'Herman Melville', 'J. R. R. Tolkien']
        self.assertEqual(result, expected)
    
    def test_wildcard_on_nested_array(self):
        """Test wildcard on nested array."""
        path = JSONPath('$.items[*].tags[*]')
        result = path.query(NESTED_ARRAY)
        self.assertEqual(result, ['a', 'b', 'c', 'd', 'e', 'f'])


# =============================================================================
# Slice Tests
# =============================================================================

class TestSliceQueries(unittest.TestCase):
    """Test slice queries."""
    
    def test_slice_start_end(self):
        """Test slice with start and end."""
        path = JSONPath('$[1:4]')
        result = path.query(ARRAY_DATA)
        self.assertEqual(result, [2, 3, 4])
    
    def test_slice_start_only(self):
        """Test slice with only start."""
        path = JSONPath('$[5:]')
        result = path.query(ARRAY_DATA)
        self.assertEqual(result, [6, 7, 8, 9, 10])
    
    def test_slice_end_only(self):
        """Test slice with only end."""
        path = JSONPath('$[:3]')
        result = path.query(ARRAY_DATA)
        self.assertEqual(result, [1, 2, 3])
    
    def test_slice_with_step(self):
        """Test slice with step."""
        path = JSONPath('$[::2]')
        result = path.query(ARRAY_DATA)
        self.assertEqual(result, [1, 3, 5, 7, 9])
    
    def test_slice_negative_start(self):
        """Test slice with negative start."""
        path = JSONPath('$[-3:]')
        result = path.query(ARRAY_DATA)
        self.assertEqual(result, [8, 9, 10])
    
    def test_slice_negative_end(self):
        """Test slice with negative end."""
        path = JSONPath('$[:-2]')
        result = path.query(ARRAY_DATA)
        self.assertEqual(result, [1, 2, 3, 4, 5, 6, 7, 8])
    
    def test_slice_on_book_array(self):
        """Test slice on book array."""
        path = JSONPath('$.store.book[0:2]')
        result = path.query(SAMPLE_DATA)
        self.assertEqual(len(result), 2)


# =============================================================================
# Union Tests
# =============================================================================

class TestUnionQueries(unittest.TestCase):
    """Test union queries."""
    
    def test_union_indices(self):
        """Test union with indices."""
        path = JSONPath('$[0,2,4]')
        result = path.query(ARRAY_DATA)
        self.assertEqual(result, [1, 3, 5])
    
    def test_union_negative_indices(self):
        """Test union with negative indices."""
        path = JSONPath('$[-1,-2]')
        result = path.query(ARRAY_DATA)
        self.assertEqual(result, [10, 9])
    
    def test_union_on_object_keys(self):
        """Test union on object keys."""
        path = JSONPath('$["store","expensive"]')
        result = path.query(SAMPLE_DATA)
        self.assertEqual(len(result), 2)


# =============================================================================
# Recursive Descent Tests
# =============================================================================

class TestRecursiveQueries(unittest.TestCase):
    """Test recursive descent queries."""
    
    def test_recursive_find_all_prices(self):
        """Test recursive finding all prices."""
        path = JSONPath('$..price')
        result = path.query(SAMPLE_DATA)
        self.assertEqual(len(result), 5)  # 4 books + 1 bicycle
        expected_prices = [8.95, 12.99, 8.99, 22.99, 19.95]
        self.assertEqual(sorted(result), sorted(expected_prices))
    
    def test_recursive_find_all_authors(self):
        """Test recursive finding all authors."""
        path = JSONPath('$..author')
        result = path.query(SAMPLE_DATA)
        self.assertEqual(len(result), 4)
    
    def test_recursive_on_simple_array(self):
        """Test recursive on simple array."""
        path = JSONPath('$..')
        result = path.query(ARRAY_DATA)
        # Should return all elements and the array itself
        self.assertTrue(len(result) > 10)
    
    def test_recursive_find_value(self):
        """Test recursive finding deep value."""
        path = JSONPath('$..value')
        result = path.query(DEEP_NESTED)
        self.assertEqual(result, ['deep'])
    
    def test_recursive_with_wildcard(self):
        """Test recursive with wildcard."""
        path = JSONPath('$..*')
        result = path.query(SAMPLE_DATA)
        # Returns all values at all levels
        self.assertTrue(len(result) > 10)


# =============================================================================
# Filter Tests
# =============================================================================

class TestFilterQueries(unittest.TestCase):
    """Test filter expression queries."""
    
    def test_filter_less_than(self):
        """Test filter with less than."""
        path = JSONPath('$.store.book[?(@.price < 10)]')
        result = path.query(SAMPLE_DATA)
        self.assertEqual(len(result), 2)  # Books with price < 10
    
    def test_filter_equals(self):
        """Test filter with equals."""
        path = JSONPath('$.store.book[?(@.category == "fiction")]')
        result = path.query(SAMPLE_DATA)
        self.assertEqual(len(result), 3)
    
    def test_filter_not_equals(self):
        """Test filter with not equals."""
        path = JSONPath('$.store.book[?(@.category != "fiction")]')
        result = path.query(SAMPLE_DATA)
        self.assertEqual(len(result), 1)
    
    def test_filter_greater_than(self):
        """Test filter with greater than."""
        path = JSONPath('$.store.book[?(@.price > 20)]')
        result = path.query(SAMPLE_DATA)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'The Lord of the Rings')
    
    def test_filter_less_than_or_equal(self):
        """Test filter with less than or equal."""
        path = JSONPath('$.store.book[?(@.price <= 8.95)]')
        result = path.query(SAMPLE_DATA)
        self.assertEqual(len(result), 1)
    
    def test_filter_greater_than_or_equal(self):
        """Test filter with greater than or equal."""
        path = JSONPath('$.store.book[?(@.price >= 12)]')
        result = path.query(SAMPLE_DATA)
        self.assertEqual(len(result), 2)
    
    def test_filter_and(self):
        """Test filter with AND."""
        path = JSONPath('$.store.book[?(@.category == "fiction" && @.price < 10)]')
        result = path.query(SAMPLE_DATA)
        self.assertEqual(len(result), 1)  # Moby Dick
    
    def test_filter_or(self):
        """Test filter with OR."""
        path = JSONPath('$.store.book[?(@.price < 10 || @.price > 20)]')
        result = path.query(SAMPLE_DATA)
        # Books with price < 10: Sayings (8.95), Moby (8.99)
        # Books with price > 20: LOTR (22.99)
        self.assertEqual(len(result), 3)
    
    def test_filter_nested_path(self):
        """Test filter with nested path reference."""
        path = JSONPath('$.store.book[?(@.price < $.expensive)]')
        result = path.query(SAMPLE_DATA)
        self.assertEqual(len(result), 2)
    
    def test_filter_exists(self):
        """Test filter checking existence."""
        path = JSONPath('$.store.book[?(@.isbn)]')
        result = path.query(SAMPLE_DATA)
        self.assertEqual(len(result), 2)
    
    def test_filter_not_exists(self):
        """Test filter checking non-existence."""
        path = JSONPath('$.store.book[?(!@.isbn)]')
        result = path.query(SAMPLE_DATA)
        self.assertEqual(len(result), 2)


# =============================================================================
# Convenience Function Tests
# =============================================================================

class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_find_function(self):
        """Test find function."""
        result = find('$.store.book[*].author', SAMPLE_DATA)
        self.assertEqual(len(result), 4)
    
    def test_find_one_function(self):
        """Test find_one function."""
        result = find_one('$.store.bicycle.color', SAMPLE_DATA)
        self.assertEqual(result, 'red')
    
    def test_find_one_no_match(self):
        """Test find_one with no match."""
        result = find_one('$.nonexistent', SAMPLE_DATA)
        self.assertIsNone(result)
    
    def test_compile_function(self):
        """Test compile function."""
        path = compile('$.store.book[*]')
        result = path.query(SAMPLE_DATA)
        self.assertEqual(len(result), 4)
    
    def test_validate_function_valid(self):
        """Test validate with valid expression."""
        self.assertTrue(validate('$.store.book[*]'))
    
    def test_validate_function_invalid(self):
        """Test validate with invalid expression."""
        self.assertFalse(validate('invalid'))
    
    def test_reuse_compiled_path(self):
        """Test reusing compiled path."""
        path = compile('$.store.book[0].author')
        result1 = path.query(SAMPLE_DATA)
        result2 = path.query(SAMPLE_DATA)
        self.assertEqual(result1, result2)


# =============================================================================
# Edge Case Tests
# =============================================================================

class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary values."""
    
    def test_empty_object(self):
        """Test query on empty object."""
        path = JSONPath('$')
        result = path.query({})
        self.assertEqual(result, [{}])
    
    def test_empty_array(self):
        """Test query on empty array."""
        path = JSONPath('$[*]')
        result = path.query([])
        self.assertEqual(result, [])
    
    def test_null_value(self):
        """Test query on null."""
        path = JSONPath('$')
        result = path.query(None)
        self.assertEqual(result, [None])
    
    def test_primitive_string(self):
        """Test query on string."""
        path = JSONPath('$')
        result = path.query('hello')
        self.assertEqual(result, ['hello'])
    
    def test_primitive_number(self):
        """Test query on number."""
        path = JSONPath('$')
        result = path.query(42)
        self.assertEqual(result, [42])
    
    def test_out_of_bounds_positive(self):
        """Test positive index out of bounds."""
        path = JSONPath('$[1000]')
        result = path.query(ARRAY_DATA)
        self.assertEqual(result, [])
    
    def test_out_of_bounds_negative(self):
        """Test negative index out of bounds."""
        path = JSONPath('$[-100]')
        result = path.query([1, 2, 3])
        self.assertEqual(result, [])
    
    def test_empty_jsonpath(self):
        """Test empty JSONPath raises error."""
        with self.assertRaises(JSONPathSyntaxError):
            JSONPath('').query(SAMPLE_DATA)
    
    def test_invalid_jsonpath_no_root(self):
        """Test invalid JSONPath without root."""
        with self.assertRaises(JSONPathSyntaxError):
            JSONPath('store').query(SAMPLE_DATA)
    
    def test_query_one_empty(self):
        """Test query_one on empty result."""
        path = JSONPath('$.nonexistent')
        result = path.query_one(SAMPLE_DATA)
        self.assertIsNone(result)
    
    def test_unicode_keys(self):
        """Test unicode keys."""
        data = {'中文': 'value', '日本語': 'another'}
        result = find('$["中文"]', data)
        self.assertEqual(result, ['value'])
    
    def test_unicode_values(self):
        """Test unicode values."""
        data = {'key': '日本語テスト'}
        result = find('$.key', data)
        self.assertEqual(result, ['日本語テスト'])
    
    def test_special_characters_in_keys(self):
        """Test special characters in keys."""
        data = {'key-with-dash': 'value', 'key.with.dot': 'another'}
        result1 = find('$["key-with-dash"]', data)
        result2 = find('$["key.with.dot"]', data)
        self.assertEqual(result1, ['value'])
        self.assertEqual(result2, ['another'])
    
    def test_numeric_keys(self):
        """Test numeric string keys."""
        data = {'123': 'value'}
        result = find('$["123"]', data)
        self.assertEqual(result, ['value'])
    
    def test_boolean_values(self):
        """Test boolean values."""
        data = {'flag': True, 'neg_flag': False}
        result = find('$.flag', data)
        self.assertEqual(result, [True])
    
    def test_none_values(self):
        """Test None values in data."""
        data = {'null_field': None}
        result = find('$.null_field', data)
        self.assertEqual(result, [None])
    
    def test_mixed_array(self):
        """Test mixed type array."""
        data = {'mixed': [1, 'two', None, True, {'nested': 'value'}]}
        result = find('$.mixed[*]', data)
        self.assertEqual(len(result), 5)
    
    def test_very_long_path(self):
        """Test very long path."""
        path = JSONPath('$.level1.level2.level3.level4.value')
        result = path.query(DEEP_NESTED)
        self.assertEqual(result, ['deep'])
    
    def test_consecutive_wildcards(self):
        """Test consecutive wildcards."""
        data = {'a': {'b': [{'c': 1}, {'c': 2}]}}
        result = find('$.*.*.*.c', data)
        self.assertEqual(result, [1, 2])
    
    def test_large_array(self):
        """Test large array handling."""
        large_data = {'items': [{'id': i} for i in range(1000)]}
        result = find('$.items[500].id', large_data)
        self.assertEqual(result, [500])
    
    def test_large_array_slice(self):
        """Test slice on large array."""
        large_data = list(range(1000))
        result = find('$[990:]', large_data)
        self.assertEqual(result, list(range(990, 1000)))


# =============================================================================
# Error Handling Tests
# =============================================================================

class TestErrorHandling(unittest.TestCase):
    """Test error handling."""
    
    def test_syntax_error_invalid_operator(self):
        """Test syntax error on invalid operator."""
        with self.assertRaises(JSONPathSyntaxError):
            JSONPath('$[?(@.x === 1)]').query({})
    
    def test_type_error_on_non_data(self):
        """Test handling non-data types."""
        # Should not raise, just return empty or the value
        path = JSONPath('$')
        result = path.query(lambda x: x)  # Function as data
        self.assertEqual(len(result), 1)


# =============================================================================
# Match Tests
# =============================================================================

class TestMatch(unittest.TestCase):
    """Test match functionality."""
    
    def test_match_single(self):
        """Test match with single result."""
        path = JSONPath('$.store.bicycle.color')
        matches = path.match(SAMPLE_DATA)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]['path'], '$.store.bicycle.color')
        self.assertEqual(matches[0]['value'], 'red')
    
    def test_match_wildcard(self):
        """Test match with wildcard."""
        path = JSONPath('$.store.book[0].*')
        matches = path.match(SAMPLE_DATA)
        self.assertEqual(len(matches), 4)


# =============================================================================
# Run Tests
# =============================================================================

if __name__ == '__main__':
    unittest.main(verbosity=2)