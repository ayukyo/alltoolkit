"""
四叉树使用示例

展示四叉树的各种使用场景：
1. 基本操作
2. 范围查询
3. 最近邻查询
4. 空间索引应用
5. 游戏开发场景
"""

import sys
import os
import random
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from quadtree_utils.mod import (
    Point, Rectangle, Circle, QuadTree,
    create_quadtree, from_points
)


def example_basic_operations():
    """示例1: 基本操作"""
    print("\n" + "=" * 50)
    print("示例1: 基本操作")
    print("=" * 50)
    
    # 创建四叉树
    tree = create_quadtree(x=0, y=0, width=100, height=100)
    
    # 插入点
    tree.insert(Point(10, 10, "商店A"))
    tree.insert(Point(50, 50, "商店B"))
    tree.insert(Point(80, 80, "商店C"))
    tree.insert(Point(25, 75, "商店D"))
    
    print(f"插入了 {len(tree)} 个点")
    
    # 查询某个点
    nearest = tree.find_nearest_one(Point(45, 45))
    if nearest:
        point, dist = nearest
        print(f"离 (45, 45) 最近的点是 {point.data}，距离 {dist:.2f}")
    
    # 删除点
    tree.remove(Point(10, 10))
    print(f"删除后剩余 {len(tree)} 个点")


def example_range_query():
    """示例2: 范围查询"""
    print("\n" + "=" * 50)
    print("示例2: 范围查询")
    print("=" * 50)
    
    # 模拟城市中的餐厅分布
    tree = create_quadtree(0, 0, 1000, 1000)  # 1000x1000 米的区域
    
    restaurants = [
        (100, 200, "肯德基"),
        (150, 250, "麦当劳"),
        (500, 500, "必胜客"),
        (520, 510, "星巴克"),
        (800, 800, "海底捞"),
        (300, 400, "外婆家"),
        (350, 450, "西贝"),
    ]
    
    for x, y, name in restaurants:
        tree.insert(Point(x, y, name))
    
    # 查询某个区域内的餐厅
    search_area = Rectangle(400, 400, 200, 200)  # 400-600 米范围
    results = tree.query(search_area)
    
    print(f"在区域 {search_area} 内找到 {len(results)} 家餐厅:")
    for p in results:
        print(f"  - {p.data} 位于 ({p.x}, {p.y})")


def example_nearest_neighbors():
    """示例3: 最近邻查询"""
    print("\n" + "=" * 50)
    print("示例3: 最近邻查询 (KNN)")
    print("=" * 50)
    
    # 创建带有随机点的树
    tree = create_quadtree(0, 0, 100, 100)
    
    random.seed(123)
    for i in range(20):
        tree.insert(Point(
            random.uniform(10, 90),
            random.uniform(10, 90),
            f"地点{i + 1}"
        ))
    
    # 用户当前位置
    user_pos = Point(50, 50)
    print(f"用户位置: ({user_pos.x}, {user_pos.y})")
    
    # 找最近的 5 个地点
    nearest = tree.find_nearest(user_pos, k=5)
    
    print("\n最近的 5 个地点:")
    for i, (point, dist) in enumerate(nearest, 1):
        print(f"  {i}. {point.data} - 距离: {dist:.2f}")


def example_radius_search():
    """示例4: 半径搜索"""
    print("\n" + "=" * 50)
    print("示例4: 半径搜索")
    print("=" * 50)
    
    # 模拟外卖配送范围
    tree = create_quadtree(0, 0, 2000, 2000)  # 2000米 x 2000米
    
    # 添加餐厅
    restaurants = [
        (500, 500, "餐厅A"),
        (600, 600, "餐厅B"),
        (1000, 1000, "餐厅C"),
        (1500, 1500, "餐厅D"),
    ]
    
    for x, y, name in restaurants:
        tree.insert(Point(x, y, name))
    
    # 用户位置
    user_x, user_y = 700, 700
    
    # 搜索 500 米范围内的餐厅
    results = tree.find_in_radius(Point(user_x, user_y), 500)
    
    print(f"用户位置: ({user_x}, {user_y})")
    print(f"500米配送范围内的餐厅 ({len(results)} 家):")
    for point, dist in results:
        print(f"  - {point.data}: 距离 {dist:.0f} 米")


def example_collision_detection():
    """示例5: 碰撞检测（游戏开发）"""
    print("\n" + "=" * 50)
    print("示例5: 碰撞检测")
    print("=" * 50)
    
    # 游戏场景：检测子弹与敌人的碰撞
    tree = create_quadtree(0, 0, 800, 600)  # 800x600 游戏画面
    
    # 添加敌人
    enemies = [
        Point(100, 100, {"id": 1, "hp": 100}),
        Point(200, 150, {"id": 2, "hp": 100}),
        Point(300, 200, {"id": 3, "hp": 100}),
        Point(400, 300, {"id": 4, "hp": 100}),
    ]
    
    for enemy in enemies:
        tree.insert(enemy)
    
    # 子弹位置
    bullet_x, bullet_y = 195, 145
    bullet_radius = 20  # 子弹爆炸半径
    
    print(f"子弹落点: ({bullet_x}, {bullet_y})")
    print(f"爆炸半径: {bullet_radius}")
    
    # 查找爆炸范围内的敌人
    hits = tree.find_in_radius(Point(bullet_x, bullet_y), bullet_radius)
    
    if hits:
        print(f"\n命中 {len(hits)} 个敌人:")
        for enemy, dist in hits:
            print(f"  - 敌人#{enemy.data['id']}: 距离 {dist:.1f}")
    else:
        print("未命中任何敌人")


def example_spatial_clustering():
    """示例6: 空间聚类"""
    print("\n" + "=" * 50)
    print("示例6: 空间聚类")
    print("=" * 50)
    
    # 模拟地理数据点
    random.seed(456)
    points = []
    
    # 创建几个聚类中心
    centers = [(100, 100), (400, 400), (700, 100)]
    
    for center_x, center_y in centers:
        for _ in range(15):
            x = center_x + random.gauss(0, 30)
            y = center_y + random.gauss(0, 30)
            points.append(Point(x, y))
    
    # 创建四叉树
    tree = from_points(points)
    
    print(f"总共 {len(tree)} 个数据点")
    
    # 找到每个聚类中心附近的点数
    for i, (cx, cy) in enumerate(centers):
        nearby = tree.find_in_radius(Point(cx, cy), 80)
        print(f"聚类 {i + 1} 中心 ({cx}, {cy}): {len(nearby)} 个点")


def example_batch_operations():
    """示例7: 批量操作"""
    print("\n" + "=" * 50)
    print("示例7: 批量操作")
    print("=" * 50)
    
    # 创建点列表
    points = [
        Point(x * 10, y * 10, f"点({x},{y})")
        for x in range(10)
        for y in range(10)
    ]
    
    print(f"创建 {len(points)} 个点")
    
    # 批量插入
    tree = create_quadtree(0, 0, 100, 100)
    count = tree.insert_many(points)
    print(f"成功插入 {count} 个点")
    
    # 遍历所有点
    processed = []
    tree.for_each(lambda p: processed.append(p.data))
    print(f"遍历处理了 {len(processed)} 个点")
    
    # 使用迭代器
    first_5 = [p for p, _ in zip(tree, range(5))]
    print(f"前 5 个点: {[p.data for p in first_5]}")
    
    # 清空
    tree.clear()
    print(f"清空后: {len(tree)} 个点")


def example_performance():
    """示例8: 性能演示"""
    print("\n" + "=" * 50)
    print("示例8: 性能演示")
    print("=" * 50)
    
    import time
    
    # 创建大量随机点
    random.seed(789)
    points = [
        Point(random.uniform(0, 10000), random.uniform(0, 10000), i)
        for i in range(10000)
    ]
    
    # 插入性能
    start = time.time()
    tree = from_points(points)
    insert_time = time.time() - start
    print(f"插入 {len(points)} 个点: {insert_time:.3f} 秒")
    
    # 范围查询性能
    start = time.time()
    for _ in range(1000):
        region = Rectangle(
            random.uniform(0, 9000),
            random.uniform(0, 9000),
            500,
            500
        )
        tree.query(region)
    query_time = time.time() - start
    print(f"1000 次范围查询: {query_time:.3f} 秒")
    
    # 最近邻查询性能
    start = time.time()
    for _ in range(100):
        query = Point(random.uniform(0, 10000), random.uniform(0, 10000))
        tree.find_nearest(query, k=5)
    knn_time = time.time() - start
    print(f"100 次 KNN 查询 (k=5): {knn_time:.3f} 秒")


def example_circle_query():
    """示例9: 圆形区域查询"""
    print("\n" + "=" * 50)
    print("示例9: 圆形区域查询")
    print("=" * 50)
    
    tree = create_quadtree(0, 0, 200, 200)
    
    # 添加 GPS 坐标点
    locations = [
        Point(50, 50, "中心公园"),
        Point(60, 55, "咖啡厅"),
        Point(45, 48, "图书馆"),
        Point(150, 150, "远郊商场"),
        Point(55, 60, "公交站"),
    ]
    
    for loc in locations:
        tree.insert(loc)
    
    # 查询圆形区域
    center = Circle(55, 55, 20)  # 圆心 (55, 55), 半径 20
    results = tree.query_circle(center)
    
    print(f"圆心: ({center.x}, {center.y}), 半径: {center.radius}")
    print(f"圆形区域内找到 {len(results)} 个地点:")
    for p in results:
        dist = math.sqrt((p.x - center.x) ** 2 + (p.y - center.y) ** 2)
        print(f"  - {p.data}: 距离圆心 {dist:.1f}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("四叉树工具模块 - 使用示例")
    print("=" * 60)
    
    example_basic_operations()
    example_range_query()
    example_nearest_neighbors()
    example_radius_search()
    example_collision_detection()
    example_spatial_clustering()
    example_batch_operations()
    example_performance()
    example_circle_query()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()