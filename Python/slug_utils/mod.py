#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Slug Utilities Module
===================================
A comprehensive URL slug generation utility module for Python with zero external dependencies.

Features:
    - Generate URL-friendly slugs from strings
    - Support for multiple languages (Chinese, Japanese, Korean, etc.)
    - Transliteration for non-Latin scripts
    - Custom separators and character mappings
    - Case conversion options
    - Duplicate slug handling
    - Batch slug generation
    - SEO-friendly output

Author: AllToolkit Contributors
License: MIT
"""

import re
import unicodedata
from typing import Callable, Dict, List, Optional, Tuple


# ============================================================================
# Character Mapping Tables
# ============================================================================

# Latin character transliteration mappings
LATIN_MAP: Dict[str, str] = {
    'À': 'A', 'Á': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A', 'Å': 'A',
    'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'å': 'a',
    'Æ': 'AE', 'æ': 'ae',
    'Ç': 'C', 'ç': 'c',
    'Ð': 'D', 'ð': 'd',
    'È': 'E', 'É': 'E', 'Ê': 'E', 'Ë': 'E',
    'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
    'Ì': 'I', 'Í': 'I', 'Î': 'I', 'Ï': 'I',
    'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i',
    'Ñ': 'N', 'ñ': 'n',
    'Ò': 'O', 'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ö': 'O', 'Ø': 'O',
    'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o', 'ø': 'o',
    'Ù': 'U', 'Ú': 'U', 'Û': 'U', 'Ü': 'U',
    'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u',
    'Ý': 'Y', 'ý': 'y', 'ÿ': 'y',
    'ß': 'ss',
    'Þ': 'Th', 'þ': 'th',
}

# Cyrillic to Latin transliteration
CYRILLIC_MAP: Dict[str, str] = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
    'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
    'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
    'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
    'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch',
    'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
    'э': 'e', 'ю': 'yu', 'я': 'ya',
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D',
    'Е': 'E', 'Ё': 'Yo', 'Ж': 'Zh', 'З': 'Z', 'И': 'I',
    'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
    'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T',
    'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch',
    'Ш': 'Sh', 'Щ': 'Sch', 'Ъ': '', 'Ы': 'Y', 'Ь': '',
    'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya',
}

# Greek to Latin transliteration
GREEK_MAP: Dict[str, str] = {
    'α': 'a', 'ά': 'a', 'β': 'b', 'γ': 'g', 'δ': 'd', 'ε': 'e', 'έ': 'e',
    'ζ': 'z', 'η': 'i', 'ή': 'i', 'θ': 'th', 'ι': 'i', 'ί': 'i', 'ϊ': 'i',
    'κ': 'k', 'λ': 'l', 'μ': 'm', 'ν': 'n', 'ξ': 'x', 'ο': 'o', 'ό': 'o',
    'π': 'p', 'ρ': 'r', 'σ': 's', 'ς': 's', 'τ': 't', 'υ': 'y', 'ύ': 'y',
    'φ': 'f', 'χ': 'ch', 'ψ': 'ps', 'ω': 'o', 'ώ': 'o',
    'Α': 'A', 'Ά': 'A', 'Β': 'B', 'Γ': 'G', 'Δ': 'D', 'Ε': 'E', 'Έ': 'E',
    'Ζ': 'Z', 'Η': 'I', 'Ή': 'I', 'Θ': 'Th', 'Ι': 'I', 'Ί': 'I', 'Ϊ': 'I',
    'Κ': 'K', 'Λ': 'L', 'Μ': 'M', 'Ν': 'N', 'Ξ': 'X', 'Ο': 'O', 'Ό': 'O',
    'Π': 'P', 'Ρ': 'R', 'Σ': 'S', 'Τ': 'T', 'Υ': 'Y', 'Ύ': 'Y',
    'Φ': 'F', 'Χ': 'Ch', 'Ψ': 'Ps', 'Ω': 'O', 'Ώ': 'O',
}

# Common word mappings for SEO-friendly slugs
WORD_MAP: Dict[str, str] = {
    '&': ' and ',
    '+': ' plus ',
    '=': ' equals ',
}


# ============================================================================
# Core Slug Functions
# ============================================================================

def transliterate(text: str) -> str:
    """
    Transliterate non-Latin characters to Latin.
    
    Args:
        text: Input text to transliterate
    
    Returns:
        Transliterated text
    
    Example:
        >>> transliterate("Héllo Wörld")
        'Hello World'
        >>> transliterate("Привет")
        'Privet'
        >>> transliterate("Γειά σου")
        'Geia sou'
    """
    result = []
    
    for char in text:
        # Check Latin map first
        if char in LATIN_MAP:
            result.append(LATIN_MAP[char])
        # Check Cyrillic map
        elif char in CYRILLIC_MAP:
            result.append(CYRILLIC_MAP[char])
        # Check Greek map
        elif char in GREEK_MAP:
            result.append(GREEK_MAP[char])
        # Try Unicode normalization for other characters
        else:
            # Normalize and check if it's a combining character
            normalized = unicodedata.normalize('NFKD', char)
            # Filter out combining characters
            filtered = ''.join(c for c in normalized 
                             if not unicodedata.combining(c))
            if filtered and filtered != char:
                result.append(filtered)
            else:
                result.append(char)
    
    return ''.join(result)


def normalize(text: str, lowercase: bool = True) -> str:
    """
    Normalize text for slug generation.
    
    Args:
        text: Input text
        lowercase: Convert to lowercase
    
    Returns:
        Normalized text
    
    Example:
        >>> normalize("Héllo Wörld!")
        'hello world'
    """
    # Transliterate
    text = transliterate(text)
    
    # Convert to lowercase if needed
    if lowercase:
        text = text.lower()
    
    return text


def generate_slug(
    text: str,
    separator: str = '-',
    lowercase: bool = True,
    max_length: Optional[int] = None,
    word_boundary: bool = True,
    custom_map: Optional[Dict[str, str]] = None,
    allowed_chars: Optional[str] = None,
    strip_common_words: bool = False,
    common_words: Optional[List[str]] = None
) -> str:
    """
    Generate a URL-friendly slug from text.
    
    Args:
        text: Input text to convert
        separator: Character to separate words (default: '-')
        lowercase: Convert to lowercase (default: True)
        max_length: Maximum slug length (default: None)
        word_boundary: Truncate at word boundary (default: True)
        custom_map: Custom character mappings
        allowed_chars: Additional allowed characters (regex pattern)
        strip_common_words: Remove common words like 'a', 'the', etc.
        common_words: List of common words to strip
    
    Returns:
        URL-friendly slug
    
    Example:
        >>> generate_slug("Hello World!")
        'hello-world'
        >>> generate_slug("Héllo Wörld!", separator='_')
        'hello_world'
        >>> generate_slug("This is a Long Title", max_length=15)
        'this-is-a-long'
    """
    if not text:
        return ''
    
    # Apply custom mappings first
    if custom_map:
        for old, new in custom_map.items():
            text = text.replace(old, new)
    
    # Apply word mappings
    for word, replacement in WORD_MAP.items():
        text = text.replace(word, f' {replacement} ')
    
    # Transliterate and normalize
    text = normalize(text, lowercase)
    
    # Strip common words if requested
    if strip_common_words:
        default_common = ['a', 'an', 'the', 'is', 'are', 'was', 'were', 
                         'be', 'been', 'being', 'have', 'has', 'had', 
                         'do', 'does', 'did', 'will', 'would', 'could', 
                         'should', 'may', 'might', 'must', 'shall', 
                         'can', 'need', 'dare', 'ought', 'used', 'to',
                         'of', 'in', 'for', 'on', 'with', 'at', 'by',
                         'from', 'as', 'into', 'through', 'during',
                         'before', 'after', 'above', 'below', 'between']
        words_to_strip = common_words or default_common
        words = text.split()
        words = [w for w in words if w not in words_to_strip]
        text = ' '.join(words)
    
    # Build allowed character pattern
    if allowed_chars:
        pattern = f'[^a-z0-9{re.escape(allowed_chars)}]'
    else:
        pattern = r'[^a-z0-9]'
    
    # Replace non-alphanumeric with separator
    slug = re.sub(pattern, separator, text)
    
    # Remove duplicate separators
    if separator:
        dup_pattern = re.escape(separator) + '+'
        slug = re.sub(dup_pattern, separator, slug)
        # Strip separators from ends
        slug = slug.strip(separator)
    
    # Handle max length
    if max_length and len(slug) > max_length:
        if word_boundary and separator:
            # Truncate at last complete word
            truncated = slug[:max_length]
            last_sep = truncated.rfind(separator)
            if last_sep > 0:
                slug = truncated[:last_sep]
            else:
                slug = truncated.rstrip(separator)
        else:
            slug = slug[:max_length].rstrip(separator)
    
    return slug


def generate_unique_slug(
    text: str,
    existing: List[str],
    separator: str = '-',
    lowercase: bool = True,
    max_length: Optional[int] = None,
    max_attempts: int = 1000
) -> str:
    """
    Generate a unique slug that doesn't conflict with existing slugs.
    
    Args:
        text: Input text
        existing: List of existing slugs to avoid
        separator: Word separator
        lowercase: Convert to lowercase
        max_length: Maximum slug length
        max_attempts: Maximum attempts before raising error
    
    Returns:
        Unique slug
    
    Example:
        >>> generate_unique_slug("Hello World", ["hello-world"])
        'hello-world-2'
        >>> generate_unique_slug("Hello World", ["hello-world", "hello-world-2"])
        'hello-world-3'
    """
    base_slug = generate_slug(text, separator, lowercase, max_length)
    
    if base_slug not in existing:
        return base_slug
    
    # Find a unique slug by appending a number
    counter = 2
    while counter < max_attempts:
        suffix = f"{separator}{counter}"
        
        # Adjust max_length to accommodate suffix
        if max_length:
            adjusted_length = max_length - len(suffix)
            if adjusted_length > 0:
                candidate = generate_slug(text, separator, lowercase, adjusted_length) + suffix
            else:
                candidate = base_slug[:max_length - len(suffix)] + suffix
        else:
            candidate = base_slug + suffix
        
        if candidate not in existing:
            return candidate
        
        counter += 1
    
    raise ValueError(f"Could not generate unique slug after {max_attempts} attempts")


def generate_sequential_slug(
    text: str,
    index: int = 1,
    separator: str = '-',
    lowercase: bool = True,
    max_length: Optional[int] = None,
    index_width: int = 0
) -> str:
    """
    Generate a slug with sequential numbering.
    
    Args:
        text: Input text
        index: Sequence number
        separator: Word separator
        lowercase: Convert to lowercase
        max_length: Maximum slug length
        index_width: Zero-pad index to this width (0 = no padding)
    
    Returns:
        Slug with sequential number
    
    Example:
        >>> generate_sequential_slug("Blog Post", 1)
        'blog-post-1'
        >>> generate_sequential_slug("Blog Post", 5, index_width=3)
        'blog-post-005'
    """
    base_slug = generate_slug(text, separator, lowercase, max_length)
    
    if index_width > 0:
        index_str = str(index).zfill(index_width)
    else:
        index_str = str(index)
    
    # Adjust max_length to accommodate index
    if max_length:
        suffix = separator + index_str
        available = max_length - len(suffix)
        if available > 0:
            base_slug = generate_slug(text, separator, lowercase, available)
    
    return f"{base_slug}{separator}{index_str}" if base_slug else index_str


# ============================================================================
# Specialized Slug Functions
# ============================================================================

def generate_date_slug(
    text: str,
    date_str: Optional[str] = None,
    separator: str = '-',
    lowercase: bool = True,
    date_format: str = "%Y-%m-%d",
    max_length: Optional[int] = None
) -> str:
    """
    Generate a slug with date prefix.
    
    Args:
        text: Input text
        date_str: Date string (ISO format) or None for today
        separator: Word separator
        lowercase: Convert to lowercase
        date_format: strftime format for date
        max_length: Maximum slug length
    
    Returns:
        Date-prefixed slug
    
    Example:
        >>> generate_date_slug("My Blog Post", "2024-01-15")
        '2024-01-15-my-blog-post'
    """
    import datetime
    
    if date_str:
        # Try common date formats (Python 3.6 compatible)
        formats = ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y"]
        for fmt in formats:
            try:
                date = datetime.datetime.strptime(date_str, fmt).date()
                break
            except ValueError:
                continue
        else:
            raise ValueError(f"Cannot parse date: {date_str}")
    else:
        date = datetime.date.today()
    
    date_prefix = date.strftime(date_format)
    text_slug = generate_slug(text, separator, lowercase, max_length)
    
    return f"{date_prefix}{separator}{text_slug}" if text_slug else date_prefix


def generate_category_slug(
    text: str,
    category: str,
    separator: str = '-',
    lowercase: bool = True,
    max_length: Optional[int] = None
) -> str:
    """
    Generate a slug with category prefix.
    
    Args:
        text: Input text
        category: Category name
        separator: Word separator
        lowercase: Convert to lowercase
        max_length: Maximum slug length
    
    Returns:
        Category-prefixed slug
    
    Example:
        >>> generate_category_slug("My Post", "Tech")
        'tech-my-post'
    """
    cat_slug = generate_slug(category, separator, lowercase)
    text_slug = generate_slug(text, separator, lowercase, max_length)
    
    return f"{cat_slug}{separator}{text_slug}" if text_slug else cat_slug


def generate_hierarchical_slug(
    parts: List[str],
    separator: str = '-',
    lowercase: bool = True,
    path_separator: str = '/'
) -> str:
    """
    Generate a hierarchical slug from multiple parts.
    
    Args:
        parts: List of path components
        separator: Word separator within parts
        lowercase: Convert to lowercase
        path_separator: Separator between parts
    
    Returns:
        Hierarchical slug
    
    Example:
        >>> generate_hierarchical_slug(["Tech", "Programming", "Python Tutorial"])
        'tech/programming/python-tutorial'
    """
    slugs = [generate_slug(part, separator, lowercase) for part in parts]
    # Filter out empty parts
    slugs = [s for s in slugs if s]
    return path_separator.join(slugs)


# ============================================================================
# Batch Operations
# ============================================================================

def generate_slug_batch(
    texts: List[str],
    separator: str = '-',
    lowercase: bool = True,
    max_length: Optional[int] = None,
    ensure_unique: bool = True
) -> List[str]:
    """
    Generate slugs for multiple texts, ensuring uniqueness.
    
    Args:
        texts: List of input texts
        separator: Word separator
        lowercase: Convert to lowercase
        max_length: Maximum slug length
        ensure_unique: Add numbers to ensure unique slugs
    
    Returns:
        List of generated slugs
    
    Example:
        >>> generate_slug_batch(["Hello", "Hello", "Hello World"])
        ['hello', 'hello-2', 'hello-world']
    """
    if not ensure_unique:
        return [generate_slug(text, separator, lowercase, max_length) for text in texts]
    
    result = []
    seen = set()
    
    for text in texts:
        base_slug = generate_slug(text, separator, lowercase, max_length)
        
        if base_slug in seen:
            counter = 2
            while True:
                candidate = f"{base_slug}{separator}{counter}"
                if candidate not in seen:
                    slug = candidate
                    break
                counter += 1
        else:
            slug = base_slug
        
        result.append(slug)
        seen.add(slug)
    
    return result


def slug_from_filename(
    filename: str,
    separator: str = '-',
    lowercase: bool = True,
    max_length: Optional[int] = None,
    remove_extension: bool = True
) -> str:
    """
    Generate a slug from a filename.
    
    Args:
        filename: Input filename
        separator: Word separator
        lowercase: Convert to lowercase
        max_length: Maximum slug length
        remove_extension: Remove file extension
    
    Returns:
        Filename-based slug
    
    Example:
        >>> slug_from_filename("My Document.pdf")
        'my-document'
        >>> slug_from_filename("2024-01-15-Report.docx", remove_extension=True)
        '2024-01-15-report'
    """
    import os
    
    if remove_extension:
        name = os.path.splitext(filename)[0]
    else:
        name = filename
    
    return generate_slug(name, separator, lowercase, max_length)


# ============================================================================
# Validation and Utilities
# ============================================================================

def is_valid_slug(
    slug: str,
    separator: str = '-',
    allow_uppercase: bool = False,
    max_length: Optional[int] = None
) -> bool:
    """
    Check if a string is a valid slug.
    
    Args:
        slug: String to validate
        separator: Allowed separator character
        allow_uppercase: Allow uppercase letters
        max_length: Maximum allowed length
    
    Returns:
        True if valid slug
    
    Example:
        >>> is_valid_slug("hello-world")
        True
        >>> is_valid_slug("hello world")
        False
        >>> is_valid_slug("")
        False
    """
    if not slug:
        return False
    
    if max_length and len(slug) > max_length:
        return False
    
    if allow_uppercase:
        pattern = f'^[a-zA-Z0-9{re.escape(separator)}]+$'
    else:
        pattern = f'^[a-z0-9{re.escape(separator)}]+$'
    
    return bool(re.match(pattern, slug))


def fix_slug(
    slug: str,
    separator: str = '-',
    lowercase: bool = True,
    max_length: Optional[int] = None
) -> str:
    """
    Fix and normalize an existing slug.
    
    Args:
        slug: Slug to fix
        separator: Word separator
        lowercase: Convert to lowercase
        max_length: Maximum slug length
    
    Returns:
        Fixed slug
    
    Example:
        >>> fix_slug("Hello___World")
        'hello-world'
        >>> fix_slug("hello world")
        'hello-world'
    """
    if lowercase:
        slug = slug.lower()
    
    # Replace spaces and underscores with separator
    slug = re.sub(r'[\s_]+', separator, slug)
    
    # Replace invalid characters with separator (to preserve word boundaries)
    slug = re.sub(r'[^a-z0-9]', separator, slug)
    
    # Remove duplicate separators
    dup_pattern = re.escape(separator) + '+'
    slug = re.sub(dup_pattern, separator, slug)
    
    # Strip separators from ends
    slug = slug.strip(separator)
    
    # Apply max length
    if max_length and len(slug) > max_length:
        slug = slug[:max_length].rstrip(separator)
    
    return slug


def slug_to_text(slug: str, separator: str = '-') -> str:
    """
    Convert a slug back to readable text.
    
    Args:
        slug: Slug to convert
        separator: Separator used in slug
    
    Returns:
        Human-readable text
    
    Example:
        >>> slug_to_text("hello-world")
        'Hello World'
        >>> slug_to_text("my-blog-post-2024")
        'My Blog Post 2024'
    """
    words = slug.split(separator)
    return ' '.join(word.capitalize() for word in words)


def compare_slugs(slug1: str, slug2: str, ignore_case: bool = True) -> bool:
    """
    Compare two slugs for equality.
    
    Args:
        slug1: First slug
        slug2: Second slug
        ignore_case: Ignore case differences
    
    Returns:
        True if slugs are equal
    
    Example:
        >>> compare_slugs("Hello-World", "hello-world")
        True
        >>> compare_slugs("hello-world", "hello_world")
        False
    """
    if ignore_case:
        return slug1.lower() == slug2.lower()
    return slug1 == slug2


def get_slug_words(slug: str, separator: str = '-') -> List[str]:
    """
    Extract words from a slug.
    
    Args:
        slug: Slug to parse
        separator: Separator used in slug
    
    Returns:
        List of words
    
    Example:
        >>> get_slug_words("hello-world-2024")
        ['hello', 'world', '2024']
    """
    return [w for w in slug.split(separator) if w]


def count_slug_words(slug: str, separator: str = '-') -> int:
    """
    Count the number of words in a slug.
    
    Args:
        slug: Slug to count
        separator: Separator used in slug
    
    Returns:
        Number of words
    
    Example:
        >>> count_slug_words("hello-world")
        2
    """
    return len(get_slug_words(slug, separator))


# ============================================================================
# Custom Slug Generator
# ============================================================================

class SlugGenerator:
    """
    Configurable slug generator with persistent settings.
    
    Example:
        >>> gen = SlugGenerator(separator='_', max_length=50)
        >>> gen.generate("Hello World!")
        'hello_world'
        >>> gen.generate_unique("Hello World!", ['hello_world'])
        'hello_world_2'
    """
    
    def __init__(
        self,
        separator: str = '-',
        lowercase: bool = True,
        max_length: Optional[int] = None,
        word_boundary: bool = True,
        custom_map: Optional[Dict[str, str]] = None,
        strip_common_words: bool = False,
        common_words: Optional[List[str]] = None
    ):
        """Initialize slug generator with custom settings."""
        self.separator = separator
        self.lowercase = lowercase
        self.max_length = max_length
        self.word_boundary = word_boundary
        self.custom_map = custom_map or {}
        self.strip_common_words = strip_common_words
        self.common_words = common_words
        self._existing: List[str] = []
    
    def generate(self, text: str) -> str:
        """Generate a slug with current settings."""
        return generate_slug(
            text,
            separator=self.separator,
            lowercase=self.lowercase,
            max_length=self.max_length,
            word_boundary=self.word_boundary,
            custom_map=self.custom_map,
            strip_common_words=self.strip_common_words,
            common_words=self.common_words
        )
    
    def generate_unique(self, text: str, existing: Optional[List[str]] = None) -> str:
        """Generate a unique slug."""
        existing = existing or self._existing
        slug = generate_unique_slug(
            text,
            existing=existing,
            separator=self.separator,
            lowercase=self.lowercase,
            max_length=self.max_length
        )
        self._existing.append(slug)
        return slug
    
    def generate_batch(self, texts: List[str], ensure_unique: bool = True) -> List[str]:
        """Generate slugs for multiple texts."""
        return generate_slug_batch(
            texts,
            separator=self.separator,
            lowercase=self.lowercase,
            max_length=self.max_length,
            ensure_unique=ensure_unique
        )
    
    def reset(self) -> None:
        """Reset the list of existing slugs."""
        self._existing = []


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    print("AllToolkit - Slug Utilities Demo")
    print("=" * 40)
    
    # Basic slug generation
    print("\n[Basic Slugs]")
    print(f"'Hello World!' → {generate_slug('Hello World!')}")
    print(f"'Héllo Wörld!' → {generate_slug('Héllo Wörld!')}")
    print(f"'Привет Мир' → {generate_slug('Привет Мир')}")
    print(f"'Γειά σου Κόσμε' → {generate_slug('Γειά σου Κόσμε')}")
    
    # Custom separator
    print("\n[Custom Separator]")
    print(f"'Hello World' with '_' → {generate_slug('Hello World', separator='_')}")
    
    # Max length
    print("\n[Max Length]")
    print(f"'This is a very long title' (max=15) → {generate_slug('This is a very long title', max_length=15)}")
    
    # Unique slugs
    print("\n[Unique Slugs]")
    existing = ['hello-world', 'hello-world-2']
    print(f"'Hello World' (existing: {existing}) → {generate_unique_slug('Hello World', existing)}")
    
    # Date slug
    print("\n[Date Slug]")
    print(f"'My Blog Post' with date → {generate_date_slug('My Blog Post', '2024-01-15')}")
    
    # Hierarchical slug
    print("\n[Hierarchical Slug]")
    print(f"['Tech', 'Python', 'Tutorial'] → {generate_hierarchical_slug(['Tech', 'Python', 'Tutorial'])}")
    
    # Batch generation
    print("\n[Batch Generation]")
    texts = ['First Post', 'First Post', 'Second Post']
    print(f"Input: {texts}")
    print(f"Output: {generate_slug_batch(texts)}")
    
    # Using SlugGenerator class
    print("\n[SlugGenerator Class]")
    gen = SlugGenerator(separator='_', max_length=20)
    print(f"'Hello Beautiful World!' → {gen.generate('Hello Beautiful World!')}")
    
    # Validation
    print("\n[Validation]")
    print(f"'hello-world' is valid: {is_valid_slug('hello-world')}")
    print(f"'hello world' is valid: {is_valid_slug('hello world')}")
    
    # Slug to text
    print("\n[Slug to Text]")
    print(f"'hello-world-2024' → '{slug_to_text('hello-world-2024')}'")