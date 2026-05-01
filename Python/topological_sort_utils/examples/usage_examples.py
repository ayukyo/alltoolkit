#!/usr/bin/env python3
"""
Topological Sort Utils 使用示例

展示拓扑排序在各种场景下的应用。
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Graph,
    TopologicalSorter,
    CycleDetectedError,
    topological_sort,
    detect_cycle,
    get_parallel_levels,
)


def example_basic_usage():
    """基础用法示例"""
    print("=" * 60)
    print("基础用法示例")
    print("=" * 60)
    
    # 创建图
    graph = Graph()
    graph.add_edges([
        ('A', 'B'),  # A -> B
        ('A', 'C'),  # A -> C
        ('B', 'D'),  # B -> D
        ('C', 'D'),  # C -> D
    ])
    
    print(f"\n图结构: {graph.node_count} 个节点, {graph.edge_count} 条边")
    
    # 创建排序器
    sorter = TopologicalSorter(graph)
    
    # Kahn 算法排序
    result = sorter.kahn_sort()
    print(f"\nKahn 算法排序结果: {' -> '.join(result)}")
    
    # DFS 排序
    result_dfs = sorter.dfs_sort()
    print(f"DFS 算法排序结果: {' -> '.join(result_dfs)}")


def example_task_scheduling():
    """任务调度示例"""
    print("\n" + "=" * 60)
    print("任务调度示例 - 构建系统")
    print("=" * 60)
    
    # 定义任务依赖
    # 任务名称 -> 依赖的任务列表
    tasks = {
        'base': [],          # 基础模块，无依赖
        'utils': ['base'],   # 工具模块，依赖基础
        'core': ['base'],    # 核心模块，依赖基础
        'api': ['core'],     # API 模块，依赖核心
        'web': ['utils', 'api'],  # Web 应用，依赖工具和 API
        'cli': ['core'],     # CLI 工具，依赖核心
        'tests': ['web', 'cli'],  # 测试，依赖所有模块
    }
    
    # 构建图
    graph = Graph()
    for task, deps in tasks.items():
        graph.add_node(task)
        for dep in deps:
            graph.add_edge(dep, task)
    
    sorter = TopologicalSorter(graph)
    
    # 获取并行执行层级
    levels = sorter.parallel_levels()
    
    print("\n任务执行计划（并行层级）:")
    for i, level in enumerate(levels):
        print(f"  第 {i} 层: {', '.join(level)} (可并行执行)")
    
    print("\n任务执行顺序:")
    order = sorter.kahn_sort()
    for i, task in enumerate(order, 1):
        print(f"  {i}. {task}")


def example_cycle_detection():
    """环检测示例"""
    print("\n" + "=" * 60)
    print("环检测示例 - 模块依赖循环")
    print("=" * 60)
    
    # 创建有环的依赖图
    graph = Graph()
    graph.add_edges([
        ('A', 'B'),  # A 依赖 B
        ('B', 'C'),  # B 依赖 C
        ('C', 'A'),  # C 依赖 A（形成环）
    ])
    
    sorter = TopologicalSorter(graph)
    
    # 检测环
    if sorter.has_cycle():
        print("\n⚠️  检测到依赖环！")
        cycle = sorter.find_cycle()
        if cycle:
            print(f"   环路径: {' -> '.join(cycle)}")
    else:
        print("\n✓ 无依赖环")
    
    # 尝试排序
    try:
        sorter.kahn_sort()
    except CycleDetectedError as e:
        print(f"   错误: {e}")


def example_course_prerequisites():
    """课程先修关系示例"""
    print("\n" + "=" * 60)
    print("课程先修关系示例 - 大学课程规划")
    print("=" * 60)
    
    # 课程先修关系
    prerequisites = [
        ('数学基础', '高等数学'),
        ('数学基础', '线性代数'),
        ('高等数学', '概率论'),
        ('高等数学', '数学分析'),
        ('线性代数', '机器学习'),
        ('概率论', '机器学习'),
        ('概率论', '统计学'),
        ('编程基础', '数据结构'),
        ('编程基础', '算法设计'),
        ('数据结构', '算法设计'),
        ('算法设计', '机器学习'),
    ]
    
    # 使用便捷函数快速排序
    order = topological_sort(prerequisites)
    
    print("\n推荐选课顺序:")
    for i, course in enumerate(order, 1):
        print(f"  第 {i} 学期: {course}")
    
    # 获取可以并行学习的课程
    levels = get_parallel_levels(prerequisites)
    
    print("\n可并行学习的课程组合:")
    for i, level in enumerate(levels):
        print(f"  阶段 {i + 1}: {', '.join(level)}")


def example_critical_path():
    """关键路径示例"""
    print("\n" + "=" * 60)
    print("关键路径示例 - 项目进度规划")
    print("=" * 60)
    
    # 项目任务（带工期）
    # 任务名称: (工期天数, 依赖任务列表)
    project = {
        '需求分析': (5, []),
        'UI设计': (10, ['需求分析']),
        '后端开发': (15, ['需求分析']),
        '前端开发': (12, ['UI设计']),
        '数据库设计': (3, ['需求分析']),
        'API开发': (8, ['后端开发', '数据库设计']),
        '前端集成': (7, ['前端开发', 'API开发']),
        '测试': (10, ['前端集成']),
        '部署': (2, ['测试']),
    }
    
    # 构建带权图
    graph = Graph()
    for task, (duration, deps) in project.items():
        graph.add_node(task, weight=duration)
        for dep in deps:
            graph.add_edge(dep, task)
    
    sorter = TopologicalSorter(graph)
    
    # 计算关键路径（最长路径）
    total_time, critical_path = sorter.longest_path_weighted()
    
    print(f"\n项目总工期: {total_time:.0f} 天")
    print(f"关键路径: {' -> '.join(critical_path)}")
    
    # 计算各任务的最早开始时间
    levels = sorter.parallel_levels()
    
    print("\n任务执行计划:")
    for i, level in enumerate(levels):
        print(f"  阶段 {i + 1}: {', '.join(level)}")


def example_package_installation():
    """包安装顺序示例"""
    print("\n" + "=" * 60)
    print("包安装顺序示例 - npm 风格依赖")
    print("=" * 60)
    
    # 包依赖关系（被依赖者 -> 依赖者）
    dependencies = [
        ('lodash', 'express'),
        ('debug', 'express'),
        ('cookie', 'express'),
        ('cookie-signature', 'cookie'),
        ('express', 'myapp'),
        ('body-parser', 'express'),
        ('mongoose', 'myapp'),
        ('mongodb', 'mongoose'),
    ]
    
    graph = Graph()
    graph.add_edges(dependencies)
    
    sorter = TopologicalSorter(graph)
    
    # 获取安装顺序（需要先安装依赖）
    install_order = sorter.kahn_sort()
    
    print("\n包安装顺序（先安装无依赖的包）:")
    for i, pkg in enumerate(install_order, 1):
        print(f"  {i}. npm install {pkg}")
    
    # 并行安装计划
    levels = sorter.parallel_levels()
    
    print("\n并行安装计划:")
    for i, level in enumerate(levels):
        pkgs = ' '.join(level)
        print(f"  批次 {i + 1}: npm install {pkgs}")


def example_docker_build():
    """Docker 镜像构建顺序示例"""
    print("\n" + "=" * 60)
    print("Docker 镜像构建顺序示例")
    print("=" * 60)
    
    # Docker 镜像依赖（基础镜像 -> 派生镜像）
    images = [
        ('ubuntu:20.04', 'python:3.9'),
        ('python:3.9', 'app-base'),
        ('app-base', 'app-api'),
        ('app-base', 'app-worker'),
        ('app-base', 'app-scheduler'),
        ('app-api', 'app-api-test'),
        ('redis:6', 'app-cache'),
        ('app-cache', 'app-worker'),
        ('nginx:latest', 'app-proxy'),
    ]
    
    graph = Graph()
    graph.add_edges(images)
    
    sorter = TopologicalSorter(graph)
    levels = sorter.parallel_levels()
    
    print("\nDocker 镜像构建计划:")
    for i, level in enumerate(levels):
        print(f"\n  构建批次 {i + 1}:")
        for image in level:
            print(f"    docker build -t {image} .")


def example_ancestor_descendant():
    """祖先和后代查询示例"""
    print("\n" + "=" * 60)
    print("依赖分析示例 - 影响范围查询")
    print("=" * 60)
    
    # 代码模块依赖
    dependencies = [
        ('core', 'utils'),
        ('core', 'logging'),
        ('utils', 'api'),
        ('utils', 'cli'),
        ('logging', 'api'),
        ('logging', 'cli'),
        ('api', 'web'),
        ('api', 'mobile'),
        ('cli', 'scripts'),
    ]
    
    graph = Graph()
    graph.add_edges(dependencies)
    
    sorter = TopologicalSorter(graph)
    
    # 查询修改 core 模块会影响哪些模块
    affected = sorter.descendants('core')
    print(f"\n修改 'core' 模块会影响: {', '.join(sorted(affected))}")
    
    # 查询 api 模块依赖哪些模块
    dependencies_of_api = sorter.ancestors('api')
    print(f"'api' 模块依赖: {', '.join(sorted(dependencies_of_api))}")
    
    # 查询修改 logging 会影响哪些模块
    affected_logging = sorter.descendants('logging')
    print(f"修改 'logging' 模块会影响: {', '.join(sorted(affected_logging))}")


def example_all_paths():
    """查找所有路径示例"""
    print("\n" + "=" * 60)
    print("路径查找示例 - 多种执行路径")
    print("=" * 60)
    
    # 工作流程
    workflow = [
        ('start', 'validate'),
        ('start', 'cache-check'),
        ('validate', 'process'),
        ('cache-check', 'process'),
        ('process', 'output'),
        ('process', 'notify'),
        ('output', 'end'),
        ('notify', 'end'),
    ]
    
    graph = Graph()
    graph.add_edges(workflow)
    
    sorter = TopologicalSorter(graph)
    
    # 查找从 start 到 end 的所有路径
    paths = sorter.all_paths('start', 'end')
    
    print(f"\n从 'start' 到 'end' 共有 {len(paths)} 条路径:")
    for i, path in enumerate(paths, 1):
        print(f"  路径 {i}: {' -> '.join(path)}")


def main():
    """运行所有示例"""
    example_basic_usage()
    example_task_scheduling()
    example_cycle_detection()
    example_course_prerequisites()
    example_critical_path()
    example_package_installation()
    example_docker_build()
    example_ancestor_descendant()
    example_all_paths()
    
    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()