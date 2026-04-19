#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Weighted Random Utilities Module

Comprehensive weighted random selection utilities for Python with zero external dependencies.
Provides weighted random sampling, alias method for O(1) selection, reservoir sampling,
and various probability distribution utilities.

Author: AllToolkit
License: MIT
"""

import random
import math
from typing import (
    Union, List, Tuple, Dict, Any, Optional, 
    Sequence, TypeVar, Callable, Generic, Iterator
)
from collections.abc import Iterable
from bisect import bisect_right
from itertools import accumulate


# =============================================================================
# Type Aliases
# =============================================================================

T = TypeVar('T')
Weight = Union[int, float]
WeightedItem = Tuple[T, Weight]


# =============================================================================
# Exceptions
# =============================================================================

class WeightedRandomError(Exception):
    """Base exception for weighted random utilities."""
    pass


class EmptyWeightsError(WeightedRandomError):
    """Raised when no weights are provided."""
    pass


class InvalidWeightError(WeightedRandomError):
    """Raised when a weight is invalid (negative or non-numeric)."""
    pass


class TotalWeightZeroError(WeightedRandomError):
    """Raised when total weight is zero."""
    pass


# =============================================================================
# Basic Weighted Random Selection
# =============================================================================

def weighted_choice(
    items: Sequence[T], 
    weights: Sequence[Weight],
    *,
    random_instance: Optional[random.Random] = None
) -> T:
    """
    Select a single item based on weights using linear search.
    
    Time complexity: O(n) for selection, O(n) preprocessing for cumulative weights.
    Suitable for small to medium-sized lists.
    
    Args:
        items: Sequence of items to choose from
        weights: Sequence of weights corresponding to items
        random_instance: Optional random.Random instance for reproducibility
        
    Returns:
        Selected item
        
    Raises:
        EmptyWeightsError: If items or weights are empty
        InvalidWeightError: If any weight is negative
        TotalWeightZeroError: If total weight is zero
        
    Example:
        >>> items = ['apple', 'banana', 'cherry']
        >>> weights = [1, 2, 3]
        >>> result = weighted_choice(items, weights)
        >>> result in items
        True
    """
    if not items or not weights:
        raise EmptyWeightsError("Items and weights must not be empty")
    
    if len(items) != len(weights):
        raise ValueError("Items and weights must have the same length")
    
    # Validate weights
    total = 0.0
    for w in weights:
        if w < 0:
            raise InvalidWeightError(f"Weight cannot be negative: {w}")
        total += w
    
    if total == 0:
        raise TotalWeightZeroError("Total weight cannot be zero")
    
    # Use provided random instance or default
    rnd = random_instance or random
    
    # Select using cumulative weights
    r = rnd.random() * total
    cumsum = 0.0
    for item, weight in zip(items, weights):
        cumsum += weight
        if r < cumsum:
            return item
    
    # Fallback (shouldn't happen with valid weights)
    return items[-1]


def weighted_choice_with_index(
    items: Sequence[T], 
    weights: Sequence[Weight],
    *,
    random_instance: Optional[random.Random] = None
) -> Tuple[T, int]:
    """
    Select a single item based on weights, returning both item and its index.
    
    Args:
        items: Sequence of items to choose from
        weights: Sequence of weights corresponding to items
        random_instance: Optional random.Random instance for reproducibility
        
    Returns:
        Tuple of (selected item, index)
        
    Example:
        >>> items = ['a', 'b', 'c']
        >>> weights = [1, 2, 3]
        >>> item, idx = weighted_choice_with_index(items, weights)
        >>> item == items[idx]
        True
    """
    if not items or not weights:
        raise EmptyWeightsError("Items and weights must not be empty")
    
    if len(items) != len(weights):
        raise ValueError("Items and weights must have the same length")
    
    total = 0.0
    for w in weights:
        if w < 0:
            raise InvalidWeightError(f"Weight cannot be negative: {w}")
        total += w
    
    if total == 0:
        raise TotalWeightZeroError("Total weight cannot be zero")
    
    rnd = random_instance or random
    r = rnd.random() * total
    
    cumsum = 0.0
    for idx, (item, weight) in enumerate(zip(items, weights)):
        cumsum += weight
        if r < cumsum:
            return item, idx
    
    return items[-1], len(items) - 1


def weighted_sample(
    items: Sequence[T], 
    weights: Sequence[Weight],
    k: int,
    *,
    replace: bool = True,
    random_instance: Optional[random.Random] = None
) -> List[T]:
    """
    Sample k items based on weights.
    
    Args:
        items: Sequence of items to choose from
        weights: Sequence of weights corresponding to items
        k: Number of items to sample
        replace: Whether to sample with replacement (default True)
        random_instance: Optional random.Random instance for reproducibility
        
    Returns:
        List of sampled items
        
    Raises:
        ValueError: If k > len(items) when sampling without replacement
        
    Example:
        >>> items = ['a', 'b', 'c']
        >>> weights = [1, 2, 3]
        >>> sample = weighted_sample(items, weights, k=5)
        >>> len(sample)
        5
    """
    if not replace and k > len(items):
        raise ValueError(f"Cannot sample {k} items without replacement from {len(items)} items")
    
    rnd = random_instance or random
    
    if replace:
        return [weighted_choice(items, weights, random_instance=rnd) for _ in range(k)]
    else:
        # Sampling without replacement using chain method
        result = []
        remaining_items = list(items)
        remaining_weights = list(weights)
        
        for _ in range(k):
            if not remaining_items:
                break
            idx = _weighted_index(remaining_weights, rnd)
            result.append(remaining_items.pop(idx))
            remaining_weights.pop(idx)
        
        return result


def _weighted_index(weights: List[Weight], rnd: random.Random) -> int:
    """Helper function to get a weighted index."""
    total = sum(weights)
    if total == 0:
        raise TotalWeightZeroError("Total weight cannot be zero")
    
    r = rnd.random() * total
    cumsum = 0.0
    for idx, w in enumerate(weights):
        cumsum += w
        if r < cumsum:
            return idx
    return len(weights) - 1


# =============================================================================
# Alias Method for O(1) Weighted Selection
# =============================================================================

class AliasMethod(Generic[T]):
    """
    Alias method for O(1) weighted random selection.
    
    Preprocessing time: O(n)
    Selection time: O(1)
    Space complexity: O(n)
    
    Ideal for scenarios where many selections are made from the same distribution.
    
    Example:
        >>> items = ['a', 'b', 'c', 'd']
        >>> weights = [1, 2, 3, 4]
        >>> alias = AliasMethod(items, weights)
        >>> selected = alias.sample()
        >>> selected in items
        True
    """
    
    def __init__(
        self, 
        items: Sequence[T], 
        weights: Sequence[Weight],
        *,
        normalize: bool = True
    ):
        """
        Initialize the AliasMethod with items and weights.
        
        Args:
            items: Items to sample from
            weights: Corresponding weights
            normalize: Whether to normalize weights (default True)
        """
        if not items or not weights:
            raise EmptyWeightsError("Items and weights must not be empty")
        
        if len(items) != len(weights):
            raise ValueError("Items and weights must have the same length")
        
        self._items = list(items)
        self._n = len(self._items)
        
        # Validate and normalize weights
        weights = [float(w) for w in weights]
        for w in weights:
            if w < 0:
                raise InvalidWeightError(f"Weight cannot be negative: {w}")
        
        total = sum(weights)
        if total == 0:
            raise TotalWeightZeroError("Total weight cannot be zero")
        
        if normalize:
            weights = [w * self._n / total for w in weights]
        
        # Build alias tables
        self._prob = [0.0] * self._n
        self._alias = [0] * self._n
        self._build_tables(weights)
    
    def _build_tables(self, weights: List[float]) -> None:
        """Build the probability and alias tables."""
        # Small and large lists
        small: List[int] = []
        large: List[int] = []
        
        # Partition items
        for i, w in enumerate(weights):
            if w < 1.0:
                small.append(i)
            else:
                large.append(i)
        
        # Process items
        while small and large:
            small_idx = small.pop()
            large_idx = large.pop()
            
            self._prob[small_idx] = weights[small_idx]
            self._alias[small_idx] = large_idx
            
            # Update large item's weight
            weights[large_idx] = weights[large_idx] + weights[small_idx] - 1.0
            
            if weights[large_idx] < 1.0:
                small.append(large_idx)
            else:
                large.append(large_idx)
        
        # Handle remaining items (due to floating point errors)
        while large:
            self._prob[large.pop()] = 1.0
        
        while small:
            self._prob[small.pop()] = 1.0
    
    def sample(self, random_instance: Optional[random.Random] = None) -> T:
        """
        Sample a single item.
        
        Args:
            random_instance: Optional random.Random instance for reproducibility
            
        Returns:
            A randomly selected item
        """
        rnd = random_instance or random
        
        # Get random bucket and check if we use alias
        i = rnd.randint(0, self._n - 1)
        
        if rnd.random() < self._prob[i]:
            return self._items[i]
        else:
            return self._items[self._alias[i]]
    
    def sample_n(self, n: int, random_instance: Optional[random.Random] = None) -> List[T]:
        """
        Sample n items with replacement.
        
        Args:
            n: Number of items to sample
            random_instance: Optional random.Random instance for reproducibility
            
        Returns:
            List of sampled items
        """
        return [self.sample(random_instance) for _ in range(n)]
    
    @property
    def items(self) -> List[T]:
        """Return the items list."""
        return self._items.copy()
    
    @property
    def probabilities(self) -> List[float]:
        """Return the probability table."""
        return self._prob.copy()
    
    @property
    def aliases(self) -> List[int]:
        """Return the alias table."""
        return self._alias.copy()


# =============================================================================
# Weight Distribution Utilities
# =============================================================================

def normalize_weights(weights: Sequence[Weight]) -> List[float]:
    """
    Normalize weights to sum to 1.0.
    
    Args:
        weights: Sequence of weights
        
    Returns:
        List of normalized weights
        
    Raises:
        TotalWeightZeroError: If total weight is zero
        
    Example:
        >>> normalize_weights([1, 2, 3])
        [0.166666..., 0.333333..., 0.5]
    """
    weights = [float(w) for w in weights]
    total = sum(weights)
    
    if total == 0:
        raise TotalWeightZeroError("Total weight cannot be zero")
    
    return [w / total for w in weights]


def cumulative_weights(weights: Sequence[Weight]) -> List[float]:
    """
    Compute cumulative weights.
    
    Args:
        weights: Sequence of weights
        
    Returns:
        List of cumulative weights
        
    Example:
        >>> cumulative_weights([1, 2, 3])
        [1, 3, 6]
    """
    return list(accumulate(weights))


def probability_from_cumulative(
    cumulative: Sequence[float], 
    value: float
) -> int:
    """
    Find the index where value would be inserted in cumulative weights.
    
    Args:
        cumulative: Sequence of cumulative weights
        value: Value to find position for (should be in [0, total_weight))
        
    Returns:
        Index of the selected item
        
    Example:
        >>> cumulative_weights = [1, 3, 6]
        >>> probability_from_cumulative(cumulative_weights, 2)
        1
    """
    return bisect_right(cumulative, value)


def softmax_weights(values: Sequence[float], temperature: float = 1.0) -> List[float]:
    """
    Convert values to probability distribution using softmax.
    
    Higher temperature makes distribution more uniform.
    Lower temperature makes distribution more peaked.
    
    Args:
        values: Sequence of values (can be negative)
        temperature: Temperature parameter (must be positive)
        
    Returns:
        List of probabilities summing to 1.0
        
    Raises:
        ValueError: If temperature <= 0
        
    Example:
        >>> softmax_weights([1, 2, 3])
        [0.090..., 0.244..., 0.665...]
    """
    if temperature <= 0:
        raise ValueError("Temperature must be positive")
    
    # Scale by temperature
    scaled = [v / temperature for v in values]
    
    # Subtract max for numerical stability
    max_val = max(scaled)
    exp_vals = [math.exp(v - max_val) for v in scaled]
    total = sum(exp_vals)
    
    return [v / total for v in exp_vals]


def exponential_weights(
    base_weights: Sequence[Weight],
    decay: float = 0.5
) -> List[float]:
    """
    Apply exponential decay to weights.
    
    Useful for implementing recency bias or temperature-based weighting.
    
    Args:
        base_weights: Original weights
        decay: Decay factor (0 < decay for valid results)
        
    Returns:
        List of exponentially decayed weights
        
    Example:
        >>> exponential_weights([1, 2, 3], decay=0.5)
        [1.0, 1.0, 0.75]
    """
    if decay <= 0:
        raise ValueError("Decay must be positive")
    
    return [float(w) ** decay for w in base_weights]


# =============================================================================
# Weighted Reservoir Sampling
# =============================================================================

class WeightedReservoirSampler(Generic[T]):
    """
    Weighted reservoir sampling for streaming data.
    
    Implements A-Res (Algorithm A with Reservoir) for weighted random sampling
    from a stream of items without knowing the total number in advance.
    
    Example:
        >>> sampler = WeightedReservoirSampler(k=3)
        >>> for item, weight in [('a', 1), ('b', 2), ('c', 3), ('d', 4)]:
        ...     sampler.add(item, weight)
        >>> sample = sampler.sample()
        >>> len(sample)
        3
    """
    
    def __init__(self, k: int, random_instance: Optional[random.Random] = None):
        """
        Initialize the weighted reservoir sampler.
        
        Args:
            k: Reservoir size
            random_instance: Optional random.Random instance for reproducibility
        """
        if k <= 0:
            raise ValueError("Reservoir size k must be positive")
        
        self._k = k
        self._rnd = random_instance or random
        self._reservoir: List[Tuple[T, float]] = []  # (item, priority)
    
    def add(self, item: T, weight: Weight) -> None:
        """
        Add an item to the reservoir.
        
        Args:
            item: Item to add
            weight: Weight of the item
        """
        if weight <= 0:
            return  # Skip zero or negative weights
        
        # Generate priority
        # Using the formula: r_i = u_i^(1/w_i) where u_i is uniform(0,1)
        u = self._rnd.random()
        if u == 0:
            return  # Avoid log(0)
        
        priority = math.log(u) / weight
        
        if len(self._reservoir) < self._k:
            self._reservoir.append((item, priority))
            self._heapify_if_needed()
        elif priority > self._reservoir[0][1]:
            # Replace the minimum priority item
            self._reservoir[0] = (item, priority)
            self._sift_down(0)
    
    def _heapify_if_needed(self) -> None:
        """Convert reservoir to min-heap if full."""
        if len(self._reservoir) == self._k:
            # Build min-heap based on priority
            n = len(self._reservoir)
            for i in range(n // 2 - 1, -1, -1):
                self._sift_down(i)
    
    def _sift_down(self, idx: int) -> None:
        """Sift down element at idx in min-heap."""
        n = len(self._reservoir)
        while True:
            smallest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2
            
            if left < n and self._reservoir[left][1] < self._reservoir[smallest][1]:
                smallest = left
            if right < n and self._reservoir[right][1] < self._reservoir[smallest][1]:
                smallest = right
            
            if smallest != idx:
                self._reservoir[idx], self._reservoir[smallest] = \
                    self._reservoir[smallest], self._reservoir[idx]
                idx = smallest
            else:
                break
    
    def sample(self) -> List[T]:
        """
        Get the current reservoir sample.
        
        Returns:
            List of sampled items
        """
        return [item for item, _ in self._reservoir]
    
    def clear(self) -> None:
        """Clear the reservoir."""
        self._reservoir.clear()
    
    @property
    def size(self) -> int:
        """Current number of items in reservoir."""
        return len(self._reservoir)
    
    @property
    def capacity(self) -> int:
        """Maximum capacity of reservoir."""
        return self._k


# =============================================================================
# Weighted Shuffle
# =============================================================================

def weighted_shuffle(
    items: Sequence[T], 
    weights: Sequence[Weight],
    *,
    random_instance: Optional[random.Random] = None
) -> List[T]:
    """
    Shuffle items with weighted probabilities.
    
    Items with higher weights are more likely to appear earlier in the result.
    
    Args:
        items: Items to shuffle
        weights: Corresponding weights
        random_instance: Optional random.Random instance for reproducibility
        
    Returns:
        Shuffled list of items
        
    Example:
        >>> items = ['a', 'b', 'c', 'd']
        >>> weights = [4, 3, 2, 1]
        >>> result = weighted_shuffle(items, weights)
        >>> len(result)
        4
    """
    if not items:
        return []
    
    if len(items) != len(weights):
        raise ValueError("Items and weights must have the same length")
    
    rnd = random_instance or random
    
    # Create list of (item, weight) tuples
    remaining = list(zip(items, weights))
    result = []
    
    while remaining:
        # Select one item weighted
        total = sum(w for _, w in remaining)
        if total == 0:
            # Random selection if all weights are zero
            idx = rnd.randint(0, len(remaining) - 1)
        else:
            r = rnd.random() * total
            cumsum = 0.0
            idx = 0
            for i, (_, w) in enumerate(remaining):
                cumsum += w
                if r < cumsum:
                    idx = i
                    break
        
        result.append(remaining.pop(idx)[0])
    
    return result


# =============================================================================
# Distribution Functions
# =============================================================================

def inverse_transform_sample(
    cdf_values: Sequence[float],
    values: Optional[Sequence[T]] = None,
    *,
    random_instance: Optional[random.Random] = None
) -> Union[int, T]:
    """
    Sample using inverse transform method from CDF.
    
    Args:
        cdf_values: Cumulative distribution function values
        values: Optional values corresponding to CDF indices
        random_instance: Optional random.Random instance for reproducibility
        
    Returns:
        Index into CDF (if values is None) or corresponding value
        
    Example:
        >>> cdf = [0.1, 0.3, 0.6, 1.0]
        >>> idx = inverse_transform_sample(cdf)
        >>> 0 <= idx < 4
        True
    """
    if not cdf_values:
        raise EmptyWeightsError("CDF values must not be empty")
    
    rnd = random_instance or random
    u = rnd.random()
    
    # Find index where CDF first exceeds u
    for idx, cdf_val in enumerate(cdf_values):
        if cdf_val >= u:
            return values[idx] if values else idx
    
    # Fallback to last index
    return values[-1] if values else len(cdf_values) - 1


def rejection_sample(
    proposal_func: Callable[[], T],
    acceptance_prob: Callable[[T], float],
    n: int,
    *,
    max_iterations: int = 10000,
    random_instance: Optional[random.Random] = None
) -> List[T]:
    """
    Rejection sampling for arbitrary distributions.
    
    Args:
        proposal_func: Function that generates proposal samples
        acceptance_prob: Function that returns acceptance probability for a sample
        n: Number of accepted samples to generate
        max_iterations: Maximum number of iterations before giving up
        random_instance: Optional random.Random instance for reproducibility
        
    Returns:
        List of accepted samples
        
    Example:
        >>> import math
        >>> # Sample from a distribution proportional to x^2 on [0, 1]
        >>> proposal = lambda: random.random()
        >>> acceptance = lambda x: x * x
        >>> samples = rejection_sample(proposal, acceptance, 100)
        >>> len(samples)
        100
    """
    if n <= 0:
        return []
    
    rnd = random_instance or random
    samples = []
    iterations = 0
    
    while len(samples) < n and iterations < max_iterations:
        proposal = proposal_func()
        if rnd.random() < acceptance_prob(proposal):
            samples.append(proposal)
        iterations += 1
    
    return samples


# =============================================================================
# Utility Functions
# =============================================================================

def weight_to_probability(items: Sequence[Tuple[T, Weight]]) -> Dict[T, float]:
    """
    Convert a list of (item, weight) pairs to a probability dictionary.
    
    Args:
        items: Sequence of (item, weight) tuples
        
    Returns:
        Dictionary mapping items to probabilities
        
    Example:
        >>> weight_to_probability([('a', 1), ('b', 2), ('c', 3)])
        {'a': 0.1666..., 'b': 0.333..., 'c': 0.5}
    """
    total = sum(w for _, w in items)
    if total == 0:
        raise TotalWeightZeroError("Total weight cannot be zero")
    
    return {item: w / total for item, w in items}


def probability_to_weight(
    probabilities: Sequence[float], 
    scale: float = 100.0
) -> List[float]:
    """
    Convert probabilities to integer-like weights.
    
    Args:
        probabilities: Probabilities summing to 1.0
        scale: Scale factor for weights
        
    Returns:
        List of scaled weights
        
    Example:
        >>> probability_to_weight([0.2, 0.3, 0.5])
        [20.0, 30.0, 50.0]
    """
    return [p * scale for p in probabilities]


def kl_divergence(p: Sequence[float], q: Sequence[float]) -> float:
    """
    Compute KL divergence D_KL(p || q).
    
    Measures how one probability distribution diverges from another.
    
    Args:
        p: First probability distribution
        q: Second probability distribution
        
    Returns:
        KL divergence value
        
    Example:
        >>> kl_divergence([0.5, 0.5], [0.5, 0.5])
        0.0
    """
    if len(p) != len(q):
        raise ValueError("Distributions must have the same length")
    
    divergence = 0.0
    for pi, qi in zip(p, q):
        if pi > 0:
            if qi == 0:
                return float('inf')
            divergence += pi * math.log(pi / qi)
    
    return divergence


def entropy(probabilities: Sequence[float]) -> float:
    """
    Compute Shannon entropy of a probability distribution.
    
    Higher entropy means more uniformity (more randomness).
    
    Args:
        probabilities: Probability distribution
        
    Returns:
        Entropy in bits (using log base 2)
        
    Example:
        >>> entropy([0.5, 0.5])  # Maximum entropy for 2 outcomes
        1.0
    """
    total = sum(probabilities)
    if total == 0:
        return 0.0
    
    h = 0.0
    for p in probabilities:
        if p > 0:
            h -= (p / total) * math.log2(p / total)
    
    return h


def effective_size(weights: Sequence[Weight]) -> float:
    """
    Compute effective sample size from weights.
    
    ESS = (sum(w))^2 / sum(w^2)
    
    Useful for importance sampling and weighted statistics.
    
    Args:
        weights: Sequence of weights
        
    Returns:
        Effective sample size
        
    Example:
        >>> effective_size([1, 1, 1, 1])  # All equal weights
        4.0
    """
    weights = [float(w) for w in weights]
    sum_w = sum(weights)
    sum_w2 = sum(w * w for w in weights)
    
    if sum_w2 == 0:
        return 0.0
    
    return (sum_w ** 2) / sum_w2


# =============================================================================
# Batch Operations
# =============================================================================

def batch_weighted_choice(
    items: Sequence[T],
    weights: Sequence[Weight],
    n: int,
    *,
    random_instance: Optional[random.Random] = None
) -> List[T]:
    """
    Efficiently sample n items using precomputed cumulative weights.
    
    More efficient than calling weighted_choice n times for large n.
    
    Args:
        items: Items to choose from
        weights: Corresponding weights
        n: Number of samples
        random_instance: Optional random.Random instance for reproducibility
        
    Returns:
        List of n sampled items
        
    Example:
        >>> items = ['a', 'b', 'c']
        >>> weights = [1, 2, 3]
        >>> samples = batch_weighted_choice(items, weights, 1000)
        >>> len(samples)
        1000
    """
    if n <= 0:
        return []
    
    # Precompute cumulative weights
    cum_weights = cumulative_weights(weights)
    total = cum_weights[-1]
    
    if total == 0:
        raise TotalWeightZeroError("Total weight cannot be zero")
    
    rnd = random_instance or random
    result = []
    
    for _ in range(n):
        r = rnd.random() * total
        idx = probability_from_cumulative(cum_weights, r)
        result.append(items[idx])
    
    return result


# =============================================================================
# Convenience Functions
# =============================================================================

def weighted_coin_flip(
    probability: float,
    *,
    random_instance: Optional[random.Random] = None
) -> bool:
    """
    Flip a weighted coin.
    
    Args:
        probability: Probability of True (0.0 to 1.0)
        random_instance: Optional random.Random instance for reproducibility
        
    Returns:
        True with given probability, False otherwise
        
    Example:
        >>> # Fair coin
        >>> weighted_coin_flip(0.5) in [True, False]
        True
    """
    if not 0 <= probability <= 1:
        raise ValueError("Probability must be between 0 and 1")
    
    rnd = random_instance or random
    return rnd.random() < probability


def weighted_random_range(
    start: int,
    end: int,
    weights: Sequence[Weight],
    *,
    random_instance: Optional[random.Random] = None
) -> int:
    """
    Select a random integer from range with weights.
    
    Args:
        start: Start of range (inclusive)
        end: End of range (exclusive)
        weights: Weights for each integer in range
        random_instance: Optional random.Random instance for reproducibility
        
    Returns:
        Selected integer
        
    Example:
        >>> # Select from 0, 1, 2, 3 with weights
        >>> result = weighted_random_range(0, 4, [1, 2, 3, 4])
        >>> 0 <= result < 4
        True
    """
    if end <= start:
        raise ValueError("End must be greater than start")
    
    range_size = end - start
    if len(weights) != range_size:
        raise ValueError(f"Weights length ({len(weights)}) must match range size ({range_size})")
    
    idx = _weighted_index(list(weights), random_instance or random)
    return start + idx


if __name__ == "__main__":
    # Quick demonstration
    print("Weighted Random Utilities Demo")
    print("=" * 50)
    
    # Basic weighted choice
    items = ['apple', 'banana', 'cherry', 'date']
    weights = [1, 2, 3, 4]
    
    print(f"\nItems: {items}")
    print(f"Weights: {weights}")
    
    # Sample 20 times
    samples = [weighted_choice(items, weights) for _ in range(20)]
    print(f"\n20 samples: {samples}")
    
    # Alias method demo
    print("\n--- Alias Method Demo ---")
    alias = AliasMethod(items, weights)
    print(f"Probabilities: {alias.probabilities}")
    print(f"Aliases: {alias.aliases}")
    print(f"5 samples: {alias.sample_n(5)}")
    
    # Weighted shuffle
    print("\n--- Weighted Shuffle Demo ---")
    shuffled = weighted_shuffle(items, weights)
    print(f"Shuffled: {shuffled}")
    
    # Probability utilities
    print("\n--- Probability Utilities Demo ---")
    probs = normalize_weights(weights)
    print(f"Normalized: {[round(p, 3) for p in probs]}")
    print(f"Softmax: {[round(p, 3) for p in softmax_weights([1, 2, 3, 4])]}")
    print(f"Entropy: {entropy(probs):.4f} bits")
    print(f"Effective size: {effective_size(weights):.2f}")
    
    print("\nDemo complete!")