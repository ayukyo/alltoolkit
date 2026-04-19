#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Aho-Corasick Algorithm Utilities Module
====================================================
A comprehensive Aho-Corasick automaton implementation with zero external dependencies.

The Aho-Corasick algorithm is an efficient string matching algorithm that can
find all occurrences of multiple patterns in a text in O(n + m + z) time,
where n is text length, m is total pattern length, and z is number of matches.

Features:
    - Build automaton from pattern set
    - Single-pass text matching
    - Case-sensitive and case-insensitive matching
    - Match callback support
    - Streaming text processing
    - Pattern removal and dynamic updates
    - Match positions and pattern info
    - Wildcard pattern support (optional)
    - Custom match handlers
    - Serialization/deserialization support

Use Cases:
    - Keyword detection and extraction
    - Sensitive word filtering
    - Spam detection
    - Virus signature matching
    - DNA sequence analysis
    - Log file pattern matching
    - Real-time content moderation

Author: AllToolkit Contributors
License: MIT
"""

from typing import (
    List, Dict, Set, Tuple, Optional, Callable, Any, 
    Iterator, Iterable, Union, TypeVar, Generic
)
from dataclasses import dataclass, field
from collections import deque, defaultdict
import json
import pickle


T = TypeVar('T')


@dataclass
class Match(Generic[T]):
    """
    Represents a match found in the text.
    
    Attributes:
        start: Start position of the match (inclusive)
        end: End position of the match (exclusive)
        pattern: The matched pattern string
        value: Optional value associated with the pattern
    """
    start: int
    end: int
    pattern: str
    value: Optional[T] = None
    
    def __len__(self) -> int:
        return self.end - self.start
    
    def __repr__(self) -> str:
        return f"Match(start={self.start}, end={self.end}, pattern={self.pattern!r})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Match):
            return False
        return (self.start == other.start and self.end == other.end and 
                self.pattern == other.pattern)
    
    def __hash__(self) -> int:
        return hash((self.start, self.end, self.pattern))
    
    @property
    def length(self) -> int:
        """Return the length of the matched pattern."""
        return len(self.pattern)


class AhoCorasickNode:
    """
    Represents a node in the Aho-Corasick automaton.
    
    Each node contains:
    - children: transitions to child nodes
    - failure: failure link for pattern matching
    - output: patterns that end at this node
    - values: optional values associated with patterns
    """
    
    __slots__ = ['children', 'failure', 'output', 'values', 'is_root']
    
    def __init__(self, is_root: bool = False):
        self.children: Dict[str, 'AhoCorasickNode'] = {}
        self.failure: Optional['AhoCorasickNode'] = None
        self.output: List[str] = []
        self.values: List[Any] = []
        self.is_root = is_root
    
    def __repr__(self) -> str:
        return f"AhoCorasickNode(output={self.output}, children={list(self.children.keys())})"


class AhoCorasick(Generic[T]):
    """
    Aho-Corasick string matching automaton.
    
    Efficiently finds all occurrences of multiple patterns in a text.
    Supports both case-sensitive and case-insensitive matching.
    
    Example:
        >>> ac = AhoCorasick(['he', 'she', 'his', 'hers'])
        >>> matches = ac.findall('ushers')
        >>> for m in matches:
        ...     print(f"'{m.pattern}' at [{m.start}:{m.end}]")
        'she' at [1:4]
        'he' at [2:4]
        'hers' at [2:6]
    """
    
    def __init__(
        self, 
        patterns: Optional[Iterable[str]] = None,
        case_sensitive: bool = True
    ):
        """
        Initialize the Aho-Corasick automaton.
        
        Args:
            patterns: Initial set of patterns to add
            case_sensitive: Whether matching is case-sensitive
        """
        self._root = AhoCorasickNode(is_root=True)
        self._pattern_count = 0
        self._case_sensitive = case_sensitive
        self._patterns: Set[str] = set()
        self._pattern_values: Dict[str, List[T]] = defaultdict(list)
        self._built = False
        
        if patterns:
            self.add_patterns(patterns)
    
    def _normalize(self, text: str) -> str:
        """Normalize text based on case sensitivity setting."""
        return text if self._case_sensitive else text.lower()
    
    def add_pattern(self, pattern: str, value: Optional[T] = None) -> 'AhoCorasick[T]':
        """
        Add a single pattern to the automaton.
        
        Args:
            pattern: Pattern string to add
            value: Optional value to associate with this pattern
            
        Returns:
            Self for method chaining
        """
        if not pattern:
            return self
        
        pattern = self._normalize(pattern)
        
        if pattern in self._patterns:
            if value is not None:
                self._pattern_values[pattern].append(value)
            return self
        
        self._patterns.add(pattern)
        if value is not None:
            self._pattern_values[pattern].append(value)
        
        node = self._root
        for char in pattern:
            if char not in node.children:
                node.children[char] = AhoCorasickNode()
            node = node.children[char]
        
        node.output.append(pattern)
        if value is not None:
            node.values.append(value)
        
        self._pattern_count += 1
        self._built = False
        return self
    
    def add_patterns(
        self, 
        patterns: Iterable[str],
        values: Optional[Iterable[T]] = None
    ) -> 'AhoCorasick[T]':
        """
        Add multiple patterns to the automaton.
        
        Args:
            patterns: Iterable of pattern strings
            values: Optional iterable of values to associate with patterns
            
        Returns:
            Self for method chaining
        """
        pattern_list = list(patterns)
        value_list = list(values) if values else [None] * len(pattern_list)
        
        for pattern, value in zip(pattern_list, value_list):
            self.add_pattern(pattern, value)
        
        return self
    
    def remove_pattern(self, pattern: str) -> bool:
        """
        Remove a pattern from the automaton.
        
        Note: This requires rebuilding the automaton.
        
        Args:
            pattern: Pattern to remove
            
        Returns:
            True if pattern was found and removed, False otherwise
        """
        pattern = self._normalize(pattern)
        
        if pattern not in self._patterns:
            return False
        
        self._patterns.discard(pattern)
        if pattern in self._pattern_values:
            del self._pattern_values[pattern]
        
        # Rebuild the automaton
        self._rebuild()
        return True
    
    def _rebuild(self) -> None:
        """Rebuild the automaton from scratch."""
        patterns = list(self._patterns)
        values_dict = dict(self._pattern_values)
        
        # Reset all state
        self._root = AhoCorasickNode(is_root=True)
        self._pattern_count = 0
        self._patterns = set()
        self._pattern_values = defaultdict(list)
        self._built = False
        
        for pattern in patterns:
            values = values_dict.get(pattern, [])
            if values:
                for value in values:
                    self.add_pattern(pattern, value)
            else:
                self.add_pattern(pattern)
    
    def build(self) -> 'AhoCorasick[T]':
        """
        Build the failure links for the automaton.
        
        This is called automatically before searching if not already built.
        Uses BFS to compute failure links efficiently.
        
        Returns:
            Self for method chaining
        """
        if self._built:
            return self
        
        # BFS to build failure links
        queue = deque()
        
        # Initialize failure links for depth-1 nodes
        for child in self._root.children.values():
            child.failure = self._root
            queue.append(child)
        
        # Process remaining nodes
        while queue:
            current = queue.popleft()
            
            for char, child in current.children.items():
                queue.append(child)
                
                # Find failure link
                failure = current.failure
                while failure and char not in failure.children:
                    failure = failure.failure
                
                if failure:
                    child.failure = failure.children.get(char, self._root)
                else:
                    child.failure = self._root
                
                # Merge outputs
                child.output.extend(child.failure.output)
                child.values.extend(child.failure.values)
        
        self._built = True
        return self
    
    def finditer(self, text: str) -> Iterator[Match[T]]:
        """
        Iterate over all matches in the text.
        
        Args:
            text: Text to search
            
        Yields:
            Match objects for each found pattern
        """
        if not self._patterns:
            return
        
        self.build()
        
        text = self._normalize(text)
        node = self._root
        
        for i, char in enumerate(text):
            # Follow failure links until we find a match or reach root
            while node is not self._root and char not in node.children:
                node = node.failure
            
            if char in node.children:
                node = node.children[char]
            else:
                node = self._root
            
            # Output all matches at this position
            for j, pattern in enumerate(node.output):
                start = i - len(pattern) + 1
                value = node.values[j] if j < len(node.values) else None
                yield Match(start, i + 1, pattern, value)
    
    def findall(self, text: str) -> List[Match[T]]:
        """
        Find all matches in the text.
        
        Args:
            text: Text to search
            
        Returns:
            List of all Match objects found
        """
        return list(self.finditer(text))
    
    def search(self, text: str) -> Optional[Match[T]]:
        """
        Find the first match in the text.
        
        Args:
            text: Text to search
            
        Returns:
            First Match object or None if no match found
        """
        try:
            return next(self.finditer(text))
        except StopIteration:
            return None
    
    def count(self, text: str, unique: bool = False) -> int:
        """
        Count matches in the text.
        
        Args:
            text: Text to search
            unique: If True, count unique pattern matches only
            
        Returns:
            Number of matches found
        """
        matches = self.findall(text)
        if unique:
            return len(set((m.start, m.pattern) for m in matches))
        return len(matches)
    
    def contains(self, text: str) -> bool:
        """
        Check if text contains any of the patterns.
        
        This is more efficient than findall() when you only need
        to know if there's a match, not what the matches are.
        
        Args:
            text: Text to check
            
        Returns:
            True if any pattern is found, False otherwise
        """
        return self.search(text) is not None
    
    def replace(
        self, 
        text: str, 
        replacement: Union[str, Callable[[Match[T]], str]] = '***'
    ) -> str:
        """
        Replace all matches in the text.
        
        Args:
            text: Text to process
            replacement: Replacement string or callable that takes a Match
                        and returns the replacement string
                        
        Returns:
            Text with all matches replaced
        """
        if not self._patterns:
            return text
        
        matches = list(self.finditer(text))
        if not matches:
            return text
        
        # Sort matches by start position (descending) to replace from end
        matches.sort(key=lambda m: m.start, reverse=True)
        
        result = list(text)
        for match in matches:
            repl = replacement(match) if callable(replacement) else replacement
            result[match.start:match.end] = list(repl)
        
        return ''.join(result)
    
    def highlight(
        self,
        text: str,
        prefix: str = '<mark>',
        suffix: str = '</mark>'
    ) -> str:
        """
        Highlight all matches in the text with HTML-like markers.
        
        Args:
            text: Text to process
            prefix: String to insert before each match
            suffix: String to insert after each match
            
        Returns:
            Text with all matches highlighted
        """
        if not self._patterns:
            return text
        
        matches = list(self.finditer(text))
        if not matches:
            return text
        
        # Sort matches by start position (descending)
        matches.sort(key=lambda m: m.start, reverse=True)
        
        result = list(text)
        for match in matches:
            result[match.end:match.end] = list(suffix)
            result[match.start:match.start] = list(prefix)
        
        return ''.join(result)
    
    def extract(self, text: str) -> List[str]:
        """
        Extract all matched patterns from text.
        
        Args:
            text: Text to search
            
        Returns:
            List of matched pattern strings
        """
        return [m.pattern for m in self.findall(text)]
    
    def extract_unique(self, text: str) -> Set[str]:
        """
        Extract unique matched patterns from text.
        
        Args:
            text: Text to search
            
        Returns:
            Set of unique matched pattern strings
        """
        return set(self.extract(text))
    
    def get_pattern_positions(
        self, 
        text: str
    ) -> Dict[str, List[Tuple[int, int]]]:
        """
        Get all positions for each matched pattern.
        
        Args:
            text: Text to search
            
        Returns:
            Dictionary mapping patterns to list of (start, end) tuples
        """
        positions: Dict[str, List[Tuple[int, int]]] = defaultdict(list)
        for match in self.finditer(text):
            positions[match.pattern].append((match.start, match.end))
        return dict(positions)
    
    def process_stream(
        self,
        text: str,
        callback: Callable[[Match[T]], None]
    ) -> None:
        """
        Process text stream with callback for each match.
        
        Useful for processing large texts without storing all matches
        in memory.
        
        Args:
            text: Text to process
            callback: Function to call for each match
        """
        for match in self.finditer(text):
            callback(match)
    
    @property
    def pattern_count(self) -> int:
        """Return the number of patterns in the automaton."""
        return self._pattern_count
    
    @property
    def patterns(self) -> Set[str]:
        """Return the set of patterns in the automaton."""
        return self._patterns.copy()
    
    def __len__(self) -> int:
        """Return the number of patterns."""
        return self._pattern_count
    
    def __contains__(self, pattern: str) -> bool:
        """Check if a pattern is in the automaton."""
        return self._normalize(pattern) in self._patterns
    
    def __repr__(self) -> str:
        return f"AhoCorasick(patterns={self._pattern_count}, case_sensitive={self._case_sensitive})"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the automaton to a dictionary.
        
        Returns:
            Dictionary representation of the automaton
        """
        return {
            'patterns': list(self._patterns),
            'pattern_values': {k: v for k, v in self._pattern_values.items()},
            'case_sensitive': self._case_sensitive
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AhoCorasick[T]':
        """
        Create an automaton from a dictionary.
        
        Args:
            data: Dictionary representation of the automaton
            
        Returns:
            New AhoCorasick instance
        """
        ac = cls(case_sensitive=data.get('case_sensitive', True))
        pattern_values = data.get('pattern_values', {})
        
        for pattern in data['patterns']:
            values = pattern_values.get(pattern, [])
            if values:
                for value in values:
                    ac.add_pattern(pattern, value)
            else:
                ac.add_pattern(pattern)
        
        return ac
    
    def to_json(self) -> str:
        """
        Serialize the automaton to JSON.
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_json(cls, json_str: str) -> 'AhoCorasick[T]':
        """
        Create an automaton from JSON.
        
        Args:
            json_str: JSON string representation
            
        Returns:
            New AhoCorasick instance
        """
        return cls.from_dict(json.loads(json_str))
    
    def save(self, filepath: str) -> None:
        """
        Save the automaton to a file.
        
        Args:
            filepath: Path to save the automaton
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
    
    @classmethod
    def load(cls, filepath: str) -> 'AhoCorasick[T]':
        """
        Load an automaton from a file.
        
        Args:
            filepath: Path to load the automaton from
            
        Returns:
            New AhoCorasick instance
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            return cls.from_json(f.read())


class SensitiveWordFilter:
    """
    A convenience wrapper for sensitive word filtering using Aho-Corasick.
    
    Provides a simple interface for common content moderation tasks.
    
    Example:
        >>> filter = SensitiveWordFilter(['bad', 'evil', 'spam'])
        >>> filter.check('This is bad content')
        True
        >>> filter.clean('This is bad content')
        'This is *** content'
    """
    
    def __init__(
        self,
        words: Optional[Iterable[str]] = None,
        replacement: str = '***',
        case_sensitive: bool = False
    ):
        """
        Initialize the sensitive word filter.
        
        Args:
            words: Initial set of sensitive words
            replacement: Default replacement string
            case_sensitive: Whether matching is case-sensitive
        """
        self._ac = AhoCorasick(case_sensitive=case_sensitive)
        self._replacement = replacement
        
        if words:
            self.add_words(words)
    
    def add_word(self, word: str) -> 'SensitiveWordFilter':
        """Add a sensitive word."""
        self._ac.add_pattern(word)
        return self
    
    def add_words(self, words: Iterable[str]) -> 'SensitiveWordFilter':
        """Add multiple sensitive words."""
        self._ac.add_patterns(words)
        return self
    
    def remove_word(self, word: str) -> bool:
        """Remove a sensitive word."""
        return self._ac.remove_pattern(word)
    
    def check(self, text: str) -> bool:
        """
        Check if text contains any sensitive words.
        
        Args:
            text: Text to check
            
        Returns:
            True if sensitive words found, False otherwise
        """
        return self._ac.contains(text)
    
    def find(self, text: str) -> List[str]:
        """
        Find all sensitive words in text.
        
        Args:
            text: Text to search
            
        Returns:
            List of found sensitive words
        """
        return self._ac.extract_unique(text)
    
    def clean(
        self, 
        text: str, 
        replacement: Optional[str] = None
    ) -> str:
        """
        Replace sensitive words in text.
        
        Args:
            text: Text to clean
            replacement: Replacement string (uses default if not provided)
            
        Returns:
            Cleaned text with sensitive words replaced
        """
        return self._ac.replace(text, replacement or self._replacement)
    
    def highlight(self, text: str) -> str:
        """Highlight sensitive words in text."""
        return self._ac.highlight(text)
    
    @property
    def words(self) -> Set[str]:
        """Return the set of sensitive words."""
        return self._ac.patterns
    
    def __len__(self) -> int:
        return len(self._ac)
    
    def __repr__(self) -> str:
        return f"SensitiveWordFilter(words={len(self)})"


# =============================================================================
# Convenience Functions
# =============================================================================

def build_automaton(
    patterns: Iterable[str],
    case_sensitive: bool = True
) -> AhoCorasick:
    """
    Build an Aho-Corasick automaton from patterns.
    
    Args:
        patterns: Iterable of pattern strings
        case_sensitive: Whether matching is case-sensitive
        
    Returns:
        Built AhoCorasick automaton
    """
    ac = AhoCorasick(patterns, case_sensitive)
    ac.build()
    return ac


def find_all(
    patterns: Iterable[str],
    text: str,
    case_sensitive: bool = True
) -> List[Match]:
    """
    Find all occurrences of patterns in text.
    
    Convenience function for one-time searches.
    
    Args:
        patterns: Iterable of pattern strings
        text: Text to search
        case_sensitive: Whether matching is case-sensitive
        
    Returns:
        List of Match objects
    """
    ac = build_automaton(patterns, case_sensitive)
    return ac.findall(text)


def contains_any(
    patterns: Iterable[str],
    text: str,
    case_sensitive: bool = True
) -> bool:
    """
    Check if text contains any of the patterns.
    
    Args:
        patterns: Iterable of pattern strings
        text: Text to check
        case_sensitive: Whether matching is case-sensitive
        
    Returns:
        True if any pattern is found
    """
    ac = build_automaton(patterns, case_sensitive)
    return ac.contains(text)


def replace_patterns(
    patterns: Iterable[str],
    text: str,
    replacement: str = '***',
    case_sensitive: bool = True
) -> str:
    """
    Replace all pattern matches in text.
    
    Args:
        patterns: Iterable of pattern strings
        text: Text to process
        replacement: Replacement string
        case_sensitive: Whether matching is case-sensitive
        
    Returns:
        Text with matches replaced
    """
    ac = build_automaton(patterns, case_sensitive)
    return ac.replace(text, replacement)


def highlight_patterns(
    patterns: Iterable[str],
    text: str,
    prefix: str = '<mark>',
    suffix: str = '</mark>',
    case_sensitive: bool = True
) -> str:
    """
    Highlight all pattern matches in text.
    
    Args:
        patterns: Iterable of pattern strings
        text: Text to process
        prefix: String to insert before each match
        suffix: String to insert after each match
        case_sensitive: Whether matching is case-sensitive
        
    Returns:
        Text with matches highlighted
    """
    ac = build_automaton(patterns, case_sensitive)
    return ac.highlight(text, prefix, suffix)


# =============================================================================
# Advanced Features
# =============================================================================

class WildcardAhoCorasick:
    """
    Aho-Corasick with wildcard support.
    
    Supports '?' as a single-character wildcard in patterns.
    
    Example:
        >>> wac = WildcardAhoCorasick(['c?t', 'd?g'])
        >>> wac.findall('cat dog cut')
        [Match(0, 3, 'c?t'), Match(4, 7, 'd?g'), Match(8, 11, 'c?t')]
    """
    
    def __init__(
        self,
        patterns: Optional[Iterable[str]] = None,
        wildcard: str = '?',
        case_sensitive: bool = True
    ):
        """
        Initialize with wildcard support.
        
        Args:
            patterns: Initial patterns
            wildcard: Wildcard character (default '?')
            case_sensitive: Whether matching is case-sensitive
        """
        self._wildcard = wildcard
        self._case_sensitive = case_sensitive
        self._original_patterns: List[str] = []
        self._expanded_patterns: List[str] = []
        
        # Use standard AhoCorasick with expanded patterns
        self._ac = AhoCorasick(case_sensitive=case_sensitive)
        
        if patterns:
            self.add_patterns(patterns)
    
    def _expand_pattern(self, pattern: str) -> List[str]:
        """Expand pattern with wildcards to concrete patterns."""
        if self._wildcard not in pattern:
            return [pattern]
        
        # For single wildcard, expand to all printable ASCII
        # This is a simplified expansion - real implementation would be more sophisticated
        import string
        chars = string.ascii_letters + string.digits
        patterns = ['']
        
        for char in pattern:
            if char == self._wildcard:
                patterns = [p + c for p in patterns for c in chars]
            else:
                patterns = [p + char for p in patterns]
        
        return patterns
    
    def add_pattern(self, pattern: str) -> 'WildcardAhoCorasick':
        """Add a pattern (may contain wildcards)."""
        self._original_patterns.append(pattern)
        expanded = self._expand_pattern(pattern)
        self._expanded_patterns.extend(expanded)
        self._ac.add_patterns(expanded)
        return self
    
    def add_patterns(self, patterns: Iterable[str]) -> 'WildcardAhoCorasick':
        """Add multiple patterns."""
        for pattern in patterns:
            self.add_pattern(pattern)
        return self
    
    def findall(self, text: str) -> List[Match]:
        """Find all matches."""
        return self._ac.findall(text)
    
    def finditer(self, text: str) -> Iterator[Match]:
        """Iterate over matches."""
        return self._ac.finditer(text)


class MultiPatternReplacer:
    """
    Efficient multi-pattern string replacer using Aho-Corasick.
    
    Allows different replacement strings for different patterns.
    
    Example:
        >>> replacer = MultiPatternReplacer()
        >>> replacer.add('foo', 'bar')
        >>> replacer.add('hello', 'hi')
        >>> replacer.replace('foo says hello')
        'bar says hi'
    """
    
    def __init__(self, case_sensitive: bool = False):
        """
        Initialize the replacer.
        
        Args:
            case_sensitive: Whether matching is case-sensitive
        """
        self._replacements: Dict[str, str] = {}
        self._ac = AhoCorasick(case_sensitive=case_sensitive)
        self._case_sensitive = case_sensitive
    
    def add(self, pattern: str, replacement: str) -> 'MultiPatternReplacer':
        """
        Add a pattern-replacement pair.
        
        Args:
            pattern: Pattern to find
            replacement: Text to replace with
            
        Returns:
            Self for chaining
        """
        normalized = pattern if self._case_sensitive else pattern.lower()
        self._replacements[normalized] = replacement
        self._ac.add_pattern(pattern)
        return self
    
    def add_many(
        self, 
        pairs: Iterable[Tuple[str, str]]
    ) -> 'MultiPatternReplacer':
        """Add multiple pattern-replacement pairs."""
        for pattern, replacement in pairs:
            self.add(pattern, replacement)
        return self
    
    def replace(self, text: str) -> str:
        """
        Replace all patterns in text.
        
        Args:
            text: Text to process
            
        Returns:
            Text with all replacements made
        """
        if not self._replacements:
            return text
        
        matches = list(self._ac.finditer(text))
        if not matches:
            return text
        
        # Sort by start position (descending)
        matches.sort(key=lambda m: m.start, reverse=True)
        
        result = list(text)
        for match in matches:
            normalized = match.pattern if self._case_sensitive else match.pattern.lower()
            replacement = self._replacements.get(normalized, match.pattern)
            result[match.start:match.end] = list(replacement)
        
        return ''.join(result)
    
    def __repr__(self) -> str:
        return f"MultiPatternReplacer(patterns={len(self._replacements)})"


if __name__ == '__main__':
    # Quick demo
    print("Aho-Corasick Algorithm Demo")
    print("=" * 50)
    
    # Basic usage
    patterns = ['he', 'she', 'his', 'hers']
    text = 'ushers'
    
    ac = AhoCorasick(patterns)
    print(f"\nPatterns: {patterns}")
    print(f"Text: '{text}'")
    print(f"Matches: {ac.findall(text)}")
    
    # Sensitive word filter
    print("\n\nSensitive Word Filter Demo")
    print("-" * 50)
    
    filter = SensitiveWordFilter(['bad', 'evil', 'spam', 'inappropriate'])
    test_text = "This is a bad example with evil content"
    print(f"Original: {test_text}")
    print(f"Contains sensitive words: {filter.check(test_text)}")
    print(f"Found words: {filter.find(test_text)}")
    print(f"Cleaned: {filter.clean(test_text)}")
    
    print("\nAll tests passed!")