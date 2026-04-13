#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Text Similarity Utilities Module
==============================================
A comprehensive text similarity utility module with zero external dependencies.

Features:
    - Levenshtein distance (edit distance)
    - Damerau-Levenshtein distance (with transpositions)
    - Hamming distance (for equal-length strings)
    - Jaro similarity and Jaro-Winkler similarity
    - Cosine similarity (vector-based)
    - Jaccard similarity (set-based)
    - Dice coefficient (Sorensen-Dice)
    - N-gram similarity
    - Longest Common Subsequence (LCS)
    - Soundex and Metaphone phonetic algorithms
    - TF-IDF similarity (basic implementation)
    - Fuzzy matching utilities

Author: AllToolkit Contributors
License: MIT
"""

import math
import re
from typing import List, Dict, Tuple, Set, Optional, Union, Callable
from collections import Counter
from functools import lru_cache


# =============================================================================
# Distance-Based Similarity Functions
# =============================================================================

def levenshtein_distance(s1: str, s2: str, case_sensitive: bool = True) -> int:
    """
    Calculate the Levenshtein (edit) distance between two strings.
    
    The Levenshtein distance is the minimum number of single-character edits
    (insertions, deletions, substitutions) required to change one string into another.
    
    Args:
        s1: First string
        s2: Second string
        case_sensitive: Whether to consider case (default True)
    
    Returns:
        Edit distance as integer
    
    Example:
        >>> levenshtein_distance("kitten", "sitting")
        3
        >>> levenshtein_distance("hello", "hallo")
        1
    """
    if not case_sensitive:
        s1 = s1.lower()
        s2 = s2.lower()
    
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1, case_sensitive=True)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = list(range(len(s2) + 1))
    
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # Insertions, deletions, substitutions
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def levenshtein_ratio(s1: str, s2: str, case_sensitive: bool = True) -> float:
    """
    Calculate Levenshtein similarity ratio (0.0 to 1.0).
    
    Ratio = 1 - (distance / max_length)
    
    Args:
        s1: First string
        s2: Second string
        case_sensitive: Whether to consider case
    
    Returns:
        Similarity ratio between 0.0 and 1.0
    
    Example:
        >>> levenshtein_ratio("hello", "hallo")
        0.8
    """
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    
    distance = levenshtein_distance(s1, s2, case_sensitive)
    max_len = max(len(s1), len(s2))
    return 1.0 - (distance / max_len)


def damerau_levenshtein_distance(s1: str, s2: str, case_sensitive: bool = True) -> int:
    """
    Calculate Damerau-Levenshtein distance (includes transpositions).
    
    Extends Levenshtein to allow transposition of adjacent characters
    as a single edit operation.
    
    Args:
        s1: First string
        s2: Second string
        case_sensitive: Whether to consider case
    
    Returns:
        Edit distance including transpositions
    
    Example:
        >>> damerau_levenshtein_distance("ca", "abc")
        2
        >>> damerau_levenshtein_distance("ab", "ba")  # Transposition counts as 1
        1
    """
    if not case_sensitive:
        s1 = s1.lower()
        s2 = s2.lower()
    
    len1, len2 = len(s1), len(s2)
    
    if len1 == 0:
        return len2
    if len2 == 0:
        return len1
    
    # Create distance matrix
    d = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    
    for i in range(len1 + 1):
        d[i][0] = i
    for j in range(len2 + 1):
        d[0][j] = j
    
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            
            d[i][j] = min(
                d[i - 1][j] + 1,      # Deletion
                d[i][j - 1] + 1,      # Insertion
                d[i - 1][j - 1] + cost  # Substitution
            )
            
            # Transposition
            if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
                d[i][j] = min(d[i][j], d[i - 2][j - 2] + 1)
    
    return d[len1][len2]


def hamming_distance(s1: str, s2: str, case_sensitive: bool = True) -> int:
    """
    Calculate Hamming distance between two equal-length strings.
    
    Hamming distance counts positions where characters differ.
    Strings must be of equal length.
    
    Args:
        s1: First string
        s2: Second string
        case_sensitive: Whether to consider case
    
    Returns:
        Number of differing positions
    
    Raises:
        ValueError: If strings have different lengths
    
    Example:
        >>> hamming_distance("karolin", "kathrin")
        3
    """
    if not case_sensitive:
        s1 = s1.lower()
        s2 = s2.lower()
    
    if len(s1) != len(s2):
        raise ValueError(f"Strings must be of equal length: {len(s1)} != {len(s2)}")
    
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))


def hamming_ratio(s1: str, s2: str, case_sensitive: bool = True) -> float:
    """
    Calculate Hamming similarity ratio.
    
    Args:
        s1: First string
        s2: Second string
        case_sensitive: Whether to consider case
    
    Returns:
        Similarity ratio between 0.0 and 1.0
    
    Raises:
        ValueError: If strings have different lengths
    """
    if not case_sensitive:
        s1 = s1.lower()
        s2 = s2.lower()
    
    if len(s1) != len(s2):
        raise ValueError(f"Strings must be of equal length: {len(s1)} != {len(s2)}")
    
    if len(s1) == 0:
        return 1.0
    
    distance = hamming_distance(s1, s2, case_sensitive=True)
    return 1.0 - (distance / len(s1))


# =============================================================================
# Jaro-Winkler Similarity
# =============================================================================

def jaro_similarity(s1: str, s2: str, case_sensitive: bool = True) -> float:
    """
    Calculate Jaro similarity between two strings.
    
    Jaro similarity is a measure of string similarity that accounts for
    transpositions and matches within a certain distance.
    
    Args:
        s1: First string
        s2: Second string
        case_sensitive: Whether to consider case
    
    Returns:
        Jaro similarity between 0.0 and 1.0
    
    Example:
        >>> jaro_similarity("MARTHA", "MARHTA")
        0.944...
    """
    if not case_sensitive:
        s1 = s1.lower()
        s2 = s2.lower()
    
    if s1 == s2:
        return 1.0
    
    len1, len2 = len(s1), len(s2)
    
    if len1 == 0 or len2 == 0:
        return 0.0
    
    # Maximum distance for matching characters
    match_distance = max(len1, len2) // 2 - 1
    match_distance = max(0, match_distance)
    
    s1_matches = [False] * len1
    s2_matches = [False] * len2
    
    matches = 0
    transpositions = 0
    
    # Find matches
    for i in range(len1):
        start = max(0, i - match_distance)
        end = min(i + match_distance + 1, len2)
        
        for j in range(start, end):
            if s2_matches[j] or s1[i] != s2[j]:
                continue
            s1_matches[i] = True
            s2_matches[j] = True
            matches += 1
            break
    
    if matches == 0:
        return 0.0
    
    # Count transpositions
    k = 0
    for i in range(len1):
        if not s1_matches[i]:
            continue
        while not s2_matches[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1
    
    jaro = (
        matches / len1 + 
        matches / len2 + 
        (matches - transpositions / 2) / matches
    ) / 3
    
    return jaro


def jaro_winkler_similarity(s1: str, s2: str, p: float = 0.1, 
                            case_sensitive: bool = True) -> float:
    """
    Calculate Jaro-Winkler similarity.
    
    Extends Jaro similarity by giving extra weight to matching prefixes.
    
    Args:
        s1: First string
        s2: Second string
        p: Scaling factor for prefix (default 0.1, max 0.25)
        case_sensitive: Whether to consider case
    
    Returns:
        Jaro-Winkler similarity between 0.0 and 1.0
    
    Example:
        >>> jaro_winkler_similarity("MARTHA", "MARHTA")
        0.961...
    """
    if p > 0.25:
        raise ValueError("Scaling factor p must not exceed 0.25")
    
    jaro_sim = jaro_similarity(s1, s2, case_sensitive)
    
    # Calculate common prefix length (max 4)
    if not case_sensitive:
        s1_lower, s2_lower = s1.lower(), s2.lower()
    else:
        s1_lower, s2_lower = s1, s2
    
    prefix_len = 0
    for c1, c2 in zip(s1_lower, s2_lower):
        if c1 == c2:
            prefix_len += 1
        else:
            break
        if prefix_len >= 4:
            break
    
    return jaro_sim + prefix_len * p * (1 - jaro_sim)


# =============================================================================
# Set-Based Similarity
# =============================================================================

def jaccard_similarity(s1: str, s2: str, ngram: int = 1, 
                       case_sensitive: bool = True) -> float:
    """
    Calculate Jaccard similarity between two strings.
    
    Jaccard similarity = |intersection| / |union|
    
    Args:
        s1: First string
        s2: Second string
        ngram: Size of n-grams (default 1 for characters)
        case_sensitive: Whether to consider case
    
    Returns:
        Jaccard similarity between 0.0 and 1.0
    
    Example:
        >>> jaccard_similarity("hello", "hallo")
        0.6
    """
    if not case_sensitive:
        s1 = s1.lower()
        s2 = s2.lower()
    
    if ngram == 1:
        set1 = set(s1)
        set2 = set(s2)
    else:
        set1 = set(s1[i:i + ngram] for i in range(len(s1) - ngram + 1))
        set2 = set(s2[i:i + ngram] for i in range(len(s2) - ngram + 1))
    
    if not set1 and not set2:
        return 1.0
    
    intersection = set1 & set2
    union = set1 | set2
    
    return len(intersection) / len(union) if union else 0.0


def dice_coefficient(s1: str, s2: str, ngram: int = 2, 
                     case_sensitive: bool = True) -> float:
    """
    Calculate Dice coefficient (Sorensen-Dice) between two strings.
    
    Dice = 2 * |intersection| / (|set1| + |set2|)
    
    Args:
        s1: First string
        s2: Second string
        ngram: Size of n-grams (default 2)
        case_sensitive: Whether to consider case
    
    Returns:
        Dice coefficient between 0.0 and 1.0
    
    Example:
        >>> dice_coefficient("hello", "hallo")
        0.8
    """
    if not case_sensitive:
        s1 = s1.lower()
        s2 = s2.lower()
    
    if ngram == 1:
        set1 = set(s1)
        set2 = set(s2)
    else:
        set1 = set(s1[i:i + ngram] for i in range(len(s1) - ngram + 1)) if len(s1) >= ngram else set()
        set2 = set(s2[i:i + ngram] for i in range(len(s2) - ngram + 1)) if len(s2) >= ngram else set()
    
    if not set1 and not set2:
        return 1.0
    if not set1 or not set2:
        return 0.0
    
    intersection = set1 & set2
    
    return 2 * len(intersection) / (len(set1) + len(set2))


def overlap_coefficient(s1: str, s2: str, ngram: int = 1,
                        case_sensitive: bool = True) -> float:
    """
    Calculate Overlap coefficient (Szymkiewicz-Simpson).
    
    Overlap = |intersection| / min(|set1|, |set2|)
    
    Args:
        s1: First string
        s2: Second string
        ngram: Size of n-grams
        case_sensitive: Whether to consider case
    
    Returns:
        Overlap coefficient between 0.0 and 1.0
    """
    if not case_sensitive:
        s1 = s1.lower()
        s2 = s2.lower()
    
    if ngram == 1:
        set1 = set(s1)
        set2 = set(s2)
    else:
        set1 = set(s1[i:i + ngram] for i in range(len(s1) - ngram + 1)) if len(s1) >= ngram else set()
        set2 = set(s2[i:i + ngram] for i in range(len(s2) - ngram + 1)) if len(s2) >= ngram else set()
    
    if not set1 or not set2:
        return 0.0
    if not set1 and not set2:
        return 1.0
    
    intersection = set1 & set2
    return len(intersection) / min(len(set1), len(set2))


# =============================================================================
# Vector-Based Similarity
# =============================================================================

def _get_ngrams(text: str, n: int) -> List[str]:
    """Generate n-grams from text."""
    if len(text) < n:
        return [text] if text else []
    return [text[i:i + n] for i in range(len(text) - n + 1)]


def _get_word_tokens(text: str) -> List[str]:
    """Tokenize text into words."""
    # Simple tokenization: split on non-alphanumeric
    tokens = re.findall(r'\b\w+\b', text.lower())
    return tokens


def cosine_similarity(s1: str, s2: str, ngram: int = 2, 
                      case_sensitive: bool = True) -> float:
    """
    Calculate Cosine similarity between two strings using n-grams.
    
    Cosine similarity measures the angle between two vectors.
    
    Args:
        s1: First string
        s2: Second string
        ngram: Size of n-grams (default 2)
        case_sensitive: Whether to consider case
    
    Returns:
        Cosine similarity between 0.0 and 1.0
    
    Example:
        >>> cosine_similarity("hello world", "world hello")
        1.0
    """
    if not case_sensitive:
        s1 = s1.lower()
        s2 = s2.lower()
    
    if s1 == s2:
        return 1.0
    
    # Generate n-grams
    ngrams1 = _get_ngrams(s1, ngram)
    ngrams2 = _get_ngrams(s2, ngram)
    
    if not ngrams1 and not ngrams2:
        return 1.0
    if not ngrams1 or not ngrams2:
        return 0.0
    
    # Count frequencies
    counter1 = Counter(ngrams1)
    counter2 = Counter(ngrams2)
    
    # Get all unique n-grams
    all_ngrams = set(counter1.keys()) | set(counter2.keys())
    
    # Calculate dot product and magnitudes
    dot_product = sum(counter1.get(ng, 0) * counter2.get(ng, 0) for ng in all_ngrams)
    magnitude1 = math.sqrt(sum(v ** 2 for v in counter1.values()))
    magnitude2 = math.sqrt(sum(v ** 2 for v in counter2.values()))
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)


def cosine_similarity_words(s1: str, s2: str, 
                           case_sensitive: bool = True) -> float:
    """
    Calculate Cosine similarity between two strings using word tokens.
    
    Args:
        s1: First string
        s2: Second string
        case_sensitive: Whether to consider case
    
    Returns:
        Cosine similarity between 0.0 and 1.0
    
    Example:
        >>> cosine_similarity_words("the quick brown fox", "quick brown fox")
        0.866...
    """
    if not case_sensitive:
        s1 = s1.lower()
        s2 = s2.lower()
    
    words1 = _get_word_tokens(s1)
    words2 = _get_word_tokens(s2)
    
    if not words1 and not words2:
        return 1.0
    if not words1 or not words2:
        return 0.0
    
    counter1 = Counter(words1)
    counter2 = Counter(words2)
    
    all_words = set(counter1.keys()) | set(counter2.keys())
    
    dot_product = sum(counter1.get(w, 0) * counter2.get(w, 0) for w in all_words)
    magnitude1 = math.sqrt(sum(v ** 2 for v in counter1.values()))
    magnitude2 = math.sqrt(sum(v ** 2 for v in counter2.values()))
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)


# =============================================================================
# TF-IDF Similarity
# =============================================================================

class TFIDFCalculator:
    """
    TF-IDF (Term Frequency-Inverse Document Frequency) calculator.
    
    Useful for comparing document similarity when you have a corpus.
    
    Example:
        >>> calc = TFIDFCalculator()
        >>> calc.add_document("the quick brown fox")
        >>> calc.add_document("the lazy dog")
        >>> calc.add_document("quick brown fox jumps")
        >>> calc.similarity("quick fox", "brown fox")
        0.816...
    """
    
    def __init__(self):
        self.documents: List[str] = []
        self.doc_tokens: List[List[str]] = []
        self.idf_cache: Dict[str, float] = {}
        self._dirty = True
    
    def add_document(self, doc: str) -> None:
        """Add a document to the corpus."""
        self.documents.append(doc)
        self.doc_tokens.append(_get_word_tokens(doc))
        self._dirty = True
    
    def _calculate_idf(self) -> None:
        """Recalculate IDF values."""
        if not self._dirty:
            return
        
        total_docs = len(self.doc_tokens)
        if total_docs == 0:
            self.idf_cache = {}
            self._dirty = False
            return
        
        # Count document frequency for each term
        doc_freq: Counter = Counter()
        for tokens in self.doc_tokens:
            unique_tokens = set(tokens)
            for token in unique_tokens:
                doc_freq[token] += 1
        
        # Calculate IDF
        self.idf_cache = {}
        for term, freq in doc_freq.items():
            self.idf_cache[term] = math.log(total_docs / (1 + freq))
        
        self._dirty = False
    
    def _get_tfidf_vector(self, text: str) -> Dict[str, float]:
        """Get TF-IDF vector for a text."""
        tokens = _get_word_tokens(text)
        if not tokens:
            return {}
        
        self._calculate_idf()
        
        # Calculate TF
        tf = Counter(tokens)
        total_terms = len(tokens)
        
        # Calculate TF-IDF
        tfidf = {}
        for term, count in tf.items():
            tf_val = count / total_terms
            idf_val = self.idf_cache.get(term, math.log(len(self.doc_tokens) + 1))
            tfidf[term] = tf_val * idf_val
        
        return tfidf
    
    def similarity(self, s1: str, s2: str) -> float:
        """
        Calculate TF-IDF cosine similarity between two texts.
        
        Uses the corpus for IDF calculations.
        
        Args:
            s1: First text
            s2: Second text
        
        Returns:
            Similarity between 0.0 and 1.0
        """
        vec1 = self._get_tfidf_vector(s1)
        vec2 = self._get_tfidf_vector(s2)
        
        if not vec1 or not vec2:
            return 0.0
        
        # Calculate cosine similarity
        all_terms = set(vec1.keys()) | set(vec2.keys())
        dot_product = sum(vec1.get(t, 0) * vec2.get(t, 0) for t in all_terms)
        mag1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
        mag2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        
        return dot_product / (mag1 * mag2)
    
    def clear(self) -> None:
        """Clear all documents."""
        self.documents.clear()
        self.doc_tokens.clear()
        self.idf_cache.clear()
        self._dirty = True


# =============================================================================
# Longest Common Subsequence
# =============================================================================

def lcs_length(s1: str, s2: str, case_sensitive: bool = True) -> int:
    """
    Calculate the length of the Longest Common Subsequence.
    
    Args:
        s1: First string
        s2: Second string
        case_sensitive: Whether to consider case
    
    Returns:
        Length of LCS
    
    Example:
        >>> lcs_length("ABCBDAB", "BDCABA")
        4
    """
    if not case_sensitive:
        s1 = s1.lower()
        s2 = s2.lower()
    
    m, n = len(s1), len(s2)
    
    if m == 0 or n == 0:
        return 0
    
    # Use two rows for space optimization
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev, curr = curr, prev
    
    return prev[n]


def lcs(s1: str, s2: str, case_sensitive: bool = True) -> str:
    """
    Find the Longest Common Subsequence string.
    
    Args:
        s1: First string
        s2: Second string
        case_sensitive: Whether to consider case
    
    Returns:
        LCS string
    
    Example:
        >>> lcs("ABCBDAB", "BDCABA")
        'BCBA'
    """
    if not case_sensitive:
        original_s1 = s1
        s1 = s1.lower()
        s2 = s2.lower()
    
    m, n = len(s1), len(s2)
    
    if m == 0 or n == 0:
        return ""
    
    # Build DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # Backtrack to find LCS
    result = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            result.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    
    return ''.join(reversed(result))


def lcs_ratio(s1: str, s2: str, case_sensitive: bool = True) -> float:
    """
    Calculate LCS-based similarity ratio.
    
    Ratio = LCS_length / max(len(s1), len(s2))
    
    Args:
        s1: First string
        s2: Second string
        case_sensitive: Whether to consider case
    
    Returns:
        Similarity ratio between 0.0 and 1.0
    """
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    
    lcs_len = lcs_length(s1, s2, case_sensitive)
    max_len = max(len(s1), len(s2))
    return lcs_len / max_len


# =============================================================================
# N-Gram Similarity
# =============================================================================

def ngram_similarity(s1: str, s2: str, n: int = 2, 
                     case_sensitive: bool = True) -> float:
    """
    Calculate n-gram based similarity.
    
    Similar to Jaccard but uses n-grams instead of single characters.
    
    Args:
        s1: First string
        s2: Second string
        n: N-gram size (default 2)
        case_sensitive: Whether to consider case
    
    Returns:
        Similarity between 0.0 and 1.0
    
    Example:
        >>> ngram_similarity("hello", "hallo", n=2)
        0.6
    """
    if not case_sensitive:
        s1 = s1.lower()
        s2 = s2.lower()
    
    if s1 == s2:
        return 1.0
    
    if len(s1) < n or len(s2) < n:
        # Fall back to character comparison for short strings
        if len(s1) == 0 and len(s2) == 0:
            return 1.0
        if len(s1) == 0 or len(s2) == 0:
            return 0.0
        # Use character set comparison
        return len(set(s1) & set(s2)) / len(set(s1) | set(s2))
    
    ngrams1 = set(s1[i:i + n] for i in range(len(s1) - n + 1))
    ngrams2 = set(s2[i:i + n] for i in range(len(s2) - n + 1))
    
    if not ngrams1 and not ngrams2:
        return 1.0
    
    intersection = ngrams1 & ngrams2
    union = ngrams1 | ngrams2
    
    return len(intersection) / len(union) if union else 0.0


# =============================================================================
# Phonetic Similarity
# =============================================================================

def soundex(text: str) -> str:
    """
    Generate Soundex code for a string.
    
    Soundex is a phonetic algorithm for indexing names by sound.
    
    Args:
        text: Input string
    
    Returns:
        Soundex code (4 characters)
    
    Example:
        >>> soundex("Robert")
        'R163'
        >>> soundex("Rupert")
        'R163'
    """
    if not text:
        return "0000"
    
    text = text.upper()
    
    # Soundex letter mapping
    mapping = {
        'B': '1', 'F': '1', 'P': '1', 'V': '1',
        'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
        'D': '3', 'T': '3',
        'L': '4',
        'M': '5', 'N': '5',
        'R': '6',
        'A': '0', 'E': '0', 'I': '0', 'O': '0', 'U': '0', 'H': '0', 'W': '0', 'Y': '0'
    }
    
    # Keep first letter
    first = text[0]
    
    # Encode remaining letters
    encoded = []
    prev_code = mapping.get(first, '0')
    
    for char in text[1:]:
        code = mapping.get(char, '0')
        if code != '0' and code != prev_code:
            encoded.append(code)
        prev_code = code
    
    # Pad or truncate to 4 characters
    result = first + ''.join(encoded) + '000'
    return result[:4]


def metaphone(text: str) -> str:
    """
    Generate Metaphone code for a string.
    
    Metaphone is a phonetic algorithm that accounts for variations in spelling.
    
    Args:
        text: Input string
    
    Returns:
        Metaphone code
    
    Example:
        >>> metaphone("Smith")
        'SM0T'
        >>> metaphone("Schmidt")
        'SMTT'
    """
    if not text:
        return ""
    
    word = text.upper()
    result = []
    i = 0
    length = len(word)
    
    # Handle initial letter combinations
    if word.startswith(('KN', 'GN', 'PN', 'AE', 'WR')):
        i = 1
    elif word.startswith('WH'):
        result.append('W')
        i = 2
    elif word.startswith('X'):
        result.append('S')
        i = 1
    
    while i < length:
        char = word[i]
        next_char = word[i + 1] if i + 1 < length else ''
        prev_char = word[i - 1] if i > 0 else ''
        
        # Skip vowels (except at start)
        if char in 'AEIOU':
            if i == 0:
                result.append(char)
            i += 1
            continue
        
        # Consonant rules
        if char == 'B':
            if not (i + 1 < length and word[i + 1] == 'B'):
                if i + 1 >= length or word[i + 1] != '-':
                    result.append('B')
            else:
                result.append('B')
                i += 1
        elif char == 'C':
            if next_char == 'H':
                result.append('X')
                i += 1
            elif next_char in 'IEY':
                result.append('S')
            else:
                result.append('K')
        elif char == 'D':
            if next_char == 'G' and (i + 2 < length and word[i + 2] in 'IEY'):
                result.append('J')
                i += 1
            else:
                result.append('T')
        elif char == 'F':
            result.append('F')
        elif char == 'G':
            if next_char == 'H':
                if i + 2 < length and word[i + 2] not in 'AEIOU':
                    i += 1
                else:
                    result.append('F')
                    i += 1
            elif next_char in 'IEY':
                result.append('J')
            elif next_char == 'N':
                i += 1  # Silent G before N
            else:
                result.append('K')
        elif char == 'H':
            if prev_char not in 'CSPTG' and next_char in 'AEIOU':
                result.append('H')
        elif char == 'J':
            result.append('J')
        elif char == 'K':
            result.append('K')
        elif char == 'L':
            result.append('L')
        elif char == 'M':
            result.append('M')
        elif char == 'N':
            result.append('N')
        elif char == 'P':
            if next_char == 'H':
                result.append('F')
                i += 1
            else:
                result.append('P')
        elif char == 'Q':
            result.append('K')
        elif char == 'R':
            result.append('R')
        elif char == 'S':
            if next_char == 'H':
                result.append('X')
                i += 1
            elif next_char == 'C' and i + 2 < length and word[i + 2] == 'H':
                result.append('X')
                i += 2
            else:
                result.append('S')
        elif char == 'T':
            if next_char == 'H':
                result.append('0')  # TH sound
                i += 1
            elif next_char == 'I' and i + 2 < length and word[i + 2] in 'AO':
                result.append('X')
            else:
                result.append('T')
        elif char == 'V':
            result.append('F')
        elif char == 'W':
            if next_char in 'AEIOU':
                result.append('W')
        elif char == 'X':
            result.append('KS')
        elif char == 'Y':
            if next_char in 'AEIOU':
                result.append('Y')
        elif char == 'Z':
            result.append('S')
        
        i += 1
    
    return ''.join(result)


def phonetic_similarity(s1: str, s2: str, algorithm: str = 'soundex') -> float:
    """
    Calculate phonetic similarity between two strings.
    
    Args:
        s1: First string
        s2: Second string
        algorithm: 'soundex' or 'metaphone' (default 'soundex')
    
    Returns:
        1.0 if codes match, 0.0 otherwise
    
    Example:
        >>> phonetic_similarity("Robert", "Rupert")
        1.0
    """
    if algorithm == 'soundex':
        code1 = soundex(s1)
        code2 = soundex(s2)
    elif algorithm == 'metaphone':
        code1 = metaphone(s1)
        code2 = metaphone(s2)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")
    
    return 1.0 if code1 == code2 else 0.0


# =============================================================================
# Fuzzy Matching Utilities
# =============================================================================

def find_best_match(query: str, choices: List[str], 
                   similarity_func: Callable[[str, str], float] = None,
                   threshold: float = 0.0) -> Tuple[str, float]:
    """
    Find the best matching string from a list of choices.
    
    Args:
        query: String to match
        choices: List of candidate strings
        similarity_func: Similarity function (default: jaro_winkler_similarity)
        threshold: Minimum similarity threshold
    
    Returns:
        Tuple of (best_match, similarity_score)
    
    Example:
        >>> find_best_match("appel", ["apple", "orange", "banana"])
        ('apple', 0.96...)
    """
    if similarity_func is None:
        similarity_func = jaro_winkler_similarity
    
    if not choices:
        return ("", 0.0)
    
    best_match = choices[0]
    best_score = similarity_func(query, best_match)
    
    for choice in choices[1:]:
        score = similarity_func(query, choice)
        if score > best_score:
            best_score = score
            best_match = choice
    
    if best_score < threshold:
        return ("", 0.0)
    
    return (best_match, best_score)


def find_all_matches(query: str, choices: List[str],
                    similarity_func: Callable[[str, str], float] = None,
                    threshold: float = 0.6) -> List[Tuple[str, float]]:
    """
    Find all strings matching above a threshold.
    
    Args:
        query: String to match
        choices: List of candidate strings
        similarity_func: Similarity function (default: jaro_winkler_similarity)
        threshold: Minimum similarity threshold
    
    Returns:
        List of (match, score) tuples sorted by score descending
    
    Example:
        >>> find_all_matches("aple", ["apple", "apple pie", "orange"], threshold=0.5)
        [('apple', 0.96...), ('apple pie', 0.78...)]
    """
    if similarity_func is None:
        similarity_func = jaro_winkler_similarity
    
    matches = []
    for choice in choices:
        score = similarity_func(query, choice)
        if score >= threshold:
            matches.append((choice, score))
    
    return sorted(matches, key=lambda x: x[1], reverse=True)


def fuzzy_search(query: str, text: str, 
                similarity_func: Callable[[str, str], float] = None,
                threshold: float = 0.7,
                min_word_length: int = 2) -> List[Tuple[int, int, str, float]]:
    """
    Search for fuzzy matches of query within text.
    
    Args:
        query: Query string
        text: Text to search in
        similarity_func: Similarity function
        threshold: Minimum similarity threshold
        min_word_length: Minimum word length to consider
    
    Returns:
        List of (start_pos, end_pos, matched_text, score) tuples
    
    Example:
        >>> fuzzy_search("apple", "I like appel pie", threshold=0.6)
        [(7, 12, 'appel', 0.933...)]
    """
    if similarity_func is None:
        similarity_func = jaro_winkler_similarity
    
    # Tokenize text
    words = re.finditer(r'\b\w+\b', text)
    matches = []
    
    query_len = len(query)
    
    for match in words:
        word = match.group()
        if len(word) < min_word_length:
            continue
        
        score = similarity_func(query, word)
        if score >= threshold:
            matches.append((
                match.start(),
                match.end(),
                word,
                score
            ))
    
    return sorted(matches, key=lambda x: x[3], reverse=True)


# =============================================================================
# Combined/Composite Similarity
# =============================================================================

def combined_similarity(s1: str, s2: str, 
                       weights: Dict[str, float] = None,
                       case_sensitive: bool = True) -> float:
    """
    Calculate combined similarity using multiple algorithms.
    
    Args:
        s1: First string
        s2: Second string
        weights: Weights for each algorithm (default: equal weights)
                 Keys: 'levenshtein', 'jaro_winkler', 'jaccard', 'cosine'
        case_sensitive: Whether to consider case
    
    Returns:
        Weighted average similarity
    
    Example:
        >>> combined_similarity("hello", "hallo")
        0.84...
    """
    if weights is None:
        weights = {
            'levenshtein': 0.3,
            'jaro_winkler': 0.3,
            'jaccard': 0.2,
            'cosine': 0.2
        }
    
    scores = {
        'levenshtein': levenshtein_ratio(s1, s2, case_sensitive),
        'jaro_winkler': jaro_winkler_similarity(s1, s2, case_sensitive=case_sensitive),
        'jaccard': jaccard_similarity(s1, s2, case_sensitive=case_sensitive),
        'cosine': cosine_similarity(s1, s2, case_sensitive=case_sensitive)
    }
    
    total_weight = sum(weights.values())
    weighted_sum = sum(weights.get(k, 0) * v for k, v in scores.items())
    
    return weighted_sum / total_weight if total_weight > 0 else 0.0


def compare_strings(s1: str, s2: str, case_sensitive: bool = True) -> Dict[str, float]:
    """
    Compare two strings using all available similarity metrics.
    
    Args:
        s1: First string
        s2: Second string
        case_sensitive: Whether to consider case
    
    Returns:
        Dictionary of all similarity scores
    
    Example:
        >>> compare_strings("hello", "hallo")
        {'levenshtein': 0.8, 'damerau_levenshtein': 0.8, 'jaro': 0.84..., ...}
    """
    return {
        'levenshtein': levenshtein_ratio(s1, s2, case_sensitive),
        'damerau_levenshtein': 1.0 - damerau_levenshtein_distance(s1, s2, case_sensitive) / max(len(s1), len(s2), 1),
        'jaro': jaro_similarity(s1, s2, case_sensitive),
        'jaro_winkler': jaro_winkler_similarity(s1, s2, case_sensitive=case_sensitive),
        'jaccard_char': jaccard_similarity(s1, s2, 1, case_sensitive),
        'jaccard_bigram': jaccard_similarity(s1, s2, 2, case_sensitive),
        'dice': dice_coefficient(s1, s2, case_sensitive=case_sensitive),
        'cosine_bigram': cosine_similarity(s1, s2, case_sensitive=case_sensitive),
        'cosine_word': cosine_similarity_words(s1, s2, case_sensitive),
        'lcs': lcs_ratio(s1, s2, case_sensitive),
        'ngram': ngram_similarity(s1, s2, case_sensitive=case_sensitive),
        'combined': combined_similarity(s1, s2, case_sensitive=case_sensitive),
        'soundex_match': phonetic_similarity(s1, s2, 'soundex'),
        'metaphone_match': phonetic_similarity(s1, s2, 'metaphone'),
    }


# =============================================================================
# Utility Functions
# =============================================================================

def normalized_levenshtein(s1: str, s2: str, case_sensitive: bool = True) -> float:
    """
    Alias for levenshtein_ratio for API consistency.
    """
    return levenshtein_ratio(s1, s2, case_sensitive)


def similar(s1: str, s2: str, threshold: float = 0.7, 
           method: str = 'jaro_winkler') -> bool:
    """
    Check if two strings are similar above a threshold.
    
    Args:
        s1: First string
        s2: Second string
        threshold: Similarity threshold (0.0 to 1.0)
        method: Similarity method ('levenshtein', 'jaro', 'jaro_winkler', etc.)
    
    Returns:
        True if similarity >= threshold
    
    Example:
        >>> similar("hello", "hallo", threshold=0.8)
        False
        >>> similar("hello", "hallo", threshold=0.7)
        True
    """
    methods = {
        'levenshtein': levenshtein_ratio,
        'jaro': jaro_similarity,
        'jaro_winkler': jaro_winkler_similarity,
        'jaccard': lambda a, b: jaccard_similarity(a, b, case_sensitive=True),
        'dice': lambda a, b: dice_coefficient(a, b, case_sensitive=True),
        'cosine': lambda a, b: cosine_similarity(a, b, case_sensitive=True),
        'lcs': lcs_ratio,
    }
    
    if method not in methods:
        raise ValueError(f"Unknown method: {method}. Choose from: {list(methods.keys())}")
    
    score = methods[method](s1, s2)
    return score >= threshold


if __name__ == "__main__":
    # Demo
    print("Text Similarity Utilities Demo")
    print("=" * 50)
    
    s1, s2 = "hello", "hallo"
    print(f"\nComparing '{s1}' and '{s2}':")
    print(f"  Levenshtein distance: {levenshtein_distance(s1, s2)}")
    print(f"  Levenshtein ratio: {levenshtein_ratio(s1, s2):.3f}")
    print(f"  Jaro similarity: {jaro_similarity(s1, s2):.3f}")
    print(f"  Jaro-Winkler: {jaro_winkler_similarity(s1, s2):.3f}")
    print(f"  Jaccard: {jaccard_similarity(s1, s2):.3f}")
    print(f"  Dice: {dice_coefficient(s1, s2):.3f}")
    print(f"  LCS ratio: {lcs_ratio(s1, s2):.3f}")
    
    print(f"\nPhonetic comparison 'Robert' vs 'Rupert':")
    print(f"  Soundex: {soundex('Robert')} vs {soundex('Rupert')} - Match: {phonetic_similarity('Robert', 'Rupert')}")
    
    print(f"\nBest match for 'appel' in ['apple', 'orange', 'banana']:")
    match, score = find_best_match("appel", ["apple", "orange", "banana"])
    print(f"  {match} (score: {score:.3f})")