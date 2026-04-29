"""
希尔伯特曲线工具使用示例

演示希尔伯特曲线在以下场景中的应用：
1. 基本编码/解码
2. 空间索引
3. 地理坐标索引
4. 空间排序
5. 范围查询

Author: AllToolkit
Date: 2026-04-30
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from hilbert_curve_utils.mod import (
    HilbertCurve, HilbertIndex,
    hilbert_encode_2d, hilbert_decode_2d,
    hilbert_encode_3d, hilbert_decode_3d,
    normalize_coordinate, denormalize_coordinate,
    hilbert_sort, hilbert_index_for_geo, geo_from_hilbert_index
)


def example_basic_2d():
    """示例 1: 基本 2D 编码/解码"""
    print("\n" + "=" * 60)
    print("示例 1: 基本 2D 编码/解码")
    print("=" * 60)
    
    # 创建 8x8 网格的希尔伯特曲线 (order=3)
    order = 3
    curve = HilbertCurve(dimension=2, order=order)
    
    print(f"\n曲线信息: {curve}")
    print(f"网格大小: {1<<order}x{1<<order}")
    print(f"坐标范围: 0 到 {curve.max_coordinate}")
    
    # 编码坐标点
    points = [(0, 0), (1, 0), (3, 3), (7, 7)]
    
    print("\n坐标 -> 希尔伯特距离:")
    for x, y in points:
        distance = curve.distance_from_point((x, y))
        print(f"  ({x}, {y}) -> {distance}")
    
    # 解码距离
    distances = [0, 10, 32, 63]
    
    print("\n距离 -> 坐标:")
    for d in distances:
        point = curve.point_from_distance(d)
        print(f"  {d} -> {point}")
    
    # 使用便捷函数
    print("\n使用便捷函数:")
    d = hilbert_encode_2d(5, 5, order=3)
    x, y = hilbert_decode_2d(d, order=3)
    print(f"  hilbert_encode_2d(5, 5, 3) = {d}")
    print(f"  hilbert_decode_2d({d}, 3) = ({x}, {y})")


def example_visualization():
    """示例 2: 希尔伯特曲线可视化"""
    print("\n" + "=" * 60)
    print("示例 2: 希尔伯特曲线可视化")
    print("=" * 60)
    
    # 小阶数的曲线可视化更清晰
    for order in [1, 2, 3]:
        curve = HilbertCurve(dimension=2, order=order)
        print(f"\nOrder={order} (网格 {1<<order}x{1<<order}):")
        print(curve.visualize_2d())


def example_spatial_sorting():
    """示例 3: 空间排序"""
    print("\n" + "=" * 60)
    print("示例 3: 使用希尔伯特曲线进行空间排序")
    print("=" * 60)
    
    # 一组随机分布的点
    points = [
        (7, 7), (0, 0), (4, 4), (1, 3), (6, 2),
        (2, 5), (8, 1), (3, 8), (5, 6), (9, 9)
    ]
    
    print(f"\n原始点顺序: {points}")
    
    # 使用希尔伯特曲线排序
    sorted_points = hilbert_sort(points, order=4)
    print(f"希尔伯特排序后: {sorted_points}")
    
    # 解释: 希尔伯特排序保持空间局部性
    # 相邻的点在空间中也通常相邻
    print("\n空间局部性验证:")
    for i in range(len(sorted_points) - 1):
        p1, p2 = sorted_points[i], sorted_points[i + 1]
        manhattan = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
        print(f"  {p1} -> {p2}: 曼哈顿距离 = {manhattan}")


def example_geographic_indexing():
    """示例 4: 地理坐标索引"""
    print("\n" + "=" * 60)
    print("示例 4: 地理坐标索引")
    print("=" * 60)
    
    # 中国主要城市
    cities = [
        ("北京", 39.9042, 116.4074),
        ("上海", 31.2304, 121.4737),
        ("广州", 23.1291, 113.2644),
        ("深圳", 22.5431, 114.0579),
        ("成都", 30.5728, 104.0668),
        ("杭州", 30.2741, 120.1551),
        ("武汉", 30.5928, 114.3055),
        ("西安", 34.3416, 108.9398),
        ("南京", 32.0603, 118.7969),
        ("重庆", 29.4316, 106.9123),
    ]
    
    order = 16  # 高精度
    print(f"\n将地理坐标转换为希尔伯特索引 (order={order}):")
    
    # 计算索引
    city_indices = []
    for name, lat, lon in cities:
        idx = hilbert_index_for_geo(lat, lon, order=order)
        city_indices.append((name, lat, lon, idx))
        print(f"  {name:4} ({lat:7.4f}, {lon:8.4f}) -> {idx}")
    
    # 排序后展示空间局部性
    print("\n按希尔伯特索引排序:")
    city_indices.sort(key=lambda x: x[3])
    for name, lat, lon, idx in city_indices:
        print(f"  {name:4} -> {idx}")
    
    # 还原坐标
    print("\n索引还原测试:")
    test_idx = city_indices[0][3]
    restored_lat, restored_lon = geo_from_hilbert_index(test_idx, order=order)
    print(f"  索引 {test_idx} -> ({restored_lat:.6f}, {restored_lon:.6f})")
    print(f"  原始: ({city_indices[0][1]:.4f}, {city_indices[0][2]:.4f})")


def example_spatial_index():
    """示例 5: 空间索引构建与查询"""
    print("\n" + "=" * 60)
    print("示例 5: 构建空间索引")
    print("=" * 60)
    
    # 创建索引
    index = HilbertIndex(dimension=2, order=4)
    
    # 添加一些地点
    locations = {
        (5, 5): "图书馆",
        (2, 3): "咖啡厅",
        (8, 8): "公园",
        (10, 10): "商场",
        (7, 5): "学校",
        (3, 7): "医院",
        (12, 2): "机场",
        (1, 12): "体育馆",
    }
    
    print("添加地点到索引:")
    for point, name in locations.items():
        index.insert(point, name)
        print(f"  {point}: {name}")
    
    print(f"\n索引统计: {index}")
    
    # 点查询
    query_point = (5, 5)
    results = index.query_point(query_point)
    print(f"\n查询点 {query_point}: {results}")
    
    # 范围查询
    min_point, max_point = (0, 0), (8, 8)
    range_results = index.query_range(min_point, max_point)
    print(f"范围查询 [{min_point}] 到 [{max_point}]: {range_results}")
    
    # 附近查询
    center = (5, 5)
    radius = 3
    nearby = index.get_nearby(center, radius)
    print(f"中心 {center} 半径 {radius} 内: {[name for _, name in nearby]}")


def example_3d_curve():
    """示例 6: 3D 希尔伯特曲线"""
    print("\n" + "=" * 60)
    print("示例 6: 3D 希尔伯特曲线")
    print("=" * 60)
    
    order = 2
    curve = HilbertCurve(dimension=3, order=order)
    
    print(f"\n曲线信息: {curve}")
    print(f"网格大小: {1<<order}x{1<<order}x{1<<order}")
    print(f"总点数: {curve.num_points}")
    
    # 编码/解码 3D 点
    points_3d = [(0, 0, 0), (1, 1, 1), (2, 3, 1), (3, 3, 3)]
    
    print("\n3D 坐标 -> 希尔伯特距离:")
    for point in points_3d:
        distance = curve.distance_from_point(point)
        print(f"  {point} -> {distance}")
    
    # 使用便捷函数
    print("\n便捷函数:")
    d = hilbert_encode_3d(2, 2, 2, order=2)
    x, y, z = hilbert_decode_3d(d, order=2)
    print(f"  hilbert_encode_3d(2, 2, 2, 2) = {d}")
    print(f"  hilbert_decode_3d({d}, 2) = ({x}, {y}, {z})")


def example_data_locality():
    """示例 7: 数据局部性应用"""
    print("\n" + "=" * 60)
    print("示例 7: 数据局部性 - 数据库索引优化")
    print("=" * 60)
    
    # 模拟一组随机分布的数据点
    import random
    random.seed(42)
    
    num_points = 100
    points = [(random.randint(0, 15), random.randint(0, 15)) for _ in range(num_points)]
    
    print(f"生成 {num_points} 个随机数据点")
    
    # 计算按 X 坐标排序的存储顺序
    sorted_by_x = sorted(points, key=lambda p: (p[0], p[1]))
    
    # 计算按希尔伯特曲线排序的存储顺序
    sorted_by_hilbert = hilbert_sort(points, order=4)
    
    # 计算范围查询的平均访问块数
    def simulate_range_query(sorted_points, min_x, min_y, max_x, max_y):
        """模拟范围查询，返回需要访问的连续块数"""
        in_range = [i for i, p in enumerate(sorted_points) 
                     if min_x <= p[0] <= max_x and min_y <= p[1] <= max_y]
        if not in_range:
            return 0
        
        # 计算连续块的断点数
        blocks = 1
        for i in range(1, len(in_range)):
            if in_range[i] != in_range[i-1] + 1:
                blocks += 1
        return blocks
    
    # 测试多个范围查询
    queries = [
        ((0, 0), (3, 3)),
        ((5, 5), (9, 9)),
        ((2, 8), (6, 12)),
    ]
    
    print("\n范围查询性能比较:")
    print("查询范围          | X排序 | 希尔伯特")
    print("-" * 45)
    
    for (min_p, max_p) in queries:
        x_blocks = simulate_range_query(sorted_by_x, min_p[0], min_p[1], max_p[0], max_p[1])
        h_blocks = simulate_range_query(sorted_by_hilbert, min_p[0], min_p[1], max_p[0], max_p[1])
        improvement = "✓" if h_blocks < x_blocks else ""
        print(f"[{min_p}] - [{max_p}] |  {x_blocks:3}   |    {h_blocks:3}    {improvement}")
    
    print("\n希尔伯特排序通常减少范围查询的磁盘访问块数")


def example_neighbors():
    """示例 8: 邻居查询"""
    print("\n" + "=" * 60)
    print("示例 8: 邻居查询")
    print("=" * 60)
    
    curve = HilbertCurve(dimension=2, order=4)
    
    # 测试点
    test_points = [(0, 0), (5, 5), (8, 8), (15, 15)]
    
    for point in test_points:
        print(f"\n点 {point}:")
        
        # 空间邻居
        spatial_neighbors = curve.get_neighbors(point)
        print(f"  空间邻居: {spatial_neighbors}")
        
        # 希尔伯特邻居
        distance = curve.distance_from_point(point)
        hilbert_neighbors = curve.get_hilbert_neighbors(distance)
        print(f"  希尔伯特距离: {distance}")
        print(f"  希尔伯特邻居 (距离): {hilbert_neighbors}")
        
        # 希尔伯特邻居的坐标
        hilbert_neighbor_points = [curve.point_from_distance(d) for d in hilbert_neighbors]
        print(f"  希尔伯特邻居 (坐标): {hilbert_neighbor_points}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("希尔伯特曲线工具使用示例")
    print("=" * 60)
    
    example_basic_2d()
    example_visualization()
    example_spatial_sorting()
    example_geographic_indexing()
    example_spatial_index()
    example_3d_curve()
    example_data_locality()
    example_neighbors()
    
    print("\n" + "=" * 60)
    print("示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()