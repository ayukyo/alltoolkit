"""
Tests for lexer_utils module.
"""

import unittest
from mod import (
    Lexer, LexerConfig, Token, TokenType, LexerError,
    tokenize, tokenize_keywords, extract_identifiers, extract_strings,
    extract_numbers, find_token, find_all_tokens, SimpleLexer, StreamingLexer
)


class TestToken(unittest.TestCase):
    """Test Token class."""
    
    def test_token_creation(self):
        """Test creating a token."""
        token = Token(TokenType.INTEGER, "42", 1, 5, 4, 6)
        self.assertEqual(token.type, TokenType.INTEGER)
        self.assertEqual(token.value, "42")
        self.assertEqual(token.line, 1)
        self.assertEqual(token.column, 5)
    
    def test_token_repr(self):
        """Test token string representation."""
        token = Token(TokenType.STRING, "hello", 2, 10, 9, 14)
        self.assertIn("STRING", repr(token))
        self.assertIn("hello", repr(token))
        self.assertIn("L2", repr(token))
    
    def test_token_equality(self):
        """Test token equality."""
        t1 = Token(TokenType.INTEGER, "42", 1, 1, 0, 2)
        t2 = Token(TokenType.INTEGER, "42", 2, 5, 10, 12)
        t3 = Token(TokenType.INTEGER, "43", 1, 1, 0, 2)
        self.assertEqual(t1, t2)  # Same type and value
        self.assertNotEqual(t1, t3)  # Different value


class TestLexerConfig(unittest.TestCase):
    """Test LexerConfig class."""
    
    def test_default_config(self):
        """Test default configuration."""
        config = LexerConfig()
        self.assertIn("if", config.keywords)  # Default empty set
        self.assertEqual(len(config.keywords), 0)
        self.assertTrue(config.skip_whitespace)
        self.assertTrue(config.skip_comments)
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = LexerConfig(
            keywords={"if", "else", "for"},
            skip_whitespace=False,
            allow_hex=False
        )
        self.assertEqual(len(config.keywords), 3)
        self.assertFalse(config.skip_whitespace)
        self.assertFalse(config.allow_hex)


class TestLexer(unittest.TestCase):
    """Test Lexer class."""
    
    def test_empty_input(self):
        """Test tokenizing empty input."""
        lexer = Lexer("")
        tokens = lexer.tokenize_all()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.EOF)
    
    def test_whitespace_only(self):
        """Test tokenizing whitespace only."""
        lexer = Lexer("   \t\t  ")
        tokens = lexer.tokenize_all()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.EOF)
    
    def test_integers(self):
        """Test integer tokenization."""
        lexer = Lexer("42 0 123456")
        tokens = lexer.tokenize_all()
        int_tokens = [t for t in tokens if t.type == TokenType.INTEGER]
        self.assertEqual(len(int_tokens), 3)
        self.assertEqual(int_tokens[0].value, "42")
        self.assertEqual(int_tokens[1].value, "0")
        self.assertEqual(int_tokens[2].value, "123456")
    
    def test_floats(self):
        """Test float tokenization."""
        lexer = Lexer("3.14 0.5 100.0")
        tokens = lexer.tokenize_all()
        float_tokens = [t for t in tokens if t.type == TokenType.FLOAT]
        self.assertEqual(len(float_tokens), 3)
        self.assertEqual(float_tokens[0].value, "3.14")
        self.assertEqual(float_tokens[1].value, "0.5")
        self.assertEqual(float_tokens[2].value, "100.0")
    
    def test_scientific_notation(self):
        """Test scientific notation."""
        lexer = Lexer("1e10 2.5e-3 1E+5")
        tokens = lexer.tokenize_all()
        float_tokens = [t for t in tokens if t.type == TokenType.FLOAT]
        self.assertEqual(len(float_tokens), 3)
        self.assertEqual(float_tokens[0].value, "1e10")
        self.assertEqual(float_tokens[1].value, "2.5e-3")
        self.assertEqual(float_tokens[2].value, "1E+5")
    
    def test_hex_numbers(self):
        """Test hexadecimal numbers."""
        lexer = Lexer("0xFF 0x1234 0xabcdef")
        tokens = lexer.tokenize_all()
        int_tokens = [t for t in tokens if t.type == TokenType.INTEGER]
        self.assertEqual(len(int_tokens), 3)
        self.assertEqual(int_tokens[0].value, "0xFF")
        self.assertEqual(int_tokens[1].value, "0x1234")
    
    def test_binary_numbers(self):
        """Test binary numbers."""
        lexer = Lexer("0b1010 0b1111 0b0")
        tokens = lexer.tokenize_all()
        int_tokens = [t for t in tokens if t.type == TokenType.INTEGER]
        self.assertEqual(len(int_tokens), 3)
        self.assertEqual(int_tokens[0].value, "0b1010")
        self.assertEqual(int_tokens[1].value, "0b1111")
    
    def test_octal_numbers(self):
        """Test octal numbers."""
        lexer = Lexer("0o77 0o123 0o0")
        tokens = lexer.tokenize_all()
        int_tokens = [t for t in tokens if t.type == TokenType.INTEGER]
        self.assertEqual(len(int_tokens), 3)
        self.assertEqual(int_tokens[0].value, "0o77")
    
    def test_strings(self):
        """Test string literals."""
        lexer = Lexer('"hello" \'world\' `template`')
        tokens = lexer.tokenize_all()
        str_tokens = [t for t in tokens if t.type == TokenType.STRING]
        self.assertEqual(len(str_tokens), 3)
        self.assertEqual(str_tokens[0].value, "hello")
        self.assertEqual(str_tokens[1].value, "world")
        self.assertEqual(str_tokens[2].value, "template")
    
    def test_string_escapes(self):
        """Test string escape sequences."""
        lexer = Lexer(r'"hello\nworld" "tab\there" "quote: \"test\""')
        tokens = lexer.tokenize_all()
        str_tokens = [t for t in tokens if t.type == TokenType.STRING]
        self.assertEqual(len(str_tokens), 3)
        self.assertIn("\n", str_tokens[0].value)
        self.assertIn("\t", str_tokens[1].value)
        self.assertIn('"', str_tokens[2].value)
    
    def test_identifiers(self):
        """Test identifier tokenization."""
        lexer = Lexer("foo bar_baz _private")
        tokens = lexer.tokenize_all()
        id_tokens = [t for t in tokens if t.type == TokenType.IDENTIFIER]
        self.assertEqual(len(id_tokens), 3)
        self.assertEqual(id_tokens[0].value, "foo")
        self.assertEqual(id_tokens[1].value, "bar_baz")
        self.assertEqual(id_tokens[2].value, "_private")
    
    def test_keywords(self):
        """Test keyword detection."""
        config = LexerConfig(keywords={"if", "else", "for"})
        lexer = Lexer("if condition else", config)
        tokens = lexer.tokenize_all()
        
        kw_tokens = [t for t in tokens if t.type == TokenType.KEYWORD]
        self.assertEqual(len(kw_tokens), 2)
        self.assertEqual(kw_tokens[0].value, "if")
        self.assertEqual(kw_tokens[1].value, "else")
        
        # "condition" should be an identifier
        id_tokens = [t for t in tokens if t.type == TokenType.IDENTIFIER]
        self.assertEqual(len(id_tokens), 1)
    
    def test_operators(self):
        """Test operator tokenization."""
        lexer = Lexer("+ - * / == != <= >= && ||")
        tokens = lexer.tokenize_all()
        op_tokens = [t for t in tokens if t.type == TokenType.OPERATOR]
        self.assertEqual(len(op_tokens), 9)
        self.assertEqual(op_tokens[0].value, "+")
        self.assertEqual(op_tokens[3].value, "==")
    
    def test_multi_char_operators(self):
        """Test multi-character operators."""
        lexer = Lexer("+= -= *= /= **= //=")
        tokens = lexer.tokenize_all()
        op_tokens = [t for t in tokens if t.type == TokenType.OPERATOR]
        self.assertEqual(len(op_tokens), 5)
        self.assertEqual(op_tokens[0].value, "+=")
        self.assertEqual(op_tokens[4].value, "//=")
    
    def test_structure_tokens(self):
        """Test structure tokens (brackets, etc.)."""
        lexer = Lexer("() [] {} , . : ;")
        tokens = lexer.tokenize_all()
        
        types = [t.type for t in tokens]
        self.assertIn(TokenType.LPAREN, types)
        self.assertIn(TokenType.RPAREN, types)
        self.assertIn(TokenType.LBRACKET, types)
        self.assertIn(TokenType.RBRACKET, types)
        self.assertIn(TokenType.LBRACE, types)
        self.assertIn(TokenType.RBRACE, types)
        self.assertIn(TokenType.COMMA, types)
        self.assertIn(TokenType.DOT, types)
        self.assertIn(TokenType.COLON, types)
        self.assertIn(TokenType.SEMICOLON, types)
    
    def test_comments_skip(self):
        """Test skipping comments."""
        lexer = Lexer("x = 1 # comment\ny = 2")
        tokens = lexer.tokenize_all()
        comment_tokens = [t for t in tokens if t.type == TokenType.COMMENT]
        self.assertEqual(len(comment_tokens), 0)  # Comments should be skipped
    
    def test_comments_preserve(self):
        """Test preserving comments."""
        config = LexerConfig(skip_comments=False)
        lexer = Lexer("x = 1 # comment", config)
        tokens = lexer.tokenize_all()
        comment_tokens = [t for t in tokens if t.type == TokenType.COMMENT]
        self.assertEqual(len(comment_tokens), 1)
    
    def test_multi_line_comment(self):
        """Test multi-line comments."""
        config = LexerConfig(skip_comments=True)
        lexer = Lexer("a /* comment */ b", config)
        tokens = lexer.tokenize_all()
        id_tokens = [t for t in tokens if t.type == TokenType.IDENTIFIER]
        self.assertEqual(len(id_tokens), 2)
        self.assertEqual(id_tokens[0].value, "a")
        self.assertEqual(id_tokens[1].value, "b")
    
    def test_position_tracking(self):
        """Test line and column tracking."""
        lexer = Lexer("ab\ncd")
        tokens = lexer.tokenize_all()
        
        ab_token = find_token(tokens, "ab")
        self.assertIsNotNone(ab_token)
        self.assertEqual(ab_token.line, 1)
        self.assertEqual(ab_token.column, 1)
        
        cd_token = find_token(tokens, "cd")
        self.assertIsNotNone(cd_token)
        self.assertEqual(cd_token.line, 2)
        self.assertEqual(cd_token.column, 1)
    
    def test_reset(self):
        """Test lexer reset."""
        lexer = Lexer("abc")
        list(lexer.tokenize())  # Consume all tokens
        self.assertEqual(lexer.pos, 3)
        
        lexer.reset()
        self.assertEqual(lexer.pos, 0)
        self.assertEqual(lexer.line, 1)
        self.assertEqual(lexer.column, 1)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_tokenize(self):
        """Test tokenize function."""
        tokens = tokenize("x = 42")
        self.assertTrue(len(tokens) > 0)
    
    def test_tokenize_keywords(self):
        """Test tokenize_keywords function."""
        tokens = tokenize_keywords("if else while", {"if", "else"})
        kw_tokens = [t for t in tokens if t.type == TokenType.KEYWORD]
        self.assertEqual(len(kw_tokens), 2)
    
    def test_extract_identifiers(self):
        """Test extract_identifiers function."""
        tokens = tokenize("foo bar 123")
        ids = extract_identifiers(tokens)
        self.assertEqual(ids, ["foo", "bar"])
    
    def test_extract_strings(self):
        """Test extract_strings function."""
        tokens = tokenize('"a" "b" "c"')
        strings = extract_strings(tokens)
        self.assertEqual(strings, ["a", "b", "c"])
    
    def test_extract_numbers(self):
        """Test extract_numbers function."""
        tokens = tokenize("1 2.5 3 4.0")
        numbers = extract_numbers(tokens)
        self.assertEqual(numbers, ["1", "2.5", "3", "4.0"])
    
    def test_find_token(self):
        """Test find_token function."""
        tokens = tokenize("foo bar baz")
        token = find_token(tokens, "bar")
        self.assertIsNotNone(token)
        self.assertEqual(token.value, "bar")
        
        self.assertIsNone(find_token(tokens, "qux"))
    
    def test_find_all_tokens(self):
        """Test find_all_tokens function."""
        tokens = tokenize("foo bar foo baz foo")
        foos = find_all_tokens(tokens, "foo")
        self.assertEqual(len(foos), 3)


class TestSimpleLexer(unittest.TestCase):
    """Test SimpleLexer class."""
    
    def test_basic_tokenize(self):
        """Test basic tokenization."""
        lexer = SimpleLexer("hello world")
        tokens = lexer.tokenize()
        self.assertEqual(tokens, ["hello", "world"])
    
    def test_custom_delimiters(self):
        """Test custom delimiters."""
        lexer = SimpleLexer("a,b,c", delimiters=",")
        tokens = lexer.tokenize()
        self.assertEqual(tokens, ["a", "b", "c"])
    
    def test_iteration(self):
        """Test iterator interface."""
        lexer = SimpleLexer("one two three")
        results = []
        for token, start, end in lexer:
            results.append((token, start, end))
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0], ("one", 0, 3))
    
    def test_empty_input(self):
        """Test empty input."""
        lexer = SimpleLexer("")
        tokens = lexer.tokenize()
        self.assertEqual(tokens, [])


class TestStreamingLexer(unittest.TestCase):
    """Test StreamingLexer class."""
    
    def test_single_feed(self):
        """Test feeding all at once."""
        lexer = StreamingLexer()
        tokens = lexer.feed("x = 42")
        self.assertTrue(len(tokens) > 0)
    
    def test_multiple_feeds(self):
        """Test feeding in chunks."""
        lexer = StreamingLexer()
        tokens = lexer.feed("x = ")
        self.assertEqual(len(tokens), 1)  # Just 'x'
        
        tokens = lexer.feed("42")
        self.assertTrue(len(tokens) >= 2)  # '=', '42'
    
    def test_flush(self):
        """Test flushing remaining buffer."""
        lexer = StreamingLexer()
        lexer.feed("x")  # Incomplete token without space
        tokens = lexer.flush()
        self.assertTrue(len(tokens) > 0)
    
    def test_preserve_newlines(self):
        """Test preserving newlines."""
        config = LexerConfig(preserve_newlines=True, skip_whitespace=False)
        lexer = StreamingLexer(config)
        tokens = lexer.feed("x\ny")
        newlines = [t for t in tokens if t.type == TokenType.NEWLINE]
        self.assertEqual(len(newlines), 1)


class TestComplexCode(unittest.TestCase):
    """Test tokenizing complex code."""
    
    def test_python_like_code(self):
        """Test Python-like code."""
        code = '''
def calculate(x, y):
    """Calculate sum."""
    result = x + y * 2
    return result
'''
        config = LexerConfig(
            keywords={"def", "return", "if", "else", "for", "while", "class"}
        )
        lexer = Lexer(code, config)
        tokens = lexer.tokenize_all()
        
        # Check keywords
        def_token = find_token(tokens, "def")
        self.assertIsNotNone(def_token)
        self.assertEqual(def_token.type, TokenType.KEYWORD)
        
        return_token = find_token(tokens, "return")
        self.assertIsNotNone(return_token)
        self.assertEqual(return_token.type, TokenType.KEYWORD)
        
        # Check identifiers
        calc_token = find_token(tokens, "calculate")
        self.assertIsNotNone(calc_token)
        self.assertEqual(calc_token.type, TokenType.IDENTIFIER)
    
    def test_json_like(self):
        """Test JSON-like content."""
        code = '{"name": "John", "age": 30, "active": true}'
        lexer = Lexer(code)
        tokens = lexer.tokenize_all()
        
        strings = extract_strings(tokens)
        self.assertIn("name", strings)
        self.assertIn("John", strings)
        
        numbers = extract_numbers(tokens)
        self.assertIn("30", numbers)
    
    def test_expression(self):
        """Test mathematical expression."""
        expr = "(a + b) * c / (d - e)"
        tokens = tokenize(expr)
        
        ids = extract_identifiers(tokens)
        self.assertEqual(ids, ["a", "b", "c", "d", "e"])
        
        ops = [t.value for t in tokens if t.type == TokenType.OPERATOR]
        self.assertEqual(ops, ["+", "*", "/", "-"])


if __name__ == "__main__":
    unittest.main()