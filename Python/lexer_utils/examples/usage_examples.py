"""
Usage Examples for lexer_utils

This module demonstrates various use cases for the lexer_utils library,
a lightweight lexical analyzer/tokenizer with zero external dependencies.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Lexer, LexerConfig, Token, TokenType,
    tokenize, tokenize_keywords,
    extract_identifiers, extract_strings, extract_numbers,
    find_token, find_all_tokens,
    SimpleLexer, StreamingLexer
)


def example_basic_tokenization():
    """Basic tokenization example."""
    print("=" * 60)
    print("Example 1: Basic Tokenization")
    print("=" * 60)
    
    code = "x = 42 + 10"
    lexer = Lexer(code)
    
    print(f"\nInput: {code!r}\n")
    print("Tokens:")
    for token in lexer.tokenize():
        if token.type != TokenType.EOF:
            print(f"  {token}")
    print()


def example_custom_keywords():
    """Custom keywords example."""
    print("=" * 60)
    print("Example 2: Custom Keywords")
    print("=" * 60)
    
    sql_keywords = {
        "SELECT", "FROM", "WHERE", "AND", "OR", "INSERT", "UPDATE",
        "DELETE", "CREATE", "TABLE", "DROP", "ALTER", "JOIN", "ON",
        "ORDER", "BY", "GROUP", "HAVING", "LIMIT", "OFFSET"
    }
    
    config = LexerConfig(keywords=sql_keywords)
    sql = "SELECT name, age FROM users WHERE age > 18 AND active = 1"
    
    lexer = Lexer(sql.upper(), config)
    
    print(f"\nInput: {sql}\n")
    print("Tokens:")
    for token in lexer.tokenize():
        if token.type != TokenType.EOF:
            print(f"  {token}")
    print()


def example_numbers():
    """Number formats example."""
    print("=" * 60)
    print("Example 3: Number Formats")
    print("=" * 60)
    
    numbers = "42 3.14 0xFF 0b1010 0o77 1.5e-10"
    
    print(f"\nInput: {numbers}\n")
    
    tokens = tokenize(numbers)
    
    print("Integer tokens:")
    for t in tokens:
        if t.type == TokenType.INTEGER:
            print(f"  {t.value}")
    
    print("\nFloat tokens:")
    for t in tokens:
        if t.type == TokenType.FLOAT:
            print(f"  {t.value}")
    print()


def example_strings():
    """String handling example."""
    print("=" * 60)
    print("Example 4: String Handling")
    print("=" * 60)
    
    code = r'''
name = "Alice"
message = 'Hello, World!'
template = `Template literal`
escaped = "Line1\nLine2\tTabbed"
'''
    
    print(f"\nInput code:\n{code}")
    
    tokens = tokenize(code)
    strings = extract_strings(tokens)
    
    print("Extracted strings:")
    for s in strings:
        print(f"  {s!r}")
    print()


def example_comments():
    """Comment handling example."""
    print("=" * 60)
    print("Example 5: Comment Handling")
    print("=" * 60)
    
    code = '''
# This is a comment
x = 1  # Inline comment
/* Multi-line
   comment */
y = 2
'''
    
    # Skip comments (default)
    print("\nWith skip_comments=True (default):\n")
    lexer1 = Lexer(code)
    tokens1 = lexer1.tokenize_all()
    for t in tokens1:
        if t.type not in (TokenType.EOF, TokenType.NEWLINE, TokenType.WHITESPACE):
            print(f"  {t}")
    
    # Preserve comments
    print("\nWith skip_comments=False:\n")
    config = LexerConfig(skip_comments=False)
    lexer2 = Lexer(code, config)
    tokens2 = lexer2.tokenize_all()
    for t in tokens2:
        if t.type not in (TokenType.EOF, TokenType.NEWLINE, TokenType.WHITESPACE):
            print(f"  {t}")
    print()


def example_position_tracking():
    """Position tracking example."""
    print("=" * 60)
    print("Example 6: Position Tracking")
    print("=" * 60)
    
    code = '''line1_word1 line1_word2
line2_word1 line2_word2
line3_word1 line3_word2'''
    
    lexer = Lexer(code)
    
    print(f"\nInput code:\n{code}\n")
    print("Token positions (line, column):")
    
    for token in lexer.tokenize():
        if token.type == TokenType.IDENTIFIER:
            print(f"  {token.value:15} -> Line {token.line}, Column {token.column}")
    print()


def example_python_code():
    """Python code tokenization."""
    print("=" * 60)
    print("Example 7: Python-like Code")
    print("=" * 60)
    
    code = '''
def fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Usage
result = fibonacci(10)
print(f"Result: {result}")
'''
    
    python_keywords = {
        "def", "return", "if", "else", "elif", "for", "while", "class",
        "import", "from", "as", "try", "except", "finally", "with",
        "lambda", "yield", "global", "nonlocal", "assert", "pass",
        "break", "continue", "raise", "True", "False", "None", "in", "is",
        "and", "or", "not", "print"
    }
    
    config = LexerConfig(
        keywords=python_keywords,
        skip_comments=True
    )
    
    lexer = Lexer(code, config)
    
    print(f"\nInput code:\n{code}")
    print("Tokens by type:\n")
    
    tokens = lexer.tokenize_all()
    
    keywords = [t for t in tokens if t.type == TokenType.KEYWORD]
    identifiers = [t for t in tokens if t.type == TokenType.IDENTIFIER]
    integers = [t for t in tokens if t.type == TokenType.INTEGER]
    strings = [t for t in tokens if t.type == TokenType.STRING]
    
    print(f"Keywords ({len(keywords)}): {[k.value for k in keywords]}")
    print(f"Identifiers ({len(identifiers)}): {[i.value for i in identifiers]}")
    print(f"Integers ({len(integers)}): {[i.value for i in integers]}")
    print(f"Strings ({len(strings)}): {[s.value for s in strings]}")
    print()


def example_json_parsing():
    """JSON-like content parsing."""
    print("=" * 60)
    print("Example 8: JSON-like Content")
    print("=" * 60)
    
    json_data = '''
{
    "name": "Alice",
    "age": 30,
    "email": "alice@example.com",
    "active": true,
    "score": 95.5,
    "tags": ["user", "admin"],
    "address": {
        "city": "Beijing",
        "zip": "100000"
    }
}
'''
    
    lexer = Lexer(json_data)
    tokens = lexer.tokenize_all()
    
    print(f"\nInput JSON:\n{json_data}")
    print("Extracted data:")
    
    strings = extract_strings(tokens)
    numbers = extract_numbers(tokens)
    
    print(f"\nStrings: {strings}")
    print(f"Numbers: {numbers}")
    print()


def example_math_expression():
    """Mathematical expression parsing."""
    print("=" * 60)
    print("Example 9: Mathematical Expression")
    print("=" * 60)
    
    expr = "result = (a + b) * c / (d - e) ** 2"
    
    lexer = Lexer(expr)
    tokens = lexer.tokenize_all()
    
    print(f"\nExpression: {expr}\n")
    print("Token breakdown:")
    
    for t in tokens:
        if t.type != TokenType.EOF:
            type_name = t.type.name
            print(f"  {t.value:8} -> {type_name}")
    print()


def example_config_parser():
    """Simple config file parsing."""
    print("=" * 60)
    print("Example 10: Config File Parsing")
    print("=" * 60)
    
    config_text = '''
# Server configuration
host = "localhost"
port = 8080
debug = true
max_connections = 100
timeout = 30.5
'''
    
    print(f"\nConfig input:\n{config_text}")
    
    tokens = tokenize(config_text)
    
    # Simple config extraction: identifier = value
    print("Extracted configuration:\n")
    
    i = 0
    while i < len(tokens):
        if tokens[i].type == TokenType.IDENTIFIER:
            key = tokens[i].value
            # Look for '='
            if i + 1 < len(tokens) and tokens[i + 1].value == "=":
                # Get the value
                if i + 2 < len(tokens):
                    value_token = tokens[i + 2]
                    if value_token.type in (TokenType.STRING, TokenType.INTEGER, TokenType.FLOAT):
                        print(f"  {key}: {value_token.value!r}")
                    elif value_token.type == TokenType.IDENTIFIER:
                        print(f"  {key}: {value_token.value} (identifier)")
                i += 3
                continue
        i += 1
    print()


def example_simple_lexer():
    """SimpleLexer usage example."""
    print("=" * 60)
    print("Example 11: SimpleLexer (Basic Tokenizer)")
    print("=" * 60)
    
    text = "hello world foo bar"
    
    lexer = SimpleLexer(text)
    
    print(f"\nInput: {text!r}\n")
    print("Tokens with positions:")
    
    for token, start, end in lexer:
        print(f"  {token!r:15} at [{start}:{end}]")
    print()


def example_streaming_lexer():
    """StreamingLexer usage example."""
    print("=" * 60)
    print("Example 12: StreamingLexer (Chunked Input)")
    print("=" * 60)
    
    # Simulate streaming input
    chunks = ["x ", "= ", "42 ", "+ ", "y"]
    
    lexer = StreamingLexer()
    
    print(f"\nProcessing chunks: {chunks}\n")
    
    for i, chunk in enumerate(chunks):
        tokens = lexer.feed(chunk)
        if tokens:
            print(f"  After chunk {i+1} ({chunk!r}):")
            for t in tokens:
                print(f"    {t}")
    
    # Flush remaining
    remaining = lexer.flush()
    if remaining:
        print("  Remaining tokens:")
        for t in remaining:
            if t.type != TokenType.EOF:
                print(f"    {t}")
    print()


def example_csv_like_parsing():
    """CSV-like parsing with SimpleLexer."""
    print("=" * 60)
    print("Example 13: CSV-like Parsing")
    print("=" * 60)
    
    csv_data = "Alice,30,Engineer\nBob,25,Designer\nCarol,35,Manager"
    
    print(f"\nInput CSV:\n{csv_data}\n")
    print("Parsed rows:\n")
    
    for line in csv_data.split("\n"):
        lexer = SimpleLexer(line, delimiters=",")
        tokens = lexer.tokenize()
        print(f"  {tokens}")
    print()


def example_find_and_extract():
    """Find and extract utilities example."""
    print("=" * 60)
    print("Example 14: Find and Extract Utilities")
    print("=" * 60)
    
    code = "def process(data): return data.filter(x => x.active)"
    tokens = tokenize(code)
    
    print(f"\nInput: {code}\n")
    
    # Find specific token
    data_token = find_token(tokens, "data")
    if data_token:
        print(f"Found 'data' at line {data_token.line}, column {data_token.column}")
    
    # Find all occurrences
    all_data = find_all_tokens(tokens, "data")
    print(f"All 'data' occurrences: {len(all_data)}")
    
    # Extract by type
    identifiers = extract_identifiers(tokens)
    print(f"All identifiers: {identifiers}")
    print()


def main():
    """Run all examples."""
    example_basic_tokenization()
    example_custom_keywords()
    example_numbers()
    example_strings()
    example_comments()
    example_position_tracking()
    example_python_code()
    example_json_parsing()
    example_math_expression()
    example_config_parser()
    example_simple_lexer()
    example_streaming_lexer()
    example_csv_like_parsing()
    example_find_and_extract()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()