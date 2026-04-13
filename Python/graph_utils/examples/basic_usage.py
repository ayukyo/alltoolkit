"""
Graph Utils 使用示例

演示图数据结构和算法的基本用法
"""

from mod import (
    Graph, GraphType, Edge,
    bfs, dfs, dfs_iterative,
    dijkstra, bellman_ford, floyd_warshall,
    kruskal, prim,
    topological_sort, topological_sort_dfs,
    connected_components, strongly_connected_components,
    has_cycle, find_cycle,
    is_bipartite,
    find_eulerian_path, has_eulerian_path, has_eulerian_circuit,
    is_tree, graph_statistics,
    reverse_graph, get_isolated_vertices,
    get_articulation_points, get_bridges,
    create_graph, shortest_path
)


def example_1_basic_operations():
    """示例 1：基本操作"""
    print("\n=== 示例 1：基本操作 ===")
    
    # 创建无向图
    graph = Graph()
    
    # 添加顶点
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_vertex('C')
    
    # 添加带权边
    graph.add_edge('A', 'B', 5)
    graph.add_edge('B', 'C', 3)
    graph.add_edge('A', 'C', 10)
    
    print(f"顶点数量: {graph.vertex_count}")
    print(f"边数量: {graph.edge_count}")
    print(f"顶点列表: {graph.vertices}")
    print(f"边列表: {[(e.source, e.target, e.weight) for e in graph.edges]}")
    
    # 查询
    print(f"存在边 A-B: {graph.has_edge('A', 'B')}")
    print(f"边 A-B 权重: {graph.get_edge_weight('A', 'B')}")
    print(f"A 的邻居: {graph.get_neighbors('A')}")
    print(f"A 的度数: {graph.get_degree('A')}")


def example_2_directed_graph():
    """示例 2：有向图"""
    print("\n=== 示例 2：有向图 ===")
    
    # 创建有向图
    graph = Graph(GraphType.DIRECTED)
    
    # 添加边：表示依赖关系（课程依赖）
    graph.add_edge('数学基础', '高等数学')
    graph.add_edge('高等数学', '线性代数')
    graph.add_edge('高等数学', '概率论')
    graph.add_edge('线性代数', '机器学习')
    graph.add_edge('概率论', '机器学习')
    
    print(f"顶点数量: {graph.vertex_count}")
    print(f"边数量: {graph.edge_count}")
    
    # 查询度数
    print(f"'高等数学' 出度: {graph.get_out_degree('高等数学')}")
    print(f"'机器学习' 入度: {graph.get_in_degree('机器学习')}")
    
    # 拓扑排序
    topo_order = topological_sort(graph)
    print(f"拓扑排序结果: {topo_order}")
    print("推荐学习顺序: " + " -> ".join(topo_order))


def example_3_graph_traversal():
    """示例 3：图遍历"""
    print("\n=== 示例 3：图遍历 ===")
    
    # 创建社交网络图
    graph = Graph()
    graph.add_edge('Alice', 'Bob')
    graph.add_edge('Alice', 'Charlie')
    graph.add_edge('Bob', 'David')
    graph.add_edge('Charlie', 'David')
    graph.add_edge('David', 'Eve')
    
    print("社交网络结构:")
    print("    Alice")
    print("   /    \\")
    print(" Bob   Charlie")
    print("   \\    /")
    print("   David")
    print("    |")
    print("   Eve")
    
    # BFS（广度优先）
    bfs_result = bfs(graph, 'Alice')
    print(f"BFS 遍历顺序: {bfs_result}")
    
    # DFS（深度优先）
    dfs_result = dfs(graph, 'Alice')
    print(f"DFS 遍历顺序: {dfs_result}")
    
    # 使用回调函数
    visited_order = []
    bfs(graph, 'Alice', visit=lambda v: visited_order.append(v))
    print(f"BFS 回调访问顺序: {visited_order}")


def example_4_shortest_path():
    """示例 4：最短路径算法"""
    print("\n=== 示例 4：最短路径算法 ===")
    
    # 创建城市距离图
    graph = Graph()
    graph.add_edge('北京', '上海', 1200)
    graph.add_edge('北京', '广州', 1900)
    graph.add_edge('上海', '广州', 1300)
    graph.add_edge('上海', '深圳', 1200)
    graph.add_edge('广州', '深圳', 100)
    
    print("城市距离图:")
    print("  北京 --1200km-- 上海")
    print("   |               |")
    print("1900km          1200km")
    print("   |               |")
    print("  广州 --100km-- 深圳")
    
    # Dijkstra 算法 - 单点到单点
    result = shortest_path(graph, '北京', '深圳')
    print(f"\n北京到深圳最短路径:")
    print(f"  路径: {' -> '.join(result.path)}")
    print(f"  总距离: {result.distance}km")
    
    # Dijkstra 算法 - 单点到所有点
    all_paths = dijkstra(graph, '北京')
    print("\n从北京出发到各城市的最短距离:")
    for city, path_result in all_paths.items():
        if path_result.found:
            print(f"  到 {city}: {path_result.distance}km")
    
    # Floyd-Warshall 算法 - 所有最短路径
    distances, _ = floyd_warshall(graph)
    print("\n所有城市间的最短距离矩阵:")
    cities = ['北京', '上海', '广州', '深圳']
    print("     " + "  ".join(f"{c:>8}" for c in cities))
    for from_city in cities:
        row = [f"{int(distances[from_city][to_city]):>8}" for to_city in cities]
        print(f"{from_city:>5} " + " ".join(row))


def example_5_minimum_spanning_tree():
    """示例 5：最小生成树"""
    print("\n=== 示例 5：最小生成树 ===")
    
    # 创建网络成本图
    graph = Graph()
    graph.add_edge('A', 'B', 4)
    graph.add_edge('A', 'C', 3)
    graph.add_edge('B', 'C', 5)
    graph.add_edge('B', 'D', 6)
    graph.add_edge('C', 'D', 7)
    graph.add_edge('D', 'E', 8)
    graph.add_edge('B', 'E', 2)
    
    print("网络成本图:")
    print("   A ---4--- B")
    print("   |         |")
    print("   3         6")
    print("   |    5    |")
    print("   C         D")
    print("        \\   /")
    print("          7")
    print("           |")
    print("           E (通过 B-E=2 连接)")
    
    # Kruskal 算法
    kruskal_result = kruskal(graph)
    print("\nKruskal 最小生成树:")
    print(f"  边: {[(e.source, e.target, e.weight) for e in kruskal_result.edges]}")
    print(f"  总成本: {kruskal_result.total_weight}")
    
    # Prim 算法
    prim_result = prim(graph)
    print("\nPrim 最小生成树:")
    print(f"  边: {[(e.source, e.target, e.weight) for e in prim_result.edges]}")
    print(f"  总成本: {prim_result.total_weight}")


def example_6_connected_components():
    """示例 6：连通分量"""
    print("\n=== 示例 6：连通分量 ===")
    
    # 创建有多个连通分量的图
    graph = Graph()
    # 分量 1
    graph.add_edge('A', 'B')
    graph.add_edge('B', 'C')
    # 分量 2
    graph.add_edge('D', 'E')
    graph.add_edge('E', 'F')
    # 分量 3（孤立顶点）
    graph.add_vertex('G')
    
    print("图结构:")
    print("  分量1: A-B-C")
    print("  分量2: D-E-F")
    print("  分量3: G (孤立)")
    
    result = connected_components(graph)
    print(f"\n连通分量数量: {result.count}")
    print(f"是否连通: {result.is_connected}")
    print("各分量:")
    for i, comp in enumerate(result.components, 1):
        print(f"  分量{i}: {sorted(comp)}")


def example_7_cycle_detection():
    """示例 7：环检测"""
    print("\n=== 示例 7：环检测 ===")
    
    # 无环图（树）
    tree_graph = Graph()
    tree_graph.add_edge('A', 'B')
    tree_graph.add_edge('B', 'C')
    tree_graph.add_edge('B', 'D')
    
    print("树结构（无环）:")
    print("    A")
    print("    |")
    print("    B")
    print("   / \\")
    print("  C   D")
    
    print(f"存在环: {has_cycle(tree_graph)}")
    print(f"是树: {is_tree(tree_graph)}")
    
    # 有环图
    cycle_graph = Graph()
    cycle_graph.add_edge('A', 'B')
    cycle_graph.add_edge('B', 'C')
    cycle_graph.add_edge('C', 'A')
    
    print("\n三角形结构（有环）:")
    print("  A -- B")
    print("   \\  /")
    print("    C")
    
    print(f"存在环: {has_cycle(cycle_graph)}")
    cycle = find_cycle(cycle_graph)
    if cycle:
        print(f"环路径: {' -> '.join(cycle)}")


def example_8_bipartite_detection():
    """示例 8：二分图检测"""
    print("\n=== 示例 8：二分图检测 ===")
    
    # 二分图（可以进行任务分配）
    bipartite_graph = Graph()
    # 工人组
    # 任务组
    bipartite_graph.add_edge('工人A', '任务1')
    bipartite_graph.add_edge('工人A', '任务2')
    bipartite_graph.add_edge('工人B', '任务1')
    bipartite_graph.add_edge('工人B', '任务3')
    bipartite_graph.add_edge('工人C', '任务2')
    bipartite_graph.add_edge('工人C', '任务3')
    
    print("任务分配图:")
    print("  工人A --- 任务1")
    print("      \\-- 任务2")
    print("  工人B --- 任务1")
    print("      \\-- 任务3")
    print("  工人C --- 任务2")
    print("      \\-- 任务3")
    
    is_bip, coloring = is_bipartite(bipartite_graph)
    print(f"\n是二分图: {is_bip}")
    
    if coloring:
        print("分组结果:")
        group0 = [v for v, c in coloring.items() if c == 0]
        group1 = [v for v, c in coloring.items() if c == 1]
        print(f"  组0: {sorted(group0)}")
        print(f"  组1: {sorted(group1)}")


def example_9_eulerian_path():
    """示例 9：欧拉路径"""
    print("\n=== 示例 9：欧拉路径 ===")
    
    # 七桥问题简化版
    graph = Graph()
    graph.add_edge('A', 'B')
    graph.add_edge('A', 'C')
    graph.add_edge('A', 'D')
    graph.add_edge('B', 'C')
    graph.add_edge('C', 'D')
    graph.add_edge('D', 'B')  # 添加额外边使其有欧拉路径
    
    print("图结构:")
    print("  A 连接 B, C, D")
    print("  B 连接 A, C, D")
    print("  C 连接 A, B, D")
    print("  D 连接 A, B, C")
    
    print(f"存在欧拉路径: {has_eulerian_path(graph)}")
    print(f"存在欧拉回路: {has_eulerian_circuit(graph)}")
    
    if has_eulerian_path(graph):
        path = find_eulerian_path(graph)
        print(f"欧拉路径: {' -> '.join(path)}")


def example_10_topological_sort():
    """示例 10：拓扑排序"""
    print("\n=== 示例 10：拓扑排序 ===")
    
    # 项目依赖关系
    graph = Graph(GraphType.DIRECTED)
    graph.add_edge('设计', '开发')
    graph.add_edge('设计', '数据库设计')
    graph.add_edge('数据库设计', '开发')
    graph.add_edge('开发', '测试')
    graph.add_edge('测试', '部署')
    graph.add_edge('部署', '上线')
    
    print("项目依赖图:")
    print("  设计 -> 开发 -> 测试 -> 部署 -> 上线")
    print("  设计 -> 数据库设计 -> 开发")
    
    # Kahn 算法
    order = topological_sort(graph)
    if order:
        print("\n项目执行顺序 (Kahn 算法):")
        print("  " + " -> ".join(order))
    
    # DFS 算法
    order_dfs = topological_sort_dfs(graph)
    if order_dfs:
        print("\n项目执行顺序 (DFS 算法):")
        print("  " + " -> ".join(order_dfs))


def example_11_graph_statistics():
    """示例 11：图统计信息"""
    print("\n=== 示例 11：图统计信息 ===")
    
    # 创建一个复杂图
    graph = Graph()
    graph.add_edge('A', 'B', 5)
    graph.add_edge('A', 'C', 3)
    graph.add_edge('B', 'C', 2)
    graph.add_edge('B', 'D', 4)
    graph.add_edge('C', 'D', 6)
    
    stats = graph_statistics(graph)
    
    print("图统计信息:")
    print(f"  顶点数量: {stats['vertex_count']}")
    print(f"  边数量: {stats['edge_count']}")
    print(f"  是否有向: {stats['is_directed']}")
    print(f"  是否连通: {stats['is_connected']}")
    print(f"  是否有环: {stats['has_cycle']}")
    print(f"  是否为树: {stats['is_tree']}")
    print(f"  是否为二分图: {stats['is_bipartite']}")
    print(f"  最小度数: {stats['min_degree']}")
    print(f"  最大度数: {stats['max_degree']}")
    print(f"  平均度数: {stats['avg_degree']:.2f}")


def example_12_articulation_points_and_bridges():
    """示例 12：割点和桥"""
    print("\n=== 示例 12：割点和桥 ===")
    
    # 创建网络拓扑图
    graph = Graph()
    graph.add_edge('核心路由器', '交换机A')
    graph.add_edge('核心路由器', '交换机B')
    graph.add_edge('交换机A', '服务器1')
    graph.add_edge('交换机A', '服务器2')
    graph.add_edge('交换机B', '服务器3')
    graph.add_edge('服务器1', '服务器2')  # 双机互备
    
    print("网络拓扑:")
    print("        核心路由器")
    print("         /    \\")
    print("     交换机A  交换机B")
    print("       / \\      |")
    print("  服务器1-服务器2 服务器3")
    
    # 找割点
    aps = get_articulation_points(graph)
    print(f"\n关键节点（割点）: {sorted(aps)}")
    print("解释：删除这些节点会导致网络断开")
    
    # 找桥
    bridges = get_bridges(graph)
    print(f"\n关键链路（桥）: {[(e.source, e.target) for e in bridges]}")
    print("解释：删除这些链路会导致网络断开")


def example_13_negative_weights():
    """示例 13：负权边（Bellman-Ford）"""
    print("\n=== 示例 13：负权边处理 ===")
    
    # 创建带负权边的图（代表收益）
    graph = Graph(GraphType.DIRECTED)
    graph.add_edge('投资A', '投资B', -5)  # 投资A转B有收益
    graph.add_edge('投资B', '投资C', -3)
    graph.add_edge('投资C', '投资D', -2)
    graph.add_edge('投资A', '投资D', 2)  # 直接投资有成本
    
    print("投资收益图（负数表示收益）:")
    print("  投资A -> 投资B (收益 5)")
    print("  投资B -> 投资C (收益 3)")
    print("  投资C -> 投资D (收益 2)")
    print("  投资A -> 投资D (成本 2)")
    
    distances, _, has_negative_cycle = bellman_ford(graph, '投资A')
    
    print(f"\n存在负收益循环: {has_negative_cycle}")
    print("从投资A出发的最小成本路径:")
    for target, dist in distances.items():
        if dist != float('inf'):
            print(f"  到 {target}: {'收益' if dist < 0 else '成本'} {abs(int(dist))}")


def example_14_create_graph_quick():
    """示例 14：快捷创建图"""
    print("\n=== 示例 14：快捷创建图 ===")
    
    # 从边列表创建图
    edges = [
        ('北京', '上海', 1200),
        ('上海', '杭州', 180),
        ('杭州', '南京', 280),
        ('南京', '北京', 1000),
    ]
    
    graph = create_graph(edges=edges)
    
    print("快捷创建的图:")
    print(f"  顶点: {sorted(graph.vertices)}")
    print(f"  边: {[(e.source, e.target, e.weight) for e in graph.edges]}")
    
    # 查找最短路径
    result = shortest_path(graph, '北京', '杭州')
    print(f"\n北京到杭州最短路径:")
    print(f"  {' -> '.join(result.path)}")
    print(f"  距离: {result.distance}km")


def example_15_strongly_connected_components():
    """示例 15：强连通分量"""
    print("\n=== 示例 15：强连通分量 ===")
    
    # 创建网页链接图
    graph = Graph(GraphType.DIRECTED)
    graph.add_edge('主页', '产品页')
    graph.add_edge('产品页', '详情页')
    graph.add_edge('详情页', '主页')  # 形成强连通
    graph.add_edge('主页', '关于页')
    graph.add_edge('关于页', '联系方式')
    
    print("网页链接结构:")
    print("  主页 <-> 产品页 <-> 详情页 (强连通)")
    print("  主页 -> 关于页 -> 联系方式")
    
    scc = strongly_connected_components(graph)
    
    print(f"\n强连通分量数量: {scc.count}")
    print("各强连通分量:")
    for i, comp in enumerate(scc.components, 1):
        print(f"  SCC{i}: {sorted(comp)}")


if __name__ == '__main__':
    print("=" * 60)
    print("Graph Utils 使用示例")
    print("=" * 60)
    
    example_1_basic_operations()
    example_2_directed_graph()
    example_3_graph_traversal()
    example_4_shortest_path()
    example_5_minimum_spanning_tree()
    example_6_connected_components()
    example_7_cycle_detection()
    example_8_bipartite_detection()
    example_9_eulerian_path()
    example_10_topological_sort()
    example_11_graph_statistics()
    example_12_articulation_points_and_bridges()
    example_13_negative_weights()
    example_14_create_graph_quick()
    example_15_strongly_connected_components()
    
    print("\n" + "=" * 60)
    print("所有示例完成！")
    print("=" * 60)