"""
N-gram Utilities Module

Provides comprehensive N-gram generation and analysis utilities for text processing.
N-grams are contiguous sequences of n items (characters, words, or tokens) from a given text.

Features:
- Character N-grams (for spell checking, language detection)
- Word N-grams (for text prediction, similarity)
- Token N-grams (custom tokenization)
- N-gram frequency analysis
- N-gram similarity scoring (Jaccard, Dice, Cosine)
- Language detection using N-gram profiles
- Text prediction based on N-gram frequencies
- Zero external dependencies

Use Cases:
- Spelling correction
- Language identification
- Text classification
- Search autocomplete
- Plagiarism detection
- Text similarity comparison
- Word prediction
"""

from collections import Counter, defaultdict
from typing import List, Dict, Tuple, Optional, Union, Callable, Set
import math
import re


def char_ngrams(text: str, n: int = 2, pad: bool = False, pad_char: str = ' ') -> List[str]:
    """
    Generate character N-grams from text.
    
    Args:
        text: Input text
        n: Size of N-grams (default 2 for bigrams)
        pad: Whether to pad the text (adds n-1 padding chars to start/end)
        pad_char: Character to use for padding
    
    Returns:
        List of character N-grams
    
    Examples:
        >>> char_ngrams("hello", 2)
        ['he', 'el', 'll', 'lo']
        >>> char_ngrams("hello", 3)
        ['hel', 'ell', 'llo']
        >>> char_ngrams("hi", 2, pad=True)
        [' h', 'hi', 'i ']
    """
    if not text or n < 1:
        return []
    
    if pad:
        padding = pad_char * (n - 1)
        text = padding + text + padding
    
    if len(text) < n:
        return [text] if text else []
    
    return [text[i:i+n] for i in range(len(text) - n + 1)]


def word_ngrams(text: str, n: int = 2, tokenizer: Optional[Callable[[str], List[str]]] = None) -> List[str]:
    """
    Generate word N-grams from text.
    
    Args:
        text: Input text
        n: Size of N-grams (default 2 for bigrams)
        tokenizer: Custom tokenizer function (default: split on whitespace and remove punctuation)
    
    Returns:
        List of word N-grams (space-separated word sequences)
    
    Examples:
        >>> word_ngrams("hello world test", 2)
        ['hello world', 'world test']
        >>> word_ngrams("the quick brown fox", 3)
        ['the quick brown', 'quick brown fox']
    """
    if not text:
        return []
    
    if tokenizer:
        words = tokenizer(text)
    else:
        # Default: lowercase and split on non-alphanumeric
        words = re.findall(r'\b\w+\b', text.lower())
    
    if len(words) < n:
        return [' '.join(words)] if words else []
    
    return [' '.join(words[i:i+n]) for i in range(len(words) - n + 1)]


def token_ngrams(tokens: List[str], n: int = 2) -> List[Tuple[str, ...]]:
    """
    Generate N-grams from a list of tokens.
    
    Args:
        tokens: List of tokens
        n: Size of N-grams (default 2 for bigrams)
    
    Returns:
        List of N-gram tuples
    
    Examples:
        >>> token_ngrams(['a', 'b', 'c', 'd'], 2)
        [('a', 'b'), ('b', 'c'), ('c', 'd')]
        >>> token_ngrams(['hello', 'world'], 3)
        [('hello', 'world')]
    """
    if not tokens or n < 1:
        return []
    
    if len(tokens) < n:
        return [tuple(tokens)]
    
    return [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]


def ngram_frequencies(ngrams: List[str], normalize: bool = False) -> Dict[str, Union[int, float]]:
    """
    Calculate frequency distribution of N-grams.
    
    Args:
        ngrams: List of N-grams
        normalize: If True, return relative frequencies (sum to 1.0)
    
    Returns:
        Dictionary mapping N-grams to frequencies
    
    Examples:
        >>> ngram_frequencies(['a', 'b', 'a', 'c'])
        {'a': 2, 'b': 1, 'c': 1}
        >>> ngram_frequencies(['a', 'b', 'a', 'c'], normalize=True)
        {'a': 0.5, 'b': 0.25, 'c': 0.25}
    """
    if not ngrams:
        return {}
    
    counter = Counter(ngrams)
    
    if normalize:
        total = sum(counter.values())
        return {ngram: count / total for ngram, count in counter.items()}
    
    return dict(counter)


def all_ngrams(text: str, min_n: int = 1, max_n: int = 3, mode: str = 'char') -> List[str]:
    """
    Generate all N-grams within a size range.
    
    Args:
        text: Input text
        min_n: Minimum N-gram size
        max_n: Maximum N-gram size
        mode: 'char' for character N-grams, 'word' for word N-grams
    
    Returns:
        List of all N-grams in the specified range
    
    Examples:
        >>> all_ngrams("hi", 1, 2, 'char')
        ['h', 'i', 'hi']
        >>> all_ngrams("a b", 1, 2, 'word')
        ['a', 'b', 'a b']
    """
    result = []
    
    for n in range(min_n, max_n + 1):
        if mode == 'char':
            result.extend(char_ngrams(text, n))
        elif mode == 'word':
            result.extend(word_ngrams(text, n))
    
    return result


def jaccard_similarity(ngrams1: Set[str], ngrams2: Set[str]) -> float:
    """
    Calculate Jaccard similarity between two sets of N-grams.
    
    Jaccard = |A ∩ B| / |A ∪ B|
    
    Args:
        ngrams1: First set of N-grams
        ngrams2: Second set of N-grams
    
    Returns:
        Jaccard similarity score (0.0 to 1.0)
    
    Examples:
        >>> jaccard_similarity({'a', 'b', 'c'}, {'b', 'c', 'd'})
        0.5
        >>> jaccard_similarity({'hello'}, {'hello'})
        1.0
    """
    if not ngrams1 and not ngrams2:
        return 1.0
    
    if not ngrams1 or not ngrams2:
        return 0.0
    
    intersection = ngrams1 & ngrams2
    union = ngrams1 | ngrams2
    
    return len(intersection) / len(union)


def dice_similarity(ngrams1: Set[str], ngrams2: Set[str]) -> float:
    """
    Calculate Dice similarity (Sørensen–Dice coefficient) between two sets of N-grams.
    
    Dice = 2 * |A ∩ B| / (|A| + |B|)
    
    Args:
        ngrams1: First set of N-grams
        ngrams2: Second set of N-grams
    
    Returns:
        Dice similarity score (0.0 to 1.0)
    
    Examples:
        >>> dice_similarity({'a', 'b', 'c'}, {'b', 'c', 'd'})
        0.666...
    """
    if not ngrams1 and not ngrams2:
        return 1.0
    
    if not ngrams1 or not ngrams2:
        return 0.0
    
    intersection = ngrams1 & ngrams2
    
    return (2 * len(intersection)) / (len(ngrams1) + len(ngrams2))


def cosine_similarity(freq1: Dict[str, float], freq2: Dict[str, float]) -> float:
    """
    Calculate Cosine similarity between two N-gram frequency vectors.
    
    Cosine = (A · B) / (||A|| * ||B||)
    
    Args:
        freq1: First frequency dictionary
        freq2: Second frequency dictionary
    
    Returns:
        Cosine similarity score (0.0 to 1.0)
    
    Examples:
        >>> cosine_similarity({'a': 1, 'b': 2}, {'a': 2, 'b': 1})
        0.8
    """
    if not freq1 or not freq2:
        return 0.0
    
    # Get all unique N-grams
    all_ngrams_set = set(freq1.keys()) | set(freq2.keys())
    
    # Calculate dot product
    dot_product = sum(freq1.get(ngram, 0) * freq2.get(ngram, 0) for ngram in all_ngrams_set)
    
    # Calculate magnitudes
    mag1 = math.sqrt(sum(v ** 2 for v in freq1.values()))
    mag2 = math.sqrt(sum(v ** 2 for v in freq2.values()))
    
    if mag1 == 0 or mag2 == 0:
        return 0.0
    
    return dot_product / (mag1 * mag2)


def ngram_profile(text: str, n: int = 3, top_k: int = 300) -> Dict[str, int]:
    """
    Create an N-gram profile for a text (useful for language detection).
    
    Args:
        text: Input text
        n: Size of N-grams (default 3 for trigrams)
        top_k: Number of top N-grams to include
    
    Returns:
        Dictionary of top N-grams with their ranks (lower rank = more frequent)
    
    Examples:
        >>> profile = ngram_profile("hello world hello", 2, 5)
        >>> len(profile) <= 5
        True
    """
    # Generate character N-grams (lowercase, alphanumeric only)
    clean_text = re.sub(r'[^a-z0-9]', '', text.lower())
    ngrams = char_ngrams(clean_text, n, pad=True)
    
    # Count frequencies
    counter = Counter(ngrams)
    
    # Return top k with ranks
    return {ngram: rank + 1 for rank, (ngram, _) in enumerate(counter.most_common(top_k))}


def language_distance(profile1: Dict[str, int], profile2: Dict[str, int]) -> int:
    """
    Calculate out-of-place distance between two N-gram profiles.
    
    Used for language identification. Lower distance = more similar.
    
    Args:
        profile1: First N-gram profile (from ngram_profile)
        profile2: Second N-gram profile
    
    Returns:
        Out-of-place distance (lower = more similar)
    
    Examples:
        >>> p1 = {'a': 1, 'b': 2}
        >>> p2 = {'a': 1, 'b': 2}
        >>> language_distance(p1, p2)
        0
    """
    max_rank = max(max(profile1.values(), default=0), max(profile2.values(), default=0))
    max_distance = max_rank * len(profile1)
    
    distance = 0
    for ngram, rank in profile1.items():
        if ngram in profile2:
            distance += abs(rank - profile2[ngram])
        else:
            distance += max_distance
    
    return distance


def build_language_profiles(texts: Dict[str, str], n: int = 3, top_k: int = 300) -> Dict[str, Dict[str, int]]:
    """
    Build N-gram profiles for multiple languages/texts.
    
    Args:
        texts: Dictionary mapping language names to sample texts
        n: Size of N-grams
        top_k: Number of top N-grams per profile
    
    Returns:
        Dictionary mapping language names to their N-gram profiles
    
    Examples:
        >>> texts = {'en': 'hello world', 'es': 'hola mundo'}
        >>> profiles = build_language_profiles(texts)
        >>> 'en' in profiles and 'es' in profiles
        True
    """
    return {lang: ngram_profile(text, n, top_k) for lang, text in texts.items()}


def detect_language(text: str, language_profiles: Dict[str, Dict[str, int]], 
                    n: int = 3, top_k: int = 300) -> Tuple[str, int]:
    """
    Detect the most likely language of a text using N-gram profiles.
    
    Args:
        text: Text to identify
        language_profiles: Dictionary of language name to N-gram profile
        n: Size of N-grams (should match profile generation)
        top_k: Number of top N-grams (should match profile generation)
    
    Returns:
        Tuple of (detected language, distance score)
    
    Examples:
        >>> profiles = {'en': ngram_profile('hello world test'), 'es': ngram_profile('hola mundo prueba')}
        >>> detect_language('hello there', profiles)[0]
        'en'
    """
    text_profile = ngram_profile(text, n, top_k)
    
    distances = {}
    for lang, profile in language_profiles.items():
        distances[lang] = language_distance(text_profile, profile)
    
    best_lang = min(distances, key=distances.get)
    return best_lang, distances[best_lang]


def ngram_frequency_analysis(text: str, min_n: int = 1, max_n: int = 5, 
                             mode: str = 'char', top_k: int = 10) -> Dict[int, List[Tuple[str, int]]]:
    """
    Perform comprehensive N-gram frequency analysis.
    
    Args:
        text: Input text
        min_n: Minimum N-gram size
        max_n: Maximum N-gram size
        mode: 'char' or 'word'
        top_k: Number of top N-grams to return per size
    
    Returns:
        Dictionary mapping N-gram size to list of (ngram, count) tuples
    
    Examples:
        >>> analysis = ngram_frequency_analysis("hello hello world", 2, 3, 'word', 5)
        >>> 2 in analysis
        True
    """
    analysis = {}
    
    for n in range(min_n, max_n + 1):
        if mode == 'char':
            ngrams = char_ngrams(text, n)
        else:
            ngrams = word_ngrams(text, n)
        
        counter = Counter(ngrams)
        analysis[n] = counter.most_common(top_k)
    
    return analysis


def most_common_ngrams(text: str, n: int, mode: str = 'char', top_k: int = 10) -> List[Tuple[str, int]]:
    """
    Get the most common N-grams in text.
    
    Args:
        text: Input text
        n: Size of N-grams
        mode: 'char' or 'word'
        top_k: Number of top N-grams to return
    
    Returns:
        List of (ngram, count) tuples
    
    Examples:
        >>> most_common_ngrams("hello hello world", 2, 'word')
        [('hello hello', 1), ('hello world', 1)]
    """
    if mode == 'char':
        ngrams = char_ngrams(text, n)
    else:
        ngrams = word_ngrams(text, n)
    
    return Counter(ngrams).most_common(top_k)


def build_ngram_model(text: str, n: int = 3, mode: str = 'word') -> Dict[Tuple[str, ...], Dict[str, int]]:
    """
    Build an N-gram language model for text prediction.
    
    The model maps (n-1)-grams to possible next words with frequencies.
    
    Args:
        text: Input text corpus
        n: Size of N-grams (model will use n-1 context to predict nth)
        mode: 'word' for word N-grams (default), 'char' for character N-grams
    
    Returns:
        Dictionary mapping context tuples to dictionaries of possible next tokens
    
    Examples:
        >>> model = build_ngram_model("the cat sat on the mat", 2)
        >>> ('the',) in model
        True
    """
    if mode == 'word':
        tokens = re.findall(r'\b\w+\b', text.lower())
    else:
        tokens = list(text.lower())
    
    model = defaultdict(lambda: defaultdict(int))
    
    if len(tokens) < n:
        return {tuple(tokens): {}}
    
    for i in range(len(tokens) - n + 1):
        context = tuple(tokens[i:i+n-1])
        next_token = tokens[i+n-1]
        model[context][next_token] += 1
    
    return {k: dict(v) for k, v in model.items()}


def predict_next(model: Dict[Tuple[str, ...], Dict[str, int]], 
                 context: List[str], top_k: int = 5) -> List[Tuple[str, float]]:
    """
    Predict the most likely next token given a context.
    
    Args:
        model: N-gram model from build_ngram_model
        context: List of preceding tokens
        top_k: Number of predictions to return
    
    Returns:
        List of (token, probability) tuples
    
    Examples:
        >>> model = build_ngram_model("the cat sat the cat ran", 2)
        >>> predict_next(model, ['the'])
        [('cat', 1.0)]
    """
    if not context:
        return []
    
    context_tuple = tuple(context)
    
    if context_tuple not in model:
        return []
    
    predictions = model[context_tuple]
    total = sum(predictions.values())
    
    return [(token, count / total) for token, count in 
            sorted(predictions.items(), key=lambda x: x[1], reverse=True)[:top_k]]


def text_similarity(text1: str, text2: str, n: int = 3, method: str = 'jaccard') -> float:
    """
    Calculate similarity between two texts using N-grams.
    
    Args:
        text1: First text
        text2: Second text
        n: Size of N-grams
        method: Similarity method ('jaccard', 'dice', 'cosine')
    
    Returns:
        Similarity score (0.0 to 1.0)
    
    Examples:
        >>> text_similarity("hello world", "hello there", 2, 'jaccard')
        0.5
    """
    # Generate character N-grams
    ngrams1 = set(char_ngrams(text1.lower(), n))
    ngrams2 = set(char_ngrams(text2.lower(), n))
    
    if method == 'jaccard':
        return jaccard_similarity(ngrams1, ngrams2)
    elif method == 'dice':
        return dice_similarity(ngrams1, ngrams2)
    elif method == 'cosine':
        freq1 = ngram_frequencies(list(ngrams1), normalize=True)
        freq2 = ngram_frequencies(list(ngrams2), normalize=True)
        return cosine_similarity(freq1, freq2)
    else:
        raise ValueError(f"Unknown method: {method}. Use 'jaccard', 'dice', or 'cosine'.")


def ngram_overlap(text1: str, text2: str, n: int = 2, mode: str = 'word') -> Dict[str, Union[int, Set[str], float]]:
    """
    Find N-gram overlap between two texts.
    
    Args:
        text1: First text
        text2: Second text
        n: Size of N-grams
        mode: 'char' or 'word'
    
    Returns:
        Dictionary with overlap statistics:
        - 'intersection': Set of common N-grams
        - 'intersection_size': Size of intersection
        - 'union_size': Size of union
        - 'jaccard': Jaccard similarity
    
    Examples:
        >>> overlap = ngram_overlap("hello world", "hello there", 2, 'word')
        >>> overlap['intersection']
        {'hello'}
    """
    if mode == 'char':
        ngrams1 = set(char_ngrams(text1.lower(), n))
        ngrams2 = set(char_ngrams(text2.lower(), n))
    else:
        ngrams1 = set(word_ngrams(text1, n))
        ngrams2 = set(word_ngrams(text2, n))
    
    intersection = ngrams1 & ngrams2
    union = ngrams1 | ngrams2
    
    return {
        'intersection': intersection,
        'intersection_size': len(intersection),
        'union_size': len(union),
        'jaccard': len(intersection) / len(union) if union else 1.0
    }


def unique_ngrams(text: str, n: int = 2, mode: str = 'char') -> Set[str]:
    """
    Get unique N-grams from text.
    
    Args:
        text: Input text
        n: Size of N-grams
        mode: 'char' or 'word'
    
    Returns:
        Set of unique N-grams
    
    Examples:
        >>> unique_ngrams("aabb", 2, 'char')
        {'aa', 'ab', 'bb'}
    """
    if mode == 'char':
        return set(char_ngrams(text, n))
    else:
        return set(word_ngrams(text, n))


def ngram_positions(text: str, n: int = 2, mode: str = 'char') -> Dict[str, List[int]]:
    """
    Find all positions of each N-gram in text.
    
    Args:
        text: Input text
        n: Size of N-grams
        mode: 'char' or 'word'
    
    Returns:
        Dictionary mapping N-grams to lists of starting positions
    
    Examples:
        >>> ngram_positions("abab", 2, 'char')
        {'ab': [0, 2], 'ba': [1]}
    """
    positions = defaultdict(list)
    
    if mode == 'char':
        for i in range(len(text) - n + 1):
            ngram = text[i:i+n]
            positions[ngram].append(i)
    else:
        words = re.findall(r'\b\w+\b', text.lower())
        for i in range(len(words) - n + 1):
            ngram = ' '.join(words[i:i+n])
            positions[ngram].append(i)
    
    return dict(positions)


def sentence_ngrams(text: str, n: int = 2) -> List[str]:
    """
    Generate sentence N-grams (contiguous sentence sequences).
    
    Args:
        text: Input text
        n: Number of sentences per N-gram
    
    Returns:
        List of sentence N-grams
    
    Examples:
        >>> sentences = "Hello. World. Test."
        >>> sentence_ngrams(sentences, 2)
        ['Hello. World.', 'World. Test.']
    """
    # Split on sentence boundaries
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s for s in sentences if s]
    
    if len(sentences) < n:
        return [' '.join(sentences)] if sentences else []
    
    return [' '.join(sentences[i:i+n]) for i in range(len(sentences) - n + 1)]


class NGramAnalyzer:
    """
    A class for comprehensive N-gram analysis of text.
    
    Provides methods for generating, analyzing, and comparing N-grams.
    
    Examples:
        >>> analyzer = NGramAnalyzer("Hello world! Hello there!")
        >>> analyzer.char_ngrams(2)[:3]
        ['He', 'el', 'll']
        >>> analyzer.word_ngrams(2)
        ['hello world', 'world hello', 'hello there']
    """
    
    def __init__(self, text: str):
        """
        Initialize the analyzer with text.
        
        Args:
            text: Text to analyze
        """
        self.text = text
        self._char_ngrams_cache = {}
        self._word_ngrams_cache = {}
    
    def char_ngrams(self, n: int = 2, pad: bool = False) -> List[str]:
        """Generate character N-grams."""
        if (n, pad) not in self._char_ngrams_cache:
            self._char_ngrams_cache[(n, pad)] = char_ngrams(self.text, n, pad)
        return self._char_ngrams_cache[(n, pad)]
    
    def word_ngrams(self, n: int = 2) -> List[str]:
        """Generate word N-grams."""
        if n not in self._word_ngrams_cache:
            self._word_ngrams_cache[n] = word_ngrams(self.text, n)
        return self._word_ngrams_cache[n]
    
    def frequencies(self, n: int = 2, mode: str = 'char', normalize: bool = False) -> Dict[str, Union[int, float]]:
        """Get N-gram frequencies."""
        ngrams = self.char_ngrams(n) if mode == 'char' else self.word_ngrams(n)
        return ngram_frequencies(ngrams, normalize)
    
    def most_common(self, n: int = 2, mode: str = 'char', top_k: int = 10) -> List[Tuple[str, int]]:
        """Get most common N-grams."""
        return most_common_ngrams(self.text, n, mode, top_k)
    
    def unique(self, n: int = 2, mode: str = 'char') -> Set[str]:
        """Get unique N-grams."""
        return unique_ngrams(self.text, n, mode)
    
    def profile(self, n: int = 3, top_k: int = 300) -> Dict[str, int]:
        """Generate N-gram profile for language detection."""
        return ngram_profile(self.text, n, top_k)
    
    def similarity_to(self, other: str, n: int = 3, method: str = 'jaccard') -> float:
        """Calculate similarity to another text."""
        return text_similarity(self.text, other, n, method)
    
    def analysis(self, min_n: int = 1, max_n: int = 5, mode: str = 'char', top_k: int = 10) -> Dict[int, List[Tuple[str, int]]]:
        """Perform comprehensive N-gram frequency analysis."""
        return ngram_frequency_analysis(self.text, min_n, max_n, mode, top_k)
    
    def build_model(self, n: int = 3, mode: str = 'word') -> Dict[Tuple[str, ...], Dict[str, int]]:
        """Build N-gram prediction model."""
        return build_ngram_model(self.text, n, mode)
    
    def __repr__(self) -> str:
        preview = self.text[:50] + '...' if len(self.text) > 50 else self.text
        return f"NGramAnalyzer('{preview}')"


# Common language profiles for quick language detection
COMMON_LANGUAGE_PROFILES = {
    'en': 'the quick brown fox jumps over the lazy dog this is a sample english text for testing purposes language detection works better with more text',
    'es': 'el veloz murciélago hindú comía feliz cardillo y kiwi la cigüeña tocaba el saxofón detrás del palenque de paja este es un texto de muestra en español',
    'fr': 'le vif zéphyr joua sur les xylophones et les cithares ceci est un texte exemple en français pour les tests de détection de langue',
    'de': 'der schnelle braune fuchs springt über den faulen hund dies ist ein beispieltext auf deutsch für spracherkennungstests',
    'it': 'il rapido volpe marrone salta sopra il cane pigro questo è un testo di esempio in italiano per test di rilevamento della lingua',
    'pt': 'a rápida raposa marrom salta sobre o cão preguiçoso este é um texto de exemplo em português para testes de detecção de idioma',
    'nl': 'de snelle bruine vos springt over de luie hond dit is een voorbeeldtekst in het nederlands voor taaldetectietests',
    'ru': 'быстрая коричневая лиса прыгает через ленивую собаку это пример текста на русском языке для тестов определения языка',
    'zh': '快速的棕色狐狸跳过懒狗 这是一个中文示例文本 用于语言检测测试',
    'ja': '速い茶色の狐が怠惰な犬を飛び越える これは言語検出テスト用の日本語サンプルテキストです',
    'ko': '빠른 갈색 여우가 게으른 개를 뛰어넘습니다 이것은 언어 감지 테스트를 위한 한국어 샘플 텍스트입니다',
    'ar': 'الثعلب البني السريع يقفز فوق الكلب الكسول هذا نص عينة باللغة العربية لاختبارات الكشف عن اللغة',
}


def get_common_language_profiles(n: int = 3, top_k: int = 300) -> Dict[str, Dict[str, int]]:
    """
    Get pre-built N-gram profiles for common languages.
    
    Returns profiles for: English, Spanish, French, German, Italian, Portuguese,
    Dutch, Russian, Chinese, Japanese, Korean, Arabic.
    
    Args:
        n: Size of N-grams
        top_k: Number of top N-grams per profile
    
    Returns:
        Dictionary mapping language codes to their N-gram profiles
    """
    return build_language_profiles(COMMON_LANGUAGE_PROFILES, n, top_k)


# Convenience functions for common N-gram types
bigrams = lambda text, mode='char': char_ngrams(text, 2) if mode == 'char' else word_ngrams(text, 2)
trigrams = lambda text, mode='char': char_ngrams(text, 3) if mode == 'char' else word_ngrams(text, 3)
quadgrams = lambda text, mode='char': char_ngrams(text, 4) if mode == 'char' else word_ngrams(text, 4)


if __name__ == '__main__':
    # Demo
    print("=== N-gram Utilities Demo ===\n")
    
    # Character N-grams
    text = "Hello World"
    print(f"Text: '{text}'")
    print(f"Character bigrams: {char_ngrams(text, 2)}")
    print(f"Character trigrams: {char_ngrams(text, 3)}")
    
    # Word N-grams
    sentence = "The quick brown fox jumps over the lazy dog"
    print(f"\nSentence: '{sentence}'")
    print(f"Word bigrams: {word_ngrams(sentence, 2)}")
    print(f"Word trigrams: {word_ngrams(sentence, 3)}")
    
    # Frequency analysis
    print(f"\nMost common character bigrams: {most_common_ngrams(text, 2, 'char', 5)}")
    
    # Text similarity
    text1 = "hello world"
    text2 = "hello there"
    print(f"\nSimilarity between '{text1}' and '{text2}':")
    print(f"  Jaccard (n=2): {text_similarity(text1, text2, 2, 'jaccard'):.4f}")
    print(f"  Dice (n=2): {text_similarity(text1, text2, 2, 'dice'):.4f}")
    print(f"  Cosine (n=2): {text_similarity(text1, text2, 2, 'cosine'):.4f}")
    
    # N-gram analyzer class
    analyzer = NGramAnalyzer("The cat sat on the mat. The cat ran away.")
    print(f"\nAnalyzer most common word bigrams: {analyzer.most_common(2, 'word', 3)}")
    
    # Language detection
    profiles = get_common_language_profiles()
    test_texts = [
        "This is a sample English text for testing language detection.",
        "Este es un texto de muestra en español para probar la detección de idioma.",
        "Ceci est un exemple de texte en français pour tester la détection de langue.",
    ]
    print("\nLanguage detection:")
    for t in test_texts:
        lang, dist = detect_language(t, profiles)
        print(f"  '{t[:40]}...' -> {lang} (distance: {dist})")