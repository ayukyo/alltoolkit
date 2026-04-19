#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Rope Data Structure Utilities Module
==================================================
A comprehensive Rope data structure implementation for efficient string manipulation.
Zero external dependencies - pure Python implementation.

Features:
    - Rope data structure for efficient string operations
    - O(log n) insert, delete, split, and concatenate operations
    - Lazy evaluation with automatic rebalancing
    - Support for large text files (millions of characters)
    - Index-based access and iteration
    - String-like interface for familiar usage
    - Memory-efficient with reference sharing

The Rope data structure is ideal for:
    - Text editors and IDEs
    - Large file manipulation
    - String processing pipelines
    - Undo/redo implementations

Author: AllToolkit Contributors
License: MIT
"""

from typing import Optional, Iterator, Union, List, Tuple
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import math


# ============================================================================
# Constants
# ============================================================================

# Maximum leaf node size (characters per leaf)
DEFAULT_LEAF_MAX = 512

# Rebalancing threshold (height imbalance ratio)
REBALANCE_THRESHOLD = 3

# Minimum characters for a node to be considered for splitting
MIN_LEAF_SIZE = 32


# ============================================================================
# Abstract Base Class
# ============================================================================

class RopeNode(ABC):
    """Abstract base class for rope nodes."""
    
    @abstractmethod
    def length(self) -> int:
        """Return total length of rope."""
        pass
    
    @abstractmethod
    def char_at(self, index: int) -> str:
        """Get character at index."""
        pass
    
    @abstractmethod
    def substring(self, start: int, end: int) -> 'RopeNode':
        """Extract substring [start, end)."""
        pass
    
    @abstractmethod
    def insert(self, index: int, text: str) -> 'RopeNode':
        """Insert text at index."""
        pass
    
    @abstractmethod
    def delete(self, start: int, end: int) -> 'RopeNode':
        """Delete characters in range [start, end)."""
        pass
    
    @abstractmethod
    def split(self, index: int) -> Tuple['RopeNode', 'RopeNode']:
        """Split rope at index, returning (left, right)."""
        pass
    
    @abstractmethod
    def to_string(self) -> str:
        """Convert rope to string."""
        pass
    
    @abstractmethod
    def depth(self) -> int:
        """Return depth of tree."""
        pass
    
    @abstractmethod
    def rebalance(self) -> 'RopeNode':
        """Rebalance the rope."""
        pass
    
    def __len__(self) -> int:
        return self.length()
    
    def __getitem__(self, index: int) -> str:
        if isinstance(index, slice):
            start, stop, step = index.start, index.stop, index.step
            if start is None:
                start = 0
            if stop is None:
                stop = self.length()
            if step is not None and step != 1:
                # For steps, convert to string first
                return self.to_string()[start:stop:step]
            result = self.substring(start, stop)
            return result.to_string()
        return self.char_at(index)


# ============================================================================
# Leaf Node
# ============================================================================

@dataclass
class LeafNode(RopeNode):
    """Leaf node containing actual string data."""
    
    text: str
    leaf_max: int = DEFAULT_LEAF_MAX
    
    def length(self) -> int:
        return len(self.text)
    
    def char_at(self, index: int) -> str:
        if index < 0 or index >= len(self.text):
            raise IndexError(f"Index {index} out of range")
        return self.text[index]
    
    def substring(self, start: int, end: int) -> RopeNode:
        if start < 0:
            start = 0
        if end > len(self.text):
            end = len(self.text)
        if start >= end:
            return LeafNode("", self.leaf_max)
        return LeafNode(self.text[start:end], self.leaf_max)
    
    def insert(self, index: int, text: str) -> RopeNode:
        if not text:
            return self
        if index < 0:
            index = 0
        if index > len(self.text):
            index = len(self.text)
        new_text = self.text[:index] + text + self.text[index:]
        
        # Split if too large
        if len(new_text) > self.leaf_max:
            mid = len(new_text) // 2
            left = LeafNode(new_text[:mid], self.leaf_max)
            right = LeafNode(new_text[mid:], self.leaf_max)
            return InternalNode(left, right, self.leaf_max)
        return LeafNode(new_text, self.leaf_max)
    
    def delete(self, start: int, end: int) -> RopeNode:
        if start >= end or start >= len(self.text):
            return self
        if start < 0:
            start = 0
        if end > len(self.text):
            end = len(self.text)
        new_text = self.text[:start] + self.text[end:]
        if not new_text:
            return LeafNode("", self.leaf_max)
        return LeafNode(new_text, self.leaf_max)
    
    def split(self, index: int) -> Tuple[RopeNode, RopeNode]:
        if index <= 0:
            return LeafNode("", self.leaf_max), self
        if index >= len(self.text):
            return self, LeafNode("", self.leaf_max)
        left = LeafNode(self.text[:index], self.leaf_max)
        right = LeafNode(self.text[index:], self.leaf_max)
        return left, right
    
    def to_string(self) -> str:
        return self.text
    
    def depth(self) -> int:
        return 1
    
    def rebalance(self) -> RopeNode:
        return self
    
    def __repr__(self) -> str:
        return f"LeafNode({self.text[:20]}...)" if len(self.text) > 20 else f"LeafNode({self.text})"


# ============================================================================
# Internal Node
# ============================================================================

@dataclass
class InternalNode(RopeNode):
    """Internal node with left and right children."""
    
    left: RopeNode
    right: RopeNode
    leaf_max: int = DEFAULT_LEAF_MAX
    _length: int = field(init=False)
    _depth: int = field(init=False, default=1)
    
    def __post_init__(self):
        self._length = self.left.length() + self.right.length()
        self._depth = max(self.left.depth(), self.right.depth()) + 1
    
    def length(self) -> int:
        return self._length
    
    def char_at(self, index: int) -> str:
        left_len = self.left.length()
        if index < left_len:
            return self.left.char_at(index)
        return self.right.char_at(index - left_len)
    
    def substring(self, start: int, end: int) -> RopeNode:
        if start <= 0 and end >= self._length:
            return self
        
        left_len = self.left.length()
        
        if end <= left_len:
            return self.left.substring(start, end)
        if start >= left_len:
            return self.right.substring(start - left_len, end - left_len)
        
        # Spans both children
        left_part = self.left.substring(start, left_len)
        right_part = self.right.substring(0, end - left_len)
        
        return InternalNode(left_part, right_part, self.leaf_max)
    
    def insert(self, index: int, text: str) -> RopeNode:
        if not text:
            return self
        
        left_len = self.left.length()
        
        if index <= left_len:
            new_left = self.left.insert(index, text)
            result = InternalNode(new_left, self.right, self.leaf_max)
        else:
            new_right = self.right.insert(index - left_len, text)
            result = InternalNode(self.left, new_right, self.leaf_max)
        
        # Check if rebalancing needed
        if result.depth() > REBALANCE_THRESHOLD * int(math.log2(max(result.length(), 1) / self.leaf_max + 1) + 1):
            return result.rebalance()
        return result
    
    def delete(self, start: int, end: int) -> RopeNode:
        if start >= end:
            return self
        if start <= 0 and end >= self._length:
            return LeafNode("", self.leaf_max)
        
        left_len = self.left.length()
        
        if end <= left_len:
            new_left = self.left.delete(start, end)
            if new_left.length() == 0:
                return self.right
            return InternalNode(new_left, self.right, self.leaf_max).rebalance()
        
        if start >= left_len:
            new_right = self.right.delete(start - left_len, end - left_len)
            if new_right.length() == 0:
                return self.left
            return InternalNode(self.left, new_right, self.leaf_max).rebalance()
        
        # Spans both children
        new_left = self.left.delete(start, left_len)
        new_right = self.right.delete(0, end - left_len)
        
        if new_left.length() == 0:
            return new_right
        if new_right.length() == 0:
            return new_left
        
        return InternalNode(new_left, new_right, self.leaf_max).rebalance()
    
    def split(self, index: int) -> Tuple[RopeNode, RopeNode]:
        if index <= 0:
            return LeafNode("", self.leaf_max), self
        if index >= self._length:
            return self, LeafNode("", self.leaf_max)
        
        left_len = self.left.length()
        
        if index < left_len:
            l1, l2 = self.left.split(index)
            return l1, concat(l2, self.right, self.leaf_max)
        elif index > left_len:
            r1, r2 = self.right.split(index - left_len)
            return concat(self.left, r1, self.leaf_max), r2
        else:
            return self.left, self.right
    
    def to_string(self) -> str:
        return self.left.to_string() + self.right.to_string()
    
    def depth(self) -> int:
        return self._depth
    
    def rebalance(self) -> RopeNode:
        """Rebalance using the leaves extraction method."""
        leaves = self._collect_leaves()
        if not leaves:
            return LeafNode("", self.leaf_max)
        if len(leaves) == 1:
            return leaves[0]
        return self._build_balanced(leaves, 0, len(leaves))
    
    def _collect_leaves(self) -> List[LeafNode]:
        """Collect all leaf nodes in order."""
        leaves = []
        self._collect_leaves_helper(self, leaves)
        return leaves
    
    @staticmethod
    def _collect_leaves_helper(node: RopeNode, leaves: List[LeafNode]):
        if isinstance(node, LeafNode):
            if node.length() > 0:
                leaves.append(node)
        elif isinstance(node, InternalNode):
            InternalNode._collect_leaves_helper(node.left, leaves)
            InternalNode._collect_leaves_helper(node.right, leaves)
    
    def _build_balanced(self, leaves: List[LeafNode], start: int, end: int) -> RopeNode:
        """Build a balanced tree from leaves."""
        if start >= end:
            return LeafNode("", self.leaf_max)
        if start == end - 1:
            return leaves[start]
        mid = (start + end) // 2
        left = self._build_balanced(leaves, start, mid)
        right = self._build_balanced(leaves, mid, end)
        return InternalNode(left, right, self.leaf_max)
    
    def __repr__(self) -> str:
        return f"InternalNode(len={self._length}, depth={self._depth})"


# ============================================================================
# Rope Class (Main API)
# ============================================================================

class Rope:
    """
    Rope data structure for efficient string manipulation.
    
    A rope is a binary tree where leaves contain short strings.
    This allows O(log n) insertions, deletions, and concatenations
    instead of O(n) for regular strings.
    
    Example:
        >>> r = Rope("Hello, World!")
        >>> r.insert(7, "Beautiful ")
        >>> print(r)  # Hello, Beautiful World!
        >>> r.delete(7, 17)
        >>> print(r)  # Hello, World!
    """
    
    def __init__(self, text: str = "", leaf_max: int = DEFAULT_LEAF_MAX):
        """
        Initialize a Rope with optional text.
        
        Args:
            text: Initial string content
            leaf_max: Maximum characters per leaf node
        """
        self._leaf_max = leaf_max
        if not text:
            self._root: RopeNode = LeafNode("", leaf_max)
        elif len(text) <= leaf_max:
            self._root = LeafNode(text, leaf_max)
        else:
            # Split into multiple leaves for large initial text
            self._root = self._build_from_string(text)
    
    def _build_from_string(self, text: str) -> RopeNode:
        """Build a balanced rope from a string."""
        if len(text) <= self._leaf_max:
            return LeafNode(text, self._leaf_max)
        
        mid = len(text) // 2
        left = self._build_from_string(text[:mid])
        right = self._build_from_string(text[mid:])
        return InternalNode(left, right, self._leaf_max)
    
    @property
    def length(self) -> int:
        """Return total length of rope."""
        return self._root.length()
    
    def __len__(self) -> int:
        return self.length
    
    def __str__(self) -> str:
        return self._root.to_string()
    
    def __repr__(self) -> str:
        text = str(self)
        preview = text[:50] + "..." if len(text) > 50 else text
        return f"Rope({preview!r}, len={len(self)}, depth={self.depth()})"
    
    def __getitem__(self, index: Union[int, slice]) -> Union[str, 'Rope']:
        """Get character or slice."""
        if isinstance(index, slice):
            start, stop, step = index.start, index.stop, index.step
            if start is None:
                start = 0
            if stop is None:
                stop = len(self)
            if start < 0:
                start = len(self) + start
            if stop < 0:
                stop = len(self) + stop
            
            if step is not None and step != 1:
                return Rope(self._root.to_string()[start:stop:step], self._leaf_max)
            
            result = self._root.substring(start, stop)
            return Rope(result.to_string(), self._leaf_max)
        
        if index < 0:
            index = len(self) + index
        return self._root.char_at(index)
    
    def __iter__(self) -> Iterator[str]:
        """Iterate over all characters."""
        for i in range(len(self)):
            yield self._root.char_at(i)
    
    def __contains__(self, char: str) -> bool:
        """Check if character is in rope."""
        return char in str(self)
    
    def __add__(self, other: Union[str, 'Rope']) -> 'Rope':
        """Concatenate ropes or rope with string."""
        if isinstance(other, str):
            other = Rope(other, self._leaf_max)
        if isinstance(other, Rope):
            return concat_ropes(self, other, self._leaf_max)
        return NotImplemented
    
    def __radd__(self, other: str) -> 'Rope':
        """Right addition with string."""
        return Rope(other, self._leaf_max) + self
    
    def __mul__(self, n: int) -> 'Rope':
        """Repeat rope n times."""
        if n <= 0:
            return Rope("", self._leaf_max)
        result = self
        for _ in range(n - 1):
            result = result + self
        return result
    
    def __eq__(self, other: object) -> bool:
        """Check equality."""
        if isinstance(other, Rope):
            return str(self) == str(other)
        if isinstance(other, str):
            return str(self) == other
        return False
    
    def __hash__(self) -> int:
        """Hash of rope content."""
        return hash(str(self))
    
    def depth(self) -> int:
        """Return depth of the rope tree."""
        return self._root.depth()
    
    def char_at(self, index: int) -> str:
        """
        Get character at index.
        
        Args:
            index: Character index (0-based)
            
        Returns:
            Character at index
            
        Raises:
            IndexError: If index out of range
        """
        return self._root.char_at(index)
    
    def insert(self, index: int, text: str) -> 'Rope':
        """
        Insert text at index.
        
        Args:
            index: Position to insert at
            text: Text to insert
            
        Returns:
            New rope with text inserted
        """
        if not text:
            return self
        new_root = self._root.insert(index, text)
        result = Rope.__new__(Rope)
        result._leaf_max = self._leaf_max
        result._root = new_root
        return result
    
    def delete(self, start: int, end: int) -> 'Rope':
        """
        Delete characters in range [start, end).
        
        Args:
            start: Start index (inclusive)
            end: End index (exclusive)
            
        Returns:
            New rope with characters deleted
        """
        if start >= end:
            return self
        new_root = self._root.delete(start, end)
        result = Rope.__new__(Rope)
        result._leaf_max = self._leaf_max
        result._root = new_root
        return result
    
    def split(self, index: int) -> Tuple['Rope', 'Rope']:
        """
        Split rope at index.
        
        Args:
            index: Position to split at
            
        Returns:
            Tuple of (left_rope, right_rope)
        """
        left, right = self._root.split(index)
        
        left_rope = Rope.__new__(Rope)
        left_rope._leaf_max = self._leaf_max
        left_rope._root = left
        
        right_rope = Rope.__new__(Rope)
        right_rope._leaf_max = self._leaf_max
        right_rope._root = right
        
        return left_rope, right_rope
    
    def substring(self, start: int, end: int) -> 'Rope':
        """
        Extract substring [start, end).
        
        Args:
            start: Start index (inclusive)
            end: End index (exclusive)
            
        Returns:
            New rope with substring
        """
        result = self._root.substring(start, end)
        return Rope(result.to_string(), self._leaf_max)
    
    def find(self, sub: str, start: int = 0) -> int:
        """
        Find substring in rope.
        
        Args:
            sub: Substring to find
            start: Start position for search
            
        Returns:
            Index of first occurrence, or -1 if not found
        """
        # For simplicity, convert to string for search
        # More sophisticated implementations could use Boyer-Moore on the tree
        text = str(self)
        return text.find(sub, start)
    
    def rfind(self, sub: str, end: int = None) -> int:
        """
        Find substring from right.
        
        Args:
            sub: Substring to find
            end: End position for search
            
        Returns:
            Index of last occurrence, or -1 if not found
        """
        text = str(self)
        if end is None:
            return text.rfind(sub)
        return text.rfind(sub, 0, end)
    
    def count(self, sub: str) -> int:
        """Count occurrences of substring."""
        return str(self).count(sub)
    
    def replace(self, old: str, new: str, count: int = -1) -> 'Rope':
        """
        Replace occurrences of old with new.
        
        Args:
            old: Substring to replace
            new: Replacement string
            count: Maximum replacements (-1 for all)
            
        Returns:
            New rope with replacements
        """
        text = str(self)
        new_text = text.replace(old, new, count)
        return Rope(new_text, self._leaf_max)
    
    def startswith(self, prefix: str) -> bool:
        """Check if rope starts with prefix."""
        return str(self).startswith(prefix)
    
    def endswith(self, suffix: str) -> bool:
        """Check if rope ends with suffix."""
        return str(self).endswith(suffix)
    
    def strip(self, chars: str = None) -> 'Rope':
        """Strip leading/trailing characters."""
        return Rope(str(self).strip(chars), self._leaf_max)
    
    def lstrip(self, chars: str = None) -> 'Rope':
        """Strip leading characters."""
        return Rope(str(self).lstrip(chars), self._leaf_max)
    
    def rstrip(self, chars: str = None) -> 'Rope':
        """Strip trailing characters."""
        return Rope(str(self).rstrip(chars), self._leaf_max)
    
    def upper(self) -> 'Rope':
        """Convert to uppercase."""
        return Rope(str(self).upper(), self._leaf_max)
    
    def lower(self) -> 'Rope':
        """Convert to lowercase."""
        return Rope(str(self).lower(), self._leaf_max)
    
    def title(self) -> 'Rope':
        """Convert to title case."""
        return Rope(str(self).title(), self._leaf_max)
    
    def capitalize(self) -> 'Rope':
        """Capitalize first character."""
        return Rope(str(self).capitalize(), self._leaf_max)
    
    def reverse(self) -> 'Rope':
        """Reverse the rope."""
        return Rope(str(self)[::-1], self._leaf_max)
    
    def join(self, items: List[Union[str, 'Rope']]) -> 'Rope':
        """Join items using this rope as separator."""
        str_items = [str(item) for item in items]
        return Rope(str(self).join(str_items), self._leaf_max)
    
    def lines(self) -> List[str]:
        """Split rope into lines."""
        return str(self).splitlines()
    
    def words(self) -> List[str]:
        """Split rope into words."""
        return str(self).split()
    
    def rebalance(self) -> 'Rope':
        """
        Rebalance the rope tree.
        
        Returns:
            Rebalanced rope
        """
        result = Rope.__new__(Rope)
        result._leaf_max = self._leaf_max
        result._root = self._root.rebalance()
        return result
    
    def is_balanced(self) -> bool:
        """Check if rope is balanced."""
        expected_depth = int(math.log2(max(len(self), 1) / self._leaf_max + 1) + 1)
        return self.depth() <= expected_depth * REBALANCE_THRESHOLD
    
    def stats(self) -> dict:
        """
        Get rope statistics.
        
        Returns:
            Dictionary with statistics
        """
        leaves = self._collect_leaves()
        return {
            'length': len(self),
            'depth': self.depth(),
            'leaf_count': len(leaves),
            'avg_leaf_size': sum(l.length() for l in leaves) / len(leaves) if leaves else 0,
            'max_leaf_size': max((l.length() for l in leaves), default=0),
            'is_balanced': self.is_balanced(),
        }
    
    def _collect_leaves(self) -> List[LeafNode]:
        """Collect all leaf nodes."""
        leaves = []
        self._collect_leaves_helper(self._root, leaves)
        return leaves
    
    @staticmethod
    def _collect_leaves_helper(node: RopeNode, leaves: List[LeafNode]):
        if isinstance(node, LeafNode):
            if node.length() > 0:
                leaves.append(node)
        elif isinstance(node, InternalNode):
            Rope._collect_leaves_helper(node.left, leaves)
            Rope._collect_leaves_helper(node.right, leaves)


# ============================================================================
# Utility Functions
# ============================================================================

def concat(left: RopeNode, right: RopeNode, leaf_max: int = DEFAULT_LEAF_MAX) -> RopeNode:
    """
    Concatenate two rope nodes.
    
    Args:
        left: Left rope node
        right: Right rope node
        leaf_max: Maximum leaf size
        
    Returns:
        New rope node containing both
    """
    if left.length() == 0:
        return right
    if right.length() == 0:
        return left
    
    # If both are small leaves, merge them
    if isinstance(left, LeafNode) and isinstance(right, LeafNode):
        combined = left.text + right.text
        if len(combined) <= leaf_max:
            return LeafNode(combined, leaf_max)
    
    return InternalNode(left, right, leaf_max)


def concat_ropes(left: Rope, right: Rope, leaf_max: int = DEFAULT_LEAF_MAX) -> Rope:
    """
    Concatenate two ropes.
    
    Args:
        left: Left rope
        right: Right rope
        leaf_max: Maximum leaf size
        
    Returns:
        New rope containing both
    """
    result = Rope.__new__(Rope)
    result._leaf_max = leaf_max
    result._root = concat(left._root, right._root, leaf_max)
    return result


def from_lines(lines: List[str], leaf_max: int = DEFAULT_LEAF_MAX) -> Rope:
    """
    Create rope from list of lines.
    
    Args:
        lines: List of strings
        leaf_max: Maximum leaf size
        
    Returns:
        Rope containing all lines joined with newlines
    """
    return Rope('\n'.join(lines), leaf_max)


def from_file(filepath: str, leaf_max: int = DEFAULT_LEAF_MAX) -> Rope:
    """
    Create rope from file contents.
    
    Args:
        filepath: Path to file
        leaf_max: Maximum leaf size
        
    Returns:
        Rope containing file contents
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return Rope(f.read(), leaf_max)


def to_file(rope: Rope, filepath: str) -> None:
    """
    Write rope contents to file.
    
    Args:
        rope: Rope to write
        filepath: Path to file
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(rope))


def build_balanced(text: str, leaf_max: int = DEFAULT_LEAF_MAX) -> Rope:
    """
    Build a balanced rope from text.
    
    Args:
        text: Text to build rope from
        leaf_max: Maximum leaf size
        
    Returns:
        Balanced rope
    """
    return Rope(text, leaf_max)


# ============================================================================
# Batch Operations
# ============================================================================

class BatchEditor:
    """
    Batch editor for efficient multiple operations on a rope.
    
    Accumulates operations and applies them all at once by building
    the result directly from the original text, avoiding index 
    shifting issues.
    """
    
    def __init__(self, rope: Rope):
        """Initialize with a rope."""
        self._original = rope
        self._operations: List[Tuple[str, int, int, Optional[str]]] = []
    
    def insert(self, index: int, text: str) -> 'BatchEditor':
        """Queue an insert operation at the given index."""
        self._operations.append(('insert', index, index + 1, text))
        return self
    
    def delete(self, start: int, end: int) -> 'BatchEditor':
        """Queue a delete operation in range [start, end)."""
        self._operations.append(('delete', start, end, None))
        return self
    
    def replace(self, start: int, end: int, text: str) -> 'BatchEditor':
        """Queue a replace operation (delete + insert at same position)."""
        self._operations.append(('replace', start, end, text))
        return self
    
    def apply(self) -> Rope:
        """Apply all queued operations and return new rope."""
        if not self._operations:
            return self._original
        
        # Convert to string for batch processing
        text = str(self._original)
        original_len = len(text)
        
        # Sort operations by start index (ascending)
        # We'll build result by merging intervals
        sorted_ops = sorted(self._operations, key=lambda x: x[1])
        
        # Build result using interval merging approach
        # Each operation creates a segment: [start, end) -> replacement text
        segments = []
        
        # First, mark all regions affected by operations
        affected_ranges = []
        for op in sorted_ops:
            start, end = op[1], op[2]
            if op[0] == 'delete':
                affected_ranges.append((start, end, ""))
            elif op[0] == 'insert':
                # Insert doesn delete anything, just adds at position
                affected_ranges.append((start, start, op[3]))
            elif op[0] == 'replace':
                affected_ranges.append((start, end, op[3]))
        
        # Sort by start position
        affected_ranges.sort(key=lambda x: x[0])
        
        # Merge overlapping ranges and build final segments
        result_parts = []
        current_pos = 0
        
        for start, end, replacement in affected_ranges:
            # Add unchanged text before this operation
            if start > current_pos:
                result_parts.append(text[current_pos:start])
            # Add the replacement
            result_parts.append(replacement)
            # Move position past the deleted region
            current_pos = max(current_pos, end)
        
        # Add remaining text after all operations
        if current_pos < original_len:
            result_parts.append(text[current_pos:])
        
        # Create result rope
        result_text = "".join(result_parts)
        return Rope(result_text, self._original._leaf_max)
    
    def clear(self) -> 'BatchEditor':
        """Clear all queued operations."""
        self._operations.clear()
        return self


# ============================================================================
# Rope Iterator
# ============================================================================

class RopeIterator:
    """Iterator for traversing rope nodes."""
    
    def __init__(self, rope: Rope):
        self._rope = rope
        self._index = 0
    
    def __iter__(self) -> 'RopeIterator':
        return self
    
    def __next__(self) -> str:
        if self._index >= len(self._rope):
            raise StopIteration
        char = self._rope.char_at(self._index)
        self._index += 1
        return char


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    'Rope',
    'RopeNode',
    'LeafNode',
    'InternalNode',
    'BatchEditor',
    'RopeIterator',
    'concat',
    'concat_ropes',
    'from_lines',
    'from_file',
    'to_file',
    'build_balanced',
    'DEFAULT_LEAF_MAX',
]