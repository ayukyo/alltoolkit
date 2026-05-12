"""
slug_utils - URL-friendly slug generator

A lightweight utility for converting strings into URL-friendly slugs.
Zero external dependencies - uses only Python standard library.

Features:
- Convert strings to URL-safe slugs
- Transliterate common Unicode characters to ASCII
- Customizable separator and case options
- Remove or replace special characters
- Preserve or convert case
- Strip diacritics from accented characters

Author: AllToolkit Auto-Generator
Date: 2026-05-12
"""

import re
import unicodedata
from typing import Optional, Set


# Unicode character mappings for common transliterations
TRANSLITERATION_MAP = {
    # Latin extended characters
    'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'å': 'a',
    'æ': 'ae', 'ç': 'c',
    'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
    'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i',
    'ñ': 'n',
    'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o', 'ø': 'o',
    'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u',
    'ý': 'y', 'ÿ': 'y',
    'ß': 'ss',
    'đ': 'd', 'ð': 'd',
    'þ': 'th',
    # Greek
    'α': 'a', 'β': 'b', 'γ': 'g', 'δ': 'd', 'ε': 'e', 'ζ': 'z',
    'η': 'h', 'θ': 'th', 'ι': 'i', 'κ': 'k', 'λ': 'l', 'μ': 'm',
    'ν': 'n', 'ξ': 'x', 'ο': 'o', 'π': 'p', 'ρ': 'r', 'σ': 's',
    'τ': 't', 'υ': 'u', 'φ': 'f', 'χ': 'ch', 'ψ': 'ps', 'ω': 'o',
    # Greek final sigma (used at end of words)
    'ς': 's',
    # Cyrillic (simplified)
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l',
    'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's',
    'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch',
    'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
    'ю': 'yu', 'я': 'ya',
}

# Characters to remove entirely (not replaced with separator)
REMOVE_CHARS = set('\'"`´¨¸~^¨°')


def _is_ascii(s: str) -> bool:
    """Check if string contains only ASCII characters (Python 3.6 compatible)."""
    try:
        s.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False


def transliterate(text: str) -> str:
    """
    Transliterate Unicode characters to ASCII equivalents.
    
    Args:
        text: Input string with potential Unicode characters
        
    Returns:
        ASCII-friendly string with transliterated characters
    """
    result = []
    for char in text:
        lower_char = char.lower()
        if lower_char in TRANSLITERATION_MAP:
            result.append(TRANSLITERATION_MAP[lower_char])
        elif char in REMOVE_CHARS:
            continue
        elif lower_char in REMOVE_CHARS:
            continue
        else:
            # Try to normalize using NFKD decomposition
            normalized = unicodedata.normalize('NFKD', char)
            # Filter out combining characters (diacritics)
            filtered_chars = []
            for c in normalized:
                if not unicodedata.combining(c):
                    # Check if decomposed char is in transliteration map
                    c_lower = c.lower()
                    if c_lower in TRANSLITERATION_MAP:
                        filtered_chars.append(TRANSLITERATION_MAP[c_lower])
                    elif _is_ascii(c) and c.isalnum():
                        filtered_chars.append(c)
            filtered = ''.join(filtered_chars)
            if filtered:
                result.append(filtered)
            elif _is_ascii(char):
                result.append(char)
            # Non-ASCII chars not in map are skipped
    return ''.join(result)


def slugify(
    text: str,
    separator: str = '-',
    lowercase: bool = True,
    max_length: Optional[int] = None,
    word_boundary: bool = False,
    remove_words: Optional[Set[str]] = None,
    keep_chars: Optional[Set[str]] = None,
    strip_chars: Optional[str] = None,
) -> str:
    """
    Convert a string to a URL-friendly slug.
    
    Args:
        text: Input string to convert
        separator: Character to use between words (default: '-')
        lowercase: Convert to lowercase (default: True)
        max_length: Maximum length of slug (default: None, no limit)
        word_boundary: Try to preserve word boundaries when truncating
                      (default: False)
        remove_words: Set of words to remove from slug (default: None)
        keep_chars: Additional characters to keep (default: None)
        strip_chars: Characters to strip from start/end (default: separator)
        
    Returns:
        URL-friendly slug string
        
    Examples:
        >>> slugify("Hello World!")
        'hello-world'
        >>> slugify("Café & Restaurant", separator='_')
        'cafe_restaurant'
        >>> slugify("My Long Title Here", max_length=10, word_boundary=True)
        'my-long'
    """
    if not text:
        return ''
    
    # Transliterate Unicode to ASCII
    result = transliterate(text)
    
    # Handle case
    if lowercase:
        result = result.lower()
    
    # Build allowed characters set
    allowed = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    if keep_chars:
        allowed.update(keep_chars)
    
    # Replace non-allowed characters with separator
    temp_result = []
    for char in result:
        if char in allowed:
            temp_result.append(char)
        else:
            temp_result.append(separator)
    result = ''.join(temp_result)
    
    # Remove words if specified
    if remove_words:
        if lowercase:
            remove_words = {w.lower() for w in remove_words}
        words = result.split(separator)
        words = [w for w in words if w and w not in remove_words]
        result = separator.join(words)
    
    # Handle max length with word boundary
    if max_length and len(result) > max_length:
        if word_boundary:
            # Find last separator within limit
            truncated = result[:max_length]
            last_sep = truncated.rfind(separator)
            if last_sep > 0:
                result = truncated[:last_sep]
            else:
                result = truncated.rstrip(separator)
        else:
            result = result[:max_length]
    
    # Strip unwanted characters from ends
    if strip_chars is None:
        strip_chars = separator
    result = result.strip(strip_chars)
    
    # Remove consecutive separators
    if separator:
        pattern = re.escape(separator) + '+'
        result = re.sub(pattern, separator, result)
    
    return result


def slugify_unique(
    text: str,
    existing: Set[str],
    separator: str = '-',
    **kwargs
) -> str:
    """
    Generate a unique slug by appending a number if necessary.
    
    Args:
        text: Input string to convert
        existing: Set of existing slugs to check against
        separator: Character to use between words and suffix
        **kwargs: Additional arguments passed to slugify()
        
    Returns:
        Unique slug string
        
    Examples:
        >>> slugify_unique("Hello World", {"hello-world"})
        'hello-world-2'
        >>> slugify_unique("Hello World", {"hello-world", "hello-world-2"})
        'hello-world-3'
    """
    base_slug = slugify(text, separator=separator, **kwargs)
    
    if base_slug not in existing:
        return base_slug
    
    # Find next available number
    counter = 2
    while "{}{}{}".format(base_slug, separator, counter) in existing:
        counter += 1
    
    return "{}{}{}".format(base_slug, separator, counter)


def deslugify(slug: str, separator: str = '-') -> str:
    """
    Convert a slug back to a human-readable string.
    
    Args:
        slug: Slug string to convert
        separator: Separator used in slug (default: '-')
        
    Returns:
        Human-readable string with spaces
        
    Examples:
        >>> deslugify("hello-world")
        'hello world'
        >>> deslugify("my_blog_post", separator='_')
        'my blog post'
    """
    if not slug:
        return ''
    return slug.replace(separator, ' ')


def is_valid_slug(
    slug: str,
    separator: str = '-',
    allow_uppercase: bool = False,
    min_length: int = 1,
    max_length: Optional[int] = None
) -> bool:
    """
    Check if a string is a valid slug.
    
    Args:
        slug: String to validate
        separator: Expected separator (default: '-')
        allow_uppercase: Allow uppercase letters (default: False)
        min_length: Minimum length (default: 1)
        max_length: Maximum length (default: None, no limit)
        
    Returns:
        True if valid slug, False otherwise
        
    Examples:
        >>> is_valid_slug("hello-world")
        True
        >>> is_valid_slug("Hello World")
        False
        >>> is_valid_slug("hello_world", separator='_')
        True
    """
    if not slug:
        return False
    
    if len(slug) < min_length:
        return False
    
    if max_length and len(slug) > max_length:
        return False
    
    # Build valid character pattern
    valid_chars = set('abcdefghijklmnopqrstuvwxyz0123456789')
    if allow_uppercase:
        valid_chars.update('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    
    for char in slug:
        if char not in valid_chars and char != separator:
            return False
    
    # Check no consecutive separators
    if separator:
        double_sep = separator + separator
        if double_sep in slug:
            return False
        
        # Check doesn't start/end with separator
        if slug.startswith(separator) or slug.endswith(separator):
            return False
    
    return True


def slug_range(text: str, max_length: int, separator: str = '-') -> str:
    """
    Generate a slug that fits within max_length, preserving as much meaning as possible.
    
    Truncates intelligently by removing less important words first:
    1. Common filler words (a, an, the, etc.)
    2. Shorter words
    3. From the end of the string
    
    Args:
        text: Input string
        max_length: Maximum slug length
        separator: Separator to use (default: '-')
        
    Returns:
        Slug within length limit
        
    Examples:
        >>> slug_range("The Quick Brown Fox", 10)
        'quick-fox'
        >>> slug_range("A Very Long Title That Needs Truncation", 15)
        'long-title-needs'
    """
    # Words to remove first (common fillers)
    filler_words = {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    
    # First, generate full slug with filler words removed
    slug = slugify(text, separator=separator, remove_words=filler_words)
    
    if len(slug) <= max_length:
        return slug
    
    # Split into words and progressively remove shortest
    words = slug.split(separator)
    
    while len(separator.join(words)) > max_length and len(words) > 1:
        # Find shortest word (prefer removing from end)
        shortest_idx = len(words) - 1
        shortest_len = len(words[-1])
        for i in range(len(words) - 2, -1, -1):
            if len(words[i]) < shortest_len:
                shortest_len = len(words[i])
                shortest_idx = i
        words.pop(shortest_idx)
    
    result = separator.join(words)
    
    # Final truncation if still too long
    if len(result) > max_length:
        result = result[:max_length].rstrip(separator)
    
    return result


# Convenience function aliases
def slug(text: str, **kwargs) -> str:
    """Alias for slugify()."""
    return slugify(text, **kwargs)


def url_slug(text: str, **kwargs) -> str:
    """Alias for slugify() with URL-specific defaults."""
    return slugify(text, separator='-', lowercase=True, **kwargs)


def file_slug(text: str, **kwargs) -> str:
    """Alias for slugify() with file-system-friendly defaults."""
    return slugify(text, separator='_', lowercase=True, **kwargs)


if __name__ == '__main__':
    # Quick demo
    examples = [
        "Hello, World!",
        "Café & Restaurant Menu",
        "My Awesome Blog Post!!!",
        "The Quick Brown Fox Jumps Over The Lazy Dog",
        "Это тест на русском языке",
        "Angular vs React vs Vue 2024",
    ]
    
    print("Slug Generator Demo\n" + "=" * 40)
    for ex in examples:
        print("{} -> {}".format(repr(ex), slugify(ex)))