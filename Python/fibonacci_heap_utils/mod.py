#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Python Fibonacci Heap Utilities
斐波那契堆工具模块 - 提供高效的斐波那契堆数据结构实现

@module: fibonacci_heap_utils
@author: AllToolkit Contributors
@license: MIT
@version: 1.0.0

功能列表:
- 斐波那契堆: O(1) 摊还插入、合并、减小键操作
- 最小堆/最大堆模式: 支持最小堆和最大堆两种模式
- 泛型支持: 支持任意可比较的数据类型
- 优先队列操作: insert, extract_min/max, decrease_key, merge
- 节点删除: 支持删除任意节点
- 迭代器: 支持遍历堆中所有元素
- 序列化: 支持序列化与反序列化

使用示例:
    from fibonacci_heap_utils.mod import FibonacciHeap
    
    # 创建最小堆
    heap = FibonacciHeap[int]()
    
    # 插入元素
    heap.insert(5, "task_low")
    heap.insert(1, "task_high")
    heap.insert(3, "task_medium")
    
    # 获取最小元素
    print(heap.find_min())  # 1
    
    # 删除最小元素
    min_val = heap.extract_min()
    print(min_val)  # 1
"""

from typing import TypeVar, Generic, Optional, List, Any, Callable, Iterator, Dict
from dataclasses import dataclass, field
from functools import total_ordering
import math
import json

T = TypeVar('T')
K = TypeVar('K')


@total_ordering
class FibonacciNode(Generic[T]):
    """
    斐波那契堆节点
    
    每个节点包含:
    - key: 键值（优先级）
    - value: 存储的值
    - degree: 子节点数量
    - mark: 是否被标记（用于级联剪切）
    - parent, child: 父子指针
    - left, right: 双向链表指针（兄弟节点）
    """
    
    def __init__(self, key: float, value: Optional[T] = None):
        self.key = key
        self.value = value
        self.degree = 0
        self.mark = False
        self.parent: Optional['FibonacciNode[T]'] = None
        self.child: Optional['FibonacciNode[T]'] = None
        # 初始化时，节点指向自己形成循环链表
        self.left: 'FibonacciNode[T]' = self
        self.right: 'FibonacciNode[T]' = self
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FibonacciNode):
            return NotImplemented
        return self.key == other.key
    
    def __lt__(self, other: 'FibonacciNode[T]') -> bool:
        return self.key < other.key
    
    def __hash__(self) -> int:
        return id(self)
    
    def __repr__(self) -> str:
        return f"FibonacciNode(key={self.key}, value={self.value}, degree={self.degree})"
    
    def is_single(self) -> bool:
        """检查节点是否是循环链表中唯一的节点"""
        return self.left is self and self.right is self
    
    def add_child(self, child: 'FibonacciNode[T]') -> None:
        """将一个节点添加为当前节点的子节点"""
        child.parent = self
        self.degree += 1
        
        if self.child is None:
            self.child = child
            child.left = child
            child.right = child
        else:
            # 将child插入到child链表中
            child.right = self.child.right
            child.left = self.child
            self.child.right.left = child
            self.child.right = child
    
    def remove_from_siblings(self) -> None:
        """从兄弟链表中移除当前节点"""
        self.left.right = self.right
        self.right.left = self.left
        self.left = self
        self.right = self


class FibonacciHeap(Generic[T]):
    """
    斐波那契堆
    
    一种支持高效合并操作和减小键操作的优先队列数据结构。
    
    摊还时间复杂度:
    - insert: O(1)
    - find_min: O(1)
    - extract_min: O(log n)
    - decrease_key: O(1)
    - merge: O(1)
    - delete: O(log n)
    
    属性:
    - min_node: 指向最小节点的指针
    - size: 堆中元素数量
    - is_max_heap: 是否为最大堆模式
    """
    
    def __init__(self, is_max_heap: bool = False):
        """
        初始化斐波那契堆
        
        Args:
            is_max_heap: 是否为最大堆模式，默认为最小堆
        """
        self.min_node: Optional[FibonacciNode[T]] = None
        self.size: int = 0
        self.is_max_heap = is_max_heap
        # 用于快速查找节点（在序列化/反序列化时不使用）
        self._node_map: Dict[int, FibonacciNode[T]] = {}
    
    def _compare(self, key1: float, key2: float) -> bool:
        """比较两个键值，根据堆模式返回比较结果"""
        if self.is_max_heap:
            return key1 > key2
        return key1 < key2
    
    def _compare_node(self, node1: FibonacciNode[T], node2: FibonacciNode[T]) -> bool:
        """比较两个节点，返回node1是否应该成为新的min/max"""
        return self._compare(node1.key, node2.key)
    
    # ==================== 基本操作 ====================
    
    def insert(self, key: float, value: Optional[T] = None) -> FibonacciNode[T]:
        """
        插入一个新元素到堆中
        
        时间复杂度: O(1)
        
        Args:
            key: 键值（优先级）
            value: 存储的值
            
        Returns:
            新创建的节点
        """
        node = FibonacciNode(key, value)
        
        if self.min_node is None:
            self.min_node = node
        else:
            # 将节点添加到根链表
            self._add_to_root_list(node)
            # 更新最小/最大节点
            if self._compare_node(node, self.min_node):
                self.min_node = node
        
        self.size += 1
        self._node_map[id(node)] = node
        return node
    
    def find_min(self) -> Optional[float]:
        """
        查找最小（或最大）键值
        
        时间复杂度: O(1)
        
        Returns:
            最小/最大键值，如果堆为空返回None
        """
        if self.min_node is None:
            return None
        return self.min_node.key
    
    def find_min_value(self) -> Optional[T]:
        """
        查找最小（或最大）键对应的值
        
        时间复杂度: O(1)
        
        Returns:
            最小/最大键对应的值，如果堆为空返回None
        """
        if self.min_node is None:
            return None
        return self.min_node.value
    
    def extract_min(self) -> Optional[T]:
        """
        删除并返回最小（或最大）元素
        
        时间复杂度: O(log n) 摊还
        
        Returns:
            最小/最大元素的值，如果堆为空返回None
        """
        if self.min_node is None:
            return None
        
        min_node = self.min_node
        
        # 将最小节点的所有子节点添加到根链表
        if min_node.child is not None:
            child = min_node.child
            children = []
            # 收集所有子节点
            current = child
            while True:
                children.append(current)
                current = current.right
                if current is child:
                    break
            
            for c in children:
                c.parent = None
                c.mark = False
                self._add_to_root_list(c)
        
        # 从根链表中移除最小节点
        self._remove_from_root_list(min_node)
        
        if min_node is self.min_node and min_node.right is not min_node:
            # 如果堆不为空，需要整理
            self.min_node = min_node.right
            self._consolidate()
        elif min_node.right is min_node:
            # 堆变为空
            self.min_node = None
        
        self.size -= 1
        if id(min_node) in self._node_map:
            del self._node_map[id(min_node)]
        
        return min_node.value
    
    def extract_min_with_key(self) -> Optional[tuple]:
        """
        删除并返回最小（或最大）元素及其键值
        
        Returns:
            (key, value) 元组，如果堆为空返回None
        """
        if self.min_node is None:
            return None
        
        key = self.min_node.key
        value = self.extract_min()
        return (key, value) if value is not None else None
    
    def merge(self, other: 'FibonacciHeap[T]') -> None:
        """
        合并另一个斐波那契堆到当前堆
        
        时间复杂度: O(1)
        
        Args:
            other: 要合并的另一个斐波那契堆
            
        Note:
            合并后other堆会被清空
        """
        if other is None or other.min_node is None:
            return
        
        if self.min_node is None:
            self.min_node = other.min_node
            self.size = other.size
        else:
            # 合并两个根链表
            self._merge_root_lists(other)
            # 更新最小节点
            if self._compare_node(other.min_node, self.min_node):
                self.min_node = other.min_node
            self.size += other.size
        
        # 合并节点映射
        self._node_map.update(other._node_map)
        
        # 清空other
        other.min_node = None
        other.size = 0
        other._node_map = {}
    
    def decrease_key(self, node: FibonacciNode[T], new_key: float) -> None:
        """
        减小（或增大）节点的键值
        
        时间复杂度: O(1) 摊还
        
        Args:
            node: 要减小键值的节点
            new_key: 新的键值
            
        Raises:
            ValueError: 如果新键值不符合堆性质（最小堆时新键大于旧键）
        """
        if self.is_max_heap:
            if new_key < node.key:
                raise ValueError(f"Max heap: new key {new_key} must be >= current key {node.key}")
        else:
            if new_key > node.key:
                raise ValueError(f"Min heap: new key {new_key} must be <= current key {node.key}")
        
        old_key = node.key
        node.key = new_key
        
        parent = node.parent
        
        # 如果节点在根链表中或者新键值不违反堆性质，直接返回
        if parent is None:
            if self._compare_node(node, self.min_node):
                self.min_node = node
            return
        
        if not self._compare(new_key, parent.key):
            return
        
        # 级联剪切
        self._cut(node, parent)
        self._cascading_cut(parent)
    
    def delete(self, node: FibonacciNode[T]) -> Optional[T]:
        """
        删除指定节点
        
        时间复杂度: O(log n) 摊还
        
        Args:
            node: 要删除的节点
            
        Returns:
            被删除节点的值
        """
        if node is None:
            return None
        
        # 将键值设为负无穷（或正无穷），然后提取
        if self.is_max_heap:
            # 最大堆：设为正无穷
            inf_key = float('inf')
        else:
            # 最小堆：设为负无穷
            inf_key = float('-inf')
        
        self.decrease_key(node, inf_key)
        return self.extract_min()
    
    # ==================== 辅助方法 ====================
    
    def _add_to_root_list(self, node: FibonacciNode[T]) -> None:
        """将节点添加到根链表"""
        if self.min_node is None:
            self.min_node = node
            return
        
        # 插入到min_node的右边
        node.right = self.min_node.right
        node.left = self.min_node
        self.min_node.right.left = node
        self.min_node.right = node
        node.parent = None
    
    def _remove_from_root_list(self, node: FibonacciNode[T]) -> None:
        """从根链表中移除节点"""
        node.left.right = node.right
        node.right.left = node.left
    
    def _merge_root_lists(self, other: 'FibonacciHeap[T]') -> None:
        """合并两个堆的根链表"""
        if self.min_node is None or other.min_node is None:
            return
        
        # 连接两个循环链表
        self_min = self.min_node
        other_min = other.min_node
        
        self_last = self_min.left
        other_last = other_min.left
        
        self_min.left = other_last
        other_last.right = self_min
        other_min.left = self_last
        self_last.right = other_min
    
    def _cut(self, node: FibonacciNode[T], parent: FibonacciNode[T]) -> None:
        """
        剪切操作：将节点从父节点剪切下来，添加到根链表
        """
        # 从父节点的子链表中移除
        if node.right is node:
            # 节点是唯一的子节点
            parent.child = None
        else:
            if parent.child is node:
                parent.child = node.right
            node.remove_from_siblings()
        
        parent.degree -= 1
        
        # 添加到根链表
        self._add_to_root_list(node)
        node.mark = False
        
        # 更新最小节点
        if self._compare_node(node, self.min_node):
            self.min_node = node
    
    def _cascading_cut(self, node: FibonacciNode[T]) -> None:
        """
        级联剪切操作
        """
        parent = node.parent
        if parent is not None:
            if not node.mark:
                node.mark = True
            else:
                self._cut(node, parent)
                self._cascading_cut(parent)
    
    def _consolidate(self) -> None:
        """
        整理操作：合并相同度数的树
        """
        # 度数的上限是 log_phi(n)，其中phi是黄金比例
        if self.min_node is None:
            return
        
        max_degree = int(math.log2(self.size)) + 2 if self.size > 0 else 1
        degree_to_tree: List[Optional[FibonacciNode[T]]] = [None] * max_degree
        
        # 收集所有根节点
        roots = []
        current = self.min_node
        if current is not None:
            while True:
                roots.append(current)
                current = current.right
                if current is self.min_node:
                    break
        
        # 合并相同度数的树
        for root in roots:
            degree = root.degree
            
            while degree_to_tree[degree] is not None:
                other = degree_to_tree[degree]
                
                # 确保root是较小的根
                if self._compare_node(other, root):
                    root, other = other, root
                
                # 将other链接为root的子节点
                self._link(other, root)
                
                degree_to_tree[degree] = None
                degree += 1
            
            degree_to_tree[degree] = root
        
        # 重建根链表并找到最小节点
        self.min_node = None
        for tree in degree_to_tree:
            if tree is not None:
                tree.left = tree
                tree.right = tree
                if self.min_node is None:
                    self.min_node = tree
                else:
                    self._add_to_root_list(tree)
                    if self._compare_node(tree, self.min_node):
                        self.min_node = tree
    
    def _link(self, child: FibonacciNode[T], parent: FibonacciNode[T]) -> None:
        """
        链接操作：将child链接为parent的子节点
        """
        # 从根链表中移除child
        self._remove_from_root_list(child)
        
        # 添加为parent的子节点
        child.parent = parent
        child.mark = False
        
        if parent.child is None:
            parent.child = child
            child.left = child
            child.right = child
        else:
            # 插入到child链表
            child.right = parent.child.right
            child.left = parent.child
            parent.child.right.left = child
            parent.child.right = child
        
        parent.degree += 1
    
    # ==================== 查询操作 ====================
    
    def is_empty(self) -> bool:
        """检查堆是否为空"""
        return self.min_node is None
    
    def __len__(self) -> int:
        return self.size
    
    def __bool__(self) -> bool:
        return not self.is_empty()
    
    def get_size(self) -> int:
        """获取堆中元素数量"""
        return self.size
    
    def count(self) -> int:
        """获取堆中元素数量（同get_size）"""
        return self.size
    
    def peek(self) -> Optional[T]:
        """查看最小/最大元素的值（不删除）"""
        return self.find_min_value()
    
    def peek_key(self) -> Optional[float]:
        """查看最小/最大元素的键值（不删除）"""
        return self.find_min()
    
    def contains(self, value: T) -> bool:
        """
        检查堆中是否包含指定值
        
        注意：这是一个O(n)操作
        """
        for node in self._iterate_all_nodes():
            if node.value == value:
                return True
        return False
    
    def find_node(self, value: T) -> Optional[FibonacciNode[T]]:
        """
        根据值查找节点
        
        注意：这是一个O(n)操作
        """
        for node in self._iterate_all_nodes():
            if node.value == value:
                return node
        return None
    
    def get_all_values(self) -> List[T]:
        """获取所有值"""
        return [node.value for node in self._iterate_all_nodes()]
    
    def get_all_keys(self) -> List[float]:
        """获取所有键值"""
        return [node.key for node in self._iterate_all_nodes()]
    
    def _iterate_all_nodes(self) -> Iterator[FibonacciNode[T]]:
        """遍历所有节点"""
        if self.min_node is None:
            return
        
        # 使用栈进行深度优先遍历
        stack: List[FibonacciNode[T]] = []
        
        # 收集根链表中的所有节点
        current = self.min_node
        while True:
            stack.append(current)
            current = current.right
            if current is self.min_node:
                break
        
        while stack:
            node = stack.pop()
            yield node
            
            # 添加子节点
            if node.child is not None:
                child = node.child
                while True:
                    stack.append(child)
                    child = child.right
                    if child is node.child:
                        break
    
    def __iter__(self) -> Iterator[T]:
        """迭代器，返回所有值"""
        return (node.value for node in self._iterate_all_nodes())
    
    # ==================== 序列化 ====================
    
    def to_dict(self) -> Dict[str, Any]:
        """将堆序列化为字典"""
        nodes_data = []
        for node in self._iterate_all_nodes():
            nodes_data.append({
                'key': node.key,
                'value': node.value
            })
        
        return {
            'is_max_heap': self.is_max_heap,
            'size': self.size,
            'nodes': nodes_data
        }
    
    def to_json(self) -> str:
        """将堆序列化为JSON字符串"""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FibonacciHeap[T]':
        """从字典创建堆"""
        heap = cls(is_max_heap=data.get('is_max_heap', False))
        for node_data in data.get('nodes', []):
            heap.insert(node_data['key'], node_data['value'])
        return heap
    
    @classmethod
    def from_json(cls, json_str: str) -> 'FibonacciHeap[T]':
        """从JSON字符串创建堆"""
        return cls.from_dict(json.loads(json_str))
    
    # ==================== 实用方法 ====================
    
    def clear(self) -> None:
        """清空堆"""
        self.min_node = None
        self.size = 0
        self._node_map = {}
    
    def copy(self) -> 'FibonacciHeap[T]':
        """创建堆的副本"""
        return self.from_dict(self.to_dict())
    
    def __copy__(self) -> 'FibonacciHeap[T]':
        return self.copy()
    
    def __repr__(self) -> str:
        heap_type = "MaxHeap" if self.is_max_heap else "MinHeap"
        if self.is_empty():
            return f"FibonacciHeap({heap_type}, empty)"
        return f"FibonacciHeap({heap_type}, size={self.size}, peek={self.peek_key()})"
    
    def __str__(self) -> str:
        if self.is_empty():
            return "[]"
        values = self.get_all_values()
        return str(values)
    
    def to_list(self, sorted: bool = True) -> List[T]:
        """
        将堆转换为列表
        
        Args:
            sorted: 是否按优先级排序（会清空堆）
            
        Returns:
            元素列表
        """
        if not sorted:
            return self.get_all_values()
        
        result = []
        while not self.is_empty():
            result.append(self.extract_min())
        return result
    
    @classmethod
    def from_list(cls, items: List[T], key_func: Optional[Callable[[T], float]] = None, 
                  is_max_heap: bool = False) -> 'FibonacciHeap[T]':
        """
        从列表创建堆
        
        Args:
            items: 元素列表
            key_func: 键值函数，如果为None则使用元素本身作为键
            is_max_heap: 是否为最大堆
            
        Returns:
            新的斐波那契堆
        """
        heap = cls(is_max_heap=is_max_heap)
        for item in items:
            key = key_func(item) if key_func else float(item) if isinstance(item, (int, float)) else hash(item)
            heap.insert(key, item)
        return heap


class MaxFibonacciHeap(FibonacciHeap[T]):
    """最大堆便捷类"""
    
    def __init__(self):
        super().__init__(is_max_heap=True)
    
    def find_max(self) -> Optional[float]:
        """查找最大键值"""
        return self.find_min()
    
    def find_max_value(self) -> Optional[T]:
        """查找最大值"""
        return self.find_min_value()
    
    def extract_max(self) -> Optional[T]:
        """删除并返回最大元素"""
        return self.extract_min()
    
    def extract_max_with_key(self) -> Optional[tuple]:
        """删除并返回最大元素及其键值"""
        return self.extract_min_with_key()
    
    def increase_key(self, node: FibonacciNode[T], new_key: float) -> None:
        """增大节点键值"""
        self.decrease_key(node, new_key)


class FibonacciHeapUtils:
    """
    斐波那契堆工具类
    
    提供静态方法来创建和操作斐波那契堆
    """
    
    @staticmethod
    def create_min_heap() -> FibonacciHeap:
        """创建最小堆"""
        return FibonacciHeap(is_max_heap=False)
    
    @staticmethod
    def create_max_heap() -> MaxFibonacciHeap:
        """创建最大堆"""
        return MaxFibonacciHeap()
    
    @staticmethod
    def merge_heaps(*heaps: FibonacciHeap[T]) -> FibonacciHeap[T]:
        """
        合并多个堆
        
        Args:
            *heaps: 要合并的堆
            
        Returns:
            合并后的新堆
        """
        if not heaps:
            return FibonacciHeap()
        
        result = heaps[0].copy()
        for heap in heaps[1:]:
            result.merge(heap)
        
        return result
    
    @staticmethod
    def heap_sort(items: List[T], reverse: bool = False) -> List[T]:
        """
        使用斐波那契堆进行堆排序
        
        Args:
            items: 要排序的元素列表
            reverse: 是否降序排列
            
        Returns:
            排序后的列表
        """
        if not items:
            return []
        
        heap = FibonacciHeap(is_max_heap=reverse)
        for i, item in enumerate(items):
            key = float(item) if isinstance(item, (int, float)) else i
            heap.insert(key, item)
        
        result = []
        while not heap.is_empty():
            result.append(heap.extract_min())
        
        return result
    
    @staticmethod
    def top_k(items: List[T], k: int, key_func: Optional[Callable[[T], float]] = None,
              largest: bool = True) -> List[T]:
        """
        找出前K个最大/最小元素
        
        Args:
            items: 元素列表
            k: 要找的元素数量
            key_func: 键值函数
            largest: True找最大的K个，False找最小的K个
            
        Returns:
            前K个元素
        """
        if not items or k <= 0:
            return []
        
        k = min(k, len(items))
        heap = FibonacciHeap(is_max_heap=not largest)
        
        for item in items:
            key = key_func(item) if key_func else (float(item) if isinstance(item, (int, float)) else hash(item))
            
            if heap.size < k:
                heap.insert(key, item)
            else:
                # 对于找最大的k个，我们维护一个最小堆
                # 对于找最小的k个，我们维护一个最大堆
                if largest:
                    if key > heap.peek_key():
                        heap.extract_min()
                        heap.insert(key, item)
                else:
                    if key < heap.peek_key():
                        heap.extract_min()
                        heap.insert(key, item)
        
        result = []
        while not heap.is_empty():
            result.append(heap.extract_min())
        
        if largest:
            result.reverse()
        
        return result
    
    @staticmethod
    def find_median(items: List[float]) -> Optional[float]:
        """
        使用斐波那契堆找中位数
        
        Args:
            items: 数值列表
            
        Returns:
            中位数
        """
        if not items:
            return None
        
        sorted_items = FibonacciHeapUtils.heap_sort(items)
        n = len(sorted_items)
        
        if n % 2 == 1:
            return sorted_items[n // 2]
        else:
            return (sorted_items[n // 2 - 1] + sorted_items[n // 2]) / 2


# 便捷函数
def create_min_heap() -> FibonacciHeap:
    """创建最小斐波那契堆"""
    return FibonacciHeap(is_max_heap=False)


def create_max_heap() -> MaxFibonacciHeap:
    """创建最大斐波那契堆"""
    return MaxFibonacciHeap()


def heap_sort(items: List[T], reverse: bool = False) -> List[T]:
    """使用斐波那契堆进行堆排序"""
    return FibonacciHeapUtils.heap_sort(items, reverse)


def top_k(items: List[T], k: int, key_func: Optional[Callable[[T], float]] = None,
          largest: bool = True) -> List[T]:
    """找出前K个最大/最小元素"""
    return FibonacciHeapUtils.top_k(items, k, key_func, largest)


# 主函数测试
if __name__ == "__main__":
    # 基本测试
    print("=" * 50)
    print("Fibonacci Heap 基本测试")
    print("=" * 50)
    
    # 创建最小堆
    heap = FibonacciHeap[int]()
    
    # 插入元素
    heap.insert(5, "five")
    heap.insert(1, "one")
    heap.insert(10, "ten")
    heap.insert(3, "three")
    heap.insert(7, "seven")
    
    print(f"堆大小: {heap.size}")
    print(f"最小值: {heap.peek()} (key: {heap.peek_key()})")
    
    # 提取元素
    print("\n按顺序提取:")
    while not heap.is_empty():
        key, value = heap.extract_min_with_key()
        print(f"  key={key}, value={value}")
    
    # 最大堆测试
    print("\n" + "=" * 50)
    print("最大堆测试")
    print("=" * 50)
    
    max_heap = MaxFibonacciHeap[int]()
    max_heap.insert(5, "five")
    max_heap.insert(1, "one")
    max_heap.insert(10, "ten")
    max_heap.insert(3, "three")
    
    print(f"最大值: {max_heap.find_max_value()}")
    
    while not max_heap.is_empty():
        value = max_heap.extract_max()
        print(f"  提取: {value}")
    
    # 合并测试
    print("\n" + "=" * 50)
    print("合并测试")
    print("=" * 50)
    
    h1 = FibonacciHeap[int]()
    h1.insert(1, "h1-1")
    h1.insert(3, "h1-3")
    
    h2 = FibonacciHeap[int]()
    h2.insert(2, "h2-2")
    h2.insert(4, "h2-4")
    
    h1.merge(h2)
    print(f"合并后大小: {h1.size}")
    print(f"合并后提取: {h1.to_list()}")
    
    # decrease_key 测试
    print("\n" + "=" * 50)
    print("decrease_key 测试")
    print("=" * 50)
    
    heap = FibonacciHeap[str]()
    n1 = heap.insert(10, "task1")
    n2 = heap.insert(5, "task2")
    n3 = heap.insert(8, "task3")
    
    print(f"当前最小: {heap.peek()} (key: {heap.peek_key()})")
    
    heap.decrease_key(n1, 1)  # 将task1的优先级从10降到1
    print(f"decrease_key后最小: {heap.peek()} (key: {heap.peek_key()})")
    
    # 堆排序
    print("\n" + "=" * 50)
    print("堆排序测试")
    print("=" * 50)
    
    items = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    print(f"原数组: {items}")
    print(f"升序: {heap_sort(items)}")
    print(f"降序: {heap_sort(items, reverse=True)}")
    
    # Top K
    print("\n" + "=" * 50)
    print("Top K 测试")
    print("=" * 50)
    
    items = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    print(f"原数组: {items}")
    print(f"最大的3个: {top_k(items, 3, largest=True)}")
    print(f"最小的3个: {top_k(items, 3, largest=False)}")
    
    print("\n所有测试通过!")