"""
Hierarchical Token Bucket Implementation

Implements nested token buckets for multi-level rate limiting.
Useful for scenarios like:
- Global rate limit + per-user rate limit
- Network bandwidth limit + per-connection limit

Each consume request checks all levels in the hierarchy.

Time complexity:
- consume: O(depth) where depth is bucket hierarchy depth
- refill: O(depth)

Space complexity: O(depth)
"""

import time
from typing import List, Optional, Tuple


class HierarchicalTokenBucket:
    """
    Hierarchical token bucket with multiple levels.
    
    Requests must pass through all levels to be approved.
    This enables fine-grained rate limiting like:
    - 1000 requests/second globally
    - 10 requests/second per user
    
    Example:
        >>> bucket = HierarchicalTokenBucket()
        >>> bucket.add_level(capacity=1000, refill_rate=100)  # Global
        >>> bucket.add_level(capacity=10, refill_rate=2)       # Per-user
        >>> bucket.consume(1)
        True
    """
    
    def __init__(self):
        """Initialize empty hierarchy."""
        self._levels: List[Tuple[int, float, float, float]] = []  # (capacity, rate, tokens, last_refill)
        self._names: List[str] = []
    
    def add_level(
        self, 
        capacity: int, 
        refill_rate: float,
        name: Optional[str] = None
    ) -> 'HierarchicalTokenBucket':
        """
        Add a level to the hierarchy.
        
        Args:
            capacity: Maximum tokens for this level
            refill_rate: Tokens per second for this level
            name: Optional name for this level
        
        Returns:
            self for chaining
        
        Example:
            >>> h = HierarchicalTokenBucket()
            >>> h.add_level(1000, 100, "global").add_level(10, 2, "user")
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        
        now = time.time()
        self._levels.append((capacity, refill_rate, float(capacity), now))
        self._names.append(name or f"level_{len(self._levels)}")
        
        return self
    
    def _refill_all(self) -> None:
        """Refill all levels."""
        now = time.time()
        
        updated_levels = []
        for capacity, rate, tokens, last_refill in self._levels:
            elapsed = now - last_refill
            if elapsed > 0:
                new_tokens = tokens + elapsed * rate
                tokens = min(capacity, new_tokens)
            updated_levels.append((capacity, rate, tokens, now))
        
        self._levels = updated_levels
    
    def consume(self, tokens: int = 1) -> Tuple[bool, Optional[str]]:
        """
        Try to consume tokens from all levels.
        
        Args:
            tokens: Number of tokens to consume
        
        Returns:
            Tuple of (success, failed_level_name)
            failed_level_name is None on success
        
        Example:
            >>> bucket = HierarchicalTokenBucket()
            >>> bucket.add_level(10, 1)
            >>> bucket.consume(5)
            (True, None)
            >>> bucket.consume(10)  # Only 5 left
            (False, 'level_1')
        """
        if tokens <= 0:
            raise ValueError("Token count must be positive")
        
        if not self._levels:
            raise RuntimeError("No levels added to hierarchy")
        
        self._refill_all()
        
        # Check all levels first
        for i, (capacity, rate, current_tokens, last_refill) in enumerate(self._levels):
            if current_tokens < tokens:
                return (False, self._names[i])
        
        # Consume from all levels
        updated_levels = []
        for i, (capacity, rate, current_tokens, last_refill) in enumerate(self._levels):
            updated_levels.append((capacity, rate, current_tokens - tokens, last_refill))
        
        self._levels = updated_levels
        return (True, None)
    
    def available(self, level: int = -1) -> float:
        """
        Get available tokens at a specific level.
        
        Args:
            level: Level index (-1 for minimum across all levels)
        
        Returns:
            Available token count
        """
        self._refill_all()
        
        if level >= 0:
            if level >= len(self._levels):
                raise IndexError(f"Level {level} does not exist")
            return self._levels[level][2]
        
        # Return minimum across all levels
        return min(level_data[2] for level_data in self._levels)
    
    def status(self) -> List[dict]:
        """
        Get status of all levels.
        
        Returns:
            List of dicts with level information
        """
        self._refill_all()
        
        return [
            {
                'name': self._names[i],
                'capacity': capacity,
                'refill_rate': rate,
                'tokens': tokens
            }
            for i, (capacity, rate, tokens, _) in enumerate(self._levels)
        ]
    
    def reset(self, level: Optional[int] = None) -> None:
        """
        Reset one or all levels to full capacity.
        
        Args:
            level: Level index to reset (None for all levels)
        """
        now = time.time()
        
        if level is not None:
            if level >= len(self._levels):
                raise IndexError(f"Level {level} does not exist")
            capacity, rate, _, _ = self._levels[level]
            self._levels[level] = (capacity, rate, float(capacity), now)
        else:
            self._levels = [
                (capacity, rate, float(capacity), now)
                for capacity, rate, _, _ in self._levels
            ]
    
    def __repr__(self) -> str:
        level_count = len(self._levels)
        return f"HierarchicalTokenBucket(levels={level_count})"