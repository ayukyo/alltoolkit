"""
Running Pace Utilities - 跑步配速计算工具

功能：
- 配速计算（时间/距离 → 配速）
- 时间预测（距离/配速 → 时间）
- 距离计算（时间/配速 → 距离）
- 配速转换（min/km ↔ min/mile ↔ km/h ↔ mph）
- 比赛配速表生成
- VDOT/年龄分级跑力计算
- 目标时间拆分（每公里/英里）
- 心率区间配速估算
- 跑步效益指数计算

零外部依赖，仅使用 Python 标准库
"""

import math
from dataclasses import dataclass
from typing import Optional, List, Tuple, Dict
from enum import Enum


class DistanceUnit(Enum):
    """距离单位"""
    KILOMETERS = "km"
    MILES = "mi"
    METERS = "m"
    YARDS = "yd"


class PaceUnit(Enum):
    """配速单位"""
    MIN_PER_KM = "min/km"      # 分钟每公里
    MIN_PER_MILE = "min/mi"    # 分钟每英里
    KM_PER_HOUR = "km/h"       # 公里每小时
    MILE_PER_HOUR = "mph"      # 英里每小时


# 标准比赛距离（米）
RACE_DISTANCES = {
    "100m": 100,
    "200m": 200,
    "400m": 400,
    "800m": 800,
    "1500m": 1500,
    "mile": 1609.344,
    "3km": 3000,
    "5km": 5000,
    "10km": 10000,
    "half_marathon": 21097.5,
    "marathon": 42195,
    "50km": 50000,
    "100km": 100000,
}

# 单位转换因子
UNIT_CONVERSIONS = {
    DistanceUnit.KILOMETERS: 1.0,
    DistanceUnit.METERS: 0.001,
    DistanceUnit.MILES: 1.609344,
    DistanceUnit.YARDS: 0.0009144,
}

# VDOT 表（Jack Daniels Running Formula 简化版）
# VDOT -> 预计 5km 时间（秒）
VDOT_5KM_TIMES = {
    30: 2100,  # 35:00
    35: 1920,  # 32:00
    40: 1770,  # 29:30
    45: 1620,  # 27:00
    50: 1500,  # 25:00
    55: 1380,  # 23:00
    60: 1260,  # 21:00
    65: 1140,  # 19:00
    70: 1020,  # 17:00
}

# 年龄分级系数（简化版，基于 WMA 标准）
AGE_GRADE_FACTORS = {
    # 年龄: 系数
    20: 1.000, 25: 0.990, 30: 0.970, 35: 0.945,
    40: 0.908, 45: 0.865, 50: 0.818, 55: 0.768,
    60: 0.715, 65: 0.660, 70: 0.605, 75: 0.550,
}

# 心率区间百分比（基于最大心率）
HEART_RATE_ZONES = {
    1: (0.50, 0.60),  # 恢复区
    2: (0.60, 0.70),  # 有氧基础区
    3: (0.70, 0.80),  # 有氧耐力区
    4: (0.80, 0.90),  # 乳酸阈值区
    5: (0.90, 1.00),  # 无氧耐力区
}


@dataclass
class PaceResult:
    """配速计算结果"""
    pace_min_per_km: float       # min/km
    pace_min_per_mile: float     # min/mi
    speed_kmh: float             # km/h
    speed_mph: float             # mph
    time_seconds: float          # 总时间（秒）
    distance_km: float           # 距离（公里）


@dataclass
class SplitTime:
    """分段计时"""
    distance: float              # 距离（公里）
    cumulative_time: float       # 累计时间（秒）
    split_time: float            # 该段用时（秒）
    pace_min_per_km: float       # 该段配速（min/km）


@dataclass
class RacePrediction:
    """比赛预测结果"""
    distance: str
    distance_km: float
    predicted_time: float        # 秒
    predicted_time_formatted: str
    pace_min_per_km: float
    pace_formatted: str


@dataclass
class TrainingZone:
    """训练区间"""
    zone: int
    name: str
    hr_min: int
    hr_max: int
    pace_min_per_km: Tuple[float, float]
    description: str


def _format_time(seconds: float) -> str:
    """将秒数格式化为 HH:MM:SS 或 MM:SS"""
    if seconds < 0:
        return "N/A"
    
    total_seconds = int(seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def _format_pace(pace_min_per_km: float) -> str:
    """将配速格式化为 MM:SS/km"""
    if pace_min_per_km <= 0 or math.isinf(pace_min_per_km):
        return "N/A"
    
    minutes = int(pace_min_per_km)
    seconds = int((pace_min_per_km - minutes) * 60)
    return f"{minutes}:{seconds:02d}/km"


def convert_distance(distance: float, from_unit: DistanceUnit, to_unit: DistanceUnit) -> float:
    """
    距离单位转换
    
    Args:
        distance: 距离值
        from_unit: 原单位
        to_unit: 目标单位
    
    Returns:
        转换后的距离值
    """
    # 先转换为公里
    km = distance * UNIT_CONVERSIONS[from_unit]
    # 再转换为目标单位
    return km / UNIT_CONVERSIONS[to_unit]


def convert_pace(pace: float, from_unit: PaceUnit, to_unit: PaceUnit) -> float:
    """
    配速单位转换
    
    Args:
        pace: 配速值
        from_unit: 原单位
        to_unit: 目标单位
    
    Returns:
        转换后的配速值
    """
    # 先转换为 min/km
    if from_unit == PaceUnit.MIN_PER_KM:
        min_per_km = pace
    elif from_unit == PaceUnit.MIN_PER_MILE:
        min_per_km = pace / 1.609344
    elif from_unit == PaceUnit.KM_PER_HOUR:
        min_per_km = 60 / pace if pace > 0 else float('inf')
    else:  # MILE_PER_HOUR
        min_per_km = 60 / (pace * 1.609344) if pace > 0 else float('inf')
    
    # 再转换为目标单位
    if to_unit == PaceUnit.MIN_PER_KM:
        return min_per_km
    elif to_unit == PaceUnit.MIN_PER_MILE:
        return min_per_km * 1.609344
    elif to_unit == PaceUnit.KM_PER_HOUR:
        return 60 / min_per_km if min_per_km > 0 else 0
    else:  # MILE_PER_HOUR
        return 60 / (min_per_km * 1.609344) if min_per_km > 0 else 0


def calculate_pace(distance: float, time_seconds: float, 
                   distance_unit: DistanceUnit = DistanceUnit.KILOMETERS) -> PaceResult:
    """
    根据距离和时间计算配速
    
    Args:
        distance: 距离
        time_seconds: 时间（秒）
        distance_unit: 距离单位
    
    Returns:
        PaceResult: 配速结果对象
    
    Raises:
        ValueError: 距离或时间无效
    """
    if distance <= 0:
        raise ValueError("距离必须大于 0")
    if time_seconds <= 0:
        raise ValueError("时间必须大于 0")
    
    # 转换为公里
    distance_km = convert_distance(distance, distance_unit, DistanceUnit.KILOMETERS)
    distance_miles = convert_distance(distance, distance_unit, DistanceUnit.MILES)
    
    # 计算配速
    pace_min_per_km = (time_seconds / 60) / distance_km
    pace_min_per_mile = (time_seconds / 60) / distance_miles
    
    # 计算速度
    speed_kmh = distance_km / (time_seconds / 3600)
    speed_mph = distance_miles / (time_seconds / 3600)
    
    return PaceResult(
        pace_min_per_km=pace_min_per_km,
        pace_min_per_mile=pace_min_per_mile,
        speed_kmh=speed_kmh,
        speed_mph=speed_mph,
        time_seconds=time_seconds,
        distance_km=distance_km
    )


def calculate_time(distance: float, pace: float, 
                   distance_unit: DistanceUnit = DistanceUnit.KILOMETERS,
                   pace_unit: PaceUnit = PaceUnit.MIN_PER_KM) -> float:
    """
    根据距离和配速计算时间
    
    Args:
        distance: 距离
        pace: 配速
        distance_unit: 距离单位
        pace_unit: 配速单位
    
    Returns:
        时间（秒）
    
    Raises:
        ValueError: 距离或配速无效
    """
    if distance <= 0:
        raise ValueError("距离必须大于 0")
    if pace <= 0:
        raise ValueError("配速必须大于 0")
    
    # 统一转换为 min/km
    pace_min_per_km = convert_pace(pace, pace_unit, PaceUnit.MIN_PER_KM)
    
    # 转换距离为公里
    distance_km = convert_distance(distance, distance_unit, DistanceUnit.KILOMETERS)
    
    # 计算时间
    return distance_km * pace_min_per_km * 60


def calculate_distance(time_seconds: float, pace: float,
                       pace_unit: PaceUnit = PaceUnit.MIN_PER_KM,
                       distance_unit: DistanceUnit = DistanceUnit.KILOMETERS) -> float:
    """
    根据时间和配速计算距离
    
    Args:
        time_seconds: 时间（秒）
        pace: 配速
        pace_unit: 配速单位
        distance_unit: 返回的距离单位
    
    Returns:
        距离
    
    Raises:
        ValueError: 时间或配速无效
    """
    if time_seconds <= 0:
        raise ValueError("时间必须大于 0")
    if pace <= 0:
        raise ValueError("配速必须大于 0")
    
    # 统一转换为 min/km
    pace_min_per_km = convert_pace(pace, pace_unit, PaceUnit.MIN_PER_KM)
    
    # 计算距离（公里）
    distance_km = (time_seconds / 60) / pace_min_per_km
    
    # 转换为目标单位
    return convert_distance(distance_km, DistanceUnit.KILOMETERS, distance_unit)


def generate_splits(distance_km: float, time_seconds: float, 
                    split_distance_km: float = 1.0) -> List[SplitTime]:
    """
    生成分段计时表
    
    Args:
        distance_km: 总距离（公里）
        time_seconds: 总时间（秒）
        split_distance_km: 分段距离（公里）
    
    Returns:
        List[SplitTime]: 分段计时列表
    """
    if distance_km <= 0 or time_seconds <= 0 or split_distance_km <= 0:
        return []
    
    # 计算平均配速
    avg_pace_min_per_km = (time_seconds / 60) / distance_km
    
    splits = []
    cumulative_time = 0.0
    current_distance = 0.0
    
    while current_distance < distance_km:
        next_distance = min(current_distance + split_distance_km, distance_km)
        segment_distance = next_distance - current_distance
        
        # 该段用时
        segment_time = segment_distance * avg_pace_min_per_km * 60
        cumulative_time += segment_time
        
        splits.append(SplitTime(
            distance=next_distance,
            cumulative_time=cumulative_time,
            split_time=segment_time,
            pace_min_per_km=avg_pace_min_per_km
        ))
        
        current_distance = next_distance
    
    return splits


def predict_race_time(distance_km: float, reference_time_seconds: float,
                      reference_distance_km: float) -> RacePrediction:
    """
    基于参考成绩预测比赛时间（使用 Riegel 公式）
    
    公式: T2 = T1 * (D2/D1)^1.06
    
    Args:
        distance_km: 目标距离（公里）
        reference_time_seconds: 参考时间（秒）
        reference_distance_km: 参考距离（公里）
    
    Returns:
        RacePrediction: 比赛预测结果
    """
    if distance_km <= 0 or reference_time_seconds <= 0 or reference_distance_km <= 0:
        raise ValueError("距离和时间必须大于 0")
    
    # Riegel 公式
    predicted_time = reference_time_seconds * math.pow(distance_km / reference_distance_km, 1.06)
    pace_min_per_km = (predicted_time / 60) / distance_km
    
    # 找到最接近的比赛名称
    distance_name = f"{distance_km}km"
    for name, dist in RACE_DISTANCES.items():
        if abs(dist / 1000 - distance_km) < 0.5:
            distance_name = name
            break
    
    return RacePrediction(
        distance=distance_name,
        distance_km=distance_km,
        predicted_time=predicted_time,
        predicted_time_formatted=_format_time(predicted_time),
        pace_min_per_km=pace_min_per_km,
        pace_formatted=_format_pace(pace_min_per_km)
    )


def calculate_vdot(distance_km: float, time_seconds: float) -> float:
    """
    计算 VDOT 跑力值（Jack Daniels 方法简化版）
    
    Args:
        distance_km: 距离（公里）
        time_seconds: 时间（秒）
    
    Returns:
        VDOT 值
    """
    if distance_km <= 0 or time_seconds <= 0:
        return 0.0
    
    # 基于 5km 时间计算 VDOT
    pace_min_per_km = (time_seconds / 60) / distance_km
    time_5km = 5 * pace_min_per_km * 60
    
    # 查表插值
    vdots = sorted(VDOT_5KM_TIMES.keys(), reverse=True)
    for i, vdot in enumerate(vdots):
        if time_5km <= VDOT_5KM_TIMES[vdot]:
            if i == 0:
                return float(vdot)
            # 线性插值
            next_vdot = vdots[i - 1] if i > 0 else vdot
            t1, t2 = VDOT_5KM_TIMES[vdot], VDOT_5KM_TIMES[next_vdot]
            ratio = (t1 - time_5km) / (t1 - t2) if t1 != t2 else 0
            return vdot + ratio * (next_vdot - vdot)
    
    return float(vdots[-1])


def calculate_age_grade(time_seconds: float, distance_km: float, 
                        age: int, gender: str = "M") -> Tuple[float, float]:
    """
    计算年龄分级成绩
    
    Args:
        time_seconds: 时间（秒）
        distance_km: 距离（公里）
        age: 年龄
        gender: 性别 ("M" 或 "F")
    
    Returns:
        Tuple[float, float]: (年龄分级系数, 年龄分级百分比)
    """
    if age < 20:
        age_factor = 1.0
    else:
        # 找到最接近的年龄系数
        ages = sorted(AGE_GRADE_FACTORS.keys())
        if age >= ages[-1]:
            age_factor = AGE_GRADE_FACTORS[ages[-1]]
        else:
            for i, a in enumerate(ages):
                if age <= a:
                    if i == 0:
                        age_factor = AGE_GRADE_FACTORS[a]
                    else:
                        # 线性插值
                        prev_age = ages[i - 1]
                        ratio = (age - prev_age) / (a - prev_age)
                        age_factor = AGE_GRADE_FACTORS[prev_age] + ratio * (
                            AGE_GRADE_FACTORS[a] - AGE_GRADE_FACTORS[prev_age]
                        )
                    break
    
    # 年龄分级百分比 = (世界最佳时间 / 实际时间) / 年龄系数 * 100
    # 简化计算：使用一个参考值
    world_best_time = distance_km * 180  # 假设世界最佳配速 3:00/km
    age_grade_percent = (world_best_time / time_seconds) / age_factor * 100
    
    return age_factor, min(age_grade_percent, 100.0)


def calculate_training_zones(max_hr: int, threshold_pace_min_per_km: float) -> List[TrainingZone]:
    """
    根据最大心率和阈值配速计算训练区间
    
    Args:
        max_hr: 最大心率
        threshold_pace_min_per_km: 阈值配速（min/km）
    
    Returns:
        List[TrainingZone]: 训练区间列表
    """
    zones = []
    zone_info = [
        (1, "恢复区", "轻松恢复跑，促进血液循环"),
        (2, "有氧基础区", "建立有氧耐力基础"),
        (3, "有氧耐力区", "提高有氧能力"),
        (4, "乳酸阈值区", "提高乳酸阈值"),
        (5, "无氧耐力区", "提高最大摄氧量"),
    ]
    
    # 阈值配速调整系数（系数越大，配速越慢）
    pace_adjustments = {
        1: 1.20,  # Zone 1 比阈值慢约 20%
        2: 1.10,  # Zone 2 比阈值慢约 10%
        3: 1.05,  # Zone 3 接近阈值，慢约 5%
        4: 1.00,  # Zone 4 阈值配速
        5: 0.95,  # Zone 5 比阈值快约 5%
    }
    
    for zone, name, desc in zone_info:
        hr_range = HEART_RATE_ZONES[zone]
        hr_min = int(max_hr * hr_range[0])
        hr_max = int(max_hr * hr_range[1])
        
        # 配速范围
        adj = pace_adjustments[zone]
        # 每个区间有上下限
        if zone < 5:
            adj_next = pace_adjustments[zone + 1]
            pace_slow = threshold_pace_min_per_km * adj
            pace_fast = threshold_pace_min_per_km * adj_next
        else:
            # Zone 5 最快
            pace_slow = threshold_pace_min_per_km * adj
            pace_fast = threshold_pace_min_per_km * 0.90  # Zone 5 最快端
        
        zones.append(TrainingZone(
            zone=zone,
            name=name,
            hr_min=hr_min,
            hr_max=hr_max,
            pace_min_per_km=(pace_fast, pace_slow),  # 从快到慢
            description=desc
        ))
    
    return zones


def calculate_running_economy(distance_km: float, time_seconds: float,
                              weight_kg: float, vo2max: Optional[float] = None) -> Dict[str, float]:
    """
    计算跑步经济性指标
    
    Args:
        distance_km: 距离（公里）
        time_seconds: 时间（秒）
        weight_kg: 体重（公斤）
        vo2max: 最大摄氧量（可选）
    
    Returns:
        Dict: 跑步经济性指标
    """
    if distance_km <= 0 or time_seconds <= 0 or weight_kg <= 0:
        return {}
    
    speed_m_per_min = (distance_km * 1000) / (time_seconds / 60)
    speed_km_per_hr = distance_km / (time_seconds / 3600)
    
    # 估算能量消耗（基于 ACSM 公式）
    # VO2 (ml/kg/min) = 0.2 * speed(m/min) + 0.9 * speed(m/min) * grade + 3.5
    # 假设平地跑步，grade = 0
    vo2 = 0.2 * speed_m_per_min + 3.5
    
    # 能量消耗（kcal/min）
    kcal_per_min = vo2 * weight_kg / 200
    
    # 总能量消耗
    total_kcal = kcal_per_min * (time_seconds / 60)
    
    # 每公里消耗
    kcal_per_km = total_kcal / distance_km
    
    result = {
        "speed_kmh": round(speed_km_per_hr, 2),
        "vo2_ml_kg_min": round(vo2, 1),
        "kcal_per_min": round(kcal_per_min, 1),
        "total_kcal": round(total_kcal, 0),
        "kcal_per_km": round(kcal_per_km, 1),
    }
    
    # 如果提供了 VO2max，计算相对强度
    if vo2max and vo2max > 0:
        intensity_percent = (vo2 / vo2max) * 100
        result["intensity_percent_vo2max"] = round(intensity_percent, 1)
    
    return result


def generate_race_pace_table(distance_km: float, 
                             finish_time_minutes: float) -> Dict[str, any]:
    """
    生成比赛配速表
    
    Args:
        distance_km: 距离（公里）
        finish_time_minutes: 目标完赛时间（分钟）
    
    Returns:
        Dict: 配速表信息
    """
    if distance_km <= 0 or finish_time_minutes <= 0:
        return {}
    
    time_seconds = finish_time_minutes * 60
    pace_result = calculate_pace(distance_km, time_seconds, DistanceUnit.KILOMETERS)
    
    # 生成每公里分段
    km_splits = generate_splits(distance_km, time_seconds, 1.0)
    
    # 生成每英里分段
    mile_splits = generate_splits(distance_km, time_seconds, 1.609344)
    
    return {
        "distance_km": distance_km,
        "target_time": _format_time(time_seconds),
        "target_time_minutes": finish_time_minutes,
        "pace_min_per_km": pace_result.pace_min_per_km,
        "pace_formatted": _format_pace(pace_result.pace_min_per_km),
        "speed_kmh": round(pace_result.speed_kmh, 2),
        "km_splits": [{
            "km": round(s.distance, 2),
            "time": _format_time(s.cumulative_time),
            "split": _format_time(s.split_time),
        } for s in km_splits],
        "mile_splits": [{
            "mile": round(s.distance, 2),
            "time": _format_time(s.cumulative_time),
            "split": _format_time(s.split_time),
        } for s in mile_splits],
    }


def calculate_interval_pace(goal_pace_min_per_km: float, 
                             interval_type: str) -> Dict[str, float]:
    """
    计算间歇训练配速
    
    Args:
        goal_pace_min_per_km: 目标配速（min/km）
        interval_type: 间歇类型 ("repetition", "interval", "threshold", "easy")
    
    Returns:
        Dict: 不同训练类型的配速建议
    """
    if goal_pace_min_per_km <= 0:
        return {}
    
    # 不同训练类型的配速调整系数
    # 系数越大，配速越慢（min/km 数字越大）
    # 系数越小，配速越快（min/km 数字越小）
    adjustments = {
        "repetition": 0.90,    # 重复跑，比目标快约 10%（系数小 → 配速快）
        "interval": 0.95,      # 间歇跑，比目标快约 5%
        "threshold": 1.00,     # 阈值跑，等于目标配速
        "tempo": 1.03,         # 节奏跑，比目标慢约 3%
        "marathon": 1.05,      # 马拉松配速，比目标慢约 5%
        "easy": 1.15,          # 轻松跑，比目标慢约 15%
        "recovery": 1.25,      # 恢复跑，比目标慢约 25%
    }
    
    result = {}
    for train_type, adj in adjustments.items():
        pace = goal_pace_min_per_km * adj
        result[train_type] = {
            "pace_min_per_km": round(pace, 2),
            "pace_formatted": _format_pace(pace),
        }
    
    return result


def estimate_finish_time_from_splits(splits: List[Tuple[float, float]], 
                                     total_distance_km: float) -> Dict[str, any]:
    """
    基于分段数据预测完赛时间
    
    Args:
        splits: 分段数据列表 [(距离km, 时间秒), ...]
        total_distance_km: 总距离（公里）
    
    Returns:
        Dict: 预测结果
    """
    if not splits or total_distance_km <= 0:
        return {}
    
    # 计算已完成距离和时间
    completed_distance = sum(s[0] for s in splits)
    elapsed_time = sum(s[1] for s in splits)
    
    if completed_distance <= 0 or elapsed_time <= 0:
        return {}
    
    # 计算当前配速
    current_pace = (elapsed_time / 60) / completed_distance
    
    # 剩余距离
    remaining_distance = total_distance_km - completed_distance
    
    if remaining_distance <= 0:
        return {
            "status": "finished",
            "total_time": _format_time(elapsed_time),
            "average_pace": _format_pace(current_pace),
        }
    
    # 预测剩余时间（考虑疲劳因素）
    # 简单模型：后半程配速下降 3-5%
    fatigue_factor = 1.03 if remaining_distance > 10 else 1.02
    predicted_remaining_time = remaining_distance * current_pace * fatigue_factor * 60
    
    total_predicted_time = elapsed_time + predicted_remaining_time
    average_pace = (total_predicted_time / 60) / total_distance_km
    
    return {
        "status": "in_progress",
        "completed_distance_km": round(completed_distance, 2),
        "remaining_distance_km": round(remaining_distance, 2),
        "elapsed_time": _format_time(elapsed_time),
        "predicted_remaining_time": _format_time(predicted_remaining_time),
        "predicted_total_time": _format_time(total_predicted_time),
        "current_pace": _format_pace(current_pace),
        "predicted_average_pace": _format_pace(average_pace),
        "progress_percent": round((completed_distance / total_distance_km) * 100, 1),
    }


def calculate_grade_adjusted_pace(pace_min_per_km: float, 
                                   grade_percent: float) -> float:
    """
    计算坡度调整配速（GAP - Grade Adjusted Pace）
    
    Args:
        pace_min_per_km: 实际配速（min/km）
        grade_percent: 坡度百分比（正值为上坡，负值为下坡）
    
    Returns:
        调整后的平地等效配速（min/km）
    """
    if pace_min_per_km <= 0:
        return 0.0
    
    # 坡度调整系数（简化版）
    # 上坡：配速变慢（等效更快）
    # 下坡：配速变快（等效更慢）
    if grade_percent > 0:
        # 上坡：每 1% 坡度约增加 4% 努力程度
        adjustment = 1 + (grade_percent * 0.04)
    else:
        # 下坡：每 -1% 坡度约减少 2% 努力程度（但有限制）
        adjustment = 1 + (grade_percent * 0.02)
        adjustment = max(adjustment, 0.7)  # 下坡最多降低 30%
    
    # 调整配速：努力程度越高，等效配速越快
    adjusted_pace = pace_min_per_km / adjustment
    
    return round(adjusted_pace, 2)


# 便捷函数
def pace_to_speed(pace_min_per_km: float) -> float:
    """配速（min/km）转速度（km/h）"""
    if pace_min_per_km <= 0:
        return 0.0
    return 60 / pace_min_per_km


def speed_to_pace(speed_kmh: float) -> float:
    """速度（km/h）转配速（min/km）"""
    if speed_kmh <= 0:
        return float('inf')
    return 60 / speed_kmh


def format_pace(pace_min_per_km: float) -> str:
    """格式化配速为 MM:SS/km"""
    return _format_pace(pace_min_per_km)


def format_time(seconds: float) -> str:
    """格式化时间为 HH:MM:SS 或 MM:SS"""
    return _format_time(seconds)