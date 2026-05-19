"""
lexer_utils - A lightweight lexical analyzer/tokenizer library.

Provides flexible tokenization of text with support for:
- Custom token types and patterns
- String literals with escape sequences
- Numbers (integers, floats, hex, binary, scientific notation)
- Identifiers and keywords
- Operators and punctuation
- Comments (single-line and multi-line)
- Whitespace handling (preserve or skip)
- Position tracking (line, column)

Zero external dependencies - pure Python implementation.
"""

import re
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, Iterator, List, Optional, Pattern, Union, Tuple, Set


class TokenType(Enum):
    """Standard token types."""
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    
    # Identifiers and keywords
    IDENTIFIER = auto()
    KEYWORD = auto()
    
    # Operators
    OPERATOR = auto()
    
    # Punctuation
    PUNCTUATION = auto()
    
    # Structure
    LPAREN = auto()      # (
    RPAREN = auto()      # )
    LBRACKET = auto()    # [
    RBRACKET = auto()    # ]
    LBRACE = auto()      # {
    RBRACE = auto()      # }
    
    # Special
    COMMA = auto()       # ,
    DOT = auto()         # .
    COLON = auto()       # :
    SEMICOLON = auto()   # ;
    ASSIGN = auto()      # =
    
    # Whitespace and comments
    WHITESPACE = auto()
    NEWLINE = auto()
    COMMENT = auto()
    
    # End of input
    EOF = auto()
    
    # Error
    ERROR = auto()
    UNKNOWN = auto()


@dataclass
class Token:
    """Represents a single token with position information."""
    type: TokenType
    value: str
    line: int
    column: int
    start_pos: int = 0
    end_pos: int = 0
    
    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, L{self.line}:C{self.column})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Token):
            return False
        return self.type == other.type and self.value == other.value


@dataclass
class LexerConfig:
    """Configuration for lexer behavior."""
    # Keywords (set of strings)
    keywords: set = field(default_factory=set)
    
    # Operators (multi-char operators first for proper matching)
    operators: list = field(default_factory=lambda: [
        '**=', '//=', '<<=', '>>=', '==', '!=', '<=', '>=', '+=', '-=', '*=',
        '/=', '%=', '&=', '|=', '^=', '<<', '>>', '//', '**', '->', '<-',
        '+', '-', '*', '/', '%', '&', '|', '^', '~', '<', '>', '!', '='
    ])
    
    # Punctuation characters
    punctuation: str = "@#$\\?"
    
    # String delimiters
    string_delimiters: list = field(default_factory=lambda: ['"', "'", '`'])
    
    # Escape character
    escape_char: str = '\\'
    
    # Comment styles
    single_line_comment: list = field(default_factory=lambda: ['#', '//'])
    multi_line_start: str = '/*'
    multi_line_end: str = '*/'
    
    # Number formats
    allow_hex: bool = True        # 0xFF
    allow_binary: bool = True     # 0b101
    allow_octal: bool = True      # 0o77
    allow_scientific: bool = True # 1e10, 1.5e-3
    
    # Behavior
    skip_whitespace: bool = True
    skip_comments: bool = True
    preserve_newlines: bool = False
    
    # Identifier pattern
    identifier_start: str = '_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    identifier_chars: str = '_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


class LexerError(Exception):
    """Exception raised for lexer errors."""
    def __init__(self, message: str, line: int, column: int, position: int):
        super().__init__(f"{message} at line {line}, column {column}")
        self.line = line
        self.column = column
        self.position = position


class Lexer:
    """
    A flexible lexical analyzer.
    
    Example:
        >>> config = LexerConfig(keywords={'if', 'else', 'for', 'while'})
        >>> lexer = Lexer("x = 42 + 10", config)
        >>> for token in lexer.tokenize():
        ...     print(token)
    """
    
    def __init__(self, text: str, config: Optional[LexerConfig] = None):
        """
        Initialize the lexer.
        
        Args:
            text: Input text to tokenize
            config: Lexer configuration (uses defaults if not provided)
        """
        self.text = text
        self.config = config or LexerConfig()
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
    @property
    def current_char(self) -> str:
        """Get the current character or empty string if at end."""
        return self.text[self.pos] if self.pos < len(self.text) else ''
    
    @property
    def peek_char(self) -> str:
        """Look at the next character without advancing."""
        return self.text[self.pos + 1] if self.pos + 1 < len(self.text) else ''
    
    @property
    def peek_two(self) -> str:
        """Look at the next two characters."""
        return self.text[self.pos:self.pos + 2] if self.pos + 1 < len(self.text) else ''
    
    @property
    def is_at_end(self) -> bool:
        """Check if at end of input."""
        return self.pos >= len(self.text)
    
    def advance(self) -> str:
        """Advance position and return the consumed character."""
        char = self.current_char
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def retreat(self) -> None:
        """Move back one position (use carefully)."""
        self.pos -= 1
        if self.pos > 0 and self.text[self.pos - 1] == '\n':
            self.line -= 1
            # Note: column restoration is approximate
            self.column = 1
    
    def match(self, expected: str) -> bool:
        """Consume character if it matches expected, return True if matched."""
        if self.current_char == expected:
            self.advance()
            return True
        return False
    
    def skip_whitespace(self) -> None:
        """Skip whitespace characters (not newlines)."""
        while self.current_char in ' \t\r':
            self.advance()
    
    def read_string(self, delimiter: str) -> str:
        """Read a string literal, handling escape sequences."""
        result = []
        self.advance()  # consume opening delimiter
        
        while not self.is_at_end:
            char = self.current_char
            
            if char == delimiter:
                self.advance()  # consume closing delimiter
                return ''.join(result)
            
            if char == self.config.escape_char:
                self.advance()  # consume escape char
                escaped = self.current_char
                if escaped:
                    escape_map = {
                        'n': '\n', 't': '\t', 'r': '\r',
                        '\\': '\\', "'": "'", '"': '"',
                        '0': '\0', 'a': '\a', 'b': '\b',
                        'f': '\f', 'v': '\v'
                    }
                    result.append(escape_map.get(escaped, escaped))
                    self.advance()
            else:
                result.append(char)
                self.advance()
        
        raise LexerError("Unterminated string", self.line, self.column, self.pos)
    
    def read_number(self) -> Token:
        """Read a number literal (integer, float, hex, binary, octal)."""
        start_line = self.line
        start_col = self.column
        start_pos = self.pos
        result = []
        
        # Check for hex/binary/octal prefix
        if self.current_char == '0' and self.peek_char:
            prefix = self.peek_char.lower()
            
            if prefix == 'x' and self.config.allow_hex:
                result.append(self.advance())  # 0
                result.append(self.advance())  # x
                while self.current_char in '0123456789abcdefABCDEF':
                    result.append(self.advance())
                return Token(TokenType.INTEGER, ''.join(result), 
                           start_line, start_col, start_pos, self.pos)
            
            elif prefix == 'b' and self.config.allow_binary:
                result.append(self.advance())  # 0
                result.append(self.advance())  # b
                while self.current_char in '01':
                    result.append(self.advance())
                return Token(TokenType.INTEGER, ''.join(result),
                           start_line, start_col, start_pos, self.pos)
            
            elif prefix == 'o' and self.config.allow_octal:
                result.append(self.advance())  # 0
                result.append(self.advance())  # o
                while self.current_char in '01234567':
                    result.append(self.advance())
                return Token(TokenType.INTEGER, ''.join(result),
                           start_line, start_col, start_pos, self.pos)
        
        # Regular integer or float
        while self.current_char.isdigit():
            result.append(self.advance())
        
        is_float = False
        
        # Check for decimal point
        if self.current_char == '.' and self.peek_char.isdigit():
            is_float = True
            result.append(self.advance())  # consume '.'
            while self.current_char.isdigit():
                result.append(self.advance())
        
        # Check for scientific notation
        if self.config.allow_scientific and self.current_char and self.current_char in 'eE':
            is_float = True
            result.append(self.advance())  # consume 'e'
            if self.current_char in '+-':
                result.append(self.advance())
            while self.current_char.isdigit():
                result.append(self.advance())
        
        token_type = TokenType.FLOAT if is_float else TokenType.INTEGER
        return Token(token_type, ''.join(result), start_line, start_col, start_pos, self.pos)
    
    def read_identifier(self) -> Token:
        """Read an identifier or keyword."""
        start_line = self.line
        start_col = self.column
        start_pos = self.pos
        result = []
        
        while self.current_char in self.config.identifier_chars:
            result.append(self.advance())
        
        value = ''.join(result)
        token_type = TokenType.KEYWORD if value in self.config.keywords else TokenType.IDENTIFIER
        
        return Token(token_type, value, start_line, start_col, start_pos, self.pos)
    
    def read_line_comment(self) -> str:
        """Read a single-line comment."""
        result = []
        while not self.is_at_end and self.current_char != '\n':
            result.append(self.advance())
        return ''.join(result)
    
    def read_block_comment(self) -> str:
        """Read a multi-line comment."""
        result = []
        # Skip opening delimiter
        self.pos += len(self.config.multi_line_start)
        self.column += len(self.config.multi_line_start)
        
        while not self.is_at_end:
            if self.text[self.pos:self.pos + len(self.config.multi_line_end)] == self.config.multi_line_end:
                self.pos += len(self.config.multi_line_end)
                self.column += len(self.config.multi_line_end)
                break
            result.append(self.advance())
        
        return ''.join(result)
    
    def get_next_token(self) -> Token:
        """Get the next token from input."""
        if self.is_at_end:
            return Token(TokenType.EOF, '', self.line, self.column, self.pos, self.pos)
        
        start_line = self.line
        start_col = self.column
        start_pos = self.pos
        char = self.current_char
        
        # Whitespace (skip if configured)
        if char in ' \t\r':
            if self.config.skip_whitespace:
                self.skip_whitespace()
                return self.get_next_token()
            result = []
            while self.current_char in ' \t\r':
                result.append(self.advance())
            return Token(TokenType.WHITESPACE, ''.join(result),
                        start_line, start_col, start_pos, self.pos)
        
        # Newline
        if char == '\n':
            self.advance()
            if self.config.preserve_newlines:
                return Token(TokenType.NEWLINE, '\n', start_line, start_col, start_pos, self.pos)
            return self.get_next_token()
        
        # Single-line comment
        for comment_start in self.config.single_line_comment:
            if self.text[self.pos:self.pos + len(comment_start)] == comment_start:
                comment = self.read_line_comment()
                if self.config.skip_comments:
                    return self.get_next_token()
                return Token(TokenType.COMMENT, comment, start_line, start_col, start_pos, self.pos)
        
        # Multi-line comment
        if (self.config.multi_line_start and 
            self.text[self.pos:self.pos + len(self.config.multi_line_start)] == self.config.multi_line_start):
            comment = self.read_block_comment()
            if self.config.skip_comments:
                return self.get_next_token()
            return Token(TokenType.COMMENT, comment, start_line, start_col, start_pos, self.pos)
        
        # String literals
        if char in self.config.string_delimiters:
            try:
                value = self.read_string(char)
                return Token(TokenType.STRING, value, start_line, start_col, start_pos, self.pos)
            except LexerError:
                return Token(TokenType.ERROR, self.text[start_pos:self.pos],
                           start_line, start_col, start_pos, self.pos)
        
        # Numbers
        if char.isdigit() or (char == '.' and self.peek_char.isdigit()):
            return self.read_number()
        
        # Identifiers
        if char in self.config.identifier_start:
            return self.read_identifier()
        
        # Structure tokens
        structure_map = {
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '[': TokenType.LBRACKET,
            ']': TokenType.RBRACKET,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            ',': TokenType.COMMA,
            '.': TokenType.DOT,
            ':': TokenType.COLON,
            ';': TokenType.SEMICOLON,
        }
        
        if char in structure_map:
            self.advance()
            return Token(structure_map[char], char, start_line, start_col, start_pos, self.pos)
        
        # Operators (check longer ones first)
        for op in self.config.operators:
            if self.text[self.pos:self.pos + len(op)] == op:
                self.pos += len(op)
                self.column += len(op)
                return Token(TokenType.OPERATOR, op, start_line, start_col, start_pos, self.pos)
        
        # Punctuation
        if char in self.config.punctuation:
            self.advance()
            return Token(TokenType.PUNCTUATION, char, start_line, start_col, start_pos, self.pos)
        
        # Unknown character
        self.advance()
        return Token(TokenType.UNKNOWN, char, start_line, start_col, start_pos, self.pos)
    
    def tokenize(self) -> Iterator[Token]:
        """
        Tokenize the entire input.
        
        Yields:
            Token objects until EOF
        """
        while True:
            token = self.get_next_token()
            yield token
            if token.type == TokenType.EOF:
                break
    
    def tokenize_all(self) -> List[Token]:
        """
        Tokenize the entire input and return all tokens.
        
        Returns:
            List of all tokens including EOF
        """
        return list(self.tokenize())
    
    def reset(self) -> None:
        """Reset the lexer to the beginning of input."""
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []


# Convenience functions

def tokenize(text: str, config: Optional[LexerConfig] = None) -> List[Token]:
    """
    Quick tokenization of text.
    
    Args:
        text: Input text to tokenize
        config: Optional lexer configuration
        
    Returns:
        List of tokens
    """
    lexer = Lexer(text, config)
    return lexer.tokenize_all()


def tokenize_keywords(text: str, keywords: set) -> List[Token]:
    """
    Tokenize text with custom keywords.
    
    Args:
        text: Input text
        keywords: Set of keyword strings
        
    Returns:
        List of tokens
    """
    config = LexerConfig(keywords=keywords)
    return tokenize(text, config)


def extract_tokens_by_type(tokens: List[Token], token_type: TokenType) -> List[Token]:
    """Extract all tokens of a specific type."""
    return [t for t in tokens if t.type == token_type]


def extract_values_by_type(tokens: List[Token], token_type: TokenType) -> List[str]:
    """Extract all token values of a specific type."""
    return [t.value for t in tokens if t.type == token_type]


def extract_identifiers(tokens: List[Token]) -> List[str]:
    """Extract all identifier values from tokens."""
    return extract_values_by_type(tokens, TokenType.IDENTIFIER)


def extract_strings(tokens: List[Token]) -> List[str]:
    """Extract all string literal values from tokens."""
    return extract_values_by_type(tokens, TokenType.STRING)


def extract_numbers(tokens: List[Token]) -> List[str]:
    """Extract all number values from tokens."""
    result = []
    for t in tokens:
        if t.type in (TokenType.INTEGER, TokenType.FLOAT):
            result.append(t.value)
    return result


def find_token(tokens: List[Token], value: str) -> Optional[Token]:
    """Find first token with matching value."""
    for token in tokens:
        if token.value == value:
            return token
    return None


def find_all_tokens(tokens: List[Token], value: str) -> List[Token]:
    """Find all tokens with matching value."""
    return [t for t in tokens if t.value == value]


def get_token_positions(tokens: List[Token]) -> List[Tuple[int, int, str]]:
    """Get (line, column, value) for all tokens."""
    return [(t.line, t.column, t.value) for t in tokens]


class SimpleLexer:
    """
    A simpler lexer for basic use cases.
    
    Example:
        >>> lexer = SimpleLexer("hello world 123")
        >>> for token in lexer:
        ...     print(token)
    """
    
    def __init__(self, text: str, delimiters: Optional[str] = None):
        """
        Initialize simple lexer.
        
        Args:
            text: Input text
            delimiters: Characters to split on (default: whitespace)
        """
        self.text = text
        self.delimiters = delimiters or ' \t\n\r'
        self.pos = 0
    
    def __iter__(self) -> Iterator[Tuple[str, int, int]]:
        """Iterate over (token, start, end) tuples."""
        while self.pos < len(self.text):
            # Skip delimiters
            while self.pos < len(self.text) and self.text[self.pos] in self.delimiters:
                self.pos += 1
            
            if self.pos >= len(self.text):
                break
            
            start = self.pos
            
            # Read token
            while self.pos < len(self.text) and self.text[self.pos] not in self.delimiters:
                self.pos += 1
            
            end = self.pos
            yield (self.text[start:end], start, end)
    
    def tokenize(self) -> List[str]:
        """Get all tokens as strings."""
        return [token for token, _, _ in self]


class StreamingLexer:
    """
    Lexer for streaming input (process text chunk by chunk).
    
    Example:
        >>> lexer = StreamingLexer()
        >>> lexer.feed("x = ")
        >>> lexer.feed("42")
        >>> tokens = lexer.flush()
    """
    
    def __init__(self, config: Optional[LexerConfig] = None):
        self.config = config or LexerConfig()
        self.buffer = ""
        self.lexer: Optional[Lexer] = None
    
    def feed(self, chunk: str) -> List[Token]:
        """
        Feed a chunk of text and get any complete tokens.
        
        Args:
            chunk: Text chunk to process
            
        Returns:
            List of complete tokens (may be empty)
        """
        self.buffer += chunk
        self.lexer = Lexer(self.buffer, self.config)
        tokens = []
        
        for token in self.lexer.tokenize():
            if token.type == TokenType.EOF:
                # Rewind buffer to current position for partial tokens
                self.buffer = self.buffer[token.start_pos:]
                break
            tokens.append(token)
        
        return tokens
    
    def flush(self) -> List[Token]:
        """
        Flush remaining buffer and get all tokens.
        
        Returns:
            List of remaining tokens including EOF
        """
        lexer = Lexer(self.buffer, self.config)
        tokens = list(lexer.tokenize())
        self.buffer = ""
        return tokens


if __name__ == "__main__":
    # Demo
    demo_code = '''
    def calculate(x, y):
        """Calculate something."""
        result = x + y * 2
        return result  # Return the result
    
    # Hex and binary
    hex_val = 0xFF
    bin_val = 0b1010
    float_val = 3.14e-10
    '''
    
    config = LexerConfig(
        keywords={'def', 'return', 'if', 'else', 'for', 'while', 'class', 'import', 'from', 'as'},
        preserve_newlines=False,
        skip_comments=True,
        skip_whitespace=True
    )
    
    lexer = Lexer(demo_code, config)
    print("Tokenizing Python-like code:\n")
    for token in lexer.tokenize():
        if token.type not in (TokenType.EOF,):
            print(f"  {token}")