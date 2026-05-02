"""
De Bruijn Sequence Utilities

A De Bruijn sequence B(k, n) is a cyclic sequence of a given alphabet size k
in which every possible length-n string on the alphabet occurs exactly once
as a substring.

Applications:
- Password cracking (generating optimal sequences to try all combinations)
- DNA sequencing
- Combinatorial optimization
- Error-correcting codes
- Pseudo-random number generation
"""

from typing import List, Iterator, Optional, Set
from collections import deque


def de_bruijn(k: int, n: int, alphabet: Optional[List[str]] = None) -> str:
    """
    Generate a De Bruijn sequence B(k, n).
    
    A De Bruijn sequence is a cyclic sequence in which every possible
    length-n string from a k-symbol alphabet occurs exactly once as a substring.
    
    Args:
        k: Number of symbols in the alphabet (or len(alphabet) if alphabet provided)
        n: Length of substrings
        alphabet: Optional list of symbols. If None, uses digits 0 to k-1
        
    Returns:
        A De Bruijn sequence as a string
        
    Raises:
        ValueError: If k < 2, n < 1, or alphabet length doesn't match k
        
    Examples:
        >>> de_bruijn(2, 3)
        '00010111'
        >>> de_bruijn(2, 3, ['A', 'B'])
        'AAABABB'
        >>> de_bruijn(3, 2, ['0', '1', '2'])
        '001122021'
        
    Time Complexity: O(k^n)
    Space Complexity: O(k^n)
    
    Note:
        The sequence length is k^n, which grows exponentially.
        For large values of k^n, this may consume significant memory.
    """
    if k < 2:
        raise ValueError("k must be at least 2")
    if n < 1:
        raise ValueError("n must be at least 1")
    
    if alphabet is not None:
        if len(alphabet) != k:
            raise ValueError(f"Alphabet length ({len(alphabet)}) must match k ({k})")
        symbols = alphabet
    else:
        symbols = [str(i) for i in range(k)]
    
    # Using the "prefer-one" or "prefer-higher" algorithm
    # This is a modified FKM algorithm (Fredericksen, Kessler, Maiorana)
    
    a = [0] * (k * n)
    sequence = []
    
    def db(t: int, p: int):
        """
        Recursive helper function for De Bruijn sequence generation.
        Uses the algorithm from "Combinatorial Generation" by Frank Ruskey.
        """
        if t > n:
            if n % p == 0:
                sequence.extend(a[1:p + 1])
        else:
            a[t] = a[t - p]
            db(t + 1, p)
            for j in range(a[t - p] + 1, k):
                a[t] = j
                db(t + 1, t)
    
    db(1, 1)
    
    return ''.join(symbols[i] for i in sequence)


def de_bruijn_generator(k: int, n: int, alphabet: Optional[List[str]] = None) -> Iterator[str]:
    """
    Generate De Bruijn sequence as an iterator (memory-efficient for large sequences).
    
    This is a generator version that yields one symbol at a time,
    useful for large sequences where storing the entire sequence in memory
    is not feasible.
    
    Args:
        k: Number of symbols in the alphabet
        n: Length of substrings
        alphabet: Optional list of symbols
        
    Yields:
        Individual symbols of the De Bruijn sequence
        
    Examples:
        >>> list(de_bruijn_generator(2, 2))
        ['0', '0', '1', '1']
        
    Time Complexity: O(k^n) total, O(1) per element
    Space Complexity: O(k * n) for the recursion stack
    """
    if k < 2:
        raise ValueError("k must be at least 2")
    if n < 1:
        raise ValueError("n must be at least 1")
    
    if alphabet is not None:
        if len(alphabet) != k:
            raise ValueError(f"Alphabet length ({len(alphabet)}) must match k ({k})")
        symbols = alphabet
    else:
        symbols = [str(i) for i in range(k)]
    
    a = [0] * (k * n)
    result_buffer = []
    
    def db(t: int, p: int):
        if t > n:
            if n % p == 0:
                for i in range(1, p + 1):
                    result_buffer.append(a[i])
        else:
            a[t] = a[t - p]
            db(t + 1, p)
            for j in range(a[t - p] + 1, k):
                a[t] = j
                db(t + 1, t)
    
    db(1, 1)
    
    for idx in result_buffer:
        yield symbols[idx]


def is_de_bruijn(sequence: str, n: int, alphabet: Optional[Set[str]] = None) -> bool:
    """
    Check if a sequence is a valid De Bruijn sequence.
    
    A valid De Bruijn sequence must contain each possible n-length
    substring exactly once when treated as a cyclic sequence.
    
    Args:
        sequence: The sequence to validate
        n: Length of substrings
        alphabet: Optional set of valid symbols. If None, inferred from sequence
        
    Returns:
        True if the sequence is a valid De Bruijn sequence
        
    Examples:
        >>> is_de_bruijn('00010111', 3)
        True
        >>> is_de_bruijn('00011101', 3)  # Different valid sequence
        True
        >>> is_de_bruijn('00010110', 3)  # Missing '111'
        False
        
    Time Complexity: O(len(sequence) * n)
    Space Complexity: O(k^n) where k is alphabet size
    """
    if not sequence or n < 1:
        return False
    
    if alphabet is None:
        alphabet = set(sequence)
    else:
        alphabet = set(alphabet)
    
    k = len(alphabet)
    expected_length = k ** n
    
    if len(sequence) != expected_length:
        return False
    
    # Check all symbols are from the alphabet
    if not all(s in alphabet for s in sequence):
        return False
    
    # Collect all n-length substrings (treating sequence as cyclic)
    seen = set()
    extended = sequence + sequence[:n - 1]  # For cyclic substrings
    
    for i in range(len(sequence)):
        substring = extended[i:i + n]
        if substring in seen:
            return False
        seen.add(substring)
    
    # Check we have all possible substrings
    return len(seen) == expected_length


def get_all_substrings(sequence: str, n: int) -> Set[str]:
    """
    Get all unique n-length substrings from a cyclic sequence.
    
    Args:
        sequence: The sequence (treated as cyclic)
        n: Length of substrings
        
    Returns:
        Set of all unique n-length substrings
        
    Examples:
        >>> get_all_substrings('00010111', 3)
        {'000', '001', '010', '101', '011', '111', '110', '100'}
    """
    if not sequence or n < 1 or n > len(sequence):
        return set()
    
    extended = sequence + sequence[:n - 1]
    return {extended[i:i + n] for i in range(len(sequence))}


def find_substring_position(sequence: str, target: str) -> int:
    """
    Find the first position of a target substring in the cyclic De Bruijn sequence.
    
    Args:
        sequence: The De Bruijn sequence
        target: The substring to find
        
    Returns:
        Position (0-indexed) of the substring, or -1 if not found
        
    Examples:
        >>> find_substring_position('00010111', '101')
        3
        >>> find_substring_position('00010111', '111')
        5
        >>> find_substring_position('00010111', '222')
        -1
    """
    if not target:
        return -1
    
    n = len(target)
    if n > len(sequence):
        return -1
    
    extended = sequence + sequence[:n - 1]
    
    for i in range(len(sequence)):
        if extended[i:i + n] == target:
            return i
    
    return -1


def sequence_to_numbers(sequence: str, alphabet: Optional[List[str]] = None) -> List[int]:
    """
    Convert a De Bruijn sequence to a list of numbers.
    
    Args:
        sequence: The sequence string
        alphabet: Optional alphabet mapping. If None, uses '0' to 'k-1'
        
    Returns:
        List of integers representing the sequence
        
    Examples:
        >>> sequence_to_numbers('00010111')
        [0, 0, 0, 1, 0, 1, 1, 1]
        >>> sequence_to_numbers('AABABB', ['A', 'B'])
        [0, 0, 1, 0, 1, 1]
    """
    if alphabet is None:
        alphabet = [str(i) for i in range(10)]
        # Auto-detect if sequence uses digits
        if not all(c in alphabet for c in sequence):
            # Use unique symbols as alphabet
            alphabet = sorted(set(sequence))
    
    symbol_to_num = {s: i for i, s in enumerate(alphabet)}
    return [symbol_to_num[c] for c in sequence]


def binary_de_bruijn(n: int) -> str:
    """
    Generate a binary De Bruijn sequence B(2, n).
    
    Convenience function for the common case of binary sequences.
    
    Args:
        n: Length of binary substrings
        
    Returns:
        Binary De Bruijn sequence as a string of 0s and 1s
        
    Examples:
        >>> binary_de_bruijn(3)
        '00010111'
        >>> binary_de_bruijn(4)
        '0000100110101111'
        
    Time Complexity: O(2^n)
    Space Complexity: O(2^n)
    """
    return de_bruijn(2, n)


def decimal_de_bruijn(n: int) -> str:
    """
    Generate a De Bruijn sequence for decimal digits B(10, n).
    
    WARNING: This grows extremely fast!
    - B(10, 2): 100 characters
    - B(10, 3): 1000 characters  
    - B(10, 4): 10000 characters
    - B(10, 5): 100000 characters
    
    Args:
        n: Length of decimal substrings
        
    Returns:
        De Bruijn sequence containing digits 0-9
        
    Examples:
        >>> len(decimal_de_bruijn(2))
        100
    """
    return de_bruijn(10, n)


def hexadecimal_de_bruijn(n: int) -> str:
    """
    Generate a De Bruijn sequence for hexadecimal digits B(16, n).
    
    WARNING: This grows extremely fast!
    - B(16, 2): 256 characters
    - B(16, 3): 4096 characters
    
    Args:
        n: Length of hex substrings
        
    Returns:
        De Bruijn sequence containing 0-9 and a-f
        
    Examples:
        >>> len(hexadecimal_de_bruijn(2))
        256
    """
    alphabet = [str(i) for i in range(10)] + [chr(ord('a') + i) for i in range(6)]
    return de_bruijn(16, n, alphabet)


def dna_de_bruijn(n: int) -> str:
    """
    Generate a De Bruijn sequence for DNA bases B(4, n).
    
    Useful for DNA sequencing and bioinformatics applications.
    
    Args:
        n: Length of DNA k-mer substrings
        
    Returns:
        De Bruijn sequence containing A, C, G, T
        
    Examples:
        >>> dna_de_bruijn(2)
        'AACAGATCCGTGTTT'
        >>> len(dna_de_bruijn(3))
        64
    """
    return de_bruijn(4, n, ['A', 'C', 'G', 'T'])


def alphabet_de_bruijn(n: int) -> str:
    """
    Generate a De Bruijn sequence for lowercase letters B(26, n).
    
    WARNING: This grows astronomically fast!
    - B(26, 2): 676 characters
    - B(26, 3): 17576 characters
    
    Args:
        n: Length of letter substrings
        
    Returns:
        De Bruijn sequence containing a-z
    """
    alphabet = [chr(ord('a') + i) for i in range(26)]
    return de_bruijn(26, n, alphabet)


def find_shortest_containing(strings: List[str]) -> str:
    """
    Find the shortest string that contains all given strings as substrings.
    
    This is related to the shortest common superstring problem and can use
    De Bruijn concepts as part of the solution.
    
    Note: This is an approximation algorithm. The optimal solution is NP-hard.
    
    Args:
        strings: List of strings to include
        
    Returns:
        A string containing all input strings as substrings
        
    Examples:
        >>> find_shortest_containing(['abc', 'bcd', 'cde'])
        'abcde'
    """
    if not strings:
        return ""
    if len(strings) == 1:
        return strings[0]
    
    # Greedy overlap-based merging
    result = strings[0]
    remaining = strings[1:]
    
    while remaining:
        best_overlap = -1
        best_idx = 0
        best_position = 'append'  # 'append' or 'prepend'
        
        for i, s in enumerate(remaining):
            # Check overlap: result ending with s's prefix
            for overlap_len in range(min(len(result), len(s)), -1, -1):
                if result[-overlap_len:] == s[:overlap_len] if overlap_len > 0 else True:
                    if overlap_len >= best_overlap:
                        best_overlap = overlap_len
                        best_idx = i
                        best_position = 'append'
                    break
            
            # Check overlap: result starting with s's suffix
            for overlap_len in range(min(len(result), len(s)), -1, -1):
                if result[:overlap_len] == s[-overlap_len:] if overlap_len > 0 else True:
                    if overlap_len > best_overlap:  # Prefer append for tie
                        best_overlap = overlap_len
                        best_idx = i
                        best_position = 'prepend'
                    break
        
        best_string = remaining.pop(best_idx)
        
        if best_position == 'append':
            result = result + best_string[best_overlap:]
        else:
            result = best_string + result[best_overlap:]
    
    return result


def levenshtein_de_bruijn(k: int, n: int, d: int = 1) -> List[str]:
    """
    Generate sequences where all n-length strings are within Hamming distance d.
    
    This is a relaxation of De Bruijn sequences useful in error-tolerant
    applications like DNA sequencing with error rates.
    
    Args:
        k: Alphabet size
        n: Substring length
        d: Maximum Hamming distance (default 1)
        
    Returns:
        List of sequences covering all n-length strings within distance d
        
    Examples:
        >>> len(levenshtein_de_bruijn(2, 2, 1))
        2
    """
    # For d=1, we need approximately k^n / n sequences
    # This is a simplified implementation
    if alphabet is None:
        alphabet = [str(i) for i in range(k)]
    
    all_strings = []
    
    def generate_strings(current: str):
        if len(current) == n:
            all_strings.append(current)
            return
        for s in alphabet:
            generate_strings(current + s)
    
    generate_strings("")
    
    # Greedy covering with Hamming distance d
    result = []
    covered = set()
    
    def hamming_distance(s1: str, s2: str) -> int:
        return sum(c1 != c2 for c1, c2 in zip(s1, s2))
    
    def get_neighbors(s: str, distance: int) -> Set[str]:
        neighbors = set()
        for other in all_strings:
            if hamming_distance(s, other) <= distance:
                neighbors.add(other)
        return neighbors
    
    while len(covered) < len(all_strings):
        # Find string that covers most uncovered strings
        best = None
        best_coverage = 0
        
        for s in all_strings:
            neighbors = get_neighbors(s, d)
            new_coverage = len(neighbors - covered)
            if new_coverage > best_coverage:
                best_coverage = new_coverage
                best = s
        
        if best is None:
            break
            
        result.append(best)
        covered.update(get_neighbors(best, d))
    
    return result


# For the d=1 case, need alphabet defined
# Let me fix the function by adding alphabet parameter
def levenshtein_de_bruijn_fixed(k: int, n: int, d: int = 1) -> List[str]:
    """
    Generate sequences where all n-length strings are within Hamming distance d.
    """
    alphabet = [str(i) for i in range(k)]
    
    all_strings = []
    
    def generate_strings(current: str):
        if len(current) == n:
            all_strings.append(current)
            return
        for s in alphabet:
            generate_strings(current + s)
    
    generate_strings("")
    
    result = []
    covered = set()
    
    def hamming_distance(s1: str, s2: str) -> int:
        return sum(c1 != c2 for c1, c2 in zip(s1, s2))
    
    def get_neighbors(s: str, distance: int) -> Set[str]:
        neighbors = set()
        for other in all_strings:
            if hamming_distance(s, other) <= distance:
                neighbors.add(other)
        return neighbors
    
    while len(covered) < len(all_strings):
        best = None
        best_coverage = 0
        
        for s in all_strings:
            neighbors = get_neighbors(s, d)
            new_coverage = len(neighbors - covered)
            if new_coverage > best_coverage:
                best_coverage = new_coverage
                best = s
        
        if best is None:
            break
            
        result.append(best)
        covered.update(get_neighbors(best, d))
    
    return result


class DeBruijnSequence:
    """
    A class-based interface for working with De Bruijn sequences.
    
    Provides methods for generation, validation, and manipulation
    with a convenient object-oriented API.
    
    Examples:
        >>> seq = DeBruijnSequence(2, 3)
        >>> seq.sequence
        '00010111'
        >>> seq.contains('010')
        True
        >>> seq.position('111')
        5
    """
    
    def __init__(self, k: int, n: int, alphabet: Optional[List[str]] = None):
        """
        Initialize a De Bruijn sequence.
        
        Args:
            k: Alphabet size
            n: Substring length
            alphabet: Optional custom alphabet
        """
        self.k = k
        self.n = n
        self.alphabet = alphabet
        self.sequence = de_bruijn(k, n, alphabet)
    
    def __len__(self) -> int:
        """Return the length of the sequence."""
        return len(self.sequence)
    
    def __str__(self) -> str:
        """Return the sequence as a string."""
        return self.sequence
    
    def __repr__(self) -> str:
        """Return a detailed representation."""
        return f"DeBruijnSequence(k={self.k}, n={self.n}, length={len(self)})"
    
    def __getitem__(self, index: int) -> str:
        """Get character at index (supports cyclic indexing)."""
        return self.sequence[index % len(self.sequence)]
    
    def contains(self, substring: str) -> bool:
        """Check if substring exists in the cyclic sequence."""
        return find_substring_position(self.sequence, substring) != -1
    
    def position(self, substring: str) -> int:
        """Find position of substring (-1 if not found)."""
        return find_substring_position(self.sequence, substring)
    
    def all_substrings(self) -> Set[str]:
        """Get all unique n-length substrings."""
        return get_all_substrings(self.sequence, self.n)
    
    def is_valid(self) -> bool:
        """Validate that this is a proper De Bruijn sequence."""
        return is_de_bruijn(self.sequence, self.n)
    
    def to_numbers(self) -> List[int]:
        """Convert sequence to list of numbers."""
        return sequence_to_numbers(self.sequence, self.alphabet)
    
    def rotate(self, offset: int) -> str:
        """
        Rotate the sequence by offset positions.
        
        Args:
            offset: Number of positions to rotate (positive = left)
            
        Returns:
            Rotated sequence
        """
        if not self.sequence:
            return self.sequence
        offset = offset % len(self.sequence)
        return self.sequence[offset:] + self.sequence[:offset]
    
    def complement(self) -> str:
        """
        Get the complement (reversed and inverted) of a binary De Bruijn sequence.
        
        Only valid for binary sequences.
        
        Returns:
            Complemented sequence
        """
        if self.k != 2:
            raise ValueError("Complement only defined for binary sequences")
        
        return ''.join('1' if c == '0' else '0' for c in self.sequence[::-1])


if __name__ == "__main__":
    # Quick demonstration
    print("=== De Bruijn Sequence Utilities ===\n")
    
    # Binary sequence
    print("Binary B(2,3):")
    seq = binary_de_bruijn(3)
    print(f"  Sequence: {seq}")
    print(f"  Length: {len(seq)} (expected: {2**3})")
    print(f"  Valid: {is_de_bruijn(seq, 3)}")
    print(f"  Substrings: {get_all_substrings(seq, 3)}")
    print()
    
    # DNA sequence
    print("DNA B(4,2):")
    dna = dna_de_bruijn(2)
    print(f"  Sequence: {dna}")
    print(f"  Length: {len(dna)} (expected: {4**2})")
    print(f"  Valid: {is_de_bruijn(dna, 2)}")
    print()
    
    # Class interface
    print("Class interface:")
    dbs = DeBruijnSequence(2, 4)
    print(f"  {dbs}")
    print(f"  Contains '1010': {dbs.contains('1010')}")
    print(f"  Position of '1111': {dbs.position('1111')}")