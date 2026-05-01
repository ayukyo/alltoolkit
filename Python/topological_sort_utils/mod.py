"""
Topological Sort Utils - 拓扑排序工具

提供图的拓扑排序功能，用于任务调度、依赖解析、构建系统等场景。

功能特性：
- Kahn 算法（BFS 风格）
- DFS 风格拓扑排序
- 检测环
- 并行层排序（可并行执行的任务分组）
- 最长路径计算（关键路径）
- 支持带权节点

零外部依赖，纯 Python 实现。
"""

from collections import deque
from typing import Dict, List, Set, Optional, Tuple, Any, Callable


class TopologicalSortError(Exception):
    """拓扑排序相关错误的基类"""
    pass


class CycleDetectedError(TopologicalSortError):
    """图中存在环时抛出"""
    pass


class Graph:
    """
    有向图数据结构
    
    支持的操作：
    - 添加节点和边
    - 拓扑排序
    - 检测环
    - 获取入度/出度
    - 并行层划分
    """
    
    def __init__(self):
        """初始化空图"""
        self._nodes: Set[str] = set()
        self._edges: Dict[str, Set[str]] = {}  # node -> set of neighbors
        self._reverse_edges: Dict[str, Set[str]] = {}  # node -> set of predecessors
        self._node_weights: Dict[str, Any] = {}  # node -> weight/data
    
    def add_node(self, node: str, weight: Any = None) -> 'Graph':
        """
        添加节点
        
        Args:
            node: 节点标识符
            weight: 节点权重或关联数据
            
        Returns:
            self，支持链式调用
        """
        self._nodes.add(node)
        if node not in self._edges:
            self._edges[node] = set()
        if node not in self._reverse_edges:
            self._reverse_edges[node] = set()
        if weight is not None:
            self._node_weights[node] = weight
        return self
    
    def add_edge(self, from_node: str, to_node: str) -> 'Graph':
        """
        添加有向边
        
        Args:
            from_node: 起点
            to_node: 终点
            
        Returns:
            self，支持链式调用
        """
        # 自动添加节点
        self.add_node(from_node)
        self.add_node(to_node)
        
        self._edges[from_node].add(to_node)
        self._reverse_edges[to_node].add(from_node)
        return self
    
    def add_edges(self, edges: List[Tuple[str, str]]) -> 'Graph':
        """
        批量添加边
        
        Args:
            edges: 边列表，每条边为 (from, to) 元组
            
        Returns:
            self，支持链式调用
        """
        for from_node, to_node in edges:
            self.add_edge(from_node, to_node)
        return self
    
    def remove_edge(self, from_node: str, to_node: str) -> 'Graph':
        """
        移除边
        
        Args:
            from_node: 起点
            to_node: 终点
            
        Returns:
            self，支持链式调用
        """
        if from_node in self._edges:
            self._edges[from_node].discard(to_node)
        if to_node in self._reverse_edges:
            self._reverse_edges[to_node].discard(from_node)
        return self
    
    def remove_node(self, node: str) -> 'Graph':
        """
        移除节点及其所有边
        
        Args:
            node: 要移除的节点
            
        Returns:
            self，支持链式调用
        """
        if node not in self._nodes:
            return self
        
        # 移除所有出边
        for neighbor in list(self._edges.get(node, set())):
            self._reverse_edges[neighbor].discard(node)
        
        # 移除所有入边
        for predecessor in list(self._reverse_edges.get(node, set())):
            self._edges[predecessor].discard(node)
        
        # 移除节点
        self._nodes.discard(node)
        self._edges.pop(node, None)
        self._reverse_edges.pop(node, None)
        self._node_weights.pop(node, None)
        
        return self
    
    def has_node(self, node: str) -> bool:
        """检查节点是否存在"""
        return node in self._nodes
    
    def has_edge(self, from_node: str, to_node: str) -> bool:
        """检查边是否存在"""
        return from_node in self._edges and to_node in self._edges[from_node]
    
    def get_nodes(self) -> Set[str]:
        """获取所有节点"""
        return self._nodes.copy()
    
    def get_edges(self) -> List[Tuple[str, str]]:
        """获取所有边"""
        edges = []
        for from_node, neighbors in self._edges.items():
            for to_node in neighbors:
                edges.append((from_node, to_node))
        return edges
    
    def get_neighbors(self, node: str) -> Set[str]:
        """获取节点的所有邻居（出边目标）"""
        return self._edges.get(node, set()).copy()
    
    def get_predecessors(self, node: str) -> Set[str]:
        """获取节点的所有前驱（入边来源）"""
        return self._reverse_edges.get(node, set()).copy()
    
    def in_degree(self, node: str) -> int:
        """获取节点的入度"""
        return len(self._reverse_edges.get(node, set()))
    
    def out_degree(self, node: str) -> int:
        """获取节点的出度"""
        return len(self._edges.get(node, set()))
    
    def get_node_weight(self, node: str, default: Any = None) -> Any:
        """获取节点权重/数据"""
        return self._node_weights.get(node, default)
    
    def set_node_weight(self, node: str, weight: Any) -> 'Graph':
        """设置节点权重/数据"""
        if node in self._nodes:
            self._node_weights[node] = weight
        return self
    
    @property
    def node_count(self) -> int:
        """节点数量"""
        return len(self._nodes)
    
    @property
    def edge_count(self) -> int:
        """边数量"""
        return sum(len(neighbors) for neighbors in self._edges.values())
    
    def copy(self) -> 'Graph':
        """创建图的深拷贝"""
        new_graph = Graph()
        for node in self._nodes:
            new_graph.add_node(node, self._node_weights.get(node))
        for from_node, neighbors in self._edges.items():
            for to_node in neighbors:
                new_graph.add_edge(from_node, to_node)
        return new_graph


class TopologicalSorter:
    """
    拓扑排序器
    
    提供多种拓扑排序算法和图分析功能。
    """
    
    def __init__(self, graph: Optional[Graph] = None):
        """
        初始化排序器
        
        Args:
            graph: 可选的图对象
        """
        self._graph = graph or Graph()
    
    @property
    def graph(self) -> Graph:
        """获取关联的图"""
        return self._graph
    
    def kahn_sort(self) -> List[str]:
        """
        Kahn 算法拓扑排序（BFS 风格）
        
        特点：
        - 时间复杂度 O(V + E)
        - 空间复杂度 O(V)
        - 当存在环时抛出异常
        
        Returns:
            拓扑排序结果列表
            
        Raises:
            CycleDetectedError: 图中存在环
        """
        graph = self._graph
        in_degree = {node: graph.in_degree(node) for node in graph.get_nodes()}
        
        # 将所有入度为 0 的节点加入队列
        queue = deque([node for node, degree in in_degree.items() if degree == 0])
        result = []
        
        while queue:
            node = queue.popleft()
            result.append(node)
            
            # 减少邻居的入度
            for neighbor in graph.get_neighbors(node):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        if len(result) != graph.node_count:
            raise CycleDetectedError("图中存在环，无法进行拓扑排序")
        
        return result
    
    def dfs_sort(self) -> List[str]:
        """
        DFS 风格拓扑排序
        
        特点：
        - 时间复杂度 O(V + E)
        - 使用递归实现
        - 当存在环时抛出异常
        
        Returns:
            拓扑排序结果列表
            
        Raises:
            CycleDetectedError: 图中存在环
        """
        graph = self._graph
        visited = set()
        rec_stack = set()  # 用于检测环
        result = []
        
        def dfs(node: str):
            if node in rec_stack:
                raise CycleDetectedError("图中存在环，无法进行拓扑排序")
            
            if node in visited:
                return
            
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get_neighbors(node):
                dfs(neighbor)
            
            rec_stack.remove(node)
            result.append(node)
        
        for node in graph.get_nodes():
            if node not in visited:
                dfs(node)
        
        return result[::-1]  # 反转结果
    
    def has_cycle(self) -> bool:
        """
        检测图中是否有环
        
        Returns:
            True 如果存在环，否则 False
        """
        graph = self._graph
        visited = set()
        rec_stack = set()
        
        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get_neighbors(node):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in graph.get_nodes():
            if node not in visited:
                if dfs(node):
                    return True
        
        return False
    
    def find_cycle(self) -> Optional[List[str]]:
        """
        查找图中的一个环
        
        Returns:
            环路径列表，如果不存在环则返回 None
        """
        graph = self._graph
        visited = set()
        rec_stack = []
        rec_stack_set = set()
        
        def dfs(node: str) -> Optional[List[str]]:
            visited.add(node)
            rec_stack.append(node)
            rec_stack_set.add(node)
            
            for neighbor in graph.get_neighbors(node):
                if neighbor in rec_stack_set:
                    # 找到环，提取环路径
                    cycle_start = rec_stack.index(neighbor)
                    return rec_stack[cycle_start:] + [neighbor]
                
                if neighbor not in visited:
                    result = dfs(neighbor)
                    if result:
                        return result
            
            rec_stack.pop()
            rec_stack_set.remove(node)
            return None
        
        for node in graph.get_nodes():
            if node not in visited:
                cycle = dfs(node)
                if cycle:
                    return cycle
        
        return None
    
    def parallel_levels(self) -> List[List[str]]:
        """
        计算并行层级
        
        将节点分组，同一层级的节点可以并行执行（没有依赖关系）。
        
        Returns:
            层级列表，每个层级是可并行执行的节点列表
            
        Raises:
            CycleDetectedError: 图中存在环
        """
        graph = self._graph
        in_degree = {node: graph.in_degree(node) for node in graph.get_nodes()}
        levels = []
        
        # 获取当前层级（入度为 0 的节点）
        current_level = [node for node, degree in in_degree.items() if degree == 0]
        
        while current_level:
            levels.append(sorted(current_level))  # 排序保证结果稳定
            
            next_level = []
            for node in current_level:
                for neighbor in graph.get_neighbors(node):
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0:
                        next_level.append(neighbor)
            
            current_level = next_level
        
        total_nodes = sum(len(level) for level in levels)
        if total_nodes != graph.node_count:
            raise CycleDetectedError("图中存在环，无法进行层级划分")
        
        return levels
    
    def longest_path(self) -> Tuple[int, List[str]]:
        """
        计算最长路径（关键路径）
        
        用于确定任务调度的最短完成时间（假设所有任务串行执行）。
        
        Returns:
            (路径长度, 路径节点列表)
            
        Raises:
            CycleDetectedError: 图中存在环
        """
        graph = self._graph
        
        # 先进行拓扑排序
        topo_order = self.kahn_sort()
        
        # dp[node] = 到达该节点的最长路径长度
        dp = {node: 0 for node in graph.get_nodes()}
        predecessor = {node: None for node in graph.get_nodes()}
        
        for node in topo_order:
            for neighbor in graph.get_neighbors(node):
                if dp[node] + 1 > dp[neighbor]:
                    dp[neighbor] = dp[node] + 1
                    predecessor[neighbor] = node
        
        # 找到最长路径的终点
        max_len = max(dp.values()) if dp else 0
        end_node = None
        for node, length in dp.items():
            if length == max_len:
                end_node = node
                break
        
        # 回溯路径
        path = []
        node = end_node
        while node is not None:
            path.append(node)
            node = predecessor[node]
        path.reverse()
        
        return max_len, path
    
    def longest_path_weighted(self) -> Tuple[float, List[str]]:
        """
        计算带权最长路径
        
        考虑节点权重计算最长路径。节点权重应为数值类型。
        
        Returns:
            (总权重, 路径节点列表)
            
        Raises:
            CycleDetectedError: 图中存在环
        """
        graph = self._graph
        
        # 先进行拓扑排序
        topo_order = self.kahn_sort()
        
        # dp[node] = 到达该节点的最长带权路径
        dp = {}
        predecessor = {}
        
        for node in topo_order:
            # 节点自身权重
            weight = graph.get_node_weight(node, 1)
            try:
                weight = float(weight)
            except (TypeError, ValueError):
                weight = 1.0
            
            # 找最大前驱路径
            max_pred_path = 0.0
            max_pred = None
            for pred in graph.get_predecessors(node):
                if dp.get(pred, 0) > max_pred_path:
                    max_pred_path = dp.get(pred, 0)
                    max_pred = pred
            
            dp[node] = max_pred_path + weight
            predecessor[node] = max_pred
        
        # 找到最长路径的终点
        if not dp:
            return 0.0, []
        
        max_weight = max(dp.values())
        end_node = None
        for node, weight in dp.items():
            if weight == max_weight:
                end_node = node
                break
        
        # 回溯路径
        path = []
        node = end_node
        while node is not None:
            path.append(node)
            node = predecessor.get(node)
        path.reverse()
        
        return max_weight, path
    
    def all_paths(self, start: str, end: str) -> List[List[str]]:
        """
        查找两个节点之间的所有路径
        
        Args:
            start: 起始节点
            end: 目标节点
            
        Returns:
            所有路径列表，每条路径是节点列表
        """
        graph = self._graph
        
        if start not in graph.get_nodes() or end not in graph.get_nodes():
            return []
        
        paths = []
        
        def dfs(node: str, path: List[str], visited: Set[str]):
            if node == end:
                paths.append(path.copy())
                return
            
            for neighbor in graph.get_neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    path.append(neighbor)
                    dfs(neighbor, path, visited)
                    path.pop()
                    visited.remove(neighbor)
        
        dfs(start, [start], {start})
        return paths
    
    def ancestors(self, node: str) -> Set[str]:
        """
        获取节点的所有祖先（直接和间接前驱）
        
        Args:
            node: 目标节点
            
        Returns:
            祖先节点集合
        """
        graph = self._graph
        ancestors = set()
        queue = deque(graph.get_predecessors(node))
        
        while queue:
            current = queue.popleft()
            if current not in ancestors:
                ancestors.add(current)
                queue.extend(graph.get_predecessors(current))
        
        return ancestors
    
    def descendants(self, node: str) -> Set[str]:
        """
        获取节点的所有后代（直接和间接后继）
        
        Args:
            node: 目标节点
            
        Returns:
            后代节点集合
        """
        graph = self._graph
        descendants = set()
        queue = deque(graph.get_neighbors(node))
        
        while queue:
            current = queue.popleft()
            if current not in descendants:
                descendants.add(current)
                queue.extend(graph.get_neighbors(current))
        
        return descendants
    
    def sort_with_priority(self, priority: Callable[[str], int] = None) -> List[str]:
        """
        带优先级的拓扑排序
        
        当多个节点可以同时选择时，按优先级选择。
        
        Args:
            priority: 优先级函数，返回值越小优先级越高
            
        Returns:
            拓扑排序结果列表
            
        Raises:
            CycleDetectedError: 图中存在环
        """
        import heapq
        
        graph = self._graph
        in_degree = {node: graph.in_degree(node) for node in graph.get_nodes()}
        
        # 优先级队列
        if priority:
            heap = [(priority(node), node) for node, degree in in_degree.items() if degree == 0]
        else:
            heap = [(node, node) for node, degree in in_degree.items() if degree == 0]
        
        heapq.heapify(heap)
        result = []
        
        while heap:
            _, node = heapq.heappop(heap)
            result.append(node)
            
            for neighbor in graph.get_neighbors(node):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    if priority:
                        heapq.heappush(heap, (priority(neighbor), neighbor))
                    else:
                        heapq.heappush(heap, (neighbor, neighbor))
        
        if len(result) != graph.node_count:
            raise CycleDetectedError("图中存在环，无法进行拓扑排序")
        
        return result


# 便捷函数

def topological_sort(edges: List[Tuple[str, str]], nodes: Optional[List[str]] = None) -> List[str]:
    """
    快速拓扑排序
    
    Args:
        edges: 边列表
        nodes: 可选的节点列表（会自动从边中提取）
        
    Returns:
        拓扑排序结果
        
    Raises:
        CycleDetectedError: 存在环
    """
    graph = Graph()
    
    if nodes:
        for node in nodes:
            graph.add_node(node)
    
    graph.add_edges(edges)
    
    sorter = TopologicalSorter(graph)
    return sorter.kahn_sort()


def detect_cycle(edges: List[Tuple[str, str]]) -> Optional[List[str]]:
    """
    快速检测环
    
    Args:
        edges: 边列表
        
    Returns:
        环路径，无环返回 None
    """
    graph = Graph()
    graph.add_edges(edges)
    
    sorter = TopologicalSorter(graph)
    return sorter.find_cycle()


def get_parallel_levels(edges: List[Tuple[str, str]], nodes: Optional[List[str]] = None) -> List[List[str]]:
    """
    获取并行层级
    
    Args:
        edges: 边列表
        nodes: 可选的节点列表
        
    Returns:
        层级列表
        
    Raises:
        CycleDetectedError: 存在环
    """
    graph = Graph()
    
    if nodes:
        for node in nodes:
            graph.add_node(node)
    
    graph.add_edges(edges)
    
    sorter = TopologicalSorter(graph)
    return sorter.parallel_levels()


# 导出
__all__ = [
    'Graph',
    'TopologicalSorter',
    'TopologicalSortError',
    'CycleDetectedError',
    'topological_sort',
    'detect_cycle',
    'get_parallel_levels',
]