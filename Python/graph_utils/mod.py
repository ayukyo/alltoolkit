"""
Graph Utils - 图算法工具集

提供完整的图数据结构和算法实现，包括：
- 图表示（邻接表/邻接矩阵）
- 图遍历（BFS/DFS）
- 最短路径（Dijkstra/Bellman-Ford/Floyd-Warshall）
- 最小生成树（Kruskal/Prim）
- 拓扑排序
- 连通分量
- 环检测
- 二分图检测
- 欧拉路径
- 图工具函数

零依赖，纯 Python 标准库实现。
"""

from typing import (
    Dict, List, Set, Tuple, Optional, Callable, Any, Union,
    Iterator, TypeVar, Generic, Deque
)
from collections import deque, defaultdict
from dataclasses import dataclass, field
from enum import Enum
from heapq import heappush, heappop
import math

T = TypeVar('T')
Weight = Union[int, float]


class GraphType(Enum):
    """图类型枚举"""
    UNDIRECTED = "undirected"
    DIRECTED = "directed"


@dataclass
class Edge(Generic[T]):
    """边数据结构"""
    source: T
    target: T
    weight: Weight = 1.0
    
    def __hash__(self):
        return hash((self.source, self.target))
    
    def __eq__(self, other):
        if not isinstance(other, Edge):
            return False
        return self.source == other.source and self.target == other.target


@dataclass
class PathResult(Generic[T]):
    """路径结果"""
    path: List[T]
    distance: Weight
    found: bool
    
    def __len__(self) -> int:
        return len(self.path)


@dataclass
class MSTResult(Generic[T]):
    """最小生成树结果"""
    edges: List[Edge[T]]
    total_weight: Weight
    vertices: Set[T]


@dataclass
class ComponentResult(Generic[T]):
    """连通分量结果"""
    components: List[Set[T]]
    count: int
    is_connected: bool


class Graph(Generic[T]):
    """
    通用图数据结构
    
    支持邻接表和邻接矩阵两种表示方式，支持有向图和无向图。
    """
    
    def __init__(
        self, 
        graph_type: GraphType = GraphType.UNDIRECTED,
        representation: str = "adjacency_list"
    ):
        """
        初始化图
        
        Args:
            graph_type: 图类型（有向/无向）
            representation: 表示方式（adjacency_list/adjacency_matrix）
        """
        self.graph_type = graph_type
        self.representation = representation
        self._vertices: Set[T] = set()
        
        if representation == "adjacency_list":
            self._adj: Dict[T, Dict[T, Weight]] = defaultdict(dict)
        else:
            self._adj: Dict[T, Dict[T, Weight]] = {}
    
    @property
    def vertices(self) -> Set[T]:
        """获取所有顶点"""
        return self._vertices.copy()
    
    @property
    def edges(self) -> List[Edge[T]]:
        """获取所有边"""
        edge_set = set()
        for u in self._adj:
            for v, w in self._adj[u].items():
                edge_set.add(Edge(u, v, w))
                if self.graph_type == GraphType.UNDIRECTED:
                    edge_set.add(Edge(v, u, w))
        return list(edge_set)
    
    @property
    def vertex_count(self) -> int:
        """顶点数量"""
        return len(self._vertices)
    
    @property
    def edge_count(self) -> int:
        """边数量"""
        count = sum(len(neighbors) for neighbors in self._adj.values())
        if self.graph_type == GraphType.UNDIRECTED:
            count //= 2
        return count
    
    @property
    def is_directed(self) -> bool:
        """是否为有向图"""
        return self.graph_type == GraphType.DIRECTED
    
    def add_vertex(self, vertex: T) -> 'Graph[T]':
        """添加顶点"""
        self._vertices.add(vertex)
        if vertex not in self._adj:
            self._adj[vertex] = {}
        return self
    
    def add_edge(
        self, 
        source: T, 
        target: T, 
        weight: Weight = 1.0
    ) -> 'Graph[T]':
        """
        添加边
        
        Args:
            source: 起点
            target: 终点
            weight: 权重
        """
        self._vertices.add(source)
        self._vertices.add(target)
        
        if source not in self._adj:
            self._adj[source] = {}
        self._adj[source][target] = weight
        
        if self.graph_type == GraphType.UNDIRECTED:
            if target not in self._adj:
                self._adj[target] = {}
            self._adj[target][source] = weight
        
        return self
    
    def remove_edge(self, source: T, target: T) -> bool:
        """删除边"""
        if source in self._adj and target in self._adj[source]:
            del self._adj[source][target]
            if self.graph_type == GraphType.UNDIRECTED:
                if target in self._adj and source in self._adj[target]:
                    del self._adj[target][source]
            return True
        return False
    
    def remove_vertex(self, vertex: T) -> bool:
        """删除顶点及其所有边"""
        if vertex not in self._vertices:
            return False
        
        self._vertices.discard(vertex)
        
        # 删除所有出边
        if vertex in self._adj:
            del self._adj[vertex]
        
        # 删除所有入边
        for u in self._adj:
            if vertex in self._adj[u]:
                del self._adj[u][vertex]
        
        return True
    
    def has_vertex(self, vertex: T) -> bool:
        """检查顶点是否存在"""
        return vertex in self._vertices
    
    def has_edge(self, source: T, target: T) -> bool:
        """检查边是否存在"""
        return source in self._adj and target in self._adj[source]
    
    def get_edge_weight(self, source: T, target: T) -> Optional[Weight]:
        """获取边权重"""
        if self.has_edge(source, target):
            return self._adj[source][target]
        return None
    
    def get_neighbors(self, vertex: T) -> Dict[T, Weight]:
        """获取邻居节点及其权重"""
        if vertex not in self._adj:
            return {}
        return self._adj[vertex].copy()
    
    def get_degree(self, vertex: T) -> int:
        """获取顶点度数"""
        if self.is_directed:
            out_degree = len(self._adj.get(vertex, {}))
            in_degree = sum(1 for u in self._adj if vertex in self._adj[u])
            return in_degree + out_degree
        return len(self._adj.get(vertex, {}))
    
    def get_in_degree(self, vertex: T) -> int:
        """获取入度（有向图）"""
        return sum(1 for u in self._adj if vertex in self._adj[u])
    
    def get_out_degree(self, vertex: T) -> int:
        """获取出度（有向图）"""
        return len(self._adj.get(vertex, {}))
    
    def copy(self) -> 'Graph[T]':
        """复制图"""
        new_graph = Graph(self.graph_type, self.representation)
        new_graph._vertices = self._vertices.copy()
        new_graph._adj = {u: v.copy() for u, v in self._adj.items()}
        return new_graph
    
    def to_adjacency_matrix(self) -> Tuple[List[T], List[List[Weight]]]:
        """
        转换为邻接矩阵表示
        
        Returns:
            (顶点列表, 邻接矩阵)
        """
        vertices = sorted(self._vertices, key=str)
        n = len(vertices)
        vertex_index = {v: i for i, v in enumerate(vertices)}
        
        # 初始化矩阵（无穷大表示不可达）
        matrix = [[float('inf')] * n for _ in range(n)]
        
        # 对角线为0
        for i in range(n):
            matrix[i][i] = 0
        
        # 填充边
        for u in self._adj:
            for v, w in self._adj[u].items():
                i, j = vertex_index[u], vertex_index[v]
                matrix[i][j] = w
        
        return vertices, matrix
    
    @classmethod
    def from_edges(
        cls,
        edges: List[Tuple[T, T, Weight]],
        graph_type: GraphType = GraphType.UNDIRECTED
    ) -> 'Graph[T]':
        """从边列表创建图"""
        graph = cls(graph_type)
        for edge in edges:
            if len(edge) == 2:
                graph.add_edge(edge[0], edge[1])
            else:
                graph.add_edge(edge[0], edge[1], edge[2])
        return graph
    
    @classmethod
    def from_adjacency_list(
        cls,
        adj_list: Dict[T, List[Union[T, Tuple[T, Weight]]]],
        graph_type: GraphType = GraphType.UNDIRECTED
    ) -> 'Graph[T]':
        """从邻接表创建图"""
        graph = cls(graph_type)
        for u, neighbors in adj_list.items():
            for neighbor in neighbors:
                if isinstance(neighbor, tuple):
                    graph.add_edge(u, neighbor[0], neighbor[1])
                else:
                    graph.add_edge(u, neighbor)
        return graph


# ==================== 图遍历算法 ====================

def bfs(
    graph: Graph[T], 
    start: T,
    visit: Optional[Callable[[T], None]] = None
) -> List[T]:
    """
    广度优先搜索
    
    Args:
        graph: 图对象
        start: 起始顶点
        visit: 访问回调函数
    
    Returns:
        BFS 遍历顺序
    """
    if start not in graph.vertices:
        return []
    
    visited = set()
    result = []
    queue = deque([start])
    visited.add(start)
    
    while queue:
        vertex = queue.popleft()
        result.append(vertex)
        
        if visit:
            visit(vertex)
        
        for neighbor in graph.get_neighbors(vertex):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return result


def dfs(
    graph: Graph[T], 
    start: T,
    visit: Optional[Callable[[T], None]] = None
) -> List[T]:
    """
    深度优先搜索
    
    Args:
        graph: 图对象
        start: 起始顶点
        visit: 访问回调函数
    
    Returns:
        DFS 遍历顺序
    """
    if start not in graph.vertices:
        return []
    
    visited = set()
    result = []
    
    def _dfs(vertex: T):
        visited.add(vertex)
        result.append(vertex)
        
        if visit:
            visit(vertex)
        
        for neighbor in graph.get_neighbors(vertex):
            if neighbor not in visited:
                _dfs(neighbor)
    
    _dfs(start)
    return result


def dfs_iterative(
    graph: Graph[T], 
    start: T,
    visit: Optional[Callable[[T], None]] = None
) -> List[T]:
    """
    深度优先搜索（迭代版本）
    
    Args:
        graph: 图对象
        start: 起始顶点
        visit: 访问回调函数
    
    Returns:
        DFS 遍历顺序
    """
    if start not in graph.vertices:
        return []
    
    visited = set()
    result = []
    stack = [start]
    
    while stack:
        vertex = stack.pop()
        
        if vertex in visited:
            continue
        
        visited.add(vertex)
        result.append(vertex)
        
        if visit:
            visit(vertex)
        
        for neighbor in graph.get_neighbors(vertex):
            if neighbor not in visited:
                stack.append(neighbor)
    
    return result


# ==================== 最短路径算法 ====================

def dijkstra(
    graph: Graph[T], 
    start: T, 
    end: Optional[T] = None
) -> Union[PathResult[T], Dict[T, PathResult[T]]]:
    """
    Dijkstra 最短路径算法
    
    Args:
        graph: 图对象
        start: 起点
        end: 终点（可选，不提供则返回到所有点的最短路径）
    
    Returns:
        单点路径结果或所有点路径结果字典
    """
    if start not in graph.vertices:
        if end:
            return PathResult([], float('inf'), False)
        return {}
    
    distances: Dict[T, Weight] = {start: 0}
    previous: Dict[T, Optional[T]] = {start: None}
    visited = set()
    heap = [(0, start)]
    
    while heap:
        dist, vertex = heappop(heap)
        
        if vertex in visited:
            continue
        visited.add(vertex)
        
        if end and vertex == end:
            break
        
        for neighbor, weight in graph.get_neighbors(vertex).items():
            new_dist = dist + weight
            if neighbor not in distances or new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = vertex
                heappush(heap, (new_dist, neighbor))
    
    def build_path(target: T) -> PathResult[T]:
        if target not in distances:
            return PathResult([], float('inf'), False)
        
        path = []
        current: Optional[T] = target
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()
        
        return PathResult(path, distances[target], True)
    
    if end:
        return build_path(end)
    
    return {v: build_path(v) for v in graph.vertices if v in distances}


def bellman_ford(
    graph: Graph[T], 
    start: T
) -> Tuple[Dict[T, Weight], Dict[T, Optional[T]], bool]:
    """
    Bellman-Ford 最短路径算法（支持负权边）
    
    Args:
        graph: 图对象
        start: 起点
    
    Returns:
        (距离字典, 前驱字典, 是否存在负环)
    """
    if start not in graph.vertices:
        return {}, {}, False
    
    distances: Dict[T, Weight] = {v: float('inf') for v in graph.vertices}
    distances[start] = 0
    previous: Dict[T, Optional[T]] = {v: None for v in graph.vertices}
    
    # 松弛操作
    for _ in range(len(graph.vertices) - 1):
        for edge in graph.edges:
            if distances[edge.source] != float('inf'):
                new_dist = distances[edge.source] + edge.weight
                if new_dist < distances[edge.target]:
                    distances[edge.target] = new_dist
                    previous[edge.target] = edge.source
    
    # 检测负环
    has_negative_cycle = False
    for edge in graph.edges:
        if distances[edge.source] != float('inf'):
            if distances[edge.source] + edge.weight < distances[edge.target]:
                has_negative_cycle = True
                break
    
    return distances, previous, has_negative_cycle


def floyd_warshall(graph: Graph[T]) -> Tuple[Dict[T, Dict[T, Weight]], Dict[T, Dict[T, Optional[T]]]]:
    """
    Floyd-Warshall 全源最短路径算法
    
    Args:
        graph: 图对象
    
    Returns:
        (距离矩阵, 前驱矩阵)
    """
    vertices = list(graph.vertices)
    n = len(vertices)
    vertex_index = {v: i for i, v in enumerate(vertices)}
    
    # 初始化距离和前驱矩阵
    dist = {u: {v: float('inf') for v in vertices} for u in vertices}
    prev = {u: {v: None for v in vertices} for u in vertices}
    
    for v in vertices:
        dist[v][v] = 0
    
    for edge in graph.edges:
        dist[edge.source][edge.target] = edge.weight
        prev[edge.source][edge.target] = edge.source
    
    # 动态规划
    for k in vertices:
        for i in vertices:
            for j in vertices:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    prev[i][j] = prev[k][j]
    
    return dist, prev


# ==================== 最小生成树算法 ====================

def kruskal(graph: Graph[T]) -> MSTResult[T]:
    """
    Kruskal 最小生成树算法
    
    Args:
        graph: 图对象
    
    Returns:
        最小生成树结果
    """
    if graph.is_directed:
        raise ValueError("Kruskal 算法仅适用于无向图")
    
    if not graph.vertices:
        return MSTResult([], 0, set())
    
    # 并查集
    parent = {}
    rank = {}
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
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
    for v in graph.vertices:
        parent[v] = v
        rank[v] = 0
    
    # 按权重排序边
    edges = sorted(graph.edges, key=lambda e: e.weight)
    
    mst_edges = []
    total_weight = 0
    
    for edge in edges:
        if union(edge.source, edge.target):
            mst_edges.append(edge)
            total_weight += edge.weight
            
            # MST 有 n-1 条边
            if len(mst_edges) == len(graph.vertices) - 1:
                break
    
    return MSTResult(mst_edges, total_weight, graph.vertices.copy())


def prim(graph: Graph[T], start: Optional[T] = None) -> MSTResult[T]:
    """
    Prim 最小生成树算法
    
    Args:
        graph: 图对象
        start: 起始顶点（可选）
    
    Returns:
        最小生成树结果
    """
    if graph.is_directed:
        raise ValueError("Prim 算法仅适用于无向图")
    
    if not graph.vertices:
        return MSTResult([], 0, set())
    
    if start is None:
        start = next(iter(graph.vertices))
    
    if start not in graph.vertices:
        return MSTResult([], 0, set())
    
    in_mst = set()
    mst_edges = []
    total_weight = 0
    heap = [(0, start, None)]  # (weight, vertex, parent)
    
    while heap and len(in_mst) < len(graph.vertices):
        weight, vertex, parent = heappop(heap)
        
        if vertex in in_mst:
            continue
        
        in_mst.add(vertex)
        
        if parent is not None:
            mst_edges.append(Edge(parent, vertex, weight))
            total_weight += weight
        
        for neighbor, edge_weight in graph.get_neighbors(vertex).items():
            if neighbor not in in_mst:
                heappush(heap, (edge_weight, neighbor, vertex))
    
    return MSTResult(mst_edges, total_weight, graph.vertices.copy())


# ==================== 拓扑排序 ====================

def topological_sort(graph: Graph[T]) -> Optional[List[T]]:
    """
    拓扑排序（Kahn 算法）
    
    Args:
        graph: 图对象
    
    Returns:
        拓扑排序结果，如果存在环则返回 None
    """
    if not graph.is_directed:
        raise ValueError("拓扑排序仅适用于有向图")
    
    # 计算入度
    in_degree = {v: 0 for v in graph.vertices}
    for u in graph._adj:
        for v in graph._adj[u]:
            in_degree[v] = in_degree.get(v, 0) + 1
    
    # 将入度为0的顶点加入队列
    queue = deque([v for v in graph.vertices if in_degree[v] == 0])
    result = []
    
    while queue:
        vertex = queue.popleft()
        result.append(vertex)
        
        for neighbor in graph.get_neighbors(vertex):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # 如果结果长度小于顶点数，说明存在环
    if len(result) != len(graph.vertices):
        return None
    
    return result


def topological_sort_dfs(graph: Graph[T]) -> Optional[List[T]]:
    """
    拓扑排序（DFS 版本）
    
    Args:
        graph: 图对象
    
    Returns:
        拓扑排序结果，如果存在环则返回 None
    """
    if not graph.is_directed:
        raise ValueError("拓扑排序仅适用于有向图")
    
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {v: WHITE for v in graph.vertices}
    result = []
    has_cycle = False
    
    def dfs_visit(v: T) -> bool:
        nonlocal has_cycle
        color[v] = GRAY
        
        for neighbor in graph.get_neighbors(v):
            if color[neighbor] == GRAY:
                has_cycle = True
                return False
            if color[neighbor] == WHITE:
                if not dfs_visit(neighbor):
                    return False
        
        color[v] = BLACK
        result.append(v)
        return True
    
    for v in graph.vertices:
        if color[v] == WHITE:
            if not dfs_visit(v):
                break
    
    if has_cycle:
        return None
    
    result.reverse()
    return result


# ==================== 连通分量 ====================

def connected_components(graph: Graph[T]) -> ComponentResult[T]:
    """
    查找连通分量（无向图）
    
    Args:
        graph: 图对象
    
    Returns:
        连通分量结果
    """
    if graph.is_directed:
        raise ValueError("请使用 strongly_connected_components 处理有向图")
    
    visited = set()
    components = []
    
    for vertex in graph.vertices:
        if vertex not in visited:
            component = set()
            queue = deque([vertex])
            visited.add(vertex)
            
            while queue:
                v = queue.popleft()
                component.add(v)
                
                for neighbor in graph.get_neighbors(v):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            
            components.append(component)
    
    return ComponentResult(
        components=components,
        count=len(components),
        is_connected=len(components) == 1
    )


def strongly_connected_components(graph: Graph[T]) -> ComponentResult[T]:
    """
    查找强连通分量（有向图，Kosaraju 算法）
    
    Args:
        graph: 图对象
    
    Returns:
        强连通分量结果
    """
    if not graph.is_directed:
        raise ValueError("强连通分量仅适用于有向图")
    
    visited = set()
    finish_order = []
    
    # 第一次 DFS，记录完成顺序
    def dfs1(v: T):
        visited.add(v)
        for neighbor in graph.get_neighbors(v):
            if neighbor not in visited:
                dfs1(neighbor)
        finish_order.append(v)
    
    for v in graph.vertices:
        if v not in visited:
            dfs1(v)
    
    # 构建反向图
    reversed_graph = Graph(GraphType.DIRECTED)
    for edge in graph.edges:
        reversed_graph.add_edge(edge.target, edge.source, edge.weight)
    
    # 第二次 DFS，按逆序处理
    visited.clear()
    components = []
    
    for v in reversed(finish_order):
        if v not in visited:
            component = set()
            
            def dfs2(vertex: T):
                visited.add(vertex)
                component.add(vertex)
                for neighbor in reversed_graph.get_neighbors(vertex):
                    if neighbor not in visited:
                        dfs2(neighbor)
            
            dfs2(v)
            components.append(component)
    
    return ComponentResult(
        components=components,
        count=len(components),
        is_connected=len(components) == 1
    )


# ==================== 环检测 ====================

def has_cycle(graph: Graph[T]) -> bool:
    """
    检测图中是否存在环
    
    Args:
        graph: 图对象
    
    Returns:
        是否存在环
    """
    if graph.is_directed:
        return _has_cycle_directed(graph)
    return _has_cycle_undirected(graph)


def _has_cycle_directed(graph: Graph[T]) -> bool:
    """有向图环检测"""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {v: WHITE for v in graph.vertices}
    
    def dfs(v: T) -> bool:
        color[v] = GRAY
        for neighbor in graph.get_neighbors(v):
            if color[neighbor] == GRAY:
                return True
            if color[neighbor] == WHITE and dfs(neighbor):
                return True
        color[v] = BLACK
        return False
    
    for v in graph.vertices:
        if color[v] == WHITE:
            if dfs(v):
                return True
    return False


def _has_cycle_undirected(graph: Graph[T]) -> bool:
    """无向图环检测"""
    visited = set()
    
    def dfs(v: T, parent: Optional[T]) -> bool:
        visited.add(v)
        for neighbor in graph.get_neighbors(v):
            if neighbor not in visited:
                if dfs(neighbor, v):
                    return True
            elif neighbor != parent:
                return True
        return False
    
    for v in graph.vertices:
        if v not in visited:
            if dfs(v, None):
                return True
    return False


def find_cycle(graph: Graph[T]) -> Optional[List[T]]:
    """
    查找图中的一个环
    
    Args:
        graph: 图对象
    
    Returns:
        环路径，不存在则返回 None
    """
    if graph.is_directed:
        return _find_cycle_directed(graph)
    return _find_cycle_undirected(graph)


def _find_cycle_directed(graph: Graph[T]) -> Optional[List[T]]:
    """有向图查找环"""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {v: WHITE for v in graph.vertices}
    parent = {v: None for v in graph.vertices}
    cycle_start = None
    cycle_end = None
    
    def dfs(v: T) -> bool:
        nonlocal cycle_start, cycle_end
        color[v] = GRAY
        
        for neighbor in graph.get_neighbors(v):
            if color[neighbor] == GRAY:
                cycle_start = neighbor
                cycle_end = v
                return True
            if color[neighbor] == WHITE:
                parent[neighbor] = v
                if dfs(neighbor):
                    return True
        
        color[v] = BLACK
        return False
    
    for v in graph.vertices:
        if color[v] == WHITE:
            if dfs(v):
                # 重构环路径
                cycle = [cycle_start]
                current = cycle_end
                while current != cycle_start:
                    cycle.append(current)
                    current = parent[current]
                cycle.append(cycle_start)
                cycle.reverse()
                return cycle
    
    return None


def _find_cycle_undirected(graph: Graph[T]) -> Optional[List[T]]:
    """无向图查找环"""
    visited = set()
    parent = {v: None for v in graph.vertices}
    cycle_end = None
    cycle_start = None
    
    def dfs(v: T, p: Optional[T]) -> bool:
        nonlocal cycle_start, cycle_end
        visited.add(v)
        
        for neighbor in graph.get_neighbors(v):
            if neighbor not in visited:
                parent[neighbor] = v
                if dfs(neighbor, v):
                    return True
            elif neighbor != p:
                cycle_start = v
                cycle_end = neighbor
                return True
        
        return False
    
    for v in graph.vertices:
        if v not in visited:
            if dfs(v, None):
                # 重构环路径
                cycle = []
                current = cycle_start
                while current != cycle_end:
                    cycle.append(current)
                    current = parent[current]
                cycle.append(cycle_end)
                cycle.append(cycle_start)
                return cycle
    
    return None


# ==================== 二分图检测 ====================

def is_bipartite(graph: Graph[T]) -> Tuple[bool, Optional[Dict[T, int]]]:
    """
    检测是否为二分图
    
    Args:
        graph: 图对象
    
    Returns:
        (是否为二分图, 着色结果)
    """
    if graph.is_directed:
        raise ValueError("二分图检测仅适用于无向图")
    
    color = {}
    
    for start in graph.vertices:
        if start in color:
            continue
        
        queue = deque([start])
        color[start] = 0
        
        while queue:
            v = queue.popleft()
            
            for neighbor in graph.get_neighbors(v):
                if neighbor not in color:
                    color[neighbor] = 1 - color[v]
                    queue.append(neighbor)
                elif color[neighbor] == color[v]:
                    return False, None
    
    return True, color


# ==================== 欧拉路径 ====================

def find_eulerian_path(graph: Graph[T]) -> Optional[List[T]]:
    """
    查找欧拉路径（Hierholzer 算法）
    
    Args:
        graph: 图对象
    
    Returns:
        欧拉路径，不存在则返回 None
    """
    if not has_eulerian_path(graph):
        return None
    
    # 找到起点
    start = None
    if graph.is_directed:
        for v in graph.vertices:
            if graph.get_out_degree(v) - graph.get_in_degree(v) == 1:
                start = v
                break
        if start is None:
            start = next(iter(graph.vertices)) if graph.vertices else None
    else:
        for v in graph.vertices:
            if graph.get_degree(v) % 2 == 1:
                start = v
                break
        if start is None:
            start = next(iter(graph.vertices)) if graph.vertices else None
    
    if start is None:
        return []
    
    # Hierholzer 算法
    graph_copy = graph.copy()
    stack = [start]
    path = []
    
    while stack:
        v = stack[-1]
        neighbors = list(graph_copy.get_neighbors(v).keys())
        
        if neighbors:
            u = neighbors[0]
            graph_copy.remove_edge(v, u)
            stack.append(u)
        else:
            path.append(stack.pop())
    
    path.reverse()
    return path


def has_eulerian_path(graph: Graph[T]) -> bool:
    """
    检测是否存在欧拉路径
    
    Args:
        graph: 图对象
    
    Returns:
        是否存在欧拉路径
    """
    if graph.is_directed:
        return _has_eulerian_path_directed(graph)
    return _has_eulerian_path_undirected(graph)


def _has_eulerian_path_undirected(graph: Graph[T]) -> bool:
    """无向图欧拉路径检测"""
    odd_degree = 0
    for v in graph.vertices:
        if graph.get_degree(v) % 2 == 1:
            odd_degree += 1
    return odd_degree in (0, 2)


def _has_eulerian_path_directed(graph: Graph[T]) -> bool:
    """有向图欧拉路径检测"""
    start_nodes = 0
    end_nodes = 0
    
    for v in graph.vertices:
        diff = graph.get_out_degree(v) - graph.get_in_degree(v)
        if diff > 1 or diff < -1:
            return False
        if diff == 1:
            start_nodes += 1
        elif diff == -1:
            end_nodes += 1
    
    return (start_nodes == 0 and end_nodes == 0) or (start_nodes == 1 and end_nodes == 1)


def has_eulerian_circuit(graph: Graph[T]) -> bool:
    """
    检测是否存在欧拉回路
    
    Args:
        graph: 图对象
    
    Returns:
        是否存在欧拉回路
    """
    if graph.is_directed:
        for v in graph.vertices:
            if graph.get_in_degree(v) != graph.get_out_degree(v):
                return False
        return True
    else:
        for v in graph.vertices:
            if graph.get_degree(v) % 2 != 0:
                return False
        return True


# ==================== 图工具函数 ====================

def is_tree(graph: Graph[T]) -> bool:
    """
    判断无向图是否为树
    
    Args:
        graph: 图对象
    
    Returns:
        是否为树
    """
    if graph.is_directed:
        return False
    
    # 树有 n-1 条边且连通
    if len(graph.vertices) == 0:
        return True
    
    if graph.edge_count != len(graph.vertices) - 1:
        return False
    
    result = connected_components(graph)
    return result.is_connected


def get_shortest_path_tree(
    graph: Graph[T], 
    start: T
) -> Optional[Graph[T]]:
    """
    获取最短路径树（使用 Dijkstra 算法）
    
    Args:
        graph: 图对象
        start: 起点
    
    Returns:
        最短路径树图
    """
    if start not in graph.vertices:
        return None
    
    distances, previous, _ = bellman_ford(graph, start)
    
    tree = Graph(GraphType.DIRECTED if graph.is_directed else GraphType.UNDIRECTED)
    
    for v in graph.vertices:
        if previous[v] is not None:
            weight = graph.get_edge_weight(previous[v], v)
            if weight is not None:
                tree.add_edge(previous[v], v, weight)
        else:
            tree.add_vertex(v)
    
    return tree


def graph_statistics(graph: Graph[T]) -> Dict[str, Any]:
    """
    获取图统计信息
    
    Args:
        graph: 图对象
    
    Returns:
        统计信息字典
    """
    degrees = [graph.get_degree(v) for v in graph.vertices]
    
    stats = {
        "vertex_count": graph.vertex_count,
        "edge_count": graph.edge_count,
        "is_directed": graph.is_directed,
        "is_connected": None,
        "has_cycle": has_cycle(graph),
        "min_degree": min(degrees) if degrees else 0,
        "max_degree": max(degrees) if degrees else 0,
        "avg_degree": sum(degrees) / len(degrees) if degrees else 0,
    }
    
    if not graph.is_directed:
        result = connected_components(graph)
        stats["is_connected"] = result.is_connected
        stats["component_count"] = result.count
        stats["is_bipartite"], _ = is_bipartite(graph)
        stats["is_tree"] = is_tree(graph)
    else:
        scc = strongly_connected_components(graph)
        stats["is_strongly_connected"] = scc.is_connected
        stats["scc_count"] = scc.count
    
    return stats


def reverse_graph(graph: Graph[T]) -> Graph[T]:
    """
    反转图（所有边的方向取反）
    
    Args:
        graph: 图对象
    
    Returns:
        反转后的图
    """
    reversed_graph = Graph(GraphType.DIRECTED)
    for v in graph.vertices:
        reversed_graph.add_vertex(v)
    for edge in graph.edges:
        reversed_graph.add_edge(edge.target, edge.source, edge.weight)
    return reversed_graph


def get_isolated_vertices(graph: Graph[T]) -> Set[T]:
    """
    获取所有孤立顶点（度为0）
    
    Args:
        graph: 图对象
    
    Returns:
        孤立顶点集合
    """
    return {v for v in graph.vertices if graph.get_degree(v) == 0}


def get_articulation_points(graph: Graph[T]) -> Set[T]:
    """
    查找割点（关节点）
    
    Args:
        graph: 图对象
    
    Returns:
        割点集合
    """
    if graph.is_directed:
        raise ValueError("割点检测仅适用于无向图")
    
    if len(graph.vertices) == 0:
        return set()
    
    disc = {}
    low = {}
    visited = set()
    ap = set()
    parent = {}
    time = [0]
    
    def dfs(u):
        children = 0
        visited.add(u)
        disc[u] = low[u] = time[0]
        time[0] += 1
        
        for v in graph.get_neighbors(u):
            if v not in visited:
                children += 1
                parent[v] = u
                dfs(v)
                low[u] = min(low[u], low[v])
                
                # u 是根节点且有两个子节点
                if parent.get(u) is None and children > 1:
                    ap.add(u)
                
                # u 不是根节点且 low[v] >= disc[u]
                if parent.get(u) is not None and low[v] >= disc[u]:
                    ap.add(u)
            elif v != parent.get(u):
                low[u] = min(low[u], disc[v])
    
    for v in graph.vertices:
        if v not in visited:
            dfs(v)
    
    return ap


def get_bridges(graph: Graph[T]) -> List[Edge[T]]:
    """
    查找桥（割边）
    
    Args:
        graph: 图对象
    
    Returns:
        桥列表
    """
    if graph.is_directed:
        raise ValueError("桥检测仅适用于无向图")
    
    if len(graph.vertices) == 0:
        return []
    
    disc = {}
    low = {}
    visited = set()
    parent = {}
    bridges = []
    time = [0]
    
    def dfs(u):
        visited.add(u)
        disc[u] = low[u] = time[0]
        time[0] += 1
        
        for v, weight in graph.get_neighbors(u).items():
            if v not in visited:
                parent[v] = u
                dfs(v)
                low[u] = min(low[u], low[v])
                
                if low[v] > disc[u]:
                    bridges.append(Edge(u, v, weight))
            elif v != parent.get(u):
                low[u] = min(low[u], disc[v])
    
    for v in graph.vertices:
        if v not in visited:
            dfs(v)
    
    return bridges


# ==================== 便捷函数 ====================

def create_graph(
    edges: Optional[List[Tuple[T, T, Weight]]] = None,
    vertices: Optional[List[T]] = None,
    directed: bool = False
) -> Graph[T]:
    """
    快速创建图
    
    Args:
        edges: 边列表 [(u, v, weight), ...]
        vertices: 顶点列表
        directed: 是否为有向图
    
    Returns:
        图对象
    """
    graph_type = GraphType.DIRECTED if directed else GraphType.UNDIRECTED
    graph = Graph(graph_type)
    
    if vertices:
        for v in vertices:
            graph.add_vertex(v)
    
    if edges:
        for edge in edges:
            if len(edge) == 2:
                graph.add_edge(edge[0], edge[1])
            else:
                graph.add_edge(edge[0], edge[1], edge[2])
    
    return graph


def shortest_path(graph: Graph[T], start: T, end: T) -> PathResult[T]:
    """
    快速查找最短路径
    
    Args:
        graph: 图对象
        start: 起点
        end: 终点
    
    Returns:
        路径结果
    """
    return dijkstra(graph, start, end)


def all_shortest_paths(graph: Graph[T]) -> Dict[T, Dict[T, PathResult[T]]]:
    """
    计算所有顶点对之间的最短路径
    
    Args:
        graph: 图对象
    
    Returns:
        所有路径结果
    """
    distances, previous = floyd_warshall(graph)
    vertices = list(graph.vertices)
    
    def build_path(start: T, end: T) -> PathResult[T]:
        if distances[start][end] == float('inf'):
            return PathResult([], float('inf'), False)
        
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous[start].get(current)
        path.reverse()
        
        return PathResult(path, distances[start][end], True)
    
    return {
        u: {v: build_path(u, v) for v in vertices}
        for u in vertices
    }