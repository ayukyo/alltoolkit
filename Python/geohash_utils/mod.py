"""
Geohash Utilities - 地理坐标与Geohash编码转换工具

功能：
1. 经纬度编码为Geohash字符串
2. Geohash解码为经纬度边界框和中心点
3. 计算相邻Geohash（用于邻近搜索）
4. 坐标间距离计算（Haversine公式）
5. Geohash精度信息查询
6. 边界框计算

零外部依赖，纯Python实现。
"""

from typing import Tuple, List, Dict
import math


# Geohash字符集 (Base32)
GEOHASH_CHARS = '0123456789bcdefghjkmnpqrstuvwxyz'
GEOHASH_CHAR_TO_INT = {c: i for i, c in enumerate(GEOHASH_CHARS)}

# 每个字符的位数
BITS_PER_CHAR = 5

# 经纬度范围
LAT_RANGE = (-90.0, 90.0)
LNG_RANGE = (-180.0, 180.0)

# 地球半径（千米）
EARTH_RADIUS_KM = 6371.0

# 不同精度的Geohash宽度和高度（千米）
GEOHASH_PRECISION_SIZES = {
    1: (5000.0, 5000.0),
    2: (1250.0, 625.0),
    3: (156.0, 156.0),
    4: (39.1, 19.5),
    5: (4.9, 4.9),
    6: (1.2, 0.61),
    7: (0.153, 0.153),
    8: (0.0382, 0.0191),
    9: (0.00477, 0.00477),
    10: (0.00119, 0.000596),
    11: (0.000149, 0.000149),
    12: (0.0000372, 0.0000186),
}


class GeoHashError(Exception):
    """Geohash相关错误"""
    pass


def encode(lat: float, lng: float, precision: int = 10) -> str:
    """
    将经纬度编码为Geohash字符串
    
    Args:
        lat: 纬度 (-90, 90)
        lng: 经度 (-180, 180)
        precision: Geohash精度 (1-12)，默认10
    
    Returns:
        Geohash字符串
    
    Raises:
        GeoHashError: 如果参数无效
    
    Example:
        >>> encode(39.9042, 116.4074, 6)
        'wx4g0b'
    """
    if not (1 <= precision <= 12):
        raise GeoHashError(f"精度必须在1-12之间，当前: {precision}")
    
    if not (LAT_RANGE[0] <= lat <= LAT_RANGE[1]):
        raise GeoHashError(f"纬度必须在{LAT_RANGE}之间，当前: {lat}")
    
    if not (LNG_RANGE[0] <= lng <= LNG_RANGE[1]):
        raise GeoHashError(f"经度必须在{LNG_RANGE}之间，当前: {lng}")
    
    # 将经纬度转换为二进制位
    lat_bits = _to_binary_bits(lat, LAT_RANGE, precision * BITS_PER_CHAR // 2)
    lng_bits = _to_binary_bits(lng, LNG_RANGE, (precision * BITS_PER_CHAR + 1) // 2)
    
    # 交替合并经纬度位 (经度在偶数索引，纬度在奇数索引)
    combined_bits = []
    for i in range(max(len(lng_bits), len(lat_bits))):
        if i < len(lng_bits):
            combined_bits.append(lng_bits[i])
        if i < len(lat_bits):
            combined_bits.append(lat_bits[i])
    
    # 将二进制位转换为Geohash字符
    geohash = []
    for i in range(0, len(combined_bits), BITS_PER_CHAR):
        chunk = combined_bits[i:i + BITS_PER_CHAR]
        # 填充到5位
        while len(chunk) < BITS_PER_CHAR:
            chunk.append(0)
        value = sum(b << (BITS_PER_CHAR - 1 - j) for j, b in enumerate(chunk))
        geohash.append(GEOHASH_CHARS[value])
    
    return ''.join(geohash[:precision])


def _to_binary_bits(value: float, value_range: Tuple[float, float], num_bits: int) -> List[int]:
    """
    将数值转换为二进制位列表
    
    Args:
        value: 要转换的值
        value_range: 值的范围 (min, max)
        num_bits: 需要的位数
    
    Returns:
        二进制位列表
    """
    bits = []
    low, high = value_range
    
    for _ in range(num_bits):
        mid = (low + high) / 2
        if value >= mid:
            bits.append(1)
            low = mid
        else:
            bits.append(0)
            high = mid
    
    return bits


def decode(geohash: str) -> Dict[str, any]:
    """
    将Geohash解码为经纬度信息
    
    Args:
        geohash: Geohash字符串
    
    Returns:
        包含以下字段的字典:
        - lat: 纬度中心点
        - lng: 经度中心点
        - lat_min: 纬度最小值
        - lat_max: 纬度最大值
        - lng_min: 经度最小值
        - lng_max: 经度最大值
        - precision: 精度
        - width_km: 宽度(千米)
        - height_km: 高度(千米)
    
    Raises:
        GeoHashError: 如果Geohash无效
    
    Example:
        >>> decode('wx4g0b')
        {'lat': 39.9042..., 'lng': 116.4074..., ...}
    """
    if not geohash:
        raise GeoHashError("Geohash不能为空")
    
    geohash = geohash.lower()
    
    # 验证字符
    for c in geohash:
        if c not in GEOHASH_CHAR_TO_INT:
            raise GeoHashError(f"无效的Geohash字符: '{c}'")
    
    # 分离经纬度位
    lng_bits = []
    lat_bits = []
    
    for i, c in enumerate(geohash):
        value = GEOHASH_CHAR_TO_INT[c]
        bits = [(value >> (BITS_PER_CHAR - 1 - j)) & 1 for j in range(BITS_PER_CHAR)]
        
        for j, bit in enumerate(bits):
            if (i * BITS_PER_CHAR + j) % 2 == 0:
                lng_bits.append(bit)  # 偶数位是经度
            else:
                lat_bits.append(bit)  # 奇数位是纬度
    
    # 解码经纬度
    lat_min, lat_max = LAT_RANGE
    lng_min, lng_max = LNG_RANGE
    
    for bit in lng_bits:
        mid = (lng_min + lng_max) / 2
        if bit:
            lng_min = mid
        else:
            lng_max = mid
    
    for bit in lat_bits:
        mid = (lat_min + lat_max) / 2
        if bit:
            lat_min = mid
        else:
            lat_max = mid
    
    precision = len(geohash)
    width_km, height_km = GEOHASH_PRECISION_SIZES.get(precision, (0, 0))
    
    return {
        'lat': (lat_min + lat_max) / 2,
        'lng': (lng_min + lng_max) / 2,
        'lat_min': lat_min,
        'lat_max': lat_max,
        'lng_min': lng_min,
        'lng_max': lng_max,
        'precision': precision,
        'width_km': width_km,
        'height_km': height_km,
    }


def get_neighbors(geohash: str) -> Dict[str, str]:
    """
    获取Geohash的8个相邻Geohash
    
    Args:
        geohash: Geohash字符串
    
    Returns:
        包含8个方向相邻Geohash的字典:
        - n: 北
        - ne: 东北
        - e: 东
        - se: 东南
        - s: 南
        - sw: 西南
        - w: 西
        - nw: 西北
    
    Raises:
        GeoHashError: 如果Geohash无效
    
    Example:
        >>> get_neighbors('wx4g0b')
        {'n': 'wx4g0c', 'ne': 'wx4g0g', ...}
    """
    if not geohash:
        raise GeoHashError("Geohash不能为空")
    
    geohash = geohash.lower()
    
    # 解码中心点
    center = decode(geohash)
    precision = center['precision']
    
    # 根据Geohash大小计算偏移
    width_km, height_km = GEOHASH_PRECISION_SIZES.get(precision, (1.0, 1.0))
    
    # 纬度每度约111km，经度随纬度变化
    lat_offset = height_km / 111.0
    lng_offset = width_km / (111.0 * math.cos(math.radians(center['lat'])))
    
    # 计算各方向的中心点并编码
    directions = {
        'n': (center['lat'] + lat_offset, center['lng']),
        'ne': (center['lat'] + lat_offset, center['lng'] + lng_offset),
        'e': (center['lat'], center['lng'] + lng_offset),
        'se': (center['lat'] - lat_offset, center['lng'] + lng_offset),
        's': (center['lat'] - lat_offset, center['lng']),
        'sw': (center['lat'] - lat_offset, center['lng'] - lng_offset),
        'w': (center['lat'], center['lng'] - lng_offset),
        'nw': (center['lat'] + lat_offset, center['lng'] - lng_offset),
    }
    
    result = {}
    for direction, (lat, lng) in directions.items():
        # 确保坐标在有效范围内
        lat = max(LAT_RANGE[0], min(LAT_RANGE[1], lat))
        lng = max(LNG_RANGE[0], min(LNG_RANGE[1], lng))
        
        # 编码为Geohash
        try:
            result[direction] = encode(lat, lng, precision)
        except GeoHashError:
            # 边界情况，使用原始值
            result[direction] = geohash
    
    return result


def distance(lat1: float, lng1: float, lat2: float, lng2: float, unit: str = 'km') -> float:
    """
    计算两个坐标之间的距离（使用Haversine公式）
    
    Args:
        lat1: 起点纬度
        lng1: 起点经度
        lat2: 终点纬度
        lng2: 终点经度
        unit: 距离单位 ('km', 'm', 'mile', 'ft', 'nmi')
            - km: 千米
            - m: 米
            - mile: 英里
            - ft: 英尺
            - nmi: 海里
    
    Returns:
        两点之间的距离
    
    Example:
        >>> distance(39.9042, 116.4074, 31.2304, 121.4737)  # 北京到上海
        1067.46...
    """
    # 转换为弧度
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    lng1_rad = math.radians(lng1)
    lng2_rad = math.radians(lng2)
    
    # 纬度和经度差
    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad
    
    # Haversine公式
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    
    # 基础距离（千米）
    dist_km = EARTH_RADIUS_KM * c
    
    # 单位转换
    unit_multipliers = {
        'km': 1.0,
        'm': 1000.0,
        'mile': 0.621371,
        'ft': 3280.84,
        'nmi': 0.539957,
    }
    
    if unit not in unit_multipliers:
        raise GeoHashError(f"不支持的单位: '{unit}'，支持的单位: {list(unit_multipliers.keys())}")
    
    return dist_km * unit_multipliers[unit]


def get_precision_info(precision: int) -> Dict[str, any]:
    """
    获取指定精度的Geohash信息
    
    Args:
        precision: Geohash精度 (1-12)
    
    Returns:
        包含以下字段的字典:
        - precision: 精度
        - width_km: 宽度(千米)
        - height_km: 高度(千米)
        - area_km2: 面积(平方千米)
        - width_m: 宽度(米)
        - height_m: 高度(米)
        - description: 精度描述
    
    Example:
        >>> get_precision_info(6)
        {'precision': 6, 'width_km': 1.2, 'height_km': 0.61, ...}
    """
    if not (1 <= precision <= 12):
        raise GeoHashError(f"精度必须在1-12之间，当前: {precision}")
    
    width_km, height_km = GEOHASH_PRECISION_SIZES[precision]
    
    descriptions = {
        1: "全球区域 (~5000km)",
        2: "国家/大区域 (~1000km)",
        3: "省/州级区域 (~150km)",
        4: "城市级区域 (~20-40km)",
        5: "区县级区域 (~5km)",
        6: "街道/社区级 (~1km)",
        7: "街区级 (~150m)",
        8: "建筑级 (~20-40m)",
        9: "房间级 (~5m)",
        10: "桌椅级 (~1m)",
        11: "精细级 (~15cm)",
        12: "超精细级 (~4cm)",
    }
    
    return {
        'precision': precision,
        'width_km': width_km,
        'height_km': height_km,
        'area_km2': width_km * height_km,
        'width_m': width_km * 1000,
        'height_m': height_km * 1000,
        'description': descriptions.get(precision, ''),
    }


def get_common_precision(distance_km: float) -> int:
    """
    根据所需覆盖距离获取推荐的Geohash精度
    
    Args:
        distance_km: 需要覆盖的距离(千米)
    
    Returns:
        推荐的Geohash精度
    
    Example:
        >>> get_common_precision(1.0)  # 1公里范围
        6
    """
    for precision in range(1, 13):
        width, height = GEOHASH_PRECISION_SIZES[precision]
        if max(width, height) <= distance_km * 2:
            return max(1, precision - 1)
    return 12


def get_bounding_box(lat: float, lng: float, radius_km: float) -> Dict[str, float]:
    """
    获取指定中心点和半径的边界框
    
    Args:
        lat: 中心点纬度
        lng: 中心点经度
        radius_km: 半径(千米)
    
    Returns:
        包含以下字段的字典:
        - lat_min: 最小纬度
        - lat_max: 最大纬度
        - lng_min: 最小经度
        - lng_max: 最大经度
    
    Example:
        >>> get_bounding_box(39.9042, 116.4074, 10)  # 北京中心，10公里半径
        {'lat_min': 39.81..., 'lat_max': 39.99..., ...}
    """
    # 纬度每度约111km
    lat_offset = radius_km / 111.0
    
    # 经度每度随纬度变化
    lng_offset = radius_km / (111.0 * math.cos(math.radians(lat)))
    
    return {
        'lat_min': max(LAT_RANGE[0], lat - lat_offset),
        'lat_max': min(LAT_RANGE[1], lat + lat_offset),
        'lng_min': max(LNG_RANGE[0], lng - lng_offset),
        'lng_max': min(LNG_RANGE[1], lng + lng_offset),
    }


def get_geohashes_in_bbox(lat_min: float, lat_max: float,
                          lng_min: float, lng_max: float,
                          precision: int) -> List[str]:
    """
    获取边界框内所有的Geohash（简化版，通过网格采样）
    
    Args:
        lat_min: 最小纬度
        lat_max: 最大纬度
        lng_min: 最小经度
        lng_max: 最大经度
        precision: Geohash精度
    
    Returns:
        Geohash列表
    
    Example:
        >>> get_geohashes_in_bbox(39.9, 40.0, 116.3, 116.5, 5)
        ['wx4g0', 'wx4g1', ...]
    """
    if not (1 <= precision <= 12):
        raise GeoHashError(f"精度必须在1-12之间，当前: {precision}")
    
    # 获取Geohash网格大小
    width_km, height_km = GEOHASH_PRECISION_SIZES[precision]
    
    # 计算采样点数量
    lat_span = lat_max - lat_min
    lng_span = lng_max - lng_min
    
    # 根据Geohash大小确定采样密度
    lat_step_deg = height_km / 111.0 * 0.8  # 稍小于一个Geohash高度
    lng_step_deg = width_km / (111.0 * math.cos(math.radians((lat_min + lat_max) / 2))) * 0.8
    
    # 确保至少有合理的采样密度
    lat_steps = max(1, int(lat_span / lat_step_deg) + 1)
    lng_steps = max(1, int(lng_span / lng_step_deg) + 1)
    
    # 限制最大采样数量防止性能问题
    max_samples = 1000
    if lat_steps * lng_steps > max_samples:
        # 自动降低精度
        scale = math.sqrt(max_samples / (lat_steps * lng_steps))
        lat_steps = max(1, int(lat_steps * scale))
        lng_steps = max(1, int(lng_steps * scale))
    
    geohashes = set()
    
    # 网格采样
    for i in range(lat_steps):
        for j in range(lng_steps):
            lat = lat_min + lat_span * i / max(1, lat_steps - 1) if lat_steps > 1 else (lat_min + lat_max) / 2
            lng = lng_min + lng_span * j / max(1, lng_steps - 1) if lng_steps > 1 else (lng_min + lng_max) / 2
            
            try:
                gh = encode(lat, lng, precision)
                geohashes.add(gh)
            except GeoHashError:
                pass
    
    return sorted(list(geohashes))


def is_valid(geohash: str) -> bool:
    """
    验证Geohash是否有效
    
    Args:
        geohash: Geohash字符串
    
    Returns:
        是否有效
    
    Example:
        >>> is_valid('wx4g0b')
        True
        >>> is_valid('wx4g0o')  # 'o' 不是有效字符
        False
    """
    if not geohash:
        return False
    
    geohash = geohash.lower()
    
    for c in geohash:
        if c not in GEOHASH_CHAR_TO_INT:
            return False
    
    return True


def expand(geohash: str, radius_km: float, max_count: int = 100) -> List[str]:
    """
    扩展Geohash以覆盖指定半径范围（简化版）
    
    Args:
        geohash: 中心Geohash
        radius_km: 半径(千米)
        max_count: 最大返回数量
    
    Returns:
        覆盖该半径范围所需的Geohash列表
    
    Example:
        >>> expand('wx4g0b', 5)
        ['wx4fb4', 'wx4fb5', ...]
    """
    center = decode(geohash)
    precision = center['precision']
    
    # 如果半径很大，可能需要降低精度
    width_km, height_km = GEOHASH_PRECISION_SIZES.get(precision, (1.0, 1.0))
    
    # 计算需要扩展的范围
    bbox = get_bounding_box(center['lat'], center['lng'], radius_km)
    
    # 使用简化方法获取范围内的Geohash
    geohashes = get_geohashes_in_bbox(
        bbox['lat_min'], bbox['lat_max'],
        bbox['lng_min'], bbox['lng_max'],
        precision
    )
    
    # 过滤掉距离太远的
    result = []
    for gh in geohashes[:max_count]:
        decoded = decode(gh)
        dist = distance(center['lat'], center['lng'], decoded['lat'], decoded['lng'])
        if dist <= radius_km * 1.5:  # 留一些余量
            result.append(gh)
    
    return sorted(result)


def midpoint(lat1: float, lng1: float, lat2: float, lng2: float) -> Tuple[float, float]:
    """
    计算两个坐标的中点
    
    Args:
        lat1: 起点纬度
        lng1: 起点经度
        lat2: 终点纬度
        lng2: 终点经度
    
    Returns:
        中点坐标 (纬度, 经度)
    
    Example:
        >>> midpoint(39.9042, 116.4074, 31.2304, 121.4737)
        (35.67..., 119.23...)
    """
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    lng1_rad = math.radians(lng1)
    lng2_rad = math.radians(lng2)
    
    dlng = lng2_rad - lng1_rad
    
    bx = math.cos(lat2_rad) * math.cos(dlng)
    by = math.cos(lat2_rad) * math.sin(dlng)
    
    lat3_rad = math.atan2(
        math.sin(lat1_rad) + math.sin(lat2_rad),
        math.sqrt((math.cos(lat1_rad) + bx) ** 2 + by ** 2)
    )
    
    lng3_rad = lng1_rad + math.atan2(by, math.cos(lat1_rad) + bx)
    
    return (math.degrees(lat3_rad), math.degrees(lng3_rad))


def destination(lat: float, lng: float,
                bearing: float, distance_km: float) -> Tuple[float, float]:
    """
    从起点沿指定方向移动一定距离后的目标点
    
    Args:
        lat: 起点纬度
        lng: 起点经度
        bearing: 方位角(度)，0=北，90=东，180=南，270=西
        distance_km: 距离(千米)
    
    Returns:
        目标点坐标 (纬度, 经度)
    
    Example:
        >>> destination(39.9042, 116.4074, 45, 100)  # 从北京向东北100公里
        (40.55..., 117.45...)
    """
    lat_rad = math.radians(lat)
    lng_rad = math.radians(lng)
    bearing_rad = math.radians(bearing)
    
    angular_dist = distance_km / EARTH_RADIUS_KM
    
    lat2_rad = math.asin(
        math.sin(lat_rad) * math.cos(angular_dist) +
        math.cos(lat_rad) * math.sin(angular_dist) * math.cos(bearing_rad)
    )
    
    lng2_rad = lng_rad + math.atan2(
        math.sin(bearing_rad) * math.sin(angular_dist) * math.cos(lat_rad),
        math.cos(angular_dist) - math.sin(lat_rad) * math.sin(lat2_rad)
    )
    
    return (math.degrees(lat2_rad), math.degrees(lng2_rad))


def bearing(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    计算从起点到终点的方位角
    
    Args:
        lat1: 起点纬度
        lng1: 赐点经度
        lat2: 终点纬度
        lng2: 终点经度
    
    Returns:
        方位角(度)，0=北，90=东，180=南，270=西
    
    Example:
        >>> bearing(39.9042, 116.4074, 31.2304, 121.4737)  # 北京到上海
        135.5...
    """
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlng_rad = math.radians(lng2 - lng1)
    
    y = math.sin(dlng_rad) * math.cos(lat2_rad)
    x = math.cos(lat1_rad) * math.sin(lat2_rad) - \
        math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlng_rad)
    
    bearing_deg = math.degrees(math.atan2(y, x))
    
    # 归一化到0-360度
    return (bearing_deg + 360) % 360


def format_geohash(geohash: str) -> str:
    """
    格式化Geohash为可视化字符串
    
    Args:
        geohash: Geohash字符串
    
    Returns:
        格式化后的字符串
    
    Example:
        >>> format_geohash('wx4g0b')
        'W X 4 G 0 B'
    """
    return ' '.join(c.upper() for c in geohash)


def geohash_to_color(geohash: str) -> str:
    """
    根据Geohash生成一个颜色代码（用于可视化）
    
    Args:
        geohash: Geohash字符串
    
    Returns:
        十六进制颜色代码
    
    Example:
        >>> geohash_to_color('wx4g0b')
        '#5c8a3f'
    """
    # 使用前3个字符生成颜色
    if len(geohash) < 3:
        geohash = geohash + '000'
    
    values = [GEOHASH_CHAR_TO_INT.get(c, 0) for c in geohash[:3]]
    
    # 映射到RGB
    r = (values[0] * 8) % 256
    g = (values[1] * 8 + 64) % 256
    b = (values[2] * 8 + 128) % 256
    
    return f'#{r:02x}{g:02x}{b:02x}'