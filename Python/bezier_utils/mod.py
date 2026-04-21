"""
贝塞尔曲线工具模块

提供贝塞尔曲线的计算、插值、分割等功能。
零外部依赖，纯 Python 实现。

支持：
- 一阶（线性）、二阶（二次）、三阶（三次）及任意阶贝塞尔曲线
- 曲线上的点计算
- 曲线长度近似计算
- 曲线切线和法线向量
- 曲线分割
- 曲线平滑（生成多点路径）
"""

from typing import List, Tuple, Optional, Callable
import math


class Point:
    """二维点类"""
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return f"Point({self.x:.4f}, {self.y:.4f})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Point):
            return False
        return abs(self.x - other.x) < 1e-9 and abs(self.y - other.y) < 1e-9
    
    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float) -> 'Point':
        return Point(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar: float) -> 'Point':
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar: float) -> 'Point':
        return Point(self.x / scalar, self.y / scalar)
    
    def distance_to(self, other: 'Point') -> float:
        """计算到另一个点的距离"""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def magnitude(self) -> float:
        """向量的模"""
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def normalize(self) -> 'Point':
        """返回单位向量"""
        mag = self.magnitude()
        if mag < 1e-9:
            return Point(0, 0)
        return self / mag
    
    def perpendicular(self) -> 'Point':
        """返回垂直向量（逆时针旋转90度）"""
        return Point(-self.y, self.x)
    
    def to_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)
    
    @staticmethod
    def from_tuple(t: Tuple[float, float]) -> 'Point':
        return Point(t[0], t[1])


class BezierCurve:
    """
    贝塞尔曲线类
    
    支持任意阶数的贝塞尔曲线计算。
    """
    
    def __init__(self, control_points: List[Point]):
        """
        初始化贝塞尔曲线
        
        Args:
            control_points: 控制点列表，至少需要2个点
        """
        if len(control_points) < 2:
            raise ValueError("贝塞尔曲线至少需要2个控制点")
        self.control_points = control_points
        self._degree = len(control_points) - 1
    
    @property
    def degree(self) -> int:
        """曲线阶数"""
        return self._degree
    
    @property
    def start_point(self) -> Point:
        """起点"""
        return self.control_points[0]
    
    @property
    def end_point(self) -> Point:
        """终点"""
        return self.control_points[-1]
    
    def point_at(self, t: float) -> Point:
        """
        计算曲线上参数 t 处的点
        
        使用 De Casteljau 算法，支持任意阶数
        
        Args:
            t: 参数值，范围 [0, 1]
        
        Returns:
            曲线上的点
        """
        if not 0 <= t <= 1:
            raise ValueError(f"参数 t 必须在 [0, 1] 范围内，当前值: {t}")
        
        # De Casteljau 算法
        points = [Point(p.x, p.y) for p in self.control_points]
        
        for k in range(1, len(points)):
            for i in range(len(points) - k):
                points[i] = points[i] * (1 - t) + points[i + 1] * t
        
        return points[0]
    
    def derivative_at(self, t: float) -> Point:
        """
        计算曲线上参数 t 处的一阶导数（切线向量）
        
        Args:
            t: 参数值，范围 [0, 1]
        
        Returns:
            切线向量（未归一化）
        """
        if not 0 <= t <= 1:
            raise ValueError(f"参数 t 必须在 [0, 1] 范围内，当前值: {t}")
        
        if self._degree == 0:
            return Point(0, 0)
        
        # 一阶导数的控制点是原控制点的差分
        derivative_points = [
            (self.control_points[i + 1] - self.control_points[i]) * self._degree
            for i in range(self._degree)
        ]
        
        if len(derivative_points) == 1:
            return derivative_points[0]
        
        # 递归计算低一阶的贝塞尔曲线在 t 处的值
        temp_curve = BezierCurve(derivative_points)
        return temp_curve.point_at(t)
    
    def tangent_at(self, t: float) -> Point:
        """
        计算曲线上参数 t 处的单位切线向量
        
        Args:
            t: 参数值，范围 [0, 1]
        
        Returns:
            单位切线向量
        """
        return self.derivative_at(t).normalize()
    
    def normal_at(self, t: float) -> Point:
        """
        计算曲线上参数 t 处的单位法线向量
        
        Args:
            t: 参数值，范围 [0, 1]
        
        Returns:
            单位法线向量（切线逆时针旋转90度）
        """
        return self.tangent_at(t).perpendicular()
    
    def curvature_at(self, t: float) -> float:
        """
        计算曲线上参数 t 处的曲率
        
        曲率 κ = |x'y'' - y'x''| / (x'^2 + y'^2)^(3/2)
        
        Args:
            t: 参数值，范围 [0, 1]
        
        Returns:
            曲率值
        """
        if self._degree < 2:
            return 0.0  # 直线的曲率为0
        
        # 一阶导数
        d1 = self.derivative_at(t)
        
        # 二阶导数
        if self._degree == 1:
            return 0.0
        
        # 计算二阶导数
        n = self._degree
        # 二阶导数的控制点
        second_derivative_points = [
            (self.control_points[i + 2] - 2 * self.control_points[i + 1] + self.control_points[i]) * (n * (n - 1))
            for i in range(n - 1)
        ]
        
        if len(second_derivative_points) == 0:
            return 0.0
        
        if len(second_derivative_points) == 1:
            d2 = second_derivative_points[0]
        else:
            # 对于更高阶曲线，需要在 t 处计算
            temp_curve = BezierCurve(second_derivative_points)
            d2 = temp_curve.point_at(t)
        
        # 曲率公式
        numerator = abs(d1.x * d2.y - d1.y * d2.x)
        denominator = (d1.x ** 2 + d1.y ** 2) ** 1.5
        
        if denominator < 1e-9:
            return 0.0
        
        return numerator / denominator
    
    def length(self, num_samples: int = 100) -> float:
        """
        计算曲线的近似长度
        
        使用数值积分方法（梯形法则）
        
        Args:
            num_samples: 采样点数量，越多越精确
        
        Returns:
            曲线长度
        """
        if num_samples < 2:
            num_samples = 2
        
        total_length = 0.0
        prev_point = self.point_at(0)
        
        for i in range(1, num_samples + 1):
            t = i / num_samples
            curr_point = self.point_at(t)
            total_length += prev_point.distance_to(curr_point)
            prev_point = curr_point
        
        return total_length
    
    def split_at(self, t: float) -> Tuple['BezierCurve', 'BezierCurve']:
        """
        在参数 t 处分割曲线
        
        使用 De Casteljau 算法
        
        Args:
            t: 分割参数，范围 [0, 1]
        
        Returns:
            两条子曲线 (左半部分, 右半部分)
        """
        if not 0 <= t <= 1:
            raise ValueError(f"参数 t 必须在 [0, 1] 范围内，当前值: {t}")
        
        # De Casteljau 分割
        n = len(self.control_points)
        left_points = [self.control_points[0]]
        right_points = [self.control_points[-1]]
        
        points = [Point(p.x, p.y) for p in self.control_points]
        
        for k in range(1, n):
            new_points = []
            for i in range(n - k):
                new_points.append(points[i] * (1 - t) + points[i + 1] * t)
            points = new_points
            left_points.append(points[0])
            right_points.insert(0, points[-1])
        
        return BezierCurve(left_points), BezierCurve(right_points)
    
    def bounding_box(self, num_samples: int = 100) -> Tuple[Point, Point]:
        """
        计算曲线的边界框
        
        Args:
            num_samples: 采样点数量
        
        Returns:
            (左下角点, 右上角点)
        """
        points = [self.point_at(t) for t in [i / num_samples for i in range(num_samples + 1)]]
        
        min_x = min(p.x for p in points)
        max_x = max(p.x for p in points)
        min_y = min(p.y for p in points)
        max_y = max(p.y for p in points)
        
        return Point(min_x, min_y), Point(max_x, max_y)
    
    def sample(self, num_points: int) -> List[Point]:
        """
        在曲线上均匀采样（参数均匀分布）
        
        Args:
            num_points: 采样点数量
        
        Returns:
            采样点列表
        """
        if num_points < 2:
            num_points = 2
        
        return [self.point_at(i / (num_points - 1)) for i in range(num_points)]
    
    def sample_uniform(self, segment_length: float) -> List[Point]:
        """
        按弧长均匀采样曲线上的点
        
        Args:
            segment_length: 每段的目标长度
        
        Returns:
            采样点列表
        """
        total_length = self.length()
        num_segments = max(1, int(total_length / segment_length))
        
        # 首先进行密集采样
        dense_samples = 1000
        points = [self.point_at(i / dense_samples) for i in range(dense_samples + 1)]
        lengths = [0.0]
        
        for i in range(1, len(points)):
            lengths.append(lengths[-1] + points[i - 1].distance_to(points[i]))
        
        result = [self.start_point]
        target_length = segment_length
        
        for i in range(1, num_segments):
            target = i * segment_length
            
            # 二分查找
            low, high = 0, len(lengths) - 1
            while low < high:
                mid = (low + high) // 2
                if lengths[mid] < target:
                    low = mid + 1
                else:
                    high = mid
            
            # 线性插值
            if low > 0:
                t_low = (low - 1) / dense_samples
                t_high = low / dense_samples
                len_low = lengths[low - 1]
                len_high = lengths[low]
                
                if len_high - len_low > 1e-9:
                    ratio = (target - len_low) / (len_high - len_low)
                    t = t_low + ratio * (t_high - t_low)
                    result.append(self.point_at(t))
        
        result.append(self.end_point)
        return result
    
    def elevate_degree(self) -> 'BezierCurve':
        """
        升阶：返回一条高一阶的等价贝塞尔曲线
        
        Returns:
            升阶后的贝塞尔曲线
        """
        n = len(self.control_points)
        new_points = [self.control_points[0]]
        
        for i in range(1, n):
            ratio = i / n
            new_point = self.control_points[i - 1] * ratio + self.control_points[i] * (1 - ratio)
            new_points.append(new_point)
        
        new_points.append(self.control_points[-1])
        return BezierCurve(new_points)
    
    def to_polyline(self, tolerance: float = 0.01) -> List[Point]:
        """
        将曲线转换为多段线（自适应细分）
        
        Args:
            tolerance: 转换容差
        
        Returns:
            多段线顶点列表
        """
        def flatten_recursive(curve: BezierCurve, points: List[Point]):
            # 计算曲线平坦度
            if curve._degree < 2:
                points.append(curve.end_point)
                return
            
            # 检查控制点是否接近直线
            start = curve.start_point
            end = curve.end_point
            line_vec = end - start
            line_len = line_vec.magnitude()
            
            if line_len < 1e-9:
                points.append(curve.end_point)
                return
            
            # 计算中间控制点到直线的距离
            max_dist = 0.0
            for i in range(1, len(curve.control_points) - 1):
                cp = curve.control_points[i]
                # 点到直线距离
                dist = abs((cp.x - start.x) * (end.y - start.y) - 
                          (cp.y - start.y) * (end.x - start.x)) / line_len
                max_dist = max(max_dist, dist)
            
            if max_dist <= tolerance:
                points.append(curve.end_point)
            else:
                # 分割并递归
                left, right = curve.split_at(0.5)
                flatten_recursive(left, points)
                flatten_recursive(right, points)
        
        points = [self.start_point]
        flatten_recursive(self, points)
        return points
    
    def reverse(self) -> 'BezierCurve':
        """
        返回反向的贝塞尔曲线
        
        Returns:
            反向的贝塞尔曲线
        """
        return BezierCurve(list(reversed(self.control_points)))


class LinearBezier(BezierCurve):
    """一阶（线性）贝塞尔曲线"""
    
    def __init__(self, p0: Point, p1: Point):
        super().__init__([p0, p1])
    
    def point_at(self, t: float) -> Point:
        if not 0 <= t <= 1:
            raise ValueError(f"参数 t 必须在 [0, 1] 范围内，当前值: {t}")
        return self.control_points[0] * (1 - t) + self.control_points[1] * t
    
    def length(self, num_samples: int = 100) -> float:
        return self.start_point.distance_to(self.end_point)


class QuadraticBezier(BezierCurve):
    """二阶（二次）贝塞尔曲线"""
    
    def __init__(self, p0: Point, p1: Point, p2: Point):
        super().__init__([p0, p1, p2])
    
    def point_at(self, t: float) -> Point:
        if not 0 <= t <= 1:
            raise ValueError(f"参数 t 必须在 [0, 1] 范围内，当前值: {t}")
        
        p0, p1, p2 = self.control_points
        mt = 1 - t
        
        # B(t) = (1-t)²P0 + 2(1-t)tP1 + t²P2
        return p0 * (mt * mt) + p1 * (2 * mt * t) + p2 * (t * t)


class CubicBezier(BezierCurve):
    """三阶（三次）贝塞尔曲线"""
    
    def __init__(self, p0: Point, p1: Point, p2: Point, p3: Point):
        super().__init__([p0, p1, p2, p3])
    
    def point_at(self, t: float) -> Point:
        if not 0 <= t <= 1:
            raise ValueError(f"参数 t 必须在 [0, 1] 范围内，当前值: {t}")
        
        p0, p1, p2, p3 = self.control_points
        mt = 1 - t
        
        # B(t) = (1-t)³P0 + 3(1-t)²tP1 + 3(1-t)t²P2 + t³P3
        return (p0 * (mt ** 3) + 
                p1 * (3 * mt * mt * t) + 
                p2 * (3 * mt * t * t) + 
                p3 * (t ** 3))


# 工厂函数
def create_bezier(points: List[Tuple[float, float]]) -> BezierCurve:
    """
    从坐标元组列表创建贝塞尔曲线
    
    Args:
        points: 坐标元组列表 [(x1, y1), (x2, y2), ...]
    
    Returns:
        BezierCurve 对象
    """
    control_points = [Point(x, y) for x, y in points]
    return BezierCurve(control_points)


def linear_bezier(p0: Tuple[float, float], p1: Tuple[float, float]) -> LinearBezier:
    """创建线性贝塞尔曲线"""
    return LinearBezier(Point(*p0), Point(*p1))


def quadratic_bezier(p0: Tuple[float, float], p1: Tuple[float, float], 
                     p2: Tuple[float, float]) -> QuadraticBezier:
    """创建二次贝塞尔曲线"""
    return QuadraticBezier(Point(*p0), Point(*p1), Point(*p2))


def cubic_bezier(p0: Tuple[float, float], p1: Tuple[float, float], 
                 p2: Tuple[float, float], p3: Tuple[float, float]) -> CubicBezier:
    """创建三次贝塞尔曲线"""
    return CubicBezier(Point(*p0), Point(*p1), Point(*p2), Point(*p3))


def smooth_path(points: List[Point], tension: float = 0.3) -> List[BezierCurve]:
    """
    通过一组点生成平滑的贝塞尔曲线路径
    
    使用 Catmull-Rom 样条转换为贝塞尔曲线
    
    Args:
        points: 经过的点列表
        tension: 张力系数，控制曲线平滑程度
    
    Returns:
        贝塞尔曲线列表
    """
    if len(points) < 2:
        return []
    
    if len(points) == 2:
        return [LinearBezier(points[0], points[1])]
    
    curves = []
    
    for i in range(len(points) - 1):
        p0 = points[max(0, i - 1)]
        p1 = points[i]
        p2 = points[i + 1]
        p3 = points[min(len(points) - 1, i + 2)]
        
        # 计算控制点
        cp1 = p1 + (p2 - p0) * tension
        cp2 = p2 - (p3 - p1) * tension
        
        curves.append(CubicBezier(p1, cp1, cp2, p2))
    
    return curves


def interpolate_points(points: List[Tuple[float, float]], 
                       tension: float = 0.5) -> List[Tuple[float, float]]:
    """
    在点之间插值生成平滑路径
    
    Args:
        points: 原始点坐标
        tension: 张力系数
    
    Returns:
        插值后的平滑路径点坐标
    """
    if len(points) < 2:
        return points
    
    bezier_points = [Point(x, y) for x, y in points]
    curves = smooth_path(bezier_points, tension)
    
    result = []
    for curve in curves:
        samples = curve.sample(20)
        for p in samples[:-1]:  # 避免重复
            result.append(p.to_tuple())
    
    # 添加最后一个点
    if curves:
        result.append(curves[-1].end_point.to_tuple())
    
    return result


def find_t_for_x(curve: BezierCurve, target_x: float, tolerance: float = 1e-6, 
                 max_iterations: int = 100) -> Optional[float]:
    """
    找到曲线上 x 坐标等于 target_x 的参数 t
    
    使用二分法求解
    
    Args:
        curve: 贝塞尔曲线
        target_x: 目标 x 坐标
        tolerance: 容差
        max_iterations: 最大迭代次数
    
    Returns:
        参数 t 值，如果找不到则返回 None
    """
    # 检查 target_x 是否在曲线 x 范围内
    min_x = min(cp.x for cp in curve.control_points)
    max_x = max(cp.x for cp in curve.control_points)
    
    if target_x < min_x - tolerance or target_x > max_x + tolerance:
        return None
    
    # 二分法
    low, high = 0.0, 1.0
    
    for _ in range(max_iterations):
        mid = (low + high) / 2
        point = curve.point_at(mid)
        
        if abs(point.x - target_x) < tolerance:
            return mid
        
        if point.x < target_x:
            low = mid
        else:
            high = mid
    
    return (low + high) / 2


def distance_to_point(curve: BezierCurve, point: Point, 
                      num_samples: int = 100) -> Tuple[float, float]:
    """
    计算点到曲线的最短距离
    
    Args:
        curve: 贝塞尔曲线
        point: 目标点
        num_samples: 采样数量
    
    Returns:
        (最短距离, 对应的参数t)
    """
    min_dist = float('inf')
    min_t = 0.0
    
    for i in range(num_samples + 1):
        t = i / num_samples
        curve_point = curve.point_at(t)
        dist = point.distance_to(curve_point)
        
        if dist < min_dist:
            min_dist = dist
            min_t = t
    
    # 局部优化
    step = 1.0 / num_samples
    for _ in range(10):
        for dt in [-step, step]:
            t = max(0, min(1, min_t + dt))
            curve_point = curve.point_at(t)
            dist = point.distance_to(curve_point)
            
            if dist < min_dist:
                min_dist = dist
                min_t = t
        
        step /= 2
    
    return min_dist, min_t