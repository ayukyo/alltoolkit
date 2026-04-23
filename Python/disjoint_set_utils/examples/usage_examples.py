"""
disjoint_set_utils 使用示例

展示并查集在各种场景下的应用
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    DisjointSet, WeightedDisjointSet,
    connected_components, detect_cycle_undirected,
    minimum_spanning_tree_kruskal
)


def example_basic_operations():
    """基本操作示例"""
    print("=" * 60)
    print("1. 并查集基本操作")
    print("=" * 60)
    
    # 创建并查集
    ds = DisjointSet()
    
    # 添加元素
    for i in range(1, 6):
        ds.make_set(i)
    
    print(f"初始状态: {ds}")
    print(f"集合数量: {ds.set_count}")
    print()
    
    # 合并操作
    print("合并 1 和 2...")
    ds.union(1, 2)
    print(f"结果: {ds}")
    print()
    
    print("合并 3 和 4...")
    ds.union(3, 4)
    print(f"结果: {ds}")
    print()
    
    print("合并 2 和 3...")
    ds.union(2, 3)
    print(f"结果: {ds}")
    print()
    
    # 连通性检查
    print("连通性检查:")
    print(f"  1 和 4: {ds.connected(1, 4)}")  # True
    print(f"  1 和 5: {ds.connected(1, 5)}")  # False
    print()
    
    # 查询集合信息
    print("集合信息:")
    print(f"  所有集合: {ds.get_sets()}")
    print(f"  元素1所在集合: {ds.get_set(1)}")
    print(f"  集合大小: {ds.get_set_size(1)}")
    print()


def example_social_network():
    """社交网络好友圈示例"""
    print("=" * 60)
    print("2. 社交网络好友圈分析")
    print("=" * 60)
    
    # 用户列表
    users = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank']
    ds = DisjointSet(users)
    
    # 好友关系
    friendships = [
        ('Alice', 'Bob'),
        ('Bob', 'Charlie'),
        ('David', 'Eve'),
    ]
    
    print("建立好友关系:")
    for u, v in friendships:
        ds.union(u, v)
        print(f"  {u} <-> {v}")
    
    print()
    print("好友圈分析:")
    circles = ds.get_sets()
    for i, circle in enumerate(circles, 1):
        print(f"  好友圈 {i}: {circle}")
    
    print()
    print("好友关系检查:")
    print(f"  Alice 和 Charlie 是好友(间接): {ds.connected('Alice', 'Charlie')}")
    print(f"  Alice 和 David 是好友: {ds.connected('Alice', 'David')}")
    print()


def example_image_processing():
    """图像处理连通区域示例"""
    print("=" * 60)
    print("3. 图像处理 - 连通区域标记")
    print("=" * 60)
    
    # 模拟一个简单的二值图像 (1=前景, 0=背景)
    # 1 1 0 0 1
    # 1 0 0 1 0
    # 0 0 1 1 1
    
    image = [
        [1, 1, 0, 0, 1],
        [1, 0, 0, 1, 0],
        [0, 0, 1, 1, 1]
    ]
    
    rows, cols = 3, 5
    
    # 为每个前景像素创建集合
    ds = DisjointSet()
    
    def pos(r, c):
        return f"({r},{c})"
    
    # 初始化前景像素
    foreground = []
    for r in range(rows):
        for c in range(cols):
            if image[r][c] == 1:
                ds.make_set(pos(r, c))
                foreground.append(pos(r, c))
    
    # 合并相邻的前景像素
    directions = [(0, 1), (1, 0)]  # 只检查右和下
    
    for r in range(rows):
        for c in range(cols):
            if image[r][c] == 1:
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and image[nr][nc] == 1:
                        ds.union(pos(r, c), pos(nr, nc))
    
    print("原始图像:")
    for row in image:
        print(f"  {row}")
    
    print()
    print(f"连通区域数量: {ds.set_count}")
    
    components = ds.get_sets()
    for i, comp in enumerate(components, 1):
        print(f"  区域 {i}: {sorted(comp)}")
    
    print()


def example_network_connectivity():
    """网络连通性示例"""
    print("=" * 60)
    print("4. 网络连通性检测")
    print("=" * 60)
    
    # 服务器节点
    servers = ['Server-A', 'Server-B', 'Server-C', 'Server-D', 'Server-E']
    ds = DisjointSet(servers)
    
    # 网络连接
    connections = [
        ('Server-A', 'Server-B'),
        ('Server-B', 'Server-C'),
        ('Server-D', 'Server-E'),
    ]
    
    print("建立网络连接:")
    for u, v in connections:
        ds.union(u, v)
        print(f"  {u} <---> {v}")
    
    print()
    print("网络状态:")
    print(f"  连通分量数: {ds.set_count}")
    
    print()
    print("连通性测试:")
    tests = [
        ('Server-A', 'Server-C'),
        ('Server-A', 'Server-D'),
        ('Server-D', 'Server-E'),
    ]
    for s1, s2 in tests:
        result = "连通" if ds.connected(s1, s2) else "不连通"
        print(f"  {s1} <-> {s2}: {result}")
    
    print()
    
    # 添加新连接
    print("添加新连接: Server-C <-> Server-D")
    ds.union('Server-C', 'Server-D')
    print(f"  现在连通分量数: {ds.set_count}")
    print(f"  Server-A <-> Server-E: {'连通' if ds.connected('Server-A', 'Server-E') else '不连通'}")
    print()


def example_cycle_detection():
    """环检测示例"""
    print("=" * 60)
    print("5. 图的环检测")
    print("=" * 60)
    
    # 无环图
    edges1 = [(1, 2), (2, 3), (3, 4), (4, 5)]
    print(f"图1 边: {edges1}")
    print(f"  存在环: {detect_cycle_undirected(edges1)}")
    print()
    
    # 有环图
    edges2 = [(1, 2), (2, 3), (3, 4), (4, 1)]
    print(f"图2 边: {edges2}")
    print(f"  存在环: {detect_cycle_undirected(edges2)}")
    print()


def example_minimum_spanning_tree():
    """最小生成树示例"""
    print("=" * 60)
    print("6. 最小生成树 (Kruskal算法)")
    print("=" * 60)
    
    # 城市网络
    cities = ['北京', '上海', '广州', '深圳', '武汉']
    
    # 城市间距离（边）
    edges = [
        ('北京', '上海', 1200),
        ('北京', '武汉', 1100),
        ('上海', '武汉', 800),
        ('上海', '广州', 1500),
        ('武汉', '广州', 1000),
        ('武汉', '深圳', 900),
        ('广州', '深圳', 150),
    ]
    
    print("城市连接成本:")
    for u, v, w in edges:
        print(f"  {u} <-> {v}: {w}km")
    
    print()
    
    mst, total_cost = minimum_spanning_tree_kruskal(cities, edges)
    
    print("最小生成树结果:")
    print("  选择的边:")
    for u, v, w in mst:
        print(f"    {u} <-> {v}: {w}km")
    print(f"  总距离: {total_cost}km")
    print()


def example_weighted_disjoint_set():
    """带权并查集示例"""
    print("=" * 60)
    print("7. 带权并查集 - 相对关系")
    print("=" * 60)
    
    # 物品称重问题
    # 已知 A 比 B 重 5，B 比 C 重 3
    # 推导 A 比 C 重 8
    
    wds = WeightedDisjointSet()
    items = ['A', 'B', 'C', 'D']
    for item in items:
        wds.make_set(item)
    
    print("建立重量关系:")
    print("  B 比 A 重 5")
    wds.union('A', 'B', weight=5)  # weight(B) - weight(A) = 5
    
    print("  C 比 B 重 3")
    wds.union('B', 'C', weight=3)  # weight(C) - weight(B) = 3
    
    print("  D 比 A 重 2")
    wds.union('A', 'D', weight=2)
    
    print()
    print("推导重量关系:")
    print(f"  A 到 C 的重量差: {wds.get_weight('A', 'C')}")  # 8
    print(f"  A 到 D 的重量差: {wds.get_weight('A', 'D')}")  # 2
    print(f"  C 到 D 的重量差: {wds.get_weight('C', 'D')}")  # -6
    print()


def example_dynamic_connectivity():
    """动态连通性示例"""
    print("=" * 60)
    print("8. 动态连通性问题")
    print("=" * 60)
    
    # 模拟一系列合并和查询操作
    operations = [
        ('union', 1, 2),
        ('union', 3, 4),
        ('query', 1, 3),
        ('union', 2, 3),
        ('query', 1, 4),
        ('union', 5, 6),
        ('query', 1, 5),
        ('union', 4, 5),
        ('query', 1, 6),
    ]
    
    ds = DisjointSet(range(1, 7))
    
    print("操作序列:")
    for op in operations:
        if op[0] == 'union':
            _, u, v = op
            result = ds.union(u, v)
            status = "合并成功" if result else "已在同一集合"
            print(f"  union({u}, {v}): {status}")
        else:
            _, u, v = op
            result = ds.connected(u, v)
            print(f"  query({u}, {v}): {'连通' if result else '不连通'}")
    
    print()
    print(f"最终状态: {ds}")
    print()


def example_performance():
    """性能测试示例"""
    print("=" * 60)
    print("9. 性能测试")
    print("=" * 60)
    
    import time
    
    # 大规模测试
    n = 100000
    
    print(f"创建 {n} 个元素的并查集...")
    start = time.time()
    ds = DisjointSet(range(n))
    create_time = time.time() - start
    print(f"  创建时间: {create_time:.4f}s")
    
    print(f"执行 {n-1} 次合并...")
    start = time.time()
    for i in range(1, n):
        ds.union(0, i)
    union_time = time.time() - start
    print(f"  合并时间: {union_time:.4f}s")
    
    print("执行查找测试...")
    start = time.time()
    for i in range(0, n, 1000):
        ds.find(i)
    find_time = time.time() - start
    print(f"  查找时间 (100次): {find_time:.6f}s")
    
    print(f"最终集合数量: {ds.set_count}")
    print(f"总元素数: {len(ds)}")
    print()


if __name__ == '__main__':
    example_basic_operations()
    example_social_network()
    example_image_processing()
    example_network_connectivity()
    example_cycle_detection()
    example_minimum_spanning_tree()
    example_weighted_disjoint_set()
    example_dynamic_connectivity()
    example_performance()
    
    print("=" * 60)
    print("所有示例完成!")
    print("=" * 60)