"""
Binary Tree Utilities - Comprehensive binary tree operations and algorithms.

Features:
- Tree construction from various input formats
- Traversal methods (preorder, inorder, postorder, level-order, zigzag)
- Search and query operations
- Tree properties (height, balance, symmetry)
- Modification operations (insert, delete, mirror)
- Serialization and deserialization
- Common algorithms (lowest common ancestor, diameter, path finding)

Zero external dependencies.
"""

from collections import deque
from typing import Optional, List, Callable, Tuple, Any


class TreeNode:
    """Binary tree node."""
    
    __slots__ = ('val', 'left', 'right')
    
    def __init__(self, val=None, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    
    def __repr__(self):
        return "TreeNode({})".format(self.val)
    
    def __eq__(self, other):
        if not isinstance(other, TreeNode):
            return False
        return self.val == other.val and self.left == other.right and self.right == other.right


def from_list(values):
    """
    Construct binary tree from level-order list representation.
    
    Args:
        values: List where index i has value, None for empty, results in flat tree
    
    Returns:
        Root node of constructed tree
    
    Example:
        >>> root = from_list([1, 2, 3, None, 4, 5, 6])
    """
    if not values:
        return None
    
    nodes = [None if v is None else TreeNode(v) for v in values]
    kids = nodes[::-1]
    root = kids.pop()
    
    for node in nodes:
        if node:
            if kids:
                node.left = kids.pop()
            if kids:
                node.right = kids.pop()
    
    return root


def from_nested_tuple(data):
    """
    Construct tree from nested tuple (left, root, right) or single value.
    
    Args:
        data: Nested tuple or single value
    
    Returns:
        Root node of constructed tree
    
    Example:
        >>> root = from_nested_tuple(((None, 2, None), 1, (None, 3, None)))
    """
    if not isinstance(data, tuple):
        return TreeNode(data)
    
    if len(data) == 3:
        left, val, right = data
        return TreeNode(val, from_nested_tuple(left), from_nested_tuple(right))
    elif len(data) == 2:
        left, val = data
        return TreeNode(val, from_nested_tuple(left))
    else:
        return TreeNode(data[0] if data else None)


def to_list(root):
    """
    Convert tree to level-order list representation.
    
    Args:
        root: Root node
    
    Returns:
        List representation of tree
    
    Example:
        >>> lst = to_list(root)
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        result.append(node.val if node else None)
        if node:
            queue.append(node.left)
            queue.append(node.right)
    
    while result and result[-1] is None:
        result.pop()
    
    return result


def to_nested_tuple(root):
    """
    Convert tree to nested tuple representation.
    
    Args:
        root: Root node
    
    Returns:
        Nested tuple representation or None
    """
    if not root:
        return None
    
    return (
        to_nested_tuple(root.left),
        root.val,
        to_nested_tuple(root.right)
    )


# Traversal methods
def preorder(root):
    """Root-Left-Right traversal."""
    if not root:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)


def inorder(root):
    """Left-Root-Right traversal."""
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)


def postorder(root):
    """Left-Right-Root traversal."""
    if not root:
        return []
    return postorder(root.left) + postorder(root.right) + [root.val]


def level_order(root):
    """Level-order traversal returning list of levels."""
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    
    return result


def zigzag_level_order(root):
    """Zigzag level-order traversal."""
    if not root:
        return []
    
    result = []
    queue = deque([root])
    left_to_right = True
    
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if left_to_right:
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            else:
                if node.right:
                    queue.append(node.right)
                if node.left:
                    queue.append(node.left)
        result.append(level if left_to_right else level[::-1])
        left_to_right = not left_to_right
    
    return result


def morris_inorder(root):
    """Morris inorder traversal - O(1) space."""
    result = []
    current = root
    
    while current:
        if not current.left:
            result.append(current.val)
            current = current.right
        else:
            predecessor = current.left
            while predecessor.right and predecessor.right != current:
                predecessor = predecessor.right
            
            if not predecessor.right:
                predecessor.right = current
                current = current.left
            else:
                predecessor.right = None
                result.append(current.val)
                current = current.right
    
    return result


# Query operations
def find(root, val):
    """Find node with given value."""
    if not root:
        return None
    if root.val == val:
        return root
    return find(root.left, val) or find(root.right, val)


def find_path(root, target):
    """Find path from root to target node."""
    def dfs(node, path):
        if not node:
            return False
        path.append(node)
        if node.val == target:
            return True
        if dfs(node.left, path) or dfs(node.right, path):
            return True
        path.pop()
        return False
    
    path = []
    dfs(root, path)
    return path


def lowest_common_ancestor(root, p, q):
    """Find lowest common ancestor of two nodes."""
    if not root or root.val == p or root.val == q:
        return root
    
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    
    if left and right:
        return root
    return left or right


def lowest_common_ancestor_nodes(root, p, q):
    """Find LCA when nodes are TreeNode objects."""
    if not root or root is p or root is q:
        return root
    
    left = lowest_common_ancestor_nodes(root.left, p, q)
    right = lowest_common_ancestor_nodes(root.right, p, q)
    
    if left and right:
        return root
    return left or right


# Tree properties
def height(root):
    """Calculate tree height (number of nodes on longest path)."""
    if not root:
        return 0
    return 1 + max(height(root.left), height(root.right))


def count(root):
    """Count total nodes in tree."""
    if not root:
        return 0
    return 1 + count(root.left) + count(root.right)


def leaf_count(root):
    """Count leaf nodes."""
    if not root:
        return 0
    if not root.left and not root.right:
        return 1
    return leaf_count(root.left) + leaf_count(root.right)


def is_balanced(root):
    """Check if tree is height-balanced."""
    def check(node):
        if not node:
            return True, 0
        balanced_l, h_l = check(node.left)
        balanced_r, h_r = check(node.right)
        return balanced_l and balanced_r and abs(h_l - h_r) <= 1, 1 + max(h_l, h_r)
    
    return check(root)[0]


def is_symmetric(root):
    """Check if tree is symmetric."""
    def mirror(left, right):
        if not left and not right:
            return True
        if not left or not right:
            return False
        return left.val == right.val and mirror(left.left, right.right) and mirror(left.right, right.left)
    
    return mirror(root, root)


def is_same_tree(t1, t2):
    """Check if two trees are identical."""
    if not t1 and not t2:
        return True
    if not t1 or not t2:
        return False
    return t1.val == t2.val and is_same_tree(t1.left, t2.left) and is_same_tree(t1.right, t2.right)


def is_subtree(s, t):
    """Check if t is subtree of s."""
    if not s:
        return False
    if is_same_tree(s, t):
        return True
    return is_subtree(s.left, t) or is_subtree(s.right, t)


# Modification operations
def mirror(root):
    """Mirror/flip tree (swap left and right children)."""
    if not root:
        return None
    root.left, root.right = root.right, root.left
    mirror(root.left)
    mirror(root.right)
    return root


def invert(root):
    """Alias for mirror."""
    return mirror(root)


def clone(root):
    """Create deep copy of tree."""
    if not root:
        return None
    return TreeNode(root.val, clone(root.left), clone(root.right))


def map_values(root, func):
    """Apply function to all node values, returning new tree."""
    if not root:
        return None
    return TreeNode(func(root.val), map_values(root.left, func), map_values(root.right, func))


def filter_nodes(root, predicate):
    """Filter tree nodes, removing those that don't satisfy predicate."""
    if not root:
        return None
    
    root.left = filter_nodes(root.left, predicate)
    root.right = filter_nodes(root.right, predicate)
    
    if predicate(root.val):
        return root
    
    return root.left or root.right


def insert_level_order(root, val):
    """Insert value at first available position in level order."""
    new_node = TreeNode(val)
    
    if not root:
        return new_node
    
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        
        if not node.left:
            node.left = new_node
            return root
        else:
            queue.append(node.left)
        
        if not node.right:
            node.right = new_node
            return root
        else:
            queue.append(node.right)
    
    return root


def delete_node(root, val):
    """Delete node with given value."""
    if not root:
        return None
    
    if root.val == val:
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        
        min_larger = root.right
        while min_larger.left:
            min_larger = min_larger.left
        root.val = min_larger.val
        root.right = delete_node(root.right, min_larger.val)
    else:
        root.left = delete_node(root.left, val)
        root.right = delete_node(root.right, val)
    
    return root


# Path and diameter operations
def diameter(root):
    """Calculate tree diameter (longest path between any two nodes)."""
    diameter_max = [0]
    
    def depth(node):
        if not node:
            return 0
        left = depth(node.left)
        right = depth(node.right)
        diameter_max[0] = max(diameter_max[0], left + right)
        return 1 + max(left, right)
    
    depth(root)
    return diameter_max[0]


def all_paths(root):
    """Find all root-to-leaf paths."""
    result = []
    
    def dfs(node, path):
        if not node:
            return
        path.append(node.val)
        if not node.left and not node.right:
            result.append(path[:])
        else:
            dfs(node.left, path)
            dfs(node.right, path)
        path.pop()
    
    dfs(root, [])
    return result


def path_sum(root, target):
    """Check if there's a root-to-leaf path with sum equal to target."""
    if not root:
        return False
    if not root.left and not root.right:
        return root.val == target
    return path_sum(root.left, target - root.val) or path_sum(root.right, target - root.val)


def max_path_sum(root):
    """Find maximum path sum (any node to any node)."""
    max_sum = [float('-inf')]
    
    def dfs(node):
        if not node:
            return 0
        left = max(dfs(node.left), 0)
        right = max(dfs(node.right), 0)
        max_sum[0] = max(max_sum[0], node.val + left + right)
        return node.val + max(left, right)
    
    dfs(root)
    return int(max_sum[0])


# Serialization
def serialize(root):
    """Serialize tree to string (preorder with markers)."""
    if not root:
        return "#"
    return "{},{},{}".format(root.val, serialize(root.left), serialize(root.right))


def deserialize(data):
    """Deserialize string back to tree."""
    def build(values):
        val = values.pop(0)
        if val == "#":
            return None
        node = TreeNode(int(val))
        node.left = build(values)
        node.right = build(values)
        return node
    
    return build(data.split(","))


# Utility
def pretty_print(root):
    """Create visual representation of tree."""
    if not root:
        return "(empty)"
    
    lines = []
    queue = deque([(root, 0)])
    level_map = {0: [str(root.val)]}
    
    while queue:
        node, level = queue.popleft()
        
        for child in (node.left, node.right):
            if child:
                child_level = level + 1
                level_map.setdefault(child_level, []).append(str(child.val))
                queue.append((child, child_level))
    
    max_level = max(level_map.keys())
    
    for lvl in range(max_level + 1):
        nodes = level_map.get(lvl, [])
        indent = " " * (2 ** (max_level - lvl) - 1)
        spacing = " " * (2 ** (max_level - lvl + 1) - 1)
        lines.append(spacing.join(nodes) if lvl == 0 else indent + spacing.join(nodes))
    
    return "\n".join(lines)