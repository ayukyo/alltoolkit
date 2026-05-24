"""
fractal_utils - 分形图形生成工具

提供多种经典分形的生成功能：Mandelbrot 集、Julia 集、Sierpinski 三角形、
Koch 曲线、Barnsley 羊齿草、Dragon 曲线、Hilbert 曲线等。

支持生成 ASCII 艺术和数值数据，零外部依赖，纯 Python 实现。

Author: AllToolkit
Date: 2026-05-24
"""

from typing import List, Tuple, Dict, Optional, Callable
from math import cos, sin, sqrt, pi, log
import random


class Point:
    """二维点"""
    
    __slots__ = ['x', 'y']
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float) -> 'Point':
        return Point(self.x * scalar, self.y * scalar)
    
    def distance_to(self, other: 'Point') -> float:
        """计算到另一点的距离"""
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"


class FractalConfig:
    """分形配置"""
    
    def __init__(
        self,
        width: int = 80,
        height: int = 40,
        max_iterations: int = 100,
        escape_radius: float = 2.0,
        x_min: float = -2.0,
        x_max: float = 2.0,
        y_min: float = -2.0,
        y_max: float = 2.0
    ):
        self.width = width
        self.height = height
        self.max_iterations = max_iterations
        self.escape_radius = escape_radius
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max


class MandelbrotSet:
    """Mandelbrot 集生成器
    
    Mandelbrot 集是复平面上满足 z_{n+1} = z_n^2 + c 不发散的点 c 的集合。
    其中 z_0 = 0。
    """
    
    @staticmethod
    def iterate(c_real: float, c_imag: float, max_iter: int = 100) -> int:
        """迭代计算逃逸次数
        
        Args:
            c_real: 复数 c 的实部
            c_imag: 复数 c 的虚部
            max_iter: 最大迭代次数
            
        Returns:
            int: 逃逸前的迭代次数（未逃逸返回 max_iter）
        """
        z_real = 0.0
        z_imag = 0.0
        
        for i in range(max_iter):
            # z = z^2 + c
            z_real_new = z_real * z_real - z_imag * z_imag + c_real
            z_imag_new = 2 * z_real * z_imag + c_imag
            
            z_real = z_real_new
            z_imag = z_imag_new
            
            # 检查是否逃逸
            if z_real * z_real + z_imag * z_imag > 4:
                return i
        
        return max_iter
    
    @staticmethod
    def generate_ascii(config: FractalConfig = None) -> str:
        """生成 ASCII 艺术
        
        Args:
            config: 分形配置
            
        Returns:
            str: ASCII 艺术字符串
        """
        if config is None:
            config = FractalConfig()
        
        # ASCII 字符映射（从暗到亮）
        chars = " .:-=+*#%@"
        
        result = []
        for row in range(config.height):
            line = ""
            for col in range(config.width):
                # 映射到复平面坐标
                x = config.x_min + (config.x_max - config.x_min) * col / config.width
                y = config.y_min + (config.y_max - config.y_min) * row / config.height
                
                # 计算迭代次数
                iterations = MandelbrotSet.iterate(x, y, config.max_iterations)
                
                # 映射到字符
                if iterations == config.max_iterations:
                    char = chars[-1]  # 在集合内
                else:
                    idx = int(iterations / config.max_iterations * (len(chars) - 1))
                    char = chars[min(idx, len(chars) - 2)]
                
                line += char
            result.append(line)
        
        return "\n".join(result)
    
    @staticmethod
    def generate_data(config: FractalConfig = None) -> List[List[int]]:
        """生成数值数据
        
        Args:
            config: 分形配置
            
        Returns:
            List[List[int]]: 迭代次数矩阵
        """
        if config is None:
            config = FractalConfig()
        
        data = []
        for row in range(config.height):
            row_data = []
            for col in range(config.width):
                x = config.x_min + (config.x_max - config.x_min) * col / config.width
                y = config.y_min + (config.y_max - config.y_min) * row / config.height
                iterations = MandelbrotSet.iterate(x, y, config.max_iterations)
                row_data.append(iterations)
            data.append(row_data)
        
        return data
    
    @staticmethod
    def zoom(center_x: float, center_y: float, scale: float, 
             base_config: FractalConfig = None) -> FractalConfig:
        """生成缩放配置
        
        Args:
            center_x: 缩放中心 X 坐标
            center_y: 缩放中心 Y 坐标
            scale: 缩放比例（越小越精细）
            base_config: 基础配置
            
        Returns:
            FractalConfig: 新的缩放配置
        """
        if base_config is None:
            base_config = FractalConfig()
        
        return FractalConfig(
            width=base_config.width,
            height=base_config.height,
            max_iterations=base_config.max_iterations,
            x_min=center_x - scale,
            x_max=center_x + scale,
            y_min=center_y - scale,
            y_max=center_y + scale
        )


class JuliaSet:
    """Julia 集生成器
    
    Julia 集是复平面上满足 z_{n+1} = z_n^2 + c 不发散的点 z_0 的集合，
    其中 c 是一个固定的复数参数。
    """
    
    # 经典 Julia 集参数
    CLASSIC_PARAMS = {
        "dendrite": (-0.8, 0.156),       # 树突状
        "rabbit": (-0.4, 0.6),           # 兔子
        "dragon": (0.285, 0.01),         # 龙
        "spiral": (-0.8, -0.156),        # 螺旋
        "san marco": (-1.25, 0),         # 圣马可
        "siegel disk": (-0.391, -0.587), # Siegel 盘
        "galaxy": (0.355, 0.355),        # 星系
        "feather": (-0.70176, -0.3842),  # 羽毛
        "crown": (-0.7269, 0.1889),      # 王冠
    }
    
    @staticmethod
    def iterate(z_real: float, z_imag: float, c_real: float, c_imag: float,
               max_iter: int = 100) -> int:
        """迭代计算逃逸次数
        
        Args:
            z_real: 初始 z 的实部
            z_imag: 初始 z 的虚部
            c_real: 参数 c 的实部
            c_imag: 参数 c 的虚部
            max_iter: 最大迭代次数
            
        Returns:
            int: 逃逸前的迭代次数
        """
        for i in range(max_iter):
            # z = z^2 + c
            z_real_new = z_real * z_real - z_imag * z_imag + c_real
            z_imag_new = 2 * z_real * z_imag + c_imag
            
            z_real = z_real_new
            z_imag = z_imag_new
            
            if z_real * z_real + z_imag * z_imag > 4:
                return i
        
        return max_iter
    
    @staticmethod
    def generate_ascii(c_real: float, c_imag: float, config: FractalConfig = None) -> str:
        """生成 ASCII 艺术
        
        Args:
            c_real: 参数 c 的实部
            c_imag: 参数 c 的虚部
            config: 分形配置
            
        Returns:
            str: ASCII 艺术字符串
        """
        if config is None:
            config = FractalConfig()
        
        chars = " .:-=+*#%@"
        
        result = []
        for row in range(config.height):
            line = ""
            for col in range(config.width):
                x = config.x_min + (config.x_max - config.x_min) * col / config.width
                y = config.y_min + (config.y_max - config.y_min) * row / config.height
                
                iterations = JuliaSet.iterate(x, y, c_real, c_imag, config.max_iterations)
                
                if iterations == config.max_iterations:
                    char = chars[-1]
                else:
                    idx = int(iterations / config.max_iterations * (len(chars) - 1))
                    char = chars[min(idx, len(chars) - 2)]
                
                line += char
            result.append(line)
        
        return "\n".join(result)
    
    @staticmethod
    def generate_data(c_real: float, c_imag: float, config: FractalConfig = None) -> List[List[int]]:
        """生成数值数据"""
        if config is None:
            config = FractalConfig()
        
        data = []
        for row in range(config.height):
            row_data = []
            for col in range(config.width):
                x = config.x_min + (config.x_max - config.x_min) * col / config.width
                y = config.y_min + (config.y_max - config.y_min) * row / config.height
                iterations = JuliaSet.iterate(x, y, c_real, c_imag, config.max_iterations)
                row_data.append(iterations)
            data.append(row_data)
        
        return data
    
    @staticmethod
    def get_classic_params(name: str) -> Optional[Tuple[float, float]]:
        """获取经典参数
        
        Args:
            name: 参数名称
            
        Returns:
            Optional[Tuple[float, float]]: (c_real, c_imag) 或 None
        """
        return JuliaSet.CLASSIC_PARAMS.get(name.lower())


class SierpinskiTriangle:
    """Sierpinski 三角形生成器
    
    通过递归删除三角形内部来生成的分形图形。
    """
    
    @staticmethod
    def generate_ascii(size: int = 32) -> str:
        """生成 ASCII 艺术
        
        Args:
            size: 三角形大小（行数）
            
        Returns:
            str: ASCII 艺术字符串
        """
        result = []
        for y in range(size):
            line = ""
            for x in range(2 * size - 1):
                # 使用位运算判断是否应该绘制
                # Sierpinski 三角形的规律：对于位置 (x, y)
                # 如果 x & y != 0，则该点在三角形内部（空白）
                # 注意需要偏移处理
                offset_x = x - (size - y - 1)
                if 0 <= offset_x < 2 * y + 1:
                    if (offset_x & y) == 0:
                        line += "*"
                    else:
                        line += " "
                else:
                    line += " "
            result.append(line)
        
        return "\n".join(result)
    
    @staticmethod
    def generate_points(iterations: int = 6) -> List[Point]:
        """使用混沌游戏生成点集
        
        Args:
            iterations: 迭代次数（点数约为 2^iterations）
            
        Returns:
            List[Point]: 点集
        """
        # 三角形顶点
        vertices = [
            Point(0.5, 0.0),      # 顶部
            Point(0.0, 1.0),      # 左下
            Point(1.0, 1.0),      # 右下
        ]
        
        # 初始点
        current = Point(0.5, 0.5)
        points = [current]
        
        num_points = 2 ** iterations
        for _ in range(num_points):
            # 随机选择一个顶点
            vertex = random.choice(vertices)
            # 移动到顶点和当前点的中点
            current = Point(
                (current.x + vertex.x) / 2,
                (current.y + vertex.y) / 2
            )
            points.append(current)
        
        return points
    
    @staticmethod
    def calculate_area_ratio(iterations: int) -> float:
        """计算面积比例
        
        Args:
            iterations: 递归迭代次数
            
        Returns:
            float: 剩余面积与原始面积的比例
        """
        # 每次迭代删除 1/4 的面积
        return (3 / 4) ** iterations
    
    @staticmethod
    def calculate_triangle_count(iterations: int) -> int:
        """计算三角形数量
        
        Args:
            iterations: 递归迭代次数
            
        Returns:
            int: 小三角形数量
        """
        return 3 ** iterations


class KochCurve:
    """Koch 曲线生成器
    
    通过不断在每段线段上添加三角形凸起来生成的分形曲线。
    """
    
    @staticmethod
    def generate_points(iterations: int = 4, length: float = 100.0) -> List[Point]:
        """生成 Koch 曲线的点集
        
        Args:
            iterations: 迭代次数
            length: 初始线段长度
            
        Returns:
            List[Point]: 曲线点集
        """
        # 初始线段
        points = [Point(0, 0), Point(length, 0)]
        
        for _ in range(iterations):
            new_points = []
            for i in range(len(points) - 1):
                p1 = points[i]
                p2 = points[i + 1]
                
                # 计算分段点
                delta = p2 - p1
                
                # 三分点
                a = p1 + delta * (1/3)
                b = p1 + delta * (2/3)
                
                # 计算凸起顶点（在 ab 的中点上，向上偏移）
                # 使用向量旋转
                mid = Point((a.x + b.x) / 2, (a.y + b.y) / 2)
                
                # 三分线段的长度
                segment_length = a.distance_to(b)
                
                # 凸起高度 = 三分线段长度 * sqrt(3) / 2
                # 方向垂直于线段（向左旋转 90 度）
                # 简化：假设线段水平，凸起向上
                dx = b.x - a.x
                dy = b.y - a.y
                
                # 旋转 -90 度
                peak_x = mid.x + dy * sqrt(3) / 2
                peak_y = mid.y - dx * sqrt(3) / 2
                
                peak = Point(peak_x, peak_y)
                
                new_points.extend([p1, a, peak, b])
            
            new_points.append(points[-1])
            points = new_points
        
        return points
    
    @staticmethod
    def generate_koch_snowflake(iterations: int = 4, size: float = 60.0) -> List[Point]:
        """生成 Koch 雪花
        
        Args:
            iterations: 迭代次数
            size: 初始三角形边长
            
        Returns:
            List[Point]: 雪花轮廓点集
        """
        # 初始等边三角形
        height = size * sqrt(3) / 2
        
        p1 = Point(0, height / 3 * 2)
        p2 = Point(size / 2, -height / 3)
        p3 = Point(-size / 2, -height / 3)
        
        # 生成三条 Koch 曲线
        curve1 = KochCurve._generate_segment(p1, p2, iterations)
        curve2 = KochCurve._generate_segment(p2, p3, iterations)
        curve3 = KochCurve._generate_segment(p3, p1, iterations)
        
        return curve1 + curve2 + curve3
    
    @staticmethod
    def _generate_segment(p1: Point, p2: Point, iterations: int) -> List[Point]:
        """生成一条 Koch 曲线段"""
        points = [p1, p2]
        
        for _ in range(iterations):
            new_points = []
            for i in range(len(points) - 1):
                start = points[i]
                end = points[i + 1]
                
                delta = end - start
                
                a = start + delta * (1/3)
                b = start + delta * (2/3)
                
                # 计算峰值点
                dx = b.x - a.x
                dy = b.y - a.y
                mid = Point((a.x + b.x) / 2, (a.y + b.y) / 2)
                
                peak = Point(
                    mid.x + dy * sqrt(3) / 2,
                    mid.y - dx * sqrt(3) / 2
                )
                
                new_points.extend([start, a, peak, b])
            
            new_points.append(points[-1])
            points = new_points
        
        return points
    
    @staticmethod
    def calculate_length_ratio(iterations: int) -> float:
        """计算长度比例
        
        Args:
            iterations: 迭代次数
            
        Returns:
            float: 曲线长度与原始长度的比例
        """
        # 每次迭代长度增加 4/3
        return (4 / 3) ** iterations


class BarnsleyFern:
    """Barnsley 羊齿草分形
    
    使用迭代函数系统（IFS）生成的植物形状分形。
    """
    
    # IFS 变换参数
    TRANSFORMS = [
        # f1: 转换到主干
        (0.0, 0.0, 0.0, 0.16, 0.0, 0.0, 0.01),
        # f2: 左叶
        (0.85, 0.04, -0.04, 0.85, 0.0, 1.6, 0.85),
        # f3: 右叶
        (0.20, -0.26, 0.23, 0.22, 0.0, 1.6, 0.07),
        # f4: 叶柄
        (-0.15, 0.28, 0.26, 0.24, 0.0, 0.44, 0.07),
    ]
    
    @staticmethod
    def generate_points(num_points: int = 10000) -> List[Point]:
        """生成羊齿草点集
        
        Args:
            num_points: 点数
            
        Returns:
            List[Point]: 点集
        """
        current = Point(0.0, 0.0)
        points = [current]
        
        for _ in range(num_points):
            # 根据概率选择变换
            r = random.random()
            
            if r < 0.01:
                # f1
                a, b, c, d, e, f, _ = BarnsleyFern.TRANSFORMS[0]
            elif r < 0.86:
                # f2
                a, b, c, d, e, f, _ = BarnsleyFern.TRANSFORMS[1]
            elif r < 0.93:
                # f3
                a, b, c, d, e, f, _ = BarnsleyFern.TRANSFORMS[2]
            else:
                # f4
                a, b, c, d, e, f, _ = BarnsleyFern.TRANSFORMS[3]
            
            # 应用变换: x' = ax + by + e, y' = cx + dy + f
            new_x = a * current.x + b * current.y + e
            new_y = c * current.x + d * current.y + f
            
            current = Point(new_x, new_y)
            points.append(current)
        
        return points
    
    @staticmethod
    def generate_ascii(width: int = 60, height: int = 40, num_points: int = 5000) -> str:
        """生成 ASCII 艺术
        
        Args:
            width: 宽度
            height: 高度
            num_points: 点数
            
        Returns:
            str: ASCII 艺术字符串
        """
        points = BarnsleyFern.generate_points(num_points)
        
        # 确定范围
        x_values = [p.x for p in points]
        y_values = [p.y for p in points]
        
        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = min(y_values), max(y_values)
        
        # 创建画布
        canvas = [[" " for _ in range(width)] for _ in range(height)]
        
        # 绘制点
        for p in points:
            # 映射到画布坐标
            col = int((p.x - x_min) / (x_max - x_min) * (width - 1))
            row = int((p.y - y_min) / (y_max - y_min) * (height - 1))
            
            # 反转 y（因为 ASCII 从上到下）
            row = height - 1 - row
            
            if 0 <= row < height and 0 <= col < width:
                canvas[row][col] = "*"
        
        return "\n".join("".join(row) for row in canvas)


class DragonCurve:
    """Dragon 曲线生成器
    
    通过反复折叠纸条生成的分形曲线。
    """
    
    @staticmethod
    def generate_turns(iterations: int) -> List[str]:
        """生成转向序列
        
        Args:
            iterations: 迭代次数
            
        Returns:
            List[str]: 转向序列（"L" 表示左转，"R" 表示右转）
            返回 2^iterations - 1 个转向
        """
        if iterations <= 0:
            return []
        
        # 使用正确的 Dragon curve 折叠规则
        # 每次迭代：在当前序列后添加 R，然后添加反转并翻转的序列
        turns = ["R"]  # 第一次迭代
        
        for i in range(1, iterations):
            # 创建中间的 R
            new_sequence = turns + ["R"]
            # 添加反转并翻转的后半部分
            for turn in reversed(turns):
                new_sequence.append("L" if turn == "R" else "R")
            turns = new_sequence
        
        return turns
    
    @staticmethod
    def generate_points(iterations: int = 12, segment_length: float = 1.0) -> List[Point]:
        """生成 Dragon 曲线点集
        
        Args:
            iterations: 迭代次数
            segment_length: 线段长度
            
        Returns:
            List[Point]: 曲线点集
            包含 2^iterations + 1 个点（2^iterations 个线段）
        """
        turns = DragonCurve.generate_turns(iterations)
        
        # 初始方向向右
        direction = 0  # 角度（度）
        current = Point(0, 0)
        points = [current]
        
        for turn in turns:
            # 转向
            if turn == "L":
                direction += 90
            else:
                direction -= 90
            
            # 移动
            rad = direction * pi / 180
            new_point = Point(
                current.x + segment_length * cos(rad),
                current.y + segment_length * sin(rad)
            )
            
            points.append(new_point)
            current = new_point
        
        # 添加最后一个点（最后一个线段，不需要转向）
        rad = direction * pi / 180
        final_point = Point(
            current.x + segment_length * cos(rad),
            current.y + segment_length * sin(rad)
        )
        points.append(final_point)
        
        return points
    
    @staticmethod
    def calculate_segments(iterations: int) -> int:
        """计算线段数量
        
        Args:
            iterations: 迭代次数
            
        Returns:
            int: 线段数量
        """
        return 2 ** iterations


class HilbertCurve:
    """Hilbert 曲线生成器
    
    一种填充空间的分形曲线，遍历二维网格的每个点。
    """
    
    @staticmethod
    def generate_points(order: int = 4, size: float = 100.0) -> List[Point]:
        """生成 Hilbert 曲线点集
        
        Args:
            order: 曲线阶数（生成 4^order 个点）
            size: 曲线尺寸
            
        Returns:
            List[Point]: 曲线点集
        """
        n = 2 ** order
        points = []
        
        for i in range(n * n):
            # 将索引转换为 Hilbert 曲线坐标
            x, y = HilbertCurve._d2xy(n, i)
            # 映射到实际坐标
            points.append(Point(x * size / n, y * size / n))
        
        return points
    
    @staticmethod
    def _d2xy(n: int, d: int) -> Tuple[int, int]:
        """将 Hilbert 曲线索引转换为坐标
        
        Args:
            n: 网格大小（必须是 2 的幂）
            d: Hilbert 曲线索引
            
        Returns:
            Tuple[int, int]: (x, y) 坐标
        """
        x = 0
        y = 0
        s = 1
        
        while s < n:
            rx = 1 & (d // 2)
            ry = 1 & (d ^ rx)
            
            x, y = HilbertCurve._rot(s, x, y, rx, ry)
            
            x += s * rx
            y += s * ry
            d //= 4
            s *= 2
        
        return x, y
    
    @staticmethod
    def _rot(n: int, x: int, y: int, rx: int, ry: int) -> Tuple[int, int]:
        """旋转/翻转坐标"""
        if ry == 0:
            if rx == 1:
                x = n - 1 - x
                y = n - 1 - y
            
            # 交换 x 和 y
            return y, x
        
        return x, y
    
    @staticmethod
    def xy2d(n: int, x: int, y: int) -> int:
        """将坐标转换为 Hilbert 曲线索引
        
        Args:
            n: 网格大小
            x: X 坐标
            y: Y 坐标
            
        Returns:
            int: Hilbert 曲线索引
        """
        d = 0
        s = n // 2
        
        while s > 0:
            rx = (x & s) > 0
            ry = (y & s) > 0
            
            d += s * s * ((3 * rx) ^ ry)
            
            x, y = HilbertCurve._rot(s, x, y, rx, ry)
            
            s //= 2
        
        return d
    
    @staticmethod
    def generate_ascii(order: int = 4) -> str:
        """生成 ASCII 艺术
        
        Args:
            order: 曲线阶数
            
        Returns:
            str: ASCII 艺术字符串
        """
        n = 2 ** order
        # 创建画布
        canvas = [[" " for _ in range(n * 2 - 1)] for _ in range(n * 2 - 1)]
        
        points = HilbertCurve.generate_points(order, n * 2 - 1)
        
        # 绘制连接线
        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i + 1]
            
            # 绘制水平或垂直线
            x1, y1 = int(p1.x), int(p1.y)
            x2, y2 = int(p2.x), int(p2.y)
            
            if x1 == x2:
                # 垂直线
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    canvas[y][x1] = "|"
            else:
                # 水平线
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    canvas[y1][x] = "-"
        
        return "\n".join("".join(row) for row in canvas)


class CantorSet:
    """Cantor 集生成器
    
    通过不断删除线段中间三分之一生成的分形集合。
    """
    
    @staticmethod
    def generate_segments(iterations: int = 5, start: float = 0.0, 
                         end: float = 100.0) -> List[Tuple[float, float]]:
        """生成 Cantor 集的线段
        
        Args:
            iterations: 迭代次数
            start: 起始位置
            end: 结束位置
            
        Returns:
            List[Tuple[float, float]]: 线段列表
        """
        segments = [(start, end)]
        
        for _ in range(iterations):
            new_segments = []
            for s_start, s_end in segments:
                length = s_end - s_start
                third = length / 3
                
                # 左段
                new_segments.append((s_start, s_start + third))
                # 右段
                new_segments.append((s_end - third, s_end))
            
            segments = new_segments
        
        return segments
    
    @staticmethod
    def generate_ascii(iterations: int = 5, width: int = 80) -> str:
        """生成 ASCII 艺术
        
        Args:
            iterations: 迭代次数
            width: 宽度
            
        Returns:
            str: ASCII 艺术字符串
        """
        result = []
        
        segments = CantorSet.generate_segments(iterations, 0, width)
        
        for level in range(iterations + 1):
            level_segments = CantorSet.generate_segments(level, 0, width)
            line = [" " for _ in range(width)]
            
            for start, end in level_segments:
                for i in range(int(start), int(end)):
                    if i < width:
                        line[i] = "*"
            
            result.append("".join(line))
        
        return "\n".join(result)
    
    @staticmethod
    def calculate_length_ratio(iterations: int) -> float:
        """计算长度比例
        
        Args:
            iterations: 迭代次数
            
        Returns:
            float: 剩余长度与原始长度的比例
        """
        return (2 / 3) ** iterations
    
    @staticmethod
    def calculate_segment_count(iterations: int) -> int:
        """计算线段数量
        
        Args:
            iterations: 迭代次数
            
        Returns:
            int: 线段数量
        """
        return 2 ** iterations


class FractalDimension:
    """分形维度计算工具"""
    
    @staticmethod
    def box_counting(points: List[Point], box_sizes: List[float] = None) -> float:
        """使用盒子计数法计算分形维度
        
        Args:
            points: 点集
            box_sizes: 盒子尺寸列表
            
        Returns:
            float: 分形维度
        """
        if box_sizes is None:
            box_sizes = [1, 2, 4, 8, 16, 32]
        
        # 确定范围
        x_values = [p.x for p in points]
        y_values = [p.y for p in points]
        
        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = min(y_values), max(y_values)
        
        width = x_max - x_min
        height = y_max - y_min
        
        counts = []
        
        for size in box_sizes:
            # 创建网格
            num_boxes_x = int(width / size) + 1
            num_boxes_y = int(height / size) + 1
            
            # 计算被点覆盖的盒子数
            occupied = set()
            for p in points:
                box_x = int((p.x - x_min) / size)
                box_y = int((p.y - y_min) / size)
                occupied.add((box_x, box_y))
            
            counts.append(len(occupied))
        
        # 使用 log-log 回归计算维度
        # N(s) ~ s^-D
        # log(N) ~ -D * log(s)
        
        if len(counts) < 2:
            return 0.0
        
        # 简化线性回归
        log_sizes = [log(s) for s in box_sizes if s > 0]
        log_counts = [log(c) for c in counts if c > 0]
        
        n = len(log_sizes)
        if n < 2:
            return 0.0
        
        # 计算斜率
        sum_x = sum(log_sizes)
        sum_y = sum(log_counts)
        sum_xy = sum(x * y for x, y in zip(log_sizes, log_counts))
        sum_x2 = sum(x * x for x in log_sizes)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        
        # 维度 = -slope
        return -slope


class CellularAutomaton:
    """细胞自动机分形
    
    使用一维细胞自动机生成的分形图案。
    """
    
    @staticmethod
    def generate_1d(rule: int, iterations: int = 20, width: int = 80) -> str:
        """生成一维细胞自动机
        
        Args:
            rule: 规则编号（0-255）
            iterations: 迭代次数
            width: 宽度
            
        Returns:
            str: ASCII 艺术字符串
        """
        # 初始状态：中心一个活细胞
        state = [False] * width
        state[width // 2] = True
        
        result = []
        
        for _ in range(iterations):
            # 绘制当前状态
            line = "".join("*" if cell else " " for cell in state)
            result.append(line)
            
            # 计算下一状态
            new_state = [False] * width
            for i in range(width):
                # 获取邻居状态
                left = state[i - 1] if i > 0 else False
                center = state[i]
                right = state[i + 1] if i < width - 1 else False
                
                # 计算规则索引
                pattern = (left << 2) | (center << 1) | right
                new_state[i] = (rule >> pattern) & 1 == 1
            
            state = new_state
        
        return "\n".join(result)
    
    @staticmethod
    def get_classic_rules() -> Dict[str, int]:
        """获取经典规则
        
        Returns:
            Dict[str, int]: 规则名称和编号
        """
        return {
            "sierpinski": 90,       # 生成 Sierpinski 三角形
            "triangles": 60,        # 三角形图案
            "stripes": 15,          # 条纹图案
            "complex": 30,          # 复杂图案
            "nested": 110,          # 嵌套结构
            "symmetric": 150,       # 对称图案
            "random": 45,           # 类随机图案
            "solid": 255,           # 全填充
        }


# 便捷函数

def mandelbrot_ascii(config: FractalConfig = None) -> str:
    """生成 Mandelbrot 集 ASCII 艺术"""
    return MandelbrotSet.generate_ascii(config)


def julia_ascii(c_real: float, c_imag: float, config: FractalConfig = None) -> str:
    """生成 Julia 集 ASCII 艺术"""
    return JuliaSet.generate_ascii(c_real, c_imag, config)


def sierpinski_ascii(size: int = 32) -> str:
    """生成 Sierpinski 三角形 ASCII 艺术"""
    return SierpinskiTriangle.generate_ascii(size)


def koch_snowflake_ascii(iterations: int = 3) -> str:
    """生成 Koch 雪花 ASCII 艺术（简化版本）"""
    # 简化：生成 Koch 曲线的 ASCII 表示
    chars = " .:+*#"
    width = 80
    height = 40
    
    canvas = [[" " for _ in range(width)] for _ in range(height)]
    
    points = KochCurve.generate_koch_snowflake(iterations, width * 0.8)
    
    # 绘制点
    x_values = [p.x for p in points]
    y_values = [p.y for p in points]
    
    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)
    
    for p in points:
        col = int((p.x - x_min) / (x_max - x_min + 0.01) * (width - 1))
        row = int((p.y - y_min) / (y_max - y_min + 0.01) * (height - 1))
        
        row = height - 1 - row
        
        if 0 <= row < height and 0 <= col < width:
            canvas[row][col] = "*"
    
    return "\n".join("".join(row) for row in canvas)


def barnsley_fern_ascii(width: int = 60, height: int = 40, num_points: int = 5000) -> str:
    """生成 Barnsley 羊齿草 ASCII 艺术"""
    return BarnsleyFern.generate_ascii(width, height, num_points)


def dragon_curve_ascii(iterations: int = 10) -> str:
    """生成 Dragon 曲线 ASCII 艺术"""
    chars = " .:+*#"
    width = 80
    height = 50
    
    canvas = [[" " for _ in range(width)] for _ in range(height)]
    
    points = DragonCurve.generate_points(iterations, segment_length=2.0)
    
    x_values = [p.x for p in points]
    y_values = [p.y for p in points]
    
    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)
    
    for p in points:
        col = int((p.x - x_min) / (x_max - x_min + 0.01) * (width - 1))
        row = int((p.y - y_min) / (y_max - y_min + 0.01) * (height - 1))
        
        row = height - 1 - row
        
        if 0 <= row < height and 0 <= col < width:
            canvas[row][col] = "*"
    
    return "\n".join("".join(row) for row in canvas)


def hilbert_curve_ascii(order: int = 3) -> str:
    """生成 Hilbert 曲线 ASCII 艺术"""
    return HilbertCurve.generate_ascii(order)


def cantor_set_ascii(iterations: int = 5, width: int = 80) -> str:
    """生成 Cantor 集 ASCII 艺术"""
    return CantorSet.generate_ascii(iterations, width)


def cellular_automaton_ascii(rule: int = 90, iterations: int = 20, width: int = 80) -> str:
    """生成细胞自动机 ASCII 艺术"""
    return CellularAutomaton.generate_1d(rule, iterations, width)


def get_fractal_info() -> Dict[str, Dict]:
    """获取所有分形的信息
    
    Returns:
        Dict[str, Dict]: 分形信息
    """
    return {
        "mandelbrot": {
            "name_cn": "Mandelbrot 集",
            "dimension": 2.0,
            "description": "复平面上的迭代分形，z_{n+1} = z_n^2 + c"
        },
        "julia": {
            "name_cn": "Julia 集",
            "dimension": 2.0,
            "description": "Mandelbrot 集的变体，c 固定而 z_0 变化"
        },
        "sierpinski": {
            "name_cn": "Sierpinski 三角形",
            "dimension": log(3) / log(2),  # ≈ 1.585
            "description": "通过递归删除三角形内部生成"
        },
        "koch": {
            "name_cn": "Koch 曲线/雪花",
            "dimension": log(4) / log(3),  # ≈ 1.262
            "description": "通过添加三角形凸起生成"
        },
        "barnsley": {
            "name_cn": "Barnsley 羊齿草",
            "dimension": 2.0,
            "description": "使用 IFS 生成的植物形状分形"
        },
        "dragon": {
            "name_cn": "Dragon 曲线",
            "dimension": 2.0,
            "description": "通过反复折叠纸条生成"
        },
        "hilbert": {
            "name_cn": "Hilbert 曲线",
            "dimension": 2.0,
            "description": "填充空间的分形曲线"
        },
        "cantor": {
            "name_cn": "Cantor 集",
            "dimension": log(2) / log(3),  # ≈ 0.631
            "description": "通过删除线段中间三分之一生成"
        }
    }