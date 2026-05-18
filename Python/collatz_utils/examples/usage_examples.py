"""
AllToolkit - Python Collatz Utilities Usage Examples

This file demonstrates various use cases for the collatz_utils module.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from collatz_utils.mod import (
    collatz_sequence,
    collatz_length,
    collatz_max_value,
    collatz_even_odd_ratio,
    collatz_rise_and_fall,
    total_stopping_time,
    collatz_statistics,
    longest_sequence_in_range,
    highest_value_in_range,
    collatz_summary,
    collatz_waterfall,
    collatz_tree_path,
    generalized_collatz_sequence,
    collatz_predecessors,
    collatz_inverse_tree,
    find_numbers_reaching_value,
    find_numbers_with_length,
)


def example_basic_sequence():
    """Example: Generate a basic Collatz sequence."""
    print("=" * 60)
    print("Example 1: Basic Collatz Sequence")
    print("=" * 60)
    
    # The famous sequence for 27
    print("\nCollatz sequence for 27:")
    seq = collatz_sequence(27)
    print(f"Length: {len(seq)}")
    print(f"Maximum value: {max(seq)}")
    print(f"First 10 values: {seq[:10]}")
    print(f"Last 10 values: {seq[-10:]}")
    
    # Simple sequence for 6
    print("\nCollatz sequence for 6:")
    print(collatz_sequence(6))


def example_sequence_properties():
    """Example: Analyze sequence properties."""
    print("\n" + "=" * 60)
    print("Example 2: Sequence Properties Analysis")
    print("=" * 60)
    
    numbers = [6, 7, 27, 100, 1000]
    
    for n in numbers:
        length = collatz_length(n)
        max_val = collatz_max_value(n)
        even, odd = collatz_even_odd_ratio(n)
        rises, falls = collatz_rise_and_fall(n)
        
        print(f"\nNumber: {n}")
        print(f"  Sequence length: {length}")
        print(f"  Maximum value: {max_val}")
        print(f"  Even/Odd ratio: {even}/{odd}")
        print(f"  Rises/Falls: {rises}/{falls}")


def example_range_statistics():
    """Example: Calculate statistics for a range of numbers."""
    print("\n" + "=" * 60)
    print("Example 3: Range Statistics")
    print("=" * 60)
    
    # Statistics for 1-100
    stats = collatz_statistics(1, 100)
    
    print("\nStatistics for numbers 1-100:")
    print(f"  Count: {stats['count']}")
    print(f"  Average length: {stats['avg_length']:.2f}")
    print(f"  Min length: {stats['min_length']}")
    print(f"  Max length: {stats['max_length']}")
    print(f"  Number with max length: {stats['max_length_number']}")
    print(f"  Highest max value: {stats['highest_max_value']}")
    print(f"  Number with highest max: {stats['highest_max_number']}")
    print(f"  Even ratio: {stats['even_ratio']:.2%}")


def example_find_longest_sequences():
    """Example: Find numbers with longest sequences."""
    print("\n" + "=" * 60)
    print("Example 4: Finding Longest Sequences")
    print("=" * 60)
    
    # Find longest sequence in 1-1000
    num, length, seq = longest_sequence_in_range(1, 1000)
    
    print(f"\nIn range 1-1000:")
    print(f"  Number with longest sequence: {num}")
    print(f"  Sequence length: {length}")
    print(f"  Maximum value in sequence: {max(seq)}")


def example_find_highest_values():
    """Example: Find numbers that reach highest values."""
    print("\n" + "=" * 60)
    print("Example 5: Finding Highest Values")
    print("=" * 60)
    
    # Find highest max value in 1-1000
    num, max_val, step = highest_value_in_range(1, 1000)
    
    print(f"\nIn range 1-1000:")
    print(f"  Number that reaches highest value: {num}")
    print(f"  Highest value reached: {max_val}")
    print(f"  Step at which max occurs: {step}")


def example_pattern_detection():
    """Example: Find patterns in Collatz sequences."""
    print("\n" + "=" * 60)
    print("Example 6: Pattern Detection")
    print("=" * 60)
    
    # Find numbers that reach a specific value
    print("\nNumbers 1-100 that reach 16:")
    result = find_numbers_reaching_value(16, 100)
    print(f"  Found: {result}")
    
    # Find numbers with specific length
    print("\nNumbers 1-100 with sequence length 9:")
    result = find_numbers_with_length(9, 100)
    print(f"  Found: {result}")


def example_visualization():
    """Example: Generate visualization helpers."""
    print("\n" + "=" * 60)
    print("Example 7: Visualization Helpers")
    print("=" * 60)
    
    # Waterfall visualization
    print("\nWaterfall visualization for 7:")
    print(collatz_waterfall(7))
    
    # Tree path with operations
    print("\nTree path for 6:")
    path = collatz_tree_path(6)
    for value, op in path:
        print(f"  {value} ({op})")


def example_comprehensive_summary():
    """Example: Generate a comprehensive summary."""
    print("\n" + "=" * 60)
    print("Example 8: Comprehensive Summary")
    print("=" * 60)
    
    summary = collatz_summary(27)
    
    print(f"\nSummary for 27:")
    print(f"  Number: {summary['number']}")
    print(f"  Sequence length: {summary['length']}")
    print(f"  Total stopping time: {summary['total_stopping_time']}")
    print(f"  Maximum value: {summary['max_value']}")
    print(f"  Max value at step: {summary['max_value_step']}")
    print(f"  Even count: {summary['even_count']}")
    print(f"  Odd count: {summary['odd_count']}")
    print(f"  Rise count: {summary['rise_count']}")
    print(f"  Fall count: {summary['fall_count']}")
    print(f"  Average step size: {summary['average_step_size']:.2f}")


def example_generalized_collatz():
    """Example: Generalized Collatz sequences."""
    print("\n" + "=" * 60)
    print("Example 9: Generalized Collatz Sequences")
    print("=" * 60)
    
    # 5n+1 variant (known to potentially diverge)
    print("\n5n+1 variant for 7:")
    seq = generalized_collatz_sequence(7, a=5, b=1, c=2, max_iterations=50)
    print(f"  First 10 values: {seq[:10]}")
    print(f"  Length: {len(seq)}")
    
    # Custom parameters
    print("\nCustom (7n+1, divide by 3) for 10:")
    seq = generalized_collatz_sequence(10, a=7, b=1, c=3, max_iterations=30)
    print(f"  Sequence: {seq}")


def example_inverse_tree():
    """Example: Build an inverse Collatz tree."""
    print("\n" + "=" * 60)
    print("Example 10: Inverse Collatz Tree")
    print("=" * 60)
    
    # Build tree from 1 going backwards
    print("\nInverse tree from 1 (2 levels):")
    tree = collatz_inverse_tree(1, depth=2)
    for node, predecessors in sorted(tree.items()):
        print(f"  {node} -> {predecessors}")
    
    # Find predecessors of specific values
    print("\nDirect predecessors of 5:")
    preds = collatz_predecessors(5)
    print(f"  {preds}")
    
    print("\nDirect predecessors of 4:")
    preds = collatz_predecessors(4)
    print(f"  {preds}")


def example_stopping_times():
    """Example: Calculate stopping times."""
    print("\n" + "=" * 60)
    print("Example 11: Stopping Time Analysis")
    print("=" * 60)
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 10, 27, 100]
    
    print("\nTotal stopping times:")
    print(f"{'Number':<10} {'Stopping Time':<15} {'Sequence Length':<15}")
    print("-" * 40)
    
    for n in numbers:
        stopping = total_stopping_time(n)
        length = collatz_length(n)
        print(f"{n:<10} {stopping:<15} {length:<15}")


def example_famous_numbers():
    """Example: Analyze famous Collatz numbers."""
    print("\n" + "=" * 60)
    print("Example 12: Famous Collatz Numbers")
    print("=" * 60)
    
    famous_numbers = {
        27: "The famous long sequence",
        703: "Reaches 250504 at step 148",
        9663: "Reaches 27114424 at step 158",
        27: "Smallest number reaching 9232",
    }
    
    print("\nAnalysis of famous Collatz numbers:")
    for n, description in famous_numbers.items():
        length = collatz_length(n)
        max_val = collatz_max_value(n)
        stopping = total_stopping_time(n)
        
        print(f"\n{n} - {description}:")
        print(f"  Sequence length: {length}")
        print(f"  Total stopping time: {stopping}")
        print(f"  Maximum value: {max_val}")


def run_all_examples():
    """Run all examples."""
    print("\n" + "#" * 60)
    print("# AllToolkit Collatz Utilities - Usage Examples")
    print("#" * 60)
    
    example_basic_sequence()
    example_sequence_properties()
    example_range_statistics()
    example_find_longest_sequences()
    example_find_highest_values()
    example_pattern_detection()
    example_visualization()
    example_comprehensive_summary()
    example_generalized_collatz()
    example_inverse_tree()
    example_stopping_times()
    example_famous_numbers()
    
    print("\n" + "#" * 60)
    print("# Examples Complete!")
    print("#" * 60)


if __name__ == '__main__':
    run_all_examples()