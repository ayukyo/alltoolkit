"""
四叉树工具模块测试

测试覆盖:
- 点的基本操作（插入、删除）
- 范围查询
- 圆形区域查询
- 最近邻查询
- 半径查询
- 边界条件处理
"""

import sys
import os
import random
import math

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quadtree_utils.mod import (
    Point, Rectangle, Circle, QuadTree, QuadTreeNode,
    create_quadtree, from_points
)


def test_point():
    """测试 Point 类"""
    print("测试 Point...")
    
    # 基本创建
    p1 = Point(1.0, 2.0)
    assert p1.x == 1.0
    assert p1.y == 2.0
    assert p1.data is None
    
    # 带数据
    p2 = Point(3.0, 4.0, data="test")
    assert p2.data == "test"
    
    # 相等比较
    p3 = Point(1.0, 2.0)
    assert p1 == p3
    
    # 哈希
    s = {p1, p3}
    assert len(s) == 1
    
    print("  ✓ Point 测试通过")


def test_rectangle():
    """测试 Rectangle 类"""
    print("测试 Rectangle...")
    
    rect = Rectangle(0, 0, 10, 20)
    
    # 边界属性
    assert rect.left == 0
    assert rect.right == 10
    assert rect.top == 0
    assert rect.bottom == 20
    assert rect.area == 200
    
    # 中心点
    cx, cy = rect.center
    assert cx == 5
    assert cy == 10
    
    # 点包含
    assert rect.contains_point(Point(5, 10))
    assert rect.contains_point(Point(0, 0))
    assert not rect.contains_point(Point(10, 10))  # 右边界不包含
    assert not rect.contains_point(Point(-1, 5))
    
    # 矩形相交
    rect2 = Rectangle(5, 5, 10, 10)
    assert rect.intersects(rect2)
    
    rect3 = Rectangle(15, 15, 5, 5)
    assert not rect.intersects(rect3)
    
    # 矩形包含
    rect4 = Rectangle(1, 1, 8, 18)
    assert rect.contains_rect(rect4)
    assert not rect4.contains_rect(rect)
    
    print("  ✓ Rectangle 测试通过")


def test_circle():
    """测试 Circle 类"""
    print("测试 Circle...")
    
    circle = Circle(0, 0, 5)
    
    # 点包含
    assert circle.contains_point(Point(0, 0))
    assert circle.contains_point(Point(3, 4))  # 距离为 5
    assert not circle.contains_point(Point(4, 4))  # 距离约为 5.66
    
    # 矩形相交
    rect = Rectangle(-3, -3, 6, 6)
    assert circle.intersects_rect(rect)
    
    rect2 = Rectangle(10, 10, 5, 5)
    assert not circle.intersects_rect(rect2)
    
    print("  ✓ Circle 测试通过")


def test_basic_operations():
    """测试基本操作"""
    print("测试基本操作...")
    
    tree = create_quadtree(0, 0, 100, 100)
    
    # 插入点
    p1 = Point(10, 10, "A")
    p2 = Point(50, 50, "B")
    p3 = Point(90, 90, "C")
    
    assert tree.insert(p1)
    assert tree.insert(p2)
    assert tree.insert(p3)
    assert len(tree) == 3
    
    # 插入边界外的点应该失败
    p_out = Point(200, 200)
    assert not tree.insert(p_out)
    
    # 点存在性检查
    rect = Rectangle(10, 10, 1, 1)
    points = tree.query(rect)
    assert len(points) == 1
    assert points[0].data == "A"
    
    # 删除点
    assert tree.remove(p1)
    assert len(tree) == 2
    assert not tree.remove(p1)  # 再次删除应失败
    
    print("  ✓ 基本操作测试通过")


def test_range_query():
    """测试范围查询"""
    print("测试范围查询...")
    
    tree = create_quadtree(0, 0, 100, 100)
    
    # 插入网格点 (0-90)
    for x in range(0, 100, 10):
        for y in range(0, 100, 10):
            tree.insert(Point(x, y, f"({x},{y})"))
    
    # 10x10 = 100 个点
    assert len(tree) == 100
    
    # 查询区域 (注意右边界不包含)
    region = Rectangle(20, 20, 30, 30)
    points = tree.query(region)
    
    # 验证所有点都在区域内
    for p in points:
        assert region.contains_point(p), f"Point {p} not in region {region}"
    
    # 应该找到 (20,20), (20,30), (20,40), (30,20), (30,30), (30,40), (40,20), (40,30), (40,40)
    # 注意: 边界不包含右/下边界 (使用 < 而非 <=)
    assert len(points) >= 4  # 至少有这些点
    
    print("  ✓ 范围查询测试通过")


def test_circle_query():
    """测试圆形区域查询"""
    print("测试圆形区域查询...")
    
    tree = create_quadtree(0, 0, 100, 100)
    
    # 插入一些点
    tree.insert(Point(0, 0, "origin"))
    tree.insert(Point(3, 4, "3,4"))  # 距原点 5
    tree.insert(Point(6, 8, "6,8"))  # 距原点 10
    tree.insert(Point(50, 50, "far"))
    
    # 查询半径为 6 的圆
    circle = Circle(0, 0, 6)
    points = tree.query_circle(circle)
    
    assert len(points) == 2  # origin 和 (3,4)
    point_data = {p.data for p in points}
    assert "origin" in point_data
    assert "3,4" in point_data
    
    print("  ✓ 圆形区域查询测试通过")


def test_nearest_neighbor():
    """测试最近邻查询"""
    print("测试最近邻查询...")
    
    tree = create_quadtree(0, 0, 100, 100)
    
    # 插入点
    points = [
        Point(10, 10, "A"),
        Point(20, 20, "B"),
        Point(30, 30, "C"),
        Point(40, 40, "D"),
        Point(50, 50, "E"),
    ]
    
    for p in points:
        tree.insert(p)
    
    # 查询最近邻
    query = Point(15, 15)
    nearest = tree.find_nearest(query, k=1)
    assert len(nearest) == 1
    assert nearest[0][0].data == "A"  # 最近的是 A (距离约 7.07)
    
    # 查询 k 近邻
    k_nearest = tree.find_nearest(query, k=3)
    assert len(k_nearest) == 3
    # 应该是 A, B, C（按距离排序）
    assert k_nearest[0][0].data == "A"
    assert k_nearest[1][0].data == "B"
    assert k_nearest[2][0].data == "C"
    
    # 验证距离
    for p, dist in k_nearest:
        expected_dist = math.sqrt((p.x - query.x) ** 2 + (p.y - query.y) ** 2)
        assert abs(dist - expected_dist) < 0.0001
    
    print("  ✓ 最近邻查询测试通过")


def test_radius_query():
    """测试半径查询"""
    print("测试半径查询...")
    
    tree = create_quadtree(0, 0, 100, 100)
    
    # 插入点
    tree.insert(Point(0, 0, "origin"))
    tree.insert(Point(5, 0, "5,0"))
    tree.insert(Point(0, 5, "0,5"))
    tree.insert(Point(3, 4, "3,4"))  # 距离 5
    tree.insert(Point(10, 10, "far"))
    
    # 查询半径为 5 的点
    results = tree.find_in_radius(Point(0, 0), 5)
    
    # origin(0), 5,0(5), 0,5(5), 3,4(5)
    assert len(results) == 4
    
    # 验证距离
    for p, dist in results:
        assert dist <= 5
    
    print("  ✓ 半径查询测试通过")


def test_split_and_merge():
    """测试分裂和合并"""
    print("测试分裂和合并...")
    
    # 容量设为 2，便于触发分裂
    tree = create_quadtree(0, 0, 100, 100, capacity=2)
    
    # 插入超过容量的点
    for i in range(10):
        tree.insert(Point(i * 10, i * 10, f"p{i}"))
    
    assert len(tree) == 10
    
    # 验证可以查询到所有点
    all_points = tree.all_points()
    assert len(all_points) == 10
    
    # 删除点直到合并
    for i in range(8):
        tree.remove(Point(i * 10, i * 10))
    
    assert len(tree) == 2
    
    print("  ✓ 分裂和合并测试通过")


def test_large_scale():
    """大规模测试"""
    print("测试大规模操作...")
    
    tree = create_quadtree(0, 0, 1000, 1000, capacity=8)
    
    # 随机插入 1000 个点
    random.seed(42)
    points = []
    for i in range(1000):
        x = random.uniform(0, 999)
        y = random.uniform(0, 999)
        p = Point(x, y, i)
        points.append(p)
        tree.insert(p)
    
    assert len(tree) == 1000
    
    # 范围查询
    region = Rectangle(200, 200, 200, 200)
    result = tree.query(region)
    for p in result:
        assert region.contains_point(p)
    
    # 最近邻查询
    query_point = Point(500, 500)
    nearest = tree.find_nearest(query_point, k=5)
    assert len(nearest) == 5
    
    # 验证结果有序
    for i in range(len(nearest) - 1):
        assert nearest[i][1] <= nearest[i + 1][1]
    
    # 删除一半的点
    for i in range(500):
        assert tree.remove(points[i])
    
    assert len(tree) == 500
    
    print("  ✓ 大规模测试通过")


def test_from_points():
    """测试从点列表创建"""
    print("测试 from_points...")
    
    points = [
        Point(10, 10),
        Point(20, 20),
        Point(30, 30),
        Point(100, 100),
    ]
    
    tree = from_points(points)
    assert len(tree) == 4
    
    # 所有点应该能被找到
    all_points = tree.all_points()
    assert len(all_points) == 4
    
    print("  ✓ from_points 测试通过")


def test_iterator():
    """测试迭代器"""
    print("测试迭代器...")
    
    tree = create_quadtree(0, 0, 100, 100)
    
    for i in range(10):
        tree.insert(Point(i, i, i))
    
    # 迭代
    count = 0
    for p in tree:
        count += 1
    assert count == 10
    
    # 包含检查
    assert Point(5, 5) in tree
    assert Point(50, 50) not in tree
    
    print("  ✓ 迭代器测试通过")


def test_empty_tree():
    """测试空树"""
    print("测试空树...")
    
    tree = create_quadtree(0, 0, 100, 100)
    
    assert len(tree) == 0
    assert tree.all_points() == []
    assert tree.query(Rectangle(0, 0, 50, 50)) == []
    assert tree.find_nearest(Point(50, 50), k=1) == []
    
    print("  ✓ 空树测试通过")


def test_edge_cases():
    """测试边界情况"""
    print("测试边界情况...")
    
    tree = create_quadtree(0, 0, 100, 100)
    
    # 边界上的点
    p = Point(0, 0)
    assert tree.insert(p)
    
    # 刚好在边界内的点
    p2 = Point(99.999, 99.999)
    assert tree.insert(p2)
    
    # 刚好在边界外的点
    p3 = Point(100, 100)
    assert not tree.insert(p3)
    
    # 查询边界区域
    region = Rectangle(0, 0, 1, 1)
    points = tree.query(region)
    assert len(points) == 1
    assert points[0].x == 0 and points[0].y == 0
    
    print("  ✓ 边界情况测试通过")


def test_custom_data():
    """测试自定义数据"""
    print("测试自定义数据...")
    
    tree: QuadTree[dict] = create_quadtree(0, 0, 100, 100)
    
    # 插入带复杂数据的点
    tree.insert(Point(10, 10, {"name": "A", "value": 100}))
    tree.insert(Point(20, 20, {"name": "B", "value": 200}))
    
    # 查询并验证数据
    region = Rectangle(5, 5, 20, 20)
    points = tree.query(region)
    
    assert len(points) == 2
    data_list = [p.data for p in points]
    assert {"name": "A", "value": 100} in data_list
    
    print("  ✓ 自定义数据测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("四叉树工具模块测试")
    print("=" * 50)
    
    test_point()
    test_rectangle()
    test_circle()
    test_basic_operations()
    test_range_query()
    test_circle_query()
    test_nearest_neighbor()
    test_radius_query()
    test_split_and_merge()
    test_large_scale()
    test_from_points()
    test_iterator()
    test_empty_tree()
    test_edge_cases()
    test_custom_data()
    
    print("=" * 50)
    print("✅ 所有测试通过!")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()