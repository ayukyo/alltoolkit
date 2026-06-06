"""
Test suite for syntax_highlight module.

Run with: python -m pytest test_syntax_highlight.py -v
Or: python test_syntax_highlight.py
"""

import unittest
from syntax_highlight import (
    Lexer, Token, TokenType, Highlighter,
    highlight, highlight_html, get_tokens, strip_ansi,
    ANSI_THEME, HTML_THEME, PYTHON_KEYWORDS, PYTHON_BUILTINS
)


class TestLexer(unittest.TestCase):
    """Test the Lexer class."""
    
    def setUp(self):
        self.lexer = Lexer("", "python")
    
    def test_empty_code(self):
        """Test tokenizing empty code."""
        self.lexer.code = ""
        tokens = self.lexer.tokenize()
        self.assertEqual(tokens, [])
    
    def test_whitespace(self):
        """Test whitespace tokenization."""
        self.lexer.code = "    "
        tokens = self.lexer.tokenize()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.WHITESPACE)
        self.assertEqual(tokens[0].value, "    ")
    
    def test_newline(self):
        """Test newline tokenization."""
        self.lexer.code = "\n"
        tokens = self.lexer.tokenize()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.NEWLINE)
    
    def test_keyword(self):
        """Test keyword recognition."""
        self.lexer.code = "def"
        tokens = self.lexer.tokenize()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.KEYWORD)
    
    def test_builtin(self):
        """Test builtin recognition."""
        self.lexer.code = "print"
        tokens = self.lexer.tokenize()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.BUILTIN)
    
    def test_string_double_quote(self):
        """Test double-quoted string."""
        self.lexer.code = '"hello world"'
        tokens = self.lexer.tokenize()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.STRING)
        self.assertEqual(tokens[0].value, '"hello world"')
    
    def test_string_single_quote(self):
        """Test single-quoted string."""
        self.lexer.code = "'hello'"
        tokens = self.lexer.tokenize()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.STRING)
    
    def test_string_with_escape(self):
        """Test string with escape sequences."""
        self.lexer.code = r'"hello\nworld"'
        tokens = self.lexer.tokenize()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.STRING)
    
    def test_triple_quoted_string(self):
        """Test triple-quoted string."""
        self.lexer.code = '"""hello\nworld"""'
        tokens = self.lexer.tokenize()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.STRING)
    
    def test_fstring(self):
        """Test f-string."""
        self.lexer.code = 'f"value: {x}"'
        tokens = self.lexer.tokenize()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.STRING)
    
    def test_number_integer(self):
        """Test integer number."""
        self.lexer.code = "42"
        tokens = self.lexer.tokenize()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
    
    def test_number_float(self):
        """Test float number."""
        self.lexer.code = "3.14159"
        tokens = self.lexer.tokenize()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
    
    def test_number_hex(self):
        """Test hexadecimal number."""
        self.lexer.code = "0xFF"
        tokens = self.lexer.tokenize()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[0].value, "0xFF")
    
    def test_number_binary(self):
        """Test binary number."""
        self.lexer.code = "0b1010"
        tokens = self.lexer.tokenize()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[0].value, "0b1010")
    
    def test_number_scientific(self):
        """Test scientific notation."""
        self.lexer.code = "1.5e-10"
        tokens = self.lexer.tokenize()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
    
    def test_comment(self):
        """Test comment."""
        self.lexer.code = "# This is a comment"
        tokens = self.lexer.tokenize()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.COMMENT)
    
    def test_decorator(self):
        """Test decorator."""
        self.lexer.code = "@property"
        tokens = self.lexer.tokenize()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.DECORATOR)
    
    def test_operator_simple(self):
        """Test simple operators."""
        self.lexer.code = "+ - * /"
        tokens = self.lexer.tokenize()
        operators = [t for t in tokens if t.type == TokenType.OPERATOR]
        self.assertEqual(len(operators), 4)
    
    def test_operator_complex(self):
        """Test complex operators."""
        self.lexer.code = "== != += **="
        tokens = self.lexer.tokenize()
        operators = [t for t in tokens if t.type == TokenType.OPERATOR]
        self.assertEqual(len(operators), 4)
    
    def test_brackets(self):
        """Test brackets."""
        self.lexer.code = "()[]{}"
        tokens = self.lexer.tokenize()
        brackets = [t for t in tokens if t.type == TokenType.BRACKET]
        self.assertEqual(len(brackets), 6)
    
    def test_class_name(self):
        """Test class name recognition."""
        self.lexer.code = "MyClass"
        tokens = self.lexer.tokenize()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.CLASS)
    
    def test_constant(self):
        """Test constant recognition."""
        self.lexer.code = "MY_CONSTANT"
        tokens = self.lexer.tokenize()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.CONSTANT)
    
    def test_true_false_none(self):
        """Test boolean and None literals."""
        for literal in ["True", "False", "None"]:
            self.lexer.code = literal
            self.lexer.pos = 0
            tokens = self.lexer.tokenize()
            self.assertEqual(len(tokens), 1)
            self.assertEqual(tokens[0].type, TokenType.CONSTANT)


class TestHighlighter(unittest.TestCase):
    """Test the Highlighter class."""
    
    def setUp(self):
        self.highlighter = Highlighter(ansi=True)
        self.highlighter_html = Highlighter(ansi=False)
    
    def test_highlight_simple(self):
        """Test simple highlighting."""
        lexer = Lexer("def test(): pass", "python")
        tokens = lexer.tokenize()
        result = self.highlighter.highlight(tokens)
        self.assertIn("def", result)
        self.assertIn("test", result)
    
    def test_highlight_with_line_numbers(self):
        """Test highlighting with line numbers."""
        code = "line1\nline2\nline3"
        lexer = Lexer(code, "python")
        tokens = lexer.tokenize()
        result = self.highlighter.highlight(tokens, line_numbers=True)
        self.assertIn("1 |", result)
        self.assertIn("2 |", result)
        self.assertIn("3 |", result)
    
    def test_html_output(self):
        """Test HTML output."""
        lexer = Lexer("def test(): pass", "python")
        tokens = lexer.tokenize()
        result = self.highlighter_html.highlight_html(tokens)
        self.assertIn("<pre", result)
        self.assertIn("<span", result)
        self.assertIn("</span>", result)
        self.assertIn("</pre>", result)
    
    def test_html_escape(self):
        """Test HTML escaping."""
        result = self.highlighter_html._escape_html("<script>alert('xss')</script>")
        self.assertIn("&lt;", result)
        self.assertIn("&gt;", result)
        self.assertNotIn("<script>", result)
    
    def test_html_with_line_numbers(self):
        """Test HTML output with line numbers."""
        code = "line1\nline2"
        lexer = Lexer(code, "python")
        tokens = lexer.tokenize()
        result = self.highlighter_html.highlight_html(tokens, line_numbers=True)
        self.assertIn("1", result)
        self.assertIn("2", result)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_highlight_function(self):
        """Test highlight() function."""
        code = "def hello(): print('world')"
        result = highlight(code)
        self.assertIsInstance(result, str)
        self.assertIn("def", result)
        self.assertIn("print", result)
    
    def test_highlight_html_function(self):
        """Test highlight_html() function."""
        code = "def hello(): print('world')"
        result = highlight_html(code)
        self.assertIn("<pre", result)
        self.assertIn("def", result)
    
    def test_get_tokens_function(self):
        """Test get_tokens() function."""
        code = "x = 42"
        tokens = get_tokens(code)
        self.assertIsInstance(tokens, list)
        self.assertTrue(len(tokens) > 0)
        self.assertIsInstance(tokens[0], Token)
    
    def test_strip_ansi(self):
        """Test strip_ansi() function."""
        text = "\033[38;5;141mdef\033[0m"
        result = strip_ansi(text)
        self.assertEqual(result, "def")
    
    def test_highlight_with_line_numbers(self):
        """Test highlight with line numbers."""
        code = "line1\nline2\nline3"
        result = highlight(code, line_numbers=True)
        self.assertIn("1 |", result)
        self.assertIn("2 |", result)
        self.assertIn("3 |", result)


class TestJavaScriptLanguage(unittest.TestCase):
    """Test JavaScript language support."""
    
    def test_js_keywords(self):
        """Test JavaScript keyword recognition."""
        lexer = Lexer("const let async await", "javascript")
        tokens = lexer.tokenize()
        keywords = [t for t in tokens if t.type == TokenType.KEYWORD]
        self.assertEqual(len(keywords), 4)
    
    def test_js_builtins(self):
        """Test JavaScript builtin recognition."""
        lexer = Lexer("console.log Math.random", "javascript")
        tokens = lexer.tokenize()
        builtins = [t for t in tokens if t.type == TokenType.BUILTIN]
        self.assertGreaterEqual(len(builtins), 2)
    
    def test_js_comment(self):
        """Test JavaScript comment."""
        lexer = Lexer("// This is a comment", "javascript")
        tokens = lexer.tokenize()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.COMMENT)
    
    def test_js_block_comment(self):
        """Test JavaScript block comment."""
        lexer = Lexer("/* multi\nline */", "javascript")
        tokens = lexer.tokenize()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.COMMENT)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases."""
    
    def test_empty_string(self):
        """Test empty string handling."""
        result = highlight("")
        self.assertEqual(result, "")
    
    def test_only_whitespace(self):
        """Test whitespace-only string."""
        result = highlight("   \t\n   ")
        self.assertIn(" ", result)
    
    def test_unclosed_string(self):
        """Test unclosed string handling."""
        lexer = Lexer('"unclosed', "python")
        tokens = lexer.tokenize()
        # Should still tokenize, just won't have closing quote
        self.assertTrue(len(tokens) > 0)
    
    def test_mixed_content(self):
        """Test code with mixed content types."""
        code = '''
# Comment
def func():
    """Docstring"""
    x = 42  # inline comment
    return "result"
'''
        tokens = get_tokens(code)
        types = [t.type for t in tokens]
        self.assertIn(TokenType.COMMENT, types)
        self.assertIn(TokenType.KEYWORD, types)
        self.assertIn(TokenType.STRING, types)
        self.assertIn(TokenType.NUMBER, types)


class TestPerformance(unittest.TestCase):
    """Test performance characteristics."""
    
    def test_large_code(self):
        """Test tokenizing large code efficiently."""
        # Generate a large piece of code
        lines = ["x = 42  # comment"] * 1000
        code = "\n".join(lines)
        
        # Should complete without timeout
        tokens = get_tokens(code)
        self.assertEqual(len(tokens), 4000)  # 1000 * (id + ws + op + ws + num + ws + comment + newline)


def run_demo():
    """Run a demonstration of the syntax highlighter."""
    print("\n" + "=" * 60)
    print("Syntax Highlighter Demo")
    print("=" * 60)
    
    # Python code
    python_code = '''
def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Constants
MAX_VALUE = 100
'''
    
    print("\n--- Python Code ---")
    print(highlight(python_code, lang="python", line_numbers=True))
    
    # JavaScript code
    js_code = '''
const fetchData = async (url) => {
    const response = await fetch(url);
    return response.json();
};

class Calculator {
    constructor(value = 0) {
        this.value = value;
    }
}
'''
    
    print("\n--- JavaScript Code ---")
    print(highlight(js_code, lang="javascript"))
    
    # Show HTML output
    html = highlight_html("def hello(): print('World')")
    print("\n--- HTML Output Sample ---")
    print(html)


if __name__ == "__main__":
    # Run unit tests
    print("Running unit tests...")
    unittest.main(verbosity=2, exit=False)
    
    # Run demo
    run_demo()