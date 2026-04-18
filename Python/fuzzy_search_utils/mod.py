"""
AllToolkit - Python Fuzzy Search Utilities

A zero-dependency, production-ready fuzzy string matching utility module.
Supports multiple algorithms: Levenshtein distance, n-gram similarity, soundex,
metaphone, Jaro-Winkler distance, and more.

Author: AllToolkit
License: MIT
"""

from typing import List, Tuple, Optional, Dict, Callable, Set
from dataclasses import dataclass
from functools import lru_cache
import re


@dataclass
class FuzzyMatch:
    """Represents a fuzzy match result."""
    value: str
    score: float
    algorithm: str
    original_query: str
    
    def __lt__(self, other: 'FuzzyMatch') -> bool:
        return self.score < other.score
    
    def __repr__(self) -> str:
        return f"FuzzyMatch(value='{self.value}', score={self.score:.3f}, algorithm='{self.algorithm}')"


# ============================================================================
# Distance Functions
# ============================================================================

def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculate the Levenshtein (edit) distance between two strings.
    
    The minimum number of single-character edits (insertions, deletions,
    or substitutions) required to change one string into the other.
    
    Args:
        s1: First string
        s2: Second string
    
    Returns:
        Edit distance (0 for identical strings)
    
    Example:
        >>> levenshtein_distance("kitten", "sitting")
        3
        >>> levenshtein_distance("", "abc")
        3
    """
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


def levenshtein_ratio(s1: str, s2: str) -> float:
    """
    Calculate the similarity ratio based on Levenshtein distance.
    
    Args:
        s1: First string
        s2: Second string
    
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
    
    distance = levenshtein_distance(s1, s2)
    max_len = max(len(s1), len(s2))
    return 1.0 - (distance / max_len)


def damerau_levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculate the Damerau-Levenshtein distance.
    
    Like Levenshtein but also allows transposition of adjacent characters.
    
    Args:
        s1: First string
        s2: Second string
    
    Returns:
        Edit distance including transpositions
    
    Example:
        >>> damerau_levenshtein_distance("ca", "abc")
        2
        >>> damerau_levenshtein_distance("abc", "acb")  # transposition
        1
    """
    if len(s1) < len(s2):
        return damerau_levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    d = {}
    len1, len2 = len(s1), len(s2)
    
    for i in range(-1, len1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, len2 + 1):
        d[(-1, j)] = j + 1
    
    for i in range(len1):
        for j in range(len2):
            cost = 0 if s1[i] == s2[j] else 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,      # deletion
                d[(i, j - 1)] + 1,      # insertion
                d[(i - 1, j - 1)] + cost  # substitution
            )
            if i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[(i - 2, j - 2)] + cost)  # transposition
    
    return d[(len1 - 1, len2 - 1)]


def hamming_distance(s1: str, s2: str) -> int:
    """
    Calculate the Hamming distance between two strings of equal length.
    
    Args:
        s1: First string
        s2: Second string
    
    Returns:
        Number of positions where characters differ
    
    Raises:
        ValueError: If strings have different lengths
    
    Example:
        >>> hamming_distance("karolin", "kathrin")
        3
    """
    if len(s1) != len(s2):
        raise ValueError("Strings must have equal length for Hamming distance")
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))


def jaro_distance(s1: str, s2: str) -> float:
    """
    Calculate the Jaro distance between two strings.
    
    Args:
        s1: First string
        s2: Second string
    
    Returns:
        Jaro distance between 0.0 and 1.0
    
    Example:
        >>> jaro_distance("MARTHA", "MARHTA")
        0.944...
    """
    if not s1 or not s2:
        return 0.0 if s1 != s2 else 1.0
    
    if s1 == s2:
        return 1.0
    
    len1, len2 = len(s1), len(s2)
    match_distance = max(len1, len2) // 2 - 1
    if match_distance < 0:
        match_distance = 0
    
    s1_matches = [False] * len1
    s2_matches = [False] * len2
    
    matches = 0
    transpositions = 0
    
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
    
    k = 0
    for i in range(len1):
        if not s1_matches[i]:
            continue
        while not s2_matches[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1
    
    jaro = ((matches / len1) + (matches / len2) + 
            ((matches - transpositions / 2) / matches)) / 3
    
    return jaro


def jaro_winkler_distance(s1: str, s2: str, scaling_factor: float = 0.1) -> float:
    """
    Calculate the Jaro-Winkler distance between two strings.
    
    Extends Jaro distance by giving extra weight to matching prefixes.
    
    Args:
        s1: First string
        s2: Second string
        scaling_factor: Weight given to prefix matches (default: 0.1)
    
    Returns:
        Jaro-Winkler distance between 0.0 and 1.0
    
    Example:
        >>> jaro_winkler_distance("MARTHA", "MARHTA")
        0.961...
    """
    jaro_sim = jaro_distance(s1, s2)
    
    # Find common prefix length (max 4)
    prefix_len = 0
    for i in range(min(len(s1), len(s2), 4)):
        if s1[i] == s2[i]:
            prefix_len += 1
        else:
            break
    
    return jaro_sim + prefix_len * scaling_factor * (1 - jaro_sim)


# ============================================================================
# N-gram Similarity
# ============================================================================

def get_ngrams(s: str, n: int = 2) -> Set[str]:
    """
    Generate n-grams from a string.
    
    Args:
        s: Input string
        n: Gram size (default: 2 for bigrams)
    
    Returns:
        Set of n-grams
    
    Example:
        >>> get_ngrams("hello", 2)
        {'he', 'el', 'll', 'lo'}
    """
    if len(s) < n:
        return {s} if s else set()
    return {s[i:i+n] for i in range(len(s) - n + 1)}


def ngram_similarity(s1: str, s2: str, n: int = 2) -> float:
    """
    Calculate n-gram based similarity between two strings.
    
    Uses Jaccard similarity on n-gram sets.
    
    Args:
        s1: First string
        s2: Second string
        n: Gram size (default: 2 for bigrams)
    
    Returns:
        Similarity between 0.0 and 1.0
    
    Example:
        >>> ngram_similarity("hello", "hallo")
        0.6
    """
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    
    ngrams1 = get_ngrams(s1.lower(), n)
    ngrams2 = get_ngrams(s2.lower(), n)
    
    if not ngrams1 and not ngrams2:
        return 1.0
    
    intersection = len(ngrams1 & ngrams2)
    union = len(ngrams1 | ngrams2)
    
    if union == 0:
        return 1.0 if intersection == 0 else 0.0
    
    return intersection / union


def dice_coefficient(s1: str, s2: str, n: int = 2) -> float:
    """
    Calculate Sørensen-Dice coefficient using n-grams.
    
    Args:
        s1: First string
        s2: Second string
        n: Gram size (default: 2)
    
    Returns:
        Dice coefficient between 0.0 and 1.0
    
    Example:
        >>> dice_coefficient("hello", "hallo")
        0.75
    """
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    
    ngrams1 = get_ngrams(s1.lower(), n)
    ngrams2 = get_ngrams(s2.lower(), n)
    
    if not ngrams1 or not ngrams2:
        return 0.0
    
    intersection = len(ngrams1 & ngrams2)
    return 2 * intersection / (len(ngrams1) + len(ngrams2))


# ============================================================================
# Phonetic Algorithms
# ============================================================================

def soundex(s: str) -> str:
    """
    Generate Soundex code for a string.
    
    Soundex encodes homophones to the same representation.
    
    Args:
        s: Input string
    
    Returns:
        4-character Soundex code
    
    Example:
        >>> soundex("Robert")
        'R163'
        >>> soundex("Rupert")
        'R163'
    """
    if not s:
        return "0000"
    
    s = s.upper()
    s = re.sub(r'[^A-Z]', '', s)
    
    if not s:
        return "0000"
    
    # Soundex letter mappings
    mappings = {
        'B': '1', 'F': '1', 'P': '1', 'V': '1',
        'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
        'D': '3', 'T': '3',
        'L': '4',
        'M': '5', 'N': '5',
        'R': '6',
        'A': '0', 'E': '0', 'I': '0', 'O': '0', 'U': '0', 'H': '0', 'W': '0', 'Y': '0'
    }
    
    first_letter = s[0]
    encoded = first_letter
    
    prev_code = mappings.get(first_letter, '0')
    
    for char in s[1:]:
        code = mappings.get(char, '0')
        if code != '0' and code != prev_code:
            encoded += code
        prev_code = code if code != '0' else prev_code
    
    # Pad or truncate to 4 characters
    encoded = encoded[:4].ljust(4, '0')
    return encoded


def metaphone(s: str) -> str:
    """
    Generate Metaphone code for a string.
    
    An improvement over Soundex for English words.
    
    Args:
        s: Input string
    
    Returns:
        Metaphone code
    
    Example:
        >>> metaphone("phone")
        'FN'
        >>> metaphone("fone")
        'FN'
    """
    if not s:
        return ""
    
    s = s.upper()
    s = re.sub(r'[^A-Z]', '', s)
    
    if not s:
        return ""
    
    result = []
    i = 0
    length = len(s)
    
    while i < length:
        char = s[i]
        next_char = s[i + 1] if i + 1 < length else ''
        prev_char = s[i - 1] if i > 0 else ''
        
        # Skip duplicate letters except C
        if char == prev_char and char != 'C':
            i += 1
            continue
        
        if char in 'AEIOU':
            if i == 0:
                result.append(char)
            i += 1
            continue
        
        if char == 'B':
            if not (i == length - 1 and prev_char == 'M'):
                result.append('B')
            i += 1
            continue
        
        if char == 'C':
            if next_char == 'H':
                result.append('X')
                i += 2
            elif next_char in 'IEY':
                result.append('S')
                i += 1
            else:
                result.append('K')
                i += 1
            continue
        
        if char == 'D':
            if next_char == 'G' and (i + 2 < length and s[i + 2] in 'IEY'):
                result.append('J')
                i += 2
            else:
                result.append('T')
                i += 1
            continue
        
        if char == 'F':
            result.append('F')
            i += 1
            continue
        
        if char == 'G':
            if next_char == 'H':
                if i + 2 < length and s[i + 2] not in 'AEIOU':
                    i += 2
                else:
                    result.append('F')
                    i += 2
            elif next_char in 'IEY':
                result.append('J')
                i += 1
            elif next_char == 'N':
                i += 1
            else:
                result.append('K')
                i += 1
            continue
        
        if char == 'H':
            if prev_char not in 'CSPTG' and next_char in 'AEIOU':
                result.append('H')
            i += 1
            continue
        
        if char == 'J':
            result.append('J')
            i += 1
            continue
        
        if char == 'K':
            if prev_char != 'C':
                result.append('K')
            i += 1
            continue
        
        if char == 'L':
            result.append('L')
            i += 1
            continue
        
        if char == 'M':
            result.append('M')
            i += 1
            continue
        
        if char == 'N':
            result.append('N')
            i += 1
            continue
        
        if char == 'P':
            if next_char == 'H':
                result.append('F')
                i += 2
            else:
                result.append('P')
                i += 1
            continue
        
        if char == 'Q':
            result.append('K')
            i += 1
            continue
        
        if char == 'R':
            result.append('R')
            i += 1
            continue
        
        if char == 'S':
            if next_char == 'H':
                result.append('X')
                i += 2
            elif next_char == 'C' and i + 2 < length and s[i + 2] == 'H':
                result.append('X')
                i += 3
            else:
                result.append('S')
                i += 1
            continue
        
        if char == 'T':
            if next_char == 'H':
                result.append('0')  # TH
                i += 2
            elif next_char == 'I' and i + 2 < length and s[i + 2] == 'O':
                result.append('X')
                i += 3
            else:
                result.append('T')
                i += 1
            continue
        
        if char == 'V':
            result.append('F')
            i += 1
            continue
        
        if char == 'W':
            if next_char in 'AEIOU':
                result.append('W')
            i += 1
            continue
        
        if char == 'X':
            result.append('KS')
            i += 1
            continue
        
        if char == 'Y':
            if next_char in 'AEIOU':
                result.append('Y')
            i += 1
            continue
        
        if char == 'Z':
            result.append('S')
            i += 1
            continue
        
        i += 1
    
    return ''.join(result).replace('0', '')


def double_metaphone(s: str) -> Tuple[str, str]:
    """
    Generate Double Metaphone code for a string.
    
    Returns primary and alternate encodings.
    
    Args:
        s: Input string
    
    Returns:
        Tuple of (primary_code, alternate_code)
    
    Example:
        >>> double_metaphone("Smith")
        ('SM0T', 'XMT')
    """
    # Simplified Double Metaphone - returns primary and alternate
    primary = metaphone(s)
    alternate = _alternate_metaphone(s)
    return (primary, alternate)


def _alternate_metaphone(s: str) -> str:
    """Generate alternate metaphone encoding."""
    # Simplified - just use standard metaphone with different rules
    if not s:
        return ""
    
    s = s.upper()
    s = re.sub(r'[^A-Z]', '', s)
    
    if not s:
        return ""
    
    # Different vowel handling for alternate
    result = []
    for i, char in enumerate(s):
        if char in 'AEIOU':
            if i == 0:
                result.append(char)
        elif char in 'BP':
            result.append('P')
        elif char in 'CKQ':
            result.append('K')
        elif char in 'DT':
            result.append('T')
        elif char in 'LR':
            result.append(char)
        elif char in 'MN':
            result.append(char)
        elif char in 'FS':
            result.append('S')
        elif char in 'GJ':
            result.append('J')
        elif char == 'H':
            result.append('H')
        elif char in 'VW':
            result.append('W')
        elif char == 'X':
            result.append('KS')
        elif char == 'Y':
            result.append('Y')
        elif char == 'Z':
            result.append('S')
    
    return ''.join(result).replace('0', '')[:4]


def phonetic_similarity(s1: str, s2: str) -> float:
    """
    Calculate phonetic similarity between two strings.
    
    Compares Soundex and Metaphone encodings.
    
    Args:
        s1: First string
        s2: Second string
    
    Returns:
        Similarity between 0.0 and 1.0
    
    Example:
        >>> phonetic_similarity("Robert", "Rupert")
        1.0
    """
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    
    s1_soundex = soundex(s1)
    s2_soundex = soundex(s2)
    s1_meta = metaphone(s1)
    s2_meta = metaphone(s2)
    
    soundex_match = 1.0 if s1_soundex == s2_soundex else 0.0
    meta_match = 1.0 if s1_meta == s2_meta else 0.0
    
    # Combine both scores
    return (soundex_match + meta_match) / 2


# ============================================================================
# Search Functions
# ============================================================================

def fuzzy_search(
    query: str,
    candidates: List[str],
    algorithm: str = "levenshtein",
    threshold: float = 0.6,
    limit: Optional[int] = None,
    case_sensitive: bool = False,
) -> List[FuzzyMatch]:
    """
    Search for fuzzy matches in a list of candidates.
    
    Args:
        query: Search query
        candidates: List of candidate strings
        algorithm: Similarity algorithm (levenshtein, jaro, jaro_winkler, ngram, dice, phonetic)
        threshold: Minimum similarity threshold (default: 0.6)
        limit: Maximum number of results (default: None = all matches)
        case_sensitive: Case-sensitive comparison (default: False)
    
    Returns:
        List of FuzzyMatch objects sorted by score (descending)
    
    Example:
        >>> fuzzy_search("hello", ["hallo", "hello", "hell", "help"], threshold=0.7)
        [FuzzyMatch(value='hello', score=1.000, ...), ...]
    """
    if not query or not candidates:
        return []
    
    # Select similarity function
    similarity_funcs = {
        "levenshtein": levenshtein_ratio,
        "jaro": jaro_distance,
        "jaro_winkler": jaro_winkler_distance,
        "ngram": ngram_similarity,
        "dice": dice_coefficient,
        "phonetic": phonetic_similarity,
    }
    
    if algorithm not in similarity_funcs:
        raise ValueError(f"Unknown algorithm: {algorithm}. "
                        f"Available: {list(similarity_funcs.keys())}")
    
    similarity_func = similarity_funcs[algorithm]
    
    q = query if case_sensitive else query.lower()
    
    matches = []
    for candidate in candidates:
        c = candidate if case_sensitive else candidate.lower()
        score = similarity_func(q, c)
        
        if score >= threshold:
            matches.append(FuzzyMatch(
                value=candidate,
                score=score,
                algorithm=algorithm,
                original_query=query,
            ))
    
    # Sort by score descending
    matches.sort(key=lambda m: m.score, reverse=True)
    
    if limit:
        matches = matches[:limit]
    
    return matches


def fuzzy_find(
    query: str,
    candidates: List[str],
    threshold: float = 0.6,
    algorithm: str = "levenshtein",
) -> Optional[str]:
    """
    Find the best fuzzy match for a query.
    
    Args:
        query: Search query
        candidates: List of candidate strings
        threshold: Minimum similarity threshold (default: 0.6)
        algorithm: Similarity algorithm (default: levenshtein)
    
    Returns:
        Best matching string or None if no match above threshold
    
    Example:
        >>> fuzzy_find("hello", ["hallo", "hello", "hell"])
        'hello'
    """
    matches = fuzzy_search(query, candidates, algorithm=algorithm, 
                          threshold=threshold, limit=1)
    return matches[0].value if matches else None


def extract_best(
    query: str,
    candidates: List[str],
    algorithm: str = "levenshtein",
    case_sensitive: bool = False,
) -> Tuple[str, float]:
    """
    Extract the best match regardless of threshold.
    
    Args:
        query: Search query
        candidates: List of candidate strings
        algorithm: Similarity algorithm (default: levenshtein)
        case_sensitive: Case-sensitive comparison (default: False)
    
    Returns:
        Tuple of (best_match, score)
    
    Example:
        >>> extract_best("hello", ["hallo", "help", "hi"])
        ('hallo', 0.8)
    """
    if not candidates:
        return ("", 0.0)
    
    matches = fuzzy_search(query, candidates, algorithm=algorithm,
                          threshold=0.0, limit=1, case_sensitive=case_sensitive)
    return (matches[0].value, matches[0].score) if matches else (candidates[0], 0.0)


def extract_top_n(
    query: str,
    candidates: List[str],
    n: int = 5,
    algorithm: str = "levenshtein",
    threshold: float = 0.0,
) -> List[Tuple[str, float]]:
    """
    Extract top N matches.
    
    Args:
        query: Search query
        candidates: List of candidate strings
        n: Number of results (default: 5)
        algorithm: Similarity algorithm (default: levenshtein)
        threshold: Minimum similarity threshold (default: 0.0)
    
    Returns:
        List of (match, score) tuples sorted by score descending
    
    Example:
        >>> extract_top_n("hello", ["hallo", "help", "hi", "hello"], n=3)
        [('hello', 1.0), ('hallo', 0.8), ('help', 0.6)]
    """
    matches = fuzzy_search(query, candidates, algorithm=algorithm,
                          threshold=threshold, limit=n)
    return [(m.value, m.score) for m in matches]


# ============================================================================
# Advanced Matching
# ============================================================================

def partial_ratio(s1: str, s2: str) -> float:
    """
    Calculate the best partial match ratio.
    
    Useful when comparing strings of very different lengths.
    
    Args:
        s1: First string
        s2: Second string
    
    Returns:
        Best partial match ratio between 0.0 and 1.0
    
    Example:
        >>> partial_ratio("hello", "hello world")
        1.0
    """
    if not s1 or not s2:
        return 0.0 if s1 != s2 else 1.0
    
    s1, s2 = s1.lower(), s2.lower()
    
    if s1 in s2 or s2 in s1:
        return 1.0
    
    shorter, longer = (s1, s2) if len(s1) < len(s2) else (s2, s1)
    
    best_ratio = 0.0
    window_size = len(shorter)
    
    for i in range(len(longer) - window_size + 1):
        substring = longer[i:i + window_size]
        ratio = levenshtein_ratio(shorter, substring)
        best_ratio = max(best_ratio, ratio)
    
    return best_ratio


def token_sort_ratio(s1: str, s2: str) -> float:
    """
    Calculate similarity after sorting tokens.
    
    Useful for matching strings with different word orders.
    
    Args:
        s1: First string
        s2: Second string
    
    Returns:
        Similarity ratio between 0.0 and 1.0
    
    Example:
        >>> token_sort_ratio("hello world", "world hello")
        1.0
    """
    tokens1 = sorted(s1.lower().split())
    tokens2 = sorted(s2.lower().split())
    
    sorted_s1 = ' '.join(tokens1)
    sorted_s2 = ' '.join(tokens2)
    
    return levenshtein_ratio(sorted_s1, sorted_s2)


def token_set_ratio(s1: str, s2: str) -> float:
    """
    Calculate similarity using token sets.
    
    Ignores duplicate words and word order.
    
    Args:
        s1: First string
        s2: Second string
    
    Returns:
        Similarity ratio between 0.0 and 1.0
    
    Example:
        >>> token_set_ratio("hello hello world", "world hello")
        1.0
    """
    tokens1 = set(s1.lower().split())
    tokens2 = set(s2.lower().split())
    
    if not tokens1 and not tokens2:
        return 1.0
    if not tokens1 or not tokens2:
        return 0.0
    
    # Common tokens
    common = tokens1 & tokens2
    # Unique to each
    unique1 = tokens1 - tokens2
    unique2 = tokens2 - tokens1
    
    if not unique1 and not unique2:
        return 1.0
    
    # Compare common + unique portions
    sorted_common = sorted(common)
    sorted_unique1 = sorted(unique1)
    sorted_unique2 = sorted(unique2)
    
    combined1 = ' '.join(sorted_common + sorted_unique1)
    combined2 = ' '.join(sorted_common + sorted_unique2)
    
    return levenshtein_ratio(combined1, combined2)


def weighted_ratio(
    s1: str,
    s2: str,
    weights: Optional[Dict[str, float]] = None,
) -> float:
    """
    Calculate weighted combination of multiple similarity metrics.
    
    Args:
        s1: First string
        s2: Second string
        weights: Weights for each algorithm (default: balanced weights)
    
    Returns:
        Weighted similarity ratio between 0.0 and 1.0
    
    Example:
        >>> weighted_ratio("hello world", "hallo world")
        0.91...
    """
    if weights is None:
        weights = {
            'levenshtein': 0.3,
            'jaro_winkler': 0.3,
            'token_sort': 0.2,
            'partial': 0.2,
        }
    
    total_weight = sum(weights.values())
    weighted_sum = 0.0
    
    for algo, weight in weights.items():
        if algo == 'levenshtein':
            score = levenshtein_ratio(s1, s2)
        elif algo == 'jaro_winkler':
            score = jaro_winkler_distance(s1, s2)
        elif algo == 'token_sort':
            score = token_sort_ratio(s1, s2)
        elif algo == 'partial':
            score = partial_ratio(s1, s2)
        elif algo == 'ngram':
            score = ngram_similarity(s1, s2)
        elif algo == 'phonetic':
            score = phonetic_similarity(s1, s2)
        else:
            continue
        
        weighted_sum += score * weight
    
    return weighted_sum / total_weight if total_weight > 0 else 0.0


# ============================================================================
# FuzzyMatcher Class
# ============================================================================

class FuzzyMatcher:
    """
    A configurable fuzzy matcher for repeated searches.
    
    Supports indexing candidates for faster repeated searches.
    
    Example:
        >>> matcher = FuzzyMatcher(["apple", "banana", "orange"])
        >>> matcher.search("aple", threshold=0.7)
        [FuzzyMatch(value='apple', score=0.8, ...)]
    """
    
    def __init__(
        self,
        candidates: Optional[List[str]] = None,
        algorithm: str = "levenshtein",
        case_sensitive: bool = False,
    ):
        """
        Initialize the fuzzy matcher.
        
        Args:
            candidates: Initial list of candidates
            algorithm: Default similarity algorithm
            case_sensitive: Case-sensitive comparison
        """
        self._candidates: List[str] = []
        self._algorithm = algorithm
        self._case_sensitive = case_sensitive
        self._index: Dict[str, Set[int]] = {}  # n-gram index
        
        if candidates:
            self.add_candidates(candidates)
    
    def add_candidates(self, candidates: List[str]) -> None:
        """Add candidates to the matcher."""
        start_idx = len(self._candidates)
        self._candidates.extend(candidates)
        
        # Build n-gram index
        for i, candidate in enumerate(candidates):
            idx = start_idx + i
            c = candidate if self._case_sensitive else candidate.lower()
            ngrams = get_ngrams(c, 2)
            for ngram in ngrams:
                if ngram not in self._index:
                    self._index[ngram] = set()
                self._index[ngram].add(idx)
    
    def add_candidate(self, candidate: str) -> None:
        """Add a single candidate."""
        self.add_candidates([candidate])
    
    def remove_candidate(self, candidate: str) -> bool:
        """Remove a candidate. Returns True if found and removed."""
        c = candidate if self._case_sensitive else candidate.lower()
        
        for i, existing in enumerate(self._candidates):
            existing_c = existing if self._case_sensitive else existing.lower()
            if existing_c == c:
                # Remove from candidates
                self._candidates.pop(i)
                # Rebuild index (simpler than incremental update)
                self._rebuild_index()
                return True
        
        return False
    
    def _rebuild_index(self) -> None:
        """Rebuild the n-gram index."""
        self._index = {}
        for i, candidate in enumerate(self._candidates):
            c = candidate if self._case_sensitive else candidate.lower()
            ngrams = get_ngrams(c, 2)
            for ngram in ngrams:
                if ngram not in self._index:
                    self._index[ngram] = set()
                self._index[ngram].add(i)
    
    def search(
        self,
        query: str,
        threshold: float = 0.6,
        limit: Optional[int] = None,
        algorithm: Optional[str] = None,
        use_index: bool = True,
    ) -> List[FuzzyMatch]:
        """
        Search for fuzzy matches.
        
        Args:
            query: Search query
            threshold: Minimum similarity threshold
            limit: Maximum number of results
            algorithm: Override default algorithm
            use_index: Use n-gram index for pre-filtering (faster for large datasets)
        
        Returns:
            List of FuzzyMatch objects
        """
        algo = algorithm or self._algorithm
        
        if not use_index or not self._index:
            return fuzzy_search(
                query, self._candidates, algorithm=algo,
                threshold=threshold, limit=limit,
                case_sensitive=self._case_sensitive,
            )
        
        # Use index to pre-filter candidates
        q = query if self._case_sensitive else query.lower()
        query_ngrams = get_ngrams(q, 2)
        
        # Find candidate indices that share at least one n-gram
        candidate_indices: Set[int] = set()
        for ngram in query_ngrams:
            if ngram in self._index:
                candidate_indices.update(self._index[ngram])
        
        # Filter and score candidates
        matches = []
        for idx in candidate_indices:
            candidate = self._candidates[idx]
            c = candidate if self._case_sensitive else candidate.lower()
            score = self._get_similarity(q, c, algo)
            
            if score >= threshold:
                matches.append(FuzzyMatch(
                    value=candidate,
                    score=score,
                    algorithm=algo,
                    original_query=query,
                ))
        
        # Sort and limit
        matches.sort(key=lambda m: m.score, reverse=True)
        if limit:
            matches = matches[:limit]
        
        return matches
    
    def _get_similarity(self, s1: str, s2: str, algorithm: str) -> float:
        """Get similarity using the specified algorithm."""
        funcs = {
            "levenshtein": levenshtein_ratio,
            "jaro": jaro_distance,
            "jaro_winkler": jaro_winkler_distance,
            "ngram": ngram_similarity,
            "dice": dice_coefficient,
            "phonetic": phonetic_similarity,
        }
        return funcs[algorithm](s1, s2)
    
    def find(self, query: str, threshold: float = 0.6) -> Optional[str]:
        """Find the best match above threshold."""
        matches = self.search(query, threshold=threshold, limit=1)
        return matches[0].value if matches else None
    
    def clear(self) -> None:
        """Clear all candidates."""
        self._candidates = []
        self._index = {}
    
    @property
    def candidates(self) -> List[str]:
        """Get list of candidates."""
        return self._candidates.copy()
    
    @property
    def count(self) -> int:
        """Get number of candidates."""
        return len(self._candidates)


# ============================================================================
# Utility Functions
# ============================================================================

def deduplicate(
    strings: List[str],
    threshold: float = 0.9,
    algorithm: str = "levenshtein",
) -> List[List[str]]:
    """
    Group similar strings together.
    
    Args:
        strings: List of strings to deduplicate
        threshold: Similarity threshold for grouping
        algorithm: Similarity algorithm
    
    Returns:
        List of groups of similar strings
    
    Example:
        >>> deduplicate(["hello", "hallo", "hi", "hey"], threshold=0.7)
        [['hello', 'hallo'], ['hi'], ['hey']]
    """
    if not strings:
        return []
    
    groups: List[List[str]] = []
    used: Set[int] = set()
    
    for i, s1 in enumerate(strings):
        if i in used:
            continue
        
        group = [s1]
        used.add(i)
        
        for j, s2 in enumerate(strings[i + 1:], i + 1):
            if j in used:
                continue
            
            similarity = fuzzy_search(s1, [s2], algorithm=algorithm, threshold=threshold)
            if similarity:
                group.append(s2)
                used.add(j)
        
        groups.append(group)
    
    return groups


def suggest_corrections(
    word: str,
    dictionary: List[str],
    max_suggestions: int = 5,
    threshold: float = 0.6,
) -> List[Tuple[str, float]]:
    """
    Suggest corrections for a possibly misspelled word.
    
    Args:
        word: Word to check
        dictionary: List of valid words
        max_suggestions: Maximum number of suggestions
        threshold: Minimum similarity threshold
    
    Returns:
        List of (suggestion, score) tuples
    
    Example:
        >>> suggest_corrections("appel", ["apple", "apply", "ape", "app"])
        [('apple', 0.8), ...]
    """
    return extract_top_n(word, dictionary, n=max_suggestions, 
                        algorithm="jaro_winkler", threshold=threshold)