"""
六边形网格工具测试

测试覆盖:
- 基础坐标操作
- 坐标转换
- 距离计算
- 区域生成
- 路径查找
- 视野计算
- 网格类操作
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Hex, HexOrientation, OffsetCoordType, HexGrid,
    hex_add, hex_subtract, hex_scale, hex_direction, hex_neighbor, hex_neighbors,
    hex_diagonal_neighbors, hex_distance, hex_distance_chebyshev,
    hex_range, hex_ring, hex_spiral, hex_line, hex_triangle, hex_parallelogram,
    hex_hexagon, hex_rectangle,
    hex_rotate_right, hex_rotate_left, hex_rotate_180,
    hex_reflect_q, hex_reflect_r, hex_reflect_s,
    hex_to_offset, offset_to_hex, hex_to_pixel, pixel_to_hex, hex_round,
    hex_corner_offset, hex_corners,
    hex_path_astar, hex_path_bfs,
    hex_fov, hex_visible_from,
    hex_flood_fill, hex_region_outline, hex_region_interior,
    visualize_hex, visualize_hex_grid, visualize_hex_path, visualize_hex_range,
    POINTY_DIRECTIONS, FLAT_DIRECTIONS
)


def test_basic_hex_operations():
    """测试基础六边形操作"""
    print("测试基础六边形操作...")
    
    # 创建六边形
    h1 = Hex(1, 2)
    assert h1.q == 1
    assert h1.r == 2
    assert h1.s == -3  # 1 + 2 + s = 0 => s = -3
    
    # 加法
    h2 = Hex(3, -1)
    h3 = hex_add(h1, h2)
    assert h3 == Hex(4, 1)
    assert h1 + h2 == Hex(4, 1)
    
    # 减法
    h4 = hex_subtract(h1, h2)
    assert h4 == Hex(-2, 3)
    assert h1 - h2 == Hex(-2, 3)
    
    # 缩放
    h5 = hex_scale(h1, 2)
    assert h5 == Hex(2, 4)
    assert h1 * 2 == Hex(2, 4)
    
    # 取反
    h6 = -h1
    assert h6 == Hex(-1, -2)
    
    # 立方体坐标转换
    cube = h1.to_cube()
    assert cube == (1, 2, -3)
    
    h7 = Hex.from_cube(1, 2, -3)
    assert h7 == h1
    
    print("✓ 基础六边形操作测试通过")


def test_directions():
    """测试方向操作"""
    print("测试方向操作...")
    
    center = Hex(0, 0)
    
    # 尖顶六边形方向
    neighbors_pointy = hex_neighbors(center, HexOrientation.POINTY_TOP)
    assert len(neighbors_pointy) == 6
    assert Hex(1, 0) in neighbors_pointy  # 右上
    
    # 平顶六边形方向
    neighbors_flat = hex_neighbors(center, HexOrientation.FLAT_TOP)
    assert len(neighbors_flat) == 6
    
    # 单个方向
    d = hex_direction(HexOrientation.POINTY_TOP, 0)
    assert d == POINTY_DIRECTIONS[0]
    
    # 单个邻居
    n = hex_neighbor(center, HexOrientation.POINTY_TOP, 0)
    assert n == center + POINTY_DIRECTIONS[0]
    
    # 对角邻居
    diagonals = hex_diagonal_neighbors(center, HexOrientation.POINTY_TOP)
    assert len(diagonals) == 6
    
    print("✓ 方向操作测试通过")


def test_distance():
    """测试距离计算"""
    print("测试距离计算...")
    
    # 曼哈顿距离
    assert hex_distance(Hex(0, 0), Hex(0, 0)) == 0
    assert hex_distance(Hex(0, 0), Hex(1, 0)) == 1
    assert hex_distance(Hex(0, 0), Hex(1, -1)) == 1
    assert hex_distance(Hex(0, 0), Hex(3, -2)) == 3
    # Hex(1,2): s=-3, Hex(3,-1): s=-2
    # distance = (|1-3| + |2-(-1)| + |-3-(-2)|)/2 = (2+3+1)/2 = 3
    assert hex_distance(Hex(1, 2), Hex(3, -1)) == 3
    
    # 切比雪夫距离
    assert hex_distance_chebyshev(Hex(0, 0), Hex(1, 0)) == 1
    assert hex_distance_chebyshev(Hex(0, 0), Hex(3, -2)) == 3
    
    print("✓ 距离计算测试通过")


def test_range_generation():
    """测试区域生成"""
    print("测试区域生成...")
    
    # 圆形区域
    radius_1 = hex_range(Hex(0, 0), 1)
    assert len(radius_1) == 7  # 中心 + 6个邻居
    assert Hex(0, 0) in radius_1
    
    radius_2 = hex_range(Hex(0, 0), 2)
    assert len(radius_2) == 19  # 1 + 6 + 12
    
    # 圆环
    ring_1 = hex_ring(Hex(0, 0), 1)
    assert len(ring_1) == 6
    assert Hex(0, 0) not in ring_1
    
    ring_2 = hex_ring(Hex(0, 0), 2)
    assert len(ring_2) == 12
    
    # 螺旋
    spiral = hex_spiral(Hex(0, 0), 2)
    assert len(spiral) == 19  # 1 + 6 + 12
    assert spiral[0] == Hex(0, 0)  # 从中心开始
    
    print("✓ 区域生成测试通过")


def test_line_drawing():
    """测试直线绘制"""
    print("测试直线绘制...")
    
    # 同一点
    line1 = hex_line(Hex(0, 0), Hex(0, 0))
    assert len(line1) == 1
    assert line1[0] == Hex(0, 0)
    
    # 简单直线
    line2 = hex_line(Hex(0, 0), Hex(3, 0))
    assert len(line2) == 4
    assert line2[0] == Hex(0, 0)
    assert line2[-1] == Hex(3, 0)
    
    # 对角线
    line3 = hex_line(Hex(0, 0), Hex(2, -2))
    assert len(line3) == 3
    
    print("✓ 直线绘制测试通过")


def test_shapes():
    """测试形状生成"""
    print("测试形状生成...")
    
    # 三角形
    triangle = hex_triangle(3)
    assert len(triangle) == 6  # 1 + 2 + 3
    
    # 平行四边形
    para = hex_parallelogram(0, 2, 0, 2)
    assert len(para) == 9
    
    # 六边形区域
    hexagon = hex_hexagon(2)
    assert len(hexagon) == 19
    
    # 矩形
    rect = hex_rectangle(3, 2)
    assert len(rect) >= 6
    
    print("✓ 形状生成测试通过")


def test_rotation_reflection():
    """测试旋转和镜像"""
    print("测试旋转和镜像...")
    
    h = Hex(1, 2)
    
    # 旋转
    r1 = hex_rotate_right(h)
    assert isinstance(r1, Hex)
    
    r2 = hex_rotate_left(h)
    assert isinstance(r2, Hex)
    
    r3 = hex_rotate_180(h)
    assert r3 == Hex(-1, -2)
    
    # 镜像
    m1 = hex_reflect_q(h)
    assert isinstance(m1, Hex)
    
    m2 = hex_reflect_r(h)
    assert isinstance(m2, Hex)
    
    m3 = hex_reflect_s(h)
    assert isinstance(m3, Hex)
    
    print("✓ 旋转和镜像测试通过")


def test_coordinate_conversion():
    """测试坐标转换"""
    print("测试坐标转换...")
    
    # 轴向 -> 偏移 -> 轴向 (往返测试)
    h = Hex(2, 3)
    
    for orientation in [HexOrientation.POINTY_TOP, HexOrientation.FLAT_TOP]:
        for coord_type in [OffsetCoordType.EVEN, OffsetCoordType.ODD]:
            offset = hex_to_offset(h, coord_type, orientation)
            back = offset_to_hex(offset[0], offset[1], coord_type, orientation)
            assert back == h, f"Failed for {orientation}, {coord_type}: {h} -> {offset} -> {back}"
    
    # 像素转换
    for orientation in [HexOrientation.POINTY_TOP, HexOrientation.FLAT_TOP]:
        size = 30
        pixel = hex_to_pixel(h, size, orientation)
        back = pixel_to_hex(pixel[0], pixel[1], size, orientation)
        assert back == h, f"Failed pixel conversion for {orientation}"
    
    # 四舍五入
    rounded = hex_round(1.4, 2.6)
    assert isinstance(rounded, Hex)
    
    print("✓ 坐标转换测试通过")


def test_corners():
    """测试角点计算"""
    print("测试角点计算...")
    
    center = (100, 100)
    size = 30
    
    for orientation in [HexOrientation.POINTY_TOP, HexOrientation.FLAT_TOP]:
        corners = hex_corners(center, size, orientation)
        assert len(corners) == 6
        
        # 验证角点距离中心相等
        for corner in corners:
            dist = ((corner[0] - center[0])**2 + (corner[1] - center[1])**2) ** 0.5
            assert abs(dist - size) < 0.001
    
    print("✓ 角点计算测试通过")


def test_pathfinding():
    """测试路径查找"""
    print("测试路径查找...")
    
    start = Hex(0, 0)
    goal = Hex(3, 2)
    obstacles = {Hex(1, 0), Hex(1, 1)}
    
    # A* 算法
    path = hex_path_astar(start, goal, obstacles)
    assert len(path) > 0
    assert path[0] == start
    assert path[-1] == goal
    
    # 验证路径不穿过障碍物
    for h in path:
        assert h not in obstacles
    
    # BFS 算法
    path_bfs = hex_path_bfs(start, goal, obstacles)
    assert len(path_bfs) > 0
    assert path_bfs[0] == start
    assert path_bfs[-1] == goal
    
    # 不可达情况
    blocked = {Hex(1, 0), Hex(0, 1), Hex(1, -1), Hex(-1, 0), Hex(-1, 1), Hex(0, -1)}
    no_path = hex_path_astar(start, Hex(5, 5), blocked)
    assert len(no_path) == 0
    
    print("✓ 路径查找测试通过")


def test_field_of_view():
    """测试视野计算"""
    print("测试视野计算...")
    
    center = Hex(0, 0)
    radius = 3
    
    # 无障碍物
    def no_block(h):
        return False
    
    fov = hex_fov(center, radius, no_block)
    expected = set(hex_range(center, radius))
    assert fov == expected
    
    # 有障碍物
    obstacles = {Hex(1, 0)}
    
    def is_blocked(h):
        return h in obstacles
    
    fov_blocked = hex_fov(center, radius, is_blocked)
    # 障碍物应该被包含，但后面的可能被遮挡
    assert len(fov_blocked) > 0
    
    # 可见性测试
    assert hex_visible_from(center, Hex(2, 0), obstacles) == False  # 被 (1,0) 阻挡
    assert hex_visible_from(center, Hex(0, 2), obstacles) == True   # 没有阻挡
    
    print("✓ 视野计算测试通过")


def test_flood_fill():
    """测试洪水填充"""
    print("测试洪水填充...")
    
    start = Hex(0, 0)
    max_radius = 2
    
    # 无障碍物
    def always_passable(h):
        return True
    
    filled = hex_flood_fill(start, always_passable, max_radius)
    # 半径 r 内的六边形数量 = 1 + 3*r*(r+1)
    # r=2: 1 + 3*2*3 = 19
    assert len(filled) == 19
    
    # 有障碍物 (围住起点)
    obstacles = {Hex(1, 0), Hex(0, 1), Hex(-1, 1), Hex(-1, 0), Hex(0, -1), Hex(1, -1)}
    
    def passable_except_obstacles(h):
        return h not in obstacles
    
    filled_blocked = hex_flood_fill(start, passable_except_obstacles, max_radius=2)
    assert filled_blocked == {start}  # 只有起点可达
    
    print("✓ 洪水填充测试通过")


def test_region_operations():
    """测试区域操作"""
    print("测试区域操作...")
    
    # 创建一个实心区域
    region = set(hex_range(Hex(0, 0), 2))
    
    # 轮廓
    outline = hex_region_outline(region)
    assert len(outline) > 0
    assert Hex(0, 0) not in outline  # 中心不在轮廓上
    
    # 内部
    interior = hex_region_interior(region)
    assert len(interior) > 0
    assert Hex(0, 0) in interior  # 中心在内部
    
    print("✓ 区域操作测试通过")


def test_hex_grid_class():
    """测试六边形网格类"""
    print("测试六边形网格类...")
    
    grid = HexGrid(radius=2)
    
    # 边界检查
    assert grid.in_bounds(Hex(0, 0)) == True
    assert grid.in_bounds(Hex(2, 0)) == True
    assert grid.in_bounds(Hex(3, 0)) == False
    
    # 设置和获取
    grid.set(Hex(0, 0), "center")
    assert grid.get(Hex(0, 0)) == "center"
    assert grid.get(Hex(1, 0)) is None
    assert grid.get(Hex(1, 0), "default") == "default"
    
    # 移除
    assert grid.remove(Hex(0, 0)) == True
    assert grid.get(Hex(0, 0)) is None
    assert grid.remove(Hex(5, 5)) == False  # 超出边界
    
    # 所有单元格
    all_cells = grid.all_cells()
    # 半径 r 内的六边形数量 = 1 + 3*r*(r+1)
    # r=2: 1 + 3*2*3 = 19
    assert len(all_cells) == 19
    
    # 邻居
    neighbors = grid.neighbors(Hex(0, 0))
    assert len(neighbors) == 6
    
    # 距离
    assert grid.distance(Hex(0, 0), Hex(2, -1)) == 2
    
    # 范围
    range_cells = grid.range(Hex(0, 0), 1)
    assert len(range_cells) == 7
    
    print("✓ 六边形网格类测试通过")


def test_visualization():
    """测试可视化函数"""
    print("测试可视化函数...")
    
    # 单个六边形
    viz = visualize_hex(Hex(0, 0), size=2)
    assert isinstance(viz, str)
    assert len(viz) > 0
    
    # 网格可视化
    hexes = hex_range(Hex(0, 0), 2)
    viz_grid = visualize_hex_grid(hexes)
    assert isinstance(viz_grid, str)
    
    # 路径可视化
    path = hex_line(Hex(0, 0), Hex(3, 0))
    viz_path = visualize_hex_path(path)
    assert isinstance(viz_path, str)
    assert 'S' in viz_path  # 起点
    assert 'E' in viz_path  # 终点
    
    # 范围可视化
    viz_range = visualize_hex_range(Hex(0, 0), 2)
    assert isinstance(viz_range, str)
    assert 'O' in viz_range  # 中心
    
    print("✓ 可视化函数测试通过")


def test_edge_cases():
    """测试边界情况"""
    print("测试边界情况...")
    
    # 零半径
    zero_range = hex_range(Hex(0, 0), 0)
    assert len(zero_range) == 1
    assert zero_range[0] == Hex(0, 0)
    
    # 零半径圆环
    zero_ring = hex_ring(Hex(0, 0), 0)
    assert len(zero_ring) == 1
    
    # 大半径
    large_range = hex_range(Hex(0, 0), 10)
    # 半径 r 的六边形数量为 1 + 6 + 12 + ... + 6r = 1 + 3r(r+1)
    expected_count = 1 + 3 * 10 * 11
    assert len(large_range) == expected_count
    
    # 空障碍物路径
    path = hex_path_astar(Hex(0, 0), Hex(5, 5), set())
    assert len(path) > 0
    
    # 相同起点终点
    same_path = hex_line(Hex(3, 3), Hex(3, 3))
    assert len(same_path) == 1
    
    print("✓ 边界情况测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("🧪 六边形网格工具测试套件")
    print("=" * 60)
    
    tests = [
        test_basic_hex_operations,
        test_directions,
        test_distance,
        test_range_generation,
        test_line_drawing,
        test_shapes,
        test_rotation_reflection,
        test_coordinate_conversion,
        test_corners,
        test_pathfinding,
        test_field_of_view,
        test_flood_fill,
        test_region_operations,
        test_hex_grid_class,
        test_visualization,
        test_edge_cases,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} 失败: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} 异常: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)