"""
Maze Core - 迷宫核心数据结构
============================

定义迷宫的基本数据结构，包括单元格、方向、迷宫类等。
"""

from enum import Enum
from typing import Optional, List, Tuple, Set
from dataclasses import dataclass, field
import copy


class Direction(Enum):
    """方向枚举"""
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)
    
    @property
    def opposite(self) -> 'Direction':
        """获取相反方向"""
        opposites = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST: Direction.WEST,
            Direction.WEST: Direction.EAST,
        }
        return opposites[self]
    
    @property
    def dx(self) -> int:
        """X方向偏移"""
        return self.value[0]
    
    @property
    def dy(self) -> int:
        """Y方向偏移"""
        return self.value[1]


@dataclass
class Cell:
    """
    迷宫单元格
    
    使用墙壁集合表示单元格的状态。
    每个单元格可以有多面墙（北、南、东、西）。
    """
    x: int
    y: int
    walls: Set[Direction] = field(default_factory=lambda: set(Direction))
    visited: bool = False
    
    def remove_wall(self, direction: Direction) -> None:
        """移除指定方向的墙"""
        self.walls.discard(direction)
    
    def add_wall(self, direction: Direction) -> None:
        """添加指定方向的墙"""
        self.walls.add(direction)
    
    def has_wall(self, direction: Direction) -> bool:
        """检查是否有指定方向的墙"""
        return direction in self.walls
    
    def can_move(self, direction: Direction) -> bool:
        """检查是否可以向指定方向移动（没有墙）"""
        return not self.has_wall(direction)
    
    def reset(self) -> None:
        """重置单元格状态"""
        self.walls = set(Direction)
        self.visited = False


class Maze:
    """
    迷宫类
    
    提供迷宫的基本操作，包括创建、访问单元格、验证等。
    """
    
    def __init__(self, width: int, height: int):
        """
        初始化迷宫
        
        Args:
            width: 迷宫宽度（单元格数量）
            height: 迷宫高度（单元格数量）
        """
        if width < 2 or height < 2:
            raise ValueError("Maze dimensions must be at least 2x2")
        
        self.width = width
        self.height = height
        self._cells: List[List[Cell]] = [
            [Cell(x, y) for x in range(width)]
            for y in range(height)
        ]
        self._start: Optional[Tuple[int, int]] = None
        self._end: Optional[Tuple[int, int]] = None
    
    @property
    def start(self) -> Tuple[int, int]:
        """起点坐标"""
        if self._start is None:
            return (0, 0)
        return self._start
    
    @start.setter
    def start(self, pos: Tuple[int, int]) -> None:
        """设置起点"""
        if not self.is_valid_pos(pos[0], pos[1]):
            raise ValueError(f"Invalid start position: {pos}")
        self._start = pos
    
    @property
    def end(self) -> Tuple[int, int]:
        """终点坐标"""
        if self._end is None:
            return (self.width - 1, self.height - 1)
        return self._end
    
    @end.setter
    def end(self, pos: Tuple[int, int]) -> None:
        """设置终点"""
        if not self.is_valid_pos(pos[0], pos[1]):
            raise ValueError(f"Invalid end position: {pos}")
        self._end = pos
    
    def is_valid_pos(self, x: int, y: int) -> bool:
        """检查坐标是否有效"""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def get_cell(self, x: int, y: int) -> Cell:
        """获取指定位置的单元格"""
        if not self.is_valid_pos(x, y):
            raise IndexError(f"Position ({x}, {y}) out of bounds")
        return self._cells[y][x]
    
    def set_cell(self, x: int, y: int, cell: Cell) -> None:
        """设置指定位置的单元格"""
        if not self.is_valid_pos(x, y):
            raise IndexError(f"Position ({x}, {y}) out of bounds")
        self._cells[y][x] = cell
    
    def get_neighbor(self, x: int, y: int, direction: Direction) -> Optional[Tuple[int, int]]:
        """
        获取指定方向的邻居坐标
        
        Args:
            x: 当前X坐标
            y: 当前Y坐标
            direction: 方向
            
        Returns:
            邻居坐标，如果越界则返回None
        """
        nx, ny = x + direction.dx, y + direction.dy
        if self.is_valid_pos(nx, ny):
            return (nx, ny)
        return None
    
    def get_neighbors(self, x: int, y: int) -> List[Tuple[Direction, Tuple[int, int]]]:
        """
        获取所有有效邻居
        
        Returns:
            列表，每个元素为(方向, 坐标)元组
        """
        neighbors = []
        for direction in Direction:
            neighbor = self.get_neighbor(x, y, direction)
            if neighbor:
                neighbors.append((direction, neighbor))
        return neighbors
    
    def get_unvisited_neighbors(self, x: int, y: int) -> List[Tuple[Direction, Tuple[int, int]]]:
        """获取所有未访问的邻居"""
        return [
            (d, pos) for d, pos in self.get_neighbors(x, y)
            if not self.get_cell(pos[0], pos[1]).visited
        ]
    
    def get_passages(self, x: int, y: int) -> List[Tuple[Direction, Tuple[int, int]]]:
        """获取所有可通行的邻居（没有墙阻挡）"""
        cell = self.get_cell(x, y)
        passages = []
        for direction, pos in self.get_neighbors(x, y):
            if cell.can_move(direction):
                passages.append((direction, pos))
        return passages
    
    def remove_wall(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """
        移除两个相邻单元格之间的墙
        
        Args:
            x1, y1: 第一个单元格坐标
            x2, y2: 第二个单元格坐标
        """
        cell1 = self.get_cell(x1, y1)
        cell2 = self.get_cell(x2, y2)
        
        # 确定方向
        dx, dy = x2 - x1, y2 - y1
        
        if abs(dx) + abs(dy) != 1:
            raise ValueError("Cells must be adjacent")
        
        if dx == 1:
            cell1.remove_wall(Direction.EAST)
            cell2.remove_wall(Direction.WEST)
        elif dx == -1:
            cell1.remove_wall(Direction.WEST)
            cell2.remove_wall(Direction.EAST)
        elif dy == 1:
            cell1.remove_wall(Direction.SOUTH)
            cell2.remove_wall(Direction.NORTH)
        elif dy == -1:
            cell1.remove_wall(Direction.NORTH)
            cell2.remove_wall(Direction.SOUTH)
    
    def add_wall(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """在两个相邻单元格之间添加墙"""
        cell1 = self.get_cell(x1, y1)
        cell2 = self.get_cell(x2, y2)
        
        dx, dy = x2 - x1, y2 - y1
        
        if abs(dx) + abs(dy) != 1:
            raise ValueError("Cells must be adjacent")
        
        if dx == 1:
            cell1.add_wall(Direction.EAST)
            cell2.add_wall(Direction.WEST)
        elif dx == -1:
            cell1.add_wall(Direction.WEST)
            cell2.add_wall(Direction.EAST)
        elif dy == 1:
            cell1.add_wall(Direction.SOUTH)
            cell2.add_wall(Direction.NORTH)
        elif dy == -1:
            cell1.add_wall(Direction.NORTH)
            cell2.add_wall(Direction.SOUTH)
    
    def reset_visited(self) -> None:
        """重置所有单元格的访问状态"""
        for row in self._cells:
            for cell in row:
                cell.visited = False
    
    def reset(self) -> None:
        """完全重置迷宫（所有墙恢复）"""
        for row in self._cells:
            for cell in row:
                cell.reset()
        self._start = None
        self._end = None
    
    def is_perfect(self) -> bool:
        """
        检查是否为完美迷宫（每两个单元格之间恰好有一条路径）
        
        使用并查集验证所有单元格是否连通
        """
        # 简单的连通性检查
        visited = set()
        stack = [(0, 0)]
        
        while stack:
            x, y = stack.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            
            for direction, (nx, ny) in self.get_passages(x, y):
                if (nx, ny) not in visited:
                    stack.append((nx, ny))
        
        return len(visited) == self.width * self.height
    
    def copy(self) -> 'Maze':
        """创建迷宫的深拷贝"""
        new_maze = Maze(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                original = self.get_cell(x, y)
                new_cell = Cell(x, y, set(original.walls), original.visited)
                new_maze.set_cell(x, y, new_cell)
        new_maze._start = self._start
        new_maze._end = self._end
        return new_maze
    
    def __repr__(self) -> str:
        return f"Maze({self.width}x{self.height})"
    
    def __str__(self) -> str:
        """返回ASCII表示"""
        from .renderer import render_ascii
        return render_ascii(self)
    
    def __iter__(self):
        """迭代所有单元格"""
        for row in self._cells:
            for cell in row:
                yield cell
    
    def __getitem__(self, key: Tuple[int, int]) -> Cell:
        """通过坐标访问单元格：maze[x, y]"""
        return self.get_cell(key[0], key[1])
    
    def __len__(self) -> int:
        """返回单元格总数"""
        return self.width * self.height