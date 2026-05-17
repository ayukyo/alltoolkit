#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hex Grid Utils Test - 六边形网格工具测试

测试模块：hex_grid_utils
测试用例数：55+
测试覆盖：坐标系统、距离计算、区域生成、路径查找、坐标转换、可视化
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Hex, HexOrientation, OffsetCoordType,
    hex_add, hex_subtract, hex_scale,
    hex_direction, hex_neighbor, hex_neighbors, hex_diagonal_neighbors,
    hex_distance, hex_distance_chebyshev,
    hex_range, hex_ring, hex_spiral, hex_line, hex_triangle,
    hex_parallelogram, hex_hexagon, hex_rectangle,
    hex_rotate_right, hex_rotate_left, hex_rotate_180,
    hex_reflect_q, hex_reflect_r, hex_reflect_s,
    hex_to_offset, offset_to_hex,
    hex_to_pixel, pixel_to_hex, hex_round,
    hex_corner_offset, hex_corners,
    hex_path_astar, hex_path_bfs,
    hex_fov, hex_visible_from,
    hex_flood_fill, hex_region_outline, hex_region_interior,
    HexGrid,
    visualize_hex, visualize_hex_grid, visualize_hex_path, visualize_hex_range
)


def test_result_collector():
    """测试结果收集器"""
    results = []
    
    def add_result(test_name: str, passed: bool, message: str = ""):
        results.append({
            "name": test_name,
            "passed": passed,
            "message": message
        })
    
    return results, add_result


def test_hex_creation(results, add_result):
    """测试六边形坐标创建"""
    # test 1: 基础创建
    h = Hex(1, 2)
    add_result("Hex basic", h.q == 1 and h.r == 2)
    
    # test 2: s 属性
    add_result("Hex s property", h.s == -3, f"Expected -3, got {h.s}")
    
    # test 3: to_tuple
    add_result("Hex to_tuple", h.to_tuple() == (1, 2))
    
    # test 4: to_cube
    add_result("Hex to_cube", h.to_cube() == (1, 2, -3))
    
    # test 5: from_cube
    h2 = Hex.from_cube(2, -1, -1)
    add_result("Hex from_cube", h2.q == 2 and h2.r == -1)
    
    # test 6: from_cube 无效坐标异常
    try:
        Hex.from_cube(1, 1, 1)  # x+y+z != 0
        add_result("Hex from_cube invalid exception", False, "Should raise ValueError")
    except ValueError:
        add_result("Hex from_cube invalid exception", True)


def test_hex_arithmetic(results, add_result):
    """测试六边形算术"""
    h1 = Hex(1, 2)
    h2 = Hex(3, 1)
    
    # test 7: 加法
    add_result("Hex add", (h1 + h2) == Hex(4, 3))
    
    # test 8: 减法
    add_result("Hex subtract", (h1 - h2) == Hex(-2, 1))
    
    # test 9: 缩放
    add_result("Hex scale", h1 * 2 == Hex(2, 4))
    
    # test 10: 取负
    add_result("Hex negate", -h1 == Hex(-1, -2))
    
    # test 11: hex_add 函数
    add_result("hex_add function", hex_add(h1, h2) == Hex(4, 3))
    
    # test 12: hex_subtract 函数
    add_result("hex_subtract function", hex_subtract(h1, h2) == Hex(-2, 1))
    
    # test 13: hex_scale 函数
    add_result("hex_scale function", hex_scale(h1, 3) == Hex(3, 6))


def test_directions(results, add_result):
    """测试方向"""
    h = Hex(0, 0)
    
    # test 14: hex_direction
    d = hex_direction(HexOrientation.POINTY_TOP, 0)
    add_result("hex_direction", d.q == 1 and d.r == 0)
    
    # test 15: hex_neighbor
    n = hex_neighbor(h, HexOrientation.POINTY_TOP, 0)
    add_result("hex_neighbor", n == Hex(1, 0))
    
    # test 16: hex_neighbors
    neighbors = hex_neighbors(h)
    add_result("hex_neighbors count", len(neighbors) == 6)
    
    # test 17: hex_neighbors 位置正确
    add_result("hex_neighbors correct", Hex(1, 0) in neighbors and Hex(0, 1) in neighbors)
    
    # test 18: hex_diagonal_neighbors
    diag = hex_diagonal_neighbors(h)
    add_result("hex_diagonal_neighbors count", len(diag) == 6)


def test_distance(results, add_result):
    """测试距离计算"""
    h1 = Hex(0, 0)
    h2 = Hex(3, -3)
    
    # test 19: hex_distance
    add_result("hex_distance", hex_distance(h1, h2) == 3)
    
    # test 20: 零距离
    add_result("hex_distance zero", hex_distance(h1, h1) == 0)
    
    # test 21: hex_distance_chebyshev
    add_result("hex_distance_chebyshev", hex_distance_chebyshev(h1, h2) == 3)


def test_regions(results, add_result):
    """测试区域生成"""
    center = Hex(0, 0)
    
    # test 22: hex_range
    range1 = hex_range(center, 1)
    add_result("hex_range radius 1", len(range1) == 7)  # 中心 + 6个邻居
    
    # test 23: hex_range radius 2
    range2 = hex_range(center, 2)
    add_result("hex_range radius 2", len(range2) == 19)  # 1 + 6 + 12
    
    # test 24: hex_ring radius 1
    ring1 = hex_ring(center, 1)
    add_result("hex_ring radius 1", len(ring1) == 6)  # 不包含中心
    
    # test 25: hex_ring radius 0
    ring0 = hex_ring(center, 0)
    add_result("hex_ring radius 0", ring0 == [center])
    
    # test 26: hex_spiral
    spiral = hex_spiral(center, 2)
    add_result("hex_spiral", len(spiral) == 19)  # 从中心向外
    
    # test 27: hex_line
    line = hex_line(Hex(0, 0), Hex(3, 0))
    add_result("hex_line", len(line) == 4)  # 0,1,2,3
    
    # test 28: hex_triangle
    triangle = hex_triangle(3)
    add_result("hex_triangle", len(triangle) > 0)
    
    # test 29: hex_parallelogram
    para = hex_parallelogram(0, 2, 0, 2)
    add_result("hex_parallelogram", len(para) == 9)
    
    # test 30: hex_hexagon
    hexagon = hex_hexagon(2)
    add_result("hex_hexagon", len(hexagon) == 19)


def test_rotation(results, add_result):
    """测试旋转"""
    h = Hex(1, 2)
    
    # test 31: hex_rotate_right (顺时针旋转60度)
    rotated = hex_rotate_right(h)
    add_result("hex_rotate_right", rotated != h)  # 旋转后应该不同
    
    # test 32: hex_rotate_left (逆时针旋转60度)
    rotated_left = hex_rotate_left(h)
    add_result("hex_rotate_left", rotated_left != h)  # 旋转后应该不同
    
    # test 33: hex_rotate_180
    rotated180 = hex_rotate_180(h)
    add_result("hex_rotate_180", rotated180 == Hex(-1, -2))


def test_reflection(results, add_result):
    """测试镜像"""
    h = Hex(2, 3)
    
    # test 34: hex_reflect_q
    add_result("hex_reflect_q", hex_reflect_q(h).q == h.q)
    
    # test 35: hex_reflect_r
    add_result("hex_reflect_r", hex_reflect_r(h).r == h.r)
    
    # test 36: hex_reflect_s
    add_result("hex_reflect_s", hex_reflect_s(h).s == h.s)


def test_offset_conversion(results, add_result):
    """测试偏移坐标转换"""
    h = Hex(3, 4)
    
    # test 37: hex_to_offset
    offset = hex_to_offset(h, OffsetCoordType.ODD, HexOrientation.POINTY_TOP)
    add_result("hex_to_offset", len(offset) == 2)
    
    # test 38: offset_to_hex
    back = offset_to_hex(offset[0], offset[1], OffsetCoordType.ODD, HexOrientation.POINTY_TOP)
    add_result("offset_to_hex", back == h)


def test_pixel_conversion(results, add_result):
    """测试像素坐标转换"""
    h = Hex(1, 2)
    size = 30
    
    # test 39: hex_to_pixel
    pixel = hex_to_pixel(h, size)
    add_result("hex_to_pixel", len(pixel) == 2 and pixel[0] > 0)
    
    # test 40: pixel_to_hex
    back = pixel_to_hex(pixel[0], pixel[1], size)
    add_result("pixel_to_hex", back == h)
    
    # test 41: hex_round
    rounded = hex_round(1.4, 2.6)
    add_result("hex_round", rounded.q == 1 or rounded.q == 2)


def test_corners(results, add_result):
    """测试角点计算"""
    center = (100, 100)
    size = 50
    
    # test 42: hex_corner_offset
    offset = hex_corner_offset(0, size)
    add_result("hex_corner_offset", len(offset) == 2)
    
    # test 43: hex_corners
    corners = hex_corners(center, size)
    add_result("hex_corners", len(corners) == 6)


def test_pathfinding(results, add_result):
    """测试路径查找"""
    start = Hex(0, 0)
    goal = Hex(3, 3)
    obstacles = {Hex(1, 1)}
    
    # test 44: hex_path_astar 无障碍
    path = hex_path_astar(start, goal, set())
    add_result("hex_path_astar no obstacles", len(path) > 0 and path[-1] == goal)
    
    # test 45: hex_path_astar 有障碍
    path_with_obstacles = hex_path_astar(start, goal, obstacles)
    add_result("hex_path_astar with obstacles", len(path_with_obstacles) > 0)
    
    # test 46: hex_path_bfs
    bfs_path = hex_path_bfs(start, goal, set())
    add_result("hex_path_bfs", len(bfs_path) > 0 and bfs_path[-1] == goal)
    
    # test 47: 不可达路径 (目标超出网格范围)
    blocked = hex_range(Hex(1, 1), 1)
    # 使用超大目标确保不可达
    unreachable = hex_path_astar(start, Hex(100, 100), blocked, max_radius=5)
    add_result("path unreachable", len(unreachable) == 0)


def test_fov(results, add_result):
    """测试视野计算"""
    center = Hex(0, 0)
    
    # test 48: hex_fov 无阻挡
    visible = hex_fov(center, 2, lambda h: False)
    add_result("hex_fov no blocking", len(visible) > 0)
    
    # test 49: hex_visible_from
    target = Hex(2, 0)
    obstacles = {Hex(1, 0)}
    is_visible = hex_visible_from(center, target, obstacles)
    add_result("hex_visible_from blocked", not is_visible)
    
    # test 50: hex_visible_from 无障碍
    is_visible2 = hex_visible_from(center, target, set())
    add_result("hex_visible_from clear", is_visible2)


def test_region_operations(results, add_result):
    """测试区域操作"""
    region = set(hex_range(Hex(0, 0), 2))
    
    # test 51: hex_flood_fill
    filled = hex_flood_fill(Hex(0, 0), lambda h: h in region)
    add_result("hex_flood_fill", len(filled) == len(region))
    
    # test 52: hex_region_outline
    outline = hex_region_outline(region)
    add_result("hex_region_outline", len(outline) > 0)
    
    # test 53: hex_region_interior
    interior = hex_region_interior(region)
    add_result("hex_region_interior", len(interior) > 0)


def test_hex_grid_class(results, add_result):
    """测试 HexGrid 类"""
    grid = HexGrid(radius=5)
    
    # test 54: in_bounds
    add_result("HexGrid in_bounds center", grid.in_bounds(Hex(0, 0)))
    add_result("HexGrid in_bounds edge", grid.in_bounds(Hex(5, 0)))
    add_result("HexGrid in_bounds outside", not grid.in_bounds(Hex(6, 0)))
    
    # test 55: set/get
    grid.set(Hex(0, 0), "center")
    add_result("HexGrid set/get", grid.get(Hex(0, 0)) == "center")
    
    # test 56: remove
    grid.remove(Hex(0, 0))
    add_result("HexGrid remove", grid.get(Hex(0, 0)) is None)
    
    # test 57: all_cells
    cells = grid.all_cells()
    add_result("HexGrid all_cells", len(cells) > 0)
    
    # test 58: neighbors
    neighbors = grid.neighbors(Hex(0, 0))
    add_result("HexGrid neighbors", len(neighbors) == 6)
    
    # test 59: path
    path = grid.path(Hex(0, 0), Hex(3, 0))
    add_result("HexGrid path", len(path) > 0)
    
    # test 60: to_ascii
    grid.set(Hex(0, 0), "C")
    ascii_str = grid.to_ascii()
    add_result("HexGrid to_ascii", len(ascii_str) > 0)


def test_visualization(results, add_result):
    """测试可视化"""
    # test 61: visualize_hex
    vis = visualize_hex(Hex(0, 0), size=2)
    add_result("visualize_hex", len(vis) > 0)
    
    # test 62: visualize_hex_grid
    hexes = hex_range(Hex(0, 0), 2)
    grid_vis = visualize_hex_grid(hexes)
    add_result("visualize_hex_grid", len(grid_vis) > 0)
    
    # test 63: visualize_hex_path
    path = hex_line(Hex(0, 0), Hex(3, 0))
    path_vis = visualize_hex_path(path)
    add_result("visualize_hex_path", "S" in path_vis and "E" in path_vis)
    
    # test 64: visualize_hex_range
    range_vis = visualize_hex_range(Hex(0, 0), 2)
    add_result("visualize_hex_range", "O" in range_vis)


def test_comparison(results, add_result):
    """测试比较"""
    h1 = Hex(1, 2)
    h2 = Hex(2, 3)
    h3 = Hex(1, 2)
    
    # test 65: 小于
    add_result("Hex lt", h1 < h2)
    
    # test 66: 等于
    add_result("Hex eq", h1 == h3)
    
    # test 67: 大于
    add_result("Hex gt", h2 > h1)


def main():
    """运行所有测试"""
    results, add_result = test_result_collector()
    
    # 运行各测试组
    test_hex_creation(results, add_result)
    test_hex_arithmetic(results, add_result)
    test_directions(results, add_result)
    test_distance(results, add_result)
    test_regions(results, add_result)
    test_rotation(results, add_result)
    test_reflection(results, add_result)
    test_offset_conversion(results, add_result)
    test_pixel_conversion(results, add_result)
    test_corners(results, add_result)
    test_pathfinding(results, add_result)
    test_fov(results, add_result)
    test_region_operations(results, add_result)
    test_hex_grid_class(results, add_result)
    test_visualization(results, add_result)
    test_comparison(results, add_result)
    
    # 输出结果
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    
    print("=" * 60)
    print("Hex Grid Utils Test Results")
    print("=" * 60)
    
    for r in results:
        status = "✅" if r["passed"] else "❌"
        print(f"{status} {r['name']}: {r['message']}")
    
    print("-" * 60)
    print(f"Summary: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("=" * 60)
    
    return passed, total


if __name__ == "__main__":
    passed, total = main()
    sys.exit(0 if passed == total else 1)