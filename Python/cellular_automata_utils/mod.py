"""
Cellular Automata Utils - 元胞自动机工具包

提供多种经典元胞自动机的实现，零外部依赖，仅使用 Python 标准库。

功能:
- Conway's Game of Life (康威生命游戏)
- Wolfram Elementary CA (沃尔夫勒姆初等元胞自动机)
- Langton's Ant (兰顿蚂蚁)
- Brian's Brain (布赖恩大脑)
- Wireworld (线世界)
- HighLife (高生命)
- Seeds (种子)
- 自定义规则支持

应用场景:
- 复杂系统模拟
- 图案生成
- 教育演示
- 艺术创作
- 算法研究

作者: AllToolkit
日期: 2026-04-24
"""

from typing import List, Tuple, Optional, Callable, Dict, Set, Iterator
from abc import ABC, abstractmethod
from copy import deepcopy


# ============================================================================
# 基础类和工具函数
# ============================================================================

class CellularAutomaton(ABC):
    """
    元胞自动机抽象基类。
    
    所有元胞自动机继承此类，实现具体的演化规则。
    """
    
    def __init__(self, width: int, height: int, wrap: bool = True):
        """
        初始化元胞自动机。
        
        Args:
            width: 网格宽度
            height: 网格高度
            wrap: 是否环绕边界（环形世界），默认 True
        """
        self.width = width
        self.height = height
        self.wrap = wrap
        self.generation = 0
        self._grid: List[List[int]] = [[0] * width for _ in range(height)]
    
    @abstractmethod
    def step(self) -> None:
        """执行一步演化。"""
        pass
    
    @abstractmethod
    def get_neighbors(self, x: int, y: int) -> List[int]:
        """获取邻居状态。"""
        pass
    
    def get_cell(self, x: int, y: int) -> int:
        """获取指定位置细胞状态。"""
        if self.wrap:
            x = x % self.width
            y = y % self.height
        else:
            if not (0 <= x < self.width and 0 <= y < self.height):
                return 0
        return self._grid[y][x]
    
    def set_cell(self, x: int, y: int, state: int) -> None:
        """设置指定位置细胞状态。"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self._grid[y][x] = state
    
    def set_pattern(self, pattern: List[Tuple[int, int, int]], offset: Tuple[int, int] = (0, 0)) -> None:
        """
        设置图案。
        
        Args:
            pattern: 图案列表，每个元素为 (x, y, state)
            offset: 偏移量 (dx, dy)
        """
        dx, dy = offset
        for x, y, state in pattern:
            self.set_cell(x + dx, y + dy, state)
    
    def clear(self) -> None:
        """清空网格。"""
        self._grid = [[0] * self.width for _ in range(self.height)]
        self.generation = 0
    
    def get_grid(self) -> List[List[int]]:
        """获取当前网格副本。"""
        return [row[:] for row in self._grid]
    
    def get_live_cells(self) -> Set[Tuple[int, int]]:
        """获取所有活细胞位置。"""
        cells = set()
        for y in range(self.height):
            for x in range(self.width):
                if self._grid[y][x]:
                    cells.add((x, y))
        return cells
    
    def count_alive(self) -> int:
        """统计活细胞数量。"""
        return sum(sum(row) for row in self._grid)
    
    def density(self) -> float:
        """计算活细胞密度。"""
        return self.count_alive() / (self.width * self.height)
    
    def evolve(self, steps: int = 1) -> None:
        """
        演化指定步数。
        
        Args:
            steps: 演化步数
        """
        for _ in range(steps):
            self.step()
    
    def run(self, max_generations: int = 1000, 
            stop_if_stable: bool = True,
            stable_generations: int = 10) -> Iterator[int]:
        """
        运行模拟，生成器模式。
        
        Args:
            max_generations: 最大代数
            stop_if_stable: 是否在稳定时停止
            stable_generations: 判断稳定的代数阈值
        
        Yields:
            当前代数
        """
        history = []
        for _ in range(max_generations):
            self.step()
            yield self.generation
            
            if stop_if_stable:
                grid_tuple = tuple(tuple(row) for row in self._grid)
                history.append(grid_tuple)
                if len(history) > stable_generations:
                    history.pop(0)
                    # 检查是否进入周期
                    if len(set(history)) <= 2:
                        return
    
    def to_string(self, alive: str = '█', dead: str = ' ') -> str:
        """
        将网格转换为字符串表示。
        
        Args:
            alive: 活细胞字符
            dead: 死细胞字符
        """
        lines = []
        for row in self._grid:
            lines.append(''.join(alive if cell else dead for cell in row))
        return '\n'.join(lines)
    
    def print_grid(self, alive: str = '█', dead: str = ' ') -> None:
        """打印当前网格。"""
        print(f"Generation {self.generation}:")
        print(self.to_string(alive, dead))


# ============================================================================
# Conway's Game of Life
# ============================================================================

class GameOfLife(CellularAutomaton):
    """
    康威生命游戏。
    
    规则:
    1. 活细胞周围有 2-3 个活邻居则存活，否则死亡
    2. 死细胞周围恰好有 3 个活邻居则复活
    
    特殊图案:
    - Glider (滑翔机): 5 格的移动图案
    - Blinker (闪烁器): 3 格的振荡器
    - Pulsar (脉冲星): 周期 3 振荡器
    - Gosper Glider Gun (高斯帕滑翔机枪): 产生滑翔机
    """
    
    def get_neighbors(self, x: int, y: int) -> List[int]:
        """获取摩尔邻域（8邻域）状态。"""
        neighbors = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbors.append(self.get_cell(x + dx, y + dy))
        return neighbors
    
    def step(self) -> None:
        """执行一步生命游戏演化。"""
        new_grid = [[0] * self.width for _ in range(self.height)]
        
        for y in range(self.height):
            for x in range(self.width):
                alive_neighbors = sum(self.get_neighbors(x, y))
                current = self._grid[y][x]
                
                # 规则应用
                if current:  # 活细胞
                    if alive_neighbors in (2, 3):
                        new_grid[y][x] = 1
                    # else 死亡（默认为0）
                else:  # 死细胞
                    if alive_neighbors == 3:
                        new_grid[y][x] = 1
        
        self._grid = new_grid
        self.generation += 1
    
    def add_glider(self, x: int = 0, y: int = 0, direction: int = 0) -> None:
        """
        添加滑翔机。
        
        Args:
            x, y: 左上角位置
            direction: 方向 (0=右下, 1=左下, 2=左上, 3=右上)
        """
        patterns = {
            0: [(1, 0, 1), (2, 1, 1), (0, 2, 1), (1, 2, 1), (2, 2, 1)],  # 右下
            1: [(0, 0, 1), (0, 1, 1), (0, 2, 1), (1, 2, 1), (2, 1, 1)],  # 左下
            2: [(0, 0, 1), (1, 0, 1), (2, 0, 1), (0, 1, 1), (2, 2, 1)],  # 左上
            3: [(0, 1, 1), (1, 0, 1), (2, 0, 1), (2, 1, 1), (2, 2, 1)],  # 右上
        }
        self.set_pattern(patterns[direction % 4], (x, y))
    
    def add_blinker(self, x: int = 0, y: int = 0, horizontal: bool = True) -> None:
        """添加闪烁器（周期 2 振荡器）。"""
        if horizontal:
            self.set_pattern([(0, 0, 1), (1, 0, 1), (2, 0, 1)], (x, y))
        else:
            self.set_pattern([(0, 0, 1), (0, 1, 1), (0, 2, 1)], (x, y))
    
    def add_pulsar(self, x: int = 0, y: int = 0) -> None:
        """添加脉冲星（周期 3 振荡器）。"""
        pulsar = [
            (2, 0, 1), (3, 0, 1), (4, 0, 1), (8, 0, 1), (9, 0, 1), (10, 0, 1),
            (0, 2, 1), (5, 2, 1), (7, 2, 1), (12, 2, 1),
            (0, 3, 1), (5, 3, 1), (7, 3, 1), (12, 3, 1),
            (0, 4, 1), (5, 4, 1), (7, 4, 1), (12, 4, 1),
            (2, 5, 1), (3, 5, 1), (4, 5, 1), (8, 5, 1), (9, 5, 1), (10, 5, 1),
            (2, 7, 1), (3, 7, 1), (4, 7, 1), (8, 7, 1), (9, 7, 1), (10, 7, 1),
            (0, 8, 1), (5, 8, 1), (7, 8, 1), (12, 8, 1),
            (0, 9, 1), (5, 9, 1), (7, 9, 1), (12, 9, 1),
            (0, 10, 1), (5, 10, 1), (7, 10, 1), (12, 10, 1),
            (2, 12, 1), (3, 12, 1), (4, 12, 1), (8, 12, 1), (9, 12, 1), (10, 12, 1),
        ]
        self.set_pattern(pulsar, (x, y))
    
    def add_gosper_glider_gun(self, x: int = 0, y: int = 0) -> None:
        """添加高斯帕滑翔机枪。"""
        gun = [
            (0, 4, 1),
            (1, 4, 1), (1, 5, 1),
            (10, 4, 1), (10, 5, 1), (10, 6, 1),
            (11, 3, 1), (11, 7, 1),
            (12, 2, 1), (12, 8, 1),
            (13, 2, 1), (13, 8, 1),
            (14, 5, 1),
            (15, 3, 1), (15, 7, 1),
            (16, 4, 1), (16, 5, 1), (16, 6, 1),
            (17, 5, 1),
            (20, 2, 1), (20, 3, 1), (20, 4, 1),
            (21, 2, 1), (21, 3, 1), (21, 4, 1),
            (22, 1, 1), (22, 5, 1),
            (24, 0, 1), (24, 1, 1), (24, 5, 1), (24, 6, 1),
            (34, 2, 1), (34, 3, 1),
            (35, 2, 1), (35, 3, 1),
        ]
        self.set_pattern(gun, (x, y))
    
    def randomize(self, density: float = 0.3) -> None:
        """
        随机填充网格。
        
        Args:
            density: 活细胞密度 (0-1)
        """
        import random
        for y in range(self.height):
            for x in range(self.width):
                self._grid[y][x] = 1 if random.random() < density else 0
        self.generation = 0


# ============================================================================
# Wolfram Elementary Cellular Automaton
# ============================================================================

class ElementaryCA(CellularAutomaton):
    """
    沃尔夫勒姆初等元胞自动机。
    
    一维元胞自动机，规则由 8 位规则号定义 (0-255)。
    
    著名规则:
    - Rule 30: 混沌图案
    - Rule 90: 分形三角形（谢尔宾斯基三角形）
    - Rule 110: 图灵完备
    - Rule 184: 交通流模型
    """
    
    def __init__(self, width: int, rule: int = 30, wrap: bool = True):
        """
        初始化初等元胞自动机。
        
        Args:
            width: 网格宽度
            rule: 规则号 (0-255)
            wrap: 是否环绕边界
        """
        # 对于一维 CA，高度为 1
        super().__init__(width, 1, wrap)
        self.rule = rule
        self._history: List[List[int]] = []
        self._rule_table = self._build_rule_table(rule)
    
    def _build_rule_table(self, rule: int) -> Dict[Tuple[int, int, int], int]:
        """构建规则查找表。"""
        table = {}
        for i in range(8):
            left = (i >> 2) & 1
            center = (i >> 1) & 1
            right = i & 1
            output = (rule >> i) & 1
            table[(left, center, right)] = output
        return table
    
    def get_neighbors(self, x: int, y: int) -> List[int]:
        """获取左右邻居。"""
        return [
            self.get_cell(x - 1, y),
            self.get_cell(x + 1, y)
        ]
    
    def step(self) -> None:
        """执行一步演化。"""
        new_row = [0] * self.width
        
        for x in range(self.width):
            left = self.get_cell(x - 1, 0)
            center = self.get_cell(x, 0)
            right = self.get_cell(x + 1, 0)
            new_row[x] = self._rule_table[(left, center, right)]
        
        self._grid[0] = new_row
        self.generation += 1
    
    def set_rule(self, rule: int) -> None:
        """设置新规则。"""
        self.rule = rule % 256
        self._rule_table = self._build_rule_table(self.rule)
    
    def initialize_single(self, x: Optional[int] = None) -> None:
        """
        初始化单个活细胞。
        
        Args:
            x: 活细胞位置，默认为中央
        """
        self.clear()
        if x is None:
            x = self.width // 2
        self.set_cell(x, 0, 1)
    
    def initialize_random(self, density: float = 0.5) -> None:
        """随机初始化。"""
        import random
        self.clear()
        for x in range(self.width):
            self.set_cell(x, 0, 1 if random.random() < density else 0)
    
    def get_history(self) -> List[List[int]]:
        """获取历史记录。"""
        return self._history[:]
    
    def run_with_history(self, steps: int) -> List[List[int]]:
        """
        运行并记录历史。
        
        Args:
            steps: 运行步数
        
        Returns:
            历史网格列表
        """
        self._history = [self._grid[0][:]]
        for _ in range(steps):
            self.step()
            self._history.append(self._grid[0][:])
        return self._history
    
    def to_string_history(self, alive: str = '█', dead: str = ' ') -> str:
        """将历史记录转换为字符串。"""
        lines = []
        for row in self._history:
            lines.append(''.join(alive if cell else dead for cell in row))
        return '\n'.join(lines)


# ============================================================================
# Langton's Ant
# ============================================================================

class LangtonsAnt(CellularAutomaton):
    """
    兰顿蚂蚁。
    
    规则:
    1. 在白色格子上，右转 90°，翻转格子颜色，前进
    2. 在黑色格子上，左转 90°，翻转格子颜色，前进
    
    特性:
    - 初期混沌行为
    - 约 10000 步后开始构建"高速公路"
    - 多蚂蚁支持
    """
    
    def __init__(self, width: int, height: int, wrap: bool = True):
        super().__init__(width, height, wrap)
        # 蚂蚁位置和方向
        self.ants: List[Dict] = []
        # 方向: 0=上, 1=右, 2=下, 3=左
        self._directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    
    def get_neighbors(self, x: int, y: int) -> List[int]:
        """蚂蚁不需要邻居信息。"""
        return []
    
    def add_ant(self, x: int, y: int, direction: int = 0) -> None:
        """
        添加蚂蚁。
        
        Args:
            x, y: 初始位置
            direction: 初始方向 (0=上, 1=右, 2=下, 3=左)
        """
        self.ants.append({
            'x': x,
            'y': y,
            'direction': direction % 4
        })
    
    def step(self) -> None:
        """执行一步蚂蚁移动。"""
        for ant in self.ants:
            x, y = ant['x'], ant['y']
            direction = ant['direction']
            
            # 获取当前格子状态
            current_state = self.get_cell(x, y)
            
            # 根据规则转向
            if current_state == 0:  # 白色 -> 右转
                direction = (direction + 1) % 4
            else:  # 黑色 -> 左转
                direction = (direction - 1) % 4
            
            # 翻转格子颜色
            self.set_cell(x, y, 1 - current_state)
            
            # 前进
            dx, dy = self._directions[direction]
            new_x = (x + dx) % self.width if self.wrap else x + dx
            new_y = (y + dy) % self.height if self.wrap else y + dy
            
            # 更新蚂蚁状态
            ant['x'] = new_x
            ant['y'] = new_y
            ant['direction'] = direction
        
        self.generation += 1
    
    def clear(self) -> None:
        """清空网格和蚂蚁。"""
        super().clear()
        self.ants = []
    
    def get_ant_positions(self) -> List[Tuple[int, int, int]]:
        """
        获取所有蚂蚁位置和方向。
        
        Returns:
            列表 of (x, y, direction)
        """
        return [(a['x'], a['y'], a['direction']) for a in self.ants]


class MultiColorAnt(LangtonsAnt):
    """
    多色蚂蚁（扩展规则）。
    
    支持多于两种颜色，使用自定义规则字符串。
    规则字符串如 'LR' 表示两种颜色：0=左转，1=右转
    规则字符串如 'LLRR' 表示四种颜色
    """
    
    def __init__(self, width: int, height: int, rule: str = 'LR', wrap: bool = True):
        super().__init__(width, height, wrap)
        self.rule = rule.upper()
        self.num_colors = len(rule)
        # 扩展网格支持多种状态
        self._grid: List[List[int]] = [[0] * width for _ in range(height)]
    
    def step(self) -> None:
        """执行一步。"""
        for ant in self.ants:
            x, y = ant['x'], ant['y']
            direction = ant['direction']
            
            # 获取当前格子状态
            current_state = self.get_cell(x, y)
            
            # 根据规则转向
            turn = self.rule[current_state]
            if turn == 'R':
                direction = (direction + 1) % 4
            elif turn == 'L':
                direction = (direction - 1) % 4
            
            # 更新格子状态
            new_state = (current_state + 1) % self.num_colors
            self.set_cell(x, y, new_state)
            
            # 前进
            dx, dy = self._directions[direction]
            new_x = (x + dx) % self.width if self.wrap else x + dx
            new_y = (y + dy) % self.height if self.wrap else y + dy
            
            ant['x'] = new_x
            ant['y'] = new_y
            ant['direction'] = direction
        
        self.generation += 1
    
    def to_string(self, chars: str = ' .:-=+*#@', default: str = ' ') -> str:
        """
        将网格转换为字符串。
        
        Args:
            chars: 各状态对应的字符
            default: 超出范围的默认字符
        """
        lines = []
        for row in self._grid:
            lines.append(''.join(
                chars[cell] if cell < len(chars) else default 
                for cell in row
            ))
        return '\n'.join(lines)


# ============================================================================
# Brian's Brain
# ============================================================================

class BriansBrain(CellularAutomaton):
    """
    布赖恩大脑。
    
    三态细胞自动机:
    - 状态 0: 死 (off)
    - 状态 1: 活 (on)
    - 状态 2: 衰减 (dying)
    
    规则:
    - 死 -> 活: 恰好 2 个活邻居
    - 活 -> 衰减
    - 衰减 -> 死
    
    产生复杂的脉冲波和螺旋图案。
    """
    
    # 状态常量
    DEAD = 0
    ALIVE = 1
    DYING = 2
    
    def get_neighbors(self, x: int, y: int) -> List[int]:
        """获取摩尔邻域状态。"""
        neighbors = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbors.append(self.get_cell(x + dx, y + dy))
        return neighbors
    
    def step(self) -> None:
        """执行一步演化。"""
        new_grid = [[0] * self.width for _ in range(self.height)]
        
        for y in range(self.height):
            for x in range(self.width):
                current = self._grid[y][x]
                alive_neighbors = sum(1 for n in self.get_neighbors(x, y) if n == self.ALIVE)
                
                if current == self.DEAD:
                    # 死细胞恰好 2 个活邻居则激活
                    new_grid[y][x] = self.ALIVE if alive_neighbors == 2 else self.DEAD
                elif current == self.ALIVE:
                    # 活细胞进入衰减状态
                    new_grid[y][x] = self.DYING
                else:  # DYING
                    # 衰减细胞死亡
                    new_grid[y][x] = self.DEAD
        
        self._grid = new_grid
        self.generation += 1
    
    def to_string(self, chars: str = ' █░') -> str:
        """
        将网格转换为字符串。
        
        Args:
            chars: 死/活/衰减状态对应的字符
        """
        lines = []
        for row in self._grid:
            lines.append(''.join(chars[cell] for cell in row))
        return '\n'.join(lines)


# ============================================================================
# Wireworld
# ============================================================================

class Wireworld(CellularAutomaton):
    """
    线世界元胞自动机。
    
    四态细胞自动机，用于模拟电子电路:
    - 状态 0: 空 (empty)
    - 状态 1: 导体 (conductor)
    - 状态 2: 电子头 (electron head)
    - 状态 3: 电子尾 (electron tail)
    
    规则:
    - 空 -> 空
    - 电子头 -> 电子尾
    - 电子尾 -> 导体
    - 导体 -> 电子头 (如果有 1 或 2 个电子头邻居)
    """
    
    EMPTY = 0
    CONDUCTOR = 1
    ELECTRON_HEAD = 2
    ELECTRON_TAIL = 3
    
    def get_neighbors(self, x: int, y: int) -> List[int]:
        """获取摩尔邻域状态。"""
        neighbors = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbors.append(self.get_cell(x + dx, y + dy))
        return neighbors
    
    def step(self) -> None:
        """执行一步演化。"""
        new_grid = [[0] * self.width for _ in range(self.height)]
        
        for y in range(self.height):
            for x in range(self.width):
                current = self._grid[y][x]
                head_neighbors = sum(1 for n in self.get_neighbors(x, y) if n == self.ELECTRON_HEAD)
                
                if current == self.EMPTY:
                    new_grid[y][x] = self.EMPTY
                elif current == self.ELECTRON_HEAD:
                    new_grid[y][x] = self.ELECTRON_TAIL
                elif current == self.ELECTRON_TAIL:
                    new_grid[y][x] = self.CONDUCTOR
                else:  # CONDUCTOR
                    if head_neighbors in (1, 2):
                        new_grid[y][x] = self.ELECTRON_HEAD
                    else:
                        new_grid[y][x] = self.CONDUCTOR
        
        self._grid = new_grid
        self.generation += 1
    
    def add_wire(self, points: List[Tuple[int, int]]) -> None:
        """
        添加导线。
        
        Args:
            points: 导线经过的点列表
        """
        for x, y in points:
            self.set_cell(x, y, self.CONDUCTOR)
    
    def add_electron(self, x: int, y: int) -> None:
        """在指定位置放置电子头。"""
        self.set_cell(x, y, self.ELECTRON_HEAD)
    
    def add_diode(self, x: int, y: int, horizontal: bool = True) -> None:
        """添加二极管（允许单向电流）。"""
        if horizontal:
            # 水平二极管
            for i in range(5):
                self.set_cell(x + i, y, self.CONDUCTOR)
            self.set_cell(x + 2, y - 1, self.CONDUCTOR)
            self.set_cell(x + 2, y + 1, self.CONDUCTOR)
        else:
            # 垂直二极管
            for i in range(5):
                self.set_cell(x, y + i, self.CONDUCTOR)
            self.set_cell(x - 1, y + 2, self.CONDUCTOR)
            self.set_cell(x + 1, y + 2, self.CONDUCTOR)
    
    def to_string(self, chars: str = ' ·●○') -> str:
        """
        将网格转换为字符串。
        
        Args:
            chars: 空/导体/电子头/电子尾对应的字符
        """
        lines = []
        for row in self._grid:
            lines.append(''.join(chars[cell] for cell in row))
        return '\n'.join(lines)


# ============================================================================
# HighLife
# ============================================================================

class HighLife(CellularAutomaton):
    """
    HighLife 元胞自动机。
    
    生命游戏的变体，增加了复制子规则。
    
    规则:
    - 活细胞周围有 2 或 3 个活邻居则存活
    - 死细胞周围有 3 或 6 个活邻居则复活
    
    特性:
    - 支持复制子 (replicator) 图案
    - 更丰富的图案多样性
    """
    
    def get_neighbors(self, x: int, y: int) -> List[int]:
        """获取摩尔邻域状态。"""
        neighbors = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbors.append(self.get_cell(x + dx, y + dy))
        return neighbors
    
    def step(self) -> None:
        """执行一步演化。"""
        new_grid = [[0] * self.width for _ in range(self.height)]
        
        for y in range(self.height):
            for x in range(self.width):
                alive_neighbors = sum(self.get_neighbors(x, y))
                current = self._grid[y][x]
                
                if current:  # 活细胞
                    if alive_neighbors in (2, 3):
                        new_grid[y][x] = 1
                else:  # 死细胞
                    if alive_neighbors in (3, 6):
                        new_grid[y][x] = 1
        
        self._grid = new_grid
        self.generation += 1
    
    def add_replicator(self, x: int = 0, y: int = 0) -> None:
        """添加复制子图案。"""
        # 简化的复制子
        pattern = [
            (1, 0, 1), (2, 0, 1), (3, 0, 1), (5, 0, 1), (6, 0, 1), (7, 0, 1),
            (0, 2, 1), (4, 2, 1), (8, 2, 1),
            (1, 3, 1), (2, 3, 1), (3, 3, 1), (5, 3, 1), (6, 3, 1), (7, 3, 1),
        ]
        self.set_pattern(pattern, (x, y))


# ============================================================================
# Seeds
# ============================================================================

class Seeds(CellularAutomaton):
    """
    Seeds 元胞自动机。
    
    规则:
    - 活细胞始终死亡
    - 死细胞周围恰好 2 个活邻居则复活
    
    产生爆炸式的混沌图案。
    """
    
    def get_neighbors(self, x: int, y: int) -> List[int]:
        """获取摩尔邻域状态。"""
        neighbors = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbors.append(self.get_cell(x + dx, y + dy))
        return neighbors
    
    def step(self) -> None:
        """执行一步演化。"""
        new_grid = [[0] * self.width for _ in range(self.height)]
        
        for y in range(self.height):
            for x in range(self.width):
                alive_neighbors = sum(self.get_neighbors(x, y))
                current = self._grid[y][x]
                
                if not current and alive_neighbors == 2:
                    new_grid[y][x] = 1
        
        self._grid = new_grid
        self.generation += 1


# ============================================================================
# Day and Night
# ============================================================================

class DayAndNight(CellularAutomaton):
    """
    Day and Night 元胞自动机。
    
    对称规则，黑白互换后仍然有效。
    
    规则:
    - 活细胞周围有 3, 4, 6, 7, 8 个活邻居则存活
    - 死细胞周围有 3, 6, 7, 8 个活邻居则复活
    """
    
    def get_neighbors(self, x: int, y: int) -> List[int]:
        """获取摩尔邻域状态。"""
        neighbors = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbors.append(self.get_cell(x + dx, y + dy))
        return neighbors
    
    def step(self) -> None:
        """执行一步演化。"""
        new_grid = [[0] * self.width for _ in range(self.height)]
        
        for y in range(self.height):
            for x in range(self.width):
                alive_neighbors = sum(self.get_neighbors(x, y))
                current = self._grid[y][x]
                
                if current:  # 活细胞
                    if alive_neighbors in (3, 4, 6, 7, 8):
                        new_grid[y][x] = 1
                else:  # 死细胞
                    if alive_neighbors in (3, 6, 7, 8):
                        new_grid[y][x] = 1
        
        self._grid = new_grid
        self.generation += 1


# ============================================================================
# 自定义规则支持
# ============================================================================

class CustomLife(CellularAutomaton):
    """
    自定义生命游戏规则。
    
    支持 B/S 记法（Birth/Survive）规则字符串。
    
    例如:
    - 生命游戏: B3/S23
    - HighLife: B36/S23
    - Seeds: B2/S
    - Day and Night: B3678/S34678
    """
    
    def __init__(self, width: int, height: int, rule: str = "B3/S23", wrap: bool = True):
        """
        初始化自定义生命游戏。
        
        Args:
            width, height: 网格尺寸
            rule: B/S 规则字符串，如 "B3/S23"
            wrap: 是否环绕边界
        """
        super().__init__(width, height, wrap)
        self.birth, self.survive = self._parse_rule(rule)
        self.rule_str = rule
    
    def _parse_rule(self, rule: str) -> Tuple[Set[int], Set[int]]:
        """解析 B/S 规则字符串。"""
        rule = rule.upper().replace(' ', '')
        birth = set()
        survive = set()
        
        parts = rule.split('/')
        for part in parts:
            if part.startswith('B'):
                birth = {int(d) for d in part[1:] if d.isdigit()}
            elif part.startswith('S'):
                survive = {int(d) for d in part[1:] if d.isdigit()}
        
        return birth, survive
    
    def get_neighbors(self, x: int, y: int) -> List[int]:
        """获取摩尔邻域状态。"""
        neighbors = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbors.append(self.get_cell(x + dx, y + dy))
        return neighbors
    
    def step(self) -> None:
        """执行一步演化。"""
        new_grid = [[0] * self.width for _ in range(self.height)]
        
        for y in range(self.height):
            for x in range(self.width):
                alive_neighbors = sum(self.get_neighbors(x, y))
                current = self._grid[y][x]
                
                if current:  # 活细胞
                    if alive_neighbors in self.survive:
                        new_grid[y][x] = 1
                else:  # 死细胞
                    if alive_neighbors in self.birth:
                        new_grid[y][x] = 1
        
        self._grid = new_grid
        self.generation += 1
    
    def set_rule(self, rule: str) -> None:
        """设置新规则。"""
        self.birth, self.survive = self._parse_rule(rule)
        self.rule_str = rule


# ============================================================================
# 工具函数
# ============================================================================

def pattern_to_coords(pattern_str: str, alive_char: str = '#') -> List[Tuple[int, int, int]]:
    """
    将图案字符串转换为坐标列表。
    
    Args:
        pattern_str: 图案字符串，使用换行分隔行
        alive_char: 表示活细胞的字符
    
    Returns:
        坐标列表 [(x, y, 1), ...]
    
    Example:
        >>> pattern = '''
        ...  # #
        ... # # #
        ...  # #
        ... '''
        >>> coords = pattern_to_coords(pattern)
    """
    coords = []
    lines = pattern_str.strip().split('\n')
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == alive_char:
                coords.append((x, y, 1))
    return coords


def rle_decode(rle: str) -> List[Tuple[int, int, int]]:
    """
    解码 RLE (Run Length Encoded) 格式的生命游戏图案。
    
    RLE 是生命游戏图案的标准格式。
    
    Args:
        rle: RLE 编码字符串
    
    Returns:
        坐标列表
    
    Example:
        >>> # Glider
        >>> coords = rle_decode("bo$2bo$3o!")
    """
    coords = []
    x, y = 0, 0
    count = ''
    
    for char in rle:
        if char.isdigit():
            count += char
        elif char == 'b':
            x += int(count) if count else 1
            count = ''
        elif char == 'o':
            repeat = int(count) if count else 1
            for _ in range(repeat):
                coords.append((x, y, 1))
                x += 1
            count = ''
        elif char == '$':
            y += int(count) if count else 1
            x = 0
            count = ''
        elif char == '!':
            break
    
    return coords


def find_oscillators(ca: CellularAutomaton, period_range: Tuple[int, int] = (2, 10),
                    max_generations: int = 100) -> List[Set[Tuple[int, int]]]:
    """
    在元胞自动机中寻找振荡器。
    
    Args:
        ca: 元胞自动机实例
        period_range: 周期范围 (min, max)
        max_generations: 最大搜索代数
    
    Returns:
        振荡器细胞集合列表
    """
    seen = {}
    oscillators = []
    
    for gen in range(max_generations):
        state = frozenset(ca.get_live_cells())
        
        if state in seen:
            period = gen - seen[state]
            if period_range[0] <= period <= period_range[1]:
                oscillators.append(state)
        
        seen[state] = gen
        ca.step()
    
    return oscillators


def detect_still_life(ca: CellularAutomaton, check_generations: int = 5) -> bool:
    """
    检测图案是否为静止状态（不再变化）。
    
    Args:
        ca: 元胞自动机实例
        check_generations: 检查的代数
    
    Returns:
        是否为静止状态
    """
    initial = tuple(tuple(row) for row in ca.get_grid())
    
    for _ in range(check_generations):
        ca.step()
        if tuple(tuple(row) for row in ca.get_grid()) == initial:
            continue
        else:
            return False
    
    return True


def compare_patterns(pattern1: Set[Tuple[int, int]], 
                    pattern2: Set[Tuple[int, int]]) -> Tuple[int, int, int]:
    """
    比较两个图案的相似度。
    
    Returns:
        (共同细胞数, 仅在 pattern1, 仅在 pattern2)
    """
    common = len(pattern1 & pattern2)
    only_1 = len(pattern1 - pattern2)
    only_2 = len(pattern2 - pattern1)
    return common, only_1, only_2


# 导出公共接口
__all__ = [
    # 基类
    'CellularAutomaton',
    
    # 生命游戏变体
    'GameOfLife',
    'HighLife',
    'Seeds',
    'DayAndNight',
    'CustomLife',
    
    # 一维元胞自动机
    'ElementaryCA',
    
    # 蚂蚁
    'LangtonsAnt',
    'MultiColorAnt',
    
    # 多态元胞自动机
    'BriansBrain',
    'Wireworld',
    
    # 工具函数
    'pattern_to_coords',
    'rle_decode',
    'find_oscillators',
    'detect_still_life',
    'compare_patterns',
]