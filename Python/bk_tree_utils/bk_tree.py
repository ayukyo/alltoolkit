"""
BK-Tree (Burkhard-Keller Tree) Implementation

A BK-Tree is a metric tree specifically designed to disassociate discrete metric spaces.
It's particularly useful for fast approximate string matching and spell checking.

Time Complexity:
- Insert: O(log n) average case
- Search: O(log n) average case for small edit distances
- Space: O(n)

Example:
    >>> tree = BKTree()
    >>> tree.insert("hello")
    >>> tree.insert("hallo")
    >>> tree.insert("help")
    >>> tree.search("hell", max_distance=1)
    ['hello', 'help']
"""

from typing import List, Optional, Set, Callable, Dict, Any
from collections import defaultdict


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculate the Levenshtein (edit) distance between two strings.
    
    The Levenshtein distance is the minimum number of single-character edits
    (insertions, deletions, or substitutions) required to change one word into the other.
    
    Time Complexity: O(m * n) where m, n are the lengths of the strings
    Space Complexity: O(min(m, n)) - using optimized space
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        The edit distance between s1 and s2
        
    Examples:
        >>> levenshtein_distance("kitten", "sitting")
        3
        >>> levenshtein_distance("hello", "hello")
        0
        >>> levenshtein_distance("", "abc")
        3
    """
    # Optimize by using the shorter string for the inner loop
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    
    if len(s2) == 0:
        return len(s1)
    
    # Use only two rows for space optimization
    previous_row = list(range(len(s2) + 1))
    
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # Calculate costs
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


class BKTreeNode:
    """A node in the BK-Tree."""
    
    __slots__ = ['word', 'children']
    
    def __init__(self, word: str):
        """
        Initialize a BK-Tree node.
        
        Args:
            word: The word stored at this node
        """
        self.word = word
        self.children: Dict[int, 'BKTreeNode'] = {}
    
    def __repr__(self) -> str:
        return f"BKTreeNode('{self.word}', children={list(self.children.keys())})"


class BKTree:
    """
    BK-Tree for efficient approximate string matching.
    
    A BK-Tree is a metric tree that organizes words based on their edit distances.
    It allows for fast lookup of words within a given edit distance threshold.
    
    Attributes:
        root: The root node of the tree
        _size: Number of words in the tree
        _distance_func: Function to calculate distance between words
    
    Example:
        >>> tree = BKTree()
        >>> tree.insert("apple")
        >>> tree.insert("apply")
        >>> tree.search("aple", max_distance=1)
        ['apple']
    """
    
    def __init__(self, distance_func: Optional[Callable[[str, str], int]] = None):
        """
        Initialize a BK-Tree.
        
        Args:
            distance_func: Custom distance function. Defaults to Levenshtein distance.
                          Must be a metric (satisfy triangle inequality).
        """
        self.root: Optional[BKTreeNode] = None
        self._size: int = 0
        self._distance_func = distance_func or levenshtein_distance
    
    def insert(self, word: str) -> None:
        """
        Insert a word into the BK-Tree.
        
        Time Complexity: O(log n) average case
        
        Args:
            word: The word to insert
            
        Raises:
            ValueError: If word is empty
            
        Example:
            >>> tree = BKTree()
            >>> tree.insert("hello")
            >>> tree.size()
            1
        """
        if not word:
            raise ValueError("Cannot insert empty word")
        
        if self.root is None:
            self.root = BKTreeNode(word)
            self._size = 1
            return
        
        node = self.root
        while True:
            distance = self._distance_func(word, node.word)
            
            if distance == 0:
                # Word already exists, don't insert duplicate
                return
            
            if distance in node.children:
                node = node.children[distance]
            else:
                node.children[distance] = BKTreeNode(word)
                self._size += 1
                return
    
    def search(self, word: str, max_distance: int = 1) -> List[str]:
        """
        Find all words within the given edit distance.
        
        Time Complexity: O(log n) average case for small distances
                        O(n) worst case
        
        Args:
            word: The word to search for
            max_distance: Maximum edit distance (default: 1)
            
        Returns:
            List of words within the specified distance, sorted by distance
            
        Example:
            >>> tree = BKTree()
            >>> for w in ["hello", "hallo", "help", "shell"]:
            ...     tree.insert(w)
            >>> sorted(tree.search("hell", max_distance=1))
            ['hallo', 'hello', 'help']
        """
        if not word or self.root is None:
            return []
        
        results: List[tuple] = []  # (distance, word) pairs
        
        def _search_recursive(node: BKTreeNode) -> None:
            distance = self._distance_func(word, node.word)
            
            if distance <= max_distance:
                results.append((distance, node.word))
            
            # Calculate the range of child distances to explore
            min_child_dist = max(1, distance - max_distance)
            max_child_dist = distance + max_distance
            
            for child_dist in range(min_child_dist, max_child_dist + 1):
                if child_dist in node.children:
                    _search_recursive(node.children[child_dist])
        
        _search_recursive(self.root)
        
        # Sort by distance, then alphabetically
        results.sort(key=lambda x: (x[0], x[1]))
        return [w for _, w in results]
    
    def find_nearest(self, word: str, max_distance: Optional[int] = None) -> Optional[str]:
        """
        Find the closest word in the tree to the given word.
        
        Args:
            word: The word to search for
            max_distance: Maximum distance to search (default: unlimited)
            
        Returns:
            The closest word, or None if tree is empty or no word within max_distance
            
        Example:
            >>> tree = BKTree()
            >>> for w in ["apple", "banana", "cherry"]:
            ...     tree.insert(w)
            >>> tree.find_nearest("aple")
            'apple'
        """
        if not word or self.root is None:
            return None
        
        best_word: Optional[str] = None
        best_distance: int = float('inf')
        
        def _search_recursive(node: BKTreeNode) -> None:
            nonlocal best_word, best_distance
            
            distance = self._distance_func(word, node.word)
            
            if distance < best_distance:
                best_distance = distance
                best_word = node.word
            
            # If we found an exact match, no need to search further
            if distance == 0:
                return
            
            # If max_distance is set and we've exceeded it, stop
            if max_distance is not None and best_distance == 0:
                return
            
            # Calculate the range of child distances to explore
            min_child_dist = max(1, distance - best_distance)
            max_child_dist = distance + best_distance
            
            for child_dist in range(min_child_dist, max_child_dist + 1):
                if child_dist in node.children:
                    _search_recursive(node.children[child_dist])
        
        _search_recursive(self.root)
        
        if max_distance is not None and best_distance > max_distance:
            return None
        
        return best_word
    
    def contains(self, word: str) -> bool:
        """
        Check if a word exists in the tree.
        
        Args:
            word: The word to check
            
        Returns:
            True if word exists, False otherwise
            
        Example:
            >>> tree = BKTree()
            >>> tree.insert("hello")
            >>> tree.contains("hello")
            True
            >>> tree.contains("hallo")
            False
        """
        if not word or self.root is None:
            return False
        
        node = self.root
        while True:
            distance = self._distance_func(word, node.word)
            
            if distance == 0:
                return True
            
            if distance in node.children:
                node = node.children[distance]
            else:
                return False
    
    def size(self) -> int:
        """
        Return the number of words in the tree.
        
        Returns:
            Number of words
            
        Example:
            >>> tree = BKTree()
            >>> tree.size()
            0
            >>> tree.insert("hello")
            >>> tree.size()
            1
        """
        return self._size
    
    def is_empty(self) -> bool:
        """
        Check if the tree is empty.
        
        Returns:
            True if tree has no words, False otherwise
        """
        return self._size == 0
    
    def clear(self) -> None:
        """
        Remove all words from the tree.
        
        Example:
            >>> tree = BKTree()
            >>> tree.insert("hello")
            >>> tree.clear()
            >>> tree.size()
            0
        """
        self.root = None
        self._size = 0
    
    def get_all_words(self) -> Set[str]:
        """
        Get all words in the tree.
        
        Time Complexity: O(n)
        
        Returns:
            Set of all words in the tree
            
        Example:
            >>> tree = BKTree()
            >>> tree.insert("hello")
            >>> tree.insert("world")
            >>> tree.get_all_words()
            {'hello', 'world'}
        """
        words: Set[str] = set()
        
        def _collect(node: BKTreeNode) -> None:
            words.add(node.word)
            for child in node.children.values():
                _collect(child)
        
        if self.root is not None:
            _collect(self.root)
        
        return words
    
    def get_height(self) -> int:
        """
        Calculate the height of the tree.
        
        Time Complexity: O(n)
        
        Returns:
            Maximum depth of the tree
            
        Example:
            >>> tree = BKTree()
            >>> tree.get_height()
            0
            >>> tree.insert("hello")
            >>> tree.get_height()
            1
        """
        if self.root is None:
            return 0
        
        def _height(node: BKTreeNode) -> int:
            if not node.children:
                return 1
            return 1 + max(_height(child) for child in node.children.values())
        
        return _height(self.root)
    
    def __len__(self) -> int:
        """Return the number of words in the tree."""
        return self._size
    
    def __contains__(self, word: str) -> bool:
        """Check if a word exists in the tree."""
        return self.contains(word)
    
    def __repr__(self) -> str:
        return f"BKTree(size={self._size})"


class SpellChecker:
    """
    A spell checker built on top of BK-Tree.
    
    Provides convenient methods for spell checking and suggestions.
    
    Example:
        >>> checker = SpellChecker(["hello", "world", "python"])
        >>> checker.suggest("pythn", max_suggestions=3)
        ['python']
        >>> checker.is_correct("hello")
        True
    """
    
    def __init__(self, words: Optional[List[str]] = None):
        """
        Initialize spell checker with optional word list.
        
        Args:
            words: Initial list of valid words
        """
        self.tree = BKTree()
        if words:
            for word in words:
                self.tree.insert(word.lower())
    
    def add_word(self, word: str) -> None:
        """Add a word to the dictionary."""
        self.tree.insert(word.lower())
    
    def add_words(self, words: List[str]) -> None:
        """Add multiple words to the dictionary."""
        for word in words:
            self.tree.insert(word.lower())
    
    def is_correct(self, word: str) -> bool:
        """Check if a word is spelled correctly."""
        return self.tree.contains(word.lower())
    
    def suggest(self, word: str, max_distance: int = 2, max_suggestions: int = 5) -> List[str]:
        """
        Get spelling suggestions for a word.
        
        Args:
            word: The misspelled word
            max_distance: Maximum edit distance for suggestions
            max_suggestions: Maximum number of suggestions to return
            
        Returns:
            List of suggested corrections, sorted by distance
        """
        return self.tree.search(word.lower(), max_distance)[:max_suggestions]
    
    def __repr__(self) -> str:
        return f"SpellChecker(words={self.tree.size()})"


# Utility functions for common use cases

def build_tree_from_words(words: List[str]) -> BKTree:
    """
    Build a BK-Tree from a list of words.
    
    Args:
        words: List of words to insert
        
    Returns:
        BKTree containing all words
        
    Example:
        >>> tree = build_tree_from_words(["apple", "banana", "cherry"])
        >>> tree.size()
        3
    """
    tree = BKTree()
    for word in words:
        tree.insert(word)
    return tree


def find_similar_words(word: str, dictionary: List[str], max_distance: int = 1) -> List[str]:
    """
    Find words similar to the given word from a dictionary.
    
    This is a convenience function that builds a temporary tree.
    For repeated queries, build a BKTree once and use its search method.
    
    Args:
        word: The word to find similar words for
        dictionary: List of words to search in
        max_distance: Maximum edit distance
        
    Returns:
        List of similar words
        
    Example:
        >>> find_similar_words("hello", ["hallo", "help", "shell", "world"], max_distance=1)
        ['hallo', 'help']
    """
    tree = build_tree_from_words(dictionary)
    return tree.search(word, max_distance)


if __name__ == "__main__":
    # Demo
    print("BK-Tree Demo")
    print("=" * 50)
    
    # Create tree and insert words
    tree = BKTree()
    words = ["hello", "hallo", "help", "shell", "held", "hero", "helicopter"]
    for w in words:
        tree.insert(w)
    
    print(f"Inserted {tree.size()} words into BK-Tree")
    print(f"Tree height: {tree.get_height()}")
    print()
    
    # Search for similar words
    test_word = "hell"
    results = tree.search(test_word, max_distance=2)
    print(f"Words similar to '{test_word}' (max distance 2): {results}")
    
    # Find nearest
    nearest = tree.find_nearest("helo")
    print(f"Nearest word to 'helo': {nearest}")
    
    # Spell checker demo
    print("\nSpell Checker Demo")
    print("=" * 50)
    
    checker = SpellChecker(["python", "programming", "computer", "algorithm"])
    print(f"Is 'python' correct? {checker.is_correct('python')}")
    print(f"Is 'pythn' correct? {checker.is_correct('pythn')}")
    print(f"Suggestions for 'algorthm': {checker.suggest('algorthm')}")