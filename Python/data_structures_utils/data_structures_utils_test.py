#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Data Structures Utilities Module Tests
====================================================
Comprehensive test suite for the data structures utilities module.

Run with: python data_structures_utils_test.py
"""

import sys
import unittest
from typing import List

# Import the module under test
from mod import (
    Stack, Queue, PriorityQueue, CircularQueue,
    LinkedList, DoublyLinkedList,
    BinarySearchTree,
    HashTable,
    Graph,
    MinHeap, MaxHeap,
    Trie,
    is_balanced_brackets, evaluate_postfix, infix_to_postfix,
    merge_sorted_lists, find_kth_largest, top_k_frequent
)


# ============================================================================
# Stack Tests
# ============================================================================

class TestStack(unittest.TestCase):
    """Test cases for Stack class."""
    
    def test_push_and_pop(self):
        """Test basic push and pop operations."""
        stack = Stack[int]()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        
        self.assertEqual(stack.pop(), 3)
        self.assertEqual(stack.pop(), 2)
        self.assertEqual(stack.pop(), 1)
    
    def test_peek(self):
        """Test peek operation."""
        stack = Stack[str]()
        stack.push("hello")
        stack.push("world")
        
        self.assertEqual(stack.peek(), "world")
        self.assertEqual(stack.peek(), "world")  # Should not remove
        self.assertEqual(stack.size(), 2)
    
    def test_is_empty(self):
        """Test is_empty method."""
        stack = Stack[int]()
        self.assertTrue(stack.is_empty())
        
        stack.push(1)
        self.assertFalse(stack.is_empty())
        
        stack.pop()
        self.assertTrue(stack.is_empty())
    
    def test_size(self):
        """Test size method."""
        stack = Stack[int]()
        self.assertEqual(stack.size(), 0)
        
        stack.push(1)
        stack.push(2)
        self.assertEqual(stack.size(), 2)
    
    def test_clear(self):
        """Test clear method."""
        stack = Stack[int]()
        stack.push(1)
        stack.push(2)
        stack.clear()
        
        self.assertTrue(stack.is_empty())
        self.assertEqual(stack.size(), 0)
    
    def test_pop_empty_raises(self):
        """Test that popping from empty stack raises IndexError."""
        stack = Stack[int]()
        with self.assertRaises(IndexError):
            stack.pop()
    
    def test_peek_empty_raises(self):
        """Test that peeking from empty stack raises IndexError."""
        stack = Stack[int]()
        with self.assertRaises(IndexError):
            stack.peek()
    
    def test_to_list(self):
        """Test to_list method."""
        stack = Stack[int]()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        
        self.assertEqual(stack.to_list(), [1, 2, 3])
    
    def test_len(self):
        """Test __len__ method."""
        stack = Stack[int]()
        stack.push(1)
        stack.push(2)
        
        self.assertEqual(len(stack), 2)


# ============================================================================
# Queue Tests
# ============================================================================

class TestQueue(unittest.TestCase):
    """Test cases for Queue class."""
    
    def test_enqueue_and_dequeue(self):
        """Test basic enqueue and dequeue operations."""
        queue = Queue[int]()
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        
        self.assertEqual(queue.dequeue(), 1)
        self.assertEqual(queue.dequeue(), 2)
        self.assertEqual(queue.dequeue(), 3)
    
    def test_front_and_back(self):
        """Test front and back methods."""
        queue = Queue[str]()
        queue.enqueue("first")
        queue.enqueue("last")
        
        self.assertEqual(queue.front(), "first")
        self.assertEqual(queue.back(), "last")
    
    def test_is_empty(self):
        """Test is_empty method."""
        queue = Queue[int]()
        self.assertTrue(queue.is_empty())
        
        queue.enqueue(1)
        self.assertFalse(queue.is_empty())
    
    def test_clear(self):
        """Test clear method."""
        queue = Queue[int]()
        queue.enqueue(1)
        queue.enqueue(2)
        queue.clear()
        
        self.assertTrue(queue.is_empty())
    
    def test_dequeue_empty_raises(self):
        """Test that dequeuing from empty queue raises IndexError."""
        queue = Queue[int]()
        with self.assertRaises(IndexError):
            queue.dequeue()


# ============================================================================
# PriorityQueue Tests
# ============================================================================

class TestPriorityQueue(unittest.TestCase):
    """Test cases for PriorityQueue class."""
    
    def test_priority_ordering(self):
        """Test that items are returned in priority order."""
        pq = PriorityQueue[str]()
        pq.push(3, "low")
        pq.push(1, "high")
        pq.push(2, "medium")
        
        self.assertEqual(pq.pop(), "high")
        self.assertEqual(pq.pop(), "medium")
        self.assertEqual(pq.pop(), "low")
    
    def test_same_priority_fifo(self):
        """Test FIFO ordering for same priority."""
        pq = PriorityQueue[str]()
        pq.push(1, "first")
        pq.push(1, "second")
        pq.push(1, "third")
        
        self.assertEqual(pq.pop(), "first")
        self.assertEqual(pq.pop(), "second")
        self.assertEqual(pq.pop(), "third")
    
    def test_is_empty(self):
        """Test is_empty method."""
        pq = PriorityQueue[int]()
        self.assertTrue(pq.is_empty())
        
        pq.push(1, "item")
        self.assertFalse(pq.is_empty())


# ============================================================================
# CircularQueue Tests
# ============================================================================

class TestCircularQueue(unittest.TestCase):
    """Test cases for CircularQueue class."""
    
    def test_basic_operations(self):
        """Test basic enqueue and dequeue."""
        cq = CircularQueue[int](3)
        cq.enqueue(1)
        cq.enqueue(2)
        cq.enqueue(3)
        
        self.assertEqual(cq.dequeue(), 1)
        self.assertEqual(cq.dequeue(), 2)
    
    def test_wrap_around(self):
        """Test that queue wraps around correctly."""
        cq = CircularQueue[int](3)
        cq.enqueue(1)
        cq.enqueue(2)
        cq.dequeue()
        cq.enqueue(3)
        cq.enqueue(4)
        
        self.assertEqual(cq.dequeue(), 2)
        self.assertEqual(cq.dequeue(), 3)
        self.assertEqual(cq.dequeue(), 4)
    
    def test_is_full(self):
        """Test is_full method."""
        cq = CircularQueue[int](2)
        self.assertFalse(cq.is_full())
        
        cq.enqueue(1)
        cq.enqueue(2)
        self.assertTrue(cq.is_full())
    
    def test_enqueue_full_returns_false(self):
        """Test that enqueue returns False when full."""
        cq = CircularQueue[int](2)
        cq.enqueue(1)
        cq.enqueue(2)
        
        self.assertFalse(cq.enqueue(3))
    
    def test_capacity(self):
        """Test capacity method."""
        cq = CircularQueue[int](5)
        self.assertEqual(cq.capacity(), 5)
    
    def test_invalid_capacity(self):
        """Test that invalid capacity raises ValueError."""
        with self.assertRaises(ValueError):
            CircularQueue[int](0)


# ============================================================================
# LinkedList Tests
# ============================================================================

class TestLinkedList(unittest.TestCase):
    """Test cases for LinkedList class."""
    
    def test_append(self):
        """Test append operation."""
        ll = LinkedList[int]()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        
        self.assertEqual(ll.to_list(), [1, 2, 3])
    
    def test_prepend(self):
        """Test prepend operation."""
        ll = LinkedList[int]()
        ll.prepend(3)
        ll.prepend(2)
        ll.prepend(1)
        
        self.assertEqual(ll.to_list(), [1, 2, 3])
    
    def test_insert(self):
        """Test insert operation."""
        ll = LinkedList[int]()
        ll.append(1)
        ll.append(3)
        ll.insert(1, 2)
        
        self.assertEqual(ll.to_list(), [1, 2, 3])
    
    def test_remove(self):
        """Test remove operation."""
        ll = LinkedList[int]()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        
        self.assertTrue(ll.remove(2))
        self.assertEqual(ll.to_list(), [1, 3])
        
        self.assertFalse(ll.remove(5))
    
    def test_remove_at(self):
        """Test remove_at operation."""
        ll = LinkedList[int]()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        
        self.assertEqual(ll.remove_at(1), 2)
        self.assertEqual(ll.to_list(), [1, 3])
    
    def test_get_and_set(self):
        """Test get and set operations."""
        ll = LinkedList[int]()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        
        self.assertEqual(ll.get(1), 2)
        
        ll.set(1, 5)
        self.assertEqual(ll.get(1), 5)
    
    def test_find(self):
        """Test find operation."""
        ll = LinkedList[int]()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        
        self.assertEqual(ll.find(2), 1)
        self.assertEqual(ll.find(5), -1)
    
    def test_reverse(self):
        """Test reverse operation."""
        ll = LinkedList[int]()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        
        ll.reverse()
        self.assertEqual(ll.to_list(), [3, 2, 1])
    
    def test_iteration(self):
        """Test iteration."""
        ll = LinkedList[int]()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        
        self.assertEqual(list(ll), [1, 2, 3])
    
    def test_get_out_of_range(self):
        """Test that get with out of range index raises IndexError."""
        ll = LinkedList[int]()
        ll.append(1)
        
        with self.assertRaises(IndexError):
            ll.get(5)


# ============================================================================
# DoublyLinkedList Tests
# ============================================================================

class TestDoublyLinkedList(unittest.TestCase):
    """Test cases for DoublyLinkedList class."""
    
    def test_append_and_prepend(self):
        """Test append and prepend operations."""
        dll = DoublyLinkedList[int]()
        dll.append(1)
        dll.append(2)
        dll.prepend(0)
        
        self.assertEqual(dll.to_list(), [0, 1, 2])
    
    def test_remove(self):
        """Test remove operation."""
        dll = DoublyLinkedList[int]()
        dll.append(1)
        dll.append(2)
        dll.append(3)
        
        self.assertTrue(dll.remove(2))
        self.assertEqual(dll.to_list(), [1, 3])
    
    def test_iteration(self):
        """Test iteration."""
        dll = DoublyLinkedList[int]()
        dll.append(1)
        dll.append(2)
        
        self.assertEqual(list(dll), [1, 2])


# ============================================================================
# BinarySearchTree Tests
# ============================================================================

class TestBinarySearchTree(unittest.TestCase):
    """Test cases for BinarySearchTree class."""
    
    def test_insert_and_search(self):
        """Test insert and search operations."""
        bst = BinarySearchTree[int]()
        bst.insert(5)
        bst.insert(3)
        bst.insert(7)
        bst.insert(1)
        
        self.assertTrue(bst.search(5))
        self.assertTrue(bst.search(3))
        self.assertTrue(bst.search(7))
        self.assertTrue(bst.search(1))
        self.assertFalse(bst.search(4))
    
    def test_inorder_traversal(self):
        """Test inorder traversal returns sorted order."""
        bst = BinarySearchTree[int]()
        bst.insert(5)
        bst.insert(3)
        bst.insert(7)
        bst.insert(1)
        bst.insert(4)
        
        self.assertEqual(bst.inorder(), [1, 3, 4, 5, 7])
    
    def test_preorder_traversal(self):
        """Test preorder traversal."""
        bst = BinarySearchTree[int]()
        bst.insert(5)
        bst.insert(3)
        bst.insert(7)
        
        self.assertEqual(bst.preorder(), [5, 3, 7])
    
    def test_postorder_traversal(self):
        """Test postorder traversal."""
        bst = BinarySearchTree[int]()
        bst.insert(5)
        bst.insert(3)
        bst.insert(7)
        
        self.assertEqual(bst.postorder(), [3, 7, 5])
    
    def test_remove(self):
        """Test remove operation."""
        bst = BinarySearchTree[int]()
        bst.insert(5)
        bst.insert(3)
        bst.insert(7)
        
        self.assertTrue(bst.remove(3))
        self.assertFalse(bst.search(3))
        self.assertTrue(bst.search(5))
        self.assertTrue(bst.search(7))
    
    def test_height(self):
        """Test height calculation."""
        bst = BinarySearchTree[int]()
        self.assertEqual(bst.height(), -1)
        
        bst.insert(5)
        self.assertEqual(bst.height(), 0)
        
        bst.insert(3)
        bst.insert(7)
        self.assertEqual(bst.height(), 1)
    
    def test_remove_leaf(self):
        """Test removing a leaf node."""
        bst = BinarySearchTree[int]()
        bst.insert(10)
        bst.insert(5)
        bst.insert(15)
        
        bst.remove(5)
        self.assertFalse(bst.search(5))
        self.assertEqual(bst.inorder(), [10, 15])
    
    def test_remove_node_with_one_child(self):
        """Test removing a node with one child."""
        bst = BinarySearchTree[int]()
        bst.insert(10)
        bst.insert(5)
        bst.insert(3)
        
        bst.remove(5)
        self.assertEqual(bst.inorder(), [3, 10])
    
    def test_remove_node_with_two_children(self):
        """Test removing a node with two children."""
        bst = BinarySearchTree[int]()
        bst.insert(10)
        bst.insert(5)
        bst.insert(15)
        bst.insert(3)
        bst.insert(7)
        
        bst.remove(10)
        self.assertFalse(bst.search(10))
        self.assertEqual(bst.inorder(), [3, 5, 7, 15])


# ============================================================================
# HashTable Tests
# ============================================================================

class TestHashTable(unittest.TestCase):
    """Test cases for HashTable class."""
    
    def test_put_and_get(self):
        """Test basic put and get operations."""
        ht = HashTable[str]()
        ht.put("name", "Alice")
        ht.put("age", "30")
        
        self.assertEqual(ht.get("name"), "Alice")
        self.assertEqual(ht.get("age"), "30")
    
    def test_update(self):
        """Test updating existing key."""
        ht = HashTable[str]()
        ht.put("name", "Alice")
        ht.put("name", "Bob")
        
        self.assertEqual(ht.get("name"), "Bob")
    
    def test_remove(self):
        """Test remove operation."""
        ht = HashTable[str]()
        ht.put("name", "Alice")
        
        self.assertTrue(ht.remove("name"))
        self.assertIsNone(ht.get("name"))
        
        self.assertFalse(ht.remove("nonexistent"))
    
    def test_contains(self):
        """Test contains method."""
        ht = HashTable[str]()
        ht.put("key", "value")
        
        self.assertTrue(ht.contains("key"))
        self.assertFalse(ht.contains("other"))
    
    def test_keys_values_items(self):
        """Test keys, values, and items methods."""
        ht = HashTable[str]()
        ht.put("a", "1")
        ht.put("b", "2")
        
        self.assertIn("a", ht.keys())
        self.assertIn("b", ht.keys())
        self.assertIn("1", ht.values())
        self.assertIn("2", ht.values())
        
        items = ht.items()
        self.assertIn(("a", "1"), items)
        self.assertIn(("b", "2"), items)
    
    def test_getitem_setitem(self):
        """Test __getitem__ and __setitem__."""
        ht = HashTable[str]()
        ht["name"] = "Alice"
        
        self.assertEqual(ht["name"], "Alice")
    
    def test_contains_operator(self):
        """Test __contains__ operator."""
        ht = HashTable[str]()
        ht.put("key", "value")
        
        self.assertIn("key", ht)
        self.assertNotIn("other", ht)
    
    def test_resize(self):
        """Test automatic resizing."""
        ht = HashTable[str](capacity=2)
        
        for i in range(10):
            ht.put(f"key{i}", f"value{i}")
        
        self.assertEqual(ht.size(), 10)
        self.assertGreater(ht.capacity(), 2)
    
    def test_default_value(self):
        """Test get with default value."""
        ht = HashTable[str]()
        
        self.assertEqual(ht.get("nonexistent", "default"), "default")


# ============================================================================
# Graph Tests
# ============================================================================

class TestGraph(unittest.TestCase):
    """Test cases for Graph class."""
    
    def test_add_edge_undirected(self):
        """Test adding edges in undirected graph."""
        g = Graph(directed=False)
        g.add_edge("A", "B")
        
        self.assertIn("B", g.neighbors("A"))
        self.assertIn("A", g.neighbors("B"))
    
    def test_add_edge_directed(self):
        """Test adding edges in directed graph."""
        g = Graph(directed=True)
        g.add_edge("A", "B")
        
        self.assertIn("B", g.neighbors("A"))
        self.assertNotIn("A", g.neighbors("B"))
    
    def test_bfs(self):
        """Test breadth-first search."""
        g = Graph(directed=False)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.add_edge("B", "D")
        g.add_edge("C", "E")
        
        result = g.bfs("A")
        self.assertEqual(result[0], "A")
        self.assertIn("B", result)
        self.assertIn("C", result)
        self.assertIn("D", result)
        self.assertIn("E", result)
    
    def test_dfs(self):
        """Test depth-first search."""
        g = Graph(directed=False)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.add_edge("B", "D")
        
        result = g.dfs("A")
        self.assertEqual(result[0], "A")
        self.assertIn("B", result)
        self.assertIn("D", result)
    
    def test_has_edge(self):
        """Test has_edge method."""
        g = Graph(directed=False)
        g.add_edge("A", "B")
        
        self.assertTrue(g.has_edge("A", "B"))
        self.assertTrue(g.has_edge("B", "A"))
        self.assertFalse(g.has_edge("A", "C"))
    
    def test_num_vertices_edges(self):
        """Test vertex and edge counting."""
        g = Graph(directed=False)
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        g.add_edge("C", "A")
        
        self.assertEqual(g.num_vertices(), 3)
        self.assertEqual(g.num_edges(), 3)
    
    def test_remove_edge(self):
        """Test remove_edge method."""
        g = Graph(directed=False)
        g.add_edge("A", "B")
        
        self.assertTrue(g.remove_edge("A", "B"))
        self.assertFalse(g.has_edge("A", "B"))


# ============================================================================
# Heap Tests
# ============================================================================

class TestMinHeap(unittest.TestCase):
    """Test cases for MinHeap class."""
    
    def test_push_and_pop(self):
        """Test basic push and pop operations."""
        heap = MinHeap[int]()
        heap.push(3)
        heap.push(1)
        heap.push(2)
        
        self.assertEqual(heap.pop(), 1)
        self.assertEqual(heap.pop(), 2)
        self.assertEqual(heap.pop(), 3)
    
    def test_peek(self):
        """Test peek operation."""
        heap = MinHeap[int]()
        heap.push(5)
        heap.push(3)
        heap.push(7)
        
        self.assertEqual(heap.peek(), 3)
        self.assertEqual(heap.peek(), 3)  # Should not remove
    
    def test_to_list(self):
        """Test to_list returns sorted list."""
        heap = MinHeap[int]()
        heap.push(5)
        heap.push(2)
        heap.push(8)
        
        self.assertEqual(heap.to_list(), [2, 5, 8])


class TestMaxHeap(unittest.TestCase):
    """Test cases for MaxHeap class."""
    
    def test_push_and_pop(self):
        """Test basic push and pop operations."""
        heap = MaxHeap[int]()
        heap.push(1)
        heap.push(3)
        heap.push(2)
        
        self.assertEqual(heap.pop(), 3)
        self.assertEqual(heap.pop(), 2)
        self.assertEqual(heap.pop(), 1)
    
    def test_peek(self):
        """Test peek operation."""
        heap = MaxHeap[int]()
        heap.push(1)
        heap.push(5)
        heap.push(3)
        
        self.assertEqual(heap.peek(), 5)


# ============================================================================
# Trie Tests
# ============================================================================

class TestTrie(unittest.TestCase):
    """Test cases for Trie class."""
    
    def test_insert_and_search(self):
        """Test basic insert and search."""
        trie = Trie()
        trie.insert("apple")
        trie.insert("app")
        
        self.assertTrue(trie.search("apple"))
        self.assertTrue(trie.search("app"))
        self.assertFalse(trie.search("appl"))
    
    def test_starts_with(self):
        """Test prefix search."""
        trie = Trie()
        trie.insert("apple")
        trie.insert("app")
        trie.insert("application")
        
        self.assertTrue(trie.starts_with("ap"))
        self.assertTrue(trie.starts_with("app"))
        self.assertTrue(trie.starts_with("appl"))
        self.assertFalse(trie.starts_with("b"))
    
    def test_remove(self):
        """Test remove operation."""
        trie = Trie()
        trie.insert("hello")
        trie.insert("hell")
        
        self.assertTrue(trie.remove("hell"))
        self.assertFalse(trie.search("hell"))
        self.assertTrue(trie.search("hello"))
    
    def test_find_words_with_prefix(self):
        """Test finding words with a given prefix."""
        trie = Trie()
        trie.insert("cat")
        trie.insert("car")
        trie.insert("card")
        trie.insert("dog")
        
        words = trie.find_words_with_prefix("ca", max_results=10)
        self.assertIn("cat", words)
        self.assertIn("car", words)
        self.assertIn("card", words)
        self.assertNotIn("dog", words)
    
    def test_max_results(self):
        """Test max_results limit."""
        trie = Trie()
        for word in ["apple", "app", "application", "apply", "apricot"]:
            trie.insert(word)
        
        words = trie.find_words_with_prefix("ap", max_results=3)
        self.assertLessEqual(len(words), 3)


# ============================================================================
# Utility Functions Tests
# ============================================================================

class TestBalancedBrackets(unittest.TestCase):
    """Test cases for is_balanced_brackets function."""
    
    def test_balanced(self):
        """Test balanced bracket strings."""
        self.assertTrue(is_balanced_brackets("()"))
        self.assertTrue(is_balanced_brackets("([])"))
        self.assertTrue(is_balanced_brackets("([]{})"))
        self.assertTrue(is_balanced_brackets("((()))"))
    
    def test_unbalanced(self):
        """Test unbalanced bracket strings."""
        self.assertFalse(is_balanced_brackets("("))
        self.assertFalse(is_balanced_brackets(")"))
        self.assertFalse(is_balanced_brackets("([)]"))
        self.assertFalse(is_balanced_brackets("(()"))
    
    def test_empty(self):
        """Test empty string."""
        self.assertTrue(is_balanced_brackets(""))


class TestPostfixEvaluation(unittest.TestCase):
    """Test cases for evaluate_postfix function."""
    
    def test_simple_addition(self):
        """Test simple addition."""
        self.assertEqual(evaluate_postfix("3 4 +"), 7.0)
    
    def test_multiplication(self):
        """Test multiplication."""
        self.assertEqual(evaluate_postfix("3 4 *"), 12.0)
    
    def test_complex_expression(self):
        """Test complex expression."""
        # (3 + 4) * 2 = 14
        self.assertEqual(evaluate_postfix("3 4 + 2 *"), 14.0)
    
    def test_standard_expression(self):
        """Test standard RPN expression."""
        # 5 + (1 + 2) * 4 - 3 = 14
        self.assertEqual(evaluate_postfix("5 1 2 + 4 * + 3 -"), 14.0)


class TestInfixToPostfix(unittest.TestCase):
    """Test cases for infix_to_postfix function."""
    
    def test_simple_addition(self):
        """Test simple addition."""
        self.assertEqual(infix_to_postfix("3 + 4"), "3 4 +")
    
    def test_precedence(self):
        """Test operator precedence."""
        # 3 + 4 * 2 -> 3 4 2 * +
        self.assertEqual(infix_to_postfix("3 + 4 * 2"), "3 4 2 * +")
    
    def test_parentheses(self):
        """Test parentheses."""
        # (3 + 4) * 2 -> 3 4 + 2 *
        self.assertEqual(infix_to_postfix("( 3 + 4 ) * 2"), "3 4 + 2 *")


class TestMergeSortedLists(unittest.TestCase):
    """Test cases for merge_sorted_lists function."""
    
    def test_merge_two_lists(self):
        """Test merging two sorted lists."""
        result = merge_sorted_lists([[1, 3, 5], [2, 4, 6]])
        self.assertEqual(result, [1, 2, 3, 4, 5, 6])
    
    def test_merge_multiple_lists(self):
        """Test merging multiple sorted lists."""
        result = merge_sorted_lists([[1, 4, 5], [1, 3, 4], [2, 6]])
        self.assertEqual(result, [1, 1, 2, 3, 4, 4, 5, 6])
    
    def test_empty_lists(self):
        """Test with empty lists."""
        self.assertEqual(merge_sorted_lists([]), [])
        self.assertEqual(merge_sorted_lists([[], []]), [])


class TestKthLargest(unittest.TestCase):
    """Test cases for find_kth_largest function."""
    
    def test_find_second_largest(self):
        """Test finding second largest."""
        result = find_kth_largest([3, 2, 1, 5, 6, 4], 2)
        self.assertEqual(result, 5)
    
    def test_find_largest(self):
        """Test finding largest."""
        result = find_kth_largest([3, 2, 1, 5, 6, 4], 1)
        self.assertEqual(result, 6)
    
    def test_find_smallest(self):
        """Test finding smallest (kth where k = len)."""
        result = find_kth_largest([3, 2, 1, 5, 6, 4], 6)
        self.assertEqual(result, 1)


class TestTopKFrequent(unittest.TestCase):
    """Test cases for top_k_frequent function."""
    
    def test_top_two_frequent(self):
        """Test finding top 2 frequent elements."""
        result = top_k_frequent([1, 1, 1, 2, 2, 3], 2)
        self.assertEqual(result, [1, 2])
    
    def test_top_one_frequent(self):
        """Test finding top 1 frequent element."""
        result = top_k_frequent([1, 1, 2, 2, 3], 1)
        self.assertEqual(result, [1])
    
    def test_all_same_frequency(self):
        """Test when all elements have same frequency."""
        result = top_k_frequent([1, 2, 3], 2)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(x in [1, 2, 3] for x in result))


# ============================================================================
# Test Runner
# ============================================================================

def run_tests():
    """Run all tests and print results."""
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestStack,
        TestQueue,
        TestPriorityQueue,
        TestCircularQueue,
        TestLinkedList,
        TestDoublyLinkedList,
        TestBinarySearchTree,
        TestHashTable,
        TestGraph,
        TestMinHeap,
        TestMaxHeap,
        TestTrie,
        TestBalancedBrackets,
        TestPostfixEvaluation,
        TestInfixToPostfix,
        TestMergeSortedLists,
        TestKthLargest,
        TestTopKFrequent,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
