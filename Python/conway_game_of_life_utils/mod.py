"""
Conway's Game of Life - 康威生命游戏工具集

一个完整的细胞自动机模拟器，支持多种规则、模式导入、演化控制等功能。

功能:
- 基本生命游戏模拟 (B3/S23 规则)
- 支持多种规则变体 (HighLife, Day & Night, Seeds 等)
- 内置经典模式 (滑翔机、枪、振荡器等)
- RLE 格式模式导入/导出
- 无限网格扩展
- 代数统计和可视化
"""

import copy
from typing import List, Tuple, Set, Optional, Dict, Any
from enum import Enum


class Rule:
    """生命游戏规则"""
    
    def __init__(self, birth: Set[int], survival: Set[int], name: str = "Custom"):
        """
        初始化规则
        
        Args:
            birth: 出生条件 - 邻居数量集合
            survival: 存活条件 - 邻居数量集合
            name: 规则名称
        """
        self.birth = birth
        self.survival = survival
        self.name = name
    
    @classmethod
    def from_string(cls, rule_str: str, name: str = "Custom") -> 'Rule':
        """
        从规则字符串创建规则
        
        支持格式:
        - "B3/S23" - 标准格式
        - "3/23" - 简化格式
        - "23/3" - Golly 格式（存活/出生）
        
        Args:
            rule_str: 规则字符串
            name: 规则名称
            
        Returns:
            Rule 对象
        """
        rule_str = rule_str.upper().replace(' ', '')
        
        if rule_str.startswith('B'):
            # B3/S23 格式
            parts = rule_str.split('/')
            birth = set(int(d) for d in parts[0][1:])
            survival = set(int(d) for d in parts[1][1:])
        elif '/' in rule_str:
            parts = rule_str.split('/')
            if len(parts[0]) <= len(parts[1]):
                # 3/23 格式 (出生/存活)
                birth = set(int(d) for d in parts[0])
                survival = set(int(d) for d in parts[1])
            else:
                # 23/3 格式 (存活/出生) - Golly 格式
                survival = set(int(d) for d in parts[0])
                birth = set(int(d) for d in parts[1])
        else:
            raise ValueError(f"Invalid rule format: {rule_str}")
        
        return cls(birth, survival, name)
    
    def __str__(self) -> str:
        """返回规则字符串表示"""
        birth_str = ''.join(str(d) for d in sorted(self.birth))
        survival_str = ''.join(str(d) for d in sorted(self.survival))
        return f"B{birth_str}/S{survival_str}"
    
    def __repr__(self) -> str:
        return f"Rule({self.birth}, {self.survival}, '{self.name}')"


# 预定义规则
RULES = {
    'conway': Rule({3}, {2, 3}, "Conway's Life"),
    'highlife': Rule({3, 6}, {2, 3}, "HighLife"),
    'day_and_night': Rule({3, 6, 7, 8}, {3, 4, 6, 7, 8}, "Day & Night"),
    'seeds': Rule({2}, set(), "Seeds"),
    'life_without_death': Rule({3}, {0, 1, 2, 3, 4, 5, 6, 7, 8}, "Life without Death"),
    'maze': Rule({3}, {1, 2, 3, 4, 5}, "Maze"),
    'diamoeba': Rule({3, 5, 6, 7, 8}, {5, 6, 7, 8}, "Diamoeba"),
    'anneal': Rule({3, 5, 6, 7, 8}, {4, 6, 7, 8}, "Anneal"),
    'twoxtwo': Rule({3, 6}, {1, 2, 5}, "2x2"),
    'live_free_or_die': Rule({3}, {0, 1, 2, 3, 4, 5, 6, 7, 8}, "Live Free or Die"),
    'gnarl': Rule({1}, {1}, "Gnarl"),
    'replicator': Rule({1, 3, 5, 7}, {1, 3, 5, 7}, "Replicator"),
    'plow_world': Rule({3}, {1, 2, 3, 4, 5, 6}, "Plow World"),
    'serviettes': Rule({2, 3, 4}, set(), "Serviettes"),
}


class Pattern:
    """预定义模式"""
    
    # 仍然生命体
    BLOCK = [(0, 0), (0, 1), (1, 0), (1, 1)]
    BEEHIVE = [(0, 1), (0, 2), (1, 0), (1, 3), (2, 1), (2, 2)]
    LOAF = [(0, 1), (0, 2), (1, 0), (1, 3), (2, 1), (2, 3), (3, 2)]
    BOAT = [(0, 0), (0, 1), (1, 0), (1, 2), (2, 1)]
    TUB = [(0, 1), (1, 0), (1, 2), (2, 1)]
    
    # 振荡器
    BLINKER = [(0, 0), (0, 1), (0, 2)]
    TOAD = [(0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2)]
    BEACON = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 2), (2, 3), (3, 2), (3, 3)]
    PULSAR = [
        (0, 2), (0, 3), (0, 4), (0, 8), (0, 9), (0, 10),
        (2, 0), (2, 5), (2, 7), (2, 12),
        (3, 0), (3, 5), (3, 7), (3, 12),
        (4, 0), (4, 5), (4, 7), (4, 12),
        (5, 2), (5, 3), (5, 4), (5, 8), (5, 9), (5, 10),
        (7, 2), (7, 3), (7, 4), (7, 8), (7, 9), (7, 10),
        (8, 0), (8, 5), (8, 7), (8, 12),
        (9, 0), (9, 5), (9, 7), (9, 12),
        (10, 0), (10, 5), (10, 7), (10, 12),
        (12, 2), (12, 3), (12, 4), (12, 8), (12, 9), (12, 10),
    ]
    PENTADecathlon = [
        (0, 1), (1, 1), (2, 0), (2, 2), (3, 1), (4, 1), (5, 1), (6, 1), (7, 0), (7, 2), (8, 1), (9, 1)
    ]
    
    # 太空船
    GLIDER = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    LWSS = [(0, 1), (0, 4), (1, 0), (2, 0), (2, 4), (3, 0), (3, 1), (3, 2), (3, 3)]
    MWSS = [(0, 2), (1, 0), (1, 4), (2, 5), (3, 0), (3, 5), (4, 1), (4, 2), (4, 3), (4, 4)]
    HWSS = [(0, 2), (0, 3), (1, 0), (1, 5), (2, 6), (3, 0), (3, 6), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5)]
    
    # 枪
    GLIDER_GUN = [
        (0, 24),
        (1, 22), (1, 24),
        (2, 12), (2, 13), (2, 20), (2, 21), (2, 34), (2, 35),
        (3, 11), (3, 15), (3, 20), (3, 21), (3, 34), (3, 35),
        (4, 0), (4, 1), (4, 10), (4, 16), (4, 20), (4, 21),
        (5, 0), (5, 1), (5, 10), (5, 14), (5, 16), (5, 17), (5, 22), (5, 24),
        (6, 10), (6, 16), (6, 24),
        (7, 11), (7, 15),
        (8, 12), (8, 13),
    ]
    
    # 其他有趣模式
    R_PENTOMINO = [(0, 1), (0, 2), (1, 0), (1, 1), (2, 1)]
    DIEHARD = [(0, 6), (1, 0), (1, 1), (2, 1), (2, 5), (2, 6), (2, 7)]
    ACORN = [(0, 1), (1, 3), (2, 0), (2, 1), (2, 4), (2, 5), (2, 6)]
    INFINITE_GROWTH_1 = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), 
                         (0, 9), (0, 10), (0, 11), (0, 12), (0, 13),
                         (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 8),
                         (2, 9), (2, 11), (2, 12), (2, 13)]
    
    @classmethod
    def get(cls, name: str) -> List[Tuple[int, int]]:
        """根据名称获取模式"""
        patterns = {
            'block': cls.BLOCK,
            'beehive': cls.BEEHIVE,
            'loaf': cls.LOAF,
            'boat': cls.BOAT,
            'tub': cls.TUB,
            'blinker': cls.BLINKER,
            'toad': cls.TOAD,
            'beacon': cls.BEACON,
            'pulsar': cls.PULSAR,
            'pentadecathlon': cls.PENTADecathlon,
            'glider': cls.GLIDER,
            'lwss': cls.LWSS,
            'mwss': cls.MWSS,
            'hwss': cls.HWSS,
            'glider_gun': cls.GLIDER_GUN,
            'r_pentomino': cls.R_PENTOMINO,
            'diehard': cls.DIEHARD,
            'acorn': cls.ACORN,
            'infinite_growth': cls.INFINITE_GROWTH_1,
        }
        
        if name.lower() not in patterns:
            raise KeyError(f"Unknown pattern: {name}. Available: {list(patterns.keys())}")
        
        return patterns[name.lower()]


class GameOfLife:
    """
    康威生命游戏模拟器
    
    支持无限网格、多种规则、模式导入导出等功能。
    """
    
    def __init__(self, rule: Optional[Rule] = None, width: int = 100, height: int = 100):
        """
        初始化游戏
        
        Args:
            rule: 游戏规则，默认为康威规则
            width: 网格宽度（用于边界模式）
            height: 网格高度（用于边界模式）
        """
        self.rule = rule or RULES['conway']
        self.width = width
        self.height = height
        self.cells: Set[Tuple[int, int]] = set()
        self.generation = 0
        self.wrap_edges = False  # 边界环绕模式
    
    def set_cell(self, x: int, y: int, alive: bool = True) -> None:
        """设置单元格状态"""
        if alive:
            self.cells.add((x, y))
        else:
            self.cells.discard((x, y))
    
    def toggle_cell(self, x: int, y: int) -> bool:
        """切换单元格状态，返回新状态"""
        if (x, y) in self.cells:
            self.cells.discard((x, y))
            return False
        else:
            self.cells.add((x, y))
            return True
    
    def get_cell(self, x: int, y: int) -> bool:
        """获取单元格状态"""
        return (x, y) in self.cells
    
    def clear(self) -> None:
        """清空网格"""
        self.cells.clear()
        self.generation = 0
    
    def load_pattern(self, pattern: List[Tuple[int, int]], offset: Tuple[int, int] = (0, 0)) -> None:
        """
        加载模式
        
        Args:
            pattern: 活细胞坐标列表
            offset: 偏移量 (x, y)
        """
        ox, oy = offset
        for x, y in pattern:
            self.cells.add((x + ox, y + oy))
    
    def load_pattern_by_name(self, name: str, offset: Tuple[int, int] = (0, 0)) -> None:
        """根据名称加载内置模式"""
        pattern = Pattern.get(name)
        self.load_pattern(pattern, offset)
    
    def load_rle(self, rle: str, offset: Tuple[int, int] = (0, 0)) -> None:
        """
        从 RLE 格式加载模式
        
        RLE (Run Length Encoded) 格式示例:
        #C Name: Glider
        #C Author: Richard K. Guy
        x = 3, y = 3, rule = B3/S23
        bo$2bo$3o!
        
        Args:
            rle: RLE 格式字符串
            offset: 偏移量
        """
        lines = rle.strip().split('\n')
        ox, oy = offset
        
        # 解析头部
        x_size, y_size = 0, 0
        pattern_lines = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                continue
            if line.startswith('x'):
                # 解析尺寸和规则
                parts = line.split(',')
                for part in parts:
                    part = part.strip()
                    if part.startswith('x'):
                        x_size = int(part.split('=')[1].strip())
                    elif part.startswith('y'):
                        y_size = int(part.split('=')[1].strip())
                    elif 'rule' in part.lower():
                        # 解析规则
                        rule_str = part.split('=')[1].strip()
                        try:
                            self.rule = Rule.from_string(rule_str)
                        except:
                            pass
            else:
                pattern_lines.append(line)
        
        # 解析模式
        rle_data = ''.join(pattern_lines)
        x, y = 0, 0
        run = 0
        
        for char in rle_data:
            if char.isdigit():
                run = run * 10 + int(char)
            elif char == 'b' or char == '.':
                # 死细胞
                run = max(1, run)
                x += run
                run = 0
            elif char == 'o' or char == '*':
                # 活细胞
                run = max(1, run)
                for _ in range(run):
                    self.cells.add((x + ox, y + oy))
                    x += 1
                run = 0
            elif char == '$':
                # 换行
                run = max(1, run)
                y += run
                x = 0
                run = 0
            elif char == '!':
                # 结束
                break
    
    def to_rle(self) -> str:
        """
        将当前状态导出为 RLE 格式
        
        Returns:
            RLE 格式字符串
        """
        if not self.cells:
            return "x = 0, y = 0, rule = " + str(self.rule) + "\n!"
        
        # 找到边界
        min_x = min(c[0] for c in self.cells)
        max_x = max(c[0] for c in self.cells)
        min_y = min(c[1] for c in self.cells)
        max_y = max(c[1] for c in self.cells)
        
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        
        lines = [f"#C Generated by Conway's Game of Life Utils",
                 f"x = {width}, y = {height}, rule = {self.rule}"]
        
        # 创建网格
        grid = set((c[0] - min_x, c[1] - min_y) for c in self.cells)
        
        rle_rows = []
        for y in range(height):
            row = []
            run = 0
            last_char = None
            
            for x in range(width):
                char = 'o' if (x, y) in grid else 'b'
                
                if char == last_char:
                    run += 1
                else:
                    if last_char is not None:
                        if run > 1:
                            row.append(f"{run}{last_char}")
                        else:
                            row.append(last_char)
                    last_char = char
                    run = 1
            
            # 添加最后的运行
            if last_char == 'o':
                if run > 1:
                    row.append(f"{run}{last_char}")
                else:
                    row.append(last_char)
            
            rle_rows.append(''.join(row))
        
        lines.append('$'.join(rle_rows) + '!')
        
        return '\n'.join(lines)
    
    def get_neighbors(self, x: int, y: int) -> int:
        """获取活邻居数量"""
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                
                nx, ny = x + dx, y + dy
                
                if self.wrap_edges:
                    nx = nx % self.width
                    ny = ny % self.height
                
                if (nx, ny) in self.cells:
                    count += 1
        
        return count
    
    def step(self, generations: int = 1) -> None:
        """
        演化指定代数
        
        Args:
            generations: 演化代数
        """
        for _ in range(generations):
            self._single_step()
    
    def _single_step(self) -> None:
        """单步演化"""
        new_cells: Set[Tuple[int, int]] = set()
        
        # 获取所有需要检查的单元格（活细胞及其邻居）
        candidates: Set[Tuple[int, int]] = set()
        for x, y in self.cells:
            candidates.add((x, y))
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    candidates.add((x + dx, y + dy))
        
        # 应用规则
        for x, y in candidates:
            neighbors = self.get_neighbors(x, y)
            
            if (x, y) in self.cells:
                # 存活规则
                if neighbors in self.rule.survival:
                    new_cells.add((x, y))
            else:
                # 出生规则
                if neighbors in self.rule.birth:
                    new_cells.add((x, y))
        
        self.cells = new_cells
        self.generation += 1
    
    def get_bounds(self) -> Tuple[int, int, int, int]:
        """
        获取活细胞边界
        
        Returns:
            (min_x, max_x, min_y, max_y)
        """
        if not self.cells:
            return (0, 0, 0, 0)
        
        min_x = min(c[0] for c in self.cells)
        max_x = max(c[0] for c in self.cells)
        min_y = min(c[1] for c in self.cells)
        max_y = max(c[1] for c in self.cells)
        
        return (min_x, max_x, min_y, max_y)
    
    def get_grid(self, padding: int = 0) -> List[List[bool]]:
        """
        获取网格表示
        
        Args:
            padding: 边界周围额外的空行/列
            
        Returns:
            二维布尔数组
        """
        if not self.cells:
            return [[False]]
        
        min_x, max_x, min_y, max_y = self.get_bounds()
        
        min_x -= padding
        max_x += padding
        min_y -= padding
        max_y += padding
        
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        
        grid = [[False] * width for _ in range(height)]
        
        for x, y in self.cells:
            grid_x = x - min_x
            grid_y = y - min_y
            if 0 <= grid_x < width and 0 <= grid_y < height:
                grid[grid_y][grid_x] = True
        
        return grid
    
    def to_string(self, alive: str = '█', dead: str = ' ', padding: int = 0) -> str:
        """
        将当前状态转换为字符串表示
        
        Args:
            alive: 活细胞字符
            dead: 死细胞字符
            padding: 边界周围额外的空行/列
            
        Returns:
            网格的字符串表示
        """
        grid = self.get_grid(padding)
        
        lines = []
        for row in grid:
            lines.append(''.join(alive if cell else dead for cell in row))
        
        return '\n'.join(lines)
    
    def count_cells(self) -> int:
        """获取活细胞数量"""
        return len(self.cells)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取统计信息
        
        Returns:
            统计字典
        """
        if not self.cells:
            return {
                'cells': 0,
                'generation': self.generation,
                'bounds': (0, 0, 0, 0),
                'width': 0,
                'height': 0,
                'density': 0,
                'rule': str(self.rule),
            }
        
        min_x, max_x, min_y, max_y = self.get_bounds()
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        area = width * height
        
        return {
            'cells': len(self.cells),
            'generation': self.generation,
            'bounds': (min_x, max_x, min_y, max_y),
            'width': width,
            'height': height,
            'density': len(self.cells) / area if area > 0 else 0,
            'rule': str(self.rule),
        }
    
    def copy(self) -> 'GameOfLife':
        """创建游戏副本"""
        new_game = GameOfLife(self.rule, self.width, self.height)
        new_game.cells = self.cells.copy()
        new_game.generation = self.generation
        new_game.wrap_edges = self.wrap_edges
        return new_game
    
    def __len__(self) -> int:
        return len(self.cells)
    
    def __repr__(self) -> str:
        return f"GameOfLife(rule={self.rule}, cells={len(self.cells)}, gen={self.generation})"


def run_simulation(pattern: List[Tuple[int, int]], 
                   generations: int = 100,
                   rule: Optional[Rule] = None,
                   stop_if_stable: bool = True) -> Dict[str, Any]:
    """
    运行模拟
    
    Args:
        pattern: 初始模式
        generations: 最大代数
        rule: 游戏规则
        stop_if_stable: 如果稳定则停止
        
    Returns:
        模拟结果字典
    """
    game = GameOfLife(rule)
    game.load_pattern(pattern)
    
    history: List[Set[Tuple[int, int]]] = []
    oscillation_period = 0
    
    for gen in range(generations):
        cells_before = game.cells.copy()
        history.append(cells_before)
        
        game.step()
        
        if stop_if_stable:
            # 检查是否稳定
            if game.cells == cells_before:
                # 静止生命
                return {
                    'stable': True,
                    'still_life': True,
                    'final_cells': len(game.cells),
                    'generations': gen + 1,
                    'oscillation_period': 1,
                    'history': history,
                }
            
            # 检查振荡
            for i, past in enumerate(history[:-1]):
                if game.cells == past:
                    oscillation_period = len(history) - i
                    return {
                        'stable': True,
                        'still_life': False,
                        'final_cells': len(game.cells),
                        'generations': gen + 1,
                        'oscillation_period': oscillation_period,
                        'history': history,
                    }
    
    return {
        'stable': False,
        'still_life': False,
        'final_cells': len(game.cells),
        'generations': generations,
        'oscillation_period': 0,
        'history': history,
    }


def detect_pattern_type(cells: Set[Tuple[int, int]], 
                        max_generations: int = 4) -> str:
    """
    检测模式类型
    
    Args:
        cells: 活细胞集合
        max_generations: 检测代数
        
    Returns:
        模式类型描述
    """
    if not cells:
        return "Empty"
    
    game = GameOfLife()
    game.cells = cells.copy()
    
    initial = cells.copy()
    history = [initial]
    
    for gen in range(max_generations):
        game.step()
        current = game.cells.copy()
        
        # 首先检查是否是静止生命（与上一代完全相同）
        if current == history[-1]:
            return "Still Life"
        
        # 检查是否回到初始状态（振荡器）
        if current == initial:
            period = gen + 1
            return f"Oscillator (period {period})"
        
        # 检查是否匹配历史中的某个状态
        for i, past in enumerate(history[:-1]):
            if current == past:
                period = len(history) - i
                return f"Oscillator (period {period})"
        
        history.append(current)
    
    # 检查是否移动
    if len(game.cells) == len(initial):
        # 可能是太空船
        min_x = min(c[0] for c in initial)
        min_y = min(c[1] for c in initial)
        new_min_x = min(c[0] for c in game.cells)
        new_min_y = min(c[1] for c in game.cells)
        
        dx = new_min_x - min_x
        dy = new_min_y - min_y
        
        # 归一化位置比较
        normalized_initial = set((x - min_x, y - min_y) for x, y in initial)
        normalized_current = set((x - new_min_x, y - new_min_y) for x, y in game.cells)
        
        if normalized_initial == normalized_current:
            return f"Spaceship (moved {dx}, {dy})"
    
    return "Pattern (evolving)"


def pattern_to_ascii(pattern: List[Tuple[int, int]], 
                      alive: str = '■', 
                      dead: str = '·') -> str:
    """
    将模式转换为 ASCII 艺术
    
    Args:
        pattern: 活细胞坐标列表
        alive: 活细胞字符
        dead: 死细胞字符
        
    Returns:
        ASCII 字符串
    """
    if not pattern:
        return ""
    
    min_x = min(c[0] for c in pattern)
    max_x = max(c[0] for c in pattern)
    min_y = min(c[1] for c in pattern)
    max_y = max(c[1] for c in pattern)
    
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    
    grid = [[dead] * width for _ in range(height)]
    
    for x, y in pattern:
        grid[y - min_y][x - min_x] = alive
    
    return '\n'.join(''.join(row) for row in grid)


def generate_random_pattern(density: float = 0.3, 
                           width: int = 20, 
                           height: int = 20,
                           seed: Optional[int] = None) -> List[Tuple[int, int]]:
    """
    生成随机模式
    
    Args:
        density: 活细胞密度 (0-1)
        width: 宽度
        height: 高度
        seed: 随机种子
        
    Returns:
        活细胞坐标列表
    """
    import random
    if seed is not None:
        random.seed(seed)
    
    cells = []
    for y in range(height):
        for x in range(width):
            if random.random() < density:
                cells.append((x, y))
    
    return cells


def compare_patterns(pattern1: Set[Tuple[int, int]], 
                     pattern2: Set[Tuple[int, int]]) -> Dict[str, Any]:
    """
    比较两个模式
    
    Args:
        pattern1: 第一个模式
        pattern2: 第二个模式
        
    Returns:
        比较结果字典
    """
    intersection = pattern1 & pattern2
    only_in_1 = pattern1 - pattern2
    only_in_2 = pattern2 - pattern1
    
    similarity = len(intersection) / max(len(pattern1), len(pattern2), 1)
    
    return {
        'cells_in_common': len(intersection),
        'only_in_first': len(only_in_1),
        'only_in_second': len(only_in_2),
        'similarity': similarity,
        'identical': pattern1 == pattern2,
    }