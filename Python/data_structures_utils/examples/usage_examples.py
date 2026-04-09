#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Data Structures Utils Usage Examples
==================================================
Comprehensive usage examples for the data structures utilities module.

Run with: python usage_examples.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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


def print_section(title: str) -> None:
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


# ============================================================================
# Stack Examples
# ============================================================================

def stack_examples():
    """Demonstrate Stack usage."""
    print_section("Stack (栈) - LIFO")
    
    # Basic operations
    stack = Stack[int]()
    print("\n1. 基本操作:")
    stack.push(10)
    stack.push(20)
    stack.push(30)
    print(f"   压栈后：{stack}")
    print(f"   栈顶元素：{stack.peek()}")
    print(f"   弹出：{stack.pop()}")
    print(f"   弹出后：{stack}")
    
    # Check if empty
    print(f"\n2. 检查空栈：{stack.is_empty()}")
    print(f"   栈大小：{stack.size()}")
    
    # Clear stack
    stack.clear()
    print(f"\n3. 清空后：{stack}")
    print(f"   是否为空：{stack.is_empty()}")


# ============================================================================
# Queue Examples
# ============================================================================

def queue_examples():
    """Demonstrate Queue usage."""
    print_section("Queue (队列) - FIFO")
    
    # Basic operations
    queue = Queue[str]()
    print("\n1. 基本操作:")
    queue.enqueue("第一")
    queue.enqueue("第二")
    queue.enqueue("第三")
    print(f"   入队后：{queue}")
    print(f"   队首：{queue.front()}")
    print(f"   队尾：{queue.back()}")
    print(f"   出队：{queue.dequeue()}")
    print(f"   出队后：{queue}")
    
    # Circular queue
    print("\n2. 循环队列:")
    cq = CircularQueue[int](3)
    cq.enqueue(1)
    cq.enqueue(2)
    cq.enqueue(3)
    print(f"   满队列：{cq}")
    print(f"   是否已满：{cq.is_full()}")
    cq.dequeue()
    cq.enqueue(4)  # 应该可以入队
    print(f"   出队后入队：{cq}")


# ============================================================================
# PriorityQueue Examples
# ============================================================================

def priority_queue_examples():
    """Demonstrate PriorityQueue usage."""
    print_section("PriorityQueue (优先队列)")
    
    pq = PriorityQueue[str]()
    print("\n1. 按优先级出队:")
    pq.push(3, "低优先级任务")
    pq.push(1, "高优先级任务")
    pq.push(2, "中优先级任务")
    
    while not pq.is_empty():
        print(f"   处理：{pq.pop()}")


# ============================================================================
# LinkedList Examples
# ============================================================================

def linked_list_examples():
    """Demonstrate LinkedList usage."""
    print_section("LinkedList (链表)")
    
    # Basic operations
    ll = LinkedList[int]()
    print("\n1. 基本操作:")
    ll.append(1)
    ll.append(2)
    ll.append(3)
    print(f"   追加后：{ll}")
    
    ll.prepend(0)
    print(f"   头部插入后：{ll}")
    
    ll.insert(2, 100)
    print(f"   位置 2 插入 100 后：{ll}")
    
    # Find and remove
    print(f"\n2. 查找和删除:")
    print(f"   查找 100 的位置：{ll.find(100)}")
    ll.remove(100)
    print(f"   删除 100 后：{ll}")
    
    # Reverse
    print(f"\n3. 反转链表:")
    ll.reverse()
    print(f"   反转后：{ll}")
    
    # Convert to list
    print(f"\n4. 转为 Python 列表：{ll.to_list()}")


# ============================================================================
# BinarySearchTree Examples
# ============================================================================

def bst_examples():
    """Demonstrate BinarySearchTree usage."""
    print_section("BinarySearchTree (二叉搜索树)")
    
    bst = BinarySearchTree[int]()
    print("\n1. 插入和遍历:")
    
    # Insert values
    values = [50, 30, 70, 20, 40, 60, 80]
    for v in values:
        bst.insert(v)
    
    print(f"   插入：{values}")
    print(f"   中序遍历（排序）：{bst.inorder()}")
    print(f"   前序遍历：{bst.preorder()}")
    print(f"   后序遍历：{bst.postorder()}")
    
    # Search and remove
    print(f"\n2. 搜索和删除:")
    print(f"   搜索 40: {bst.search(40)}")
    print(f"   搜索 25: {bst.search(25)}")
    
    bst.remove(30)
    print(f"   删除 30 后中序遍历：{bst.inorder()}")
    
    # Height
    print(f"\n3. 树的高度：{bst.height()}")


# ============================================================================
# HashTable Examples
# ============================================================================

def hashtable_examples():
    """Demonstrate HashTable usage."""
    print_section("HashTable (哈希表)")
    
    ht = HashTable[str]()
    print("\n1. 基本操作:")
    
    ht.put("name", "Alice")
    ht.put("age", "30")
    ht.put("city", "Beijing")
    
    print(f"   name: {ht.get('name')}")
    print(f"   age: {ht.get('age')}")
    print(f"   city: {ht.get('city')}")
    
    # Update
    print(f"\n2. 更新值:")
    ht.put("age", "31")
    print(f"   更新后 age: {ht.get('age')}")
    
    # Dictionary-style access
    print(f"\n3. 字典式访问:")
    ht["country"] = "China"
    print(f"   country: {ht['country']}")
    
    # Keys and values
    print(f"\n4. 所有键：{ht.keys()}")
    print(f"   所有值：{ht.values()}")
    
    # Remove
    ht.remove("city")
    print(f"\n5. 删除 city 后：{ht}")


# ============================================================================
# Graph Examples
# ============================================================================

def graph_examples():
    """Demonstrate Graph usage."""
    print_section("Graph (图)")
    
    # Undirected graph
    print("\n1. 无向图:")
    g = Graph(directed=False)
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    g.add_edge("C", "E")
    g.add_edge("D", "E")
    
    print(f"   顶点：{g.vertices()}")
    print(f"   边数：{g.num_edges()}")
    print(f"   A 的邻居：{g.neighbors('A')}")
    
    # BFS and DFS
    print(f"\n2. 图遍历:")
    print(f"   BFS 从 A: {g.bfs('A')}")
    print(f"   DFS 从 A: {g.dfs('A')}")
    
    # Directed graph
    print("\n3. 有向图:")
    dg = Graph(directed=True)
    dg.add_edge("A", "B")
    dg.add_edge("B", "C")
    dg.add_edge("C", "A")
    
    print(f"   A 的邻居：{dg.neighbors('A')}")
    print(f"   B 的邻居：{dg.neighbors('B')}")
    print(f"   C 的邻居：{dg.neighbors('C')}")


# ============================================================================
# Heap Examples
# ============================================================================

def heap_examples():
    """Demonstrate Heap usage."""
    print_section("Heap (堆)")
    
    # Min heap
    print("\n1. 最小堆:")
    min_heap = MinHeap[int]()
    for num in [5, 2, 8, 1, 9, 3]:
        min_heap.push(num)
    
    print(f"   入堆：[5, 2, 8, 1, 9, 3]")
    print(f"   出堆顺序：", end="")
    while not min_heap.is_empty():
        print(min_heap.pop(), end=" ")
    print()
    
    # Max heap
    print("\n2. 最大堆:")
    max_heap = MaxHeap[int]()
    for num in [5, 2, 8, 1, 9, 3]:
        max_heap.push(num)
    
    print(f"   入堆：[5, 2, 8, 1, 9, 3]")
    print(f"   出堆顺序：", end="")
    while not max_heap.is_empty():
        print(max_heap.pop(), end=" ")
    print()


# ============================================================================
# Trie Examples
# ============================================================================

def trie_examples():
    """Demonstrate Trie usage."""
    print_section("Trie (字典树/前缀树)")
    
    trie = Trie()
    print("\n1. 插入和搜索:")
    
    words = ["apple", "app", "application", "apply", "apricot", "banana"]
    for word in words:
        trie.insert(word)
    
    print(f"   插入单词：{words}")
    print(f"   搜索 'apple': {trie.search('apple')}")
    print(f"   搜索 'app': {trie.search('app')}")
    print(f"   搜索 'appl': {trie.search('appl')}")
    
    # Prefix search
    print(f"\n2. 前缀匹配:")
    print(f"   starts_with('ap'): {trie.starts_with('ap')}")
    print(f"   starts_with('b'): {trie.starts_with('b')}")
    print(f"   starts_with('c'): {trie.starts_with('c')}")
    
    # Find words with prefix
    print(f"\n3. 查找前缀匹配的单词:")
    matches = trie.find_words_with_prefix("app", max_results=5)
    print(f"   前缀 'app' 匹配：{matches}")


# ============================================================================
# Utility Functions Examples
# ============================================================================

def utility_examples():
    """Demonstrate utility functions."""
    print_section("Utility Functions (工具函数)")
    
    # Balanced brackets
    print("\n1. 括号平衡检查:")
    test_cases = [
        "([]{})",
        "([)]",
        "((()))",
        "()[]{}"
    ]
    for expr in test_cases:
        result = is_balanced_brackets(expr)
        print(f"   '{expr}': {result}")
    
    # Postfix evaluation
    print("\n2. 后缀表达式求值:")
    expressions = [
        "3 4 +",
        "3 4 + 2 *",
        "5 1 2 + 4 * + 3 -"
    ]
    for expr in expressions:
        result = evaluate_postfix(expr)
        print(f"   '{expr}' = {result}")
    
    # Infix to postfix
    print("\n3. 中缀转后缀:")
    infix_exprs = [
        "3 + 4",
        "3 + 4 * 2",
        "( 3 + 4 ) * 2"
    ]
    for expr in infix_exprs:
        postfix = infix_to_postfix(expr)
        print(f"   '{expr}' -> '{postfix}'")
    
    # Merge sorted lists
    print("\n4. 合并有序列表:")
    lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
    merged = merge_sorted_lists(lists)
    print(f"   输入：{lists}")
    print(f"   合并：{merged}")
    
    # Kth largest
    print("\n5. 第 K 大元素:")
    nums = [3, 2, 1, 5, 6, 4]
    for k in [1, 2, 3]:
        result = find_kth_largest(nums, k)
        print(f"   第{k}大：{result}")
    
    # Top K frequent
    print("\n6. Top K 频繁元素:")
    elements = [1, 1, 1, 2, 2, 3, 3, 3, 3]
    top = top_k_frequent(elements, 2)
    print(f"   输入：{elements}")
    print(f"   Top 2 频繁：{top}")


# ============================================================================
# Practical Examples
# ============================================================================

def practical_examples():
    """Demonstrate practical use cases."""
    print_section("Practical Examples (实际应用)")
    
    # Example 1: Undo/Redo using stacks
    print("\n1. 使用栈实现撤销/重做:")
    
    class TextEditor:
        def __init__(self):
            self.content = ""
            self.undo_stack = Stack[str]()
            self.redo_stack = Stack[str]()
        
        def type(self, text: str):
            self.undo_stack.push(self.content)
            self.content += text
            self.redo_stack.clear()
        
        def undo(self):
            if not self.undo_stack.is_empty():
                self.redo_stack.push(self.content)
                self.content = self.undo_stack.pop()
        
        def redo(self):
            if not self.redo_stack.is_empty():
                self.undo_stack.push(self.content)
                self.content = self.redo_stack.pop()
    
    editor = TextEditor()
    editor.type("Hello")
    editor.type(" World")
    print(f"   输入后：'{editor.content}'")
    editor.undo()
    print(f"   撤销后：'{editor.content}'")
    editor.redo()
    print(f"   重做后：'{editor.content}'")
    
    # Example 2: Auto-complete using Trie
    print("\n2. 使用 Trie 实现自动补全:")
    
    class AutoComplete:
        def __init__(self):
            self.trie = Trie()
        
        def add_word(self, word: str):
            self.trie.insert(word)
        
        def suggest(self, prefix: str):
            return self.trie.find_words_with_prefix(prefix, 5)
    
    ac = AutoComplete()
    words = ["python", "programming", "program", "project", "proton", "java"]
    for w in words:
        ac.add_word(w)
    
    suggestions = ac.suggest("pro")
    print(f"   输入 'pro' 的建议：{suggestions}")
    
    # Example 3: Task scheduler using priority queue
    print("\n3. 使用优先队列实现任务调度:")
    
    scheduler = PriorityQueue[str]()
    tasks = [
        (3, "备份数据"),
        (1, "处理紧急告警"),
        (2, "发送邮件"),
        (1, "数据库维护"),
    ]
    
    for priority, task in tasks:
        scheduler.push(priority, task)
    
    print("   任务执行顺序:")
    while not scheduler.is_empty():
        print(f"      - {scheduler.pop()}")


# ============================================================================
# Main
# ============================================================================

def main():
    """Run all examples."""
    print("\n" + "🗂️" * 30)
    print("  AllToolkit - Data Structures Utils 使用示例")
    print("🗂️" * 30)
    
    stack_examples()
    queue_examples()
    priority_queue_examples()
    linked_list_examples()
    bst_examples()
    hashtable_examples()
    graph_examples()
    heap_examples()
    trie_examples()
    utility_examples()
    practical_examples()
    
    print("\n" + "=" * 60)
    print("  示例运行完成!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
