"""
LIS (Longest Increasing Subsequence) Utils

A utility module for finding the Longest Increasing Subsequence and related operations.
Uses efficient O(n log n) algorithm based on binary search and patience sorting.

Features:
- Find length of LIS
- Find the actual LIS sequence
- Find multiple LIS (all possible LIS of same length)
- Find LDS (Longest Decreasing Subsequence)
- Find LNDS (Longest Non-Decreasing Subsequence)
- Find number of LIS
- Find LIS index positions

Zero external dependencies - uses only Python stdlib.
"""

from bisect import bisect_left, bisect_right
from typing import List, Tuple, Optional, Callable, Any


def lis_length(arr: List[int]) -> int:
    """
    Find the length of the Longest Increasing Subsequence.
    
    Uses O(n log n) algorithm with binary search.
    
    Args:
        arr: Input sequence of integers
        
    Returns:
        Length of the longest increasing subsequence
        
    Example:
        >>> lis_length([10, 9, 2, 5, 3, 7, 101, 18])
        4
        >>> lis_length([0, 1, 0, 3, 2, 3])
        4
    """
    if not arr:
        return 0
    
    tails = []
    for num in arr:
        pos = bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    return len(tails)


def lis_sequence(arr: List[int]) -> List[int]:
    """
    Find one Longest Increasing Subsequence.
    
    Uses O(n log n) algorithm and reconstructs the actual sequence.
    
    Args:
        arr: Input sequence of integers
        
    Returns:
        One of the longest increasing subsequences
        
    Example:
        >>> lis_sequence([10, 9, 2, 5, 3, 7, 101, 18])
        [2, 3, 7, 18]
        >>> lis_sequence([1, 3, 5, 4, 7])
        [1, 3, 4, 7]
    """
    if not arr:
        return []
    
    n = len(arr)
    # tails[i] = smallest tail element for LIS of length i+1
    tails = []
    # tails_idx[i] = index in arr of tails[i]
    tails_idx = []
    # prev[i] = index of previous element in LIS ending at arr[i]
    prev = [-1] * n
    
    for i, num in enumerate(arr):
        pos = bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
            tails_idx.append(i)
        else:
            tails[pos] = num
            tails_idx[pos] = i
        
        if pos > 0:
            prev[i] = tails_idx[pos - 1]
    
    # Reconstruct LIS
    result = []
    curr = tails_idx[-1]
    while curr != -1:
        result.append(arr[curr])
        curr = prev[curr]
    
    return result[::-1]


def lis_with_indices(arr: List[int]) -> Tuple[List[int], List[int]]:
    """
    Find LIS along with original indices.
    
    Args:
        arr: Input sequence of integers
        
    Returns:
        Tuple of (LIS sequence, indices in original array)
        
    Example:
        >>> lis_with_indices([10, 9, 2, 5, 3, 7, 101, 18])
        ([2, 3, 7, 18], [2, 4, 5, 7])
    """
    if not arr:
        return [], []
    
    n = len(arr)
    tails = []
    tails_idx = []
    prev = [-1] * n
    
    for i, num in enumerate(arr):
        pos = bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
            tails_idx.append(i)
        else:
            tails[pos] = num
            tails_idx[pos] = i
        
        if pos > 0:
            prev[i] = tails_idx[pos - 1]
    
    # Reconstruct
    indices = []
    curr = tails_idx[-1]
    while curr != -1:
        indices.append(curr)
        curr = prev[curr]
    
    indices = indices[::-1]
    sequence = [arr[i] for i in indices]
    
    return sequence, indices


def lds_length(arr: List[int]) -> int:
    """
    Find the length of the Longest Decreasing Subsequence.
    
    Args:
        arr: Input sequence of integers
        
    Returns:
        Length of the longest decreasing subsequence
        
    Example:
        >>> lds_length([10, 9, 2, 5, 3, 7, 101, 18])
        4
    """
    if not arr:
        return 0
    
    # Negate values and find LIS
    negated = [-x for x in arr]
    return lis_length(negated)


def lds_sequence(arr: List[int]) -> List[int]:
    """
    Find one Longest Decreasing Subsequence.
    
    Args:
        arr: Input sequence of integers
        
    Returns:
        One of the longest decreasing subsequences
        
    Example:
        >>> lds_sequence([10, 9, 2, 5, 3, 7, 101, 18])
        [10, 9, 5, 3]
    """
    if not arr:
        return []
    
    # Negate values and find LIS
    negated = [-x for x in arr]
    seq, idx = lis_with_indices(negated)
    return [arr[i] for i in idx]


def lnds_length(arr: List[int]) -> int:
    """
    Find the length of the Longest Non-Decreasing Subsequence.
    
    Non-decreasing means equal elements are allowed.
    
    Args:
        arr: Input sequence of integers
        
    Returns:
        Length of the longest non-decreasing subsequence
        
    Example:
        >>> lnds_length([1, 3, 5, 4, 7, 7, 2])
        5
    """
    if not arr:
        return 0
    
    tails = []
    for num in arr:
        # Use bisect_right for non-decreasing (allows equal elements)
        pos = bisect_right(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    return len(tails)


def lnds_sequence(arr: List[int]) -> List[int]:
    """
    Find one Longest Non-Decreasing Subsequence.
    
    Args:
        arr: Input sequence of integers
        
    Returns:
        One of the longest non-decreasing subsequences
        
    Example:
        >>> lnds_sequence([1, 3, 5, 4, 7, 7, 2])
        [1, 3, 4, 7, 7]
    """
    if not arr:
        return []
    
    n = len(arr)
    tails = []
    tails_idx = []
    prev = [-1] * n
    
    for i, num in enumerate(arr):
        pos = bisect_right(tails, num)
        if pos == len(tails):
            tails.append(num)
            tails_idx.append(i)
        else:
            tails[pos] = num
            tails_idx[pos] = i
        
        if pos > 0:
            prev[i] = tails_idx[pos - 1]
    
    result = []
    curr = tails_idx[-1]
    while curr != -1:
        result.append(arr[curr])
        curr = prev[curr]
    
    return result[::-1]


def count_lis(arr: List[int]) -> int:
    """
    Count the number of Longest Increasing Subsequences.
    
    Uses O(n^2) DP approach for counting.
    Note: For sequences with duplicates, counts distinct index-based LIS,
    not unique value sequences.
    
    Args:
        arr: Input sequence of integers
        
    Returns:
        Number of LIS (counting different index positions as different)
        
    Example:
        >>> count_lis([1, 3, 5, 4, 7])
        2
        >>> count_lis([2, 2, 2, 2, 2])
        5
    """
    if not arr:
        return 0
    
    n = len(arr)
    if n == 1:
        return 1
    
    # dp_len[i] = length of LIS ending at i
    # dp_cnt[i] = number of LIS ending at i with length dp_len[i]
    dp_len = [1] * n
    dp_cnt = [1] * n
    
    max_len = 1
    
    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i]:
                if dp_len[j] + 1 > dp_len[i]:
                    dp_len[i] = dp_len[j] + 1
                    dp_cnt[i] = dp_cnt[j]
                elif dp_len[j] + 1 == dp_len[i]:
                    dp_cnt[i] += dp_cnt[j]
        
        max_len = max(max_len, dp_len[i])
    
    # Sum up counts for all LIS of max length
    total = 0
    for i in range(n):
        if dp_len[i] == max_len:
            total += dp_cnt[i]
    
    return total


def lis_all_sequences(arr: List[int]) -> List[List[int]]:
    """
    Find all Longest Increasing Subsequences (unique by value).
    
    Warning: This can generate many sequences if there are many LIS.
    Use count_lis() first to check if feasible.
    
    Args:
        arr: Input sequence of integers
        
    Returns:
        List of all unique longest increasing subsequences
        
    Example:
        >>> lis_all_sequences([1, 3, 5, 4, 7])
        [[1, 3, 5, 7], [1, 3, 4, 7]]
    """
    if not arr:
        return [[]]
    
    n = len(arr)
    if n == 1:
        return [[arr[0]]]
    
    # dp_len[i] = length of LIS ending at i
    dp_len = [1] * n
    max_len = 1
    
    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i]:
                dp_len[i] = max(dp_len[i], dp_len[j] + 1)
        max_len = max(max_len, dp_len[i])
    
    # Backtrack using recursion to find all LIS
    def collect_lis(end_idx: int, target_len: int, current: List[int]) -> List[List[int]]:
        """Collect all LIS sequences ending at end_idx with given length."""
        if target_len == 1:
            return [current[::-1]]
        
        results = []
        last_val = current[-1] if current else None
        
        for j in range(end_idx):
            if dp_len[j] == target_len - 1 and arr[j] < last_val:
                results.extend(collect_lis(j, target_len - 1, current + [arr[j]]))
        
        return results
    
    # Find all LIS ending at positions with max_len
    all_results = []
    for i in range(n):
        if dp_len[i] == max_len:
            all_results.extend(collect_lis(i, max_len, [arr[i]]))
    
    # Remove duplicates (same value sequence)
    unique = []
    seen = set()
    for seq in all_results:
        t = tuple(seq)
        if t not in seen:
            seen.add(t)
            unique.append(seq)
    
    return unique


def lis_on_sequence(
    arr: List[Any],
    key: Callable[[Any], int] = lambda x: x
) -> List[Any]:
    """
    Find LIS on a sequence of arbitrary objects using a key function.
    
    Args:
        arr: Input sequence of any objects
        key: Function to extract comparable value from each object
        
    Returns:
        One of the longest increasing subsequences
        
    Example:
        >>> data = [{'val': 1}, {'val': 3}, {'val': 2}, {'val': 5}]
        >>> lis_on_sequence(data, key=lambda x: x['val'])
        [{'val': 1}, {'val': 2}, {'val': 5}]
    """
    if not arr:
        return []
    
    n = len(arr)
    tails = []  # list of key values
    tails_idx = []  # indices in arr
    prev = [-1] * n
    
    for i, obj in enumerate(arr):
        k_val = key(obj)
        pos = bisect_left(tails, k_val) if tails else 0
        
        if pos == len(tails):
            tails.append(k_val)
            tails_idx.append(i)
        else:
            tails[pos] = k_val
            tails_idx[pos] = i
        
        if pos > 0:
            prev[i] = tails_idx[pos - 1]
    
    # Reconstruct LIS
    result = []
    curr = tails_idx[-1]
    while curr != -1:
        result.append(arr[curr])
        curr = prev[curr]
    
    return result[::-1]


def minimum_removals_for_sorted(arr: List[int]) -> int:
    """
    Find minimum number of elements to remove to make array sorted.
    
    Equivalent to n - LIS_length.
    
    Args:
        arr: Input sequence of integers
        
    Returns:
        Minimum number of elements to remove
        
    Example:
        >>> minimum_removals_for_sorted([5, 2, 8, 6, 3, 6, 9, 5])
        4
    """
    return len(arr) - lis_length(arr)


def patience_sort(arr: List[int]) -> List[int]:
    """
    Sort using patience sorting algorithm.
    
    Patience sort is the algorithm used for LIS and has O(n log n) complexity.
    Named after the card game "Patience" (Solitaire).
    
    Args:
        arr: Input sequence of integers
        
    Returns:
        Sorted array
        
    Example:
        >>> patience_sort([5, 2, 8, 6, 3, 6, 9, 5])
        [2, 3, 5, 5, 6, 6, 8, 9]
    """
    if not arr:
        return []
    
    # Create piles
    piles = []
    pile_tops = []
    
    for num in arr:
        pos = bisect_left(pile_tops, num)
        if pos == len(piles):
            piles.append([num])
            pile_tops.append(num)
        else:
            piles[pos].append(num)
            pile_tops[pos] = num
    
    # Merge piles using k-way merge
    import heapq
    heap = []
    for i, pile in enumerate(piles):
        if pile:
            heapq.heappush(heap, (pile[-1], i))
    
    result = []
    while heap:
        _, pile_idx = heapq.heappop(heap)
        result.append(piles[pile_idx].pop())
        if piles[pile_idx]:
            heapq.heappush(heap, (piles[pile_idx][-1], pile_idx))
    
    return result


# Convenience function
def find_lis(arr: List[int], mode: str = "sequence") -> Any:
    """
    Convenience function to find LIS with different modes.
    
    Args:
        arr: Input sequence
        mode: One of "length", "sequence", "indices", "count"
        
    Returns:
        Result based on mode
        
    Example:
        >>> find_lis([10, 9, 2, 5, 3, 7, 101, 18], mode="length")
        4
        >>> find_lis([10, 9, 2, 5, 3, 7, 101, 18], mode="sequence")
        [2, 3, 7, 18]
    """
    modes = {
        "length": lis_length,
        "sequence": lis_sequence,
        "indices": lis_with_indices,
        "count": count_lis,
    }
    
    if mode not in modes:
        raise ValueError(f"Unknown mode: {mode}. Use one of {list(modes.keys())}")
    
    return modes[mode](arr)


if __name__ == "__main__":
    # Demo
    arr = [10, 9, 2, 5, 3, 7, 101, 18]
    print(f"Array: {arr}")
    print(f"LIS length: {lis_length(arr)}")
    print(f"LIS sequence: {lis_sequence(arr)}")
    print(f"LIS with indices: {lis_with_indices(arr)}")
    print(f"LDS length: {lds_length(arr)}")
    print(f"LDS sequence: {lds_sequence(arr)}")
    print(f"LNDS length: {lnds_length(arr)}")
    print(f"LNDS sequence: {lnds_sequence(arr)}")
    print(f"Count of LIS: {count_lis(arr)}")