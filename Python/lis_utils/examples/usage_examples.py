"""
LIS Utils - Usage Examples

This file demonstrates various use cases for the LIS (Longest Increasing Subsequence) utils.
"""

import sys
sys.path.insert(0, '..')

from mod import (
    lis_length,
    lis_sequence,
    lis_with_indices,
    lds_length,
    lds_sequence,
    lnds_length,
    lnds_sequence,
    count_lis,
    lis_all_sequences,
    lis_on_sequence,
    minimum_removals_for_sorted,
    patience_sort,
    find_lis,
)


def example_1_basic_lis():
    """Example 1: Basic LIS finding"""
    print("=" * 50)
    print("Example 1: Basic LIS Finding")
    print("=" * 50)
    
    arr = [10, 9, 2, 5, 3, 7, 101, 18]
    print(f"Array: {arr}")
    print(f"LIS Length: {lis_length(arr)}")
    print(f"LIS Sequence: {lis_sequence(arr)}")
    print()


def example_2_lis_with_positions():
    """Example 2: Find LIS with original indices"""
    print("=" * 50)
    print("Example 2: LIS with Original Indices")
    print("=" * 50)
    
    arr = [10, 9, 2, 5, 3, 7, 101, 18]
    seq, indices = lis_with_indices(arr)
    
    print(f"Array: {arr}")
    print(f"LIS Sequence: {seq}")
    print(f"Original Indices: {indices}")
    
    # Reconstruct from indices
    reconstructed = [arr[i] for i in indices]
    print(f"Reconstructed: {reconstructed}")
    print()


def example_3_lds_lnds():
    """Example 3: Decreasing and Non-Decreasing variants"""
    print("=" * 50)
    print("Example 3: LDS and LNDS Variants")
    print("=" * 50)
    
    arr = [1, 3, 5, 4, 7, 7, 2]
    print(f"Array: {arr}")
    
    print(f"\nLongest Increasing Subsequence:")
    print(f"  Length: {lis_length(arr)}")
    print(f"  Sequence: {lis_sequence(arr)}")
    
    print(f"\nLongest Decreasing Subsequence:")
    print(f"  Length: {lds_length(arr)}")
    print(f"  Sequence: {lds_sequence(arr)}")
    
    print(f"\nLongest Non-Decreasing Subsequence (allows equal):")
    print(f"  Length: {lnds_length(arr)}")
    print(f"  Sequence: {lnds_sequence(arr)}")
    print()


def example_4_count_and_find_all():
    """Example 4: Count and find all LIS"""
    print("=" * 50)
    print("Example 4: Count and Find All LIS")
    print("=" * 50)
    
    arr = [1, 3, 5, 4, 7]
    print(f"Array: {arr}")
    print(f"LIS Length: {lis_length(arr)}")
    print(f"Number of LIS: {count_lis(arr)}")
    print(f"All LIS sequences:")
    
    all_lis = lis_all_sequences(arr)
    for i, seq in enumerate(all_lis, 1):
        print(f"  {i}. {seq}")
    print()


def example_5_custom_objects():
    """Example 5: LIS on custom objects with key function"""
    print("=" * 50)
    print("Example 5: LIS on Custom Objects")
    print("=" * 50)
    
    # List of students with scores
    students = [
        {'name': 'Alice', 'score': 85},
        {'name': 'Bob', 'score': 70},
        {'name': 'Charlie', 'score': 90},
        {'name': 'Diana', 'score': 75},
        {'name': 'Eve', 'score': 95},
    ]
    
    print("Students:")
    for s in students:
        print(f"  {s['name']}: {s['score']}")
    
    result = lis_on_sequence(students, key=lambda x: x['score'])
    print(f"\nLongest increasing score subsequence:")
    for s in result:
        print(f"  {s['name']}: {s['score']}")
    print()


def example_6_minimum_removals():
    """Example 6: Minimum removals to make array sorted"""
    print("=" * 50)
    print("Example 6: Minimum Removals for Sorted Array")
    print("=" * 50)
    
    arr = [5, 2, 8, 6, 3, 6, 9, 5]
    print(f"Array: {arr}")
    print(f"LIS: {lis_sequence(arr)} (length: {lis_length(arr)})")
    print(f"Minimum removals to make sorted: {minimum_removals_for_sorted(arr)}")
    print(f"Explanation: Remove {len(arr) - lis_length(arr)} elements to get sorted sequence")
    print()


def example_7_patience_sort():
    """Example 7: Patience sorting algorithm"""
    print("=" * 50)
    print("Example 7: Patience Sort")
    print("=" * 50)
    
    arr = [5, 2, 8, 6, 3, 6, 9, 5]
    print(f"Original: {arr}")
    print(f"Sorted:   {patience_sort(arr)}")
    
    # Note: LIS length equals number of piles in patience sorting
    print(f"\nLIS length ({lis_length(arr)}) = Number of piles in patience sort")
    print()


def example_8_practical_use_cases():
    """Example 8: Practical use cases"""
    print("=" * 50)
    print("Example 8: Practical Use Cases")
    print("=" * 50)
    
    # Use case 1: Box stacking problem (height sequence)
    heights = [4, 1, 6, 2, 5, 3, 8]
    print("Use case 1: Box stacking - find max stackable boxes")
    print(f"  Heights: {heights}")
    print(f"  Max stackable: {lis_sequence(heights)}")
    
    # Use case 2: Event scheduling (end times for maximum events)
    end_times = [3, 1, 6, 4, 5, 2, 9]
    print("\nUse case 2: Scheduling - find maximum events sequence")
    print(f"  End times: {end_times}")
    print(f"  Max events sequence: {lis_sequence(end_times)}")
    
    # Use case 3: Stock prices - find longest upward trend
    prices = [100, 95, 98, 102, 99, 105, 110, 108, 115]
    print("\nUse case 3: Stock prices - longest upward trend")
    print(f"  Prices: {prices}")
    print(f"  Longest upward: {lis_sequence(prices)}")
    print()


def example_9_convenience_function():
    """Example 9: Using the convenience find_lis function"""
    print("=" * 50)
    print("Example 9: Convenience find_lis Function")
    print("=" * 50)
    
    arr = [10, 9, 2, 5, 3, 7, 101, 18]
    print(f"Array: {arr}")
    
    print(f"\nMode 'length': {find_lis(arr, mode='length')}")
    print(f"Mode 'sequence': {find_lis(arr, mode='sequence')}")
    print(f"Mode 'indices': {find_lis(arr, mode='indices')}")
    print(f"Mode 'count': {find_lis(arr, mode='count')}")
    print()


def example_10_performance_comparison():
    """Example 10: Performance with larger arrays"""
    print("=" * 50)
    print("Example 10: Performance with Larger Arrays")
    print("=" * 50)
    
    import random
    import time
    
    # Generate random array
    sizes = [100, 1000, 10000]
    
    for size in sizes:
        arr = [random.randint(1, 10000) for _ in range(size)]
        
        start = time.time()
        length = lis_length(arr)
        length_time = time.time() - start
        
        start = time.time()
        seq = lis_sequence(arr)
        seq_time = time.time() - start
        
        print(f"Size {size}:")
        print(f"  LIS length: {length}")
        print(f"  lis_length time: {length_time*1000:.2f}ms")
        print(f"  lis_sequence time: {seq_time*1000:.2f}ms")
    
    print()


if __name__ == "__main__":
    example_1_basic_lis()
    example_2_lis_with_positions()
    example_3_lds_lnds()
    example_4_count_and_find_all()
    example_5_custom_objects()
    example_6_minimum_removals()
    example_7_patience_sort()
    example_8_practical_use_cases()
    example_9_convenience_function()
    example_10_performance_comparison()
    
    print("=" * 50)
    print("All examples completed!")
    print("=" * 50)