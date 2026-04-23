"""
disjoint_set_utils - 并查集（Union-Find）数据结构实现

零外部依赖的并查集实现，支持路径压缩和按秩合并优化。
广泛应用于图连通性问题、最小生成树算法、网络连接检测等场景。

主要功能:
- 基本并查集操作 (make_set, find, union)
- 路径压缩和按秩合并优化
- 连通性检测
- 集合计数
- 批量操作
- 序列化/反序列化

作者: AllToolkit
日期: 2026-04-23
"""

from typing import Dict, List, Set, Tuple, Optional, Any, Iterator, Generic, TypeVar, Iterable
from collections import defaultdict

T = TypeVar('T')


class DisjointSet(Generic[T]):
    """
    泛型并查集数据结构
    
    使用路径压缩和按秩合并优化，近乎 O(1) 的查找和合并操作。
    
    时间复杂度:
    - find: O(α(n)) ≈ O(1), α 是反阿克曼函数
    - union: O(α(n)) ≈ O(1)
    - make_set: O(1)
    
    空间复杂度: O(n)
    
    示例:
        >>> ds = DisjointSet()
        >>> ds.make_set(1)
        >>> ds.make_set(2)
        >>> ds.union(1, 2)
        >>> ds.connected(1, 2)
        True
    """
    
    def __init__(self, elements: Optional[Iterable[T]] = None):
        """
        初始化并查集
        
        Args:
            elements: 可选的初始元素集合
        """
        self._parent: Dict[T, T] = {}
        self._rank: Dict[T, int] = {}
        self._size: Dict[T, int] = {}  # 每个集合的大小
        self._count: int = 0  # 集合数量
        
        if elements:
            for elem in elements:
                self.make_set(elem)
    
    def __len__(self) -> int:
        """返回元素总数"""
        return len(self._parent)
    
    def __contains__(self, element: T) -> bool:
        """检查元素是否存在"""
        return element in self._parent
    
    def __iter__(self) -> Iterator[T]:
        """迭代所有元素"""
        return iter(self._parent.keys())
    
    def __repr__(self) -> str:
        sets = self.get_sets()
        sets_str = ", ".join(f"{{{', '.join(map(str, s))}}}" for s in sets)
        return f"DisjointSet({sets_str})"
    
    def make_set(self, element: T) -> None:
        """
        创建一个新集合，包含单个元素
        
        Args:
            element: 要创建集合的元素
            
        Raises:
            ValueError: 如果元素已存在
        """
        if element in self._parent:
            raise ValueError(f"元素 '{element}' 已存在")
        
        self._parent[element] = element
        self._rank[element] = 0
        self._size[element] = 1
        self._count += 1
    
    def make_sets(self, elements: Iterable[T]) -> None:
        """
        批量创建集合
        
        Args:
            elements: 元素集合
        """
        for elem in elements:
            if elem not in self._parent:
                self.make_set(elem)
    
    def find(self, element: T) -> T:
        """
        查找元素所属集合的根节点
        
        使用路径压缩优化，将沿途节点直接连接到根节点。
        
        Args:
            element: 要查找的元素
            
        Returns:
            集合的根节点（代表元素）
            
        Raises:
            KeyError: 如果元素不存在
        """
        if element not in self._parent:
            raise KeyError(f"元素 '{element}' 不存在")
        
        # 路径压缩：递归查找时将节点直接连接到根
        if self._parent[element] != element:
            self._parent[element] = self.find(self._parent[element])
        
        return self._parent[element]
    
    def find_path(self, element: T) -> List[T]:
        """
        查找从元素到根节点的路径
        
        Args:
            element: 起始元素
            
        Returns:
            从元素到根节点的路径列表
        """
        if element not in self._parent:
            raise KeyError(f"元素 '{element}' 不存在")
        
        path = [element]
        current = element
        
        while self._parent[current] != current:
            current = self._parent[current]
            path.append(current)
        
        return path
    
    def union(self, element1: T, element2: T) -> bool:
        """
        合并两个元素所属的集合
        
        使用按秩合并优化，将较矮的树连接到较高的树。
        
        Args:
            element1: 第一个元素
            element2: 第二个元素
            
        Returns:
            True 如果合并成功（原本不同集合），False 如果已在同一集合
            
        Raises:
            KeyError: 如果任一元素不存在
        """
        root1 = self.find(element1)
        root2 = self.find(element2)
        
        if root1 == root2:
            return False
        
        # 按秩合并：将较低的树连接到较高的树
        if self._rank[root1] < self._rank[root2]:
            root1, root2 = root2, root1
        
        self._parent[root2] = root1
        self._size[root1] += self._size[root2]
        
        if self._rank[root1] == self._rank[root2]:
            self._rank[root1] += 1
        
        self._count -= 1
        return True
    
    def union_all(self, elements: Iterable[T]) -> int:
        """
        将多个元素全部合并到同一集合
        
        Args:
            elements: 要合并的元素集合
            
        Returns:
            实际执行的合并次数
        """
        elements = list(elements)
        if len(elements) < 2:
            return 0
        
        merges = 0
        first = elements[0]
        for elem in elements[1:]:
            if self.union(first, elem):
                merges += 1
        
        return merges
    
    def connected(self, element1: T, element2: T) -> bool:
        """
        检查两个元素是否在同一集合
        
        Args:
            element1: 第一个元素
            element2: 第二个元素
            
        Returns:
            True 如果在同一集合，False 否则
        """
        try:
            return self.find(element1) == self.find(element2)
        except KeyError:
            return False
    
    def get_set_size(self, element: T) -> int:
        """
        获取元素所属集合的大小
        
        Args:
            element: 要查询的元素
            
        Returns:
            集合大小（元素数量）
        """
        root = self.find(element)
        return self._size[root]
    
    def get_sets(self) -> List[Set[T]]:
        """
        获取所有集合
        
        Returns:
            集合列表，每个集合是一个包含该集合所有元素的 set
        """
        sets_dict: Dict[T, Set[T]] = defaultdict(set)
        
        for element in self._parent:
            root = self.find(element)
            sets_dict[root].add(element)
        
        return list(sets_dict.values())
    
    def get_set(self, element: T) -> Set[T]:
        """
        获取元素所属集合的所有元素
        
        Args:
            element: 要查询的元素
            
        Returns:
            该集合的所有元素
        """
        root = self.find(element)
        return {elem for elem in self._parent if self.find(elem) == root}
    
    @property
    def set_count(self) -> int:
        """返回当前集合数量"""
        return self._count
    
    @property
    def element_count(self) -> int:
        """返回元素总数"""
        return len(self._parent)
    
    def is_empty(self) -> bool:
        """检查是否为空"""
        return len(self._parent) == 0
    
    def clear(self) -> None:
        """清空所有元素"""
        self._parent.clear()
        self._rank.clear()
        self._size.clear()
        self._count = 0
    
    def copy(self) -> 'DisjointSet[T]':
        """
        创建并查集的深拷贝
        
        Returns:
            新的 DisjointSet 实例
        """
        new_ds = DisjointSet()
        new_ds._parent = dict(self._parent)
        new_ds._rank = dict(self._rank)
        new_ds._size = dict(self._size)
        new_ds._count = self._count
        return new_ds
    
    def to_dict(self) -> Dict[str, Any]:
        """
        序列化为字典
        
        Returns:
            包含并查集状态的字典
        """
        return {
            'parent': dict(self._parent),
            'rank': dict(self._rank),
            'size': dict(self._size),
            'count': self._count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DisjointSet':
        """
        从字典反序列化
        
        Args:
            data: 包含并查集状态的字典
            
        Returns:
            新的 DisjointSet 实例
        """
        ds = cls()
        ds._parent = dict(data['parent'])
        ds._rank = dict(data['rank'])
        ds._size = dict(data['size'])
        ds._count = data['count']
        return ds
    
    def remove(self, element: T) -> bool:
        """
        从并查集中移除元素
        
        注意：如果移除的不是根节点，需要重建相关集合
        
        Args:
            element: 要移除的元素
            
        Returns:
            True 如果移除成功，False 如果元素不存在
        """
        if element not in self._parent:
            return False
        
        root = self.find(element)
        
        # 如果是根节点且集合大小 > 1，需要选择新根
        if element == root:
            children = [e for e in self._parent if self._parent[e] == element and e != element]
            
            if children:
                # 选择第一个子节点作为新根
                new_root = children[0]
                self._parent[new_root] = new_root
                self._rank[new_root] = self._rank[element]
                self._size[new_root] = self._size[element] - 1
                
                # 更新其他子节点的父指针
                for child in children[1:]:
                    self._parent[child] = new_root
            else:
                # 集合只有这一个元素
                self._count -= 1
        else:
            # 元素不是根，直接移除
            self._size[root] -= 1
        
        del self._parent[element]
        if element in self._rank:
            del self._rank[element]
        if element in self._size:
            del self._size[element]
        
        return True


class WeightedDisjointSet(Generic[T]):
    """
    带权并查集
    
    支持维护元素之间的相对权重/距离关系。
    常用于食物链问题、差分约束等场景。
    
    示例:
        >>> wds = WeightedDisjointSet()
        >>> wds.make_set(1)
        >>> wds.make_set(2)
        >>> wds.union(1, 2, weight=5)  # 2 比 1 重 5
        >>> wds.get_weight(1, 2)
        5
    """
    
    def __init__(self, elements: Optional[Iterable[T]] = None):
        """初始化带权并查集"""
        self._parent: Dict[T, T] = {}
        self._rank: Dict[T, int] = {}
        self._weight: Dict[T, float] = {}  # 到父节点的权重
        self._count: int = 0
        
        if elements:
            for elem in elements:
                self.make_set(elem)
    
    def __len__(self) -> int:
        """返回元素总数"""
        return len(self._parent)
    
    def __contains__(self, element: T) -> bool:
        """检查元素是否存在"""
        return element in self._parent
    
    def make_set(self, element: T) -> None:
        """创建新集合"""
        if element in self._parent:
            raise ValueError(f"元素 '{element}' 已存在")
        
        self._parent[element] = element
        self._rank[element] = 0
        self._weight[element] = 0
        self._count += 1
    
    def find(self, element: T) -> T:
        """
        查找根节点，同时维护权重路径
        
        返回根节点，并更新沿途权重
        """
        if element not in self._parent:
            raise KeyError(f"元素 '{element}' 不存在")
        
        if self._parent[element] != element:
            root = self.find(self._parent[element])
            self._weight[element] += self._weight[self._parent[element]]
            self._parent[element] = root
        
        return self._parent[element]
    
    def union(self, element1: T, element2: T, weight: float = 0) -> bool:
        """
        合并两个集合，设置相对权重
        
        Args:
            element1: 第一个元素
            element2: 第二个元素
            weight: element2 相对于 element1 的权重
                   (weight[element2] - weight[element1] = weight)
        """
        root1 = self.find(element1)
        root2 = self.find(element2)
        
        if root1 == root2:
            return False
        
        # 按 rank 合并
        if self._rank[root1] < self._rank[root2]:
            root1, root2 = root2, root1
            weight = -weight
        
        self._parent[root2] = root1
        self._weight[root2] = weight + self._weight[element1] - self._weight[element2]
        
        if self._rank[root1] == self._rank[root2]:
            self._rank[root1] += 1
        
        self._count -= 1
        return True
    
    def get_weight(self, element1: T, element2: T) -> Optional[float]:
        """
        获取两个元素之间的相对权重
        
        如果两个元素不在同一集合，返回 None
        """
        if not self.connected(element1, element2):
            return None
        
        return self._weight[element2] - self._weight[element1]
    
    def connected(self, element1: T, element2: T) -> bool:
        """检查两个元素是否在同一集合"""
        try:
            return self.find(element1) == self.find(element2)
        except KeyError:
            return False


def connected_components(edges: List[Tuple[T, T]]) -> List[Set[T]]:
    """
    从边列表计算连通分量
    
    Args:
        edges: 边列表，每条边是一个 (node1, node2) 元组
        
    Returns:
        连通分量列表
        
    示例:
        >>> edges = [(1, 2), (2, 3), (4, 5)]
        >>> connected_components(edges)
        [{1, 2, 3}, {4, 5}]
    """
    if not edges:
        return []
    
    # 收集所有节点
    nodes: Set[T] = set()
    for u, v in edges:
        nodes.add(u)
        nodes.add(v)
    
    ds = DisjointSet(nodes)
    
    for u, v in edges:
        ds.union(u, v)
    
    return ds.get_sets()


def detect_cycle_undirected(edges: List[Tuple[T, T]]) -> bool:
    """
    检测无向图中是否存在环
    
    使用并查集实现，时间复杂度 O(E * α(V))
    
    Args:
        edges: 边列表
        
    Returns:
        True 如果存在环，False 否则
        
    示例:
        >>> detect_cycle_undirected([(1, 2), (2, 3), (3, 1)])  # 三角形
        True
        >>> detect_cycle_undirected([(1, 2), (2, 3)])  # 线性
        False
    """
    if not edges:
        return False
    
    nodes: Set[T] = set()
    for u, v in edges:
        nodes.add(u)
        nodes.add(v)
    
    ds = DisjointSet(nodes)
    
    for u, v in edges:
        if ds.connected(u, v):
            return True
        ds.union(u, v)
    
    return False


def minimum_spanning_tree_kruskal(
    nodes: List[T],
    edges: List[Tuple[T, T, float]]
) -> Tuple[List[Tuple[T, T, float]], float]:
    """
    使用 Kruskal 算法求最小生成树
    
    Args:
        nodes: 节点列表
        edges: 边列表，每条边是 (node1, node2, weight) 元组
        
    Returns:
        (最小生成树的边列表, 总权重)
        
    示例:
        >>> nodes = [1, 2, 3, 4]
        >>> edges = [(1, 2, 1), (2, 3, 2), (3, 4, 3), (1, 4, 4)]
        >>> mst_edges, total = minimum_spanning_tree_kruskal(nodes, edges)
        >>> total
        6
    """
    if not nodes or not edges:
        return [], 0.0
    
    # 按权重排序边
    sorted_edges = sorted(edges, key=lambda e: e[2])
    
    ds = DisjointSet(nodes)
    mst_edges: List[Tuple[T, T, float]] = []
    total_weight = 0.0
    
    for u, v, w in sorted_edges:
        if ds.union(u, v):  # 如果合并成功（原本不在同一集合）
            mst_edges.append((u, v, w))
            total_weight += w
            
            if len(mst_edges) == len(nodes) - 1:
                break
    
    return mst_edges, total_weight


# 便捷函数
def create_disjoint_set(elements: Optional[Iterable[T]] = None) -> DisjointSet[T]:
    """创建并查集的便捷函数"""
    return DisjointSet(elements)


def create_weighted_disjoint_set(elements: Optional[Iterable[T]] = None) -> WeightedDisjointSet[T]:
    """创建带权并查集的便捷函数"""
    return WeightedDisjointSet(elements)


if __name__ == '__main__':
    # 简单演示
    print("=== 并查集基本演示 ===")
    
    # 创建并查集
    ds = DisjointSet(range(1, 6))
    print(f"初始状态: {ds}")
    print(f"集合数量: {ds.set_count}")
    
    # 合并操作
    ds.union(1, 2)
    ds.union(3, 4)
    print(f"合并 (1,2) 和 (3,4) 后: {ds}")
    
    ds.union(2, 3)
    print(f"合并 (2,3) 后: {ds}")
    print(f"连通性 1-4: {ds.connected(1, 4)}")
    print(f"连通性 1-5: {ds.connected(1, 5)}")
    print(f"集合大小: {ds.get_set_size(1)}")
    
    print("\n=== 最小生成树演示 ===")
    nodes = ['A', 'B', 'C', 'D']
    edges = [
        ('A', 'B', 4),
        ('A', 'C', 2),
        ('B', 'C', 1),
        ('B', 'D', 3),
        ('C', 'D', 5)
    ]
    
    mst, total = minimum_spanning_tree_kruskal(nodes, edges)
    print(f"MST 边: {mst}")
    print(f"总权重: {total}")