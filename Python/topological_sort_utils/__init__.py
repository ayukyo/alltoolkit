"""
Topological Sort Utilities - 拓扑排序工具库

提供两种经典拓扑排序算法实现，支持循环依赖检测、并行任务分层等功能。
零外部依赖，纯 Python 标准库实现。

使用方法:
    from topological_sort import (
        TopologicalSort,
        topological_sort,
        detect_cycle,
        parallel_layers,
        CycleDetectedError
    )
    
    # 方式1：使用类
    ts = TopologicalSort()
    ts.add_edge('A', 'B')  # A 依赖 B
    ts.add_edge('B', 'C')  # B 依赖 C
    order = ts.sort()  # ['C', 'B', 'A']
    
    # 方式2：使用便捷函数
    nodes = ['A', 'B', 'C']
    edges = [('A', 'B'), ('B', 'C')]
    order = topological_sort(nodes, edges)

功能:
    - Kahn's Algorithm (BFS) 拓扑排序
    - DFS Algorithm 拓扑排序
    - 循环依赖检测
    - 并行任务分层
    - 关键路径分析
    - 依赖关系查询
    - 图操作（反向、拷贝、合并）
"""

from .topological_sort import (
    TopologicalSort,
    topological_sort,
    detect_cycle,
    parallel_layers,
    CycleDetectedError
)

__version__ = '1.0.0'
__all__ = [
    'TopologicalSort',
    'topological_sort',
    'detect_cycle',
    'parallel_layers',
    'CycleDetectedError'
]