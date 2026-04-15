"""
Dependency Resolver Utils 高级用法示例

演示更复杂的依赖解析场景。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dependency_resolver_utils.mod import (
    DependencyGraph,
    CyclicDependencyError,
    resolve_dependencies,
)


def example_module_loader():
    """模块加载器示例"""
    print("=== 模块加载器模拟 ===")
    
    # 模拟模块依赖关系
    modules = {
        "core": [],
        "events": ["core"],
        "config": ["core"],
        "logger": ["core", "config"],
        "database": ["core", "config", "logger"],
        "cache": ["core", "config"],
        "auth": ["core", "database", "cache", "logger"],
        "api": ["auth", "logger", "events"],
        "web": ["api", "auth"],
        "cli": ["core", "config", "logger"],
    }
    
    graph = DependencyGraph(name="模块系统")
    for mod, deps in modules.items():
        graph.add_node(mod, dependencies=deps, metadata={"loaded": False})
    
    # 获取加载顺序
    result = graph.resolve()
    
    print("模块加载顺序:")
    for i, level in enumerate(result.levels, 1):
        print(f"  批次 {i}: {', '.join(sorted(level))}")
    print()
    
    # 分析模块关系
    print("模块分析:")
    print(f"  核心模块(根节点): {graph.get_roots()}")
    print(f"  终端模块(叶节点): {graph.get_leaves()}")
    print()
    
    # 查看模块的所有依赖
    print("api 模块的所有依赖:")
    all_deps = graph.get_all_dependencies("api")
    print(f"  {all_deps}")
    print()


def example_microservices():
    """微服务启动顺序示例"""
    print("=== 微服务启动顺序 ===")
    
    # 定义微服务依赖关系
    services = {
        "service-registry": [],
        "config-server": [],
        "api-gateway": ["service-registry"],
        "auth-service": ["service-registry", "config-server"],
        "user-service": ["service-registry", "auth-service"],
        "order-service": ["service-registry", "auth-service", "user-service"],
        "payment-service": ["service-registry", "auth-service", "user-service"],
        "notification-service": ["service-registry", "user-service"],
        "inventory-service": ["service-registry", "order-service"],
        "frontend": ["api-gateway", "auth-service"],
    }
    
    graph = DependencyGraph(name="微服务架构")
    for svc, deps in services.items():
        graph.add_node(svc, dependencies=deps)
    
    result = graph.resolve()
    
    print("服务启动计划:")
    for i, level in enumerate(result.levels, 1):
        print(f"\n  阶段 {i} (可并行启动):")
        for svc in sorted(level):
            deps = graph.get_dependencies(svc)
            dep_str = f" (依赖: {', '.join(sorted(deps))})" if deps else ""
            print(f"    - {svc}{dep_str}")
    print()


def example_plugin_system():
    """插件系统示例"""
    print("=== 插件依赖管理 ===")
    
    # 定义插件依赖
    plugins = {
        "base-plugin": [],
        "logging-plugin": ["base-plugin"],
        "security-plugin": ["base-plugin"],
        "database-plugin": ["base-plugin", "logging-plugin"],
        "auth-plugin": ["security-plugin", "database-plugin"],
        "api-plugin": ["auth-plugin", "logging-plugin"],
        "admin-plugin": ["api-plugin", "auth-plugin"],
        "reporting-plugin": ["database-plugin", "logging-plugin"],
    }
    
    graph = DependencyGraph(name="插件系统")
    for plugin, deps in plugins.items():
        graph.add_node(plugin, dependencies=deps, metadata={"enabled": True})
    
    # 检查循环依赖
    cycles = graph.detect_cycles()
    if cycles:
        print("警告: 检测到循环依赖!")
        for cycle in cycles:
            print(f"  {cycle}")
    else:
        print("依赖检查通过!")
    print()
    
    # 获取插件加载顺序
    result = graph.resolve()
    print(f"插件加载顺序: {' -> '.join(result.order)}")
    print()
    
    # 模拟禁用某个插件后重新计算
    print("模拟禁用 auth-plugin:")
    subgraph = graph.subgraph([p for p in plugins if p != "auth-plugin"])
    affected = graph.get_all_dependents("auth-plugin")
    print(f"  受影响的插件: {affected}")
    print()


def example_ci_pipeline():
    """CI/CD 流水线示例"""
    print("=== CI/CD 流水线依赖 ===")
    
    # 定义流水线阶段
    stages = {
        "checkout": [],
        "install-deps": ["checkout"],
        "lint": ["install-deps"],
        "type-check": ["install-deps"],
        "unit-test": ["install-deps"],
        "integration-test": ["unit-test"],
        "e2e-test": ["integration-test"],
        "build": ["lint", "type-check", "unit-test"],
        "docker-build": ["build"],
        "security-scan": ["docker-build"],
        "deploy-staging": ["docker-build", "integration-test"],
        "deploy-production": ["deploy-staging", "security-scan", "e2e-test"],
    }
    
    graph = DependencyGraph(name="CI/CD流水线")
    for stage, deps in stages.items():
        graph.add_node(stage, dependencies=deps)
    
    result = graph.resolve()
    
    print("流水线执行计划:")
    for i, level in enumerate(result.levels, 1):
        print(f"  阶段 {i}: {' | '.join(sorted(level))}")
    print()
    
    # 计算关键路径
    print("关键路径分析:")
    leaves = graph.get_leaves()
    for leaf in leaves:
        all_deps = graph.get_all_dependencies(leaf)
        print(f"  {leaf} 需要经过 {len(all_deps)} 个前置步骤")
    print()


def example_dynamic_dependency():
    """动态依赖管理示例"""
    print("=== 动态依赖管理 ===")
    
    graph = DependencyGraph(name="动态系统")
    
    # 初始依赖
    graph.add_node("A")
    graph.add_node("B", dependencies=["A"])
    graph.add_node("C", dependencies=["A"])
    
    print("初始状态:")
    print(f"  执行顺序: {graph.get_execution_order()}")
    print()
    
    # 动态添加新依赖
    print("添加 D 依赖 B 和 C:")
    graph.add_node("D", dependencies=["B", "C"])
    print(f"  新执行顺序: {graph.get_execution_order()}")
    print()
    
    # 动态移除依赖
    print("移除 D 对 B 的依赖:")
    graph.remove_dependency("D", "B")
    print(f"  新执行顺序: {graph.get_execution_order()}")
    print()
    
    # 动态添加新的依赖关系
    print("添加 E 依赖 D:")
    graph.add_node("E", dependencies=["D"])
    levels = graph.get_parallel_levels()
    print(f"  并行层级: {levels}")
    print()


def example_error_handling():
    """错误处理示例"""
    print("=== 错误处理 ===")
    
    # 循环依赖错误
    print("处理循环依赖:")
    graph = DependencyGraph(name="循环示例")
    graph.add_node("X", dependencies=["Y"])
    graph.add_node("Y", dependencies=["Z"])
    graph.add_node("Z", dependencies=["X"])
    
    try:
        graph.resolve()
    except CyclicDependencyError as e:
        print(f"  错误: {e}")
        
        # 优雅处理：允许循环继续
        result = graph.resolve(allow_cycles=True)
        print(f"  可解析的节点: {result.order}")
        print(f"  循环节点: {set(result.cycles[0][:-1])}")
    print()


def example_batch_processing():
    """批量处理优化示例"""
    print("=== 批量处理优化 ===")
    
    # 模拟数据处理任务依赖
    tasks = {}
    
    # 创建复杂的依赖网络
    for i in range(10):
        task_name = f"task_{i:02d}"
        deps = []
        if i > 0:
            deps.append(f"task_{i-1:02d}")
        if i > 2:
            deps.append(f"task_{i-3:02d}")
        tasks[task_name] = deps
    
    result = resolve_dependencies(tasks)
    
    print(f"总任务数: {len(tasks)}")
    print(f"并行批次数: {len(result.levels)}")
    print()
    
    # 找出最大并行批次
    max_batch = max(result.levels, key=len)
    print(f"最大并行批次大小: {len(max_batch)}")
    print(f"任务: {max_batch}")
    print()
    
    # 计算理论加速比
    sequential_time = len(tasks)
    parallel_time = len(result.levels)
    speedup = sequential_time / parallel_time
    print(f"理论加速比: {speedup:.2f}x")
    print()


def example_dependency_analysis():
    """依赖分析示例"""
    print("=== 依赖分析 ===")
    
    graph = DependencyGraph(name="分析示例")
    graph.add_node("foundation")
    graph.add_node("logging", dependencies=["foundation"])
    graph.add_node("config", dependencies=["foundation"])
    graph.add_node("database", dependencies=["foundation", "config"])
    graph.add_node("cache", dependencies=["foundation", "config"])
    graph.add_node("api", dependencies=["database", "cache", "logging"])
    graph.add_node("web", dependencies=["api", "logging"])
    graph.add_node("cli", dependencies=["database", "config"])
    
    # 分析特定模块
    target = "web"
    print(f"分析模块: {target}")
    print()
    
    # 所有依赖
    all_deps = graph.get_all_dependencies(target)
    print(f"所有依赖 ({len(all_deps)}):")
    print(f"  {sorted(all_deps)}")
    print()
    
    # 所有被依赖
    all_dependents = graph.get_all_dependents("foundation")
    print(f"'foundation' 被依赖 ({len(all_dependents)}):")
    print(f"  {sorted(all_dependents)}")
    print()
    
    # 直接依赖
    direct_deps = graph.get_dependencies(target)
    print(f"直接依赖:")
    print(f"  {sorted(direct_deps)}")
    print()
    
    # 可视化
    print("依赖关系图:")
    print(graph.visualize())


if __name__ == "__main__":
    example_module_loader()
    example_microservices()
    example_plugin_system()
    example_ci_pipeline()
    example_dynamic_dependency()
    example_error_handling()
    example_batch_processing()
    example_dependency_analysis()