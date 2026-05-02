"""
Interpolation Utils - 插值工具模块

提供多种插值方法，包括：
- 线性插值 (Linear)
- 多项式插值 (Lagrange, Newton)
- 分段线性插值 (Piecewise Linear)
- 反距离加权插值 (IDW)
- 双线性插值 (Bilinear)
- 三线性插值 (Trilinear)
- 最近邻插值 (Nearest Neighbor)
- Akima 插值
- 样条插值 (Cubic Spline - 简化版)

所有实现仅使用 Python 标准库，零外部依赖。
"""

import math
from typing import List, Tuple, Optional, Union, Callable

Number = Union[int, float]


class InterpolationError(Exception):
    """插值相关错误"""
    pass


def validate_points(points: List[Tuple[Number, Number]]) -> None:
    """
    验证插值点数据
    
    Args:
        points: 插值点列表 [(x, y), ...]
        
    Raises:
        InterpolationError: 数据无效时抛出
    """
    if not points:
        raise InterpolationError("插值点列表不能为空")
    if len(points) < 2:
        raise InterpolationError("至少需要两个插值点")
    
    # 检查 x 值是否唯一
    x_values = [p[0] for p in points]
    if len(set(x_values)) != len(x_values):
        raise InterpolationError("x 值必须唯一，不能有重复")


def sort_points(points: List[Tuple[Number, Number]]) -> List[Tuple[Number, Number]]:
    """
    按 x 值排序插值点
    
    Args:
        points: 插值点列表
        
    Returns:
        排序后的点列表
    """
    return sorted(points, key=lambda p: p[0])


# ============== 线性插值 ==============

def linear_interpolate(points: List[Tuple[Number, Number]], x: Number) -> float:
    """
    线性插值
    
    在两个相邻点之间进行线性插值。对于超出范围的点，
    使用边界处的线性外推。
    
    Args:
        points: 插值点列表 [(x0, y0), (x1, y1), ...]，无需排序
        x: 要插值的 x 值
        
    Returns:
        插值结果 y
        
    Example:
        >>> points = [(0, 0), (1, 1), (2, 4)]
        >>> linear_interpolate(points, 0.5)
        0.5
        >>> linear_interpolate(points, 1.5)
        2.5
    """
    validate_points(points)
    sorted_points = sort_points(points)
    
    # 外推 - 左边界
    if x <= sorted_points[0][0]:
        if len(sorted_points) == 1:
            return float(sorted_points[0][1])
        x0, y0 = sorted_points[0]
        x1, y1 = sorted_points[1]
        return float(y0 + (y1 - y0) * (x - x0) / (x1 - x0))
    
    # 外推 - 右边界
    if x >= sorted_points[-1][0]:
        if len(sorted_points) == 1:
            return float(sorted_points[-1][1])
        x0, y0 = sorted_points[-2]
        x1, y1 = sorted_points[-1]
        return float(y1 + (y1 - y0) * (x - x1) / (x1 - x0))
    
    # 内插 - 找到包含 x 的区间
    for i in range(len(sorted_points) - 1):
        x0, y0 = sorted_points[i]
        x1, y1 = sorted_points[i + 1]
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0)
            return float(y0 + t * (y1 - y0))
    
    # 不应该到达这里
    raise InterpolationError(f"无法为 x={x} 找到合适的插值区间")


# ============== 多项式插值 ==============

def lagrange_interpolate(points: List[Tuple[Number, Number]], x: Number) -> float:
    """
    拉格朗日多项式插值
    
    通过所有给定点的唯一多项式进行插值。
    注意：高阶多项式可能在端点附近出现 Runge 现象（震荡）。
    
    Args:
        points: 插值点列表 [(x0, y0), (x1, y1), ...]
        x: 要插值的 x 值
        
    Returns:
        插值结果 y
        
    Example:
        >>> points = [(0, 1), (1, 3), (2, 2)]
        >>> round(lagrange_interpolate(points, 0.5), 4)
        2.375
    """
    validate_points(points)
    n = len(points)
    
    result = 0.0
    for i in range(n):
        xi, yi = points[i]
        term = float(yi)
        for j in range(n):
            if i != j:
                xj, _ = points[j]
                term *= (x - xj) / (xi - xj)
        result += term
    
    return result


def newton_divided_difference(points: List[Tuple[Number, Number]]) -> List[List[float]]:
    """
    计算牛顿差商表
    
    Args:
        points: 插值点列表
        
    Returns:
        差商表（下三角矩阵）
    """
    n = len(points)
    # 初始化差商表
    table = [[0.0] * n for _ in range(n)]
    
    # 第一列为 y 值
    for i in range(n):
        table[i][0] = float(points[i][1])
    
    # 计算差商
    for j in range(1, n):
        for i in range(n - j):
            xi, xij = points[i][0], points[i + j][0]
            table[i][j] = (table[i + 1][j - 1] - table[i][j - 1]) / (xij - xi)
    
    return table


def newton_interpolate(points: List[Tuple[Number, Number]], x: Number) -> float:
    """
    牛顿多项式插值
    
    使用牛顿形式的多项式插值，便于动态添加新点。
    
    Args:
        points: 插值点列表 [(x0, y0), (x1, y1), ...]
        x: 要插值的 x 值
        
    Returns:
        插值结果 y
        
    Example:
        >>> points = [(0, 1), (1, 3), (2, 2)]
        >>> round(newton_interpolate(points, 0.5), 4)
        2.375
    """
    validate_points(points)
    
    # 计算差商
    table = newton_divided_difference(points)
    n = len(points)
    
    # 牛顿多项式求值
    result = table[0][0]
    for i in range(1, n):
        term = table[0][i]
        for j in range(i):
            term *= (x - points[j][0])
        result += term
    
    return result


# ============== 分段插值 ==============

def piecewise_linear_interpolate(
    points: List[Tuple[Number, Number]], 
    x: Number,
    extrapolate: bool = True
) -> Optional[float]:
    """
    分段线性插值
    
    在每个区间内使用线性插值。对于超出范围的点，
    可选择返回 None（不外推）或使用线性外推。
    
    Args:
        points: 插值点列表
        x: 要插值的 x 值
        extrapolate: 是否允许外推
        
    Returns:
        插值结果 y，如果不外推且超出范围则返回 None
        
    Example:
        >>> points = [(0, 0), (1, 2), (2, 1)]
        >>> piecewise_linear_interpolate(points, 0.5)
        1.0
        >>> piecewise_linear_interpolate(points, 3, extrapolate=False) is None
        True
    """
    validate_points(points)
    sorted_points = sort_points(points)
    
    # 超出范围
    if x < sorted_points[0][0] or x > sorted_points[-1][0]:
        if not extrapolate:
            return None
        return linear_interpolate(sorted_points, x)
    
    # 找到包含 x 的区间
    for i in range(len(sorted_points) - 1):
        x0, y0 = sorted_points[i]
        x1, y1 = sorted_points[i + 1]
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)
    
    return None


# ============== 反距离加权插值 ==============

def idw_interpolate(
    points: List[Tuple[Number, Number]], 
    x: Number,
    power: float = 2.0,
    k: Optional[int] = None
) -> float:
    """
    反距离加权插值 (Inverse Distance Weighting)
    
    使用距离的倒数作为权重进行加权平均。
    距离越近的点权重越大。
    
    Args:
        points: 插值点列表 [(x, y), ...]
        x: 要插值的 x 值
        power: 距离权重的幂次，默认为 2（平方反比）
        k: 只考虑最近的 k 个点，None 表示使用所有点
        
    Returns:
        插值结果 y
        
    Example:
        >>> points = [(0, 0), (1, 1), (2, 4)]
        >>> round(idw_interpolate(points, 0.5), 2)
        0.31
    """
    validate_points(points)
    
    # 检查是否正好在某个数据点上
    for px, py in points:
        if abs(px - x) < 1e-10:
            return float(py)
    
    # 计算距离
    distances = [(abs(px - x), py) for px, py in points]
    distances.sort(key=lambda d: d[0])
    
    # 选择最近的 k 个点
    if k is not None and k < len(distances):
        distances = distances[:k]
    
    # 计算权重和加权值
    total_weight = 0.0
    weighted_sum = 0.0
    
    for dist, y in distances:
        weight = 1.0 / (dist ** power)
        weighted_sum += weight * y
        total_weight += weight
    
    return weighted_sum / total_weight


# ============== 双线性插值 ==============

def bilinear_interpolate(
    points: List[Tuple[Number, Number, Number]], 
    x: Number, 
    y: Number
) -> float:
    """
    双线性插值（2D）
    
    在矩形网格的四个角点之间进行双线性插值。
    
    Args:
        points: 四个角点 [(x0, y0, z00), (x1, y0, z10), (x0, y1, z01), (x1, y1, z11)]
                或任意四个点组成的网格
        x: 要插值的 x 坐标
        y: 要插值的 y 坐标
        
    Returns:
        插值结果 z
        
    Example:
        >>> points = [(0, 0, 1), (1, 0, 2), (0, 1, 3), (1, 1, 4)]
        >>> bilinear_interpolate(points, 0.5, 0.5)
        2.5
    """
    if len(points) != 4:
        raise InterpolationError("双线性插值需要恰好 4 个点")
    
    # 提取坐标
    xs = sorted(set(p[0] for p in points))
    ys = sorted(set(p[1] for p in points))
    
    if len(xs) != 2 or len(ys) != 2:
        raise InterpolationError("双线性插值需要 2x2 网格点")
    
    x0, x1 = xs
    y0, y1 = ys
    
    # 创建点映射
    point_map = {(p[0], p[1]): p[2] for p in points}
    
    z00 = point_map[(x0, y0)]
    z10 = point_map[(x1, y0)]
    z01 = point_map[(x0, y1)]
    z11 = point_map[(x1, y1)]
    
    # 双线性插值公式
    if abs(x1 - x0) < 1e-10 or abs(y1 - y0) < 1e-10:
        raise InterpolationError("网格点坐标差异过小")
    
    tx = (x - x0) / (x1 - x0)
    ty = (y - y0) / (y1 - y0)
    
    # 先在 y 方向插值
    z0 = z00 * (1 - tx) + z10 * tx
    z1 = z01 * (1 - tx) + z11 * tx
    
    # 再在 y 方向插值
    return z0 * (1 - ty) + z1 * ty


# ============== 三线性插值 ==============

def trilinear_interpolate(
    points: List[Tuple[Number, Number, Number, Number]], 
    x: Number, 
    y: Number, 
    z: Number
) -> float:
    """
    三线性插值（3D）
    
    在立方体网格的八个角点之间进行三线性插值。
    
    Args:
        points: 八个角点 [(x, y, z, value), ...]
        x: 要插值的 x 坐标
        y: 要插值的 y 坐标
        z: 要插值的 z 坐标
        
    Returns:
        插值结果值
        
    Example:
        >>> points = [
        ...     (0, 0, 0, 0), (1, 0, 0, 1),
        ...     (0, 1, 0, 2), (1, 1, 0, 3),
        ...     (0, 0, 1, 4), (1, 0, 1, 5),
        ...     (0, 1, 1, 6), (1, 1, 1, 7)
        ... ]
        >>> trilinear_interpolate(points, 0.5, 0.5, 0.5)
        3.5
    """
    if len(points) != 8:
        raise InterpolationError("三线性插值需要恰好 8 个点")
    
    # 提取坐标
    xs = sorted(set(p[0] for p in points))
    ys = sorted(set(p[1] for p in points))
    zs = sorted(set(p[2] for p in points))
    
    if len(xs) != 2 or len(ys) != 2 or len(zs) != 2:
        raise InterpolationError("三线性插值需要 2x2x2 网格点")
    
    x0, x1 = xs
    y0, y1 = ys
    z0, z1 = zs
    
    # 创建点映射
    point_map = {(p[0], p[1], p[2]): p[3] for p in points}
    
    # 获取八个角点的值
    v000 = point_map[(x0, y0, z0)]
    v100 = point_map[(x1, y0, z0)]
    v010 = point_map[(x0, y1, z0)]
    v110 = point_map[(x1, y1, z0)]
    v001 = point_map[(x0, y0, z1)]
    v101 = point_map[(x1, y0, z1)]
    v011 = point_map[(x0, y1, z1)]
    v111 = point_map[(x1, y1, z1)]
    
    # 计算插值参数
    if abs(x1 - x0) < 1e-10 or abs(y1 - y0) < 1e-10 or abs(z1 - z0) < 1e-10:
        raise InterpolationError("网格点坐标差异过小")
    
    tx = (x - x0) / (x1 - x0)
    ty = (y - y0) / (y1 - y0)
    tz = (z - z0) / (z1 - z0)
    
    # 三线性插值公式
    c00 = v000 * (1 - tx) + v100 * tx
    c01 = v001 * (1 - tx) + v101 * tx
    c10 = v010 * (1 - tx) + v110 * tx
    c11 = v011 * (1 - tx) + v111 * tx
    
    c0 = c00 * (1 - ty) + c10 * ty
    c1 = c01 * (1 - ty) + c11 * ty
    
    return c0 * (1 - tz) + c1 * tz


# ============== 最近邻插值 ==============

def nearest_neighbor_interpolate(
    points: List[Tuple[Number, Number]], 
    x: Number
) -> float:
    """
    最近邻插值
    
    返回距离最近的点的 y 值。
    
    Args:
        points: 插值点列表 [(x, y), ...]
        x: 要插值的 x 值
        
    Returns:
        最近点的 y 值
        
    Example:
        >>> points = [(0, 0), (1, 1), (2, 4)]
        >>> nearest_neighbor_interpolate(points, 0.4)
        0.0
        >>> nearest_neighbor_interpolate(points, 0.6)
        1.0
    """
    validate_points(points)
    
    min_dist = float('inf')
    nearest_y = None
    
    for px, py in points:
        dist = abs(px - x)
        if dist < min_dist:
            min_dist = dist
            nearest_y = py
    
    return float(nearest_y)


# ============== Akima 插值 ==============

def akima_interpolate(points: List[Tuple[Number, Number]], x: Number) -> float:
    """
    Akima 插值
    
    一种局部插值方法，使用分段三次多项式，
    在数据点处产生平滑的曲线，不会出现 Runge 现象。
    
    Args:
        points: 插值点列表 [(x, y), ...]，至少需要 2 个点
        x: 要插值的 x 值
        
    Returns:
        插值结果 y
        
    Example:
        >>> points = [(0, 0), (1, 1), (2, 0), (3, 1)]
        >>> result = akima_interpolate(points, 1.5)
        >>> isinstance(result, float)
        True
    """
    validate_points(points)
    sorted_points = sort_points(points)
    n = len(sorted_points)
    
    if n < 2:
        raise InterpolationError("Akima 插值至少需要 2 个点")
    
    # 提取 x 和 y
    xs = [p[0] for p in sorted_points]
    ys = [p[1] for p in sorted_points]
    
    # 计算斜率
    slopes = []
    for i in range(n - 1):
        if abs(xs[i + 1] - xs[i]) < 1e-10:
            slopes.append(0.0)
        else:
            slopes.append((ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i]))
    
    # 扩展斜率（用于边界）
    # Akima 方法使用两个额外的斜率
    if n == 2:
        # 只有两个点，使用线性插值
        return linear_interpolate(sorted_points, x)
    
    # 计算端点斜率（Akima 边界处理）
    if len(slopes) >= 2:
        s0 = 2 * slopes[0] - slopes[1]
        s1 = 2 * slopes[-1] - slopes[-2]
    else:
        s0 = slopes[0] if slopes else 0.0
        s1 = slopes[-1] if slopes else 0.0
    
    extended_slopes = [s0] + slopes + [s1]
    
    # 找到包含 x 的区间
    if x <= xs[0]:
        return linear_interpolate(sorted_points, x)
    if x >= xs[-1]:
        return linear_interpolate(sorted_points, x)
    
    for i in range(n - 1):
        if xs[i] <= x <= xs[i + 1]:
            # Akima 权重计算
            s_im2 = extended_slopes[i]
            s_im1 = extended_slopes[i + 1]
            s_i = extended_slopes[i + 2] if i + 2 < len(extended_slopes) else extended_slopes[i + 1]
            s_ip1 = extended_slopes[i + 3] if i + 3 < len(extended_slopes) else extended_slopes[i + 2]
            
            # 计算 Akima 导数
            w1 = abs(s_i - s_im1)
            w2 = abs(s_ip1 - s_im2)
            
            if w1 + w2 < 1e-10:
                # 特殊情况：使用简单平均
                t_i = (s_im1 + s_i) / 2
            else:
                t_i = (w2 * s_im1 + w1 * s_i) / (w1 + w2)
            
            # 下一个点的导数
            s_ip2 = extended_slopes[i + 4] if i + 4 < len(extended_slopes) else s_ip1
            
            w1 = abs(s_ip1 - s_i)
            w2 = abs(s_ip2 - s_im1)
            
            if w1 + w2 < 1e-10:
                t_ip1 = (s_i + s_ip1) / 2
            else:
                t_ip1 = (w2 * s_i + w1 * s_ip1) / (w1 + w2)
            
            # Hermite 插值
            h = xs[i + 1] - xs[i]
            t = (x - xs[i]) / h
            
            h00 = 2 * t ** 3 - 3 * t ** 2 + 1
            h10 = t ** 3 - 2 * t ** 2 + t
            h01 = -2 * t ** 3 + 3 * t ** 2
            h11 = t ** 3 - t ** 2
            
            return h00 * ys[i] + h10 * h * t_i + h01 * ys[i + 1] + h11 * h * t_ip1
    
    # 不应该到达这里
    return linear_interpolate(sorted_points, x)


# ============== 三次样条插值（简化版）==============

def cubic_spline_interpolate(
    points: List[Tuple[Number, Number]], 
    x: Number,
    natural: bool = True
) -> float:
    """
    三次样条插值（简化版）
    
    使用自然边界条件或固定边界条件的样条插值。
    产生平滑的曲线，通过所有数据点。
    
    Args:
        points: 插值点列表 [(x, y), ...]，至少需要 3 个点
        x: 要插值的 x 值
        natural: 是否使用自然边界条件（端点二阶导数为 0）
        
    Returns:
        插值结果 y
        
    Example:
        >>> points = [(0, 0), (1, 1), (2, 0)]
        >>> result = cubic_spline_interpolate(points, 0.5)
        >>> isinstance(result, float)
        True
    """
    validate_points(points)
    sorted_points = sort_points(points)
    n = len(sorted_points)
    
    if n < 3:
        # 点数太少，退化为线性插值
        return linear_interpolate(sorted_points, x)
    
    xs = [p[0] for p in sorted_points]
    ys = [p[1] for p in sorted_points]
    
    # 计算步长
    h = [xs[i + 1] - xs[i] for i in range(n - 1)]
    
    # 构建三对角矩阵求解二阶导数
    # 使用 Thomas 算法（追赶法）
    # 对于自然样条，M[0] = M[n-1] = 0
    
    # 构建方程组右侧
    alpha = [0.0] * n
    for i in range(1, n - 1):
        alpha[i] = 3.0 / h[i] * (ys[i + 1] - ys[i]) - 3.0 / h[i - 1] * (ys[i] - ys[i - 1])
    
    # 构建三对角矩阵
    l = [1.0] + [2.0 * (h[i] + h[i + 1]) for i in range(n - 2)] + [1.0]
    mu = [0.0] + [h[i] / (h[i] + h[i + 1]) for i in range(n - 2)] + [0.0]
    z = [0.0] * n
    
    # 前向消元
    for i in range(1, n):
        l[i] = 2.0 * (xs[min(i + 1, n - 1)] - xs[i - 1]) - h[i - 1] * mu[i - 1]
        if abs(l[i]) < 1e-10:
            l[i] = 1e-10
        mu[i] = h[i] / l[i] if i < n - 1 else 0.0
        z[i] = (alpha[i] - h[i - 1] * z[i - 1]) / l[i]
    
    # 后向回代，计算二阶导数 M
    M = [0.0] * n
    for i in range(n - 2, -1, -1):
        M[i] = z[i] - mu[i] * M[i + 1]
    
    # 找到包含 x 的区间
    if x <= xs[0]:
        return linear_interpolate(sorted_points, x)
    if x >= xs[-1]:
        return linear_interpolate(sorted_points, x)
    
    for i in range(n - 1):
        if xs[i] <= x <= xs[i + 1]:
            # 三次样条公式
            hi = h[i]
            t1 = xs[i + 1] - x
            t2 = x - xs[i]
            
            result = (M[i] * t1 ** 3 + M[i + 1] * t2 ** 3) / (6 * hi)
            result += (ys[i] / hi - M[i] * hi / 6) * t1
            result += (ys[i + 1] / hi - M[i + 1] * hi / 6) * t2
            
            return result
    
    return linear_interpolate(sorted_points, x)


# ============== 多项式拟合 ==============

def polynomial_fit(
    points: List[Tuple[Number, Number]], 
    degree: int
) -> List[float]:
    """
    多项式拟合（最小二乘法）
    
    使用最小二乘法拟合多项式曲线。
    
    Args:
        points: 数据点列表 [(x, y), ...]
        degree: 多项式阶数
        
    Returns:
        多项式系数 [a0, a1, ..., an]，其中 y = a0 + a1*x + ... + an*x^n
        
    Example:
        >>> points = [(0, 1), (1, 2), (2, 5)]
        >>> coeffs = polynomial_fit(points, 2)
        >>> len(coeffs) == 3
        True
    """
    if not points:
        raise InterpolationError("数据点列表不能为空")
    
    n = len(points)
    if degree < 0:
        raise InterpolationError("多项式阶数必须非负")
    if degree >= n:
        raise InterpolationError("多项式阶数必须小于数据点数量")
    
    # 构建范德蒙德矩阵
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    
    # 使用正规方程求解: (A^T * A) * c = A^T * y
    # 构建 A^T * A
    m = degree + 1
    ata = [[0.0] * m for _ in range(m)]
    aty = [0.0] * m
    
    for i in range(m):
        for j in range(m):
            for k in range(n):
                ata[i][j] += xs[k] ** (i + j)
        for k in range(n):
            aty[i] += xs[k] ** i * ys[k]
    
    # 高斯消元求解
    # 复制矩阵以避免修改原矩阵
    aug = [row[:] + [aty[i]] for i, row in enumerate(ata)]
    
    # 前向消元
    for col in range(m):
        # 找主元
        max_row = col
        for row in range(col + 1, m):
            if abs(aug[row][col]) > abs(aug[max_row][col]):
                max_row = row
        aug[col], aug[max_row] = aug[max_row], aug[col]
        
        # 检查是否奇异
        if abs(aug[col][col]) < 1e-10:
            continue
        
        # 消元
        for row in range(col + 1, m):
            factor = aug[row][col] / aug[col][col]
            for j in range(col, m + 1):
                aug[row][j] -= factor * aug[col][j]
    
    # 后向回代
    coeffs = [0.0] * m
    for i in range(m - 1, -1, -1):
        coeffs[i] = aug[i][m]
        for j in range(i + 1, m):
            coeffs[i] -= aug[i][j] * coeffs[j]
        if abs(aug[i][i]) > 1e-10:
            coeffs[i] /= aug[i][i]
    
    return coeffs


def evaluate_polynomial(coeffs: List[float], x: Number) -> float:
    """
    计算多项式值
    
    使用 Horner 方法高效计算多项式值。
    
    Args:
        coeffs: 多项式系数 [a0, a1, ..., an]
        x: 自变量值
        
    Returns:
        多项式值 y
        
    Example:
        >>> coeffs = [1, 2, 1]  # 1 + 2x + x^2
        >>> evaluate_polynomial(coeffs, 3)
        16.0
    """
    result = 0.0
    for coeff in reversed(coeffs):
        result = result * x + coeff
    return result


# ============== 工具类 ==============

class Interpolator:
    """
    插值器类
    
    预处理数据后支持多次插值查询，提高效率。
    
    Example:
        >>> points = [(0, 0), (1, 1), (2, 4)]
        >>> interp = Interpolator(points, method='linear')
        >>> interp.interpolate(0.5)
        0.5
        >>> interp.interpolate(1.5)
        2.5
    """
    
    def __init__(
        self, 
        points: List[Tuple[Number, Number]], 
        method: str = 'linear',
        **kwargs
    ):
        """
        初始化插值器
        
        Args:
            points: 插值点列表 [(x, y), ...]
            method: 插值方法，支持：
                    'linear' - 线性插值（默认）
                    'nearest' - 最近邻插值
                    'lagrange' - 拉格朗日多项式插值
                    'newton' - 牛顿多项式插值
                    'cubic_spline' - 三次样条插值
                    'akima' - Akima 插值
                    'idw' - 反距离加权插值
            **kwargs: 传递给插值方法的额外参数
        """
        validate_points(points)
        self.points = sort_points(points)
        self.method = method
        self.kwargs = kwargs
        
        # 方法映射
        self._methods = {
            'linear': linear_interpolate,
            'nearest': nearest_neighbor_interpolate,
            'lagrange': lagrange_interpolate,
            'newton': newton_interpolate,
            'cubic_spline': cubic_spline_interpolate,
            'akima': akima_interpolate,
            'idw': idw_interpolate,
            'piecewise_linear': piecewise_linear_interpolate,
        }
        
        if method not in self._methods:
            raise InterpolationError(f"不支持的插值方法: {method}")
    
    def interpolate(self, x: Number) -> float:
        """
        执行插值
        
        Args:
            x: 要插值的 x 值
            
        Returns:
            插值结果 y
        """
        func = self._methods[self.method]
        return func(self.points, x, **self.kwargs)
    
    def __call__(self, x: Number) -> float:
        """支持直接调用"""
        return self.interpolate(x)
    
    def interpolate_batch(self, xs: List[Number]) -> List[float]:
        """
        批量插值
        
        Args:
            xs: 要插值的 x 值列表
            
        Returns:
            插值结果列表
        """
        return [self.interpolate(x) for x in xs]


class BilinearInterpolator:
    """
    双线性插值器
    
    用于 2D 网格数据的插值。
    """
    
    def __init__(self, grid_x: List[Number], grid_y: List[Number], values: List[List[Number]]):
        """
        初始化双线性插值器
        
        Args:
            grid_x: x 坐标网格点
            grid_y: y 坐标网格点
            values: 值矩阵 values[i][j] 对应 (grid_x[j], grid_y[i])
        """
        if len(grid_x) < 2 or len(grid_y) < 2:
            raise InterpolationError("网格点数量不足")
        
        if len(values) != len(grid_y) or any(len(row) != len(grid_x) for row in values):
            raise InterpolationError("值矩阵维度与网格不匹配")
        
        self.grid_x = sorted(grid_x)
        self.grid_y = sorted(grid_y)
        self.values = values
    
    def interpolate(self, x: Number, y: Number) -> float:
        """
        执行双线性插值
        
        Args:
            x: x 坐标
            y: y 坐标
            
        Returns:
            插值结果
        """
        # 找到包含 (x, y) 的网格单元
        i = 0
        while i < len(self.grid_x) - 1 and self.grid_x[i + 1] < x:
            i += 1
        if i >= len(self.grid_x) - 1:
            i = len(self.grid_x) - 2
        
        j = 0
        while j < len(self.grid_y) - 1 and self.grid_y[j + 1] < y:
            j += 1
        if j >= len(self.grid_y) - 1:
            j = len(self.grid_y) - 2
        
        x0, x1 = self.grid_x[i], self.grid_x[i + 1]
        y0, y1 = self.grid_y[j], self.grid_y[j + 1]
        
        v00 = self.values[j][i]
        v10 = self.values[j][i + 1]
        v01 = self.values[j + 1][i]
        v11 = self.values[j + 1][i + 1]
        
        # 双线性插值
        tx = (x - x0) / (x1 - x0) if abs(x1 - x0) > 1e-10 else 0.0
        ty = (y - y0) / (y1 - y0) if abs(y1 - y0) > 1e-10 else 0.0
        
        v0 = v00 * (1 - tx) + v10 * tx
        v1 = v01 * (1 - tx) + v11 * tx
        
        return v0 * (1 - ty) + v1 * ty


# ============== 辅助函数 ==============

def find_interpolation_bounds(
    points: List[Tuple[Number, Number]], 
    x: Number
) -> Tuple[int, int]:
    """
    找到包含 x 的区间索引
    
    Args:
        points: 已排序的插值点列表
        x: 要查找的 x 值
        
    Returns:
        区间索引 (i, i+1)，如果 x 在范围外则返回边界索引
    """
    sorted_points = sort_points(points)
    
    if x <= sorted_points[0][0]:
        return (0, 0)
    if x >= sorted_points[-1][0]:
        return (len(sorted_points) - 1, len(sorted_points) - 1)
    
    for i in range(len(sorted_points) - 1):
        if sorted_points[i][0] <= x <= sorted_points[i + 1][0]:
            return (i, i + 1)
    
    return (0, 0)


def interpolate_2d_grid(
    x_coords: List[Number],
    y_coords: List[Number],
    values: List[List[Number]],
    method: str = 'bilinear'
) -> Callable[[Number, Number], float]:
    """
    创建 2D 网格插值函数
    
    Args:
        x_coords: x 坐标数组
        y_coords: y 坐标数组
        values: 值网格 values[i][j] 对应 (x_coords[j], y_coords[i])
        method: 插值方法 ('bilinear' 或 'nearest')
        
    Returns:
        插值函数 f(x, y) -> float
        
    Example:
        >>> x = [0, 1, 2]
        >>> y = [0, 1]
        >>> values = [[0, 1, 2], [1, 2, 3]]
        >>> interp = interpolate_2d_grid(x, y, values)
        >>> interp(0.5, 0.5)
        1.0
    """
    if method == 'bilinear':
        interp = BilinearInterpolator(x_coords, y_coords, values)
        return lambda x, y: interp.interpolate(x, y)
    elif method == 'nearest':
        def nearest(x, y):
            # 找最近的 x 坐标
            xi = min(range(len(x_coords)), key=lambda i: abs(x_coords[i] - x))
            # 找最近的 y 坐标
            yi = min(range(len(y_coords)), key=lambda i: abs(y_coords[i] - y))
            return float(values[yi][xi])
        return nearest
    else:
        raise InterpolationError(f"不支持的 2D 插值方法: {method}")


if __name__ == "__main__":
    # 简单测试
    print("插值工具模块测试")
    print("=" * 50)
    
    # 测试数据
    points = [(0, 0), (1, 1), (2, 4), (3, 9)]
    
    print(f"测试数据: {points}")
    print()
    
    # 线性插值
    print("线性插值:")
    for x in [0.5, 1.5, 2.5]:
        print(f"  f({x}) = {linear_interpolate(points, x)}")
    
    # 拉格朗日插值
    print("\n拉格朗日插值:")
    for x in [0.5, 1.5, 2.5]:
        print(f"  f({x}) = {lagrange_interpolate(points, x):.4f}")
    
    # 牛顿插值
    print("\n牛顿插值:")
    for x in [0.5, 1.5, 2.5]:
        print(f"  f({x}) = {newton_interpolate(points, x):.4f}")
    
    # 最近邻插值
    print("\n最近邻插值:")
    for x in [0.4, 0.6, 1.3]:
        print(f"  f({x}) = {nearest_neighbor_interpolate(points, x)}")
    
    # 反距离加权插值
    print("\n反距离加权插值 (IDW):")
    for x in [0.5, 1.5, 2.5]:
        print(f"  f({x}) = {idw_interpolate(points, x):.4f}")
    
    # 三次样条插值
    print("\n三次样条插值:")
    for x in [0.5, 1.5, 2.5]:
        print(f"  f({x}) = {cubic_spline_interpolate(points, x):.4f}")
    
    # Akima 插值
    print("\nAkima 插值:")
    for x in [0.5, 1.5, 2.5]:
        print(f"  f({x}) = {akima_interpolate(points, x):.4f}")
    
    # 双线性插值
    print("\n双线性插值:")
    bi_points = [(0, 0, 1), (1, 0, 2), (0, 1, 3), (1, 1, 4)]
    print(f"  f(0.5, 0.5) = {bilinear_interpolate(bi_points, 0.5, 0.5)}")
    
    # 多项式拟合
    print("\n多项式拟合 (degree=2):")
    coeffs = polynomial_fit(points[:3], 2)
    print(f"  系数: {coeffs}")
    for x in [0.5, 1, 1.5]:
        print(f"  f({x}) = {evaluate_polynomial(coeffs, x):.4f}")
    
    # Interpolator 类
    print("\nInterpolator 类测试:")
    interp = Interpolator(points, method='linear')
    print(f"  线性: f(1.5) = {interp(1.5)}")
    
    interp = Interpolator(points, method='cubic_spline')
    print(f"  样条: f(1.5) = {interp(1.5):.4f}")
    
    # 批量插值
    results = interp.interpolate_batch([0.5, 1.0, 1.5, 2.0, 2.5])
    print(f"  批量: {[round(r, 2) for r in results]}")
    
    print("\n" + "=" * 50)
    print("测试完成！")