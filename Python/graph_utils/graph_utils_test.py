"""
图论算法工具模块测试
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Graph, dfs, dfs_iterative, bfs, bfs_with_distance,
    dijkstra, get_shortest_path, bfs_path, bellman_ford, floyd_warshall,
    kruskal, prim,
    topological_sort, topological_sort_dfs,
    is_connected, find_connected_components, find_strongly_connected_components,
    has_cycle, has_cycle_directed, has_cycle_undirected, find_cycle, find_cycle_directed, find_cycle_undirected,
    is_bipartite, get_bipartition,
    get_degree_sequence, get_eccentricity, get_diameter, get_radius, get_center,
    to_adjacency_matrix, from_adjacency_matrix, copy_graph,
    create_empty_graph, create_complete_graph, create_path_graph, create_cycle_graph, create_star_graph
)


def test_graph_creation():
    """测试图的创建和基本操作"""
    print("测试图的创建...")
    
    # 无向无权图
    g = Graph()
    g.add_edge('A', 'B')
    g.add_edge('B', 'C')
    g.add_edge('C', 'D')
    
    assert g.get_vertex_count() == 4
    assert g.get_edge_count() == 3
    assert g.has_edge('A', 'B')
    assert g.has_edge('B', 'A')  # 无向图双向
    assert not g.has_edge('A', 'D')
    print("  ✓ 无向无权图创建成功")
    
    # 有向带权图
    dg = Graph(directed=True, weighted=True)
    dg.add_edge('A', 'B', 5)
    dg.add_edge('B', 'C', 3)
    
    assert dg.get_edge_weight('A', 'B') == 5
    assert dg.get_edge_weight('B', 'A') is None  # 有向图单向
    print("  ✓ 有向带权图创建成功")
    
    # 移除边和顶点
    g2 = Graph()
    g2.add_edge(1, 2)
    g2.add_edge(2, 3)
    assert g2.remove_edge(1, 2) == True
    assert not g2.has_edge(1, 2)
    assert g2.remove_edge(1, 2) == False  # 已不存在
    print("  ✓ 移除边成功")
    
    assert g2.remove_vertex(3) == True
    assert 3 not in g2.get_vertices()
    print("  ✓ 移除顶点成功")


def test_traversal():
    """测试遍历算法"""
    print("\n测试遍历算法...")
    
    # 创建测试图
    #     A
    #    / \
    #   B   C
    #  / \   \
    # D   E   F
    g = Graph()
    edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'F')]
    for u, v in edges:
        g.add_edge(u, v)
    
    # DFS
    dfs_result = dfs(g, 'A')
    assert dfs_result[0] == 'A'
    assert len(dfs_result) == 6
    print("  ✓ DFS 遍历正确")
    
    # DFS 迭代版
    dfs_iter_result = dfs_iterative(g, 'A')
    assert len(dfs_iter_result) == 6
    print("  ✓ DFS 迭代版本正确")
    
    # BFS
    bfs_result = bfs(g, 'A')
    assert bfs_result[0] == 'A'
    assert bfs_result[1] in ['B', 'C']
    assert len(bfs_result) == 6
    print("  ✓ BFS 遍历正确")
    
    # BFS 带距离
    bfs_result, distances = bfs_with_distance(g, 'A')
    assert distances['A'] == 0
    assert distances['B'] == 1
    assert distances['D'] == 2
    print("  ✓ BFS 距离计算正确")


def test_shortest_path():
    """测试最短路径算法"""
    print("\n测试最短路径算法...")
    
    # 创建带权图
    #     A --2--> B
    #     |        |
    #     1        3
    #     |        |
    #     v        v
    #     C --4--> D
    g = Graph(directed=True, weighted=True)
    g.add_edge('A', 'B', 2)
    g.add_edge('A', 'C', 1)
    g.add_edge('B', 'D', 3)
    g.add_edge('C', 'D', 4)
    
    # Dijkstra
    distances, predecessors = dijkstra(g, 'A')
    assert distances['A'] == 0
    assert distances['B'] == 2
    assert distances['C'] == 1
    assert distances['D'] == 5  # A->B->D (2+3=5) 比 A->C->D (1+4=5) 相同
    print("  ✓ Dijkstra 算法正确")
    
    # 获取最短路径
    path = get_shortest_path(g, 'A', 'D')
    assert path[0] == 'A'
    assert path[-1] == 'D'
    print("  ✓ 最短路径获取正确")
    
    # 无权图 BFS 最短路径
    g2 = Graph(directed=True)
    g2.add_edge('A', 'B')
    g2.add_edge('B', 'C')
    g2.add_edge('A', 'C')  # 直接边
    
    path = get_shortest_path(g2, 'A', 'C', algorithm='bfs')
    assert path == ['A', 'C']  # 直接连接最短
    print("  ✓ BFS 最短路径正确")
    
    # Bellman-Ford
    bg = Graph(directed=True, weighted=True)
    bg.add_edge('A', 'B', 4)
    bg.add_edge('A', 'C', 2)
    bg.add_edge('C', 'B', -1)  # 负权边
    
    distances, predecessors, has_neg_cycle = bellman_ford(bg, 'A')
    assert not has_neg_cycle
    assert distances['B'] == 1  # A->C->B = 2 + (-1) = 1
    print("  ✓ Bellman-Ford 算法正确")
    
    # Floyd-Warshall
    fg = Graph(directed=True, weighted=True)
    fg.add_edge('A', 'B', 3)
    fg.add_edge('B', 'C', 2)
    fg.add_edge('A', 'C', 10)
    
    dist_matrix = floyd_warshall(fg)
    assert dist_matrix['A']['C'] == 5  # A->B->C = 3+2=5
    print("  ✓ Floyd-Warshall 算法正确")


def test_minimum_spanning_tree():
    """测试最小生成树算法"""
    print("\n测试最小生成树算法...")
    
    # 创建无向带权图
    #     A --2-- B
    #     |      /|
    #     1    3  4
    #     |  /    |
    #     C --5-- D
    g = Graph(weighted=True)
    g.add_edge('A', 'B', 2)
    g.add_edge('A', 'C', 1)
    g.add_edge('B', 'C', 3)
    g.add_edge('B', 'D', 4)
    g.add_edge('C', 'D', 5)
    
    # Kruskal
    edges, total = kruskal(g)
    assert len(edges) == 3  # n-1 条边
    assert total == 7  # 1 + 2 + 4 = 7
    print("  ✓ Kruskal 算法正确")
    
    # Prim
    edges, total = prim(g)
    assert len(edges) == 3
    assert total == 7
    print("  ✓ Prim 算法正确")


def test_topological_sort():
    """测试拓扑排序"""
    print("\n测试拓扑排序...")
    
    # 创建 DAG
    #     A --> B --> D
    #     |     |
    #     v     v
    #     C --> E
    g = Graph(directed=True)
    g.add_edge('A', 'B')
    g.add_edge('A', 'C')
    g.add_edge('B', 'D')
    g.add_edge('B', 'E')
    g.add_edge('C', 'E')
    
    # Kahn 算法
    result = topological_sort(g)
    assert result is not None
    assert result.index('A') < result.index('B')
    assert result.index('A') < result.index('C')
    assert result.index('B') < result.index('D')
    print("  ✓ Kahn 拓扑排序正确")
    
    # DFS 算法
    result_dfs = topological_sort_dfs(g)
    assert result_dfs is not None
    assert result_dfs.index('A') < result_dfs.index('B')
    print("  ✓ DFS 拓扑排序正确")
    
    # 带环的图
    cyclic = Graph(directed=True)
    cyclic.add_edge('A', 'B')
    cyclic.add_edge('B', 'C')
    cyclic.add_edge('C', 'A')  # 环
    
    assert topological_sort(cyclic) is None
    assert topological_sort_dfs(cyclic) is None
    print("  ✓ 环检测正确（返回 None）")


def test_connectivity():
    """测试连通性算法"""
    print("\n测试连通性算法...")
    
    # 连通图
    g1 = Graph()
    g1.add_edge(1, 2)
    g1.add_edge(2, 3)
    assert is_connected(g1)
    print("  ✓ 连通图检测正确")
    
    # 非连通图
    g2 = Graph()
    g2.add_edge(1, 2)
    g2.add_edge(3, 4)
    assert not is_connected(g2)
    
    components = find_connected_components(g2)
    assert len(components) == 2
    print("  ✓ 连通分量检测正确")
    
    # 强连通分量
    #     A --> B --> C
    #     ^     |
    #     |     v
    #     D <-- E
    scc_g = Graph(directed=True)
    scc_g.add_edge('A', 'B')
    scc_g.add_edge('B', 'C')
    scc_g.add_edge('B', 'E')
    scc_g.add_edge('E', 'D')
    scc_g.add_edge('D', 'A')
    
    sccs = find_strongly_connected_components(scc_g)
    # {A, B, D, E} 形成一个强连通分量，{C} 单独一个
    assert len(sccs) == 2
    print("  ✓ 强连通分量检测正确")


def test_cycle_detection():
    """测试环检测"""
    print("\n测试环检测...")
    
    # 无向图有环
    g1 = Graph()
    g1.add_edge(1, 2)
    g1.add_edge(2, 3)
    g1.add_edge(3, 1)  # 环
    assert has_cycle(g1)
    assert has_cycle_undirected(g1)
    print("  ✓ 无向图环检测正确")
    
    # 无向图无环
    g2 = Graph()
    g2.add_edge(1, 2)
    g2.add_edge(2, 3)
    assert not has_cycle(g2)
    print("  ✓ 无向图无环检测正确")
    
    # 有向图有环
    g3 = Graph(directed=True)
    g3.add_edge('A', 'B')
    g3.add_edge('B', 'C')
    g3.add_edge('C', 'A')  # 环
    assert has_cycle(g3)
    assert has_cycle_directed(g3)
    print("  ✓ 有向图环检测正确")
    
    # 有向图无环
    g4 = Graph(directed=True)
    g4.add_edge('A', 'B')
    g4.add_edge('B', 'C')
    assert not has_cycle(g4)
    print("  ✓ 有向图无环检测正确")


def test_bipartite():
    """测试二分图检测"""
    print("\n测试二分图...")
    
    # 二分图
    # 左边: A, C    右边: B, D
    # A-B, A-D, C-B, C-D
    g1 = Graph()
    g1.add_edge('A', 'B')
    g1.add_edge('A', 'D')
    g1.add_edge('C', 'B')
    g1.add_edge('C', 'D')
    
    assert is_bipartite(g1)
    set_a, set_b = get_bipartition(g1)
    assert ('A' in set_a and 'C' in set_a) or ('A' in set_b and 'C' in set_b)
    print("  ✓ 二分图检测正确")
    
    # 非二分图（奇环）
    g2 = Graph()
    g2.add_edge(1, 2)
    g2.add_edge(2, 3)
    g2.add_edge(3, 1)  # 三角形
    assert not is_bipartite(g2)
    assert get_bipartition(g2) is None
    print("  ✓ 非二分图检测正确")


def test_graph_metrics():
    """测试图度量"""
    print("\n测试图度量...")
    
    # 创建路径图 P5: 0-1-2-3-4
    g = create_path_graph(5)
    
    assert get_diameter(g) == 4
    assert get_radius(g) == 2
    assert get_center(g) == {2}
    print("  ✓ 直径、半径、中心计算正确")
    
    degree_seq = get_degree_sequence(g)
    assert 2 in degree_seq  # 内部顶点度为2
    print("  ✓ 度序列正确")


def test_factory_functions():
    """测试工厂函数"""
    print("\n测试工厂函数...")
    
    # 空图
    g = create_empty_graph()
    assert g.get_vertex_count() == 0
    print("  ✓ 创建空图成功")
    
    # 完全图 K4
    complete = create_complete_graph(4)
    assert complete.get_vertex_count() == 4
    assert complete.get_edge_count() == 6  # C(4,2) = 6
    print("  ✓ 创建完全图成功")
    
    # 路径图 P5
    path = create_path_graph(5)
    assert path.get_vertex_count() == 5
    assert path.get_edge_count() == 4
    print("  ✓ 创建路径图成功")
    
    # 环图 C5
    cycle = create_cycle_graph(5)
    assert cycle.get_vertex_count() == 5
    assert cycle.get_edge_count() == 5
    assert has_cycle(cycle)
    print("  ✓ 创建环图成功")
    
    # 星图 S4
    star = create_star_graph(4)
    assert star.get_vertex_count() == 5  # 中心 + 4 叶子
    assert star.get_edge_count() == 4
    assert star.get_degree(0) == 4  # 中心度最大
    print("  ✓ 创建星图成功")


def test_adjacency_matrix():
    """测试邻接矩阵转换"""
    print("\n测试邻接矩阵转换...")
    
    g = Graph(weighted=True)
    g.add_edge(0, 1, 2)
    g.add_edge(1, 2, 3)
    g.add_edge(0, 2, 5)
    
    matrix, vertices = to_adjacency_matrix(g)
    assert matrix[0][1] == 2
    assert matrix[1][2] == 3
    assert matrix[0][2] == 5
    print("  ✓ 邻接矩阵转换正确")
    
    # 从邻接矩阵创建图
    g2 = from_adjacency_matrix(matrix, vertices)
    assert g2.get_edge_weight(0, 1) == 2
    print("  ✓ 从邻接矩阵创建图正确")


def test_copy_graph():
    """测试图复制"""
    print("\n测试图复制...")
    
    g1 = Graph(directed=True, weighted=True)
    g1.add_edge('A', 'B', 5)
    g1.add_edge('B', 'C', 3)
    
    g2 = copy_graph(g1)
    
    assert g2.directed == g1.directed
    assert g2.weighted == g1.weighted
    assert g2.get_edge_weight('A', 'B') == 5
    
    # 修改 g1 不影响 g2
    g1.add_edge('A', 'C', 10)
    assert g2.get_edge_weight('A', 'C') is None
    print("  ✓ 图深拷贝正确")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("图论算法工具模块测试")
    print("=" * 50)
    
    test_graph_creation()
    test_traversal()
    test_shortest_path()
    test_minimum_spanning_tree()
    test_topological_sort()
    test_connectivity()
    test_cycle_detection()
    test_bipartite()
    test_graph_metrics()
    test_factory_functions()
    test_adjacency_matrix()
    test_copy_graph()
    
    print("\n" + "=" * 50)
    print("✅ 所有测试通过！")
    print("=" * 50)


if __name__ == '__main__':
    run_all_tests()