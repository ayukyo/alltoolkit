"""
Alias Method Utils - Walker's Alias Method for O(1) Weighted Random Sampling

This module implements the alias method, which allows efficient sampling from
discrete probability distributions. After O(n) preprocessing, each sample
can be drawn in O(1) time.

The alias method is particularly useful for:
- Weighted random selection in games (loot tables, spawn rates)
- Monte Carlo simulations
- A/B testing frameworks
- Load balancing with weighted servers
- Natural language processing (sampling from word distributions)

Time Complexity:
- Preprocessing: O(n)
- Sampling: O(1)
- Space: O(n)

Author: AllToolkit
Date: 2026-05-03
"""

import random
from typing import List, Tuple, Optional, Dict, Any, Sequence


class AliasMethod:
    """
    Walker's Alias Method for efficient weighted random sampling.
    
    This implementation uses the Vose's algorithm variant which is
    simpler and equally efficient.
    
    Example:
        >>> weights = [1, 2, 3, 4]
        >>> alias = AliasMethod(weights)
        >>> sample = alias.sample()  # Returns index 0-3
        >>> # Higher weights have higher probability
    """
    
    def __init__(self, weights: Sequence[float], normalize: bool = True):
        """
        Initialize the alias method with given weights.
        
        Args:
            weights: A sequence of non-negative weights. 
                    Each weight represents the relative probability
                    of selecting its corresponding index.
            normalize: If True (default), weights are normalized to sum to 1.
                      If False, weights are assumed to already be normalized
                      or to sum to len(weights).
        
        Raises:
            ValueError: If weights is empty or all weights are zero.
        """
        if not weights:
            raise ValueError("Weights cannot be empty")
        
        self._n = len(weights)
        self._weights = list(weights)
        
        # Check for negative weights
        if any(w < 0 for w in self._weights):
            raise ValueError("Weights must be non-negative")
        
        total = sum(self._weights)
        if total == 0:
            raise ValueError("At least one weight must be positive")
        
        # Normalize weights if requested
        if normalize:
            self._probabilities = [w / total for w in self._weights]
        else:
            self._probabilities = self._weights.copy()
        
        # Build the alias tables
        self._build_alias_tables()
    
    def _build_alias_tables(self) -> None:
        """
        Build the probability and alias tables using Vose's algorithm.
        
        The idea is to create two arrays:
        - prob[i]: the probability of choosing index i directly
        - alias[i]: the alternative index if not choosing i directly
        
        Each bin (index) has probability summing to 1/n (scaled).
        """
        n = self._n
        
        # Scale probabilities so they sum to n
        scaled_probs = [p * n for p in self._probabilities]
        
        # Initialize tables
        self._prob_table = [0.0] * n
        self._alias_table = [0] * n
        
        # Separate indices into small (below average) and large (above average)
        small = []
        large = []
        
        for i, prob in enumerate(scaled_probs):
            if prob < 1.0:
                small.append(i)
            else:
                large.append(i)
        
        # Process small and large lists
        while small and large:
            small_idx = small.pop()
            large_idx = large.pop()
            
            # Store the probability and alias
            self._prob_table[small_idx] = scaled_probs[small_idx]
            self._alias_table[small_idx] = large_idx
            
            # Update the large probability
            scaled_probs[large_idx] = scaled_probs[large_idx] + scaled_probs[small_idx] - 1.0
            
            if scaled_probs[large_idx] < 1.0:
                small.append(large_idx)
            else:
                large.append(large_idx)
        
        # Remaining items have probability 1.0
        while large:
            idx = large.pop()
            self._prob_table[idx] = 1.0
        
        while small:
            idx = small.pop()
            self._prob_table[idx] = 1.0
    
    def sample(self, rng: Optional[random.Random] = None) -> int:
        """
        Sample an index according to the weight distribution.
        
        Args:
            rng: Optional random number generator. If None, uses the
                 default random module.
        
        Returns:
            An index in the range [0, n-1] sampled according to weights.
        
        Time Complexity: O(1)
        """
        if rng is None:
            rng = random
        
        # Choose a random bin
        i = rng.randrange(self._n)
        
        # Flip a biased coin
        if rng.random() < self._prob_table[i]:
            return i
        else:
            return self._alias_table[i]
    
    def sample_n(self, n: int, rng: Optional[random.Random] = None,
                 replace: bool = True) -> List[int]:
        """
        Sample n indices from the distribution.
        
        Args:
            n: Number of samples to draw.
            rng: Optional random number generator.
            replace: If True (default), sample with replacement.
                    If False, sample without replacement (uses reservoir sampling).
        
        Returns:
            A list of n sampled indices.
        
        Time Complexity:
            - With replacement: O(n)
            - Without replacement: O(n * k) where k is original size
        """
        if n < 0:
            raise ValueError("n must be non-negative")
        
        if replace:
            return [self.sample(rng) for _ in range(n)]
        else:
            return self._sample_without_replacement(n, rng)
    
    def _sample_without_replacement(self, n: int, 
                                    rng: Optional[random.Random] = None) -> List[int]:
        """
        Sample without replacement using rejection sampling.
        
        For small n relative to the population size, this is efficient.
        For large n, consider using a different approach.
        """
        if n > self._n:
            n = self._n
        
        if rng is None:
            rng = random
        
        selected = set()
        result = []
        
        while len(result) < n:
            idx = self.sample(rng)
            if idx not in selected:
                selected.add(idx)
                result.append(idx)
        
        return result
    
    @property
    def probabilities(self) -> List[float]:
        """Return the normalized probabilities."""
        return self._probabilities.copy()
    
    @property
    def weights(self) -> List[float]:
        """Return the original weights (may not be normalized)."""
        return self._weights.copy()
    
    @property
    def size(self) -> int:
        """Return the number of items in the distribution."""
        return self._n
    
    def get_probability(self, index: int) -> float:
        """
        Get the probability of a specific index.
        
        Args:
            index: The index to query.
        
        Returns:
            The probability of selecting this index.
        
        Raises:
            IndexError: If index is out of range.
        """
        if not 0 <= index < self._n:
            raise IndexError(f"Index {index} out of range [0, {self._n})")
        return self._probabilities[index]
    
    def __len__(self) -> int:
        """Return the number of items in the distribution."""
        return self._n
    
    def __repr__(self) -> str:
        return f"AliasMethod(size={self._n})"


class WeightedRandomPicker:
    """
    A convenience class for picking items (not just indices) with weights.
    
    This wraps AliasMethod to allow picking actual items instead of indices.
    
    Example:
        >>> items = ['apple', 'banana', 'cherry']
        >>> weights = [1, 2, 3]
        >>> picker = WeightedRandomPicker(items, weights)
        >>> item = picker.pick()  # Returns one of the items
    """
    
    def __init__(self, items: Sequence[Any], weights: Sequence[float],
                 normalize: bool = True):
        """
        Initialize the picker with items and their weights.
        
        Args:
            items: A sequence of items to pick from.
            weights: A sequence of weights corresponding to each item.
            normalize: Whether to normalize weights.
        
        Raises:
            ValueError: If items and weights have different lengths.
        """
        if len(items) != len(weights):
            raise ValueError(
                f"Items and weights must have the same length. "
                f"Got {len(items)} items and {len(weights)} weights."
            )
        
        self._items = list(items)
        self._alias = AliasMethod(weights, normalize=normalize)
    
    def pick(self, rng: Optional[random.Random] = None) -> Any:
        """
        Pick a random item according to weights.
        
        Args:
            rng: Optional random number generator.
        
        Returns:
            A randomly selected item.
        """
        index = self._alias.sample(rng)
        return self._items[index]
    
    def pick_n(self, n: int, rng: Optional[random.Random] = None,
               replace: bool = True) -> List[Any]:
        """
        Pick n items from the distribution.
        
        Args:
            n: Number of items to pick.
            rng: Optional random number generator.
            replace: Whether to sample with replacement.
        
        Returns:
            A list of n randomly selected items.
        """
        indices = self._alias.sample_n(n, rng, replace)
        return [self._items[i] for i in indices]
    
    @property
    def items(self) -> List[Any]:
        """Return the list of items."""
        return self._items.copy()
    
    @property
    def probabilities(self) -> List[float]:
        """Return the normalized probabilities for each item."""
        return self._alias.probabilities
    
    def get_item_probability(self, item: Any) -> float:
        """
        Get the probability of picking a specific item.
        
        Args:
            item: The item to query.
        
        Returns:
            The probability of selecting this item.
        
        Raises:
            ValueError: If the item is not in the picker.
        """
        try:
            index = self._items.index(item)
            return self._alias.get_probability(index)
        except ValueError:
            raise ValueError(f"Item {item!r} not found in picker")
    
    def __len__(self) -> int:
        """Return the number of items."""
        return len(self._items)
    
    def __repr__(self) -> str:
        return f"WeightedRandomPicker(size={len(self._items)})"


def create_alias_from_dict(weight_dict: Dict[Any, float],
                          normalize: bool = True) -> WeightedRandomPicker:
    """
    Create a WeightedRandomPicker from a dictionary.
    
    Args:
        weight_dict: A dictionary mapping items to their weights.
        normalize: Whether to normalize weights.
    
    Returns:
        A WeightedRandomPicker instance.
    
    Example:
        >>> weight_dict = {'apple': 1, 'banana': 2, 'cherry': 3}
        >>> picker = create_alias_from_dict(weight_dict)
        >>> item = picker.pick()
    """
    items = list(weight_dict.keys())
    weights = list(weight_dict.values())
    return WeightedRandomPicker(items, weights, normalize)


def sample_with_weights(items: Sequence[Any], 
                        weights: Sequence[float],
                        n: int = 1,
                        replace: bool = True,
                        rng: Optional[random.Random] = None) -> List[Any]:
    """
    Convenience function to sample items with weights.
    
    This creates a temporary AliasMethod instance and samples from it.
    For repeated sampling, create an AliasMethod or WeightedRandomPicker
    instance instead.
    
    Args:
        items: Items to sample from.
        weights: Weights for each item.
        n: Number of samples to draw.
        replace: Whether to sample with replacement.
        rng: Optional random number generator.
    
    Returns:
        A list of sampled items.
    
    Example:
        >>> items = ['a', 'b', 'c']
        >>> weights = [1, 2, 3]
        >>> samples = sample_with_weights(items, weights, n=5)
    """
    picker = WeightedRandomPicker(items, weights, normalize=True)
    return picker.pick_n(n, rng, replace)


def weighted_shuffle(items: Sequence[Any],
                     weights: Sequence[float],
                     rng: Optional[random.Random] = None) -> List[Any]:
    """
    Shuffle items according to weights, with higher-weighted items
    more likely to appear early.
    
    This repeatedly samples without replacement, so items with higher
    weights tend to be selected first.
    
    Args:
        items: Items to shuffle.
        weights: Weights for each item.
        rng: Optional random number generator.
    
    Returns:
        A new list with items shuffled according to weights.
    
    Example:
        >>> items = ['a', 'b', 'c']
        >>> weights = [1, 2, 3]
        >>> shuffled = weighted_shuffle(items, weights)
        >>> # 'c' is more likely to be first
    """
    picker = WeightedRandomPicker(items, weights)
    return picker.pick_n(len(items), rng, replace=False)


class AliasMethodBuilder:
    """
    Builder pattern for creating AliasMethod instances.
    
    Useful for incremental construction of weight distributions.
    
    Example:
        >>> builder = AliasMethodBuilder()
        >>> builder.add('apple', 1.0)
        >>> builder.add('banana', 2.0)
        >>> builder.add('cherry', 3.0)
        >>> picker = builder.build_picker()
    """
    
    def __init__(self):
        """Initialize an empty builder."""
        self._items: List[Any] = []
        self._weights: List[float] = []
    
    def add(self, item: Any, weight: float) -> 'AliasMethodBuilder':
        """
        Add an item with its weight.
        
        Args:
            item: The item to add.
            weight: The weight for this item.
        
        Returns:
            Self for chaining.
        
        Raises:
            ValueError: If weight is negative.
        """
        if weight < 0:
            raise ValueError(f"Weight must be non-negative, got {weight}")
        
        self._items.append(item)
        self._weights.append(weight)
        return self
    
    def add_many(self, items: Sequence[Any], 
                 weights: Sequence[float]) -> 'AliasMethodBuilder':
        """
        Add multiple items with their weights.
        
        Args:
            items: Items to add.
            weights: Corresponding weights.
        
        Returns:
            Self for chaining.
        
        Raises:
            ValueError: If lengths don't match or any weight is negative.
        """
        if len(items) != len(weights):
            raise ValueError("Items and weights must have the same length")
        
        for item, weight in zip(items, weights):
            self.add(item, weight)
        
        return self
    
    def clear(self) -> 'AliasMethodBuilder':
        """Clear all items and weights."""
        self._items.clear()
        self._weights.clear()
        return self
    
    def build(self, normalize: bool = True) -> AliasMethod:
        """
        Build an AliasMethod instance from the added items.
        
        Args:
            normalize: Whether to normalize weights.
        
        Returns:
            An AliasMethod instance.
        
        Raises:
            ValueError: If no items have been added.
        """
        if not self._items:
            raise ValueError("Cannot build AliasMethod with no items")
        
        return AliasMethod(self._weights, normalize)
    
    def build_picker(self, normalize: bool = True) -> WeightedRandomPicker:
        """
        Build a WeightedRandomPicker instance.
        
        Args:
            normalize: Whether to normalize weights.
        
        Returns:
            A WeightedRandomPicker instance.
        
        Raises:
            ValueError: If no items have been added.
        """
        if not self._items:
            raise ValueError("Cannot build picker with no items")
        
        return WeightedRandomPicker(self._items, self._weights, normalize)
    
    @property
    def size(self) -> int:
        """Return the number of items added."""
        return len(self._items)
    
    def __len__(self) -> int:
        """Return the number of items added."""
        return self.size


# Convenience exports
__all__ = [
    'AliasMethod',
    'WeightedRandomPicker', 
    'AliasMethodBuilder',
    'create_alias_from_dict',
    'sample_with_weights',
    'weighted_shuffle',
]