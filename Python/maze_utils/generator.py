"""
Maze Generators - 迷宫生成算法
==============================

实现多种经典的迷宫生成算法：
- DFS（深度优先搜索）
- Prim算法
- Kruskal算法
- 递归分割
- Eller算法
- 二叉树算法
"""

import random
from typing import Optional, List, Tuple, Set
from .maze import Maze, Cell, Direction


def generate_dfs(width: int, height: int, seed: Optional[int] = None) -> Maze:
    """
    使用深度优先搜索（递归回溯）生成迷宫
    
    特点：
    - 生成长廊较多
    - 偏差较大，路径曲折
    - 实现简单，效率高
    
    Args:
        width: 迷宫宽度
        height: 迷宫高度
        seed: 随机种子（用于复现）
        
    Returns:
        生成的迷宫
    """
    if seed is not None:
        random.seed(seed)
    
    maze = Maze(width, height)
    
    # 使用栈实现非递归DFS
    stack = [(0, 0)]
    maze.get_cell(0, 0).visited = True
    
    while stack:
        x, y = stack[-1]
        
        # 获取未访问的邻居
        neighbors = maze.get_unvisited_neighbors(x, y)
        
        if neighbors:
            # 随机选择一个邻居
            direction, (nx, ny) = random.choice(neighbors)
            
            # 移除墙壁
            maze.remove_wall(x, y, nx, ny)
            
            # 标记访问并压栈
            maze.get_cell(nx, ny).visited = True
            stack.append((nx, ny))
        else:
            # 回溯
            stack.pop()
    
    maze.reset_visited()
    return maze


def generate_prim(width: int, height: int, seed: Optional[int] = None) -> Maze:
    """
    使用Prim算法生成迷宫
    
    特点：
    - 生成更均匀的迷宫
    - 路径分支多，较短的死胡同
    - 类似于最小生成树
    
    Args:
        width: 迷宫宽度
        height: 迷宫高度
        seed: 随机种子
        
    Returns:
        生成的迷宫
    """
    if seed is not None:
        random.seed(seed)
    
    maze = Maze(width, height)
    
    # 从起点开始
    start_x, start_y = 0, 0
    maze.get_cell(start_x, start_y).visited = True
    
    # 候选边列表：(当前单元格, 邻居单元格)
    frontier = []
    
    def add_frontier(x: int, y: int) -> None:
        for _, (nx, ny) in maze.get_unvisited_neighbors(x, y):
            frontier.append(((x, y), (nx, ny)))
    
    add_frontier(start_x, start_y)
    
    while frontier:
        # 随机选择一条边
        idx = random.randint(0, len(frontier) - 1)
        (x, y), (nx, ny) = frontier.pop(idx)
        
        if maze.get_cell(nx, ny).visited:
            continue
        
        # 连接单元格
        maze.remove_wall(x, y, nx, ny)
        maze.get_cell(nx, ny).visited = True
        add_frontier(nx, ny)
    
    maze.reset_visited()
    return maze


def generate_kruskal(width: int, height: int, seed: Optional[int] = None) -> Maze:
    """
    使用Kruskal算法生成迷宫
    
    特点：
    - 生成均匀分布的迷宫
    - 没有明显的偏差
    - 基于最小生成树
    
    Args:
        width: 迷宫宽度
        height: 迷宫高度
        seed: 随机种子
        
    Returns:
        生成的迷宫
    """
    if seed is not None:
        random.seed(seed)
    
    maze = Maze(width, height)
    
    # 并查集
    parent = {(x, y): (x, y) for y in range(height) for x in range(width)}
    
    def find(pos: Tuple[int, int]) -> Tuple[int, int]:
        if parent[pos] != pos:
            parent[pos] = find(parent[pos])
        return parent[pos]
    
    def union(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> bool:
        root1, root2 = find(pos1), find(pos2)
        if root1 != root2:
            parent[root1] = root2
            return True
        return False
    
    # 所有边
    edges = []
    for y in range(height):
        for x in range(width):
            for direction, (nx, ny) in maze.get_neighbors(x, y):
                if direction in (Direction.EAST, Direction.SOUTH):
                    edges.append(((x, y), (nx, ny)))
    
    random.shuffle(edges)
    
    for (x, y), (nx, ny) in edges:
        if union((x, y), (nx, ny)):
            maze.remove_wall(x, y, nx, ny)
    
    return maze


def generate_recursive_division(width: int, height: int, 
                                seed: Optional[int] = None) -> Maze:
    """
    使用递归分割算法生成迷宫
    
    特点：
    - 先创建空房间，再添加墙壁
        - 生成长直走廊
    - 视觉上有规律性
    
    Args:
        width: 迷宫宽度
        height: 迷宫高度
        seed: 随机种子
        
    Returns:
        生成的迷宫
    """
    if seed is not None:
        random.seed(seed)
    
    maze = Maze(width, height)
    
    # 先移除所有内部墙壁
    for y in range(height):
        for x in range(width):
            cell = maze.get_cell(x, y)
            cell.walls = set()
    
    def divide(x: int, y: int, w: int, h: int) -> None:
        if w < 2 or h < 2:
            return
        
        # 选择分割方向
        if w > h:
            # 垂直分割
            wall_x = x + random.randint(1, w - 1)
            passage_y = random.randint(y, y + h - 1)
            
            for py in range(y, y + h):
                if py != passage_y and wall_x < width:
                    maze.add_wall(wall_x - 1, py, wall_x, py)
            
            divide(x, y, wall_x - x, h)
            divide(wall_x, y, x + w - wall_x, h)
        else:
            # 水平分割
            wall_y = y + random.randint(1, h - 1)
            passage_x = random.randint(x, x + w - 1)
            
            for px in range(x, x + w):
                if px != passage_x and wall_y < height:
                    maze.add_wall(px, wall_y - 1, px, wall_y)
            
            divide(x, y, w, wall_y - y)
            divide(x, wall_y, w, y + h - wall_y)
    
    divide(0, 0, width, height)
    return maze


def generate_ellers(width: int, height: int, seed: Optional[int] = None) -> Maze:
    """
    使用Eller算法生成迷宫
    
    特点：
    - 逐行生成，内存效率高
    - 可以生成无限大的迷宫
    - 产生适中的纹理
    
    Args:
        width: 迷宫宽度
        height: 迷宫高度
        seed: 随机种子
        
    Returns:
        生成的迷宫
    """
    if seed is not None:
        random.seed(seed)
    
    maze = Maze(width, height)
    
    # 每行的集合标记
    sets = [i for i in range(width)]
    next_set = width
    
    for y in range(height):
        # 水平连接：随机合并相邻不同集合的单元格
        for x in range(width - 1):
            if sets[x] != sets[x + 1] and (y == height - 1 or random.random() < 0.5):
                # 合并集合
                old_set = sets[x + 1]
                new_set = sets[x]
                for i in range(width):
                    if sets[i] == old_set:
                        sets[i] = new_set
                # 移除墙壁
                maze.remove_wall(x, y, x + 1, y)
        
        if y == height - 1:
            continue
        
        # 垂直连接：每个集合至少向下连接一次
        verticals = {}
        for x in range(width):
            s = sets[x]
            if s not in verticals:
                verticals[s] = []
            verticals[s].append(x)
        
        new_sets = [-1] * width
        
        for s, columns in verticals.items():
            # 随机选择要向下连接的单元格
            num_down = random.randint(1, len(columns))
            down_cols = random.sample(columns, num_down)
            
            for col in down_cols:
                maze.remove_wall(col, y, col, y + 1)
                new_sets[col] = s
        
        # 分配新集合给未连接的单元格
        for x in range(width):
            if new_sets[x] == -1:
                new_sets[x] = next_set
                next_set += 1
        
        sets = new_sets
    
    return maze


def generate_binary_tree(width: int, height: int, 
                         seed: Optional[int] = None,
                         bias: str = 'northeast') -> Maze:
    """
    使用二叉树算法生成迷宫
    
    特点：
    - 最简单的迷宫算法之一
    - 有明显的对角线偏差
    - 非常快速
    
    Args:
        width: 迷宫宽度
        height: 迷宫高度
        seed: 随机种子
        bias: 偏差方向 ('northeast', 'northwest', 'southeast', 'southwest')
        
    Returns:
        生成的迷宫
    """
    if seed is not None:
        random.seed(seed)
    
    maze = Maze(width, height)
    
    # 根据偏差方向确定主方向和次方向
    biases = {
        'northeast': (Direction.NORTH, Direction.EAST),
        'northwest': (Direction.NORTH, Direction.WEST),
        'southeast': (Direction.SOUTH, Direction.EAST),
        'southwest': (Direction.SOUTH, Direction.WEST),
    }
    
    primary, secondary = biases.get(bias, biases['northeast'])
    
    for y in range(height):
        for x in range(width):
            # 获取可用的方向
            options = []
            
            if primary == Direction.NORTH and y > 0:
                options.append((x, y, x, y - 1))
            elif primary == Direction.SOUTH and y < height - 1:
                options.append((x, y, x, y + 1))
            elif primary == Direction.EAST and x < width - 1:
                options.append((x, y, x + 1, y))
            elif primary == Direction.WEST and x > 0:
                options.append((x, y, x - 1, y))
            
            if secondary == Direction.NORTH and y > 0:
                options.append((x, y, x, y - 1))
            elif secondary == Direction.SOUTH and y < height - 1:
                options.append((x, y, x, y + 1))
            elif secondary == Direction.EAST and x < width - 1:
                options.append((x, y, x + 1, y))
            elif secondary == Direction.WEST and x > 0:
                options.append((x, y, x - 1, y))
            
            if options:
                # 随机选择一个方向
                x1, y1, x2, y2 = random.choice(options)
                maze.remove_wall(x1, y1, x2, y2)
    
    return maze


def generate_sidewinder(width: int, height: int, seed: Optional[int] = None) -> Maze:
    """
    使用Sidewinder算法生成迷宫
    
    特点：
    - 简单高效
    - 有水平偏差
    - 顶部行完全水平
    
    Args:
        width: 迷宫宽度
        height: 迷宫高度
        seed: 随机种子
        
    Returns:
        生成的迷宫
    """
    if seed is not None:
        random.seed(seed)
    
    maze = Maze(width, height)
    
    # 顶行：全部向东连通
    for x in range(width - 1):
        maze.remove_wall(x, 0, x + 1, 0)
    
    # 其余行
    for y in range(1, height):
        run_start = 0
        
        for x in range(width):
            # 向东延伸或向北
            if x == width - 1 or random.random() < 0.5:
                # 从当前run中随机选择一个单元格向北连接
                north_x = random.randint(run_start, x)
                maze.remove_wall(north_x, y, north_x, y - 1)
                run_start = x + 1
            else:
                # 向东延伸
                maze.remove_wall(x, y, x + 1, y)
    
    return maze