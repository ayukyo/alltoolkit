"""
Photography Utilities - 摄影计算工具

提供曝光计算、景深计算、超焦距、视角、闪光灯计算等功能。

功能模块:
- 曝光值 (EV) 计算
- 光圈/快门/ISO 组合推荐
- 景深计算
- 超焦距计算
- 视角计算
- 等效焦距转换
- 闪光灯计算
- 阳光16法则
- 黄金时刻/蓝调时刻判断
"""

import math
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass


# ============== 常量定义 ==============

# 传感器尺寸 (mm) - 宽 x 高
SENSOR_SIZES = {
    "full_frame": (36.0, 24.0),
    "aps_c": (23.5, 15.6),  # Canon: 22.2 x 14.8, Nikon/Sony: 23.5 x 15.6
    "aps_c_canon": (22.2, 14.8),
    "micro_four_thirds": (17.3, 13.0),
    "medium_format": (44.0, 33.0),
    "aps_h": (28.7, 19.0),
    "1_inch": (13.2, 8.8),
    "smartphone": (7.6, 5.7),
}

# 标准光圈值 (f-stops)
APERTURES = [
    1.0, 1.1, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.5, 2.8,
    3.2, 3.5, 4.0, 4.5, 5.0, 5.6, 6.3, 7.1, 8.0,
    9.0, 10.0, 11.0, 13.0, 14.0, 16.0, 18.0, 20.0, 22.0
]

# 标准快门速度 (秒)
SHUTTER_SPEEDS = [
    1/8000, 1/6400, 1/5000, 1/4000, 1/3200, 1/2500, 1/2000, 1/1600,
    1/1250, 1/1000, 1/800, 1/640, 1/500, 1/400, 1/320, 1/250,
    1/200, 1/160, 1/125, 1/100, 1/80, 1/60, 1/50, 1/40, 1/30,
    1/25, 1/20, 1/15, 1/13, 1/10, 1/8, 1/6, 1/5, 1/4,
    0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.3, 1.6, 2.0, 2.5,
    3.2, 4.0, 5.0, 6.0, 8.0, 10.0, 13.0, 15.0, 20.0, 25.0, 30.0
]

# 标准 ISO 值
ISO_VALUES = [
    50, 64, 80, 100, 125, 160, 200, 250, 320, 400,
    500, 640, 800, 1000, 1250, 1600, 2000, 2500, 3200,
    4000, 5000, 6400, 8000, 10000, 12800, 16000, 20000, 25600,
    32000, 40000, 51200, 64000, 80000, 102400
]

# 阳光16法则参数
SUNNY_16_EV = {
    "sunny": 16,      # 阳光明媚
    "slight_overcast": 11,  # 轻微阴天
    "overcast": 8,    # 阴天
    "heavy_overcast": 5.6,  # 重度阴天
    "sunset": 4,      # 日落
}


@dataclass
class ExposureSettings:
    """曝光设置"""
    aperture: float
    shutter_speed: float  # 秒
    iso: int
    ev: float


@dataclass
class DepthOfField:
    """景深结果"""
    near_focus: float      # 近对焦距离 (米)
    far_focus: float       # 远对焦距离 (米)
    total_dof: float      # 总景深 (米)
    hyperfocal: float     # 超焦距 (米)


@dataclass
class AngleOfView:
    """视角结果"""
    horizontal: float      # 水平视角 (度)
    vertical: float        # 垂直视角 (度)
    diagonal: float        # 对角线视角 (度)


# ============== 曝光值计算 ==============

def calculate_ev(aperture: float, shutter_speed: float, iso: int = 100) -> float:
    """
    计算曝光值 (EV)
    
    公式: EV = log2(N²/t) - log2(ISO/100)
    其中 N 为光圈值，t 为快门速度
    
    Args:
        aperture: 光圈值 (如 f/2.8 -> 2.8)
        shutter_speed: 快门速度 (秒)
        iso: ISO 感光度 (默认 100)
    
    Returns:
        曝光值 (EV)
    
    Examples:
        >>> calculate_ev(2.8, 1/125, 100)
        10.93...
        >>> calculate_ev(8, 1/250, 200)
        13.0
    """
    if aperture <= 0 or shutter_speed <= 0 or iso <= 0:
        raise ValueError("光圈、快门速度和 ISO 必须为正数")
    
    ev_base = math.log2((aperture ** 2) / shutter_speed)
    ev_corrected = ev_base - math.log2(iso / 100)
    return round(ev_corrected, 2)


def ev_to_settings(ev: float, iso: int = 100) -> List[ExposureSettings]:
    """
    根据曝光值推荐光圈/快门组合
    
    Args:
        ev: 曝光值
        iso: ISO 感光度 (默认 100)
    
    Returns:
        推荐的曝光设置列表
    
    Examples:
        >>> settings = ev_to_settings(15, 100)
        >>> len(settings) > 0
        True
    """
    results = []
    
    for aperture in APERTURES:
        # EV = log2(N²/t) - log2(ISO/100)
        # log2(N²/t) = EV + log2(ISO/100)
        # N²/t = 2^(EV + log2(ISO/100))
        # t = N² / 2^(EV + log2(ISO/100))
        
        ev_at_iso = ev + math.log2(iso / 100)
        shutter = (aperture ** 2) / (2 ** ev_at_iso)
        
        # 找到最接近的标准快门速度
        closest_shutter = min(SHUTTER_SPEEDS, key=lambda s: abs(s - shutter))
        
        results.append(ExposureSettings(
            aperture=aperture,
            shutter_speed=closest_shutter,
            iso=iso,
            ev=round(ev, 2)
        ))
    
    return results


def adjust_exposure(
    base_aperture: float,
    base_shutter: float,
    base_iso: int,
    aperture: Optional[float] = None,
    shutter: Optional[float] = None,
    iso: Optional[int] = None
) -> ExposureSettings:
    """
    调整曝光参数（等效曝光计算）
    
    保持相同曝光值的前提下，改变其中一个参数，计算其他参数。
    
    Args:
        base_aperture: 基础光圈
        base_shutter: 基础快门速度
        base_iso: 基础 ISO
        aperture: 目标光圈 (可选)
        shutter: 目标快门速度 (可选)
        iso: 目标 ISO (可选)
    
    Returns:
        调整后的曝光设置
    
    Examples:
        >>> result = adjust_exposure(2.8, 1/125, 100, aperture=4.0)
        >>> round(result.shutter_speed, 4)
        0.004
    """
    base_ev = calculate_ev(base_aperture, base_shutter, base_iso)
    
    if aperture is not None and shutter is not None and iso is not None:
        return ExposureSettings(aperture, shutter, iso, calculate_ev(aperture, shutter, iso))
    
    if aperture is not None:
        # 改变光圈，调整快门
        if iso is not None:
            # 同时改变光圈和 ISO，计算快门
            new_shutter = (aperture ** 2) / (2 ** (base_ev + math.log2(iso / 100)))
            closest_shutter = min(SHUTTER_SPEEDS, key=lambda s: abs(s - new_shutter))
            return ExposureSettings(aperture, closest_shutter, iso, base_ev)
        else:
            # 只改变光圈，调整快门
            # N1²/t1 = N2²/t2 (at same ISO)
            new_shutter = base_shutter * (aperture ** 2) / (base_aperture ** 2)
            closest_shutter = min(SHUTTER_SPEEDS, key=lambda s: abs(s - new_shutter))
            return ExposureSettings(aperture, closest_shutter, base_iso, base_ev)
    
    if shutter is not None:
        if iso is not None:
            # 改变快门和 ISO，计算光圈
            ev_at_iso = base_ev + math.log2(iso / 100)
            aperture_squared = shutter * (2 ** ev_at_iso)
            new_aperture = math.sqrt(aperture_squared)
            closest_aperture = min(APERTURES, key=lambda a: abs(a - new_aperture))
            return ExposureSettings(closest_aperture, shutter, iso, base_ev)
        else:
            # 只改变快门，调整光圈
            new_aperture = math.sqrt(base_aperture ** 2 * shutter / base_shutter)
            closest_aperture = min(APERTURES, key=lambda a: abs(a - new_aperture))
            return ExposureSettings(closest_aperture, shutter, base_iso, base_ev)
    
    if iso is not None:
        # 只改变 ISO，调整快门
        # EV 不变: N²/t ~ ISO
        iso_ratio = iso / base_iso
        new_shutter = base_shutter / iso_ratio
        closest_shutter = min(SHUTTER_SPEEDS, key=lambda s: abs(s - new_shutter))
        return ExposureSettings(base_aperture, closest_shutter, iso, base_ev)
    
    return ExposureSettings(base_aperture, base_shutter, base_iso, base_ev)


# ============== 景深计算 ==============

def calculate_dof(
    focal_length: float,
    aperture: float,
    distance: float,
    sensor_size: str = "full_frame",
    circle_of_confusion: Optional[float] = None
) -> DepthOfField:
    """
    计算景深
    
    Args:
        focal_length: 焦距 (mm)
        aperture: 光圈值
        distance: 对焦距离 (米)
        sensor_size: 传感器尺寸类型
        circle_of_confusion: 弥散圆直径 (mm)，不指定则自动计算
    
    Returns:
        景深计算结果
    
    Examples:
        >>> dof = calculate_dof(50, 2.8, 3)
        >>> dof.total_dof > 0
        True
    """
    if focal_length <= 0 or aperture <= 0 or distance <= 0:
        raise ValueError("焦距、光圈和距离必须为正数")
    
    # 获取传感器尺寸
    if isinstance(sensor_size, str):
        if sensor_size not in SENSOR_SIZES:
            raise ValueError(f"未知的传感器尺寸: {sensor_size}")
        sensor_width, sensor_height = SENSOR_SIZES[sensor_size]
        sensor_diagonal = math.sqrt(sensor_width ** 2 + sensor_height ** 2)
    else:
        sensor_diagonal = sensor_size
    
    # 计算弥散圆 (CoC)
    # 通常取传感器对角线的 1/1500
    if circle_of_confusion is None:
        circle_of_confusion = sensor_diagonal / 1500
    
    # 转换单位
    f = focal_length  # mm
    N = aperture
    s = distance * 1000  # 转换为 mm
    c = circle_of_confusion  # mm
    
    # 超焦距 H = f²/(N*c) + f
    hyperfocal = (f ** 2) / (N * c) + f  # mm
    
    # 近对焦距离: H*s / (H + (s - f))
    near_focus = (hyperfocal * s) / (hyperfocal + s - f)  # mm
    
    # 远对焦距离: H*s / (H - (s - f))
    # 如果 s > H，则远对焦距离为无穷大
    if s >= hyperfocal:
        far_focus = float('inf')
    else:
        far_focus = (hyperfocal * s) / (hyperfocal - s + f)  # mm
    
    # 转换为米
    near_focus_m = near_focus / 1000
    far_focus_m = far_focus / 1000 if far_focus != float('inf') else float('inf')
    hyperfocal_m = hyperfocal / 1000
    
    # 总景深
    if far_focus == float('inf'):
        total_dof = float('inf')
    else:
        total_dof = (far_focus - near_focus) / 1000
    
    return DepthOfField(
        near_focus=round(near_focus_m, 4),
        far_focus=round(far_focus_m, 4) if far_focus_m != float('inf') else float('inf'),
        total_dof=round(total_dof, 4) if total_dof != float('inf') else float('inf'),
        hyperfocal=round(hyperfocal_m, 4)
    )


def calculate_hyperfocal(
    focal_length: float,
    aperture: float,
    sensor_size: str = "full_frame",
    circle_of_confusion: Optional[float] = None
) -> float:
    """
    计算超焦距
    
    对焦在超焦距时，景深从超焦距的一半延伸到无穷远。
    
    Args:
        focal_length: 焦距 (mm)
        aperture: 光圈值
        sensor_size: 传感器尺寸类型
        circle_of_confusion: 弥散圆直径 (mm)
    
    Returns:
        超焦距 (米)
    
    Examples:
        >>> h = calculate_hyperfocal(50, 8)
        >>> h > 0
        True
    """
    if focal_length <= 0 or aperture <= 0:
        raise ValueError("焦距和光圈必须为正数")
    
    # 获取传感器尺寸
    if isinstance(sensor_size, str):
        if sensor_size not in SENSOR_SIZES:
            raise ValueError(f"未知的传感器尺寸: {sensor_size}")
        sensor_width, sensor_height = SENSOR_SIZES[sensor_size]
        sensor_diagonal = math.sqrt(sensor_width ** 2 + sensor_height ** 2)
    else:
        sensor_diagonal = sensor_size
    
    if circle_of_confusion is None:
        circle_of_confusion = sensor_diagonal / 1500
    
    f = focal_length
    N = aperture
    c = circle_of_confusion
    
    hyperfocal = (f ** 2) / (N * c) + f  # mm
    return round(hyperfocal / 1000, 4)  # 转换为米


# ============== 视角计算 ==============

def calculate_angle_of_view(
    focal_length: float,
    sensor_size: str = "full_frame"
) -> AngleOfView:
    """
    计算视角
    
    Args:
        focal_length: 焦距 (mm)
        sensor_size: 传感器尺寸类型或 (宽, 高) 元组
    
    Returns:
        视角计算结果
    
    Examples:
        >>> aov = calculate_angle_of_view(50)
        >>> round(aov.diagonal, 1)
        46.8
    """
    if focal_length <= 0:
        raise ValueError("焦距必须为正数")
    
    # 获取传感器尺寸
    if isinstance(sensor_size, str):
        if sensor_size not in SENSOR_SIZES:
            raise ValueError(f"未知的传感器尺寸: {sensor_size}")
        sensor_width, sensor_height = SENSOR_SIZES[sensor_size]
    else:
        sensor_width, sensor_height = sensor_size
    
    # 计算视角: 2 * arctan(d / (2 * f))
    horizontal = 2 * math.degrees(math.atan(sensor_width / (2 * focal_length)))
    vertical = 2 * math.degrees(math.atan(sensor_height / (2 * focal_length)))
    
    sensor_diagonal = math.sqrt(sensor_width ** 2 + sensor_height ** 2)
    diagonal = 2 * math.degrees(math.atan(sensor_diagonal / (2 * focal_length)))
    
    return AngleOfView(
        horizontal=round(horizontal, 2),
        vertical=round(vertical, 2),
        diagonal=round(diagonal, 2)
    )


def calculate_equivalent_focal_length(
    focal_length: float,
    source_sensor: str,
    target_sensor: str = "full_frame"
) -> float:
    """
    计算等效焦距
    
    Args:
        focal_length: 实际焦距 (mm)
        source_sensor: 源传感器尺寸类型
        target_sensor: 目标传感器尺寸类型 (默认全画幅)
    
    Returns:
        等效焦距 (mm)
    
    Examples:
        >>> eq = calculate_equivalent_focal_length(35, "aps_c")
        >>> round(eq, 1)
        52.5
    """
    if focal_length <= 0:
        raise ValueError("焦距必须为正数")
    
    if source_sensor not in SENSOR_SIZES:
        raise ValueError(f"未知的源传感器尺寸: {source_sensor}")
    if target_sensor not in SENSOR_SIZES:
        raise ValueError(f"未知的目标传感器尺寸: {target_sensor}")
    
    # 计算裁剪系数
    source_diagonal = math.sqrt(SENSOR_SIZES[source_sensor][0] ** 2 + 
                                SENSOR_SIZES[source_sensor][1] ** 2)
    target_diagonal = math.sqrt(SENSOR_SIZES[target_sensor][0] ** 2 + 
                                SENSOR_SIZES[target_sensor][1] ** 2)
    
    crop_factor = target_diagonal / source_diagonal
    equivalent = focal_length * crop_factor
    
    return round(equivalent, 2)


def get_crop_factor(sensor_size: str, reference: str = "full_frame") -> float:
    """
    获取裁剪系数
    
    Args:
        sensor_size: 传感器尺寸类型
        reference: 参考传感器 (默认全画幅)
    
    Returns:
        裁剪系数
    
    Examples:
        >>> cf = get_crop_factor("aps_c")
        >>> round(cf, 2)
        1.53
    """
    if sensor_size not in SENSOR_SIZES:
        raise ValueError(f"未知的传感器尺寸: {sensor_size}")
    if reference not in SENSOR_SIZES:
        raise ValueError(f"未知的参考传感器尺寸: {reference}")
    
    ref_diagonal = math.sqrt(SENSOR_SIZES[reference][0] ** 2 + 
                             SENSOR_SIZES[reference][1] ** 2)
    sensor_diagonal = math.sqrt(SENSOR_SIZES[sensor_size][0] ** 2 + 
                                SENSOR_SIZES[sensor_size][1] ** 2)
    
    return round(ref_diagonal / sensor_diagonal, 2)


# ============== 闪光灯计算 ==============

def calculate_flash_distance(
    guide_number: float,
    aperture: float,
    iso: int = 100
) -> float:
    """
    根据闪光指数计算闪光灯有效距离
    
    公式: 距离 = GN / 光圈 (ISO 100)
    
    Args:
        guide_number: 闪光指数 (米 @ ISO 100)
        aperture: 光圈值
        iso: ISO 感光度
    
    Returns:
        有效距离 (米)
    
    Examples:
        >>> dist = calculate_flash_distance(36, 4, 100)
        >>> dist
        9.0
    """
    if guide_number <= 0 or aperture <= 0 or iso <= 0:
        raise ValueError("闪光指数、光圈和 ISO 必须为正数")
    
    # ISO 修正: 距离增加 sqrt(ISO/100) 倍
    distance = (guide_number / aperture) * math.sqrt(iso / 100)
    return round(distance, 2)


def calculate_guide_number(
    distance: float,
    aperture: float,
    iso: int = 100
) -> float:
    """
    根据距离和光圈计算所需闪光指数
    
    Args:
        distance: 距离 (米)
        aperture: 光圈值
        iso: ISO 感光度
    
    Returns:
        闪光指数 (米 @ ISO 100)
    
    Examples:
        >>> gn = calculate_guide_number(9, 4, 100)
        >>> gn
        36.0
    """
    if distance <= 0 or aperture <= 0 or iso <= 0:
        raise ValueError("距离、光圈和 ISO 必须为正数")
    
    # 反算 GN
    gn = distance * aperture / math.sqrt(iso / 100)
    return round(gn, 2)


def calculate_flash_aperture(
    guide_number: float,
    distance: float,
    iso: int = 100
) -> float:
    """
    根据闪光指数和距离计算所需光圈
    
    Args:
        guide_number: 闪光指数 (米 @ ISO 100)
        distance: 距离 (米)
        iso: ISO 感光度
    
    Returns:
        所需光圈值
    
    Examples:
        >>> ap = calculate_flash_aperture(36, 9, 100)
        >>> ap
        4.0
    """
    if guide_number <= 0 or distance <= 0 or iso <= 0:
        raise ValueError("闪光指数、距离和 ISO 必须为正数")
    
    aperture = guide_number / (distance * math.sqrt(iso / 100))
    # 找到最接近的标准光圈
    closest = min(APERTURES, key=lambda a: abs(a - aperture))
    return closest


# ============== 阳光16法则 ==============

def sunny_16(
    condition: str = "sunny",
    aperture: float = 16,
    iso: int = 100
) -> Tuple[float, int, float]:
    """
    阳光16法则 - 估计曝光
    
    在阳光明媚的日子里，f/16 光圈下快门速度约为 1/ISO。
    
    Args:
        condition: 光照条件 (sunny, slight_overcast, overcast, heavy_overcast, sunset)
        aperture: 光圈值 (默认 f/16)
        iso: ISO 感光度
    
    Returns:
        (推荐快门速度, ISO, 曝光值)
    
    Examples:
        >>> shutter, iso, ev = sunny_16("sunny", 16, 100)
        >>> round(shutter, 4)
        0.01
    """
    if condition not in SUNNY_16_EV:
        raise ValueError(f"未知的光照条件: {condition}。可选: {list(SUNNY_16_EV.keys())}")
    
    # 基础光圈
    base_aperture = SUNNY_16_EV[condition]
    
    # 计算快门速度
    # 阳光16法则: 在 f/16 下，快门速度 = 1/ISO
    # 如果光圈不是 f/16，则调整快门
    base_shutter = 1 / iso  # 基础快门 @ f/16
    
    # 根据光圈调整快门
    # 曝光恒定: N²/t = 常数
    # t = N² / (16² * base_shutter)
    shutter = base_shutter * (aperture / base_aperture) ** 2
    
    # 计算曝光值
    ev = calculate_ev(aperture, shutter, iso)
    
    return (round(shutter, 6), iso, ev)


# ============== 黄金时刻/蓝调时刻 ==============

def is_golden_hour(
    solar_elevation: float,
    morning: bool = True
) -> Tuple[bool, str]:
    """
    判断是否为黄金时刻
    
    黄金时刻: 太阳高度角 0°-6° (日出后/日落前)
    
    Args:
        solar_elevation: 太阳高度角 (度)
        morning: True 为早晨，False 为傍晚
    
    Returns:
        (是否黄金时刻, 描述)
    
    Examples:
        >>> is_golden, desc = is_golden_hour(3)
        >>> is_golden
        True
    """
    if 0 <= solar_elevation <= 6:
        period = "日出黄金时刻" if morning else "日落黄金时刻"
        return (True, period)
    elif 6 < solar_elevation <= 15:
        return (False, "黄金时刻刚结束/即将开始")
    else:
        return (False, "非黄金时刻")


def is_blue_hour(
    solar_elevation: float,
    morning: bool = True
) -> Tuple[bool, str]:
    """
    判断是否为蓝调时刻
    
    蓝调时刻: 太阳高度角 -4° 到 6° (日出前/日落后)
    
    Args:
        solar_elevation: 太阳高度角 (度)
        morning: True 为早晨，False 为傍晚
    
    Returns:
        (是否蓝调时刻, 描述)
    
    Examples:
        >>> is_blue, desc = is_blue_hour(-2)
        >>> is_blue
        True
    """
    if -4 <= solar_elevation < 0:
        period = "早晨蓝调时刻" if morning else "傍晚蓝调时刻"
        return (True, period)
    elif 0 <= solar_elevation <= 6:
        return (True, "蓝调时刻/黄金时刻重叠")
    else:
        return (False, "非蓝调时刻")


# ============== 放大倍率 ==============

def calculate_magnification(
    focal_length: float,
    subject_distance: float
) -> float:
    """
    计算放大倍率
    
    对于普通镜头（非微距），近似公式: M = f / (s - f)
    
    Args:
        focal_length: 焦距 (mm)
        subject_distance: 主体距离 (米)
    
    Returns:
        放大倍率
    
    Examples:
        >>> m = calculate_magnification(50, 1)
        >>> round(m, 4)
        0.0526
    """
    if focal_length <= 0 or subject_distance <= 0:
        raise ValueError("焦距和主体距离必须为正数")
    
    f = focal_length
    s = subject_distance * 1000  # 转换为 mm
    
    magnification = f / (s - f)
    return round(magnification, 6)


def calculate_closest_focus_distance(
    focal_length: float,
    max_magnification: float
) -> float:
    """
    根据最大放大倍率计算最近对焦距离
    
    Args:
        focal_length: 焦距 (mm)
        max_magnification: 最大放大倍率
    
    Returns:
        最近对焦距离 (米)
    
    Examples:
        >>> dist = calculate_closest_focus_distance(50, 0.15)
        >>> round(dist, 2)
        0.38
    """
    if focal_length <= 0 or max_magnification <= 0:
        raise ValueError("焦距和最大放大倍率必须为正数")
    
    # M = f / (s - f)
    # s = f * (1/M + 1)
    distance_mm = focal_length * (1 / max_magnification + 1)
    return round(distance_mm / 1000, 2)


# ============== 镜头分类 ==============

def classify_lens(focal_length: float, sensor_size: str = "full_frame") -> str:
    """
    根据焦距分类镜头类型
    
    Args:
        focal_length: 焦距 (mm)
        sensor_size: 传感器尺寸类型
    
    Returns:
        镜头类型描述
    
    Examples:
        >>> classify_lens(14)
        '超广角'
        >>> classify_lens(50)
        '标准'
        >>> classify_lens(200)
        '长焦'
    """
    # 转换为等效焦距
    if sensor_size != "full_frame":
        eq_focal = calculate_equivalent_focal_length(focal_length, sensor_size)
    else:
        eq_focal = focal_length
    
    if eq_focal < 14:
        return "鱼眼"
    elif eq_focal < 24:
        return "超广角"
    elif eq_focal < 35:
        return "广角"
    elif eq_focal < 50:
        return "小广角"
    elif eq_focal < 60:
        return "标准"
    elif eq_focal < 85:
        return "中焦"
    elif eq_focal < 135:
        return "人像"
    elif eq_focal < 300:
        return "长焦"
    elif eq_focal < 500:
        return "超长焦"
    else:
        return "超远摄"


# ============== 安全快门 ==============

def calculate_safe_shutter(
    focal_length: float,
    sensor_size: str = "full_frame",
    image_stabilization: int = 0
) -> float:
    """
    计算安全快门速度（防止手抖模糊）
    
    经验法则: 安全快门 ≥ 1/等效焦距
    
    Args:
        focal_length: 焦距 (mm)
        sensor_size: 传感器尺寸类型
        image_stabilization: 防抖级数 (如 4 表示 4 档防抖)
    
    Returns:
        推荐的最慢快门速度 (秒)
    
    Examples:
        >>> shutter = calculate_safe_shutter(50)
        >>> round(shutter, 4)
        0.02
    """
    # 转换为等效焦距
    eq_focal = calculate_equivalent_focal_length(focal_length, sensor_size) \
        if sensor_size != "full_frame" else focal_length
    
    # 安全快门 = 1 / 等效焦距
    safe_shutter = 1 / eq_focal
    
    # 考虑防抖
    if image_stabilization > 0:
        safe_shutter *= (2 ** image_stabilization)
    
    # 找到最接近的标准快门速度
    closest = min(SHUTTER_SPEEDS, key=lambda s: abs(s - safe_shutter))
    return closest


# ============== 星空摄影 ==============

def calculate_500_rule(
    focal_length: float,
    sensor_size: str = "full_frame"
) -> float:
    """
    计算500法则 - 星空摄影最大曝光时间
    
    防止星星拖尾的经验法则: 曝光时间 ≤ 500 / 等效焦距
    
    Args:
        focal_length: 焦距 (mm)
        sensor_size: 传感器尺寸类型
    
    Returns:
        最大曝光时间 (秒)
    
    Examples:
        >>> max_exp = calculate_500_rule(24)
        >>> round(max_exp, 1)
        20.8
    """
    eq_focal = calculate_equivalent_focal_length(focal_length, sensor_size) \
        if sensor_size != "full_frame" else focal_length
    
    max_exposure = 500 / eq_focal
    return round(max_exposure, 1)


def calculate_npf_rule(
    focal_length: float,
    aperture: float,
    pixel_pitch: float,
    sensor_size: str = "full_frame"
) -> float:
    """
    计算NPF法则 - 更精确的星空曝光计算
    
    考虑传感器像素间距的更精确法则
    
    Args:
        focal_length: 焦距 (mm)
        aperture: 光圈值
        pixel_pitch: 像素间距 (微米)
        sensor_size: 传感器尺寸类型
    
    Returns:
        最大曝光时间 (秒)
    
    Examples:
        >>> max_exp = calculate_npf_rule(24, 1.4, 4.8)
        >>> round(max_exp, 1) > 0
        True
    """
    eq_focal = calculate_equivalent_focal_length(focal_length, sensor_size) \
        if sensor_size != "full_frame" else focal_length
    
    # NPF 公式
    # t = (35 * N + 30 * p) / f
    # N = 光圈, p = 像素间距 (μm), f = 等效焦距
    
    max_exposure = (35 * aperture + 30 * pixel_pitch) / eq_focal
    return round(max_exposure, 1)


# ============== 综合曝光计算 ==============

def exposure_recommendation(
    ev: float,
    priority: str = "aperture",
    target_value: Optional[float] = None,
    iso: int = 100
) -> ExposureSettings:
    """
    根据曝光值推荐曝光参数
    
    Args:
        ev: 曝光值
        priority: 优先模式 ("aperture" 光圈优先, "shutter" 快门优先, "iso" ISO优先)
        target_value: 目标值 (光圈/快门/ISO)
        iso: 基础 ISO
    
    Returns:
        推荐的曝光设置
    
    Examples:
        >>> settings = exposure_recommendation(15, "aperture", 8)
        >>> settings.aperture == 8
        True
    """
    if priority == "aperture" and target_value is not None:
        # 光圈优先，计算快门
        ev_at_iso = ev + math.log2(iso / 100)
        shutter = (target_value ** 2) / (2 ** ev_at_iso)
        closest_shutter = min(SHUTTER_SPEEDS, key=lambda s: abs(s - shutter))
        return ExposureSettings(target_value, closest_shutter, iso, ev)
    
    elif priority == "shutter" and target_value is not None:
        # 快门优先，计算光圈
        ev_at_iso = ev + math.log2(iso / 100)
        aperture_sq = target_value * (2 ** ev_at_iso)
        aperture = math.sqrt(aperture_sq)
        closest_aperture = min(APERTURES, key=lambda a: abs(a - aperture))
        return ExposureSettings(closest_aperture, target_value, iso, ev)
    
    elif priority == "iso" and target_value is not None:
        # ISO 优先，计算光圈和快门
        # 使用中等光圈
        aperture = 5.6
        ev_at_iso = ev + math.log2(target_value / 100)
        shutter = (aperture ** 2) / (2 ** ev_at_iso)
        closest_shutter = min(SHUTTER_SPEEDS, key=lambda s: abs(s - shutter))
        return ExposureSettings(aperture, closest_shutter, int(target_value), ev)
    
    else:
        # 自动模式，使用 f/8 光圈
        return exposure_recommendation(ev, "aperture", 8.0, iso)


# ============== 格式化工具 ==============

def format_shutter_speed(seconds: float) -> str:
    """
    格式化快门速度
    
    Args:
        seconds: 快门速度 (秒)
    
    Returns:
        格式化的字符串 (如 "1/125" 或 "1.5s")
    
    Examples:
        >>> format_shutter_speed(1/125)
        '1/125'
        >>> format_shutter_speed(1.5)
        '1.5s'
    """
    if seconds >= 1:
        return f"{seconds:.1f}s".rstrip('0').rstrip('.')
    else:
        # 找到最接近的分数表示
        fraction = round(1 / seconds)
        return f"1/{fraction}"


def format_aperture(aperture: float) -> str:
    """
    格式化光圈值
    
    Args:
        aperture: 光圈值
    
    Returns:
        格式化的字符串 (如 "f/2.8")
    
    Examples:
        >>> format_aperture(2.8)
        'f/2.8'
    """
    return f"f/{aperture}"


def format_focal_length(focal_length: float) -> str:
    """
    格式化焦距
    
    Args:
        focal_length: 焦距 (mm)
    
    Returns:
        格式化的字符串 (如 "50mm")
    
    Examples:
        >>> format_focal_length(50)
        '50mm'
    """
    return f"{int(focal_length)}mm"


if __name__ == "__main__":
    # 示例用法
    print("=== 曝光值计算 ===")
    ev = calculate_ev(2.8, 1/125, 100)
    print(f"f/2.8, 1/125s, ISO 100 -> EV: {ev}")
    
    print("\n=== 景深计算 ===")
    dof = calculate_dof(50, 2.8, 3, "full_frame")
    print(f"50mm @ f/2.8, 对焦3米 -> 景深: {dof.near_focus}m - {dof.far_focus}m")
    print(f"超焦距: {dof.hyperfocal}m")
    
    print("\n=== 视角计算 ===")
    aov = calculate_angle_of_view(50)
    print(f"50mm 镜头视角: 水平{aov.horizontal}°, 垂直{aov.vertical}°, 对角{aov.diagonal}°")
    
    print("\n=== 等效焦距 ===")
    eq = calculate_equivalent_focal_length(35, "aps_c")
    print(f"APS-C 35mm 等效焦距: {eq}mm")
    
    print("\n=== 闪光灯计算 ===")
    dist = calculate_flash_distance(36, 4, 100)
    print(f"GN 36 @ f/4 ISO 100 -> 距离: {dist}m")
    
    print("\n=== 阳光16法则 ===")
    shutter, iso, ev = sunny_16("sunny", 16, 100)
    print(f"晴天 f/16 ISO 100 -> 快门: {format_shutter_speed(shutter)}")
    
    print("\n=== 镜头分类 ===")
    print(f"14mm: {classify_lens(14)}")
    print(f"50mm: {classify_lens(50)}")
    print(f"200mm: {classify_lens(200)}")
    
    print("\n=== 安全快门 ===")
    safe = calculate_safe_shutter(50)
    print(f"50mm 安全快门: {format_shutter_speed(safe)}")
    
    print("\n=== 星空摄影 ===")
    max_exp = calculate_500_rule(24)
    print(f"24mm 星空最大曝光 (500法则): {max_exp}s")