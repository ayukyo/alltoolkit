"""
AllToolkit - Python Collatz Sequence Utilities

A zero-dependency module for working with the Collatz conjecture (3n+1 problem).
Provides sequence generation, analysis, cycle detection, and visualization helpers.

The Collatz conjecture states that for any positive integer n, repeatedly applying:
  - n/2 if n is even
  - 3n+1 if n is odd
Will eventually reach 1. This remains an unsolved problem in mathematics!

Features:
- Generate Collatz sequences
- Calculate sequence lengths
- Find maximum values in sequences
- Analyze stopping times
- Detect patterns and properties
- Generate statistics for ranges

Author: AllToolkit
License: MIT
"""

from typing import List, Tuple, Dict, Optional, Iterator, Set
from functools import lru_cache
import math


class CollatzError(Exception):
    """Base exception for Collatz operations."""
    pass


class InvalidInputError(CollatzError):
    """Raised when input is invalid."""
    pass


class MaxIterationsError(CollatzError):
    """Raised when maximum iterations is exceeded."""
    pass


# ============================================================================
# Core Collatz Functions
# ============================================================================

def collatz_step(n: int) -> int:
    """
    Apply one step of the Collatz function.
    
    Args:
        n: A positive integer
        
    Returns:
        Next number in the Collatz sequence
        
    Raises:
        InvalidInputError: If n is not a positive integer
        
    Examples:
        >>> collatz_step(6)
        3
        >>> collatz_step(7)
        22
        >>> collatz_step(1)
        4
    """
    if not isinstance(n, int) or n < 1:
        raise InvalidInputError(f"Input must be a positive integer, got {n}")
    
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1


def collatz_sequence(n: int, max_iterations: int = 10000) -> List[int]:
    """
    Generate the complete Collatz sequence starting from n.
    
    Args:
        n: Starting positive integer
        max_iterations: Safety limit to prevent infinite loops
        
    Returns:
        List of integers in the sequence (including starting n and ending 1)
        
    Raises:
        InvalidInputError: If n is not a positive integer
        MaxIterationsError: If max_iterations is exceeded
        
    Examples:
        >>> collatz_sequence(6)
        [6, 3, 10, 5, 16, 8, 4, 2, 1]
        >>> collatz_sequence(7)
        [7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
    """
    if not isinstance(n, int) or n < 1:
        raise InvalidInputError(f"Input must be a positive integer, got {n}")
    
    sequence = [n]
    current = n
    iterations = 0
    
    while current != 1:
        current = collatz_step(current)
        sequence.append(current)
        iterations += 1
        
        if iterations >= max_iterations:
            raise MaxIterationsError(
                f"Exceeded {max_iterations} iterations for n={n}. "
                "This may indicate a counterexample to the Collatz conjecture!"
            )
    
    return sequence


def collatz_generator(n: int, max_iterations: int = 100000) -> Iterator[int]:
    """
    Generator that yields Collatz sequence values one at a time.
    
    Memory-efficient way to iterate through a Collatz sequence.
    
    Args:
        n: Starting positive integer
        max_iterations: Safety limit
        
    Yields:
        Each integer in the sequence
        
    Examples:
        >>> list(collatz_generator(6))
        [6, 3, 10, 5, 16, 8, 4, 2, 1]
    """
    if not isinstance(n, int) or n < 1:
        raise InvalidInputError(f"Input must be a positive integer, got {n}")
    
    current = n
    iterations = 0
    
    while True:
        yield current
        if current == 1:
            break
        current = collatz_step(current)
        iterations += 1
        
        if iterations >= max_iterations:
            raise MaxIterationsError(
                f"Exceeded {max_iterations} iterations for n={n}"
            )


# ============================================================================
# Sequence Properties
# ============================================================================

def collatz_length(n: int, max_iterations: int = 100000) -> int:
    """
    Calculate the length of the Collatz sequence for n.
    
    This is also called the "stopping time" + 1 (includes both start and end).
    
    Args:
        n: Starting positive integer
        max_iterations: Safety limit
        
    Returns:
        Number of steps until reaching 1 (including start and end)
        
    Examples:
        >>> collatz_length(6)
        9
        >>> collatz_length(1)
        1
    """
    if n == 1:
        return 1
    
    count = 1  # Start with the initial number
    current = n
    iterations = 0
    
    while current != 1:
        current = collatz_step(current)
        count += 1
        iterations += 1
        
        if iterations >= max_iterations:
            raise MaxIterationsError(
                f"Exceeded {max_iterations} iterations for n={n}"
            )
    
    return count


@lru_cache(maxsize=100000)
def collatz_length_cached(n: int) -> int:
    """
    Cached version of collatz_length for better performance on repeated calls.
    
    Args:
        n: Starting positive integer
        
    Returns:
        Number of steps until reaching 1
        
    Note:
        Uses LRU cache with maxsize=100000 for memoization
    """
    if n == 1:
        return 1
    return 1 + collatz_length_cached(collatz_step(n))


def collatz_max_value(n: int, max_iterations: int = 100000) -> int:
    """
    Find the maximum value reached in the Collatz sequence.
    
    Args:
        n: Starting positive integer
        max_iterations: Safety limit
        
    Returns:
        Maximum value in the sequence
        
    Examples:
        >>> collatz_max_value(6)
        16
        >>> collatz_max_value(27)
        9232
    """
    if n == 1:
        return 1
    
    max_val = n
    current = n
    iterations = 0
    
    while current != 1:
        current = collatz_step(current)
        max_val = max(max_val, current)
        iterations += 1
        
        if iterations >= max_iterations:
            raise MaxIterationsError(
                f"Exceeded {max_iterations} iterations for n={n}"
            )
    
    return max_val


def collatz_even_odd_ratio(n: int, max_iterations: int = 100000) -> Tuple[int, int]:
    """
    Count the number of even and odd values in the Collatz sequence.
    
    Args:
        n: Starting positive integer
        max_iterations: Safety limit
        
    Returns:
        Tuple of (even_count, odd_count)
        
    Examples:
        >>> collatz_even_odd_ratio(6)
        (6, 3)
    """
    if n == 1:
        return (1, 0)
    
    even_count = 0
    odd_count = 0
    current = n
    iterations = 0
    
    while True:
        if current % 2 == 0:
            even_count += 1
        else:
            odd_count += 1
        
        if current == 1:
            break
            
        current = collatz_step(current)
        iterations += 1
        
        if iterations >= max_iterations:
            raise MaxIterationsError(
                f"Exceeded {max_iterations} iterations for n={n}"
            )
    
    return (even_count, odd_count)


def collatz_rise_and_fall(n: int, max_iterations: int = 100000) -> Tuple[int, int]:
    """
    Count how many times the sequence rises (n -> 3n+1) vs falls (n -> n/2).
    
    Args:
        n: Starting positive integer
        max_iterations: Safety limit
        
    Returns:
        Tuple of (rises, falls)
        
    Examples:
        >>> collatz_rise_and_fall(6)
        (3, 5)
    """
    if n == 1:
        return (0, 0)
    
    rises = 0
    falls = 0
    current = n
    iterations = 0
    
    while current != 1:
        next_val = collatz_step(current)
        if next_val > current:
            rises += 1
        else:
            falls += 1
        current = next_val
        iterations += 1
        
        if iterations >= max_iterations:
            raise MaxIterationsError(
                f"Exceeded {max_iterations} iterations for n={n}"
            )
    
    return (rises, falls)


# ============================================================================
# Stopping Time Variants
# ============================================================================

def total_stopping_time(n: int, max_iterations: int = 100000) -> int:
    """
    Calculate the total stopping time (steps to reach 1).
    
    This is collatz_length(n) - 1.
    
    Args:
        n: Starting positive integer
        max_iterations: Safety limit
        
    Returns:
        Number of steps to reach 1
        
    Examples:
        >>> total_stopping_time(6)
        8
        >>> total_stopping_time(1)
        0
    """
    return collatz_length(n, max_iterations) - 1


def stopping_time_to_value(n: int, target: int, max_iterations: int = 100000) -> Optional[int]:
    """
    Calculate steps to reach a specific target value.
    
    Args:
        n: Starting positive integer
        target: Target value to reach
        max_iterations: Safety limit
        
    Returns:
        Number of steps to reach target, or None if never reached
        
    Examples:
        >>> stopping_time_to_value(6, 10)
        2
        >>> stopping_time_to_value(6, 5)
        3
    """
    if n == target:
        return 0
    
    current = n
    steps = 0
    iterations = 0
    
    while current != target and current != 1:
        current = collatz_step(current)
        steps += 1
        iterations += 1
        
        if iterations >= max_iterations:
            raise MaxIterationsError(
                f"Exceeded {max_iterations} iterations for n={n}"
            )
    
    return steps if current == target else None


# ============================================================================
# Range Analysis
# ============================================================================

def longest_sequence_in_range(start: int, end: int) -> Tuple[int, int, List[int]]:
    """
    Find the number in a range with the longest Collatz sequence.
    
    Args:
        start: Start of range (inclusive)
        end: End of range (inclusive)
        
    Returns:
        Tuple of (number, length, sequence)
        
    Examples:
        >>> longest_sequence_in_range(1, 10)
        (9, 20, [9, 28, 14, 7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1])
    """
    max_length = 0
    max_number = start
    max_sequence = [start]
    
    for n in range(start, end + 1):
        seq = collatz_sequence(n)
        if len(seq) > max_length:
            max_length = len(seq)
            max_number = n
            max_sequence = seq
    
    return (max_number, max_length, max_sequence)


def highest_value_in_range(start: int, end: int) -> Tuple[int, int, int]:
    """
    Find the number in a range that reaches the highest maximum value.
    
    Args:
        start: Start of range (inclusive)
        end: End of range (inclusive)
        
    Returns:
        Tuple of (number, max_value_reached, step_at_max)
        
    Examples:
        >>> highest_value_in_range(1, 10)
        (9, 52, 9)
    """
    highest_max = 0
    best_number = start
    step_at_max = 0
    
    for n in range(start, end + 1):
        max_val = collatz_max_value(n)
        if max_val > highest_max:
            highest_max = max_val
            best_number = n
            seq = collatz_sequence(n)
            step_at_max = seq.index(max_val)
    
    return (best_number, highest_max, step_at_max)


def collatz_statistics(start: int, end: int) -> Dict[str, any]:
    """
    Calculate statistics for Collatz sequences in a range.
    
    Args:
        start: Start of range (inclusive)
        end: End of range (inclusive)
        
    Returns:
        Dictionary with statistics:
        - count: Number of sequences analyzed
        - avg_length: Average sequence length
        - min_length: Minimum sequence length
        - max_length: Maximum sequence length
        - max_length_number: Number with longest sequence
        - avg_max_value: Average maximum value reached
        - highest_max_value: Highest maximum value
        - highest_max_number: Number with highest max value
        - total_even: Total even numbers across all sequences
        - total_odd: Total odd numbers across all sequences
        
    Examples:
        >>> stats = collatz_statistics(1, 10)
        >>> stats['max_length']
        20
    """
    lengths = []
    max_values = []
    all_even = 0
    all_odd = 0
    
    for n in range(start, end + 1):
        lengths.append(collatz_length(n))
        max_values.append(collatz_max_value(n))
        even, odd = collatz_even_odd_ratio(n)
        all_even += even
        all_odd += odd
    
    count = end - start + 1
    
    return {
        'count': count,
        'avg_length': sum(lengths) / count,
        'min_length': min(lengths),
        'max_length': max(lengths),
        'max_length_number': start + lengths.index(max(lengths)),
        'avg_max_value': sum(max_values) / count,
        'highest_max_value': max(max_values),
        'highest_max_number': start + max_values.index(max(max_values)),
        'total_even': all_even,
        'total_odd': all_odd,
        'even_ratio': all_even / (all_even + all_odd) if (all_even + all_odd) > 0 else 0,
    }


# ============================================================================
# Pattern Detection
# ============================================================================

def find_numbers_reaching_value(target: int, limit: int = 1000) -> List[int]:
    """
    Find all numbers up to limit that reach a specific value in their sequence.
    
    Args:
        target: Target value to search for
        limit: Maximum number to check
        
    Returns:
        List of numbers that reach the target value
        
    Examples:
        >>> find_numbers_reaching_value(16, 20)
        [5, 10, 16, 20]
    """
    result = []
    
    for n in range(1, limit + 1):
        seq = collatz_sequence(n)
        if target in seq:
            result.append(n)
    
    return result


def find_numbers_with_length(length: int, limit: int = 1000) -> List[int]:
    """
    Find all numbers up to limit with a specific sequence length.
    
    Args:
        length: Target sequence length
        limit: Maximum number to check
        
    Returns:
        List of numbers with the specified sequence length
        
    Examples:
        >>> find_numbers_with_length(9, 20)
        [6]
    """
    result = []
    
    for n in range(1, limit + 1):
        if collatz_length(n) == length:
            result.append(n)
    
    return result


def find_numbers_with_max_value(max_val: int, limit: int = 1000) -> List[int]:
    """
    Find all numbers up to limit whose sequence reaches a specific maximum value.
    
    Args:
        max_val: Target maximum value
        limit: Maximum number to check
        
    Returns:
        List of numbers whose sequence reaches max_val as maximum
    """
    result = []
    
    for n in range(1, limit + 1):
        if collatz_max_value(n) == max_val:
            result.append(n)
    
    return result


# ============================================================================
# Extended Collatz Variants
# ============================================================================

def generalized_collatz_sequence(n: int, a: int = 3, b: int = 1, 
                                  c: int = 2, max_iterations: int = 10000) -> List[int]:
    """
    Generate a generalized Collatz sequence.
    
    The generalized Collatz function is:
    - n/c if n ≡ 0 (mod c)
    - a*n + b if n ≢ 0 (mod c)
    
    The standard Collatz uses a=3, b=1, c=2.
    
    Args:
        n: Starting positive integer
        a: Multiplier for odd step (default 3)
        b: Adder for odd step (default 1)
        c: Divisor for even step (default 2)
        max_iterations: Safety limit
        
    Returns:
        List of integers in the sequence
        
    Examples:
        >>> generalized_collatz_sequence(6)  # Same as standard
        [6, 3, 10, 5, 16, 8, 4, 2, 1]
        >>> generalized_collatz_sequence(7, a=5, b=1, c=2)  # 5n+1 variant
        [7, 36, 18, 9, 46, 23, 116, 58, 29, 146, 73, 366, 183, 916, 458, 229, 1146, 573, 2866, 1433, ...]
    """
    if not isinstance(n, int) or n < 1:
        raise InvalidInputError(f"Input must be a positive integer, got {n}")
    
    sequence = [n]
    current = n
    iterations = 0
    
    while current != 1:
        if current % c == 0:
            current = current // c
        else:
            current = a * current + b
        sequence.append(current)
        iterations += 1
        
        if iterations >= max_iterations:
            raise MaxIterationsError(
                f"Exceeded {max_iterations} iterations for n={n}"
            )
        
        # Safety check for overflow
        if current > 10**15:
            raise MaxIterationsError(
                f"Value exceeded 10^15 for n={n}, may diverge"
            )
    
    return sequence


def lazy_caterer_sequence(n: int, max_iterations: int = 10000) -> List[int]:
    """
    Generate the "lazy caterer" variant Collatz sequence.
    
    This is the 5n+1 problem, known to have some numbers that may not reach 1.
    
    Args:
        n: Starting positive integer
        max_iterations: Safety limit
        
    Returns:
        List of integers in the sequence
        
    Note:
        This variant may not always converge to 1!
    """
    return generalized_collatz_sequence(n, a=5, b=1, c=2, max_iterations=max_iterations)


# ============================================================================
# Visualization Helpers
# ============================================================================

def collatz_tree_path(n: int) -> List[Tuple[int, str]]:
    """
    Generate the Collatz path with operation labels.
    
    Args:
        n: Starting positive integer
        
    Returns:
        List of (value, operation) tuples
        
    Examples:
        >>> collatz_tree_path(6)
        [(6, 'start'), (3, '/2'), (10, '*3+1'), (5, '/2'), (16, '*3+1'), (8, '/2'), (4, '/2'), (2, '/2'), (1, '/2')]
    """
    if n == 1:
        return [(1, 'start')]
    
    path = [(n, 'start')]
    current = n
    
    while current != 1:
        if current % 2 == 0:
            current = current // 2
            path.append((current, '/2'))
        else:
            current = 3 * current + 1
            path.append((current, '*3+1'))
    
    return path


def collatz_waterfall(n: int, width: int = 40) -> str:
    """
    Generate a text-based "waterfall" visualization of the Collatz sequence.
    
    Args:
        n: Starting positive integer
        width: Width of the output (default 40)
        
    Returns:
        String representation of the sequence
        
    Examples:
        >>> print(collatz_waterfall(7))
        7 → 22 → 11 → 34 → 17 → 52 → 26 → 13
        ↓
        40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1
    """
    seq = collatz_sequence(n)
    
    # Find the maximum value for positioning
    max_val = max(seq)
    max_idx = seq.index(max_val)
    
    lines = []
    current_line = []
    
    for i, val in enumerate(seq):
        current_line.append(str(val))
        
        # Start new line at max value or when line gets too long
        if i == max_idx or len(' → '.join(current_line)) > width - 10:
            if current_line:
                lines.append(' → '.join(current_line))
                current_line = []
    
    if current_line:
        lines.append(' → '.join(current_line))
    
    return '\n↓\n'.join(lines)


def collatz_summary(n: int) -> Dict[str, any]:
    """
    Generate a comprehensive summary of a number's Collatz sequence.
    
    Args:
        n: Starting positive integer
        
    Returns:
        Dictionary with all key metrics
        
    Examples:
        >>> collatz_summary(27)
        {'number': 27, 'length': 112, 'total_stopping_time': 111, 'max_value': 9232, 'max_value_step': 78, ...}
    """
    seq = collatz_sequence(n)
    max_val = max(seq)
    even, odd = collatz_even_odd_ratio(n)
    rises, falls = collatz_rise_and_fall(n)
    
    return {
        'number': n,
        'length': len(seq),
        'total_stopping_time': len(seq) - 1,
        'max_value': max_val,
        'max_value_step': seq.index(max_val),
        'sequence': seq,
        'even_count': even,
        'odd_count': odd,
        'rise_count': rises,
        'fall_count': falls,
        'average_step_size': sum(abs(seq[i+1] - seq[i]) for i in range(len(seq)-1)) / (len(seq) - 1) if len(seq) > 1 else 0,
    }


# ============================================================================
# Utility Functions
# ============================================================================

def is_collatz_number(n: int) -> bool:
    """
    Check if a number eventually reaches 1 under the Collatz function.
    
    Since the Collatz conjecture is unproven, this might not terminate
    for potential counterexamples. Use with caution for very large numbers.
    
    Args:
        n: Number to check
        
    Returns:
        True (always, assuming the conjecture is true)
        
    Raises:
        MaxIterationsError: If max iterations exceeded
    """
    try:
        collatz_sequence(n)
        return True
    except MaxIterationsError:
        raise MaxIterationsError(
            f"Could not verify that {n} reaches 1. "
            "This might be a counterexample to the Collatz conjecture!"
        )


def first_n_collatz_values(n: int) -> Dict[int, int]:
    """
    Get the first number that reaches each value 1 through n.
    
    Args:
        n: Maximum value to find first occurrence for
        
    Returns:
        Dictionary mapping values to the first number that reaches them
    """
    result = {}
    found = set()
    
    for start in range(1, n * 100):  # Heuristic limit
        seq = collatz_sequence(start)
        for val in seq:
            if val not in found and val <= n:
                result[val] = start
                found.add(val)
        
        if len(found) == n:
            break
    
    return result


def collatz_predecessors(n: int, max_predecessors: int = 100) -> Set[int]:
    """
    Find all numbers that lead to n in one Collatz step.
    
    Args:
        n: Target number
        max_predecessors: Maximum number of predecessors to find
        
    Returns:
        Set of predecessors
        
    Examples:
        >>> collatz_predecessors(5)
        {10}
        >>> collatz_predecessors(4)
        {1, 8}
    """
    predecessors = set()
    
    # Even predecessor: n * 2 always works
    predecessors.add(n * 2)
    
    # Odd predecessor: (n - 1) / 3 if valid
    if (n - 1) % 3 == 0:
        odd_pred = (n - 1) // 3
        if odd_pred > 1 and odd_pred % 2 == 1:  # Must be odd and > 1
            predecessors.add(odd_pred)
    
    return predecessors


def collatz_inverse_tree(n: int, depth: int = 5) -> Dict[int, List[int]]:
    """
    Generate an inverse Collatz tree (numbers that lead to n).
    
    Args:
        n: Root number
        depth: How many levels to generate
        
    Returns:
        Dictionary mapping each number to its direct predecessors
    """
    tree = {}
    current_level = {n}
    
    for _ in range(depth):
        next_level = set()
        for num in current_level:
            if num not in tree:
                preds = collatz_predecessors(num)
                tree[num] = sorted(list(preds))
                next_level.update(preds)
        current_level = next_level
    
    return tree