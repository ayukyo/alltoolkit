"""
图着色工具 - 使用示例
Graph Coloring Utils - Usage Examples

图着色是图论中的经典问题，广泛应用于：
- 课程表安排（避免冲突）
- 寄存器分配（编译器优化）
- 地图着色（相邻区域不同色）
- 频率分配（无线通信）
- 任务调度（资源冲突）
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from graph_coloring_utils.mod import (
    Graph, greedy_coloring, welsh_powell_coloring, dsatur_coloring,
    backtracking_coloring, is_valid_coloring, count_colors,
    get_color_groups, chromatic_number_bounds, find_coloring,
    compare_algorithms, IntervalGraph, BipartiteChecker
)


def example_basic_coloring():
    """示例1: 基本图着色"""
    print("=" * 60)
    print("示例1: 基本图着色")
    print("=" * 60)
    
    # 创建一个简单的图
    graph = Graph()
    edges = [
        ("北京", "上海"), ("北京", "广州"), ("北京", "深圳"),
        ("上海", "杭州"), ("上海", "南京"),
        ("广州", "深圳"), ("广州", "杭州"),
        ("深圳", "南京")
    ]
    
    for v1, v2 in edges:
        graph.add_edge(v1, v2)
    
    print(f"图信息: {len(graph.vertices)} 个城市, {len(graph.edges)} 条航线")
    print()
    
    # 使用不同算法着色
    print("--- 贪心算法 ---")
    coloring = greedy_coloring(graph)
    print(f"使用颜色数: {count_colors(coloring)}")
    print(f"着色方案: {coloring}")
    print()
    
    print("--- Welsh-Powell 算法 ---")
    coloring = welsh_powell_coloring(graph)
    print(f"使用颜色数: {count_colors(coloring)}")
    print(f"着色方案: {coloring}")
    print()
    
    print("--- DSatur 算法 ---")
    coloring = dsatur_coloring(graph)
    print(f"使用颜色数: {count_colors(coloring)}")
    print(f"着色方案: {coloring}")
    print()


def example_course_scheduling():
    """示例2: 课程表安排问题"""
    print("=" * 60)
    print("示例2: 课程表安排问题")
    print("=" * 60)
    
    # 使用区间图解决课程安排
    interval_graph = IntervalGraph()
    
    # 添加课程时间段
    courses = [
        ("高等数学", 8, 10),
        ("线性代数", 9, 11),
        ("概率统计", 10, 12),
        ("大学英语", 8, 9),
        ("大学物理", 11, 13),
        ("程序设计", 13, 15),
        ("数据结构", 14, 16),
        ("算法分析", 15, 17),
    ]
    
    for name, start, end in courses:
        interval_graph.add_interval(name, start, end)
    
    # 获取最优着色
    coloring = interval_graph.optimal_coloring()
    rooms_needed = count_colors(coloring)
    
    print(f"需要 {rooms_needed} 间教室来安排所有课程")
    print()
    
    # 按教室分组显示
    groups = get_color_groups(coloring)
    for room_id in sorted(groups.keys()):
        courses_in_room = groups[room_id]
        print(f"教室 {room_id + 1}: {', '.join(courses_in_room)}")
    
    print()


def example_map_coloring():
    """示例3: 地图着色问题"""
    print("=" * 60)
    print("示例3: 地图着色问题")
    print("=" * 60)
    
    # 中国部分省份相邻关系（简化版）
    provinces = [
        ("北京", "天津"),
        ("北京", "河北"),
        ("天津", "河北"),
        ("河北", "山东"),
        ("河北", "河南"),
        ("河北", "山西"),
        ("山东", "河南"),
        ("河南", "山西"),
        ("山西", "陕西"),
        ("河南", "陕西"),
        ("山东", "江苏"),
        ("江苏", "安徽"),
        ("江苏", "浙江"),
        ("浙江", "安徽"),
        ("安徽", "河南"),
    ]
    
    graph = Graph.from_edges(provinces)
    
    print(f"地图包含 {len(graph.vertices)} 个省份")
    print()
    
    # 使用 DSatur 算法着色
    coloring = dsatur_coloring(graph)
    colors_used = count_colors(coloring)
    
    print(f"需要 {colors_used} 种颜色（地图四色定理保证 ≤4）")
    print()
    
    # 显示各省颜色
    color_names = ["红色", "蓝色", "绿色", "黄色", "紫色"]
    for province in sorted(coloring.keys()):
        color = coloring[province]
        color_name = color_names[color] if color < len(color_names) else f"颜色{color+1}"
        print(f"  {province}: {color_name}")
    
    print()


def example_bipartite_check():
    """示例4: 二分图检测"""
    print("=" * 60)
    print("示例4: 二分图检测")
    print("=" * 60)
    
    # 任务分配问题：工人和任务
    workers = ["工人A", "工人B", "工人C"]
    tasks = ["任务1", "任务2", "任务3", "任务4"]
    
    graph = Graph()
    
    # 工人可以做的任务
    assignments = [
        ("工人A", "任务1"), ("工人A", "任务2"),
        ("工人B", "任务2"), ("工人B", "任务3"),
        ("工人C", "任务3"), ("工人C", "任务4"),
    ]
    
    for w, t in assignments:
        graph.add_edge(w, t)
    
    is_bip, two_coloring = BipartiteChecker.is_bipartite(graph)
    
    print(f"是否为二分图: {is_bip}")
    
    if is_bip:
        print("二着色方案:")
        group_a = [v for v, c in two_coloring.items() if c == 0]
        group_b = [v for v, c in two_coloring.items() if c == 1]
        print(f"  组1: {group_a}")
        print(f"  组2: {group_b}")
    
    print()


def example_algorithm_comparison():
    """示例5: 算法性能比较"""
    print("=" * 60)
    print("示例5: 算法性能比较")
    print("=" * 60)
    
    # 创建一个中等复杂度的图
    edges = []
    # 生成一个随机-ish 的图结构
    for i in range(15):
        for j in range(i + 1, 15):
            if (i + j) % 3 == 0 or (i * j) % 7 < 2:
                edges.append((f"V{i}", f"V{j}"))
    
    graph = Graph.from_edges(edges)
    
    print(f"测试图: {len(graph.vertices)} 个顶点, {len(graph.edges)} 条边")
    print()
    
    import time
    
    results = {}
    
    # 贪心
    start = time.time()
    g = greedy_coloring(graph)
    results["贪心"] = (count_colors(g), time.time() - start)
    
    # Welsh-Powell
    start = time.time()
    w = welsh_powell_coloring(graph)
    results["Welsh-Powell"] = (count_colors(w), time.time() - start)
    
    # DSatur
    start = time.time()
    d = dsatur_coloring(graph)
    results["DSatur"] = (count_colors(d), time.time() - start)
    
    # 回溯（可能较慢，限制最大颜色数）
    start = time.time()
    b = backtracking_coloring(graph, max_colors=5)
    bt_colors = count_colors(b) if b else "N/A"
    results["回溯"] = (bt_colors, time.time() - start)
    
    print(f"{'算法':<15} {'颜色数':<10} {'耗时':<15}")
    print("-" * 40)
    for name, (colors, t) in results.items():
        print(f"{name:<15} {colors:<10} {t:.6f}s")
    
    print()


def example_network_frequency():
    """示例6: 无线网络频率分配"""
    print("=" * 60)
    print("示例6: 无线网络频率分配")
    print("=" * 60)
    
    # 假设有多个无线接入点，相邻的需要不同频率
    access_points = Graph.from_edges([
        ("AP1", "AP2"), ("AP1", "AP3"), ("AP1", "AP4"),
        ("AP2", "AP3"), ("AP2", "AP5"),
        ("AP3", "AP4"), ("AP3", "AP5"), ("AP3", "AP6"),
        ("AP4", "AP6"),
        ("AP5", "AP6"), ("AP5", "AP7"),
        ("AP6", "AP7"),
    ])
    
    print(f"网络包含 {len(access_points.vertices)} 个接入点")
    print(f"相邻约束: {len(access_points.edges)} 对")
    print()
    
    # 使用 DSatur 算法分配频率
    coloring = dsatur_coloring(access_points)
    frequencies = count_colors(coloring)
    
    # 频率信道映射
    freq_channels = {
        0: "信道 1 (2.412 GHz)",
        1: "信道 6 (2.437 GHz)",
        2: "信道 11 (2.462 GHz)",
        3: "信道 36 (5.180 GHz)",
        4: "信道 52 (5.260 GHz)",
    }
    
    print(f"需要 {frequencies} 个不同信道避免干扰")
    print()
    print("频率分配方案:")
    for ap in sorted(coloring.keys()):
        color = coloring[ap]
        channel = freq_channels.get(color, f"信道 {color+1}")
        print(f"  {ap}: {channel}")
    
    print()


def example_scheduler():
    """示例7: 任务调度问题"""
    print("=" * 60)
    print("示例7: 任务调度问题")
    print("=" * 60)
    
    # 有依赖关系的任务
    tasks = Graph.from_edges([
        ("需求分析", "系统设计"),
        ("需求分析", "UI设计"),
        ("系统设计", "后端开发"),
        ("系统设计", "数据库设计"),
        ("UI设计", "前端开发"),
        ("数据库设计", "后端开发"),
        ("后端开发", "测试"),
        ("前端开发", "测试"),
        ("测试", "部署"),
    ])
    
    print("软件开发任务依赖关系:")
    print()
    
    # 这里我们用反向图来调度：没有依赖的任务可以并行
    # 先计算各任务的"层级"
    levels = {}
    remaining = set(tasks.vertices)
    
    while remaining:
        # 找到没有未处理依赖的任务
        ready = set()
        for task in remaining:
            deps = tasks.get_neighbors(task)
            if not (deps & remaining):
                ready.add(task)
        
        level = len(levels)
        for task in ready:
            levels[task] = level
            remaining.remove(task)
    
    print("可并行执行的任务层级:")
    max_level = max(levels.values()) if levels else 0
    for l in range(max_level + 1):
        tasks_at_level = [t for t, lv in levels.items() if lv == l]
        print(f"  阶段 {l + 1}: {', '.join(tasks_at_level)}")
    
    print(f"\n最少需要 {max_level + 1} 个阶段完成所有任务")
    print()


def example_graph_structures():
    """示例8: 特殊图结构"""
    print("=" * 60)
    print("示例8: 特殊图结构")
    print("=" * 60)
    
    # 完全图 K5
    k5 = Graph.create_complete(5)
    print(f"完全图 K5:")
    print(f"  顶点数: {len(k5.vertices)}")
    print(f"  边数: {len(k5.edges)}")
    coloring = greedy_coloring(k5)
    print(f"  着色数: {count_colors(coloring)} (理论值: 5)")
    print()
    
    # 环图 C6
    c6 = Graph.create_cycle(6)
    print(f"环图 C6:")
    print(f"  顶点数: {len(c6.vertices)}")
    print(f"  边数: {len(c6.edges)}")
    coloring = dsatur_coloring(c6)
    print(f"  着色数: {count_colors(coloring)} (理论值: 2, 偶环)")
    is_bip, _ = BipartiteChecker.is_bipartite(c6)
    print(f"  是否二分图: {is_bip}")
    print()
    
    # 环图 C5
    c5 = Graph.create_cycle(5)
    print(f"环图 C5:")
    print(f"  顶点数: {len(c5.vertices)}")
    coloring = dsatur_coloring(c5)
    print(f"  着色数: {count_colors(coloring)} (理论值: 3, 奇环)")
    is_bip, _ = BipartiteChecker.is_bipartite(c5)
    print(f"  是否二分图: {is_bip}")
    print()
    
    # 网格图
    grid = Graph.create_grid(4, 4)
    print(f"网格图 4x4:")
    print(f"  顶点数: {len(grid.vertices)}")
    print(f"  边数: {len(grid.edges)}")
    coloring = dsatur_coloring(grid)
    print(f"  着色数: {count_colors(coloring)} (理论值: 2, 网格图是二分图)")
    is_bip, _ = BipartiteChecker.is_bipartite(grid)
    print(f"  是否二分图: {is_bip}")
    print()


def run_all_examples():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("图着色工具 - 完整使用示例")
    print("=" * 60 + "\n")
    
    example_basic_coloring()
    example_course_scheduling()
    example_map_coloring()
    example_bipartite_check()
    example_algorithm_comparison()
    example_network_frequency()
    example_scheduler()
    example_graph_structures()
    
    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()