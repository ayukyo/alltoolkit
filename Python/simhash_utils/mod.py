#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - SimHash Utilities Module
=====================================
A comprehensive SimHash (Similarity Hash) utility module with zero external dependencies.

SimHash is a locality-sensitive hashing technique used for:
    - Near-duplicate document detection
    - Web page deduplication
    - Code similarity detection
    - Quick document fingerprinting

Features:
    - SimHash generation from text using various tokenization strategies
    - Hamming distance calculation for fingerprint comparison
    - Similarity threshold detection
    - Multiple hash algorithms support (built-in)
    - Chinese text support with character/word tokenization
    - N-gram based tokenization
    - Batch processing capabilities
    - Index-based similarity search

Author: AllToolkit Contributors
License: MIT
"""

import hashlib
import re
import math
from typing import List, Dict, Tuple, Set, Optional, Union, Callable, Iterator
from collections import defaultdict
from functools import lru_cache


# =============================================================================
# Constants
# =============================================================================

DEFAULT_FINGERPRINT_SIZE = 64  # bits
DEFAULT_TOKENIZER = 'word'  # word, char, ngram
DEFAULT_NGRAM_SIZE = 3


# =============================================================================
# Core Hash Functions
# =============================================================================

def _murmur_like_hash(data: str, seed: int = 0) -> int:
    """
    A simple hash function similar to MurmurHash behavior.
    
    Uses Python's built-in hash with additional mixing for consistency
    across Python sessions (unlike Python's default hash which is randomized).
    
    Args:
        data: String to hash
        seed: Seed value for hashing
    
    Returns:
        64-bit hash value as integer
    """
    # Use SHA-256 and take first 8 bytes for a consistent 64-bit hash
    h = hashlib.sha256(f"{seed}:{data}".encode('utf-8'))
    return int.from_bytes(h.digest()[:8], 'big')


def _fnv1a_hash(data: str, seed: int = 0) -> int:
    """
    FNV-1a hash implementation.
    
    Args:
        data: String to hash
        seed: Initial hash value (FNV offset basis)
    
    Returns:
        Hash value as integer
    """
    # FNV-1a parameters for 64-bit
    FNV_PRIME = 0x100000001b3
    FNV_OFFSET = 0xcbf29ce484222325
    
    h = FNV_OFFSET ^ seed
    for byte in data.encode('utf-8'):
        h ^= byte
        h = (h * FNV_PRIME) & 0xFFFFFFFFFFFFFFFF
    return h


def hash_token(token: str, algorithm: str = 'sha256', size: int = 64) -> int:
    """
    Hash a token to a fixed-size integer.
    
    Args:
        token: Token string to hash
        algorithm: Hash algorithm ('sha256', 'md5', 'fnv1a', 'murmur')
        size: Desired output size in bits (32, 64, or 128)
    
    Returns:
        Hash value as integer
    
    Example:
        >>> h = hash_token("hello")
        >>> isinstance(h, int)
        True
    """
    if algorithm == 'sha256':
        h = hashlib.sha256(token.encode('utf-8'))
        byte_size = size // 8
        return int.from_bytes(h.digest()[:byte_size], 'big')
    elif algorithm == 'md5':
        h = hashlib.md5(token.encode('utf-8'))
        byte_size = size // 8
        return int.from_bytes(h.digest()[:byte_size], 'big')
    elif algorithm == 'fnv1a':
        return _fnv1a_hash(token) & ((1 << size) - 1)
    elif algorithm == 'murmur':
        return _murmur_like_hash(token) & ((1 << size) - 1)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")


# =============================================================================
# Tokenization Functions
# =============================================================================

def tokenize_words(text: str, 
                   lowercase: bool = True,
                   remove_punctuation: bool = True,
                   min_length: int = 1) -> List[str]:
    """
    Tokenize text into words.
    
    Args:
        text: Input text
        lowercase: Convert to lowercase
        remove_punctuation: Remove punctuation
        min_length: Minimum token length
    
    Returns:
        List of word tokens
    
    Example:
        >>> tokenize_words("Hello, World!")
        ['hello', 'world']
    """
    if lowercase:
        text = text.lower()
    
    if remove_punctuation:
        # Keep alphanumeric and spaces
        text = re.sub(r'[^\w\s]', ' ', text)
    
    tokens = text.split()
    return [t for t in tokens if len(t) >= min_length]


def tokenize_chars(text: str, 
                   lowercase: bool = True,
                   remove_whitespace: bool = False) -> List[str]:
    """
    Tokenize text into characters.
    
    Args:
        text: Input text
        lowercase: Convert to lowercase
        remove_whitespace: Remove whitespace characters
    
    Returns:
        List of character tokens
    
    Example:
        >>> tokenize_chars("Hi!")
        ['h', 'i', '!']
    """
    if lowercase:
        text = text.lower()
    
    if remove_whitespace:
        text = ''.join(c for c in text if not c.isspace())
    
    return list(text)


def tokenize_ngrams(text: str, 
                    n: int = DEFAULT_NGRAM_SIZE,
                    lowercase: bool = True,
                    word_level: bool = False) -> List[str]:
    """
    Tokenize text into n-grams.
    
    Args:
        text: Input text
        n: N-gram size
        lowercase: Convert to lowercase
        word_level: If True, create word n-grams; if False, character n-grams
    
    Returns:
        List of n-gram tokens
    
    Example:
        >>> tokenize_ngrams("hello", n=2)
        ['he', 'el', 'll', 'lo']
        >>> tokenize_ngrams("hello world", n=2, word_level=True)
        ['hello world']
    """
    if lowercase:
        text = text.lower()
    
    if word_level:
        words = text.split()
        if len(words) < n:
            return [' '.join(words)]
        return [' '.join(words[i:i+n]) for i in range(len(words) - n + 1)]
    else:
        if len(text) < n:
            return [text]
        return [text[i:i+n] for i in range(len(text) - n + 1)]


def tokenize_chinese(text: str, 
                     mode: str = 'char',
                     ngram_size: int = 2) -> List[str]:
    """
    Tokenize Chinese text.
    
    Simple Chinese tokenization without external dependencies.
    For better results, use with jieba or similar libraries.
    
    Args:
        text: Input Chinese text
        mode: 'char' for character-level, 'ngram' for character n-grams
        ngram_size: N-gram size when mode is 'ngram'
    
    Returns:
        List of tokens
    
    Example:
        >>> tokenize_chinese("你好世界")
        ['你', '好', '世', '界']
        >>> tokenize_chinese("你好世界", mode='ngram', ngram_size=2)
        ['你好', '好世', '世界']
    """
    # Remove whitespace and punctuation for Chinese
    cleaned = re.sub(r'[\s\u3000\uff00-\uffef]+', '', text)
    
    if mode == 'char':
        return list(cleaned)
    elif mode == 'ngram':
        if len(cleaned) < ngram_size:
            return [cleaned]
        return [cleaned[i:i+ngram_size] for i in range(len(cleaned) - ngram_size + 1)]
    else:
        return list(cleaned)


# =============================================================================
# SimHash Core Functions
# =============================================================================

def compute_simhash(tokens: List[str], 
                    fingerprint_size: int = DEFAULT_FINGERPRINT_SIZE,
                    hash_algorithm: str = 'sha256',
                    weights: Optional[Dict[str, float]] = None) -> int:
    """
    Compute SimHash fingerprint from a list of tokens.
    
    The SimHash algorithm:
    1. Hash each token to a fixed-size bit vector
    2. Sum the bit vectors (adding 1 for 1-bits, subtracting 1 for 0-bits)
    3. Generate final fingerprint: bit is 1 if sum > 0, else 0
    
    Args:
        tokens: List of token strings
        fingerprint_size: Size of fingerprint in bits (32, 64, or 128)
        hash_algorithm: Hash algorithm to use
        weights: Optional token weights (default: all tokens weighted equally)
    
    Returns:
        SimHash fingerprint as integer
    
    Example:
        >>> tokens = tokenize_words("the quick brown fox")
        >>> h = compute_simhash(tokens)
        >>> isinstance(h, int)
        True
    """
    if not tokens:
        return 0
    
    # Initialize bit counters
    bit_counts = [0] * fingerprint_size
    
    for token in tokens:
        # Get token hash
        h = hash_token(token, algorithm=hash_algorithm, size=fingerprint_size)
        
        # Get weight
        weight = weights.get(token, 1.0) if weights else 1.0
        
        # Update bit counts
        for i in range(fingerprint_size):
            bit = (h >> i) & 1
            bit_counts[i] += weight if bit else -weight
    
    # Generate fingerprint
    fingerprint = 0
    for i in range(fingerprint_size):
        if bit_counts[i] > 0:
            fingerprint |= (1 << i)
    
    return fingerprint


def compute_simhash_text(text: str,
                         tokenizer: str = DEFAULT_TOKENIZER,
                         ngram_size: int = DEFAULT_NGRAM_SIZE,
                         fingerprint_size: int = DEFAULT_FINGERPRINT_SIZE,
                         hash_algorithm: str = 'sha256',
                         lowercase: bool = True) -> int:
    """
    Compute SimHash fingerprint directly from text.
    
    Args:
        text: Input text
        tokenizer: Tokenization strategy ('word', 'char', 'ngram', 'chinese', 'chinese_ngram')
        ngram_size: N-gram size for ngram tokenizers
        fingerprint_size: Size of fingerprint in bits
        hash_algorithm: Hash algorithm to use
        lowercase: Convert text to lowercase
    
    Returns:
        SimHash fingerprint as integer
    
    Example:
        >>> h1 = compute_simhash_text("hello world")
        >>> h2 = compute_simhash_text("hello world!")
        >>> hamming_distance(h1, h2) < 5  # Similar texts have low distance
        True
    """
    # Tokenize
    if tokenizer == 'word':
        tokens = tokenize_words(text, lowercase=lowercase)
    elif tokenizer == 'char':
        tokens = tokenize_chars(text, lowercase=lowercase)
    elif tokenizer == 'ngram':
        tokens = tokenize_ngrams(text, n=ngram_size, lowercase=lowercase)
    elif tokenizer == 'chinese':
        tokens = tokenize_chinese(text, mode='char')
    elif tokenizer == 'chinese_ngram':
        tokens = tokenize_chinese(text, mode='ngram', ngram_size=ngram_size)
    else:
        tokens = tokenize_words(text, lowercase=lowercase)
    
    return compute_simhash(tokens, fingerprint_size, hash_algorithm)


def hamming_distance(fp1: int, fp2: int, size: int = DEFAULT_FINGERPRINT_SIZE) -> int:
    """
    Calculate Hamming distance between two fingerprints.
    
    The Hamming distance is the number of positions at which the corresponding
    bits are different.
    
    Args:
        fp1: First fingerprint
        fp2: Second fingerprint
        size: Fingerprint size in bits
    
    Returns:
        Number of differing bits
    
    Example:
        >>> hamming_distance(0b1111, 0b1100)
        2
    """
    xor = fp1 ^ fp2
    # Count set bits (popcount)
    return bin(xor).count('1')


def hamming_distance_normalized(fp1: int, fp2: int, size: int = DEFAULT_FINGERPRINT_SIZE) -> float:
    """
    Calculate normalized Hamming distance (0 to 1).
    
    Args:
        fp1: First fingerprint
        fp2: Second fingerprint
        size: Fingerprint size in bits
    
    Returns:
        Normalized distance (0 = identical, 1 = completely different)
    
    Example:
        >>> hamming_distance_normalized(0b1111, 0b1100, size=4)
        0.5
    """
    return hamming_distance(fp1, fp2, size) / size


def similarity(fp1: int, fp2: int, size: int = DEFAULT_FINGERPRINT_SIZE) -> float:
    """
    Calculate similarity between two fingerprints.
    
    Args:
        fp1: First fingerprint
        fp2: Second fingerprint
        size: Fingerprint size in bits
    
    Returns:
        Similarity score (0 to 1, where 1 is identical)
    
    Example:
        >>> similarity(0b1111, 0b1100, size=4)
        0.5
    """
    return 1 - hamming_distance_normalized(fp1, fp2, size)


def are_similar(fp1: int, fp2: int, 
                threshold: int = 3,
                size: int = DEFAULT_FINGERPRINT_SIZE) -> bool:
    """
    Check if two documents are similar based on Hamming distance threshold.
    
    Args:
        fp1: First fingerprint
        fp2: Second fingerprint
        threshold: Maximum Hamming distance to consider similar
        size: Fingerprint size in bits
    
    Returns:
        True if documents are similar (distance <= threshold)
    
    Example:
        >>> h1 = compute_simhash_text("hello world")
        >>> h2 = compute_simhash_text("hello world!")
        >>> are_similar(h1, h2, threshold=5)
        True
    """
    return hamming_distance(fp1, fp2, size) <= threshold


# =============================================================================
# Fingerprint Utilities
# =============================================================================

def fingerprint_to_binary(fp: int, size: int = DEFAULT_FINGERPRINT_SIZE) -> str:
    """
    Convert fingerprint to binary string representation.
    
    Args:
        fp: Fingerprint integer
        size: Fingerprint size in bits
    
    Returns:
        Binary string representation
    
    Example:
        >>> fingerprint_to_binary(0b1100, size=4)
        '1100'
    """
    return format(fp, f'0{size}b')


def fingerprint_to_hex(fp: int, size: int = DEFAULT_FINGERPRINT_SIZE) -> str:
    """
    Convert fingerprint to hexadecimal string representation.
    
    Args:
        fp: Fingerprint integer
        size: Fingerprint size in bits
    
    Returns:
        Hexadecimal string representation
    
    Example:
        >>> fingerprint_to_hex(255, size=8)
        'ff'
    """
    hex_size = (size + 3) // 4  # bits to hex digits
    return format(fp, f'0{hex_size}x')


def hex_to_fingerprint(hex_str: str) -> int:
    """
    Convert hexadecimal string to fingerprint integer.
    
    Args:
        hex_str: Hexadecimal string
    
    Returns:
        Fingerprint integer
    
    Example:
        >>> hex_to_fingerprint('ff')
        255
    """
    return int(hex_str, 16)


def fingerprint_chunks(fp: int, chunk_size: int = 16, 
                       total_size: int = DEFAULT_FINGERPRINT_SIZE) -> List[int]:
    """
    Split fingerprint into chunks for indexed search.
    
    This is useful for building a search index where documents
    are indexed by chunks of their fingerprint.
    
    Args:
        fp: Fingerprint integer
        chunk_size: Size of each chunk in bits
        total_size: Total fingerprint size in bits
    
    Returns:
        List of chunk values
    
    Example:
        >>> fingerprint_chunks(0xDEADBEEF, chunk_size=8, total_size=32)
        [222, 173, 190, 239]
    """
    chunks = []
    mask = (1 << chunk_size) - 1
    for i in range(0, total_size, chunk_size):
        chunk = (fp >> i) & mask
        chunks.append(chunk)
    return chunks


# =============================================================================
# SimHash Index for Similarity Search
# =============================================================================

class SimHashIndex:
    """
    An index for fast similarity search using SimHash.
    
    Uses chunked indexing to find near-duplicates efficiently.
    
    Example:
        >>> index = SimHashIndex()
        >>> index.add("doc1", "Hello world")
        >>> index.add("doc2", "Hello world!")
        >>> duplicates = index.query("Hello world", threshold=3)
        >>> len(duplicates) >= 1
        True
    """
    
    def __init__(self, 
                 fingerprint_size: int = DEFAULT_FINGERPRINT_SIZE,
                 chunk_size: int = 16,
                 tokenizer: str = DEFAULT_TOKENIZER,
                 ngram_size: int = DEFAULT_NGRAM_SIZE,
                 hash_algorithm: str = 'sha256'):
        """
        Initialize SimHash index.
        
        Args:
            fingerprint_size: Size of fingerprints in bits
            chunk_size: Size of chunks for indexing
            tokenizer: Tokenization strategy
            ngram_size: N-gram size
            hash_algorithm: Hash algorithm
        """
        self.fingerprint_size = fingerprint_size
        self.chunk_size = chunk_size
        self.tokenizer = tokenizer
        self.ngram_size = ngram_size
        self.hash_algorithm = hash_algorithm
        
        # Number of chunks
        self.num_chunks = fingerprint_size // chunk_size
        
        # Index: chunk_index -> chunk_value -> set of doc_ids
        self._index: List[Dict[int, Set[str]]] = [
            defaultdict(set) for _ in range(self.num_chunks)
        ]
        
        # Document storage: doc_id -> (fingerprint, text)
        self._docs: Dict[str, Tuple[int, str]] = {}
    
    def add(self, doc_id: str, text: str) -> int:
        """
        Add a document to the index.
        
        Args:
            doc_id: Unique document identifier
            text: Document text
        
        Returns:
            SimHash fingerprint
        
        Example:
            >>> index = SimHashIndex()
            >>> fp = index.add("doc1", "hello world")
            >>> isinstance(fp, int)
            True
        """
        fp = compute_simhash_text(
            text, 
            tokenizer=self.tokenizer,
            ngram_size=self.ngram_size,
            fingerprint_size=self.fingerprint_size,
            hash_algorithm=self.hash_algorithm
        )
        
        # Store document
        self._docs[doc_id] = (fp, text)
        
        # Index by chunks
        chunks = fingerprint_chunks(fp, self.chunk_size, self.fingerprint_size)
        for i, chunk in enumerate(chunks):
            self._index[i][chunk].add(doc_id)
        
        return fp
    
    def add_batch(self, documents: Dict[str, str]) -> Dict[str, int]:
        """
        Add multiple documents to the index.
        
        Args:
            documents: Dictionary of doc_id -> text
        
        Returns:
            Dictionary of doc_id -> fingerprint
        """
        fingerprints = {}
        for doc_id, text in documents.items():
            fingerprints[doc_id] = self.add(doc_id, text)
        return fingerprints
    
    def remove(self, doc_id: str) -> bool:
        """
        Remove a document from the index.
        
        Args:
            doc_id: Document identifier to remove
        
        Returns:
            True if document was found and removed
        """
        if doc_id not in self._docs:
            return False
        
        fp, _ = self._docs[doc_id]
        chunks = fingerprint_chunks(fp, self.chunk_size, self.fingerprint_size)
        
        for i, chunk in enumerate(chunks):
            self._index[i][chunk].discard(doc_id)
            if not self._index[i][chunk]:
                del self._index[i][chunk]
        
        del self._docs[doc_id]
        return True
    
    def query(self, text: str, threshold: int = 3, brute_force: bool = False) -> List[Tuple[str, int, float]]:
        """
        Query for similar documents.
        
        Args:
            text: Query text
            threshold: Maximum Hamming distance
            brute_force: If True, scan all documents; if False, use chunked index
        
        Returns:
            List of (doc_id, distance, similarity) tuples sorted by similarity
        """
        fp = compute_simhash_text(
            text,
            tokenizer=self.tokenizer,
            ngram_size=self.ngram_size,
            fingerprint_size=self.fingerprint_size,
            hash_algorithm=self.hash_algorithm
        )
        
        # Get candidate documents from chunks
        candidates: Set[str] = set()
        
        if brute_force:
            # Use all documents as candidates
            candidates = set(self._docs.keys())
        else:
            # Try chunk-based index first
            chunks = fingerprint_chunks(fp, self.chunk_size, self.fingerprint_size)
            
            for i, chunk in enumerate(chunks):
                if chunk in self._index[i]:
                    candidates.update(self._index[i][chunk])
            
            # Fallback to brute force if no candidates found (useful for small datasets)
            if not candidates and len(self._docs) <= 100:
                candidates = set(self._docs.keys())
        
        # Calculate exact distances
        results = []
        for doc_id in candidates:
            doc_fp, _ = self._docs[doc_id]
            dist = hamming_distance(fp, doc_fp, self.fingerprint_size)
            if dist <= threshold:
                sim = similarity(fp, doc_fp, self.fingerprint_size)
                results.append((doc_id, dist, sim))
        
        # Sort by similarity (descending)
        results.sort(key=lambda x: -x[2])
        return results
    
    def get_duplicates(self, threshold: int = 3, brute_force: bool = False) -> List[List[str]]:
        """
        Find all groups of duplicate documents.
        
        Args:
            threshold: Maximum Hamming distance for duplicates
            brute_force: If True, scan all documents; if False, use chunked index
        
        Returns:
            List of duplicate groups (each group is a list of doc_ids)
        """
        processed: Set[str] = set()
        groups: List[List[str]] = []
        
        for doc_id in self._docs:
            if doc_id in processed:
                continue
            
            # Query for similar documents
            _, text = self._docs[doc_id]
            similar = self.query(text, threshold, brute_force=brute_force)
            
            if len(similar) > 1:  # More than just itself
                group = [s[0] for s in similar]
                groups.append(group)
                processed.update(group)
        
        return groups
    
    def get_fingerprint(self, doc_id: str) -> Optional[int]:
        """
        Get the fingerprint for a document.
        
        Args:
            doc_id: Document identifier
        
        Returns:
            Fingerprint or None if not found
        """
        if doc_id in self._docs:
            return self._docs[doc_id][0]
        return None
    
    def get_document(self, doc_id: str) -> Optional[str]:
        """
        Get the text for a document.
        
        Args:
            doc_id: Document identifier
        
        Returns:
            Document text or None if not found
        """
        if doc_id in self._docs:
            return self._docs[doc_id][1]
        return None
    
    def __len__(self) -> int:
        return len(self._docs)
    
    def __contains__(self, doc_id: str) -> bool:
        return doc_id in self._docs


# =============================================================================
# Advanced Features
# =============================================================================

def compute_weighted_simhash(tokens: List[str],
                             weights: Dict[str, float],
                             fingerprint_size: int = DEFAULT_FINGERPRINT_SIZE,
                             hash_algorithm: str = 'sha256') -> int:
    """
    Compute SimHash with custom token weights.
    
    Useful when some tokens are more important than others
    (e.g., title words, keywords, named entities).
    
    Args:
        tokens: List of token strings
        weights: Dictionary mapping tokens to their weights
        fingerprint_size: Size of fingerprint in bits
        hash_algorithm: Hash algorithm to use
    
    Returns:
        Weighted SimHash fingerprint
    
    Example:
        >>> tokens = ["the", "quick", "brown", "fox"]
        >>> weights = {"fox": 2.0, "quick": 1.5}  # Emphasize key words
        >>> fp = compute_weighted_simhash(tokens, weights)
    """
    return compute_simhash(tokens, fingerprint_size, hash_algorithm, weights)


def compute_simhash_with_features(features: Dict[str, float],
                                  fingerprint_size: int = DEFAULT_FINGERPRINT_SIZE,
                                  hash_algorithm: str = 'sha256') -> int:
    """
    Compute SimHash from pre-computed feature weights.
    
    Useful when you have features extracted by other means
    (e.g., TF-IDF weights, named entities, etc.)
    
    Args:
        features: Dictionary mapping feature names to their weights
        fingerprint_size: Size of fingerprint in bits
        hash_algorithm: Hash algorithm to use
    
    Returns:
        SimHash fingerprint
    
    Example:
        >>> features = {"title:python": 3.0, "body:programming": 1.5}
        >>> fp = compute_simhash_with_features(features)
    """
    bit_counts = [0] * fingerprint_size
    
    for feature, weight in features.items():
        h = hash_token(feature, algorithm=hash_algorithm, size=fingerprint_size)
        for i in range(fingerprint_size):
            bit = (h >> i) & 1
            bit_counts[i] += weight if bit else -weight
    
    fingerprint = 0
    for i in range(fingerprint_size):
        if bit_counts[i] > 0:
            fingerprint |= (1 << i)
    
    return fingerprint


def batch_compute_simhash(texts: List[str],
                          tokenizer: str = DEFAULT_TOKENIZER,
                          ngram_size: int = DEFAULT_NGRAM_SIZE,
                          fingerprint_size: int = DEFAULT_FINGERPRINT_SIZE,
                          hash_algorithm: str = 'sha256') -> List[int]:
    """
    Compute SimHash fingerprints for multiple texts.
    
    Args:
        texts: List of text strings
        tokenizer: Tokenization strategy
        ngram_size: N-gram size
        fingerprint_size: Size of fingerprints in bits
        hash_algorithm: Hash algorithm to use
    
    Returns:
        List of fingerprints
    
    Example:
        >>> texts = ["hello world", "hello there", "goodbye world"]
        >>> fps = batch_compute_simhash(texts)
        >>> len(fps) == 3
        True
    """
    return [
        compute_simhash_text(
            text,
            tokenizer=tokenizer,
            ngram_size=ngram_size,
            fingerprint_size=fingerprint_size,
            hash_algorithm=hash_algorithm
        )
        for text in texts
    ]


def find_near_duplicates(fingerprints: List[int],
                         threshold: int = 3,
                         size: int = DEFAULT_FINGERPRINT_SIZE) -> List[Tuple[int, int, int]]:
    """
    Find pairs of near-duplicate fingerprints in a list.
    
    Args:
        fingerprints: List of fingerprints
        threshold: Maximum Hamming distance for duplicates
        size: Fingerprint size in bits
    
    Returns:
        List of (index1, index2, distance) tuples
    
    Example:
        >>> fps = batch_compute_simhash(["hello", "hello!", "goodbye"])
        >>> dups = find_near_duplicates(fps, threshold=5)
        >>> len(dups) >= 1  # "hello" and "hello!" should be similar
        True
    """
    n = len(fingerprints)
    duplicates = []
    
    for i in range(n):
        for j in range(i + 1, n):
            dist = hamming_distance(fingerprints[i], fingerprints[j], size)
            if dist <= threshold:
                duplicates.append((i, j, dist))
    
    return duplicates


# =============================================================================
# Distance Matrix and Clustering
# =============================================================================

def compute_distance_matrix(fingerprints: List[int],
                           size: int = DEFAULT_FINGERPRINT_SIZE) -> List[List[int]]:
    """
    Compute pairwise Hamming distance matrix.
    
    Args:
        fingerprints: List of fingerprints
        size: Fingerprint size in bits
    
    Returns:
        2D matrix of distances
    
    Example:
        >>> fps = batch_compute_simhash(["a", "b", "c"])
        >>> matrix = compute_distance_matrix(fps)
        >>> len(matrix) == 3
        True
    """
    n = len(fingerprints)
    matrix = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(i + 1, n):
            dist = hamming_distance(fingerprints[i], fingerprints[j], size)
            matrix[i][j] = dist
            matrix[j][i] = dist
    
    return matrix


def compute_similarity_matrix(fingerprints: List[int],
                              size: int = DEFAULT_FINGERPRINT_SIZE) -> List[List[float]]:
    """
    Compute pairwise similarity matrix.
    
    Args:
        fingerprints: List of fingerprints
        size: Fingerprint size in bits
    
    Returns:
        2D matrix of similarities (0 to 1)
    
    Example:
        >>> fps = batch_compute_simhash(["a", "a!", "b"])
        >>> matrix = compute_similarity_matrix(fps)
        >>> matrix[0][1] > matrix[0][2]  # "a" more similar to "a!" than "b"
        True
    """
    n = len(fingerprints)
    matrix = [[1.0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(i + 1, n):
            sim = similarity(fingerprints[i], fingerprints[j], size)
            matrix[i][j] = sim
            matrix[j][i] = sim
    
    return matrix


# =============================================================================
# Chinese Text Special Handling
# =============================================================================

def compute_simhash_chinese(text: str,
                            mode: str = 'ngram',
                            ngram_size: int = 2,
                            fingerprint_size: int = DEFAULT_FINGERPRINT_SIZE,
                            hash_algorithm: str = 'sha256') -> int:
    """
    Compute SimHash optimized for Chinese text.
    
    Args:
        text: Chinese text
        mode: 'char' for character-level, 'ngram' for character n-grams
        ngram_size: N-gram size (default 2 for good balance)
        fingerprint_size: Size of fingerprint in bits
        hash_algorithm: Hash algorithm to use
    
    Returns:
        SimHash fingerprint
    
    Example:
        >>> fp1 = compute_simhash_chinese("今天天气很好")
        >>> fp2 = compute_simhash_chinese("今天天气真好")  # One character different
        >>> hamming_distance(fp1, fp2) < 20  # Should be similar
        True
    """
    tokens = tokenize_chinese(text, mode=mode, ngram_size=ngram_size)
    return compute_simhash(tokens, fingerprint_size, hash_algorithm)


# =============================================================================
# Utility Functions
# =============================================================================

def is_valid_fingerprint(fp: int, size: int = DEFAULT_FINGERPRINT_SIZE) -> bool:
    """
    Check if a fingerprint is valid.
    
    Args:
        fp: Fingerprint to validate
        size: Expected fingerprint size in bits
    
    Returns:
        True if fingerprint is valid
    
    Example:
        >>> is_valid_fingerprint(0xFFFF, size=16)
        True
        >>> is_valid_fingerprint(-1)  # Negative is invalid
        False
    """
    if fp < 0:
        return False
    max_value = (1 << size) - 1
    return fp <= max_value


def compare_documents(text1: str, text2: str,
                     tokenizer: str = DEFAULT_TOKENIZER,
                     fingerprint_size: int = DEFAULT_FINGERPRINT_SIZE) -> Dict[str, Union[int, float, str]]:
    """
    Compare two documents using SimHash.
    
    Args:
        text1: First document text
        text2: Second document text
        tokenizer: Tokenization strategy
        fingerprint_size: Size of fingerprints in bits
    
    Returns:
        Dictionary with comparison results
    
    Example:
        >>> result = compare_documents("hello world", "hello world!")
        >>> result['similarity'] > 0.9  # Very similar
        True
    """
    fp1 = compute_simhash_text(text1, tokenizer=tokenizer, fingerprint_size=fingerprint_size)
    fp2 = compute_simhash_text(text2, tokenizer=tokenizer, fingerprint_size=fingerprint_size)
    
    dist = hamming_distance(fp1, fp2, fingerprint_size)
    sim = similarity(fp1, fp2, fingerprint_size)
    
    return {
        'fingerprint1': fp1,
        'fingerprint2': fp2,
        'fingerprint1_hex': fingerprint_to_hex(fp1, fingerprint_size),
        'fingerprint2_hex': fingerprint_to_hex(fp2, fingerprint_size),
        'hamming_distance': dist,
        'similarity': sim,
        'is_near_duplicate': dist <= 3,
        'interpretation': _interpret_similarity(sim)
    }


def _interpret_similarity(sim: float) -> str:
    """Interpret similarity score as human-readable text."""
    if sim >= 0.95:
        return "Nearly identical"
    elif sim >= 0.85:
        return "Very similar"
    elif sim >= 0.70:
        return "Similar"
    elif sim >= 0.50:
        return "Somewhat similar"
    elif sim >= 0.30:
        return "Slightly similar"
    else:
        return "Dissimilar"


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("SimHash Utilities Demo")
    print("=" * 60)
    
    # Example 1: Basic usage
    print("\n--- Example 1: Basic SimHash ---")
    text1 = "The quick brown fox jumps over the lazy dog"
    text2 = "The quick brown fox jumped over the lazy dog"
    text3 = "A completely different sentence about cats"
    
    fp1 = compute_simhash_text(text1)
    fp2 = compute_simhash_text(text2)
    fp3 = compute_simhash_text(text3)
    
    print(f"Text 1: '{text1}'")
    print(f"Text 2: '{text2}'")
    print(f"Text 3: '{text3}'")
    print(f"\nFingerprint 1: {fingerprint_to_hex(fp1)}")
    print(f"Fingerprint 2: {fingerprint_to_hex(fp2)}")
    print(f"Fingerprint 3: {fingerprint_to_hex(fp3)}")
    
    print(f"\nDistance 1-2: {hamming_distance(fp1, fp2)} (similarity: {similarity(fp1, fp2):.2%})")
    print(f"Distance 1-3: {hamming_distance(fp1, fp3)} (similarity: {similarity(fp1, fp3):.2%})")
    
    # Example 2: SimHash Index
    print("\n--- Example 2: Similarity Search Index ---")
    index = SimHashIndex()
    
    docs = {
        "doc1": "Python is a programming language",
        "doc2": "Python is a popular programming language",
        "doc3": "Java is another programming language",
        "doc4": "The weather is nice today",
        "doc5": "Python programming tutorial"
    }
    
    for doc_id, text in docs.items():
        index.add(doc_id, text)
    
    print(f"Indexed {len(index)} documents")
    
    query = "Python programming guide"
    results = index.query(query, threshold=10)
    print(f"\nQuery: '{query}'")
    print("Results:")
    for doc_id, dist, sim in results:
        print(f"  {doc_id}: distance={dist}, similarity={sim:.2%}")
    
    # Example 3: Chinese text
    print("\n--- Example 3: Chinese Text ---")
    cn_text1 = "今天天气很好，适合外出散步"
    cn_text2 = "今天天气真好，适合外出散步"
    
    cn_fp1 = compute_simhash_chinese(cn_text1)
    cn_fp2 = compute_simhash_chinese(cn_text2)
    
    print(f"Text 1: '{cn_text1}'")
    print(f"Text 2: '{cn_text2}'")
    print(f"Hamming distance: {hamming_distance(cn_fp1, cn_fp2)}")
    print(f"Similarity: {similarity(cn_fp1, cn_fp2):.2%}")
    
    # Example 4: Document comparison
    print("\n--- Example 4: Document Comparison ---")
    result = compare_documents(
        "Machine learning is a subset of artificial intelligence",
        "Machine learning is part of artificial intelligence"
    )
    print(f"Similarity: {result['similarity']:.2%}")
    print(f"Interpretation: {result['interpretation']}")
    print(f"Near duplicate: {result['is_near_duplicate']}")