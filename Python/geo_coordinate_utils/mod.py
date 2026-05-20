"""
地理坐标工具模块 (Geo Coordinate Utils)

提供坐标格式转换、距离计算、方位角计算等功能。
零外部依赖，纯 Python 实现。

功能列表：
- DMS（度分秒）与 Decimal（十进制度）格式互转
- Haversine 距离计算（两点间球面距离）
- 方位角计算（从一个点到另一个点的方向）
- 边界框计算（给定中心和半径）
- 坐标解析（支持多种输入格式）
- 坐标验证
"""

import math
import re
from typing import Tuple, Optional, List, Dict, Any
from dataclasses import dataclass


@dataclass
class Coordinate:
    """坐标数据类"""
    latitude: float
    longitude: float
    
    def __post_init__(self):
        """验证坐标范围"""
        if not -90 <= self.latitude <= 90:
            raise ValueError(f"纬度必须在 -90 到 90 之间，当前值: {self.latitude}")
        if not -180 <= self.longitude <= 180:
            raise ValueError(f"经度必须在 -180 到 180 之间，当前值: {self.longitude}")
    
    @property
    def is_valid(self) -> bool:
        """检查坐标是否有效"""
        return -90 <= self.latitude <= 90 and -180 <= self.longitude <= 180
    
    def to_dms(self) -> Tuple[str, str]:
        """转换为DMS格式"""
        return (
            decimal_to_dms(self.latitude, is_latitude=True),
            decimal_to_dms(self.longitude, is_latitude=False)
        )
    
    def __repr__(self) -> str:
        lat_dir = "N" if self.latitude >= 0 else "S"
        lon_dir = "E" if self.longitude >= 0 else "W"
        return f"Coordinate({abs(self.latitude):.6f}°{lat_dir}, {abs(self.longitude):.6f}°{lon_dir})"


# ==================== 格式转换 ====================

def decimal_to_dms(decimal: float, is_latitude: bool = True) -> str:
    """
    将十进制度转换为度分秒格式
    
    Args:
        decimal: 十进制度数值
        is_latitude: 是否为纬度（True=纬度，False=经度）
    
    Returns:
        度分秒格式字符串，如 "39°54'30.12\"N"
    
    Example:
        >>> decimal_to_dms(39.9084, is_latitude=True)
        "39°54'30.24\\"N"
    """
    direction = ""
    if is_latitude:
        direction = "N" if decimal >= 0 else "S"
    else:
        direction = "E" if decimal >= 0 else "W"
    
    decimal = abs(decimal)
    degrees = int(decimal)
    minutes_decimal = (decimal - degrees) * 60
    minutes = int(minutes_decimal)
    seconds = (minutes_decimal - minutes) * 60
    
    return f'{degrees}°{minutes}\'{seconds:.2f}"{direction}'


def dms_to_decimal(dms: str) -> float:
    """
    将度分秒格式转换为十进制度
    
    支持多种格式：
    - "39°54'30\"N"
    - "39°54'30.12N"
    - "39 54 30 N"
    - "N39°54'30\""
    
    Args:
        dms: 度分秒格式字符串
    
    Returns:
        十进制度数值
    
    Example:
        >>> dms_to_decimal("39°54'30\"N")
        39.90833333333333
        >>> dms_to_decimal("116°23'50\"E")
        116.39722222222222
    """
    dms = dms.strip().upper()
    
    # 提取方向
    direction = None
    for char in "NSEW":
        if char in dms:
            direction = char
            dms = dms.replace(char, "")
            break
    
    # 清理并分割
    dms = dms.replace("°", " ").replace("'", " ").replace('"', " ").strip()
    parts = dms.split()
    
    if len(parts) < 1:
        raise ValueError(f"无法解析DMS格式: {dms}")
    
    degrees = float(parts[0])
    minutes = float(parts[1]) if len(parts) > 1 else 0
    seconds = float(parts[2]) if len(parts) > 2 else 0
    
    decimal = degrees + minutes / 60 + seconds / 3600
    
    # 应用方向
    if direction in ("S", "W"):
        decimal = -decimal
    
    return decimal


def parse_coordinate(lat_str: str, lon_str: str) -> Coordinate:
    """
    解析坐标字符串，自动识别格式
    
    支持格式：
    - 十进制: "39.9084", "116.3972"
    - DMS: "39°54'30\"N", "116°23'50\"E"
    - 带方向: "N39.9084", "E116.3972"
    
    Args:
        lat_str: 纬度字符串
        lon_str: 经度字符串
    
    Returns:
        Coordinate 对象
    
    Example:
        >>> parse_coordinate("39.9084", "116.3972")
        Coordinate(39.908400°N, 116.397200°E)
        >>> parse_coordinate("39°54'30\"N", "116°23'50\"E")
        Coordinate(39.908333°N, 116.397222°E)
    """
    def parse_single(s: str, is_latitude: bool) -> float:
        s = s.strip().upper()
        
        # 检查是否为DMS格式
        if "°" in s or "'" in s:
            return dms_to_decimal(s)
        
        # 检查方向前缀/后缀
        direction = None
        for char in "NSEW":
            if char in s:
                direction = char
                s = s.replace(char, "")
                break
        
        decimal = float(s.strip())
        
        # 应用方向
        if direction == "S" or direction == "W":
            decimal = -decimal
        
        return decimal
    
    lat = parse_single(lat_str, is_latitude=True)
    lon = parse_single(lon_str, is_latitude=False)
    
    return Coordinate(lat, lon)


# ==================== 距离和方位计算 ====================

# 地球半径（千米）
EARTH_RADIUS_KM = 6371.0
EARTH_RADIUS_MILES = 3958.8
EARTH_RADIUS_METERS = 6371000.0


def haversine_distance(
    coord1: Coordinate,
    coord2: Coordinate,
    unit: str = "km"
) -> float:
    """
    使用 Haversine 公式计算两点间的球面距离
    
    Args:
        coord1: 起点坐标
        coord2: 终点坐标
        unit: 距离单位 ("km", "mile", "m", "nmi"-海里)
    
    Returns:
        两点间距离
    
    Example:
        >>> beijing = Coordinate(39.9042, 116.4074)
        >>> shanghai = Coordinate(31.2304, 121.4737)
        >>> haversine_distance(beijing, shanghai)
        1068.0 (约)
    """
    lat1, lon1 = math.radians(coord1.latitude), math.radians(coord1.longitude)
    lat2, lon2 = math.radians(coord2.latitude), math.radians(coord2.longitude)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    
    # 选择地球半径
    if unit == "km":
        radius = EARTH_RADIUS_KM
    elif unit == "mile":
        radius = EARTH_RADIUS_MILES
    elif unit == "m":
        radius = EARTH_RADIUS_METERS
    elif unit == "nmi":  # 海里
        radius = EARTH_RADIUS_KM / 1.852
    else:
        radius = EARTH_RADIUS_KM
    
    return radius * c


def bearing(coord1: Coordinate, coord2: Coordinate) -> float:
    """
    计算从 coord1 到 coord2 的方位角（初始方位角）
    
    Args:
        coord1: 起点
        coord2: 终点
    
    Returns:
        方位角（度），范围 0-360，正北为0，顺时针方向
    
    Example:
        >>> bearing(Coordinate(0, 0), Coordinate(1, 0))  # 正北
        0.0
        >>> bearing(Coordinate(0, 0), Coordinate(0, 1))  # 正东
        90.0
    """
    lat1 = math.radians(coord1.latitude)
    lat2 = math.radians(coord2.latitude)
    dlon = math.radians(coord2.longitude - coord1.longitude)
    
    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    
    initial_bearing = math.atan2(x, y)
    initial_bearing = math.degrees(initial_bearing)
    
    # 转换为0-360范围
    compass_bearing = (initial_bearing + 360) % 360
    
    return compass_bearing


def bearing_to_direction(bearing_deg: float) -> str:
    """
    将方位角转换为方向描述
    
    Args:
        bearing_deg: 方位角（度）
    
    Returns:
        方向描述，如 "北", "东北", "东" 等
    
    Example:
        >>> bearing_to_direction(0)
        "北"
        >>> bearing_to_direction(45)
        "东北"
        >>> bearing_to_direction(225)
        "西南"
    """
    directions = [
        ("北", 0, 22.5),
        ("东北", 22.5, 67.5),
        ("东", 67.5, 112.5),
        ("东南", 112.5, 157.5),
        ("南", 157.5, 202.5),
        ("西南", 202.5, 247.5),
        ("西", 247.5, 292.5),
        ("西北", 292.5, 337.5),
        ("北", 337.5, 360),
    ]
    
    for direction, low, high in directions:
        if low <= bearing_deg < high:
            return direction
    
    return "北"


def destination_point(
    start: Coordinate,
    distance: float,
    bearing_deg: float,
    unit: str = "km"
) -> Coordinate:
    """
    根据起点、距离和方位角计算终点坐标
    
    Args:
        start: 起点坐标
        distance: 距离
        bearing_deg: 方位角（度）
        unit: 距离单位 ("km", "mile", "m", "nmi")
    
    Returns:
        终点坐标
    
    Example:
        >>> start = Coordinate(39.9042, 116.4074)  # 北京
        >>> destination_point(start, 100, 180)  # 向南100公里
        Coordinate 约 (39.0°N, 116.4°E)
    """
    # 转换距离单位为公里
    if unit == "mile":
        distance = distance * 1.60934
    elif unit == "m":
        distance = distance / 1000
    elif unit == "nmi":
        distance = distance * 1.852
    
    # 角度转弧度
    lat1 = math.radians(start.latitude)
    lon1 = math.radians(start.longitude)
    brng = math.radians(bearing_deg)
    
    # 角距离
    d = distance / EARTH_RADIUS_KM
    
    # 计算终点
    lat2 = math.asin(
        math.sin(lat1) * math.cos(d) + 
        math.cos(lat1) * math.sin(d) * math.cos(brng)
    )
    
    lon2 = lon1 + math.atan2(
        math.sin(brng) * math.sin(d) * math.cos(lat1),
        math.cos(d) - math.sin(lat1) * math.sin(lat2)
    )
    
    return Coordinate(math.degrees(lat2), math.degrees(lon2))


# ==================== 边界框计算 ====================

@dataclass
class BoundingBox:
    """边界框数据类"""
    min_lat: float
    max_lat: float
    min_lon: float
    max_lon: float
    
    def contains(self, coord: Coordinate) -> bool:
        """检查坐标是否在边界框内"""
        return (
            self.min_lat <= coord.latitude <= self.max_lat and
            self.min_lon <= coord.longitude <= self.max_lon
        )
    
    def center(self) -> Coordinate:
        """获取边界框中心点"""
        return Coordinate(
            (self.min_lat + self.max_lat) / 2,
            (self.min_lon + self.max_lon) / 2
        )
    
    def to_dict(self) -> Dict[str, float]:
        """转换为字典"""
        return {
            "min_lat": self.min_lat,
            "max_lat": self.max_lat,
            "min_lon": self.min_lon,
            "max_lon": self.max_lon
        }
    
    def __repr__(self) -> str:
        return f"BoundingBox(lat: [{self.min_lat:.4f}, {self.max_lat:.4f}], lon: [{self.min_lon:.4f}, {self.max_lon:.4f}])"


def bounding_box(
    center: Coordinate,
    radius: float,
    unit: str = "km"
) -> BoundingBox:
    """
    计算给定中心点和半径的边界框
    
    Args:
        center: 中心点坐标
        radius: 半径
        unit: 距离单位 ("km", "mile", "m", "nmi")
    
    Returns:
        BoundingBox 对象
    
    Example:
        >>> center = Coordinate(39.9042, 116.4074)  # 北京
        >>> bounding_box(center, 10)  # 10公里范围
        BoundingBox(...)
    """
    # 转换为公里
    if unit == "mile":
        radius = radius * 1.60934
    elif unit == "m":
        radius = radius / 1000
    elif unit == "nmi":
        radius = radius * 1.852
    
    # 计算纬度偏移
    lat_offset = math.degrees(radius / EARTH_RADIUS_KM)
    
    # 计算经度偏移（需要考虑纬度）
    lon_offset = math.degrees(
        radius / (EARTH_RADIUS_KM * math.cos(math.radians(center.latitude)))
    )
    
    return BoundingBox(
        min_lat=center.latitude - lat_offset,
        max_lat=center.latitude + lat_offset,
        min_lon=center.longitude - lon_offset,
        max_lon=center.longitude + lon_offset
    )


# ==================== 坐标验证和工具 ====================

def is_valid_coordinate(lat: float, lon: float) -> bool:
    """
    验证坐标是否有效
    
    Args:
        lat: 纬度
        lon: 经度
    
    Returns:
        是否有效
    """
    return -90 <= lat <= 90 and -180 <= lon <= 180


def normalize_longitude(lon: float) -> float:
    """
    将经度标准化到 -180 到 180 范围
    
    Args:
        lon: 经度值
    
    Returns:
        标准化后的经度
    
    Example:
        >>> normalize_longitude(190)
        -170.0
        >>> normalize_longitude(-190)
        170.0
    """
    while lon > 180:
        lon -= 360
    while lon < -180:
        lon += 360
    return lon


def midpoint(coord1: Coordinate, coord2: Coordinate) -> Coordinate:
    """
    计算两个坐标之间的中点
    
    Args:
        coord1: 第一个坐标
        coord2: 第二个坐标
    
    Returns:
        中点坐标
    
    Example:
        >>> midpoint(Coordinate(0, 0), Coordinate(10, 20))
        Coordinate 约 (5°N, 10°E)
    """
    lat1 = math.radians(coord1.latitude)
    lon1 = math.radians(coord1.longitude)
    lat2 = math.radians(coord2.latitude)
    dlon = math.radians(coord2.longitude - coord1.longitude)
    
    bx = math.cos(lat2) * math.cos(dlon)
    by = math.cos(lat2) * math.sin(dlon)
    
    lat_mid = math.atan2(
        math.sin(lat1) + math.sin(lat2),
        math.sqrt((math.cos(lat1) + bx) ** 2 + by ** 2)
    )
    
    lon_mid = lon1 + math.atan2(by, math.cos(lat1) + bx)
    
    return Coordinate(math.degrees(lat_mid), normalize_longitude(math.degrees(lon_mid)))


# ==================== 批量计算 ====================

def total_distance(coords: List[Coordinate], unit: str = "km") -> float:
    """
    计算路径总距离
    
    Args:
        coords: 坐标列表（按顺序）
        unit: 距离单位
    
    Returns:
        总距离
    
    Example:
        >>> coords = [Coordinate(0, 0), Coordinate(1, 0), Coordinate(1, 1)]
        >>> total_distance(coords)
        约 222 公里
    """
    if len(coords) < 2:
        return 0.0
    
    total = 0.0
    for i in range(len(coords) - 1):
        total += haversine_distance(coords[i], coords[i + 1], unit)
    
    return total


def find_nearest(
    target: Coordinate,
    candidates: List[Coordinate]
) -> Tuple[Coordinate, float, int]:
    """
    找到距离目标最近的坐标点
    
    Args:
        target: 目标坐标
        candidates: 候选坐标列表
    
    Returns:
        (最近坐标, 距离(km), 索引)
    
    Example:
        >>> target = Coordinate(39.9, 116.4)
        >>> candidates = [Coordinate(31.2, 121.5), Coordinate(34.3, 108.9)]
        >>> find_nearest(target, candidates)
        (Coordinate(34.3, 108.9), 约900km, 1)
    """
    if not candidates:
        raise ValueError("候选列表不能为空")
    
    min_dist = float("inf")
    nearest = None
    nearest_idx = -1
    
    for idx, coord in enumerate(candidates):
        dist = haversine_distance(target, coord)
        if dist < min_dist:
            min_dist = dist
            nearest = coord
            nearest_idx = idx
    
    return nearest, min_dist, nearest_idx


def coordinates_within_radius(
    center: Coordinate,
    coords: List[Coordinate],
    radius: float,
    unit: str = "km"
) -> List[Tuple[Coordinate, float]]:
    """
    找出半径范围内的所有坐标
    
    Args:
        center: 中心点
        coords: 候选坐标列表
        radius: 半径
        unit: 距离单位
    
    Returns:
        [(坐标, 距离), ...] 按距离排序
    
    Example:
        >>> center = Coordinate(39.9, 116.4)
        >>> coords = [Coordinate(39.91, 116.41), Coordinate(35, 120)]
        >>> coordinates_within_radius(center, coords, 10)
        [(Coordinate(39.91, 116.41), 约1.2km)]
    """
    results = []
    
    for coord in coords:
        dist = haversine_distance(center, coord, unit)
        if dist <= radius:
            results.append((coord, dist))
    
    # 按距离排序
    results.sort(key=lambda x: x[1])
    
    return results


# ==================== 坐标格式化输出 ====================

def format_coordinate(
    coord: Coordinate,
    format_type: str = "decimal",
    precision: int = 6
) -> str:
    """
    格式化坐标输出
    
    Args:
        coord: 坐标
        format_type: 格式类型 ("decimal", "dms", "geojson")
        precision: 十进制精度位数
    
    Returns:
        格式化字符串
    
    Example:
        >>> coord = Coordinate(39.9042, 116.4074)
        >>> format_coordinate(coord, "decimal")
        "39.904200, 116.407400"
        >>> format_coordinate(coord, "dms")
        "39°54'15.12\"N, 116°24'26.64\"E"
        >>> format_coordinate(coord, "geojson")
        "[116.407400, 39.904200]"
    """
    if format_type == "decimal":
        lat_dir = "N" if coord.latitude >= 0 else "S"
        lon_dir = "E" if coord.longitude >= 0 else "W"
        return f"{abs(coord.latitude):.{precision}f}°{lat_dir}, {abs(coord.longitude):.{precision}f}°{lon_dir}"
    
    elif format_type == "dms":
        lat_dms, lon_dms = coord.to_dms()
        return f"{lat_dms}, {lon_dms}"
    
    elif format_type == "geojson":
        return f"[{coord.longitude:.{precision}f}, {coord.latitude:.{precision}f}]"
    
    else:
        raise ValueError(f"不支持的格式类型: {format_type}")


def to_geojson(coords: List[Coordinate]) -> Dict[str, Any]:
    """
    将坐标列表转换为 GeoJSON FeatureCollection
    
    Args:
        coords: 坐标列表
    
    Returns:
        GeoJSON FeatureCollection 字典
    
    Example:
        >>> coords = [Coordinate(39.9, 116.4), Coordinate(31.2, 121.5)]
        >>> to_geojson(coords)
        {"type": "FeatureCollection", "features": [...]}
    """
    features = []
    for i, coord in enumerate(coords):
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [coord.longitude, coord.latitude]
            },
            "properties": {
                "index": i
            }
        })
    
    return {
        "type": "FeatureCollection",
        "features": features
    }


# 模块导出
__all__ = [
    "Coordinate",
    "BoundingBox",
    "decimal_to_dms",
    "dms_to_decimal",
    "parse_coordinate",
    "haversine_distance",
    "bearing",
    "bearing_to_direction",
    "destination_point",
    "bounding_box",
    "is_valid_coordinate",
    "normalize_longitude",
    "midpoint",
    "total_distance",
    "find_nearest",
    "coordinates_within_radius",
    "format_coordinate",
    "to_geojson",
    "EARTH_RADIUS_KM",
    "EARTH_RADIUS_MILES",
    "EARTH_RADIUS_METERS",
]