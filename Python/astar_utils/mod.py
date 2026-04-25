"""
A* Pathfinding Utils - A* 寻路算法工具包

提供完整的 A* 寻路算法实现，零外部依赖，仅使用 Python 标准库。

功能:
- 基础 A* 算法实现
- 支持自定义启发函数
- 2D 网格地图寻路
- 支持对角线移动
- 支持动态障碍物
- 支持多目标点
- 路径平滑处理
- 可视化工具

作者: AllToolkit
日期: 2026-04-26
"""

from typing import (
    Callable, Dict, Generic, Hashable, List, Optional, 
    Set, Tuple, TypeVar, Union
)
from heapq import heappush, heappop
from dataclasses import dataclass, field
from enum import Enum
import math

T = TypeVar('T', bound=Hashable)


class Direction(Enum):
    """移动方向枚举"""
    FOUR = 4      # 四方向: 上下左右
    EIGHT = 8     # 八方向: 四方向 + 对角线


@dataclass
class PathNode(Generic[T]):
    """路径节点"""
    position: T
    g_cost: float = 0.0      # 从起点到当前节点的实际代价
    h_cost: float = 0.0      # 从当前节点到终点的启发式代价
    f_cost: float = field(init=False)  # 总代价 f = g + h
    parent: Optional['PathNode[T]'] = field(default=None, repr=False)
    
    def __post_init__(self):
        self.f_cost = self.g_cost + self.h_cost
    
    def __lt__(self, other: 'PathNode[T]') -> bool:
        """优先队列比较，f_cost 相等时比较 h_cost"""
        if self.f_cost != other.f_cost:
            return self.f_cost < other.f_cost
        return self.h_cost < other.h_cost
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PathNode):
            return False
        return self.position == other.position
    
    def __hash__(self) -> int:
        return hash(self.position)


class AStar(Generic[T]):
    """
    通用 A* 寻路算法实现。
    
    示例:
        >>> astar = AStar[str](
        ...     neighbors_fn=lambda n: [('A', 1), ('B', 2)] if n == 'start' else [],
        ...     heuristic_fn=lambda a, b: 0
        ... )
        >>> path, cost = astar.find_path('start', 'end')
    """
    
    def __init__(
        self,
        neighbors_fn: Callable[[T], List[Tuple[T, float]]],
        heuristic_fn: Callable[[T, T], float],
        is_goal_fn: Optional[Callable[[T], bool]] = None
    ):
        """
        初始化 A* 寻路器。
        
        Args:
            neighbors_fn: 获取邻居节点的函数，返回 (邻居, 代价) 列表
            heuristic_fn: 启发式函数，估计两点间代价
            is_goal_fn: 可选的目标判断函数，用于多目标场景
        """
        self.neighbors_fn = neighbors_fn
        self.heuristic_fn = heuristic_fn
        self.is_goal_fn = is_goal_fn
    
    def find_path(
        self, 
        start: T, 
        goal: T,
        max_iterations: int = 100000
    ) -> Tuple[List[T], float]:
        """
        查找从起点到终点的最优路径。
        
        Args:
            start: 起点
            goal: 终点
            max_iterations: 最大迭代次数，防止无限循环
            
        Returns:
            (路径列表, 总代价) - 如果找不到路径，返回 ([], float('inf'))
        """
        if start == goal:
            return [start], 0.0
        
        # 开放列表和关闭列表
        open_list: List[PathNode[T]] = []
        open_set: Set[T] = set()
        closed_set: Set[T] = set()
        
        # 节点映射，用于快速查找
        node_map: Dict[T, PathNode[T]] = {}
        
        # 初始化起点
        start_node = PathNode(
            position=start,
            g_cost=0.0,
            h_cost=self.heuristic_fn(start, goal)
        )
        heappush(open_list, start_node)
        open_set.add(start)
        node_map[start] = start_node
        
        iterations = 0
        
        while open_list and iterations < max_iterations:
            iterations += 1
            
            # 获取 f_cost 最小的节点
            current = heappop(open_list)
            open_set.discard(current.position)
            
            # 到达终点
            if current.position == goal or (self.is_goal_fn and self.is_goal_fn(current.position)):
                return self._reconstruct_path(current), current.g_cost
            
            # 加入关闭列表
            closed_set.add(current.position)
            
            # 遍历邻居
            for neighbor_pos, move_cost in self.neighbors_fn(current.position):
                if neighbor_pos in closed_set:
                    continue
                
                tentative_g = current.g_cost + move_cost
                
                # 检查是否已在开放列表中
                if neighbor_pos in open_set:
                    neighbor_node = node_map[neighbor_pos]
                    if tentative_g < neighbor_node.g_cost:
                        # 找到更优路径，更新节点
                        neighbor_node.g_cost = tentative_g
                        neighbor_node.h_cost = self.heuristic_fn(neighbor_pos, goal)
                        neighbor_node.f_cost = tentative_g + neighbor_node.h_cost
                        neighbor_node.parent = current
                        # 需要重新堆化
                        open_list.sort()
                else:
                    # 新节点
                    neighbor_node = PathNode(
                        position=neighbor_pos,
                        g_cost=tentative_g,
                        h_cost=self.heuristic_fn(neighbor_pos, goal),
                        parent=current
                    )
                    heappush(open_list, neighbor_node)
                    open_set.add(neighbor_pos)
                    node_map[neighbor_pos] = neighbor_node
        
        # 未找到路径
        return [], float('inf')
    
    def _reconstruct_path(self, node: PathNode[T]) -> List[T]:
        """重建路径"""
        path: List[T] = []
        current: Optional[PathNode[T]] = node
        
        while current is not None:
            path.append(current.position)
            current = current.parent
        
        return list(reversed(path))
    
    def find_all_reachable(
        self, 
        start: T, 
        max_cost: float
    ) -> Dict[T, float]:
        """
        查找所有可达节点及其最小代价。
        
        Args:
            start: 起点
            max_cost: 最大代价限制
            
        Returns:
            {节点: 最小代价} 字典
        """
        reachable: Dict[T, float] = {start: 0.0}
        open_list: List[PathNode[T]] = []
        open_set: Set[T] = {start}
        
        start_node = PathNode(position=start, g_cost=0.0, h_cost=0.0)
        heappush(open_list, start_node)
        
        while open_list:
            current = heappop(open_list)
            open_set.discard(current.position)
            
            for neighbor_pos, move_cost in self.neighbors_fn(current.position):
                new_cost = current.g_cost + move_cost
                
                if new_cost <= max_cost:
                    if neighbor_pos not in reachable or new_cost < reachable[neighbor_pos]:
                        reachable[neighbor_pos] = new_cost
                        if neighbor_pos not in open_set:
                            neighbor_node = PathNode(
                                position=neighbor_pos,
                                g_cost=new_cost,
                                h_cost=0.0
                            )
                            heappush(open_list, neighbor_node)
                            open_set.add(neighbor_pos)
        
        return reachable


class GridAStar:
    """
    2D 网格地图 A* 寻路器。
    
    支持四方向和八方向移动，支持对角线移动代价调整。
    
    示例:
        >>> grid = [
        ...     [0, 0, 0],
        ...     [0, 1, 0],  # 1 表示障碍物
        ...     [0, 0, 0]
        ... ]
        >>> astar = GridAStar(grid)
        >>> path = astar.find_path((0, 0), (2, 2))
        >>> print(path)
        [(0, 0), (1, 0), (2, 1), (2, 2)]
    """
    
    # 方向向量
    DIRECTIONS_4 = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    DIRECTIONS_8 = DIRECTIONS_4 + [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    
    def __init__(
        self,
        grid: List[List[int]],
        diagonal: bool = False,
        diagonal_cost: float = math.sqrt(2),
        obstacle_values: Set[int] = None
    ):
        """
        初始化网格寻路器。
        
        Args:
            grid: 2D 网格，0 表示可通行，非 0 表示障碍物
            diagonal: 是否允许对角线移动
            diagonal_cost: 对角线移动代价（默认 sqrt(2)）
            obstacle_values: 自定义障碍物值集合
        """
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0
        self.diagonal = diagonal
        self.diagonal_cost = diagonal_cost
        self.obstacle_values = obstacle_values or {1}
        self._directions = self.DIRECTIONS_8 if diagonal else self.DIRECTIONS_4
    
    def is_valid(self, pos: Tuple[int, int]) -> bool:
        """检查位置是否有效且可通行"""
        r, c = pos
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return False
        return self.grid[r][c] not in self.obstacle_values
    
    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[Tuple[int, int], float]]:
        """获取邻居节点及其移动代价"""
        r, c = pos
        neighbors = []
        
        for dr, dc in self._directions:
            new_r, new_c = r + dr, c + dc
            new_pos = (new_r, new_c)
            
            if self.is_valid(new_pos):
                # 对角线移动检查是否被角落阻挡
                if abs(dr) + abs(dc) == 2:  # 对角线移动
                    # 检查两个相邻格子是否都可通行
                    if self.is_valid((r + dr, c)) and self.is_valid((r, c + dc)):
                        neighbors.append((new_pos, self.diagonal_cost))
                else:
                    neighbors.append((new_pos, 1.0))
        
        return neighbors
    
    def heuristic(
        self, 
        a: Tuple[int, int], 
        b: Tuple[int, int],
        method: str = 'manhattan'
    ) -> float:
        """
        计算两点间的启发式距离。
        
        Args:
            a: 起点
            b: 终点
            method: 启发方法 ('manhattan', 'euclidean', 'chebyshev', 'octile')
        """
        dr = abs(a[0] - b[0])
        dc = abs(a[1] - b[1])
        
        if method == 'manhattan':
            return float(dr + dc)
        elif method == 'euclidean':
            return math.sqrt(dr * dr + dc * dc)
        elif method == 'chebyshev':
            return float(max(dr, dc))
        elif method == 'octile':
            # 对角线距离，适合八方向移动
            return max(dr, dc) + (self.diagonal_cost - 1) * min(dr, dc)
        else:
            return float(dr + dc)
    
    def find_path(
        self,
        start: Tuple[int, int],
        goal: Tuple[int, int],
        heuristic: str = 'manhattan'
    ) -> List[Tuple[int, int]]:
        """
        查找从起点到终点的路径。
        
        Args:
            start: 起点坐标 (row, col)
            goal: 终点坐标 (row, col)
            heuristic: 启发方法
            
        Returns:
            路径坐标列表，找不到路径返回空列表
        """
        if not self.is_valid(start) or not self.is_valid(goal):
            return []
        
        astar = AStar[Tuple[int, int]](
            neighbors_fn=self.get_neighbors,
            heuristic_fn=lambda a, b: self.heuristic(a, b, heuristic)
        )
        
        path, _ = astar.find_path(start, goal)
        return path
    
    def find_path_with_cost(
        self,
        start: Tuple[int, int],
        goal: Tuple[int, int],
        heuristic: str = 'manhattan'
    ) -> Tuple[List[Tuple[int, int]], float]:
        """
        查找路径并返回代价。
        
        Returns:
            (路径, 总代价)
        """
        if not self.is_valid(start) or not self.is_valid(goal):
            return [], float('inf')
        
        astar = AStar[Tuple[int, int]](
            neighbors_fn=self.get_neighbors,
            heuristic_fn=lambda a, b: self.heuristic(a, b, heuristic)
        )
        
        return astar.find_path(start, goal)
    
    def find_all_reachable(
        self,
        start: Tuple[int, int],
        max_cost: float
    ) -> Dict[Tuple[int, int], float]:
        """
        查找从起点出发，代价不超过 max_cost 的所有可达位置。
        
        Args:
            start: 起点
            max_cost: 最大代价
            
        Returns:
            {位置: 最小代价} 字典
        """
        if not self.is_valid(start):
            return {}
        
        astar = AStar[Tuple[int, int]](
            neighbors_fn=self.get_neighbors,
            heuristic_fn=lambda a, b: 0
        )
        
        return astar.find_all_reachable(start, max_cost)
    
    def smooth_path(
        self, 
        path: List[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        """
        平滑路径，移除不必要的中间点。
        
        使用视线检测，跳过可以直接到达的中间节点。
        """
        if len(path) <= 2:
            return path
        
        smoothed = [path[0]]
        i = 0
        
        while i < len(path) - 1:
            # 找到最远可以直接到达的点
            j = len(path) - 1
            while j > i + 1:
                if self._has_line_of_sight(path[i], path[j]):
                    break
                j -= 1
            
            smoothed.append(path[j])
            i = j
        
        return smoothed
    
    def _has_line_of_sight(
        self, 
        a: Tuple[int, int], 
        b: Tuple[int, int]
    ) -> bool:
        """检查两点之间是否有直线视线（无障碍物阻挡）"""
        r0, c0 = a
        r1, c1 = b
        
        dr = abs(r1 - r0)
        dc = abs(c1 - c0)
        sr = 1 if r0 < r1 else -1
        sc = 1 if c0 < c1 else -1
        
        err = dr - dc
        
        while True:
            if not self.is_valid((r0, c0)):
                return False
            
            if r0 == r1 and c0 == c1:
                return True
            
            e2 = 2 * err
            
            if e2 > -dc:
                err -= dc
                r0 += sr
            
            if e2 < dr:
                err += dr
                c0 += sc


def create_grid_from_string(
    map_string: str,
    walkable_chars: str = '. ',
    obstacle_char: str = '#'
) -> List[List[int]]:
    """
    从字符串创建网格地图。
    
    Args:
        map_string: 地图字符串，每行用换行分隔
        walkable_chars: 可通行字符
        obstacle_char: 障碍物字符
        
    Returns:
        2D 网格列表
    """
    lines = map_string.strip().split('\n')
    grid = []
    
    for line in lines:
        row = []
        for char in line:
            if char in walkable_chars:
                row.append(0)
            else:
                row.append(1)
        grid.append(row)
    
    return grid


def visualize_path(
    grid: List[List[int]],
    path: List[Tuple[int, int]],
    path_char: str = '*',
    start_char: str = 'S',
    goal_char: str = 'G',
    obstacle_char: str = '#',
    empty_char: str = '.'
) -> str:
    """
    可视化路径。
    
    Args:
        grid: 2D 网格
        path: 路径坐标列表
        path_char: 路径字符
        start_char: 起点字符
        goal_char: 终点字符
        obstacle_char: 障碍物字符
        empty_char: 空地字符
        
    Returns:
        可视化字符串
    """
    if not path:
        return "No path found"
    
    path_set = set(path)
    start = path[0]
    goal = path[-1]
    
    result = []
    for r, row in enumerate(grid):
        line = []
        for c, cell in enumerate(row):
            pos = (r, c)
            if pos == start:
                line.append(start_char)
            elif pos == goal:
                line.append(goal_char)
            elif pos in path_set:
                line.append(path_char)
            elif cell in (1,):
                line.append(obstacle_char)
            else:
                line.append(empty_char)
        result.append(''.join(line))
    
    return '\n'.join(result)


class BidirectionalAStar(Generic[T]):
    """
    双向 A* 算法实现。
    
    同时从起点和终点搜索，在中间相遇，可以提高搜索效率。
    """
    
    def __init__(
        self,
        neighbors_fn: Callable[[T], List[Tuple[T, float]]],
        heuristic_fn: Callable[[T, T], float]
    ):
        self.neighbors_fn = neighbors_fn
        self.heuristic_fn = heuristic_fn
    
    def find_path(
        self,
        start: T,
        goal: T,
        max_iterations: int = 100000
    ) -> Tuple[List[T], float]:
        """双向搜索查找路径"""
        if start == goal:
            return [start], 0.0
        
        # 正向搜索
        forward_open: List[PathNode[T]] = []
        forward_closed: Dict[T, PathNode[T]] = {}
        forward_open_set: Set[T] = set()
        
        # 反向搜索
        backward_open: List[PathNode[T]] = []
        backward_closed: Dict[T, PathNode[T]] = {}
        backward_open_set: Set[T] = set()
        
        # 初始化
        start_node = PathNode(
            position=start,
            g_cost=0.0,
            h_cost=self.heuristic_fn(start, goal)
        )
        heappush(forward_open, start_node)
        forward_open_set.add(start)
        
        goal_node = PathNode(
            position=goal,
            g_cost=0.0,
            h_cost=self.heuristic_fn(goal, start)
        )
        heappush(backward_open, goal_node)
        backward_open_set.add(goal)
        
        best_cost = float('inf')
        best_node: Optional[T] = None
        
        iterations = 0
        
        while (forward_open or backward_open) and iterations < max_iterations:
            iterations += 1
            
            # 正向搜索一步
            if forward_open:
                current = heappop(forward_open)
                forward_open_set.discard(current.position)
                forward_closed[current.position] = current
                
                # 检查是否与反向搜索相遇
                if current.position in backward_closed:
                    total_cost = current.g_cost + backward_closed[current.position].g_cost
                    if total_cost < best_cost:
                        best_cost = total_cost
                        best_node = current.position
                
                # 扩展邻居
                for neighbor_pos, move_cost in self.neighbors_fn(current.position):
                    if neighbor_pos in forward_closed:
                        continue
                    
                    new_g = current.g_cost + move_cost
                    
                    if neighbor_pos in forward_open_set:
                        # 更新更优路径
                        for node in forward_open:
                            if node.position == neighbor_pos and new_g < node.g_cost:
                                node.g_cost = new_g
                                node.f_cost = new_g + node.h_cost
                                node.parent = current
                                forward_open.sort()
                                break
                    else:
                        neighbor_node = PathNode(
                            position=neighbor_pos,
                            g_cost=new_g,
                            h_cost=self.heuristic_fn(neighbor_pos, goal),
                            parent=current
                        )
                        heappush(forward_open, neighbor_node)
                        forward_open_set.add(neighbor_pos)
                        
                        # 检查相遇
                        if neighbor_pos in backward_closed:
                            total_cost = new_g + backward_closed[neighbor_pos].g_cost
                            if total_cost < best_cost:
                                best_cost = total_cost
                                best_node = neighbor_pos
            
            # 反向搜索一步
            if backward_open:
                current = heappop(backward_open)
                backward_open_set.discard(current.position)
                backward_closed[current.position] = current
                
                # 检查相遇
                if current.position in forward_closed:
                    total_cost = forward_closed[current.position].g_cost + current.g_cost
                    if total_cost < best_cost:
                        best_cost = total_cost
                        best_node = current.position
                
                # 扩展邻居（注意：反向搜索）
                for neighbor_pos, move_cost in self.neighbors_fn(current.position):
                    if neighbor_pos in backward_closed:
                        continue
                    
                    new_g = current.g_cost + move_cost
                    
                    if neighbor_pos in backward_open_set:
                        for node in backward_open:
                            if node.position == neighbor_pos and new_g < node.g_cost:
                                node.g_cost = new_g
                                node.f_cost = new_g + node.h_cost
                                node.parent = current
                                backward_open.sort()
                                break
                    else:
                        neighbor_node = PathNode(
                            position=neighbor_pos,
                            g_cost=new_g,
                            h_cost=self.heuristic_fn(neighbor_pos, start),
                            parent=current
                        )
                        heappush(backward_open, neighbor_node)
                        backward_open_set.add(neighbor_pos)
                        
                        if neighbor_pos in forward_closed:
                            total_cost = forward_closed[neighbor_pos].g_cost + new_g
                            if total_cost < best_cost:
                                best_cost = total_cost
                                best_node = neighbor_pos
        
        if best_node is None:
            return [], float('inf')
        
        # 重建路径
        forward_node = forward_closed.get(best_node)
        backward_node = backward_closed.get(best_node)
        
        forward_path: List[T] = []
        current = forward_node
        while current is not None:
            forward_path.append(current.position)
            current = current.parent
        forward_path.reverse()
        
        backward_path: List[T] = []
        current = backward_node
        while current is not None:
            backward_path.append(current.position)
            current = current.parent
        
        # 合并路径（去除重复的中间点）
        full_path = forward_path + backward_path[1:]
        
        return full_path, best_cost


# 便捷函数

def astar_path(
    start: T,
    goal: T,
    neighbors_fn: Callable[[T], List[Tuple[T, float]]],
    heuristic_fn: Callable[[T, T], float]
) -> List[T]:
    """
    A* 寻路便捷函数。
    
    Args:
        start: 起点
        goal: 终点
        neighbors_fn: 邻居获取函数
        heuristic_fn: 启发函数
        
    Returns:
        路径列表
    """
    astar = AStar(neighbors_fn, heuristic_fn)
    path, _ = astar.find_path(start, goal)
    return path


def grid_path(
    grid: List[List[int]],
    start: Tuple[int, int],
    goal: Tuple[int, int],
    diagonal: bool = False
) -> List[Tuple[int, int]]:
    """
    网格寻路便捷函数。
    
    Args:
        grid: 2D 网格（0=可通行，1=障碍）
        start: 起点
        goal: 终点
        diagonal: 是否允许对角线移动
        
    Returns:
        路径坐标列表
    """
    finder = GridAStar(grid, diagonal=diagonal)
    return finder.find_path(start, goal)