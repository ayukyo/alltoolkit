"""
Topological Sort Utilities - 拓扑排序工具库

提供两种经典拓扑排序算法实现，支持循环依赖检测、并行任务分层等功能。
零外部依赖，纯 Python 标准库实现。

用途：
- 任务调度（处理依赖关系）
- 编译顺序确定
- 包管理器依赖解析
- 课程安排
- 构建系统
"""

from collections import deque
from typing import Dict, List, Set, Tuple, Optional, Any, Iterator


class CycleDetectedError(Exception):
    """检测到循环依赖时抛出的异常"""
    
    def __init__(self, cycle: List[str]):
        self.cycle = cycle
        cycle_str = " -> ".join(str(n) for n in cycle)
        super().__init__(f"Cycle detected: {cycle_str}")


class TopologicalSort:
    """
    拓扑排序工具类
    
    支持两种经典算法：
    - Kahn's Algorithm (BFS): 基于入度的广度优先算法
    - DFS Algorithm: 基于深度优先搜索的算法
    
    功能：
    - 拓扑排序
    - 循环依赖检测
    - 并行任务分层
    - 依赖关系分析
    """
    
    def __init__(self):
        self._graph: Dict[Any, Set[Any]] = {}  # 邻接表：节点 -> 依赖的节点集合
        self._nodes: Set[Any] = set()  # 所有节点
    
    def add_node(self, node: Any) -> 'TopologicalSort':
        """
        添加节点
        
        Args:
            node: 节点标识（可以是任意可哈希类型）
        
        Returns:
            self，支持链式调用
        """
        self._nodes.add(node)
        if node not in self._graph:
            self._graph[node] = set()
        return self
    
    def add_edge(self, from_node: Any, to_node: Any) -> 'TopologicalSort':
        """
        添加依赖关系：from_node 依赖 to_node
        即 to_node 必须在 from_node 之前完成
        
        Args:
            from_node: 依赖方节点
            to_node: 被依赖方节点
        
        Returns:
            self，支持链式调用
        """
        self.add_node(from_node)
        self.add_node(to_node)
        self._graph[from_node].add(to_node)
        return self
    
    def add_edges(self, edges: List[Tuple[Any, Any]]) -> 'TopologicalSort':
        """
        批量添加依赖关系
        
        Args:
            edges: 依赖关系列表 [(from, to), ...]
        
        Returns:
            self，支持链式调用
        """
        for from_node, to_node in edges:
            self.add_edge(from_node, to_node)
        return self
    
    def remove_edge(self, from_node: Any, to_node: Any) -> bool:
        """
        移除依赖关系
        
        Args:
            from_node: 依赖方节点
            to_node: 被依赖方节点
        
        Returns:
            是否成功移除
        """
        if from_node in self._graph and to_node in self._graph[from_node]:
            self._graph[from_node].remove(to_node)
            return True
        return False
    
    def remove_node(self, node: Any) -> bool:
        """
        移除节点及其所有相关边
        
        Args:
            node: 要移除的节点
        
        Returns:
            是否成功移除
        """
        if node not in self._nodes:
            return False
        
        self._nodes.remove(node)
        del self._graph[node]
        
        # 移除所有指向该节点的边
        for n in self._graph:
            self._graph[n].discard(node)
        
        return True
    
    def get_dependencies(self, node: Any) -> Set[Any]:
        """
        获取节点的直接依赖
        
        Args:
            node: 目标节点
        
        Returns:
            直接依赖集合
        """
        return self._graph.get(node, set()).copy()
    
    def get_dependents(self, node: Any) -> Set[Any]:
        """
        获取依赖该节点的所有节点
        
        Args:
            node: 目标节点
        
        Returns:
            依赖该节点的节点集合
        """
        dependents = set()
        for n, deps in self._graph.items():
            if node in deps:
                dependents.add(n)
        return dependents
    
    def get_all_dependencies(self, node: Any) -> Set[Any]:
        """
        获取节点的所有依赖（包括传递依赖）
        
        Args:
            node: 目标节点
        
        Returns:
            所有依赖集合
        """
        all_deps = set()
        visited = set()
        stack = list(self._graph.get(node, set()))
        
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            all_deps.add(current)
            stack.extend(self._graph.get(current, set()))
        
        return all_deps
    
    def _compute_indegree(self) -> Dict[Any, int]:
        """计算所有节点的入度"""
        indegree = {node: 0 for node in self._nodes}
        for node in self._nodes:
            for dep in self._graph.get(node, set()):
                indegree[node] += 1
        return indegree
    
    def sort_kahn(self) -> List[Any]:
        """
        Kahn's Algorithm (BFS) 拓扑排序
        
        时间复杂度: O(V + E)
        空间复杂度: O(V)
        
        Returns:
            排序后的节点列表
        
        Raises:
            CycleDetectedError: 存在循环依赖时
        """
        indegree = self._compute_indegree()
        
        # 找到所有入度为0的节点
        queue = deque(node for node, degree in indegree.items() if degree == 0)
        result = []
        
        while queue:
            node = queue.popleft()
            result.append(node)
            
            # 减少依赖该节点的所有节点的入度
            for dependent in self._nodes:
                if node in self._graph.get(dependent, set()):
                    indegree[dependent] -= 1
                    if indegree[dependent] == 0:
                        queue.append(dependent)
        
        if len(result) != len(self._nodes):
            # 存在循环，找出循环路径
            cycle = self._find_cycle()
            raise CycleDetectedError(cycle)
        
        return result
    
    def sort_dfs(self) -> List[Any]:
        """
        DFS Algorithm 拓扑排序
        
        时间复杂度: O(V + E)
        空间复杂度: O(V)
        
        Returns:
            排序后的节点列表
        
        Raises:
            CycleDetectedError: 存在循环依赖时
        """
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {node: WHITE for node in self._nodes}
        result = []
        path = []  # 用于追踪循环路径
        
        def dfs(node: Any) -> bool:
            """DFS遍历，返回是否成功"""
            if color[node] == GRAY:
                # 发现循环，构建循环路径
                cycle_start = path.index(node)
                raise CycleDetectedError(path[cycle_start:] + [node])
            
            if color[node] == BLACK:
                return True
            
            color[node] = GRAY
            path.append(node)
            
            # 先访问依赖的节点
            for dep in self._graph.get(node, set()):
                dfs(dep)
            
            path.pop()
            color[node] = BLACK
            result.append(node)
            return True
        
        for node in self._nodes:
            if color[node] == WHITE:
                dfs(node)
        
        return result
    
    def sort(self, algorithm: str = 'kahn') -> List[Any]:
        """
        拓扑排序（默认使用 Kahn's Algorithm）
        
        Args:
            algorithm: 'kahn' 或 'dfs'
        
        Returns:
            排序后的节点列表
        """
        if algorithm == 'dfs':
            return self.sort_dfs()
        return self.sort_kahn()
    
    def _find_cycle(self) -> List[Any]:
        """查找图中的循环路径"""
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {node: WHITE for node in self._nodes}
        path = []
        
        def dfs(node: Any) -> Optional[List[Any]]:
            color[node] = GRAY
            path.append(node)
            
            for dep in self._graph.get(node, set()):
                if color[dep] == GRAY:
                    # 找到循环
                    cycle_start = path.index(dep)
                    return path[cycle_start:] + [dep]
                elif color[dep] == WHITE:
                    result = dfs(dep)
                    if result:
                        return result
            
            path.pop()
            color[node] = BLACK
            return None
        
        for node in self._nodes:
            if color[node] == WHITE:
                cycle = dfs(node)
                if cycle:
                    return cycle
        
        return []
    
    def has_cycle(self) -> bool:
        """
        检测是否存在循环依赖
        
        Returns:
            是否存在循环
        """
        try:
            self.sort_kahn()
            return False
        except CycleDetectedError:
            return True
    
    def get_cycle(self) -> Optional[List[Any]]:
        """
        获取循环依赖路径
        
        Returns:
            循环路径，如果不存在循环则返回 None
        """
        if not self.has_cycle():
            return None
        return self._find_cycle()
    
    def layers(self) -> List[List[Any]]:
        """
        并行任务分层
        
        将节点分成多层，每层的节点可以并行执行。
        第 i 层的节点只依赖于第 0 到 i-1 层的节点。
        
        Returns:
            分层列表，每层是一个节点列表
        
        Raises:
            CycleDetectedError: 存在循环依赖时
        """
        if self.has_cycle():
            raise CycleDetectedError(self._find_cycle())
        
        indegree = self._compute_indegree()
        layers = []
        remaining = set(self._nodes)
        
        while remaining:
            # 找到当前入度为0的所有节点
            current_layer = [node for node in remaining if indegree[node] == 0]
            
            if not current_layer:
                break
            
            layers.append(current_layer)
            
            # 移除当前层的节点，更新入度
            for node in current_layer:
                remaining.remove(node)
                for dependent in self._nodes:
                    if node in self._graph.get(dependent, set()):
                        indegree[dependent] -= 1
        
        return layers
    
    def parallel_levels(self) -> Dict[Any, int]:
        """
        获取每个节点的并行层级
        
        Returns:
            节点到层级的映射，层级从0开始
        
        Raises:
            CycleDetectedError: 存在循环依赖时
        """
        layers = self.layers()
        levels = {}
        for i, layer in enumerate(layers):
            for node in layer:
                levels[node] = i
        return levels
    
    def critical_path(self) -> Tuple[List[Any], int]:
        """
        计算关键路径（最长依赖路径）
        
        Returns:
            (关键路径节点列表, 路径长度)
        
        Raises:
            CycleDetectedError: 存在循环依赖时
        """
        if self.has_cycle():
            raise CycleDetectedError(self._find_cycle())
        
        # 计算每个节点的最长距离
        distances: Dict[Any, int] = {}
        predecessors: Dict[Any, Any] = {}
        
        sorted_nodes = self.sort_kahn()
        
        for node in sorted_nodes:
            max_dist = 0
            max_pred = None
            for dep in self._graph.get(node, set()):
                if distances.get(dep, 0) + 1 > max_dist:
                    max_dist = distances.get(dep, 0) + 1
                    max_pred = dep
            distances[node] = max_dist
            if max_pred is not None:
                predecessors[node] = max_pred
        
        if not distances:
            return [], 0
        
        # 找到最大距离的节点
        end_node = max(distances, key=distances.get)
        path_length = distances[end_node]
        
        # 重建路径
        path = [end_node]
        current = end_node
        while current in predecessors:
            current = predecessors[current]
            path.append(current)
        
        return path[::-1], path_length
    
    def min_steps(self) -> int:
        """
        计算完成所有任务所需的最少步骤数
        
        等同于并行分层的层数
        
        Returns:
            最少步骤数
        """
        return len(self.layers())
    
    def is_valid_order(self, nodes: List[Any]) -> bool:
        """
        验证给定的顺序是否是有效的拓扑排序
        
        Args:
            nodes: 节点顺序列表
        
        Returns:
            是否有效
        """
        if set(nodes) != self._nodes:
            return False
        
        position = {node: i for i, node in enumerate(nodes)}
        
        for node in self._nodes:
            for dep in self._graph.get(node, set()):
                if position[dep] >= position[node]:
                    return False
        
        return True
    
    def can_reach(self, from_node: Any, to_node: Any) -> bool:
        """
        检查是否可以从 from_node 到达 to_node（通过依赖关系）
        
        Args:
            from_node: 起点
            to_node: 终点
        
        Returns:
            是否可达
        """
        visited = set()
        stack = list(self._graph.get(from_node, set()))
        
        while stack:
            current = stack.pop()
            if current == to_node:
                return True
            if current in visited:
                continue
            visited.add(current)
            stack.extend(self._graph.get(current, set()))
        
        return False
    
    def reverse(self) -> 'TopologicalSort':
        """
        创建反向图（依赖关系反转）
        
        Returns:
            新的 TopologicalSort 实例
        """
        reversed_graph = TopologicalSort()
        for node in self._nodes:
            reversed_graph.add_node(node)
        for node, deps in self._graph.items():
            for dep in deps:
                reversed_graph.add_edge(dep, node)
        return reversed_graph
    
    def copy(self) -> 'TopologicalSort':
        """
        创建图的深拷贝
        
        Returns:
            新的 TopologicalSort 实例
        """
        new_graph = TopologicalSort()
        new_graph._nodes = self._nodes.copy()
        new_graph._graph = {k: v.copy() for k, v in self._graph.items()}
        return new_graph
    
    def merge(self, other: 'TopologicalSort') -> 'TopologicalSort':
        """
        合并另一个拓扑图
        
        Args:
            other: 另一个 TopologicalSort 实例
        
        Returns:
            合并后的新实例
        """
        merged = self.copy()
        for node in other._nodes:
            merged.add_node(node)
        for node, deps in other._graph.items():
            for dep in deps:
                merged.add_edge(node, dep)
        return merged
    
    @property
    def node_count(self) -> int:
        """节点数量"""
        return len(self._nodes)
    
    @property
    def edge_count(self) -> int:
        """边数量"""
        return sum(len(deps) for deps in self._graph.values())
    
    def __len__(self) -> int:
        return self.node_count
    
    def __contains__(self, node: Any) -> bool:
        return node in self._nodes
    
    def __iter__(self) -> Iterator[Any]:
        return iter(self._nodes)
    
    def __repr__(self) -> str:
        return f"TopologicalSort(nodes={self.node_count}, edges={self.edge_count})"


def topological_sort(
    nodes: List[Any],
    edges: List[Tuple[Any, Any]],
    algorithm: str = 'kahn'
) -> List[Any]:
    """
    便捷函数：对给定的节点和边进行拓扑排序
    
    Args:
        nodes: 节点列表
        edges: 边列表 [(from, to), ...]，表示 from 依赖 to
        algorithm: 算法选择，'kahn' 或 'dfs'
    
    Returns:
        排序后的节点列表
    
    Raises:
        CycleDetectedError: 存在循环依赖时
    
    Example:
        >>> nodes = ['A', 'B', 'C']
        >>> edges = [('A', 'B'), ('B', 'C')]  # A 依赖 B, B 依赖 C
        >>> topological_sort(nodes, edges)
        ['C', 'B', 'A']
    """
    ts = TopologicalSort()
    for node in nodes:
        ts.add_node(node)
    ts.add_edges(edges)
    return ts.sort(algorithm)


def detect_cycle(
    nodes: List[Any],
    edges: List[Tuple[Any, Any]]
) -> Optional[List[Any]]:
    """
    便捷函数：检测图中是否存在循环
    
    Args:
        nodes: 节点列表
        edges: 边列表
    
    Returns:
        循环路径，如果不存在则返回 None
    
    Example:
        >>> nodes = ['A', 'B', 'C']
        >>> edges = [('A', 'B'), ('B', 'C'), ('C', 'A')]
        >>> detect_cycle(nodes, edges)
        ['A', 'B', 'C', 'A']
    """
    ts = TopologicalSort()
    for node in nodes:
        ts.add_node(node)
    ts.add_edges(edges)
    return ts.get_cycle()


def parallel_layers(
    nodes: List[Any],
    edges: List[Tuple[Any, Any]]
) -> List[List[Any]]:
    """
    便捷函数：计算并行分层
    
    Args:
        nodes: 节点列表
        edges: 边列表
    
    Returns:
        分层列表
    
    Raises:
        CycleDetectedError: 存在循环依赖时
    
    Example:
        >>> nodes = ['A', 'B', 'C', 'D']
        >>> edges = [('A', 'C'), ('B', 'C'), ('C', 'D')]
        >>> parallel_layers(nodes, edges)
        [['C'], ['A', 'B'], ['D']]  # 修正：C无依赖，A和B只依赖C，D依赖C
    """
    ts = TopologicalSort()
    for node in nodes:
        ts.add_node(node)
    ts.add_edges(edges)
    return ts.layers()