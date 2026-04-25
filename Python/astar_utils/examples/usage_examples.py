"""
A* 寻路算法使用示例

演示如何使用 astar_utils 进行路径规划。
"""

from mod import (
    AStar, GridAStar, BidirectionalAStar,
    astar_path, grid_path, 
    create_grid_from_string, visualize_path
)


def example_basic_astar():
    """基础 A* 使用示例"""
    print("=" * 50)
    print("示例 1: 基础 A* 算法")
    print("=" * 50)
    
    # 定义图结构: {节点: [(邻居, 代价), ...]}
    graph = {
        'A': [('B', 1), ('C', 4)],
        'B': [('C', 2), ('D', 5)],
        'C': [('D', 1)],
        'D': []
    }
    
    # 启发函数 (这里使用简单估计)
    def heuristic(a, b):
        # 可以使用预定义的距离估计
        estimates = {'A': 3, 'B': 2, 'C': 1, 'D': 0}
        return abs(estimates[a] - estimates[b])
    
    # 创建 A* 寻路器
    astar = AStar(
        neighbors_fn=lambda n: graph.get(n, []),
        heuristic_fn=heuristic
    )
    
    # 查找路径
    path, cost = astar.find_path('A', 'D')
    
    print(f"图结构: {graph}")
    print(f"从 A 到 D 的路径: {' -> '.join(path)}")
    print(f"总代价: {cost}")
    print()


def example_grid_pathfinding():
    """网格地图寻路示例"""
    print("=" * 50)
    print("示例 2: 网格地图寻路")
    print("=" * 50)
    
    # 创建网格地图 (0 = 可通行, 1 = 障碍物)
    grid = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    
    # 创建寻路器
    finder = GridAStar(grid, diagonal=False)
    
    # 查找路径
    start = (0, 0)
    goal = (4, 4)
    path = finder.find_path(start, goal, heuristic='manhattan')
    
    print("地图:")
    for row in grid:
        print(' '.join('.' if c == 0 else '#' for c in row))
    
    print(f"\n从 {start} 到 {goal} 的路径:")
    print(f"路径点数: {len(path)}")
    print(f"路径: {path}")
    
    # 可视化
    print("\n可视化:")
    visual = visualize_path(grid, path)
    print(visual)
    print()


def example_diagonal_movement():
    """对角线移动示例"""
    print("=" * 50)
    print("示例 3: 对角线移动")
    print("=" * 50)
    
    grid = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    
    # 四方向
    finder4 = GridAStar(grid, diagonal=False)
    path4 = finder4.find_path((2, 2), (0, 0))
    
    # 八方向
    finder8 = GridAStar(grid, diagonal=True)
    path8 = finder8.find_path((2, 2), (0, 0))
    
    print("地图 (中心被包围):")
    for row in grid:
        print(' '.join('.' if c == 0 else '#' for c in row))
    
    print(f"\n四方向路径长度: {len(path4)}")
    print(f"八方向路径长度: {len(path8)}")
    
    # 四方向无法从中心出来
    # 八方向也无法（被完全包围）
    print()


def example_reachable_area():
    """查找可达区域示例"""
    print("=" * 50)
    print("示例 4: 查找可达区域")
    print("=" * 50)
    
    grid = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    
    finder = GridAStar(grid)
    
    # 查找从中心出发，代价 <= 2 的所有可达位置
    reachable = finder.find_all_reachable((2, 2), max_cost=2)
    
    print("地图:")
    for row in grid:
        print(' '.join('.' if c == 0 else '#' for c in row))
    
    print(f"\n从 (2, 2) 出发，代价 <= 2 的可达位置:")
    for pos, cost in sorted(reachable.items()):
        print(f"  {pos}: 代价 {cost}")
    print()


def example_path_smoothing():
    """路径平滑示例"""
    print("=" * 50)
    print("示例 5: 路径平滑")
    print("=" * 50)
    
    # 大空地
    grid = [[0] * 10 for _ in range(10)]
    finder = GridAStar(grid)
    
    # 原始路径
    path = finder.find_path((0, 0), (9, 9), heuristic='manhattan')
    
    # 平滑路径
    smoothed = finder.smooth_path(path)
    
    print(f"原始路径长度: {len(path)}")
    print(f"平滑后路径长度: {len(smoothed)}")
    print(f"原始路径: {path[:3]}...{path[-3:]}")
    print(f"平滑路径: {smoothed}")
    print()


def example_maze_solving():
    """迷宫求解示例"""
    print("=" * 50)
    print("示例 6: 迷宫求解")
    print("=" * 50)
    
    maze_str = """
    #################
    #S..............#
    #.###.#####.###.#
    #.#...#...#...#.#
    #.#.###.#.###.#.#
    #...#...#.#...#.#
    #####.###.#.###.#
    #.....#...#.....#
    #.#####.#####.#.#
    #.#...........#.#
    #.###########.#.#
    #.............G#
    #################
    """
    
    grid = create_grid_from_string(maze_str)
    finder = GridAStar(grid)
    
    # 找起点 S (1, 1) 和终点 G (11, 14)
    path = finder.find_path((1, 1), (11, 14))
    
    print("迷宫:")
    print(maze_str)
    
    print(f"路径长度: {len(path)}")
    
    # 可视化
    visual = visualize_path(grid, path, start_char='S', goal_char='G')
    print("\n可视化路径:")
    print(visual)
    print()


def example_heuristic_comparison():
    """不同启发函数比较"""
    print("=" * 50)
    print("示例 7: 启发函数比较")
    print("=" * 50)
    
    grid = [[0] * 20 for _ in range(20)]
    finder = GridAStar(grid)
    
    start = (0, 0)
    goal = (19, 19)
    
    heuristics = ['manhattan', 'euclidean', 'chebyshev', 'octile']
    
    print(f"从 {start} 到 {goal}:")
    print(f"网格大小: 20x20")
    
    for h in heuristics:
        path = finder.find_path(start, goal, heuristic=h)
        print(f"  {h}: 路径长度 {len(path)}")
    print()


def example_bidirectional_astar():
    """双向 A* 示例"""
    print("=" * 50)
    print("示例 8: 双向 A* 算法")
    print("=" * 50)
    
    # 创建一个较大的图
    graph = {}
    for i in range(100):
        graph[str(i)] = []
        if i > 0:
            graph[str(i)].append((str(i-1), 1))
        if i < 99:
            graph[str(i)].append((str(i+1), 1))
    
    astar = BidirectionalAStar(
        neighbors_fn=lambda n: graph.get(n, []),
        heuristic_fn=lambda a, b: abs(int(a) - int(b))
    )
    
    path, cost = astar.find_path('0', '99')
    
    print(f"图: 线性链 0-99")
    print(f"路径长度: {len(path)}")
    print(f"总代价: {cost}")
    print(f"路径: {' -> '.join(path[:3])} ... {' -> '.join(path[-3:])}")
    print()


def example_convenience_functions():
    """便捷函数示例"""
    print("=" * 50)
    print("示例 9: 便捷函数")
    print("=" * 50)
    
    # 使用便捷函数快速寻路
    
    # 1. 通用图寻路
    graph = {
        'A': [('B', 1), ('C', 2)],
        'B': [('D', 3)],
        'C': [('D', 1)],
        'D': []
    }
    
    path = astar_path(
        'A', 'D',
        neighbors_fn=lambda n: graph.get(n, []),
        heuristic_fn=lambda a, b: 0
    )
    print(f"图寻路: {' -> '.join(path)}")
    
    # 2. 网格寻路
    grid = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    
    path = grid_path(grid, (0, 0), (2, 2))
    print(f"网格寻路: {path}")
    print()


def example_game_pathfinding():
    """游戏场景寻路示例"""
    print("=" * 50)
    print("示例 10: 游戏场景")
    print("=" * 50)
    
    # 模拟一个简单的游戏地图
    # . = 空地, # = 墙, T = 树, W = 水
    game_map = """
    ....................
    ..####...........##.
    ..#..#..TTT.....#..#.
    ..#..#..T.T.....#W.#.
    ..#..#..TTT.....#W.#.
    ..####...........##.
    ....................
    """
    
    # 创建网格（T 和 W 也视为障碍物）
    lines = game_map.strip().split('\n')
    grid = []
    for line in lines:
        row = []
        for c in line:
            if c in '. ':
                row.append(0)
            else:
                row.append(1)
        grid.append(row)
    
    finder = GridAStar(grid, diagonal=True, diagonal_cost=1.414)
    
    # 玩家位置 (1, 2) -> 目标位置 (3, 17)
    start = (1, 2)
    goal = (3, 17)
    
    path, cost = finder.find_path_with_cost(start, goal, heuristic='octile')
    
    print(f"玩家从 {start} 移动到 {goal}:")
    print(f"路径长度: {len(path)}")
    print(f"移动代价: {cost:.2f}")
    
    # 可视化
    visual = visualize_path(grid, path, path_char='@')
    print("\n可视化:")
    print(visual)
    print()


if __name__ == '__main__':
    example_basic_astar()
    example_grid_pathfinding()
    example_diagonal_movement()
    example_reachable_area()
    example_path_smoothing()
    example_maze_solving()
    example_heuristic_comparison()
    example_bidirectional_astar()
    example_convenience_functions()
    example_game_pathfinding()
    
    print("所有示例运行完成！")