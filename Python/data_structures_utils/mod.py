#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Data Structures Utilities Module
==============================================
A comprehensive data structures utility module for Python with zero external dependencies.

Features:
    - Stack implementation with common operations
    - Queue implementation (FIFO, priority, circular)
    - Linked List (singly and doubly linked)
    - Binary Search Tree operations
    - Hash Table implementation
    - Graph utilities (adjacency list, BFS, DFS)
    - Heap operations (min-heap, max-heap)
    - Trie (prefix tree) for string operations
    - Utility functions for common data structure operations

Author: AllToolkit Contributors
License: MIT
"""

from typing import Any, Dict, List, Optional, Union, Callable, Tuple, Generic, TypeVar
from collections import deque
import heapq

T = TypeVar('T')


# ============================================================================
# Stack Implementation
# ============================================================================

class Stack(Generic[T]):
    """
    A generic stack implementation (LIFO - Last In First Out).
    
    Example:
        >>> stack = Stack[int]()
        >>> stack.push(1)
        >>> stack.push(2)
        >>> stack.pop()
        2
    """
    
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def push(self, item: T) -> None:
        """Push an item onto the stack."""
        self._items.append(item)
    
    def pop(self) -> T:
        """Remove and return the top item. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()
    
    def peek(self) -> T:
        """Return the top item without removing it. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]
    
    def is_empty(self) -> bool:
        """Check if the stack is empty."""
        return len(self._items) == 0
    
    def size(self) -> int:
        """Return the number of items in the stack."""
        return len(self._items)
    
    def clear(self) -> None:
        """Remove all items from the stack."""
        self._items.clear()
    
    def to_list(self) -> List[T]:
        """Return a copy of the stack as a list."""
        return self._items.copy()
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __repr__(self) -> str:
        return f"Stack({self._items})"


# ============================================================================
# Queue Implementations
# ============================================================================

class Queue(Generic[T]):
    """
    A generic queue implementation (FIFO - First In First Out).
    
    Example:
        >>> queue = Queue[int]()
        >>> queue.enqueue(1)
        >>> queue.enqueue(2)
        >>> queue.dequeue()
        1
    """
    
    def __init__(self) -> None:
        self._items: deque = deque()
    
    def enqueue(self, item: T) -> None:
        """Add an item to the back of the queue."""
        self._items.append(item)
    
    def dequeue(self) -> T:
        """Remove and return the front item. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()
    
    def front(self) -> T:
        """Return the front item without removing it. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("front from empty queue")
        return self._items[0]
    
    def back(self) -> T:
        """Return the back item without removing it. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("back from empty queue")
        return self._items[-1]
    
    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return len(self._items) == 0
    
    def size(self) -> int:
        """Return the number of items in the queue."""
        return len(self._items)
    
    def clear(self) -> None:
        """Remove all items from the queue."""
        self._items.clear()
    
    def to_list(self) -> List[T]:
        """Return a copy of the queue as a list."""
        return list(self._items)
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __repr__(self) -> str:
        return f"Queue({list(self._items)})"


class PriorityQueue(Generic[T]):
    """
    A priority queue implementation using a heap.
    Lower values have higher priority.
    
    Example:
        >>> pq = PriorityQueue[int]()
        >>> pq.push(3, "low")
        >>> pq.push(1, "high")
        >>> pq.pop()
        'high'
    """
    
    def __init__(self) -> None:
        self._heap: List[Tuple[int, int, T]] = []
        self._counter = 0
    
    def push(self, priority: int, item: T) -> None:
        """Push an item with the given priority."""
        heapq.heappush(self._heap, (priority, self._counter, item))
        self._counter += 1
    
    def pop(self) -> T:
        """Remove and return the highest priority item. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("pop from empty priority queue")
        return heapq.heappop(self._heap)[2]
    
    def peek(self) -> T:
        """Return the highest priority item without removing it."""
        if self.is_empty():
            raise IndexError("peek from empty priority queue")
        return self._heap[0][2]
    
    def is_empty(self) -> bool:
        """Check if the priority queue is empty."""
        return len(self._heap) == 0
    
    def size(self) -> int:
        """Return the number of items in the priority queue."""
        return len(self._heap)
    
    def clear(self) -> None:
        """Remove all items from the priority queue."""
        self._heap.clear()
        self._counter = 0
    
    def __len__(self) -> int:
        return len(self._heap)
    
    def __repr__(self) -> str:
        return f"PriorityQueue(size={len(self._heap)})"


class CircularQueue(Generic[T]):
    """
    A circular queue implementation with fixed capacity.
    
    Example:
        >>> cq = CircularQueue[int](3)
        >>> cq.enqueue(1)
        >>> cq.enqueue(2)
        >>> cq.dequeue()
        1
    """
    
    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self._capacity = capacity
        self._items: List[Optional[T]] = [None] * capacity
        self._front = 0
        self._rear = 0
        self._size = 0
    
    def enqueue(self, item: T) -> bool:
        """Add an item to the queue. Returns False if full."""
        if self.is_full():
            return False
        self._items[self._rear] = item
        self._rear = (self._rear + 1) % self._capacity
        self._size += 1
        return True
    
    def dequeue(self) -> T:
        """Remove and return the front item. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        item = self._items[self._front]
        self._items[self._front] = None
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return item
    
    def front(self) -> T:
        """Return the front item without removing it."""
        if self.is_empty():
            raise IndexError("front from empty queue")
        return self._items[self._front]
    
    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return self._size == 0
    
    def is_full(self) -> bool:
        """Check if the queue is full."""
        return self._size == self._capacity
    
    def size(self) -> int:
        """Return the number of items in the queue."""
        return self._size
    
    def capacity(self) -> int:
        """Return the maximum capacity of the queue."""
        return self._capacity
    
    def clear(self) -> None:
        """Remove all items from the queue."""
        self._items = [None] * self._capacity
        self._front = 0
        self._rear = 0
        self._size = 0
    
    def __len__(self) -> int:
        return self._size
    
    def __repr__(self) -> str:
        return f"CircularQueue(size={self._size}/{self._capacity})"


# ============================================================================
# Linked List Implementations
# ============================================================================

class ListNode(Generic[T]):
    """A node in a singly linked list."""
    
    def __init__(self, value: T, next_node: Optional['ListNode[T]'] = None) -> None:
        self.value = value
        self.next = next_node
    
    def __repr__(self) -> str:
        return f"ListNode({self.value})"


class DoublyListNode(Generic[T]):
    """A node in a doubly linked list."""
    
    def __init__(self, value: T, 
                 prev_node: Optional['DoublyListNode[T]'] = None,
                 next_node: Optional['DoublyListNode[T]'] = None) -> None:
        self.value = value
        self.prev = prev_node
        self.next = next_node
    
    def __repr__(self) -> str:
        return f"DoublyListNode({self.value})"


class LinkedList(Generic[T]):
    """
    A singly linked list implementation.
    
    Example:
        >>> ll = LinkedList[int]()
        >>> ll.append(1)
        >>> ll.append(2)
        >>> ll.prepend(0)
        >>> list(ll)
        [0, 1, 2]
    """
    
    def __init__(self) -> None:
        self._head: Optional[ListNode[T]] = None
        self._size = 0
    
    def append(self, value: T) -> None:
        """Add a node to the end of the list."""
        new_node = ListNode(value)
        if self._head is None:
            self._head = new_node
        else:
            current = self._head
            while current.next:
                current = current.next
            current.next = new_node
        self._size += 1
    
    def prepend(self, value: T) -> None:
        """Add a node to the beginning of the list."""
        new_node = ListNode(value, self._head)
        self._head = new_node
        self._size += 1
    
    def insert(self, index: int, value: T) -> None:
        """Insert a node at the specified index."""
        if index < 0 or index > self._size:
            raise IndexError("index out of range")
        
        if index == 0:
            self.prepend(value)
            return
        
        current = self._head
        for _ in range(index - 1):
            current = current.next
        
        new_node = ListNode(value, current.next)
        current.next = new_node
        self._size += 1
    
    def remove(self, value: T) -> bool:
        """Remove the first occurrence of a value. Returns True if found."""
        if self._head is None:
            return False
        
        if self._head.value == value:
            self._head = self._head.next
            self._size -= 1
            return True
        
        current = self._head
        while current.next:
            if current.next.value == value:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        
        return False
    
    def remove_at(self, index: int) -> T:
        """Remove and return the node at the specified index."""
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")
        
        if index == 0:
            value = self._head.value
            self._head = self._head.next
            self._size -= 1
            return value
        
        current = self._head
        for _ in range(index - 1):
            current = current.next
        
        value = current.next.value
        current.next = current.next.next
        self._size -= 1
        return value
    
    def get(self, index: int) -> T:
        """Get the value at the specified index."""
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")
        
        current = self._head
        for _ in range(index):
            current = current.next
        
        return current.value
    
    def set(self, index: int, value: T) -> None:
        """Set the value at the specified index."""
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")
        
        current = self._head
        for _ in range(index):
            current = current.next
        
        current.value = value
    
    def find(self, value: T) -> int:
        """Find the index of a value. Returns -1 if not found."""
        current = self._head
        index = 0
        
        while current:
            if current.value == value:
                return index
            current = current.next
            index += 1
        
        return -1
    
    def is_empty(self) -> bool:
        """Check if the list is empty."""
        return self._size == 0
    
    def size(self) -> int:
        """Return the number of nodes in the list."""
        return self._size
    
    def clear(self) -> None:
        """Remove all nodes from the list."""
        self._head = None
        self._size = 0
    
    def reverse(self) -> None:
        """Reverse the list in place."""
        prev = None
        current = self._head
        
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        
        self._head = prev
    
    def to_list(self) -> List[T]:
        """Convert the linked list to a Python list."""
        result = []
        current = self._head
        while current:
            result.append(current.value)
            current = current.next
        return result
    
    def __len__(self) -> int:
        return self._size
    
    def __iter__(self):
        current = self._head
        while current:
            yield current.value
            current = current.next
    
    def __repr__(self) -> str:
        return f"LinkedList({self.to_list()})"


class DoublyLinkedList(Generic[T]):
    """
    A doubly linked list implementation.
    
    Example:
        >>> dll = DoublyLinkedList[int]()
        >>> dll.append(1)
        >>> dll.append(2)
        >>> dll.prepend(0)
        >>> list(dll)
        [0, 1, 2]
    """
    
    def __init__(self) -> None:
        self._head: Optional[DoublyListNode[T]] = None
        self._tail: Optional[DoublyListNode[T]] = None
        self._size = 0
    
    def append(self, value: T) -> None:
        """Add a node to the end of the list."""
        new_node = DoublyListNode(value)
        
        if self._head is None:
            self._head = self._tail = new_node
        else:
            new_node.prev = self._tail
            if self._tail:
                self._tail.next = new_node
            self._tail = new_node
        
        self._size += 1
    
    def prepend(self, value: T) -> None:
        """Add a node to the beginning of the list."""
        new_node = DoublyListNode(value, None, self._head)
        
        if self._head is None:
            self._head = self._tail = new_node
        else:
            if self._head:
                self._head.prev = new_node
            self._head = new_node
        
        self._size += 1
    
    def remove(self, value: T) -> bool:
        """Remove the first occurrence of a value. Returns True if found."""
        current = self._head
        
        while current:
            if current.value == value:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self._head = current.next
                
                if current.next:
                    current.next.prev = current.prev
                else:
                    self._tail = current.prev
                
                self._size -= 1
                return True
            
            current = current.next
        
        return False
    
    def is_empty(self) -> bool:
        """Check if the list is empty."""
        return self._size == 0
    
    def size(self) -> int:
        """Return the number of nodes in the list."""
        return self._size
    
    def to_list(self) -> List[T]:
        """Convert the linked list to a Python list."""
        result = []
        current = self._head
        while current:
            result.append(current.value)
            current = current.next
        return result
    
    def __len__(self) -> int:
        return self._size
    
    def __iter__(self):
        current = self._head
        while current:
            yield current.value
            current = current.next
    
    def __repr__(self) -> str:
        return f"DoublyLinkedList({self.to_list()})"


# ============================================================================
# Binary Search Tree
# ============================================================================

class TreeNode(Generic[T]):
    """A node in a binary search tree."""
    
    def __init__(self, value: T) -> None:
        self.value = value
        self.left: Optional['TreeNode[T]'] = None
        self.right: Optional['TreeNode[T]'] = None
    
    def __repr__(self) -> str:
        return f"TreeNode({self.value})"


class BinarySearchTree(Generic[T]):
    """
    A binary search tree implementation.
    
    Example:
        >>> bst = BinarySearchTree[int]()
        >>> bst.insert(5)
        >>> bst.insert(3)
        >>> bst.insert(7)
        >>> bst.search(3)
        True
        >>> bst.search(4)
        False
    """
    
    def __init__(self) -> None:
        self._root: Optional[TreeNode[T]] = None
        self._size = 0
    
    def insert(self, value: T) -> None:
        """Insert a value into the tree."""
        self._root = self._insert_recursive(self._root, value)
        self._size += 1
    
    def _insert_recursive(self, node: Optional[TreeNode[T]], value: T) -> TreeNode[T]:
        if node is None:
            return TreeNode(value)
        
        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        else:
            node.right = self._insert_recursive(node.right, value)
        
        return node
    
    def search(self, value: T) -> bool:
        """Search for a value in the tree."""
        return self._search_recursive(self._root, value) is not None
    
    def _search_recursive(self, node: Optional[TreeNode[T]], value: T) -> Optional[TreeNode[T]]:
        if node is None or node.value == value:
            return node
        
        if value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)
    
    def remove(self, value: T) -> bool:
        """Remove a value from the tree. Returns True if found and removed."""
        if not self.search(value):
            return False
        
        self._root = self._remove_recursive(self._root, value)
        self._size -= 1
        return True
    
    def _remove_recursive(self, node: Optional[TreeNode[T]], value: T) -> Optional[TreeNode[T]]:
        if node is None:
            return None
        
        if value < node.value:
            node.left = self._remove_recursive(node.left, value)
        elif value > node.value:
            node.right = self._remove_recursive(node.right, value)
        else:
            # Node found
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            # Node with two children
            min_value = self._find_min(node.right)
            node.value = min_value
            node.right = self._remove_recursive(node.right, min_value)
        
        return node
    
    def _find_min(self, node: TreeNode[T]) -> T:
        current = node
        while current.left:
            current = current.left
        return current.value
    
    def inorder(self) -> List[T]:
        """Return values in inorder traversal (sorted for BST)."""
        result = []
        self._inorder_recursive(self._root, result)
        return result
    
    def _inorder_recursive(self, node: Optional[TreeNode[T]], result: List[T]) -> None:
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)
    
    def preorder(self) -> List[T]:
        """Return values in preorder traversal."""
        result = []
        self._preorder_recursive(self._root, result)
        return result
    
    def _preorder_recursive(self, node: Optional[TreeNode[T]], result: List[T]) -> None:
        if node:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)
    
    def postorder(self) -> List[T]:
        """Return values in postorder traversal."""
        result = []
        self._postorder_recursive(self._root, result)
        return result
    
    def _postorder_recursive(self, node: Optional[TreeNode[T]], result: List[T]) -> None:
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)
    
    def height(self) -> int:
        """Return the height of the tree."""
        return self._height_recursive(self._root)
    
    def _height_recursive(self, node: Optional[TreeNode[T]]) -> int:
        if node is None:
            return -1
        
        left_height = self._height_recursive(node.left)
        right_height = self._height_recursive(node.right)
        
        return 1 + max(left_height, right_height)
    
    def is_empty(self) -> bool:
        """Check if the tree is empty."""
        return self._root is None
    
    def size(self) -> int:
        """Return the number of nodes in the tree."""
        return self._size
    
    def clear(self) -> None:
        """Remove all nodes from the tree."""
        self._root = None
        self._size = 0
    
    def __len__(self) -> int:
        return self._size
    
    def __repr__(self) -> str:
        return f"BinarySearchTree(inorder={self.inorder()})"


# ============================================================================
# Hash Table
# ============================================================================

class HashTable(Generic[T]):
    """
    A hash table implementation with chaining for collision resolution.
    
    Example:
        >>> ht = HashTable[str]()
        >>> ht.put("name", "Alice")
        >>> ht.get("name")
        'Alice'
        >>> ht.remove("name")
    """
    
    def __init__(self, capacity: int = 16) -> None:
        self._capacity = capacity
        self._buckets: List[List[Tuple[str, T]]] = [[] for _ in range(capacity)]
        self._size = 0
    
    def _hash(self, key: str) -> int:
        """Generate a hash for the given key."""
        return hash(key) % self._capacity
    
    def put(self, key: str, value: T) -> None:
        """Insert or update a key-value pair."""
        index = self._hash(key)
        bucket = self._buckets[index]
        
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        
        bucket.append((key, value))
        self._size += 1
        
        # Resize if load factor too high
        if self._size / self._capacity > 0.75:
            self._resize()
    
    def get(self, key: str, default: Optional[T] = None) -> Optional[T]:
        """Get the value for a key, or default if not found."""
        index = self._hash(key)
        bucket = self._buckets[index]
        
        for k, v in bucket:
            if k == key:
                return v
        
        return default
    
    def remove(self, key: str) -> bool:
        """Remove a key-value pair. Returns True if found."""
        index = self._hash(key)
        bucket = self._buckets[index]
        
        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self._size -= 1
                return True
        
        return False
    
    def contains(self, key: str) -> bool:
        """Check if a key exists in the hash table."""
        index = self._hash(key)
        bucket = self._buckets[index]
        
        return any(k == key for k, _ in bucket)
    
    def keys(self) -> List[str]:
        """Return all keys in the hash table."""
        result = []
        for bucket in self._buckets:
            for k, _ in bucket:
                result.append(k)
        return result
    
    def values(self) -> List[T]:
        """Return all values in the hash table."""
        result = []
        for bucket in self._buckets:
            for _, v in bucket:
                result.append(v)
        return result
    
    def items(self) -> List[Tuple[str, T]]:
        """Return all key-value pairs."""
        result = []
        for bucket in self._buckets:
            result.extend(bucket)
        return result
    
    def _resize(self) -> None:
        """Resize the hash table to double capacity."""
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0
        
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)
    
    def is_empty(self) -> bool:
        """Check if the hash table is empty."""
        return self._size == 0
    
    def size(self) -> int:
        """Return the number of key-value pairs."""
        return self._size
    
    def capacity(self) -> int:
        """Return the current capacity."""
        return self._capacity
    
    def clear(self) -> None:
        """Remove all key-value pairs."""
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0
    
    def __len__(self) -> int:
        return self._size
    
    def __getitem__(self, key: str) -> T:
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value
    
    def __setitem__(self, key: str, value: T) -> None:
        self.put(key, value)
    
    def __delitem__(self, key: str) -> None:
        if not self.remove(key):
            raise KeyError(key)
    
    def __contains__(self, key: str) -> bool:
        return self.contains(key)
    
    def __repr__(self) -> str:
        return f"HashTable({dict(self.items())})"


# ============================================================================
# Graph Utilities
# ============================================================================

class Graph:
    """
    A graph implementation using adjacency list representation.
    Supports both directed and undirected graphs.
    
    Example:
        >>> g = Graph(directed=False)
        >>> g.add_edge("A", "B")
        >>> g.add_edge("B", "C")
        >>> g.neighbors("B")
        ['A', 'C']
    """
    
    def __init__(self, directed: bool = False) -> None:
        self._adjacency: Dict[str, List[str]] = {}
        self._directed = directed
    
    def add_vertex(self, vertex: str) -> None:
        """Add a vertex to the graph."""
        if vertex not in self._adjacency:
            self._adjacency[vertex] = []
    
    def add_edge(self, from_vertex: str, to_vertex: str, weight: Optional[float] = None) -> None:
        """Add an edge between two vertices."""
        self.add_vertex(from_vertex)
        self.add_vertex(to_vertex)
        
        if weight is not None:
            self._adjacency[from_vertex].append((to_vertex, weight))
            if not self._directed:
                self._adjacency[to_vertex].append((from_vertex, weight))
        else:
            if to_vertex not in self._adjacency[from_vertex]:
                self._adjacency[from_vertex].append(to_vertex)
            if not self._directed:
                if from_vertex not in self._adjacency[to_vertex]:
                    self._adjacency[to_vertex].append(from_vertex)
    
    def remove_edge(self, from_vertex: str, to_vertex: str) -> bool:
        """Remove an edge. Returns True if found."""
        if from_vertex not in self._adjacency:
            return False
        
        if to_vertex in self._adjacency[from_vertex]:
            self._adjacency[from_vertex].remove(to_vertex)
            if not self._directed and to_vertex in self._adjacency:
                if from_vertex in self._adjacency[to_vertex]:
                    self._adjacency[to_vertex].remove(from_vertex)
            return True
        
        return False
    
    def neighbors(self, vertex: str) -> List[str]:
        """Return the neighbors of a vertex."""
        return self._adjacency.get(vertex, []).copy()
    
    def has_vertex(self, vertex: str) -> bool:
        """Check if a vertex exists in the graph."""
        return vertex in self._adjacency
    
    def has_edge(self, from_vertex: str, to_vertex: str) -> bool:
        """Check if an edge exists."""
        return to_vertex in self._adjacency.get(from_vertex, [])
    
    def vertices(self) -> List[str]:
        """Return all vertices."""
        return list(self._adjacency.keys())
    
    def edges(self) -> List[Tuple[str, str]]:
        """Return all edges."""
        result = []
        for from_vertex, neighbors in self._adjacency.items():
            for to_vertex in neighbors:
                if self._directed or (from_vertex, to_vertex) not in result:
                    result.append((from_vertex, to_vertex))
        return result
    
    def bfs(self, start: str) -> List[str]:
        """Perform breadth-first search from a starting vertex."""
        if start not in self._adjacency:
            return []
        
        visited = set()
        result = []
        queue = deque([start])
        
        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                queue.extend(v for v in self._adjacency[vertex] if v not in visited)
        
        return result
    
    def dfs(self, start: str) -> List[str]:
        """Perform depth-first search from a starting vertex."""
        if start not in self._adjacency:
            return []
        
        visited = set()
        result = []
        
        def dfs_recursive(vertex: str) -> None:
            visited.add(vertex)
            result.append(vertex)
            for neighbor in self._adjacency[vertex]:
                if neighbor not in visited:
                    dfs_recursive(neighbor)
        
        dfs_recursive(start)
        return result
    
    def num_vertices(self) -> int:
        """Return the number of vertices."""
        return len(self._adjacency)
    
    def num_edges(self) -> int:
        """Return the number of edges."""
        total = sum(len(neighbors) for neighbors in self._adjacency.values())
        return total // 2 if not self._directed else total
    
    def clear(self) -> None:
        """Remove all vertices and edges."""
        self._adjacency.clear()
    
    def __repr__(self) -> str:
        return f"Graph(vertices={self.num_vertices()}, edges={self.num_edges()})"


# ============================================================================
# Heap Utilities
# ============================================================================

class MinHeap(Generic[T]):
    """
    A min-heap implementation.
    
    Example:
        >>> heap = MinHeap[int]()
        >>> heap.push(3)
        >>> heap.push(1)
        >>> heap.push(2)
        >>> heap.pop()
        1
    """
    
    def __init__(self) -> None:
        self._heap: List[T] = []
    
    def push(self, item: T) -> None:
        """Push an item onto the heap."""
        heapq.heappush(self._heap, item)
    
    def pop(self) -> T:
        """Remove and return the minimum item. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("pop from empty heap")
        return heapq.heappop(self._heap)
    
    def peek(self) -> T:
        """Return the minimum item without removing it."""
        if self.is_empty():
            raise IndexError("peek from empty heap")
        return self._heap[0]
    
    def is_empty(self) -> bool:
        """Check if the heap is empty."""
        return len(self._heap) == 0
    
    def size(self) -> int:
        """Return the number of items in the heap."""
        return len(self._heap)
    
    def clear(self) -> None:
        """Remove all items from the heap."""
        self._heap.clear()
    
    def to_list(self) -> List[T]:
        """Return a copy of the heap as a sorted list."""
        return sorted(self._heap)
    
    def __len__(self) -> int:
        return len(self._heap)
    
    def __repr__(self) -> str:
        return f"MinHeap({self._heap})"


class MaxHeap(Generic[T]):
    """
    A max-heap implementation.
    
    Example:
        >>> heap = MaxHeap[int]()
        >>> heap.push(1)
        >>> heap.push(3)
        >>> heap.push(2)
        >>> heap.pop()
        3
    """
    
    def __init__(self) -> None:
        self._heap: List[T] = []
    
    def push(self, item: T) -> None:
        """Push an item onto the heap."""
        # Negate for max-heap behavior
        heapq.heappush(self._heap, (-item, item) if isinstance(item, (int, float)) else item)
    
    def pop(self) -> T:
        """Remove and return the maximum item. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("pop from empty heap")
        item = heapq.heappop(self._heap)
        return item[1] if isinstance(item, tuple) else item
    
    def peek(self) -> T:
        """Return the maximum item without removing it."""
        if self.is_empty():
            raise IndexError("peek from empty heap")
        item = self._heap[0]
        return item[1] if isinstance(item, tuple) else item
    
    def is_empty(self) -> bool:
        """Check if the heap is empty."""
        return len(self._heap) == 0
    
    def size(self) -> int:
        """Return the number of items in the heap."""
        return len(self._heap)
    
    def clear(self) -> None:
        """Remove all items from the heap."""
        self._heap.clear()
    
    def __len__(self) -> int:
        return len(self._heap)
    
    def __repr__(self) -> str:
        return f"MaxHeap(size={len(self._heap)})"


# ============================================================================
# Trie (Prefix Tree)
# ============================================================================

class TrieNode:
    """A node in a trie."""
    
    def __init__(self) -> None:
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word = False


class Trie:
    """
    A trie (prefix tree) implementation for efficient string operations.
    
    Example:
        >>> trie = Trie()
        >>> trie.insert("apple")
        >>> trie.insert("app")
        >>> trie.search("apple")
        True
        >>> trie.search("app")
        True
        >>> trie.starts_with("ap")
        True
        >>> trie.starts_with("appl")
        True
        >>> trie.starts_with("b")
        False
    """
    
    def __init__(self) -> None:
        self._root = TrieNode()
        self._size = 0
    
    def insert(self, word: str) -> None:
        """Insert a word into the trie."""
        node = self._root
        
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        if not node.is_end_of_word:
            node.is_end_of_word = True
            self._size += 1
    
    def search(self, word: str) -> bool:
        """Search for a complete word in the trie."""
        node = self._search_node(word)
        return node is not None and node.is_end_of_word
    
    def starts_with(self, prefix: str) -> bool:
        """Check if any word in the trie starts with the given prefix."""
        return self._search_node(prefix) is not None
    
    def _search_node(self, prefix: str) -> Optional[TrieNode]:
        """Search for the node at the end of a prefix."""
        node = self._root
        
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        
        return node
    
    def remove(self, word: str) -> bool:
        """Remove a word from the trie. Returns True if found and removed."""
        if not self.search(word):
            return False
        
        self._remove_recursive(self._root, word, 0)
        self._size -= 1
        return True
    
    def _remove_recursive(self, node: TrieNode, word: str, index: int) -> bool:
        if index == len(word):
            if not node.is_end_of_word:
                return False
            node.is_end_of_word = False
            return len(node.children) == 0
        
        char = word[index]
        if char not in node.children:
            return False
        
        should_delete = self._remove_recursive(node.children[char], word, index + 1)
        
        if should_delete:
            del node.children[char]
            return len(node.children) == 0 and not node.is_end_of_word
        
        return False
    
    def find_words_with_prefix(self, prefix: str, max_results: int = 10) -> List[str]:
        """Find all words that start with the given prefix."""
        node = self._search_node(prefix)
        if node is None:
            return []
        
        results = []
        self._collect_words(node, prefix, results, max_results)
        return results
    
    def _collect_words(self, node: TrieNode, prefix: str, results: List[str], max_results: int) -> None:
        if len(results) >= max_results:
            return
        
        if node.is_end_of_word:
            results.append(prefix)
        
        for char, child in sorted(node.children.items()):
            self._collect_words(child, prefix + char, results, max_results)
    
    def is_empty(self) -> bool:
        """Check if the trie is empty."""
        return self._size == 0
    
    def size(self) -> int:
        """Return the number of words in the trie."""
        return self._size
    
    def clear(self) -> None:
        """Remove all words from the trie."""
        self._root = TrieNode()
        self._size = 0
    
    def __len__(self) -> int:
        return self._size
    
    def __repr__(self) -> str:
        return f"Trie(words={self._size})"


# ============================================================================
# Utility Functions
# ============================================================================

def is_balanced_brackets(s: str) -> bool:
    """
    Check if brackets in a string are balanced.
    Supports (), [], {}.
    
    Example:
        >>> is_balanced_brackets("([]{})")
        True
        >>> is_balanced_brackets("([)]")
        False
    """
    stack = Stack[str]()
    pairs = {')': '(', ']': '[', '}': '{'}
    
    for char in s:
        if char in '([{':
            stack.push(char)
        elif char in ')]}':
            if stack.is_empty() or stack.pop() != pairs[char]:
                return False
    
    return stack.is_empty()


def evaluate_postfix(expression: str) -> float:
    """
    Evaluate a postfix (Reverse Polish Notation) expression.
    
    Example:
        >>> evaluate_postfix("3 4 + 2 *")
        14.0
        >>> evaluate_postfix("5 1 2 + 4 * + 3 -")
        14.0
    """
    stack = Stack[float]()
    tokens = expression.split()
    
    for token in tokens:
        if token.replace('.', '').replace('-', '').isdigit():
            stack.push(float(token))
        else:
            b = stack.pop()
            a = stack.pop()
            
            if token == '+':
                stack.push(a + b)
            elif token == '-':
                stack.push(a - b)
            elif token == '*':
                stack.push(a * b)
            elif token == '/':
                stack.push(a / b)
            elif token == '**':
                stack.push(a ** b)
    
    return stack.pop()


def infix_to_postfix(expression: str) -> str:
    """
    Convert an infix expression to postfix notation.
    
    Example:
        >>> infix_to_postfix("3 + 4 * 2")
        '3 4 2 * +'
    """
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '**': 3}
    stack = Stack[str]()
    output = []
    tokens = expression.replace('(', ' ( ').replace(')', ' ) ').split()
    
    for token in tokens:
        if token.replace('.', '').replace('-', '').isdigit():
            output.append(token)
        elif token == '(':
            stack.push(token)
        elif token == ')':
            while not stack.is_empty() and stack.peek() != '(':
                output.append(stack.pop())
            stack.pop()  # Remove '('
        else:
            while (not stack.is_empty() and 
                   stack.peek() != '(' and
                   precedence.get(stack.peek(), 0) >= precedence.get(token, 0)):
                output.append(stack.pop())
            stack.push(token)
    
    while not stack.is_empty():
        output.append(stack.pop())
    
    return ' '.join(output)


def merge_sorted_lists(lists: List[List[T]]) -> List[T]:
    """
    Merge multiple sorted lists into one sorted list.
    
    Example:
        >>> merge_sorted_lists([[1, 4, 5], [1, 3, 4], [2, 6]])
        [1, 1, 2, 3, 4, 4, 5, 6]
    """
    if not lists:
        return []
    
    heap = MinHeap[Tuple[T, int, int]]()
    result = []
    
    for i, lst in enumerate(lists):
        if lst:
            heap.push((lst[0], i, 0))
    
    while not heap.is_empty():
        value, list_idx, elem_idx = heap.pop()
        result.append(value)
        
        if elem_idx + 1 < len(lists[list_idx]):
            next_value = lists[list_idx][elem_idx + 1]
            heap.push((next_value, list_idx, elem_idx + 1))
    
    return result


def find_kth_largest(nums: List[T], k: int) -> T:
    """
    Find the kth largest element in a list.
    
    Example:
        >>> find_kth_largest([3, 2, 1, 5, 6, 4], 2)
        5
    """
    heap = MinHeap[T]()
    
    for num in nums:
        heap.push(num)
        if heap.size() > k:
            heap.pop()
    
    return heap.peek()


def top_k_frequent(elements: List[T], k: int) -> List[T]:
    """
    Find the k most frequent elements in a list.
    
    Example:
        >>> top_k_frequent([1, 1, 1, 2, 2, 3], 2)
        [1, 2]
    """
    from collections import Counter
    
    freq = Counter(elements)
    # Use a list and sort by frequency (descending)
    sorted_items = sorted(freq.items(), key=lambda x: -x[1])
    
    return [item[0] for item in sorted_items[:k]]
