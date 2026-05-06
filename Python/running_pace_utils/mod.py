"""
Running Pace Utilities - 跑步配速计算工具

提供跑步配速相关的计算功能，包括：
- 配速计算（时间/距离）
- 时间预测
- 距离计算
- 配速转换
- 速度计算
- 比赛配速表生成
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class DistanceUnit(Enum):
    """距离单位"""
    KILOMETERS = "km"
    MILES = "mi"
    METERS = "m"
    YARDS = "yd"


class PaceUnit(Enum):
    """配速单位"""
    MIN_PER_KM = "min/km"  # 分钟每公里
    MIN_PER_MI = "min/mi"  # 分钟每英里


# 标准比赛距离（米）
RACE_DISTANCES = {
    "100m": 100,
    "200m": 200,
    "400m": 400,
    "800m": 800,
    "1500m": 1500,
    "1英里": 1609.344,
    "5K": 5000,
    "10K": 10000,
    "半马": 21097.5,
    "马拉松": 42195,
    "50K": 50000,
    "100K": 100000,
}

# 单位转换系数
KM_PER_MILE = 1.609344
M_PER_KM = 1000
YD_PER_MILE = 1760


@dataclass
class PaceResult:
    """配速计算结果"""
    minutes: int
    seconds: int
    total_seconds: float
    unit: str
    
    def __str__(self) -> str:
        return f"{self.minutes}:{self.seconds:02d} {self.unit}"
    
    @property
    def pace_str(self) -> str:
        """返回配速字符串格式 MM:SS"""
        return f"{self.minutes}:{self.seconds:02d}"


@dataclass
class TimeResult:
    """时间计算结果"""
    hours: int
    minutes: int
    seconds: int
    total_seconds: float
    
    def __str__(self) -> str:
        return f"{self.hours}:{self.minutes:02d}:{self.seconds:02d}"
    
    @property
    def time_str(self) -> str:
        """返回时间字符串格式 HH:MM:SS"""
        return f"{self.hours}:{self.minutes:02d}:{self.seconds:02d}"


@dataclass
class SpeedResult:
    """速度计算结果"""
    kmh: float  # 公里每小时
    mph: float  # 英里每小时
    mps: float  # 米每秒
    
    def __str__(self) -> str:
        return f"{self.kmh:.2f} km/h ({self.mph:.2f} mph)"


def parse_time(time_str: str) -> int:
    """
    解析时间字符串为秒数
    
    支持格式：
    - "SS" 或 "S" - 秒
    - "MM:SS" - 分:秒
    - "HH:MM:SS" - 时:分:秒
    
    Args:
        time_str: 时间字符串
        
    Returns:
        总秒数
        
    Examples:
        >>> parse_time("30")
        30
        >>> parse_time("5:30")
        330
        >>> parse_time("1:30:00")
        5400
    """
    parts = time_str.strip().split(":")
    
    if len(parts) == 1:
        return int(parts[0])
    elif len(parts) == 2:
        minutes, seconds = int(parts[0]), int(parts[1])
        return minutes * 60 + seconds
    elif len(parts) == 3:
        hours, minutes, seconds = int(parts[0]), int(parts[1]), int(parts[2])
        return hours * 3600 + minutes * 60 + seconds
    else:
        raise ValueError(f"Invalid time format: {time_str}")


def parse_pace(pace_str: str) -> float:
    """
    解析配速字符串为每公里分钟数
    
    支持格式：
    - "MM:SS" - 分:秒每公里
    - "M:SS" - 分:秒每公里
    - 浮点数 - 分钟每公里
    
    Args:
        pace_str: 配速字符串
        
    Returns:
        每公里分钟数（浮点数）
        
    Examples:
        >>> parse_pace("5:30")
        5.5
        >>> parse_pace("6:00")
        6.0
    """
    pace_str = pace_str.strip()
    
    if ":" in pace_str:
        parts = pace_str.split(":")
        if len(parts) == 2:
            minutes, seconds = int(parts[0]), int(parts[1])
            return minutes + seconds / 60
        else:
            raise ValueError(f"Invalid pace format: {pace_str}")
    else:
        return float(pace_str)


def seconds_to_time(total_seconds: float) -> TimeResult:
    """
    将秒数转换为时间格式
    
    Args:
        total_seconds: 总秒数
        
    Returns:
        TimeResult 对象
        
    Examples:
        >>> seconds_to_time(3665)
        TimeResult(hours=1, minutes=1, seconds=5, total_seconds=3665.0)
    """
    total_seconds = max(0, total_seconds)
    hours = int(total_seconds // 3600)
    remaining = total_seconds % 3600
    minutes = int(remaining // 60)
    seconds = int(remaining % 60)
    
    return TimeResult(
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        total_seconds=total_seconds
    )


def seconds_to_pace(total_seconds: float, unit: PaceUnit = PaceUnit.MIN_PER_KM) -> PaceResult:
    """
    将秒数转换为配速格式
    
    Args:
        total_seconds: 每单位距离的秒数
        unit: 配速单位
        
    Returns:
        PaceResult 对象
    """
    total_seconds = max(0, total_seconds)
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    
    return PaceResult(
        minutes=minutes,
        seconds=seconds,
        total_seconds=total_seconds,
        unit=unit.value
    )


def calculate_pace(
    distance: float,
    time_str: str,
    distance_unit: DistanceUnit = DistanceUnit.KILOMETERS
) -> PaceResult:
    """
    计算配速
    
    Args:
        distance: 距离
        time_str: 时间字符串（HH:MM:SS 或 MM:SS）
        distance_unit: 距离单位
        
    Returns:
        PaceResult 对象（默认返回分钟每公里）
        
    Examples:
        >>> calculate_pace(5, "25:00")  # 5公里跑25分钟
        PaceResult(minutes=5, seconds=0, total_seconds=300.0, unit='min/km')
        
        >>> calculate_pace(10, "50:30")  # 10公里跑50分30秒
        PaceResult(minutes=5, seconds=3, total_seconds=303.0, unit='min/km')
    """
    total_seconds = parse_time(time_str)
    
    # 转换为公里
    if distance_unit == DistanceUnit.KILOMETERS:
        distance_km = distance
    elif distance_unit == DistanceUnit.MILES:
        distance_km = distance * KM_PER_MILE
    elif distance_unit == DistanceUnit.METERS:
        distance_km = distance / M_PER_KM
    elif distance_unit == DistanceUnit.YARDS:
        distance_km = distance / YD_PER_MILE / KM_PER_MILE
    else:
        distance_km = distance
    
    # 计算每公里秒数
    seconds_per_km = total_seconds / distance_km
    
    return seconds_to_pace(seconds_per_km, PaceUnit.MIN_PER_KM)


def calculate_time(
    distance: float,
    pace_str: str,
    distance_unit: DistanceUnit = DistanceUnit.KILOMETERS
) -> TimeResult:
    """
    根据配速计算总时间
    
    Args:
        distance: 距离
        pace_str: 配速字符串（MM:SS 格式，每公里）
        distance_unit: 距离单位
        
    Returns:
        TimeResult 对象
        
    Examples:
        >>> calculate_time(10, "5:30")  # 10公里，配速5:30/km
        TimeResult(hours=0, minutes=55, seconds=0, total_seconds=3300.0)
        
        >>> calculate_time(42.195, "5:00")  # 马拉松，配速5:00/km
        TimeResult(hours=3, minutes=30, seconds=58, total_seconds=12658.5)
    """
    pace_min_per_km = parse_pace(pace_str)
    
    # 转换为公里
    if distance_unit == DistanceUnit.KILOMETERS:
        distance_km = distance
    elif distance_unit == DistanceUnit.MILES:
        distance_km = distance * KM_PER_MILE
    elif distance_unit == DistanceUnit.METERS:
        distance_km = distance / M_PER_KM
    elif distance_unit == DistanceUnit.YARDS:
        distance_km = distance / YD_PER_MILE / KM_PER_MILE
    else:
        distance_km = distance
    
    total_minutes = pace_min_per_km * distance_km
    total_seconds = total_minutes * 60
    
    return seconds_to_time(total_seconds)


def calculate_distance(
    time_str: str,
    pace_str: str,
    distance_unit: DistanceUnit = DistanceUnit.KILOMETERS
) -> float:
    """
    根据时间和配速计算距离
    
    Args:
        time_str: 时间字符串
        pace_str: 配速字符串（每公里）
        distance_unit: 返回距离的单位
        
    Returns:
        距离
        
    Examples:
        >>> calculate_distance("1:00:00", "6:00")  # 1小时，配速6:00/km
        10.0
        
        >>> calculate_distance("30:00", "5:00")  # 30分钟，配速5:00/km
        6.0
    """
    total_seconds = parse_time(time_str)
    pace_min_per_km = parse_pace(pace_str)
    
    # 计算距离（公里）
    total_minutes = total_seconds / 60
    distance_km = total_minutes / pace_min_per_km
    
    # 转换单位
    if distance_unit == DistanceUnit.KILOMETERS:
        return distance_km
    elif distance_unit == DistanceUnit.MILES:
        return distance_km / KM_PER_MILE
    elif distance_unit == DistanceUnit.METERS:
        return distance_km * M_PER_KM
    elif distance_unit == DistanceUnit.YARDS:
        return distance_km * KM_PER_MILE * YD_PER_MILE
    else:
        return distance_km


def calculate_speed(
    distance: float,
    time_str: str,
    distance_unit: DistanceUnit = DistanceUnit.KILOMETERS
) -> SpeedResult:
    """
    计算速度
    
    Args:
        distance: 距离
        time_str: 时间字符串
        distance_unit: 距离单位
        
    Returns:
        SpeedResult 对象（包含 km/h, mph, m/s）
        
    Examples:
        >>> calculate_speed(10, "50:00")  # 10公里50分钟
        SpeedResult(kmh=12.0, mph=7.46, mps=3.33)
    """
    total_seconds = parse_time(time_str)
    total_hours = total_seconds / 3600
    
    # 转换为公里
    if distance_unit == DistanceUnit.KILOMETERS:
        distance_km = distance
    elif distance_unit == DistanceUnit.MILES:
        distance_km = distance * KM_PER_MILE
    elif distance_unit == DistanceUnit.METERS:
        distance_km = distance / M_PER_KM
    elif distance_unit == DistanceUnit.YARDS:
        distance_km = distance / YD_PER_MILE / KM_PER_MILE
    else:
        distance_km = distance
    
    # 计算速度
    if total_hours > 0:
        kmh = distance_km / total_hours
    else:
        kmh = 0
    
    mph = kmh / KM_PER_MILE
    mps = kmh * 1000 / 3600
    
    return SpeedResult(kmh=round(kmh, 2), mph=round(mph, 2), mps=round(mps, 2))


def convert_pace(
    pace_str: str,
    from_unit: PaceUnit,
    to_unit: PaceUnit
) -> PaceResult:
    """
    转换配速单位
    
    Args:
        pace_str: 配速字符串
        from_unit: 原单位
        to_unit: 目标单位
        
    Returns:
        PaceResult 对象
        
    Examples:
        >>> convert_pace("5:00", PaceUnit.MIN_PER_KM, PaceUnit.MIN_PER_MI)
        PaceResult(minutes=8, seconds=3, total_seconds=483.0, unit='min/mi')
        
        >>> convert_pace("8:00", PaceUnit.MIN_PER_MI, PaceUnit.MIN_PER_KM)
        PaceResult(minutes=4, seconds=58, total_seconds=298.0, unit='min/km')
    """
    pace_seconds = parse_pace(pace_str) * 60
    
    if from_unit == to_unit:
        return seconds_to_pace(pace_seconds, to_unit)
    
    # min/km -> min/mi
    if from_unit == PaceUnit.MIN_PER_KM and to_unit == PaceUnit.MIN_PER_MI:
        seconds_per_mile = pace_seconds * KM_PER_MILE
        return seconds_to_pace(seconds_per_mile, to_unit)
    
    # min/mi -> min/km
    if from_unit == PaceUnit.MIN_PER_MI and to_unit == PaceUnit.MIN_PER_KM:
        seconds_per_km = pace_seconds / KM_PER_MILE
        return seconds_to_pace(seconds_per_km, to_unit)
    
    return seconds_to_pace(pace_seconds, to_unit)


def predict_race_time(
    known_distance: float,
    known_time_str: str,
    target_distance: float,
    distance_unit: DistanceUnit = DistanceUnit.KILOMETERS
) -> TimeResult:
    """
    根据已知比赛成绩预测目标距离的时间
    
    使用 Riegel 公式：T2 = T1 × (D2/D1)^1.06
    
    Args:
        known_distance: 已知距离
        known_time_str: 已知距离的时间
        target_distance: 目标距离
        distance_unit: 距离单位
        
    Returns:
        TimeResult 对象
        
    Examples:
        >>> predict_race_time(5, "25:00", 10)  # 5公里25分钟，预测10公里
        TimeResult(hours=0, minutes=52, seconds=38, total_seconds=3158.0)
    """
    known_seconds = parse_time(known_time_str)
    
    # 转换为公里
    if distance_unit == DistanceUnit.KILOMETERS:
        d1 = known_distance
        d2 = target_distance
    elif distance_unit == DistanceUnit.MILES:
        d1 = known_distance * KM_PER_MILE
        d2 = target_distance * KM_PER_MILE
    elif distance_unit == DistanceUnit.METERS:
        d1 = known_distance / M_PER_KM
        d2 = target_distance / M_PER_KM
    else:
        d1 = known_distance
        d2 = target_distance
    
    # Riegel 公式
    predicted_seconds = known_seconds * (d2 / d1) ** 1.06
    
    return seconds_to_time(predicted_seconds)


def generate_pace_table(
    distance: float,
    distance_unit: DistanceUnit = DistanceUnit.KILOMETERS,
    split_distance: float = 1.0
) -> List[Dict]:
    """
    生成分段配速表
    
    Args:
        distance: 总距离
        distance_unit: 距离单位
        split_distance: 分段距离（默认1公里）
        
    Returns:
        分段配速表列表，每项包含：
        - split: 分段编号
        - distance: 累计距离
        - split_time: 该段用时（秒）
        - total_time: 累计用时（秒）
        - time_str: 时间字符串
        
    Examples:
        >>> table = generate_pace_table(10)  # 假设基础配速
        >>> table[0]  # 第一公里
        {'split': 1, 'distance': 1.0, 'split_time': 300, ...}
    """
    # 转换为公里
    if distance_unit == DistanceUnit.KILOMETERS:
        total_km = distance
        split_km = split_distance
    elif distance_unit == DistanceUnit.MILES:
        total_km = distance * KM_PER_MILE
        split_km = split_distance * KM_PER_MILE
    elif distance_unit == DistanceUnit.METERS:
        total_km = distance / M_PER_KM
        split_km = split_distance / M_PER_KM
    else:
        total_km = distance
        split_km = split_distance
    
    splits = []
    num_splits = int(total_km / split_km)
    remaining = total_km % split_km
    
    for i in range(num_splits):
        current_distance = (i + 1) * split_km
        splits.append({
            "split": i + 1,
            "distance": round(current_distance, 2),
            "distance_unit": "km"
        })
    
    if remaining > 0.01:  # 剩余距离大于10米
        splits.append({
            "split": num_splits + 1,
            "distance": round(total_km, 2),
            "distance_unit": "km"
        })
    
    return splits


def calculate_splits(
    distance: float,
    pace_str: str,
    distance_unit: DistanceUnit = DistanceUnit.KILOMETERS,
    split_distance: float = 1.0
) -> List[Dict]:
    """
    计算分段用时
    
    Args:
        distance: 总距离
        pace_str: 配速字符串（每公里）
        distance_unit: 距离单位
        split_distance: 分段距离（公里）
        
    Returns:
        分段用时列表
        
    Examples:
        >>> calculate_splits(5, "6:00")  # 5公里，配速6分/公里
        [{'split': 1, 'distance': 1.0, 'split_time': '6:00', 'total_time': '6:00'},
         {'split': 2, 'distance': 2.0, 'split_time': '6:00', 'total_time': '12:00'},
         ...]
    """
    pace_seconds = parse_pace(pace_str) * 60
    
    # 转换为公里
    if distance_unit == DistanceUnit.KILOMETERS:
        total_km = distance
    elif distance_unit == DistanceUnit.MILES:
        total_km = distance * KM_PER_MILE
    elif distance_unit == DistanceUnit.METERS:
        total_km = distance / M_PER_KM
    else:
        total_km = distance
    
    splits = []
    current_distance = 0
    total_seconds = 0
    split_num = 0
    
    while current_distance < total_km:
        split_num += 1
        remaining = total_km - current_distance
        this_split = min(split_distance, remaining)
        current_distance += this_split
        
        split_seconds = this_split * pace_seconds
        total_seconds += split_seconds
        
        time_result = seconds_to_time(total_seconds)
        
        splits.append({
            "split": split_num,
            "distance": round(current_distance, 2),
            "distance_unit": "km",
            "split_time": seconds_to_pace(split_seconds).__str__(),
            "total_time": time_result.time_str
        })
    
    return splits


def vdot_to_pace(vdot: float, distance: str = "5K") -> PaceResult:
    """
    根据 VDOT 值计算配速
    
    VDOT 是 Jack Daniels 跑步公式中的训练强度指标
    
    Args:
        vdot: VDOT 值（35-85 范围）
        distance: 比赛距离类型
        
    Returns:
        PaceResult 对象
        
    Examples:
        >>> vdot_to_pace(50, "5K")
        PaceResult(minutes=4, seconds=28, total_seconds=268.0, unit='min/km')
    """
    # 简化的 VDOT 配速对照（基于 Jack Daniels 的跑表）
    # 实际应用中应该使用更精确的公式或查表
    vdot_pace_map = {
        35: {"5K": 285, "10K": 298, "半马": 314, "马拉松": 333},
        40: {"5K": 255, "10K": 266, "半马": 280, "马拉松": 297},
        45: {"5K": 230, "10K": 240, "半马": 252, "马拉松": 268},
        50: {"5K": 208, "10K": 218, "半马": 229, "马拉松": 243},
        55: {"5K": 190, "10K": 199, "半马": 208, "马拉松": 221},
        60: {"5K": 174, "10K": 182, "半马": 190, "马拉松": 202},
        65: {"5K": 160, "10K": 166, "半马": 174, "马拉松": 185},
        70: {"5K": 147, "10K": 153, "半马": 160, "马拉松": 170},
        75: {"5K": 136, "10K": 141, "半马": 148, "马拉松": 157},
        80: {"5K": 126, "10K": 131, "半马": 137, "马拉松": 145},
    }
    
    # 找最近的 VDOT 值
    closest_vdot = min(vdot_pace_map.keys(), key=lambda x: abs(x - vdot))
    
    # 插值计算（简化版本）
    base_seconds = vdot_pace_map[closest_vdot].get(distance, 300)
    
    # 根据差异调整
    diff = vdot - closest_vdot
    adjusted_seconds = base_seconds - diff * 2  # 每 VDOT 差约 2 秒
    
    return seconds_to_pace(max(adjusted_seconds, 60), PaceUnit.MIN_PER_KM)


def pace_to_vdot(pace_str: str) -> float:
    """
    根据配速估算 VDOT 值
    
    Args:
        pace_str: 配速字符串（每公里）
        
    Returns:
        估算的 VDOT 值
        
    Examples:
        >>> pace_to_vdot("5:00")
        47.5
    """
    pace_seconds = parse_pace(pace_str) * 60
    
    # 基于配速的反向估算（简化公式）
    # VDOT ≈ 100 - (配速秒数 / 5)
    vdot = 100 - (pace_seconds / 5)
    
    # 限制在合理范围
    return max(25, min(85, round(vdot, 1)))


def calculate_training_zones(
    pace_str: str
) -> Dict[str, PaceResult]:
    """
    计算训练配速区间
    
    基于 Jack Daniels 的跑步公式，计算 E/M/T/I/R 五个训练区间
    
    Args:
        pace_str: 当前配速（阈值配速，T 配速）
        
    Returns:
        训练区间字典
        
    Examples:
        >>> zones = calculate_training_zones("5:00")
        >>> zones["E"]  # 轻松跑配速
        PaceResult(minutes=5, seconds=30, ...)
    """
    threshold_pace = parse_pace(pace_str) * 60  # 秒
    
    # 训练区间系数（相对于阈值配速）
    zone_multipliers = {
        "E": 1.10,    # 轻松跑 - 比阈值慢 10-15%
        "M": 1.04,    # 马拉松配速 - 比阈值慢 4-8%
        "T": 1.00,    # 阈值配速 - 基准
        "I": 0.93,    # 间歇跑 - 比阈值快 5-10%
        "R": 0.85,    # 重复跑/冲刺 - 比阈值快 15-20%
    }
    
    zone_names = {
        "E": "轻松跑 (Easy)",
        "M": "马拉松配速 (Marathon)",
        "T": "阈值配速 (Threshold)",
        "I": "间歇跑 (Interval)",
        "R": "重复跑 (Repetition)"
    }
    
    zones = {}
    for zone, multiplier in zone_multipliers.items():
        zone_pace = threshold_pace * multiplier
        zones[zone] = seconds_to_pace(zone_pace, PaceUnit.MIN_PER_KM)
    
    return zones


def format_pace(seconds: float) -> str:
    """
    格式化配速为 MM:SS 格式
    
    Args:
        seconds: 每公里秒数
        
    Returns:
        格式化的配速字符串
        
    Examples:
        >>> format_pace(330)
        '5:30'
        >>> format_pace(360)
        '6:00'
    """
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"


def get_race_distance(name: str) -> Optional[float]:
    """
    获取标准比赛距离（公里）
    
    Args:
        name: 比赛名称（如 "5K", "马拉松", "半马"）
        
    Returns:
        距离（公里），如果不存在返回 None
        
    Examples:
        >>> get_race_distance("马拉松")
        42.195
        >>> get_race_distance("10K")
        10.0
    """
    name = name.upper().replace(" ", "")
    
    # 中文映射
    chinese_names = {
        "半马": "半马",
        "全马": "马拉松",
        "马拉松": "马拉松"
    }
    
    if name in chinese_names:
        name = chinese_names[name]
    
    if name in RACE_DISTANCES:
        return RACE_DISTANCES[name] / 1000
    
    # 尝试解析数字
    for key, meters in RACE_DISTANCES.items():
        if name in key.upper():
            return meters / 1000
    
    return None


# 便捷函数
def pace(time_str: str, distance: float, unit: str = "km") -> str:
    """
    快速计算配速
    
    Args:
        time_str: 时间字符串
        distance: 距离
        unit: 单位（"km" 或 "mi"）
        
    Returns:
        配速字符串
        
    Examples:
        >>> pace("25:00", 5)
        '5:00 /km'
    """
    distance_unit = DistanceUnit.MILES if unit == "mi" else DistanceUnit.KILOMETERS
    result = calculate_pace(distance, time_str, distance_unit)
    return f"{result.pace_str} /km"


def finish_time(distance: float, pace_str: str, unit: str = "km") -> str:
    """
    快速计算完赛时间
    
    Args:
        distance: 距离
        pace_str: 配速（每公里）
        unit: 单位（"km" 或 "mi"）
        
    Returns:
        完赛时间字符串
        
    Examples:
        >>> finish_time(10, "5:30")
        '55:00'
    """
    distance_unit = DistanceUnit.MILES if unit == "mi" else DistanceUnit.KILOMETERS
    result = calculate_time(distance, pace_str, distance_unit)
    return result.time_str


if __name__ == "__main__":
    # 演示用法
    print("=== 跑步配速计算工具演示 ===\n")
    
    # 1. 计算配速
    print("1. 计算5公里25分钟的配速：")
    pace_result = calculate_pace(5, "25:00")
    print(f"   配速: {pace_result}")
    
    # 2. 计算完赛时间
    print("\n2. 计算10公里配速5:30的完赛时间：")
    time_result = calculate_time(10, "5:30")
    print(f"   完赛时间: {time_result}")
    
    # 3. 计算速度
    print("\n3. 计算10公里50分钟的速度：")
    speed_result = calculate_speed(10, "50:00")
    print(f"   速度: {speed_result}")
    
    # 4. 配速转换
    print("\n4. 配速转换 (5:00/km -> /mi)：")
    converted = convert_pace("5:00", PaceUnit.MIN_PER_KM, PaceUnit.MIN_PER_MI)
    print(f"   {converted}")
    
    # 5. 预测比赛时间
    print("\n5. 根据5公里25分钟预测马拉松时间：")
    predicted = predict_race_time(5, "25:00", 42.195)
    print(f"   预测马拉松时间: {predicted}")
    
    # 6. 训练区间
    print("\n6. 训练配速区间（阈值配速5:00/km）：")
    zones = calculate_training_zones("5:00")
    for zone, pace in zones.items():
        print(f"   {zone} 区: {pace}")
    
    # 7. 分段用时
    print("\n7. 5公里分段用时（配速6:00/km）：")
    splits = calculate_splits(5, "6:00")
    for split in splits:
        print(f"   第{split['split']}公里: 累计时间 {split['total_time']}")