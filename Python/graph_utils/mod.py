"""
Graph Utils - 图论算法工具包

提供完整的图论算法实现，零外部依赖，仅使用 Python 标准库。

功能:
- 图的表示和操作（邻接表/邻接矩阵）
- 遍历算法（BFS/DFS）
- 最短路径算法（Dijkstra/Bellman-Ford/Floyd-Warshall）
- 最小生成树（Prim/Kruskal）
- 拓扑排序
- 连通分量
- 环检测
- 二分图检测
- 其他实用算法

作者: AllToolkit
日期: 2026-04-21
"""

from collections import deque, defaultdict
from typing import (
    Any, Callable, Dict, Generic, Hashable, List, Optional, 
    Set, Tuple, TypeVar, Union
)
from heapq import heappush, heappop
import copy

T = TypeVar('T', bound=Hashable)
Weight = Union[int, float]


class Graph(Generic[T]):
    """
    通用图数据结构，支持有向/无向、带权/无权图。
    
    内部使用邻接表表示，支持任意可哈希的节点类型。
    
    示例:
        >>> g = Graph[str]()
        >>> g.add_edge("A", "B", weight=5)
        >>> g.add_edge("B", "C")
        >>> g.neighbors("A")
        [('B', 5)]
    """
    
    def __init__(self, directed: bool = False):
        """
        初始化图。
        
        Args:
            directed: 是否为有向图，默认 False（无向图）
        """
        self.directed = directed
        self._adj: Dict[T, List[Tuple[T, Weight]]] = defaultdict(list)
        self._nodes: Set[T] = set()
    
    def add_node(self, node: T) -> None:
        """添加节点。"""
        self._nodes.add(node)
    
    def add_edge(self, u: T, v: T, weight: Weight = 1) -> None:
        """
        添加边。
        
        Args:
            u: 起点
            v: 终点
            weight: 边权重，默认为 1
        """
        self._nodes.add(u)
        self._nodes.add(v)
        self._adj[u].append((v, weight))
        
        if not self.directed:
            self._adj[v].append((u, weight))
    
    def remove_edge(self, u: T, v: T) -> bool:
        """
        移除边。
        
        Returns:
            是否成功移除
        """
        removed = False
        self._adj[u] = [(n, w) for n, w in self._adj[u] if n != v]
        removed = len(self._adj[u]) < len([n for n, w in self._adj.get(u, []) if n == v]) + len(self._adj[u])
        
        if not self.directed and u in self._adj:
            original_len = len(self._adj.get(v, []))
            self._adj[v] = [(n, w) for n, w in self._adj.get(v, []) if n != u]
            removed = original_len > len(self._adj.get(v, []))
        
        return removed
    
    def remove_node(self, node: T) -> bool:
        """
        移除节点及其所有关联边。
        
        Returns:
            是否成功移除
        """
        if node not in self._nodes:
            return False
        
        self._nodes.discard(node)
        del self._adj[node]
        
        # 移除所有指向该节点的边
        for u in self._adj:
            self._adj[u] = [(v, w) for v, w in self._adj[u] if v != node]
        
        return True
    
    def neighbors(self, node: T) -> List[Tuple[T, Weight]]:
        """获取节点的邻居及边权重。"""
        return self._adj.get(node, [])
    
    def get_nodes(self) -> Set[T]:
        """获取所有节点。"""
        return self._nodes.copy()
    
    def get_edges(self) -> List[Tuple[T, T, Weight]]:
        """获取所有边（起点，终点，权重）。"""
        edges = []
        seen = set()
        
        for u in self._adj:
            for v, w in self._adj[u]:
                if self.directed:
                    edges.append((u, v, w))
                else:
                    edge_key = (min(u, v), max(u, v))
                    if edge_key not in seen:
                        edges.append((u, v, w))
                        seen.add(edge_key)
        
        return edges
    
    def has_node(self, node: T) -> bool:
        """检查节点是否存在。"""
        return node in self._nodes
    
    def has_edge(self, u: T, v: T) -> bool:
        """检查边是否存在。"""
        return any(n == v for n, _ in self._adj.get(u, []))
    
    def degree(self, node: T) -> int:
        """获取节点的度。"""
        return len(self._adj.get(node, []))
    
    def node_count(self) -> int:
        """获取节点数量。"""
        return len(self._nodes)
    
    def edge_count(self) -> int:
        """获取边数量。"""
        if self.directed:
            return sum(len(adj) for adj in self._adj.values())
        return len(self.get_edges())
    
    def copy(self) -> 'Graph[T]':
        """创建图的深拷贝。"""
        new_graph = Graph[T](directed=self.directed)
        new_graph._nodes = self._nodes.copy()
        new_graph._adj = defaultdict(list)
        for u in self._adj:
            new_graph._adj[u] = self._adj[u].copy()
        return new_graph
    
    def to_adjacency_matrix(self) -> Tuple[List[T], List[List[Weight]]]:
        """
        转换为邻接矩阵表示。
        
        Returns:
            (节点列表, 邻接矩阵)
        """
        nodes = sorted(self._nodes, key=lambda x: (str(type(x)), str(x)))
        n = len(nodes)
        node_index = {node: i for i, node in enumerate(nodes)}
        
        # 使用无穷大表示无连接
        matrix = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            matrix[i][i] = 0  # 对角线为0
        
        for u in self._adj:
            for v, w in self._adj[u]:
                i, j = node_index[u], node_index[v]
                matrix[i][j] = w
        
        return nodes, matrix
    
    @classmethod
    def from_edges(cls, edges: List[Tuple[T, T]], directed: bool = False) -> 'Graph[T]':
        """
        从边列表创建图。
        
        Args:
            edges: 边列表，每条边为 (u, v) 或 (u, v, weight)
            directed: 是否为有向图
        
        Returns:
            新建的图
        """
        graph = cls[T](directed=directed)
        for edge in edges:
            if len(edge) == 2:
                graph.add_edge(edge[0], edge[1])
            else:
                graph.add_edge(edge[0], edge[1], edge[2])
        return graph


# ============================================================================
# 遍历算法
# ============================================================================

def bfs(g: Graph[T], start: T) -> List[T]:
    """
    广度优先搜索遍历。
    
    Args:
        g: 图
        start: 起始节点
    
    Returns:
        遍历顺序节点列表
    """
    if start not in g.get_nodes():
        return []
    
    visited = set()
    result = []
    queue = deque([start])
    visited.add(start)
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor, _ in g.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return result


def dfs(g: Graph[T], start: T, recursive: bool = True) -> List[T]:
    """
    深度优先搜索遍历。
    
    Args:
        g: 图
        start: 起始节点
        recursive: 是否使用递归实现，默认 True
    
    Returns:
        遍历顺序节点列表
    """
    if start not in g.get_nodes():
        return []
    
    if recursive:
        visited = set()
        result = []
        
        def _dfs(node: T) -> None:
            visited.add(node)
            result.append(node)
            for neighbor, _ in g.neighbors(node):
                if neighbor not in visited:
                    _dfs(neighbor)
        
        _dfs(start)
        return result
    else:
        # 迭代实现
        visited = set()
        result = []
        stack = [start]
        
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                result.append(node)
                # 逆序入栈以保持正确顺序
                for neighbor, _ in reversed(g.neighbors(node)):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return result


def dfs_postorder(g: Graph[T], start: T) -> List[T]:
    """
    后序深度优先遍历（先访问子节点再访问当前节点）。
    
    用于拓扑排序等场景。
    """
    if start not in g.get_nodes():
        return []
    
    visited = set()
    result = []
    
    def _postorder(node: T) -> None:
        visited.add(node)
        for neighbor, _ in g.neighbors(node):
            if neighbor not in visited:
                _postorder(neighbor)
        result.append(node)
    
    _postorder(start)
    return result


# ============================================================================
# 最短路径算法
# ============================================================================

def dijkstra(g: Graph[T], start: T, end: Optional[T] = None) -> Dict[T, Tuple[Weight, Optional[T]]]:
    """
    Dijkstra 最短路径算法。
    
    时间复杂度: O((V + E) log V)
    
    Args:
        g: 图（边权重必须非负）
        start: 起点
        end: 可选终点，若指定则提前终止
    
    Returns:
        字典: {节点: (最短距离, 前驱节点)}
    
    Raises:
        ValueError: 存在负权边
    """
    # 检查负权边
    for u, v, w in g.get_edges():
        if w < 0:
            raise ValueError("Dijkstra 算法不支持负权边")
    
    if start not in g.get_nodes():
        return {}
    
    # 初始化
    distances: Dict[T, Weight] = {node: float('inf') for node in g.get_nodes()}
    distances[start] = 0
    predecessors: Dict[T, Optional[T]] = {node: None for node in g.get_nodes()}
    visited: Set[T] = set()
    
    # 优先队列: (距离, 节点)
    heap = [(0, start)]
    
    while heap:
        dist, node = heappop(heap)
        
        if node in visited:
            continue
        visited.add(node)
        
        # 提前终止
        if end is not None and node == end:
            break
        
        for neighbor, weight in g.neighbors(node):
            if neighbor in visited:
                continue
            
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                predecessors[neighbor] = node
                heappush(heap, (new_dist, neighbor))
    
    return {node: (distances[node], predecessors[node]) for node in g.get_nodes()}


def bellman_ford(g: Graph[T], start: T) -> Tuple[Dict[T, Tuple[Weight, Optional[T]]], bool]:
    """
    Bellman-Ford 最短路径算法。
    
    支持负权边，可检测负环。
    
    时间复杂度: O(V * E)
    
    Args:
        g: 图
        start: 起点
    
    Returns:
        (结果字典, 是否存在负环)
        结果字典: {节点: (最短距离, 前驱节点)}
    """
    if start not in g.get_nodes():
        return {}, False
    
    nodes = g.get_nodes()
    distances: Dict[T, Weight] = {node: float('inf') for node in nodes}
    distances[start] = 0
    predecessors: Dict[T, Optional[T]] = {node: None for node in nodes}
    
    edges = g.get_edges()
    
    # 松弛 V-1 次
    for _ in range(len(nodes) - 1):
        updated = False
        for u, v, w in edges:
            if distances[u] != float('inf') and distances[u] + w < distances[v]:
                distances[v] = distances[u] + w
                predecessors[v] = u
                updated = True
        if not updated:
            break
    
    # 检测负环
    has_negative_cycle = False
    for u, v, w in edges:
        if distances[u] != float('inf') and distances[u] + w < distances[v]:
            has_negative_cycle = True
            break
    
    return {node: (distances[node], predecessors[node]) for node in nodes}, has_negative_cycle


def floyd_warshall(g: Graph[T]) -> Tuple[Dict[T, Dict[T, Weight]], Dict[T, Dict[T, Optional[T]]]]:
    """
    Floyd-Warshall 全源最短路径算法。
    
    时间复杂度: O(V^3)
    
    Args:
        g: 图
    
    Returns:
        (距离矩阵, 前驱矩阵)
        距离矩阵: dist[u][v] = u到v的最短距离
        前驱矩阵: pred[u][v] = u到v路径上v的前驱节点
    """
    nodes = list(g.get_nodes())
    n = len(nodes)
    
    # 初始化距离矩阵
    dist: Dict[T, Dict[T, Weight]] = {u: {v: float('inf') for v in nodes} for u in nodes}
    pred: Dict[T, Dict[T, Optional[T]]] = {u: {v: None for v in nodes} for u in nodes}
    
    for u in nodes:
        dist[u][u] = 0
    
    for u, v, w in g.get_edges():
        dist[u][v] = w
        pred[u][v] = u
    
    # 动态规划
    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    pred[i][j] = pred[k][j]
    
    return dist, pred


def get_path(predecessors: Dict[T, Optional[T]], start: T, end: T) -> List[T]:
    """
    从前驱字典重构路径。
    
    Args:
        predecessors: 前驱节点字典
        start: 起点
        end: 终点
    
    Returns:
        路径节点列表，若不存在路径则返回空列表
    """
    if end not in predecessors:
        return []
    
    path = []
    current: Optional[T] = end
    
    while current is not None:
        path.append(current)
        current = predecessors.get(current)
    
    path.reverse()
    
    # 验证路径起点
    if path and path[0] == start:
        return path
    return []


# ============================================================================
# 最小生成树算法
# ============================================================================

def prim(g: Graph[T], start: Optional[T] = None) -> List[Tuple[T, T, Weight]]:
    """
    Prim 最小生成树算法。
    
    适用于连通无向图。
    
    时间复杂度: O((V + E) log V)
    
    Args:
        g: 无向连通图
        start: 可选起始节点
    
    Returns:
        最小生成树的边列表 [(u, v, weight), ...]
    """
    if g.directed:
        raise ValueError("Prim 算法仅适用于无向图")
    
    nodes = g.get_nodes()
    if not nodes:
        return []
    
    if start is None:
        start = next(iter(nodes))
    
    if start not in nodes:
        return []
    
    mst_edges: List[Tuple[T, T, Weight]] = []
    visited: Set[T] = set()
    
    # 优先队列: (权重, 节点, 前驱节点)
    heap = [(0, start, None)]
    
    while heap and len(visited) < len(nodes):
        weight, node, pred = heappop(heap)
        
        if node in visited:
            continue
        visited.add(node)
        
        if pred is not None:
            mst_edges.append((pred, node, weight))
        
        for neighbor, w in g.neighbors(node):
            if neighbor not in visited:
                heappush(heap, (w, neighbor, node))
    
    return mst_edges


def kruskal(g: Graph[T]) -> List[Tuple[T, T, Weight]]:
    """
    Kruskal 最小生成树算法。
    
    适用于无向图，可处理非连通图（返回最小生成森林）。
    
    时间复杂度: O(E log E)
    
    Args:
        g: 无向图
    
    Returns:
        最小生成树/森林的边列表
    """
    if g.directed:
        raise ValueError("Kruskal 算法仅适用于无向图")
    
    # 并查集
    parent: Dict[T, T] = {}
    rank: Dict[T, int] = {}
    
    def find(x: T) -> T:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x: T, y: T) -> bool:
        px, py = find(x), find(y)
        if px == py:
            return False
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1
        return True
    
    # 初始化并查集
    for node in g.get_nodes():
        parent[node] = node
        rank[node] = 0
    
    # 按权重排序边
    edges = sorted(g.get_edges(), key=lambda e: e[2])
    
    mst_edges: List[Tuple[T, T, Weight]] = []
    
    for u, v, w in edges:
        if union(u, v):
            mst_edges.append((u, v, w))
    
    return mst_edges


# ============================================================================
# 拓扑排序
# ============================================================================

def topological_sort(g: Graph[T]) -> Optional[List[T]]:
    """
    拓扑排序（Kahn 算法）。
    
    仅适用于有向无环图（DAG）。
    
    时间复杂度: O(V + E)
    
    Args:
        g: 有向图
    
    Returns:
        拓扑序列，若存在环则返回 None
    """
    if not g.directed:
        raise ValueError("拓扑排序仅适用于有向图")
    
    nodes = g.get_nodes()
    if not nodes:
        return []
    
    # 计算入度
    in_degree: Dict[T, int] = {node: 0 for node in nodes}
    for u in g._adj:
        for v, _ in g.neighbors(u):
            in_degree[v] = in_degree.get(v, 0) + 1
    
    # 初始化队列（入度为0的节点）
    queue = deque([node for node in nodes if in_degree[node] == 0])
    result: List[T] = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor, _ in g.neighbors(node):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # 检测环
    if len(result) != len(nodes):
        return None  # 存在环
    
    return result


def topological_sort_dfs(g: Graph[T]) -> Optional[List[T]]:
    """
    使用 DFS 实现的拓扑排序。
    
    Args:
        g: 有向图
    
    Returns:
        拓扑序列，若存在环则返回 None
    """
    if not g.directed:
        raise ValueError("拓扑排序仅适用于有向图")
    
    nodes = g.get_nodes()
    visited: Set[T] = set()
    temp_visited: Set[T] = set()
    result: List[T] = []
    
    def dfs(node: T) -> bool:
        if node in temp_visited:
            return False  # 存在环
        if node in visited:
            return True
        
        temp_visited.add(node)
        
        for neighbor, _ in g.neighbors(node):
            if not dfs(neighbor):
                return False
        
        temp_visited.remove(node)
        visited.add(node)
        result.append(node)
        return True
    
    for node in nodes:
        if node not in visited:
            if not dfs(node):
                return None
    
    result.reverse()
    return result


# ============================================================================
# 连通性算法
# ============================================================================

def connected_components(g: Graph[T]) -> List[Set[T]]:
    """
    查找无向图的连通分量。
    
    Args:
        g: 无向图
    
    Returns:
        连通分量列表，每个分量是节点集合
    """
    if g.directed:
        raise ValueError("connected_components 适用于无向图，请使用 strongly_connected_components 处理有向图")
    
    nodes = g.get_nodes()
    visited: Set[T] = set()
    components: List[Set[T]] = []
    
    for node in nodes:
        if node not in visited:
            component: Set[T] = set()
            queue = deque([node])
            visited.add(node)
            
            while queue:
                current = queue.popleft()
                component.add(current)
                
                for neighbor, _ in g.neighbors(current):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            
            components.append(component)
    
    return components


def is_connected(g: Graph[T]) -> bool:
    """
    检查无向图是否连通。
    """
    if g.directed:
        raise ValueError("is_connected 适用于无向图")
    
    nodes = g.get_nodes()
    if not nodes:
        return True
    
    # 从任意节点开始 BFS
    start = next(iter(nodes))
    visited = set(bfs(g, start))
    
    return visited == nodes


def strongly_connected_components(g: Graph[T]) -> List[Set[T]]:
    """
    查找有向图的强连通分量（Kosaraju 算法）。
    
    时间复杂度: O(V + E)
    
    Args:
        g: 有向图
    
    Returns:
        强连通分量列表
    """
    if not g.directed:
        raise ValueError("strongly_connected_components 适用于有向图")
    
    nodes = g.get_nodes()
    visited: Set[T] = set()
    finish_order: List[T] = []
    
    # 第一次 DFS，记录完成顺序
    def dfs1(node: T) -> None:
        visited.add(node)
        for neighbor, _ in g.neighbors(node):
            if neighbor not in visited:
                dfs1(neighbor)
        finish_order.append(node)
    
    for node in nodes:
        if node not in visited:
            dfs1(node)
    
    # 构建反向图
    reversed_graph = Graph[T](directed=True)
    for node in nodes:
        reversed_graph.add_node(node)
    for u, v, w in g.get_edges():
        reversed_graph.add_edge(v, u, w)
    
    # 第二次 DFS，按完成时间的逆序
    visited.clear()
    components: List[Set[T]] = []
    
    def dfs2(node: T, component: Set[T]) -> None:
        visited.add(node)
        component.add(node)
        for neighbor, _ in reversed_graph.neighbors(node):
            if neighbor not in visited:
                dfs2(neighbor, component)
    
    for node in reversed(finish_order):
        if node not in visited:
            component: Set[T] = set()
            dfs2(node, component)
            components.append(component)
    
    return components


# ============================================================================
# 环检测
# ============================================================================

def has_cycle(g: Graph[T]) -> bool:
    """
    检测图中是否存在环。
    
    适用于有向图和无向图。
    """
    if g.directed:
        return _has_cycle_directed(g)
    else:
        return _has_cycle_undirected(g)


def _has_cycle_directed(g: Graph[T]) -> bool:
    """检测有向图中的环。"""
    nodes = g.get_nodes()
    visited: Set[T] = set()
    rec_stack: Set[T] = set()
    
    def dfs(node: T) -> bool:
        visited.add(node)
        rec_stack.add(node)
        
        for neighbor, _ in g.neighbors(node):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True
        
        rec_stack.remove(node)
        return False
    
    for node in nodes:
        if node not in visited:
            if dfs(node):
                return True
    
    return False


def _has_cycle_undirected(g: Graph[T]) -> bool:
    """检测无向图中的环。"""
    nodes = g.get_nodes()
    visited: Set[T] = set()
    
    def dfs(node: T, parent: Optional[T]) -> bool:
        visited.add(node)
        
        for neighbor, _ in g.neighbors(node):
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True
        
        return False
    
    for node in nodes:
        if node not in visited:
            if dfs(node, None):
                return True
    
    return False


def find_cycle(g: Graph[T]) -> Optional[List[T]]:
    """
    查找图中的一个环。
    
    Returns:
        环路径，若无环则返回 None
    """
    if g.directed:
        return _find_cycle_directed(g)
    else:
        return _find_cycle_undirected(g)


def _find_cycle_directed(g: Graph[T]) -> Optional[List[T]]:
    """查找有向图中的环。"""
    nodes = g.get_nodes()
    visited: Set[T] = set()
    rec_stack: Set[T] = set()
    path: List[T] = []
    
    def dfs(node: T) -> Optional[List[T]]:
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        
        for neighbor, _ in g.neighbors(node):
            if neighbor not in visited:
                result = dfs(neighbor)
                if result:
                    return result
            elif neighbor in rec_stack:
                # 找到环，重构环路径
                cycle_start = path.index(neighbor)
                return path[cycle_start:] + [neighbor]
        
        path.pop()
        rec_stack.remove(node)
        return None
    
    for node in nodes:
        if node not in visited:
            result = dfs(node)
            if result:
                return result
    
    return None


def _find_cycle_undirected(g: Graph[T]) -> Optional[List[T]]:
    """查找无向图中的环。"""
    nodes = g.get_nodes()
    visited: Set[T] = set()
    parent: Dict[T, Optional[T]] = {}
    
    def dfs(node: T, par: Optional[T]) -> Optional[List[T]]:
        visited.add(node)
        parent[node] = par
        
        for neighbor, _ in g.neighbors(node):
            if neighbor not in visited:
                parent[neighbor] = node
                result = dfs(neighbor, node)
                if result:
                    return result
            elif neighbor != par:
                # 找到环
                cycle = [neighbor, node]
                current = node
                while parent.get(current) != neighbor and parent.get(current) is not None:
                    current = parent[current]
                    cycle.insert(1, current)
                return cycle
        
        return None
    
    for node in nodes:
        if node not in visited:
            result = dfs(node, None)
            if result:
                return result
    
    return None


# ============================================================================
# 二分图检测
# ============================================================================

def is_bipartite(g: Graph[T]) -> Tuple[bool, Optional[Tuple[Set[T], Set[T]]]]:
    """
    检测图是否为二分图。
    
    二分图可以将节点分为两个集合，使得所有边都连接两个不同集合的节点。
    
    Args:
        g: 无向图
    
    Returns:
        (是否为二分图, (集合A, 集合B) 或 None)
    """
    if g.directed:
        raise ValueError("is_bipartite 适用于无向图")
    
    nodes = g.get_nodes()
    color: Dict[T, int] = {}  # 0 或 1
    
    def bfs_color(start: T) -> bool:
        queue = deque([start])
        color[start] = 0
        
        while queue:
            node = queue.popleft()
            for neighbor, _ in g.neighbors(node):
                if neighbor not in color:
                    color[neighbor] = 1 - color[node]
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False
        return True
    
    for node in nodes:
        if node not in color:
            if not bfs_color(node):
                return False, None
    
    set_a = {node for node, c in color.items() if c == 0}
    set_b = {node for node, c in color.items() if c == 1}
    
    return True, (set_a, set_b)


# ============================================================================
# 其他实用算法
# ============================================================================

def degree_sequence(g: Graph[T]) -> List[int]:
    """
    获取图的度序列（按降序排列）。
    """
    return sorted([g.degree(node) for node in g.get_nodes()], reverse=True)


def is_eulerian(g: Graph[T]) -> bool:
    """
    检测无向图是否为欧拉图（存在欧拉回路）。
    
    欧拉图的充要条件：连通且所有节点度数为偶数。
    """
    if g.directed:
        raise ValueError("is_eulerian 适用于无向图")
    
    if not is_connected(g):
        return False
    
    return all(g.degree(node) % 2 == 0 for node in g.get_nodes())


def is_semi_eulerian(g: Graph[T]) -> bool:
    """
    检测无向图是否为半欧拉图（存在欧拉路径）。
    
    半欧拉图的充要条件：连通且恰好有两个奇度节点。
    """
    if g.directed:
        raise ValueError("is_semi_eulerian 适用于无向图")
    
    if not is_connected(g):
        return False
    
    odd_degree_count = sum(1 for node in g.get_nodes() if g.degree(node) % 2 == 1)
    return odd_degree_count == 2


def articulation_points(g: Graph[T]) -> Set[T]:
    """
    查找无向图的割点（关节点）。
    
    割点是移除后会使图不连通的节点。
    
    时间复杂度: O(V + E)
    """
    if g.directed:
        raise ValueError("articulation_points 适用于无向图")
    
    nodes = g.get_nodes()
    if not nodes:
        return set()
    
    visited: Set[T] = set()
    disc: Dict[T, int] = {}  # 发现时间
    low: Dict[T, int] = {}   # 最早可到达祖先
    parent: Dict[T, Optional[T]] = {}
    ap: Set[T] = set()
    time = [0]  # 使用列表以便在闭包中修改
    
    def dfs(node: T) -> None:
        children = 0
        visited.add(node)
        disc[node] = low[node] = time[0]
        time[0] += 1
        
        for neighbor, _ in g.neighbors(node):
            if neighbor not in visited:
                children += 1
                parent[neighbor] = node
                dfs(neighbor)
                
                # 更新 low 值
                low[node] = min(low[node], low[neighbor])
                
                # 判断是否为割点
                if parent.get(node) is None and children > 1:
                    ap.add(node)
                if parent.get(node) is not None and low[neighbor] >= disc[node]:
                    ap.add(node)
            elif neighbor != parent.get(node):
                low[node] = min(low[node], disc[neighbor])
    
    for node in nodes:
        if node not in visited:
            parent[node] = None
            dfs(node)
    
    return ap


def bridges(g: Graph[T]) -> List[Tuple[T, T]]:
    """
    查找无向图的桥（割边）。
    
    桥是移除后会使图不连通的边。
    
    时间复杂度: O(V + E)
    """
    if g.directed:
        raise ValueError("bridges 适用于无向图")
    
    nodes = g.get_nodes()
    if not nodes:
        return []
    
    visited: Set[T] = set()
    disc: Dict[T, int] = {}
    low: Dict[T, int] = {}
    parent: Dict[T, Optional[T]] = {}
    bridge_list: List[Tuple[T, T]] = []
    time = [0]
    
    def dfs(node: T) -> None:
        visited.add(node)
        disc[node] = low[node] = time[0]
        time[0] += 1
        
        for neighbor, _ in g.neighbors(node):
            if neighbor not in visited:
                parent[neighbor] = node
                dfs(neighbor)
                
                low[node] = min(low[node], low[neighbor])
                
                # 判断是否为桥
                if low[neighbor] > disc[node]:
                    bridge_list.append((node, neighbor))
            elif neighbor != parent.get(node):
                low[node] = min(low[node], disc[neighbor])
    
    for node in nodes:
        if node not in visited:
            parent[node] = None
            dfs(node)
    
    return bridge_list


def shortest_path_bfs(g: Graph[T], start: T, end: T) -> Optional[List[T]]:
    """
    BFS 最短路径（无权图）。
    
    返回从 start 到 end 的最短路径，若不存在则返回 None。
    """
    if start not in g.get_nodes() or end not in g.get_nodes():
        return None
    
    if start == end:
        return [start]
    
    visited: Set[T] = set()
    parent: Dict[T, Optional[T]] = {start: None}
    queue = deque([start])
    visited.add(start)
    
    while queue:
        node = queue.popleft()
        
        for neighbor, _ in g.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                queue.append(neighbor)
                
                if neighbor == end:
                    # 重构路径
                    path = []
                    current: Optional[T] = end
                    while current is not None:
                        path.append(current)
                        current = parent[current]
                    path.reverse()
                    return path
    
    return None


def all_paths(g: Graph[T], start: T, end: T, max_paths: int = 1000) -> List[List[T]]:
    """
    查找所有从 start 到 end 的路径。
    
    Args:
        g: 图
        start: 起点
        end: 终点
        max_paths: 最大路径数，防止组合爆炸
    
    Returns:
        路径列表
    """
    if start not in g.get_nodes() or end not in g.get_nodes():
        return []
    
    paths: List[List[T]] = []
    
    def dfs(node: T, path: List[T], visited: Set[T]) -> None:
        if len(paths) >= max_paths:
            return
        
        path.append(node)
        visited.add(node)
        
        if node == end:
            paths.append(path.copy())
        else:
            for neighbor, _ in g.neighbors(node):
                if neighbor not in visited:
                    dfs(neighbor, path, visited)
        
        path.pop()
        visited.remove(node)
    
    dfs(start, [], set())
    return paths


def degree_centrality(g: Graph[T]) -> Dict[T, float]:
    """
    计算度中心性。
    
    度中心性 = 节点度数 / (n-1)
    """
    n = g.node_count()
    if n <= 1:
        return {node: 0.0 for node in g.get_nodes()}
    
    return {node: g.degree(node) / (n - 1) for node in g.get_nodes()}


def betweenness_centrality(g: Graph[T]) -> Dict[T, float]:
    """
    计算介数中心性（简化版）。
    
    介数中心性衡量节点在最短路径中的重要性。
    
    时间复杂度: O(V * (V + E))
    """
    nodes = list(g.get_nodes())
    n = len(nodes)
    if n <= 2:
        return {node: 0.0 for node in nodes}
    
    betweenness: Dict[T, float] = {node: 0.0 for node in nodes}
    
    for source in nodes:
        # BFS 计算最短路径
        stack: List[T] = []
        predecessors: Dict[T, List[T]] = {node: [] for node in nodes}
        sigma: Dict[T, int] = {node: 0 for node in nodes}  # 最短路径数
        sigma[source] = 1
        dist: Dict[T, int] = {node: -1 for node in nodes}
        dist[source] = 0
        queue = deque([source])
        
        while queue:
            v = queue.popleft()
            stack.append(v)
            for w, _ in g.neighbors(v):
                if dist[w] < 0:
                    queue.append(w)
                    dist[w] = dist[v] + 1
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]
                    predecessors[w].append(v)
        
        # 累积依赖
        delta: Dict[T, float] = {node: 0.0 for node in nodes}
        while stack:
            w = stack.pop()
            for v in predecessors[w]:
                delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
            if w != source:
                betweenness[w] += delta[w]
    
    # 归一化
    if not g.directed:
        scale = 2.0 / ((n - 1) * (n - 2))
    else:
        scale = 1.0 / ((n - 1) * (n - 2))
    
    return {node: betweenness[node] * scale for node in nodes}


def clustering_coefficient(g: Graph[T], node: Optional[T] = None) -> Union[float, Dict[T, float]]:
    """
    计算聚类系数。
    
    聚类系数衡量节点的邻居之间的连接程度。
    
    Args:
        g: 无向图
        node: 可选，计算单个节点的聚类系数
    
    Returns:
        单个节点的聚类系数或所有节点的聚类系数字典
    """
    if g.directed:
        raise ValueError("clustering_coefficient 适用于无向图")
    
    def _local_cc(n: T) -> float:
        neighbors = [v for v, _ in g.neighbors(n)]
        k = len(neighbors)
        if k < 2:
            return 0.0
        
        neighbor_set = set(neighbors)
        triangles = 0
        
        for i, u in enumerate(neighbors):
            for v in neighbors[i+1:]:
                if v in neighbor_set and g.has_edge(u, v):
                    triangles += 1
        
        return 2.0 * triangles / (k * (k - 1))
    
    if node is not None:
        return _local_cc(node)
    
    return {n: _local_cc(n) for n in g.get_nodes()}


def average_clustering_coefficient(g: Graph[T]) -> float:
    """计算平均聚类系数。"""
    cc = clustering_coefficient(g)
    if not cc:
        return 0.0
    return sum(cc.values()) / len(cc)


# 导出公共接口
__all__ = [
    # 图类
    'Graph',
    
    # 遍历
    'bfs',
    'dfs',
    'dfs_postorder',
    
    # 最短路径
    'dijkstra',
    'bellman_ford',
    'floyd_warshall',
    'get_path',
    'shortest_path_bfs',
    'all_paths',
    
    # 最小生成树
    'prim',
    'kruskal',
    
    # 拓扑排序
    'topological_sort',
    'topological_sort_dfs',
    
    # 连通性
    'connected_components',
    'is_connected',
    'strongly_connected_components',
    
    # 环检测
    'has_cycle',
    'find_cycle',
    
    # 二分图
    'is_bipartite',
    
    # 其他
    'degree_sequence',
    'is_eulerian',
    'is_semi_eulerian',
    'articulation_points',
    'bridges',
    'degree_centrality',
    'betweenness_centrality',
    'clustering_coefficient',
    'average_clustering_coefficient',
]