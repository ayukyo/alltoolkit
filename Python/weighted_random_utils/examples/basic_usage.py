#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Basic usage examples for Weighted Random Utilities."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from weighted_random_utils.mod import (
    weighted_choice,
    weighted_sample,
    weighted_shuffle,
    AliasMethod,
    normalize_weights,
    softmax_weights,
)


def demo_basic_selection():
    """Demonstrate basic weighted selection."""
    print("=" * 60)
    print("Basic Weighted Selection")
    print("=" * 60)
    
    items = ['apple', 'banana', 'cherry', 'date', 'elderberry']
    weights = [10, 20, 30, 25, 15]  # Relative weights
    
    print(f"\nItems: {items}")
    print(f"Weights: {weights}")
    
    # Normalize to see probabilities
    probs = normalize_weights(weights)
    print(f"Probabilities: {[f'{p:.1%}' for p in probs]}")
    
    # Single selection
    print(f"\nSelected item: {weighted_choice(items, weights)}")
    
    # Multiple selections
    print("\n5 selections (with replacement):")
    for i in range(5):
        print(f"  {i+1}. {weighted_choice(items, weights)}")
    
    # Sample without replacement
    print("\n3 selections (without replacement):")
    sample = weighted_sample(items, weights, k=3, replace=False)
    for i, item in enumerate(sample, 1):
        print(f"  {i}. {item}")


def demo_alias_method():
    """Demonstrate Alias method for efficient sampling."""
    print("\n" + "=" * 60)
    print("Alias Method - O(1) Sampling")
    print("=" * 60)
    
    items = ['common', 'uncommon', 'rare', 'epic', 'legendary']
    weights = [50, 25, 15, 8, 2]  # Game drop rates
    
    print(f"\nItems: {items}")
    print(f"Drop rates: {weights}")
    
    # Create alias table (preprocessing)
    alias = AliasMethod(items, weights)
    
    # Fast sampling
    print("\nSimulating 100 drops:")
    from collections import Counter
    drops = Counter(alias.sample_n(100))
    
    for item in items:
        print(f"  {item}: {drops[item]:3d} ({drops[item]}%)")


def demo_weighted_shuffle():
    """Demonstrate weighted shuffle."""
    print("\n" + "=" * 60)
    print("Weighted Shuffle")
    print("=" * 60)
    
    items = ['Task A', 'Task B', 'Task C', 'Task D']
    priorities = [4, 3, 2, 1]  # Higher = more important
    
    print(f"\nTasks: {items}")
    print(f"Priorities: {priorities}")
    
    print("\nPriority-based ordering (higher priority more likely first):")
    for trial in range(3):
        shuffled = weighted_shuffle(items, priorities)
        print(f"  Trial {trial + 1}: {' > '.join(shuffled)}")


def demo_softmax_weights():
    """Demonstrate softmax weight transformation."""
    print("\n" + "=" * 60)
    print("Softmax Weights")
    print("=" * 60)
    
    scores = [1.0, 2.0, 3.0, 4.0, 5.0]
    
    print(f"\nScores: {scores}")
    
    # Low temperature = more peaked distribution
    probs_low = softmax_weights(scores, temperature=0.5)
    print(f"\nLow temp (0.5): {[f'{p:.1%}' for p in probs_low]}")
    
    # Normal temperature
    probs_normal = softmax_weights(scores, temperature=1.0)
    print(f"Normal temp (1.0): {[f'{p:.1%}' for p in probs_normal]}")
    
    # High temperature = more uniform distribution
    probs_high = softmax_weights(scores, temperature=2.0)
    print(f"High temp (2.0): {[f'{p:.1%}' for p in probs_high]}")


def demo_statistical_analysis():
    """Demonstrate statistical analysis of weighted sampling."""
    print("\n" + "=" * 60)
    print("Statistical Analysis")
    print("=" * 60)
    
    from collections import Counter
    from weighted_random_utils.mod import entropy, effective_size
    
    items = ['A', 'B', 'C']
    weights = [1, 2, 3]
    
    print(f"\nItems: {items}")
    print(f"Weights: {weights}")
    
    # Run many trials
    trials = 10000
    results = [weighted_choice(items, weights) for _ in range(trials)]
    
    counter = Counter(results)
    print(f"\nResults from {trials} trials:")
    for item in items:
        expected = weights[items.index(item)] / sum(weights)
        actual = counter[item] / trials
        print(f"  {item}: expected {expected:.1%}, actual {actual:.1%}")
    
    # Entropy
    probs = normalize_weights(weights)
    print(f"\nEntropy: {entropy(probs):.4f} bits (max: {entropy([1/3]*3):.4f} bits)")
    
    # Effective sample size
    print(f"Effective sample size: {effective_size(weights):.2f}")


if __name__ == '__main__':
    demo_basic_selection()
    demo_alias_method()
    demo_weighted_shuffle()
    demo_softmax_weights()
    demo_statistical_analysis()
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)