"""
Glob Pattern Utils - A pure Python implementation of glob-style pattern matching.

This module provides utilities for matching strings against glob patterns without
any external dependencies. It supports standard glob syntax plus extended features.

Supported Pattern Syntax:
    *       Matches any sequence of characters (including empty)
    ?       Matches any single character
    [abc]   Matches any character in the set
    [!abc]  Matches any character NOT in the set
    [^abc]  Same as [!abc] - matches any character NOT in the set
    [a-z]   Matches any character in the range
    {a,b,c} Matches any of the alternatives (brace expansion)
    \\      Escape character - treats the next character literally

Features:
    - Zero external dependencies
    - Case-sensitive and case-insensitive matching
    - Recursive directory pattern matching (globstar **)
    - Brace expansion support
    - Character class support with ranges and negation
    - Escape character support
"""

from typing import List, Set, Tuple, Optional, Pattern
import re


class GlobPattern:
    """
    A compiled glob pattern for efficient repeated matching.
    
    Example:
        >>> pattern = GlobPattern("*.txt")
        >>> pattern.match("file.txt")
        True
        >>> pattern.match("file.py")
        False
    """
    
    def __init__(self, pattern: str, case_sensitive: bool = True):
        """
        Initialize a compiled glob pattern.
        
        Args:
            pattern: The glob pattern string
            case_sensitive: Whether matching should be case-sensitive (default: True)
        """
        self.pattern = pattern
        self.case_sensitive = case_sensitive
        self._regex = self._compile_to_regex(pattern)
    
    def _compile_to_regex(self, pattern: str) -> Pattern:
        """Compile glob pattern to a regex pattern."""
        regex_parts = []
        i = 0
        n = len(pattern)
        
        while i < n:
            char = pattern[i]
            
            if char == '\\':
                # Escape next character
                if i + 1 < n:
                    regex_parts.append(re.escape(pattern[i + 1]))
                    i += 2
                else:
                    regex_parts.append(re.escape('\\'))
                    i += 1
            
            elif char == '*':
                # Check for globstar **
                if i + 1 < n and pattern[i + 1] == '*':
                    # ** matches anything including path separators
                    # Handle **/ specially - it can match zero or more directories
                    if i + 2 < n and pattern[i + 2] == '/':
                        # **/ can match nothing (root) or any path ending with /
                        regex_parts.append('(?:.*/)?')
                        i += 3  # Skip **/
                    else:
                        # ** at end or followed by non-/
                        regex_parts.append('.*')
                        i += 2
                else:
                    # * matches anything except path separator
                    regex_parts.append('[^/]*')
                    i += 1
            
            elif char == '?':
                # ? matches any single character
                regex_parts.append('.')
                i += 1
            
            elif char == '[':
                # Character class
                end, char_class = self._parse_char_class(pattern, i)
                regex_parts.append(char_class)
                i = end
            
            elif char == '{':
                # Brace expansion
                end, brace_pattern = self._parse_brace(pattern, i)
                regex_parts.append(brace_pattern)
                i = end
            
            else:
                # Regular character - escape for regex
                regex_parts.append(re.escape(char))
                i += 1
        
        # Compile the regex
        regex_str = '^' + ''.join(regex_parts) + '$'
        flags = 0 if self.case_sensitive else re.IGNORECASE
        return re.compile(regex_str, flags)
    
    def _parse_char_class(self, pattern: str, start: int) -> Tuple[int, str]:
        """
        Parse a character class [...].
        
        Returns:
            Tuple of (end_index, regex_char_class)
        """
        i = start + 1  # Skip the opening [
        n = len(pattern)
        char_class_parts = ['[']
        
        if i < n and pattern[i] in '!^':
            # Negated character class
            char_class_parts.append('^')
            i += 1
        
        # Handle ] as first character in class (literal)
        if i < n and pattern[i] == ']':
            char_class_parts.append(']')
            i += 1
        
        while i < n and pattern[i] != ']':
            if pattern[i] == '\\' and i + 1 < n:
                # Escaped character
                char_class_parts.append('\\' + pattern[i + 1])
                i += 2
            elif i + 2 < n and pattern[i + 1] == '-':
                # Character range
                char_class_parts.append(pattern[i] + '-' + pattern[i + 2])
                i += 3
            else:
                char_class_parts.append(pattern[i])
                i += 1
        
        if i < n:
            i += 1  # Skip the closing ]
        
        char_class_parts.append(']')
        return i, ''.join(char_class_parts)
    
    def _parse_brace(self, pattern: str, start: int) -> Tuple[int, str]:
        """
        Parse brace expansion {a,b,c}.
        
        Returns:
            Tuple of (end_index, regex_alternation)
        """
        i = start + 1  # Skip the opening {
        n = len(pattern)
        alternatives = []
        current = []
        
        while i < n and pattern[i] != '}':
            if pattern[i] == '\\' and i + 1 < n:
                current.append(pattern[i + 1])
                i += 2
            elif pattern[i] == ',':
                alternatives.append(''.join(current))
                current = []
                i += 1
            else:
                current.append(pattern[i])
                i += 1
        
        if current:
            alternatives.append(''.join(current))
        
        if i < n:
            i += 1  # Skip the closing }
        
        if not alternatives:
            return i, ''
        
        # Escape each alternative for regex
        escaped = [re.escape(alt) for alt in alternatives]
        return i, '(' + '|'.join(escaped) + ')'
    
    def match(self, text: str) -> bool:
        """
        Check if the text matches this glob pattern.
        
        Args:
            text: The string to match against
        
        Returns:
            True if the text matches the pattern, False otherwise
        """
        return bool(self._regex.match(text))
    
    def __repr__(self) -> str:
        return f"GlobPattern({self.pattern!r}, case_sensitive={self.case_sensitive})"


def match(pattern: str, text: str, case_sensitive: bool = True) -> bool:
    """
    Check if a string matches a glob pattern.
    
    This is a convenience function that creates a GlobPattern and matches against it.
    For repeated matching with the same pattern, use GlobPattern directly.
    
    Args:
        pattern: The glob pattern
        text: The string to match
        case_sensitive: Whether to match case-sensitively (default: True)
    
    Returns:
        True if the text matches the pattern, False otherwise
    
    Example:
        >>> match("*.txt", "file.txt")
        True
        >>> match("file?.txt", "file1.txt")
        True
        >>> match("file?.txt", "file12.txt")
        False
        >>> match("[abc]*", "apple")
        True
    """
    return GlobPattern(pattern, case_sensitive).match(text)


def filter_strings(pattern: str, strings: List[str], case_sensitive: bool = True) -> List[str]:
    """
    Filter a list of strings, returning only those that match the glob pattern.
    
    Args:
        pattern: The glob pattern
        strings: List of strings to filter
        case_sensitive: Whether to match case-sensitively (default: True)
    
    Returns:
        List of strings that match the pattern
    
    Example:
        >>> filter_strings("*.py", ["main.py", "test.txt", "utils.py"])
        ['main.py', 'utils.py']
    """
    compiled = GlobPattern(pattern, case_sensitive)
    return [s for s in strings if compiled.match(s)]


def expand_braces(pattern: str) -> List[str]:
    """
    Expand brace expressions in a glob pattern.
    
    This returns all possible expansions of brace expressions without
    performing matching.
    
    Args:
        pattern: The glob pattern with brace expressions
    
    Returns:
        List of expanded patterns
    
    Example:
        >>> expand_braces("file.{txt,py,md}")
        ['file.txt', 'file.py', 'file.md']
        >>> expand_braces("{a,b}{1,2}")
        ['a1', 'a2', 'b1', 'b2']
    """
    # Find all brace expressions
    result = ['']
    i = 0
    n = len(pattern)
    
    while i < n:
        if pattern[i] == '{':
            # Find the matching closing brace
            depth = 1
            start = i + 1
            i += 1
            while i < n and depth > 0:
                if pattern[i] == '{':
                    depth += 1
                elif pattern[i] == '}':
                    depth -= 1
                i += 1
            
            # Parse alternatives
            brace_content = pattern[start:i-1]
            alternatives = _split_brace_alternatives(brace_content)
            
            # Expand with existing results
            new_result = []
            for prefix in result:
                for alt in alternatives:
                    new_result.append(prefix + alt)
            result = new_result
        
        elif pattern[i] == '\\' and i + 1 < n:
            # Escape character
            for j in range(len(result)):
                result[j] += pattern[i + 1]
            i += 2
        
        else:
            # Regular character
            for j in range(len(result)):
                result[j] += pattern[i]
            i += 1
    
    return result


def _split_brace_alternatives(content: str) -> List[str]:
    """Split brace content by commas, respecting nested braces."""
    alternatives = []
    current = []
    depth = 0
    
    for char in content:
        if char == '{':
            depth += 1
            current.append(char)
        elif char == '}':
            depth -= 1
            current.append(char)
        elif char == ',' and depth == 0:
            alternatives.append(''.join(current))
            current = []
        else:
            current.append(char)
    
    if current:
        alternatives.append(''.join(current))
    
    return alternatives


def translate(pattern: str) -> str:
    """
    Translate a glob pattern to a regular expression string.
    
    Args:
        pattern: The glob pattern
    
    Returns:
        A regex pattern string (without ^ and $ anchors)
    
    Example:
        >>> translate("*.txt")
        '[^/]*\\\\.txt'
    """
    compiled = GlobPattern(pattern)
    regex = compiled._regex.pattern
    # Remove anchors
    if regex.startswith('^'):
        regex = regex[1:]
    if regex.endswith('$'):
        regex = regex[:-1]
    return regex


def is_glob(pattern: str) -> bool:
    """
    Check if a pattern contains glob special characters.
    
    Args:
        pattern: The pattern to check
    
    Returns:
        True if the pattern contains glob metacharacters, False otherwise
    
    Example:
        >>> is_glob("*.txt")
        True
        >>> is_glob("file.txt")
        False
    """
    special_chars = set('*?[]{}')
    i = 0
    while i < len(pattern):
        if pattern[i] == '\\' and i + 1 < len(pattern):
            i += 2
            continue
        if pattern[i] in special_chars:
            return True
        i += 1
    return False


def escape(pattern: str) -> str:
    """
    Escape glob metacharacters in a string.
    
    This is useful when you want to match a literal string that may
    contain glob metacharacters.
    
    Args:
        pattern: The string to escape
    
    Returns:
        The escaped string with glob metacharacters escaped
    
    Example:
        >>> escape("file*.txt")
        'file\\\\*.txt'
        >>> escape("file[1].txt")
        'file\\\\[1\\\\].txt'
    """
    special_chars = set('*?[]{}\\')
    result = []
    for char in pattern:
        if char in special_chars:
            result.append('\\')
        result.append(char)
    return ''.join(result)


class GlobMatcher:
    """
    A stateful glob matcher for matching multiple patterns against multiple strings.
    
    This is more efficient than creating multiple GlobPattern objects when
    matching many patterns against many strings.
    
    Example:
        >>> matcher = GlobMatcher()
        >>> matcher.add_pattern("*.py")
        >>> matcher.add_pattern("*.txt")
        >>> matcher.match_any("file.py")
        True
        >>> matcher.match_any("file.md")
        False
    """
    
    def __init__(self, case_sensitive: bool = True):
        """Initialize the matcher."""
        self.case_sensitive = case_sensitive
        self._patterns: List[GlobPattern] = []
    
    def add_pattern(self, pattern: str) -> None:
        """Add a pattern to the matcher."""
        self._patterns.append(GlobPattern(pattern, self.case_sensitive))
    
    def match_any(self, text: str) -> bool:
        """
        Check if the text matches any of the added patterns.
        
        Args:
            text: The string to match
        
        Returns:
            True if the text matches any pattern, False otherwise
        """
        return any(p.match(text) for p in self._patterns)
    
    def match_all(self, text: str) -> bool:
        """
        Check if the text matches all of the added patterns.
        
        Args:
            text: The string to match
        
        Returns:
            True if the text matches all patterns, False otherwise
        """
        return all(p.match(text) for p in self._patterns)
    
    def filter(self, strings: List[str]) -> List[str]:
        """
        Filter strings that match any of the patterns.
        
        Args:
            strings: List of strings to filter
        
        Returns:
            List of strings that match at least one pattern
        """
        return [s for s in strings if self.match_any(s)]
    
    def clear(self) -> None:
        """Remove all patterns from the matcher."""
        self._patterns.clear()


def fnmatch_translate(name: str, pattern: str, case_sensitive: bool = True) -> bool:
    """
    Unix-style fnmatch - check if a name matches a pattern.
    
    This follows Unix shell-style wildcard matching conventions.
    
    Args:
        name: The name to check
        pattern: The glob pattern
        case_sensitive: Whether matching is case-sensitive
    
    Returns:
        True if the name matches the pattern
    
    Example:
        >>> fnmatch_translate("file.txt", "*.txt")
        True
        >>> fnmatch_translate("FILE.TXT", "*.txt", case_sensitive=False)
        True
    """
    return match(pattern, name, case_sensitive)


def glob_to_regex(pattern: str) -> Pattern:
    """
    Convert a glob pattern to a compiled regex Pattern object.
    
    Args:
        pattern: The glob pattern
    
    Returns:
        A compiled re.Pattern object
    
    Example:
        >>> regex = glob_to_regex("*.txt")
        >>> bool(regex.match("file.txt"))
        True
    """
    return GlobPattern(pattern)._regex


# Convenience constants for common patterns
ANYTHING = "*"
ANY_SINGLE = "?"
ANY_DIGIT = "[0-9]"
ANY_LETTER = "[a-zA-Z]"
ANY_LETTER_LOWER = "[a-z]"
ANY_LETTER_UPPER = "[A-Z]"
ANY_ALPHANUMERIC = "[a-zA-Z0-9]"
HEX_DIGIT = "[0-9a-fA-F]"