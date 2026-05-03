"""
Geohash 工具模块

Geohash 是一种将经纬度坐标编码为字符串的算法，广泛应用于：
- 地理位置存储和索引
- 地理范围查询
- 地理位置聚合
- 缓存键生成

特点：
- 零外部依赖
- 支持编码/解码
- 支持相邻区域计算
- 支持距离计算
- 支持前缀搜索区域计算

Author: AllToolkit
Date: 2026-05-03
"""

from typing import Tuple, List, Optional
import math

# Base32 编码字符表
BASE32_CHARS = "0123456789bcdefghjkmnpqrstuvwxyz"

# Base32 解码映射
BASE32_DECODE = {char: i for i, char in enumerate(BASE32_CHARS)}


def encode(lat: float, lon: float, precision: int = 12) -> str:
    """
    将经纬度编码为 geohash 字符串
    
    Args:
        lat: 纬度 (-90, 90)
        lon: 经度 (-180, 180)
        precision: 编码精度 (1-12)，默认 12
                   精度越高，表示的位置越精确
                   - 1: ±2500km
                   - 5: ±4.9km
                   - 6: ±1.2km
                   - 12: ±0.0006m
    
    Returns:
        geohash 字符串
    
    Raises:
        ValueError: 坐标超出范围或精度无效
    
    Examples:
        >>> encode(39.9042, 116.4074, 6)
        'wx4g0b'
        >>> encode(31.2304, 121.4737, 6)
        'wtw3sj'
    """
    if not (-90 <= lat <= 90):
        raise ValueError(f"纬度必须在 -90 到 90 之间，当前值: {lat}")
    if not (-180 <= lon <= 180):
        raise ValueError(f"经度必须在 -180 到 180 之间，当前值: {lon}")
    if not (1 <= precision <= 12):
        raise ValueError(f"精度必须在 1 到 12 之间，当前值: {precision}")
    
    # 处理边界情况
    if lat == 90:
        lat = 89.999999
    if lon == 180:
        lon = 179.999999
    
    # 初始化区间
    lat_min, lat_max = -90.0, 90.0
    lon_min, lon_max = -180.0, 180.0
    
    geohash = []
    bit = 0
    ch = 0
    
    while len(geohash) < precision:
        if bit % 2 == 0:
            # 偶数位：经度
            mid = (lon_min + lon_max) / 2
            if lon >= mid:
                ch |= 16 >> (bit % 5)
                lon_min = mid
            else:
                lon_max = mid
        else:
            # 奇数位：纬度
            mid = (lat_min + lat_max) / 2
            if lat >= mid:
                ch |= 16 >> (bit % 5)
                lat_min = mid
            else:
                lat_max = mid
        
        bit += 1
        
        if bit % 5 == 0:
            geohash.append(BASE32_CHARS[ch])
            ch = 0
    
    return ''.join(geohash)


def decode(geohash: str) -> Tuple[Tuple[float, float], Tuple[float, float, float, float]]:
    """
    将 geohash 字符串解码为经纬度
    
    Args:
        geohash: geohash 字符串
    
    Returns:
        ((lat, lon), (lat_min, lat_max, lon_min, lon_max))
        - 第一个元组是中心点坐标
        - 第二个元组是边界框坐标
    
    Raises:
        ValueError: geohash 字符串无效
    
    Examples:
        >>> decode('wx4g0b')
        ((39.9042..., 116.4074...), (39.9033..., 39.9050..., 116.4062..., 116.4086...))
    """
    if not geohash:
        raise ValueError("geohash 不能为空")
    
    for char in geohash:
        if char not in BASE32_DECODE:
            raise ValueError(f"无效的 geohash 字符: {char}")
    
    # 初始化区间
    lat_min, lat_max = -90.0, 90.0
    lon_min, lon_max = -180.0, 180.0
    
    bit = 0
    for char in geohash:
        ch = BASE32_DECODE[char]
        
        for i in range(5):
            mask = 16 >> i
            
            if bit % 2 == 0:
                # 偶数位：经度
                mid = (lon_min + lon_max) / 2
                if ch & mask:
                    lon_min = mid
                else:
                    lon_max = mid
            else:
                # 奇数位：纬度
                mid = (lat_min + lat_max) / 2
                if ch & mask:
                    lat_min = mid
                else:
                    lat_max = mid
            
            bit += 1
    
    # 计算中心点
    lat = (lat_min + lat_max) / 2
    lon = (lon_min + lon_max) / 2
    
    return ((lat, lon), (lat_min, lat_max, lon_min, lon_max))


def get_neighbors(geohash: str) -> List[str]:
    """
    获取 geohash 周围 8 个相邻区域的 geohash
    
    Args:
        geohash: geohash 字符串
    
    Returns:
        相邻 8 个 geohash 的列表，顺序为：
        [n, ne, e, se, s, sw, w, nw]
    
    Raises:
        ValueError: geohash 字符串无效
    
    Examples:
        >>> get_neighbors('wx4g0b')
        ['wx4g0c', 'wx4g12', 'wx4g10', 'wx4g14', 'wx4g09', 'wx4g08', 'wx4g02', 'wx4g03']
    """
    if not geohash:
        raise ValueError("geohash 不能为空")
    
    # 方向偏移量：北、东、南、西
    # 在 geohash 网格中的偏移
    directions = {
        'n': (1, 0),
        's': (-1, 0),
        'e': (0, 1),
        'w': (0, -1)
    }
    
    # 获取相邻方向
    def get_adjacent(gh: str, direction: str) -> str:
        """获取指定方向的相邻 geohash"""
        lat_min, lat_max, lon_min, lon_max = decode(gh)[1]
        
        # 计算中心点
        lat = (lat_min + lat_max) / 2
        lon = (lon_min + lon_max) / 2
        
        # 计算跨度
        lat_span = lat_max - lat_min
        lon_span = lon_max - lon_min
        
        # 根据方向偏移
        dy, dx = directions[direction]
        new_lat = lat + dy * lat_span
        new_lon = lon + dx * lon_span
        
        # 处理边界跨越
        if new_lat > 90:
            new_lat = 90 - (new_lat - 90)
        if new_lat < -90:
            new_lat = -90 - (new_lat + 90)
        if new_lon > 180:
            new_lon = new_lon - 360
        if new_lon < -180:
            new_lon = new_lon + 360
        
        return encode(new_lat, new_lon, len(gh))
    
    # 计算 8 个相邻区域
    n = get_adjacent(geohash, 'n')
    s = get_adjacent(geohash, 's')
    e = get_adjacent(geohash, 'e')
    w = get_adjacent(geohash, 'w')
    
    ne = get_adjacent(n, 'e')
    nw = get_adjacent(n, 'w')
    se = get_adjacent(s, 'e')
    sw = get_adjacent(s, 'w')
    
    return [n, ne, e, se, s, sw, w, nw]


def distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    计算两个地理点之间的距离（使用 Haversine 公式）
    
    Args:
        lat1: 第一个点的纬度
        lon1: 第一个点的经度
        lat2: 第二个点的纬度
        lon2: 第二个点的经度
    
    Returns:
        两点之间的距离（单位：千米）
    
    Examples:
        >>> distance(39.9042, 116.4074, 31.2304, 121.4737)
        1068.5...
    """
    # 地球半径（千米）
    R = 6371.0
    
    # 转换为弧度
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    lon1_rad = math.radians(lon1)
    lon2_rad = math.radians(lon2)
    
    # 差值
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine 公式
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


def get_precision_meters(precision: int) -> float:
    """
    获取指定精度的误差范围（单位：米）
    
    Args:
        precision: geohash 精度 (1-12)
    
    Returns:
        误差范围（米），取纬度和经度方向的最大值
    
    Examples:
        >>> get_precision_meters(6)
        1229.76...
    """
    # 各精度对应的误差范围（单位：度）
    # 精度每增加 1，误差大约缩小 32 倍（实际上是 2^5）
    precision_error = {
        1: 2500000,
        2: 630000,
        3: 78000,
        4: 20000,
        5: 2400,
        6: 610,
        7: 76,
        8: 19,
        9: 2.4,
        10: 0.6,
        11: 0.074,
        12: 0.019
    }
    
    return precision_error.get(precision, 0.019)


def get_bounding_box(lat: float, lon: float, radius_km: float) -> Tuple[float, float, float, float]:
    """
    根据中心点和半径计算边界框
    
    Args:
        lat: 中心点纬度
        lon: 中心点经度
        radius_km: 半径（千米）
    
    Returns:
        (lat_min, lat_max, lon_min, lon_max)
    
    Examples:
        >>> get_bounding_box(39.9042, 116.4074, 10)
        (39.8142..., 39.9942..., 116.2624..., 116.5524...)
    """
    # 地球半径（千米）
    R = 6371.0
    
    # 纬度方向的角度变化
    lat_delta = math.degrees(radius_km / R)
    
    # 经度方向的角度变化（考虑纬度）
    lon_delta = math.degrees(radius_km / (R * math.cos(math.radians(lat))))
    
    lat_min = max(-90, lat - lat_delta)
    lat_max = min(90, lat + lat_delta)
    lon_min = max(-180, lon - lon_delta)
    lon_max = min(180, lon + lon_delta)
    
    return (lat_min, lat_max, lon_min, lon_max)


def get_geohashes_in_radius(lat: float, lon: float, radius_km: float, precision: int = 6) -> List[str]:
    """
    获取指定半径范围内的所有 geohash
    
    Args:
        lat: 中心点纬度
        lon: 中心点经度
        radius_km: 搜索半径（千米）
        precision: geohash 精度
    
    Returns:
        范围内的 geohash 列表
    
    Examples:
        >>> len(get_geohashes_in_radius(39.9042, 116.4074, 5, 5))
        9
    """
    # 获取边界框
    lat_min, lat_max, lon_min, lon_max = get_bounding_box(lat, lon, radius_km)
    
    # 计算精度对应的单元格大小
    cell_size = get_precision_meters(precision) / 1000  # 转换为千米
    
    # 生成所有 geohash
    geohashes = set()
    
    # 步长（使用单元格大小的一部分来确保覆盖）
    lat_step = cell_size / 111.0  # 1度纬度约等于111公里
    lon_step = cell_size / (111.0 * math.cos(math.radians(lat)))  # 根据纬度调整经度步长
    
    current_lat = lat_min
    while current_lat <= lat_max:
        current_lon = lon_min
        while current_lon <= lon_max:
            gh = encode(current_lat, current_lon, precision)
            geohashes.add(gh)
            current_lon += lon_step
        current_lat += lat_step
    
    return list(geohashes)


def is_valid(geohash: str) -> bool:
    """
    检查 geohash 字符串是否有效
    
    Args:
        geohash: geohash 字符串
    
    Returns:
        True 如果有效，False 否则
    
    Examples:
        >>> is_valid('wx4g0b')
        True
        >>> is_valid('wx4g0bi')  # 包含无效字符 'i'
        False
    """
    if not geohash:
        return False
    
    return all(char in BASE32_DECODE for char in geohash)


def common_prefix(geohashes: List[str]) -> str:
    """
    计算多个 geohash 的公共前缀
    
    公共前缀越长，表示这些点在地理上越接近
    
    Args:
        geohashes: geohash 字符串列表
    
    Returns:
        公共前缀字符串
    
    Examples:
        >>> common_prefix(['wx4g0b', 'wx4g0c', 'wx4g0d'])
        'wx4g0'
    """
    if not geohashes:
        return ""
    
    prefix = geohashes[0]
    for gh in geohashes[1:]:
        # 找到公共前缀
        i = 0
        while i < min(len(prefix), len(gh)) and prefix[i] == gh[i]:
            i += 1
        prefix = prefix[:i]
        
        if not prefix:
            break
    
    return prefix


def get_center(geohashes: List[str]) -> Tuple[float, float]:
    """
    计算多个 geohash 的中心点
    
    Args:
        geohashes: geohash 字符串列表
    
    Returns:
        (lat, lon) 中心点坐标
    
    Examples:
        >>> get_center(['wx4g0b', 'wx4g0c'])
        (39.904..., 116.407...)
    """
    if not geohashes:
        raise ValueError("geohashes 列表不能为空")
    
    lats = []
    lons = []
    
    for gh in geohashes:
        (lat, lon), _ = decode(gh)
        lats.append(lat)
        lons.append(lon)
    
    return (sum(lats) / len(lats), sum(lons) / len(lons))


# 便捷类
class Geohash:
    """
    Geohash 对象，提供面向对象的接口
    
    Examples:
        >>> gh = Geohash(39.9042, 116.4074, precision=6)
        >>> gh.hash
        'wx4g0b'
        >>> gh.neighbors
        ['wx4g0c', 'wx4g12', ...]
    """
    
    def __init__(self, lat: float, lon: float, precision: int = 12):
        """
        初始化 Geohash 对象
        
        Args:
            lat: 纬度
            lon: 经度
            precision: 精度
        """
        self._lat = lat
        self._lon = lon
        self._precision = precision
        self._hash = encode(lat, lon, precision)
        self._neighbors: Optional[List[str]] = None
        self._bounds: Optional[Tuple[float, float, float, float]] = None
    
    @property
    def hash(self) -> str:
        """geohash 字符串"""
        return self._hash
    
    @property
    def lat(self) -> float:
        """纬度"""
        return self._lat
    
    @property
    def lon(self) -> float:
        """经度"""
        return self._lon
    
    @property
    def precision(self) -> int:
        """精度"""
        return self._precision
    
    @property
    def neighbors(self) -> List[str]:
        """相邻 8 个区域的 geohash"""
        if self._neighbors is None:
            self._neighbors = get_neighbors(self._hash)
        return self._neighbors
    
    @property
    def bounds(self) -> Tuple[float, float, float, float]:
        """边界框 (lat_min, lat_max, lon_min, lon_max)"""
        if self._bounds is None:
            _, bounds = decode(self._hash)
            self._bounds = bounds
        return self._bounds
    
    @property
    def center(self) -> Tuple[float, float]:
        """中心点坐标"""
        return (self._lat, self._lon)
    
    def distance_to(self, other: 'Geohash') -> float:
        """
        计算到另一个 Geohash 的距离
        
        Args:
            other: 另一个 Geohash 对象
        
        Returns:
            距离（千米）
        """
        return distance(self._lat, self._lon, other._lat, other._lon)
    
    def contains(self, lat: float, lon: float) -> bool:
        """
        检查指定的坐标是否在当前 geohash 范围内
        
        Args:
            lat: 纬度
            lon: 经度
        
        Returns:
            True 如果在范围内
        """
        lat_min, lat_max, lon_min, lon_max = self.bounds
        return lat_min <= lat <= lat_max and lon_min <= lon <= lon_max
    
    @classmethod
    def from_hash(cls, geohash: str) -> 'Geohash':
        """
        从 geohash 字符串创建对象
        
        Args:
            geohash: geohash 字符串
        
        Returns:
            Geohash 对象
        """
        (lat, lon), _ = decode(geohash)
        return cls(lat, lon, precision=len(geohash))
    
    def __repr__(self) -> str:
        return f"Geohash('{self._hash}', lat={self._lat:.6f}, lon={self._lon:.6f})"
    
    def __str__(self) -> str:
        return self._hash
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Geohash):
            return self._hash == other._hash
        if isinstance(other, str):
            return self._hash == other
        return False
    
    def __hash__(self) -> int:
        return hash(self._hash)
    
    def __len__(self) -> int:
        return len(self._hash)