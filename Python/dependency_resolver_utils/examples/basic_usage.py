"""
Dependency Resolver Utils 基础用法示例

演示依赖解析工具的基本使用方法。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dependency_resolver_utils.mod import (
    DependencyGraph,
    topological_sort,
    resolve_dependencies,
    find_cycles,
)


def example_basic_usage():
    """基础使用示例"""
    print("=== 基础使用 ===")
    
    # 创建依赖图
    graph = DependencyGraph(name="项目依赖")
    
    # 添加节点和依赖关系
    # D 依赖 B 和 C，B 依赖 A，C 依赖 A
    graph.add_node("A")
    graph.add_node("B", dependencies=["A"])
    graph.add_node("C", dependencies=["A"])
    graph.add_node("D", dependencies=["B", "C"])
    
    # 解析执行顺序
    result = graph.resolve()
    
    print(f"执行顺序: {result.order}")
    print(f"并行层级: {result.levels}")
    print(f"节点总数: {len(result.order)}")
    print()


def example_package_manager():
    """包管理器示例"""
    print("=== 包管理器依赖解析 ===")
    
    # 模拟包依赖关系
    packages = {
        "react": [],
        "react-dom": ["react"],
        "redux": [],
        "react-redux": ["react", "redux"],
        "typescript": [],
        "@types/react": ["react", "typescript"],
        "@types/react-dom": ["react-dom", "typescript"],
    }
    
    # 创建依赖图
    graph = DependencyGraph(name="npm依赖")
    for pkg, deps in packages.items():
        graph.add_node(pkg, dependencies=deps)
    
    # 获取安装顺序
    result = graph.resolve()
    
    print("推荐安装顺序:")
    for i, level in enumerate(result.levels, 1):
        print(f"  第{i}批(可并行): {', '.join(level)}")
    print()


def example_build_system():
    """构建系统示例"""
    print("=== 构建系统任务调度 ===")
    
    # 模拟构建任务依赖
    tasks = {
        "compile-core": [],
        "compile-utils": [],
        "compile-api": ["compile-core"],
        "compile-ui": ["compile-core", "compile-utils"],
        "test-core": ["compile-core"],
        "test-api": ["compile-api", "test-core"],
        "test-ui": ["compile-ui", "test-core"],
        "package": ["test-api", "test-ui"],
        "deploy": ["package"],
    }
    
    # 创建依赖图
    graph = DependencyGraph(name="构建任务")
    for task, deps in tasks.items():
        graph.add_node(task, dependencies=deps)
    
    # 解析并获取并行执行层级
    result = graph.resolve()
    
    print("构建执行计划:")
    for i, level in enumerate(result.levels, 1):
        print(f"  阶段 {i}: {' || '.join(level)}")
    print()
    
    # 查看根节点和叶节点
    print(f"起始任务: {graph.get_roots()}")
    print(f"最终任务: {graph.get_leaves()}")
    print()


def example_cycle_detection():
    """循环检测示例"""
    print("=== 循环依赖检测 ===")
    
    # 创建有循环依赖的图
    graph = DependencyGraph(name="循环依赖示例")
    graph.add_node("A", dependencies=["B"])
    graph.add_node("B", dependencies=["C"])
    graph.add_node("C", dependencies=["A"])  # 创建循环
    graph.add_node("D")  # 独立节点
    
    # 检测循环
    cycles = graph.detect_cycles()
    
    if cycles:
        print(f"检测到 {len(cycles)} 个循环:")
        for cycle in cycles:
            print(f"  循环路径: {' -> '.join(cycle)}")
    print()
    
    # 允许循环模式解析
    result = graph.resolve(allow_cycles=True)
    print(f"可解析的节点: {result.order}")
    print(f"循环中的节点: {set(result.cycles[0][:-1]) if result.cycles else set()}")
    print()


def example_convenience_functions():
    """便捷函数示例"""
    print("=== 便捷函数 ===")
    
    # 使用字典快速定义依赖
    deps = {
        "E": ["C", "D"],
        "D": ["B"],
        "C": ["A"],
        "B": ["A"],
        "A": [],
    }
    
    # 快速拓扑排序
    order = topological_sort(deps)
    print(f"拓扑排序结果: {order}")
    
    # 获取完整解析结果
    result = resolve_dependencies(deps)
    print(f"并行层级: {result.levels}")
    
    # 快速检测循环
    cycle_deps = {"A": ["B"], "B": ["C"], "C": ["A"]}
    cycles = find_cycles(cycle_deps)
    print(f"循环检测: {cycles}")
    print()


def example_subgraph():
    """子图示例"""
    print("=== 子图提取 ===")
    
    # 创建完整依赖图
    graph = DependencyGraph(name="完整系统")
    graph.add_node("config")
    graph.add_node("logger", dependencies=["config"])
    graph.add_node("database", dependencies=["config"])
    graph.add_node("cache", dependencies=["config"])
    graph.add_node("api", dependencies=["logger", "database"])
    graph.add_node("web", dependencies=["logger", "cache"])
    graph.add_node("scheduler", dependencies=["database"])
    graph.add_node("monitor", dependencies=["logger"])
    
    # 提取 web 模块相关的子图
    subgraph = graph.subgraph(["web"])
    
    print("web 模块及其依赖:")
    for node in subgraph:
        deps = subgraph.get_dependencies(node)
        if deps:
            print(f"  {node} <- {deps}")
        else:
            print(f"  {node} (根节点)")
    print()


def example_serialization():
    """序列化示例"""
    print("=== 序列化与反序列化 ===")
    
    # 创建依赖图
    graph = DependencyGraph(name="可序列化图")
    graph.add_node("base", metadata={"version": "1.0"})
    graph.add_node("core", dependencies=["base"], metadata={"version": "2.0"})
    graph.add_node("plugin", dependencies=["core"], metadata={"version": "1.5"})
    
    # 序列化为JSON
    json_str = graph.to_json()
    print("JSON表示:")
    print(json_str)
    print()
    
    # 从JSON恢复
    restored = DependencyGraph.from_json(json_str)
    print(f"恢复后节点数: {len(restored)}")
    print(f"执行顺序: {restored.get_execution_order()}")
    print()


def example_visualization():
    """可视化示例"""
    print("=== 依赖关系可视化 ===")
    
    graph = DependencyGraph(name="示例项目")
    graph.add_node("main")
    graph.add_node("utils", dependencies=["main"])
    graph.add_node("api", dependencies=["utils"])
    graph.add_node("ui", dependencies=["utils"])
    graph.add_node("test", dependencies=["api", "ui"])
    
    print(graph.visualize())
    print()


if __name__ == "__main__":
    example_basic_usage()
    example_package_manager()
    example_build_system()
    example_cycle_detection()
    example_convenience_functions()
    example_subgraph()
    example_serialization()
    example_visualization()