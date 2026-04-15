"""
Dependency Resolver Utils - 依赖解析工具模块

提供基于拓扑排序的依赖解析功能，支持循环检测、并行执行顺序优化等。

功能特性:
- 拓扑排序: 将依赖图转换为线性执行顺序
- 循环检测: 检测并报告循环依赖
- 并行层级: 计算可并行执行的任务层级
- 依赖图可视化: 文本格式的依赖关系图
- 最小依赖集: 找出无依赖的根节点

使用场景:
- 包管理器依赖解析
- 构建系统任务调度
- 插件加载顺序
- 模块初始化顺序
- 任务调度系统

零外部依赖，纯 Python 标准库实现。
"""

from typing import Dict, List, Set, Tuple, Optional, Any, Iterator
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
import json


class ResolutionError(Exception):
    """依赖解析错误基类"""
    pass


class CyclicDependencyError(ResolutionError):
    """循环依赖错误"""
    
    def __init__(self, cycle: List[str]):
        self.cycle = cycle
        cycle_str = " -> ".join(cycle)
        super().__init__(f"检测到循环依赖: {cycle_str}")


class MissingDependencyError(ResolutionError):
    """缺少依赖错误"""
    
    def __init__(self, node: str, missing: str):
        self.node = node
        self.missing = missing
        super().__init__(f"节点 '{node}' 依赖不存在的节点 '{missing}'")


class NodeType(Enum):
    """节点类型枚举"""
    NORMAL = "normal"      # 普通节点
    ROOT = "root"          # 根节点（无依赖）
    LEAF = "leaf"          # 叶节点（无被依赖）


@dataclass
class NodeInfo:
    """节点信息"""
    name: str
    dependencies: Set[str] = field(default_factory=set)
    dependents: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def in_degree(self) -> int:
        """入度（依赖数量）"""
        return len(self.dependencies)
    
    @property
    def out_degree(self) -> int:
        """出度（被依赖数量）"""
        return len(self.dependents)
    
    @property
    def is_root(self) -> bool:
        """是否为根节点"""
        return self.in_degree == 0
    
    @property
    def is_leaf(self) -> bool:
        """是否为叶节点"""
        return self.out_degree == 0


@dataclass
class ResolutionResult:
    """解析结果"""
    order: List[str]                    # 拓扑排序结果
    levels: List[List[str]]             # 并行层级
    nodes: Dict[str, NodeInfo]          # 节点信息
    has_cycles: bool = False            # 是否存在循环
    cycles: List[List[str]] = field(default_factory=list)  # 循环列表
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "order": self.order,
            "levels": self.levels,
            "has_cycles": self.has_cycles,
            "cycles": self.cycles,
            "node_count": len(self.nodes)
        }
    
    def to_json(self, indent: int = 2) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


class DependencyGraph:
    """
    依赖图类
    
    用于管理依赖关系图，支持添加节点、设置依赖、解析执行顺序等。
    
    示例:
        >>> graph = DependencyGraph()
        >>> graph.add_node("A")
        >>> graph.add_node("B", dependencies=["A"])
        >>> graph.add_node("C", dependencies=["A", "B"])
        >>> result = graph.resolve()
        >>> print(result.order)  # ['A', 'B', 'C']
    """
    
    def __init__(self, name: str = "DependencyGraph"):
        """
        初始化依赖图
        
        Args:
            name: 图名称，用于标识
        """
        self.name = name
        self._nodes: Dict[str, NodeInfo] = {}
        self._resolved: bool = False
        self._result: Optional[ResolutionResult] = None
    
    def __contains__(self, node: str) -> bool:
        """检查节点是否存在"""
        return node in self._nodes
    
    def __len__(self) -> int:
        """返回节点数量"""
        return len(self._nodes)
    
    def __iter__(self) -> Iterator[str]:
        """迭代所有节点名称"""
        return iter(self._nodes)
    
    def __repr__(self) -> str:
        return f"DependencyGraph(name={self.name!r}, nodes={len(self)})"
    
    @property
    def nodes(self) -> Dict[str, NodeInfo]:
        """获取所有节点"""
        return self._nodes
    
    @property
    def node_names(self) -> Set[str]:
        """获取所有节点名称"""
        return set(self._nodes.keys())
    
    def add_node(
        self, 
        name: str, 
        dependencies: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> "DependencyGraph":
        """
        添加节点
        
        Args:
            name: 节点名称
            dependencies: 依赖节点列表
            metadata: 节点元数据
            
        Returns:
            self，支持链式调用
            
        Raises:
            ValueError: 节点名称为空
        """
        if not name or not name.strip():
            raise ValueError("节点名称不能为空")
        
        name = name.strip()
        
        if name not in self._nodes:
            self._nodes[name] = NodeInfo(name=name)
        
        if dependencies:
            for dep in dependencies:
                self.add_dependency(name, dep)
        
        if metadata:
            self._nodes[name].metadata.update(metadata)
        
        self._resolved = False
        return self
    
    def add_dependency(self, node: str, dependency: str) -> "DependencyGraph":
        """
        添加依赖关系
        
        Args:
            node: 节点名称
            dependency: 依赖的节点名称
            
        Returns:
            self，支持链式调用
            
        Raises:
            ValueError: 节点不存在
        """
        node = node.strip()
        dependency = dependency.strip()
        
        if node not in self._nodes:
            raise ValueError(f"节点 '{node}' 不存在，请先添加节点")
        
        # 自动创建依赖节点（如果不存在）
        if dependency not in self._nodes:
            self._nodes[dependency] = NodeInfo(name=dependency)
        
        self._nodes[node].dependencies.add(dependency)
        self._nodes[dependency].dependents.add(node)
        self._resolved = False
        return self
    
    def remove_dependency(self, node: str, dependency: str) -> "DependencyGraph":
        """
        移除依赖关系
        
        Args:
            node: 节点名称
            dependency: 依赖的节点名称
            
        Returns:
            self，支持链式调用
        """
        if node in self._nodes and dependency in self._nodes[node].dependencies:
            self._nodes[node].dependencies.discard(dependency)
            self._nodes[dependency].dependents.discard(node)
            self._resolved = False
        return self
    
    def remove_node(self, name: str) -> "DependencyGraph":
        """
        移除节点及其所有依赖关系
        
        Args:
            name: 节点名称
            
        Returns:
            self，支持链式调用
        """
        if name not in self._nodes:
            return self
        
        # 移除该节点对其他节点的依赖关系
        for dep in list(self._nodes[name].dependencies):
            self._nodes[dep].dependents.discard(name)
        
        # 移除其他节点对该节点的依赖关系
        for dependent in list(self._nodes[name].dependents):
            self._nodes[dependent].dependencies.discard(name)
        
        del self._nodes[name]
        self._resolved = False
        return self
    
    def get_roots(self) -> List[str]:
        """
        获取根节点（无依赖的节点）
        
        Returns:
            根节点名称列表
        """
        return [name for name, info in self._nodes.items() if info.is_root]
    
    def get_leaves(self) -> List[str]:
        """
        获取叶节点（无被依赖的节点）
        
        Returns:
            叶节点名称列表
        """
        return [name for name, info in self._nodes.items() if info.is_leaf]
    
    def get_dependencies(self, node: str) -> Set[str]:
        """
        获取节点的直接依赖
        
        Args:
            node: 节点名称
            
        Returns:
            依赖节点集合
        """
        if node not in self._nodes:
            raise ValueError(f"节点 '{node}' 不存在")
        return self._nodes[node].dependencies.copy()
    
    def get_dependents(self, node: str) -> Set[str]:
        """
        获取直接依赖该节点的节点
        
        Args:
            node: 节点名称
            
        Returns:
            依赖该节点的节点集合
        """
        if node not in self._nodes:
            raise ValueError(f"节点 '{node}' 不存在")
        return self._nodes[node].dependents.copy()
    
    def get_all_dependencies(self, node: str) -> Set[str]:
        """
        获取节点的所有传递依赖（包括依赖的依赖）
        
        Args:
            node: 节点名称
            
        Returns:
            所有依赖节点集合
        """
        if node not in self._nodes:
            raise ValueError(f"节点 '{node}' 不存在")
        
        all_deps = set()
        queue = deque(self._nodes[node].dependencies)
        
        while queue:
            dep = queue.popleft()
            if dep not in all_deps and dep in self._nodes:
                all_deps.add(dep)
                queue.extend(self._nodes[dep].dependencies)
        
        return all_deps
    
    def get_all_dependents(self, node: str) -> Set[str]:
        """
        获取所有直接或间接依赖该节点的节点
        
        Args:
            node: 节点名称
            
        Returns:
            所有依赖该节点的节点集合
        """
        if node not in self._nodes:
            raise ValueError(f"节点 '{node}' 不存在")
        
        all_dependents = set()
        queue = deque(self._nodes[node].dependents)
        
        while queue:
            dep = queue.popleft()
            if dep not in all_dependents and dep in self._nodes:
                all_dependents.add(dep)
                queue.extend(self._nodes[dep].dependents)
        
        return all_dependents
    
    def detect_cycles(self) -> List[List[str]]:
        """
        检测循环依赖
        
        Returns:
            循环路径列表，每个循环是一个节点名称列表
        """
        cycles = []
        visited = set()
        rec_stack = set()
        path = []
        
        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for dep in self._nodes.get(node, NodeInfo(name="")).dependencies:
                if dep not in visited:
                    if dfs(dep):
                        return True
                elif dep in rec_stack:
                    # 找到循环
                    cycle_start = path.index(dep)
                    cycle = path[cycle_start:] + [dep]
                    cycles.append(cycle)
            
            path.pop()
            rec_stack.discard(node)
            return False
        
        for node in self._nodes:
            if node not in visited:
                dfs(node)
        
        return cycles
    
    def resolve(self, allow_cycles: bool = False) -> ResolutionResult:
        """
        解析依赖，返回拓扑排序结果
        
        Args:
            allow_cycles: 是否允许循环依赖（如果允许，会尝试最大程度解析）
            
        Returns:
            ResolutionResult 对象
            
        Raises:
            CyclicDependencyError: 存在循环依赖且不允许循环
            MissingDependencyError: 存在不存在的依赖
        """
        # 检测循环
        cycles = self.detect_cycles()
        
        # 构建入度表（排除循环节点）
        in_degree = {}
        cycle_nodes = set()
        
        if cycles:
            for cycle in cycles:
                cycle_nodes.update(cycle[:-1])  # 最后一个是重复的起点
            
            if not allow_cycles:
                raise CyclicDependencyError(cycles[0])
        
        # 初始化入度
        for name, info in self._nodes.items():
            if name not in cycle_nodes:
                in_degree[name] = len([
                    d for d in info.dependencies 
                    if d not in cycle_nodes
                ])
        
        # Kahn 算法
        queue = deque([n for n, d in in_degree.items() if d == 0])
        order = []
        
        while queue:
            node = queue.popleft()
            order.append(node)
            
            for dependent in self._nodes[node].dependents:
                if dependent in in_degree:
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        queue.append(dependent)
        
        # 计算并行层级
        levels = self._compute_levels(order, cycle_nodes)
        
        self._result = ResolutionResult(
            order=order,
            levels=levels,
            nodes=dict(self._nodes),
            has_cycles=len(cycles) > 0,
            cycles=cycles
        )
        self._resolved = True
        
        return self._result
    
    def _compute_levels(
        self, 
        order: List[str], 
        exclude: Set[str]
    ) -> List[List[str]]:
        """
        计算并行执行层级
        
        Args:
            order: 拓扑排序结果
            exclude: 要排除的节点集合
            
        Returns:
            层级列表，每层可并行执行
        """
        if not order:
            return []
        
        levels = []
        node_level: Dict[str, int] = {}
        
        for node in order:
            if node in exclude:
                continue
                
            # 节点的层级是其依赖的最大层级 + 1
            max_dep_level = -1
            for dep in self._nodes[node].dependencies:
                if dep in node_level:
                    max_dep_level = max(max_dep_level, node_level[dep])
            
            node_level[node] = max_dep_level + 1
        
        # 按层级分组
        if node_level:
            max_level = max(node_level.values())
            levels = [[] for _ in range(max_level + 1)]
            for node, level in node_level.items():
                levels[level].append(node)
        
        return levels
    
    def get_execution_order(self) -> List[str]:
        """
        获取执行顺序（快捷方法）
        
        Returns:
            节点执行顺序列表
        """
        if not self._resolved:
            result = self.resolve()
        else:
            result = self._result
        return result.order if result else []
    
    def get_parallel_levels(self) -> List[List[str]]:
        """
        获取并行执行层级（快捷方法）
        
        Returns:
            层级列表，每层可并行执行
        """
        if not self._resolved:
            result = self.resolve()
        else:
            result = self._result
        return result.levels if result else []
    
    def visualize(self, max_depth: int = 10) -> str:
        """
        生成文本格式的依赖关系图
        
        Args:
            max_depth: 最大显示深度
            
        Returns:
            文本格式的依赖图
        """
        lines = [f"=== {self.name} ===", ""]
        
        roots = self.get_roots()
        if not roots:
            roots = list(self._nodes.keys())[:5]  # 如果没有根节点，取前5个
        
        visited = set()
        
        def render(node: str, prefix: str = "", is_last: bool = True) -> List[str]:
            if node in visited or len(visited) > max_depth * 10:
                return [f"{prefix}└── {node} (循环)"]
            
            visited.add(node)
            result = []
            connector = "└── " if is_last else "├── "
            result.append(f"{prefix}{connector}{node}")
            
            deps = sorted(self._nodes[node].dependencies)
            for i, dep in enumerate(deps):
                is_last_dep = i == len(deps) - 1
                new_prefix = prefix + ("    " if is_last else "│   ")
                result.extend(render(dep, new_prefix, is_last_dep))
            
            return result
        
        for i, root in enumerate(sorted(roots)):
            is_last_root = i == len(roots) - 1
            lines.append(f"根节点: {root}")
            for dep in sorted(self._nodes[root].dependencies):
                is_last = dep == sorted(self._nodes[root].dependencies)[-1]
                lines.extend(render(dep, "", is_last))
            if i < len(roots) - 1:
                lines.append("")
        
        # 统计信息
        lines.append("")
        lines.append(f"节点总数: {len(self._nodes)}")
        lines.append(f"根节点数: {len(self.get_roots())}")
        lines.append(f"叶节点数: {len(self.get_leaves())}")
        
        cycles = self.detect_cycles()
        if cycles:
            lines.append(f"⚠️  检测到 {len(cycles)} 个循环依赖!")
        
        return "\n".join(lines)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将依赖图转换为字典格式
        
        Returns:
            包含所有节点和依赖关系的字典
        """
        return {
            "name": self.name,
            "nodes": {
                name: {
                    "dependencies": list(info.dependencies),
                    "dependents": list(info.dependents),
                    "metadata": info.metadata
                }
                for name, info in self._nodes.items()
            }
        }
    
    def to_json(self, indent: int = 2) -> str:
        """
        将依赖图转换为JSON字符串
        
        Args:
            indent: 缩进空格数
            
        Returns:
            JSON字符串
        """
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DependencyGraph":
        """
        从字典创建依赖图
        
        Args:
            data: 包含依赖图数据的字典
            
        Returns:
            DependencyGraph 实例
        """
        graph = cls(name=data.get("name", "DependencyGraph"))
        nodes_data = data.get("nodes", {})
        
        # 先添加所有节点
        for name in nodes_data:
            graph.add_node(name)
        
        # 再添加依赖关系
        for name, info in nodes_data.items():
            for dep in info.get("dependencies", []):
                graph.add_dependency(name, dep)
            if "metadata" in info:
                graph._nodes[name].metadata.update(info["metadata"])
        
        return graph
    
    @classmethod
    def from_json(cls, json_str: str) -> "DependencyGraph":
        """
        从JSON字符串创建依赖图
        
        Args:
            json_str: JSON格式字符串
            
        Returns:
            DependencyGraph 实例
        """
        return cls.from_dict(json.loads(json_str))
    
    def copy(self) -> "DependencyGraph":
        """
        创建依赖图的副本
        
        Returns:
            新的 DependencyGraph 实例
        """
        return DependencyGraph.from_dict(self.to_dict())
    
    def subgraph(self, nodes: List[str]) -> "DependencyGraph":
        """
        创建子图（只包含指定节点及其依赖）
        
        Args:
            nodes: 要包含的节点列表
            
        Returns:
            新的 DependencyGraph 子图
        """
        sub = DependencyGraph(name=f"{self.name}_subgraph")
        
        # 收集所有相关节点
        all_nodes = set(nodes)
        for node in nodes:
            if node in self._nodes:
                all_nodes.update(self.get_all_dependencies(node))
        
        # 添加节点和依赖
        for node in all_nodes:
            if node in self._nodes:
                info = self._nodes[node]
                sub.add_node(node, metadata=info.metadata.copy())
        
        for node in all_nodes:
            if node in self._nodes:
                for dep in self._nodes[node].dependencies:
                    if dep in all_nodes:
                        sub.add_dependency(node, dep)
        
        return sub


def topological_sort(
    dependencies: Dict[str, List[str]]
) -> List[str]:
    """
    拓扑排序快捷函数
    
    Args:
        dependencies: 依赖关系字典 {节点: [依赖列表]}
        
    Returns:
        排序后的节点列表
        
    Raises:
        CyclicDependencyError: 存在循环依赖
        
    示例:
        >>> deps = {"C": ["A", "B"], "B": ["A"], "A": []}
        >>> topological_sort(deps)
        ['A', 'B', 'C']
    """
    graph = DependencyGraph()
    
    for node, deps in dependencies.items():
        graph.add_node(node, dependencies=deps)
    
    result = graph.resolve()
    return result.order


def resolve_dependencies(
    dependencies: Dict[str, List[str]],
    allow_cycles: bool = False
) -> ResolutionResult:
    """
    解析依赖关系快捷函数
    
    Args:
        dependencies: 依赖关系字典 {节点: [依赖列表]}
        allow_cycles: 是否允许循环依赖
        
    Returns:
        ResolutionResult 对象
        
    示例:
        >>> deps = {"C": ["A", "B"], "B": ["A"], "A": []}
        >>> result = resolve_dependencies(deps)
        >>> print(result.levels)  # [['A'], ['B'], ['C']]
    """
    graph = DependencyGraph()
    
    for node, deps in dependencies.items():
        graph.add_node(node, dependencies=deps)
    
    return graph.resolve(allow_cycles=allow_cycles)


def find_cycles(
    dependencies: Dict[str, List[str]]
) -> List[List[str]]:
    """
    检测循环依赖快捷函数
    
    Args:
        dependencies: 依赖关系字典 {节点: [依赖列表]}
        
    Returns:
        循环路径列表
        
    示例:
        >>> deps = {"A": ["B"], "B": ["C"], "C": ["A"]}
        >>> find_cycles(deps)
        [['A', 'B', 'C', 'A']]
    """
    graph = DependencyGraph()
    
    for node, deps in dependencies.items():
        graph.add_node(node, dependencies=deps)
    
    return graph.detect_cycles()


# 便捷导出
__all__ = [
    "DependencyGraph",
    "ResolutionResult",
    "NodeInfo",
    "NodeType",
    "ResolutionError",
    "CyclicDependencyError",
    "MissingDependencyError",
    "topological_sort",
    "resolve_dependencies",
    "find_cycles",
]