"""
AllToolkit - Python Text Utilities

A zero-dependency, production-ready text utility module.
Supports text formatting, analysis, transformation, cleaning, and statistics.

Author: AllToolkit
License: MIT
"""

import re
import string
import hashlib
from typing import List, Dict, Tuple, Optional, Set, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import Counter, defaultdict
import unicodedata


# =============================================================================
# Constants and Configuration
# =============================================================================

# Common punctuation sets
PUNCTUATION_ALL = string.punctuation
PUNCTUATION_BASIC = '.,!?;:'
PUNCTUATION_QUOTES = '"\'"\'""''«»‹›'
PUNCTUATION_BRACKETS = '()[]{}<>'

# Whitespace characters
WHITESPACE_ALL = ' \t\n\r\f\v'
WHITESPACE_VISIBLE = ' \t'

# Common stop words (English)
STOP_WORDS_EN = {
    'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
    'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare', 'ought',
    'used', 'it', 'its', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
    'she', 'we', 'they', 'what', 'which', 'who', 'whom', 'whose', 'where',
    'when', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more',
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
    'same', 'so', 'than', 'too', 'very', 'just', 'also', 'now', 'here',
    'there', 'then', 'once', 'if', 'unless', 'until', 'while', 'about',
    'against', 'between', 'into', 'through', 'during', 'before', 'after',
    'above', 'below', 'up', 'down', 'out', 'off', 'over', 'under', 'again',
    'further', 'am', 'being', 'because', 'any', 'my', 'your', 'his', 'her',
    'our', 'their', 'me', 'him', 'us', 'them', 'mine', 'yours', 'hers',
    'ours', 'theirs', 'myself', 'yourself', 'himself', 'herself', 'itself',
    'ourselves', 'themselves', 's', 't', 'd', 'll', 've', 're', 'm'
}

# Text case styles
class TextCase(Enum):
    """Text case styles."""
    LOWER = "lower"
    UPPER = "upper"
    TITLE = "title"
    SENTENCE = "sentence"
    CAMEL = "camel"
    PASCAL = "pascal"
    SNAKE = "snake"
    KEBAB = "kebab"
    CONSTANT = "constant"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class TextStats:
    """Text statistics."""
    char_count: int = 0
    char_count_no_spaces: int = 0
    word_count: int = 0
    sentence_count: int = 0
    paragraph_count: int = 0
    line_count: int = 0
    avg_word_length: float = 0.0
    avg_sentence_length: float = 0.0
    unique_words: int = 0
    readability_score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'char_count': self.char_count,
            'char_count_no_spaces': self.char_count_no_spaces,
            'word_count': self.word_count,
            'sentence_count': self.sentence_count,
            'paragraph_count': self.paragraph_count,
            'line_count': self.line_count,
            'avg_word_length': self.avg_word_length,
            'avg_sentence_length': self.avg_sentence_length,
            'unique_words': self.unique_words,
            'readability_score': self.readability_score,
        }


@dataclass
class WordInfo:
    """Word information."""
    word: str
    count: int = 1
    positions: List[int] = field(default_factory=list)
    is_stop_word: bool = False
    is_number: bool = False
    is_mixed_case: bool = False


@dataclass
class TextAnalysis:
    """Comprehensive text analysis result."""
    stats: TextStats
    word_frequencies: Dict[str, int]
    char_frequencies: Dict[str, int]
    ngrams: Dict[int, List[Tuple[str, ...]]]
    keywords: List[str]
    sentences: List[str]
    words: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'stats': self.stats.to_dict(),
            'word_frequencies': self.word_frequencies,
            'char_frequencies': self.char_frequencies,
            'ngrams': {k: [list(t) for t in v] for k, v in self.ngrams.items()},
            'keywords': self.keywords,
            'sentences': self.sentences,
            'words': self.words,
        }


# =============================================================================
# Main Utility Class
# =============================================================================

class TextUtils:
    """
    Comprehensive text utility class for formatting, analysis,
    transformation, cleaning, and statistics.
    """
    
    def __init__(self, stop_words: Optional[Set[str]] = None):
        """
        Initialize TextUtils.
        
        Args:
            stop_words: Custom stop words set. Defaults to English stop words.
        """
        self.stop_words = stop_words or STOP_WORDS_EN
    
    # -------------------------------------------------------------------------
    # Formatting
    # -------------------------------------------------------------------------
    
    def to_case(self, text: str, case: TextCase, separator: str = '_') -> str:
        """
        Convert text to specified case style.
        
        Args:
            text: Input text
            case: Target case style
            separator: Separator for compound words (default: '_')
        
        Returns:
            Formatted text
        """
        # Normalize: split into words
        words = self.split_into_words(text)
        words = [w.lower() for w in words if w]
        
        if case == TextCase.LOWER:
            return text.lower()
        elif case == TextCase.UPPER:
            return text.upper()
        elif case == TextCase.TITLE:
            return text.title()
        elif case == TextCase.SENTENCE:
            return self.to_sentence_case(text)
        elif case == TextCase.CAMEL:
            if not words:
                return ''
            return words[0] + ''.join(w.capitalize() for w in words[1:])
        elif case == TextCase.PASCAL:
            return ''.join(w.capitalize() for w in words)
        elif case == TextCase.SNAKE:
            return separator.join(words)
        elif case == TextCase.KEBAB:
            return '-'.join(words)
        elif case == TextCase.CONSTANT:
            return '_'.join(w.upper() for w in words)
        else:
            return text
    
    def to_sentence_case(self, text: str) -> str:
        """
        Convert text to sentence case (first letter capitalized, rest lower).
        
        Args:
            text: Input text
        
        Returns:
            Sentence case text
        """
        if not text:
            return text
        
        # Find first alphabetic character
        for i, char in enumerate(text):
            if char.isalpha():
                return text[:i] + char.upper() + text[i+1:].lower()
        return text.lower()
    
    def split_into_words(self, text: str) -> List[str]:
        """
        Split text into words, handling various separators.
        
        Args:
            text: Input text
        
        Returns:
            List of words
        """
        # Replace common separators with space
        normalized = re.sub(r'[-_\s/.\\]+', ' ', text)
        # Handle camelCase and PascalCase
        normalized = re.sub(r'([a-z])([A-Z])', r'\1 \2', normalized)
        # Split and filter
        return [w.strip() for w in normalized.split() if w.strip()]
    
    def pad(self, text: str, width: int, side: str = 'left', 
            char: str = ' ', truncate: bool = False) -> str:
        """
        Pad text to specified width.
        
        Args:
            text: Input text
            width: Target width
            side: 'left', 'right', 'both', or 'center'
            char: Padding character
            truncate: If True, truncate text if longer than width
        
        Returns:
            Padded text
        """
        if truncate and len(text) > width:
            if side == 'left':
                return text[-width:]
            elif side == 'right':
                return text[:width]
            else:
                # Center truncate
                half = width // 2
                return text[:half] + text[-(width - half):]
        
        if side == 'left':
            return text.rjust(width, char)
        elif side == 'right':
            return text.ljust(width, char)
        elif side == 'center':
            return text.center(width, char)
        elif side == 'both':
            padding = width - len(text)
            left = padding // 2
            right = padding - left
            return char * left + text + char * right
        else:
            return text
    
    def wrap(self, text: str, width: int = 80, 
             break_long_words: bool = True) -> List[str]:
        """
        Wrap text to specified width.
        
        Args:
            text: Input text
            width: Maximum line width
            break_long_words: If True, break words longer than width
        
        Returns:
            List of wrapped lines
        """
        words = text.split()
        if not words:
            return []
        
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_len = len(word)
            
            if current_length + word_len + len(current_line) <= width:
                current_line.append(word)
                current_length += word_len
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_len
                
                # Handle very long words
                if word_len > width and break_long_words:
                    while len(current_line[0]) > width:
                        lines.append(current_line[0][:width])
                        current_line[0] = current_line[0][width:]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    # -------------------------------------------------------------------------
    # Cleaning
    # -------------------------------------------------------------------------
    
    def clean(self, text: str, 
              remove_punctuation: bool = False,
              remove_digits: bool = False,
              remove_extra_spaces: bool = True,
              normalize_unicode: bool = True,
              strip: bool = True) -> str:
        """
        Clean text with various options.
        
        Args:
            text: Input text
            remove_punctuation: Remove punctuation marks
            remove_digits: Remove digits
            remove_extra_spaces: Normalize whitespace
            normalize_unicode: Normalize Unicode characters
            strip: Strip leading/trailing whitespace
        
        Returns:
            Cleaned text
        """
        # 优化：按操作顺序组织，减少不必要的字符串操作
        # Unicode normalization 应首先进行，因为它可能改变字符
        if normalize_unicode:
            result = unicodedata.normalize('NFKC', text)
        else:
            result = text
        
        # 优化：合并删除操作为单次遍历，避免多次字符串重建
        if remove_punctuation or remove_digits:
            # 构建需要删除的字符集合
            chars_to_remove = set()
            if remove_punctuation:
                chars_to_remove.update(PUNCTUATION_ALL)
            if remove_digits:
                chars_to_remove.update('0123456789')
            
            # 单次遍历删除所有目标字符
            result = ''.join(c for c in result if c not in chars_to_remove)
        
        # 空格处理
        if remove_extra_spaces:
            result = re.sub(r'\s+', ' ', result)
        
        if strip:
            result = result.strip()
        
        return result
    
    def remove_html(self, text: str) -> str:
        """
        Remove HTML tags from text.
        
        Args:
            text: Input text with HTML
        
        Returns:
            Text without HTML tags
        """
        # Remove HTML tags
        result = re.sub(r'<[^>]+>', '', text)
        # Decode common HTML entities
        html_entities = {
            '&nbsp;': ' ', '&amp;': '&', '&lt;': '<', '&gt;': '>',
            '&quot;': '"', '&#39;': "'", '&apos;': "'", '&ndash;': '–',
            '&mdash;': '—', '&lsquo;': ''', '&rsquo;': ''',
            '&ldquo;': '"', '&rdquo;': '"', '&hellip;': '…',
            '&copy;': '©', '&reg;': '®', '&trade;': '™',
        }
        for entity, char in html_entities.items():
            result = result.replace(entity, char)
        return result
    
    def remove_urls(self, text: str, replace_with: str = '') -> str:
        """
        Remove URLs from text.
        
        Args:
            text: Input text
            replace_with: Replacement string
        
        Returns:
            Text without URLs
        """
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        return re.sub(url_pattern, replace_with, text)
    
    def remove_emails(self, text: str, replace_with: str = '') -> str:
        """
        Remove email addresses from text.
        
        Args:
            text: Input text
            replace_with: Replacement string
        
        Returns:
            Text without email addresses
        """
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return re.sub(email_pattern, replace_with, text)
    
    def normalize_whitespace(self, text: str) -> str:
        """
        Normalize all whitespace to single spaces.
        
        Args:
            text: Input text
        
        Returns:
            Text with normalized whitespace
        """
        return ' '.join(text.split())
    
    def normalize_line_endings(self, text: str, style: str = 'unix') -> str:
        """
        Normalize line endings to specified style.
        
        Args:
            text: Input text
            style: 'unix' (\n), 'windows' (\r\n), or 'old_mac' (\r)
        
        Returns:
            Text with normalized line endings
        """
        # First normalize all to \n
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        if style == 'windows':
            return text.replace('\n', '\r\n')
        elif style == 'old_mac':
            return text.replace('\n', '\r')
        else:  # unix
            return text
    
    # -------------------------------------------------------------------------
    # Analysis
    # -------------------------------------------------------------------------
    
    def analyze(self, text: str, top_n: int = 10, 
                ngram_range: Tuple[int, int] = (1, 2)) -> TextAnalysis:
        """
        Perform comprehensive text analysis.
        
        Args:
            text: Input text
            top_n: Number of top items to return
            ngram_range: (min_n, max_n) for n-gram analysis
        
        Returns:
            TextAnalysis object with all analysis results
        """
        stats = self.get_stats(text)
        words = self.extract_words(text)
        sentences = self.split_sentences(text)
        
        # Word frequencies
        word_counts = Counter(w.lower() for w in words)
        word_frequencies = dict(word_counts.most_common(top_n))
        
        # Character frequencies
        char_counts = Counter(c for c in text if not c.isspace())
        char_frequencies = dict(char_counts.most_common(top_n))
        
        # N-grams
        ngrams = {}
        for n in range(ngram_range[0], min(ngram_range[1] + 1, 4)):
            ngrams[n] = self.get_ngrams(words, n)[:top_n]
        
        # Keywords (non-stop words, sorted by frequency)
        keywords = [
            w for w, _ in word_counts.most_common(top_n * 2)
            if w.lower() not in self.stop_words and len(w) > 2
        ][:top_n]
        
        return TextAnalysis(
            stats=stats,
            word_frequencies=word_frequencies,
            char_frequencies=char_frequencies,
            ngrams=ngrams,
            keywords=keywords,
            sentences=sentences,
            words=words,
        )
    
    def get_stats(self, text: str) -> TextStats:
        """
        Get comprehensive text statistics.
        
        Args:
            text: Input text
        
        Returns:
            TextStats object
        """
        if not text:
            return TextStats()
        
        chars = len(text)
        chars_no_spaces = len(text.replace(' ', '').replace('\t', ''))
        
        words = self.extract_words(text)
        word_count = len(words)
        
        sentences = self.split_sentences(text)
        sentence_count = len(sentences)
        
        paragraphs = [p for p in text.split('\n\n') if p.strip()]
        paragraph_count = len(paragraphs)
        
        lines = [l for l in text.split('\n') if l.strip()]
        line_count = len(lines)
        
        avg_word_length = sum(len(w) for w in words) / word_count if word_count else 0
        avg_sentence_length = word_count / sentence_count if sentence_count else 0
        
        unique_words = len(set(w.lower() for w in words))
        
        # Simple readability score (Flesch-like)
        syllable_count = sum(self.count_syllables(w) for w in words)
        if sentence_count > 0 and word_count > 0:
            readability_score = 206.835 - 1.015 * (word_count / sentence_count) - \
                               84.6 * (syllable_count / word_count)
            readability_score = max(0, min(100, readability_score))
        else:
            readability_score = 0
        
        return TextStats(
            char_count=chars,
            char_count_no_spaces=chars_no_spaces,
            word_count=word_count,
            sentence_count=sentence_count,
            paragraph_count=paragraph_count,
            line_count=line_count,
            avg_word_length=avg_word_length,
            avg_sentence_length=avg_sentence_length,
            unique_words=unique_words,
            readability_score=readability_score,
        )
    
    def count_syllables(self, word: str) -> int:
        """
        Estimate syllable count in a word.
        
        Args:
            word: Input word
        
        Returns:
            Estimated syllable count
        """
        word = word.lower()
        if len(word) <= 3:
            return 1
        
        # Count vowel groups
        vowels = 'aeiouy'
        count = 0
        prev_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_vowel:
                count += 1
            prev_vowel = is_vowel
        
        # Adjust for silent e
        if word.endswith('e') and count > 1:
            count -= 1
        
        # Adjust for -le endings
        if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
            count += 1
        
        return max(1, count)
    
    def extract_words(self, text: str, min_length: int = 1) -> List[str]:
        """
        Extract words from text.
        
        Args:
            text: Input text
            min_length: Minimum word length
        
        Returns:
            List of words
        """
        words = re.findall(r'\b\w+\b', text)
        return [w for w in words if len(w) >= min_length]
    
    def split_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences.
        
        Args:
            text: Input text
        
        Returns:
            List of sentences
        """
        # Handle common abbreviations
        abbreviations = r'(?:Mr|Mrs|Ms|Dr|Prof|Sr|Jr|vs|etc|Inc|Ltd|Co|Corp)\.'
        
        # Split on sentence-ending punctuation
        sentences = re.split(
            r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s',
            text
        )
        
        return [s.strip() for s in sentences if s.strip()]
    
    def get_ngrams(self, words: List[str], n: int = 2) -> List[Tuple[str, ...]]:
        """
        Generate n-grams from word list.
        
        Args:
            words: List of words
            n: N-gram size
        
        Returns:
            List of n-grams
        """
        if len(words) < n:
            return []
        
        return [tuple(words[i:i+n]) for i in range(len(words) - n + 1)]
    
    def keyword_density(self, text: str, 
                        min_length: int = 3) -> List[Tuple[str, float]]:
        """
        Calculate keyword density.
        
        Args:
            text: Input text
            min_length: Minimum word length
        
        Returns:
            List of (keyword, density) tuples
        """
        words = self.extract_words(text, min_length)
        total = len(words)
        
        if total == 0:
            return []
        
        # Filter stop words
        keywords = [w.lower() for w in words if w.lower() not in self.stop_words]
        counts = Counter(keywords)
        
        return [(word, count / total * 100) 
                for word, count in counts.most_common()]
    
    # -------------------------------------------------------------------------
    # Transformation
    # -------------------------------------------------------------------------
    
    def reverse(self, text: str, preserve_words: bool = False) -> str:
        """
        Reverse text.
        
        Args:
            text: Input text
            preserve_words: If True, reverse word order but keep words intact
        
        Returns:
            Reversed text
        """
        if preserve_words:
            return ' '.join(text.split()[::-1])
        return text[::-1]
    
    def rotate(self, text: str, shift: int) -> str:
        """
        Rotate text characters.
        
        Args:
            text: Input text
            shift: Number of positions to shift (positive = right, negative = left)
        
        Returns:
            Rotated text
        """
        if not text:
            return text
        shift = shift % len(text)
        return text[-shift:] + text[:-shift]
    
    def alternate_case(self, text: str) -> str:
        """
        Convert text to alternating case.
        
        Args:
            text: Input text
        
        Returns:
            Alternating case text
        """
        result = []
        upper = True
        for char in text:
            if char.isalpha():
                result.append(char.upper() if upper else char.lower())
                upper = not upper
            else:
                result.append(char)
        return ''.join(result)
    
    def mirror(self, text: str) -> str:
        """
        Create mirrored text (text + reversed text).
        
        Args:
            text: Input text
        
        Returns:
            Mirrored text
        """
        return text + text[::-1]
    
    def truncate(self, text: str, max_length: int, 
                 suffix: str = '...', align: str = 'start') -> str:
        """
        Truncate text to maximum length.
        
        Args:
            text: Input text
            max_length: Maximum length
            suffix: Suffix to add
            align: 'start', 'end', or 'middle'
        
        Returns:
            Truncated text
        """
        if len(text) <= max_length:
            return text
        
        suffix_len = len(suffix)
        if max_length <= suffix_len:
            return suffix[:max_length]
        
        available = max_length - suffix_len
        
        if align == 'start':
            return text[:available] + suffix
        elif align == 'middle':
            half = available // 2
            return text[:half] + suffix + text[-(available - half):]
        else:  # end
            return suffix + text[-available:]
    
    def abbreviate(self, text: str, max_words: int = 3) -> str:
        """
        Create abbreviation from text (first letters of words).
        
        Args:
            text: Input text
            max_words: Maximum words to abbreviate
        
        Returns:
            Abbreviation
        """
        words = self.split_into_words(text)
        return ''.join(w[0].upper() for w in words[:max_words])
    
    # -------------------------------------------------------------------------
    # Hashing and Encoding
    # -------------------------------------------------------------------------
    
    def hash_text(self, text: str, algorithm: str = 'md5') -> str:
        """
        Hash text using specified algorithm.
        
        Args:
            text: Input text
            algorithm: Hash algorithm ('md5', 'sha1', 'sha256', 'sha512')
        
        Returns:
            Hex digest
        """
        algorithms = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha256': hashlib.sha256,
            'sha512': hashlib.sha512,
        }
        
        if algorithm not in algorithms:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        
        return algorithms[algorithm](text.encode()).hexdigest()
    
    def to_base64(self, text: str) -> str:
        """
        Convert text to Base64 (using standard library).
        
        Args:
            text: Input text
        
        Returns:
            Base64 encoded string
        """
        import base64
        return base64.b64encode(text.encode()).decode()
    
    def from_base64(self, text: str) -> str:
        """
        Decode Base64 to text.
        
        Args:
            text: Base64 encoded string
        
        Returns:
            Decoded text
        """
        import base64
        return base64.b64decode(text.encode()).decode()
    
    # -------------------------------------------------------------------------
    # Search and Replace
    # -------------------------------------------------------------------------
    
    def find_all(self, text: str, pattern: str, 
                 case_sensitive: bool = True) -> List[int]:
        """
        Find all occurrences of pattern in text.
        
        Args:
            text: Input text
            pattern: Pattern to find
            case_sensitive: Case sensitivity
        
        Returns:
            List of start positions
        """
        if not case_sensitive:
            text = text.lower()
            pattern = pattern.lower()
        
        positions = []
        start = 0
        while True:
            pos = text.find(pattern, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1
        
        return positions
    
    def replace_all(self, text: str, replacements: Dict[str, str],
                    case_sensitive: bool = True) -> str:
        """
        Replace multiple patterns in text.
        
        Args:
            text: Input text
            replacements: Dict of {pattern: replacement}
            case_sensitive: Case sensitivity
        
        Returns:
            Text with replacements
        """
        result = text
        
        if not case_sensitive:
            for pattern, replacement in replacements.items():
                result = re.sub(
                    re.escape(pattern),
                    replacement,
                    result,
                    flags=re.IGNORECASE
                )
        else:
            for pattern, replacement in replacements.items():
                result = result.replace(pattern, replacement)
        
        return result
    
    def highlight(self, text: str, terms: List[str],
                  marker: str = '**') -> str:
        """
        Highlight terms in text.
        
        Args:
            text: Input text
            terms: Terms to highlight
            marker: Marker to wrap terms
        
        Returns:
            Text with highlighted terms
        """
        result = text
        for term in sorted(terms, key=len, reverse=True):
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            result = pattern.sub(f'{marker}\\g<0>{marker}', result)
        return result
    
    # -------------------------------------------------------------------------
    # Comparison
    # -------------------------------------------------------------------------
    
    def similarity(self, text1: str, text2: str) -> float:
        """
        Calculate text similarity (Jaccard index on words).
        
        Args:
            text1: First text
            text2: Second text
        
        Returns:
            Similarity score (0.0 to 1.0)
        """
        words1 = set(w.lower() for w in self.extract_words(text1))
        words2 = set(w.lower() for w in self.extract_words(text2))
        
        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union)
    
    def contains_all(self, text: str, terms: List[str],
                     case_sensitive: bool = False) -> bool:
        """
        Check if text contains all terms.
        
        Args:
            text: Input text
            terms: Terms to check
            case_sensitive: Case sensitivity
        
        Returns:
            True if all terms found
        """
        if not case_sensitive:
            text = text.lower()
            terms = [t.lower() for t in terms]
        
        return all(term in text for term in terms)
    
    def contains_any(self, text: str, terms: List[str],
                     case_sensitive: bool = False) -> bool:
        """
        Check if text contains any term.
        
        Args:
            text: Input text
            terms: Terms to check
            case_sensitive: Case sensitivity
        
        Returns:
            True if any term found
        """
        if not case_sensitive:
            text = text.lower()
            terms = [t.lower() for t in terms]
        
        return any(term in text for term in terms)
    
    def levenshtein_distance(self, s1: str, s2: str) -> int:
        """
        Calculate Levenshtein distance between two strings.
        
        Optimized implementation using O(min(m,n)) space instead of O(m*n).
        Only keeps two rows of the DP matrix in memory.
        
        Args:
            s1: First string
            s2: Second string
        
        Returns:
            Edit distance
        """
        # Ensure s1 is the longer string for memory efficiency
        if len(s1) < len(s2):
            return self.levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        # Use array module for better performance with large strings
        # Previous row: distance from empty prefix of s1 to prefixes of s2
        previous_row = list(range(len(s2) + 1))
        
        for i, c1 in enumerate(s1):
            # Current row: distance from prefix s1[:i+1] to prefixes of s2
            current_row = [i + 1]
            
            for j, c2 in enumerate(s2):
                # Three possible operations
                insertions = previous_row[j + 1] + 1     # Insert c2
                deletions = current_row[j] + 1           # Delete c1
                substitutions = previous_row[j] + (c1 != c2)  # Substitute
                
                # Minimum cost operation
                current_row.append(min(insertions, deletions, substitutions))
            
            # Swap rows (previous_row becomes current_row for next iteration)
            previous_row = current_row
        
        return previous_row[-1]


# =============================================================================
# Module-level Functions (Convenience)
# =============================================================================

# Default instance for module-level functions
_default_utils = TextUtils()


def to_case(text: str, case: TextCase, separator: str = '_') -> str:
    """Convert text to specified case style."""
    return _default_utils.to_case(text, case, separator)


def to_sentence_case(text: str) -> str:
    """Convert text to sentence case."""
    return _default_utils.to_sentence_case(text)


def clean(text: str, **kwargs) -> str:
    """Clean text with various options."""
    return _default_utils.clean(text, **kwargs)


def analyze(text: str, **kwargs) -> TextAnalysis:
    """Perform comprehensive text analysis."""
    return _default_utils.analyze(text, **kwargs)


def get_stats(text: str) -> TextStats:
    """Get text statistics."""
    return _default_utils.get_stats(text)


def extract_words(text: str, min_length: int = 1) -> List[str]:
    """Extract words from text."""
    return _default_utils.extract_words(text, min_length)


def split_sentences(text: str) -> List[str]:
    """Split text into sentences."""
    return _default_utils.split_sentences(text)


def get_ngrams(words: List[str], n: int = 2) -> List[Tuple[str, ...]]:
    """Generate n-grams from word list."""
    return _default_utils.get_ngrams(words, n)


def remove_html(text: str) -> str:
    """Remove HTML tags from text."""
    return _default_utils.remove_html(text)


def remove_urls(text: str, replace_with: str = '') -> str:
    """Remove URLs from text."""
    return _default_utils.remove_urls(text, replace_with)


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace."""
    return _default_utils.normalize_whitespace(text)


def truncate(text: str, max_length: int, **kwargs) -> str:
    """Truncate text."""
    return _default_utils.truncate(text, max_length, **kwargs)


def hash_text(text: str, algorithm: str = 'md5') -> str:
    """Hash text."""
    return _default_utils.hash_text(text, algorithm)


def similarity(text1: str, text2: str) -> float:
    """Calculate text similarity."""
    return _default_utils.similarity(text1, text2)


def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculate Levenshtein distance."""
    return _default_utils.levenshtein_distance(s1, s2)


# =============================================================================
# CLI Interface
# =============================================================================

if __name__ == '__main__':
    import sys
    import json
    
    utils = TextUtils()
    
    if len(sys.argv) < 2:
        print("Text Utils - Command Line Interface")
        print("Usage: python mod.py <command> [args]")
        print("\nCommands:")
        print("  stats <text>       - Get text statistics")
        print("  clean <text>       - Clean text")
        print("  case <text> <style> - Convert case (lower/upper/title/snake/kebab)")
        print("  analyze <text>     - Full text analysis")
        print("  hash <text>        - Hash text (MD5)")
        print("  similarity <t1> <t2> - Compare two texts")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == 'stats' and len(sys.argv) > 2:
        text = ' '.join(sys.argv[2:])
        stats = utils.get_stats(text)
        print(json.dumps(stats.to_dict(), indent=2))
    
    elif command == 'clean' and len(sys.argv) > 2:
        text = ' '.join(sys.argv[2:])
        print(utils.clean(text, remove_extra_spaces=True))
    
    elif command == 'case' and len(sys.argv) > 3:
        text = sys.argv[2]
        case_style = sys.argv[3]
        try:
            case = TextCase[case_style.upper()]
            print(utils.to_case(text, case))
        except KeyError:
            print(f"Invalid case style: {case_style}")
            sys.exit(1)
    
    elif command == 'analyze' and len(sys.argv) > 2:
        text = ' '.join(sys.argv[2:])
        analysis = utils.analyze(text)
        print(json.dumps(analysis.to_dict(), indent=2, ensure_ascii=False))
    
    elif command == 'hash' and len(sys.argv) > 2:
        text = ' '.join(sys.argv[2:])
        print(f"MD5: {utils.hash_text(text, 'md5')}")
        print(f"SHA256: {utils.hash_text(text, 'sha256')}")
    
    elif command == 'similarity' and len(sys.argv) > 3:
        text1 = sys.argv[2]
        text2 = ' '.join(sys.argv[3:])
        sim = utils.similarity(text1, text2)
        print(f"Similarity: {sim:.2%}")
    
    else:
        print(f"Unknown command or missing arguments: {command}")
        sys.exit(1)
