"""
Burrows-Wheeler Transform (BWT) Utilities

A comprehensive implementation of BWT and related transforms for compression
and text processing applications.

Features:
- Forward BWT transform
- Inverse BWT transform
- Move-to-Front (MTF) encoding/decoding
- BWT-based pattern matching
- Zero external dependencies

The BWT is a reversible transformation that rearranges characters in a way
that groups similar characters together, making it highly effective for
compression (used in bzip2).
"""

from typing import List, Tuple, Optional, Union, Dict
from collections import defaultdict


def bwt_transform(data: Union[str, bytes]) -> Tuple[Union[str, bytes], int]:
    """
    Perform Burrows-Wheeler Transform on input data.
    
    Args:
        data: Input string or bytes to transform
        
    Returns:
        Tuple of (transformed data, original index position)
        
    Example:
        >>> result, idx = bwt_transform("banana")
        >>> idx
        4
    """
    if isinstance(data, str):
        data_with_sentinel = data + '$'
        is_string = True
    else:
        data_with_sentinel = data + b'$'
        is_string = False
    
    n = len(data_with_sentinel)
    
    # Generate sorted rotations (via indices)
    sorted_indices = sorted(range(n), key=lambda i: data_with_sentinel[i:] + data_with_sentinel[:i])
    
    # Find position of original string (rotation starting at index 0)
    original_index = sorted_indices.index(0)
    
    # Extract last column: character at position (i-1) for rotation starting at sorted_indices[i]
    last_column = []
    for i in sorted_indices:
        # Last char of rotation starting at i is at position (i + n - 1) % n = (i - 1) % n
        last_idx = (i - 1) % n
        last_column.append(data_with_sentinel[last_idx])
    
    result = ''.join(last_column) if is_string else bytes(last_column)
    return result, original_index


def bwt_inverse(transformed: Union[str, bytes], index: int) -> Union[str, bytes]:
    """
    Perform inverse Burrows-Wheeler Transform.
    
    Args:
        transformed: BWT-transformed data (with sentinel at end)
        index: Original index position from forward transform
        
    Returns:
        Original data (without sentinel character)
        
    Example:
        >>> bwt_inverse("annb$aa", 4)
        'banana'
    """
    if isinstance(transformed, str):
        is_string = True
        L = list(transformed)  # Last column
    else:
        is_string = False
        L = list(transformed)
    
    n = len(L)
    
    if n <= 1:
        return "" if is_string else b""
    
    # First column F is just L sorted
    F = sorted(L)
    
    # Build LF mapping: for each position i in L, find corresponding position in F
    # Use occurrence counting for stable matching
    # For character c at position i in L with rank k, find the position in F of c with rank k
    
    # Compute occurrence ranks for L
    L_rank = []
    count = defaultdict(int)
    for c in L:
        L_rank.append(count[c])
        count[c] += 1
    
    # Build lookup for F: for each (char, rank), store position in F
    # F is sorted, so same chars are consecutive
    F_positions = {}
    count = defaultdict(int)
    for i, c in enumerate(F):
        F_positions[(c, count[c])] = i
        count[c] += 1
    
    # LF mapping
    LF = [F_positions[(c, rank)] for c, rank in zip(L, L_rank)]
    
    # Reconstruct original string by following LF starting at index
    # We traverse all n positions, getting the original string in reverse order
    result_chars = []
    current = index
    for _ in range(n):  # n iterations to get all chars including sentinel
        result_chars.append(L[current])
        current = LF[current]
    
    # The chars are in reverse order of original, so reverse them
    result_chars = result_chars[::-1]
    
    # Strip the sentinel character (should be at the end after reversal)
    # Sentinel is '$' for strings or b'$'[0] = 36 for bytes
    if is_string:
        # Find and remove the sentinel
        if result_chars and result_chars[-1] == '$':
            result_chars = result_chars[:-1]
        else:
            result_chars = [c for c in result_chars if c != '$']
        return ''.join(result_chars)
    else:
        sentinel = 36  # ASCII for '$'
        if result_chars and result_chars[-1] == sentinel:
            result_chars = result_chars[:-1]
        else:
            result_chars = [c for c in result_chars if c != sentinel]
        return bytes(result_chars)


def mtf_encode(data: Union[str, bytes], alphabet: Optional[Union[str, bytes]] = None) -> List[int]:
    """
    Perform Move-to-Front encoding.
    
    MTF encoding converts repeated characters into smaller integers,
    which compresses well with entropy coding.
    
    Args:
        data: Input string or bytes
        alphabet: Optional custom alphabet (default: all unique chars in order of first appearance)
        
    Returns:
        List of integer codes
        
    Example:
        >>> mtf_encode("aaabbbaaa")
        [0, 0, 0, 1, 0, 0, 1, 0, 0]
    """
    if isinstance(data, str):
        chars = list(data)
    else:
        chars = list(data)
    
    # Build alphabet if not provided - use order of first appearance
    if alphabet is None:
        seen = []
        for c in chars:
            if c not in seen:
                seen.append(c)
        symbol_list = seen.copy()
    else:
        symbol_list = list(alphabet)
    
    result = []
    
    for char in chars:
        idx = symbol_list.index(char)
        result.append(idx)
        # Move to front
        symbol_list.pop(idx)
        symbol_list.insert(0, char)
    
    return result


def mtf_decode(codes: List[int], alphabet: Union[str, bytes]) -> Union[str, bytes]:
    """
    Perform Move-to-Front decoding.
    
    Args:
        codes: List of integer codes from MTF encoding
        alphabet: The alphabet used for encoding
        
    Returns:
        Decoded string or bytes
        
    Example:
        >>> mtf_decode([0, 0, 0, 1, 0, 0, 1, 0, 0], "ab")
        'aaabbbaaa'
    """
    symbol_list = list(alphabet)
    result = []
    
    for idx in codes:
        char = symbol_list[idx]
        result.append(char)
        # Move to front
        symbol_list.pop(idx)
        symbol_list.insert(0, char)
    
    if isinstance(alphabet, str):
        return ''.join(result)
    else:
        return bytes(result)


def bwt_mtf_compress(data: Union[str, bytes]) -> Tuple[List[int], int, Union[str, bytes]]:
    """
    Combined BWT + MTF transform for compression preprocessing.
    
    This is the first stage of bzip2-like compression.
    
    Args:
        data: Input string or bytes
        
    Returns:
        Tuple of (MTF codes, BWT index, alphabet used)
    """
    # Apply BWT
    transformed, index = bwt_transform(data)
    
    # Build alphabet from transformed data (sorted for consistent ordering)
    if isinstance(transformed, str):
        alphabet = ''.join(sorted(set(transformed)))
    else:
        alphabet = bytes(sorted(set(transformed)))
    
    # Apply MTF
    codes = mtf_encode(transformed, alphabet)
    
    return codes, index, alphabet


def bwt_mtf_decompress(codes: List[int], index: int, alphabet: Union[str, bytes]) -> Union[str, bytes]:
    """
    Inverse of bwt_mtf_compress.
    
    Args:
        codes: MTF codes
        index: BWT index
        alphabet: Alphabet used during encoding
        
    Returns:
        Original data
    """
    # Decode MTF
    transformed = mtf_decode(codes, alphabet)
    
    # Inverse BWT
    return bwt_inverse(transformed, index)


def bwt_search(text: str, pattern: str) -> List[int]:
    """
    Search for pattern in text using BWT-based FM-index approach.
    
    This is a simplified version that demonstrates the principle.
    Uses the first-last property of BWT for efficient pattern matching.
    
    Args:
        text: Text to search in (without $ sentinel)
        pattern: Pattern to find
        
    Returns:
        List of starting positions (0-indexed)
        
    Example:
        >>> bwt_search("banana", "ana")
        [1, 3]
    """
    if not pattern:
        return []
    
    # Build BWT and auxiliary structures
    text_with_sentinel = text + '$'
    n = len(text_with_sentinel)
    
    # Build suffix array
    suffixes = [(text_with_sentinel[i:], i) for i in range(n)]
    suffixes.sort()
    sa = [pos for _, pos in suffixes]
    
    # Build BWT
    bwt = ''.join(text_with_sentinel[(sa[i] - 1) % n] for i in range(n))
    
    # Build occurrence count and C arrays
    sorted_chars = sorted(set(text_with_sentinel))
    c = {}
    occ = defaultdict(lambda: [0] * (n + 1))
    
    for i, char in enumerate(bwt):
        for ch in sorted_chars:
            occ[ch][i + 1] = occ[ch][i]
        occ[char][i + 1] += 1
    
    # Build C array
    cumsum = 0
    for char in sorted_chars:
        c[char] = cumsum
        cumsum += text_with_sentinel.count(char)
    
    # Backward search using FM-index
    first = 0
    last = n - 1
    
    for char in reversed(pattern):
        if char not in c:
            return []
        first = c[char] + occ[char][first]
        last = c[char] + occ[char][last + 1] - 1
        
        if first > last:
            return []
    
    # Return positions from suffix array
    return sorted([sa[i] for i in range(first, last + 1)])


def bwt_compress_ratio(data: Union[str, bytes]) -> Dict:
    """
    Analyze the compression potential of data after BWT + MTF.
    
    Args:
        data: Input data to analyze
        
    Returns:
        Dictionary with compression statistics
    """
    codes, index, alphabet = bwt_mtf_compress(data)
    
    # Calculate statistics
    code_counts = defaultdict(int)
    for code in codes:
        code_counts[code] += 1
    
    total = len(codes)
    small_code_ratio = sum(code_counts.get(i, 0) for i in range(4)) / total if total > 0 else 0
    
    return {
        'original_length': len(data),
        'transformed_length': len(codes),
        'alphabet_size': len(alphabet),
        'unique_codes': len(code_counts),
        'small_code_ratio': small_code_ratio,
        'code_distribution': dict(sorted(code_counts.items())[:10]),
        'compression_potential': 'high' if small_code_ratio > 0.5 else ('medium' if small_code_ratio > 0.3 else 'low')
    }


class BWT:
    """
    Object-oriented interface for BWT operations.
    
    Example:
        >>> bwt = BWT("banana")
        >>> transformed = bwt.transform()
        >>> original = BWT.inverse(transformed, bwt.index)
    """
    
    def __init__(self, data: Union[str, bytes]):
        """Initialize with data to transform."""
        self.data = data
        self._transformed = None
        self._index = None
    
    def transform(self) -> Union[str, bytes]:
        """Perform BWT transform."""
        self._transformed, self._index = bwt_transform(self.data)
        return self._transformed
    
    @property
    def index(self) -> int:
        """Get the BWT index (computes transform if needed)."""
        if self._index is None:
            self.transform()
        return self._index
    
    @staticmethod
    def inverse(transformed: Union[str, bytes], index: int) -> Union[str, bytes]:
        """Perform inverse BWT."""
        return bwt_inverse(transformed, index)
    
    def search(self, pattern: str) -> List[int]:
        """Search for pattern in the data using BWT."""
        if isinstance(self.data, bytes):
            text = self.data.decode('utf-8', errors='replace')
            pat = pattern if isinstance(pattern, str) else pattern.decode('utf-8', errors='replace')
        else:
            text = self.data
            pat = pattern
        return bwt_search(text, pat)
    
    def analyze(self) -> Dict:
        """Analyze compression potential."""
        return bwt_compress_ratio(self.data)


# Convenience functions
def transform(data: Union[str, bytes]) -> Tuple[Union[str, bytes], int]:
    """Alias for bwt_transform."""
    return bwt_transform(data)


def inverse(transformed: Union[str, bytes], index: int) -> Union[str, bytes]:
    """Alias for bwt_inverse."""
    return bwt_inverse(transformed, index)


if __name__ == "__main__":
    # Quick demo
    test_strings = [
        "banana",
        "abracadabra",
        "mississippi",
        "the quick brown fox jumps over the lazy dog",
    ]
    
    print("Burrows-Wheeler Transform Demo\n" + "=" * 40)
    
    for s in test_strings:
        print(f"\nOriginal: {s}")
        transformed, idx = bwt_transform(s)
        print(f"Transformed: {transformed}")
        print(f"Index: {idx}")
        recovered = bwt_inverse(transformed, idx)
        print(f"Recovered: {recovered}")
        print(f"Match: {s == recovered}")
        
        # Compression analysis
        analysis = bwt_compress_ratio(s)
        print(f"Compression potential: {analysis['compression_potential']}")
        print(f"Small code ratio: {analysis['small_code_ratio']:.2%}")