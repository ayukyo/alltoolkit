"""
Red-Black Tree Utils - 红黑树工具模块

红黑树是一种自平衡二叉搜索树，具有以下性质：
1. 每个节点要么是红色，要么是黑色
2. 根节点是黑色
3. 所有叶子节点（NIL）是黑色
4. 红色节点的子节点必须是黑色（不能有连续红色节点）
5. 从任一节点到其每个叶子的所有简单路径都包含相同数目的黑色节点

时间复杂度：
- 查找：O(log n)
- 插入：O(log n)
- 删除：O(log n)

应用场景：
- 关联数组（C++ STL map/set）
- 进程调度
- 内存管理
- 文件系统
"""

from typing import TypeVar, Generic, Optional, Callable, List, Tuple, Any
from enum import Enum
import sys

T = TypeVar('T')


class Color(Enum):
    """红黑树节点颜色"""
    RED = True
    BLACK = False


class Node(Generic[T]):
    """红黑树节点"""
    
    __slots__ = ['key', 'value', 'color', 'left', 'right', 'parent']
    
    def __init__(self, key: T, value: Any = None, color: Color = Color.RED):
        self.key = key
        self.value = value
        self.color = color
        self.left: Optional['Node[T]'] = None
        self.right: Optional['Node[T]'] = None
        self.parent: Optional['Node[T]'] = None
    
    def __repr__(self) -> str:
        color_name = "R" if self.color == Color.RED else "B"
        return f"Node({self.key}, {color_name})"
    
    def is_red(self) -> bool:
        """检查节点是否为红色"""
        return self.color == Color.RED
    
    def is_black(self) -> bool:
        """检查节点是否为黑色"""
        return self.color == Color.BLACK


class RedBlackTree(Generic[T]):
    """
    红黑树实现
    
    特点：
    - 自动平衡，保证树的高度不超过 2*log2(n+1)
    - 支持高效的查找、插入、删除操作
    - 支持范围查询和有序遍历
    """
    
    def __init__(self):
        """初始化空的红黑树"""
        self._nil = Node(None, None, Color.BLACK)  # 哨兵节点
        self._nil.left = self._nil.right = self._nil.parent = self._nil
        self._root: Node[T] = self._nil
        self._size: int = 0
    
    @property
    def size(self) -> int:
        """返回树中节点数量"""
        return self._size
    
    @property
    def is_empty(self) -> bool:
        """检查树是否为空"""
        return self._size == 0
    
    def __len__(self) -> int:
        return self._size
    
    def __contains__(self, key: T) -> bool:
        node = self._search_node(key)
        return node != self._nil
    
    def contains(self, key: T) -> bool:
        """检查键是否存在"""
        return key in self
    
    def __iter__(self):
        """中序遍历迭代器"""
        return iter(self.inorder())
    
    # ==================== 基本操作 ====================
    
    def search(self, key: T) -> Optional[Any]:
        """
        查找键对应的值
        
        Args:
            key: 要查找的键
            
        Returns:
            找到的值，未找到返回 None
        """
        node = self._search_node(key)
        return node.value if node != self._nil else None
    
    def _search_node(self, key: T) -> Node[T]:
        """查找节点"""
        current = self._root
        while current != self._nil:
            if key == current.key:
                return current
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return self._nil
    
    def insert(self, key: T, value: Any = None) -> bool:
        """
        插入键值对
        
        Args:
            key: 键
            value: 值（可选）
            
        Returns:
            True 表示插入成功，False 表示键已存在
        """
        # 创建新节点
        new_node = Node(key, value, Color.RED)
        new_node.left = new_node.right = self._nil
        
        # 查找插入位置
        parent = self._nil
        current = self._root
        
        while current != self._nil:
            parent = current
            if key == current.key:
                # 键已存在，更新值
                current.value = value
                return False
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        
        # 设置新节点的父节点
        new_node.parent = parent
        
        if parent == self._nil:
            # 树为空，新节点成为根
            self._root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        self._size += 1
        
        # 修复红黑树性质
        self._fix_insert(new_node)
        
        return True
    
    def delete(self, key: T) -> bool:
        """
        删除键值对
        
        Args:
            key: 要删除的键
            
        Returns:
            True 表示删除成功，False 表示键不存在
        """
        node = self._search_node(key)
        if node == self._nil:
            return False
        
        self._delete_node(node)
        self._size -= 1
        return True
    
    def _delete_node(self, node: Node[T]):
        """删除节点的内部实现"""
        # 找到要删除的节点及其子节点
        y = node  # 要移除的节点
        y_original_color = y.color
        x = self._nil  # y 的子节点
        
        if node.left == self._nil:
            x = node.right
            self._transplant(node, node.right)
        elif node.right == self._nil:
            x = node.left
            self._transplant(node, node.left)
        else:
            # 有两个子节点，找后继
            y = self._minimum(node.right)
            y_original_color = y.color
            x = y.right
            
            if y.parent == node:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = node.right
                y.right.parent = y
            
            self._transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color
        
        # 如果删除的是黑色节点，需要修复
        if y_original_color == Color.BLACK:
            self._fix_delete(x)
    
    # ==================== 辅助操作 ====================
    
    def _transplant(self, u: Node[T], v: Node[T]):
        """用子树 v 替换子树 u"""
        if u.parent == self._nil:
            self._root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent
    
    def _minimum(self, node: Node[T]) -> Node[T]:
        """找到以 node 为根的子树的最小节点"""
        while node.left != self._nil:
            node = node.left
        return node
    
    def _maximum(self, node: Node[T]) -> Node[T]:
        """找到以 node 为根的子树的最大节点"""
        while node.right != self._nil:
            node = node.right
        return node
    
    def minimum(self) -> Optional[T]:
        """返回树中最小的键"""
        if self._root == self._nil:
            return None
        return self._minimum(self._root).key
    
    def maximum(self) -> Optional[T]:
        """返回树中最大的键"""
        if self._root == self._nil:
            return None
        return self._maximum(self._root).key
    
    # ==================== 旋转操作 ====================
    
    def _left_rotate(self, x: Node[T]):
        """左旋"""
        y = x.right
        x.right = y.left
        
        if y.left != self._nil:
            y.left.parent = x
        
        y.parent = x.parent
        
        if x.parent == self._nil:
            self._root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        
        y.left = x
        x.parent = y
    
    def _right_rotate(self, y: Node[T]):
        """右旋"""
        x = y.left
        y.left = x.right
        
        if x.right != self._nil:
            x.right.parent = y
        
        x.parent = y.parent
        
        if y.parent == self._nil:
            self._root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        
        x.right = y
        y.parent = x
    
    # ==================== 修复操作 ====================
    
    def _fix_insert(self, node: Node[T]):
        """插入后修复红黑树性质"""
        while node.parent.is_red():
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.is_red():
                    # Case 1: 叔叔是红色
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        # Case 2: 叔叔是黑色，节点是右子节点
                        node = node.parent
                        self._left_rotate(node)
                    # Case 3: 叔叔是黑色，节点是左子节点
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self._right_rotate(node.parent.parent)
            else:
                # 镜像情况
                uncle = node.parent.parent.left
                if uncle.is_red():
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self._left_rotate(node.parent.parent)
        
        self._root.color = Color.BLACK
    
    def _fix_delete(self, node: Node[T]):
        """删除后修复红黑树性质"""
        while node != self._root and node.is_black():
            if node == node.parent.left:
                sibling = node.parent.right
                if sibling.is_red():
                    # Case 1: 兄弟是红色
                    sibling.color = Color.BLACK
                    node.parent.color = Color.RED
                    self._left_rotate(node.parent)
                    sibling = node.parent.right
                
                if sibling.left.is_black() and sibling.right.is_black():
                    # Case 2: 兄弟的两个子节点都是黑色
                    sibling.color = Color.RED
                    node = node.parent
                else:
                    if sibling.right.is_black():
                        # Case 3: 兄弟的右子节点是黑色
                        sibling.left.color = Color.BLACK
                        sibling.color = Color.RED
                        self._right_rotate(sibling)
                        sibling = node.parent.right
                    # Case 4: 兄弟的右子节点是红色
                    sibling.color = node.parent.color
                    node.parent.color = Color.BLACK
                    sibling.right.color = Color.BLACK
                    self._left_rotate(node.parent)
                    node = self._root
            else:
                # 镜像情况
                sibling = node.parent.left
                if sibling.is_red():
                    sibling.color = Color.BLACK
                    node.parent.color = Color.RED
                    self._right_rotate(node.parent)
                    sibling = node.parent.left
                
                if sibling.right.is_black() and sibling.left.is_black():
                    sibling.color = Color.RED
                    node = node.parent
                else:
                    if sibling.left.is_black():
                        sibling.right.color = Color.BLACK
                        sibling.color = Color.RED
                        self._left_rotate(sibling)
                        sibling = node.parent.left
                    sibling.color = node.parent.color
                    node.parent.color = Color.BLACK
                    sibling.left.color = Color.BLACK
                    self._right_rotate(node.parent)
                    node = self._root
        
        node.color = Color.BLACK
    
    # ==================== 遍历操作 ====================
    
    def inorder(self) -> List[Tuple[T, Any]]:
        """中序遍历（升序）"""
        result = []
        self._inorder_helper(self._root, result)
        return result
    
    def _inorder_helper(self, node: Node[T], result: List):
        if node != self._nil:
            self._inorder_helper(node.left, result)
            result.append((node.key, node.value))
            self._inorder_helper(node.right, result)
    
    def preorder(self) -> List[Tuple[T, Any]]:
        """前序遍历"""
        result = []
        self._preorder_helper(self._root, result)
        return result
    
    def _preorder_helper(self, node: Node[T], result: List):
        if node != self._nil:
            result.append((node.key, node.value))
            self._preorder_helper(node.left, result)
            self._preorder_helper(node.right, result)
    
    def postorder(self) -> List[Tuple[T, Any]]:
        """后序遍历"""
        result = []
        self._postorder_helper(self._root, result)
        return result
    
    def _postorder_helper(self, node: Node[T], result: List):
        if node != self._nil:
            self._postorder_helper(node.left, result)
            self._postorder_helper(node.right, result)
            result.append((node.key, node.value))
    
    # ==================== Floor/Ceiling 查询 ====================
    
    def _find_floor(self, key: T) -> Optional[T]:
        """
        找到小于等于 key 的最大键
        
        Args:
            key: 目标键
            
        Returns:
            找到的键，不存在返回 None
        """
        floor = None
        current = self._root
        
        while current != self._nil:
            if key == current.key:
                return current.key
            elif key < current.key:
                current = current.left
            else:
                floor = current.key
                current = current.right
        
        return floor
    
    def _find_ceiling(self, key: T) -> Optional[T]:
        """
        找到大于等于 key 的最小键
        
        Args:
            key: 目标键
            
        Returns:
            找到的键，不存在返回 None
        """
        ceiling = None
        current = self._root
        
        while current != self._nil:
            if key == current.key:
                return current.key
            elif key > current.key:
                current = current.right
            else:
                ceiling = current.key
                current = current.left
        
        return ceiling
    
    # ==================== 范围查询 ====================
    
    def range_query(self, low: T, high: T) -> List[Tuple[T, Any]]:
        """
        范围查询：返回 [low, high] 范围内的所有键值对
        
        Args:
            low: 下界
            high: 上界
            
        Returns:
            范围内的键值对列表（升序）
        """
        result = []
        self._range_query_helper(self._root, low, high, result)
        return result
    
    def _range_query_helper(self, node: Node[T], low: T, high: T, result: List):
        if node == self._nil:
            return
        
        # 如果当前节点大于 low，递归左子树
        if low < node.key:
            self._range_query_helper(node.left, low, high, result)
        
        # 如果当前节点在范围内，添加到结果
        if low <= node.key <= high:
            result.append((node.key, node.value))
        
        # 如果当前节点小于 high，递归右子树
        if node.key < high:
            self._range_query_helper(node.right, low, high, result)
    
    # ==================== 前驱后继 ====================
    
    def successor(self, key: T) -> Optional[T]:
        """
        查找键的后继（比 key 大的最小键）
        
        Args:
            key: 要查找后继的键
            
        Returns:
            后继键，不存在返回 None
        """
        node = self._search_node(key)
        if node == self._nil:
            return None
        
        if node.right != self._nil:
            return self._minimum(node.right).key
        
        parent = node.parent
        while parent != self._nil and node == parent.right:
            node = parent
            parent = parent.parent
        
        return parent.key if parent != self._nil else None
    
    def predecessor(self, key: T) -> Optional[T]:
        """
        查找键的前驱（比 key 小的最大键）
        
        Args:
            key: 要查找前驱的键
            
        Returns:
            前驱键，不存在返回 None
        """
        node = self._search_node(key)
        if node == self._nil:
            return None
        
        if node.left != self._nil:
            return self._maximum(node.left).key
        
        parent = node.parent
        while parent != self._nil and node == parent.left:
            node = parent
            parent = parent.parent
        
        return parent.key if parent != self._nil else None
    
    # ==================== 排名操作 ====================
    
    def rank(self, key: T) -> int:
        """
        返回键的排名（第几小）
        
        Args:
            key: 要查询的键
            
        Returns:
            排名（1-based），不存在返回 -1
        """
        node = self._search_node(key)
        if node == self._nil:
            return -1
        
        r = 1
        # 计算左子树大小 + 1
        r += self._count_nodes(node.left)
        
        # 向上遍历
        current = node
        while current.parent != self._nil:
            if current == current.parent.right:
                r += self._count_nodes(current.parent.left) + 1
            current = current.parent
        
        return r
    
    def _count_nodes(self, node: Node[T]) -> int:
        """计算子树节点数"""
        if node == self._nil:
            return 0
        return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)
    
    # ==================== 树属性 ====================
    
    def height(self) -> int:
        """返回树的高度"""
        return self._height_helper(self._root)
    
    def _height_helper(self, node: Node[T]) -> int:
        if node == self._nil:
            return 0
        return 1 + max(
            self._height_helper(node.left),
            self._height_helper(node.right)
        )
    
    def black_height(self) -> int:
        """返回黑高度（从根到叶子的黑色节点数）"""
        count = 0
        node = self._root
        while node != self._nil:
            if node.is_black():
                count += 1
            node = node.left
        return count
    
    def is_valid(self) -> bool:
        """
        验证是否为合法的红黑树
        
        Returns:
            True 如果满足所有红黑树性质
        """
        if self._root == self._nil:
            return True
        
        # 性质 2: 根节点是黑色
        if self._root.is_red():
            return False
        
        # 性质 4 & 5: 通过遍历验证
        try:
            self._validate_properties(self._root)
            return True
        except ValueError:
            return False
    
    def _validate_properties(self, node: Node[T]) -> int:
        """
        验证红黑树性质，返回黑高度
        
        Raises:
            ValueError: 如果违反任何性质
        """
        if node == self._nil:
            return 0
        
        # 性质 4: 红色节点的子节点必须是黑色
        if node.is_red():
            if node.left.is_red() or node.right.is_red():
                raise ValueError("红色节点有红色子节点")
        
        left_bh = self._validate_properties(node.left)
        right_bh = self._validate_properties(node.right)
        
        # 性质 5: 左右子树的黑高度必须相等
        if left_bh != right_bh:
            raise ValueError(f"黑高度不等: 左={left_bh}, 右={right_bh}")
        
        return left_bh + (1 if node.is_black() else 0)
    
    # ==================== 工具方法 ====================
    
    def to_list(self) -> List[Tuple[T, Any]]:
        """转换为列表（中序）"""
        return self.inorder()
    
    def clear(self):
        """清空树"""
        self._root = self._nil
        self._size = 0
    
    def __str__(self) -> str:
        """字符串表示"""
        items = self.inorder()
        if not items:
            return "{}"
        return "{" + ", ".join(f"{k}: {v}" for k, v in items) + "}"
    
    def __repr__(self) -> str:
        return f"RedBlackTree(size={self._size})"


class RedBlackTreeSet(Generic[T]):
    """
    基于红黑树的集合实现
    
    支持高效的插入、删除、查找和范围查询
    """
    
    def __init__(self):
        self._tree = RedBlackTree[T]()
    
    def add(self, key: T) -> bool:
        """添加元素"""
        return self._tree.insert(key, True)
    
    def remove(self, key: T) -> bool:
        """移除元素"""
        return self._tree.delete(key)
    
    def contains(self, key: T) -> bool:
        """检查元素是否存在"""
        return key in self._tree
    
    def __contains__(self, key: T) -> bool:
        return self.contains(key)
    
    def __len__(self) -> int:
        return len(self._tree)
    
    def __iter__(self):
        for key, _ in self._tree:
            yield key
    
    def minimum(self) -> Optional[T]:
        """返回最小元素"""
        return self._tree.minimum()
    
    def maximum(self) -> Optional[T]:
        """返回最大元素"""
        return self._tree.maximum()
    
    def range_query(self, low: T, high: T) -> List[T]:
        """范围查询"""
        return [k for k, _ in self._tree.range_query(low, high)]
    
    def successor(self, key: T) -> Optional[T]:
        """查找后继"""
        return self._tree.successor(key)
    
    def predecessor(self, key: T) -> Optional[T]:
        """查找前驱"""
        return self._tree.predecessor(key)
    
    def is_valid(self) -> bool:
        """验证红黑树性质"""
        return self._tree.is_valid()


class RedBlackTreeMap(Generic[T]):
    """
    基于红黑树的有序映射实现
    
    支持高效的键值存储和范围查询
    """
    
    def __init__(self):
        self._tree = RedBlackTree[T]()
    
    @property
    def is_empty(self) -> bool:
        """检查是否为空"""
        return len(self._tree) == 0
    
    def put(self, key: T, value: Any) -> Optional[Any]:
        """
        插入键值对
        
        Returns:
            如果键已存在，返回旧值；否则返回 None
        """
        node = self._tree._search_node(key)
        if node != self._tree._nil:
            old_value = node.value
            node.value = value
            return old_value
        self._tree.insert(key, value)
        return None
    
    def get(self, key: T, default: Any = None) -> Any:
        """获取键对应的值"""
        value = self._tree.search(key)
        return value if value is not None else default
    
    def remove(self, key: T) -> Optional[Any]:
        """移除键值对，返回被移除的值"""
        node = self._tree._search_node(key)
        if node == self._tree._nil:
            return None
        value = node.value
        self._tree.delete(key)
        return value
    
    def __getitem__(self, key: T) -> Any:
        value = self._tree.search(key)
        if value is None:
            raise KeyError(key)
        return value
    
    def __setitem__(self, key: T, value: Any):
        self._tree.insert(key, value)
    
    def __delitem__(self, key: T):
        if not self._tree.delete(key):
            raise KeyError(key)
    
    def __contains__(self, key: T) -> bool:
        return key in self._tree
    
    def __len__(self) -> int:
        return len(self._tree)
    
    def __iter__(self):
        for key, _ in self._tree:
            yield key
    
    def keys(self) -> List[T]:
        """返回所有键"""
        return [k for k, _ in self._tree.inorder()]
    
    def values(self) -> List[Any]:
        """返回所有值"""
        return [v for _, v in self._tree.inorder()]
    
    def items(self) -> List[Tuple[T, Any]]:
        """返回所有键值对"""
        return self._tree.inorder()
    
    def first_key(self) -> Optional[T]:
        """返回最小键"""
        return self._tree.minimum()
    
    def last_key(self) -> Optional[T]:
        """返回最大键"""
        return self._tree.maximum()
    
    def range_query(self, low: T, high: T) -> List[Tuple[T, Any]]:
        """范围查询"""
        return self._tree.range_query(low, high)
    
    def floor_key(self, key: T) -> Optional[T]:
        """返回小于等于 key 的最大键"""
        # 使用专用方法查找 floor
        return self._tree._find_floor(key)
    
    def ceiling_key(self, key: T) -> Optional[T]:
        """返回大于等于 key 的最小键"""
        # 使用专用方法查找 ceiling
        return self._tree._find_ceiling(key)
    
    def is_valid(self) -> bool:
        """验证红黑树性质"""
        return self._tree.is_valid()


# ==================== 便捷函数 ====================

def create_tree(items: List[Tuple[T, Any]] = None) -> RedBlackTree[T]:
    """
    从键值对列表创建红黑树
    
    Args:
        items: 键值对列表
        
    Returns:
        创建的红黑树
    """
    tree = RedBlackTree[T]()
    if items:
        for key, value in items:
            tree.insert(key, value)
    return tree


def create_set(items: List[T] = None) -> RedBlackTreeSet[T]:
    """
    从元素列表创建红黑树集合
    
    Args:
        items: 元素列表
        
    Returns:
        创建的红黑树集合
    """
    s = RedBlackTreeSet[T]()
    if items:
        for item in items:
            s.add(item)
    return s


def create_map(items: dict = None) -> RedBlackTreeMap[T]:
    """
    从字典创建红黑树映射
    
    Args:
        items: 字典
        
    Returns:
        创建的红黑树映射
    """
    m = RedBlackTreeMap[T]()
    if items:
        for key, value in items.items():
            m.put(key, value)
    return m


if __name__ == "__main__":
    # 简单测试
    print("=== Red-Black Tree Demo ===\n")
    
    # 创建树并插入数据
    tree = RedBlackTree[int]()
    data = [7, 3, 18, 10, 22, 8, 11, 26]
    
    print(f"插入数据: {data}")
    for key in data:
        tree.insert(key, f"value_{key}")
    
    print(f"\n树大小: {tree.size}")
    print(f"树高度: {tree.height()}")
    print(f"黑高度: {tree.black_height()}")
    print(f"是否合法: {tree.is_valid()}")
    
    print(f"\n中序遍历: {tree.inorder()}")
    print(f"最小值: {tree.minimum()}")
    print(f"最大值: {tree.maximum()}")
    
    print(f"\n范围查询 [8, 18]: {tree.range_query(8, 18)}")
    print(f"键 10 的后继: {tree.successor(10)}")
    print(f"键 10 的前驱: {tree.predecessor(10)}")
    
    # 测试删除
    print(f"\n删除键 18...")
    tree.delete(18)
    print(f"删除后中序遍历: {tree.inorder()}")
    print(f"是否合法: {tree.is_valid()}")
    
    # 测试 Set
    print("\n=== RedBlackTreeSet Demo ===\n")
    rb_set = create_set([5, 2, 8, 1, 9, 3])
    print(f"集合: {list(rb_set)}")
    print(f"包含 5: {5 in rb_set}")
    print(f"包含 10: {10 in rb_set}")
    print(f"范围查询 [3, 8]: {rb_set.range_query(3, 8)}")
    
    # 测试 Map
    print("\n=== RedBlackTreeMap Demo ===\n")
    rb_map = create_map({"apple": 1, "banana": 2, "cherry": 3})
    rb_map["date"] = 4
    print(f"Map: {dict(rb_map.items())}")
    print(f"banana 的值: {rb_map['banana']}")
    print(f"范围查询 ['b', 'd']: {rb_map.range_query('b', 'd')}")