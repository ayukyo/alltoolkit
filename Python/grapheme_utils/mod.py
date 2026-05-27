"""
Grapheme Cluster Utilities
==========================

A pure Python implementation for handling Unicode grapheme clusters.
Correctly processes emoji, combining characters, and complex scripts.
Zero external dependencies.

A "grapheme cluster" is what users perceive as a single character.
For example, the family emoji "👨‍👩‍👧‍👦" is 7 code points but 1 grapheme.

Features:
- Count grapheme clusters (not code points)
- Split strings by grapheme clusters
- Slice strings by grapheme index
- Reverse strings by grapheme
- Detect combining characters
- Get grapheme cluster information

Author: AllToolkit
Date: 2026-05-27
"""

import unicodedata
from typing import List, Tuple, Optional, Iterator


# Unicode property categories
COMBINING_MARK_CATEGORIES = {
    'Mn',  # Mark, Nonspacing (e.g., combining accents)
    'Mc',  # Mark, Spacing Combining
    'Me',  # Mark, Enclosing
}

# Common combining characters
COMBINING_DIACRITICS = {
    '\u0300', '\u0301', '\u0302', '\u0303', '\u0304', '\u0305', '\u0306',
    '\u0307', '\u0308', '\u0309', '\u030A', '\u030B', '\u030C', '\u030D',
    '\u030E', '\u030F', '\u0310', '\u0311', '\u0312', '\u0313', '\u0314',
    '\u0315', '\u0316', '\u0317', '\u0318', '\u0319', '\u031A', '\u031B',
    '\u031C', '\u031D', '\u031E', '\u031F', '\u0320', '\u0321', '\u0322',
    '\u0323', '\u0324', '\u0325', '\u0326', '\u0327', '\u0328', '\u0329',
    '\u032A', '\u032B', '\u032C', '\u032D', '\u032E', '\u032F', '\u0330',
    '\u0331', '\u0332', '\u0333', '\u0334', '\u0335', '\u0336', '\u0337',
    '\u0338', '\u0339', '\u033A', '\u033B', '\u033C', '\u033D', '\u033E',
    '\u033F', '\u0340', '\u0341', '\u0342', '\u0343', '\u0344', '\u0345',
    '\u0346', '\u0347', '\u0348', '\u0349', '\u034A', '\u034B', '\u034C',
    '\u034D', '\u034E', '\u034F', '\u0350', '\u0351', '\u0352', '\u0353',
    '\u0354', '\u0355', '\u0356', '\u0357', '\u0358', '\u0359', '\u035A',
    '\u035B', '\u035C', '\u035D', '\u035E', '\u035F', '\u0360', '\u0361',
    '\u0362', '\u0363', '\u0364', '\u0365', '\u0366', '\u0367', '\u0368',
    '\u0369', '\u036A', '\u036B', '\u036C', '\u036D', '\u036E', '\u036F',
}

# Variation selectors (FE00-FE0F, E0100-E01EF)
VARIATION_SELECTOR_RANGES = [
    (0xFE00, 0xFE0F),  # Variation Selectors
    (0xE0100, 0xE01EF),  # Variation Selectors Supplement
]

# Zero-width joiner
ZWJ = '\u200D'

# Zero-width non-joiner
ZWNJ = '\u200C'

# Emoji modifiers (skin tone)
EMOJI_MODIFIERS = {
    '\U0001F3FB',  # Light Skin Tone
    '\U0001F3FC',  # Medium-Light Skin Tone
    '\U0001F3FD',  # Medium Skin Tone
    '\U0001F3FE',  # Medium-Dark Skin Tone
    '\U0001F3FF',  # Dark Skin Tone
}

# Regional indicator symbols (used for flag emoji)
REGIONAL_INDICATOR_START = 0x1F1E6  # 🇦
REGIONAL_INDICATOR_END = 0x1F1FF    # 🇿

# Emoji tag characters (for flag sequences like England, Scotland, Wales)
EMOJI_TAG_START = 0xE0020
EMOJI_TAG_END = 0xE007E

# Enclosing marks
ENCLOSING_MARKS = {
    '\u20DD',  # Combining Enclosing Circle
    '\u20DE',  # Combining Enclosing Square
    '\u20DF',  # Combining Enclosing Diamond
    '\u20E0',  # Combining Enclosing Circle Backslash
    '\u20E1',  # Combining Left Right Arrow Above
    '\u20E2',  # Combining Enclosing Screen
    '\u20E3',  # Combining Enclosing Keycap
    '\u20E4',  # Combining Enclosing Upward Pointing Triangle
}


def is_combining_mark(char: str) -> bool:
    """
    Check if a character is a combining mark.
    
    Args:
        char: A single Unicode code point
        
    Returns:
        True if the character is a combining mark
        
    Example:
        >>> is_combining_mark('\\u0301')  # Combining acute accent
        True
        >>> is_combining_mark('a')
        False
    """
    if len(char) == 0:
        return False
    
    # Check category
    category = unicodedata.category(char)
    if category in COMBINING_MARK_CATEGORIES:
        return True
    
    # Check known combining diacritics
    if char in COMBINING_DIACRITICS:
        return True
    
    return False


def is_variation_selector(char: str) -> bool:
    """
    Check if a character is a variation selector.
    
    Args:
        char: A single Unicode code point
        
    Returns:
        True if the character is a variation selector
    """
    if len(char) == 0:
        return False
    
    code_point = ord(char)
    for start, end in VARIATION_SELECTOR_RANGES:
        if start <= code_point <= end:
            return True
    return False


def is_regional_indicator(char: str) -> bool:
    """
    Check if a character is a regional indicator (used in flag emoji).
    
    Args:
        char: A single Unicode code point
        
    Returns:
        True if the character is a regional indicator
    """
    if len(char) == 0:
        return False
    
    code_point = ord(char)
    return REGIONAL_INDICATOR_START <= code_point <= REGIONAL_INDICATOR_END


def is_emoji_modifier(char: str) -> bool:
    """
    Check if a character is an emoji modifier (skin tone).
    
    Args:
        char: A single Unicode code point
        
    Returns:
        True if the character is an emoji modifier
    """
    return char in EMOJI_MODIFIERS


def is_emoji_tag(char: str) -> bool:
    """
    Check if a character is an emoji tag character.
    
    Args:
        char: A single Unicode code point
        
    Returns:
        True if the character is an emoji tag
    """
    if len(char) == 0:
        return False
    
    code_point = ord(char)
    return EMOJI_TAG_START <= code_point <= EMOJI_TAG_END


def is_zwj(char: str) -> bool:
    """Check if a character is a zero-width joiner."""
    return char == ZWJ


def is_zwnj(char: str) -> bool:
    """Check if a character is a zero-width non-joiner."""
    return char == ZWNJ


def _is_extend_char(char: str) -> bool:
    """
    Check if a character extends the previous grapheme cluster.
    
    According to UAX #29, a character extends a grapheme cluster if it is:
    - A combining mark
    - A variation selector
    - A zero-width joiner
    - A zero-width non-joiner
    - An emoji modifier
    - An emoji tag character
    - An enclosing mark
    """
    return (
        is_combining_mark(char) or
        is_variation_selector(char) or
        is_zwj(char) or
        is_emoji_modifier(char) or
        is_emoji_tag(char) or
        char in ENCLOSING_MARKS
    )


def _is_extended_pictographic(char: str) -> bool:
    """
    Check if a character is an extended pictographic (emoji).
    
    This is a simplified check. Full implementation requires Unicode data.
    """
    code_point = ord(char)
    
    # Emoji ranges (simplified)
    emoji_ranges = [
        (0x1F600, 0x1F64F),  # Emoticons
        (0x1F300, 0x1F5FF),  # Misc Symbols and Pictographs
        (0x1F680, 0x1F6FF),  # Transport and Map
        (0x1F1E0, 0x1F1FF),  # Flags (regional indicators)
        (0x2600, 0x26FF),    # Misc symbols
        (0x2700, 0x27BF),    # Dingbats
        (0x1F900, 0x1F9FF),  # Supplemental Symbols and Pictographs
        (0x1FA00, 0x1FA6F),  # Chess Symbols
        (0x1FA70, 0x1FAFF),  # Symbols and Pictographs Extended-A
        (0x231A, 0x231B),    # Watch, Hourglass
        (0x23E9, 0x23F3),    # Various
        (0x23F8, 0x23FA),    # Media controls
        (0x25AA, 0x25AB),    # Squares
        (0x25B6, 0x25B6),    # Play button
        (0x25C0, 0x25C0),    # Reverse button
        (0x25FB, 0x25FE),    # Squares
        (0x2614, 0x2615),    # Umbrella, hot beverage
        (0x2648, 0x2653),    # Zodiac
        (0x267F, 0x267F),    # Wheelchair
        (0x2693, 0x2693),    # Anchor
        (0x26A1, 0x26A1),    # High voltage
        (0x26AA, 0x26AB),    # Circles
        (0x26BD, 0x26BE),    # Sports
        (0x26C4, 0x26C5),    # Snowman, sun
        (0x26CE, 0x26CE),    # Ophiuchus
        (0x26D4, 0x26D4),    # No entry
        (0x26EA, 0x26EA),    # Church
        (0x26F2, 0x26F3),    # Fountain, golf
        (0x26F5, 0x26F5),    # Sailboat
        (0x26FA, 0x26FA),    # Tent
        (0x26FD, 0x26FD),    # Fuel pump
        (0x2702, 0x2702),    # Scissors
        (0x2705, 0x2705),    # Check mark
        (0x2708, 0x270D),    # Various
        (0x270F, 0x270F),    # Pencil
        (0x2712, 0x2712),    # Pen
        (0x2714, 0x2714),    # Check mark
        (0x2716, 0x2716),    # X mark
        (0x271D, 0x271D),    # Cross
        (0x2721, 0x2721),    # Star of David
        (0x2728, 0x2728),    # Sparkles
        (0x2733, 0x2734),    # Eight-pointed star
        (0x2744, 0x2744),    # Snowflake
        (0x2747, 0x2747),    # Sparkle
        (0x274C, 0x274C),    # Cross mark
        (0x274E, 0x274E),    # Cross mark
        (0x2753, 0x2755),    # Question marks
        (0x2757, 0x2757),    # Exclamation mark
        (0x2763, 0x2764),    # Heart exclamation, heavy heart
        (0x2795, 0x2797),    # Math
        (0x27A1, 0x27A1),    # Right arrow
        (0x27B0, 0x27B0),    # Curly loop
        (0x27BF, 0x27BF),    # Double curly loop
        (0x2934, 0x2935),    # Arrows
        (0x2B05, 0x2B07),    # Arrows
        (0x2B1B, 0x2B1C),    # Squares
        (0x2B50, 0x2B50),    # Star
        (0x2B55, 0x2B55),    # Circle
        (0x3030, 0x3030),    # Wavy dash
        (0x303D, 0x303D),    # Part alternation mark
        (0x3297, 0x3297),    # Circled ideograph congratulation
        (0x3299, 0x3299),    # Circled ideograph secret
        (0x00A9, 0x00A9),    # Copyright
        (0x00AE, 0x00AE),    # Registered
        (0x203C, 0x203C),    # Double exclamation mark
        (0x2049, 0x2049),    # Exclamation question mark
        (0x2122, 0x2122),    # Trade mark
        (0x2139, 0x2139),    # Information source
        (0x2194, 0x2199),    # Arrows
        (0x21A9, 0x21AA),    # Arrows
        (0x2299, 0x2299),    # Circled operator
        (0x231A, 0x231B),    # Watch, hourglass
        (0x2328, 0x2328),    # Keyboard
        (0x23CF, 0x23CF),    # Eject
        (0x23E9, 0x23F3),    # Media
        (0x23F8, 0x23FA),    # Media controls
    ]
    
    for start, end in emoji_ranges:
        if start <= code_point <= end:
            return True
    
    return False


def graphemes(text: str) -> Iterator[str]:
    """
    Iterate over grapheme clusters in a string.
    
    A grapheme cluster is a user-perceived character, which may consist
    of multiple Unicode code points.
    
    Args:
        text: The input string
        
    Yields:
        Each grapheme cluster as a string
        
    Example:
        >>> list(graphemes("café"))
        ['c', 'a', 'f', 'é']
        >>> list(graphemes("👨‍👩‍👧‍👦"))
        ['👨‍👩‍👧‍👦']
    """
    if not text:
        return
    
    cluster = ""
    prev_was_zwj = False
    regional_indicator_count = 0
    
    for char in text:
        if cluster:
            # Check if this character extends the current cluster
            if prev_was_zwj:
                # ZWJ always joins with the next character
                cluster += char
                prev_was_zwj = False
                regional_indicator_count = 0
            elif is_zwj(char):
                # Zero-width joiner starts a ZWJ sequence
                cluster += char
                prev_was_zwj = True
            elif _is_extend_char(char):
                # This character extends the current cluster
                cluster += char
                regional_indicator_count = 0
            elif is_regional_indicator(char):
                # Regional indicator handling
                if is_regional_indicator(cluster[-1]) and regional_indicator_count < 2:
                    # Second regional indicator in a pair forms a flag
                    cluster += char
                    regional_indicator_count += 1
                else:
                    # Start new cluster (previous was a complete flag)
                    yield cluster
                    cluster = char
                    prev_was_zwj = False
                    regional_indicator_count = 1
            else:
                # Start a new cluster
                yield cluster
                cluster = char
                prev_was_zwj = False
                regional_indicator_count = 0
        else:
            cluster = char
            prev_was_zwj = False
            if is_regional_indicator(char):
                regional_indicator_count = 1
            else:
                regional_indicator_count = 0
    
    if cluster:
        yield cluster


def grapheme_count(text: str) -> int:
    """
    Count the number of grapheme clusters in a string.
    
    This returns the number of user-perceived characters, not code points.
    
    Args:
        text: The input string
        
    Returns:
        The number of grapheme clusters
        
    Example:
        >>> grapheme_count("café")
        4
        >>> grapheme_count("👨‍👩‍👧‍👦")
        1
        >>> grapheme_count("नमस्ते")  # Hindi "namaste"
        4
    """
    return sum(1 for _ in graphemes(text))


def grapheme_split(text: str) -> List[str]:
    """
    Split a string into a list of grapheme clusters.
    
    Args:
        text: The input string
        
    Returns:
        List of grapheme clusters
        
    Example:
        >>> grapheme_split("hello")
        ['h', 'e', 'l', 'l', 'o']
        >>> grapheme_split("👨‍👩‍👧‍👦👋")
        ['👨‍👩‍👧‍👦', '👋']
    """
    return list(graphemes(text))


def grapheme_slice(text: str, start: int, end: Optional[int] = None) -> str:
    """
    Slice a string by grapheme indices.
    
    Args:
        text: The input string
        start: Starting grapheme index (0-based)
        end: Ending grapheme index (exclusive). If None, slices to the end.
        
    Returns:
        The sliced substring
        
    Example:
        >>> grapheme_slice("café", 0, 2)
        'ca'
        >>> grapheme_slice("👨‍👩‍👧‍👦hello", 0, 1)
        '👨‍👩‍👧‍👦'
        >>> grapheme_slice("👨‍👩‍👧‍👦hello", 1, 3)
        'he'
    """
    clusters = grapheme_split(text)
    
    if end is None:
        return ''.join(clusters[start:])
    else:
        return ''.join(clusters[start:end])


def grapheme_reverse(text: str) -> str:
    """
    Reverse a string by grapheme clusters.
    
    This correctly handles combining characters and emoji sequences.
    
    Args:
        text: The input string
        
    Returns:
        The reversed string
        
    Example:
        >>> grapheme_reverse("hello")
        'olleh'
        >>> grapheme_reverse("café")
        'éfac'
        >>> grapheme_reverse("👋👨‍👩‍👧‍👦")
        '👨‍👩‍👧‍👦👋'
    """
    clusters = grapheme_split(text)
    return ''.join(reversed(clusters))


def grapheme_at(text: str, index: int) -> str:
    """
    Get the grapheme cluster at a specific index.
    
    Args:
        text: The input string
        index: The grapheme index (0-based)
        
    Returns:
        The grapheme cluster at the given index
        
    Raises:
        IndexError: If the index is out of range
        
    Example:
        >>> grapheme_at("hello", 0)
        'h'
        >>> grapheme_at("👨‍👩‍👧‍👦👋", 0)
        '👨‍👩‍👧‍👦'
    """
    clusters = grapheme_split(text)
    return clusters[index]


def grapheme_index(text: str, grapheme: str) -> int:
    """
    Find the index of a grapheme cluster in a string.
    
    Args:
        text: The input string
        grapheme: The grapheme cluster to find
        
    Returns:
        The index of the first occurrence
        
    Raises:
        ValueError: If the grapheme is not found
        
    Example:
        >>> grapheme_index("hello", "l")
        2
    """
    clusters = grapheme_split(text)
    return clusters.index(grapheme)


def grapheme_find(text: str, substring: str) -> int:
    """
    Find the grapheme index of a substring.
    
    Args:
        text: The input string
        substring: The substring to find
        
    Returns:
        The grapheme index of the first occurrence, or -1 if not found
        
    Example:
        >>> grapheme_find("hello world", "world")
        6
        >>> grapheme_find("👨‍👩‍👧‍👦hello", "he")
        1
    """
    clusters = grapheme_split(text)
    sub_clusters = grapheme_split(substring)
    
    if not sub_clusters:
        return 0
    
    for i in range(len(clusters) - len(sub_clusters) + 1):
        if clusters[i:i + len(sub_clusters)] == sub_clusters:
            return i
    
    return -1


def grapheme_contains(text: str, substring: str) -> bool:
    """
    Check if a string contains a substring (by grapheme clusters).
    
    Args:
        text: The input string
        substring: The substring to check
        
    Returns:
        True if the substring is found
        
    Example:
        >>> grapheme_contains("hello", "ell")
        True
    """
    return grapheme_find(text, substring) >= 0


def grapheme_replace(text: str, old: str, new: str, count: int = -1) -> str:
    """
    Replace occurrences of a substring (by grapheme clusters).
    
    Args:
        text: The input string
        old: The substring to replace
        new: The replacement string
        count: Maximum number of replacements (-1 for all)
        
    Returns:
        The string with replacements
        
    Example:
        >>> grapheme_replace("hello hello", "ll", "pp")
        'heppo heppo'
    """
    if count == 0 or not old:
        return text
    
    clusters = grapheme_split(text)
    old_clusters = grapheme_split(old)
    
    if not old_clusters:
        return text
    
    result = []
    i = 0
    replacements = 0
    
    while i < len(clusters):
        if count != -1 and replacements >= count:
            result.extend(clusters[i:])
            break
        
        if clusters[i:i + len(old_clusters)] == old_clusters:
            result.append(new)
            i += len(old_clusters)
            replacements += 1
        else:
            result.append(clusters[i])
            i += 1
    
    return ''.join(result)


def grapheme_info(text: str) -> List[dict]:
    """
    Get detailed information about each grapheme cluster.
    
    Args:
        text: The input string
        
    Returns:
        List of dictionaries with grapheme information
        
    Example:
        >>> info = grapheme_info("é")
        >>> info[0]['grapheme']
        'é'
        >>> info[0]['code_points']
        [233]
    """
    result = []
    
    for cluster in graphemes(text):
        info = {
            'grapheme': cluster,
            'code_points': [ord(c) for c in cluster],
            'length_code_points': len(cluster),
            'length_bytes': len(cluster.encode('utf-8')),
            'is_emoji': any(_is_extended_pictographic(c) for c in cluster),
            'has_combining': any(is_combining_mark(c) for c in cluster),
            'has_zwj': ZWJ in cluster,
        }
        result.append(info)
    
    return result


def code_points_to_graphemes(code_points: List[int]) -> str:
    """
    Convert a list of Unicode code points to a string.
    
    Args:
        code_points: List of Unicode code points
        
    Returns:
        The resulting string
        
    Example:
        >>> code_points_to_graphemes([72, 101, 108, 108, 111])
        'Hello'
    """
    return ''.join(chr(cp) for cp in code_points)


def graphemes_to_code_points(text: str) -> List[int]:
    """
    Convert a string to a list of Unicode code points.
    
    Args:
        text: The input string
        
    Returns:
        List of Unicode code points
        
    Example:
        >>> graphemes_to_code_points("Hello")
        [72, 101, 108, 108, 111]
    """
    return [ord(c) for c in text]


def normalize_graphemes(text: str, form: str = 'NFC') -> str:
    """
    Normalize Unicode graphemes to a canonical form.
    
    Args:
        text: The input string
        form: Normalization form ('NFC', 'NFD', 'NFKC', 'NFKD')
        
    Returns:
        The normalized string
        
    Example:
        >>> # 'é' can be single code point or 'e' + combining acute
        >>> normalize_graphemes('é', 'NFC') == normalize_graphemes('é', 'NFC')
        True
    """
    return unicodedata.normalize(form, text)


def grapheme_equal(text1: str, text2: str, normalize: bool = True) -> bool:
    """
    Compare two strings for grapheme equivalence.
    
    Args:
        text1: First string
        text2: Second string
        normalize: Whether to normalize before comparing
        
    Returns:
        True if the strings are grapheme-equivalent
        
    Example:
        >>> # 'é' (single) vs 'e' + combining acute accent
        >>> grapheme_equal('é', 'é')
        True
    """
    if normalize:
        text1 = normalize_graphemes(text1)
        text2 = normalize_graphemes(text2)
    
    return grapheme_split(text1) == grapheme_split(text2)


def grapheme_length_in_bytes(text: str, encoding: str = 'utf-8') -> List[int]:
    """
    Get the byte length of each grapheme cluster.
    
    Args:
        text: The input string
        encoding: The encoding to use (default: utf-8)
        
    Returns:
        List of byte lengths for each grapheme
        
    Example:
        >>> grapheme_length_in_bytes("Hello")
        [1, 1, 1, 1, 1]
        >>> grapheme_length_in_bytes("中文")
        [3, 3]
    """
    return [len(cluster.encode(encoding)) for cluster in graphemes(text)]


def truncate_graphemes(text: str, max_length: int, ellipsis: str = "...") -> str:
    """
    Truncate a string to a maximum number of grapheme clusters.
    
    Args:
        text: The input string
        max_length: Maximum number of grapheme clusters
        ellipsis: String to append if truncated
        
    Returns:
        The truncated string
        
    Example:
        >>> truncate_graphemes("Hello World", 5)
        'Hello...'
        >>> truncate_graphemes("👨‍👩‍👧‍👦 Family", 2)
        '👨‍👩‍👧‍👦 ...'
    """
    clusters = grapheme_split(text)
    
    if len(clusters) <= max_length:
        return text
    
    return ''.join(clusters[:max_length]) + ellipsis


def pad_graphemes(text: str, length: int, char: str = ' ', 
                  side: str = 'right') -> str:
    """
    Pad a string to a specific grapheme length.
    
    Args:
        text: The input string
        length: Target grapheme length
        char: Padding character (default: space)
        side: 'left', 'right', or 'center'
        
    Returns:
        The padded string
        
    Example:
        >>> pad_graphemes("Hi", 5)
        'Hi   '
        >>> pad_graphemes("Hi", 5, side='center')
        '  Hi  '
        >>> pad_graphemes("Hi", 5, side='left')
        '   Hi'
    """
    clusters = grapheme_split(text)
    current_length = len(clusters)
    
    if current_length >= length:
        return text
    
    padding_needed = length - current_length
    
    if side == 'right':
        return text + char * padding_needed
    elif side == 'left':
        return char * padding_needed + text
    elif side == 'center':
        left_pad = padding_needed // 2
        right_pad = padding_needed - left_pad
        return char * left_pad + text + char * right_pad
    else:
        raise ValueError(f"Invalid side: {side}. Use 'left', 'right', or 'center'.")


# Convenience aliases
def count(text: str) -> int:
    """Alias for grapheme_count()."""
    return grapheme_count(text)


def split(text: str) -> List[str]:
    """Alias for grapheme_split()."""
    return grapheme_split(text)


def slice_(text: str, start: int, end: Optional[int] = None) -> str:
    """Alias for grapheme_slice()."""
    return grapheme_slice(text, start, end)


def reverse(text: str) -> str:
    """Alias for grapheme_reverse()."""
    return grapheme_reverse(text)


if __name__ == "__main__":
    # Quick demo
    print("Grapheme Cluster Utilities Demo")
    print("=" * 50)
    
    # Example with combining characters
    text1 = "café"  # 'é' might be single code point or 'e' + combining accent
    print(f"\nText: {text1}")
    print(f"Code points: {len(text1)}")
    print(f"Graphemes: {grapheme_count(text1)}")
    print(f"Split: {grapheme_split(text1)}")
    
    # Example with emoji
    text2 = "👨‍👩‍👧‍👦"  # Family emoji (ZWJ sequence)
    print(f"\nText: {text2}")
    print(f"Code points: {len(text2)}")
    print(f"Graphemes: {grapheme_count(text2)}")
    print(f"Split: {grapheme_split(text2)}")
    print(f"Info: {grapheme_info(text2)}")
    
    # Example with complex script (Devanagari)
    text3 = "नमस्ते"  # Hindi "namaste"
    print(f"\nText: {text3}")
    print(f"Code points: {len(text3)}")
    print(f"Graphemes: {grapheme_count(text3)}")
    print(f"Split: {grapheme_split(text3)}")
    
    # Example with flag emoji
    text4 = "🇺🇸🇬🇧"  # US and UK flags
    print(f"\nText: {text4}")
    print(f"Code points: {len(text4)}")
    print(f"Graphemes: {grapheme_count(text4)}")
    print(f"Split: {grapheme_split(text4)}")
    
    # Truncation example
    text5 = "Hello 👨‍👩‍👧‍👦 World"
    print(f"\nOriginal: {text5}")
    print(f"Truncated (5): {truncate_graphemes(text5, 5)}")
    print(f"Reversed: {grapheme_reverse(text5)}")
    
    print("\n" + "=" * 50)
    print("Demo complete!")