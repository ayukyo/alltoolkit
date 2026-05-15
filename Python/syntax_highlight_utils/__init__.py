"""
Syntax Highlight Utils - Zero-dependency syntax highlighting for Python.

A pure Python syntax highlighter supporting both ANSI terminal output
and HTML output for web display.
"""

from .syntax_highlight import (
    # Main functions
    highlight,
    highlight_html,
    get_tokens,
    strip_ansi,
    
    # Classes
    Lexer,
    Highlighter,
    Token,
    TokenType,
    
    # Themes
    ANSI_THEME,
    HTML_THEME,
    
    # Data
    PYTHON_KEYWORDS,
    PYTHON_BUILTINS,
    JS_KEYWORDS,
    JS_BUILTINS,
)

__version__ = "1.0.0"
__author__ = "AllToolkit"
__all__ = [
    "highlight",
    "highlight_html",
    "get_tokens",
    "strip_ansi",
    "Lexer",
    "Highlighter",
    "Token",
    "TokenType",
    "ANSI_THEME",
    "HTML_THEME",
    "PYTHON_KEYWORDS",
    "PYTHON_BUILTINS",
    "JS_KEYWORDS",
    "JS_BUILTINS",
]