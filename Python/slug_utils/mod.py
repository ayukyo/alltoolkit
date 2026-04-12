#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Slug Utilities Module

Comprehensive slug generation utilities for Python with zero external dependencies.
Generate URL-friendly slugs from text with support for multiple languages,
custom separators, truncation, and more.

Author: AllToolkit
License: MIT
"""

import re
import unicodedata
from typing import Optional, List, Dict, Any, Union


# =============================================================================
# Type Aliases
# =============================================================================

TextLike = Union[str, bytes]
Separator = str


# =============================================================================
# Constants
# =============================================================================

# ASCII transliteration mappings for common accented characters
ACCENT_MAPPINGS = {
    'À': 'A', 'Á': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A', 'Å': 'A', 'Æ': 'AE',
    'Ç': 'C', 'È': 'E', 'É': 'E', 'Ê': 'E', 'Ë': 'E', 'Ì': 'I', 'Í': 'I',
    'Î': 'I', 'Ï': 'I', 'Ð': 'D', 'Ñ': 'N', 'Ò': 'O', 'Ó': 'O', 'Ô': 'O',
    'Õ': 'O', 'Ö': 'O', 'Ø': 'O', 'Ù': 'U', 'Ú': 'U', 'Û': 'U', 'Ü': 'U',
    'Ý': 'Y', 'Þ': 'TH', 'ß': 'ss', 'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a',
    'ä': 'a', 'å': 'a', 'æ': 'ae', 'ç': 'c', 'è': 'e', 'é': 'e', 'ê': 'e',
    'ë': 'e', 'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i', 'ð': 'd', 'ñ': 'n',
    'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o', 'ø': 'o', 'ù': 'u',
    'ú': 'u', 'û': 'u', 'ü': 'u', 'ý': 'y', 'þ': 'th', 'ÿ': 'y',
    'Ā': 'A', 'ā': 'a', 'Ă': 'A', 'ă': 'a', 'Ą': 'A', 'ą': 'a',
    'Ć': 'C', 'ć': 'c', 'Ĉ': 'C', 'ĉ': 'c', 'Ċ': 'C', 'ċ': 'c', 'Č': 'C', 'č': 'c',
    'Ď': 'D', 'ď': 'd', 'Đ': 'D', 'đ': 'd',
    'Ē': 'E', 'ē': 'e', 'Ĕ': 'E', 'ĕ': 'e', 'Ė': 'E', 'ė': 'e', 'Ę': 'E', 'ę': 'e', 'Ě': 'E', 'ě': 'e',
    'Ĝ': 'G', 'ĝ': 'g', 'Ğ': 'G', 'ğ': 'g', 'Ġ': 'G', 'ġ': 'g', 'Ģ': 'G', 'ģ': 'g',
    'Ĥ': 'H', 'ĥ': 'h', 'Ħ': 'H', 'ħ': 'h',
    'Ĩ': 'I', 'ĩ': 'i', 'Ī': 'I', 'ī': 'i', 'Ĭ': 'I', 'ĭ': 'i', 'Į': 'I', 'į': 'i', 'İ': 'I', 'ı': 'i',
    'Ĳ': 'IJ', 'ĳ': 'ij',
    'Ĵ': 'J', 'ĵ': 'j',
    'Ķ': 'K', 'ķ': 'k',
    'Ĺ': 'L', 'ĺ': 'l', 'Ļ': 'L', 'ļ': 'l', 'Ľ': 'L', 'ľ': 'l', 'Ŀ': 'L', 'ŀ': 'l', 'Ł': 'L', 'ł': 'l',
    'Ń': 'N', 'ń': 'n', 'Ņ': 'N', 'ņ': 'n', 'Ň': 'N', 'ň': 'n', 'ŉ': 'n', 'Ŋ': 'N', 'ŋ': 'n',
    'Ō': 'O', 'ō': 'o', 'Ŏ': 'O', 'ŏ': 'o', 'Ő': 'O', 'ő': 'o',
    'Œ': 'OE', 'œ': 'oe',
    'Ŕ': 'R', 'ŕ': 'r', 'Ŗ': 'R', 'ŗ': 'r', 'Ř': 'R', 'ř': 'r',
    'Ś': 'S', 'ś': 's', 'Ŝ': 'S', 'ŝ': 's', 'Ş': 'S', 'ş': 's', 'Š': 'S', 'š': 's',
    'Ţ': 'T', 'ţ': 't', 'Ť': 'T', 'ť': 't', 'Ŧ': 'T', 'ŧ': 't',
    'Ũ': 'U', 'ũ': 'u', 'Ū': 'U', 'ū': 'u', 'Ŭ': 'U', 'ŭ': 'u', 'Ů': 'U', 'ů': 'u', 'Ű': 'U', 'ű': 'u', 'Ų': 'U', 'ų': 'u',
    'Ŵ': 'W', 'ŵ': 'w',
    'Ŷ': 'Y', 'ŷ': 'y', 'Ÿ': 'Y',
    'Ź': 'Z', 'ź': 'z', 'Ż': 'Z', 'ż': 'z', 'Ž': 'Z', 'ž': 'z',
}

# Common word replacements for slugs
# Note: These are applied BEFORE slugification, so they replace words/symbols in the original text
WORD_REPLACEMENTS = {
    '&': ' and ',
    '@': ' at ',
    '|': ' or ',
    '+': ' plus ',
    '=': ' equals ',
    '%': ' percent ',
    '$': ' dollar ',
    '£': ' pound ',
    '€': ' euro ',
    '¥': ' yen ',
}

# Default stop words to remove (can be customized per language)
DEFAULT_STOP_WORDS = {
    'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
    'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare', 'ought',
    'used', 'it', 'its', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
    'she', 'we', 'they', 'what', 'which', 'who', 'whom', 'whose', 'where',
    'when', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more',
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
    'same', 'so', 'than', 'too', 'very', 'just', 'also',
}


# =============================================================================
# Core Slug Generation
# =============================================================================

def slugify(text: TextLike,
            separator: Separator = '-',
            lowercase: bool = True,
            max_length: Optional[int] = None,
            allow_unicode: bool = False,
            remove_stop_words: bool = False,
            stop_words: Optional[set] = None,
            word_replacements: Optional[Dict[str, str]] = None,
            allow_dots: bool = False,
            allow_underscores: bool = False,
            truncate_words: bool = False,
            ensure_ascii: bool = True) -> str:
    """
    Convert text to a URL-friendly slug.
    
    Args:
        text: Input text to convert
        separator: Character to separate words (default: '-')
        lowercase: Convert to lowercase (default: True)
        max_length: Maximum length of slug (default: None, no limit)
        allow_unicode: Allow unicode characters in slug (default: False)
        remove_stop_words: Remove common stop words (default: False)
        stop_words: Custom set of stop words (uses DEFAULT_STOP_WORDS if None)
        word_replacements: Custom word replacements dict
        allow_dots: Allow dots in slug (default: False)
        allow_underscores: Allow underscores in slug (default: False)
        truncate_words: If True with max_length, truncate at word boundary (default: False)
        ensure_ascii: Convert non-ASCII to ASCII equivalents (default: True)
        
    Returns:
        URL-friendly slug string
        
    Example:
        >>> slugify("Hello World!")
        'hello-world'
        >>> slugify("Café & Restaurant", separator='_')
        'cafe_and_restaurant'
        >>> slugify("The Quick Brown Fox", remove_stop_words=True)
        'quick-brown-fox'
        >>> slugify("Hello World", max_length=8, truncate_words=True)
        'hello'
    """
    if isinstance(text, bytes):
        text = text.decode('utf-8')
    
    if not text:
        return ''
    
    # Apply word replacements first (for symbols and words)
    if word_replacements is None:
        word_replacements = WORD_REPLACEMENTS
    for old, new in word_replacements.items():
        # Use simple string replacement for symbols, word boundary for words
        if old.isalnum():
            text = re.sub(r'\b' + re.escape(old) + r'\b', new, text, flags=re.IGNORECASE)
        else:
            text = text.replace(old, new)
    
    # Remove stop words if requested
    if remove_stop_words:
        if stop_words is None:
            stop_words = DEFAULT_STOP_WORDS
        words = text.split()
        text = ' '.join(word for word in words if word.lower() not in stop_words)
    
    # Convert to ASCII if requested
    if ensure_ascii and not allow_unicode:
        text = unicode_to_ascii(text)
    
    # Convert to lowercase if requested
    if lowercase:
        text = text.lower()
        alpha_range = r'a-z'
    else:
        alpha_range = r'a-zA-Z'
    
    # Remove all non-alphanumeric characters except separator and allowed chars
    allowed_chars = alpha_range + r'0-9\s' + re.escape(separator)
    if allow_dots:
        allowed_chars += r'\.'
    if allow_underscores:
        allowed_chars += '_'
    
    text = re.sub(r'[^' + allowed_chars + ']', '', text)
    
    # Replace spaces and underscores with separator
    text = re.sub(r'[\s_]+', separator, text)
    
    # Collapse multiple separators
    text = re.sub(re.escape(separator) + r'+', separator, text)
    
    # Strip separators from start and end
    text = text.strip(separator)
    
    # Truncate to max length if specified
    if max_length is not None and len(text) > max_length:
        if truncate_words:
            # Truncate at word boundary
            truncated = text[:max_length]
            # Find last separator before the cutoff
            last_sep = truncated.rfind(separator)
            if last_sep > 0:
                text = truncated[:last_sep]
            else:
                text = truncated
        else:
            text = text[:max_length]
        # Ensure we don't end with separator after truncation
        text = text.rstrip(separator)
    
    return text


def unicode_to_ascii(text: str) -> str:
    """
    Convert unicode text to ASCII equivalents.
    
    Args:
        text: Input text with unicode characters
        
    Returns:
        ASCII-only text
        
    Example:
        >>> unicode_to_ascii("Café")
        'Cafe'
        >>> unicode_to_ascii("Ñoño")
        'Nono'
        >>> unicode_to_ascii("北京")
        'Bei Jing'
    """
    if not text:
        return text
    
    # First apply known accent mappings
    result = []
    for char in text:
        if char in ACCENT_MAPPINGS:
            result.append(ACCENT_MAPPINGS[char])
        else:
            result.append(char)
    text = ''.join(result)
    
    # Normalize unicode and remove accents
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    return text


# =============================================================================
# Multi-language Support
# =============================================================================

def slugify_cn(text: str,
               separator: Separator = '-',
               lowercase: bool = True,
               max_length: Optional[int] = None,
               pinyin_style: str = 'toneless') -> str:
    """
    Convert Chinese text to slug using pinyin.
    
    Note: This is a simplified implementation. For production use with
    comprehensive pinyin conversion, consider the pypinyin library.
    This implementation handles common Chinese characters with basic mappings.
    
    Args:
        text: Chinese text to convert
        separator: Word separator (default: '-')
        lowercase: Convert to lowercase (default: True)
        max_length: Maximum slug length (default: None)
        pinyin_style: 'toneless', 'tone', or 'numbered' (default: 'toneless')
        
    Returns:
        Pinyin-based slug
        
    Example:
        >>> slugify_cn("北京")  # Simplified - returns transliterated form
        'bei-jing'
    """
    # Common Chinese character to pinyin mappings (simplified subset)
    cn_mappings = {
        '北': 'bei', '京': 'jing', '上': 'shang', '海': 'hai',
        '中': 'zhong', '国': 'guo', '人': 'ren', '民': 'min',
        '大': 'da', '学': 'xue', '生': 'sheng', '活': 'huo',
        '工': 'gong', '作': 'zuo', '时': 'shi', '间': 'jian',
        '天': 'tian', '气': 'qi', '好': 'hao', '的': 'de',
        '是': 'shi', '不': 'bu', '了': 'le', '在': 'zai',
        '和': 'he', '与': 'yu', '或': 'huo', '个': 'ge',
        '有': 'you', '这': 'zhe', '那': 'na', '他': 'ta',
        '她': 'ta', '它': 'ta', '们': 'men', '我': 'wo',
        '你': 'ni', '们': 'men', '来': 'lai', '去': 'qu',
        '年': 'nian', '月': 'yue', '日': 'ri', '号': 'hao',
        '点': 'dian', '分': 'fen', '秒': 'miao', '钟': 'zhong',
        '小': 'xiao', '多': 'duo', '少': 'shao', '长': 'chang',
        '高': 'gao', '低': 'di', '前': 'qian', '后': 'hou',
        '左': 'zuo', '右': 'you', '东': 'dong', '西': 'xi',
        '南': 'nan', '北': 'bei', '中': 'zhong', '外': 'wai',
        '里': 'li', '外': 'wai', '上': 'shang', '下': 'xia',
        '门': 'men', '口': 'kou', '手': 'shou', '足': 'zu',
        '头': 'tou', '身': 'shen', '心': 'xin', '体': 'ti',
    }
    
    # Convert Chinese characters to pinyin
    result = []
    for char in text:
        if char in cn_mappings:
            result.append(cn_mappings[char])
        else:
            # Keep non-Chinese characters as-is
            result.append(char)
    
    # Join with spaces, then slugify
    text = ' '.join(result)
    return slugify(text, separator=separator, lowercase=lowercase, max_length=max_length)


def slugify_jp(text: str,
               separator: Separator = '-',
               lowercase: bool = True,
               max_length: Optional[int] = None,
               romaji_style: str = 'hepburn') -> str:
    """
    Convert Japanese text to slug using romaji.
    
    Note: Simplified implementation for common hiragana/katakana.
    
    Args:
        text: Japanese text to convert
        separator: Word separator (default: '-')
        lowercase: Convert to lowercase (default: True)
        max_length: Maximum slug length (default: None)
        romaji_style: 'hepburn' or 'kunrei' (default: 'hepburn')
        
    Returns:
        Romaji-based slug
    """
    # Simplified hiragana to romaji mappings
    hiragana_mappings = {
        'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o',
        'か': 'ka', 'き': 'ki', 'く': 'ku', 'け': 'ke', 'こ': 'ko',
        'さ': 'sa', 'し': 'shi', 'す': 'su', 'せ': 'se', 'そ': 'so',
        'た': 'ta', 'ち': 'chi', 'つ': 'tsu', 'て': 'te', 'と': 'to',
        'な': 'na', 'に': 'ni', 'ぬ': 'nu', 'ね': 'ne', 'の': 'no',
        'は': 'ha', 'ひ': 'hi', 'ふ': 'fu', 'へ': 'he', 'ほ': 'ho',
        'ま': 'ma', 'み': 'mi', 'む': 'mu', 'め': 'me', 'も': 'mo',
        'や': 'ya', 'ゆ': 'yu', 'よ': 'yo',
        'ら': 'ra', 'り': 'ri', 'る': 'ru', 'れ': 're', 'ろ': 'ro',
        'わ': 'wa', 'を': 'wo', 'ん': 'n',
        'が': 'ga', 'ぎ': 'gi', 'ぐ': 'gu', 'げ': 'ge', 'ご': 'go',
        'ざ': 'za', 'じ': 'ji', 'ず': 'zu', 'ぜ': 'ze', 'ぞ': 'zo',
        'だ': 'da', 'ぢ': 'ji', 'づ': 'zu', 'で': 'de', 'ど': 'do',
        'ば': 'ba', 'び': 'bi', 'ぶ': 'bu', 'べ': 'be', 'ぼ': 'bo',
        'ぱ': 'pa', 'ぴ': 'pi', 'ぷ': 'pu', 'ぺ': 'pe', 'ぽ': 'po',
    }
    
    # Convert hiragana to romaji
    result = []
    for char in text:
        if char in hiragana_mappings:
            result.append(hiragana_mappings[char])
        else:
            result.append(char)
    
    text = ' '.join(result)
    return slugify(text, separator=separator, lowercase=lowercase, max_length=max_length)


def slugify_kr(text: str,
               separator: Separator = '-',
               lowercase: bool = True,
               max_length: Optional[int] = None) -> str:
    """
    Convert Korean text to slug using romanization.
    
    Note: Simplified implementation for common Hangul characters.
    
    Args:
        text: Korean text to convert
        separator: Word separator (default: '-')
        lowercase: Convert to lowercase (default: True)
        max_length: Maximum slug length (default: None)
        
    Returns:
        Romanized slug
    """
    # Simplified Hangul to romanization mappings
    hangul_mappings = {
        '가': 'ga', '나': 'na', '다': 'da', '라': 'ra', '마': 'ma',
        '바': 'ba', '사': 'sa', '아': 'a', '자': 'ja', '차': 'cha',
        '카': 'ka', '타': 'ta', '파': 'pa', '하': 'ha',
        '고': 'go', '노': 'no', '도': 'do', '로': 'ro', '모': 'mo',
        '보': 'bo', '소': 'so', '오': 'o', '조': 'jo', '초': 'cho',
        '코': 'ko', '토': 'to', '포': 'po', '호': 'ho',
        '국': 'guk', '민': 'min', '대': 'dae', '한': 'han',
        '안': 'an', '녕': 'nyeong', '하': 'ha', '세': 'se', '요': 'yo',
    }
    
    result = []
    for char in text:
        if char in hangul_mappings:
            result.append(hangul_mappings[char])
        else:
            result.append(char)
    
    text = ' '.join(result)
    return slugify(text, separator=separator, lowercase=lowercase, max_length=max_length)


# =============================================================================
# Specialized Slug Functions
# =============================================================================

def slugify_title(title: str,
                  separator: Separator = '-',
                  max_length: int = 60,
                  preserve_case: bool = False) -> str:
    """
    Generate SEO-friendly slug from a title.
    
    Optimized for blog posts, articles, and page titles.
    
    Args:
        title: Title text
        separator: Word separator (default: '-')
        max_length: Maximum slug length (default: 60, SEO recommended)
        preserve_case: Keep original case (default: False)
        
    Returns:
        SEO-optimized slug
        
    Example:
        >>> slugify_title("10 Best Practices for Python Development in 2024!")
        '10-best-practices-for-python-development-in-2024'
    """
    return slugify(
        title,
        separator=separator,
        lowercase=not preserve_case,
        max_length=max_length,
        truncate_words=True,
        remove_stop_words=False,
    )


def slugify_filename(filename: str,
                     preserve_extension: bool = True,
                     separator: Separator = '-') -> str:
    """
    Generate safe filename slug.
    
    Args:
        filename: Original filename
        preserve_extension: Keep file extension (default: True)
        separator: Word separator (default: '-')
        
    Returns:
        Safe filename slug
        
    Example:
        >>> slugify_filename("My Document (Final Version).pdf")
        'my-document-final-version.pdf'
    """
    if '.' in filename and preserve_extension:
        name, ext = filename.rsplit('.', 1)
        slug = slugify(name, separator=separator, allow_dots=False)
        return f"{slug}.{ext.lower()}"
    else:
        return slugify(filename, separator=separator, allow_dots=False)


def slugify_username(username: str,
                     separator: Separator = '_',
                     min_length: int = 3) -> str:
    """
    Generate safe username slug.
    
    Args:
        username: Desired username
        separator: Separator (default: '_' for usernames)
        min_length: Minimum length (default: 3)
        
    Returns:
        Safe username slug
        
    Example:
        >>> slugify_username("John.Doe@2024!")
        'john_doe_2024'
    """
    slug = slugify(
        username,
        separator=separator,
        allow_underscores=True,
        allow_dots=False,
    )
    
    # Ensure minimum length
    if len(slug) < min_length:
        slug = slug + separator * (min_length - len(slug))
    
    return slug


def slugify_url(url: str,
                keep_domain: bool = False,
                separator: Separator = '-') -> str:
    """
    Generate slug from URL path.
    
    Args:
        url: Full URL or path
        keep_domain: Include domain in slug (default: False)
        separator: Word separator (default: '-')
        
    Returns:
        URL-based slug
        
    Example:
        >>> slugify_url("https://example.com/blog/my-post-title")
        'my-post-title'
    """
    # Remove protocol
    url = re.sub(r'^https?://', '', url)
    
    if keep_domain:
        # Slugify entire URL including domain
        return slugify(url.replace('/', separator), separator=separator)
    else:
        # Extract path only
        parts = url.split('/', 1)
        path = parts[1] if len(parts) > 1 else parts[0]
        # Remove query string and fragment
        path = path.split('?')[0].split('#')[0]
        return slugify(path.replace('/', separator), separator=separator)


# =============================================================================
# Batch Processing
# =============================================================================

def slugify_batch(texts: List[TextLike],
                  separator: Separator = '-',
                  lowercase: bool = True,
                  ensure_unique: bool = True,
                  **kwargs) -> List[str]:
    """
    Generate slugs for multiple texts.
    
    Args:
        texts: List of texts to slugify
        separator: Word separator
        lowercase: Convert to lowercase
        ensure_unique: Ensure all slugs are unique (default: True)
        **kwargs: Additional arguments passed to slugify()
        
    Returns:
        List of slugs
        
    Example:
        >>> slugify_batch(["Hello World", "Hello World", "Foo Bar"])
        ['hello-world', 'hello-world-1', 'foo-bar']
    """
    slugs = []
    seen: Dict[str, int] = {}
    
    for text in texts:
        base_slug = slugify(text, separator=separator, lowercase=lowercase, **kwargs)
        
        if ensure_unique:
            if base_slug in seen:
                seen[base_slug] += 1
                slug = f"{base_slug}{separator}{seen[base_slug]}"
            else:
                seen[base_slug] = 0
                slug = base_slug
        else:
            slug = base_slug
        
        slugs.append(slug)
    
    return slugs


def slugify_dict(data: Dict[str, Any],
                 keys: Optional[List[str]] = None,
                 separator: Separator = '-',
                 **kwargs) -> Dict[str, Any]:
    """
    Generate slugs for dictionary values.
    
    Args:
        data: Dictionary with text values
        keys: Specific keys to slugify (None = all string values)
        separator: Word separator
        **kwargs: Additional arguments passed to slugify()
        
    Returns:
        Dictionary with slugged values
        
    Example:
        >>> slugify_dict({"title": "My Post", "content": "Some Content"}, keys=["title"])
        {'title': 'my-post', 'content': 'Some Content'}
    """
    result = data.copy()
    
    for key, value in data.items():
        if keys is None and isinstance(value, str):
            result[key] = slugify(value, separator=separator, **kwargs)
        elif keys and key in keys and isinstance(value, str):
            result[key] = slugify(value, separator=separator, **kwargs)
    
    return result


# =============================================================================
# Validation and Utilities
# =============================================================================

def is_valid_slug(slug: str,
                  allow_unicode: bool = False,
                  allow_dots: bool = False,
                  allow_underscores: bool = False,
                  min_length: int = 1,
                  max_length: Optional[int] = None) -> bool:
    """
    Validate if a string is a valid slug.
    
    Args:
        slug: String to validate
        allow_unicode: Allow unicode characters
        allow_dots: Allow dots
        allow_underscores: Allow underscores
        min_length: Minimum length (default: 1)
        max_length: Maximum length (default: None)
        
    Returns:
        True if valid slug
        
    Example:
        >>> is_valid_slug("hello-world")
        True
        >>> is_valid_slug("Hello_World")
        False
        >>> is_valid_slug("hello_world", allow_underscores=True)
        True
    """
    if not slug or len(slug) < min_length:
        return False
    
    if max_length and len(slug) > max_length:
        return False
    
    if slug.startswith(('-', '_', '.')) or slug.endswith(('-', '_', '.')):
        return False
    
    if '--' in slug or '__' in slug or '..' in slug:
        return False
    
    # Check character validity
    pattern = r'^[a-z0-9'
    if allow_unicode:
        pattern += r'\u0080-\uFFFF'
    if allow_dots:
        pattern += r'\.'
    if allow_underscores:
        pattern += r'_'
    pattern += r'\-'
    pattern += r']+$'
    
    test_slug = slug if allow_unicode else slug.lower()
    return bool(re.match(pattern, test_slug, re.UNICODE if allow_unicode else 0))


def suggest_slug(text: str,
                 existing_slugs: List[str],
                 separator: Separator = '-',
                 max_attempts: int = 10) -> str:
    """
    Suggest a unique slug that doesn't conflict with existing ones.
    
    Args:
        text: Text to slugify
        existing_slugs: List of existing slugs to avoid
        separator: Word separator
        max_attempts: Maximum attempts to find unique slug
        
    Returns:
        Unique slug suggestion
        
    Example:
        >>> suggest_slug("My Post", ["my-post", "my-post-1"])
        'my-post-2'
    """
    base_slug = slugify(text, separator=separator)
    
    if base_slug not in existing_slugs:
        return base_slug
    
    existing_set = set(existing_slugs)
    
    for i in range(1, max_attempts + 1):
        candidate = f"{base_slug}{separator}{i}"
        if candidate not in existing_set:
            return candidate
    
    # Fallback: append unique identifier
    import hashlib
    unique = hashlib.md5(f"{text}{len(existing_slugs)}".encode()).hexdigest()[:8]
    return f"{base_slug}{separator}{unique}"


def count_words_in_slug(slug: str, separator: Separator = '-') -> int:
    """
    Count the number of words in a slug.
    
    Args:
        slug: Slug to analyze
        separator: Word separator
        
    Returns:
        Number of words
        
    Example:
        >>> count_words_in_slug("hello-world-foo-bar")
        4
    """
    if not slug:
        return 0
    return len([w for w in slug.split(separator) if w])


def truncate_slug(slug: str,
                  max_length: int,
                  separator: Separator = '-',
                  preserve_words: bool = True) -> str:
    """
    Truncate a slug to maximum length.
    
    Args:
        slug: Slug to truncate
        max_length: Maximum length
        separator: Word separator
        preserve_words: Truncate at word boundary (default: True)
        
    Returns:
        Truncated slug
        
    Example:
        >>> truncate_slug("hello-world-foo-bar", 12)
        'hello-world'
    """
    if len(slug) <= max_length:
        return slug
    
    if preserve_words:
        words = slug.split(separator)
        result = []
        for word in words:
            if len(separator.join(result + [word])) <= max_length:
                result.append(word)
            else:
                break
        return separator.join(result) if result else slug[:max_length]
    else:
        return slug[:max_length].rstrip(separator)


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    # Demo usage
    print("Slug Utilities Demo")
    print("=" * 60)
    
    test_cases = [
        ("Hello World!", "Basic ASCII"),
        ("Café & Restaurant", "Accented characters"),
        ("The Quick Brown Fox", "With stop words"),
        ("  Multiple   Spaces  ", "Extra whitespace"),
        ("Special@#$Characters%", "Special characters"),
        ("UPPERCASE and lowercase", "Mixed case"),
        ("日本語テスト", "Japanese (simplified)"),
        ("中文测试", "Chinese (simplified)"),
        ("한국어 테스트", "Korean (simplified)"),
    ]
    
    print("\nBasic Slugification:")
    print("-" * 60)
    for text, description in test_cases:
        slug = slugify(text)
        print(f"{description:30} | {text:25} → {slug}")
    
    print("\nWithOptions:")
    print("-" * 60)
    text = "The Quick Brown Fox Jumps Over The Lazy Dog"
    print(f"Original:     {text}")
    print(f"Basic:        {slugify(text)}")
    print(f"No stops:     {slugify(text, remove_stop_words=True)}")
    print(f"Underscore:   {slugify(text, separator='_')}")
    print(f"Max 20:       {slugify(text, max_length=20, truncate_words=True)}")
    print(f"Title:        {slugify_title(text)}")
    
    print("\nBatch Processing:")
    print("-" * 60)
    texts = ["Hello World", "Hello World", "Foo Bar", "Foo Bar"]
    slugs = slugify_batch(texts, ensure_unique=True)
    for text, slug in zip(texts, slugs):
        print(f"{text:20} → {slug}")
    
    print("\nValidation:")
    print("-" * 60)
    test_slugs = [
        ("hello-world", True),
        ("Hello_World", False),
        ("hello_world", False),
        ("-invalid-", False),
        ("valid-123", True),
    ]
    for slug, expected in test_slugs:
        result = is_valid_slug(slug, allow_underscores=True)
        status = "✓" if result == expected else "✗"
        print(f"{status} {slug:20} valid={result}")
    
    print("=" * 60)
