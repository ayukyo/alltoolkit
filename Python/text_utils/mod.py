#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Text Utilities Module
====================================
A comprehensive text processing utility module for Python with zero external dependencies.

Features:
    - String cleaning and normalization
    - Text formatting and transformation
    - Search and replace utilities
    - Text analysis (word count, readability, etc.)
    - Pattern matching helpers
    - Encoding and escaping utilities

Author: AllToolkit Contributors
License: MIT
"""

import re
import string
import hashlib
from typing import Any, Dict, List, Optional, Union, Callable, Pattern, Tuple
from collections import Counter


# ============================================================================
# String Cleaning Functions
# ============================================================================

def clean_whitespace(text: str, normalize: bool = True) -> str:
    """
    Clean and normalize whitespace in text.
    
    Args:
        text: The input text
        normalize: Whether to normalize all whitespace to single spaces (default: True)
    
    Returns:
        Cleaned text with normalized whitespace
    
    Example:
        >>> clean_whitespace("  hello   world  ")
        'hello world'
        >>> clean_whitespace("hello\\n\\nworld", normalize=False)
        'hello world'
    """
    if text is None:
        return ""
    # Replace all whitespace sequences with single space
    result = re.sub(r'\s+', ' ', text)
    if normalize:
        return result.strip()
    return result


def clean_text(text: str, 
               remove_punctuation: bool = False,
               remove_digits: bool = False,
               lowercase: bool = False,
               strip: bool = True) -> str:
    """
    Clean text with multiple options.
    
    Args:
        text: The input text
        remove_punctuation: Whether to remove punctuation (default: False)
        remove_digits: Whether to remove digits (default: False)
        lowercase: Whether to convert to lowercase (default: False)
        strip: Whether to strip leading/trailing whitespace (default: True)
    
    Returns:
        Cleaned text
    
    Example:
        >>> clean_text("Hello, World! 123", remove_punctuation=True, remove_digits=True)
        'Hello World'
    """
    if text is None:
        return ""
    
    result = text
    
    if remove_punctuation:
        result = result.translate(str.maketrans('', '', string.punctuation))
    
    if remove_digits:
        result = re.sub(r'\d', '', result)
    
    if lowercase:
        result = result.lower()
    
    if strip:
        result = result.strip()
    
    return result


def remove_html_tags(text: str) -> str:
    """
    Remove HTML tags from text.
    
    Args:
        text: Text containing HTML tags
    
    Returns:
        Text with HTML tags removed
    
    Example:
        >>> remove_html_tags("<p>Hello <b>World</b></p>")
        'Hello World'
    """
    if text is None:
        return ""
    return re.sub(r'<[^>]+>', '', text)


def remove_urls(text: str, replacement: str = '') -> str:
    """
    Remove URLs from text.
    
    Args:
        text: The input text
        replacement: String to replace URLs with (default: '')
    
    Returns:
        Text with URLs removed
    
    Example:
        >>> remove_urls("Visit https://example.com for more")
        'Visit  for more'
    """
    if text is None:
        return ""
    url_pattern = r'https?://\S+|www\.\S+'
    return re.sub(url_pattern, replacement, text)


def remove_emojis(text: str) -> str:
    """
    Remove emojis from text.
    
    Args:
        text: The input text
    
    Returns:
        Text with emojis removed
    
    Example:
        >>> remove_emojis("Hello 👋 World 🌍")
        'Hello  World '
    """
    if text is None:
        return ""
    # Emoji Unicode ranges
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub('', text)


# ============================================================================
# Text Formatting Functions
# ============================================================================

def truncate(text: str, max_length: int, suffix: str = '...') -> str:
    """
    Truncate text to a maximum length with suffix.
    
    Args:
        text: The input text
        max_length: Maximum length including suffix
        suffix: Suffix to add when truncated (default: '...')
    
    Returns:
        Truncated text
    
    Example:
        >>> truncate("Hello World", 8)
        'Hello...'
    """
    if text is None:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def pad_left(text: str, width: int, fill_char: str = ' ') -> str:
    """
    Pad text on the left to reach specified width.
    
    Args:
        text: The input text
        width: Desired total width
        fill_char: Character to use for padding (default: ' ')
    
    Returns:
        Left-padded text
    
    Example:
        >>> pad_left("42", 5, '0')
        '00042'
    """
    if text is None:
        return fill_char * width
    return text.rjust(width, fill_char)


def pad_right(text: str, width: int, fill_char: str = ' ') -> str:
    """
    Pad text on the right to reach specified width.
    
    Args:
        text: The input text
        width: Desired total width
        fill_char: Character to use for padding (default: ' ')
    
    Returns:
        Right-padded text
    
    Example:
        >>> pad_right("Hello", 10)
        'Hello     '
    """
    if text is None:
        return fill_char * width
    return text.ljust(width, fill_char)


def pad_center(text: str, width: int, fill_char: str = ' ') -> str:
    """
    Center text within specified width.
    
    Args:
        text: The input text
        width: Desired total width
        fill_char: Character to use for padding (default: ' ')
    
    Returns:
        Centered text
    
    Example:
        >>> pad_center("Title", 20, '=')
        '=======Title======='
    """
    if text is None:
        return fill_char * width
    return text.center(width, fill_char)


def wrap_text(text: str, width: int = 80, break_long_words: bool = True) -> str:
    """
    Wrap text to specified width.
    
    Args:
        text: The input text
        width: Maximum line width (default: 80)
        break_long_words: Whether to break words longer than width (default: True)
    
    Returns:
        Wrapped text with newlines
    
    Example:
        >>> wrap_text("Hello world this is a long line", width=15)
        'Hello world\\nthis is a long\\nline'
    """
    if text is None:
        return ""
    if width <= 0:
        raise ValueError(f"width must be positive, got {width}")
    
    words = text.split()
    if not words:
        return ""
    
    lines = []
    current_line_parts = []
    current_length = 0
    
    for word in words:
        word_length = len(word)
        
        if break_long_words and word_length > width:
            # Flush current line first
            if current_line_parts:
                lines.append(' '.join(current_line_parts))
                current_line_parts = []
                current_length = 0
            
            # Break long word into chunks
            for i in range(0, word_length, width):
                chunk = word[i:i + width]
                if i + width < word_length:
                    lines.append(chunk)
                else:
                    current_line_parts.append(chunk)
                    current_length = len(chunk)
        else:
            # Check if word fits (add 1 for space if not first word)
            space_needed = 1 if current_line_parts else 0
            if current_length + word_length + space_needed <= width:
                current_line_parts.append(word)
                current_length += word_length + space_needed
            else:
                lines.append(' '.join(current_line_parts))
                current_line_parts = [word]
                current_length = word_length
    
    if current_line_parts:
        lines.append(' '.join(current_line_parts))
    
    return '\n'.join(lines)


def indent_text(text: str, spaces: int = 4, skip_first: bool = False) -> str:
    """
    Add indentation to each line of text.
    
    Args:
        text: The input text
        spaces: Number of spaces for indentation (default: 4)
        skip_first: Whether to skip indenting the first line (default: False)
    
    Returns:
        Indented text
    
    Example:
        >>> indent_text("line1\\nline2", spaces=2)
        '  line1\\n  line2'
    """
    if text is None:
        return ""
    
    indent = ' ' * spaces
    lines = text.split('\n')
    
    if skip_first:
        return lines[0] + '\n' + '\n'.join(indent + line for line in lines[1:])
    
    return '\n'.join(indent + line for line in lines)


# ============================================================================
# Case Conversion Functions
# ============================================================================

def to_camel_case(text: str) -> str:
    """
    Convert text to camelCase.
    
    Args:
        text: The input text (snake_case, kebab-case, or space-separated)
    
    Returns:
        camelCase text
    
    Example:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("Hello World")
        'helloWorld'
    """
    if text is None:
        return ""
    
    # Split on various separators
    words = re.split(r'[-_\s]+', text.lower())
    if not words:
        return ""
    
    return words[0] + ''.join(word.capitalize() for word in words[1:])


def to_pascal_case(text: str) -> str:
    """
    Convert text to PascalCase.
    
    Args:
        text: The input text
    
    Returns:
        PascalCase text
    
    Example:
        >>> to_pascal_case("hello_world")
        'HelloWorld'
    """
    if text is None:
        return ""
    
    words = re.split(r'[-_\s]+', text.lower())
    return ''.join(word.capitalize() for word in words)


def to_snake_case(text: str) -> str:
    """
    Convert text to snake_case.
    
    Args:
        text: The input text (camelCase, PascalCase, or space-separated)
    
    Returns:
        snake_case text
    
    Example:
        >>> to_snake_case("helloWorld")
        'hello_world'
    """
    if text is None:
        return ""
    
    # Handle camelCase and PascalCase
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', text)
    s2 = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1)
    
    # Replace other separators with underscore
    s3 = re.sub(r'[-\s]+', '_', s2)
    
    return s3.lower()


def to_kebab_case(text: str) -> str:
    """
    Convert text to kebab-case.
    
    Args:
        text: The input text
    
    Returns:
        kebab-case text
    
    Example:
        >>> to_kebab_case("helloWorld")
        'hello-world'
    """
    if text is None:
        return ""
    
    snake = to_snake_case(text)
    return snake.replace('_', '-')


def to_title_case(text: str) -> str:
    """
    Convert text to title case.
    
    Args:
        text: The input text
    
    Returns:
        Title case text
    
    Example:
        >>> to_title_case("hello world")
        'Hello World'
    """
    if text is None:
        return ""
    return text.title()


# ============================================================================
# Search and Replace Functions
# ============================================================================

def replace_all(text: str, replacements: Dict[str, str]) -> str:
    """
    Replace multiple patterns in text.
    
    Args:
        text: The input text
        replacements: Dictionary of {pattern: replacement}
    
    Returns:
        Text with all replacements applied
    
    Example:
        >>> replace_all("hello world", {"hello": "hi", "world": "there"})
        'hi there'
    """
    if text is None:
        return ""
    
    result = text
    for pattern, replacement in replacements.items():
        result = result.replace(pattern, replacement)
    return result


def replace_regex(text: str, pattern: Union[str, Pattern], replacement: Union[str, Callable]) -> str:
    """
    Replace all matches of a regex pattern in text.
    
    Args:
        text: The input text
        pattern: Regex pattern (string or compiled pattern)
        replacement: Replacement string or function
    
    Returns:
        Text with replacements applied
    
    Example:
        >>> replace_regex("abc123def", r'\\d+', 'X')
        'abcXdef'
    """
    if text is None:
        return ""
    return re.sub(pattern, replacement, text)


def find_all(text: str, pattern: Union[str, Pattern]) -> List[str]:
    """
    Find all matches of a pattern in text.
    
    Args:
        text: The input text
        pattern: Regex pattern
    
    Returns:
        List of all matches
    
    Example:
        >>> find_all("abc123def456", r'\\d+')
        ['123', '456']
    """
    if text is None:
        return []
    return re.findall(pattern, text)


def find_first(text: str, pattern: Union[str, Pattern], default: str = '') -> str:
    """
    Find the first match of a pattern in text.
    
    Args:
        text: The input text
        pattern: Regex pattern
        default: Default value if no match found (default: '')
    
    Returns:
        First match or default value
    
    Example:
        >>> find_first("abc123def", r'\\d+')
        '123'
    """
    if text is None:
        return default
    match = re.search(pattern, text)
    return match.group(0) if match else default


# ============================================================================
# Text Analysis Functions
# ============================================================================

def count_words(text: str) -> int:
    """
    Count the number of words in text.
    
    Args:
        text: The input text
    
    Returns:
        Word count
    
    Example:
        >>> count_words("Hello world this is a test")
        6
    """
    if text is None:
        return 0
    return len(text.split())


def count_chars(text: str, include_spaces: bool = True) -> int:
    """
    Count the number of characters in text.
    
    Args:
        text: The input text
        include_spaces: Whether to include spaces (default: True)
    
    Returns:
        Character count
    
    Example:
        >>> count_chars("Hello World", include_spaces=False)
        10
    """
    if text is None:
        return 0
    if include_spaces:
        return len(text)
    return len(text.replace(' ', ''))


def count_lines(text: str) -> int:
    """
    Count the number of lines in text.
    
    Args:
        text: The input text
    
    Returns:
        Line count
    
    Example:
        >>> count_lines("line1\\nline2\\nline3")
        3
    """
    if text is None:
        return 0
    if not text:
        return 0
    return text.count('\n') + 1


def word_frequency(text: str, lowercase: bool = True) -> Dict[str, int]:
    """
    Calculate word frequency in text.
    
    Args:
        text: The input text
        lowercase: Whether to normalize to lowercase (default: True)
    
    Returns:
        Dictionary of {word: count}
    
    Example:
        >>> word_frequency("hello world hello")
        {'hello': 2, 'world': 1}
    """
    if text is None:
        return {}
    
    words = text.split()
    if lowercase:
        words = [w.lower() for w in words]
    
    return dict(Counter(words))


def char_frequency(text: str) -> Dict[str, int]:
    """
    Calculate character frequency in text.
    
    Args:
        text: The input text
    
    Returns:
        Dictionary of {char: count}
    
    Example:
        >>> char_frequency("hello")
        {'h': 1, 'e': 1, 'l': 2, 'o': 1}
    """
    if text is None:
        return {}
    return dict(Counter(text))


def readability_score(text: str) -> Dict[str, float]:
    """
    Calculate basic readability metrics.
    
    Args:
        text: The input text
    
    Returns:
        Dictionary with readability metrics:
        - avg_sentence_length: Average words per sentence
        - avg_word_length: Average characters per word
        - sentence_count: Number of sentences
        - word_count: Number of words
    
    Example:
        >>> readability_score("Hello world. This is a test.")
        {'avg_sentence_length': 3.5, 'avg_word_length': 3.5, ...}
    """
    if text is None:
        return {}
    
    # Split into sentences (simple approach)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    words = text.split()
    
    if not sentences or not words:
        return {
            'avg_sentence_length': 0.0,
            'avg_word_length': 0.0,
            'sentence_count': 0,
            'word_count': 0
        }
    
    total_word_length = sum(len(word) for word in words)
    
    return {
        'avg_sentence_length': len(words) / len(sentences),
        'avg_word_length': total_word_length / len(words),
        'sentence_count': len(sentences),
        'word_count': len(words)
    }


# ============================================================================
# Encoding and Escaping Functions
# ============================================================================

def escape_html(text: str) -> str:
    """
    Escape HTML special characters.
    
    Args:
        text: The input text
    
    Returns:
        HTML-escaped text
    
    Example:
        >>> escape_html("<script>alert('XSS')</script>")
        '&lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;'
    """
    if text is None:
        return ""
    
    replacements = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#x27;',
    }
    
    result = text
    for char, replacement in replacements.items():
        result = result.replace(char, replacement)
    return result


def unescape_html(text: str) -> str:
    """
    Unescape HTML entities.
    
    Args:
        text: HTML-escaped text
    
    Returns:
        Unescaped text
    
    Example:
        >>> unescape_html("&lt;hello&gt;")
        '<hello>'
    """
    if text is None:
        return ""
    
    replacements = {
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&quot;': '"',
        '&#x27;': "'",
        '&apos;': "'",
        '&nbsp;': ' ',
    }
    
    result = text
    for entity, char in replacements.items():
        result = result.replace(entity, char)
    return result


def escape_regex(text: str) -> str:
    """
    Escape special regex characters in text.
    
    Args:
        text: The input text
    
    Returns:
        Regex-escaped text
    
    Example:
        >>> escape_regex("price: $100")
        'price: \\$100'
    """
    if text is None:
        return ""
    return re.escape(text)


def hash_text(text: str, algorithm: str = 'sha256') -> str:
    """
    Generate a hash of the text.
    
    Args:
        text: The input text
        algorithm: Hash algorithm ('md5', 'sha1', 'sha256', 'sha512') (default: 'sha256')
    
    Returns:
        Hexadecimal hash string
    
    Example:
        >>> hash_text("hello", algorithm='md5')
        '5d41402abc4b2a76b9719d911017c592'
    """
    if text is None:
        return ""
    
    algorithms = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512,
    }
    
    if algorithm not in algorithms:
        raise ValueError(f"Unsupported algorithm: {algorithm}. Choose from {list(algorithms.keys())}")
    
    return algorithms[algorithm](text.encode('utf-8')).hexdigest()


# ============================================================================
# String Comparison Functions
# ============================================================================

def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculate the Levenshtein distance between two strings.
    
    Args:
        s1: First string
        s2: Second string
    
    Returns:
        Edit distance between the strings
    
    Example:
        >>> levenshtein_distance("kitten", "sitting")
        3
    """
    if s1 is None:
        s1 = ""
    if s2 is None:
        s2 = ""
    
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def similarity_ratio(s1: str, s2: str) -> float:
    """
    Calculate similarity ratio between two strings (0.0 to 1.0).
    
    Args:
        s1: First string
        s2: Second string
    
    Returns:
        Similarity ratio (1.0 = identical, 0.0 = completely different)
    
    Example:
        >>> similarity_ratio("hello", "hello")
        1.0
        >>> similarity_ratio("hello", "hallo")
        0.8
    """
    if s1 is None:
        s1 = ""
    if s2 is None:
        s2 = ""
    
    if not s1 and not s2:
        return 1.0
    
    distance = levenshtein_distance(s1, s2)
    max_length = max(len(s1), len(s2))
    
    return 1.0 - (distance / max_length)


def is_palindrome(text: str, ignore_case: bool = True, ignore_spaces: bool = True) -> bool:
    """
    Check if text is a palindrome.
    
    Args:
        text: The input text
        ignore_case: Whether to ignore case (default: True)
        ignore_spaces: Whether to ignore spaces (default: True)
    
    Returns:
        True if palindrome, False otherwise
    
    Example:
        >>> is_palindrome("A man a plan a canal Panama")
        True
    """
    if text is None:
        return False
    
    processed = text
    if ignore_case:
        processed = processed.lower()
    if ignore_spaces:
        processed = processed.replace(' ', '')
    
    return processed == processed[::-1]


# ============================================================================
# Utility Functions
# ============================================================================

def is_empty(text: str) -> bool:
    """
    Check if text is empty or whitespace-only.
    
    Args:
        text: The input text
    
    Returns:
        True if empty or whitespace-only
    
    Example:
        >>> is_empty("   ")
        True
    """
    if text is None:
        return True
    return len(text.strip()) == 0


def is_not_empty(text: str) -> bool:
    """
    Check if text is not empty.
    
    Args:
        text: The input text
    
    Returns:
        True if not empty
    
    Example:
        >>> is_not_empty("hello")
        True
    """
    return not is_empty(text)


def reverse_string(text: str) -> str:
    """
    Reverse a string.
    
    Args:
        text: The input text
    
    Returns:
        Reversed string
    
    Example:
        >>> reverse_string("hello")
        'olleh'
    """
    if text is None:
        return ""
    return text[::-1]


def repeat_string(text: str, count: int, separator: str = '') -> str:
    """
    Repeat a string multiple times.
    
    Args:
        text: The input text
        count: Number of times to repeat
        separator: Separator between repetitions (default: '')
    
    Returns:
        Repeated string
    
    Example:
        >>> repeat_string("ab", 3, separator='-')
        'ab-ab-ab'
    """
    if text is None:
        return ""
    if count <= 0:
        return ""
    return separator.join([text] * count)


def generate_random_string(length: int, 
                           use_letters: bool = True,
                           use_digits: bool = True,
                           use_special: bool = False) -> str:
    """
    Generate a random string.
    
    Args:
        length: Length of the string to generate
        use_letters: Whether to include letters (default: True)
        use_digits: Whether to include digits (default: True)
        use_special: Whether to include special characters (default: False)
    
    Returns:
        Random string
    
    Example:
        >>> generate_random_string(10)  # e.g., 'aB3xK9mP2q'
    """
    import random
    
    chars = ''
    if use_letters:
        chars += string.ascii_letters
    if use_digits:
        chars += string.digits
    if use_special:
        chars += string.punctuation
    
    if not chars:
        chars = string.ascii_letters + string.digits
    
    return ''.join(random.choice(chars) for _ in range(length))


def extract_numbers(text: str) -> List[int]:
    """
    Extract all numbers from text.
    
    Args:
        text: The input text
    
    Returns:
        List of integers found in text
    
    Example:
        >>> extract_numbers("I have 3 apples and 5 oranges")
        [3, 5]
    """
    if text is None:
        return []
    return [int(n) for n in re.findall(r'\d+', text)]


def extract_emails(text: str) -> List[str]:
    """
    Extract all email addresses from text.
    
    Args:
        text: The input text
    
    Returns:
        List of email addresses found in text
    
    Example:
        >>> extract_emails("Contact us at support@example.com or sales@company.org")
        ['support@example.com', 'sales@company.org']
    """
    if text is None:
        return []
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)


def mask_text(text: str, 
              mask_char: str = '*',
              visible_start: int = 0,
              visible_end: int = 0) -> str:
    """
    Mask text (useful for sensitive data like passwords, credit cards).
    
    Args:
        text: The input text to mask
        mask_char: Character to use for masking (default: '*')
        visible_start: Number of characters to leave visible at start (default: 0)
        visible_end: Number of characters to leave visible at end (default: 0)
    
    Returns:
        Masked text
    
    Example:
        >>> mask_text("1234567890", visible_end=4)
        '******7890'
        >>> mask_text("password", mask_char='*', visible_start=2, visible_end=2)
        'pa****rd'
    """
    if text is None:
        return ""
    
    total_length = len(text)
    visible_total = visible_start + visible_end
    
    if visible_total >= total_length:
        return text
    
    masked_length = total_length - visible_total
    
    return text[:visible_start] + (mask_char * masked_length) + text[-visible_end:] if visible_end else text[:visible_start] + (mask_char * masked_length)
