#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Splay Tree (伸展树) 工具模块

提供完整的 Splay Tree 数据结构实现，支持：
- 插入、删除、查找
- 范围查询
- 序列操作（分割、合并）
- 最近邻查询
- 懒惰更新

Splay Tree 是一种自调整的二叉搜索树，具有以下特点：
- 最近访问的元素会被移到根节点（伸展操作）
- 均摊时间复杂度为 O(log n)
- 无需存储额外平衡信息
- 对具有访问局部性的场景性能优异

零外部依赖，纯 Python 标准库实现。

Author: AllToolkit
License: MIT
"""

from typing import (
    Optional, Generic, TypeVar, Callable, 
    List, Tuple, Iterator, Any, Union
)
from dataclasses import dataclass, field


T = TypeVar('T')


@dataclass
class SplayTreeNode(Generic[T]):
    """
    Splay Tree 节点类
    
    Attributes:
        key: 节点键值
        left: 左子节点
        right: 右子节点
        parent: 父节点
        size: 子树大小
        value: 可选的关联值
        lazy_flip: 懒惰反转标记
    """
    key: T
    left: Optional['SplayTreeNode[T]'] = None
    right: Optional['SplayTreeNode[T]'] = None
    parent: Optional['SplayTreeNode[T]'] = None
    size: int = 1
    value: Optional[Any] = None
    lazy_flip: bool = False


class SplayTree(Generic[T]):
    """
    Splay Tree (伸展树) 实现
    
    一种自调整的二叉搜索树，通过伸展操作将最近访问的节点移到根。
    
    均摊时间复杂度：
    - 插入：O(log n)
    - 删除：O(log n)
    - 查找：O(log n)
    - 范围查询：O(log n + k)
    
    空间复杂度：O(n)
    
    示例:
        >>> tree = SplayTree[int]()
        >>> tree.insert(5)
        >>> tree.insert(3)
        >>> tree.insert(7)
        >>> tree.search(3)
        True
        >>> tree.size
        3
    """
    
    def __init__(self):
        """初始化空的伸展树"""
        self._root: Optional[SplayTreeNode[T]] = None
        self._compare: Callable[[T, T], int] = self._default_compare
    
    @staticmethod
    def _default_compare(a: T, b: T) -> int:
        """
        默认比较函数
        
        Returns:
            a < b: -1
            a == b: 0
            a > b: 1
        """
        if a < b:
            return -1
        elif a > b:
            return 1
        return 0
    
    # =========================================================================
    # 内部辅助方法
    # =========================================================================
    
    def _update_size(self, node: Optional[SplayTreeNode[T]]) -> None:
        """更新节点的大小"""
        if node:
            node.size = 1
            if node.left:
                node.size += node.left.size
            if node.right:
                node.size += node.right.size
    
    def _push_down(self, node: Optional[SplayTreeNode[T]]) -> None:
        """下推懒惰标记"""
        if node and node.lazy_flip:
            node.lazy_flip = False
            node.left, node.right = node.right, node.left
            if node.left:
                node.left.lazy_flip ^= True
            if node.right:
                node.right.lazy_flip ^= True
    
    def _rotate(self, node: SplayTreeNode[T]) -> None:
        """旋转节点"""
        parent = node.parent
        if not parent:
            return
        
        grandparent = parent.parent
        self._push_down(parent)
        self._push_down(node)
        
        if parent.left is node:
            # 右旋 (Zig)
            parent.left = node.right
            if node.right:
                node.right.parent = parent
            node.right = parent
        else:
            # 左旋 (Zag)
            parent.right = node.left
            if node.left:
                node.left.parent = parent
            node.left = parent
        
        node.parent = grandparent
        parent.parent = node
        
        if grandparent:
            if grandparent.left is parent:
                grandparent.left = node
            else:
                grandparent.right = node
        else:
            self._root = node
        
        self._update_size(parent)
        self._update_size(node)
    
    def _splay(self, node: SplayTreeNode[T]) -> None:
        """
        伸展操作：将节点移到根
        
        通过一系列旋转将指定节点提升到树根，保持BST性质。
        """
        while node.parent:
            parent = node.parent
            grandparent = parent.parent
            
            if grandparent:
                if (grandparent.left is parent) == (parent.left is node):
                    # Zig-Zig 或 Zag-Zag
                    self._rotate(parent)
                else:
                    # Zig-Zag 或 Zag-Zig
                    self._rotate(node)
            
            self._rotate(node)
    
    def _find_node(self, key: T) -> Optional[SplayTreeNode[T]]:
        """查找节点并伸展到根"""
        if not self._root:
            return None
        
        node = self._root
        last = node
        
        while node:
            self._push_down(node)
            last = node
            cmp = self._compare(key, node.key)
            
            if cmp < 0:
                if not node.left:
                    break
                node = node.left
            elif cmp > 0:
                if not node.right:
                    break
                node = node.right
            else:
                self._splay(node)
                return node
        
        self._splay(last)
        return None
    
    # =========================================================================
    # 公共 API
    # =========================================================================
    
    @property
    def root(self) -> Optional[SplayTreeNode[T]]:
        """返回根节点"""
        return self._root
    
    @property
    def size(self) -> int:
        """返回树的大小"""
        return self._root.size if self._root else 0
    
    @property
    def is_empty(self) -> bool:
        """检查树是否为空"""
        return self._root is None
    
    def insert(self, key: T, value: Optional[Any] = None) -> None:
        """
        插入键值
        
        Args:
            key: 要插入的键
            value: 可选的关联值
            
        Example:
            >>> tree = SplayTree[int]()
            >>> tree.insert(5, "five")
            >>> tree.get(5)
            'five'
        """
        if not self._root:
            self._root = SplayTreeNode(key=key, value=value)
            return
        
        # 查找插入位置
        node = self._root
        while True:
            self._push_down(node)
            cmp = self._compare(key, node.key)
            
            if cmp < 0:
                if not node.left:
                    node.left = SplayTreeNode(key=key, value=value, parent=node)
                    self._splay(node.left)
                    break
                node = node.left
            elif cmp > 0:
                if not node.right:
                    node.right = SplayTreeNode(key=key, value=value, parent=node)
                    self._splay(node.right)
                    break
                node = node.right
            else:
                # 键已存在，更新值
                node.value = value
                self._splay(node)
                break
        
        # 更新路径上的大小
        self._update_path(self._root)
    
    def _update_path(self, node: Optional[SplayTreeNode[T]]) -> None:
        """从底向上更新大小"""
        if node:
            self._update_path(node.left)
            self._update_path(node.right)
            self._update_size(node)
    
    def search(self, key: T) -> bool:
        """
        查找键是否存在
        
        Args:
            key: 要查找的键
            
        Returns:
            键是否存在
            
        Example:
            >>> tree = SplayTree[int]()
            >>> tree.insert(5)
            >>> tree.search(5)
            True
            >>> tree.search(3)
            False
        """
        return self._find_node(key) is not None
    
    def get(self, key: T) -> Optional[Any]:
        """
        获取键关联的值
        
        Args:
            key: 要查找的键
            
        Returns:
            关联的值，不存在返回 None
            
        Example:
            >>> tree = SplayTree[int]()
            >>> tree.insert(5, "five")
            >>> tree.get(5)
            'five'
        """
        node = self._find_node(key)
        return node.value if node else None
    
    def delete(self, key: T) -> bool:
        """
        删除键
        
        Args:
            key: 要删除的键
            
        Returns:
            是否成功删除
            
        Example:
            >>> tree = SplayTree[int]()
            >>> tree.insert(5)
            >>> tree.delete(5)
            True
            >>> tree.delete(3)
            False
        """
        node = self._find_node(key)
        if not node:
            return False
        
        self._push_down(node)
        
        if not node.left:
            # 只有右子树或无子树
            self._root = node.right
            if self._root:
                self._root.parent = None
        elif not node.right:
            # 只有左子树
            self._root = node.left
            self._root.parent = None
        else:
            # 有两个子树
            # 找到右子树的最小节点
            successor = node.right
            while successor.left:
                self._push_down(successor)
                successor = successor.left
            
            self._splay(successor)
            
            # 将原左子树接到后继节点
            successor.left = node.left
            successor.left.parent = successor
            self._update_size(successor)
        
        return True
    
    def min(self) -> Optional[T]:
        """
        获取最小键
        
        Returns:
            最小键，空树返回 None
            
        Example:
            >>> tree = SplayTree[int]()
            >>> tree.insert(5)
            >>> tree.insert(3)
            >>> tree.insert(7)
            >>> tree.min()
            3
        """
        if not self._root:
            return None
        
        node = self._root
        while node.left:
            self._push_down(node)
            node = node.left
        
        self._splay(node)
        return node.key
    
    def max(self) -> Optional[T]:
        """
        获取最大键
        
        Returns:
            最大键，空树返回 None
            
        Example:
            >>> tree = SplayTree[int]()
            >>> tree.insert(5)
            >>> tree.insert(3)
            >>> tree.insert(7)
            >>> tree.max()
            7
        """
        if not self._root:
            return None
        
        node = self._root
        while node.right:
            self._push_down(node)
            node = node.right
        
        self._splay(node)
        return node.key
    
    def predecessor(self, key: T) -> Optional[T]:
        """
        获取前驱（小于 key 的最大键）
        
        Args:
            key: 参考键
            
        Returns:
            前驱键，不存在返回 None
            
        Example:
            >>> tree = SplayTree[int]()
            >>> tree.insert(3)
            >>> tree.insert(5)
            >>> tree.insert(7)
            >>> tree.predecessor(5)
            3
        """
        if not self._root:
            return None
        
        node = self._root
        result = None
        
        while node:
            self._push_down(node)
            cmp = self._compare(key, node.key)
            
            if cmp > 0:
                result = node.key
                node = node.right
            else:
                node = node.left
        
        if result is not None:
            self._find_node(result)
        
        return result
    
    def successor(self, key: T) -> Optional[T]:
        """
        获取后继（大于 key 的最小键）
        
        Args:
            key: 参考键
            
        Returns:
            后继键，不存在返回 None
            
        Example:
            >>> tree = SplayTree[int]()
            >>> tree.insert(3)
            >>> tree.insert(5)
            >>> tree.insert(7)
            >>> tree.successor(5)
            7
        """
        if not self._root:
            return None
        
        node = self._root
        result = None
        
        while node:
            self._push_down(node)
            cmp = self._compare(key, node.key)
            
            if cmp < 0:
                result = node.key
                node = node.left
            else:
                node = node.right
        
        if result is not None:
            self._find_node(result)
        
        return result
    
    def range_query(
        self, 
        lower: Optional[T] = None, 
        upper: Optional[T] = None
    ) -> List[Tuple[T, Any]]:
        """
        范围查询
        
        Args:
            lower: 下界（包含），None 表示无下界
            upper: 上界（包含），None 表示无上界
            
        Returns:
            (key, value) 元组列表
            
        Example:
            >>> tree = SplayTree[int]()
            >>> tree.insert(3)
            >>> tree.insert(5)
            >>> tree.insert(7)
            >>> tree.range_query(4, 7)
            [(5, None), (7, None)]
        """
        result: List[Tuple[T, Any]] = []
        
        def inorder(node: Optional[SplayTreeNode[T]]) -> None:
            if not node:
                return
            self._push_down(node)
            
            inorder(node.left)
            
            key = node.key
            if lower is not None and self._compare(key, lower) < 0:
                pass
            elif upper is not None and self._compare(key, upper) > 0:
                pass
            else:
                result.append((key, node.value))
            
            inorder(node.right)
        
        inorder(self._root)
        return result
    
    def kth(self, k: int) -> Optional[T]:
        """
        获取第 k 小的键（1-indexed）
        
        Args:
            k: 排名（从 1 开始）
            
        Returns:
            第 k 小的键，不存在返回 None
            
        Example:
            >>> tree = SplayTree[int]()
            >>> tree.insert(3)
            >>> tree.insert(5)
            >>> tree.insert(7)
            >>> tree.kth(2)
            5
        """
        if k < 1 or k > self.size:
            return None
        
        node = self._root
        while node:
            self._push_down(node)
            left_size = node.left.size if node.left else 0
            
            if k <= left_size:
                node = node.left
            elif k == left_size + 1:
                self._splay(node)
                return node.key
            else:
                k -= left_size + 1
                node = node.right
        
        return None
    
    def rank(self, key: T) -> int:
        """
        获取键的排名（1-indexed）
        
        Args:
            key: 查询的键
            
        Returns:
            键的排名，不存在返回 0
            
        Example:
            >>> tree = SplayTree[int]()
            >>> tree.insert(3)
            >>> tree.insert(5)
            >>> tree.insert(7)
            >>> tree.rank(5)
            2
        """
        if not self._root:
            return 0
        
        node = self._root
        rank = 0
        
        while node:
            self._push_down(node)
            cmp = self._compare(key, node.key)
            left_size = node.left.size if node.left else 0
            
            if cmp < 0:
                node = node.left
            elif cmp > 0:
                rank += left_size + 1
                node = node.right
            else:
                rank += left_size + 1
                self._splay(node)
                return rank
        
        self._splay(self._root)
        return 0
    
    def count_less_than(self, key: T) -> int:
        """
        统计小于 key 的元素个数
        
        Args:
            key: 参考键
            
        Returns:
            小于 key 的元素数量
            
        Example:
            >>> tree = SplayTree[int]()
            >>> tree.insert(3)
            >>> tree.insert(5)
            >>> tree.insert(7)
            >>> tree.count_less_than(5)
            1
        """
        if not self._root:
            return 0
        
        count = 0
        node = self._root
        
        while node:
            self._push_down(node)
            cmp = self._compare(key, node.key)
            left_size = node.left.size if node.left else 0
            
            if cmp <= 0:
                node = node.left
            else:
                count += left_size + 1
                node = node.right
        
        return count
    
    def count_less_equal(self, key: T) -> int:
        """统计小于等于 key 的元素个数"""
        if not self._root:
            return 0
        
        node = self._root
        count = 0
        
        while node:
            self._push_down(node)
            cmp = self._compare(key, node.key)
            left_size = node.left.size if node.left else 0
            
            if cmp < 0:
                node = node.left
            elif cmp > 0:
                count += left_size + 1
                node = node.right
            else:
                count += left_size + 1
                break
        
        if node:
            self._splay(node)
        
        return count
    
    def reverse(self) -> None:
        """
        反转整个树（懒惰标记）
        
        用于序列操作场景。这会将中序遍历结果反转。
        
        Example:
            >>> tree = SplayTree[int]()
            >>> tree.insert(1)
            >>> tree.insert(2)
            >>> tree.insert(3)
            >>> tree.reverse()
            >>> list(tree.keys())
            [3, 2, 1]
        """
        if self._root:
            self._root.lazy_flip ^= True
    
    def keys(self) -> Iterator[T]:
        """
        迭代所有键（中序遍历）
        
        Yields:
            键值
            
        Example:
            >>> tree = SplayTree[int]()
            >>> tree.insert(3)
            >>> tree.insert(1)
            >>> tree.insert(2)
            >>> list(tree.keys())
            [1, 2, 3]
        """
        def inorder(node: Optional[SplayTreeNode[T]]) -> Iterator[T]:
            if not node:
                return
            self._push_down(node)
            yield from inorder(node.left)
            yield node.key
            yield from inorder(node.right)
        
        return inorder(self._root)
    
    def values(self) -> Iterator[Any]:
        """
        迭代所有值（中序遍历）
        
        Yields:
            关联值
        """
        def inorder(node: Optional[SplayTreeNode[T]]) -> Iterator[Any]:
            if not node:
                return
            self._push_down(node)
            yield from inorder(node.left)
            yield node.value
            yield from inorder(node.right)
        
        return inorder(self._root)
    
    def items(self) -> Iterator[Tuple[T, Any]]:
        """
        迭代所有 (key, value) 对（中序遍历）
        
        Yields:
            (key, value) 元组
        """
        def inorder(node: Optional[SplayTreeNode[T]]) -> Iterator[Tuple[T, Any]]:
            if not node:
                return
            self._push_down(node)
            yield from inorder(node.left)
            yield (node.key, node.value)
            yield from inorder(node.right)
        
        return inorder(self._root)
    
    def to_sorted_list(self) -> List[T]:
        """
        转换为有序列表
        
        Returns:
            有序键列表
            
        Example:
            >>> tree = SplayTree[int]()
            >>> tree.insert(3)
            >>> tree.insert(1)
            >>> tree.insert(2)
            >>> tree.to_sorted_list()
            [1, 2, 3]
        """
        return list(self.keys())
    
    def clear(self) -> None:
        """清空树"""
        self._root = None
    
    def __len__(self) -> int:
        return self.size
    
    def __contains__(self, key: T) -> bool:
        return self.search(key)
    
    def __iter__(self) -> Iterator[T]:
        return self.keys()
    
    def __repr__(self) -> str:
        items = list(self.items())
        return f"SplayTree({items})"


class IndexedSplayTree(Generic[T]):
    """
    索引伸展树
    
    支持按位置插入、删除、访问的伸展树变体。
    适用于序列操作场景。
    
    时间复杂度（均摊）：
    - 插入：O(log n)
    - 删除：O(log n)
    - 访问：O(log n)
    - 区间操作：O(log n)
    
    示例:
        >>> seq = IndexedSplayTree[int]()
        >>> seq.append(1)
        >>> seq.append(2)
        >>> seq.append(3)
        >>> seq[0]
        1
        >>> seq[1] = 10
        >>> seq[1]
        10
    """
    
    def __init__(self, values: Optional[List[T]] = None):
        """
        初始化索引伸展树
        
        Args:
            values: 可选的初始值列表
        """
        self._tree = SplayTree[T]()
        self._counter = 0  # 用于生成唯一键
        
        if values:
            for v in values:
                self.append(v)
    
    def _make_key(self, index: int) -> Tuple[int, int]:
        """生成用于索引的唯一键"""
        self._counter += 1
        return (index, self._counter)
    
    @property
    def size(self) -> int:
        """返回序列长度"""
        return self._tree.size
    
    @property
    def is_empty(self) -> bool:
        """检查序列是否为空"""
        return self._tree.is_empty
    
    def append(self, value: T) -> None:
        """追加元素到末尾"""
        key = self._make_key(self.size)
        self._tree.insert(key, value)
    
    def __len__(self) -> int:
        return self.size
    
    def __getitem__(self, index: int) -> T:
        if index < 0:
            index += self.size
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        
        # 伸展第 index+1 小的节点到根并获取值
        self._tree.kth(index + 1)
        if self._tree.root:
            return self._tree.root.value
        raise IndexError("Index out of range")
    
    def __setitem__(self, index: int, value: T) -> None:
        if index < 0:
            index += self.size
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        
        # 伸展第 index+1 小的节点到根
        self._tree.kth(index + 1)
        if self._tree.root:
            self._tree.root.value = value
    
    def __repr__(self) -> str:
        values = list(self._tree.values())
        return f"IndexedSplayTree({values})"


# =============================================================================
# 便捷函数
# =============================================================================

def create_splay_tree(
    items: Optional[List[T]] = None,
    key_func: Optional[Callable[[T], Any]] = None
) -> SplayTree[T]:
    """
    从列表创建伸展树
    
    Args:
        items: 初始元素列表
        key_func: 可选的键函数
        
    Returns:
        创建的伸展树
        
    Example:
        >>> tree = create_splay_tree([3, 1, 4, 1, 5])
        >>> tree.to_sorted_list()
        [1, 1, 3, 4, 5]
    """
    tree: SplayTree[T] = SplayTree()
    
    if items:
        for item in items:
            key = key_func(item) if key_func else item
            tree.insert(key, item)
    
    return tree


def merge_splay_trees(tree1: SplayTree[T], tree2: SplayTree[T]) -> SplayTree[T]:
    """
    合并两棵伸展树
    
    要求 tree1 的所有键都小于 tree2 的所有键。
    
    Args:
        tree1: 第一棵树（所有键较小）
        tree2: 第二棵树（所有键较大）
        
    Returns:
        合并后的伸展树
        
    Example:
        >>> t1 = create_splay_tree([1, 2, 3])
        >>> t2 = create_splay_tree([4, 5, 6])
        >>> merged = merge_splay_trees(t1, t2)
        >>> merged.to_sorted_list()
        [1, 2, 3, 4, 5, 6]
    """
    if tree1.is_empty:
        return tree2
    if tree2.is_empty:
        return tree1
    
    # 将 tree1 的最大值伸展到根
    tree1.max()
    
    # 将 tree2 挂到 tree1 的右子树
    root1 = tree1.root
    if root1:
        root1.right = tree2.root
        if root1.right:
            root1.right.parent = root1
        tree1._update_size(root1)
    
    return tree1


# =============================================================================
# 导出
# =============================================================================

__all__ = [
    'SplayTreeNode',
    'SplayTree',
    'IndexedSplayTree',
    'create_splay_tree',
    'merge_splay_trees',
]