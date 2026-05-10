"""
Hexagonal Grid Utilities - 六边形网格工具

功能:
- 六边形坐标系统 (轴向坐标、立方体坐标、偏移坐标)
- 坐标系统互相转换
- 六边形邻居计算
- 距离计算 (曼哈顿距离)
- 路径查找 (A* 算法)
- 视野计算 (FOV)
- 六边形区域生成 (圆环、扇形、直线)
- 像素坐标转换
- 六边形网格可视化 (ASCII 和文本)

零外部依赖，纯 Python 实现。
"""

import math
from typing import List, Tuple, Dict, Set, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum
from collections import deque
import heapq


class HexOrientation(Enum):
    """六边形朝向"""
    POINTY_TOP = "pointy"  # 尖顶朝上
    FLAT_TOP = "flat"      # 平顶朝上


class OffsetCoordType(Enum):
    """偏移坐标类型"""
    EVEN = "even"
    ODD = "odd"


@dataclass(frozen=True)
class Hex:
    """六边形立方体坐标 (axial 投影)"""
    q: int  # 列
    r: int  # 行
    
    @property
    def s(self) -> int:
        """立方体坐标的第三个分量"""
        return -self.q - self.r
    
    def __add__(self, other: 'Hex') -> 'Hex':
        return Hex(self.q + other.q, self.r + other.r)
    
    def __sub__(self, other: 'Hex') -> 'Hex':
        return Hex(self.q - other.q, self.r - other.r)
    
    def __mul__(self, scalar: int) -> 'Hex':
        return Hex(self.q * scalar, self.r * scalar)
    
    def __neg__(self) -> 'Hex':
        return Hex(-self.q, -self.r)
    
    def __lt__(self, other: 'Hex') -> bool:
        """用于 heapq 排序"""
        return (self.q, self.r) < (other.q, other.r)
    
    def __le__(self, other: 'Hex') -> bool:
        return (self.q, self.r) <= (other.q, other.r)
    
    def __gt__(self, other: 'Hex') -> bool:
        return (self.q, self.r) > (other.q, other.r)
    
    def __ge__(self, other: 'Hex') -> bool:
        return (self.q, self.r) >= (other.q, other.r)
    
    def __repr__(self) -> str:
        return f"Hex({self.q}, {self.r})"
    
    def to_tuple(self) -> Tuple[int, int]:
        return (self.q, self.r)
    
    def to_cube(self) -> Tuple[int, int, int]:
        """转换为立方体坐标 (x, y, z)"""
        return (self.q, self.r, self.s)
    
    @classmethod
    def from_cube(cls, x: int, y: int, z: int) -> 'Hex':
        """从立方体坐标创建"""
        if x + y + z != 0:
            raise ValueError(f"Invalid cube coordinates: x + y + z must be 0, got {x + y + z}")
        return cls(x, y)


# ==================== 方向定义 ====================

# 尖顶六边形方向 (POINTY_TOP)
POINTY_DIRECTIONS = [
    Hex(1, 0),   # 右上
    Hex(1, -1),  # 右
    Hex(0, -1),  # 左
    Hex(-1, 0),  # 左下
    Hex(-1, 1),  # 右下
    Hex(0, 1),   # 下
]

# 平顶六边形方向 (FLAT_TOP)
FLAT_DIRECTIONS = [
    Hex(1, -1),  # 右上
    Hex(1, 0),   # 右
    Hex(0, 1),   # 右下
    Hex(-1, 1),  # 左下
    Hex(-1, 0),  # 左
    Hex(0, -1),  # 左上
]

# 方向名称
DIRECTION_NAMES = {
    0: "E",   # 东/右上
    1: "NE",  # 东北/右
    2: "NW",  # 西北/左
    3: "W",   # 西/左下
    4: "SW",  # 西南/右下
    5: "SE",  # 东南/下
}


# ==================== 基础函数 ====================

def hex_add(a: Hex, b: Hex) -> Hex:
    """六边形相加"""
    return a + b


def hex_subtract(a: Hex, b: Hex) -> Hex:
    """六边形相减"""
    return a - b


def hex_scale(h: Hex, scalar: int) -> Hex:
    """六边形缩放"""
    return h * scalar


def hex_direction(orientation: HexOrientation, direction: int) -> Hex:
    """获取指定方向的六边形
    
    Args:
        orientation: 六边形朝向
        direction: 方向索引 (0-5)
    
    Returns:
        该方向的六边形
    """
    directions = POINTY_DIRECTIONS if orientation == HexOrientation.POINTY_TOP else FLAT_DIRECTIONS
    return directions[direction % 6]


def hex_neighbor(h: Hex, orientation: HexOrientation, direction: int) -> Hex:
    """获取相邻六边形
    
    Args:
        h: 当前六边形
        orientation: 六边形朝向
        direction: 方向索引 (0-5)
    
    Returns:
        相邻的六边形
    """
    return h + hex_direction(orientation, direction)


def hex_neighbors(h: Hex, orientation: HexOrientation = HexOrientation.POINTY_TOP) -> List[Hex]:
    """获取所有相邻六边形
    
    Args:
        h: 当前六边形
        orientation: 六边形朝向
    
    Returns:
        6个相邻六边形列表
    """
    directions = POINTY_DIRECTIONS if orientation == HexOrientation.POINTY_TOP else FLAT_DIRECTIONS
    return [h + d for d in directions]


def hex_diagonal_neighbors(h: Hex, orientation: HexOrientation = HexOrientation.POINTY_TOP) -> List[Hex]:
    """获取对角相邻六边形 (间隔一格)
    
    Args:
        h: 当前六边形
        orientation: 六边形朝向
    
    Returns:
        6个对角相邻六边形列表
    """
    if orientation == HexOrientation.POINTY_TOP:
        diagonals = [
            Hex(2, -1), Hex(1, -2), Hex(-1, -1),
            Hex(-2, 1), Hex(-1, 2), Hex(1, 1)
        ]
    else:
        diagonals = [
            Hex(2, -2), Hex(2, 0), Hex(0, 2),
            Hex(-2, 2), Hex(-2, 0), Hex(0, -2)
        ]
    return [h + d for d in diagonals]


# ==================== 距离计算 ====================

def hex_distance(a: Hex, b: Hex) -> int:
    """计算两个六边形之间的曼哈顿距离
    
    Args:
        a: 起点六边形
        b: 终点六边形
    
    Returns:
        距离 (整数)
    """
    return (abs(a.q - b.q) + abs(a.r - b.r) + abs(a.s - b.s)) // 2


def hex_distance_chebyshev(a: Hex, b: Hex) -> int:
    """切比雪夫距离 (六边形网格中的最大坐标差)"""
    return max(abs(a.q - b.q), abs(a.r - b.r), abs(a.s - b.s))


# ==================== 区域生成 ====================

def hex_range(center: Hex, radius: int) -> List[Hex]:
    """生成以中心为圆心的圆形区域
    
    Args:
        center: 中心六边形
        radius: 半径
    
    Returns:
        区域内所有六边形列表
    """
    results = []
    for q in range(-radius, radius + 1):
        for r in range(max(-radius, -q - radius), min(radius, -q + radius) + 1):
            results.append(center + Hex(q, r))
    return results


def hex_ring(center: Hex, radius: int) -> List[Hex]:
    """生成圆环
    
    Args:
        center: 中心六边形
        radius: 半径 (圆环到中心的距离)
    
    Returns:
        圆环上的六边形列表 (不包含中心，除非 radius=0)
    """
    if radius <= 0:
        return [center]
    
    results = []
    # 简单方法: 找所有距离中心恰好为 radius 的六边形
    # 使用标准的立方体坐标遍历
    for q in range(-radius, radius + 1):
        r_min = max(-radius, -q - radius)
        r_max = min(radius, -q + radius)
        for r in range(r_min, r_max + 1):
            h = Hex(center.q + q, center.r + r)
            if hex_distance(center, h) == radius:
                results.append(h)
    
    return results


def hex_spiral(center: Hex, radius: int) -> List[Hex]:
    """生成螺旋形区域
    
    Args:
        center: 中心六边形
        radius: 最大半径
    
    Returns:
        从中心向外螺旋排列的六边形列表
    """
    results = [center]
    for r in range(1, radius + 1):
        results.extend(hex_ring(center, r))
    return results


def hex_line(a: Hex, b: Hex) -> List[Hex]:
    """生成两点之间的直线
    
    使用线性插值算法
    
    Args:
        a: 起点
        b: 终点
    
    Returns:
        直线上的六边形列表
    """
    distance = hex_distance(a, b)
    if distance == 0:
        return [a]
    
    results = []
    for i in range(distance + 1):
        t = i / distance
        # 线性插值
        q = round(a.q + (b.q - a.q) * t)
        r = round(a.r + (b.r - a.r) * t)
        results.append(Hex(q, r))
    
    return results


def hex_triangle(size: int) -> List[Hex]:
    """生成三角形区域
    
    Args:
        size: 三角形大小
    
    Returns:
        三角形区域内的六边形列表
    """
    results = []
    for q in range(size):
        for r in range(size - q):
            results.append(Hex(q, r))
    return results


def hex_parallelogram(q1: int, q2: int, r1: int, r2: int) -> List[Hex]:
    """生成平行四边形区域
    
    Args:
        q1, q2: q 坐标范围
        r1, r2: r 坐标范围
    
    Returns:
        平行四边形区域内的六边形列表
    """
    results = []
    for q in range(q1, q2 + 1):
        for r in range(r1, r2 + 1):
            results.append(Hex(q, r))
    return results


def hex_hexagon(radius: int) -> List[Hex]:
    """生成六边形形状的区域
    
    Args:
        radius: 半径 (从中心到边缘)
    
    Returns:
        六边形区域内的六边形列表
    """
    return hex_range(Hex(0, 0), radius)


def hex_rectangle(width: int, height: int, orientation: HexOrientation = HexOrientation.POINTY_TOP) -> List[Hex]:
    """生成矩形区域 (使用偏移坐标)
    
    Args:
        width: 宽度
        height: 高度
        orientation: 六边形朝向
    
    Returns:
        矩形区域内的六边形列表
    """
    results = []
    for r in range(height):
        r_offset = r // 2
        for q in range(-r_offset, width - r_offset):
            results.append(Hex(q, r))
    return results


# ==================== 旋转和镜像 ====================

def hex_rotate_right(h: Hex) -> Hex:
    """顺时针旋转60度"""
    return Hex(-h.r, -h.s)


def hex_rotate_left(h: Hex) -> Hex:
    """逆时针旋转60度"""
    return Hex(-h.s, -h.q)


def hex_rotate_180(h: Hex) -> Hex:
    """旋转180度"""
    return Hex(-h.q, -h.r)


def hex_reflect_q(h: Hex) -> Hex:
    """沿 Q 轴镜像"""
    return Hex(h.q, h.s)


def hex_reflect_r(h: Hex) -> Hex:
    """沿 R 轴镜像"""
    return Hex(h.s, h.r)


def hex_reflect_s(h: Hex) -> Hex:
    """沿 S 轴镜像"""
    return Hex(h.r, h.q)


# ==================== 坐标转换 ====================

def hex_to_offset(h: Hex, coord_type: OffsetCoordType, orientation: HexOrientation) -> Tuple[int, int]:
    """轴向坐标转偏移坐标
    
    Args:
        h: 六边形坐标
        coord_type: 偏移类型 (偶数/奇数)
        orientation: 六边形朝向
    
    Returns:
        (col, row) 偏移坐标
    """
    if orientation == HexOrientation.POINTY_TOP:
        if coord_type == OffsetCoordType.ODD:
            col = h.q + (h.r - (h.r & 1)) // 2
            row = h.r
        else:  # EVEN
            col = h.q + (h.r + (h.r & 1)) // 2
            row = h.r
    else:  # FLAT_TOP
        if coord_type == OffsetCoordType.ODD:
            col = h.q
            row = h.r + (h.q - (h.q & 1)) // 2
        else:  # EVEN
            col = h.q
            row = h.r + (h.q + (h.q & 1)) // 2
    
    return (col, row)


def offset_to_hex(col: int, row: int, coord_type: OffsetCoordType, orientation: HexOrientation) -> Hex:
    """偏移坐标转轴向坐标
    
    Args:
        col, row: 偏移坐标
        coord_type: 偏移类型 (偶数/奇数)
        orientation: 六边形朝向
    
    Returns:
        六边形坐标
    """
    if orientation == HexOrientation.POINTY_TOP:
        if coord_type == OffsetCoordType.ODD:
            q = col - (row - (row & 1)) // 2
            r = row
        else:  # EVEN
            q = col - (row + (row & 1)) // 2
            r = row
    else:  # FLAT_TOP
        if coord_type == OffsetCoordType.ODD:
            q = col
            r = row - (col - (col & 1)) // 2
        else:  # EVEN
            q = col
            r = row - (col + (col & 1)) // 2
    
    return Hex(q, r)


def hex_to_pixel(h: Hex, size: float, orientation: HexOrientation = HexOrientation.POINTY_TOP,
                 origin: Tuple[float, float] = (0, 0)) -> Tuple[float, float]:
    """六边形坐标转像素坐标
    
    Args:
        h: 六边形坐标
        size: 六边形大小 (外接圆半径)
        orientation: 六边形朝向
        origin: 原点位置
    
    Returns:
        (x, y) 像素坐标
    """
    if orientation == HexOrientation.POINTY_TOP:
        x = size * (math.sqrt(3) * h.q + math.sqrt(3) / 2 * h.r)
        y = size * (3 / 2 * h.r)
    else:  # FLAT_TOP
        x = size * (3 / 2 * h.q)
        y = size * (math.sqrt(3) / 2 * h.q + math.sqrt(3) * h.r)
    
    return (x + origin[0], y + origin[1])


def pixel_to_hex(x: float, y: float, size: float, orientation: HexOrientation = HexOrientation.POINTY_TOP,
                 origin: Tuple[float, float] = (0, 0)) -> Hex:
    """像素坐标转六边形坐标
    
    Args:
        x, y: 像素坐标
        size: 六边形大小 (外接圆半径)
        orientation: 六边形朝向
        origin: 原点位置
    
    Returns:
        六边形坐标
    """
    x = x - origin[0]
    y = y - origin[1]
    
    if orientation == HexOrientation.POINTY_TOP:
        q = (math.sqrt(3) / 3 * x - 1 / 3 * y) / size
        r = (2 / 3 * y) / size
    else:  # FLAT_TOP
        q = (2 / 3 * x) / size
        r = (-1 / 3 * x + math.sqrt(3) / 3 * y) / size
    
    return hex_round(q, r)


def hex_round(q: float, r: float) -> Hex:
    """四舍五入到最近的六边形坐标
    
    Args:
        q, r: 浮点坐标
    
    Returns:
        最近的六边形坐标
    """
    s = -q - r
    
    rq = round(q)
    rr = round(r)
    rs = round(s)
    
    q_diff = abs(rq - q)
    r_diff = abs(rr - r)
    s_diff = abs(rs - s)
    
    if q_diff > r_diff and q_diff > s_diff:
        rq = -rr - rs
    elif r_diff > s_diff:
        rr = -rq - rs
    else:
        rs = -rq - rr
    
    return Hex(rq, rr)


def hex_corner_offset(corner: int, size: float, orientation: HexOrientation = HexOrientation.POINTY_TOP
                      ) -> Tuple[float, float]:
    """获取六边形角点偏移
    
    Args:
        corner: 角点索引 (0-5)
        size: 六边形大小
        orientation: 六边形朝向
    
    Returns:
        相对于中心的角点偏移 (x, y)
    """
    angle_offset = math.pi / 6 if orientation == HexOrientation.POINTY_TOP else 0
    angle = 2 * math.pi * corner / 6 + angle_offset
    
    return (size * math.cos(angle), size * math.sin(angle))


def hex_corners(center: Tuple[float, float], size: float, 
                orientation: HexOrientation = HexOrientation.POINTY_TOP) -> List[Tuple[float, float]]:
    """获取六边形所有角点坐标
    
    Args:
        center: 中心像素坐标
        size: 六边形大小
        orientation: 六边形朝向
    
    Returns:
        6个角点坐标列表
    """
    corners = []
    for i in range(6):
        offset = hex_corner_offset(i, size, orientation)
        corners.append((center[0] + offset[0], center[1] + offset[1]))
    return corners


# ==================== 路径查找 ====================

def hex_lerp(a: Hex, b: Hex, t: float) -> Tuple[float, float]:
    """线性插值两点
    
    Args:
        a: 起点
        b: 终点
        t: 插值参数 (0-1)
    
    Returns:
        浮点坐标 (q, r)
    """
    return (a.q + (b.q - a.q) * t, a.r + (b.r - a.r) * t)


def hex_linedraw(a: Hex, b: Hex) -> List[Hex]:
    """画线算法 (改进版)
    
    Args:
        a: 起点
        b: 终点
    
    Returns:
        直线上的六边形列表
    """
    distance = hex_distance(a, b)
    if distance == 0:
        return [a]
    
    results = []
    for i in range(distance + 1):
        t = i / distance
        q, r = hex_lerp(a, b, t)
        results.append(hex_round(q, r))
    
    return results


def hex_path_astar(start: Hex, goal: Hex, 
                   obstacles: Set[Hex],
                   orientation: HexOrientation = HexOrientation.POINTY_TOP,
                   max_radius: int = None) -> List[Hex]:
    """A* 路径查找算法
    
    Args:
        start: 起点
        goal: 终点
        obstacles: 障碍物集合
        orientation: 六边形朝向
        max_radius: 搜索最大半径 (可选，用于限制搜索范围)
    
    Returns:
        路径列表 (从起点到终点)，如果不可达则返回空列表
    """
    def heuristic(a: Hex, b: Hex) -> int:
        return hex_distance(a, b)
    
    open_set = [(0, start)]
    came_from: Dict[Hex, Hex] = {}
    g_score: Dict[Hex, int] = {start: 0}
    f_score: Dict[Hex, int] = {start: heuristic(start, goal)}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            # 重建路径
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return list(reversed(path))
        
        for neighbor in hex_neighbors(current, orientation):
            # 检查障碍物
            if neighbor in obstacles:
                continue
            
            # 检查搜索半径
            if max_radius is not None:
                if hex_distance(start, neighbor) > max_radius:
                    continue
            
            tentative_g = g_score[current] + 1
            
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return []  # 无法到达


def hex_path_bfs(start: Hex, goal: Hex,
                 obstacles: Set[Hex],
                 orientation: HexOrientation = HexOrientation.POINTY_TOP) -> List[Hex]:
    """BFS 路径查找算法
    
    Args:
        start: 起点
        goal: 终点
        obstacles: 障碍物集合
        orientation: 六边形朝向
    
    Returns:
        路径列表 (从起点到终点)，如果不可达则返回空列表
    """
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        current, path = queue.popleft()
        
        if current == goal:
            return path
        
        for neighbor in hex_neighbors(current, orientation):
            if neighbor in visited or neighbor in obstacles:
                continue
            
            visited.add(neighbor)
            queue.append((neighbor, path + [neighbor]))
    
    return []


# ==================== 视野计算 ====================

def hex_fov(center: Hex, radius: int, 
            is_blocking: Callable[[Hex], bool],
            orientation: HexOrientation = HexOrientation.POINTY_TOP) -> Set[Hex]:
    """计算视野范围内的可见六边形
    
    使用阴影投射算法
    
    Args:
        center: 中心位置
        radius: 视野半径
        is_blocking: 判断六边形是否阻挡视野的函数
        orientation: 六边形朝向
    
    Returns:
        可见的六边形集合
    """
    visible = {center}
    
    def cast_fov(row: int, start_slope: float, end_slope: float, quadrant: int):
        """递归投射视野"""
        if start_slope < end_slope:
            return
        
        for r in range(row, radius + 1):
            blocked = False
            new_start = start_slope
            
            for c in range(int(-start_slope * r - 0.5), int(-end_slope * r + 0.5) + 1):
                # 计算六边形位置 (简化版)
                dq = c
                dr = r
                h = center + Hex(dq, dr)
                
                if hex_distance(center, h) > radius:
                    continue
                
                visible.add(h)
                
                if is_blocking(h):
                    blocked = True
                elif blocked:
                    blocked = False
                    cast_fov(r + 1, start_slope, new_start, quadrant)
    
    # 简化实现：检查所有范围内的六边形
    for h in hex_range(center, radius):
        line = hex_linedraw(center, h)
        if all(not is_blocking(l) for l in line[:-1]):
            visible.add(h)
    
    return visible


def hex_visible_from(center: Hex, target: Hex, 
                     obstacles: Set[Hex]) -> bool:
    """判断从中心能否看到目标
    
    Args:
        center: 观察点
        target: 目标点
        obstacles: 障碍物集合
    
    Returns:
        是否可见
    """
    line = hex_linedraw(center, target)
    for h in line[:-1]:  # 不包括目标本身
        if h in obstacles:
            return False
    return True


# ==================== 区域操作 ====================

def hex_flood_fill(start: Hex, 
                   is_passable: Callable[[Hex], bool],
                   max_radius: int = None,
                   orientation: HexOrientation = HexOrientation.POINTY_TOP) -> Set[Hex]:
    """洪水填充算法
    
    Args:
        start: 起点
        is_passable: 判断六边形是否可通行的函数
        max_radius: 最大搜索半径
        orientation: 六边形朝向
    
    Returns:
        可到达的所有六边形集合
    """
    visited = set()
    queue = deque([start])
    
    while queue:
        current = queue.popleft()
        
        if current in visited:
            continue
        
        if max_radius is not None and hex_distance(start, current) > max_radius:
            continue
        
        if not is_passable(current):
            continue
        
        visited.add(current)
        
        for neighbor in hex_neighbors(current, orientation):
            if neighbor not in visited:
                queue.append(neighbor)
    
    return visited


def hex_region_outline(region: Set[Hex], 
                       orientation: HexOrientation = HexOrientation.POINTY_TOP) -> List[Hex]:
    """计算区域的轮廓
    
    Args:
        region: 区域内的六边形集合
        orientation: 六边形朝向
    
    Returns:
        轮廓上的六边形列表
    """
    outline = []
    for h in region:
        for neighbor in hex_neighbors(h, orientation):
            if neighbor not in region:
                outline.append(h)
                break
    return outline


def hex_region_interior(region: Set[Hex],
                        orientation: HexOrientation = HexOrientation.POINTY_TOP) -> List[Hex]:
    """计算区域的内部 (非边界)
    
    Args:
        region: 区域内的六边形集合
        orientation: 六边形朝向
    
    Returns:
        内部六边形列表
    """
    interior = []
    for h in region:
        is_interior = all(neighbor in region for neighbor in hex_neighbors(h, orientation))
        if is_interior:
            interior.append(h)
    return interior


# ==================== 网格类 ====================

class HexGrid:
    """六边形网格类"""
    
    def __init__(self, radius: int = 10, orientation: HexOrientation = HexOrientation.POINTY_TOP):
        """
        Args:
            radius: 网格半径
            orientation: 六边形朝向
        """
        self.radius = radius
        self.orientation = orientation
        self.cells: Dict[Hex, Any] = {}
        
    def in_bounds(self, h: Hex) -> bool:
        """检查坐标是否在网格范围内"""
        return hex_distance(Hex(0, 0), h) <= self.radius
    
    def get(self, h: Hex, default: Any = None) -> Any:
        """获取单元格内容"""
        return self.cells.get(h, default)
    
    def set(self, h: Hex, value: Any):
        """设置单元格内容"""
        if self.in_bounds(h):
            self.cells[h] = value
    
    def remove(self, h: Hex) -> bool:
        """移除单元格"""
        if h in self.cells:
            del self.cells[h]
            return True
        return False
    
    def clear(self):
        """清空网格"""
        self.cells.clear()
    
    def all_cells(self) -> List[Hex]:
        """获取所有有效坐标"""
        return hex_range(Hex(0, 0), self.radius)
    
    def occupied_cells(self) -> List[Hex]:
        """获取所有已占用的坐标"""
        return list(self.cells.keys())
    
    def neighbors(self, h: Hex) -> List[Hex]:
        """获取相邻单元格"""
        return [n for n in hex_neighbors(h, self.orientation) if self.in_bounds(n)]
    
    def distance(self, a: Hex, b: Hex) -> int:
        """计算距离"""
        return hex_distance(a, b)
    
    def path(self, start: Hex, goal: Hex, obstacles: Set[Hex] = None) -> List[Hex]:
        """查找路径"""
        if obstacles is None:
            obstacles = set()
        return hex_path_astar(start, goal, obstacles, self.orientation, self.radius)
    
    def range(self, center: Hex, radius: int) -> List[Hex]:
        """获取范围内的单元格"""
        return [h for h in hex_range(center, radius) if self.in_bounds(h)]
    
    def fov(self, center: Hex, radius: int, 
            is_blocking: Callable[[Hex], bool] = None) -> Set[Hex]:
        """计算视野"""
        if is_blocking is None:
            is_blocking = lambda h: False
        return hex_fov(center, min(radius, self.radius), is_blocking, self.orientation)
    
    def to_ascii(self, char_func: Callable[[Hex], str] = None, 
                 empty: str = '.') -> str:
        """转换为 ASCII 字符画
        
        Args:
            char_func: 获取每个六边形字符的函数
            empty: 空单元格字符
        
        Returns:
            ASCII 字符画
        """
        if char_func is None:
            char_func = lambda h: str(self.cells.get(h, empty))
        
        lines = []
        for r in range(-self.radius, self.radius + 1):
            line = " " * abs(r)  # 偏移
            for q in range(-self.radius, self.radius + 1):
                h = Hex(q, r)
                if self.in_bounds(h):
                    line += char_func(h) + " "
            lines.append(line)
        return "\n".join(lines)
    
    def __repr__(self) -> str:
        return f"HexGrid(radius={self.radius}, cells={len(self.cells)})"


# ==================== 可视化 ====================

def visualize_hex(h: Hex, size: int = 3, char: str = '#') -> str:
    """可视化单个六边形 (ASCII)
    
    Args:
        h: 六边形坐标
        size: 显示大小
        char: 填充字符
    
    Returns:
        ASCII 图案
    """
    lines = []
    for row in range(-size, size + 1):
        line = " " * abs(row)
        for col in range(-size * 2, size * 2 + 1):
            ch = Hex(col, row)
            if hex_distance(Hex(0, 0), ch) <= size:
                line += char
            else:
                line += " "
        lines.append(line)
    return "\n".join(lines)


def visualize_hex_grid(hexes: List[Hex], 
                       char: str = '#',
                       empty: str = ' ',
                       show_coords: bool = False) -> str:
    """可视化六边形网格
    
    Args:
        hexes: 六边形列表
        char: 填充字符
        empty: 空白字符
        show_coords: 是否显示坐标
    
    Returns:
        ASCII 图案
    """
    if not hexes:
        return "(empty)"
    
    hex_set = set(hexes)
    
    # 计算边界
    min_q = min(h.q for h in hexes)
    max_q = max(h.q for h in hexes)
    min_r = min(h.r for h in hexes)
    max_r = max(h.r for h in hexes)
    
    lines = []
    for r in range(min_r, max_r + 1):
        line = " " * (r - min_r)  # 偏移
        for q in range(min_q, max_q + 1):
            h = Hex(q, r)
            if h in hex_set:
                if show_coords:
                    line += f"({q},{r})"
                else:
                    line += char + " "
            else:
                if show_coords:
                    line += empty * 5
                else:
                    line += empty + " "
        lines.append(line)
    
    return "\n".join(lines)


def visualize_hex_path(path: List[Hex], 
                       start_char: str = 'S',
                       end_char: str = 'E',
                       path_char: str = '*',
                       empty: str = '.') -> str:
    """可视化路径
    
    Args:
        path: 路径六边形列表
        start_char: 起点字符
        end_char: 终点字符
        path_char: 路径字符
        empty: 空白字符
    
    Returns:
        ASCII 图案
    """
    if not path:
        return "(no path)"
    
    path_set = set(path)
    
    min_q = min(h.q for h in path)
    max_q = max(h.q for h in path)
    min_r = min(h.r for h in path)
    max_r = max(h.r for h in path)
    
    # 扩展边界
    min_q -= 1
    max_q += 1
    min_r -= 1
    max_r += 1
    
    lines = []
    for r in range(min_r, max_r + 1):
        line = " " * (r - min_r)
        for q in range(min_q, max_q + 1):
            h = Hex(q, r)
            if h == path[0]:
                line += start_char + " "
            elif h == path[-1]:
                line += end_char + " "
            elif h in path_set:
                line += path_char + " "
            else:
                line += empty + " "
        lines.append(line)
    
    return "\n".join(lines)


def visualize_hex_range(center: Hex, radius: int,
                        center_char: str = 'O',
                        ring_char: str = '#',
                        empty: str = '.') -> str:
    """可视化圆形范围
    
    Args:
        center: 中心
        radius: 半径
        center_char: 中心字符
        ring_char: 范围字符
        empty: 空白字符
    
    Returns:
        ASCII 图案
    """
    hexes = hex_range(center, radius)
    hex_set = set(hexes)
    
    min_q = center.q - radius
    max_q = center.q + radius
    min_r = center.r - radius
    max_r = center.r + radius
    
    lines = []
    for r in range(min_r, max_r + 1):
        line = " " * abs(r - center.r)
        for q in range(min_q, max_q + 1):
            h = Hex(q, r)
            if h == center:
                line += center_char + " "
            elif h in hex_set:
                d = hex_distance(center, h)
                line += str(d) + " "
            else:
                line += empty + " "
        lines.append(line)
    
    return "\n".join(lines)


# ==================== 示例用法 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("🔷 六边形网格工具演示")
    print("=" * 60)
    
    # 1. 基础坐标
    print("\n📌 基础坐标操作")
    print("-" * 40)
    h1 = Hex(1, 2)
    h2 = Hex(3, -1)
    print(f"六边形1: {h1}, s={h1.s}")
    print(f"六边形2: {h2}, s={h2.s}")
    print(f"相加: {h1} + {h2} = {h1 + h2}")
    print(f"相减: {h1} - {h2} = {h1 - h2}")
    print(f"距离: {hex_distance(h1, h2)}")
    
    # 2. 邻居
    print("\n📌 邻居计算")
    print("-" * 40)
    center = Hex(0, 0)
    neighbors = hex_neighbors(center)
    print(f"中心: {center}")
    print(f"邻居: {neighbors}")
    
    # 3. 区域生成
    print("\n📌 区域生成")
    print("-" * 40)
    radius_2 = hex_range(Hex(0, 0), 2)
    print(f"半径2的范围: {len(radius_2)} 个六边形")
    ring_2 = hex_ring(Hex(0, 0), 2)
    print(f"半径2的圆环: {len(ring_2)} 个六边形")
    
    # 4. 直线
    print("\n📌 直线绘制")
    print("-" * 40)
    line = hex_line(Hex(0, 0), Hex(3, -2))
    print(f"从 (0,0) 到 (3,-2) 的直线:")
    print(visualize_hex_path(line))
    
    # 5. 路径查找
    print("\n📌 A* 路径查找")
    print("-" * 40)
    start = Hex(0, 0)
    goal = Hex(5, -3)
    obstacles = {Hex(2, -1), Hex(2, 0), Hex(3, -1), Hex(3, -2)}
    path = hex_path_astar(start, goal, obstacles)
    print(f"起点: {start}, 终点: {goal}")
    print(f"障碍物: {obstacles}")
    print(f"路径: {path}")
    print(visualize_hex_path(path))
    
    # 6. 坐标转换
    print("\n📌 坐标转换")
    print("-" * 40)
    h = Hex(2, 3)
    offset = hex_to_offset(h, OffsetCoordType.ODD, HexOrientation.POINTY_TOP)
    print(f"轴向坐标 {h} -> 偏移坐标 {offset}")
    back = offset_to_hex(offset[0], offset[1], OffsetCoordType.ODD, HexOrientation.POINTY_TOP)
    print(f"偏移坐标 {offset} -> 轴向坐标 {back}")
    
    pixel = hex_to_pixel(h, 30, HexOrientation.POINTY_TOP)
    print(f"轴向坐标 {h} -> 像素坐标 {pixel}")
    back_hex = pixel_to_hex(pixel[0], pixel[1], 30, HexOrientation.POINTY_TOP)
    print(f"像素坐标 {pixel} -> 轴向坐标 {back_hex}")
    
    # 7. 六边形网格类
    print("\n📌 六边形网格类")
    print("-" * 40)
    grid = HexGrid(radius=3)
    grid.set(Hex(0, 0), "中心")
    grid.set(Hex(1, 0), "东")
    grid.set(Hex(0, 1), "南")
    print(f"网格: {grid}")
    print(f"中心内容: {grid.get(Hex(0, 0))}")
    
    # 8. 可视化
    print("\n📌 可视化")
    print("-" * 40)
    print("半径2的六边形区域:")
    print(visualize_hex_range(Hex(0, 0), 2))
    
    print("\n六边形网格示例:")
    hexes = hex_range(Hex(0, 0), 2)
    print(visualize_hex_grid(hexes, char='⬡'))