"""
Treap (树堆) 工具模块

Treap 是一种随机化平衡二叉搜索树，结合了二叉搜索树和堆的特性。
- 二叉搜索树性质：左子树所有节点值 < 当前节点值 < 右子树所有节点值
- 堆性质：每个节点的优先级 >= 其子节点的优先级

通过随机优先级，Treap 在期望情况下保持 O(log n) 的高度，
实现高效的插入、删除、查找等操作。

零外部依赖，纯 Python 实现。
"""

import random
from typing import Optional, List, Any, Callable, TypeVar, Generic, Tuple

T = TypeVar('T')


class TreapNode(Generic[T]):
    """Treap 节点类"""
    
    __slots__ = ['key', 'priority', 'left', 'right', 'size', 'count']
    
    def __init__(self, key: T, priority: Optional[float] = None):
        """
        初始化 Treap 节点
        
        Args:
            key: 节点键值
            priority: 节点优先级（默认随机生成）
        """
        self.key = key
        self.priority = priority if priority is not None else random.random()
        self.left: Optional['TreapNode[T]'] = None
        self.right: Optional['TreapNode[T]'] = None
        self.size = 1  # 以该节点为根的子树大小
        self.count = 1  # 相同键值的数量（支持重复元素）
    
    def update_size(self) -> None:
        """更新子树大小"""
        self.size = self.count
        if self.left:
            self.size += self.left.size
        if self.right:
            self.size += self.right.size
    
    def __repr__(self) -> str:
        return f"TreapNode(key={self.key}, priority={self.priority:.4f})"


class Treap(Generic[T]):
    """
    Treap（树堆）数据结构
    
    特性：
    - 支持重复元素
    - O(log n) 期望时间复杂度的插入、删除、查找
    - 支持范围查询、第 k 小元素查询
    - 支持前驱后继查询
    """
    
    def __init__(self, keys: Optional[List[T]] = None, 
                 key_func: Optional[Callable[[T], Any]] = None):
        """
        初始化 Treap
        
        Args:
            keys: 初始键值列表
            key_func: 键值比较函数（用于自定义排序）
        """
        self.root: Optional[TreapNode[T]] = None
        self.key_func = key_func
        self._compare: Callable[[T, T], int] = self._default_compare
        
        if keys:
            for key in keys:
                self.insert(key)
    
    def _default_compare(self, a: T, b: T) -> int:
        """默认比较函数"""
        if self.key_func:
            a_val = self.key_func(a)
            b_val = self.key_func(b)
            # 先比较 key_func 的值
            if a_val < b_val:
                return -1
            elif a_val > b_val:
                return 1
            # 如果 key_func 的值相同，再用原始值比较（保证不同元素可共存）
            try:
                if a < b:
                    return -1
                elif a > b:
                    return 1
            except TypeError:
                # 无法比较的原始值，视为相等（允许重复）
                pass
            return 0
        else:
            if a < b:
                return -1
            elif a > b:
                return 1
            return 0
    
    def _get_size(self, node: Optional[TreapNode[T]]) -> int:
        """获取子树大小"""
        return node.size if node else 0
    
    def _rotate_right(self, node: TreapNode[T]) -> TreapNode[T]:
        """右旋"""
        left_child = node.left
        if left_child is None:
            return node
        
        node.left = left_child.right
        left_child.right = node
        
        node.update_size()
        left_child.update_size()
        
        return left_child
    
    def _rotate_left(self, node: TreapNode[T]) -> TreapNode[T]:
        """左旋"""
        right_child = node.right
        if right_child is None:
            return node
        
        node.right = right_child.left
        right_child.left = node
        
        node.update_size()
        right_child.update_size()
        
        return right_child
    
    def insert(self, key: T, priority: Optional[float] = None) -> None:
        """
        插入键值
        
        Args:
            key: 要插入的键值
            priority: 可选的优先级（主要用于测试）
        """
        self.root = self._insert(self.root, key, priority)
    
    def _insert(self, node: Optional[TreapNode[T]], key: T, 
                priority: Optional[float] = None) -> TreapNode[T]:
        """递归插入"""
        if node is None:
            return TreapNode(key, priority)
        
        cmp = self._compare(key, node.key)
        
        if cmp < 0:
            node.left = self._insert(node.left, key, priority)
            if node.left and node.left.priority > node.priority:
                node = self._rotate_right(node)
        elif cmp > 0:
            node.right = self._insert(node.right, key, priority)
            if node.right and node.right.priority > node.priority:
                node = self._rotate_left(node)
        else:
            # 键值相同，增加计数
            node.count += 1
        
        node.update_size()
        return node
    
    def delete(self, key: T) -> bool:
        """
        删除键值
        
        Args:
            key: 要删除的键值
            
        Returns:
            是否成功删除
        """
        result = [False]
        self.root = self._delete(self.root, key, result)
        return result[0]
    
    def _delete(self, node: Optional[TreapNode[T]], key: T, 
                result: List[bool]) -> Optional[TreapNode[T]]:
        """递归删除"""
        if node is None:
            result[0] = False
            return None
        
        cmp = self._compare(key, node.key)
        
        if cmp < 0:
            node.left = self._delete(node.left, key, result)
        elif cmp > 0:
            node.right = self._delete(node.right, key, result)
        else:
            # 找到目标节点
            result[0] = True
            if node.count > 1:
                node.count -= 1
            else:
                # 需要完全删除节点
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
                else:
                    # 两个子节点都存在
                    if node.left.priority > node.right.priority:
                        node = self._rotate_right(node)
                        node.right = self._delete(node.right, key, result)
                    else:
                        node = self._rotate_left(node)
                        node.left = self._delete(node.left, key, result)
        
        if node:
            node.update_size()
        return node
    
    def search(self, key: T) -> int:
        """
        查找键值的数量
        
        Args:
            key: 要查找的键值
            
        Returns:
            该键值的数量（0 表示不存在）
        """
        node = self.root
        while node:
            cmp = self._compare(key, node.key)
            if cmp < 0:
                node = node.left
            elif cmp > 0:
                node = node.right
            else:
                return node.count
        return 0
    
    def contains(self, key: T) -> bool:
        """检查是否包含键值"""
        return self.search(key) > 0
    
    def __contains__(self, key: T) -> bool:
        return self.contains(key)
    
    def __len__(self) -> int:
        return self._get_size(self.root)
    
    def is_empty(self) -> bool:
        """检查是否为空"""
        return self.root is None
    
    def get_min(self) -> Optional[T]:
        """获取最小键值"""
        if self.root is None:
            return None
        node = self.root
        while node.left:
            node = node.left
        return node.key
    
    def get_max(self) -> Optional[T]:
        """获取最大键值"""
        if self.root is None:
            return None
        node = self.root
        while node.right:
            node = node.right
        return node.key
    
    def kth_smallest(self, k: int) -> Optional[T]:
        """
        获取第 k 小的元素（1-indexed）
        
        Args:
            k: 排名（从 1 开始）
            
        Returns:
            第 k 小的键值，如果 k 超出范围返回 None
        """
        if k < 1 or k > len(self):
            return None
        return self._kth(self.root, k)
    
    def _kth(self, node: Optional[TreapNode[T]], k: int) -> Optional[T]:
        """查找第 k 小元素"""
        if node is None:
            return None
        
        left_size = self._get_size(node.left)
        
        if k <= left_size:
            return self._kth(node.left, k)
        elif k <= left_size + node.count:
            return node.key
        else:
            return self._kth(node.right, k - left_size - node.count)
    
    def rank(self, key: T) -> int:
        """
        获取键值的排名（1-indexed）
        
        Args:
            key: 键值
            
        Returns:
            排名（从 1 开始），如果键值不存在返回应该插入的位置
        """
        return self._rank(self.root, key)
    
    def _rank(self, node: Optional[TreapNode[T]], key: T) -> int:
        """计算键值排名"""
        if node is None:
            return 1
        
        cmp = self._compare(key, node.key)
        
        if cmp < 0:
            return self._rank(node.left, key)
        elif cmp > 0:
            return self._get_size(node.left) + node.count + self._rank(node.right, key)
        else:
            return self._get_size(node.left) + 1
    
    def predecessor(self, key: T) -> Optional[T]:
        """
        获取键值的前驱（小于 key 的最大值）
        
        Args:
            key: 键值
            
        Returns:
            前驱键值，如果不存在返回 None
        """
        result = None
        node = self.root
        
        while node:
            cmp = self._compare(key, node.key)
            if cmp <= 0:
                node = node.left
            else:
                result = node.key
                node = node.right
        
        return result
    
    def successor(self, key: T) -> Optional[T]:
        """
        获取键值的后继（大于 key 的最小值）
        
        Args:
            key: 键值
            
        Returns:
            后继键值，如果不存在返回 None
        """
        result = None
        node = self.root
        
        while node:
            cmp = self._compare(key, node.key)
            if cmp >= 0:
                node = node.right
            else:
                result = node.key
                node = node.left
        
        return result
    
    def count_range(self, low: T, high: T) -> int:
        """
        统计区间 [low, high] 内的元素数量
        
        Args:
            low: 下界（包含）
            high: 上界（包含）
            
        Returns:
            区间内元素数量
        """
        return self._count_range(self.root, low, high)
    
    def _count_range(self, node: Optional[TreapNode[T]], low: T, high: T) -> int:
        """统计区间内元素数量"""
        if node is None:
            return 0
        
        cmp_low = self._compare(node.key, low)
        cmp_high = self._compare(node.key, high)
        
        if cmp_low < 0:
            # 当前节点小于下界，搜索右子树
            return self._count_range(node.right, low, high)
        elif cmp_high > 0:
            # 当前节点大于上界，搜索左子树
            return self._count_range(node.left, low, high)
        else:
            # 当前节点在区间内
            count = node.count
            count += self._count_range(node.left, low, high)
            count += self._count_range(node.right, low, high)
            return count
    
    def range_query(self, low: T, high: T) -> List[T]:
        """
        查询区间 [low, high] 内的所有元素
        
        Args:
            low: 下界（包含）
            high: 上界（包含）
            
        Returns:
            排序后的元素列表
        """
        result: List[T] = []
        self._range_query(self.root, low, high, result)
        return result
    
    def _range_query(self, node: Optional[TreapNode[T]], low: T, high: T, 
                     result: List[T]) -> None:
        """区间查询递归实现"""
        if node is None:
            return
        
        cmp_low = self._compare(node.key, low)
        cmp_high = self._compare(node.key, high)
        
        # 如果节点大于下界，搜索左子树
        if cmp_low > 0:
            self._range_query(node.left, low, high, result)
        
        # 如果节点在区间内
        if cmp_low >= 0 and cmp_high <= 0:
            result.extend([node.key] * node.count)
        
        # 如果节点小于上界，搜索右子树
        if cmp_high < 0:
            self._range_query(node.right, low, high, result)
    
    def to_sorted_list(self) -> List[T]:
        """转换为排序后的列表"""
        result: List[T] = []
        self._inorder(self.root, result)
        return result
    
    def _inorder(self, node: Optional[TreapNode[T]], result: List[T]) -> None:
        """中序遍历"""
        if node is None:
            return
        self._inorder(node.left, result)
        result.extend([node.key] * node.count)
        self._inorder(node.right, result)
    
    def clear(self) -> None:
        """清空 Treap"""
        self.root = None
    
    def get_height(self) -> int:
        """获取树的高度"""
        return self._get_height(self.root)
    
    def _get_height(self, node: Optional[TreapNode[T]]) -> int:
        """递归计算高度"""
        if node is None:
            return 0
        return 1 + max(self._get_height(node.left), self._get_height(node.right))
    
    def merge(self, other: 'Treap[T]') -> 'Treap[T]':
        """
        合并另一个 Treap（要求所有键值都小于当前 Treap 或都大于）
        
        Args:
            other: 要合并的 Treap
            
        Returns:
            合并后的新 Treap
        """
        # 创建新 Treap 并复制所有元素
        result = Treap(key_func=self.key_func)
        for key in self.to_sorted_list():
            result.insert(key)
        for key in other.to_sorted_list():
            result.insert(key)
        return result
    
    def split(self, key: T) -> Tuple['Treap[T]', 'Treap[T]']:
        """
        按 key 分裂为两个 Treap
        - 第一个包含所有小于 key 的元素
        - 第二个包含所有大于等于 key 的元素
        
        Args:
            key: 分裂点
            
        Returns:
            两个 Treap 的元组
        """
        left_keys: List[T] = []
        right_keys: List[T] = []
        
        for k in self.to_sorted_list():
            if self._compare(k, key) < 0:
                left_keys.append(k)
            else:
                right_keys.append(k)
        
        left_treap = Treap(left_keys, self.key_func)
        right_treap = Treap(right_keys, self.key_func)
        
        return left_treap, right_treap
    
    def __iter__(self):
        """迭代器（中序遍历）"""
        return iter(self.to_sorted_list())
    
    def __repr__(self) -> str:
        return f"Treap({self.to_sorted_list()})"


class ImplicitTreap(Generic[T]):
    """
    隐式 Treap（按位置索引）
    
    支持在任意位置插入/删除元素，维护序列。
    用于实现高效序列操作。
    """
    
    __slots__ = ['root', '_size']
    
    def __init__(self, values: Optional[List[T]] = None):
        """
        初始化隐式 Treap
        
        Args:
            values: 初始值列表
        """
        self.root: Optional['ImplicitTreapNode[T]'] = None
        self._size = 0
        
        if values:
            for i, v in enumerate(values):
                self.insert_at(i, v)
    
    def _get_size(self, node) -> int:
        return node.size if node else 0
    
    def _update(self, node) -> None:
        if node:
            node.size = 1 + self._get_size(node.left) + self._get_size(node.right)
    
    def _split(self, node, pos: int) -> Tuple:
        """
        按位置分裂
        
        Args:
            node: 当前节点
            pos: 分裂位置（左边保留 pos 个元素）
        """
        if node is None:
            return None, None
        
        left_size = self._get_size(node.left)
        
        if pos <= left_size:
            left, right = self._split(node.left, pos)
            node.left = right
            self._update(node)
            return left, node
        else:
            left, right = self._split(node.right, pos - left_size - 1)
            node.right = left
            self._update(node)
            return node, right
    
    def _merge(self, left, right):
        """合并两个 Treap"""
        if left is None:
            return right
        if right is None:
            return left
        
        if left.priority > right.priority:
            left.right = self._merge(left.right, right)
            self._update(left)
            return left
        else:
            right.left = self._merge(left, right.left)
            self._update(right)
            return right
    
    def _create_node(self, value: T):
        """创建新节点"""
        node = ImplicitTreapNode(value)
        return node
    
    def insert_at(self, pos: int, value: T) -> None:
        """
        在指定位置插入元素
        
        Args:
            pos: 插入位置（0-indexed）
            value: 要插入的值
        """
        if pos < 0 or pos > self._size:
            raise IndexError(f"Position {pos} out of range [0, {self._size}]")
        
        left, right = self._split(self.root, pos)
        new_node = self._create_node(value)
        self.root = self._merge(self._merge(left, new_node), right)
        self._size += 1
    
    def delete_at(self, pos: int) -> T:
        """
        删除指定位置的元素
        
        Args:
            pos: 删除位置（0-indexed）
            
        Returns:
            被删除的元素
        """
        if pos < 0 or pos >= self._size:
            raise IndexError(f"Position {pos} out of range [0, {self._size})")
        
        left, mid_right = self._split(self.root, pos)
        mid, right = self._split(mid_right, 1)
        
        self.root = self._merge(left, right)
        self._size -= 1
        
        return mid.value if mid else None
    
    def get_at(self, pos: int) -> T:
        """
        获取指定位置的元素
        
        Args:
            pos: 位置（0-indexed）
            
        Returns:
            该位置的元素
        """
        if pos < 0 or pos >= self._size:
            raise IndexError(f"Position {pos} out of range [0, {self._size})")
        
        node = self.root
        while node:
            left_size = self._get_size(node.left)
            if pos < left_size:
                node = node.left
            elif pos == left_size:
                return node.value
            else:
                pos -= left_size + 1
                node = node.right
        
        raise IndexError("Unexpected error in get_at")
    
    def set_at(self, pos: int, value: T) -> None:
        """
        设置指定位置的元素
        
        Args:
            pos: 位置（0-indexed）
            value: 新值
        """
        if pos < 0 or pos >= self._size:
            raise IndexError(f"Position {pos} out of range [0, {self._size})")
        
        # 通过删除和插入实现
        old_value = self.delete_at(pos)
        self.insert_at(pos, value)
    
    def reverse_range(self, left: int, right: int) -> None:
        """
        反转区间 [left, right) 内的元素
        
        Args:
            left: 左边界（包含）
            right: 右边界（不包含）
        """
        if left < 0 or right > self._size or left >= right:
            raise IndexError(f"Invalid range [{left}, {right})")
        
        # 提取区间
        l, mr = self._split(self.root, left)
        m, r = self._split(mr, right - left)
        
        # 反转中间部分
        m = self._reverse(m)
        
        # 合并回去
        self.root = self._merge(l, self._merge(m, r))
    
    def _reverse(self, node):
        """递归反转子树"""
        if node is None:
            return None
        node.left, node.right = node.right, node.left
        node.reversed = not getattr(node, 'reversed', False)
        self._reverse(node.left)
        self._reverse(node.right)
        return node
    
    def to_list(self) -> List[T]:
        """转换为列表"""
        result: List[T] = []
        self._to_list(self.root, result)
        return result
    
    def _to_list(self, node, result: List[T]) -> None:
        """中序遍历"""
        if node is None:
            return
        self._to_list(node.left, result)
        result.append(node.value)
        self._to_list(node.right, result)
    
    def __len__(self) -> int:
        return self._size
    
    def __getitem__(self, pos: int) -> T:
        return self.get_at(pos)
    
    def __setitem__(self, pos: int, value: T) -> None:
        self.set_at(pos, value)
    
    def __repr__(self) -> str:
        return f"ImplicitTreap({self.to_list()})"


class ImplicitTreapNode(Generic[T]):
    """隐式 Treap 节点"""
    
    __slots__ = ['value', 'priority', 'left', 'right', 'size', 'reversed']
    
    def __init__(self, value: T):
        self.value = value
        self.priority = random.random()
        self.left: Optional['ImplicitTreapNode[T]'] = None
        self.right: Optional['ImplicitTreapNode[T]'] = None
        self.size = 1
        self.reversed = False
    
    def __repr__(self) -> str:
        return f"ImplicitTreapNode(value={self.value})"


# 便捷函数
def create_treap(keys: List[T], key_func: Optional[Callable[[T], Any]] = None) -> Treap[T]:
    """
    创建 Treap 的便捷函数
    
    Args:
        keys: 键值列表
        key_func: 可选的键值比较函数
        
    Returns:
        新的 Treap 实例
    """
    return Treap(keys, key_func)


def create_implicit_treap(values: List[T]) -> ImplicitTreap[T]:
    """
    创建隐式 Treap 的便捷函数
    
    Args:
        values: 值列表
        
    Returns:
        新的 ImplicitTreap 实例
    """
    return ImplicitTreap(values)


# 导出
__all__ = [
    'Treap',
    'TreapNode',
    'ImplicitTreap',
    'ImplicitTreapNode',
    'create_treap',
    'create_implicit_treap',
]