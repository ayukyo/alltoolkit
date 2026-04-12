"""
AllToolkit - Python Emoji Utilities

A zero-dependency, production-ready emoji utility module.
Supports emoji extraction, counting, conversion, analysis, and manipulation.

Author: AllToolkit
License: MIT
"""

import re
import unicodedata
from typing import List, Dict, Tuple, Optional, Set, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import Counter


# Emoji Unicode ranges (comprehensive coverage)
EMOJI_RANGES = [
    (0x1F600, 0x1F64F),  # Emoticons
    (0x1F300, 0x1F5FF),  # Misc Symbols and Pictographs
    (0x1F680, 0x1F6FF),  # Transport and Map
    (0x1F1E0, 0x1F1FF),  # Regional Indicators (flags)
    (0x2600, 0x26FF),    # Misc Symbols
    (0x2700, 0x27BF),    # Dingbats
    (0xFE00, 0xFE0F),    # Variation Selectors
    (0x1F900, 0x1F9FF),  # Supplemental Symbols and Pictographs
    (0x1F004, 0x1F004),  # Mahjong Tile
    (0x1F0CF, 0x1F0CF),  # Playing Card
    (0x1F170, 0x1F171),  # Negative Squared A/B
    (0x1F17E, 0x1F17F),  # Negative Squared O/P
    (0x1F18E, 0x1F18E),  # Negative Squared AB
    (0x1F191, 0x1F19A),  # Squared Latin Abbreviations
    (0x1F201, 0x1F251),  # Enclosed Ideographics
    (0x1F300, 0x1F9FF),  # Extended coverage
    (0x200D, 0x200D),    # Zero Width Joiner (for complex emojis)
    (0x20E3, 0x20E3),    # Combining Enclosing Keycap
    (0x231A, 0x231B),    # Watch, Hourglass
    (0x2328, 0x2328),    # Keyboard
    (0x23CF, 0x23CF),    # Eject Symbol
    (0x23E9, 0x23F3),    # Various Symbols
    (0x23F8, 0x23FA),    # Media Symbols
    (0x25AA, 0x25AB),    # Squares
    (0x25B6, 0x25B6),    # Play Button
    (0x25C0, 0x25C0),    # Reverse Button
    (0x25FB, 0x25FE),    # Squares
    (0x2614, 0x2615),    # Umbrella, Hot Beverage
    (0x2648, 0x2653),    # Zodiac
    (0x267F, 0x267F),    # Wheelchair
    (0x2693, 0x2693),    # Anchor
    (0x26A1, 0x26A1),    # High Voltage
    (0x26AA, 0x26AB),    # Circles
    (0x26BD, 0x26BE),    # Soccer, Baseball
    (0x26C4, 0x26C5),    # Snowman, Sun
    (0x26CE, 0x26CE),    # Ophiuchus
    (0x26D4, 0x26D4),    # No Entry
    (0x26EA, 0x26EA),    # Church
    (0x26F2, 0x26F3),    # Fountain, Golf
    (0x26F5, 0x26F5),    # Sailboat
    (0x26FA, 0x26FA),    # Tent
    (0x26FD, 0x26FD),    # Fuel Pump
    (0x2702, 0x2702),    # Scissors
    (0x2705, 0x2705),    # Check Mark
    (0x2708, 0x270D),    # Various Symbols
    (0x270F, 0x270F),    # Pencil
    (0x2712, 0x2712),    # Black Nib
    (0x2714, 0x2714),    # Check Mark
    (0x2716, 0x2716),    # X Mark
    (0x271D, 0x271D),    # Cross
    (0x2721, 0x2721),    # Star of David
    (0x2728, 0x2728),    # Sparkles
    (0x2733, 0x2734),    # Eight Spoked Asterisk
    (0x2744, 0x2744),    # Snowflake
    (0x2747, 0x2747),    # Sparkle
    (0x274C, 0x274C),    # Cross Mark
    (0x274E, 0x274E),    # Cross Mark Button
    (0x2753, 0x2755),    # Question Marks
    (0x2757, 0x2757),    # Exclamation Mark
    (0x2763, 0x2764),    # Heart Exclamation, Red Heart
    (0x2795, 0x2797),    # Plus, Minus, Divide
    (0x27A1, 0x27A1),    # Right Arrow
    (0x27B0, 0x27B0),    # Curly Loop
    (0x27BF, 0x27BF),    # Double Curly Loop
    (0x2934, 0x2935),    # Arrows
    (0x2B05, 0x2B07),    # Arrows
    (0x2B1B, 0x2B1C),    # Squares
    (0x2B50, 0x2B50),    # Star
    (0x2B55, 0x2B55),    # Circle
    (0x3030, 0x3030),    # Wavy Dash
    (0x303D, 0x303D),    # Part Alternation Mark
    (0x3297, 0x3297),    # Circled Ideograph Cong
    (0x3299, 0x3299),    # Circled Ideograph Secret
]


class EmojiCategory(Enum):
    """Emoji categories based on Unicode CLDR."""
    SMILEY = "smiley"
    PERSON = "person"
    ANIMAL = "animal"
    FOOD = "food"
    TRAVEL = "travel"
    ACTIVITY = "activity"
    OBJECT = "object"
    SYMBOL = "symbol"
    FLAG = "flag"
    NATURE = "nature"
    UNKNOWN = "unknown"


# Category keywords for basic classification
CATEGORY_KEYWORDS = {
    EmojiCategory.SMILEY: ['face', 'smile', 'laugh', 'cry', 'angry', 'sad', 'happy', 'emotion', 'expression'],
    EmojiCategory.PERSON: ['person', 'man', 'woman', 'child', 'baby', 'hand', 'body', 'gesture'],
    EmojiCategory.ANIMAL: ['animal', 'dog', 'cat', 'bird', 'fish', 'insect', 'mammal', 'wild'],
    EmojiCategory.FOOD: ['food', 'drink', 'fruit', 'vegetable', 'meal', 'snack', 'sweet'],
    EmojiCategory.TRAVEL: ['travel', 'place', 'building', 'transport', 'vehicle', 'map', 'location'],
    EmojiCategory.ACTIVITY: ['activity', 'sport', 'game', 'hobby', 'event', 'celebration'],
    EmojiCategory.OBJECT: ['object', 'tool', 'device', 'clothing', 'household', 'office'],
    EmojiCategory.SYMBOL: ['symbol', 'sign', 'arrow', 'shape', 'math', 'currency', 'zodiac'],
    EmojiCategory.FLAG: ['flag', 'country', 'national'],
    EmojiCategory.NATURE: ['nature', 'plant', 'flower', 'tree', 'weather', 'sky', 'celestial'],
}


@dataclass
class EmojiInfo:
    """Information about a single emoji."""
    char: str
    unicode: str
    name: str
    category: EmojiCategory
    skin_tone: Optional[str] = None
    is_variant: bool = False
    codepoints: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'char': self.char,
            'unicode': self.unicode,
            'name': self.name,
            'category': self.category.value,
            'skin_tone': self.skin_tone,
            'is_variant': self.is_variant,
            'codepoints': self.codepoints,
        }


@dataclass
class EmojiAnalysis:
    """Analysis result for text containing emojis."""
    text: str
    total_emojis: int
    unique_emojis: int
    emojis: List[str]
    emoji_info: List[EmojiInfo]
    emoji_counts: Dict[str, int]
    categories: Dict[str, int]
    emoji_density: float  # percentage of text that is emoji
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'text': self.text,
            'total_emojis': self.total_emojis,
            'unique_emojis': self.unique_emojis,
            'emojis': self.emojis,
            'emoji_counts': self.emoji_counts,
            'categories': self.categories,
            'emoji_density': self.emoji_density,
        }


class EmojiUtils:
    """
    Comprehensive emoji utility class.
    
    Provides methods for extracting, analyzing, converting, and manipulating
    emojis in text. All methods are zero-dependency and use only Python
    standard library.
    """
    
    def __init__(self):
        """Initialize emoji utilities with compiled regex pattern."""
        self._pattern = self._build_emoji_pattern()
        self._skin_tones = {
            '\U0001F3FB': 'light',
            '\U0001F3FC': 'medium_light',
            '\U0001F3FD': 'medium',
            '\U0001F3FE': 'medium_dark',
            '\U0001F3FF': 'dark',
        }
    
    def _build_emoji_pattern(self):
        """Build regex pattern for matching emojis."""
        # Build character class from Unicode ranges
        chars = []
        for start, end in EMOJI_RANGES:
            if start == end:
                chars.append(chr(start))
            else:
                chars.append(f'{chr(start)}-{chr(end)}')
        
        # Create character class pattern
        char_class = ''.join(chars)
        # Match emoji base character optionally followed by modifiers
        # Modifiers: ZWJ, variation selector, combining enclosing keycap, skin tones
        pattern = f'[{char_class}](?:[\\u200D\\uFE0F\\u20E3\\u1F3FB-\\u1F3FF][{char_class}])*'
        return re.compile(pattern)
    
    def extract_emojis(self, text: str) -> List[str]:
        """
        Extract all emojis from text.
        
        Args:
            text: Input text string
            
        Returns:
            List of emoji characters found in text
            
        Example:
            >>> utils = EmojiUtils()
            >>> utils.extract_emojis("Hello 👋 World 🌍!")
            ['👋', '🌍']
        """
        if not text:
            return []
        return self._pattern.findall(text)
    
    def count_emojis(self, text: str) -> int:
        """
        Count total number of emojis in text.
        
        Args:
            text: Input text string
            
        Returns:
            Count of emojis
            
        Example:
            >>> utils = EmojiUtils()
            >>> utils.count_emojis("😀😃😄")
            3
        """
        return len(self.extract_emojis(text))
    
    def get_unique_emojis(self, text: str) -> Set[str]:
        """
        Get unique emojis from text.
        
        Args:
            text: Input text string
            
        Returns:
            Set of unique emoji characters
            
        Example:
            >>> utils = EmojiUtils()
            >>> utils.get_unique_emojis("😀😃😀😄😃")
            {'😀', '😃', '😄'}
        """
        return set(self.extract_emojis(text))
    
    def get_emoji_counts(self, text: str) -> Dict[str, int]:
        """
        Get count of each unique emoji in text.
        
        Args:
            text: Input text string
            
        Returns:
            Dictionary mapping emoji to count
            
        Example:
            >>> utils = EmojiUtils()
            >>> utils.get_emoji_counts("😀😃😀")
            {'😀': 2, '😃': 1}
        """
        emojis = self.extract_emojis(text)
        return dict(Counter(emojis))
    
    def remove_emojis(self, text: str, strip_whitespace: bool = True) -> str:
        """
        Remove all emojis from text.
        
        Args:
            text: Input text string
            strip_whitespace: Whether to strip extra whitespace after removal
            
        Returns:
            Text with emojis removed
            
        Example:
            >>> utils = EmojiUtils()
            >>> utils.remove_emojis("Hello 👋 World 🌍!")
            'Hello World!'
        """
        if not text:
            return text
        result = self._pattern.sub('', text)
        if strip_whitespace:
            # Remove extra spaces but preserve punctuation spacing
            result = re.sub(r'\s+', ' ', result).strip()
            # Fix space before punctuation
            result = re.sub(r'\s+([!?.:,;])', r'\1', result)
        return result
    
    def replace_emojis(self, text: str, replacement: str = '') -> str:
        """
        Replace all emojis with a specified string.
        
        Args:
            text: Input text string
            replacement: String to replace emojis with
            
        Returns:
            Text with emojis replaced
            
        Example:
            >>> utils = EmojiUtils()
            >>> utils.replace_emojis("Hello 👋", "[emoji]")
            'Hello [emoji]'
        """
        if not text:
            return text
        return self._pattern.sub(replacement, text)
    
    def has_emoji(self, text: str) -> bool:
        """
        Check if text contains any emoji.
        
        Args:
            text: Input text string
            
        Returns:
            True if text contains at least one emoji
            
        Example:
            >>> utils = EmojiUtils()
            >>> utils.has_emoji("Hello 👋")
            True
            >>> utils.has_emoji("Hello")
            False
        """
        return bool(self._pattern.search(text))
    
    def is_emoji(self, char: str) -> bool:
        """
        Check if a character or string is an emoji.
        
        Args:
            char: Character or string to check
            
        Returns:
            True if the entire string is an emoji
            
        Example:
            >>> utils = EmojiUtils()
            >>> utils.is_emoji("😀")
            True
            >>> utils.is_emoji("Hello")
            False
        """
        if not char:
            return False
        return self._pattern.fullmatch(char) is not None
    
    def get_emoji_info(self, emoji: str) -> Optional[EmojiInfo]:
        """
        Get detailed information about an emoji.
        
        Args:
            emoji: Emoji character
            
        Returns:
            EmojiInfo object or None if not an emoji
            
        Example:
            >>> utils = EmojiUtils()
            >>> info = utils.get_emoji_info("😀")
            >>> info.name
            'GRINNING FACE'
        """
        if not self.is_emoji(emoji):
            return None
        
        # Get Unicode codepoints
        codepoints = [f'U+{ord(c):04X}' for c in emoji]
        unicode_str = '-'.join(codepoints)
        
        # Get name from Unicode database
        try:
            name = unicodedata.name(emoji[0], 'UNKNOWN')
        except ValueError:
            name = 'UNKNOWN'
        
        # Determine category
        category = self._categorize_emoji(emoji, name)
        
        # Check for skin tone
        skin_tone = None
        for tone_char, tone_name in self._skin_tones.items():
            if tone_char in emoji:
                skin_tone = tone_name
                break
        
        # Check for variation selector
        is_variant = '\uFE0F' in emoji or '\u200D' in emoji
        
        return EmojiInfo(
            char=emoji,
            unicode=unicode_str,
            name=name,
            category=category,
            skin_tone=skin_tone,
            is_variant=is_variant,
            codepoints=codepoints,
        )
    
    def _categorize_emoji(self, emoji: str, name: str) -> EmojiCategory:
        """Categorize an emoji based on its name."""
        name_lower = name.lower()
        
        for category, keywords in CATEGORY_KEYWORDS.items():
            if any(kw in name_lower for kw in keywords):
                return category
        
        return EmojiCategory.UNKNOWN
    
    def analyze(self, text: str) -> EmojiAnalysis:
        """
        Perform comprehensive analysis of emojis in text.
        
        Args:
            text: Input text string
            
        Returns:
            EmojiAnalysis object with detailed statistics
            
        Example:
            >>> utils = EmojiUtils()
            >>> analysis = utils.analyze("Hello 👋 World 🌍! 👋")
            >>> analysis.total_emojis
            3
            >>> analysis.unique_emojis
            2
        """
        emojis = self.extract_emojis(text)
        emoji_counts = self.get_emoji_counts(text)
        unique_emojis = set(emojis)
        
        # Get info for each unique emoji
        emoji_info = []
        categories: Dict[str, int] = {}
        
        for emoji in unique_emojis:
            info = self.get_emoji_info(emoji)
            if info:
                emoji_info.append(info)
                cat = info.category.value
                categories[cat] = categories.get(cat, 0) + emoji_counts[emoji]
        
        # Calculate density
        total_chars = len(text) if text else 1
        emoji_density = (len(emojis) / total_chars) * 100
        
        return EmojiAnalysis(
            text=text,
            total_emojis=len(emojis),
            unique_emojis=len(unique_emojis),
            emojis=emojis,
            emoji_info=emoji_info,
            emoji_counts=emoji_counts,
            categories=categories,
            emoji_density=round(emoji_density, 2),
        )
    
    def to_unicode_escape(self, emoji: str) -> str:
        """
        Convert emoji to Unicode escape sequence.
        
        Args:
            emoji: Emoji character
            
        Returns:
            Unicode escape string
            
        Example:
            >>> utils = EmojiUtils()
            >>> utils.to_unicode_escape("😀")
            '\\\\U0001F600'
        """
        return '-'.join(f'U+{ord(c):04X}' for c in emoji)
    
    def from_unicode_escape(self, unicode_str: str) -> str:
        """
        Convert Unicode escape sequence to emoji.
        
        Args:
            unicode_str: Unicode escape string (e.g., "U+1F600" or "1F600")
            
        Returns:
            Emoji character
            
        Example:
            >>> utils = EmojiUtils()
            >>> utils.from_unicode_escape("U+1F600")
            '😀'
        """
        # Handle various formats
        unicode_str = unicode_str.upper().replace('U+', '').replace('\\U', '')
        codepoints = re.findall(r'[0-9A-F]+', unicode_str)
        
        try:
            return ''.join(chr(int(cp, 16)) for cp in codepoints)
        except (ValueError, OverflowError):
            raise ValueError(f"Invalid Unicode escape: {unicode_str}")
    
    def get_skin_tone_variants(self, emoji: str) -> Dict[str, str]:
        """
        Get all skin tone variants of an emoji (if applicable).
        
        Args:
            emoji: Base emoji character
            
        Returns:
            Dictionary mapping skin tone name to variant emoji
            
        Example:
            >>> utils = EmojiUtils()
            >>> variants = utils.get_skin_tone_variants("👋")
            >>> 'medium' in variants
            True
        """
        variants = {}
        
        # Check if emoji can have skin tone (contains hand, person, etc.)
        info = self.get_emoji_info(emoji)
        if not info:
            return variants
        
        # Base emoji without skin tone
        base_emoji = emoji
        for tone_char in self._skin_tones.keys():
            base_emoji = base_emoji.replace(tone_char, '')
        
        # Generate variants by appending skin tone modifier to base emoji
        for tone_char, tone_name in self._skin_tones.items():
            # Insert skin tone after the base emoji character
            variant = base_emoji + tone_char
            if variant != emoji:
                variants[tone_name] = variant
        
        return variants
    
    def strip_skin_tone(self, emoji: str) -> str:
        """
        Remove skin tone modifier from emoji.
        
        Args:
            emoji: Emoji with potential skin tone
            
        Returns:
            Emoji without skin tone modifier
            
        Example:
            >>> utils = EmojiUtils()
            >>> utils.strip_skin_tone("👋🏽")
            '👋'
        """
        result = emoji
        for tone_char in self._skin_tones.keys():
            result = result.replace(tone_char, '')
        return result
    
    def emoji_to_text(self, emoji: str, use_shortcodes: bool = False) -> str:
        """
        Convert emoji to text description.
        
        Args:
            emoji: Emoji character
            use_shortcodes: Whether to use shortcode format (e.g., :smile:)
            
        Returns:
            Text description of emoji
            
        Example:
            >>> utils = EmojiUtils()
            >>> utils.emoji_to_text("😀")
            'grinning face'
        """
        info = self.get_emoji_info(emoji)
        if not info:
            return emoji
        
        name = info.name.lower().replace('_', ' ')
        
        if use_shortcodes:
            # Simple shortcode conversion
            shortcode = name.replace(' ', '_')
            return f':{shortcode}:'
        
        return name
    
    def text_to_emoji(self, text: str) -> Optional[str]:
        """
        Try to convert text description to emoji (basic support).
        
        Args:
            text: Text description or shortcode
            
        Returns:
            Emoji character or None if not found
            
        Example:
            >>> utils = EmojiUtils()
            >>> utils.text_to_emoji("smile")
            '😀'
        """
        # Common mappings (extensible)
        mappings = {
            'smile': '😀',
            'laugh': '😂',
            'love': '❤️',
            'heart': '❤️',
            'thumbs up': '👍',
            'thumbsup': '👍',
            'wave': '👋',
            'hello': '👋',
            'world': '🌍',
            'earth': '🌍',
            'fire': '🔥',
            'star': '⭐',
            'check': '✅',
            'cross': '❌',
            'warning': '⚠️',
            'party': '🎉',
            'celebration': '🎉',
        }
        
        text_lower = text.lower().strip(':')
        return mappings.get(text_lower)
    
    def filter_by_category(self, text: str, category: EmojiCategory) -> List[str]:
        """
        Filter emojis in text by category.
        
        Args:
            text: Input text string
            category: Emoji category to filter by
            
        Returns:
            List of emojis matching the category
            
        Example:
            >>> utils = EmojiUtils()
            >>> utils.filter_by_category("😀🐕🍎", EmojiCategory.SMILEY)
            ['😀']
        """
        emojis = self.extract_emojis(text)
        result = []
        
        for emoji in emojis:
            info = self.get_emoji_info(emoji)
            if info and info.category == category:
                result.append(emoji)
        
        return result
    
    def get_emoji_positions(self, text: str) -> List[Tuple[int, int, str]]:
        """
        Get positions of all emojis in text.
        
        Args:
            text: Input text string
            
        Returns:
            List of (start, end, emoji) tuples
            
        Example:
            >>> utils = EmojiUtils()
            >>> utils.get_emoji_positions("Hi 👋")
            [(3, 5, '👋')]
        """
        positions = []
        for match in self._pattern.finditer(text):
            positions.append((match.start(), match.end(), match.group()))
        return positions
    
    def reverse(self, text: str) -> str:
        """
        Reverse text while keeping emoji sequences intact.
        
        Args:
            text: Input text string
            
        Returns:
            Reversed text with emojis preserved
            
        Example:
            >>> utils = EmojiUtils()
            >>> utils.reverse("Hi 👋🌍")
            '🌍👋 iH'
        """
        if not text:
            return text
        
        # Extract emojis with positions
        positions = self.get_emoji_positions(text)
        
        # Build list of (is_emoji, content)
        parts = []
        last_end = 0
        
        for start, end, emoji in positions:
            if start > last_end:
                # Text before emoji - reverse it
                parts.append(('text', text[last_end:start][::-1]))
            parts.append(('emoji', emoji))
            last_end = end
        
        # Handle remaining text
        if last_end < len(text):
            parts.append(('text', text[last_end:][::-1]))
        
        # Reverse the order of parts and join
        return ''.join(content for _, content in reversed(parts))


# Module-level convenience functions
_default_utils = EmojiUtils()


def extract_emojis(text: str) -> List[str]:
    """Extract all emojis from text."""
    return _default_utils.extract_emojis(text)


def count_emojis(text: str) -> int:
    """Count total number of emojis in text."""
    return _default_utils.count_emojis(text)


def get_unique_emojis(text: str) -> Set[str]:
    """Get unique emojis from text."""
    return _default_utils.get_unique_emojis(text)


def get_emoji_counts(text: str) -> Dict[str, int]:
    """Get count of each unique emoji in text."""
    return _default_utils.get_emoji_counts(text)


def remove_emojis(text: str, strip_whitespace: bool = True) -> str:
    """Remove all emojis from text."""
    return _default_utils.remove_emojis(text, strip_whitespace)


def replace_emojis(text: str, replacement: str = '') -> str:
    """Replace all emojis with a specified string."""
    return _default_utils.replace_emojis(text, replacement)


def has_emoji(text: str) -> bool:
    """Check if text contains any emoji."""
    return _default_utils.has_emoji(text)


def is_emoji(char: str) -> bool:
    """Check if a character or string is an emoji."""
    return _default_utils.is_emoji(char)


def analyze(text: str) -> EmojiAnalysis:
    """Perform comprehensive analysis of emojis in text."""
    return _default_utils.analyze(text)


def to_unicode_escape(emoji: str) -> str:
    """Convert emoji to Unicode escape sequence."""
    return _default_utils.to_unicode_escape(emoji)


def from_unicode_escape(unicode_str: str) -> str:
    """Convert Unicode escape sequence to emoji."""
    return _default_utils.from_unicode_escape(unicode_str)


def strip_skin_tone(emoji: str) -> str:
    """Remove skin tone modifier from emoji."""
    return _default_utils.strip_skin_tone(emoji)


def emoji_to_text(emoji: str, use_shortcodes: bool = False) -> str:
    """Convert emoji to text description."""
    return _default_utils.emoji_to_text(emoji, use_shortcodes)


def text_to_emoji(text: str) -> Optional[str]:
    """Try to convert text description to emoji."""
    return _default_utils.text_to_emoji(text)


def filter_by_category(text: str, category: EmojiCategory) -> List[str]:
    """Filter emojis in text by category."""
    return _default_utils.filter_by_category(text, category)


def get_emoji_positions(text: str) -> List[Tuple[int, int, str]]:
    """Get positions of all emojis in text."""
    return _default_utils.get_emoji_positions(text)


def reverse(text: str) -> str:
    """Reverse text while keeping emoji sequences intact."""
    return _default_utils.reverse(text)


if __name__ == '__main__':
    # Quick demo
    utils = EmojiUtils()
    
    test_text = "Hello 👋 World 🌍! Today is great 🌟🎉 #happy 😀😃😄"
    
    print("=" * 60)
    print("Emoji Utils Demo")
    print("=" * 60)
    print(f"\nInput: {test_text}\n")
    
    print(f"Extracted: {utils.extract_emojis(test_text)}")
    print(f"Count: {utils.count_emojis(test_text)}")
    print(f"Unique: {utils.get_unique_emojis(test_text)}")
    print(f"Has emoji: {utils.has_emoji(test_text)}")
    print(f"Without emojis: {utils.remove_emojis(test_text)}")
    
    print("\n" + "=" * 60)
    print("Analysis")
    print("=" * 60)
    analysis = utils.analyze(test_text)
    print(f"Total: {analysis.total_emojis}")
    print(f"Unique: {analysis.unique_emojis}")
    print(f"Density: {analysis.emoji_density}%")
    print(f"Categories: {analysis.categories}")
    
    print("\n" + "=" * 60)
    print("Emoji Info")
    print("=" * 60)
    for emoji in ['😀', '👋', '🌍', '🎉']:
        info = utils.get_emoji_info(emoji)
        if info:
            print(f"{emoji}: {info.name} ({info.unicode}) - {info.category.value}")
