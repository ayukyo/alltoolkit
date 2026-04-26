"""
并查集（Disjoint Set Union, DSU）工具模块

提供高效的集合合并与查询操作，支持路径压缩和按秩合并优化。
适用于连通分量、最小生成树(Kruskal)、网络连接等场景。

核心功能:
- 并查集数据结构
- 路径压缩优化
- 按秩合并优化
- 集合大小跟踪
- 连通性查询
"""

from typing import Dict, Generic, List, Optional, Set, Tuple, TypeVar

T = TypeVar('T')


class DisjointSet(Generic[T]):
    """
    泛型并查集实现
    
    支持任意可哈希类型的元素，使用路径压缩和按秩合并优化。
    
    时间复杂度:
    - find: O(α(n)) ≈ O(1)，α为反阿克曼函数
    - union: O(α(n)) ≈ O(1)
    - connected: O(α(n)) ≈ O(1)
    
    示例:
        >>> ds = DisjointSet[int]()
        >>> ds.union(1, 2)
        >>> ds.union(2, 3)
        >>> ds.connected(1, 3)
        True
        >>> ds.count_sets()
        1
    """
    
    def __init__(self) -> None:
        """初始化空的并查集"""
        self._parent: Dict[T, T] = {}      # 父节点映射
        self._rank: Dict[T, int] = {}       # 秩（树的高度估计）
        self._size: Dict[T, int] = {}       # 集合大小
        self._count = 0                      # 集合数量
    
    def make_set(self, x: T) -> None:
        """
        创建单元素集合
        
        Args:
            x: 要创建集合的元素
        """
        if x not in self._parent:
            self._parent[x] = x
            self._rank[x] = 0
            self._size[x] = 1
            self._count += 1
    
    def find(self, x: T) -> Optional[T]:
        """
        查找元素的根节点（代表元素）
        
        使用路径压缩优化，使后续查询更快。
        
        Args:
            x: 要查找的元素
            
        Returns:
            根节点，如果元素不存在则返回 None
        """
        if x not in self._parent:
            return None
        
        # 路径压缩：将路径上所有节点直接连到根
        if self._parent[x] != x:
            self._parent[x] = self.find(self._parent[x])
        return self._parent[x]
    
    def union(self, x: T, y: T) -> bool:
        """
        合并两个元素所在的集合
        
        使用按秩合并优化，保持树的平衡。
        
        Args:
            x: 第一个元素
            y: 第二个元素
            
        Returns:
            如果成功合并返回 True，如果已在同一集合返回 False
        """
        # 确保两个元素都存在
        if x not in self._parent:
            self.make_set(x)
        if y not in self._parent:
            self.make_set(y)
        
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x is None or root_y is None:
            return False
        
        # 已在同一集合
        if root_x == root_y:
            return False
        
        # 按秩合并：将较矮的树连到较高的树
        if self._rank[root_x] < self._rank[root_y]:
            root_x, root_y = root_y, root_x
        
        self._parent[root_y] = root_x
        self._size[root_x] += self._size[root_y]
        
        # 如果高度相同，合并后高度加1
        if self._rank[root_x] == self._rank[root_y]:
            self._rank[root_x] += 1
        
        self._count -= 1
        return True
    
    def connected(self, x: T, y: T) -> bool:
        """
        检查两个元素是否在同一集合中
        
        Args:
            x: 第一个元素
            y: 第二个元素
            
        Returns:
            如果在同一集合返回 True，否则返回 False
        """
        root_x = self.find(x)
        root_y = self.find(y)
        return root_x is not None and root_y is not None and root_x == root_y
    
    def count_sets(self) -> int:
        """
        获取当前集合数量
        
        Returns:
            集合数量
        """
        return self._count
    
    def set_size(self, x: T) -> int:
        """
        获取元素所在集合的大小
        
        Args:
            x: 要查询的元素
            
        Returns:
            集合大小，如果元素不存在返回 0
        """
        root = self.find(x)
        if root is None:
            return 0
        return self._size[root]
    
    def get_sets(self) -> Dict[T, Set[T]]:
        """
        获取所有集合及其元素
        
        Returns:
            字典，键为根节点，值为集合中的所有元素
        """
        sets: Dict[T, Set[T]] = {}
        for x in self._parent:
            root = self.find(x)
            if root is not None:
                if root not in sets:
                    sets[root] = set()
                sets[root].add(x)
        return sets
    
    def get_elements(self) -> Set[T]:
        """
        获取所有元素
        
        Returns:
            所有元素的集合
        """
        return set(self._parent.keys())
    
    def __len__(self) -> int:
        """返回元素总数"""
        return len(self._parent)
    
    def __contains__(self, x: T) -> bool:
        """检查元素是否在并查集中"""
        return x in self._parent
    
    def __repr__(self) -> str:
        return f"DisjointSet(elements={len(self)}, sets={self._count})"


class WeightedDisjointSet(Generic[T]):
    """
    带权并查集实现
    
    维护节点间的关系权重。语义：union(x, y, w) 表示 y 到 x 的偏移量为 w。
    即：如果 union(A, B, 2)，则 B 的值 = A 的值 + 2。
    
    get_weight(x, y) 返回 y 相对于 x 的偏移量：y = x + get_weight(x, y)
    
    适用场景:
    - 判断变量间的相对关系
    - 食物链问题
    - 差分约束
    
    示例:
        >>> wds = WeightedDisjointSet[str]()
        >>> wds.union_with_weight('A', 'B', 2)  # B = A + 2
        >>> wds.union_with_weight('B', 'C', 3)  # C = B + 3, 所以 C = A + 5
        >>> wds.get_weight('A', 'C')  # C 相对于 A 的偏移
        5.0
    """
    
    def __init__(self) -> None:
        """初始化空的带权并查集"""
        self._parent: Dict[T, T] = {}      # 父节点
        self._diff: Dict[T, float] = {}    # 到父节点的偏移量
        self._rank: Dict[T, int] = {}      # 秩
    
    def make_set(self, x: T) -> None:
        """创建单元素集合"""
        if x not in self._parent:
            self._parent[x] = x
            self._diff[x] = 0.0
            self._rank[x] = 0
    
    def find(self, x: T) -> Optional[Tuple[T, float]]:
        """
        查找根节点和到根的累积偏移量
        
        Args:
            x: 要查找的元素
            
        Returns:
            (根节点, x相对于根的偏移量)，不存在返回 None
        """
        if x not in self._parent:
            return None
        
        if self._parent[x] == x:
            return (x, 0.0)
        
        # 递归查找根
        result = self.find(self._parent[x])
        if result is None:
            return None
        
        root, parent_diff = result
        # 路径压缩，更新偏移量
        self._diff[x] += parent_diff
        self._parent[x] = root
        
        return (root, self._diff[x])
    
    def union_with_weight(self, x: T, y: T, w: float) -> bool:
        """
        合并集合，设置 x - y = w
        
        Args:
            x: 第一个元素
            y: 第二个元素  
            w: 偏移量（x - y = w，即 x = y + w）
            
        Returns:
            合并成功返回 True，已在同一集合返回 False
        """
        if x not in self._parent:
            self.make_set(x)
        if y not in self._parent:
            self.make_set(y)
        
        x_result = self.find(x)
        y_result = self.find(y)
        
        if x_result is None or y_result is None:
            return False
        
        root_x, diff_x = x_result  # x 相对于 root_x 的偏移
        root_y, diff_y = y_result  # y 相对于 root_y 的偏移
        
        # 已在同一集合
        if root_x == root_y:
            return False
        
        # 按秩合并
        # 需要设置: root_y 的父节点为 root_x
        # 使得: diff_y + new_diff = diff_x + w (即 y 的根相对于 x 的根)
        # new_diff = diff_x + w - diff_y
        if self._rank[root_x] < self._rank[root_y]:
            root_x, root_y = root_y, root_x
            diff_x, diff_y = diff_y, diff_x
            w = -w  # 因为交换了 x, y，所以关系变成 y - x = w，即 x - y = -w
        
        self._parent[root_y] = root_x
        self._diff[root_y] = diff_x + w - diff_y
        
        if self._rank[root_x] == self._rank[root_y]:
            self._rank[root_x] += 1
        
        return True
    
    def get_weight(self, x: T, y: T) -> Optional[float]:
        """
        获取两个元素间的偏移量
        
        Args:
            x: 第一个元素
            y: 第二个元素
            
        Returns:
            y 相对于 x 的偏移量（y = x + 返回值），如果不在同一集合返回 None
        """
        x_result = self.find(x)
        y_result = self.find(y)
        
        if x_result is None or y_result is None:
            return None
        
        root_x, diff_x = x_result
        root_y, diff_y = y_result
        
        if root_x != root_y:
            return None
        
        # x 到根的偏移是 diff_x，y 到根的偏移是 diff_y
        # y 相对于 x 的偏移 = diff_y - diff_x
        return diff_y - diff_x


class UnionFind:
    """
    整数并查集的优化实现
    
    针对连续整数索引优化的高性能版本，使用列表而非字典。
    
    示例:
        >>> uf = UnionFind(5)  # 元素 0-4
        >>> uf.union(0, 1)
        >>> uf.union(1, 2)
        >>> uf.find(2)
        0
        >>> uf.connected(0, 2)
        True
    """
    
    def __init__(self, n: int) -> None:
        """
        初始化 n 个元素的并查集
        
        Args:
            n: 元素数量（元素为 0 到 n-1）
        """
        self._parent = list(range(n))
        self._rank = [0] * n
        self._size = [1] * n
        self._count = n
    
    def find(self, x: int) -> int:
        """
        查找元素的根节点
        
        Args:
            x: 要查找的元素
            
        Returns:
            根节点
        """
        if self._parent[x] != x:
            self._parent[x] = self.find(self._parent[x])
        return self._parent[x]
    
    def union(self, x: int, y: int) -> bool:
        """
        合并两个元素所在的集合
        
        Args:
            x: 第一个元素
            y: 第二个元素
            
        Returns:
            合并成功返回 True，已在同一集合返回 False
        """
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
        
        # 按秩合并
        if self._rank[root_x] < self._rank[root_y]:
            root_x, root_y = root_y, root_x
        
        self._parent[root_y] = root_x
        self._size[root_x] += self._size[root_y]
        
        if self._rank[root_x] == self._rank[root_y]:
            self._rank[root_x] += 1
        
        self._count -= 1
        return True
    
    def connected(self, x: int, y: int) -> bool:
        """检查两个元素是否连通"""
        return self.find(x) == self.find(y)
    
    def count_sets(self) -> int:
        """获取集合数量"""
        return self._count
    
    def set_size(self, x: int) -> int:
        """获取元素所在集合的大小"""
        return self._size[self.find(x)]
    
    def reset(self) -> None:
        """重置并查集到初始状态"""
        n = len(self._parent)
        self._parent = list(range(n))
        self._rank = [0] * n
        self._size = [1] * n
        self._count = n
    
    def __repr__(self) -> str:
        return f"UnionFind(elements={len(self._parent)}, sets={self._count})"


def connected_components(n: int, edges: List[Tuple[int, int]]) -> List[List[int]]:
    """
    计算图的连通分量
    
    Args:
        n: 节点数量（节点为 0 到 n-1）
        edges: 边列表，每条边为 (u, v)
        
    Returns:
        连通分量列表，每个分量是节点列表
        
    示例:
        >>> edges = [(0, 1), (1, 2), (3, 4)]
        >>> connected_components(5, edges)
        [[0, 1, 2], [3, 4]]
    """
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    
    # 按根节点分组
    components: Dict[int, List[int]] = {}
    for i in range(n):
        root = uf.find(i)
        if root not in components:
            components[root] = []
        components[root].append(i)
    
    return list(components.values())


def detect_cycle_undirected(n: int, edges: List[Tuple[int, int]]) -> bool:
    """
    检测无向图中是否存在环
    
    Args:
        n: 节点数量
        edges: 边列表
        
    Returns:
        存在环返回 True，否则返回 False
        
    示例:
        >>> detect_cycle_undirected(3, [(0, 1), (1, 2), (2, 0)])
        True
        >>> detect_cycle_undirected(3, [(0, 1), (1, 2)])
        False
    """
    uf = UnionFind(n)
    for u, v in edges:
        if uf.connected(u, v):
            return True
        uf.union(u, v)
    return False


def kruskal_mst(n: int, edges: List[Tuple[int, int, float]]) -> Tuple[float, List[Tuple[int, int, float]]]:
    """
    Kruskal 最小生成树算法
    
    Args:
        n: 节点数量
        edges: 边列表，每条边为 (u, v, weight)
        
    Returns:
        (最小生成树权重, 最小生成树的边列表)
        如果图不连通，返回 (float('inf'), [])
        
    示例:
        >>> edges = [(0, 1, 1), (1, 2, 2), (0, 2, 3)]
        >>> weight, mst = kruskal_mst(3, edges)
        >>> weight
        3.0
    """
    # 按权重排序
    sorted_edges = sorted(edges, key=lambda e: e[2])
    
    uf = UnionFind(n)
    mst_edges: List[Tuple[int, int, float]] = []
    total_weight = 0.0
    
    for u, v, w in sorted_edges:
        if not uf.connected(u, v):
            uf.union(u, v)
            mst_edges.append((u, v, w))
            total_weight += w
            
            if len(mst_edges) == n - 1:
                break
    
    # 检查是否连通
    if len(mst_edges) != n - 1:
        return (float('inf'), [])
    
    return (total_weight, mst_edges)


def accounts_merge(accounts: List[Tuple[str, List[str]]]) -> List[Tuple[str, List[str]]]:
    """
    合并具有相同邮箱的账户
    
    Args:
        accounts: 账户列表，每个账户为 (名称, 邮箱列表)
        
    Returns:
        合并后的账户列表
        
    示例:
        >>> accounts = [
        ...     ("John", ["john@email.com", "john.smith@email.com"]),
        ...     ("John", ["john.smith@email.com", "john.doe@email.com"]),
        ...     ("Mary", ["mary@email.com"])
        ... ]
        >>> merged = accounts_merge(accounts)
        >>> len(merged)
        2
    """
    ds = DisjointSet[int]()
    email_to_idx: Dict[str, int] = {}
    email_to_name: Dict[str, str] = {}
    
    idx = 0
    for name, emails in accounts:
        for email in emails:
            email_to_name[email] = name
            if email not in email_to_idx:
                email_to_idx[email] = idx
                idx += 1
            # 将同一账户的所有邮箱合并
            if emails[0] in email_to_idx:
                ds.union(email_to_idx[emails[0]], email_to_idx[email])
    
    # 按根节点分组邮箱
    merged: Dict[int, List[str]] = {}
    for email, i in email_to_idx.items():
        root = ds.find(i)
        if root is not None:
            if root not in merged:
                merged[root] = []
            merged[root].append(email)
    
    # 构建结果
    result: List[Tuple[str, List[str]]] = []
    for emails in merged.values():
        name = email_to_name[emails[0]]
        result.append((name, sorted(emails)))
    
    return result