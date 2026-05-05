#!/usr/bin/env python3
"""
Topological Sort Utilities 使用示例

演示如何使用拓扑排序工具解决实际问题：
1. 任务调度
2. 课程先修关系
3. 包依赖解析
4. 并行任务执行
5. 循环依赖检测
"""

from topological_sort import (
    TopologicalSort,
    topological_sort,
    detect_cycle,
    parallel_layers,
    CycleDetectedError
)


def example_1_task_scheduling():
    """
    示例1：任务调度
    
    场景：项目管理中的任务依赖
    """
    print("=" * 60)
    print("示例1：任务调度")
    print("=" * 60)
    
    ts = TopologicalSort()
    
    # 定义任务依赖关系
    # add_edge(A, B) 表示 A 依赖 B（B 必须先完成）
    ts.add_edge('前端开发', 'UI设计')
    ts.add_edge('后端开发', '数据库设计')
    ts.add_edge('后端开发', 'API设计')
    ts.add_edge('集成测试', '前端开发')
    ts.add_edge('集成测试', '后端开发')
    ts.add_edge('部署上线', '集成测试')
    ts.add_edge('部署上线', '安全审查')
    
    print("\n任务依赖关系：")
    print("  - 前端开发 依赖 UI设计")
    print("  - 后端开发 依赖 数据库设计、API设计")
    print("  - 集成测试 依赖 前端开发、后端开发")
    print("  - 部署上线 依赖 集成测试、安全审查")
    
    # 拓扑排序
    order = ts.sort()
    print(f"\n执行顺序: {' -> '.join(order)}")
    
    # 并行分层
    layers = ts.layers()
    print(f"\n并行执行计划（共 {len(layers)} 轮）：")
    for i, layer in enumerate(layers, 1):
        print(f"  第{i}轮: {', '.join(sorted(layer))}")
    
    print(f"\n最少需要 {ts.min_steps()} 轮完成所有任务")


def example_2_course_prerequisites():
    """
    示例2：课程先修关系
    
    场景：大学课程安排
    """
    print("\n" + "=" * 60)
    print("示例2：课程先修关系")
    print("=" * 60)
    
    # 使用便捷函数
    courses = [
        '微积分I', '微积分II', '线性代数', '概率论',
        '机器学习', '深度学习', '计算机视觉', '自然语言处理'
    ]
    
    # 先修关系：(课程, 先修课程)
    prerequisites = [
        ('微积分II', '微积分I'),
        ('线性代数', '微积分I'),
        ('概率论', '微积分II'),
        ('机器学习', '线性代数'),
        ('机器学习', '概率论'),
        ('深度学习', '机器学习'),
        ('计算机视觉', '深度学习'),
        ('自然语言处理', '深度学习'),
    ]
    
    print("\n先修关系：")
    for course, prereq in prerequisites:
        print(f"  - {course} 需要 {prereq}")
    
    order = topological_sort(courses, prerequisites)
    print(f"\n推荐修课顺序: {' -> '.join(order)}")
    
    # 查看哪些课程可以同时修
    layers = parallel_layers(courses, prerequisites)
    print(f"\n每学期可选课程：")
    for i, layer in enumerate(layers, 1):
        print(f"  学期{i}: {', '.join(sorted(layer))}")


def example_3_package_dependencies():
    """
    示例3：包依赖解析
    
    场景：类似 npm/pip 的依赖管理
    """
    print("\n" + "=" * 60)
    print("示例3：包依赖解析")
    print("=" * 60)
    
    ts = TopologicalSort()
    
    # 定义包依赖
    packages = {
        'react': ['loose-envify', 'object-assign'],
        'react-dom': ['react', 'scheduler'],
        'antd': ['react', 'react-dom', '@babel/runtime'],
        'my-app': ['react', 'react-dom', 'antd', 'axios'],
    }
    
    print("\n包依赖关系：")
    for pkg, deps in packages.items():
        for dep in deps:
            ts.add_edge(pkg, dep)
            print(f"  - {pkg} 依赖 {dep}")
    
    # 添加独立包
    for pkg in ['loose-envify', 'object-assign', 'scheduler', '@babel/runtime', 'axios']:
        ts.add_node(pkg)
    
    # 安装顺序
    install_order = ts.sort()
    print(f"\n安装顺序: {' -> '.join(install_order)}")
    
    # 查看某个包的所有依赖
    print(f"\n'my-app' 的所有依赖: {ts.get_all_dependencies('my-app')}")
    
    # 查看谁依赖某个包
    print(f"'react' 被依赖: {ts.get_dependents('react')}")


def example_4_parallel_execution():
    """
    示例4：并行任务执行
    
    场景：CI/CD 流水线
    """
    print("\n" + "=" * 60)
    print("示例4：并行任务执行（CI/CD流水线）")
    print("=" * 60)
    
    ts = TopologicalSort()
    
    # CI/CD 任务
    ts.add_edge('unit_test', 'checkout')
    ts.add_edge('lint', 'checkout')
    ts.add_edge('build', 'unit_test')
    ts.add_edge('build', 'lint')
    ts.add_edge('integration_test', 'build')
    ts.add_edge('e2e_test', 'build')
    ts.add_edge('deploy_staging', 'integration_test')
    ts.add_edge('deploy_staging', 'e2e_test')
    ts.add_edge('deploy_prod', 'deploy_staging')
    
    layers = ts.layers()
    print(f"\n并行执行计划：")
    for i, layer in enumerate(layers):
        print(f"  阶段{i}: {', '.join(sorted(layer))}")
    
    # 每个任务的并行层级
    levels = ts.parallel_levels()
    print(f"\n任务阶段分配：")
    for task in sorted(levels.keys()):
        print(f"  {task}: 阶段{levels[task]}")


def example_5_cycle_detection():
    """
    示例5：循环依赖检测
    
    场景：检测代码中的循环引用
    """
    print("\n" + "=" * 60)
    print("示例5：循环依赖检测")
    print("=" * 60)
    
    # 场景1：无循环
    print("\n场景1：正常的依赖关系")
    ts1 = TopologicalSort()
    ts1.add_edge('module_a', 'module_b')
    ts1.add_edge('module_b', 'module_c')
    ts1.add_edge('module_c', 'module_d')
    
    if not ts1.has_cycle():
        print("  ✓ 无循环依赖")
        print(f"  加载顺序: {' -> '.join(ts1.sort())}")
    
    # 场景2：有循环
    print("\n场景2：存在循环依赖")
    ts2 = TopologicalSort()
    ts2.add_edge('module_a', 'module_b')
    ts2.add_edge('module_b', 'module_c')
    ts2.add_edge('module_c', 'module_a')  # 循环！
    
    cycle = ts2.get_cycle()
    if cycle:
        print(f"  ✗ 检测到循环: {' -> '.join(cycle)}")
    
    # 使用便捷函数
    print("\n场景3：使用便捷函数检测")
    nodes = ['A', 'B', 'C', 'D']
    edges = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'B')]
    
    cycle = detect_cycle(nodes, edges)
    if cycle:
        print(f"  ✗ 发现循环依赖: {' -> '.join(cycle)}")


def example_6_critical_path():
    """
    示例6：关键路径分析
    
    场景：项目管理中的最长路径
    """
    print("\n" + "=" * 60)
    print("示例6：关键路径分析")
    print("=" * 60)
    
    ts = TopologicalSort()
    
    # 项目任务链
    ts.add_edge('需求分析', '项目启动')
    ts.add_edge('架构设计', '需求分析')
    ts.add_edge('UI设计', '需求分析')
    ts.add_edge('前端开发', 'UI设计')
    ts.add_edge('后端开发', '架构设计')
    ts.add_edge('测试', '前端开发')
    ts.add_edge('测试', '后端开发')
    ts.add_edge('部署', '测试')
    
    path, length = ts.critical_path()
    print(f"\n关键路径: {' -> '.join(path)}")
    print(f"关键路径长度: {length} 个任务")
    
    print(f"\n项目最少需要 {ts.min_steps()} 个阶段完成")


def example_7_build_system():
    """
    示例7：构建系统
    
    场景：Makefile 风格的文件依赖
    """
    print("\n" + "=" * 60)
    print("示例7：构建系统（Makefile风格）")
    print("=" * 60)
    
    ts = TopologicalSort()
    
    # 文件依赖关系
    # add_edge(target, dependency)
    ts.add_edge('main.o', 'main.c')
    ts.add_edge('main.o', 'utils.h')
    ts.add_edge('utils.o', 'utils.c')
    ts.add_edge('utils.o', 'utils.h')
    ts.add_edge('parser.o', 'parser.c')
    ts.add_edge('parser.o', 'parser.h')
    ts.add_edge('app', 'main.o')
    ts.add_edge('app', 'utils.o')
    ts.add_edge('app', 'parser.o')
    
    print("\n文件依赖关系：")
    for target in ['app', 'main.o', 'utils.o', 'parser.o']:
        deps = ts.get_dependencies(target)
        if deps:
            print(f"  {target}: {', '.join(sorted(deps))}")
    
    # 构建顺序
    build_order = ts.sort()
    print(f"\n构建顺序: {' -> '.join(build_order)}")
    
    # 增量构建：找出需要重新编译的文件
    print("\n如果 'utils.h' 被修改，需要重新编译：")
    affected = ts.get_dependents('utils.h')
    affected.add('utils.h')
    print(f"  {', '.join(sorted(affected))}")


def example_8_graph_operations():
    """
    示例8：图操作
    
    场景：图的变换和合并
    """
    print("\n" + "=" * 60)
    print("示例8：图操作")
    print("=" * 60)
    
    # 创建图
    ts = TopologicalSort()
    ts.add_edge('B', 'A')
    ts.add_edge('C', 'B')
    
    print(f"\n原图: {ts}")
    print(f"  节点数: {ts.node_count}")
    print(f"  边数: {ts.edge_count}")
    
    # 反向图
    reversed_ts = ts.reverse()
    print(f"\n反向图:")
    print(f"  排序结果: {' -> '.join(reversed_ts.sort())}")
    
    # 拷贝
    copied = ts.copy()
    copied.add_edge('D', 'C')
    print(f"\n拷贝后添加节点:")
    print(f"  原图边数: {ts.edge_count}")
    print(f"  新图边数: {copied.edge_count}")
    
    # 合并
    ts1 = TopologicalSort()
    ts1.add_edge('A', 'B')
    
    ts2 = TopologicalSort()
    ts2.add_edge('C', 'D')
    
    merged = ts1.merge(ts2)
    print(f"\n合并图:")
    print(f"  节点数: {merged.node_count}")
    print(f"  边数: {merged.edge_count}")


def example_9_validation():
    """
    示例9：验证排序结果
    
    场景：检查给定顺序是否有效
    """
    print("\n" + "=" * 60)
    print("示例9：验证排序结果")
    print("=" * 60)
    
    ts = TopologicalSort()
    ts.add_edge('A', 'B')
    ts.add_edge('B', 'C')
    ts.add_edge('C', 'D')
    
    valid_order = ['D', 'C', 'B', 'A']
    invalid_order = ['A', 'B', 'C', 'D']
    
    print(f"\n依赖关系: A -> B -> C -> D")
    print(f"  排序 '{valid_order}' 有效: {ts.is_valid_order(valid_order)}")
    print(f"  排序 '{invalid_order}' 有效: {ts.is_valid_order(invalid_order)}")


def example_10_dynamic_updates():
    """
    示例10：动态更新依赖关系
    
    场景：运行时修改依赖图
    """
    print("\n" + "=" * 60)
    print("示例10：动态更新依赖关系")
    print("=" * 60)
    
    ts = TopologicalSort()
    ts.add_edge('A', 'B')
    ts.add_edge('B', 'C')
    
    print("初始状态:")
    print(f"  排序: {' -> '.join(ts.sort())}")
    
    # 添加新依赖
    print("\n添加新依赖: A -> D")
    ts.add_edge('A', 'D')
    print(f"  排序: {' -> '.join(ts.sort())}")
    
    # 移除依赖
    print("\n移除依赖: A -> B")
    ts.remove_edge('A', 'B')
    print(f"  排序: {' -> '.join(ts.sort())}")
    
    # 移除节点
    print("\n移除节点: B")
    ts.remove_node('B')
    print(f"  排序: {' -> '.join(ts.sort())}")
    print(f"  剩余节点: {sorted(ts)}")


if __name__ == '__main__':
    example_1_task_scheduling()
    example_2_course_prerequisites()
    example_3_package_dependencies()
    example_4_parallel_execution()
    example_5_cycle_detection()
    example_6_critical_path()
    example_7_build_system()
    example_8_graph_operations()
    example_9_validation()
    example_10_dynamic_updates()
    
    print("\n" + "=" * 60)
    print("所有示例完成！")
    print("=" * 60)