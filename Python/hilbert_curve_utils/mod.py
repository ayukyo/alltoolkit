"""
希尔伯特曲线工具模块 (Hilbert Curve Utils)

提供希尔伯特曲线编码/解码功能，支持将多维坐标映射到一维希尔伯特索引，
以及从索引还原坐标。广泛应用于空间索引、数据库优化、图像处理等领域。

希尔伯特曲线特点：
- 间局部性：相邻的索引值对应的空间位置也相邻
- 连续性：曲线连续穿过空间中的每个点
- 可逆性：坐标和索引之间可以双向转换

Author: AllToolkit
Date: 2026-04-30
"""

from typing import List, Tuple, Optional


class HilbertCurve:
    """
    希尔伯特曲线类
    
    使用经典算法实现希尔伯特曲线编码/解码。
    参考: Wikipedia - Hilbert curve
    
    Attributes:
        dimension: 维度
        order: 曲线阶数
        num_points: 曲线上的总点数
    """
    
    def __init__(self, dimension: int, order: int):
        if dimension < 2:
            raise ValueError(f"维度必须 >= 2")
        if order < 1:
            raise ValueError(f"阶数必须 >= 1")
        
        self.dimension = dimension
        self.order = order
        self.num_points = (1 << order) ** dimension
        self.max_coordinate = (1 << order) - 1
    
    def point_from_distance(self, distance: int) -> Tuple[int, ...]:
        """将距离转换为坐标"""
        if distance < 0 or distance >= self.num_points:
            raise ValueError(f"距离超出范围")
        return self._decode(distance)
    
    def distance_from_point(self, point: Tuple[int, ...]) -> int:
        """将坐标转换为距离"""
        if len(point) != self.dimension:
            raise ValueError(f"点维度不匹配")
        for i, coord in enumerate(point):
            if coord < 0 or coord > self.max_coordinate:
                raise ValueError(f"坐标超出范围")
        return self._encode(point)
    
    def _encode(self, point: Tuple[int, ...]) -> int:
        """希尔伯特编码"""
        if self.dimension == 2:
            return self._encode_2d(point[0], point[1])
        return self._encode_nd(list(point))
    
    def _decode(self, distance: int) -> Tuple[int, ...]:
        """希尔伯特解码"""
        if self.dimension == 2:
            x, y = self._decode_2d(distance)
            return (x, y)
        return self._decode_nd(distance)
    
    # ===== 2D 经典算法 (Wikipedia Hilbert Curve) =====
    
    def _encode_2d(self, x: int, y: int) -> int:
        """
        2D 希尔伯特编码 - Wikipedia 经典算法
        
        Convert (x,y) to d
        参考: https://en.wikipedia.org/wiki/Hilbert_curve
        """
        n = 1 << self.order  # 2^order
        d = 0
        s = n >> 1
        
        xi = x
        yi = y
        
        while s > 0:
            rx = (xi & s) > 0
            ry = (yi & s) > 0
            
            d += s * s * ((3 * rx) ^ ry)
            
            # 旋转/翻转
            if ry == 0:
                if rx == 1:
                    xi = s - 1 - xi
                    yi = s - 1 - yi
                # 交换 x 和 y
                xi, yi = yi, xi
            
            s >>= 1
        
        return d
    
    def _decode_2d(self, d: int) -> Tuple[int, int]:
        """
        2D 希尔伯特解码 - Wikipedia 经典算法
        
        Convert d to (x,y)
        参考: https://en.wikipedia.org/wiki/Hilbert_curve
        """
        n = 1 << self.order  # 2^order
        x = 0
        y = 0
        s = 1
        t = d
        
        while s < n:
            rx = 1 & (t // 2)
            ry = 1 & (t ^ rx)
            
            # 旋转/翻转
            if ry == 0:
                if rx == 1:
                    x = s - 1 - x
                    y = s - 1 - y
                # 交换 x 和 y
                x, y = y, x
            
            x += s * rx
            y += s * ry
            t //= 4
            s <<= 1
        
        return x, y
    
    def _encode_nd(self, X: List[int]) -> int:
        """N维编码"""
        h = 0
        
        for i in range(self.order):
            # 提取当前位
            bits = 0
            for j in range(self.dimension):
                bits |= ((X[j] >> (self.order - 1 - i)) & 1) << j
            
            # 格雷码
            bits = bits ^ (bits >> 1)
            
            h = (h << self.dimension) | bits
        
        return h
    
    def _decode_nd(self, h: int) -> Tuple[int, ...]:
        """N维解码"""
        X = [0] * self.dimension
        
        for i in range(self.order):
            bits = (h >> (self.order - 1 - i) * self.dimension) & ((1 << self.dimension) - 1)
            
            # 反格雷码
            temp = bits
            while temp:
                bits ^= temp
                temp >>= 1
            
            for j in range(self.dimension):
                X[j] |= ((bits >> j) & 1) << (self.order - 1 - i)
        
        return tuple(X)
    
    def get_neighbors(self, point: Tuple[int, ...]) -> List[Tuple[int, ...]]:
        """获取相邻点"""
        neighbors = []
        for i in range(self.dimension):
            if point[i] > 0:
                neighbors.append(tuple(point[j] - 1 if j == i else point[j] for j in range(self.dimension)))
            if point[i] < self.max_coordinate:
                neighbors.append(tuple(point[j] + 1 if j == i else point[j] for j in range(self.dimension)))
        return neighbors
    
    def get_hilbert_neighbors(self, distance: int) -> List[int]:
        """获取希尔伯特邻居"""
        neighbors = []
        if distance > 0:
            neighbors.append(distance - 1)
        if distance < self.num_points - 1:
            neighbors.append(distance + 1)
        return neighbors
    
    def get_bounding_box(self, distances: List[int]) -> Tuple[Tuple[int, ...], Tuple[int, ...]]:
        """计算包围盒"""
        if not distances:
            raise ValueError("距离列表为空")
        points = [self.point_from_distance(d) for d in distances]
        min_coords = list(points[0])
        max_coords = list(points[0])
        for point in points[1:]:
            for i in range(self.dimension):
                min_coords[i] = min(min_coords[i], point[i])
                max_coords[i] = max(max_coords[i], point[i])
        return tuple(min_coords), tuple(max_coords)
    
    def get_distances_in_range(self, center: Tuple[int, ...], radius: int) -> List[int]:
        """范围搜索"""
        distances = []
        self._range_search(center, radius, [0] * self.dimension, 0, distances)
        return sorted(distances)
    
    def _range_search(self, center: Tuple[int, ...], radius: int, 
                      current: List[int], dim: int, distances: List[int]):
        if dim == self.dimension:
            manhattan = sum(abs(current[i] - center[i]) for i in range(self.dimension))
            if manhattan <= radius:
                distances.append(self.distance_from_point(tuple(current)))
            return
        for coord in range(self.max_coordinate + 1):
            if abs(coord - center[dim]) > radius:
                continue
            current[dim] = coord
            self._range_search(center, radius, current, dim + 1, distances)
    
    def visualize_2d(self, max_points: int = 64) -> str:
        """可视化"""
        if self.dimension != 2:
            raise ValueError("仅支持 2D")
        grid_size = 1 << self.order
        grid = [[' ' for _ in range(grid_size * 2 - 1)] for _ in range(grid_size)]
        n = min(self.num_points, max_points)
        for i in range(n):
            x, y = self.point_from_distance(i)
            grid[y][x * 2] = '*'
            if i > 0:
                px, py = self.point_from_distance(i - 1)
                if px == x:
                    for yi in range(min(py, y) + 1, max(py, y)):
                        grid[yi][x * 2] = '|'
                else:
                    for xi in range(min(px, x) + 1, max(px, x)):
                        grid[y][xi * 2] = '-'
        return '\n'.join(''.join(row) for row in grid)
    
    def __repr__(self) -> str:
        return f"HilbertCurve(dimension={self.dimension}, order={self.order}, num_points={self.num_points})"


# ===== 便捷函数 =====

def hilbert_encode_2d(x: int, y: int, order: int) -> int:
    """2D 编码"""
    curve = HilbertCurve(dimension=2, order=order)
    return curve.distance_from_point((x, y))


def hilbert_decode_2d(distance: int, order: int) -> Tuple[int, int]:
    """2D 解码"""
    curve = HilbertCurve(dimension=2, order=order)
    point = curve.point_from_distance(distance)
    return point[0], point[1]


def hilbert_encode_3d(x: int, y: int, z: int, order: int) -> int:
    """3D 编码"""
    curve = HilbertCurve(dimension=3, order=order)
    return curve.distance_from_point((x, y, z))


def hilbert_decode_3d(distance: int, order: int) -> Tuple[int, int, int]:
    """3D 解码"""
    curve = HilbertCurve(dimension=3, order=order)
    point = curve.point_from_distance(distance)
    return point[0], point[1], point[2]


def normalize_coordinate(coord: float, min_val: float, max_val: float, order: int) -> int:
    """归一化"""
    if max_val <= min_val:
        raise ValueError("范围无效")
    max_grid = (1 << order) - 1
    norm = (coord - min_val) / (max_val - min_val)
    return min(max_grid, max(0, int(norm * (max_grid + 1))))


def denormalize_coordinate(grid_coord: int, min_val: float, max_val: float, order: int) -> float:
    """反归一化"""
    max_grid = (1 << order) - 1
    norm = grid_coord / max_grid
    return min_val + norm * (max_val - min_val)


def compute_curve_length(order: int, dimension: int = 2) -> int:
    """曲线长度"""
    return (1 << order) ** dimension


def get_curve_segment(curve: HilbertCurve, start: int, end: int) -> List[Tuple[int, ...]]:
    """曲线片段"""
    if start < 0 or end >= curve.num_points or start > end:
        raise ValueError("范围无效")
    return [curve.point_from_distance(d) for d in range(start, end + 1)]


def hilbert_sort(points: List[Tuple[int, ...]], order: int) -> List[Tuple[int, ...]]:
    """希尔伯特排序"""
    if not points:
        return []
    dim = len(points[0])
    curve = HilbertCurve(dimension=dim, order=order)
    result = [(p, curve.distance_from_point(p)) for p in points]
    result.sort(key=lambda x: x[1])
    return [p for p, _ in result]


def hilbert_index_for_geo(lat: float, lon: float, 
                          lat_range: Tuple[float, float] = (-90.0, 90.0),
                          lon_range: Tuple[float, float] = (-180.0, 180.0),
                          order: int = 16) -> int:
    """地理索引"""
    x = normalize_coordinate(lon, lon_range[0], lon_range[1], order)
    y = normalize_coordinate(lat, lat_range[0], lat_range[1], order)
    return hilbert_encode_2d(x, y, order)


def geo_from_hilbert_index(index: int, order: int = 16,
                           lat_range: Tuple[float, float] = (-90.0, 90.0),
                           lon_range: Tuple[float, float] = (-180.0, 180.0)) -> Tuple[float, float]:
    """还原地理坐标"""
    x, y = hilbert_decode_2d(index, order)
    lon = denormalize_coordinate(x, lon_range[0], lon_range[1], order)
    lat = denormalize_coordinate(y, lat_range[0], lat_range[1], order)
    return lat, lon


class HilbertIndex:
    """希尔伯特索引"""
    
    def __init__(self, dimension: int, order: int):
        self.curve = HilbertCurve(dimension, order)
        self.dimension = dimension
        self.order = order
        self._data = {}
    
    def insert(self, point: Tuple[int, ...], data: any) -> None:
        d = self.curve.distance_from_point(point)
        if d not in self._data:
            self._data[d] = []
        self._data[d].append(data)
    
    def query_point(self, point: Tuple[int, ...]) -> List[any]:
        d = self.curve.distance_from_point(point)
        return self._data.get(d, [])
    
    def query_range(self, min_point: Tuple[int, ...], max_point: Tuple[int, ...]) -> List[any]:
        distances = set()
        self._range_query(min_point, max_point, [0] * self.dimension, 0, distances)
        result = []
        for d in distances:
            if d in self._data:
                result.extend(self._data[d])
        return result
    
    def _range_query(self, min_p: Tuple[int, ...], max_p: Tuple[int, ...], 
                     curr: List[int], dim: int, dists: set):
        if dim == self.dimension:
            dists.add(self.curve.distance_from_point(tuple(curr)))
            return
        for c in range(min_p[dim], max_p[dim] + 1):
            if c > self.curve.max_coordinate:
                break
            curr[dim] = c
            self._range_query(min_p, max_p, curr, dim + 1, dists)
    
    def get_nearby(self, point: Tuple[int, ...], radius: int) -> List[Tuple[int, any]]:
        dists = self.curve.get_distances_in_range(point, radius)
        result = []
        for d in dists:
            if d in self._data:
                for item in self._data[d]:
                    result.append((d, item))
        return result
    
    def get_sorted_data(self) -> List[Tuple[int, List[any]]]:
        return sorted(self._data.items())
    
    def __len__(self) -> int:
        return sum(len(v) for v in self._data.values())
    
    def __repr__(self) -> str:
        return f"HilbertIndex(dimension={self.dimension}, order={self.order}, points={len(self)})"


__all__ = [
    'HilbertCurve', 'HilbertIndex',
    'hilbert_encode_2d', 'hilbert_decode_2d',
    'hilbert_encode_3d', 'hilbert_decode_3d',
    'normalize_coordinate', 'denormalize_coordinate',
    'compute_curve_length', 'get_curve_segment',
    'hilbert_sort', 'hilbert_index_for_geo', 'geo_from_hilbert_index',
]