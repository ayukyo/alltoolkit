#!/usr/bin/env python3
"""
Syntax Highlight Utils - Examples

This file demonstrates various uses of the syntax_highlight module.
Run with: python examples.py
"""

from syntax_highlight import highlight, highlight_html, get_tokens, strip_ansi


def example_basic_highlight():
    """Basic syntax highlighting example."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Syntax Highlighting")
    print("=" * 60)
    
    code = '''
def greet(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}!"

# Call the function
message = greet("World")
print(message)
'''
    
    # Print with syntax highlighting
    print(highlight(code, lang="python"))


def example_with_line_numbers():
    """Syntax highlighting with line numbers."""
    print("\n" + "=" * 60)
    print("Example 2: With Line Numbers")
    print("=" * 60)
    
    code = '''
class Calculator:
    """A simple calculator class."""
    
    def add(self, a: int, b: int) -> int:
        return a + b
    
    def multiply(self, a: int, b: int) -> int:
        return a * b
'''
    
    print(highlight(code, lang="python", line_numbers=True))


def example_javascript():
    """JavaScript syntax highlighting."""
    print("\n" + "=" * 60)
    print("Example 3: JavaScript Highlighting")
    print("=" * 60)
    
    js_code = '''
const fetchData = async (url) => {
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
};

class EventEmitter {
    constructor() {
        this.listeners = new Map();
    }
}
'''
    
    print(highlight(js_code, lang="javascript"))


def example_html_output():
    """Generate HTML output for web display."""
    print("\n" + "=" * 60)
    print("Example 4: HTML Output")
    print("=" * 60)
    
    code = '''
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
'''
    
    html = highlight_html(code, lang="python", line_numbers=True)
    print("Generated HTML (first 500 chars):")
    print(html[:500] + "...")
    
    # Save to file
    with open("example_output.html", "w") as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>Syntax Highlighting Example</title>
    <style>
        body {{
            background: #1e1e1e;
            color: #abb2bf;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            padding: 40px;
        }}
        h1 {{
            color: #61afef;
        }}
    </style>
</head>
<body>
    <h1>Quicksort Algorithm</h1>
    {html}
</body>
</html>""")
    
    print("\nHTML saved to: example_output.html")


def example_token_analysis():
    """Analyze code tokens."""
    print("\n" + "=" * 60)
    print("Example 5: Token Analysis")
    print("=" * 60)
    
    code = '''
@dataclass
class Person:
    name: str
    age: int = 0
    
    def greet(self) -> str:
        return f"Hi, I'm {self.name}"
'''
    
    tokens = get_tokens(code)
    
    # Count token types
    from collections import Counter
    type_counts = Counter(t.type.value for t in tokens)
    
    print("Token type counts:")
    for token_type, count in sorted(type_counts.items()):
        print(f"  {token_type}: {count}")
    
    print(f"\nTotal tokens: {len(tokens)}")


def example_strip_ansi():
    """Strip ANSI codes from highlighted output."""
    print("\n" + "=" * 60)
    print("Example 6: Strip ANSI Codes")
    print("=" * 60)
    
    code = "def hello(): return 'world'"
    highlighted = highlight(code)
    plain = strip_ansi(highlighted)
    
    print(f"Highlighted: {repr(highlighted[:30])}...")
    print(f"Plain: {repr(plain)}")


def example_complex_code():
    """Highlight more complex code."""
    print("\n" + "=" * 60)
    print("Example 7: Complex Code")
    print("=" * 60)
    
    code = '''
#!/usr/bin/env python3
"""Module docstring."""

from __future__ import annotations
from typing import List, Dict, Optional, Union
from dataclasses import dataclass
from functools import lru_cache
import re

# Constants
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30.0
PATTERN = re.compile(r"\\d+")

@dataclass
class Config:
    """Configuration settings."""
    host: str = "localhost"
    port: int = 8080
    debug: bool = False

class ApiClient:
    """API client with retry logic."""
    
    def __init__(self, config: Config):
        self.config = config
        self._session = None
    
    @lru_cache(maxsize=128)
    def get_cached(self, endpoint: str) -> Optional[Dict]:
        """Fetch and cache API response."""
        url = f"http://{self.config.host}:{self.config.port}/{endpoint}"
        # Simulated response
        return {"status": "ok", "data": [1, 2, 3]}
    
    async def fetch_all(self, endpoints: List[str]) -> List[Dict]:
        """Fetch multiple endpoints concurrently."""
        results = []
        for ep in endpoints:
            data = self.get_cached(ep)
            if data:
                results.append(data)
        return results

def main():
    """Main entry point."""
    config = Config(debug=True)
    client = ApiClient(config)
    
    # Test the client
    data = client.get_cached("api/v1/users")
    print(f"Users: {data}")
    
    # List comprehension with conditional
    nums = [x for x in range(10) if x % 2 == 0]
    
    # Dictionary comprehension
    squares = {n: n ** 2 for n in nums}
    
    # Match statement (Python 3.10+)
    value = "hello"
    match value:
        case "hello":
            print("Hi!")
        case _:
            print("Unknown")

if __name__ == "__main__":
    main()
'''
    
    print(highlight(code, lang="python", line_numbers=True))


def example_custom_styling():
    """Customize HTML output."""
    print("\n" + "=" * 60)
    print("Example 8: Custom HTML Styling")
    print("=" * 60)
    
    code = '''
def magic():
    """Do something magical."""
    return 42
'''
    
    custom_style = (
        "background: #1a1a2e; "
        "color: #e0e0e0; "
        "padding: 20px; "
        "border-radius: 12px; "
        "border: 1px solid #4a4a6a; "
        "font-family: 'JetBrains Mono', monospace; "
        "font-size: 13px; "
        "box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);"
    )
    
    html = highlight_html(code, lang="python", pre_style=custom_style)
    print("Custom styled HTML:")
    print(html)


def main():
    """Run all examples."""
    print("=" * 60)
    print("SYNTAX HIGHLIGHT UTILS - EXAMPLES")
    print("=" * 60)
    
    example_basic_highlight()
    example_with_line_numbers()
    example_javascript()
    example_html_output()
    example_token_analysis()
    example_strip_ansi()
    example_complex_code()
    example_custom_styling()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()