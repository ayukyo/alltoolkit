"""
Scapegoat Tree - 自平衡二叉搜索树实现

替罪羊树是一种自平衡二叉搜索树，具有以下特点：
1. 无需在每个节点存储额外的高度或平衡信息
2. 通过重建不平衡子树来维持平衡
3. 摊还时间复杂度为 O(log n)
4. 空间复杂度为 O(n)

参数 alpha (平衡因子): 0.5 < alpha < 1.0
- alpha 越接近 0.5，树越平衡，但重建频率越高
- alpha 越接近 1.0，重建频率越低，但树可能更不平衡
- 推荐值: 0.5 ~ 0.7
"""

from typing import TypeVar, Generic, Optional, Callable, List, Iterator, Tuple, Any
from dataclasses import dataclass
import math

T = TypeVar('T')


@dataclass
class TreeNode(Generic[T]):
    """替罪羊树节点"""
    key: T
    left: Optional['TreeNode[T]'] = None
    right: Optional['TreeNode[T]'] = None
    
    def __repr__(self) -> str:
        return f"TreeNode({self.key})"


class ScapegoatTree(Generic[T]):
    """
    替罪羊树实现
    
    替罪羊树是一种简单且高效的自平衡二叉搜索树。
    与 AVL 树和红黑树不同，它不需要在每个节点存储平衡因子或颜色信息。
    
    示例:
        >>> tree = ScapegoatTree[int](alpha=0.7)
        >>> tree.insert(5)
        >>> tree.insert(3)
        >>> tree.insert(7)
        >>> tree.contains(5)
        True
        >>> tree.delete(5)
        True
        >>> tree.contains(5)
        False
    """
    
    def __init__(self, alpha: float = 0.7, comparator: Optional[Callable[[T, T], int]] = None):
        """
        初始化替罪羊树
        
        Args:
            alpha: 平衡因子，范围 (0.5, 1.0)，默认 0.7
            comparator: 自定义比较函数，返回负数表示 a < b，正数表示 a > b，0 表示相等
                       如果不提供，将使用 < 和 == 运算符
        """
        if not 0.5 < alpha < 1.0:
            raise ValueError(f"alpha must be in range (0.5, 1.0), got {alpha}")
        
        self._alpha = alpha
        self._comparator = comparator
        self._root: Optional[TreeNode[T]] = None
        self._size = 0
        self._max_size = 0  # 上次重建后的最大节点数
    
    def _compare(self, a: T, b: T) -> int:
        """比较两个元素"""
        if self._comparator:
            return self._comparator(a, b)
        if a < b:
            return -1
        elif a > b:
            return 1
        return 0
    
    def _size_of(self, node: Optional[TreeNode[T]]) -> int:
        """计算子树大小"""
        if node is None:
            return 0
        return 1 + self._size_of(node.left) + self._size_of(node.right)
    
    def _height_of(self, node: Optional[TreeNode[T]]) -> int:
        """计算子树高度"""
        if node is None:
            return 0
        return 1 + max(self._height_of(node.left), self._height_of(node.right))
    
    def _flatten(self, node: Optional[TreeNode[T]], result: List[T]) -> None:
        """中序遍历收集节点"""
        if node is None:
            return
        self._flatten(node.left, result)
        result.append(node.key)
        self._flatten(node.right, result)
    
    def _build_balanced(self, keys: List[T], start: int, end: int) -> Optional[TreeNode[T]]:
        """从有序数组构建平衡树"""
        if start >= end:
            return None
        
        mid = (start + end) // 2
        node = TreeNode(keys[mid])
        node.left = self._build_balanced(keys, start, mid)
        node.right = self._build_balanced(keys, mid + 1, end)
        return node
    
    def _rebuild(self, node: TreeNode[T]) -> TreeNode[T]:
        """重建子树"""
        keys: List[T] = []
        self._flatten(node, keys)
        return self._build_balanced(keys, 0, len(keys))
    
    def _find_scapegoat(self, node: TreeNode[T], key: T, path: List[Tuple[TreeNode[T], str]]) -> Optional[TreeNode[T]]:
        """
        找到替罪羊节点
        
        从插入点到根节点，找到第一个不平衡的节点作为替罪羊
        """
        size = 1
        current = node
        
        # 从插入点向上遍历
        for parent, direction in reversed(path):
            if direction == 'left':
                sibling_size = self._size_of(parent.right)
            else:
                sibling_size = self._size_of(parent.left)
            
            total_size = 1 + size + sibling_size
            
            # 检查是否不平衡
            if size > self._alpha * total_size:
                return parent
            
            size = total_size
            current = parent
        
        return None
    
    def insert(self, key: T) -> bool:
        """
        插入元素
        
        Args:
            key: 要插入的键
        
        Returns:
            如果插入成功返回 True，如果元素已存在返回 False
        
        时间复杂度: 摊还 O(log n)
        """
        if self._root is None:
            self._root = TreeNode(key)
            self._size = 1
            self._max_size = 1
            return True
        
        path: List[Tuple[TreeNode[T], str]] = []
        current = self._root
        
        while current is not None:
            cmp = self._compare(key, current.key)
            
            if cmp == 0:
                return False  # 元素已存在
            
            if cmp < 0:
                path.append((current, 'left'))
                if current.left is None:
                    current.left = TreeNode(key)
                    break
                current = current.left
            else:
                path.append((current, 'right'))
                if current.right is None:
                    current.right = TreeNode(key)
                    break
                current = current.right
        
        self._size += 1
        self._max_size = max(self._max_size, self._size)
        
        # 检查是否需要重建
        h_alpha = math.log(self._size, 1 / self._alpha)
        actual_height = self._height_of(self._root)
        
        if actual_height > h_alpha:
            # 找到替罪羊节点并重建
            scapegoat = self._find_scapegoat(self._root, key, path)
            if scapegoat:
                rebuilt = self._rebuild(scapegoat)
                
                # 更新父节点的引用
                if scapegoat is self._root:
                    self._root = rebuilt
                else:
                    # 找到替罪羊的父节点
                    for i, (parent, direction) in enumerate(path):
                        if parent.left is scapegoat:
                            parent.left = rebuilt
                            break
                        elif parent.right is scapegoat:
                            parent.right = rebuilt
                            break
                
                self._max_size = self._size
        
        return True
    
    def contains(self, key: T) -> bool:
        """
        检查元素是否存在
        
        Args:
            key: 要查找的键
        
        Returns:
            如果元素存在返回 True，否则返回 False
        
        时间复杂度: O(log n)
        """
        current = self._root
        
        while current is not None:
            cmp = self._compare(key, current.key)
            
            if cmp == 0:
                return True
            elif cmp < 0:
                current = current.left
            else:
                current = current.right
        
        return False
    
    def find(self, key: T) -> Optional[T]:
        """
        查找元素
        
        Args:
            key: 要查找的键
        
        Returns:
            如果找到返回元素值，否则返回 None
        
        时间复杂度: O(log n)
        """
        current = self._root
        
        while current is not None:
            cmp = self._compare(key, current.key)
            
            if cmp == 0:
                return current.key
            elif cmp < 0:
                current = current.left
            else:
                current = current.right
        
        return None
    
    def delete(self, key: T) -> bool:
        """
        删除元素
        
        Args:
            key: 要删除的键
        
        Returns:
            如果删除成功返回 True，如果元素不存在返回 False
        
        时间复杂度: 摊还 O(log n)
        """
        # 查找节点及其父节点
        parent: Optional[TreeNode[T]] = None
        parent_direction: Optional[str] = None
        current = self._root
        
        while current is not None:
            cmp = self._compare(key, current.key)
            
            if cmp == 0:
                break
            elif cmp < 0:
                parent = current
                parent_direction = 'left'
                current = current.left
            else:
                parent = current
                parent_direction = 'right'
                current = current.right
        
        if current is None:
            return False
        
        # 删除节点
        if current.left is None:
            replacement = current.right
        elif current.right is None:
            replacement = current.left
        else:
            # 找到中序后继
            successor_parent = current
            successor = current.right
            
            while successor.left is not None:
                successor_parent = successor
                successor = successor.left
            
            # 将后继的键移到当前节点
            current.key = successor.key
            
            # 删除后继节点
            if successor_parent is current:
                successor_parent.right = successor.right
            else:
                successor_parent.left = successor.right
            
            self._size -= 1
            
            # 检查是否需要重建
            if self._size < self._alpha * self._max_size:
                if self._root:
                    self._root = self._rebuild(self._root)
                self._max_size = self._size
            
            return True
        
        # 更新父节点引用
        if parent is None:
            self._root = replacement
        elif parent_direction == 'left':
            parent.left = replacement
        else:
            parent.right = replacement
        
        self._size -= 1
        
        # 检查是否需要重建
        if self._size < self._alpha * self._max_size:
            if self._root:
                self._root = self._rebuild(self._root)
            self._max_size = self._size
        
        return True
    
    def min(self) -> Optional[T]:
        """
        获取最小元素
        
        Returns:
            最小元素，如果树为空返回 None
        """
        if self._root is None:
            return None
        
        current = self._root
        while current.left is not None:
            current = current.left
        
        return current.key
    
    def max(self) -> Optional[T]:
        """
        获取最大元素
        
        Returns:
            最大元素，如果树为空返回 None
        """
        if self._root is None:
            return None
        
        current = self._root
        while current.right is not None:
            current = current.right
        
        return current.key
    
    def predecessor(self, key: T) -> Optional[T]:
        """
        获取前驱元素（小于 key 的最大元素）
        
        Args:
            key: 目标键
        
        Returns:
            前驱元素，如果不存在返回 None
        """
        result = None
        current = self._root
        
        while current is not None:
            if self._compare(key, current.key) > 0:
                result = current.key
                current = current.right
            else:
                current = current.left
        
        return result
    
    def successor(self, key: T) -> Optional[T]:
        """
        获取后继元素（大于 key 的最小元素）
        
        Args:
            key: 目标键
        
        Returns:
            后继元素，如果不存在返回 None
        """
        result = None
        current = self._root
        
        while current is not None:
            if self._compare(key, current.key) < 0:
                result = current.key
                current = current.left
            else:
                current = current.right
        
        return result
    
    def inorder(self) -> Iterator[T]:
        """
        中序遍历迭代器
        
        Yields:
            按升序排列的元素
        """
        def _inorder(node: Optional[TreeNode[T]]) -> Iterator[T]:
            if node is None:
                return
            yield from _inorder(node.left)
            yield node.key
            yield from _inorder(node.right)
        
        return _inorder(self._root)
    
    def preorder(self) -> Iterator[T]:
        """
        前序遍历迭代器
        
        Yields:
            按前序排列的元素
        """
        def _preorder(node: Optional[TreeNode[T]]) -> Iterator[T]:
            if node is None:
                return
            yield node.key
            yield from _preorder(node.left)
            yield from _preorder(node.right)
        
        return _preorder(self._root)
    
    def postorder(self) -> Iterator[T]:
        """
        后序遍历迭代器
        
        Yields:
            按后序排列的元素
        """
        def _postorder(node: Optional[TreeNode[T]]) -> Iterator[T]:
            if node is None:
                return
            yield from _postorder(node.left)
            yield from _postorder(node.right)
            yield node.key
        
        return _postorder(self._root)
    
    def range_query(self, low: T, high: T) -> List[T]:
        """
        范围查询
        
        Args:
            low: 下界（包含）
            high: 上界（包含）
        
        Returns:
            在范围内的所有元素列表
        """
        result: List[T] = []
        
        def _range_query(node: Optional[TreeNode[T]]) -> None:
            if node is None:
                return
            
            # 如果当前节点大于下界，搜索左子树
            if self._compare(node.key, low) > 0:
                _range_query(node.left)
            
            # 如果当前节点在范围内，添加到结果
            if self._compare(node.key, low) >= 0 and self._compare(node.key, high) <= 0:
                result.append(node.key)
            
            # 如果当前节点小于上界，搜索右子树
            if self._compare(node.key, high) < 0:
                _range_query(node.right)
        
        _range_query(self._root)
        return result
    
    def count_less_than(self, key: T) -> int:
        """
        统计小于指定值的元素数量
        
        Args:
            key: 目标键
        
        Returns:
            小于 key 的元素数量
        """
        count = 0
        current = self._root
        
        while current is not None:
            cmp = self._compare(key, current.key)
            
            if cmp <= 0:
                current = current.left
            else:
                count += 1 + self._size_of(current.left)
                current = current.right
        
        return count
    
    def count_greater_than(self, key: T) -> int:
        """
        统计大于指定值的元素数量
        
        Args:
            key: 目标键
        
        Returns:
            大于 key 的元素数量
        """
        count = 0
        current = self._root
        
        while current is not None:
            cmp = self._compare(key, current.key)
            
            if cmp >= 0:
                current = current.right
            else:
                count += 1 + self._size_of(current.right)
                current = current.left
        
        return count
    
    def kth_smallest(self, k: int) -> Optional[T]:
        """
        获取第 k 小的元素
        
        Args:
            k: 排名（从 1 开始）
        
        Returns:
            第 k 小的元素，如果 k 超出范围返回 None
        """
        if k < 1 or k > self._size:
            return None
        
        current = self._root
        k_remaining = k
        
        while current is not None:
            left_size = self._size_of(current.left)
            
            if k_remaining == left_size + 1:
                return current.key
            elif k_remaining <= left_size:
                current = current.left
            else:
                k_remaining -= left_size + 1
                current = current.right
        
        return None
    
    def kth_largest(self, k: int) -> Optional[T]:
        """
        获取第 k 大的元素
        
        Args:
            k: 排名（从 1 开始）
        
        Returns:
            第 k 大的元素，如果 k 超出范围返回 None
        """
        return self.kth_smallest(self._size - k + 1)
    
    def rank(self, key: T) -> int:
        """
        获取元素的排名（从 1 开始）
        
        Args:
            key: 目标键
        
        Returns:
            元素的排名，如果元素不存在返回 0
        """
        if not self.contains(key):
            return 0
        
        return self.count_less_than(key) + 1
    
    def clear(self) -> None:
        """清空树"""
        self._root = None
        self._size = 0
        self._max_size = 0
    
    def is_balanced(self) -> bool:
        """
        检查树是否平衡
        
        替罪羊树的平衡条件是：
        - 高度 <= log_{1/alpha}(size)
        
        Returns:
            如果树满足替罪羊树的平衡条件返回 True
        """
        if self._size == 0:
            return True
        
        # 高度条件：height <= log_{1/alpha}(size)
        import math
        max_height = math.log(self._size, 1 / self._alpha)
        return self.height <= max_height + 1
    
    def to_list(self) -> List[T]:
        """
        将树转换为有序列表
        
        Returns:
            按升序排列的元素列表
        """
        return list(self.inorder())
    
    def to_tree_string(self) -> str:
        """
        将树转换为可视化的字符串表示
        
        Returns:
            树的可视化字符串
        """
        lines: List[str] = []
        
        def _build_lines(node: Optional[TreeNode[T]], prefix: str = '', is_left: bool = True) -> None:
            if node is None:
                return
            
            _build_lines(node.right, prefix + ('│   ' if is_left else '    '), False)
            lines.append(prefix + ('└── ' if is_left else '┌── ') + str(node.key))
            _build_lines(node.left, prefix + ('    ' if is_left else '│   '), True)
        
        _build_lines(self._root)
        return '\n'.join(lines)
    
    @property
    def size(self) -> int:
        """获取树的节点数"""
        return self._size
    
    @property
    def height(self) -> int:
        """获取树的高度"""
        return self._height_of(self._root)
    
    @property
    def is_empty(self) -> bool:
        """检查树是否为空"""
        return self._size == 0
    
    @property
    def alpha(self) -> float:
        """获取平衡因子"""
        return self._alpha
    
    def __len__(self) -> int:
        return self._size
    
    def __contains__(self, key: T) -> bool:
        return self.contains(key)
    
    def __iter__(self) -> Iterator[T]:
        return self.inorder()
    
    def __repr__(self) -> str:
        return f"ScapegoatTree(size={self._size}, alpha={self._alpha})"
    
    def __str__(self) -> str:
        return f"ScapegoatTree({self.to_list()})"


class ScapegoatTreeSet(Generic[T]):
    """
    基于替罪羊树的集合实现
    
    示例:
        >>> s = ScapegoatTreeSet[int]()
        >>> s.add(1)
        >>> s.add(2)
        >>> s.add(3)
        >>> len(s)
        3
        >>> 2 in s
        True
    """
    
    def __init__(self, alpha: float = 0.7, comparator: Optional[Callable[[T, T], int]] = None):
        self._tree = ScapegoatTree[T](alpha=alpha, comparator=comparator)
    
    def add(self, key: T) -> bool:
        """添加元素"""
        return self._tree.insert(key)
    
    def remove(self, key: T) -> bool:
        """移除元素"""
        return self._tree.delete(key)
    
    def discard(self, key: T) -> bool:
        """移除元素（如果存在）"""
        return self._tree.delete(key)
    
    def contains(self, key: T) -> bool:
        """检查元素是否存在"""
        return self._tree.contains(key)
    
    def min(self) -> Optional[T]:
        """获取最小元素"""
        return self._tree.min()
    
    def max(self) -> Optional[T]:
        """获取最大元素"""
        return self._tree.max()
    
    def predecessor(self, key: T) -> Optional[T]:
        """获取前驱元素"""
        return self._tree.predecessor(key)
    
    def successor(self, key: T) -> Optional[T]:
        """获取后继元素"""
        return self._tree.successor(key)
    
    def range_query(self, low: T, high: T) -> List[T]:
        """范围查询"""
        return self._tree.range_query(low, high)
    
    def kth_smallest(self, k: int) -> Optional[T]:
        """获取第 k 小的元素"""
        return self._tree.kth_smallest(k)
    
    def kth_largest(self, k: int) -> Optional[T]:
        """获取第 k 大的元素"""
        return self._tree.kth_largest(k)
    
    def rank(self, key: T) -> int:
        """获取元素的排名"""
        return self._tree.rank(key)
    
    def clear(self) -> None:
        """清空集合"""
        self._tree.clear()
    
    def to_list(self) -> List[T]:
        """转换为列表"""
        return self._tree.to_list()
    
    @property
    def size(self) -> int:
        return len(self._tree)
    
    @property
    def is_empty(self) -> bool:
        return self._tree.is_empty
    
    def __len__(self) -> int:
        return len(self._tree)
    
    def __contains__(self, key: T) -> bool:
        return key in self._tree
    
    def __iter__(self) -> Iterator[T]:
        return iter(self._tree)
    
    def __repr__(self) -> str:
        return f"ScapegoatTreeSet({self.to_list()})"


class ScapegoatTreeMultiSet(Generic[T]):
    """
    基于替罪羊树的可重复集合（多重集）实现
    
    支持重复元素，每个元素维护一个计数器
    
    示例:
        >>> ms = ScapegoatTreeMultiSet[str]()
        >>> ms.add("apple")
        >>> ms.add("apple")
        >>> ms.add("banana")
        >>> ms.count("apple")
        2
        >>> len(ms)
        3
    """
    
    def __init__(self, alpha: float = 0.7, comparator: Optional[Callable[[T, T], int]] = None):
        # 存储元素和计数的元组
        def _make_tuple_comparator():
            def _compare(a: Tuple[T, int], b: Tuple[T, int]) -> int:
                if comparator:
                    return comparator(a[0], b[0])
                if a[0] < b[0]:
                    return -1
                elif a[0] > b[0]:
                    return 1
                return 0
            return _compare
        
        self._tree = ScapegoatTree[Tuple[T, int]](
            alpha=alpha,
            comparator=_make_tuple_comparator()
        )
        self._total_count = 0
    
    def add(self, key: T, count: int = 1) -> None:
        """添加元素"""
        if count <= 0:
            return
        
        # 查找是否存在
        existing = self._tree.find((key, 0))
        if existing:
            # 更新计数
            self._tree.delete((key, 0))
            self._tree.insert((key, existing[1] + count))
        else:
            self._tree.insert((key, count))
        
        self._total_count += count
    
    def remove(self, key: T, count: int = 1) -> int:
        """移除元素，返回实际移除的数量"""
        existing = self._tree.find((key, 0))
        if not existing:
            return 0
        
        actual_remove = min(count, existing[1])
        self._tree.delete((key, 0))
        
        if existing[1] > actual_remove:
            self._tree.insert((key, existing[1] - actual_remove))
        
        self._total_count -= actual_remove
        return actual_remove
    
    def count(self, key: T) -> int:
        """获取元素的计数"""
        existing = self._tree.find((key, 0))
        return existing[1] if existing else 0
    
    def contains(self, key: T) -> bool:
        """检查元素是否存在"""
        return self.count(key) > 0
    
    def min(self) -> Optional[T]:
        """获取最小元素"""
        result = self._tree.min()
        return result[0] if result else None
    
    def max(self) -> Optional[T]:
        """获取最大元素"""
        result = self._tree.max()
        return result[0] if result else None
    
    def unique_elements(self) -> List[T]:
        """获取所有不重复的元素"""
        return [item[0] for item in self._tree]
    
    def to_list(self) -> List[T]:
        """转换为列表（包含重复元素）"""
        result = []
        for key, count in self._tree:
            result.extend([key] * count)
        return result
    
    def clear(self) -> None:
        """清空多重集"""
        self._tree.clear()
        self._total_count = 0
    
    @property
    def size(self) -> int:
        """获取元素总数（包含重复）"""
        return self._total_count
    
    @property
    def unique_size(self) -> int:
        """获取不重复元素的数量"""
        return len(self._tree)
    
    @property
    def is_empty(self) -> bool:
        return self._total_count == 0
    
    def __len__(self) -> int:
        return self._total_count
    
    def __contains__(self, key: T) -> bool:
        return self.contains(key)
    
    def __repr__(self) -> str:
        return f"ScapegoatTreeMultiSet({self.to_list()})"


def _cmp_result(a: Any, b: Any) -> int:
    """默认比较函数"""
    if a < b:
        return -1
    elif a > b:
        return 1
    return 0