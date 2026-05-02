#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Maze Utilities Usage Examples
===========================================
Practical examples demonstrating the maze_utils module capabilities.

Run with: python usage_examples.py
"""

import sys
import os

# Import directly from the module file
mod_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'mod.py')
import importlib.util
spec = importlib.util.spec_from_file_location("maze_utils_mod", mod_path)
maze_utils_mod = importlib.util.module_from_spec(spec)
sys.modules['maze_utils_mod'] = maze_utils_mod
spec.loader.exec_module(maze_utils_mod)

# Import functions
Maze = maze_utils_mod.Maze
MazeSolution = maze_utils_mod.MazeSolution
MazeMetrics = maze_utils_mod.MazeMetrics
Cell = maze_utils_mod.Cell
Direction = maze_utils_mod.Direction
create_maze = maze_utils_mod.create_maze
solve_maze = maze_utils_mod.solve_maze
maze_from_string = maze_utils_mod.maze_from_string
compare_solvers = maze_utils_mod.compare_solvers
get_path_directions = maze_utils_mod.get_path_directions
generate_maze_collection = maze_utils_mod.generate_maze_collection
print_maze_with_solution = maze_utils_mod.print_maze_with_solution


def example_maze_generation():
    """Demonstrate maze generation with different algorithms."""
    print("\n" + "="*60)
    print("迷宫生成示例 (Maze Generation Examples)")
    print("="*60)
    
    algorithms = ['DFS', 'Prim', 'Kruskal', 'Eller']
    
    print("\n使用 4 种不同算法生成 15x15 迷宫:")
    
    for algo in algorithms:
        print(f"\n--- {algo} 算法 ---")
        maze = create_maze(15, 15, algo.lower(), seed=42)
        
        # Count paths and walls
        metrics = maze.analyze()
        print(f"路径单元格: {metrics.path_cells}, 墙壁单元格: {metrics.wall_cells}")
        print(f"死胡同: {metrics.dead_ends}, 分支点: {metrics.branching_points}")
        
        # Show maze
        print(maze)
    
    print("\n各算法特点说明:")
    print("  DFS (深度优先): 长走廊，少分支，较难")
    print("  Prim: 更多分支，较短走廊，中等难度")
    print("  Kruskal: 均匀分布，平衡难度")
    print("  Eller: 可无限生成，内存效率高")


def example_maze_solving():
    """Demonstrate maze solving with different algorithms."""
    print("\n" + "="*60)
    print("迷宫求解示例 (Maze Solving Examples)")
    print("="*60)
    
    maze = create_maze(21, 21, 'dfs', seed=100)
    
    print("\n原始迷宫 (21x21):")
    print(maze)
    
    # Compare all solvers
    print("\n比较所有求解算法:")
    results = compare_solvers(maze)
    
    print("\n算法性能对比:")
    print(f"{'算法':<20} {'步数':<10} {'访问单元格':<15}")
    print("-" * 45)
    for name, sol in results.items():
        print(f"{name:<20} {sol.steps:<10} {len(sol.visited_cells):<15}")
    
    # Show BFS solution (shortest)
    print("\nBFS 最短路径解:")
    maze._solution = results['bfs']
    print_maze_with_solution(maze)
    
    # Direction sequence
    print("\n路径方向序列:")
    directions = get_path_directions(results['bfs'])
    print(f"  共 {len(directions)} 步: {' '.join(directions[:20])}...")
    
    print("\n算法特点说明:")
    print("  DFS: 可能找到较长路径，内存效率高")
    print("  BFS: 保证找到最短路径，需要更多内存")
    print("  A*: 高效的最短路径搜索，使用启发式")
    print("  Dead-End Filling: 通过填充死胡同找到唯一路径")


def example_maze_from_string():
    """Demonstrate creating maze from ASCII string."""
    print("\n" + "="*60)
    print("从字符串创建迷宫示例 (Maze from String)")
    print("="*60)
    
    # Simple maze
    simple_maze_str = """
########
#S     #
# #### #
#      #
# #### #
#     E#
########
"""
    
    print("\n输入字符串迷宫:")
    print(simple_maze_str)
    
    maze = maze_from_string(simple_maze_str)
    
    print(f"\n解析结果: {maze.width}x{maze.height}")
    print(f"起点: {maze.start}, 终点: {maze.end}")
    
    solution = maze.solve_bfs()
    if solution:
        print(f"\n求解成功! 最短路径: {solution.steps} 步")
        print("解法:")
        print_maze_with_solution(maze)
    
    # More complex example
    complex_maze_str = """
###############
#S#   #       #
# # # # ##### #
#   # #     # #
### # ##### # #
#   #     #   #
# ##### ##### #
#     #     #E#
###############
"""
    
    print("\n复杂迷宫示例:")
    maze2 = maze_from_string(complex_maze_str)
    solution2 = maze2.solve_bfs()
    if solution2:
        print(f"路径长度: {solution2.steps} 步")
        print_maze_with_solution(maze2)
    else:
        print("迷宫不可解")
        print(maze2)


def example_maze_analysis():
    """Demonstrate maze analysis and metrics."""
    print("\n" + "="*60)
    print("迷宫分析示例 (Maze Analysis)")
    print("="*60)
    
    # Generate different sized mazes
    sizes = [11, 21, 31]
    
    print("\n不同大小迷宫的分析对比:")
    print(f"{'大小':<10} {'路径数':<10} {'死胡同':<10} {'分支点':<10} {'最短路径':<12} {'难度':<10}")
    print("-" * 62)
    
    for size in sizes:
        maze = create_maze(size, size, 'dfs', seed=42)
        metrics = maze.analyze()
        
        print(f"{size}x{size:<6} {metrics.path_cells:<10} {metrics.dead_ends:<10} "
              f"{metrics.branching_points:<10} {metrics.shortest_path:<12} "
              f"{metrics.difficulty_score:.1f}")
    
    print("\n难度计算因素:")
    print("  - 死胡同数量 (增加探索难度)")
    print("  - 分支点数量 (增加决策难度)")
    print("  - 最短路径长度 (增加时间难度)")
    
    # Detailed analysis
    print("\n详细分析 (21x21 DFS迷宫):")
    maze = create_maze(21, 21, 'dfs', seed=42)
    
    dead_ends = maze.find_dead_ends()
    branches = maze.find_branching_points()
    
    print(f"  死胡同位置 ({len(dead_ends)} 个):")
    for i, (x, y) in enumerate(dead_ends[:5]):
        print(f"    [{i+1}] ({x}, {y})")
    if len(dead_ends) > 5:
        print(f"    ... 还有 {len(dead_ends) - 5} 个")
    
    print(f"  分支点位置 ({len(branches)} 个):")
    for i, (x, y) in enumerate(branches[:5]):
        print(f"    [{i+1}] ({x}, {y})")
    if len(branches) > 5:
        print(f"    ... 还有 {len(branches) - 5} 个")


def example_maze_collection():
    """Demonstrate maze collection generation."""
    print("\n" + "="*60)
    print("迷宫集合示例 (Maze Collection)")
    print("="*60)
    
    print("\n生成 5 个随机大小迷宫:")
    mazes = generate_maze_collection(5, min_size=11, max_size=21)
    
    for i, maze in enumerate(mazes):
        metrics = maze.analyze()
        solution = maze.solve_bfs()
        
        print(f"\n迷宫 {i+1} ({maze.width}x{maze.height}):")
        print(f"  路径单元格: {metrics.path_cells}")
        print(f"  死胡同: {metrics.dead_ends}")
        print(f"  最短解: {solution.steps} 步")
        print(f"  难度: {metrics.difficulty_score:.1f}/100")


def example_reproducible_mazes():
    """Demonstrate reproducible maze generation with seeds."""
    print("\n" + "="*60)
    print("可复现迷宫示例 (Reproducible Mazes)")
    print("="*60)
    
    print("\n使用种子生成相同迷宫:")
    
    seeds = [42, 42, 100]
    results = []
    
    for seed in seeds:
        maze = create_maze(15, 15, 'dfs', seed=seed)
        solution = maze.solve_bfs()
        results.append((seed, solution.steps, str(maze)))
    
    print("\n种子对比:")
    for seed, steps, _ in results:
        print(f"  seed={seed} → 最短路径: {steps} 步")
    
    print("\n验证种子 42 的迷宫是否相同:")
    if results[0][1] == results[1][1]:
        print("  ✓ seed=42 的迷宫完全相同")
    else:
        print("  ✗ 迷宫不同 (可能有随机状态污染)")
    
    print("\n应用场景:")
    print("  - 竞赛/游戏中生成固定迷宫")
    print("  - 测试中使用稳定数据")
    print("  - 分享特定迷宫设计")


def example_custom_maze():
    """Demonstrate creating custom maze with specific features."""
    print("\n" + "="*60)
    print("自定义迷宫示例 (Custom Maze)")
    print("="*60)
    
    # Create maze manually
    print("\n手动创建迷宫:")
    maze = Maze(15, 15)
    
    # Set start and end
    maze.start = (1, 1)
    maze.end = (13, 13)
    
    # Create a simple spiral pattern
    for y in range(1, maze.height - 1):
        for x in range(1, maze.width - 1):
            # Simple spiral logic
            if x == 1 or x == maze.width - 2:
                maze.set_cell(x, y, Cell.PATH.value)
            elif y == 1 or y == maze.height - 2:
                maze.set_cell(x, y, Cell.PATH.value)
            elif x == y or x + y == maze.width:
                maze.set_cell(x, y, Cell.PATH.value)
    
    # Connect to end
    maze.set_cell(maze.end[0], maze.end[1], Cell.PATH.value)
    
    print("自定义螺旋迷宫:")
    print(maze)
    
    solution = maze.solve_bfs()
    if solution:
        print(f"\n求解成功: {solution.steps} 步")
    else:
        print("\n迷宫不可解 (需要调整)")
    
    # Use different algorithms on same seed
    print("\n不同算法、相同种子对比:")
    for algo in ['dfs', 'prim', 'kruskal']:
        maze = create_maze(11, 11, algo, seed=42)
        metrics = maze.analyze()
        print(f"  {algo}: 最短路径={metrics.shortest_path}, 死胡同={metrics.dead_ends}")


def example_large_maze():
    """Demonstrate large maze generation."""
    print("\n" + "="*60)
    print("大型迷宫示例 (Large Maze)")
    print("="*60)
    
    size = 41
    
    print(f"\n生成 {size}x{size} 大型迷宫:")
    maze = create_maze(size, size, 'dfs', seed=42)
    
    metrics = maze.analyze()
    print(f"  总单元格: {metrics.total_cells}")
    print(f"  路径单元格: {metrics.path_cells}")
    print(f"  墙壁单元格: {metrics.wall_cells}")
    print(f"  死胡同: {metrics.dead_ends}")
    print(f"  分支点: {metrics.branching_points}")
    
    # Solve
    print(f"\n求解大型迷宫...")
    solution = maze.solve_bfs()
    print(f"  最短路径: {solution.steps} 步")
    
    # Show partial view
    print(f"\n迷宫局部视图 (中心区域):")
    center_x = size // 2 - 5
    center_y = size // 2 - 5
    
    for y in range(center_y, center_y + 10):
        row = ''.join(maze.get_cell(x, y) for x in range(center_x, center_x + 10))
        print(f"  {row}")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("AllToolkit Maze Utilities - 使用示例")
    print("="*60)
    
    example_maze_generation()
    example_maze_solving()
    example_maze_from_string()
    example_maze_analysis()
    example_maze_collection()
    example_reproducible_mazes()
    example_custom_maze()
    example_large_maze()
    
    print("\n" + "="*60)
    print("示例完成!")
    print("="*60)


if __name__ == '__main__':
    main()