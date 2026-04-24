"""
Binary Search Tree (BST) Utilities
===================================
A comprehensive, zero-dependency implementation of Binary Search Tree operations.

Features:
- Core BST operations: insert, delete, search
- Multiple traversal methods: in-order, pre-order, post-order, level-order
- Tree analysis: height, size, min/max, validation
- Serialization/Deserialization to/from various formats
- Balanced BST operations with AVL-style rotations
- Range queries and predecessor/successor finding
"""

from typing import Optional, List, Any, Callable, Iterator, TypeVar, Generic
from collections import deque
import json

T = TypeVar('T')


class BSTNode(Generic[T]):
    """A node in the Binary Search Tree."""
    
    __slots__ = ['value', 'left', 'right', 'parent']
    
    def __init__(self, value: T, parent: Optional['BSTNode[T]'] = None):
        self.value: T = value
        self.left: Optional[BSTNode[T]] = None
        self.right: Optional[BSTNode[T]] = None
        self.parent: Optional[BSTNode[T]] = parent
    
    def __repr__(self) -> str:
        return f"BSTNode({self.value})"
    
    def is_leaf(self) -> bool:
        """Check if this node is a leaf (no children)."""
        return self.left is None and self.right is None
    
    def has_one_child(self) -> bool:
        """Check if this node has exactly one child."""
        return (self.left is None) != (self.right is None)
    
    def has_two_children(self) -> bool:
        """Check if this node has two children."""
        return self.left is not None and self.right is not None


class BST(Generic[T]):
    """
    Binary Search Tree implementation with comprehensive operations.
    
    Example:
        >>> bst = BST[int]()
        >>> bst.insert(5)
        >>> bst.insert(3)
        >>> bst.insert(7)
        >>> list(bst.inorder())
        [3, 5, 7]
    """
    
    def __init__(self):
        self._root: Optional[BSTNode[T]] = None
        self._size: int = 0
        self._comparator: Callable[[T, T], int] = self._default_compare
    
    @staticmethod
    def _default_compare(a: T, b: T) -> int:
        """Default comparison function (works for comparable types)."""
        if a < b:
            return -1
        elif a > b:
            return 1
        return 0
    
    # ==================== Core Operations ====================
    
    @property
    def root(self) -> Optional[BSTNode[T]]:
        """Get the root node."""
        return self._root
    
    @property
    def size(self) -> int:
        """Get the number of nodes in the tree."""
        return self._size
    
    @property
    def is_empty(self) -> bool:
        """Check if the tree is empty."""
        return self._root is None
    
    def insert(self, value: T) -> bool:
        """
        Insert a value into the BST.
        
        Args:
            value: The value to insert
            
        Returns:
            True if inserted, False if value already exists
        """
        if self._root is None:
            self._root = BSTNode(value)
            self._size = 1
            return True
        
        current = self._root
        while True:
            cmp = self._comparator(value, current.value)
            
            if cmp < 0:
                if current.left is None:
                    current.left = BSTNode(value, parent=current)
                    self._size += 1
                    return True
                current = current.left
            elif cmp > 0:
                if current.right is None:
                    current.right = BSTNode(value, parent=current)
                    self._size += 1
                    return True
                current = current.right
            else:
                # Value already exists
                return False
    
    def insert_many(self, values: List[T]) -> int:
        """
        Insert multiple values.
        
        Args:
            values: List of values to insert
            
        Returns:
            Number of values actually inserted
        """
        count = 0
        for value in values:
            if self.insert(value):
                count += 1
        return count
    
    def search(self, value: T) -> Optional[BSTNode[T]]:
        """
        Search for a value in the BST.
        
        Args:
            value: The value to search for
            
        Returns:
            The node containing the value, or None if not found
        """
        current = self._root
        while current is not None:
            cmp = self._comparator(value, current.value)
            if cmp < 0:
                current = current.left
            elif cmp > 0:
                current = current.right
            else:
                return current
        return None
    
    def contains(self, value: T) -> bool:
        """Check if a value exists in the BST."""
        return self.search(value) is not None
    
    def delete(self, value: T) -> bool:
        """
        Delete a value from the BST.
        
        Uses the standard BST deletion algorithm:
        - For leaf nodes: simply remove
        - For nodes with one child: replace with child
        - For nodes with two children: replace with in-order successor
        
        Args:
            value: The value to delete
            
        Returns:
            True if deleted, False if value not found
        """
        node = self.search(value)
        if node is None:
            return False
        
        self._delete_node(node)
        self._size -= 1
        return True
    
    def _delete_node(self, node: BSTNode[T]) -> None:
        """Internal method to delete a node."""
        if node.is_leaf():
            self._replace_node(node, None)
        elif node.has_one_child():
            child = node.left if node.left is not None else node.right
            self._replace_node(node, child)
        else:
            # Two children: find in-order successor
            successor = self._find_min_node(node.right)
            node.value = successor.value
            self._delete_node(successor)
    
    def _replace_node(self, node: BSTNode[T], replacement: Optional[BSTNode[T]]) -> None:
        """Replace a node with another node."""
        parent = node.parent
        if parent is None:
            self._root = replacement
        elif parent.left is node:
            parent.left = replacement
        else:
            parent.right = replacement
        
        if replacement is not None:
            replacement.parent = parent
    
    # ==================== Min/Max Operations ====================
    
    def find_min(self) -> Optional[T]:
        """Find the minimum value in the BST."""
        node = self._find_min_node(self._root)
        return node.value if node else None
    
    def find_max(self) -> Optional[T]:
        """Find the maximum value in the BST."""
        node = self._find_max_node(self._root)
        return node.value if node else None
    
    def _find_min_node(self, root: Optional[BSTNode[T]]) -> Optional[BSTNode[T]]:
        """Find the node with minimum value starting from root."""
        if root is None:
            return None
        current = root
        while current.left is not None:
            current = current.left
        return current
    
    def _find_max_node(self, root: Optional[BSTNode[T]]) -> Optional[BSTNode[T]]:
        """Find the node with maximum value starting from root."""
        if root is None:
            return None
        current = root
        while current.right is not None:
            current = current.right
        return current
    
    # ==================== Predecessor/Successor ====================
    
    def find_successor(self, value: T) -> Optional[T]:
        """
        Find the in-order successor of a value.
        
        Args:
            value: The value to find successor for
            
        Returns:
            The successor value, or None if no successor exists
        """
        node = self.search(value)
        if node is None:
            return None
        
        # If right subtree exists, successor is minimum in right subtree
        if node.right is not None:
            successor = self._find_min_node(node.right)
            return successor.value if successor else None
        
        # Otherwise, go up until we find an ancestor whose left subtree contains the node
        current = node.parent
        while current is not None and node is current.right:
            node = current
            current = current.parent
        
        return current.value if current else None
    
    def find_predecessor(self, value: T) -> Optional[T]:
        """
        Find the in-order predecessor of a value.
        
        Args:
            value: The value to find predecessor for
            
        Returns:
            The predecessor value, or None if no predecessor exists
        """
        node = self.search(value)
        if node is None:
            return None
        
        # If left subtree exists, predecessor is maximum in left subtree
        if node.left is not None:
            predecessor = self._find_max_node(node.left)
            return predecessor.value if predecessor else None
        
        # Otherwise, go up until we find an ancestor whose right subtree contains the node
        current = node.parent
        while current is not None and node is current.left:
            node = current
            current = current.parent
        
        return current.value if current else None
    
    # ==================== Traversals ====================
    
    def inorder(self) -> Iterator[T]:
        """
        In-order traversal (left, root, right).
        Yields values in sorted order for BST.
        """
        yield from self._inorder(self._root)
    
    def _inorder(self, node: Optional[BSTNode[T]]) -> Iterator[T]:
        """Recursive in-order traversal."""
        if node is not None:
            yield from self._inorder(node.left)
            yield node.value
            yield from self._inorder(node.right)
    
    def preorder(self) -> Iterator[T]:
        """
        Pre-order traversal (root, left, right).
        Useful for creating a copy of the tree.
        """
        yield from self._preorder(self._root)
    
    def _preorder(self, node: Optional[BSTNode[T]]) -> Iterator[T]:
        """Recursive pre-order traversal."""
        if node is not None:
            yield node.value
            yield from self._preorder(node.left)
            yield from self._preorder(node.right)
    
    def postorder(self) -> Iterator[T]:
        """
        Post-order traversal (left, right, root).
        Useful for deleting nodes or evaluating expression trees.
        """
        yield from self._postorder(self._root)
    
    def _postorder(self, node: Optional[BSTNode[T]]) -> Iterator[T]:
        """Recursive post-order traversal."""
        if node is not None:
            yield from self._postorder(node.left)
            yield from self._postorder(node.right)
            yield node.value
    
    def levelorder(self) -> Iterator[T]:
        """
        Level-order (BFS) traversal.
        Visits nodes level by level from top to bottom.
        """
        if self._root is None:
            return
        
        queue = deque([self._root])
        while queue:
            node = queue.popleft()
            yield node.value
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    def reverse_inorder(self) -> Iterator[T]:
        """
        Reverse in-order traversal (right, root, left).
        Yields values in descending order for BST.
        """
        yield from self._reverse_inorder(self._root)
    
    def _reverse_inorder(self, node: Optional[BSTNode[T]]) -> Iterator[T]:
        """Recursive reverse in-order traversal."""
        if node is not None:
            yield from self._reverse_inorder(node.right)
            yield node.value
            yield from self._reverse_inorder(node.left)
    
    # ==================== Tree Properties ====================
    
    def height(self) -> int:
        """
        Calculate the height of the tree.
        
        Returns:
            Height of the tree (-1 for empty tree, 0 for single node)
        """
        return self._height(self._root)
    
    def _height(self, node: Optional[BSTNode[T]]) -> int:
        """Recursively calculate height."""
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))
    
    def depth(self, value: T) -> int:
        """
        Find the depth of a value in the tree.
        
        Args:
            value: The value to find depth for
            
        Returns:
            Depth of the value, or -1 if not found
        """
        depth = 0
        current = self._root
        while current is not None:
            cmp = self._comparator(value, current.value)
            if cmp < 0:
                current = current.left
                depth += 1
            elif cmp > 0:
                current = current.right
                depth += 1
            else:
                return depth
        return -1
    
    def is_balanced(self) -> bool:
        """
        Check if the tree is balanced (AVL condition).
        A tree is balanced if for every node, the height difference
        between left and right subtrees is at most 1.
        """
        return self._check_balance(self._root) != -2
    
    def _check_balance(self, node: Optional[BSTNode[T]]) -> int:
        """
        Check balance and return height.
        Returns -2 if unbalanced, otherwise returns height.
        """
        if node is None:
            return -1
        
        left_height = self._check_balance(node.left)
        if left_height == -2:
            return -2
        
        right_height = self._check_balance(node.right)
        if right_height == -2:
            return -2
        
        if abs(left_height - right_height) > 1:
            return -2
        
        return 1 + max(left_height, right_height)
    
    def is_valid_bst(self) -> bool:
        """
        Validate that the tree is a valid BST.
        Checks if all left descendants are less than node
        and all right descendants are greater than node.
        """
        return self._validate_bst(self._root, None, None)
    
    def _validate_bst(self, node: Optional[BSTNode[T]], 
                      min_val: Optional[T], max_val: Optional[T]) -> bool:
        """Recursively validate BST property."""
        if node is None:
            return True
        
        if min_val is not None and self._comparator(node.value, min_val) <= 0:
            return False
        if max_val is not None and self._comparator(node.value, max_val) >= 0:
            return False
        
        return (self._validate_bst(node.left, min_val, node.value) and
                self._validate_bst(node.right, node.value, max_val))
    
    # ==================== Range Queries ====================
    
    def range_query(self, low: T, high: T) -> List[T]:
        """
        Find all values in the given range [low, high].
        
        Args:
            low: Lower bound (inclusive)
            high: Upper bound (inclusive)
            
        Returns:
            List of values in the range, in sorted order
        """
        result: List[T] = []
        self._range_query(self._root, low, high, result)
        return result
    
    def _range_query(self, node: Optional[BSTNode[T]], 
                     low: T, high: T, result: List[T]) -> None:
        """Recursive range query."""
        if node is None:
            return
        
        # If current value > low, there might be values in left subtree
        if self._comparator(node.value, low) > 0:
            self._range_query(node.left, low, high, result)
        
        # If current value is in range, add it
        if self._comparator(node.value, low) >= 0 and self._comparator(node.value, high) <= 0:
            result.append(node.value)
        
        # If current value < high, there might be values in right subtree
        if self._comparator(node.value, high) < 0:
            self._range_query(node.right, low, high, result)
    
    def count_range(self, low: T, high: T) -> int:
        """Count values in the given range."""
        return len(self.range_query(low, high))
    
    # ==================== K-th Element ====================
    
    def kth_smallest(self, k: int) -> Optional[T]:
        """
        Find the k-th smallest value (1-indexed).
        
        Args:
            k: The position (1-indexed)
            
        Returns:
            The k-th smallest value, or None if k is invalid
        """
        if k < 1 or k > self._size:
            return None
        
        # Iterative in-order traversal to avoid recursion depth issues
        count = 0
        stack = []
        current = self._root
        
        while stack or current:
            # Go to leftmost node
            while current:
                stack.append(current)
                current = current.left
            
            # Process current node
            current = stack.pop()
            count += 1
            
            if count == k:
                return current.value
            
            # Move to right subtree
            current = current.right
        
        return None
    
    def kth_largest(self, k: int) -> Optional[T]:
        """
        Find the k-th largest value (1-indexed).
        
        Args:
            k: The position (1-indexed)
            
        Returns:
            The k-th largest value, or None if k is invalid
        """
        return self.kth_smallest(self._size - k + 1)
    
    # ==================== Serialization ====================
    
    def to_list(self) -> List[Optional[T]]:
        """
        Serialize the BST to a list (level-order with None markers).
        
        Returns:
            List representation of the tree
        """
        if self._root is None:
            return []
        
        result: List[Optional[T]] = []
        queue: deque = deque([self._root])
        
        while queue:
            node = queue.popleft()
            if node is None:
                result.append(None)
            else:
                result.append(node.value)
                queue.append(node.left)
                queue.append(node.right)
        
        # Remove trailing None values
        while result and result[-1] is None:
            result.pop()
        
        return result
    
    @classmethod
    def from_list(cls, values: List[Optional[T]]) -> 'BST[T]':
        """
        Deserialize a BST from a list (level-order with None markers).
        
        Args:
            values: List representation of the tree
            
        Returns:
            A new BST instance
        """
        bst = cls()
        if not values:
            return bst
        
        bst._root = BSTNode(values[0])
        bst._size = 1
        queue: deque = deque([bst._root])
        i = 1
        
        while queue and i < len(values):
            node = queue.popleft()
            
            if i < len(values) and values[i] is not None:
                node.left = BSTNode(values[i], parent=node)
                bst._size += 1
            queue.append(node.left)
            i += 1
            
            if i < len(values) and values[i] is not None:
                node.right = BSTNode(values[i], parent=node)
                bst._size += 1
            queue.append(node.right)
            i += 1
        
        return bst
    
    def to_sorted_list(self) -> List[T]:
        """Get all values in sorted order."""
        return list(self.inorder())
    
    # ==================== Tree Building ====================
    
    @classmethod
    def from_sorted_list(cls, values: List[T]) -> 'BST[T]':
        """
        Build a balanced BST from a sorted list.
        
        Args:
            values: Sorted list of values
            
        Returns:
            A balanced BST
        """
        bst = cls()
        if not values:
            return bst
        
        bst._root, bst._size = bst._build_balanced_iterative(values)
        return bst
    
    def _build_balanced_iterative(self, values: List[T]) -> tuple:
        """Iteratively build a balanced BST to avoid recursion depth issues."""
        n = len(values)
        if n == 0:
            return None, 0
        
        # Use a stack to simulate recursion
        # Each entry: (parent, is_left, start, end)
        root = BSTNode(values[n // 2])
        size = 1
        stack = [(root, True, 0, n // 2 - 1), (root, False, n // 2 + 1, n - 1)]
        
        while stack:
            parent, is_left, start, end = stack.pop()
            if start > end:
                continue
            
            mid = (start + end) // 2
            node = BSTNode(values[mid], parent)
            size += 1
            
            if is_left:
                parent.left = node
            else:
                parent.right = node
            
            # Push children to process
            stack.append((node, True, start, mid - 1))
            stack.append((node, False, mid + 1, end))
        
        return root, size
    
    def balance(self) -> None:
        """Balance the BST by rebuilding from sorted values."""
        if self._root is None:
            return
        
        values = list(self.inorder())
        self._root, self._size = self._build_balanced_iterative(values)
    
    # ==================== Visualization ====================
    
    def __str__(self) -> str:
        """String representation of the tree."""
        if self._root is None:
            return "BST(empty)"
        
        lines: List[str] = []
        self._build_string(self._root, "", True, lines)
        return "BST:\n" + "\n".join(lines)
    
    def _build_string(self, node: Optional[BSTNode[T]], prefix: str, 
                      is_last: bool, lines: List[str]) -> None:
        """Build string representation recursively."""
        if node is None:
            return
        
        lines.append(prefix + ("└── " if is_last else "├── ") + str(node.value))
        
        children = []
        if node.left:
            children.append((node.left, "L"))
        if node.right:
            children.append((node.right, "R"))
        
        for i, (child, _) in enumerate(children):
            is_last_child = i == len(children) - 1
            new_prefix = prefix + ("    " if is_last else "│   ")
            self._build_string(child, new_prefix, is_last_child, lines)
    
    def __repr__(self) -> str:
        return f"BST(size={self._size})"
    
    def __len__(self) -> int:
        return self._size
    
    def __contains__(self, value: T) -> bool:
        return self.contains(value)
    
    def __iter__(self) -> Iterator[T]:
        return self.inorder()
    
    def clear(self) -> None:
        """Clear all nodes from the tree."""
        self._root = None
        self._size = 0


# ==================== Utility Functions ====================

def create_bst(values: List[T]) -> BST[T]:
    """
    Create a BST from a list of values.
    
    Args:
        values: Values to insert
        
    Returns:
        A new BST containing the values
    """
    bst = BST()
    for value in values:
        bst.insert(value)
    return bst


def create_balanced_bst(values: List[T]) -> BST[T]:
    """
    Create a balanced BST from a list of values.
    
    Args:
        values: Values to insert (will be sorted)
        
    Returns:
        A balanced BST containing the values
    """
    sorted_values = sorted(values)
    return BST.from_sorted_list(sorted_values)


def merge_bsts(bst1: BST[T], bst2: BST[T]) -> BST[T]:
    """
    Merge two BSTs into a new balanced BST.
    
    Args:
        bst1: First BST
        bst2: Second BST
        
    Returns:
        A new balanced BST containing all values from both trees
    """
    values = list(bst1.inorder()) + list(bst2.inorder())
    sorted_values = sorted(set(values))
    return BST.from_sorted_list(sorted_values)


def are_identical(bst1: BST[T], bst2: BST[T]) -> bool:
    """
    Check if two BSTs have identical structure and values.
    
    Args:
        bst1: First BST
        bst2: Second BST
        
    Returns:
        True if trees are identical
    """
    return _check_identical(bst1.root, bst2.root)


def _check_identical(node1: Optional[BSTNode[T]], node2: Optional[BSTNode[T]]) -> bool:
    """Recursively check if two subtrees are identical."""
    if node1 is None and node2 is None:
        return True
    if node1 is None or node2 is None:
        return False
    return (node1.value == node2.value and
            _check_identical(node1.left, node2.left) and
            _check_identical(node1.right, node2.right))


def lowest_common_ancestor(bst: BST[T], value1: T, value2: T) -> Optional[T]:
    """
    Find the lowest common ancestor of two values in a BST.
    
    Args:
        bst: The BST to search in
        value1: First value
        value2: Second value
        
    Returns:
        The LCA value, or None if either value is not in the tree
    """
    if bst.root is None:
        return None
    
    if not bst.contains(value1) or not bst.contains(value2):
        return None
    
    current = bst.root
    while current:
        if value1 < current.value and value2 < current.value:
            current = current.left
        elif value1 > current.value and value2 > current.value:
            current = current.right
        else:
            return current.value
    
    return None