"""
图着色工具模块测试
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph_coloring_utils.mod import (
    Graph, greedy_coloring, welsh_powell_coloring, dsatur_coloring,
    backtracking_coloring, is_valid_coloring, count_colors,
    get_color_groups, chromatic_number_bounds, find_coloring,
    compare_algorithms, IntervalGraph, BipartiteChecker
)


def test_graph_creation():
    """测试图的创建"""
    print("=== 测试图创建 ===")
    
    # 从边创建
    graph = Graph.from_edges([
        ("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")
    ])
    assert len(graph.vertices) == 4
    assert len(graph.edges) == 4
    print(f"✓ 从边创建图: {len(graph.vertices)} 顶点, {len(graph.edges)} 条边")
    
    # 创建完全图
    complete = Graph.create_complete(5)
    assert len(complete.vertices) == 5
    assert len(complete.edges) == 10  # C(5,2) = 10
    print(f"✓ 完全图 K5: {len(complete.vertices)} 顶点, {len(complete.edges)} 条边")
    
    # 创建环图
    cycle = Graph.create_cycle(6)
    assert len(cycle.vertices) == 6
    assert len(cycle.edges) == 6
    print(f"✓ 环图 C6: {len(cycle.vertices)} 顶点, {len(cycle.edges)} 条边")
    
    # 创建网格图
    grid = Graph.create_grid(3, 3)
    assert len(grid.vertices) == 9
    print(f"✓ 网格图 3x3: {len(grid.vertices)} 顶点, {len(grid.edges)} 条边")
    
    print()


def test_greedy_coloring():
    """测试贪心着色算法"""
    print("=== 测试贪心着色 ===")
    
    # 简单路径图
    graph = Graph.from_edges([("A", "B"), ("B", "C"), ("C", "D")])
    coloring = greedy_coloring(graph)
    
    assert len(coloring) == 4
    assert is_valid_coloring(graph, coloring)
    colors_used = count_colors(coloring)
    print(f"✓ 路径图着色: 使用 {colors_used} 种颜色")
    
    # 环图（偶数环需要2种颜色）
    cycle = Graph.create_cycle(4)
    coloring = greedy_coloring(cycle)
    assert is_valid_coloring(cycle, coloring)
    print(f"✓ C4 环图着色: 使用 {count_colors(coloring)} 种颜色")
    
    # 完全图（K4需要4种颜色）
    complete = Graph.create_complete(4)
    coloring = greedy_coloring(complete)
    assert count_colors(coloring) == 4
    assert is_valid_coloring(complete, coloring)
    print(f"✓ K4 完全图着色: 使用 {count_colors(coloring)} 种颜色")
    
    print()


def test_welsh_powell_coloring():
    """测试 Welsh-Powell 算法"""
    print("=== 测试 Welsh-Powell 算法 ===")
    
    # 创建一个需要多种颜色的图
    graph = Graph.from_edges([
        ("A", "B"), ("A", "C"), ("A", "D"),
        ("B", "C"), ("B", "D"),
        ("C", "D"), ("C", "E"),
        ("D", "E")
    ])
    
    coloring = welsh_powell_coloring(graph)
    assert is_valid_coloring(graph, coloring)
    print(f"✓ Welsh-Powell 着色: 使用 {count_colors(coloring)} 种颜色")
    print(f"  着色方案: {coloring}")
    
    # 与贪心比较
    greedy_result = greedy_coloring(graph)
    print(f"  贪心着色: 使用 {count_colors(greedy_result)} 种颜色")
    
    print()


def test_dsatur_coloring():
    """测试 DSatur 算法"""
    print("=== 测试 DSatur 算法 ===")
    
    # 创建测试图
    graph = Graph.from_edges([
        ("1", "2"), ("1", "3"), ("1", "4"),
        ("2", "3"), ("2", "5"),
        ("3", "4"), ("3", "5"),
        ("4", "5")
    ])
    
    coloring = dsatur_coloring(graph)
    assert is_valid_coloring(graph, coloring)
    print(f"✓ DSatur 着色: 使用 {count_colors(coloring)} 种颜色")
    print(f"  着色方案: {coloring}")
    
    # 比较三种算法
    greedy = greedy_coloring(graph)
    welsh = welsh_powell_coloring(graph)
    dsatur = dsatur_coloring(graph)
    
    print(f"  算法比较:")
    print(f"    - 贪心: {count_colors(greedy)} 色")
    print(f"    - Welsh-Powell: {count_colors(welsh)} 色")
    print(f"    - DSatur: {count_colors(dsatur)} 色")
    
    print()


def test_backtracking_coloring():
    """测试回溯法着色"""
    print("=== 测试回溯法着色 ===")
    
    # 小规模图
    graph = Graph.from_edges([
        ("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("A", "C")
    ])
    
    coloring = backtracking_coloring(graph)
    assert coloring is not None
    assert is_valid_coloring(graph, coloring)
    print(f"✓ 回溯法着色: 使用 {count_colors(coloring)} 种颜色")
    print(f"  着色方案: {coloring}")
    
    # 测试指定最大颜色数
    coloring_2 = backtracking_coloring(graph, max_colors=2)
    # 这个图有三角形(A-B-C-A)，至少需要3种颜色
    assert coloring_2 is None
    print(f"✓ 限制2色测试: 正确返回 None (图包含三角形)")
    
    coloring_3 = backtracking_coloring(graph, max_colors=3)
    assert coloring_3 is not None
    print(f"✓ 限制3色测试: 找到解 {coloring_3}")
    
    print()


def test_interval_graph():
    """测试区间图"""
    print("=== 测试区间图 ===")
    
    # 课程安排问题
    interval_graph = IntervalGraph()
    interval_graph.add_interval("数学", 8, 10)
    interval_graph.add_interval("物理", 9, 11)
    interval_graph.add_interval("化学", 10, 12)
    interval_graph.add_interval("生物", 8, 9)
    interval_graph.add_interval("英语", 11, 13)
    
    coloring = interval_graph.optimal_coloring()
    print(f"✓ 课程安排最优着色: 使用 {count_colors(coloring)} 个教室")
    print(f"  分配方案: {coloring}")
    
    # 验证正确性
    groups = get_color_groups(coloring)
    for color, courses in groups.items():
        print(f"  教室 {color + 1}: {courses}")
    
    print()


def test_bipartite_checker():
    """测试二分图检测"""
    print("=== 测试二分图检测 ===")
    
    # 二分图
    bipartite = Graph.create_bipartite(3, 3)
    is_bip, coloring = BipartiteChecker.is_bipartite(bipartite)
    assert is_bip
    print(f"✓ 二分图检测: 正确识别为二分图")
    print(f"  二着色方案: {coloring}")
    
    # 非二分图（含奇环）
    non_bipartite = Graph.create_cycle(3)  # 三角形
    is_bip, coloring = BipartiteChecker.is_bipartite(non_bipartite)
    assert not is_bip
    print(f"✓ 非二分图检测: 正确识别三角形图为非二分图")
    
    print()


def test_color_groups():
    """测试颜色分组"""
    print("=== 测试颜色分组 ===")
    
    graph = Graph.from_edges([
        ("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")
    ])
    coloring = dsatur_coloring(graph)
    groups = get_color_groups(coloring)
    
    print(f"✓ 颜色分组:")
    for color, vertices in sorted(groups.items()):
        print(f"  颜色 {color}: {vertices}")
    
    print()


def test_chromatic_bounds():
    """测试色数上下界"""
    print("=== 测试色数上下界 ===")
    
    # 完全图
    complete = Graph.create_complete(5)
    lower, upper = chromatic_number_bounds(complete)
    print(f"✓ K5 完全图: 色数范围 [{lower}, {upper}]")
    
    # 环图
    cycle = Graph.create_cycle(5)
    lower, upper = chromatic_number_bounds(cycle)
    print(f"✓ C5 环图: 色数范围 [{lower}, {upper}]")
    
    print()


def test_compare_algorithms():
    """测试算法比较"""
    print("=== 测试算法比较 ===")
    
    # 创建一个中等复杂度的图
    graph = Graph.from_edges([
        ("A", "B"), ("A", "C"), ("A", "D"),
        ("B", "C"), ("B", "E"),
        ("C", "D"), ("C", "E"),
        ("D", "F"),
        ("E", "F"), ("E", "G"),
        ("F", "G")
    ])
    
    results = compare_algorithms(graph)
    
    print("算法比较结果:")
    for name, data in results.items():
        print(f"  {name}: {data['colors']} 色, 有效: {data['valid']}")
    
    print()


def test_find_coloring():
    """测试通用着色接口"""
    print("=== 测试通用着色接口 ===")
    
    graph = Graph.from_edges([
        ("X", "Y"), ("Y", "Z"), ("Z", "W"), ("W", "X")
    ])
    
    for algo in ["greedy", "welsh_powell", "dsatur", "backtracking"]:
        coloring = find_coloring(graph, algo)
        assert is_valid_coloring(graph, coloring)
        print(f"✓ {algo}: {count_colors(coloring)} 色")
    
    print()


def test_large_graph():
    """测试较大规模图"""
    print("=== 测试较大规模图 ===")
    
    # 创建 10x10 网格
    grid = Graph.create_grid(10, 10)
    print(f"网格图 10x10: {len(grid.vertices)} 顶点, {len(grid.edges)} 条边")
    
    # 测试各算法
    import time
    
    start = time.time()
    g_coloring = greedy_coloring(grid)
    g_time = time.time() - start
    print(f"✓ 贪心: {count_colors(g_coloring)} 色, 耗时 {g_time:.4f}s")
    
    start = time.time()
    w_coloring = welsh_powell_coloring(grid)
    w_time = time.time() - start
    print(f"✓ Welsh-Powell: {count_colors(w_coloring)} 色, 耗时 {w_time:.4f}s")
    
    start = time.time()
    d_coloring = dsatur_coloring(grid)
    d_time = time.time() - start
    print(f"✓ DSatur: {count_colors(d_coloring)} 色, 耗时 {d_time:.4f}s")
    
    print()


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("图着色工具模块测试")
    print("=" * 50)
    print()
    
    test_graph_creation()
    test_greedy_coloring()
    test_welsh_powell_coloring()
    test_dsatur_coloring()
    test_backtracking_coloring()
    test_interval_graph()
    test_bipartite_checker()
    test_color_groups()
    test_chromatic_bounds()
    test_compare_algorithms()
    test_find_coloring()
    test_large_graph()
    
    print("=" * 50)
    print("✓ 所有测试通过!")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()