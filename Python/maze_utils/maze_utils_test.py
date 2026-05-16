"""
迷宫工具模块测试

测试迷宫生成和求解功能。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from maze_utils.mod import (
    Maze, MazeGenerator, MazeSolver, MazeUtils,
    generate_maze, solve_maze, print_maze
)


def test_maze_creation():
    """测试迷宫创建。"""
    print("测试迷宫创建...")
    
    maze = Maze(11, 7)
    assert maze.width == 11
    assert maze.height == 7
    
    # 检查初始状态（全墙）
    for row in maze.grid:
        assert all(cell == Maze.WALL for cell in row)
    
    print("  ✓ 迷宫创建测试通过")


def test_maze_operations():
    """测试迷宫基本操作。"""
    print("测试迷宫基本操作...")
    
    maze = Maze(11, 7)
    
    # 测试有效性检查
    assert maze.is_valid(0, 0) == True
    assert maze.is_valid(10, 6) == True
    assert maze.is_valid(-1, 0) == False
    assert maze.is_valid(11, 0) == False
    
    # 测试设置和获取
    maze.set_cell(5, 3, Maze.PATH)
    assert maze.get_cell(5, 3) == Maze.PATH
    assert maze.is_path(5, 3) == True
    
    # 测试起点终点设置
    maze.set_start(1, 1)
    maze.set_end(9, 5)
    assert maze.start == (1, 1)
    assert maze.end == (9, 5)
    assert maze.get_cell(1, 1) == Maze.START
    assert maze.get_cell(9, 5) == Maze.END
    
    print("  ✓ 基本操作测试通过")


def test_maze_copy():
    """测试迷宫复制。"""
    print("测试迷宫复制...")
    
    maze1 = Maze(11, 7)
    maze1.set_cell(5, 3, Maze.PATH)
    maze1.set_start(1, 1)
    
    maze2 = maze1.copy()
    assert maze2.width == maze1.width
    assert maze2.height == maze1.height
    assert maze2.start == maze1.start
    
    # 修改maze2不应影响maze1
    maze2.set_cell(5, 3, Maze.WALL)
    assert maze1.get_cell(5, 3) == Maze.PATH
    
    print("  ✓ 复制测试通过")


def test_dfs_generation():
    """测试DFS迷宫生成。"""
    print("测试DFS迷宫生成...")
    
    maze = MazeGenerator.generate_dfs(21, 11, seed=42)
    
    # 检查起点终点
    assert maze.start == (1, 1)
    assert maze.end == (19, 9)
    
    # 检查边界
    for x in range(maze.width):
        assert maze.is_wall(x, 0)
        assert maze.is_wall(x, maze.height - 1)
    
    for y in range(maze.height):
        assert maze.is_wall(0, y)
        assert maze.is_wall(maze.width - 1, y)
    
    # 检查迷宫可解
    path = MazeSolver.solve_bfs(maze)
    assert path is not None
    assert path[0] == maze.start
    assert path[-1] == maze.end
    
    print("  ✓ DFS生成测试通过")


def test_prim_generation():
    """测试Prim算法迷宫生成。"""
    print("测试Prim算法迷宫生成...")
    
    maze = MazeGenerator.generate_prim(21, 11, seed=42)
    
    assert maze.start is not None
    assert maze.end is not None
    
    # 检查迷宫可解
    path = MazeSolver.solve_bfs(maze)
    assert path is not None
    
    print("  ✓ Prim生成测试通过")


def test_kruskal_generation():
    """测试Kruskal算法迷宫生成。"""
    print("测试Kruskal算法迷宫生成...")
    
    maze = MazeGenerator.generate_kruskal(21, 11, seed=42)
    
    # 检查迷宫可解
    path = MazeSolver.solve_bfs(maze)
    assert path is not None
    
    print("  ✓ Kruskal生成测试通过")


def test_recursive_division_generation():
    """测试递归分割算法迷宫生成。"""
    print("测试递归分割算法迷宫生成...")
    
    maze = MazeGenerator.generate_recursive_division(21, 11, seed=42)
    
    # 检查迷宫可解
    path = MazeSolver.solve_bfs(maze)
    assert path is not None
    
    print("  ✓ 递归分割生成测试通过")


def test_eller_generation():
    """测试Eller算法迷宫生成。"""
    print("测试Eller算法迷宫生成...")
    
    maze = MazeGenerator.generate_eller(21, 11, seed=42)
    
    # 检查迷宫可解
    path = MazeSolver.solve_bfs(maze)
    assert path is not None
    
    print("  ✓ Eller生成测试通过")


def test_bfs_solver():
    """测试BFS求解器。"""
    print("测试BFS求解器...")
    
    maze = generate_maze(21, 11, 'dfs', seed=42)
    path = MazeSolver.solve_bfs(maze)
    
    assert path is not None
    assert path[0] == maze.start
    assert path[-1] == maze.end
    
    # BFS应该找到最短路径
    # 验证路径连续性
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        distance = abs(x2 - x1) + abs(y2 - y1)
        assert distance == 1, f"路径不连续: {path[i]} -> {path[i+1]}"
    
    print("  ✓ BFS求解测试通过")


def test_dfs_solver():
    """测试DFS求解器。"""
    print("测试DFS求解器...")
    
    maze = generate_maze(21, 11, 'dfs', seed=42)
    path = MazeSolver.solve_dfs(maze)
    
    assert path is not None
    assert path[0] == maze.start
    assert path[-1] == maze.end
    
    print("  ✓ DFS求解测试通过")


def test_astar_solver():
    """测试A*求解器。"""
    print("测试A*求解器...")
    
    maze = generate_maze(21, 11, 'dfs', seed=42)
    path = MazeSolver.solve_astar(maze)
    
    assert path is not None
    assert path[0] == maze.start
    assert path[-1] == maze.end
    
    # A*也应该找到最短路径
    bfs_path = MazeSolver.solve_bfs(maze)
    assert len(path) == len(bfs_path), "A*路径长度应与BFS相同"
    
    print("  ✓ A*求解测试通过")


def test_wall_follower_solver():
    """测试墙壁跟随求解器。"""
    print("测试墙壁跟随求解器...")
    
    maze = generate_maze(21, 11, 'dfs', seed=42)
    
    # 右手法则
    path_right = MazeSolver.solve_wall_follower(maze, 'right')
    assert path_right is not None
    
    # 左手法则
    path_left = MazeSolver.solve_wall_follower(maze, 'left')
    assert path_left is not None
    
    print("  ✓ 墙壁跟随求解测试通过")


def test_dead_end_filling_solver():
    """测试死胡同填充求解器。"""
    print("测试死胡同填充求解器...")
    
    maze = generate_maze(21, 11, 'dfs', seed=42)
    path = MazeSolver.solve_dead_end_filling(maze)
    
    assert path is not None
    assert path[0] == maze.start
    assert path[-1] == maze.end
    
    print("  ✓ 死胡同填充求解测试通过")


def test_maze_utils():
    """测试工具类便捷方法。"""
    print("测试工具类便捷方法...")
    
    # 生成
    maze = MazeUtils.generate(21, 11, 'dfs', seed=42)
    assert maze is not None
    
    # 求解
    path = MazeUtils.solve(maze, 'bfs')
    assert path is not None
    
    # 可视化
    viz = MazeUtils.visualize(maze, path)
    assert len(viz) > 0
    assert Maze.START in viz or '#' in viz
    
    # 统计
    stats = MazeUtils.get_statistics(maze)
    assert stats['width'] == 21
    assert stats['height'] == 11
    assert stats['walls'] > 0
    assert stats['passages'] > 0
    
    print("  ✓ 工具类测试通过")


def test_validate_maze():
    """测试迷宫验证。"""
    print("测试迷宫验证...")
    
    # 有效迷宫
    maze = generate_maze(21, 11, 'dfs', seed=42)
    valid, errors = MazeUtils.validate_maze(maze)
    assert valid == True
    assert len(errors) == 0
    
    # 无效迷宫（无起点）
    invalid_maze = Maze(11, 7)
    valid, errors = MazeUtils.validate_maze(invalid_maze)
    assert valid == False
    assert "缺少起点" in errors[0] or "无解" in str(errors)
    
    print("  ✓ 验证测试通过")


def test_create_from_string():
    """测试从字符串创建迷宫。"""
    print("测试从字符串创建迷宫...")
    
    # 使用一个有解的迷宫
    maze_str = """
#########
#S      #
# ##### #
#     # #
##### # #
#     #E#
#########
"""
    maze = MazeUtils.create_from_string(maze_str)
    
    assert maze.start == (1, 1)
    assert maze.end == (7, 5)
    
    # 求解
    path = solve_maze(maze, 'bfs')
    assert path is not None
    assert path[0] == (1, 1)
    assert path[-1] == (7, 5)
    
    print("  ✓ 字符串创建测试通过")


def test_find_all_paths():
    """测试查找所有路径。"""
    print("测试查找所有路径...")
    
    # 创建一个有多个路径的迷宫
    maze_str = """
#######
#S    #
# ### #
#   # #
### # #
#    E#
#######
"""
    maze = MazeUtils.create_from_string(maze_str)
    
    paths = MazeUtils.find_all_paths(maze, max_paths=10)
    assert len(paths) >= 1
    
    # 所有路径都应该从起点到终点
    for path in paths:
        assert path[0] == maze.start
        assert path[-1] == maze.end
    
    print("  ✓ 查找所有路径测试通过")


def test_path_length():
    """测试路径长度计算。"""
    print("测试路径长度计算...")
    
    maze = generate_maze(21, 11, 'dfs', seed=42)
    length = MazeUtils.get_path_length(maze, 'bfs')
    
    assert length is not None
    assert length > 0
    
    print("  ✓ 路径长度测试通过")


def test_compare_algorithms():
    """测试算法比较。"""
    print("测试算法比较...")
    
    maze = generate_maze(21, 11, 'dfs', seed=42)
    results = MazeUtils.compare_algorithms(maze)
    
    # 所有算法应该都能求解
    for algo, result in results.items():
        assert result['solved'] == True
        assert result['path_length'] > 0
        assert result['time_seconds'] >= 0
    
    print("  ✓ 算法比较测试通过")


def test_clear_solution():
    """测试清除解决方案。"""
    print("测试清除解决方案...")
    
    maze = generate_maze(21, 11, 'dfs', seed=42)
    path = solve_maze(maze, 'bfs')
    
    # 绘制路径
    for x, y in path:
        if (x, y) != maze.start and (x, y) != maze.end:
            maze.set_cell(x, y, Maze.SOLUTION)
    
    # 清除
    maze.clear_solution()
    
    # 检查解决方案标记已清除
    for row in maze.grid:
        assert Maze.SOLUTION not in row
    
    # 起点终点应该保持
    assert maze.get_cell(*maze.start) == Maze.START
    assert maze.get_cell(*maze.end) == Maze.END
    
    print("  ✓ 清除解决方案测试通过")


def test_different_sizes():
    """测试不同尺寸的迷宫。"""
    print("测试不同尺寸迷宫...")
    
    sizes = [(11, 11), (21, 21), (31, 15), (15, 31)]
    
    for width, height in sizes:
        maze = generate_maze(width, height, 'dfs', seed=42)
        path = solve_maze(maze, 'bfs')
        assert path is not None, f"迷宫 {width}x{height} 无解"
    
    print("  ✓ 不同尺寸测试通过")


def test_deterministic_generation():
    """测试确定性生成（相同种子产生相同迷宫）。"""
    print("测试确定性生成...")
    
    maze1 = generate_maze(21, 11, 'dfs', seed=12345)
    maze2 = generate_maze(21, 11, 'dfs', seed=12345)
    
    # 检查两个迷宫相同
    for y in range(maze1.height):
        for x in range(maze1.width):
            assert maze1.get_cell(x, y) == maze2.get_cell(x, y)
    
    print("  ✓ 确定性生成测试通过")


def test_custom_start_end():
    """测试自定义起点终点。"""
    print("测试自定义起点终点...")
    
    maze = MazeGenerator.generate_dfs(21, 11, start=(1, 1), end=(15, 7), seed=42)
    
    assert maze.start == (1, 1)
    assert maze.end == (15, 7)
    
    # 检查可解
    path = solve_maze(maze, 'bfs')
    assert path is not None
    
    print("  ✓ 自定义起点终点测试通过")


def run_all_tests():
    """运行所有测试。"""
    print("\n" + "=" * 60)
    print("迷宫工具模块测试")
    print("=" * 60 + "\n")
    
    tests = [
        test_maze_creation,
        test_maze_operations,
        test_maze_copy,
        test_dfs_generation,
        test_prim_generation,
        test_kruskal_generation,
        test_recursive_division_generation,
        test_eller_generation,
        test_bfs_solver,
        test_dfs_solver,
        test_astar_solver,
        test_wall_follower_solver,
        test_dead_end_filling_solver,
        test_maze_utils,
        test_validate_maze,
        test_create_from_string,
        test_find_all_paths,
        test_path_length,
        test_compare_algorithms,
        test_clear_solution,
        test_different_sizes,
        test_deterministic_generation,
        test_custom_start_end,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ 测试失败: {test.__name__}")
            print(f"    错误: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ 测试异常: {test.__name__}")
            print(f"    异常: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)