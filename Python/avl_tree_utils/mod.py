"""
AllToolkit - Python AVL Tree Utilities

零依赖的 AVL 树实现，仅使用 Python 标准库
支持：自平衡二叉搜索树、插入、删除、查找、遍历、范围查询

@author AllToolkit
@version 1.0.0
"""

from typing import TypeVar, Generic, Optional, List, Callable, Iterator, Tuple, Any
from collections import deque
import math

T = TypeVar('T')


class AVLNode(Generic[T]):
    """AVL 树节点"""
    
    __slots__ = ['key', 'value', 'left', 'right', 'height', 'size']
    
    def __init__(self, key: T, value: Any = None):
        self.key = key
        self.value = value  # 可选的关联值
        self.left: Optional['AVLNode[T]'] = None
        self.right: Optional['AVLNode[T]'] = None
        self.height: int = 1  # 节点高度
        self.size: int = 1    # 子树大小（节点数）
    
    def __repr__(self) -> str:
        return f"AVLNode({self.key})"
    
    def update_height(self) -> None:
        """更新节点高度"""
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        self.height = max(left_height, right_height) + 1
    
    def update_size(self) -> None:
        """更新子树大小"""
        left_size = self.left.size if self.left else 0
        right_size = self.right.size if self.right else 0
        self.size = left_size + right_size + 1
    
    def balance_factor(self) -> int:
        """计算平衡因子（左子树高度 - 右子树高度）"""
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        return left_height - right_height
    
    def is_balanced(self) -> bool:
        """检查节点是否平衡"""
        return abs(self.balance_factor()) <= 1


class AVLTree(Generic[T]):
    """
    AVL 树 - 自平衡二叉搜索树
    
    特性：
    - 任何节点的两个子树高度差不超过 1
    - 查找、插入、删除操作时间复杂度 O(log n)
    - 支持范围查询、顺序统计
    """
    
    def __init__(self, allow_duplicates: bool = False):
        """
        初始化 AVL 树
        
        Args:
            allow_duplicates: 是否允许重复键
        """
        self._root: Optional[AVLNode[T]] = None
        self._allow_duplicates = allow_duplicates
        self._count = 0
    
    # ==================== 公共属性 ====================
    
    @property
    def root(self) -> Optional[AVLNode[T]]:
        """获取根节点"""
        return self._root
    
    @property
    def size(self) -> int:
        """获取树的节点数"""
        return self._count
    
    @property
    def height(self) -> int:
        """获取树的高度"""
        return self._root.height if self._root else 0
    
    @property
    def is_empty(self) -> bool:
        """检查树是否为空"""
        return self._root is None
    
    @property
    def allow_duplicates(self) -> bool:
        """是否允许重复键"""
        return self._allow_duplicates
    
    # ==================== 查找操作 ====================
    
    def search(self, key: T) -> Optional[AVLNode[T]]:
        """
        查找键对应的节点
        
        Args:
            key: 要查找的键
            
        Returns:
            找到的节点，未找到返回 None
        """
        return self._search(self._root, key)
    
    def _search(self, node: Optional[AVLNode[T]], key: T) -> Optional[AVLNode[T]]:
        """递归查找"""
        if node is None:
            return None
        
        if key == node.key:
            return node
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)
    
    def contains(self, key: T) -> bool:
        """检查键是否存在"""
        return self.search(key) is not None
    
    def get_value(self, key: T) -> Any:
        """获取键关联的值"""
        node = self.search(key)
        return node.value if node else None
    
    def find_min(self) -> Optional[AVLNode[T]]:
        """查找最小键节点"""
        if self._root is None:
            return None
        return self._find_min(self._root)
    
    def _find_min(self, node: AVLNode[T]) -> AVLNode[T]:
        """递归查找最小节点"""
        while node.left:
            node = node.left
        return node
    
    def find_max(self) -> Optional[AVLNode[T]]:
        """查找最大键节点"""
        if self._root is None:
            return None
        return self._find_max(self._root)
    
    def _find_max(self, node: AVLNode[T]) -> AVLNode[T]:
        """递归查找最大节点"""
        while node.right:
            node = node.right
        return node
    
    def find_floor(self, key: T) -> Optional[AVLNode[T]]:
        """
        查找小于等于 key 的最大节点
        
        Args:
            key: 目标键
            
        Returns:
            Floor 节点，不存在返回 None
        """
        return self._find_floor(self._root, key)
    
    def _find_floor(self, node: Optional[AVLNode[T]], key: T) -> Optional[AVLNode[T]]:
        """递归查找 floor"""
        if node is None:
            return None
        
        if key == node.key:
            return node
        
        if key < node.key:
            return self._find_floor(node.left, key)
        
        # key > node.key，当前节点可能是 floor
        floor = self._find_floor(node.right, key)
        return floor if floor else node
    
    def find_ceiling(self, key: T) -> Optional[AVLNode[T]]:
        """
        查找大于等于 key 的最小节点
        
        Args:
            key: 目标键
            
        Returns:
            Ceiling 节点，不存在返回 None
        """
        return self._find_ceiling(self._root, key)
    
    def _find_ceiling(self, node: Optional[AVLNode[T]], key: T) -> Optional[AVLNode[T]]:
        """递归查找 ceiling"""
        if node is None:
            return None
        
        if key == node.key:
            return node
        
        if key > node.key:
            return self._find_ceiling(node.right, key)
        
        # key < node.key，当前节点可能是 ceiling
        ceiling = self._find_ceiling(node.left, key)
        return ceiling if ceiling else node
    
    def find_kth(self, k: int) -> Optional[AVLNode[T]]:
        """
        查找第 k 小的节点（顺序统计）
        
        Args:
            k: 排名（1-indexed）
            
        Returns:
            第 k 小的节点，不存在返回 None
        """
        if k < 1 or k > self._count:
            return None
        return self._find_kth(self._root, k)
    
    def _find_kth(self, node: Optional[AVLNode[T]], k: int) -> Optional[AVLNode[T]]:
        """递归查找第 k 小"""
        if node is None:
            return None
        
        left_size = node.left.size if node.left else 0
        
        if k <= left_size:
            return self._find_kth(node.left, k)
        elif k == left_size + 1:
            return node
        else:
            return self._find_kth(node.right, k - left_size - 1)
    
    def rank(self, key: T) -> int:
        """
        获取键的排名（小于 key 的元素个数 + 1）
        
        Args:
            key: 目标键
            
        Returns:
            排名（1-indexed），不存在返回 0
        """
        return self._rank(self._root, key)
    
    def _rank(self, node: Optional[AVLNode[T]], key: T) -> int:
        """递归计算排名"""
        if node is None:
            return 0
        
        if key == node.key:
            return (node.left.size if node.left else 0) + 1
        elif key < node.key:
            return self._rank(node.left, key)
        else:
            left_size = node.left.size if node.left else 0
            return left_size + 1 + self._rank(node.right, key)
    
    def count_range(self, low: T, high: T) -> int:
        """
        计算范围内的元素数量
        
        Args:
            low: 下界
            high: 上界
            
        Returns:
            范围内的元素数量
        """
        return self._count_range(self._root, low, high)
    
    def _count_range(self, node: Optional[AVLNode[T]], low: T, high: T) -> int:
        """递归计算范围数量"""
        if node is None:
            return 0
        
        if node.key < low:
            return self._count_range(node.right, low, high)
        elif node.key > high:
            return self._count_range(node.left, low, high)
        else:
            return 1 + self._count_range(node.left, low, high) + self._count_range(node.right, low, high)
    
    # ==================== 插入操作 ====================
    
    def insert(self, key: T, value: Any = None) -> bool:
        """
        插入键值
        
        Args:
            key: 键
            value: 关联值（可选）
            
        Returns:
            是否成功插入（不允许重复时，已存在返回 False，但值仍会更新）
        """
        # 先检查是否已存在
        existing = self.search(key) if not self._allow_duplicates else None
        
        self._root = self._insert(self._root, key, value)
        
        if existing is not None:
            # 已存在，更新值但不增加计数
            return False
        
        self._count += 1
        return True
    
    def _insert(self, node: Optional[AVLNode[T]], key: T, value: Any) -> AVLNode[T]:
        """递归插入并平衡"""
        if node is None:
            return AVLNode(key, value)
        
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            # 键已存在
            if self._allow_duplicates:
                # 允许重复：插入到右子树
                node.right = self._insert(node.right, key, value)
            else:
                # 不允许重复：更新值
                node.value = value
                return node
        
        # 更新高度和大小
        node.update_height()
        node.update_size()
        
        # 平衡
        return self._balance(node)
    
    # ==================== 删除操作 ====================
    
    def delete(self, key: T) -> bool:
        """
        删除键
        
        Args:
            key: 要删除的键
            
        Returns:
            是否成功删除
        """
        if not self.contains(key):
            return False
        
        self._root = self._delete(self._root, key)
        self._count -= 1
        return True
    
    def _delete(self, node: Optional[AVLNode[T]], key: T) -> Optional[AVLNode[T]]:
        """递归删除并平衡"""
        if node is None:
            return None
        
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # 找到要删除的节点
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                # 两个子节点都存在
                # 用右子树的最小节点替换
                min_node = self._find_min(node.right)
                node.key = min_node.key
                node.value = min_node.value
                node.right = self._delete(node.right, min_node.key)
        
        # 更新高度和大小
        node.update_height()
        node.update_size()
        
        # 平衡
        return self._balance(node)
    
    def delete_min(self) -> Optional[T]:
        """删除最小键节点，返回其键"""
        if self._root is None:
            return None
        
        min_node = self.find_min()
        key = min_node.key
        self._root = self._delete_min(self._root)
        self._count -= 1
        return key
    
    def _delete_min(self, node: AVLNode[T]) -> Optional[AVLNode[T]]:
        """递归删除最小节点"""
        if node.left is None:
            return node.right
        
        node.left = self._delete_min(node.left)
        node.update_height()
        node.update_size()
        return self._balance(node)
    
    def delete_max(self) -> Optional[T]:
        """删除最大键节点，返回其键"""
        if self._root is None:
            return None
        
        max_node = self.find_max()
        key = max_node.key
        self._root = self._delete_max(self._root)
        self._count -= 1
        return key
    
    def _delete_max(self, node: AVLNode[T]) -> Optional[AVLNode[T]]:
        """递归删除最大节点"""
        if node.right is None:
            return node.left
        
        node.right = self._delete_max(node.right)
        node.update_height()
        node.update_size()
        return self._balance(node)
    
    # ==================== 平衡操作 ====================
    
    def _balance(self, node: AVLNode[T]) -> AVLNode[T]:
        """平衡节点"""
        bf = node.balance_factor()
        
        # 左子树过高
        if bf > 1:
            if node.left.balance_factor() < 0:
                # LR 情况：先左旋左子树
                node.left = self._rotate_left(node.left)
            # LL 情况：右旋
            return self._rotate_right(node)
        
        # 右子树过高
        if bf < -1:
            if node.right.balance_factor() > 0:
                # RL 情况：先右旋右子树
                node.right = self._rotate_right(node.right)
            # RR 情况：左旋
            return self._rotate_left(node)
        
        return node
    
    def _rotate_left(self, node: AVLNode[T]) -> AVLNode[T]:
        """左旋"""
        right = node.right
        node.right = right.left
        right.left = node
        
        # 更新高度（先更新下层节点）
        node.update_height()
        right.update_height()
        
        # 更新大小
        node.update_size()
        right.update_size()
        
        return right
    
    def _rotate_right(self, node: AVLNode[T]) -> AVLNode[T]:
        """右旋"""
        left = node.left
        node.left = left.right
        left.right = node
        
        # 更新高度（先更新下层节点）
        node.update_height()
        left.update_height()
        
        # 更新大小
        node.update_size()
        left.update_size()
        
        return left
    
    # ==================== 验证 ====================
    
    def is_valid_avl(self) -> bool:
        """验证是否为有效的 AVL 树"""
        return self._is_valid_avl(self._root)
    
    def _is_valid_avl(self, node: Optional[AVLNode[T]]) -> bool:
        """递归验证 AVL 树"""
        if node is None:
            return True
        
        # 检查平衡
        if not node.is_balanced():
            return False
        
        # 检查高度正确性
        expected_height = 1 + max(
            node.left.height if node.left else 0,
            node.right.height if node.right else 0
        )
        if node.height != expected_height:
            return False
        
        # 检查大小正确性
        expected_size = 1 + (node.left.size if node.left else 0) + (node.right.size if node.right else 0)
        if node.size != expected_size:
            return False
        
        # 检查 BST 性质
        if node.left and node.left.key >= node.key:
            return False
        if node.right and node.right.key <= node.key:
            return False
        
        return self._is_valid_avl(node.left) and self._is_valid_avl(node.right)
    
    # ==================== 遍历操作 ====================
    
    def inorder(self) -> Iterator[T]:
        """中序遍历（升序）"""
        return self._inorder(self._root)
    
    def _inorder(self, node: Optional[AVLNode[T]]) -> Iterator[T]:
        """递归中序遍历"""
        if node:
            yield from self._inorder(node.left)
            yield node.key
            yield from self._inorder(node.right)
    
    def preorder(self) -> Iterator[T]:
        """前序遍历"""
        return self._preorder(self._root)
    
    def _preorder(self, node: Optional[AVLNode[T]]) -> Iterator[T]:
        """递归前序遍历"""
        if node:
            yield node.key
            yield from self._preorder(node.left)
            yield from self._preorder(node.right)
    
    def postorder(self) -> Iterator[T]:
        """后序遍历"""
        return self._postorder(self._root)
    
    def _postorder(self, node: Optional[AVLNode[T]]) -> Iterator[T]:
        """递归后序遍历"""
        if node:
            yield from self._postorder(node.left)
            yield from self._postorder(node.right)
            yield node.key
    
    def level_order(self) -> Iterator[T]:
        """层序遍历"""
        if self._root is None:
            return
        
        queue = deque([self._root])
        while queue:
            node = queue.popleft()
            yield node.key
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    def inorder_nodes(self) -> Iterator[AVLNode[T]]:
        """中序遍历节点"""
        return self._inorder_nodes(self._root)
    
    def _inorder_nodes(self, node: Optional[AVLNode[T]]) -> Iterator[AVLNode[T]]:
        """递归中序遍历节点"""
        if node:
            yield from self._inorder_nodes(node.left)
            yield node
            yield from self._inorder_nodes(node.right)
    
    # ==================== 范围查询 ====================
    
    def range_query(self, low: T, high: T) -> List[T]:
        """
        获取范围内的所有键
        
        Args:
            low: 下界
            high: 上界
            
        Returns:
            范围内的键列表（升序）
        """
        result = []
        self._range_query(self._root, low, high, result)
        return result
    
    def _range_query(self, node: Optional[AVLNode[T]], low: T, high: T, result: List[T]) -> None:
        """递归范围查询"""
        if node is None:
            return
        
        if node.key > low:
            self._range_query(node.left, low, high, result)
        
        if low <= node.key <= high:
            result.append(node.key)
        
        if node.key < high:
            self._range_query(node.right, low, high, result)
    
    def range_query_nodes(self, low: T, high: T) -> List[AVLNode[T]]:
        """
        获取范围内的所有节点
        
        Args:
            low: 下界
            high: 上界
            
        Returns:
            范围内的节点列表（升序）
        """
        result = []
        self._range_query_nodes(self._root, low, high, result)
        return result
    
    def _range_query_nodes(self, node: Optional[AVLNode[T]], low: T, high: T, result: List[AVLNode[T]]) -> None:
        """递归范围查询节点"""
        if node is None:
            return
        
        if node.key > low:
            self._range_query_nodes(node.left, low, high, result)
        
        if low <= node.key <= high:
            result.append(node)
        
        if node.key < high:
            self._range_query_nodes(node.right, low, high, result)
    
    # ==================== 转换操作 ====================
    
    def to_list(self) -> List[T]:
        """转换为有序列表"""
        return list(self.inorder())
    
    def to_sorted_list(self) -> List[T]:
        """转换为有序列表（同 to_list）"""
        return self.to_list()
    
    def to_dict(self) -> dict:
        """转换为字典（键值对）"""
        return {node.key: node.value for node in self.inorder_nodes()}
    
    def keys(self) -> List[T]:
        """获取所有键（有序）"""
        return self.to_list()
    
    def values(self) -> List[Any]:
        """获取所有值（按键顺序）"""
        return [node.value for node in self.inorder_nodes()]
    
    # ==================== 批量操作 ====================
    
    def bulk_insert(self, items: List[Tuple[T, Any]]) -> int:
        """
        批量插入
        
        Args:
            items: 键值对列表
            
        Returns:
            成功插入的数量
        """
        count = 0
        for key, value in items:
            if self.insert(key, value):
                count += 1
        return count
    
    def clear(self) -> None:
        """清空树"""
        self._root = None
        self._count = 0
    
    # ==================== 其他操作 ====================
    
    def predecessor(self, key: T) -> Optional[T]:
        """
        获取键的前驱（小于 key 的最大键）
        
        Args:
            key: 目标键
            
        Returns:
            前驱键，不存在返回 None
        """
        node = self.find_floor(key)
        if node and node.key == key:
            # 找严格小于的前驱
            node = self.find_floor(key - 1 if isinstance(key, (int, float)) else key)
            # 对于非数值类型，需要特殊处理
        return node.key if node and node.key < key else None
    
    def successor(self, key: T) -> Optional[T]:
        """
        获取键的后继（大于 key 的最小键）
        
        Args:
            key: 目标键
            
        Returns:
            后继键，不存在返回 None
        """
        node = self.find_ceiling(key)
        if node and node.key == key:
            # 找严格大于的后继
            node = self.find_ceiling(key + 1 if isinstance(key, (int, float)) else key)
        return node.key if node and node.key > key else None
    
    def depth(self, key: T) -> int:
        """
        获取键的深度（从根到节点的路径长度）
        
        Args:
            key: 目标键
            
        Returns:
            深度（根节点为 0），不存在返回 -1
        """
        return self._depth(self._root, key, 0)
    
    def _depth(self, node: Optional[AVLNode[T]], key: T, current_depth: int) -> int:
        """递归计算深度"""
        if node is None:
            return -1
        
        if key == node.key:
            return current_depth
        elif key < node.key:
            return self._depth(node.left, key, current_depth + 1)
        else:
            return self._depth(node.right, key, current_depth + 1)
    
    def path_to(self, key: T) -> List[T]:
        """
        获取从根到键的路径
        
        Args:
            key: 目标键
            
        Returns:
            路径上的键列表，不存在返回空列表
        """
        path = []
        self._path_to(self._root, key, path)
        return path
    
    def _path_to(self, node: Optional[AVLNode[T]], key: T, path: List[T]) -> bool:
        """递归获取路径"""
        if node is None:
            return False
        
        path.append(node.key)
        
        if key == node.key:
            return True
        elif key < node.key:
            if self._path_to(node.left, key, path):
                return True
        else:
            if self._path_to(node.right, key, path):
                return True
        
        path.pop()
        return False
    
    def visualize(self) -> str:
        """
        生成树的字符串可视化
        
        Returns:
            树的可视化字符串
        """
        if self._root is None:
            return "(empty tree)"
        
        lines = []
        self._visualize(self._root, "", True, lines)
        return "\n".join(lines)
    
    def _visualize(self, node: Optional[AVLNode[T]], prefix: str, is_last: bool, lines: List[str]) -> None:
        """递归生成可视化"""
        if node is None:
            return
        
        lines.append(prefix + ("└── " if is_last else "├── ") + f"{node.key} (h={node.height})")
        
        children = [(node.left, False), (node.right, True)]
        for i, (child, is_last_child) in enumerate(children):
            if child:
                new_prefix = prefix + ("    " if is_last else "│   ")
                self._visualize(child, new_prefix, is_last_child, lines)
    
    def __len__(self) -> int:
        return self.size
    
    def __contains__(self, key: T) -> bool:
        return self.contains(key)
    
    def __iter__(self) -> Iterator[T]:
        return self.inorder()
    
    def __repr__(self) -> str:
        return f"AVLTree(size={self.size}, height={self.height})"


# ==================== 工具函数 ====================

def create_avl_tree(items: Optional[List[Tuple[T, Any]]] = None, 
                    allow_duplicates: bool = False) -> AVLTree[T]:
    """
    创建并初始化 AVL 树
    
    Args:
        items: 初始键值对列表
        allow_duplicates: 是否允许重复
        
    Returns:
        初始化后的 AVL 树
    """
    tree = AVLTree(allow_duplicates)
    if items:
        tree.bulk_insert(items)
    return tree


def from_sorted_list(keys: List[T], values: Optional[List[Any]] = None) -> AVLTree[T]:
    """
    从有序列表构建平衡 AVL 树（最优构建方式）
    
    Args:
        keys: 有序键列表
        values: 对应的值列表
        
    Returns:
        平衡的 AVL 树
    """
    tree = AVLTree()
    if not keys:
        return tree
    
    if values is None:
        values = [None] * len(keys)
    
    # 使用二分构建确保平衡
    def build_balanced(start: int, end: int) -> Optional[AVLNode[T]]:
        if start > end:
            return None
        
        mid = (start + end) // 2
        node = AVLNode(keys[mid], values[mid])
        node.left = build_balanced(start, mid - 1)
        node.right = build_balanced(mid + 1, end)
        node.update_height()
        node.update_size()
        return node
    
    tree._root = build_balanced(0, len(keys) - 1)
    tree._count = len(keys)
    return tree


def merge_avl_trees(tree1: AVLTree[T], tree2: AVLTree[T], 
                    allow_duplicates: bool = False) -> AVLTree[T]:
    """
    合并两个 AVL 树
    
    Args:
        tree1: 第一个树
        tree2: 第二个树
        allow_duplicates: 是否允许重复
        
    Returns:
        合合后的新 AVL 树
    """
    result = AVLTree(allow_duplicates)
    
    for node in tree1.inorder_nodes():
        result.insert(node.key, node.value)
    
    for node in tree2.inorder_nodes():
        result.insert(node.key, node.value)
    
    return result


def split_avl_tree(tree: AVLTree[T], key: T) -> Tuple[AVLTree[T], AVLTree[T]]:
    """
    根据 key 分割 AVL 树
    
    Args:
        tree: 原 AVL 树
        key: 分割键
        
    Returns:
        (小于 key 的树, 大于等于 key 的树)
    """
    left_tree = AVLTree(tree.allow_duplicates)
    right_tree = AVLTree(tree.allow_duplicates)
    
    for node in tree.inorder_nodes():
        if node.key < key:
            left_tree.insert(node.key, node.value)
        else:
            right_tree.insert(node.key, node.value)
    
    return left_tree, right_tree


def avl_tree_to_dict(tree: AVLTree[T]) -> dict:
    """AVL 树转字典"""
    return tree.to_dict()


def dict_to_avl_tree(d: dict, allow_duplicates: bool = False) -> AVLTree[T]:
    """字典转 AVL 树"""
    return create_avl_tree(list(d.items()), allow_duplicates)


def find_common_elements(tree1: AVLTree[T], tree2: AVLTree[T]) -> List[T]:
    """
    找两个 AVL 树的公共元素
    
    Args:
        tree1: 第一个树
        tree2: 第二个树
        
    Returns:
        公共键列表
    """
    set1 = set(tree1.to_list())
    set2 = set(tree2.to_list())
    return sorted(set1 & set2)


def find_difference(tree1: AVLTree[T], tree2: AVLTree[T]) -> Tuple[List[T], List[T]]:
    """
    找两个 AVL 树的差集
    
    Args:
        tree1: 第一个树
        tree2: 第二个树
        
    Returns:
        (tree1 独有的元素, tree2 独有的元素)
    """
    set1 = set(tree1.to_list())
    set2 = set(tree2.to_list())
    return sorted(set1 - set2), sorted(set2 - set1)


def validate_avl_tree(tree: AVLTree[T]) -> Tuple[bool, str]:
    """
    验证 AVL 树并返回详细信息
    
    Args:
        tree: 要验证的树
        
    Returns:
        (是否有效, 详细信息)
    """
    if tree.is_empty:
        return True, "Empty tree is valid"
    
    issues = []
    
    # 检查大小一致性
    actual_count = sum(1 for _ in tree.inorder())
    if actual_count != tree.size:
        issues.append(f"Size mismatch: claimed {tree.size}, actual {actual_count}")
    
    # 检查 AVL 性质
    if not tree.is_valid_avl():
        issues.append("AVL balance property violated")
    
    # 检查 BST 性质（通过中序遍历）
    prev = None
    for key in tree.inorder():
        if prev is not None and key <= prev:
            issues.append(f"BST property violated: {prev} <= {key}")
            break
        prev = key
    
    if issues:
        return False, "; ".join(issues)
    return True, "Tree is valid AVL tree"


def get_tree_statistics(tree: AVLTree[T]) -> dict:
    """
    获取树的统计信息
    
    Args:
        tree: 目标树
        
    Returns:
        统计信息字典
    """
    if tree.is_empty:
        return {
            "size": 0,
            "height": 0,
            "is_balanced": True,
            "min_key": None,
            "max_key": None,
            "avg_depth": 0,
            "theoretical_min_height": 0,
            "theoretical_max_height": 0
        }
    
    # 计算平均深度
    depths = []
    for key in tree.inorder():
        depths.append(tree.depth(key))
    avg_depth = sum(depths) / len(depths) if depths else 0
    
    min_node = tree.find_min()
    max_node = tree.find_max()
    
    size = tree.size
    theoretical_min_height = math.ceil(math.log2(size + 1))
    theoretical_max_height = int(1.44 * math.log2(size + 2) - 0.328)  # AVL 树最大高度
    
    return {
        "size": size,
        "height": tree.height,
        "is_balanced": tree.is_valid_avl(),
        "min_key": min_node.key if min_node else None,
        "max_key": max_node.key if max_node else None,
        "avg_depth": round(avg_depth, 2),
        "theoretical_min_height": theoretical_min_height,
        "theoretical_max_height": theoretical_max_height,
        "height_efficiency": round(tree.height / theoretical_max_height * 100, 2) if theoretical_max_height else 100
    }