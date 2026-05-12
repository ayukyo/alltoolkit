"""
图论算法工具模块使用示例

演示：
1. 图的创建和基本操作
2. 遍历算法（DFS、BFS）
3. 最短路径算法（Dijkstra、Bellman-Ford、Floyd-Warshall）
4. 最小生成树（Kruskal、Prim）
5. 拓扑排序
6. 连通性分析
7. 环检测
8. 二分图检测
9. 图度量
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Graph, dfs, bfs, dijkstra, get_shortest_path, bellman_ford, floyd_warshall,
    kruskal, prim, topological_sort, is_connected, find_connected_components,
    find_strongly_connected_components, has_cycle, is_bipartite, get_bipartition,
    get_diameter, get_radius, get_center, to_adjacency_matrix, from_adjacency_matrix,
    create_complete_graph, create_path_graph, create_cycle_graph, create_star_graph
)


def example_1_basic_operations():
    """示例1：图的创建和基本操作"""
    print("\n" + "=" * 60)
    print("示例1：图的创建和基本操作")
    print("=" * 60)
    
    # 创建无向无权图
    print("\n【无向无权图】")
    g = Graph()
    g.add_edge('北京', '上海')
    g.add_edge('北京', '广州')
    g.add_edge('上海', '深圳')
    g.add_edge('广州', '深圳')
    g.add_edge('深圳', '香港')
    
    print(f"图信息: {g}")
    print(f"顶点数: {g.get_vertex_count()}")
    print(f"边数: {g.get_edge_count()}")
    print(f"北京的邻居: {list(g.get_neighbors('北京').keys())}")
    print(f"北京-上海是否有边: {g.has_edge('北京', '上海')}")
    print(f"上海-北京是否有边: {g.has_edge('上海', '北京')} (无向图双向)")
    
    # 创建有向带权图
    print("\n【有向带权图】")
    dg = Graph(directed=True, weighted=True)
    dg.add_edge('A', 'B', 5)
    dg.add_edge('A', 'C', 3)
    dg.add_edge('B', 'D', 2)
    dg.add_edge('C', 'D', 4)
    dg.add_edge('D', 'E', 1)
    
    print(f"图信息: {dg}")
    print(f"边 A->B 的权重: {dg.get_edge_weight('A', 'B')}")
    print(f"边 B->A 的权重: {dg.get_edge_weight('B', 'A')} (有向图单向)")
    
    # 获取所有边
    print("\n【所有边】")
    for u, v, w in dg.get_edges():
        print(f"  {u} --{w}--> {v}")


def example_2_traversal():
    """示例2：遍历算法"""
    print("\n" + "=" * 60)
    print("示例2：遍历算法（DFS 和 BFS）")
    print("=" * 60)
    
    # 创建树形结构
    #         1
    #       / | \
    #      2  3  4
    #     /|     |
    #    5 6     7
    g = Graph()
    edges = [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (4, 7)]
    for u, v in edges:
        g.add_edge(u, v)
    
    print("\n【图结构】")
    print("         1")
    print("       / | \\")
    print("      2  3  4")
    print("     /|     |")
    print("    5 6     7")
    
    print("\n【深度优先搜索 DFS】")
    dfs_result = dfs(g, 1)
    print(f"遍历顺序: {' -> '.join(map(str, dfs_result))}")
    
    print("\n【广度优先搜索 BFS】")
    bfs_result = bfs(g, 1)
    print(f"遍历顺序: {' -> '.join(map(str, bfs_result))}")
    
    print("\n【BFS 层级距离】")
    from mod import bfs_with_distance
    _, distances = bfs_with_distance(g, 1)
    for vertex in sorted(distances.keys()):
        print(f"  节点 {vertex} 到根节点距离: {distances[vertex]}")


def example_3_shortest_path():
    """示例3：最短路径算法"""
    print("\n" + "=" * 60)
    print("示例3：最短路径算法")
    print("=" * 60)
    
    # 创建城市交通图
    print("\n【城市交通图 - 正权重】")
    #     北京 ---300-- 上海
    #       |            |
    #      500          200
    #       |            |
    #     广州 ---400-- 深圳
    g = Graph(weighted=True)
    g.add_edge('北京', '上海', 300)
    g.add_edge('北京', '广州', 500)
    g.add_edge('上海', '深圳', 200)
    g.add_edge('广州', '深圳', 400)
    
    print("\n【Dijkstra 最短路径】")
    distances, predecessors = dijkstra(g, '北京')
    print(f"从北京出发到各城市的最短距离:")
    for city, dist in sorted(distances.items()):
        print(f"  {city}: {dist}km")
    
    path = get_shortest_path(g, '北京', '深圳')
    print(f"\n北京到深圳的最短路径: {' -> '.join(path)}")
    
    # 负权边示例
    print("\n【带负权边的图 - Bellman-Ford】")
    # 有时某些路径有"奖励"，相当于负权重
    bg = Graph(directed=True, weighted=True)
    bg.add_edge('A', 'B', 4)
    bg.add_edge('A', 'C', 2)
    bg.add_edge('B', 'D', 3)
    bg.add_edge('C', 'B', -1)  # 有奖励的路径
    bg.add_edge('C', 'D', 5)
    
    distances, _, has_neg_cycle = bellman_ford(bg, 'A')
    print(f"是否存在负环: {has_neg_cycle}")
    print(f"从 A 出发的最短距离:")
    for v, dist in sorted(distances.items()):
        if dist != float('inf'):
            print(f"  {v}: {dist}")
    
    # 全源最短路径
    print("\n【Floyd-Warshall 全源最短路径】")
    fg = Graph(weighted=True)
    fg.add_edge('A', 'B', 3)
    fg.add_edge('A', 'C', 8)
    fg.add_edge('B', 'C', 2)
    fg.add_edge('B', 'D', 5)
    fg.add_edge('C', 'D', 1)
    
    dist_matrix = floyd_warshall(fg)
    print("各城市间最短距离矩阵:")
    vertices = sorted(fg.get_vertices())
    print("     " + "  ".join(f"{v:>5}" for v in vertices))
    for u in vertices:
        row = [f"{dist_matrix[u][v]:>5.0f}" if dist_matrix[u][v] != float('inf') else "  inf" for v in vertices]
        print(f"{u:>5} " + "  ".join(row))


def example_4_minimum_spanning_tree():
    """示例4：最小生成树"""
    print("\n" + "=" * 60)
    print("示例4：最小生成树")
    print("=" * 60)
    
    # 创建网络连接图
    #     A ---2--- B
    #     |\       /|
    #     1 \     / 4
    #     |  \   /  |
    #     C   \ /   D
    #     5   \|/   3
    #     |   / \   |
    #     E--6---F--7
    g = Graph(weighted=True)
    g.add_edge('A', 'B', 2)
    g.add_edge('A', 'C', 1)
    g.add_edge('A', 'F', 8)
    g.add_edge('B', 'D', 4)
    g.add_edge('C', 'E', 5)
    g.add_edge('D', 'F', 3)
    g.add_edge('E', 'F', 6)
    
    print("\n【Kruskal 算法】")
    edges, total = kruskal(g)
    print("最小生成树的边:")
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        print(f"  {u} -- {v}: {w}")
    print(f"总权重: {total}")
    
    print("\n【Prim 算法】")
    edges, total = prim(g, start='A')
    print("最小生成树的边:")
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        print(f"  {u} -- {v}: {w}")
    print(f"总权重: {total}")


def example_5_topological_sort():
    """示例5：拓扑排序"""
    print("\n" + "=" * 60)
    print("示例5：拓扑排序（任务调度）")
    print("=" * 60)
    
    # 课程依赖关系
    # CS101 -> CS201 -> CS301
    # CS101 -> CS202 -> CS301
    # MATH101 -> CS202
    g = Graph(directed=True)
    g.add_edge('CS101', 'CS201')
    g.add_edge('CS101', 'CS202')
    g.add_edge('CS201', 'CS301')
    g.add_edge('CS202', 'CS301')
    g.add_edge('MATH101', 'CS202')
    
    print("\n【课程依赖图】")
    print("CS101 -> CS201 -> CS301")
    print("CS101 -> CS202 -> CS301")
    print("MATH101 -> CS202")
    
    result = topological_sort(g)
    print("\n【拓扑排序结果（学习顺序）】")
    for i, course in enumerate(result, 1):
        print(f"  第{i}学期: {course}")


def example_6_connectivity():
    """示例6：连通性分析"""
    print("\n" + "=" * 60)
    print("示例6：连通性分析")
    print("=" * 60)
    
    # 连通图
    print("\n【连通图】")
    g1 = Graph()
    for u, v in [('A', 'B'), ('B', 'C'), ('C', 'D')]:
        g1.add_edge(u, v)
    print(f"图是否连通: {is_connected(g1)}")
    
    # 非连通图
    print("\n【非连通图】")
    g2 = Graph()
    g2.add_edge('A', 'B')
    g2.add_edge('B', 'C')
    g2.add_edge('D', 'E')  # 独立分量
    
    components = find_connected_components(g2)
    print(f"连通分量数量: {len(components)}")
    for i, comp in enumerate(components, 1):
        print(f"  分量 {i}: {comp}")
    
    # 强连通分量
    print("\n【强连通分量（有向图）】")
    #     0 -> 1 -> 2
    #     ^    |
    #     |    v
    #     4 <- 3
    #     |
    #     v
    #     5
    g3 = Graph(directed=True)
    g3.add_edge(0, 1)
    g3.add_edge(1, 2)
    g3.add_edge(2, 3)
    g3.add_edge(3, 4)
    g3.add_edge(4, 0)  # 环 0-1-2-3-4
    g3.add_edge(4, 5)  # 5 单独
    
    sccs = find_strongly_connected_components(g3)
    print(f"强连通分量数量: {len(sccs)}")
    for i, scc in enumerate(sccs, 1):
        print(f"  分量 {i}: {scc}")


def example_7_cycle_detection():
    """示例7：环检测"""
    print("\n" + "=" * 60)
    print("示例7：环检测")
    print("=" * 60)
    
    # 无向图有环
    print("\n【无向图检测环】")
    g1 = Graph()
    g1.add_edge(1, 2)
    g1.add_edge(2, 3)
    g1.add_edge(3, 1)  # 环
    print(f"图是否有环: {has_cycle(g1)}")
    
    # 无向图无环（树）
    print("\n【无向图无环（树）】")
    g2 = Graph()
    g2.add_edge(1, 2)
    g2.add_edge(2, 3)
    g2.add_edge(2, 4)
    print(f"图是否有环: {has_cycle(g2)}")
    
    # 有向图检测
    print("\n【有向图检测环】")
    g3 = Graph(directed=True)
    g3.add_edge('A', 'B')
    g3.add_edge('B', 'C')
    g3.add_edge('C', 'A')  # 环
    print(f"图是否有环: {has_cycle(g3)}")


def example_8_bipartite():
    """示例8：二分图检测"""
    print("\n" + "=" * 60)
    print("示例8：二分图检测")
    print("=" * 60)
    
    # 二分图 - 社交匹配
    print("\n【二分图示例 - 用户与兴趣匹配】")
    g = Graph()
    # 左侧：用户
    # 右侧：兴趣
    g.add_edge('用户A', '音乐')
    g.add_edge('用户A', '阅读')
    g.add_edge('用户B', '运动')
    g.add_edge('用户B', '音乐')
    g.add_edge('用户C', '阅读')
    g.add_edge('用户C', '运动')
    
    print(f"是否为二分图: {is_bipartite(g)}")
    
    set_a, set_b = get_bipartition(g)
    print(f"分组 A: {set_a}")
    print(f"分组 B: {set_b}")
    
    # 非二分图
    print("\n【非二分图 - 奇数环】")
    g2 = Graph()
    g2.add_edge(1, 2)
    g2.add_edge(2, 3)
    g2.add_edge(3, 1)  # 三角形
    print(f"是否为二分图: {is_bipartite(g2)}")


def example_9_graph_metrics():
    """示例9：图度量"""
    print("\n" + "=" * 60)
    print("示例9：图度量")
    print("=" * 60)
    
    # 创建社交网络图
    g = Graph()
    # 中心人物 A 连接多人
    g.add_edge('Alice', 'Bob')
    g.add_edge('Alice', 'Carol')
    g.add_edge('Alice', 'David')
    g.add_edge('Bob', 'Carol')
    g.add_edge('Carol', 'Eve')
    g.add_edge('David', 'Eve')
    
    print("\n【社交网络分析】")
    print(f"直径（最长最短路径）: {get_diameter(g)}")
    print(f"半径（最小离心率）: {get_radius(g)}")
    print(f"中心节点（离心率等于半径）: {get_center(g)}")
    
    from mod import get_degree_sequence
    degrees = get_degree_sequence(g)
    print(f"度序列（降序）: {degrees}")


def example_10_factory_functions():
    """示例10：工厂函数创建特殊图"""
    print("\n" + "=" * 60)
    print("示例10：工厂函数创建特殊图")
    print("=" * 60)
    
    print("\n【完全图 K5】")
    complete = create_complete_graph(5)
    print(f"{complete}")
    print(f"每个顶点的度: {complete.get_degree(0)} (n-1=4)")
    
    print("\n【路径图 P5】")
    path = create_path_graph(5)
    print(f"{path}")
    print(f"顶点: {sorted(path.get_vertices())}")
    
    print("\n【环图 C5】")
    cycle = create_cycle_graph(5)
    print(f"{cycle}")
    print(f"是否有环: {has_cycle(cycle)}")
    
    print("\n【星图 S4】")
    star = create_star_graph(4)
    print(f"{star}")
    print(f"中心顶点的度: {star.get_degree(0)}")
    print(f"叶子顶点的度: {star.get_degree(1)}")


def example_11_adjacency_matrix():
    """示例11：邻接矩阵转换"""
    print("\n" + "=" * 60)
    print("示例11：邻接矩阵转换")
    print("=" * 60)
    
    # 创建图
    g = Graph(weighted=True)
    g.add_edge(0, 1, 2)
    g.add_edge(1, 2, 3)
    g.add_edge(2, 0, 1)
    
    print("\n【原图】")
    print(g)
    
    print("\n【转换为邻接矩阵】")
    matrix, vertices = to_adjacency_matrix(g)
    print("顶点顺序:", vertices)
    print("矩阵:")
    for row in matrix:
        print("  ", [f"{x:.0f}" if x != float('inf') else "∞" for x in row])
    
    print("\n【从邻接矩阵重建图】")
    g2 = from_adjacency_matrix(matrix, vertices, weighted=True)
    print(g2)
    print(f"边数量: {g2.get_edge_count()}")


def main():
    """运行所有示例"""
    example_1_basic_operations()
    example_2_traversal()
    example_3_shortest_path()
    example_4_minimum_spanning_tree()
    example_5_topological_sort()
    example_6_connectivity()
    example_7_cycle_detection()
    example_8_bipartite()
    example_9_graph_metrics()
    example_10_factory_functions()
    example_11_adjacency_matrix()
    
    print("\n" + "=" * 60)
    print("所有示例演示完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()