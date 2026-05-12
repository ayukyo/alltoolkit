"""
图论算法工具模块 (Graph Utilities)

提供常用图论算法的实现，包括：
- 图的创建和操作 (有向图/无向图/带权图)
- 深度优先搜索 (DFS)
- 广度优先搜索 (BFS)
- 最短路径算法 (Dijkstra, Bellman-Ford, Floyd-Warshall)
- 最小生成树 (Kruskal, Prim)
- 拓扑排序
- 连通分量检测
- 环检测
- 二分图检测

零外部依赖，纯 Python 实现。
"""

from typing import Dict, List, Set, Tuple, Optional, Any, Union
from collections import defaultdict, deque
from dataclasses import dataclass, field
import heapq


@dataclass
class Graph:
    """
    图数据结构
    
    支持：
    - 有向图/无向图
    - 带权边/无权边
    - 自环和多重边检测
    """
    directed: bool = False
    weighted: bool = False
    _adj: Dict[Any, Dict[Any, float]] = field(default_factory=lambda: defaultdict(dict))
    _vertices: Set[Any] = field(default_factory=set)
    
    def add_vertex(self, vertex: Any) -> None:
        """添加顶点"""
        self._vertices.add(vertex)
    
    def add_edge(self, u: Any, v: Any, weight: float = 1.0) -> None:
        """
        添加边
        
        Args:
            u: 起始顶点
            v: 终止顶点
            weight: 边的权重（默认为 1.0）
        """
        self._vertices.add(u)
        self._vertices.add(v)
        
        if self.weighted:
            self._adj[u][v] = weight
            if not self.directed:
                self._adj[v][u] = weight
        else:
            self._adj[u][v] = 1
            if not self.directed:
                self._adj[v][u] = 1
    
    def remove_edge(self, u: Any, v: Any) -> bool:
        """移除边，返回是否成功"""
        if u in self._adj and v in self._adj[u]:
            del self._adj[u][v]
            if not self.directed and v in self._adj and u in self._adj[v]:
                del self._adj[v][u]
            return True
        return False
    
    def remove_vertex(self, vertex: Any) -> bool:
        """移除顶点及其所有关联边"""
        if vertex not in self._vertices:
            return False
        
        # 移除所有以该顶点为终点的边
        for u in list(self._adj.keys()):
            if vertex in self._adj[u]:
                del self._adj[u][vertex]
        
        # 移除以该顶点为起点的边
        if vertex in self._adj:
            del self._adj[vertex]
        
        self._vertices.discard(vertex)
        return True
    
    def get_neighbors(self, vertex: Any) -> Dict[Any, float]:
        """获取顶点的所有邻居及边权重"""
        return dict(self._adj.get(vertex, {}))
    
    def get_vertices(self) -> Set[Any]:
        """获取所有顶点"""
        return self._vertices.copy()
    
    def get_edges(self) -> List[Tuple[Any, Any, float]]:
        """获取所有边 (u, v, weight)"""
        edges = []
        visited = set()
        for u in self._adj:
            for v, w in self._adj[u].items():
                if self.directed:
                    edges.append((u, v, w))
                else:
                    edge_key = tuple(sorted([str(u), str(v)]))
                    if edge_key not in visited:
                        edges.append((u, v, w))
                        visited.add(edge_key)
        return edges
    
    def has_edge(self, u: Any, v: Any) -> bool:
        """检查边是否存在"""
        return u in self._adj and v in self._adj[u]
    
    def get_edge_weight(self, u: Any, v: Any) -> Optional[float]:
        """获取边的权重"""
        if self.has_edge(u, v):
            return self._adj[u][v]
        return None
    
    def get_vertex_count(self) -> int:
        """获取顶点数量"""
        return len(self._vertices)
    
    def get_edge_count(self) -> int:
        """获取边数量"""
        count = sum(len(neighbors) for neighbors in self._adj.values())
        if not self.directed:
            count //= 2
        return count
    
    def get_degree(self, vertex: Any) -> int:
        """获取顶点的度"""
        return len(self._adj.get(vertex, {}))
    
    def __str__(self) -> str:
        graph_type = "有向" if self.directed else "无向"
        weight_type = "带权" if self.weighted else "无权"
        return f"{weight_type}{graph_type}图(顶点:{self.get_vertex_count()}, 边:{self.get_edge_count()})"
    
    def __repr__(self) -> str:
        return self.__str__()


# ==================== 遍历算法 ====================

def dfs(graph: Graph, start: Any, visited: Optional[Set] = None) -> List[Any]:
    """
    深度优先搜索 (DFS)
    
    Args:
        graph: 图对象
        start: 起始顶点
        visited: 已访问集合（用于递归）
    
    Returns:
        DFS 遍历序列
    """
    if visited is None:
        visited = set()
    
    result = []
    
    def _dfs(vertex: Any):
        if vertex in visited:
            return
        visited.add(vertex)
        result.append(vertex)
        
        for neighbor in graph.get_neighbors(vertex):
            if neighbor not in visited:
                _dfs(neighbor)
    
    _dfs(start)
    return result


def dfs_iterative(graph: Graph, start: Any) -> List[Any]:
    """
    深度优先搜索（迭代版本）
    
    使用栈实现，避免递归深度限制。
    """
    visited = set()
    result = []
    stack = [start]
    
    while stack:
        vertex = stack.pop()
        if vertex in visited:
            continue
        
        visited.add(vertex)
        result.append(vertex)
        
        # 逆序添加邻居以保持与递归版本相同的顺序
        neighbors = list(graph.get_neighbors(vertex).keys())
        for neighbor in reversed(neighbors):
            if neighbor not in visited:
                stack.append(neighbor)
    
    return result


def bfs(graph: Graph, start: Any) -> List[Any]:
    """
    广度优先搜索 (BFS)
    
    Args:
        graph: 图对象
        start: 起始顶点
    
    Returns:
        BFS 遍历序列
    """
    visited = {start}
    result = [start]
    queue = deque([start])
    
    while queue:
        vertex = queue.popleft()
        
        for neighbor in graph.get_neighbors(vertex):
            if neighbor not in visited:
                visited.add(neighbor)
                result.append(neighbor)
                queue.append(neighbor)
    
    return result


def bfs_with_distance(graph: Graph, start: Any) -> Tuple[List[Any], Dict[Any, int]]:
    """
    广度优先搜索，同时计算距离
    
    Returns:
        (BFS 序列, 顶点到起点的距离字典)
    """
    visited = {start}
    result = [start]
    distance = {start: 0}
    queue = deque([start])
    
    while queue:
        vertex = queue.popleft()
        
        for neighbor in graph.get_neighbors(vertex):
            if neighbor not in visited:
                visited.add(neighbor)
                result.append(neighbor)
                distance[neighbor] = distance[vertex] + 1
                queue.append(neighbor)
    
    return result, distance


# ==================== 最短路径算法 ====================

def dijkstra(graph: Graph, start: Any, end: Any = None) -> Tuple[Dict[Any, float], Dict[Any, Optional[Any]]]:
    """
    Dijkstra 最短路径算法
    
    适用于非负权重图。
    
    Args:
        graph: 图对象
        start: 起点
        end: 终点（可选，如果指定则提前终止）
    
    Returns:
        (距离字典, 前驱字典)
    
    Raises:
        ValueError: 如果图包含负权边
    """
    # 检查负权边
    for u, v, w in graph.get_edges():
        if w < 0:
            raise ValueError("Dijkstra 算法不支持负权边")
    
    distance = {v: float('inf') for v in graph.get_vertices()}
    distance[start] = 0
    predecessor = {v: None for v in graph.get_vertices()}
    visited = set()
    
    # 优先队列: (distance, vertex)
    pq = [(0, start)]
    
    while pq:
        dist, vertex = heapq.heappop(pq)
        
        if vertex in visited:
            continue
        
        visited.add(vertex)
        
        # 如果到达终点，提前终止
        if end is not None and vertex == end:
            break
        
        for neighbor, weight in graph.get_neighbors(vertex).items():
            if neighbor in visited:
                continue
            
            new_dist = dist + weight
            if new_dist < distance[neighbor]:
                distance[neighbor] = new_dist
                predecessor[neighbor] = vertex
                heapq.heappush(pq, (new_dist, neighbor))
    
    return distance, predecessor


def get_shortest_path(graph: Graph, start: Any, end: Any, algorithm: str = 'dijkstra') -> Optional[List[Any]]:
    """
    获取两点间的最短路径
    
    Args:
        graph: 图对象
        start: 起点
        end: 终点
        algorithm: 算法选择 ('dijkstra', 'bfs')
    
    Returns:
        路径列表，如果不存在则返回 None
    """
    if algorithm == 'bfs' or not graph.weighted:
        # 无权图使用 BFS
        _, predecessor = bfs_path(graph, start)
    else:
        _, predecessor = dijkstra(graph, start, end)
    
    if predecessor.get(end) is None and start != end:
        return None
    
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = predecessor.get(current)
    
    path.reverse()
    return path if path and path[0] == start else None


def bfs_path(graph: Graph, start: Any) -> Tuple[Dict[Any, int], Dict[Any, Optional[Any]]]:
    """
    BFS 求无权图最短路径
    
    Returns:
        (距离字典, 前驱字典)
    """
    distance = {v: float('inf') for v in graph.get_vertices()}
    distance[start] = 0
    predecessor = {v: None for v in graph.get_vertices()}
    visited = {start}
    queue = deque([start])
    
    while queue:
        vertex = queue.popleft()
        
        for neighbor in graph.get_neighbors(vertex):
            if neighbor not in visited:
                visited.add(neighbor)
                distance[neighbor] = distance[vertex] + 1
                predecessor[neighbor] = vertex
                queue.append(neighbor)
    
    return distance, predecessor


def bellman_ford(graph: Graph, start: Any) -> Tuple[Dict[Any, float], Dict[Any, Optional[Any]], bool]:
    """
    Bellman-Ford 最短路径算法
    
    支持负权边，可检测负环。
    
    Args:
        graph: 图对象
        start: 起点
    
    Returns:
        (距离字典, 前驱字典, 是否存在负环)
    """
    distance = {v: float('inf') for v in graph.get_vertices()}
    distance[start] = 0
    predecessor = {v: None for v in graph.get_vertices()}
    
    edges = graph.get_edges()
    vertices = graph.get_vertices()
    
    # 松弛 V-1 次
    for _ in range(len(vertices) - 1):
        updated = False
        for u, v, w in edges:
            if distance[u] != float('inf') and distance[u] + w < distance[v]:
                distance[v] = distance[u] + w
                predecessor[v] = u
                updated = True
        if not updated:
            break
    
    # 检测负环
    has_negative_cycle = False
    for u, v, w in edges:
        if distance[u] != float('inf') and distance[u] + w < distance[v]:
            has_negative_cycle = True
            break
    
    return distance, predecessor, has_negative_cycle


def floyd_warshall(graph: Graph) -> Dict[Any, Dict[Any, float]]:
    """
    Floyd-Warshall 全源最短路径算法
    
    返回所有顶点对之间的最短距离矩阵。
    时间复杂度: O(V^3)
    """
    vertices = list(graph.get_vertices())
    n = len(vertices)
    vertex_to_idx = {v: i for i, v in enumerate(vertices)}
    
    # 初始化距离矩阵
    dist = {v: {u: float('inf') for u in vertices} for v in vertices}
    for v in vertices:
        dist[v][v] = 0
    
    # 填入边权重
    for u, v, w in graph.get_edges():
        dist[u][v] = w
        if not graph.directed:
            dist[v][u] = w
    
    # Floyd-Warshall 主循环
    for k in vertices:
        for i in vertices:
            for j in vertices:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    return dist


# ==================== 最小生成树算法 ====================

def kruskal(graph: Graph) -> Tuple[List[Tuple[Any, Any, float]], float]:
    """
    Kruskal 最小生成树算法
    
    使用并查集实现。
    
    Args:
        graph: 无向图对象
    
    Returns:
        (边列表, 总权重)
    
    Raises:
        ValueError: 如果图是有向图
    """
    if graph.directed:
        raise ValueError("最小生成树算法仅适用于无向图")
    
    vertices = graph.get_vertices()
    edges = sorted(graph.get_edges(), key=lambda e: e[2])
    
    # 并查集
    parent = {v: v for v in vertices}
    rank = {v: 0 for v in vertices}
    
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
    
    mst_edges = []
    total_weight = 0.0
    
    for u, v, w in edges:
        if find(u) != find(v):
            union(u, v)
            mst_edges.append((u, v, w))
            total_weight += w
    
    return mst_edges, total_weight


def prim(graph: Graph, start: Any = None) -> Tuple[List[Tuple[Any, Any, float]], float]:
    """
    Prim 最小生成树算法
    
    Args:
        graph: 无向图对象
        start: 起始顶点（可选）
    
    Returns:
        (边列表, 总权重)
    
    Raises:
        ValueError: 如果图是有向图
    """
    if graph.directed:
        raise ValueError("最小生成树算法仅适用于无向图")
    
    vertices = graph.get_vertices()
    if not vertices:
        return [], 0.0
    
    if start is None:
        start = next(iter(vertices))
    
    visited = set()
    mst_edges = []
    total_weight = 0.0
    
    # 优先队列: (weight, u, v)
    pq = [(0, start, start)]
    
    while pq and len(visited) < len(vertices):
        weight, u, v = heapq.heappop(pq)
        
        if v in visited:
            continue
        
        visited.add(v)
        
        if u != v:
            mst_edges.append((u, v, weight))
            total_weight += weight
        
        for neighbor, w in graph.get_neighbors(v).items():
            if neighbor not in visited:
                heapq.heappush(pq, (w, v, neighbor))
    
    return mst_edges, total_weight


# ==================== 拓扑排序 ====================

def topological_sort(graph: Graph) -> Optional[List[Any]]:
    """
    拓扑排序（Kahn 算法）
    
    Args:
        graph: 有向无环图
    
    Returns:
        拓扑序列，如果存在环则返回 None
    
    Raises:
        ValueError: 如果图是无向图
    """
    if not graph.directed:
        raise ValueError("拓扑排序仅适用于有向图")
    
    # 计算入度
    in_degree = {v: 0 for v in graph.get_vertices()}
    for u, v, _ in graph.get_edges():
        in_degree[v] = in_degree.get(v, 0) + 1
    
    # 入度为 0 的顶点入队
    queue = deque([v for v, d in in_degree.items() if d == 0])
    result = []
    
    while queue:
        vertex = queue.popleft()
        result.append(vertex)
        
        for neighbor in graph.get_neighbors(vertex):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # 检查是否所有顶点都被访问
    if len(result) != len(graph.get_vertices()):
        return None  # 存在环
    
    return result


def topological_sort_dfs(graph: Graph) -> Optional[List[Any]]:
    """
    拓扑排序（DFS 版本）
    
    Returns:
        拓扑序列（逆后序），如果存在环则返回 None
    """
    if not graph.directed:
        raise ValueError("拓扑排序仅适用于有向图")
    
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {v: WHITE for v in graph.get_vertices()}
    result = []
    has_cycle = False
    
    def dfs(vertex):
        nonlocal has_cycle
        if has_cycle:
            return
        
        color[vertex] = GRAY
        
        for neighbor in graph.get_neighbors(vertex):
            if color[neighbor] == GRAY:
                has_cycle = True  # 检测到环
                return
            elif color[neighbor] == WHITE:
                dfs(neighbor)
        
        color[vertex] = BLACK
        result.append(vertex)
    
    for vertex in graph.get_vertices():
        if color[vertex] == WHITE:
            dfs(vertex)
    
    if has_cycle:
        return None
    
    result.reverse()
    return result


# ==================== 连通性算法 ====================

def is_connected(graph: Graph) -> bool:
    """
    检查图是否连通
    
    对于有向图，检查是否强连通。
    对于无向图，检查是否连通。
    """
    vertices = graph.get_vertices()
    if not vertices:
        return True
    
    if graph.directed:
        # 有向图：检查强连通性
        start = next(iter(vertices))
        # 从 start 能到达所有顶点
        visited = set(dfs(graph, start))
        if visited != vertices:
            return False
        
        # 反转图，再从 start 能到达所有顶点
        reversed_graph = Graph(directed=True, weighted=graph.weighted)
        for v in vertices:
            reversed_graph.add_vertex(v)
        for u, v, w in graph.get_edges():
            reversed_graph.add_edge(v, u, w)
        
        visited = set(dfs(reversed_graph, start))
        return visited == vertices
    else:
        # 无向图：一次 DFS 能访问所有顶点
        start = next(iter(vertices))
        visited = set(dfs(graph, start))
        return visited == vertices


def find_connected_components(graph: Graph) -> List[Set[Any]]:
    """
    查找连通分量
    
    Returns:
        连通分量列表，每个分量是一个顶点集合
    """
    if graph.directed:
        return find_strongly_connected_components(graph)
    
    visited = set()
    components = []
    
    for vertex in graph.get_vertices():
        if vertex not in visited:
            component = set(dfs(graph, vertex))
            components.append(component)
            visited.update(component)
    
    return components


def find_strongly_connected_components(graph: Graph) -> List[Set[Any]]:
    """
    查找强连通分量（Kosaraju 算法）
    
    Args:
        graph: 有向图
    
    Returns:
        强连通分量列表
    """
    if not graph.directed:
        raise ValueError("强连通分量算法仅适用于有向图")
    
    vertices = graph.get_vertices()
    
    # 第一步：在原图上进行 DFS，记录完成时间
    visited = set()
    finish_order = []
    
    def dfs1(v):
        visited.add(v)
        for neighbor in graph.get_neighbors(v):
            if neighbor not in visited:
                dfs1(neighbor)
        finish_order.append(v)
    
    for v in vertices:
        if v not in visited:
            dfs1(v)
    
    # 第二步：构建反转图
    reversed_graph = Graph(directed=True, weighted=graph.weighted)
    for v in vertices:
        reversed_graph.add_vertex(v)
    for u, v, w in graph.get_edges():
        reversed_graph.add_edge(v, u, w)
    
    # 第三步：在反转图上按完成时间的逆序进行 DFS
    visited = set()
    components = []
    
    def dfs2(v, component):
        visited.add(v)
        component.add(v)
        for neighbor in reversed_graph.get_neighbors(v):
            if neighbor not in visited:
                dfs2(neighbor, component)
    
    for v in reversed(finish_order):
        if v not in visited:
            component = set()
            dfs2(v, component)
            components.append(component)
    
    return components


# ==================== 环检测 ====================

def has_cycle(graph: Graph) -> bool:
    """
    检测图中是否存在环
    """
    if graph.directed:
        return has_cycle_directed(graph)
    else:
        return has_cycle_undirected(graph)


def has_cycle_directed(graph: Graph) -> bool:
    """
    检测有向图中是否存在环
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {v: WHITE for v in graph.get_vertices()}
    
    def dfs(v):
        color[v] = GRAY
        for neighbor in graph.get_neighbors(v):
            if color[neighbor] == GRAY:
                return True  # 检测到环
            if color[neighbor] == WHITE:
                if dfs(neighbor):
                    return True
        color[v] = BLACK
        return False
    
    for v in graph.get_vertices():
        if color[v] == WHITE:
            if dfs(v):
                return True
    
    return False


def has_cycle_undirected(graph: Graph) -> bool:
    """
    检测无向图中是否存在环
    """
    visited = set()
    
    def dfs(v, parent):
        visited.add(v)
        for neighbor in graph.get_neighbors(v):
            if neighbor not in visited:
                if dfs(neighbor, v):
                    return True
            elif neighbor != parent:
                return True  # 检测到环
        return False
    
    for v in graph.get_vertices():
        if v not in visited:
            if dfs(v, None):
                return True
    
    return False


def find_cycle(graph: Graph) -> Optional[List[Any]]:
    """
    查找图中的一个环
    
    Returns:
        环路径，如果不存在则返回 None
    """
    if graph.directed:
        return find_cycle_directed(graph)
    else:
        return find_cycle_undirected(graph)


def find_cycle_directed(graph: Graph) -> Optional[List[Any]]:
    """查找有向图中的环"""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {v: WHITE for v in graph.get_vertices()}
    parent = {v: None for v in graph.get_vertices()}
    cycle_end = None
    
    def dfs(v):
        nonlocal cycle_end
        color[v] = GRAY
        for neighbor in graph.get_neighbors(v):
            if color[neighbor] == GRAY:
                cycle_end = (v, neighbor)
                return True
            if color[neighbor] == WHITE:
                parent[neighbor] = v
                if dfs(neighbor):
                    return True
        color[v] = BLACK
        return False
    
    for v in graph.get_vertices():
        if color[v] == WHITE:
            if dfs(v):
                # 重建环
                cycle = [cycle_end[1]]
                current = cycle_end[0]
                while current != cycle_end[1]:
                    cycle.append(current)
                    current = parent[current]
                cycle.append(cycle_end[1])
                cycle.reverse()
                return cycle
    
    return None


def find_cycle_undirected(graph: Graph) -> Optional[List[Any]]:
    """查找无向图中的环"""
    visited = set()
    parent = {}
    
    def dfs(v, p):
        visited.add(v)
        parent[v] = p
        for neighbor in graph.get_neighbors(v):
            if neighbor not in visited:
                if dfs(neighbor, v):
                    return True
            elif neighbor != p:
                # 找到环，重建路径
                cycle = [neighbor, v]
                current = p
                while current != neighbor:
                    cycle.append(current)
                    current = parent[current]
                cycle.append(neighbor)
                return True
        return False
    
    for v in graph.get_vertices():
        if v not in visited:
            if dfs(v, None):
                return None  # 简化处理
    
    return None


# ==================== 二分图检测 ====================

def is_bipartite(graph: Graph) -> bool:
    """
    检测图是否为二分图
    
    使用 BFS 染色算法。
    """
    if graph.directed:
        raise ValueError("二分图检测仅适用于无向图")
    
    color = {}  # 0 或 1
    
    for start in graph.get_vertices():
        if start in color:
            continue
        
        color[start] = 0
        queue = deque([start])
        
        while queue:
            vertex = queue.popleft()
            
            for neighbor in graph.get_neighbors(vertex):
                if neighbor not in color:
                    color[neighbor] = 1 - color[vertex]
                    queue.append(neighbor)
                elif color[neighbor] == color[vertex]:
                    return False
    
    return True


def get_bipartition(graph: Graph) -> Optional[Tuple[Set[Any], Set[Any]]]:
    """
    获取二分图的划分
    
    Returns:
        (集合A, 集合B)，如果不是二分图则返回 None
    """
    if graph.directed:
        raise ValueError("二分图检测仅适用于无向图")
    
    color = {}
    
    for start in graph.get_vertices():
        if start in color:
            continue
        
        color[start] = 0
        queue = deque([start])
        
        while queue:
            vertex = queue.popleft()
            
            for neighbor in graph.get_neighbors(vertex):
                if neighbor not in color:
                    color[neighbor] = 1 - color[vertex]
                    queue.append(neighbor)
                elif color[neighbor] == color[vertex]:
                    return None
    
    set_a = {v for v, c in color.items() if c == 0}
    set_b = {v for v, c in color.items() if c == 1}
    
    return set_a, set_b


# ==================== 其他实用函数 ====================

def get_degree_sequence(graph: Graph) -> List[int]:
    """
    获取度序列（降序排列）
    """
    degrees = [graph.get_degree(v) for v in graph.get_vertices()]
    degrees.sort(reverse=True)
    return degrees


def get_eccentricity(graph: Graph, vertex: Any) -> int:
    """
    计算顶点的离心率
    
    定义：顶点到图中其他顶点的最短距离的最大值。
    """
    if graph.weighted:
        distances, _ = dijkstra(graph, vertex)
    else:
        distances, _ = bfs_path(graph, vertex)
    
    max_dist = max((d for d in distances.values() if d != float('inf')), default=0)
    return int(max_dist)


def get_diameter(graph: Graph) -> int:
    """
    计算图的直径
    
    定义：任意两顶点间最短距离的最大值。
    """
    if graph.weighted:
        distances = floyd_warshall(graph)
        max_dist = 0
        for u in distances:
            for v in distances[u]:
                if distances[u][v] != float('inf') and distances[u][v] > max_dist:
                    max_dist = distances[u][v]
        return int(max_dist)
    else:
        max_eccentricity = 0
        for v in graph.get_vertices():
            ecc = get_eccentricity(graph, v)
            max_eccentricity = max(max_eccentricity, ecc)
        return max_eccentricity


def get_radius(graph: Graph) -> int:
    """
    计算图的半径
    
    定义：所有顶点离心率的最小值。
    """
    min_eccentricity = float('inf')
    for v in graph.get_vertices():
        ecc = get_eccentricity(graph, v)
        min_eccentricity = min(min_eccentricity, ecc)
    return int(min_eccentricity)


def get_center(graph: Graph) -> Set[Any]:
    """
    获取图的中心
    
    定义：离心率等于半径的顶点集合。
    """
    radius = get_radius(graph)
    center = set()
    for v in graph.get_vertices():
        if get_eccentricity(graph, v) == radius:
            center.add(v)
    return center


def to_adjacency_matrix(graph: Graph) -> Tuple[List[List[float]], List[Any]]:
    """
    转换为邻接矩阵表示
    
    Returns:
        (邻接矩阵, 顶点列表)
    """
    vertices = sorted(graph.get_vertices(), key=str)
    n = len(vertices)
    vertex_to_idx = {v: i for i, v in enumerate(vertices)}
    
    # 初始化矩阵
    matrix = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 0
    
    # 填入边
    for u, v, w in graph.get_edges():
        i, j = vertex_to_idx[u], vertex_to_idx[v]
        matrix[i][j] = w
        if not graph.directed:
            matrix[j][i] = w
    
    return matrix, vertices


def from_adjacency_matrix(matrix: List[List[float]], vertices: List[Any], 
                          directed: bool = False, threshold: float = 0) -> Graph:
    """
    从邻接矩阵创建图
    
    Args:
        matrix: 邻接矩阵
        vertices: 顶点列表
        directed: 是否为有向图
        threshold: 权重阈值，小于此值的边将被忽略
    
    Returns:
        图对象
    """
    n = len(matrix)
    weighted = any(matrix[i][j] != 1 and matrix[i][j] != float('inf') 
                   for i in range(n) for j in range(n) if i != j)
    
    graph = Graph(directed=directed, weighted=weighted)
    
    for v in vertices:
        graph.add_vertex(v)
    
    for i in range(n):
        for j in range(n):
            if i != j and matrix[i][j] != float('inf') and matrix[i][j] >= threshold:
                graph.add_edge(vertices[i], vertices[j], matrix[i][j])
    
    return graph


def copy_graph(graph: Graph) -> Graph:
    """创建图的深拷贝"""
    new_graph = Graph(directed=graph.directed, weighted=graph.weighted)
    
    for v in graph.get_vertices():
        new_graph.add_vertex(v)
    
    for u, v, w in graph.get_edges():
        new_graph.add_edge(u, v, w)
    
    return new_graph


# ==================== 工厂函数 ====================

def create_empty_graph(directed: bool = False, weighted: bool = False) -> Graph:
    """创建空图"""
    return Graph(directed=directed, weighted=weighted)


def create_complete_graph(n: int, directed: bool = False, weighted: bool = False) -> Graph:
    """
    创建完全图
    
    Args:
        n: 顶点数量
        directed: 是否为有向图
        weighted: 是否带权
    """
    graph = Graph(directed=directed, weighted=weighted)
    
    for i in range(n):
        graph.add_vertex(i)
    
    for i in range(n):
        for j in range(n):
            if i != j:
                if directed or i < j:
                    weight = 1.0 if not weighted else float(i * n + j)
                    graph.add_edge(i, j, weight)
    
    return graph


def create_path_graph(n: int, directed: bool = False, weighted: bool = False) -> Graph:
    """创建路径图 P_n"""
    graph = Graph(directed=directed, weighted=weighted)
    
    for i in range(n):
        graph.add_vertex(i)
    
    for i in range(n - 1):
        graph.add_edge(i, i + 1, 1.0 if not weighted else float(i + 1))
    
    return graph


def create_cycle_graph(n: int, directed: bool = False, weighted: bool = False) -> Graph:
    """创建环图 C_n"""
    graph = Graph(directed=directed, weighted=weighted)
    
    for i in range(n):
        graph.add_vertex(i)
    
    for i in range(n):
        weight = 1.0 if not weighted else float(i + 1)
        graph.add_edge(i, (i + 1) % n, weight)
    
    return graph


def create_star_graph(n: int, directed: bool = False, weighted: bool = False) -> Graph:
    """创建星图 S_n（n 个叶子节点）"""
    graph = Graph(directed=directed, weighted=weighted)
    
    # 中心节点为 0，叶子节点为 1 到 n
    for i in range(n + 1):
        graph.add_vertex(i)
    
    for i in range(1, n + 1):
        weight = 1.0 if not weighted else float(i)
        graph.add_edge(0, i, weight)
    
    return graph