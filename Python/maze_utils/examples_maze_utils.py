"""
Maze Utils Examples - 迷宫工具使用示例
=====================================

演示如何使用 maze_utils 模块的各种功能。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from maze_utils import (
    Maze, Direction,
    generate_dfs, generate_prim, generate_kruskal,
    generate_recursive_division, generate_ellers, generate_binary_tree,
    solve_bfs, solve_dfs, solve_astar, solve_wall_follower,
    render_ascii, render_unicode, render_path,
    to_json, from_json, to_binary, from_binary,
)


def example_basic_generation():
    """基础迷宫生成示例"""
    print("=" * 60)
    print("基础迷宫生成")
    print("=" * 60)
    
    # 使用DFS生成迷宫
    maze = generate_dfs(15, 10, seed=42)
    
    print(f"\n迷宫尺寸: {maze.width}x{maze.height}")
    print(f"单元格总数: {len(maze)}")
    
    print("\nASCII渲染:")
    print(render_ascii(maze))
    
    print("\nUnicode渲染:")
    print(render_unicode(maze))


def example_all_generators():
    """所有生成算法对比示例"""
    print("\n" + "=" * 60)
    print("不同生成算法对比")
    print("=" * 60)
    
    generators = [
        ("DFS (深度优先)", generate_dfs),
        ("Prim", generate_prim),
        ("Kruskal", generate_kruskal),
        ("递归分割", generate_recursive_division),
        ("Eller", generate_ellers),
        ("二叉树 (东北)", lambda w, h: generate_binary_tree(w, h, bias='northeast')),
    ]
    
    for name, gen_func in generators:
        maze = gen_func(10, 10, seed=42)
        path = solve_bfs(maze)
        
        print(f"\n{name}:")
        print(f"  路径长度: {len(path) - 1} 步")
        print(render_ascii(maze, path))


def example_solving_methods():
    """不同求解方法示例"""
    print("\n" + "=" * 60)
    print("不同求解方法对比")
    print("=" * 60)
    
    maze = generate_prim(15, 15, seed=123)
    
    solvers = [
        ("BFS (最短路径)", solve_bfs),
        ("DFS", solve_dfs),
        ("A*", solve_astar),
        ("墙跟随 (右)", lambda m: solve_wall_follower(m, hand='right')),
    ]
    
    for name, solver in solvers:
        path = solver(maze)
        if path:
            print(f"\n{name}:")
            print(f"  路径长度: {len(path) - 1} 步")
            # 显示路径前10步和最后5步
            print(f"  路径开始: {path[:10]}")
            print(f"  路径结束: {path[-5:]}")


def example_large_maze():
    """大迷宫示例"""
    print("\n" + "=" * 60)
    print("大迷宫生成与求解")
    print("=" * 60)
    
    # 生成30x30的迷宫
    maze = generate_kruskal(30, 30, seed=42)
    
    print(f"\n迷宫尺寸: {maze.width}x{maze.height}")
    print(f"是完美迷宫吗: {maze.is_perfect()}")
    
    # 使用不同算法求解
    import time
    
    start = time.time()
    bfs_path = solve_bfs(maze)
    bfs_time = time.time() - start
    
    start = time.time()
    astar_path = solve_astar(maze)
    astar_time = time.time() - start
    
    print(f"\nBFS求解时间: {bfs_time:.4f}s, 路径长度: {len(bfs_path) - 1}")
    print(f"A*求解时间: {astar_time:.4f}s, 路径长度: {len(astar_path) - 1}")
    
    # 显示迷宫的一部分
    print("\n迷宫中心区域 (展示10x10):")
    center_x, center_y = 10, 10
    # 创建一个小的展示区域
    small_maze = generate_dfs(10, 10, seed=42)
    small_path = solve_bfs(small_maze)
    print(render_unicode(small_maze, small_path))


def example_serialization():
    """序列化示例"""
    print("\n" + "=" * 60)
    print("迷宫序列化")
    print("=" * 60)
    
    maze = generate_dfs(8, 8, seed=42)
    
    # JSON序列化
    json_str = to_json(maze)
    print(f"\nJSON序列化 (前500字符):")
    print(json_str[:500] + "...")
    
    # 反序列化
    restored = from_json(json_str)
    print(f"\n从JSON恢复的迷宫是否完整: {restored.is_perfect()}")
    
    # 二进制序列化
    binary_data = to_binary(maze)
    print(f"\n二进制数据大小: {len(binary_data)} 字节")
    
    # 反序列化
    restored_binary = from_binary(binary_data)
    print(f"从二进制恢复的迷宫是否完整: {restored_binary.is_perfect()}")


def example_path_visualization():
    """路径可视化示例"""
    print("\n" + "=" * 60)
    print("路径可视化")
    print("=" * 60)
    
    maze = generate_prim(15, 10, seed=42)
    path = solve_bfs(maze)
    
    print("\n带路径标记的迷宫:")
    print(render_path(maze, path))
    
    # 计算路径统计
    print(f"\n路径统计:")
    print(f"  起点: {path[0]}")
    print(f"  终点: {path[-1]}")
    print(f"  总步数: {len(path) - 1}")
    
    # 获取方向序列
    from maze_utils.solver import get_path_directions, get_path_length
    directions = get_path_directions(path)
    
    print(f"  方向序列: {len(directions)} 步")
    print(f"  北: {sum(1 for d in directions if d == Direction.NORTH)}")
    print(f"  南: {sum(1 for d in directions if d == Direction.SOUTH)}")
    print(f"  东: {sum(1 for d in directions if d == Direction.EAST)}")
    print(f"  西: {sum(1 for d in directions if d == Direction.WEST)}")


def example_custom_maze():
    """自定义迷宫示例"""
    print("\n" + "=" * 60)
    print("创建自定义迷宫")
    print("=" * 60)
    
    # 创建一个空迷宫
    maze = Maze(5, 5)
    
    # 手动移除一些墙壁创建路径
    # 这是一个简单的十字形路径
    maze.remove_wall(0, 0, 1, 0)  # 第一行水平连通
    maze.remove_wall(1, 0, 1, 1)  # 向下
    maze.remove_wall(1, 1, 2, 1)  # 向右
    maze.remove_wall(2, 1, 2, 2)  # 向下
    maze.remove_wall(2, 2, 2, 3)  # 向下
    maze.remove_wall(2, 2, 3, 2)  # 向右
    maze.remove_wall(3, 2, 4, 2)  # 向右出口
    
    maze.start = (0, 0)
    maze.end = (4, 2)
    
    print("\n自定义迷宫:")
    print(render_ascii(maze, show_start_end=True))
    
    # 尝试求解
    path = solve_bfs(maze)
    if path:
        print("\n求解路径:")
        print(f"  路径: {path}")
        print(render_ascii(maze, path))


def example_unicode_styles():
    """Unicode样式对比示例"""
    print("\n" + "=" * 60)
    print("Unicode渲染样式对比")
    print("=" * 60)
    
    maze = generate_dfs(8, 8, seed=42)
    
    for style in ['box', 'round', 'double']:
        print(f"\n{style} 样式:")
        print(render_unicode(maze, style=style))


def main():
    """运行所有示例"""
    example_basic_generation()
    example_all_generators()
    example_solving_methods()
    example_large_maze()
    example_serialization()
    example_path_visualization()
    example_custom_maze()
    example_unicode_styles()
    
    print("\n" + "=" * 60)
    print("示例完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()