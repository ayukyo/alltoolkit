"""
地理坐标工具模块 (Geo Utils)

提供地理坐标计算功能，包括：
- 两点间距离计算（Haversine公式）
- 方位角计算
- 目标点坐标计算
- 坐标边界计算
- 经纬度格式转换

纯 Python 实现，零外部依赖。
"""

import math
from typing import Tuple, List, Optional, Dict, Any


# 地球半径（米）
EARTH_RADIUS_METERS = 6371000.0

# 地球半径（公里）
EARTH_RADIUS_KM = 6371.0

# 地球半径（英里）
EARTH_RADIUS_MILES = 3958.8


def degrees_to_radians(degrees: float) -> float:
    """角度转弧度"""
    return degrees * math.pi / 180.0


def radians_to_degrees(radians: float) -> float:
    """弧度转角度"""
    return radians * 180.0 / math.pi


def haversine_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    unit: str = "km"
) -> float:
    """
    使用 Haversine 公式计算两点之间的球面距离
    
    Args:
        lat1: 起点纬度
        lon1: 起点经度
        lat2: 终点纬度
        lon2: 终点经度
        unit: 距离单位，可选 "km"(公里), "m"(米), "mi"(英里), "nm"(海里)
    
    Returns:
        两点之间的距离
    
    Example:
        >>> haversine_distance(39.9042, 116.4074, 31.2304, 121.4737)
        1067.44  # 北京到上海的距离约1067公里
    """
    # 转换为弧度
    lat1_rad = degrees_to_radians(lat1)
    lat2_rad = degrees_to_radians(lat2)
    delta_lat = degrees_to_radians(lat2 - lat1)
    delta_lon = degrees_to_radians(lon2 - lon1)
    
    # Haversine 公式
    a = (math.sin(delta_lat / 2) ** 2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) *
         math.sin(delta_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # 根据单位选择地球半径
    radius_map = {
        "km": EARTH_RADIUS_KM,
        "m": EARTH_RADIUS_METERS,
        "mi": EARTH_RADIUS_MILES,
        "nm": EARTH_RADIUS_KM * 0.539957  # 海里
    }
    
    radius = radius_map.get(unit.lower(), EARTH_RADIUS_KM)
    return radius * c


def calculate_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    计算从起点到终点的初始方位角
    
    Args:
        lat1: 起点纬度
        lon1: 起点经度
        lat2: 终点纬度
        lon2: 终点经度
    
    Returns:
        方位角（0-360度），0度为正北，顺时针方向
    
    Example:
        >>> calculate_bearing(39.9042, 116.4074, 31.2304, 121.4737)
        153.5  # 北京到上海的方向约为东南方向
    """
    lat1_rad = degrees_to_radians(lat1)
    lat2_rad = degrees_to_radians(lat2)
    delta_lon = degrees_to_radians(lon2 - lon1)
    
    x = math.sin(delta_lon) * math.cos(lat2_rad)
    y = (math.cos(lat1_rad) * math.sin(lat2_rad) -
         math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(delta_lon))
    
    bearing = math.atan2(x, y)
    bearing_deg = radians_to_degrees(bearing)
    
    # 转换为0-360度
    return (bearing_deg + 360) % 360


def bearing_to_compass(bearing: float) -> str:
    """
    将方位角转换为罗盘方向
    
    Args:
        bearing: 方位角（0-360度）
    
    Returns:
        罗盘方向字符串（N, NE, E, SE, S, SW, W, NW）
    
    Example:
        >>> bearing_to_compass(0)
        'N'
        >>> bearing_to_compass(45)
        'NE'
        >>> bearing_to_compass(225)
        'SW'
    """
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    index = round(bearing / 45) % 8
    return directions[index]


def destination_point(
    lat: float,
    lon: float,
    bearing: float,
    distance: float,
    unit: str = "km"
) -> Tuple[float, float]:
    """
    根据起点、方位角和距离计算目标点坐标
    
    Args:
        lat: 起点纬度
        lon: 起点经度
        bearing: 方位角（度）
        distance: 距离
        unit: 距离单位
    
    Returns:
        目标点坐标 (纬度, 经度)
    
    Example:
        >>> destination_point(39.9042, 116.4074, 153.5, 1067, "km")
        (31.23, 121.47)  # 从北京向东南方向1067公里
    """
    # 转换为弧度
    lat_rad = degrees_to_radians(lat)
    lon_rad = degrees_to_radians(lon)
    bearing_rad = degrees_to_radians(bearing)
    
    # 根据单位转换距离
    radius_map = {
        "km": EARTH_RADIUS_KM,
        "m": EARTH_RADIUS_METERS / 1000,
        "mi": EARTH_RADIUS_MILES * 1.60934,
        "nm": EARTH_RADIUS_KM * 0.539957 * 1.852
    }
    radius_km = radius_map.get(unit.lower(), EARTH_RADIUS_KM)
    
    # 角距离
    angular_distance = distance / radius_km
    
    # 计算目标点
    lat2_rad = math.asin(
        math.sin(lat_rad) * math.cos(angular_distance) +
        math.cos(lat_rad) * math.sin(angular_distance) * math.cos(bearing_rad)
    )
    
    lon2_rad = lon_rad + math.atan2(
        math.sin(bearing_rad) * math.sin(angular_distance) * math.cos(lat_rad),
        math.cos(angular_distance) - math.sin(lat_rad) * math.sin(lat2_rad)
    )
    
    return (radians_to_degrees(lat2_rad), radians_to_degrees(lon2_rad))


def get_bounding_box(
    lat: float,
    lon: float,
    distance: float,
    unit: str = "km"
) -> Dict[str, float]:
    """
    计算以某点为中心、指定距离为半径的边界框
    
    Args:
        lat: 中心点纬度
        lon: 中心点经度
        distance: 距离半径
        unit: 距离单位
    
    Returns:
        边界框字典 {'min_lat', 'max_lat', 'min_lon', 'max_lon'}
    
    Example:
        >>> get_bounding_box(39.9042, 116.4074, 10, "km")
        {'min_lat': 39.81, 'max_lat': 39.99, 'min_lon': 116.27, 'max_lon': 116.54}
    """
    # 转换距离为公里
    unit_conversion = {
        "km": 1,
        "m": 0.001,
        "mi": 1.60934,
        "nm": 1.852
    }
    distance_km = distance * unit_conversion.get(unit.lower(), 1)
    
    # 计算纬度变化
    lat_delta = distance_km / EARTH_RADIUS_KM * (180 / math.pi)
    
    # 计算经度变化（考虑纬度）
    lon_delta = distance_km / (EARTH_RADIUS_KM * math.cos(degrees_to_radians(lat))) * (180 / math.pi)
    
    return {
        'min_lat': lat - lat_delta,
        'max_lat': lat + lat_delta,
        'min_lon': lon - lon_delta,
        'max_lon': lon + lon_delta
    }


def is_point_in_bounding_box(
    point_lat: float,
    point_lon: float,
    bbox: Dict[str, float]
) -> bool:
    """
    判断点是否在边界框内
    
    Args:
        point_lat: 点纬度
        point_lon: 点经度
        bbox: 边界框字典
    
    Returns:
        是否在边界框内
    
    Example:
        >>> bbox = get_bounding_box(39.9042, 116.4074, 10, "km")
        >>> is_point_in_bounding_box(39.91, 116.41, bbox)
        True
    """
    return (bbox['min_lat'] <= point_lat <= bbox['max_lat'] and
            bbox['min_lon'] <= point_lon <= bbox['max_lon'])


def midpoint(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float
) -> Tuple[float, float]:
    """
    计算两点之间的中点
    
    Args:
        lat1: 起点纬度
        lon1: 起点经度
        lat2: 终点纬度
        lon2: 终点经度
    
    Returns:
        中点坐标 (纬度, 经度)
    
    Example:
        >>> midpoint(39.9042, 116.4074, 31.2304, 121.4737)
        (35.67, 118.98)  # 北京和上海之间的大圆中点
    """
    lat1_rad = degrees_to_radians(lat1)
    lat2_rad = degrees_to_radians(lat2)
    lon1_rad = degrees_to_radians(lon1)
    lon2_rad = degrees_to_radians(lon2)
    
    d_lon = lon2_rad - lon1_rad
    
    bx = math.cos(lat2_rad) * math.cos(d_lon)
    by = math.cos(lat2_rad) * math.sin(d_lon)
    
    lat_mid_rad = math.atan2(
        math.sin(lat1_rad) + math.sin(lat2_rad),
        math.sqrt((math.cos(lat1_rad) + bx) ** 2 + by ** 2)
    )
    
    lon_mid_rad = lon1_rad + math.atan2(by, math.cos(lat1_rad) + bx)
    
    return (radians_to_degrees(lat_mid_rad), radians_to_degrees(lon_mid_rad))


def interpolate_points(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    num_points: int
) -> List[Tuple[float, float]]:
    """
    在两点之间插值生成多个点
    
    Args:
        lat1: 起点纬度
        lon1: 起点经度
        lat2: 终点纬度
        lon2: 终点经度
        num_points: 要生成的点数（不包括端点）
    
    Returns:
        插值点列表，包含起点、插值点和终点
    
    Example:
        >>> interpolate_points(39.9042, 116.4074, 31.2304, 121.4737, 2)
        [(39.90, 116.41), (35.67, 118.98), (31.23, 121.47)]
    """
    if num_points < 1:
        return [(lat1, lon1), (lat2, lon2)]
    
    points = [(lat1, lon1)]
    total_distance = haversine_distance(lat1, lon1, lat2, lon2, "km")
    bearing = calculate_bearing(lat1, lon1, lat2, lon2)
    
    for i in range(1, num_points + 1):
        fraction = i / (num_points + 1)
        distance = total_distance * fraction
        point = destination_point(lat1, lon1, bearing, distance, "km")
        points.append(point)
    
    points.append((lat2, lon2))
    return points


def dms_to_decimal(
    degrees: int,
    minutes: int,
    seconds: float,
    direction: str = 'N'
) -> float:
    """
    将度分秒格式转换为十进制度
    
    Args:
        degrees: 度
        minutes: 分
        seconds: 秒
        direction: 方向 (N/S/E/W)
    
    Returns:
        十进制度
    
    Example:
        >>> dms_to_decimal(39, 54, 15.12, 'N')
        39.9042
        >>> dms_to_decimal(116, 24, 26.64, 'E')
        116.4074
    """
    decimal = degrees + minutes / 60.0 + seconds / 3600.0
    if direction.upper() in ['S', 'W']:
        decimal = -decimal
    return decimal


def decimal_to_dms(decimal: float, is_latitude: bool = True) -> Tuple[int, int, float, str]:
    """
    将十进制度转换为度分秒格式
    
    Args:
        decimal: 十进制度
        is_latitude: 是否为纬度
    
    Returns:
        (度, 分, 秒, 方向)
    
    Example:
        >>> decimal_to_dms(39.9042, True)
        (39, 54, 15.12, 'N')
        >>> decimal_to_dms(-116.4074, False)
        (116, 24, 26.64, 'W')
    """
    # 确定方向
    if is_latitude:
        direction = 'S' if decimal < 0 else 'N'
    else:
        direction = 'W' if decimal < 0 else 'E'
    
    decimal = abs(decimal)
    degrees = int(decimal)
    minutes_decimal = (decimal - degrees) * 60
    minutes = int(minutes_decimal)
    seconds = (minutes_decimal - minutes) * 60
    
    return (degrees, minutes, round(seconds, 2), direction)


def format_coordinates(lat: float, lon: float, fmt: str = "decimal") -> str:
    """
    格式化坐标显示
    
    Args:
        lat: 纬度
        lon: 经度
        fmt: 格式类型 ("decimal" 十进制, "dms" 度分秒)
    
    Returns:
        格式化的坐标字符串
    
    Example:
        >>> format_coordinates(39.9042, 116.4074, "decimal")
        '39.9042°N, 116.4074°E'
        >>> format_coordinates(39.9042, 116.4074, "dms")
        '39°54\'15.12"N, 116°24\'26.64"E'
    """
    if fmt == "dms":
        lat_dms = decimal_to_dms(lat, True)
        lon_dms = decimal_to_dms(lon, False)
        return f"{lat_dms[0]}°{lat_dms[1]}'{lat_dms[2]:.2f}\"{lat_dms[3]}, {lon_dms[0]}°{lon_dms[1]}'{lon_dms[2]:.2f}\"{lon_dms[3]}"
    else:
        lat_dir = 'N' if lat >= 0 else 'S'
        lon_dir = 'E' if lon >= 0 else 'W'
        return f"{abs(lat):.4f}°{lat_dir}, {abs(lon):.4f}°{lon_dir}"


def find_nearest_point(
    target_lat: float,
    target_lon: float,
    points: List[Tuple[float, float]],
    unit: str = "km"
) -> Tuple[int, Tuple[float, float], float]:
    """
    从点列表中找到最近的点
    
    Args:
        target_lat: 目标纬度
        target_lon: 目标经度
        points: 点列表 [(lat, lon), ...]
        unit: 距离单位
    
    Returns:
        (索引, 最近点坐标, 距离)
    
    Example:
        >>> points = [(31.2304, 121.4737), (30.5728, 114.3052), (29.5630, 106.5516)]
        >>> find_nearest_point(39.9042, 116.4074, points)
        (0, (31.2304, 121.4737), 1067.44)  # 上海最近
    """
    min_distance = float('inf')
    nearest_idx = 0
    nearest_point = points[0]
    
    for idx, (lat, lon) in enumerate(points):
        distance = haversine_distance(target_lat, target_lon, lat, lon, unit)
        if distance < min_distance:
            min_distance = distance
            nearest_idx = idx
            nearest_point = (lat, lon)
    
    return (nearest_idx, nearest_point, min_distance)


def calculate_area(
    polygon: List[Tuple[float, float]],
    unit: str = "km2"
) -> float:
    """
    计算多边形区域的面积（使用局部投影近似方法）
    
    Args:
        polygon: 多边形顶点列表 [(lat, lon), ...]，必须按顺序排列
        unit: 面积单位 ("km2" 平方公里, "m2" 平方米, "mi2" 平方英里)
    
    Returns:
        面积
    
    Example:
        >>> polygon = [(39.9, 116.3), (39.9, 116.5), (39.8, 116.5), (39.8, 116.3)]
        >>> calculate_area(polygon, "km2")
        31.5  # 北京某区域面积约31.5平方公里
    """
    if len(polygon) < 3:
        return 0.0
    
    # 使用简化的经纬度投影方法计算近似面积
    # 将经纬度坐标转换为局部的平面近似
    # 以多边形中心为参考点
    
    center_lat = sum(p[0] for p in polygon) / len(polygon)
    center_lon = sum(p[1] for p in polygon) / len(polygon)
    
    # 计算每个点到中心的相对坐标（米）
    # 纬度方向：每度约111km
    # 经度方向：取决于纬度
    lat_scale = 111000  # 米/度
    lon_scale = 111000 * math.cos(degrees_to_radians(center_lat))  # 米/度
    
    # 转换坐标
    points_xy = []
    for lat, lon in polygon:
        x = (lon - center_lon) * lon_scale
        y = (lat - center_lat) * lat_scale
        points_xy.append((x, y))
    
    # 使用鞋带公式计算平面多边形面积
    area_m2 = 0
    n = len(points_xy)
    for i in range(n):
        x1, y1 = points_xy[i]
        x2, y2 = points_xy[(i + 1) % n]
        area_m2 += x1 * y2 - x2 * y1
    
    area_m2 = abs(area_m2) / 2
    
    # 单位转换
    unit_conversion = {
        "km2": 1 / 1_000_000,
        "m2": 1,
        "mi2": 1 / 2_589_988.11
    }
    
    return area_m2 * unit_conversion.get(unit.lower(), 1 / 1_000_000)





class GeoPoint:
    """地理坐标点类"""
    
    def __init__(self, lat: float, lon: float, name: str = ""):
        """
        初始化地理坐标点
        
        Args:
            lat: 纬度
            lon: 经度
            name: 点名称（可选）
        """
        self.lat = lat
        self.lon = lon
        self.name = name
    
    def distance_to(self, other: 'GeoPoint', unit: str = "km") -> float:
        """计算到另一个点的距离"""
        return haversine_distance(self.lat, self.lon, other.lat, other.lon, unit)
    
    def bearing_to(self, other: 'GeoPoint') -> float:
        """计算到另一个点的方位角"""
        return calculate_bearing(self.lat, self.lon, other.lat, other.lon)
    
    def destination(self, bearing: float, distance: float, unit: str = "km") -> 'GeoPoint':
        """根据方位角和距离计算目标点"""
        lat, lon = destination_point(self.lat, self.lon, bearing, distance, unit)
        return GeoPoint(lat, lon)
    
    def midpoint_to(self, other: 'GeoPoint') -> 'GeoPoint':
        """计算与另一个点的中点"""
        lat, lon = midpoint(self.lat, self.lon, other.lat, other.lon)
        return GeoPoint(lat, lon)
    
    def bounding_box(self, distance: float, unit: str = "km") -> Dict[str, float]:
        """计算边界框"""
        return get_bounding_box(self.lat, self.lon, distance, unit)
    
    def to_dms(self) -> Tuple[str, str]:
        """转换为度分秒格式"""
        lat_dms = decimal_to_dms(self.lat, True)
        lon_dms = decimal_to_dms(self.lon, False)
        lat_str = f"{lat_dms[0]}°{lat_dms[1]}'{lat_dms[2]:.2f}\"{lat_dms[3]}"
        lon_str = f"{lon_dms[0]}°{lon_dms[1]}'{lon_dms[2]:.2f}\"{lon_dms[3]}"
        return (lat_str, lon_str)
    
    def __repr__(self) -> str:
        name_str = f" '{self.name}'" if self.name else ""
        return f"GeoPoint({self.lat}, {self.lon}{name_str})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GeoPoint):
            return False
        return abs(self.lat - other.lat) < 1e-6 and abs(self.lon - other.lon) < 1e-6


# 常用城市坐标
CITY_COORDINATES: Dict[str, Tuple[float, float]] = {
    # 中国城市
    "北京": (39.9042, 116.4074),
    "上海": (31.2304, 121.4737),
    "广州": (23.1291, 113.2644),
    "深圳": (22.5431, 114.0579),
    "杭州": (30.2741, 120.1551),
    "成都": (30.5728, 104.0668),
    "武汉": (30.5928, 114.3052),
    "西安": (34.3416, 108.9398),
    "南京": (32.0603, 118.7969),
    "重庆": (29.4316, 106.9123),
    "天津": (39.0842, 117.2008),
    "苏州": (31.2990, 120.5853),
    "香港": (22.3193, 114.1694),
    "台北": (25.0330, 121.5654),
    
    # 国际城市
    "东京": (35.6762, 139.6503),
    "首尔": (37.5665, 126.9780),
    "新加坡": (1.3521, 103.8198),
    "曼谷": (13.7563, 100.5018),
    "迪拜": (25.2048, 55.2708),
    "悉尼": (-33.8688, 151.2093),
    "伦敦": (51.5074, -0.1278),
    "巴黎": (48.8566, 2.3522),
    "纽约": (40.7128, -74.0060),
    "洛杉矶": (34.0522, -118.2437),
    "旧金山": (37.7749, -122.4194),
    "莫斯科": (55.7558, 37.6173),
}


def get_city_coordinates(city_name: str) -> Optional[Tuple[float, float]]:
    """
    获取城市坐标
    
    Args:
        city_name: 城市名称
    
    Returns:
        城市坐标 (纬度, 经度)，如果未找到则返回 None
    
    Example:
        >>> get_city_coordinates("北京")
        (39.9042, 116.4074)
    """
    return CITY_COORDINATES.get(city_name)


def distance_between_cities(city1: str, city2: str, unit: str = "km") -> Optional[float]:
    """
    计算两个城市之间的距离
    
    Args:
        city1: 城市名称1
        city2: 城市名称2
        unit: 距离单位
    
    Returns:
        距离，如果任一城市未找到则返回 None
    
    Example:
        >>> distance_between_cities("北京", "上海")
        1067.44
    """
    coord1 = get_city_coordinates(city1)
    coord2 = get_city_coordinates(city2)
    
    if coord1 and coord2:
        return haversine_distance(coord1[0], coord1[1], coord2[0], coord2[1], unit)
    return None