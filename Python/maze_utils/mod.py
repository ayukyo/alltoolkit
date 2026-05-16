"""
迷宫工具模块 (Maze Utilities)

提供迷宫生成和求解的完整工具集，零外部依赖。

功能:
- 迷宫生成: DFS递归回溯、Prim随机、Kruskal、递归分割
- 迷宫求解: BFS最短路径、DFS路径查找、A*算法
- 迷宫可视化: ASCII艺术、字符串表示
- 迷宫验证: 检查路径有效性、迷宫完整性

作者: AllToolkit 自动生成
日期: 2026-05-16
"""

from typing import List, Tuple, Optional, Set, Generator
from collections import deque
import random


class Maze:
    """
    迷宫类，支持生成和求解操作。
    
    使用二维网格表示迷宫:
    - '#' 表示墙壁
    - ' ' 表示通道
    - 'S' 表示起点
    - 'E' 表示终点
    - '.' 表示路径
    """
    
    WALL = '#'
    PATH = ' '
    START = 'S'
    END = 'E'
    SOLUTION = '.'
    VISITED = 'o'
    
    def __init__(self, width: int, height: int):
        """
        初始化迷宫（全墙壁）。
        
        Args:
            width: 迷宫宽度（奇数，确保边界）
            height: 迷宫高度（奇数，确保边界）
        """
        self.width = width if width % 2 == 1 else width + 1
        self.height = height if height % 2 == 1 else height + 1
        self.grid: List[List[str]] = [[self.WALL for _ in range(self.width)] 
                                       for _ in range(self.height)]
        self.start: Optional[Tuple[int, int]] = None
        self.end: Optional[Tuple[int, int]] = None
    
    def __str__(self) -> str:
        """返回迷宫的字符串表示。"""
        return '\n'.join(''.join(row) for row in self.grid)
    
    def __repr__(self) -> str:
        return f"Maze(width={self.width}, height={self.height})"
    
    def copy(self) -> 'Maze':
        """创建迷宫的深拷贝。"""
        new_maze = Maze(self.width, self.height)
        new_maze.grid = [row[:] for row in self.grid]
        new_maze.start = self.start
        new_maze.end = self.end
        return new_maze
    
    def is_valid(self, x: int, y: int) -> bool:
        """检查坐标是否在迷宫范围内。"""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def is_wall(self, x: int, y: int) -> bool:
        """检查位置是否为墙壁。"""
        if not self.is_valid(x, y):
            return True
        return self.grid[y][x] == self.WALL
    
    def is_path(self, x: int, y: int) -> bool:
        """检查位置是否为通道。"""
        if not self.is_valid(x, y):
            return False
        return self.grid[y][x] != self.WALL
    
    def set_cell(self, x: int, y: int, value: str):
        """设置指定位置的值。"""
        if self.is_valid(x, y):
            self.grid[y][x] = value
    
    def get_cell(self, x: int, y: int) -> str:
        """获取指定位置的值。"""
        if self.is_valid(x, y):
            return self.grid[y][x]
        return self.WALL
    
    def get_neighbors(self, x: int, y: int, diagonal: bool = False) -> List[Tuple[int, int]]:
        """
        获取相邻位置。
        
        Args:
            x: x坐标
            y: y坐标
            diagonal: 是否包含对角方向
            
        Returns:
            相邻位置列表 [(x1, y1), ...]
        """
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if diagonal:
            directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_valid(nx, ny):
                neighbors.append((nx, ny))
        return neighbors
    
    def set_start(self, x: int, y: int):
        """设置起点。"""
        self.start = (x, y)
        self.set_cell(x, y, self.START)
    
    def set_end(self, x: int, y: int):
        """设置终点。"""
        self.end = (x, y)
        self.set_cell(x, y, self.END)
    
    def clear_solution(self):
        """清除解决方案路径。"""
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == self.SOLUTION:
                    self.grid[y][x] = self.PATH
        # 恢复起点和终点
        if self.start:
            self.set_cell(self.start[0], self.start[1], self.START)
        if self.end:
            self.set_cell(self.end[0], self.end[1], self.END)


class MazeGenerator:
    """迷宫生成器，提供多种生成算法。"""
    
    @staticmethod
    def generate_dfs(width: int, height: int, 
                    start: Optional[Tuple[int, int]] = None,
                    end: Optional[Tuple[int, int]] = None,
                    seed: Optional[int] = None) -> Maze:
        """
        使用深度优先搜索（递归回溯）生成迷宫。
        
        这是最经典的迷宫生成算法，生成的迷宫路径较长且有特点。
        
        Args:
            width: 迷宫宽度
            height: 迷宫高度
            start: 起点坐标（可选，默认左上角）
            end: 终点坐标（可选，默认右下角）
            seed: 随机种子（用于复现）
            
        Returns:
            生成的迷宫对象
        """
        if seed is not None:
            random.seed(seed)
        
        maze = Maze(width, height)
        
        # 从(1,1)开始挖掘
        stack = [(1, 1)]
        maze.set_cell(1, 1, Maze.PATH)
        
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        
        while stack:
            x, y = stack[-1]
            
            # 找到未访问的邻居
            neighbors = []
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if maze.is_valid(nx, ny) and maze.is_wall(nx, ny):
                    neighbors.append((nx, ny, dx, dy))
            
            if neighbors:
                # 随机选择一个邻居
                nx, ny, dx, dy = random.choice(neighbors)
                # 打通墙壁
                maze.set_cell(x + dx // 2, y + dy // 2, Maze.PATH)
                maze.set_cell(nx, ny, Maze.PATH)
                stack.append((nx, ny))
            else:
                stack.pop()
        
        # 设置起点和终点
        sx, sy = start if start else (1, 1)
        ex, ey = end if end else (maze.width - 2, maze.height - 2)
        maze.set_start(sx, sy)
        maze.set_end(ex, ey)
        
        return maze
    
    @staticmethod
    def generate_prim(width: int, height: int,
                     start: Optional[Tuple[int, int]] = None,
                     end: Optional[Tuple[int, int]] = None,
                     seed: Optional[int] = None) -> Maze:
        """
        使用Prim算法生成迷宫。
        
        生成的迷宫分支较多，路径较短。
        
        Args:
            width: 迷宫宽度
            height: 迷宫高度
            start: 起点坐标
            end: 终点坐标
            seed: 随机种子
            
        Returns:
            生成的迷宫对象
        """
        if seed is not None:
            random.seed(seed)
        
        maze = Maze(width, height)
        
        # 从(1,1)开始
        maze.set_cell(1, 1, Maze.PATH)
        
        # 候选墙壁列表
        walls = set()
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            wx, wy = 1 + dx, 1 + dy
            if maze.is_valid(wx, wy) and maze.is_wall(wx, wy):
                walls.add((wx, wy, 1, 1))
        
        while walls:
            # 随机选择一面墙
            wall = random.choice(list(walls))
            walls.remove(wall)
            wx, wy, cx, cy = wall
            
            if maze.is_wall(wx, wy):
                # 检查墙另一侧
                dx, dy = wx - cx, wy - cy
                nx, ny = wx + dx, wy + dy
                
                if maze.is_valid(nx, ny) and maze.is_wall(nx, ny):
                    # 打通墙壁和新单元格
                    maze.set_cell(wx, wy, Maze.PATH)
                    maze.set_cell(nx, ny, Maze.PATH)
                    
                    # 添加新候选墙壁
                    for ddx, ddy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nwx, nwy = nx + ddx, ny + ddy
                        if maze.is_valid(nwx, nwy) and maze.is_wall(nwx, nwy):
                            walls.add((nwx, nwy, nx, ny))
        
        # 设置起点和终点
        sx, sy = start if start else (1, 1)
        ex, ey = end if end else (maze.width - 2, maze.height - 2)
        maze.set_start(sx, sy)
        maze.set_end(ex, ey)
        
        return maze
    
    @staticmethod
    def generate_kruskal(width: int, height: int,
                        start: Optional[Tuple[int, int]] = None,
                        end: Optional[Tuple[int, int]] = None,
                        seed: Optional[int] = None) -> Maze:
        """
        使用Kruskal算法生成迷宫。
        
        基于最小生成树思想，使用并查集实现。
        
        Args:
            width: 迷宫宽度
            height: 迷宫高度
            start: 起点坐标
            end: 终点坐标
            seed: 随机种子
            
        Returns:
            生成的迷宫对象
        """
        if seed is not None:
            random.seed(seed)
        
        maze = Maze(width, height)
        
        # 收集所有单元格（奇数坐标）
        cells = []
        for y in range(1, maze.height, 2):
            for x in range(1, maze.width, 2):
                cells.append((x, y))
                maze.set_cell(x, y, Maze.PATH)
        
        # 并查集
        parent = {cell: cell for cell in cells}
        rank = {cell: 0 for cell in cells}
        
        def find(cell):
            if parent[cell] != cell:
                parent[cell] = find(parent[cell])
            return parent[cell]
        
        def union(cell1, cell2):
            root1, root2 = find(cell1), find(cell2)
            if root1 != root2:
                if rank[root1] < rank[root2]:
                    root1, root2 = root2, root1
                parent[root2] = root1
                if rank[root1] == rank[root2]:
                    rank[root1] += 1
                return True
            return False
        
        # 收集所有可能的墙
        walls = []
        for y in range(1, maze.height, 2):
            for x in range(1, maze.width, 2):
                if x + 2 < maze.width:
                    walls.append(((x, y), (x + 2, y), (x + 1, y)))
                if y + 2 < maze.height:
                    walls.append(((x, y), (x, y + 2), (x, y + 1)))
        
        random.shuffle(walls)
        
        for cell1, cell2, wall in walls:
            if union(cell1, cell2):
                maze.set_cell(wall[0], wall[1], Maze.PATH)
        
        # 设置起点和终点
        sx, sy = start if start else (1, 1)
        ex, ey = end if end else (maze.width - 2, maze.height - 2)
        maze.set_start(sx, sy)
        maze.set_end(ex, ey)
        
        return maze
    
    @staticmethod
    def generate_recursive_division(width: int, height: int,
                                    start: Optional[Tuple[int, int]] = None,
                                    end: Optional[Tuple[int, int]] = None,
                                    seed: Optional[int] = None) -> Maze:
        """
        使用递归分割算法生成迷宫。
        
        从空房间开始，递归添加墙壁和通道。
        
        Args:
            width: 迷宫宽度
            height: 迷宫高度
            start: 起点坐标
            end: 终点坐标
            seed: 随机种子
            
        Returns:
            生成的迷宫对象
        """
        if seed is not None:
            random.seed(seed)
        
        maze = Maze(width, height)
        
        # 初始化为全通道
        for y in range(maze.height):
            for x in range(maze.width):
                maze.set_cell(x, y, Maze.PATH)
        
        # 设置边界墙
        for x in range(maze.width):
            maze.set_cell(x, 0, Maze.WALL)
            maze.set_cell(x, maze.height - 1, Maze.WALL)
        for y in range(maze.height):
            maze.set_cell(0, y, Maze.WALL)
            maze.set_cell(maze.width - 1, y, Maze.WALL)
        
        def divide(x, y, w, h, orientation):
            if w < 3 or h < 3:
                return
            
            horizontal = orientation == 'h'
            
            if horizontal:
                # 水平分割 - 选择偶数行作为墙
                # 确保在有效范围内
                possible_y = [y + i for i in range(2, h - 1, 2)]
                if not possible_y:
                    possible_y = [y + i for i in range(2, h - 1)]
                if not possible_y:
                    return
                py = random.choice(possible_y)
                
                # 选择通道位置（奇数列）
                possible_x = [x + i for i in range(1, w - 1, 2)]
                if not possible_x:
                    possible_x = [x + i for i in range(1, w - 1)]
                if not possible_x:
                    return
                px = random.choice(possible_x)
                
                # 添加墙
                for i in range(w):
                    if x + i != px:
                        maze.set_cell(x + i, py, Maze.WALL)
                
                # 递归
                divide(x, y, w, py - y, choose_orientation(w, py - y))
                divide(x, py + 1, w, y + h - py - 1, choose_orientation(w, y + h - py - 1))
            else:
                # 垂直分割 - 选择偶数列作为墙
                possible_x = [x + i for i in range(2, w - 1, 2)]
                if not possible_x:
                    possible_x = [x + i for i in range(2, w - 1)]
                if not possible_x:
                    return
                px = random.choice(possible_x)
                
                # 选择通道位置（奇数行）
                possible_y = [y + i for i in range(1, h - 1, 2)]
                if not possible_y:
                    possible_y = [y + i for i in range(1, h - 1)]
                if not possible_y:
                    return
                py = random.choice(possible_y)
                
                # 添加墙
                for i in range(h):
                    if y + i != py:
                        maze.set_cell(px, y + i, Maze.WALL)
                
                # 递归
                divide(x, y, px - x, h, choose_orientation(px - x, h))
                divide(px + 1, y, x + w - px - 1, h, choose_orientation(x + w - px - 1, h))
        
        def choose_orientation(w, h):
            if w < h:
                return 'h'
            elif h < w:
                return 'v'
            else:
                return random.choice(['h', 'v'])
        
        divide(1, 1, maze.width - 2, maze.height - 2, choose_orientation(maze.width - 2, maze.height - 2))
        
        # 设置起点和终点
        sx, sy = start if start else (1, 1)
        ex, ey = end if end else (maze.width - 2, maze.height - 2)
        maze.set_start(sx, sy)
        maze.set_end(ex, ey)
        
        return maze
    
    @staticmethod
    def generate_eller(width: int, height: int,
                      start: Optional[Tuple[int, int]] = None,
                      end: Optional[Tuple[int, int]] = None,
                      seed: Optional[int] = None) -> Maze:
        """
        使用Eller算法生成迷宫。
        
        逐行生成，内存效率高，适合生成大型迷宫。
        
        Args:
            width: 迷宫宽度
            height: 迷宫高度
            start: 起点坐标
            end: 终点坐标
            seed: 随机种子
            
        Returns:
            生成的迷宫对象
        """
        if seed is not None:
            random.seed(seed)
        
        maze = Maze(width, height)
        
        # 确保奇数尺寸
        w = (maze.width - 1) // 2  # 单元格数量
        h = (maze.height - 1) // 2
        
        if w < 1 or h < 1:
            # 迷宫太小，直接设置起点终点
            maze.set_start(1, 1)
            maze.set_end(maze.width - 2, maze.height - 2)
            return maze
        
        # 当前行的集合
        sets = {}  # 列 -> 集合编号
        next_set = 0
        
        for row in range(h):
            # 分配集合（新单元格分配新集合）
            for col in range(w):
                if col not in sets:
                    sets[col] = next_set
                    next_set += 1
            
            # 绘制当前行单元格
            for col in range(w):
                maze.set_cell(1 + col * 2, 1 + row * 2, Maze.PATH)
            
            # 水平连接（同一行相邻单元格）
            for col in range(w - 1):
                # 最后一行强制连接不同集合
                should_connect = (row == h - 1) or (random.random() < 0.5)
                
                if sets[col] != sets[col + 1] and should_connect:
                    # 合并集合
                    old_set = sets[col + 1]
                    new_set = sets[col]
                    for c in list(sets.keys()):
                        if sets[c] == old_set:
                            sets[c] = new_set
                    # 打通墙壁（单元格之间的墙）
                    maze.set_cell(1 + col * 2 + 1, 1 + row * 2, Maze.PATH)
            
            if row < h - 1:
                # 垂直连接（到下一行）
                # 每个集合至少有一个向下连接
                connections = {}  # 集合 -> 连接列表
                for col in range(w):
                    s = sets[col]
                    if s not in connections:
                        connections[s] = []
                    connections[s].append(col)
                
                # 确保每个集合至少有一个向下连接
                for s, cols in connections.items():
                    # 随机选择至少一个单元格向下连接
                    # 每个单元格有50%概率向下连接，但至少一个
                    down_cols = []
                    for col in cols:
                        if random.random() < 0.5:
                            down_cols.append(col)
                    
                    # 如果没有连接，随机选一个
                    if not down_cols:
                        down_cols = [random.choice(cols)]
                    
                    for col in down_cols:
                        maze.set_cell(1 + col * 2, 1 + row * 2 + 1, Maze.PATH)
                
                # 为下一行准备 - 只有有向下连接的单元格保持集合
                new_sets = {}
                for col in range(w):
                    # 检查是否有向下的连接
                    if maze.get_cell(1 + col * 2, 1 + row * 2 + 1) == Maze.PATH:
                        new_sets[col] = sets[col]
                sets = new_sets
        
        # 设置起点和终点
        sx, sy = start if start else (1, 1)
        ex, ey = end if end else (maze.width - 2, maze.height - 2)
        maze.set_start(sx, sy)
        maze.set_end(ex, ey)
        
        return maze


class MazeSolver:
    """迷宫求解器，提供多种求解算法。"""
    
    @staticmethod
    def solve_bfs(maze: Maze) -> Optional[List[Tuple[int, int]]]:
        """
        使用广度优先搜索求解迷宫，找到最短路径。
        
        Args:
            maze: 迷宫对象
            
        Returns:
            路径坐标列表 [(x1, y1), ...]，如果无解返回 None
        """
        if not maze.start or not maze.end:
            return None
        
        start = maze.start
        end = maze.end
        
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            (x, y), path = queue.popleft()
            
            if (x, y) == end:
                return path
            
            for nx, ny in maze.get_neighbors(x, y):
                if (nx, ny) not in visited and maze.is_path(nx, ny):
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))
        
        return None
    
    @staticmethod
    def solve_dfs(maze: Maze) -> Optional[List[Tuple[int, int]]]:
        """
        使用深度优先搜索求解迷宫。
        
        不保证最短路径，但内存使用较少。
        
        Args:
            maze: 迷宫对象
            
        Returns:
            路径坐标列表，如果无解返回 None
        """
        if not maze.start or not maze.end:
            return None
        
        start = maze.start
        end = maze.end
        
        stack = [(start, [start])]
        visited = {start}
        
        while stack:
            (x, y), path = stack.pop()
            
            if (x, y) == end:
                return path
            
            for nx, ny in maze.get_neighbors(x, y):
                if (nx, ny) not in visited and maze.is_path(nx, ny):
                    visited.add((nx, ny))
                    stack.append(((nx, ny), path + [(nx, ny)]))
        
        return None
    
    @staticmethod
    def solve_astar(maze: Maze) -> Optional[List[Tuple[int, int]]]:
        """
        使用A*算法求解迷宫，找到最短路径。
        
        Args:
            maze: 迷宫对象
            
        Returns:
            路径坐标列表，如果无解返回 None
        """
        if not maze.start or not maze.end:
            return None
        
        start = maze.start
        end = maze.end
        
        def heuristic(pos):
            """曼哈顿距离启发式函数。"""
            return abs(pos[0] - end[0]) + abs(pos[1] - end[1])
        
        # 优先队列：(f_score, g_score, position, path)
        import heapq
        open_set = [(heuristic(start), 0, start, [start])]
        visited = {}
        
        while open_set:
            f, g, pos, path = heapq.heappop(open_set)
            
            if pos == end:
                return path
            
            if pos in visited and visited[pos] <= g:
                continue
            visited[pos] = g
            
            for nx, ny in maze.get_neighbors(pos[0], pos[1]):
                if maze.is_path(nx, ny):
                    new_g = g + 1
                    new_f = new_g + heuristic((nx, ny))
                    heapq.heappush(open_set, (new_f, new_g, (nx, ny), path + [(nx, ny)]))
        
        return None
    
    @staticmethod
    def solve_wall_follower(maze: Maze, direction: str = 'right') -> Optional[List[Tuple[int, int]]]:
        """
        使用墙壁跟随算法求解迷宫。
        
        一直沿着墙壁的一侧行走，简单但效率较低。
        
        Args:
            maze: 迷宫对象
            direction: 跟随方向 ('left' 或 'right')
            
        Returns:
            路径坐标列表，如果无解返回 None
        """
        if not maze.start or not maze.end:
            return None
        
        # 方向: 北、东、南、西
        dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        
        pos = maze.start
        end = maze.end
        path = [pos]
        
        # 初始方向朝东
        d = 1
        
        # 右手法则：右-前-左-后
        # 左手法则：左-前-右-后
        if direction == 'right':
            turn_order = [3, 0, 1, 2]  # 右转、直行、左转、后转
        else:
            turn_order = [1, 0, 3, 2]  # 左转、直行、右转、后转
        
        max_steps = maze.width * maze.height * 4
        steps = 0
        
        while pos != end and steps < max_steps:
            steps += 1
            
            # 尝试按顺序转向
            moved = False
            for turn in turn_order:
                new_d = (d + turn) % 4
                dx, dy = dirs[new_d]
                nx, ny = pos[0] + dx, pos[1] + dy
                
                if maze.is_path(nx, ny):
                    pos = (nx, ny)
                    d = new_d
                    path.append(pos)
                    moved = True
                    break
            
            if not moved:
                # 死胡同，原路返回
                if len(path) > 1:
                    path.pop()
                    pos = path[-1] if path else maze.start
                else:
                    break
        
        if pos == end:
            return path
        return None
    
    @staticmethod
    def solve_dead_end_filling(maze: Maze) -> Optional[List[Tuple[int, int]]]:
        """
        使用死胡同填充算法求解迷宫。
        
        通过填充所有死胡同，最终留下正确路径。
        
        Args:
            maze: 迷宫对象
            
        Returns:
            路径坐标列表，如果无解返回 None
        """
        if not maze.start or not maze.end:
            return None
        
        # 创建迷宫副本
        grid = [row[:] for row in maze.grid]
        start = maze.start
        end = maze.end
        
        def is_dead_end(x, y):
            """检查是否为死胡同。"""
            if (x, y) == start or (x, y) == end:
                return False
            if grid[y][x] == Maze.WALL:
                return False
            # 计算通道邻居数
            passages = 0
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                    if grid[ny][nx] != Maze.WALL:
                        passages += 1
            return passages == 1
        
        # 填充所有死胡同
        changed = True
        while changed:
            changed = False
            for y in range(len(grid)):
                for x in range(len(grid[0])):
                    if is_dead_end(x, y):
                        grid[y][x] = Maze.WALL
                        changed = True
        
        # 从剩余通道中提取路径
        path = []
        visited = set()
        pos = start
        
        while pos != end:
            path.append(pos)
            visited.add(pos)
            
            # 找下一个位置
            found = False
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = pos[0] + dx, pos[1] + dy
                if (0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and
                    (nx, ny) not in visited and grid[ny][nx] != Maze.WALL):
                    pos = (nx, ny)
                    found = True
                    break
            
            if not found:
                return None
        
        path.append(end)
        return path


class MazeUtils:
    """迷宫工具类，提供便捷的静态方法。"""
    
    @staticmethod
    def generate(width: int, height: int, 
                 algorithm: str = 'dfs',
                 seed: Optional[int] = None) -> Maze:
        """
        生成迷宫的便捷方法。
        
        Args:
            width: 迷宫宽度
            height: 迷宫高度
            algorithm: 生成算法 ('dfs', 'prim', 'kruskal', 'division', 'eller')
            seed: 随机种子
            
        Returns:
            生成的迷宫对象
        """
        algorithms = {
            'dfs': MazeGenerator.generate_dfs,
            'prim': MazeGenerator.generate_prim,
            'kruskal': MazeGenerator.generate_kruskal,
            'division': MazeGenerator.generate_recursive_division,
            'eller': MazeGenerator.generate_eller
        }
        
        if algorithm not in algorithms:
            raise ValueError(f"未知算法: {algorithm}，可选: {list(algorithms.keys())}")
        
        return algorithms[algorithm](width, height, seed=seed)
    
    @staticmethod
    def solve(maze: Maze, algorithm: str = 'bfs') -> Optional[List[Tuple[int, int]]]:
        """
        求解迷宫的便捷方法。
        
        Args:
            maze: 迷宫对象
            algorithm: 求解算法 ('bfs', 'dfs', 'astar', 'wall_right', 'wall_left', 'dead_end')
            
        Returns:
            路径坐标列表，如果无解返回 None
        """
        algorithms = {
            'bfs': MazeSolver.solve_bfs,
            'dfs': MazeSolver.solve_dfs,
            'astar': MazeSolver.solve_astar,
            'wall_right': lambda m: MazeSolver.solve_wall_follower(m, 'right'),
            'wall_left': lambda m: MazeSolver.solve_wall_follower(m, 'left'),
            'dead_end': MazeSolver.solve_dead_end_filling
        }
        
        if algorithm not in algorithms:
            raise ValueError(f"未知算法: {algorithm}，可选: {list(algorithms.keys())}")
        
        return algorithms[algorithm](maze)
    
    @staticmethod
    def visualize(maze: Maze, path: Optional[List[Tuple[int, int]]] = None) -> str:
        """
        可视化迷宫和路径。
        
        Args:
            maze: 迷宫对象
            path: 路径坐标列表（可选）
            
        Returns:
            ASCII艺术字符串
        """
        # 创建副本
        display = [row[:] for row in maze.grid]
        
        # 绘制路径
        if path:
            for i, (x, y) in enumerate(path):
                if display[y][x] not in (Maze.START, Maze.END):
                    display[y][x] = Maze.SOLUTION
        
        return '\n'.join(''.join(row) for row in display)
    
    @staticmethod
    def validate_maze(maze: Maze) -> Tuple[bool, List[str]]:
        """
        验证迷宫的有效性。
        
        Args:
            maze: 迷宫对象
            
        Returns:
            (是否有效, 错误信息列表)
        """
        errors = []
        
        # 检查起点和终点
        if not maze.start:
            errors.append("迷宫缺少起点")
        if not maze.end:
            errors.append("迷宫缺少终点")
        
        # 检查起点和终点是否为通道
        if maze.start and not maze.is_path(*maze.start):
            errors.append("起点位于墙壁上")
        if maze.end and not maze.is_path(*maze.end):
            errors.append("终点位于墙壁上")
        
        # 检查是否有解
        if maze.start and maze.end:
            path = MazeSolver.solve_bfs(maze)
            if path is None:
                errors.append("迷宫无解：起点和终点之间没有路径")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def get_statistics(maze: Maze) -> dict:
        """
        获取迷宫统计信息。
        
        Args:
            maze: 迷宫对象
            
        Returns:
            统计信息字典
        """
        total_cells = maze.width * maze.height
        wall_count = sum(row.count(Maze.WALL) for row in maze.grid)
        path_count = total_cells - wall_count
        
        return {
            'width': maze.width,
            'height': maze.height,
            'total_cells': total_cells,
            'walls': wall_count,
            'passages': path_count,
            'wall_ratio': wall_count / total_cells,
            'passage_ratio': path_count / total_cells
        }
    
    @staticmethod
    def create_from_string(maze_str: str) -> Maze:
        """
        从字符串创建迷宫。
        
        Args:
            maze_str: 迷宫字符串，'#'为墙，' '为通道，'S'为起点，'E'为终点
            
        Returns:
            迷宫对象
        """
        lines = maze_str.strip().split('\n')
        height = len(lines)
        width = max(len(line) for line in lines) if lines else 0
        
        maze = Maze(width, height)
        
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == Maze.START:
                    maze.start = (x, y)
                    maze.set_cell(x, y, Maze.PATH)
                elif char == Maze.END:
                    maze.end = (x, y)
                    maze.set_cell(x, y, Maze.PATH)
                elif char == Maze.WALL:
                    maze.set_cell(x, y, Maze.WALL)
                else:
                    maze.set_cell(x, y, Maze.PATH)
        
        # 确保起点终点标记
        if maze.start:
            maze.set_cell(*maze.start, Maze.START)
        if maze.end:
            maze.set_cell(*maze.end, Maze.END)
        
        return maze
    
    @staticmethod
    def find_all_paths(maze: Maze, max_paths: int = 100) -> List[List[Tuple[int, int]]]:
        """
        找到所有可能的路径（最多 max_paths 条）。
        
        Args:
            maze: 迷宫对象
            max_paths: 最大路径数量
            
        Returns:
            路径列表
        """
        if not maze.start or not maze.end:
            return []
        
        paths = []
        stack = [(maze.start, [maze.start])]
        
        while stack and len(paths) < max_paths:
            pos, path = stack.pop()
            
            if pos == maze.end:
                paths.append(path)
                continue
            
            for nx, ny in maze.get_neighbors(*pos):
                if (nx, ny) not in path and maze.is_path(nx, ny):
                    stack.append(((nx, ny), path + [(nx, ny)]))
        
        return paths
    
    @staticmethod
    def get_path_length(maze: Maze, algorithm: str = 'bfs') -> Optional[int]:
        """
        获取路径长度。
        
        Args:
            maze: 迷宫对象
            algorithm: 求解算法
            
        Returns:
            路径长度，如果无解返回 None
        """
        path = MazeUtils.solve(maze, algorithm)
        return len(path) if path else None
    
    @staticmethod
    def compare_algorithms(maze: Maze) -> dict:
        """
        比较不同求解算法的结果。
        
        Args:
            maze: 迷宫对象
            
        Returns:
            比较结果字典
        """
        import time
        
        algorithms = ['bfs', 'dfs', 'astar', 'wall_right', 'dead_end']
        results = {}
        
        for algo in algorithms:
            start_time = time.time()
            path = MazeUtils.solve(maze, algo)
            elapsed = time.time() - start_time
            
            results[algo] = {
                'solved': path is not None,
                'path_length': len(path) if path else None,
                'time_seconds': elapsed
            }
        
        return results


# 便捷函数
def generate_maze(width: int, height: int, algorithm: str = 'dfs', 
                  seed: Optional[int] = None) -> Maze:
    """生成迷宫的便捷函数。"""
    return MazeUtils.generate(width, height, algorithm, seed)


def solve_maze(maze: Maze, algorithm: str = 'bfs') -> Optional[List[Tuple[int, int]]]:
    """求解迷宫的便捷函数。"""
    return MazeUtils.solve(maze, algorithm)


def print_maze(maze: Maze, path: Optional[List[Tuple[int, int]]] = None):
    """打印迷宫的便捷函数。"""
    print(MazeUtils.visualize(maze, path))


if __name__ == '__main__':
    # 演示代码
    print("=" * 60)
    print("迷宫工具模块演示")
    print("=" * 60)
    
    # 生成不同类型的迷宫
    print("\n1. DFS递归回溯迷宫 (21x11):")
    maze1 = generate_maze(21, 11, 'dfs', seed=42)
    print(maze1)
    
    print("\n2. Prim算法迷宫 (21x11):")
    maze2 = generate_maze(21, 11, 'prim', seed=42)
    print(maze2)
    
    # 求解迷宫
    print("\n3. 求解迷宫 (BFS最短路径):")
    path = solve_maze(maze1, 'bfs')
    if path:
        print(f"路径长度: {len(path)}")
        print(MazeUtils.visualize(maze1, path))
    
    # 比较算法
    print("\n4. 比较不同算法:")
    stats = MazeUtils.compare_algorithms(maze1)
    for algo, result in stats.items():
        if result['solved']:
            print(f"  {algo}: 路径长度={result['path_length']}, 耗时={result['time_seconds']:.6f}s")
        else:
            print(f"  {algo}: 无解")
    
    # 从字符串创建迷宫
    print("\n5. 从字符串创建迷宫:")
    maze_str = """
#########
#S  #   #
# # # # #
#   # # #
##### # #
#     #E#
#########
"""
    maze3 = MazeUtils.create_from_string(maze_str)
    print(maze3)
    path3 = solve_maze(maze3, 'astar')
    if path3:
        print(f"\nA*求解路径 (长度{len(path3)}):")
        print(MazeUtils.visualize(maze3, path3))