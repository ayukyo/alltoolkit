"""
Spline Utils - 样条曲线工具库
提供多种样条曲线插值和生成方法

支持的样条类型：
- Linear Spline: 线性样条插值
- Cubic Spline: 三次样条插值（自然边界条件）
- Catmull-Rom Spline: 卡特穆-罗姆样条（通过控制点）
- B-Spline: 均匀B样条曲线
- Hermite Spline: 埃尔米特样条

零外部依赖，纯 Python 实现
"""

from typing import List, Tuple, Optional, Callable
import math


class Point2D:
    """二维点"""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Point2D({self.x:.4f}, {self.y:.4f})"
    
    def __eq__(self, other):
        if not isinstance(other, Point2D):
            return False
        return abs(self.x - other.x) < 1e-10 and abs(self.y - other.y) < 1e-10
    
    def distance_to(self, other: 'Point2D') -> float:
        """计算到另一点的距离"""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def to_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)


class Point3D:
    """三维点"""
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self):
        return f"Point3D({self.x:.4f}, {self.y:.4f}, {self.z:.4f})"
    
    def __eq__(self, other):
        if not isinstance(other, Point3D):
            return False
        return (abs(self.x - other.x) < 1e-10 and 
                abs(self.y - other.y) < 1e-10 and 
                abs(self.z - other.z) < 1e-10)
    
    def to_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)


# ============================================================================
# 线性样条插值
# ============================================================================

def linear_spline(points: List[Point2D], num_points: int = 100) -> List[Point2D]:
    """
    线性样条插值 - 连接各点的直线段
    
    Args:
        points: 控制点列表（至少2个点）
        num_points: 生成的点数
    
    Returns:
        插值后的点列表
    """
    if len(points) < 2:
        raise ValueError("至少需要2个控制点")
    
    # 计算每个段的长度和总长度
    segments = []
    total_length = 0
    for i in range(len(points) - 1):
        length = points[i].distance_to(points[i + 1])
        segments.append((points[i], points[i + 1], length))
        total_length += length
    
    if total_length < 1e-10:
        return [Point2D(points[0].x, points[0].y) for _ in range(num_points)]
    
    result = []
    for i in range(num_points):
        t = i / (num_points - 1) if num_points > 1 else 0
        target_dist = t * total_length
        
        # 找到对应的段
        current_dist = 0
        found = False
        for j, (p1, p2, length) in enumerate(segments):
            if current_dist + length >= target_dist:
                # 在这个段内
                if length > 1e-10:
                    local_t = (target_dist - current_dist) / length
                else:
                    local_t = 0
                local_t = max(0, min(1, local_t))
                x = p1.x + local_t * (p2.x - p1.x)
                y = p1.y + local_t * (p2.y - p1.y)
                result.append(Point2D(x, y))
                found = True
                break
            current_dist += length
        
        # 如果没找到（target_dist >= total_length），使用最后一个段
        if not found:
            p1, p2, length = segments[-1]
            x = p2.x
            y = p2.y
            result.append(Point2D(x, y))
    
    return result


# ============================================================================
# 三次样条插值
# ============================================================================

def _solve_tridiagonal(a: List[float], b: List[float], c: List[float], d: List[float]) -> List[float]:
    """求解三对角线性方程组（Thomas算法）"""
    n = len(d)
    if n == 0:
        return []
    
    # 复制输入
    c_prime = [0.0] * n
    d_prime = [0.0] * n
    
    c_prime[0] = c[0] / b[0] if b[0] != 0 else 0
    d_prime[0] = d[0] / b[0] if b[0] != 0 else 0
    
    for i in range(1, n):
        denom = b[i] - a[i] * c_prime[i - 1]
        if abs(denom) < 1e-15:
            denom = 1e-15 if denom >= 0 else -1e-15
        c_prime[i] = c[i] / denom
        d_prime[i] = (d[i] - a[i] * d_prime[i - 1]) / denom
    
    # 回代
    x = [0.0] * n
    x[n - 1] = d_prime[n - 1]
    for i in range(n - 2, -1, -1):
        x[i] = d_prime[i] - c_prime[i] * x[i + 1]
    
    return x


def cubic_spline(points: List[Point2D], num_points: int = 100) -> List[Point2D]:
    """
    三次样条插值（自然边界条件：二阶导数为0）
    
    Args:
        points: 控制点列表（至少2个点，按x坐标排序）
        num_points: 生成的点数
    
    Returns:
        插值后的点列表
    """
    n = len(points)
    if n < 2:
        raise ValueError("至少需要2个控制点")
    if n == 2:
        return linear_spline(points, num_points)
    
    # 按x坐标排序
    sorted_points = sorted(points, key=lambda p: p.x)
    
    # 提取x和y值
    xs = [p.x for p in sorted_points]
    ys = [p.y for p in sorted_points]
    
    # 计算h值（区间宽度）
    h = [xs[i + 1] - xs[i] for i in range(n - 1)]
    
    # 构建三对角矩阵求解二阶导数M
    # 自然边界条件：M[0] = M[n-1] = 0
    
    if n == 2:
        return linear_spline(points, num_points)
    
    # 内部点的方程
    size = n - 2
    if size == 0:
        return linear_spline(points, num_points)
    
    a = [0.0] + [h[i] for i in range(n - 2)]
    b = [2 * (h[i] + h[i + 1]) for i in range(n - 2)]
    c = [h[i + 1] for i in range(n - 3)] + [0.0]
    d = [6 * ((ys[i + 2] - ys[i + 1]) / h[i + 1] - (ys[i + 1] - ys[i]) / h[i]) 
         for i in range(n - 2)]
    
    # 求解内部点的M值
    m_inner = _solve_tridiagonal(a, b, c, d)
    
    # 完整的M数组（包含边界）
    M = [0.0] + m_inner + [0.0]
    
    # 生成插值点
    result = []
    x_min, x_max = xs[0], xs[-1]
    
    for i in range(num_points):
        x = x_min + (x_max - x_min) * i / (num_points - 1) if num_points > 1 else x_min
        
        # 找到x所在的区间
        k = 0
        for j in range(n - 1):
            if xs[j] <= x <= xs[j + 1] or j == n - 2:
                k = j
                break
        
        # 三次样条插值公式
        h_k = h[k]
        if abs(h_k) < 1e-15:
            result.append(Point2D(x, ys[k]))
            continue
        
        t1 = xs[k + 1] - x
        t2 = x - xs[k]
        
        y = (M[k] * t1 ** 3 / (6 * h_k) + 
             M[k + 1] * t2 ** 3 / (6 * h_k) +
             (ys[k] / h_k - M[k] * h_k / 6) * t1 +
             (ys[k + 1] / h_k - M[k + 1] * h_k / 6) * t2)
        
        result.append(Point2D(x, y))
    
    return result


# ============================================================================
# Catmull-Rom 样条
# ============================================================================

def catmull_rom_spline(points: List[Point2D], num_points: int = 100, 
                        tension: float = 0.5, close: bool = False) -> List[Point2D]:
    """
    Catmull-Rom 样条曲线
    
    特点：曲线通过所有控制点
    
    Args:
        points: 控制点列表（至少2个点）
        num_points: 生成的点数
        tension: 张力参数（0-1），默认0.5
        close: 是否闭合曲线
    
    Returns:
        插值后的点列表
    """
    n = len(points)
    if n < 2:
        raise ValueError("至少需要2个控制点")
    if n == 2:
        return linear_spline(points, num_points)
    
    # 处理闭合曲线
    if close:
        pts = [points[-1]] + points + [points[0], points[1]]
    else:
        p0 = Point2D(2 * points[0].x - points[1].x, 2 * points[0].y - points[1].y)
        pn = Point2D(2 * points[-1].x - points[-2].x, 2 * points[-1].y - points[-2].y)
        pts = [p0] + points + [pn]
    
    result = []
    num_segments = n - 1 if not close else n
    points_per_segment = max(1, num_points // num_segments)
    
    for seg in range(num_segments):
        p0, p1, p2, p3 = pts[seg], pts[seg + 1], pts[seg + 2], pts[seg + 3]
        
        for i in range(points_per_segment):
            t = i / points_per_segment
            
            # Catmull-Rom 基函数
            t2 = t * t
            t3 = t2 * t
            
            x = 0.5 * ((2 * p1.x) +
                       (-p0.x + p2.x) * t +
                       (2 * p0.x - 5 * p1.x + 4 * p2.x - p3.x) * t2 +
                       (-p0.x + 3 * p1.x - 3 * p2.x + p3.x) * t3)
            
            y = 0.5 * ((2 * p1.y) +
                       (-p0.y + p2.y) * t +
                       (2 * p0.y - 5 * p1.y + 4 * p2.y - p3.y) * t2 +
                       (-p0.y + 3 * p1.y - 3 * p2.y + p3.y) * t3)
            
            result.append(Point2D(x, y))
    
    # 确保包含最后一个点
    if not close and result:
        result.append(Point2D(points[-1].x, points[-1].y))
    
    return result[:num_points] if len(result) > num_points else result


# ============================================================================
# B-Spline 样条
# ============================================================================

def _b_spline_basis(i: int, k: int, t: float, knots: List[float]) -> float:
    """
    计算B样条基函数值（递归定义）
    
    Args:
        i: 控制点索引
        k: 阶数（degree + 1）
        t: 参数值
        knots: 节点向量
    
    Returns:
        基函数值
    """
    if k == 1:
        if knots[i] <= t < knots[i + 1]:
            return 1.0
        elif t == knots[-1] and i == len(knots) - 2:
            return 1.0
        return 0.0
    
    # 递归计算
    denom1 = knots[i + k - 1] - knots[i]
    denom2 = knots[i + k] - knots[i + 1]
    
    result = 0.0
    
    if abs(denom1) > 1e-10:
        result += ((t - knots[i]) / denom1) * _b_spline_basis(i, k - 1, t, knots)
    
    if abs(denom2) > 1e-10:
        result += ((knots[i + k] - t) / denom2) * _b_spline_basis(i + 1, k - 1, t, knots)
    
    return result


def b_spline(points: List[Point2D], degree: int = 3, num_points: int = 100, 
             close: bool = False) -> List[Point2D]:
    """
    均匀B样条曲线
    
    Args:
        points: 控制点列表（至少degree+1个点）
        degree: 样条阶数（1=线性, 2=二次, 3=三次，默认）
        num_points: 生成的点数
        close: 是否闭合曲线
    
    Returns:
        插值后的点列表
    """
    n = len(points)
    min_points = degree + 1
    
    if n < min_points:
        if n < 2:
            raise ValueError(f"B样条至少需要{min_points}个控制点（当前{n}个）")
        # 降低阶数
        degree = n - 1
    
    # 处理闭合曲线
    if close:
        points = list(points) + points[:degree]
        n = len(points)
    
    # 均匀节点向量
    m = n + degree + 1
    knots = [float(i) for i in range(m)]
    
    result = []
    t_min = knots[degree]
    t_max = knots[n] - 1e-10
    
    for i in range(num_points):
        t = t_min + (t_max - t_min) * i / (num_points - 1) if num_points > 1 else t_min
        
        x, y = 0.0, 0.0
        for j in range(n):
            basis = _b_spline_basis(j, degree + 1, t, knots)
            x += basis * points[j].x
            y += basis * points[j].y
        
        result.append(Point2D(x, y))
    
    return result


# ============================================================================
# Hermite 样条
# ============================================================================

def hermite_spline(points: List[Point2D], tangents: List[Point2D], 
                   num_points: int = 100) -> List[Point2D]:
    """
    Hermite 样条曲线
    
    Args:
        points: 控制点列表（至少2个点）
        tangents: 各点的切线向量（长度与points相同）
        num_points: 生成的点数
    
    Returns:
        插值后的点列表
    """
    n = len(points)
    if n < 2:
        raise ValueError("至少需要2个控制点")
    if len(tangents) != n:
        raise ValueError("切线向量数量必须与控制点数量相同")
    
    result = []
    num_segments = n - 1
    points_per_segment = max(1, num_points // num_segments)
    
    for seg in range(num_segments):
        p0, p1 = points[seg], points[seg + 1]
        m0, m1 = tangents[seg], tangents[seg + 1]
        
        for i in range(points_per_segment):
            t = i / points_per_segment
            t2 = t * t
            t3 = t2 * t
            
            # Hermite 基函数
            h00 = 2 * t3 - 3 * t2 + 1
            h10 = t3 - 2 * t2 + t
            h01 = -2 * t3 + 3 * t2
            h11 = t3 - t2
            
            x = h00 * p0.x + h10 * m0.x + h01 * p1.x + h11 * m1.x
            y = h00 * p0.y + h10 * m0.y + h01 * p1.y + h11 * m1.y
            
            result.append(Point2D(x, y))
    
    # 确保包含最后一个点
    if result:
        result.append(Point2D(points[-1].x, points[-1].y))
    
    return result[:num_points] if len(result) > num_points else result


def hermite_spline_auto(points: List[Point2D], num_points: int = 100) -> List[Point2D]:
    """
    自动计算切线的 Hermite 样条
    
    Args:
        points: 控制点列表（至少2个点）
        num_points: 生成的点数
    
    Returns:
        插值后的点列表
    """
    n = len(points)
    if n < 2:
        raise ValueError("至少需要2个控制点")
    
    # 自动计算切线（中心差分）
    tangents = []
    for i in range(n):
        if i == 0:
            tx = points[1].x - points[0].x
            ty = points[1].y - points[0].y
        elif i == n - 1:
            tx = points[-1].x - points[-2].x
            ty = points[-1].y - points[-2].y
        else:
            tx = (points[i + 1].x - points[i - 1].x) / 2
            ty = (points[i + 1].y - points[i - 1].y) / 2
        tangents.append(Point2D(tx, ty))
    
    return hermite_spline(points, tangents, num_points)


# ============================================================================
# 工具函数
# ============================================================================

def sample_curve(points: List[Point2D], sample_distance: float) -> List[Point2D]:
    """
    按距离采样曲线点
    
    Args:
        points: 曲线点列表
        sample_distance: 采样距离
    
    Returns:
        采样后的点列表
    """
    if len(points) < 2:
        return points.copy()
    
    result = [points[0]]
    accumulated_dist = 0.0
    
    for i in range(1, len(points)):
        segment_dist = points[i].distance_to(points[i - 1])
        accumulated_dist += segment_dist
        
        if accumulated_dist >= sample_distance:
            # 插值采样点
            t = (accumulated_dist - sample_distance) / segment_dist if segment_dist > 0 else 0
            x = points[i - 1].x + t * (points[i].x - points[i - 1].x)
            y = points[i - 1].y + t * (points[i].y - points[i - 1].y)
            result.append(Point2D(x, y))
            accumulated_dist = 0.0
    
    if result[-1] != points[-1]:
        result.append(points[-1])
    
    return result


def curve_length(points: List[Point2D]) -> float:
    """
    计算曲线长度
    
    Args:
        points: 曲线点列表
    
    Returns:
        曲线总长度
    """
    if len(points) < 2:
        return 0.0
    
    length = 0.0
    for i in range(1, len(points)):
        length += points[i].distance_to(points[i - 1])
    
    return length


def resample_curve(points: List[Point2D], num_points: int) -> List[Point2D]:
    """
    按曲线长度均匀重采样
    
    Args:
        points: 曲线点列表
        num_points: 目标点数
    
    Returns:
        重采样后的点列表
    """
    if len(points) < 2:
        return points.copy() if points else []
    
    total_length = curve_length(points)
    if total_length < 1e-10:
        return [Point2D(points[0].x, points[0].y) for _ in range(num_points)]
    
    # 计算每个点的累积弧长
    arc_lengths = [0.0]
    for i in range(1, len(points)):
        arc_lengths.append(arc_lengths[-1] + points[i].distance_to(points[i - 1]))
    
    result = []
    for i in range(num_points):
        target = total_length * i / (num_points - 1) if num_points > 1 else 0
        
        # 二分查找
        left, right = 0, len(arc_lengths) - 1
        while left < right - 1:
            mid = (left + right) // 2
            if arc_lengths[mid] <= target:
                left = mid
            else:
                right = mid
        
        # 线性插值
        if left < len(points) - 1:
            segment_length = arc_lengths[left + 1] - arc_lengths[left]
            if segment_length > 1e-10:
                t = (target - arc_lengths[left]) / segment_length
            else:
                t = 0
            x = points[left].x + t * (points[left + 1].x - points[left].x)
            y = points[left].y + t * (points[left + 1].y - points[left].y)
        else:
            x, y = points[-1].x, points[-1].y
        
        result.append(Point2D(x, y))
    
    return result


def smooth_points(points: List[Point2D], iterations: int = 1, factor: float = 0.5) -> List[Point2D]:
    """
    平滑点列（Laplacian平滑）
    
    Args:
        points: 点列表
        iterations: 迭代次数
        factor: 平滑因子（0-1）
    
    Returns:
        平滑后的点列表
    """
    if len(points) < 3:
        return points.copy()
    
    result = [Point2D(p.x, p.y) for p in points]
    
    for _ in range(iterations):
        new_result = [Point2D(result[0].x, result[0].y)]
        for i in range(1, len(result) - 1):
            x = result[i].x + factor * ((result[i - 1].x + result[i + 1].x) / 2 - result[i].x)
            y = result[i].y + factor * ((result[i - 1].y + result[i + 1].y) / 2 - result[i].y)
            new_result.append(Point2D(x, y))
        new_result.append(Point2D(result[-1].x, result[-1].y))
        result = new_result
    
    return result


# ============================================================================
# 便捷函数
# ============================================================================

def interpolate(points: List[Tuple[float, float]], 
                method: str = 'cubic', 
                num_points: int = 100) -> List[Tuple[float, float]]:
    """
    便捷插值函数
    
    Args:
        points: 控制点列表 [(x1, y1), (x2, y2), ...]
        method: 插值方法 ('linear', 'cubic', 'catmull_rom', 'b_spline', 'hermite')
        num_points: 生成的点数
    
    Returns:
        插值后的点列表 [(x, y), ...]
    """
    pts = [Point2D(x, y) for x, y in points]
    
    if method == 'linear':
        result = linear_spline(pts, num_points)
    elif method == 'cubic':
        result = cubic_spline(pts, num_points)
    elif method == 'catmull_rom':
        result = catmull_rom_spline(pts, num_points)
    elif method == 'b_spline':
        result = b_spline(pts, degree=3, num_points=num_points)
    elif method == 'hermite':
        result = hermite_spline_auto(pts, num_points)
    else:
        raise ValueError(f"未知的插值方法: {method}")
    
    return [p.to_tuple() for p in result]


if __name__ == "__main__":
    # 简单演示
    points = [
        Point2D(0, 0),
        Point2D(1, 2),
        Point2D(3, 1),
        Point2D(5, 3),
        Point2D(6, 0)
    ]
    
    print("控制点:", points)
    print("\n线性样条插值:")
    linear = linear_spline(points, 10)
    for p in linear:
        print(f"  {p}")
    
    print("\n三次样条插值:")
    cubic = cubic_spline(points, 10)
    for p in cubic:
        print(f"  {p}")
    
    print("\nCatmull-Rom 样条:")
    cr = catmull_rom_spline(points, 10)
    for p in cr:
        print(f"  {p}")
    
    print("\nB样条:")
    bs = b_spline(points, degree=3, num_points=10)
    for p in bs:
        print(f"  {p}")