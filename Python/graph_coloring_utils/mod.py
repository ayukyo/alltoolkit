"""
图着色工具模块
Graph Coloring Utils - 多种图着色算法实现

图着色问题是图论中的经典问题，应用场景包括：
- 课程表安排
- 寄存器分配
- 地图着色
- 频率分配
- 任务调度
"""

from typing import Dict, List, Optional, Set, Tuple, Callable
from collections import defaultdict


class Graph:
    """图数据结构"""
    
    def __init__(self):
        """初始化空图"""
        self.vertices: Set[str] = set()
        self.edges: List[Tuple[str, str]] = []
        self.adjacency: Dict[str, Set[str]] = defaultdict(set)
    
    def add_vertex(self, vertex: str) -> None:
        """添加顶点"""
        self.vertices.add(vertex)
    
    def add_edge(self, v1: str, v2: str) -> None:
        """添加边"""
        self.vertices.add(v1)
        self.vertices.add(v2)
        self.adjacency[v1].add(v2)
        self.adjacency[v2].add(v1)
        self.edges.append((v1, v2))
    
    def get_neighbors(self, vertex: str) -> Set[str]:
        """获取邻居顶点"""
        return self.adjacency.get(vertex, set())
    
    def get_degree(self, vertex: str) -> int:
        """获取顶点的度"""
        return len(self.adjacency.get(vertex, set()))
    
    def get_all_degrees(self) -> Dict[str, int]:
        """获取所有顶点的度"""
        return {v: self.get_degree(v) for v in self.vertices}
    
    @classmethod
    def from_edges(cls, edges: List[Tuple[str, str]]) -> 'Graph':
        """从边列表创建图"""
        graph = cls()
        for v1, v2 in edges:
            graph.add_edge(v1, v2)
        return graph
    
    @classmethod
    def create_grid(cls, rows: int, cols: int) -> 'Graph':
        """创建网格图"""
        graph = cls()
        for r in range(rows):
            for c in range(cols):
                vertex = f"({r},{c})"
                if r > 0:
                    graph.add_edge(vertex, f"({r-1},{c})")
                if c > 0:
                    graph.add_edge(vertex, f"({r},{c-1})")
        return graph
    
    @classmethod
    def create_cycle(cls, n: int) -> 'Graph':
        """创建环图"""
        graph = cls()
        for i in range(n):
            graph.add_edge(f"v{i}", f"v{(i+1)%n}")
        return graph
    
    @classmethod
    def create_complete(cls, n: int) -> 'Graph':
        """创建完全图"""
        graph = cls()
        for i in range(n):
            for j in range(i+1, n):
                graph.add_edge(f"v{i}", f"v{j}")
        return graph
    
    @classmethod
    def create_bipartite(cls, m: int, n: int) -> 'Graph':
        """创建二分图"""
        graph = cls()
        for i in range(m):
            for j in range(n):
                graph.add_edge(f"A{i}", f"B{j}")
        return graph


def greedy_coloring(graph: Graph) -> Dict[str, int]:
    """
    贪心着色算法
    按顶点顺序依次着色，每个顶点选择最小的可用颜色
    
    时间复杂度: O(V + E)
    
    Args:
        graph: 图对象
        
    Returns:
        着色方案字典，顶点 -> 颜色编号
    """
    coloring: Dict[str, int] = {}
    vertices = sorted(graph.vertices)  # 排序确保确定性
    
    for vertex in vertices:
        neighbors = graph.get_neighbors(vertex)
        used_colors = {coloring[n] for n in neighbors if n in coloring}
        
        # 找到最小的未使用颜色
        color = 0
        while color in used_colors:
            color += 1
        
        coloring[vertex] = color
    
    return coloring


def welsh_powell_coloring(graph: Graph) -> Dict[str, int]:
    """
    Welsh-Powell 算法
    按顶点度数降序排列，贪心着色
    通常能比简单贪心获得更少的颜色数
    
    时间复杂度: O(V log V + E)
    
    Args:
        graph: 图对象
        
    Returns:
        着色方案字典
    """
    coloring: Dict[str, int] = {}
    degrees = graph.get_all_degrees()
    
    # 按度数降序排列顶点
    sorted_vertices = sorted(graph.vertices, key=lambda v: degrees[v], reverse=True)
    
    current_color = 0
    uncolored = set(sorted_vertices)
    
    while uncolored:
        # 对当前颜色，遍历所有未着色的顶点
        for vertex in sorted_vertices:
            if vertex not in uncolored:
                continue
            
            # 检查是否可以用当前颜色
            neighbors = graph.get_neighbors(vertex)
            can_color = True
            for n in neighbors:
                if coloring.get(n) == current_color:
                    can_color = False
                    break
            
            if can_color:
                coloring[vertex] = current_color
                uncolored.remove(vertex)
        
        current_color += 1
    
    return coloring


def dsatur_coloring(graph: Graph) -> Dict[str, int]:
    """
    DSatur 算法 (Degree of Saturation)
    选择饱和度最高（已着色邻居颜色种类最多）的顶点着色
    是目前已知的最有效的贪心着色算法之一
    
    时间复杂度: O(V log V + E)
    
    Args:
        graph: 图对象
        
    Returns:
        着色方案字典
    """
    coloring: Dict[str, int] = {}
    
    if not graph.vertices:
        return coloring
    
    # 每个顶点的饱和度（已着色邻居使用的颜色集合）
    saturation: Dict[str, Set[int]] = {v: set() for v in graph.vertices}
    # 未着色顶点的度数
    degrees = graph.get_all_degrees()
    uncolored = set(graph.vertices)
    
    while uncolored:
        # 选择饱和度最高的顶点，如果相同则选择度数最大的
        vertex = max(uncolored, key=lambda v: (len(saturation[v]), degrees[v]))
        
        # 找到最小可用颜色
        neighbors = graph.get_neighbors(vertex)
        used_colors = {coloring[n] for n in neighbors if n in coloring}
        
        color = 0
        while color in used_colors:
            color += 1
        
        coloring[vertex] = color
        uncolored.remove(vertex)
        
        # 更新邻居的饱和度
        for n in neighbors:
            if n in uncolored:
                saturation[n].add(color)
    
    return coloring


def backtracking_coloring(graph: Graph, max_colors: Optional[int] = None) -> Optional[Dict[str, int]]:
    """
    回溯法着色
    尝试找到使用最少颜色的方案（精确算法，但可能较慢）
    
    时间复杂度: O(k^V) 最坏情况
    
    Args:
        graph: 图对象
        max_colors: 最大尝试颜色数，None 表示自动寻找
        
    Returns:
        着色方案字典，如果无法着色返回 None
    """
    vertices = sorted(graph.vertices)
    if not vertices:
        return {}
    
    if max_colors is None:
        # 先用贪心算法估计颜色数上界
        greedy = dsatur_coloring(graph)
        max_colors = max(greedy.values()) + 1 if greedy else 1
        # 尝试找到更优解
        while max_colors > 1:
            result = _backtrack(graph, vertices, {}, 0, max_colors - 1)
            if result is not None:
                max_colors -= 1
            else:
                break
        max_colors += 1
    
    return _backtrack(graph, vertices, {}, 0, max_colors)


def _backtrack(
    graph: Graph,
    vertices: List[str],
    coloring: Dict[str, int],
    index: int,
    max_colors: int
) -> Optional[Dict[str, int]]:
    """回溯辅助函数"""
    if index == len(vertices):
        return coloring.copy()
    
    vertex = vertices[index]
    neighbors = graph.get_neighbors(vertex)
    
    for color in range(max_colors):
        # 检查颜色是否可用
        if any(coloring.get(n) == color for n in neighbors):
            continue
        
        coloring[vertex] = color
        result = _backtrack(graph, vertices, coloring, index + 1, max_colors)
        if result is not None:
            return result
        
        del coloring[vertex]
    
    return None


def is_valid_coloring(graph: Graph, coloring: Dict[str, int]) -> bool:
    """
    验证着色方案是否有效
    
    Args:
        graph: 图对象
        coloring: 着色方案
        
    Returns:
        是否为有效的着色方案
    """
    for v1, v2 in graph.edges:
        if v1 in coloring and v2 in coloring:
            if coloring[v1] == coloring[v2]:
                return False
    return True


def count_colors(coloring: Dict[str, int]) -> int:
    """
    统计使用的颜色数
    
    Args:
        coloring: 着色方案
        
    Returns:
        使用的颜色数量
    """
    return len(set(coloring.values())) if coloring else 0


def get_color_groups(coloring: Dict[str, int]) -> Dict[int, List[str]]:
    """
    按颜色分组顶点
    
    Args:
        coloring: 着色方案
        
    Returns:
        颜色 -> 顶点列表的映射
    """
    groups: Dict[int, List[str]] = defaultdict(list)
    for vertex, color in coloring.items():
        groups[color].append(vertex)
    return dict(groups)


def chromatic_number_bounds(graph: Graph) -> Tuple[int, int]:
    """
    计算色数的下界和上界
    
    下界: 最大团大小或最大度+1的最小值
    上界: 最大度+1（Brooks 定理改进）
    
    Args:
        graph: 图对象
        
    Returns:
        (下界, 上界) 元组
    """
    if not graph.vertices:
        return (0, 0)
    
    if not graph.edges:
        return (1, 1)
    
    degrees = graph.get_all_degrees()
    max_degree = max(degrees.values())
    
    # 下界：最大度至少需要这么多颜色（简化版）
    lower = max_degree // 2 + 1
    
    # 上界：Brooks 定理，最大度+1（简化）
    upper = max_degree + 1
    
    return (lower, upper)


def find_coloring(
    graph: Graph,
    algorithm: str = "dsatur"
) -> Dict[str, int]:
    """
    使用指定算法找图着色方案
    
    Args:
        graph: 图对象
        algorithm: 算法名称 ("greedy", "welsh_powell", "dsatur", "backtracking")
        
    Returns:
        着色方案字典
    """
    algorithms = {
        "greedy": greedy_coloring,
        "welsh_powell": welsh_powell_coloring,
        "dsatur": dsatur_coloring,
        "backtracking": backtracking_coloring
    }
    
    if algorithm not in algorithms:
        raise ValueError(f"未知算法: {algorithm}，可用: {list(algorithms.keys())}")
    
    result = algorithms[algorithm](graph)
    if result is None:
        return {}
    return result


def compare_algorithms(graph: Graph) -> Dict[str, Dict]:
    """
    比较不同算法的着色结果
    
    Args:
        graph: 图对象
        
    Returns:
        各算法的结果统计
    """
    results = {}
    
    for name, algo in [
        ("greedy", greedy_coloring),
        ("welsh_powell", welsh_powell_coloring),
        ("dsatur", dsatur_coloring)
    ]:
        coloring = algo(graph)
        results[name] = {
            "colors": count_colors(coloring),
            "valid": is_valid_coloring(graph, coloring),
            "coloring": coloring
        }
    
    # 回溯法可能较慢，单独处理
    bt_result = backtracking_coloring(graph)
    if bt_result:
        results["backtracking"] = {
            "colors": count_colors(bt_result),
            "valid": is_valid_coloring(graph, bt_result),
            "coloring": bt_result
        }
    
    return results


class IntervalGraph:
    """
    区间图
    特殊的图结构，可以用贪心算法找到最优着色
    应用：课程安排、资源分配
    """
    
    def __init__(self):
        """初始化区间图"""
        self.intervals: List[Tuple[str, Tuple[int, int]]] = []
    
    def add_interval(self, name: str, start: int, end: int) -> None:
        """添加区间"""
        self.intervals.append((name, (start, end)))
    
    def build_graph(self) -> Graph:
        """构建冲突图"""
        graph = Graph()
        for name, _ in self.intervals:
            graph.add_vertex(name)
        
        # 检查区间重叠
        for i, (name1, (s1, e1)) in enumerate(self.intervals):
            for j in range(i + 1, len(self.intervals)):
                name2, (s2, e2) = self.intervals[j]
                # 区间重叠
                if s1 < e2 and s2 < e1:
                    graph.add_edge(name1, name2)
        
        return graph
    
    def optimal_coloring(self) -> Dict[str, int]:
        """
        区间图的最优着色
        使用区间调度算法，O(n log n)
        """
        if not self.intervals:
            return {}
        
        # 按开始时间排序
        sorted_intervals = sorted(self.intervals, key=lambda x: x[1][0])
        coloring: Dict[str, int] = {}
        
        # 每种颜色最后结束时间
        color_end: List[int] = []
        
        for name, (start, end) in sorted_intervals:
            # 找到可用的颜色
            assigned = False
            for i, last_end in enumerate(color_end):
                if start >= last_end:
                    coloring[name] = i
                    color_end[i] = end
                    assigned = True
                    break
            
            if not assigned:
                # 需要新颜色
                color_idx = len(color_end)
                coloring[name] = color_idx
                color_end.append(end)
        
        return coloring


class BipartiteChecker:
    """二分图检测器"""
    
    @staticmethod
    def is_bipartite(graph: Graph) -> Tuple[bool, Optional[Dict[str, int]]]:
        """
        检测图是否为二分图
        
        Returns:
            (是否二分图, 二着色方案)
        """
        coloring: Dict[str, int] = {}
        
        for start in graph.vertices:
            if start in coloring:
                continue
            
            # BFS
            queue = [start]
            coloring[start] = 0
            
            while queue:
                vertex = queue.pop(0)
                for neighbor in graph.get_neighbors(vertex):
                    if neighbor not in coloring:
                        coloring[neighbor] = 1 - coloring[vertex]
                        queue.append(neighbor)
                    elif coloring[neighbor] == coloring[vertex]:
                        return (False, None)
        
        return (True, coloring)