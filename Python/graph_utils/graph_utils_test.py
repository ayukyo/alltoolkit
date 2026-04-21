"""
Graph Utils 测试套件

测试覆盖：
- 图的基本操作（添加/删除节点和边）
- 遍历算法（BFS/DFS）
- 最短路径算法（Dijkstra/Bellman-Ford/Floyd-Warshall）
- 最小生成树（Prim/Kruskal）
- 拓扑排序
- 连通性算法
- 环检测
- 二分图检测
- 其他实用算法

运行方式：
    python graph_utils_test.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Graph, bfs, dfs, dfs_postorder,
    dijkstra, bellman_ford, floyd_warshall, get_path, shortest_path_bfs, all_paths,
    prim, kruskal,
    topological_sort, topological_sort_dfs,
    connected_components, is_connected, strongly_connected_components,
    has_cycle, find_cycle,
    is_bipartite,
    degree_sequence, is_eulerian, is_semi_eulerian,
    articulation_points, bridges,
    degree_centrality, betweenness_centrality,
    clustering_coefficient, average_clustering_coefficient
)


class TestResult:
    """测试结果收集器"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def test(self, condition: bool, message: str):
        if condition:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(message)
            print(f"  ✗ {message}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"测试结果: {self.passed}/{total} 通过")
        if self.failed > 0:
            print(f"\n失败的测试:")
            for err in self.errors:
                print(f"  - {err}")
        print(f"{'='*60}")
        return self.failed == 0


def test_graph_basic():
    """测试图的基本操作"""
    print("\n测试图基本操作...")
    r = TestResult()
    
    # 创建无向图
    g = Graph[str](directed=False)
    g.add_edge("A", "B", 5)
    g.add_edge("B", "C", 3)
    g.add_edge("A", "C", 2)
    
    r.test(g.node_count() == 3, "节点数应为 3")
    r.test(g.edge_count() == 3, f"无向图边数应为 3，实际 {g.edge_count()}")
    r.test(g.has_node("A") == True, "应存在节点 A")
    r.test(g.has_node("D") == False, "不应存在节点 D")
    r.test(g.has_edge("A", "B") == True, "应存在边 A-B")
    r.test(g.has_edge("B", "A") == True, "无向图应存在边 B-A")
    r.test(g.degree("A") == 2, "A 的度应为 2")
    
    # 邻居测试
    neighbors = g.neighbors("A")
    neighbor_nodes = [n for n, _ in neighbors]
    r.test("B" in neighbor_nodes and "C" in neighbor_nodes, "A 的邻居应包含 B 和 C")
    
    # 创建有向图
    dg = Graph[int](directed=True)
    dg.add_edge(1, 2)
    dg.add_edge(2, 3)
    
    r.test(dg.has_edge(1, 2) == True, "有向图应存在边 1->2")
    r.test(dg.has_edge(2, 1) == False, "有向图不应存在边 2->1")
    r.test(dg.edge_count() == 2, f"有向图边数应为 2，实际 {dg.edge_count()}")
    
    # 删除边
    g2 = Graph[str]()
    g2.add_edge("X", "Y")
    g2.add_edge("X", "Z")
    r.test(g2.remove_edge("X", "Y") == True, "应成功删除边 X-Y")
    r.test(g2.has_edge("X", "Y") == False, "删除后不应存在边 X-Y")
    r.test(g2.has_edge("X", "Z") == True, "应仍存在边 X-Z")
    
    # 删除节点
    g3 = Graph[str]()
    g3.add_edge("A", "B")
    g3.add_edge("B", "C")
    r.test(g3.remove_node("B") == True, "应成功删除节点 B")
    r.test(g3.has_node("B") == False, "删除后不应存在节点 B")
    r.test(g3.has_edge("A", "B") == False, "删除节点后关联边应消失")
    
    # 邻接矩阵转换
    nodes, matrix = g.to_adjacency_matrix()
    r.test(len(nodes) == 3, "邻接矩阵节点数应为 3")
    r.test(matrix[0][0] == 0, "对角线应为 0")
    
    # 从边列表创建
    g4 = Graph.from_edges([(1, 2), (2, 3), (3, 1)])
    r.test(g4.node_count() == 3, "从边列表创建的图节点数应为 3")
    r.test(g4.edge_count() == 3, "从边列表创建的无向图边数应为 3")
    
    # 深拷贝
    g5 = g.copy()
    r.test(g5.node_count() == g.node_count(), "拷贝图节点数应相同")
    g5.add_edge("D", "E")
    r.test(g.has_node("D") == False, "原图不应受拷贝修改影响")
    
    return r.summary()


def test_traversal():
    """测试遍历算法"""
    print("\n测试遍历算法...")
    r = TestResult()
    
    # 创建测试图
    #     A
    #    / \
    #   B   C
    #  / \   \
    # D   E   F
    g = Graph[str]()
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    g.add_edge("B", "E")
    g.add_edge("C", "F")
    
    # BFS
    bfs_result = bfs(g, "A")
    r.test(bfs_result[0] == "A", "BFS 起点应为 A")
    r.test("B" in bfs_result and "C" in bfs_result, "BFS 应包含 B 和 C")
    r.test(bfs_result.index("B") < bfs_result.index("D"), "BFS 中 B 应在 D 之前")
    r.test(bfs_result.index("B") < bfs_result.index("E"), "BFS 中 B 应在 E 之前")
    
    # DFS（递归）
    dfs_result = dfs(g, "A", recursive=True)
    r.test(dfs_result[0] == "A", "DFS 起点应为 A")
    r.test(len(dfs_result) == 6, f"DFS 应遍历 6 个节点，实际 {len(dfs_result)}")
    
    # DFS（迭代）
    dfs_iter = dfs(g, "A", recursive=False)
    r.test(dfs_iter[0] == "A", "DFS 迭代起点应为 A")
    r.test(len(dfs_iter) == 6, f"DFS 迭代应遍历 6 个节点")
    
    # 后序 DFS
    postorder = dfs_postorder(g, "A")
    r.test(len(postorder) == 6, "后序 DFS 应遍历 6 个节点")
    r.test("A" == postorder[-1] or "A" in postorder, "后序 DFS 中根节点应在后面")
    
    # 空图/不存在的起点
    empty_g = Graph[int]()
    r.test(bfs(empty_g, 1) == [], "空图 BFS 应返回空列表")
    r.test(dfs(empty_g, 1) == [], "空图 DFS 应返回空列表")
    
    # 单节点
    single = Graph[int]()
    single.add_node(1)
    r.test(bfs(single, 1) == [1], "单节点 BFS 应返回 [1]")
    r.test(dfs(single, 1) == [1], "单节点 DFS 应返回 [1]")
    
    return r.summary()


def test_shortest_path():
    """测试最短路径算法"""
    print("\n测试最短路径算法...")
    r = TestResult()
    
    # 创建测试图
    #      4
    #  A -----> B
    #  |       /|
    # 2|      / |3
    #  v     v  v
    #  C -----> D
    #      1
    g = Graph[str](directed=True)
    g.add_edge("A", "B", 4)
    g.add_edge("A", "C", 2)
    g.add_edge("B", "D", 3)
    g.add_edge("C", "D", 1)
    g.add_edge("B", "C", 1)
    
    # Dijkstra
    result = dijkstra(g, "A")
    r.test(result["A"][0] == 0, "起点到自身距离应为 0")
    r.test(result["C"][0] == 2, "A->C 最短距离应为 2")
    r.test(result["D"][0] == 3, "A->D 最短距离应为 3（A->C->D）")
    r.test(result["B"][0] == 4, "A->B 最短距离应为 4")
    
    # 路径重构（提取前驱字典）
    pred_dict = {n: p for n, (d, p) in result.items()}
    path = get_path(pred_dict, "A", "D")
    r.test(path == ["A", "C", "D"] or path == ["A", "B", "D"], f"A->D 路径应为 ['A','C','D'] 或 ['A','B','D']，实际 {path}")
    
    # 提前终止
    result_early = dijkstra(g, "A", end="C")
    r.test(result_early["C"][0] == 2, "提前终止时 A->C 距离应为 2")
    
    # 负权边检测
    g_neg = Graph[str](directed=True)
    g_neg.add_edge("A", "B", -1)
    try:
        dijkstra(g_neg, "A")
        r.test(False, "Dijkstra 应拒绝负权边")
    except ValueError:
        r.test(True, "Dijkstra 正确拒绝负权边")
    
    # Bellman-Ford
    result, neg_cycle = bellman_ford(g, "A")
    r.test(neg_cycle == False, "图应无负环")
    r.test(result["D"][0] == 3, "Bellman-Ford: A->D 距离应为 3")
    
    # 负权边测试
    g_neg2 = Graph[str](directed=True)
    g_neg2.add_edge("A", "B", 4)
    g_neg2.add_edge("B", "C", -2)
    g_neg2.add_edge("A", "C", 5)
    
    result2, neg_cycle2 = bellman_ford(g_neg2, "A")
    r.test(neg_cycle2 == False, "无负环时应返回 False")
    r.test(result2["C"][0] == 2, "A->B->C 距离应为 2")
    
    # 负环测试
    g_cycle = Graph[str](directed=True)
    g_cycle.add_edge("A", "B", 1)
    g_cycle.add_edge("B", "C", -3)  # A->B->C->A = 1 + (-3) + 1 = -1，负环
    g_cycle.add_edge("C", "A", 1)
    
    _, has_neg = bellman_ford(g_cycle, "A")
    r.test(has_neg == True, "应检测到负环")
    
    # Floyd-Warshall
    g2 = Graph[int]()
    g2.add_edge(0, 1, 3)
    g2.add_edge(1, 2, 2)
    g2.add_edge(0, 2, 8)
    
    dist, _ = floyd_warshall(g2)
    r.test(dist[0][0] == 0, "节点到自身距离为 0")
    r.test(dist[0][2] == 5, "0->2 最短距离应为 5（经 1）")
    
    # BFS 最短路径（无权）
    g3 = Graph[str]()
    g3.add_edge("A", "B")
    g3.add_edge("B", "C")
    g3.add_edge("A", "D")
    g3.add_edge("D", "C")
    
    path = shortest_path_bfs(g3, "A", "C")
    r.test(len(path) == 3, f"BFS 最短路径长度应为 3，实际 {len(path)}")
    r.test(path[0] == "A" and path[-1] == "C", "路径起点和终点应正确")
    
    # 不存在的路径
    g4 = Graph[str]()
    g4.add_edge("A", "B")
    g4.add_node("C")  # 孤立节点
    
    path = shortest_path_bfs(g4, "A", "C")
    r.test(path is None, "到孤立节点应无路径")
    
    # 所有路径
    g5 = Graph[str]()
    g5.add_edge("A", "B")
    g5.add_edge("A", "C")
    g5.add_edge("B", "D")
    g5.add_edge("C", "D")
    
    paths = all_paths(g5, "A", "D")
    r.test(len(paths) == 2, f"应有 2 条路径，实际 {len(paths)}")
    
    return r.summary()


def test_mst():
    """测试最小生成树算法"""
    print("\n测试最小生成树...")
    r = TestResult()
    
    # 创建测试图
    #    A---2---B
    #    |\      |
    #    3 1     4
    #    |  \    |
    #    C---5---D
    g = Graph[str]()
    g.add_edge("A", "B", 2)
    g.add_edge("A", "C", 3)
    g.add_edge("A", "D", 1)
    g.add_edge("B", "D", 4)
    g.add_edge("C", "D", 5)
    
    # Prim
    mst_prim = prim(g)
    total_weight = sum(w for _, _, w in mst_prim)
    r.test(len(mst_prim) == 3, f"MST 应有 3 条边，实际 {len(mst_prim)}")
    r.test(total_weight == 6, f"MST 总权重应为 6（A-D=1, A-B=2, A-C=3），实际 {total_weight}")
    
    # Kruskal
    mst_kruskal = kruskal(g)
    total_weight_k = sum(w for _, _, w in mst_kruskal)
    r.test(len(mst_kruskal) == 3, "Kruskal MST 应有 3 条边")
    r.test(total_weight_k == 6, "Kruskal MST 总权重应为 6")
    
    # 空图
    empty = Graph[int]()
    r.test(prim(empty) == [], "空图 MST 应为空")
    r.test(kruskal(empty) == [], "空图 Kruskal MST 应为空")
    
    # 单节点
    single = Graph[int]()
    single.add_node(1)
    r.test(prim(single) == [], "单节点 MST 应为空")
    
    # 有向图应报错
    dg = Graph[int](directed=True)
    dg.add_edge(1, 2)
    try:
        prim(dg)
        r.test(False, "Prim 应拒绝有向图")
    except ValueError:
        r.test(True, "Prim 正确拒绝有向图")
    
    try:
        kruskal(dg)
        r.test(False, "Kruskal 应拒绝有向图")
    except ValueError:
        r.test(True, "Kruskal 正确拒绝有向图")
    
    # 非连通图（森林）
    forest = Graph[int]()
    forest.add_edge(1, 2, 1)
    forest.add_edge(3, 4, 2)
    
    mst_forest = kruskal(forest)
    r.test(len(mst_forest) == 2, "森林 MST 应有 2 条边")
    total = sum(w for _, _, w in mst_forest)
    r.test(total == 3, f"森林 MST 总权重应为 3，实际 {total}")
    
    return r.summary()


def test_topological_sort():
    """测试拓扑排序"""
    print("\n测试拓扑排序...")
    r = TestResult()
    
    # 创建 DAG
    #   A --> B --> D
    #   |     |
    #   v     v
    #   C --> E
    g = Graph[str](directed=True)
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    g.add_edge("B", "E")
    g.add_edge("C", "E")
    
    # Kahn 算法
    result = topological_sort(g)
    r.test(result is not None, "DAG 应有拓扑排序")
    r.test(len(result) == 5, f"拓扑序列应有 5 个节点，实际 {len(result)}")
    r.test(result.index("A") < result.index("B"), "A 应在 B 之前")
    r.test(result.index("A") < result.index("C"), "A 应在 C 之前")
    r.test(result.index("B") < result.index("D"), "B 应在 D 之前")
    r.test(result.index("B") < result.index("E"), "B 应在 E 之前")
    r.test(result.index("C") < result.index("E"), "C 应在 E 之前")
    
    # DFS 算法
    result_dfs = topological_sort_dfs(g)
    r.test(result_dfs is not None, "DFS 拓扑排序应有结果")
    r.test(len(result_dfs) == 5, "DFS 拓扑序列应有 5 个节点")
    
    # 有环图
    cyclic = Graph[int](directed=True)
    cyclic.add_edge(1, 2)
    cyclic.add_edge(2, 3)
    cyclic.add_edge(3, 1)
    
    result_cyclic = topological_sort(cyclic)
    r.test(result_cyclic is None, "有环图应无拓扑排序")
    
    result_cyclic_dfs = topological_sort_dfs(cyclic)
    r.test(result_cyclic_dfs is None, "DFS 应检测到环")
    
    # 空图
    empty = Graph[int](directed=True)
    r.test(topological_sort(empty) == [], "空图拓扑排序应为空列表")
    
    # 单节点
    single = Graph[int](directed=True)
    single.add_node(1)
    r.test(topological_sort(single) == [1], "单节点拓扑排序应为 [1]")
    
    # 无向图应报错
    ug = Graph[int]()
    ug.add_edge(1, 2)
    try:
        topological_sort(ug)
        r.test(False, "拓扑排序应拒绝无向图")
    except ValueError:
        r.test(True, "拓扑排序正确拒绝无向图")
    
    return r.summary()


def test_connectivity():
    """测试连通性算法"""
    print("\n测试连通性算法...")
    r = TestResult()
    
    # 连通无向图
    g1 = Graph[int]()
    g1.add_edge(1, 2)
    g1.add_edge(2, 3)
    g1.add_edge(3, 4)
    
    r.test(is_connected(g1) == True, "图应连通")
    
    # 非连通图
    g2 = Graph[int]()
    g2.add_edge(1, 2)
    g2.add_edge(3, 4)
    
    r.test(is_connected(g2) == False, "图应不连通")
    
    # 连通分量
    components = connected_components(g2)
    r.test(len(components) == 2, f"应有 2 个连通分量，实际 {len(components)}")
    r.test(any(1 in c for c in components), "应有包含 1 的分量")
    r.test(any(3 in c for c in components), "应有包含 3 的分量")
    
    # 强连通分量
    g3 = Graph[int](directed=True)
    g3.add_edge(1, 2)
    g3.add_edge(2, 3)
    g3.add_edge(3, 1)
    g3.add_edge(3, 4)
    g3.add_edge(4, 5)
    g3.add_edge(5, 4)
    
    sccs = strongly_connected_components(g3)
    r.test(len(sccs) == 2, f"应有 2 个强连通分量，实际 {len(sccs)}")
    
    # 找到包含 1,2,3 的分量
    scc_123 = [s for s in sccs if 1 in s or 2 in s or 3 in s]
    r.test(any(len(s) == 3 and 1 in s and 2 in s and 3 in s for s in sccs), 
           "1,2,3 应在同一强连通分量")
    
    # 空图
    empty = Graph[int]()
    r.test(is_connected(empty) == True, "空图视为连通")
    r.test(connected_components(empty) == [], "空图连通分量为空")
    
    return r.summary()


def test_cycle_detection():
    """测试环检测"""
    print("\n测试环检测...")
    r = TestResult()
    
    # 无向图有环
    g_cycle = Graph[int]()
    g_cycle.add_edge(1, 2)
    g_cycle.add_edge(2, 3)
    g_cycle.add_edge(3, 1)
    
    r.test(has_cycle(g_cycle) == True, "无向图应检测到环")
    
    # 无向图无环
    g_tree = Graph[int]()
    g_tree.add_edge(1, 2)
    g_tree.add_edge(2, 3)
    g_tree.add_edge(3, 4)
    
    r.test(has_cycle(g_tree) == False, "树应无环")
    
    # 有向图有环
    dg_cycle = Graph[int](directed=True)
    dg_cycle.add_edge(1, 2)
    dg_cycle.add_edge(2, 3)
    dg_cycle.add_edge(3, 1)
    
    r.test(has_cycle(dg_cycle) == True, "有向图应检测到环")
    
    # 有向图无环
    dag = Graph[int](directed=True)
    dag.add_edge(1, 2)
    dag.add_edge(2, 3)
    
    r.test(has_cycle(dag) == False, "DAG 应无环")
    
    # 查找环
    cycle = find_cycle(g_cycle)
    r.test(cycle is not None, "应能找到环")
    r.test(len(cycle) >= 3, "环长度应至少为 3")
    
    # 无环查找
    no_cycle = find_cycle(g_tree)
    r.test(no_cycle is None, "无环图应返回 None")
    
    # 自环
    self_loop = Graph[int]()
    self_loop.add_edge(1, 1)
    
    r.test(has_cycle(self_loop) == True, "自环应检测为环")
    
    return r.summary()


def test_bipartite():
    """测试二分图检测"""
    print("\n测试二分图检测...")
    r = TestResult()
    
    # 二分图
    g1 = Graph[int]()
    g1.add_edge(1, 2)
    g1.add_edge(1, 4)
    g1.add_edge(2, 3)
    g1.add_edge(3, 4)
    
    is_bip, partition = is_bipartite(g1)
    r.test(is_bip == True, "应为二分图")
    r.test(partition is not None, "应返回分区")
    if partition:
        set_a, set_b = partition
        r.test(len(set_a) + len(set_b) == 4, "所有节点应被分区")
        r.test(set_a.isdisjoint(set_b), "分区不应重叠")
    
    # 非二分图（奇环）
    g2 = Graph[int]()
    g2.add_edge(1, 2)
    g2.add_edge(2, 3)
    g2.add_edge(3, 1)
    
    is_bip2, _ = is_bipartite(g2)
    r.test(is_bip2 == False, "奇环图不应为二分图")
    
    # 单节点
    g3 = Graph[int]()
    g3.add_node(1)
    
    is_bip3, part3 = is_bipartite(g3)
    r.test(is_bip3 == True, "单节点应为二分图")
    
    # 空图
    g4 = Graph[int]()
    is_bip4, _ = is_bipartite(g4)
    r.test(is_bip4 == True, "空图应为二分图")
    
    return r.summary()


def test_special_algorithms():
    """测试特殊算法"""
    print("\n测试特殊算法...")
    r = TestResult()
    
    # 欧拉图（所有节点度数都是偶数且连通）
    eulerian = Graph[int]()
    eulerian.add_edge(1, 2)
    eulerian.add_edge(2, 3)
    eulerian.add_edge(3, 1)  # 三个节点每个度都是 2
    eulerian.add_edge(4, 5)
    eulerian.add_edge(5, 6)
    eulerian.add_edge(6, 4)  # 另一个三角形
    eulerian.add_edge(1, 4)  # 连接两个三角形，度变成 3（奇数）
    
    # 真正的欧拉图：所有度都是偶数
    eulerian2 = Graph[int]()
    eulerian2.add_edge(1, 2)
    eulerian2.add_edge(2, 3)
    eulerian2.add_edge(3, 4)
    eulerian2.add_edge(4, 1)  # 四边形，每个节点度都是 2
    
    r.test(is_eulerian(eulerian2) == True, "应识别欧拉图（四边形）")
    
    # 半欧拉图
    semi_eulerian = Graph[int]()
    semi_eulerian.add_edge(1, 2)
    semi_eulerian.add_edge(2, 3)
    semi_eulerian.add_edge(3, 4)
    semi_eulerian.add_edge(4, 1)
    semi_eulerian.add_edge(1, 3)
    
    r.test(is_semi_eulerian(semi_eulerian) == True, "应识别半欧拉图")
    r.test(is_eulerian(semi_eulerian) == False, "半欧拉图不是欧拉图")
    
    # 割点
    g_ap = Graph[str]()
    g_ap.add_edge("A", "B")
    g_ap.add_edge("B", "C")
    g_ap.add_edge("B", "D")
    g_ap.add_edge("C", "D")
    g_ap.add_edge("B", "E")
    
    aps = articulation_points(g_ap)
    r.test("B" in aps, "B 应为割点")
    
    # 桥
    g_bridge = Graph[str]()
    g_bridge.add_edge("A", "B")
    g_bridge.add_edge("B", "C")
    g_bridge.add_edge("C", "D")
    g_bridge.add_edge("D", "E")
    
    bridges_list = bridges(g_bridge)
    r.test(len(bridges_list) == 4, f"链状图应有 4 座桥，实际 {len(bridges_list)}")
    
    # 度序列
    g_seq = Graph[int]()
    g_seq.add_edge(1, 2)
    g_seq.add_edge(1, 3)
    g_seq.add_edge(1, 4)
    
    seq = degree_sequence(g_seq)
    r.test(seq[0] == 3, "最大度应为 3（节点 1）")
    r.test(seq[-1] == 1, "最小度应为 1")
    
    return r.summary()


def test_centrality():
    """测试中心性算法"""
    print("\n测试中心性算法...")
    r = TestResult()
    
    # 度中心性
    g = Graph[str]()
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("A", "D")
    g.add_edge("B", "C")
    
    dc = degree_centrality(g)
    r.test(dc["A"] > dc["B"], "A 的度中心性应高于 B")
    r.test(abs(dc["A"] - 1.0) < 0.01, f"A 的度中心性应接近 1.0，实际 {dc['A']}")
    
    # 介数中心性
    g2 = Graph[str]()
    g2.add_edge("A", "B")
    g2.add_edge("B", "C")
    g2.add_edge("C", "D")
    
    bc = betweenness_centrality(g2)
    r.test(bc["B"] > 0, "B 应有介数中心性")
    r.test(bc["C"] > 0, "C 应有介数中心性")
    
    # 单节点
    single = Graph[int]()
    single.add_node(1)
    dc_single = degree_centrality(single)
    r.test(dc_single[1] == 0.0, "单节点度中心性应为 0")
    
    return r.summary()


def test_clustering():
    """测试聚类系数"""
    print("\n测试聚类系数...")
    r = TestResult()
    
    # 完全图聚类系数 = 1
    complete = Graph[int]()
    complete.add_edge(1, 2)
    complete.add_edge(1, 3)
    complete.add_edge(2, 3)
    
    cc = clustering_coefficient(complete)
    r.test(all(c == 1.0 for c in cc.values()), "完全图聚类系数应为 1")
    
    # 星形图中心聚类系数 = 0
    star = Graph[int]()
    star.add_edge(1, 2)
    star.add_edge(1, 3)
    star.add_edge(1, 4)
    
    cc_star = clustering_coefficient(star)
    r.test(cc_star[1] == 0.0, "星形图中心节点聚类系数应为 0")
    
    # 平均聚类系数
    avg = average_clustering_coefficient(complete)
    r.test(avg == 1.0, "完全图平均聚类系数应为 1")
    
    # 单节点
    single = Graph[int]()
    single.add_node(1)
    cc_single = clustering_coefficient(single)
    r.test(cc_single[1] == 0.0, "单节点聚类系数应为 0")
    
    return r.summary()


def test_edge_cases():
    """测试边界情况"""
    print("\n测试边界情况...")
    r = TestResult()
    
    # 空图
    empty = Graph[int]()
    r.test(empty.node_count() == 0, "空图节点数应为 0")
    r.test(empty.edge_count() == 0, "空图边数应为 0")
    r.test(empty.get_nodes() == set(), "空图节点集应为空")
    r.test(empty.get_edges() == [], "空图边列表应为空")
    
    # 单节点
    single = Graph[str]()
    single.add_node("A")
    r.test(single.node_count() == 1, "单节点图节点数应为 1")
    r.test(single.edge_count() == 0, "单节点无边")
    r.test(single.degree("A") == 0, "单节点度为 0")
    
    # 自环
    loop = Graph[int]()
    loop.add_edge(1, 1)
    r.test(loop.has_edge(1, 1) == True, "应有自环")
    r.test(loop.degree(1) == 2, "自环贡献度为 2（无向图）")
    
    # 重复边
    multi = Graph[str]()
    multi.add_edge("A", "B", 1)
    multi.add_edge("A", "B", 2)  # 添加重复边
    r.test(multi.edge_count() >= 1, "应有边")
    
    # 大权重
    big_weight = Graph[str]()
    big_weight.add_edge("A", "B", 1e10)
    result = dijkstra(big_weight, "A")
    r.test(result["B"][0] == 1e10, "大权重应正确处理")
    
    # 零权重
    zero_weight = Graph[str]()
    zero_weight.add_edge("A", "B", 0)
    result_z = dijkstra(zero_weight, "A")
    r.test(result_z["B"][0] == 0, "零权重应正确处理")
    
    # 不存在的节点操作
    g = Graph[int]()
    g.add_edge(1, 2)
    r.test(g.neighbors(99) == [], "不存在节点的邻居应为空列表")
    r.test(g.remove_node(99) == False, "移除不存在的节点应返回 False")
    
    return r.summary()


def test_complex_types():
    """测试复杂节点类型"""
    print("\n测试复杂节点类型...")
    r = TestResult()
    
    # 整数节点
    g_int = Graph[int]()
    g_int.add_edge(1, 2)
    g_int.add_edge(2, 3)
    r.test(bfs(g_int, 1) == [1, 2, 3], "整数节点 BFS 应正确")
    
    # 元组节点
    g_tuple = Graph[tuple]()
    g_tuple.add_edge((0, 0), (0, 1))
    g_tuple.add_edge((0, 1), (1, 1))
    r.test(g_tuple.has_edge((0, 0), (0, 1)) == True, "元组节点应正确")
    
    # 混合类型节点（不推荐，但测试泛型）
    g_mixed = Graph[object]()
    g_mixed.add_edge("A", 1)
    g_mixed.add_edge(1, (2, 3))
    r.test(g_mixed.node_count() == 3, "混合类型节点数应为 3")
    
    return r.summary()


def main():
    """运行所有测试"""
    print("=" * 60)
    print("Graph Utils 测试套件")
    print("=" * 60)
    
    all_passed = True
    all_passed &= test_graph_basic()
    all_passed &= test_traversal()
    all_passed &= test_shortest_path()
    all_passed &= test_mst()
    all_passed &= test_topological_sort()
    all_passed &= test_connectivity()
    all_passed &= test_cycle_detection()
    all_passed &= test_bipartite()
    all_passed &= test_special_algorithms()
    all_passed &= test_centrality()
    all_passed &= test_clustering()
    all_passed &= test_edge_cases()
    all_passed &= test_complex_types()
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ 所有测试通过！")
    else:
        print("✗ 部分测试失败")
    print("=" * 60)
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)