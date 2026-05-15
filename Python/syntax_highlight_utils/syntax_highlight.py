"""
Syntax Highlight Utilities - A zero-dependency syntax highlighter for Python.

This module provides syntax highlighting capabilities for multiple programming
languages without any external dependencies. It supports both terminal (ANSI)
and HTML output formats.

Features:
- Python syntax highlighting (built-in)
- JSON/YAML highlighting
- JavaScript-like syntax support
- Configurable color themes
- Line number support
- Both ANSI and HTML output

Example:
    >>> from syntax_highlight import highlight, highlight_html
    >>> code = 'def hello(): print("World")'
    >>> print(highlight(code, lang='python'))
    >>> print(highlight_html(code, lang='python'))
"""

import re
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass


class TokenType(Enum):
    """Token types for syntax highlighting."""
    KEYWORD = "keyword"
    STRING = "string"
    NUMBER = "number"
    COMMENT = "comment"
    OPERATOR = "operator"
    FUNCTION = "function"
    CLASS = "class"
    DECORATOR = "decorator"
    VARIABLE = "variable"
    BUILTIN = "builtin"
    CONSTANT = "constant"
    PUNCTUATION = "punctuation"
    BRACKET = "bracket"
    WHITESPACE = "whitespace"
    NEWLINE = "newline"
    UNKNOWN = "unknown"


@dataclass
class Token:
    """Represents a syntax token."""
    type: TokenType
    value: str
    start: int
    end: int


# Color themes
ANSI_THEME = {
    TokenType.KEYWORD: "\033[38;5;141m",      # Purple
    TokenType.STRING: "\033[38;5;186m",       # Yellow-green
    TokenType.NUMBER: "\033[38;5;208m",       # Orange
    TokenType.COMMENT: "\033[38;5;72m",        # Cyan-green
    TokenType.OPERATOR: "\033[38;5;203m",     # Red-pink
    TokenType.FUNCTION: "\033[38;5;79m",      # Cyan
    TokenType.CLASS: "\033[38;5;216m",         # Light orange
    TokenType.DECORATOR: "\033[38;5;183m",    # Light purple
    TokenType.VARIABLE: "\033[38;5;252m",     # Light gray
    TokenType.BUILTIN: "\033[38;5;117m",       # Light cyan
    TokenType.CONSTANT: "\033[38;5;173m",      # Light salmon
    TokenType.PUNCTUATION: "\033[38;5;248m",  # Gray
    TokenType.BRACKET: "\033[38;5;248m",      # Gray
    TokenType.WHITESPACE: "",
    TokenType.NEWLINE: "",
    TokenType.UNKNOWN: "\033[0m",
}

HTML_THEME = {
    TokenType.KEYWORD: "color: #c678dd;",
    TokenType.STRING: "color: #98c379;",
    TokenType.NUMBER: "color: #d19a66;",
    TokenType.COMMENT: "color: #5c6370; font-style: italic;",
    TokenType.OPERATOR: "color: #56b6c2;",
    TokenType.FUNCTION: "color: #61afef;",
    TokenType.CLASS: "color: #e5c07b;",
    TokenType.DECORATOR: "color: #abb2bf;",
    TokenType.VARIABLE: "color: #abb2bf;",
    TokenType.BUILTIN: "color: #61afef;",
    TokenType.CONSTANT: "color: #e06c75;",
    TokenType.PUNCTUATION: "color: #abb2bf;",
    TokenType.BRACKET: "color: #abb2bf;",
    TokenType.WHITESPACE: "",
    TokenType.NEWLINE: "",
    TokenType.UNKNOWN: "",
}

ANSI_RESET = "\033[0m"

# Python keywords and builtins
PYTHON_KEYWORDS = {
    "False", "None", "True", "and", "as", "assert", "async", "await",
    "break", "class", "continue", "def", "del", "elif", "else", "except",
    "finally", "for", "from", "global", "if", "import", "in", "is",
    "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try",
    "while", "with", "yield", "match", "case"
}

PYTHON_BUILTINS = {
    "abs", "aiter", "all", "any", "anext", "ascii", "bin", "bool",
    "breakpoint", "bytearray", "bytes", "callable", "chr", "classmethod",
    "compile", "complex", "delattr", "dict", "dir", "divmod", "enumerate",
    "eval", "exec", "filter", "float", "format", "frozenset", "getattr",
    "globals", "hasattr", "hash", "help", "hex", "id", "input", "int",
    "isinstance", "issubclass", "iter", "len", "list", "locals", "map",
    "max", "memoryview", "min", "next", "object", "oct", "open", "ord",
    "pow", "print", "property", "range", "repr", "reversed", "round",
    "set", "setattr", "slice", "sorted", "staticmethod", "str", "sum",
    "super", "tuple", "type", "vars", "zip", "__import__", "__name__",
    "__doc__", "__package__", "__loader__", "__spec__", "__path__",
    "__file__", "__cached__", "__builtins__", "self", "cls"
}

# JavaScript keywords
JS_KEYWORDS = {
    "async", "await", "break", "case", "catch", "class", "const",
    "continue", "debugger", "default", "delete", "do", "else", "export",
    "extends", "finally", "for", "function", "if", "import", "in",
    "instanceof", "let", "new", "of", "return", "static", "super",
    "switch", "this", "throw", "try", "typeof", "undefined", "var",
    "void", "while", "with", "yield", "true", "false", "null"
}

JS_BUILTINS = {
    "Array", "Boolean", "Date", "Error", "Function", "JSON", "Map",
    "Math", "Number", "Object", "Promise", "RegExp", "Set", "String",
    "Symbol", "console", "document", "window", "fetch", "setTimeout",
    "setInterval", "clearTimeout", "clearInterval", "parseInt", "parseFloat",
    "isNaN", "isFinite", "encodeURI", "decodeURI", "encodeURIComponent",
    "decodeURIComponent"
}


class Lexer:
    """Tokenizer for source code."""
    
    def __init__(self, code: str, lang: str = "python"):
        self.code = code
        self.pos = 0
        self.lang = lang.lower()
        self.keywords = PYTHON_KEYWORDS if lang == "python" else JS_KEYWORDS
        self.builtins = PYTHON_BUILTINS if lang == "python" else JS_BUILTINS
    
    def peek(self, offset: int = 0) -> str:
        """Look at character at current position + offset."""
        pos = self.pos + offset
        if pos < len(self.code):
            return self.code[pos]
        return ""
    
    def advance(self, count: int = 1) -> str:
        """Advance position and return consumed characters."""
        result = self.code[self.pos:self.pos + count]
        self.pos += count
        return result
    
    def at_end(self) -> bool:
        """Check if at end of code."""
        return self.pos >= len(self.code)
    
    def tokenize(self) -> List[Token]:
        """Tokenize the entire code."""
        tokens = []
        
        while not self.at_end():
            token = self._next_token()
            if token:
                tokens.append(token)
        
        return tokens
    
    def _next_token(self) -> Optional[Token]:
        """Get the next token."""
        start = self.pos
        char = self.peek()
        
        # Whitespace
        if char in " \t":
            return self._read_whitespace()
        
        # Newline
        if char == "\n":
            self.advance()
            return Token(TokenType.NEWLINE, "\n", start, self.pos)
        
        # Carriage return (handle \r\n)
        if char == "\r":
            self.advance()
            if self.peek() == "\n":
                self.advance()
            return Token(TokenType.NEWLINE, "\r\n", start, self.pos)
        
        # Comments
        if char == "#":
            return self._read_comment()
        
        # Multi-line comments (/* */)
        if char == "/" and self.peek(1) == "*":
            return self._read_block_comment()
        
        # Single-line comments (//)
        if char == "/" and self.peek(1) == "/":
            return self._read_line_comment()
        
        # Strings
        if char in '"\'':
            return self._read_string(char)
        
        # F-strings (Python)
        if char == "f" and self.peek(1) in '"\'':
            self.advance()  # consume 'f'
            return self._read_fstring()
        
        # Triple-quoted strings
        if char * 3 in ('"""', "'''"):
            if self.code[self.pos:self.pos + 3] in ('"""', "'''"):
                return self._read_triple_string()
        
        # Numbers
        if char.isdigit():
            return self._read_number()
        
        # Identifiers and keywords
        if char.isalpha() or char == "_":
            return self._read_identifier()
        
        # Decorators
        if char == "@":
            return self._read_decorator()
        
        # Operators
        if char in "+-*/%=<>!&|^~":
            return self._read_operator()
        
        # Brackets
        if char in "()[]{}":
            self.advance()
            return Token(TokenType.BRACKET, char, start, self.pos)
        
        # Punctuation
        if char in ":;,.":
            self.advance()
            return Token(TokenType.PUNCTUATION, char, start, self.pos)
        
        # Unknown
        self.advance()
        return Token(TokenType.UNKNOWN, char, start, self.pos)
    
    def _read_whitespace(self) -> Token:
        """Read whitespace token."""
        start = self.pos
        while self.peek() in " \t":
            self.advance()
        return Token(TokenType.WHITESPACE, self.code[start:self.pos], start, self.pos)
    
    def _read_comment(self) -> Token:
        """Read a Python-style comment."""
        start = self.pos
        while self.peek() and self.peek() != "\n":
            self.advance()
        return Token(TokenType.COMMENT, self.code[start:self.pos], start, self.pos)
    
    def _read_block_comment(self) -> Token:
        """Read a C-style block comment."""
        start = self.pos
        self.advance(2)  # Skip /*
        while not self.at_end():
            if self.peek() == "*" and self.peek(1) == "/":
                self.advance(2)
                break
            self.advance()
        return Token(TokenType.COMMENT, self.code[start:self.pos], start, self.pos)
    
    def _read_line_comment(self) -> Token:
        """Read a C++-style line comment."""
        start = self.pos
        while self.peek() and self.peek() != "\n":
            self.advance()
        return Token(TokenType.COMMENT, self.code[start:self.pos], start, self.pos)
    
    def _read_string(self, quote: str) -> Token:
        """Read a string literal."""
        start = self.pos
        self.advance()  # Skip opening quote
        
        while not self.at_end():
            char = self.peek()
            if char == "\\":
                self.advance(2)  # Skip escape sequence
            elif char == quote:
                self.advance()  # Skip closing quote
                break
            elif char == "\n":
                break
            else:
                self.advance()
        
        return Token(TokenType.STRING, self.code[start:self.pos], start, self.pos)
    
    def _read_triple_string(self) -> Token:
        """Read a triple-quoted string."""
        start = self.pos
        quote = self.advance(3)  # Skip opening quotes
        
        while not self.at_end():
            if self.code[self.pos:self.pos + 3] == quote:
                self.advance(3)  # Skip closing quotes
                break
            self.advance()
        
        return Token(TokenType.STRING, self.code[start:self.pos], start, self.pos)
    
    def _read_fstring(self) -> Token:
        """Read an f-string."""
        start = self.pos - 1  # Include 'f'
        quote = self.advance()  # Get opening quote
        
        # Handle triple-quoted f-strings
        if self.code[self.pos:self.pos + 2] == quote * 2:
            self.advance(2)  # Skip additional quotes
            quote = quote * 3
            
            while not self.at_end():
                if self.code[self.pos:self.pos + 3] == quote:
                    self.advance(3)
                    break
                self.advance()
        else:
            while not self.at_end():
                char = self.peek()
                if char == "\\":
                    self.advance(2)
                elif char == quote:
                    self.advance()
                    break
                else:
                    self.advance()
        
        return Token(TokenType.STRING, self.code[start:self.pos], start, self.pos)
    
    def _read_number(self) -> Token:
        """Read a number literal."""
        start = self.pos
        
        # Handle hex
        if self.peek() == "0" and self.peek(1) in "xX":
            self.advance(2)
            while self.peek() in "0123456789abcdefABCDEF":
                self.advance()
            return Token(TokenType.NUMBER, self.code[start:self.pos], start, self.pos)
        
        # Handle binary
        if self.peek() == "0" and self.peek(1) in "bB":
            self.advance(2)
            while self.peek() in "01":
                self.advance()
            return Token(TokenType.NUMBER, self.code[start:self.pos], start, self.pos)
        
        # Handle octal
        if self.peek() == "0" and self.peek(1) in "oO":
            self.advance(2)
            while self.peek() in "01234567":
                self.advance()
            return Token(TokenType.NUMBER, self.code[start:self.pos], start, self.pos)
        
        # Decimal number
        while self.peek().isdigit():
            self.advance()
        
        # Decimal part
        if self.peek() == "." and self.peek(1).isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()
        
        # Exponent
        if self.peek() in "eE":
            self.advance()
            if self.peek() in "+-":
                self.advance()
            while self.peek().isdigit():
                self.advance()
        
        # Type suffix
        if self.peek() in "jJ":
            self.advance()
        
        return Token(TokenType.NUMBER, self.code[start:self.pos], start, self.pos)
    
    def _read_identifier(self) -> Token:
        """Read an identifier or keyword."""
        start = self.pos
        
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()
        
        value = self.code[start:self.pos]
        token_type = TokenType.VARIABLE
        
        # Check if keyword
        if value in self.keywords:
            if value in ("True", "False", "None", "true", "false", "null", "undefined"):
                token_type = TokenType.CONSTANT
            else:
                token_type = TokenType.KEYWORD
        # Check if builtin
        elif value in self.builtins:
            token_type = TokenType.BUILTIN
        # Check if class (Capitalized)
        elif value[0].isupper() and not value.isupper():
            token_type = TokenType.CLASS
        # Check for ALL_CAPS constants
        elif value.isupper() and len(value) > 1:
            token_type = TokenType.CONSTANT
        
        # Check if followed by '(' (function call)
        # We'll handle this in post-processing
        
        return Token(token_type, value, start, self.pos)
    
    def _read_decorator(self) -> Token:
        """Read a Python decorator."""
        start = self.pos
        self.advance()  # Skip @
        
        # Read decorator name
        while self.peek().isalnum() or self.peek() in "_.":
            self.advance()
        
        return Token(TokenType.DECORATOR, self.code[start:self.pos], start, self.pos)
    
    def _read_operator(self) -> Token:
        """Read an operator."""
        start = self.pos
        
        # Multi-character operators
        multi_ops = ["===", "!==", "==", "!=", "<=", ">=", "->", "=>",
                     "+=", "-=", "*=", "/=", "%=", "**=", "//=",
                     "++", "--", "&&", "||", "<<", ">>", "**", "//"]
        
        for op in multi_ops:
            if self.code[self.pos:self.pos + len(op)] == op:
                self.advance(len(op))
                return Token(TokenType.OPERATOR, op, start, self.pos)
        
        # Single-character operator
        self.advance()
        return Token(TokenType.OPERATOR, self.code[start:self.pos], start, self.pos)


class Highlighter:
    """Syntax highlighter for code."""
    
    def __init__(self, theme: Dict[TokenType, str] = None, ansi: bool = True):
        self.theme = theme or (ANSI_THEME if ansi else HTML_THEME)
        self.ansi = ansi
        self.reset = ANSI_RESET if ansi else ""
    
    def highlight(self, tokens: List[Token], line_numbers: bool = False) -> str:
        """Apply highlighting to tokens."""
        result = []
        
        if line_numbers:
            line_num = 1
            line_num_str = f"{line_num:4d} | "
            result.append(line_num_str)
        
        for i, token in enumerate(tokens):
            # Handle line numbers
            if token.type == TokenType.NEWLINE:
                result.append(token.value)
                if line_numbers and i < len(tokens) - 1:
                    line_num += 1
                    line_num_str = f"\n{line_num:4d} | "
                    continue
            else:
                color = self.theme.get(token.type, "")
                if color:
                    result.append(f"{color}{token.value}{self.reset}")
                else:
                    result.append(token.value)
        
        return "".join(result)
    
    def highlight_html(self, tokens: List[Token], line_numbers: bool = False,
                       pre_style: str = None) -> str:
        """Generate HTML with syntax highlighting."""
        result = ["<pre style='"]
        result.append(pre_style or "background: #282c34; color: #abb2bf; padding: 16px; border-radius: 8px; overflow-x: auto; font-family: 'Fira Code', 'Consolas', monospace; font-size: 14px; line-height: 1.5;'>")
        
        if line_numbers:
            result.append("<code style='display: flex;'>")
            # Line numbers column
            line_count = sum(1 for t in tokens if t.type == TokenType.NEWLINE) + 1
            result.append("<span style='display: inline-block; text-align: right; padding-right: 16px; color: #5c6370; border-right: 1px solid #3e4451; margin-right: 16px; user-select: none;'>")
            for i in range(1, line_count + 1):
                result.append(f"{i}\n")
            result.append("</span>")
            result.append("<span>")
        else:
            result.append("<code>")
        
        for token in tokens:
            if token.type == TokenType.NEWLINE:
                result.append("<br/>")
            elif token.type == TokenType.WHITESPACE:
                result.append(token.value)
            else:
                style = self.theme.get(token.type, "")
                if style:
                    escaped_value = self._escape_html(token.value)
                    result.append(f"<span style='{style}'>{escaped_value}</span>")
                else:
                    result.append(self._escape_html(token.value))
        
        result.append("</code>")
        if line_numbers:
            result.append("</span>")
        result.append("</pre>")
        
        return "".join(result)
    
    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        return (text
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&#39;"))


def highlight(code: str, lang: str = "python", line_numbers: bool = False) -> str:
    """
    Highlight code with ANSI colors for terminal display.
    
    Args:
        code: Source code to highlight
        lang: Programming language (python, javascript, json, etc.)
        line_numbers: Whether to show line numbers
    
    Returns:
        ANSI-colored code string
    
    Example:
        >>> code = 'def hello(): print("World")'
        >>> print(highlight(code))
    """
    lexer = Lexer(code, lang)
    tokens = lexer.tokenize()
    highlighter = Highlighter(ansi=True)
    return highlighter.highlight(tokens, line_numbers)


def highlight_html(code: str, lang: str = "python", line_numbers: bool = False,
                   pre_style: str = None) -> str:
    """
    Highlight code with HTML spans for web display.
    
    Args:
        code: Source code to highlight
        lang: Programming language
        line_numbers: Whether to show line numbers
        pre_style: Custom CSS style for the <pre> element
    
    Returns:
        HTML string with syntax highlighting
    
    Example:
        >>> code = 'def hello(): print("World")'
        >>> html = highlight_html(code)
    """
    lexer = Lexer(code, lang)
    tokens = lexer.tokenize()
    highlighter = Highlighter(ansi=False)
    return highlighter.highlight_html(tokens, line_numbers, pre_style)


def get_tokens(code: str, lang: str = "python") -> List[Token]:
    """
    Get list of tokens for code analysis.
    
    Args:
        code: Source code to tokenize
        lang: Programming language
    
    Returns:
        List of Token objects
    """
    lexer = Lexer(code, lang)
    return lexer.tokenize()


def strip_ansi(text: str) -> str:
    """
    Remove ANSI escape sequences from text.
    
    Args:
        text: Text containing ANSI codes
    
    Returns:
        Plain text without ANSI codes
    """
    ansi_pattern = re.compile(r'\033\[[0-9;]*m')
    return ansi_pattern.sub('', text)


# Convenience function for quick testing
def demo():
    """Run a demo showing syntax highlighting capabilities."""
    code = '''
# Example Python code
import os
from typing import List, Dict

CONSTANT_VALUE = 42

@decorator
def calculate_sum(numbers: List[int]) -> int:
    """Calculate the sum of numbers."""
    total = 0
    for num in numbers:
        total += num
    return total

class Calculator:
    """A simple calculator class."""
    
    def __init__(self, value: int = 0):
        self.value = value
    
    def add(self, x: int) -> None:
        self.value += x

# String examples
message = "Hello, World!"
fstring = f"Value: {CONSTANT_VALUE}"
multiline = """
This is a
multiline string
"""

# Numbers
hex_num = 0xFF
binary = 0b1010
float_num = 3.14159
complex_num = 2 + 3j
'''
    
    print("=" * 60)
    print("Syntax Highlight Demo (ANSI Terminal Output)")
    print("=" * 60)
    print(highlight(code, lang="python", line_numbers=True))
    
    print("\n" + "=" * 60)
    print("HTML Output Sample:")
    print("=" * 60)
    html = highlight_html(code[:100], lang="python")
    print(html[:300] + "...")


if __name__ == "__main__":
    demo()