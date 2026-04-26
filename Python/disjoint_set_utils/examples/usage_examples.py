"""
并查集工具使用示例

展示 DisjointSet、WeightedDisjointSet、UnionFind 的典型应用场景。
"""

import os
import sys
# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    DisjointSet,
    WeightedDisjointSet,
    UnionFind,
    connected_components,
    detect_cycle_undirected,
    kruskal_mst,
    accounts_merge
)


def example_basic_disjoint_set():
    """基本并查集操作示例"""
    print("=== 基本 DisjointSet 示例 ===\n")
    
    # 创建并查集
    ds = DisjointSet[int]()
    
    # 合并元素
    print("合并 1 和 2...")
    ds.union(1, 2)
    print(f"1 和 2 是否连通: {ds.connected(1, 2)}")
    print(f"当前集合数: {ds.count_sets()}")
    print(f"集合大小: {ds.set_size(1)}")
    
    print("\n合并 3 和 4...")
    ds.union(3, 4)
    print(f"当前集合数: {ds.count_sets()}")
    
    print("\n合并 2 和 3...")
    ds.union(2, 3)
    print(f"当前集合数: {ds.count_sets()}")
    print(f"1 和 4 是否连通: {ds.connected(1, 4)}")
    
    # 显示所有集合
    print("\n所有集合:")
    for root, elements in ds.get_sets().items():
        print(f"  根 {root}: {elements}")
    
    print()


def example_string_elements():
    """字符串元素并查集示例"""
    print("=== 字符串元素示例 ===\n")
    
    # 社交网络：检测朋友群组
    friendships = [
        ("Alice", "Bob"),
        ("Bob", "Charlie"),
        ("David", "Eve"),
        ("Frank", "Grace"),
        ("Grace", "Henry")
    ]
    
    ds = DisjointSet[str]()
    for p1, p2 in friendships:
        ds.union(p1, p2)
    
    print(f"社交群组数量: {ds.count_sets()}")
    print("\n各群组成员:")
    for root, members in ds.get_sets().items():
        print(f"  群组: {sorted(members)}")
    
    print(f"\nAlice 和 Charlie 是朋友吗? {ds.connected('Alice', 'Charlie')}")
    print(f"Alice 和 David 是朋友吗? {ds.connected('Alice', 'David')}")
    print()


def example_weighted_disjoint_set():
    """带权并查集示例"""
    print("=== 带权并查集示例 ===\n")
    
    # 场景：变量关系推导
    # union(x, y, w) 表示 y = x + w
    # get_weight(x, y) 返回 y 相对于 x 的偏移量
    wds = WeightedDisjointSet[str]()
    
    print("建立关系:")
    print("  B = A + 2 (union_with_weight('A', 'B', 2))")
    wds.union_with_weight('A', 'B', 2)
    
    print("  C = B + 3 (union_with_weight('B', 'C', 3))")
    wds.union_with_weight('B', 'C', 3)
    
    print("  D = C + 1 (union_with_weight('C', 'D', 1))")
    wds.union_with_weight('C', 'D', 1)
    
    print("\n推导关系:")
    print(f"  C 相对于 A = {wds.get_weight('A', 'C')}")  # 应为 5 (C = A + 5)
    print(f"  D 相对于 A = {wds.get_weight('A', 'D')}")  # 应为 6 (D = A + 6)
    print(f"  A 相对于 D = {wds.get_weight('D', 'A')}")  # 应为 -6 (A = D - 6)
    print()


def example_union_find_optimized():
    """优化版整数并查集示例"""
    print("=== 优化版 UnionFind 示例 ===\n")
    
    # 网络连接模拟
    uf = UnionFind(6)
    
    connections = [(0, 1), (1, 2), (3, 4), (4, 5)]
    
    for u, v in connections:
        uf.union(u, v)
        print(f"连接 {u} - {v}, 当前分组数: {uf.count_sets()}")
    
    print(f"\n节点 0 和 2 连通: {uf.connected(0, 2)}")
    print(f"节点 0 和 3 连通: {uf.connected(0, 3)}")
    print(f"分组 1 的大小: {uf.set_size(1)}")
    
    # 重置
    print("\n重置后...")
    uf.reset()
    print(f"分组数: {uf.count_sets()}")
    print()


def example_connected_components():
    """连通分量计算示例"""
    print("=== 连通分量计算示例 ===\n")
    
    # 图结构:
    # 0 -- 1 -- 2    3 -- 4    5
    n = 6
    edges = [(0, 1), (1, 2), (3, 4)]
    
    components = connected_components(n, edges)
    
    print(f"图的连通分量数: {len(components)}")
    for i, comp in enumerate(components):
        print(f"  分量 {i + 1}: {comp}")
    print()


def example_cycle_detection():
    """环检测示例"""
    print("=== 无向图环检测示例 ===\n")
    
    # 有环图
    edges_with_cycle = [(0, 1), (1, 2), (2, 0)]
    print(f"图 {edges_with_cycle} 有环: {detect_cycle_undirected(3, edges_with_cycle)}")
    
    # 无环图（树）
    edges_no_cycle = [(0, 1), (1, 2), (2, 3)]
    print(f"图 {edges_no_cycle} 有环: {detect_cycle_undirected(4, edges_no_cycle)}")
    print()


def example_kruskal_mst():
    """Kruskal 最小生成树示例"""
    print("=== Kruskal 最小生成树示例 ===\n")
    
    # 图结构（边: (起点, 终点, 权重)）:
    #     1
    #   0 --- 1
    #   | \   |
    #  4|  3\ |2
    #   |    \|
    #   3-----2
    #     5
    
    n = 4
    edges = [
        (0, 1, 1),
        (1, 2, 2),
        (0, 2, 3),
        (0, 3, 4),
        (2, 3, 5)
    ]
    
    print("原图边:")
    for u, v, w in edges:
        print(f"  {u} -- {v}: 权重 {w}")
    
    weight, mst = kruskal_mst(n, edges)
    
    print(f"\n最小生成树总权重: {weight}")
    print("最小生成树边:")
    for u, v, w in mst:
        print(f"  {u} -- {v}: 权重 {w}")
    print()


def example_accounts_merge():
    """账户合并示例"""
    print("=== 账户合并示例 ===\n")
    
    accounts = [
        ("John", ["john@email.com", "john.smith@email.com"]),
        ("John", ["john.smith@email.com", "john.doe@email.com"]),
        ("Mary", ["mary@email.com"]),
        ("John", ["john.doe@email.com", "john.junior@email.com"])
    ]
    
    print("原始账户:")
    for name, emails in accounts:
        print(f"  {name}: {emails}")
    
    merged = accounts_merge(accounts)
    
    print("\n合并后账户:")
    for name, emails in merged:
        print(f"  {name}: {emails}")
    print()


def example_image_segmentation():
    """图像分割模拟示例（并查集经典应用）"""
    print("=== 图像分割模拟示例 ===\n")
    
    # 模拟 4x4 图像的像素相似度
    # 像素编号: 0-15
    # 相似的相邻像素会被合并
    
    width, height = 4, 4
    pixels = width * height
    
    # 模拟相似度: 假设以下相邻像素相似
    similar_pairs = [
        (0, 1), (1, 2), (2, 3),      # 第一行相似
        (4, 5), (5, 6),              # 第二行部分相似
        (8, 9), (10, 11),            # 第三行部分相似
        (12, 13), (13, 14), (14, 15) # 第四行相似
    ]
    
    # 区域合并
    ds = DisjointSet[int]()
    for p1, p2 in similar_pairs:
        ds.union(p1, p2)
    
    print(f"原始像素数: {pixels}")
    print(f"分割后区域数: {ds.count_sets()}")
    print("\n各区域包含的像素:")
    for root, pixels in ds.get_sets().items():
        print(f"  区域 {root}: {sorted(pixels)}")
    print()


def main():
    """运行所有示例"""
    example_basic_disjoint_set()
    example_string_elements()
    example_weighted_disjoint_set()
    example_union_find_optimized()
    example_connected_components()
    example_cycle_detection()
    example_kruskal_mst()
    example_accounts_merge()
    example_image_segmentation()
    
    print("=" * 50)
    print("所有示例完成！")


if __name__ == '__main__':
    main()