"""
B+树工具模块
B+ Tree Utilities

提供完整的B+树实现，包括：
- 插入、删除、查询操作
- 范围查询
- 叶节点链表遍历
- 持久化支持（序列化/反序列化）

B+树特点：
- 所有数据存储在叶节点
- 叶节点通过链表连接，支持高效范围查询
- 内部节点只存储键和子节点指针
- 自动平衡，保持高效查询性能

零外部依赖，仅使用 Python 标准库
"""

from typing import List, Optional, Tuple, Any, Iterator, Dict, Union
import json
import pickle


# ============================================================================
# B+树节点类
# ============================================================================

class BPlusTreeNode:
    """B+树节点基类"""
    
    def __init__(self):
        self.keys: List[Any] = []
        self.is_leaf: bool = True


class InternalNode(BPlusTreeNode):
    """B+树内部节点"""
    
    def __init__(self):
        super().__init__()
        self.children: List[BPlusTreeNode] = []
        self.is_leaf = False


class LeafNode(BPlusTreeNode):
    """B+树叶节点"""
    
    def __init__(self):
        super().__init__()
        self.values: List[Any] = []
        self.next_leaf: Optional[LeafNode] = None
        self.prev_leaf: Optional[LeafNode] = None
        self.is_leaf = True


# ============================================================================
# B+树实现
# ============================================================================

class BPlusTree:
    """
    B+树实现
    
    支持插入、删除、精确查找、范围查询等操作
    
    Args:
        order: B+树的阶数（默认为4），每个节点最多有order个子节点
               最小阶数为3，阶数越大树越扁平
    """
    
    def __init__(self, order: int = 4):
        if order < 3:
            raise ValueError("B+树的阶数必须至少为3")
        self.order = order
        self.max_keys = order - 1  # 每个节点最多max_keys个键
        self.min_keys = order // 2  # 每个节点最少min_keys个键（根节点除外）
        
        self.root: BPlusTreeNode = LeafNode()
        self._size = 0
    
    @property
    def size(self) -> int:
        """返回树中键值对的数量"""
        return self._size
    
    @property
    def is_empty(self) -> bool:
        """检查树是否为空"""
        return self._size == 0
    
    @property
    def height(self) -> int:
        """计算树的高度"""
        if self.root is None or len(self.root.keys) == 0:
            return 0
        height = 1
        node = self.root
        while not node.is_leaf:
            node = node.children[0]
            height += 1
        return height
    
    # ========================================================================
    # 查询操作
    # ========================================================================
    
    def get(self, key: Any) -> Optional[Any]:
        """精确查找键对应的值"""
        if len(self.root.keys) == 0:
            return None
        
        leaf = self._find_leaf(key)
        idx = self._binary_search(leaf.keys, key)
        
        if idx < len(leaf.keys) and leaf.keys[idx] == key:
            return leaf.values[idx]
        return None
    
    def __getitem__(self, key: Any) -> Any:
        """支持 [] 操作符"""
        result = self.get(key)
        if result is None:
            raise KeyError(key)
        return result
    
    def contains(self, key: Any) -> bool:
        """检查键是否存在"""
        return self.get(key) is not None
    
    def __contains__(self, key: Any) -> bool:
        """支持 in 操作符"""
        return self.contains(key)
    
    def range_query(
        self, 
        start_key: Any, 
        end_key: Any,
        include_start: bool = True,
        include_end: bool = True
    ) -> List[Tuple[Any, Any]]:
        """范围查询：查找键在[start_key, end_key]范围内的键值对"""
        if len(self.root.keys) == 0:
            return []
        
        results = []
        leaf = self._find_leaf(start_key)
        idx = self._binary_search(leaf.keys, start_key)
        
        # 处理起始边界
        if idx < len(leaf.keys) and not include_start and leaf.keys[idx] == start_key:
            idx += 1
        
        # 遍历叶节点链表
        while leaf is not None:
            while idx < len(leaf.keys):
                key = leaf.keys[idx]
                
                # 检查是否超出范围
                if key > end_key:
                    return results
                if not include_end and key == end_key:
                    return results
                
                results.append((key, leaf.values[idx]))
                idx += 1
            
            leaf = leaf.next_leaf
            idx = 0
        
        return results
    
    def get_all(self) -> List[Tuple[Any, Any]]:
        """获取所有键值对（按键排序）"""
        results = []
        leaf = self._get_first_leaf()
        
        while leaf is not None:
            for i in range(len(leaf.keys)):
                results.append((leaf.keys[i], leaf.values[i]))
            leaf = leaf.next_leaf
        
        return results
    
    def get_keys(self) -> List[Any]:
        """获取所有键（排序）"""
        return [kv[0] for kv in self.get_all()]
    
    def get_values(self) -> List[Any]:
        """获取所有值"""
        return [kv[1] for kv in self.get_all()]
    
    def get_min(self) -> Optional[Tuple[Any, Any]]:
        """获取最小键值对"""
        leaf = self._get_first_leaf()
        if leaf is None or len(leaf.keys) == 0:
            return None
        return (leaf.keys[0], leaf.values[0])
    
    def get_max(self) -> Optional[Tuple[Any, Any]]:
        """获取最大键值对"""
        if len(self.root.keys) == 0:
            return None
        
        node = self.root
        while not node.is_leaf:
            node = node.children[-1]
        
        if len(node.keys) == 0:
            return None
        return (node.keys[-1], node.values[-1])
    
    # ========================================================================
    # 插入操作
    # ========================================================================
    
    def insert(self, key: Any, value: Any) -> None:
        """插入键值对，如果键已存在则更新其值"""
        # 找到目标叶节点
        leaf = self._find_leaf(key)
        
        # 检查键是否已存在
        idx = self._binary_search(leaf.keys, key)
        if idx < len(leaf.keys) and leaf.keys[idx] == key:
            # 键已存在，更新值
            leaf.values[idx] = value
            return
        
        # 在叶节点中插入键值对
        leaf.keys.insert(idx, key)
        leaf.values.insert(idx, value)
        self._size += 1
        
        # 检查是否需要分裂
        if len(leaf.keys) > self.max_keys:
            self._split_leaf(leaf)
    
    def __setitem__(self, key: Any, value: Any) -> None:
        """支持 [] 赋值操作"""
        self.insert(key, value)
    
    def _split_leaf(self, leaf: LeafNode) -> None:
        """分裂叶节点"""
        mid = len(leaf.keys) // 2
        
        # 创建新叶节点（保存右半部分）
        new_leaf = LeafNode()
        new_leaf.keys = leaf.keys[mid:]
        new_leaf.values = leaf.values[mid:]
        
        # 更新链表指针
        new_leaf.next_leaf = leaf.next_leaf
        new_leaf.prev_leaf = leaf
        if leaf.next_leaf is not None:
            leaf.next_leaf.prev_leaf = new_leaf
        leaf.next_leaf = new_leaf
        
        # 截断原叶节点（保存左半部分）
        split_key = leaf.keys[mid]  # 分裂键是新叶节点的第一个键
        leaf.keys = leaf.keys[:mid]
        leaf.values = leaf.values[:mid]
        
        # 向上插入分裂键
        self._insert_in_parent(leaf, split_key, new_leaf)
    
    def _insert_in_parent(
        self, 
        left: BPlusTreeNode, 
        key: Any, 
        right: BPlusTreeNode
    ) -> None:
        """在父节点中插入分裂后的键和右节点"""
        # 如果left是根节点，创建新根
        if left is self.root:
            new_root = InternalNode()
            new_root.keys = [key]
            new_root.children = [left, right]
            self.root = new_root
            return
        
        # 找到父节点
        parent = self._find_parent(self.root, left)
        if parent is None:
            raise RuntimeError("无法找到父节点")
        
        # 找到left在父节点中的位置
        idx = 0
        while idx < len(parent.children) and parent.children[idx] is not left:
            idx += 1
        
        # 插入新键和右节点
        parent.keys.insert(idx, key)
        parent.children.insert(idx + 1, right)
        
        # 检查是否需要分裂内部节点
        if len(parent.keys) > self.max_keys:
            self._split_internal(parent)
    
    def _split_internal(self, node: InternalNode) -> None:
        """分裂内部节点"""
        mid = len(node.keys) // 2
        
        # 中间键上移
        up_key = node.keys[mid]
        
        # 创建新内部节点（右半部分）
        new_node = InternalNode()
        new_node.keys = node.keys[mid + 1:]
        new_node.children = node.children[mid + 1:]
        
        # 截断原节点（左半部分）
        node.keys = node.keys[:mid]
        node.children = node.children[:mid + 1]
        
        # 向上插入
        self._insert_in_parent(node, up_key, new_node)
    
    # ========================================================================
    # 删除操作
    # ========================================================================
    
    def delete(self, key: Any) -> bool:
        """删除键值对"""
        if len(self.root.keys) == 0:
            return False
        
        leaf = self._find_leaf(key)
        idx = self._binary_search(leaf.keys, key)
        
        if idx >= len(leaf.keys) or leaf.keys[idx] != key:
            return False  # 键不存在
        
        # 从叶节点删除
        leaf.keys.pop(idx)
        leaf.values.pop(idx)
        self._size -= 1
        
        # 如果删除后节点为空且不是根节点
        if len(leaf.keys) == 0 and leaf is not self.root:
            # 从链表中移除
            if leaf.prev_leaf is not None:
                leaf.prev_leaf.next_leaf = leaf.next_leaf
            if leaf.next_leaf is not None:
                leaf.next_leaf.prev_leaf = leaf.prev_leaf
        
        # 处理根节点变空的情况
        if self.root.is_leaf:
            if len(self.root.keys) == 0:
                # 根节点为空，保持为空叶节点
                pass
        elif len(self.root.keys) == 0:
            # 内部根节点为空，下降到唯一的子节点
            self.root = self.root.children[0]
        
        return True
    
    def remove(self, key: Any) -> bool:
        """删除键值对的别名"""
        return self.delete(key)
    
    def __delitem__(self, key: Any) -> None:
        """支持 del 操作符"""
        if not self.delete(key):
            raise KeyError(key)
    
    def clear(self) -> None:
        """清空树"""
        self.root = LeafNode()
        self._size = 0
    
    # ========================================================================
    # 辅助方法
    # ========================================================================
    
    def _get_first_leaf(self) -> Optional[LeafNode]:
        """获取第一个叶节点"""
        if len(self.root.keys) == 0:
            return None
        
        node = self.root
        while not node.is_leaf:
            node = node.children[0]
        return node
    
    def _find_leaf(self, key: Any) -> LeafNode:
        """找到键应该所在的叶节点"""
        node = self.root
        
        while not node.is_leaf:
            # B+树内部节点：
            # children[0] 包含 < keys[0] 的数据
            # children[i] 包含 >= keys[i-1] 且 < keys[i] 的数据（对于i在1到len(keys)之间）
            # children[len(keys)] 包含 >= keys[-1] 的数据
            
            # 找到第一个 >= key 的键的位置
            idx = 0
            while idx < len(node.keys) and key >= node.keys[idx]:
                idx += 1
            node = node.children[idx]
        
        return node
    
    def _find_parent(
        self, 
        node: BPlusTreeNode, 
        target: BPlusTreeNode
    ) -> Optional[InternalNode]:
        """找到目标节点的父节点"""
        if node.is_leaf or node is target:
            return None
        
        # 检查直接子节点
        for child in node.children:
            if child is target:
                return node
        
        # 递归检查子节点
        for child in node.children:
            if not child.is_leaf:
                result = self._find_parent(child, target)
                if result is not None:
                    return result
        
        return None
    
    def _binary_search(self, arr: List[Any], key: Any) -> int:
        """二分查找，返回插入位置"""
        left, right = 0, len(arr)
        while left < right:
            mid = (left + right) // 2
            if arr[mid] < key:
                left = mid + 1
            elif arr[mid] > key:
                right = mid
            else:
                return mid  # 找到精确位置
        return left
    
    # ========================================================================
    # 遍历操作
    # ========================================================================
    
    def __iter__(self) -> Iterator[Tuple[Any, Any]]:
        """支持迭代"""
        leaf = self._get_first_leaf()
        while leaf is not None:
            for i in range(len(leaf.keys)):
                yield (leaf.keys[i], leaf.values[i])
            leaf = leaf.next_leaf
    
    def iterate_keys(self) -> Iterator[Any]:
        """迭代所有键"""
        for key, _ in self:
            yield key
    
    def iterate_values(self) -> Iterator[Any]:
        """迭代所有值"""
        for _, value in self:
            yield value
    
    # ========================================================================
    # 序列化/反序列化
    # ========================================================================
    
    def to_dict(self) -> Dict[str, Any]:
        """将树转换为字典"""
        return {
            'order': self.order,
            'size': self._size,
            'items': self.get_all()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BPlusTree':
        """从字典创建B+树"""
        tree = cls(order=data['order'])
        for key, value in data['items']:
            tree.insert(key, value)
        return tree
    
    def to_json(self) -> str:
        """序列化为JSON字符串"""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_json(cls, json_str: str) -> 'BPlusTree':
        """从JSON字符串反序列化"""
        return cls.from_dict(json.loads(json_str))
    
    def to_pickle(self) -> bytes:
        """序列化为pickle字节"""
        return pickle.dumps(self.to_dict())
    
    @classmethod
    def from_pickle(cls, data: bytes) -> 'BPlusTree':
        """从pickle字节反序列化"""
        return cls.from_dict(pickle.loads(data))
    
    # ========================================================================
    # 调试和可视化
    # ========================================================================
    
    def __len__(self) -> int:
        return self._size
    
    def __repr__(self) -> str:
        return f"BPlusTree(order={self.order}, size={self._size})"
    
    def print_tree(self) -> None:
        """打印树结构"""
        if len(self.root.keys) == 0:
            print("Empty tree")
            return
        
        self._print_node(self.root, 0)
    
    def _print_node(self, node: BPlusTreeNode, level: int) -> None:
        """递归打印节点"""
        indent = "  " * level
        if node.is_leaf:
            print(f"{indent}Leaf: keys={node.keys}, values={node.values}")
        else:
            print(f"{indent}Internal: keys={node.keys}")
            for child in node.children:
                self._print_node(child, level + 1)
    
    def validate(self) -> bool:
        """验证树的有效性"""
        if len(self.root.keys) == 0:
            return True
        
        # 检查叶节点链表
        leaf = self._get_first_leaf()
        prev = None
        all_keys = []
        
        while leaf is not None:
            # 检查前驱指针
            if leaf.prev_leaf is not prev:
                return False
            
            # 检查键有序
            for i in range(len(leaf.keys) - 1):
                if leaf.keys[i] >= leaf.keys[i + 1]:
                    return False
            
            all_keys.extend(leaf.keys)
            prev = leaf
            leaf = leaf.next_leaf
        
        # 检查所有键有序
        for i in range(len(all_keys) - 1):
            if all_keys[i] >= all_keys[i + 1]:
                return False
        
        # 检查键数量
        if len(all_keys) != self._size:
            return False
        
        return True


# ============================================================================
# 批量操作
# ============================================================================

def bulk_load(items: List[Tuple[Any, Any]], order: int = 4) -> BPlusTree:
    """批量加载数据创建B+树"""
    tree = BPlusTree(order=order)
    sorted_items = sorted(items, key=lambda x: x[0])
    for key, value in sorted_items:
        tree.insert(key, value)
    return tree


def merge_trees(tree1: BPlusTree, tree2: BPlusTree) -> BPlusTree:
    """合并两棵B+树"""
    order = max(tree1.order, tree2.order)
    result = BPlusTree(order=order)
    
    for key, value in tree1:
        result.insert(key, value)
    
    for key, value in tree2:
        result.insert(key, value)
    
    return result


# ============================================================================
# 统计和分析
# ============================================================================

def get_tree_stats(tree: BPlusTree) -> Dict[str, Any]:
    """获取B+树统计信息"""
    if tree.is_empty:
        return {
            'size': 0,
            'height': 0,
            'order': tree.order,
            'leaf_count': 0,
            'internal_count': 0,
            'avg_leaf_fill': 0,
            'min_leaf_keys': 0,
            'max_leaf_keys': 0
        }
    
    leaf_count = 0
    internal_count = 0
    leaf_keys = []
    
    def count_nodes(node: BPlusTreeNode):
        if node.is_leaf:
            leaf_count += 1
            leaf_keys.append(len(node.keys))
        else:
            internal_count += 1
            for child in node.children:
                count_nodes(child)
    
    # 使用外部变量跟踪
    leaf_count = 0
    internal_count = 0
    leaf_keys = []
    
    def count_nodes_local(node: BPlusTreeNode):
        nonlocal leaf_count, internal_count, leaf_keys
        if node.is_leaf:
            leaf_count += 1
            leaf_keys.append(len(node.keys))
        else:
            internal_count += 1
            for child in node.children:
                count_nodes_local(child)
    
    count_nodes_local(tree.root)
    
    return {
        'size': tree.size,
        'height': tree.height,
        'order': tree.order,
        'leaf_count': leaf_count,
        'internal_count': internal_count,
        'avg_leaf_fill': sum(leaf_keys) / len(leaf_keys) if leaf_keys else 0,
        'min_leaf_keys': min(leaf_keys) if leaf_keys else 0,
        'max_leaf_keys': max(leaf_keys) if leaf_keys else 0
    }