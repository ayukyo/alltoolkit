"""
Maze Solvers - 迷宫求解算法
==========================

实现多种迷宫求解算法：
- BFS（广度优先搜索）- 最短路径
- DFS（深度优先搜索）- 快速找到路径
- A*算法 - 启发式最短路径
- 墙跟随算法 - 简单有效
- 死胡同填充算法 - 系统性消除
"""

import random
import heapq
from typing import Optional, List, Tuple, Set, Dict, Callable
from .maze import Maze, Direction


# 类型别名
Position = Tuple[int, int]
Path = List[Position]


def solve_bfs(maze: Maze, start: Optional[Position] = None, 
              end: Optional[Position] = None) -> Optional[Path]:
    """
    使用BFS（广度优先搜索）求解迷宫
    
    特点：
    - 保证找到最短路径
    - 探索所有等距离节点
    - 时间复杂度: O(n)
    
    Args:
        maze: 迷宫对象
        start: 起点坐标，默认(0, 0)
        end: 终点坐标，默认(width-1, height-1)
        
    Returns:
        路径坐标列表，如果无解返回None
    """
    start = start if start else maze.start
    end = end if end else maze.end
    
    if start == end:
        return [start]
    
    # BFS队列
    queue = [start]
    visited = {start}
    parent: Dict[Position, Position] = {}
    
    while queue:
        current = queue.pop(0)
        
        if current == end:
            # 重建路径
            path = []
            pos = end
            while pos is not None:
                path.append(pos)
                pos = parent.get(pos)
            return list(reversed(path))
        
        x, y = current
        for direction, (nx, ny) in maze.get_passages(x, y):
            neighbor = (nx, ny)
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    
    return None


def solve_dfs(maze: Maze, start: Optional[Position] = None,
              end: Optional[Position] = None) -> Optional[Path]:
    """
    使用DFS（深度优先搜索）求解迷宫
    
    特点：
    - 快速找到一条路径（不一定最短）
    - 使用栈实现非递归版本
    - 内存效率高
    
    Args:
        maze: 迷宫对象
        start: 起点坐标
        end: 终点坐标
        
    Returns:
        路径坐标列表，如果无解返回None
    """
    start = start if start else maze.start
    end = end if end else maze.end
    
    if start == end:
        return [start]
    
    stack = [(start, [start])]
    visited = {start}
    
    while stack:
        current, path = stack.pop()
        
        if current == end:
            return path
        
        x, y = current
        neighbors = list(maze.get_passages(x, y))
        random.shuffle(neighbors)  # 增加随机性
        
        for direction, (nx, ny) in neighbors:
            neighbor = (nx, ny)
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor]))
    
    return None


def solve_astar(maze: Maze, start: Optional[Position] = None,
                end: Optional[Position] = None,
                heuristic: Optional[Callable[[Position, Position], float]] = None) -> Optional[Path]:
    """
    使用A*算法求解迷宫
    
    特点：
    - 保证找到最短路径
    - 使用启发式函数加速搜索
    - 比BFS更高效（在有良好启发函数时）
    
    Args:
        maze: 迷宫对象
        start: 起点坐标
        end: 终点坐标
        heuristic: 启发式函数，默认使用曼哈顿距离
        
    Returns:
        路径坐标列表，如果无解返回None
    """
    start = start if start else maze.start
    end = end if end else maze.end
    
    if start == end:
        return [start]
    
    # 默认启发式：曼哈顿距离
    if heuristic is None:
        def heuristic(a: Position, b: Position) -> float:
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    # 优先队列: (f_score, counter, position)
    counter = 0
    open_set = [(heuristic(start, end), counter, start)]
    
    g_score: Dict[Position, float] = {start: 0}
    f_score: Dict[Position, float] = {start: heuristic(start, end)}
    parent: Dict[Position, Position] = {}
    
    visited = set()
    
    while open_set:
        _, _, current = heapq.heappop(open_set)
        
        if current in visited:
            continue
        visited.add(current)
        
        if current == end:
            # 重建路径
            path = []
            pos = end
            while pos is not None:
                path.append(pos)
                pos = parent.get(pos)
            return list(reversed(path))
        
        x, y = current
        for direction, (nx, ny) in maze.get_passages(x, y):
            neighbor = (nx, ny)
            
            if neighbor in visited:
                continue
            
            tentative_g = g_score[current] + 1
            
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                parent[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, end)
                counter += 1
                heapq.heappush(open_set, (f_score[neighbor], counter, neighbor))
    
    return None


def solve_wall_follower(maze: Maze, start: Optional[Position] = None,
                        end: Optional[Position] = None,
                        hand: str = 'right') -> Optional[Path]:
    """
    使用墙跟随算法求解迷宫
    
    特点：
    - 简单直观
    - 始终保持一只手贴着墙
    - 适用于完美迷宫（无环）
    - 不保证最短路径
    
    Args:
        maze: 迷宫对象
        start: 起点坐标
        end: 终点坐标
        hand: 'right' 或 'left'，表示使用哪只手
        
    Returns:
        路径坐标列表，如果无解返回None
    """
    start = start if start else maze.start
    end = end if end else maze.end
    
    if start == end:
        return [start]
    
    # 方向顺序：北、东、南、西
    directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
    
    # 获取转向顺序
    if hand == 'right':
        turn_offset = 1  # 右转
    else:
        turn_offset = -1  # 左转
    
    path = [start]
    current = start
    
    # 初始面向东方
    facing_idx = 1  # Direction.EAST
    
    visited_states: Set[Tuple[Position, int]] = set()
    max_steps = len(maze) * 4  # 防止无限循环
    steps = 0
    
    while current != end and steps < max_steps:
        steps += 1
        state = (current, facing_idx)
        
        if state in visited_states:
            # 检测到循环，迷宫可能有环
            break
        visited_states.add(state)
        
        # 尝试转向并移动
        moved = False
        
        # 从当前方向的"手边"开始尝试
        for i in range(4):
            check_idx = (facing_idx + i * turn_offset) % 4
            direction = directions[check_idx]
            
            x, y = current
            if maze.get_cell(x, y).can_move(direction):
                # 可以向这个方向移动
                nx, ny = x + direction.dx, y + direction.dy
                if maze.is_valid_pos(nx, ny):
                    current = (nx, ny)
                    facing_idx = check_idx
                    path.append(current)
                    moved = True
                    break
        
        if not moved:
            # 死胡同，返回
            break
    
    if current == end:
        return path
    return None


def solve_dead_end_filling(maze: Maze, start: Optional[Position] = None,
                           end: Optional[Position] = None) -> Optional[Path]:
    """
    使用死胡同填充算法求解迷宫
    
    特点：
    - 通过标记并填充死胡同来解决问题
    - 最后剩下的就是正确路径
    - 视觉上很直观
    - 适用于完美迷宫
    
    Args:
        maze: 迷宫对象
        start: 起点坐标
        end: 终点坐标
        
    Returns:
        路径坐标列表，如果无解返回None
    """
    start = start if start else maze.start
    end = end if end else maze.end
    
    # 创建迷宫副本
    maze_copy = maze.copy()
    
    # 标记死胡同
    dead_ends: Set[Position] = set()
    
    def is_dead_end(x: int, y: int) -> bool:
        if (x, y) == start or (x, y) == end:
            return False
        cell = maze_copy.get_cell(x, y)
        # 统计可通行方向
        passages = sum(1 for d in Direction if cell.can_move(d))
        return passages == 1
    
    def fill_dead_ends():
        changed = True
        while changed:
            changed = False
            for y in range(maze_copy.height):
                for x in range(maze_copy.width):
                    if (x, y) in dead_ends:
                        continue
                    if is_dead_end(x, y):
                        dead_ends.add((x, y))
                        # 封闭这个死胡同
                        cell = maze_copy.get_cell(x, y)
                        for d in Direction:
                            if cell.can_move(d):
                                nx, ny = x + d.dx, y + d.dy
                                if maze_copy.is_valid_pos(nx, ny):
                                    maze_copy.add_wall(x, y, nx, ny)
                        changed = True
                        break
                if changed:
                    break
    
    fill_dead_ends()
    
    # 剩余的单元格形成路径
    # 使用BFS在剩余空间中找到路径
    remaining_path = solve_bfs(maze_copy, start, end)
    
    return remaining_path


def solve_all_paths(maze: Maze, start: Optional[Position] = None,
                    end: Optional[Position] = None,
                    max_paths: int = 100) -> List[Path]:
    """
    找到所有可能的路径（仅在迷宫有环时有用）
    
    警告：对于大迷宫或有很多环的迷宫，可能会非常慢
    
    Args:
        maze: 迷宫对象
        start: 起点坐标
        end: 终点坐标
        max_paths: 最大路径数量限制
        
    Returns:
        路径列表
    """
    start = start if start else maze.start
    end = end if end else maze.end
    
    paths = []
    stack = [(start, [start])]
    
    while stack and len(paths) < max_paths:
        current, path = stack.pop()
        
        if current == end:
            paths.append(path)
            continue
        
        x, y = current
        for direction, (nx, ny) in maze.get_passages(x, y):
            neighbor = (nx, ny)
            if neighbor not in path:  # 避免循环
                stack.append((neighbor, path + [neighbor]))
    
    return paths


def get_path_length(path: Optional[Path]) -> int:
    """获取路径长度"""
    if path is None:
        return -1
    return len(path) - 1  # 步数 = 节点数 - 1


def get_path_directions(path: Path) -> List[Direction]:
    """
    将路径坐标转换为方向序列
    
    Args:
        path: 路径坐标列表
        
    Returns:
        方向列表
    """
    directions = []
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        dx, dy = x2 - x1, y2 - y1
        
        if dx == 1:
            directions.append(Direction.EAST)
        elif dx == -1:
            directions.append(Direction.WEST)
        elif dy == 1:
            directions.append(Direction.SOUTH)
        elif dy == -1:
            directions.append(Direction.NORTH)
    
    return directions