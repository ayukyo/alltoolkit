"""
Tarjan's Algorithm Utilities

Tarjan 算法用于在有向图中查找强连通分量（Strongly Connected Components, SCC）。
强连通分量是指图中的一组节点，其中每个节点都可以到达该组中的任何其他节点。

零外部依赖，仅使用 Python 标准库。
"""

from typing import Dict, List, Set, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class TarjanResult:
    """Tarjan 算法结果"""
    sccs: List[List[Any]]
    scc_count: int
    node_to_scc: Dict[Any, int]
    is_dag: bool


class TarjanAlgorithm:
    """Tarjan 算法实现"""
    
    def __init__(self):
        self.index = 0
        self.stack: List[Any] = []
        self.on_stack: Set[Any] = set()
        self.indices: Dict[Any, int] = {}
        self.lowlinks: Dict[Any, int] = {}
        self.sccs: List[List[Any]] = []
        self.node_to_scc: Dict[Any, int] = {}
    
    def find_sccs(self, graph: Dict[Any, List[Any]]) -> TarjanResult:
        """执行 Tarjan 算法，查找所有强连通分量"""
        self.index = 0
        self.stack = []
        self.on_stack = set()
        self.indices = {}
        self.lowlinks = {}
        self.sccs = []
        self.node_to_scc = {}
        
        all_nodes = set(graph.keys())
        for neighbors in graph.values():
            all_nodes.update(neighbors)
        
        for node in all_nodes:
            if node not in graph:
                graph[node] = []
        
        for node in all_nodes:
            if node not in self.indices:
                self._strongconnect(node, graph)
        
        for i, scc in enumerate(self.sccs):
            for node in scc:
                self.node_to_scc[node] = i
        
        return TarjanResult(
            sccs=self.sccs,
            scc_count=len(self.sccs),
            node_to_scc=self.node_to_scc,
            is_dag=len(self.sccs) == len(all_nodes)
        )
    
    def _strongconnect(self, v: Any, graph: Dict[Any, List[Any]]):
        """Tarjan 算法的核心递归函数"""
        self.indices[v] = self.index
        self.lowlinks[v] = self.index
        self.index += 1
        self.stack.append(v)
        self.on_stack.add(v)
        
        neighbors = graph.get(v, [])
        for w in neighbors:
            if w not in self.indices:
                self._strongconnect(w, graph)
                self.lowlinks[v] = min(self.lowlinks[v], self.lowlinks[w])
            elif w in self.on_stack:
                self.lowlinks[v] = min(self.lowlinks[v], self.indices[w])
        
        if self.lowlinks[v] == self.indices[v]:
            scc = []
            while True:
                w = self.stack.pop()
                self.on_stack.remove(w)
                scc.append(w)
                if w == v:
                    break
            self.sccs.append(scc)


def tarjan(graph: Dict[Any, List[Any]]) -> List[List[Any]]:
    """
    使用 Tarjan 算法查找所有强连通分量
    
    Args:
        graph: 有向图，格式为 {node: [neighbors]}
    
    Returns:
        强连通分量列表，每个 SCC 是一个节点列表
    
    Examples:
        >>> graph = {0: [1], 1: [2], 2: [0, 3], 3: [4], 4: [3]}
        >>> tarjan(graph)
        [[0, 1, 2], [3, 4]]
    """
    algo = TarjanAlgorithm()
    result = algo.find_sccs(graph)
    return result.sccs


def tarjan_with_info(graph: Dict[Any, List[Any]]) -> TarjanResult:
    """
    使用 Tarjan 算法查找 SCC，返回完整信息
    
    Args:
        graph: 有向图
    
    Returns:
        TarjanResult 包含所有信息
    """
    algo = TarjanAlgorithm()
    return algo.find_sccs(graph)


def is_strongly_connected(graph: Dict[Any, List[Any]]) -> bool:
    """
    检查图是否强连通（只有一个 SCC）
    
    Args:
        graph: 有向图
    
    Returns:
        是否强连通
    """
    result = tarjan_with_info(graph)
    return result.scc_count == 1


def count_scc(graph: Dict[Any, List[Any]]) -> int:
    """
    计算强连通分量数量
    
    Args:
        graph: 有向图
    
    Returns:
        SCC 数量
    """
    return len(tarjan(graph))


def largest_scc(graph: Dict[Any, List[Any]]) -> List[Any]:
    """
    获取最大的强连通分量
    
    Args:
        graph: 有向图
    
    Returns:
        最大的 SCC（节点数量最多）
    """
    sccs = tarjan(graph)
    if not sccs:
        return []
    return max(sccs, key=len)


def smallest_scc(graph: Dict[Any, List[Any]]) -> List[Any]:
    """
    获取最小的强连通分量
    
    Args:
        graph: 有向图
    
    Returns:
        最小的 SCC
    """
    sccs = tarjan(graph)
    if not sccs:
        return []
    multi_node_sccs = [scc for scc in sccs if len(scc) > 1]
    if not multi_node_sccs:
        return min(sccs, key=len) if sccs else []
    return min(multi_node_sccs, key=len)


def find_cycles(graph: Dict[Any, List[Any]]) -> List[List[Any]]:
    """
    使用 SCC 查找图中的所有环
    
    Args:
        graph: 有向图
    
    Returns:
        所有环（每个 SCC 中大小 > 1）
    """
    sccs = tarjan(graph)
    return [scc for scc in sccs if len(scc) > 1]


def has_cycle(graph: Dict[Any, List[Any]]) -> bool:
    """
    检查图中是否有环
    
    Args:
        graph: 有向图
    
    Returns:
        是否有环
    """
    # 检查自环
    for node, neighbors in graph.items():
        if node in neighbors:
            return True
    
    # 检查 SCC 中的环
    sccs = tarjan(graph)
    return any(len(scc) > 1 for scc in sccs)


def condensation_graph(graph: Dict[Any, List[Any]]) -> Dict[int, List[int]]:
    """
    构建缩点图（将每个 SCC 缩为一个节点）
    
    Args:
        graph: 原始图
    
    Returns:
        缩点图，是一个 DAG
    """
    result = tarjan_with_info(graph)
    condensed: Dict[int, Set[int]] = defaultdict(set)
    
    for node, neighbors in graph.items():
        node_scc = result.node_to_scc[node]
        for neighbor in neighbors:
            neighbor_scc = result.node_to_scc[neighbor]
            if node_scc != neighbor_scc:
                condensed[node_scc].add(neighbor_scc)
    
    return {k: list(v) for k, v in condensed.items()}


def scc_sizes(graph: Dict[Any, List[Any]]) -> List[int]:
    """
    获取所有 SCC 的大小
    
    Args:
        graph: 有向图
    
    Returns:
        SCC 大小列表
    """
    sccs = tarjan(graph)
    return [len(scc) for scc in sccs]


def scc_distribution(graph: Dict[Any, List[Any]]) -> Dict[int, int]:
    """
    获取 SCC 大小分布
    
    Args:
        graph: 有向图
    
    Returns:
        {大小: 数量} 分布字典
    """
    sizes = scc_sizes(graph)
    distribution: Dict[int, int] = defaultdict(int)
    for size in sizes:
        distribution[size] += 1
    return dict(distribution)


def get_scc_for_node(graph: Dict[Any, List[Any]], node: Any) -> List[Any]:
    """
    获取包含指定节点的 SCC
    
    Args:
        graph: 有向图
        node: 目标节点
    
    Returns:
        包含该节点的 SCC
    """
    result = tarjan_with_info(graph)
    if node not in result.node_to_scc:
        return [node]
    scc_index = result.node_to_scc[node]
    return result.sccs[scc_index]


def is_in_cycle(graph: Dict[Any, List[Any]], node: Any) -> bool:
    """
    检查节点是否在环中
    
    Args:
        graph: 有向图
        node: 目标节点
    
    Returns:
        是否在环中
    """
    scc = get_scc_for_node(graph, node)
    return len(scc) > 1


def build_scc_adjacency(graph: Dict[Any, List[Any]]):
    """
    构建 SCC 内部的邻接表
    
    Args:
        graph: 原始图
    
    Returns:
        字典格式: {scc_index: {node: [neighbors_in_same_scc]}}
    """
    result = tarjan_with_info(graph)
    scc_adjacency = defaultdict(dict)
    
    for node, neighbors in graph.items():
        node_scc = result.node_to_scc[node]
        same_scc_neighbors = [
            n for n in neighbors 
            if result.node_to_scc.get(n) == node_scc
        ]
        if same_scc_neighbors:
            if node not in scc_adjacency[node_scc]:
                scc_adjacency[node_scc][node] = []
            scc_adjacency[node_scc][node].extend(same_scc_neighbors)
    
    return dict(scc_adjacency)


def sort_nodes_by_scc(graph: Dict[Any, List[Any]]) -> List[Any]:
    """
    按 SCC 顺序排序节点（用于处理依赖关系）
    
    Args:
        graph: 有向图
    
    Returns:
        排序后的节点列表
    """
    sccs = tarjan(graph)
    result = []
    for scc in sccs:
        result.extend(scc)
    return result


def from_edge_list(edges: List[Tuple[Any, Any]]) -> Dict[Any, List[Any]]:
    """
    从边列表构建图
    
    Args:
        edges: [(from, to), ...] 边列表
    
    Returns:
        图邻接表
    """
    graph: Dict[Any, List[Any]] = defaultdict(list)
    for from_node, to_node in edges:
        graph[from_node].append(to_node)
        if to_node not in graph:
            graph[to_node] = []
    return dict(graph)


def from_adjacency_matrix(matrix: List[List[int]]) -> Dict[int, List[int]]:
    """
    从邻接矩阵构建图
    
    Args:
        matrix: 邻接矩阵
    
    Returns:
        图邻接表
    """
    graph: Dict[int, List[int]] = {}
    n = len(matrix)
    for i in range(n):
        graph[i] = []
        for j in range(n):
            if matrix[i][j]:
                graph[i].append(j)
    return graph


# Convenience aliases
strongly_connected_components = tarjan
find_scc = tarjan
scc_count = count_scc


if __name__ == "__main__":
    # Demo
    print("Tarjan's Algorithm - Strongly Connected Components")
    print("=" * 50)
    
    graph1 = {
        0: [1],
        1: [2],
        2: [0, 3],
        3: [4],
        4: [3]
    }
    
    print("\nGraph 1: 0->1->2->0, 2->3->4->3")
    sccs1 = tarjan(graph1)
    print(f"SCCs: {sccs1}")
    print(f"SCC count: {count_scc(graph1)}")
    print(f"Largest SCC: {largest_scc(graph1)}")
    print(f"Has cycle: {has_cycle(graph1)}")
    
    graph2 = {
        0: [1, 2],
        1: [3],
        2: [3],
        3: []
    }
    
    print("\nGraph 2: DAG")
    sccs2 = tarjan(graph2)
    print(f"SCCs: {sccs2}")
    print(f"Is DAG: {tarjan_with_info(graph2).is_dag}")
    
    graph3 = {
        0: [1],
        1: [2],
        2: [0]
    }
    
    print("\nGraph 3: Strongly connected")
    print(f"Is strongly connected: {is_strongly_connected(graph3)}")
    
    print("\nCondensation graph of Graph 1:")
    condensed = condensation_graph(graph1)
    print(f"Condensed: {condensed}")