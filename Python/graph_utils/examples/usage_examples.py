"""
Graph Utils 使用示例

展示图论算法的各种应用场景。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Graph, bfs, dfs,
    dijkstra, bellman_ford, floyd_warshall, get_path, shortest_path_bfs, all_paths,
    prim, kruskal,
    topological_sort,
    connected_components, strongly_connected_components,
    has_cycle, find_cycle,
    is_bipartite,
    articulation_points, bridges,
    degree_centrality, betweenness_centrality,
    clustering_coefficient, average_clustering_coefficient
)


def example_1_basic_operations():
    """示例1：图的基本操作"""
    print("\n" + "="*60)
    print("示例1：图的基本操作")
    print("="*60)
    
    # 创建无向图
    g = Graph[str]()
    
    # 添加边
    g.add_edge("北京", "上海", weight=1200)
    g.add_edge("北京", "广州", weight=1800)
    g.add_edge("上海", "广州", weight=1200)
    g.add_edge("上海", "深圳", weight=1000)
    g.add_edge("广州", "深圳", weight=150)
    
    print(f"节点数: {g.node_count()}")
    print(f"边数: {g.edge_count()}")
    print(f"节点列表: {g.get_nodes()}")
    
    # 获取邻居
    print("\n上海连接的城市:")
    for neighbor, distance in g.neighbors("上海"):
        print(f"  -> {neighbor}: {distance}km")
    
    # 检查连通性
    print(f"\n北京-上海是否连通: {g.has_edge('北京', '上海')}")
    print(f"上海-北京是否连通: {g.has_edge('上海', '北京')}")


def example_2_traversal():
    """示例2：图的遍历"""
    print("\n" + "="*60)
    print("示例2：图的遍历（BFS/DFS）")
    print("="*60)
    
    # 创建社交网络图
    g = Graph[str]()
    g.add_edge("Alice", "Bob")
    g.add_edge("Alice", "Carol")
    g.add_edge("Bob", "David")
    g.add_edge("Carol", "Eve")
    g.add_edge("David", "Eve")
    g.add_edge("Eve", "Frank")
    
    # BFS - 适合找最近的朋友
    print("BFS遍历（从Alice开始）:")
    bfs_result = bfs(g, "Alice")
    for i, person in enumerate(bfs_result):
        print(f"  第{i+1}层: {person}")
    
    # DFS - 适合深入探索
    print("\nDFS遍历（从Alice开始）:")
    dfs_result = dfs(g, "Alice")
    print(f"  访问顺序: {' -> '.join(dfs_result)}")


def example_3_shortest_path():
    """示例3：最短路径算法"""
    print("\n" + "="*60)
    print("示例3：最短路径算法")
    print("="*60)
    
    # 创建交通网络（有向图）
    g = Graph[str](directed=True)
    g.add_edge("A", "B", weight=4)
    g.add_edge("A", "C", weight=2)
    g.add_edge("B", "C", weight=1)
    g.add_edge("B", "D", weight=5)
    g.add_edge("C", "D", weight=8)
    g.add_edge("C", "E", weight=10)
    g.add_edge("D", "E", weight=2)
    
    # Dijkstra算法
    print("Dijkstra最短路径（从A开始）:")
    result = dijkstra(g, "A")
    
    for dest, (dist, pred) in result.items():
        if dist != float('inf'):
            print(f"  A -> {dest}: 距离={dist}, 前驱={pred}")
    
    # 获取具体路径
    path = get_path({n: (d, p) for n, (d, p) in result.items()}, "A", "E")
    print(f"\n从A到E的路径: {' -> '.join(path)}")


def example_4_mst():
    """示例4：最小生成树"""
    print("\n" + "="*60)
    print("示例4：最小生成树")
    print("="*60)
    
    # 创建电网连接图
    g = Graph[str]()
    g.add_edge("城市1", "城市2", weight=10)
    g.add_edge("城市1", "城市3", weight=15)
    g.add_edge("城市1", "城市4", weight=20)
    g.add_edge("城市2", "城市3", weight=35)
    g.add_edge("城市2", "城市4", weight=25)
    g.add_edge("城市3", "城市4", weight=30)
    
    # Prim算法
    print("Prim算法最小生成树:")
    mst_prim = prim(g)
    total_cost = 0
    for u, v, w in mst_prim:
        print(f"  {u} -> {v}: {w}")
        total_cost += w
    print(f"总成本: {total_cost}")
    
    # Kruskal算法
    print("\nKruskal算法最小生成树:")
    mst_kruskal = kruskal(g)
    total_cost_k = 0
    for u, v, w in mst_kruskal:
        print(f"  {u} -> {v}: {w}")
        total_cost_k += w
    print(f"总成本: {total_cost_k}")


def example_5_topological_sort():
    """示例5：拓扑排序"""
    print("\n" + "="*60)
    print("示例5：拓扑排序（任务依赖）")
    print("="*60)
    
    # 创建任务依赖图
    g = Graph[str](directed=True)
    g.add_edge("编译", "测试")
    g.add_edge("测试", "打包")
    g.add_edge("打包", "部署")
    g.add_edge("写代码", "编译")
    g.add_edge("写代码", "单元测试")
    g.add_edge("单元测试", "测试")
    
    # 拓扑排序
    order = topological_sort(g)
    if order:
        print("任务执行顺序:")
        for i, task in enumerate(order):
            print(f"  {i+1}. {task}")
    else:
        print("存在循环依赖！")


def example_6_cycle_detection():
    """示例6：环检测"""
    print("\n" + "="*60)
    print("示例6：环检测")
    print("="*60)
    
    # 无环图（树）
    tree = Graph[int]()
    tree.add_edge(1, 2)
    tree.add_edge(1, 3)
    tree.add_edge(2, 4)
    tree.add_edge(2, 5)
    
    print(f"树是否有环: {has_cycle(tree)}")
    
    # 有环图
    cycle_graph = Graph[int]()
    cycle_graph.add_edge(1, 2)
    cycle_graph.add_edge(2, 3)
    cycle_graph.add_edge(3, 1)
    
    print(f"环图是否有环: {has_cycle(cycle_graph)}")
    
    # 找环路径
    cycle_path = find_cycle(cycle_graph)
    if cycle_path:
        print(f"环路径: {' -> '.join(map(str, cycle_path))}")


def example_7_connectivity():
    """示例7：连通性分析"""
    print("\n" + "="*60)
    print("示例7：连通性分析")
    print("="*60)
    
    # 创建有多个连通分量的图
    g = Graph[int]()
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(4, 5)
    g.add_edge(5, 6)
    g.add_node(7)  # 孤立节点
    
    # 连通分量
    components = connected_components(g)
    print(f"连通分量数量: {len(components)}")
    for i, comp in enumerate(components):
        print(f"  分量{i+1}: {comp}")
    
    # 强连通分量（有向图）
    dg = Graph[int](directed=True)
    dg.add_edge(1, 2)
    dg.add_edge(2, 3)
    dg.add_edge(3, 1)
    dg.add_edge(3, 4)
    dg.add_edge(4, 5)
    dg.add_edge(5, 4)
    
    sccs = strongly_connected_components(dg)
    print(f"\n强连通分量数量: {len(sccs)}")
    for i, scc in enumerate(sccs):
        print(f"  SCC{i+1}: {scc}")


def example_8_bipartite():
    """示例8：二分图检测"""
    print("\n" + "="*60)
    print("示例8：二分图检测")
    print("="*60)
    
    # 创建二分图（员工-部门关系）
    g = Graph[str]()
    employees = ["张三", "李四", "王五"]
    departments = ["研发部", "市场部", "财务部"]
    
    # 添加边（员工可以属于多个部门）
    g.add_edge("张三", "研发部")
    g.add_edge("张三", "市场部")
    g.add_edge("李四", "研发部")
    g.add_edge("李四", "财务部")
    g.add_edge("王五", "市场部")
    g.add_edge("王五", "财务部")
    
    is_bip, partition = is_bipartite(g)
    print(f"是否为二分图: {is_bip}")
    if partition:
        print(f"分区A（员工）: {partition[0]}")
        print(f"分区B（部门）: {partition[1]}")


def example_9_centrality():
    """示例9：中心性分析"""
    print("\n" + "="*60)
    print("示例9：中心性分析（社交网络重要性）")
    print("="*60)
    
    # 创建社交网络
    g = Graph[str]()
    g.add_edge("Alice", "Bob")
    g.add_edge("Alice", "Carol")
    g.add_edge("Alice", "David")
    g.add_edge("Alice", "Eve")  # Alice是核心人物
    g.add_edge("Bob", "Carol")
    g.add_edge("Carol", "David")
    g.add_edge("David", "Eve")
    
    # 度中心性
    dc = degree_centrality(g)
    print("度中心性:")
    for person, value in sorted(dc.items(), key=lambda x: -x[1]):
        print(f"  {person}: {value:.3f}")
    
    # 介数中心性
    bc = betweenness_centrality(g)
    print("\n介数中心性:")
    for person, value in sorted(bc.items(), key=lambda x: -x[1]):
        print(f"  {person}: {value:.3f}")


def example_10_clustering():
    """示例10：聚类系数"""
    print("\n" + "="*60)
    print("示例10：聚类系数（朋友关系的紧密程度）")
    print("="*60)
    
    # 创建三角网络（朋友圈）
    g = Graph[str]()
    # 完全三角形
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("C", "A")
    # 另一个三角形
    g.add_edge("D", "E")
    g.add_edge("E", "F")
    g.add_edge("F", "D")
    # 连接两个三角形
    g.add_edge("C", "D")
    
    # 聚类系数
    cc = clustering_coefficient(g)
    print("各节点聚类系数:")
    for node, value in cc.items():
        print(f"  {node}: {value:.3f}")
    
    # 平均聚类系数
    avg_cc = average_clustering_coefficient(g)
    print(f"\n平均聚类系数: {avg_cc:.3f}")


def example_11_articulation_bridges():
    """示例11：割点和桥"""
    print("\n" + "="*60)
    print("示例11：割点和桥（网络脆弱性分析）")
    print("="*60)
    
    # 创建网络拓扑
    g = Graph[str]()
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("C", "D")
    g.add_edge("D", "E")
    g.add_edge("E", "F")
    g.add_edge("B", "E")  # 添加冗余路径
    
    # 割点
    aps = articulation_points(g)
    print(f"割点（关键节点）: {aps}")
    
    # 桥
    bridges_list = bridges(g)
    print(f"桥（关键连接）: {bridges_list}")


def example_12_all_paths():
    """示例12：所有路径查找"""
    print("\n" + "="*60)
    print("示例12：所有路径查找")
    print("="*60)
    
    # 创建迷宫图
    g = Graph[str]()
    g.add_edge("入口", "A")
    g.add_edge("入口", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "C")
    g.add_edge("C", "D")
    g.add_edge("D", "出口")
    g.add_edge("C", "出口")
    
    # 查找所有路径
    paths = all_paths(g, "入口", "出口")
    print(f"从入口到出口的所有路径（共{len(paths)}条）:")
    for i, path in enumerate(paths):
        print(f"  路径{i+1}: {' -> '.join(path)}")


def main():
    """运行所有示例"""
    example_1_basic_operations()
    example_2_traversal()
    example_3_shortest_path()
    example_4_mst()
    example_5_topological_sort()
    example_6_cycle_detection()
    example_7_connectivity()
    example_8_bipartite()
    example_9_centrality()
    example_10_clustering()
    example_11_articulation_bridges()
    example_12_all_paths()
    
    print("\n" + "="*60)
    print("所有示例运行完成！")
    print("="*60)


if __name__ == "__main__":
    main()