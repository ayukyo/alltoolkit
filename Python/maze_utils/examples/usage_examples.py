"""
迷宫工具模块使用示例

展示迷宫生成、求解和可视化的各种用法。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from maze_utils.mod import (
    Maze, MazeGenerator, MazeSolver, MazeUtils,
    generate_maze, solve_maze, print_maze
)


def example_basic_generation():
    """基本迷宫生成示例。"""
    print("\n" + "=" * 60)
    print("示例1: 基本迷宫生成")
    print("=" * 60)
    
    # 生成21x11的迷宫（实际会是21x11，确保奇数）
    maze = generate_maze(21, 11, algorithm='dfs', seed=42)
    
    print("\nDFS算法生成的迷宫:")
    print(maze)
    
    # 求解迷宫
    path = solve_maze(maze, 'bfs')
    print(f"\nBFS求解路径长度: {len(path)}")
    
    # 显示解决方案
    print("\n迷宫解决方案:")
    print(MazeUtils.visualize(maze, path))


def example_all_generation_algorithms():
    """展示所有生成算法。"""
    print("\n" + "=" * 60)
    print("示例2: 所有生成算法对比")
    print("=" * 60)
    
    algorithms = ['dfs', 'prim', 'kruskal', 'division', 'eller']
    
    for algo in algorithms:
        print(f"\n--- {algo.upper()} 算法 ---")
        maze = generate_maze(21, 11, algorithm=algo, seed=42)
        path = solve_maze(maze, 'bfs')
        stats = MazeUtils.get_statistics(maze)
        
        print(f"通道数: {stats['passages']}, 墙壁比例: {stats['wall_ratio']:.1%}")
        print(f"最短路径长度: {len(path)}")
        print(maze)


def example_all_solving_algorithms():
    """展示所有求解算法。"""
    print("\n" + "=" * 60)
    print("示例3: 所有求解算法对比")
    print("=" * 60)
    
    maze = generate_maze(31, 15, algorithm='dfs', seed=100)
    
    print("\n生成的迷宫:")
    print(maze)
    
    # 比较所有算法
    results = MazeUtils.compare_algorithms(maze)
    
    print("\n算法性能对比:")
    print("-" * 40)
    for algo, result in results.items():
        print(f"  {algo:15s}: 路径长度={result['path_length']:4d}, "
              f"耗时={result['time_seconds']*1000:.2f}ms")


def example_custom_maze():
    """自定义迷宫示例。"""
    print("\n" + "=" * 60)
    print("示例4: 自定义迷宫")
    print("=" * 60)
    
    # 从字符串创建自定义迷宫
    maze_str = """
#####################
#S  #       #       #
# # # ##### # ##### #
# #   #   # #     # #
# ##### # # ##### # #
#       # #     #   #
# ########### ##### #
# #       # #     # #
# # ##### # # ##### #
#   #     #       #E#
#####################
"""
    
    maze = MazeUtils.create_from_string(maze_str)
    
    print("\n自定义迷宫:")
    print(maze)
    
    # 用不同算法求解
    for algo in ['bfs', 'dfs', 'astar']:
        path = solve_maze(maze, algo)
        print(f"\n{algo.upper()} 求解结果 (长度: {len(path)}):")
        print(MazeUtils.visualize(maze, path))


def example_maze_statistics():
    """迷宫统计信息示例。"""
    print("\n" + "=" * 60)
    print("示例5: 迷宫统计信息")
    print("=" * 60)
    
    maze = generate_maze(31, 15, algorithm='dfs', seed=42)
    
    stats = MazeUtils.get_statistics(maze)
    
    print("\n迷宫统计:")
    print(f"  宽度: {stats['width']}")
    print(f"  高度: {stats['height']}")
    print(f"  总单元格: {stats['total_cells']}")
    print(f"  墙壁数: {stats['walls']}")
    print(f"  通道数: {stats['passages']}")
    print(f"  墙壁比例: {stats['wall_ratio']:.1%}")
    print(f"  通道比例: {stats['passage_ratio']:.1%}")


def example_find_all_paths():
    """查找所有路径示例。"""
    print("\n" + "=" * 60)
    print("示例6: 查找所有路径")
    print("=" * 60)
    
    # 创建一个有多个路径的小迷宫
    maze_str = """
###########
#S    #   #
# ### # # #
# #   # # #
# # ### # #
# #     #E#
###########
"""
    
    maze = MazeUtils.create_from_string(maze_str)
    
    print("\n迷宫:")
    print(maze)
    
    # 查找所有路径（最多10条）
    paths = MazeUtils.find_all_paths(maze, max_paths=10)
    
    print(f"\n找到 {len(paths)} 条路径:")
    for i, path in enumerate(paths, 1):
        print(f"  路径 {i}: 长度 {len(path)}")
        print(MazeUtils.visualize(maze, path))
        print()


def example_maze_validation():
    """迷宫验证示例。"""
    print("\n" + "=" * 60)
    print("示例7: 迷宫验证")
    print("=" * 60)
    
    # 有效迷宫
    maze = generate_maze(21, 11, seed=42)
    valid, errors = MazeUtils.validate_maze(maze)
    
    print("\n有效迷宫验证:")
    print(f"  结果: {'有效' if valid else '无效'}")
    if errors:
        for err in errors:
            print(f"  错误: {err}")
    
    # 无效迷宫（手动创建）
    print("\n无效迷宫验证（无起点终点）:")
    invalid_maze = Maze(11, 7)
    valid, errors = MazeUtils.validate_maze(invalid_maze)
    print(f"  结果: {'有效' if valid else '无效'}")
    for err in errors:
        print(f"  错误: {err}")


def example_different_sizes():
    """不同尺寸迷宫示例。"""
    print("\n" + "=" * 60)
    print("示例8: 不同尺寸迷宫")
    print("=" * 60)
    
    sizes = [(11, 7), (21, 11), (31, 15), (41, 21)]
    
    for width, height in sizes:
        maze = generate_maze(width, height, seed=42)
        path = solve_maze(maze, 'bfs')
        stats = MazeUtils.get_statistics(maze)
        
        print(f"\n{width}x{height} 迷宫:")
        print(f"  通道数: {stats['passages']}")
        print(f"  路径长度: {len(path)}")


def example_wall_follower():
    """墙壁跟随算法演示。"""
    print("\n" + "=" * 60)
    print("示例9: 墙壁跟随算法")
    print("=" * 60)
    
    maze = generate_maze(21, 11, seed=50)
    
    print("\n迷宫:")
    print(maze)
    
    # 右手法则
    path_right = MazeSolver.solve_wall_follower(maze, 'right')
    print(f"\n右手法则路径长度: {len(path_right)}")
    print(MazeUtils.visualize(maze, path_right))
    
    # 左手法则
    maze.clear_solution()
    path_left = MazeSolver.solve_wall_follower(maze, 'left')
    print(f"\n左手法则路径长度: {len(path_left)}")
    print(MazeUtils.visualize(maze, path_left))


def example_dead_end_filling():
    """死胡同填充算法演示。"""
    print("\n" + "=" * 60)
    print("示例10: 死胡同填充算法")
    print("=" * 60)
    
    maze = generate_maze(21, 11, seed=60)
    
    print("\n原始迷宫:")
    print(maze)
    
    path = MazeSolver.solve_dead_end_filling(maze)
    print(f"\n死胡同填充算法路径长度: {len(path)}")
    print(MazeUtils.visualize(maze, path))


def example_maze_copy_and_modify():
    """迷宫复制和修改示例。"""
    print("\n" + "=" * 60)
    print("示例11: 迷宫复制和修改")
    print("=" * 60)
    
    original = generate_maze(21, 11, seed=42)
    
    print("\n原始迷宫:")
    print(original)
    
    # 创建副本并修改
    copy = original.copy()
    
    # 在副本中添加额外通道
    copy.set_cell(5, 5, Maze.PATH)
    copy.set_cell(6, 5, Maze.PATH)
    copy.set_cell(7, 5, Maze.PATH)
    
    print("\n修改后的迷宫副本:")
    print(copy)
    
    # 比较路径长度
    path_orig = solve_maze(original, 'bfs')
    path_copy = solve_maze(copy, 'bfs')
    
    print(f"\n原始迷宫最短路径: {len(path_orig)}")
    print(f"修改后最短路径: {len(path_copy)}")


def example_reproducible_mazes():
    """可复现迷宫示例。"""
    print("\n" + "=" * 60)
    print("示例12: 可复现迷宫（使用种子）")
    print("=" * 60)
    
    # 相同种子产生相同迷宫
    maze1 = generate_maze(21, 11, seed=999)
    maze2 = generate_maze(21, 11, seed=999)
    
    print("\n使用相同种子(999)生成的两个迷宫是否相同:")
    same = str(maze1) == str(maze2)
    print(f"  结果: {'相同' if same else '不同'}")
    
    # 不同种子产生不同迷宫
    maze3 = generate_maze(21, 11, seed=1000)
    
    print("\n使用不同种子(1000)生成的迷宫:")
    print(f"  与种子999的迷宫是否相同: {'是' if str(maze1) == str(maze3) else '否'}")


def example_custom_start_end():
    """自定义起点终点示例。"""
    print("\n" + "=" * 60)
    print("示例13: 自定义起点终点")
    print("=" * 60)
    
    # 自定义起点终点
    maze = MazeGenerator.generate_dfs(
        21, 11, 
        start=(1, 1), 
        end=(19, 9),
        seed=42
    )
    
    print(f"\n起点: {maze.start}, 终点: {maze.end}")
    print(maze)
    
    path = solve_maze(maze, 'bfs')
    print(f"\n路径长度: {len(path)}")
    print(MazeUtils.visualize(maze, path))


def main():
    """运行所有示例。"""
    print("=" * 60)
    print("迷宫工具模块 - 使用示例")
    print("=" * 60)
    
    example_basic_generation()
    example_all_generation_algorithms()
    example_all_solving_algorithms()
    example_custom_maze()
    example_maze_statistics()
    example_find_all_paths()
    example_maze_validation()
    example_different_sizes()
    example_wall_follower()
    example_dead_end_filling()
    example_maze_copy_and_modify()
    example_reproducible_mazes()
    example_custom_start_end()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()