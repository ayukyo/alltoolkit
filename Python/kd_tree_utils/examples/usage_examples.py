"""
KD树工具模块使用示例
====================

展示KD树的各种用法，包括：
1. 基本操作（创建、插入、查询）
2. 最近邻搜索
3. k近邻搜索
4. 范围查询
5. 圆形区域查询
6. 删除节点
7. 使用构建器
8. 实际应用场景
"""

from mod import KDTree, create_kd_tree, nearest_neighbor_search, KDTreeBuilder
import math


def example_basic_operations():
    """基本操作示例"""
    print("=" * 60)
    print("1. 基本操作")
    print("=" * 60)
    
    # 创建2维KD树
    tree = KDTree(dimension=2)
    
    # 插入点
    tree.insert([2, 3], data="商店A")
    tree.insert([5, 4], data="商店B")
    tree.insert([9, 6], data="商店C")
    tree.insert([4, 7], data="商店D")
    tree.insert([8, 1], data="商店E")
    tree.insert([7, 2], data="商店F")
    
    print(f"树的大小: {tree.size()}")
    print(f"树的高度: {tree.height()}")
    print(f"是否平衡: {tree.is_balanced()}")
    
    # 检查点是否存在
    print(f"\n包含点[2, 3]: {tree.contains([2, 3])}")
    print(f"包含点[10, 10]: {tree.contains([10, 10])}")
    
    # 获取所有点
    all_points = tree.all_points()
    print(f"\n所有点 ({len(all_points)} 个):")
    for point, data in all_points:
        print(f"  {point} - {data}")


def example_nearest_neighbor():
    """最近邻搜索示例"""
    print("\n" + "=" * 60)
    print("2. 最近邻搜索")
    print("=" * 60)
    
    tree = KDTree(dimension=2)
    cities = [
        ([0, 0], "北京"),
        ([10, 0], "上海"),
        ([0, 10], "广州"),
        ([10, 10], "深圳"),
        ([5, 5], "武汉"),
    ]
    for point, name in cities:
        tree.insert(point, name)
    
    # 查找最近的邻居
    query = [4, 4]
    result = tree.nearest_neighbor(query)
    
    if result:
        print(f"查询位置: {query}")
        print(f"最近的城市: {result[1]}")
        print(f"位置: {result[0]}")
        print(f"距离: {result[2]:.2f}")


def example_k_nearest_neighbors():
    """k近邻搜索示例"""
    print("\n" + "=" * 60)
    print("3. k近邻搜索")
    print("=" * 60)
    
    tree = KDTree(dimension=2)
    
    # 模拟餐厅位置
    restaurants = [
        ([1, 1], "餐厅A - 中餐"),
        ([2, 5], "餐厅B - 西餐"),
        ([3, 3], "餐厅C - 日料"),
        ([4, 1], "餐厅D - 韩餐"),
        ([5, 4], "餐厅E - 泰餐"),
        ([6, 2], "餐厅F - 印餐"),
        ([7, 6], "餐厅G - 法餐"),
    ]
    for point, name in restaurants:
        tree.insert(point, name)
    
    # 查找最近的3家餐厅
    user_location = [3, 2]
    k = 3
    nearest = tree.k_nearest_neighbors(user_location, k)
    
    print(f"用户位置: {user_location}")
    print(f"最近的 {k} 家餐厅:")
    for i, (point, name, dist) in enumerate(nearest, 1):
        print(f"  {i}. {name}")
        print(f"     位置: {point}, 距离: {dist:.2f}")


def example_range_query():
    """范围查询示例"""
    print("\n" + "=" * 60)
    print("4. 范围查询（矩形区域）")
    print("=" * 60)
    
    tree = KDTree(dimension=2)
    
    # 模拟商店位置
    stores = [
        ([2, 2], "便利店A"),
        ([3, 4], "超市B"),
        ([5, 5], "商场C"),
        ([6, 3], "商店D"),
        ([8, 8], "购物中心E"),
        ([1, 7], "小店F"),
    ]
    for point, name in stores:
        tree.insert(point, name)
    
    # 查询矩形区域内的商店
    # 定义查询范围: x在[1,5], y在[2,6]
    query_range = [(1, 5), (2, 6)]
    results = tree.range_query(query_range)
    
    print(f"查询范围: x ∈ [{query_range[0][0]}, {query_range[0][1]}], "
          f"y ∈ [{query_range[1][0]}, {query_range[1][1]}]")
    print(f"找到 {len(results)} 家商店:")
    for point, name in results:
        print(f"  {name} at {point}")


def example_radius_query():
    """圆形区域查询示例"""
    print("\n" + "=" * 60)
    print("5. 圆形区域查询")
    print("=" * 60)
    
    tree = KDTree(dimension=2)
    
    # 模拟共享单车位置
    bikes = [
        ([1, 1], "单车001"),
        ([1.5, 1.5], "单车002"),
        ([2, 2], "单车003"),
        ([3, 3], "单车004"),
        ([4, 4], "单车005"),
        ([1.2, 1.8], "单车006"),
    ]
    for point, bike_id in bikes:
        tree.insert(point, bike_id)
    
    # 用户位置和搜索半径
    user_pos = [1.5, 1.5]
    radius = 1.0
    
    nearby = tree.radius_query(user_pos, radius)
    
    print(f"用户位置: {user_pos}")
    print(f"搜索半径: {radius}")
    print(f"找到 {len(nearby)} 辆可用单车:")
    for point, bike_id, dist in sorted(nearby, key=lambda x: x[2]):
        print(f"  {bike_id} - 距离: {dist:.2f}")


def example_delete():
    """删除节点示例"""
    print("\n" + "=" * 60)
    print("6. 删除节点")
    print("=" * 60)
    
    tree = KDTree(dimension=2)
    points = [([1, 1], "A"), ([2, 2], "B"), ([3, 3], "C")]
    for point, data in points:
        tree.insert(point, data)
    
    print(f"初始大小: {tree.size()}")
    print(f"所有点: {[p[0] for p in tree.all_points()]}")
    
    # 删除一个点
    print(f"\n删除点 [2, 2]...")
    success = tree.delete([2, 2])
    print(f"删除结果: {'成功' if success else '失败'}")
    print(f"删除后大小: {tree.size()}")
    print(f"剩余点: {[p[0] for p in tree.all_points()]}")
    
    # 尝试删除不存在的点
    print(f"\n尝试删除不存在的点 [10, 10]...")
    success = tree.delete([10, 10])
    print(f"删除结果: {'成功' if success else '失败'}")


def example_builder():
    """使用构建器示例"""
    print("\n" + "=" * 60)
    print("7. 使用构建器（流式API）")
    print("=" * 60)
    
    # 使用构建器创建KD树
    tree = (KDTreeBuilder(dimension=2, distance_metric='euclidean')
        .add([1, 1], "点A")
        .add([2, 2], "点B")
        .add([3, 3], "点C")
        .add([4, 4], "点D")
        .build())
    
    print(f"树: {tree}")
    
    # 查询
    result = tree.nearest_neighbor([2.5, 2.5])
    if result:
        print(f"查询 [2.5, 2.5] 的最近邻: {result[0]} ({result[1]})")


def example_create_function():
    """使用便捷函数示例"""
    print("\n" + "=" * 60)
    print("8. 使用便捷函数")
    print("=" * 60)
    
    # 使用 create_kd_tree 快速创建
    points = [
        ([1, 2], "数据A"),
        ([3, 4], "数据B"),
        ([5, 6], "数据C"),
    ]
    tree = create_kd_tree(points)
    print(f"创建的树: {tree}")
    
    # 使用 nearest_neighbor_search 快速查询
    all_points = [[p[0][0], p[0][1]] for p in points]
    results = nearest_neighbor_search(all_points, [2, 3], k=2)
    print(f"\n查询 [2, 3] 的最近2个点:")
    for point, dist in results:
        print(f"  {point} - 距离: {dist:.2f}")


def example_distance_metrics():
    """不同距离度量示例"""
    print("\n" + "=" * 60)
    print("9. 不同距离度量")
    print("=" * 60)
    
    metrics = ['euclidean', 'manhattan', 'chebyshev']
    point = [3, 4]
    query = [0, 0]
    
    for metric in metrics:
        tree = KDTree(dimension=2, distance_metric=metric)
        tree.insert(point)
        result = tree.nearest_neighbor(query)
        
        if result:
            print(f"{metric:12s}: 距离 = {result[2]:.2f}")


def example_3d_tree():
    """3D KD树示例"""
    print("\n" + "=" * 60)
    print("10. 3D空间中的KD树")
    print("=" * 60)
    
    tree = KDTree(dimension=3)
    
    # 模拟3D空间中的点（如无人机位置）
    drones = [
        ([0, 0, 10], "无人机A"),
        ([5, 5, 15], "无人机B"),
        ([10, 0, 20], "无人机C"),
        ([5, 10, 12], "无人机D"),
        ([2, 3, 8], "无人机E"),
    ]
    for point, name in drones:
        tree.insert(point, name)
    
    print(f"3D KD树: {tree}")
    
    # 最近邻
    target = [4, 4, 12]
    result = tree.nearest_neighbor(target)
    if result:
        print(f"\n位置 {target} 最近的无人机:")
        print(f"  {result[1]} at {result[0]}, 距离: {result[2]:.2f}")
    
    # 3D范围查询
    range_3d = [(0, 6), (0, 6), (5, 20)]
    in_range = tree.range_query(range_3d)
    print(f"\n在范围 {range_3d} 内的无人机:")
    for point, name in in_range:
        print(f"  {name} at {point}")


def example_geographic_search():
    """地理搜索示例（模拟）"""
    print("\n" + "=" * 60)
    print("11. 地理位置搜索（模拟）")
    print("=" * 60)
    
    # 注意：真实地理搜索需要考虑地球曲率
    # 这里用简化的平面坐标演示
    
    tree = KDTree(dimension=2)
    
    # 模拟城市坐标（经度, 纬度）
    cities = [
        ([116.4, 39.9], "北京"),
        ([121.5, 31.2], "上海"),
        ([113.3, 23.1], "广州"),
        ([114.1, 22.5], "深圳"),
        ([120.2, 30.3], "杭州"),
        ([117.3, 31.8], "合肥"),
        ([104.1, 30.7], "成都"),
        ([106.6, 26.6], "贵阳"),
    ]
    for point, name in cities:
        tree.insert(point, name)
    
    # 查找离某位置最近的城市
    location = [118, 32]  # 南京附近
    nearest = tree.nearest_neighbor(location)
    
    if nearest:
        print(f"位置 {location} 附近最近的城市: {nearest[1]}")
        print(f"坐标: {nearest[0]}")
    
    # 查找附近多个城市
    print(f"\n距离 {location} 最近的3个城市:")
    k_nearest = tree.k_nearest_neighbors(location, 3)
    for i, (point, name, dist) in enumerate(k_nearest, 1):
        print(f"  {i}. {name} - 距离: {dist:.2f}")


def example_balanced_tree():
    """平衡树构建示例"""
    print("\n" + "=" * 60)
    print("12. 平衡树构建")
    print("=" * 60)
    
    # 使用 build 方法创建平衡树
    tree = KDTree(dimension=2)
    
    # 创建有序点列表
    points = [([i, i], f"点{i}") for i in range(15)]
    tree.build(points)
    
    print(f"树: {tree}")
    print(f"是否平衡: {tree.is_balanced()}")
    print(f"高度: {tree.height()} (理论上最优高度: {math.ceil(math.log2(15))})")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("KD树工具模块 - 使用示例")
    print("=" * 60)
    
    example_basic_operations()
    example_nearest_neighbor()
    example_k_nearest_neighbors()
    example_range_query()
    example_radius_query()
    example_delete()
    example_builder()
    example_create_function()
    example_distance_metrics()
    example_3d_tree()
    example_geographic_search()
    example_balanced_tree()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()