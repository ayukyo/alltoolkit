"""
Ventilation Utils - 室内通风计算工具

功能：
- 房间通风需求计算
- 换气次数计算（ACH - Air Changes per Hour）
- CO2浓度预测与评估
- 通风时间计算
- 空气质量评估
- 自然通风与机械通风计算
- 新风量计算
- 污染物浓度衰减计算
"""

from dataclasses import dataclass
from typing import Optional, List, Tuple, Dict
import math
from enum import Enum


class AirQualityLevel(Enum):
    """空气质量等级"""
    EXCELLENT = "excellent"      # CO2 < 600 ppm
    GOOD = "good"                # CO2 600-800 ppm
    MODERATE = "moderate"        # CO2 800-1000 ppm
    POOR = "poor"                # CO2 1000-1500 ppm
    VERY_POOR = "very_poor"      # CO2 > 1500 ppm


class VentilationType(Enum):
    """通风类型"""
    NATURAL = "natural"          # 自然通风
    MECHANICAL = "mechanical"    # 机械通风
    HYBRID = "hybrid"           # 混合通风


@dataclass
class RoomInfo:
    """房间信息"""
    length: float       # 长度 (米)
    width: float        # 宽度 (米)
    height: float       # 高度 (米)
    occupants: int = 0  # 入住人数
    
    @property
    def volume(self) -> float:
        """房间体积 (立方米)"""
        return self.length * self.width * self.height
    
    @property
    def floor_area(self) -> float:
        """地板面积 (平方米)"""
        return self.length * self.width


@dataclass
class VentilationResult:
    """通风计算结果"""
    required_ach: float           # 所需换气次数 (次/小时)
    required_airflow: float       # 所需风量 (立方米/小时)
    recommended_airflow: float    # 推荐风量 (立方米/小时)
    ventilation_type: VentilationType
    quality_level: AirQualityLevel
    co2_steady_state: float       # 稳态CO2浓度 (ppm)
    notes: List[str]


@dataclass
class CO2Prediction:
    """CO2浓度预测结果"""
    initial_ppm: float
    target_ppm: float
    time_minutes: float
    final_ppm: float
    ach_used: float
    reached_target: bool


# 常量定义
CO2_OUTDOOR = 420  # 室外CO2浓度 (ppm)
CO2_PER_PERSON_HOURLY = 0.03  # 每人每小时CO2产生量 (立方米) - 约30升/小时，典型成年人轻体力活动
CO2_EXCELLENT_LIMIT = 600
CO2_GOOD_LIMIT = 800
CO2_MODERATE_LIMIT = 1000
CO2_POOR_LIMIT = 1500

# 标准换气次数参考 (ACH)
STANDARD_ACH = {
    "bedroom": 0.5,
    "living_room": 0.5,
    "office": 1.0,
    "classroom": 2.0,
    "hospital": 6.0,
    "kitchen": 3.0,
    "bathroom": 5.0,
    "gym": 4.0,
    "restaurant": 6.0,
}

# 每人所需新风量 (立方米/小时/人)
FRESH_AIR_PER_PERSON = {
    "minimal": 25,      # 最低标准
    "standard": 30,     # 标准要求
    "comfort": 40,      # 舒适标准
    "premium": 50,      # 高端标准
}


def calculate_ach(volume: float, airflow: float) -> float:
    """
    计算换气次数 (Air Changes per Hour)
    
    Args:
        volume: 房间体积 (立方米)
        airflow: 通风量 (立方米/小时)
    
    Returns:
        换气次数 (次/小时)
    """
    if volume <= 0:
        raise ValueError("房间体积必须大于0")
    return airflow / volume


def calculate_airflow_for_ach(volume: float, ach: float) -> float:
    """
    根据换气次数计算所需风量
    
    Args:
        volume: 房间体积 (立方米)
        ach: 换气次数 (次/小时)
    
    Returns:
        所需风量 (立方米/小时)
    """
    return volume * ach


def calculate_co2_steady_state(
    room: RoomInfo,
    airflow: float,
    co2_generation: float = None,
    outdoor_co2: float = CO2_OUTDOOR
) -> float:
    """
    计算室内稳态CO2浓度
    
    Args:
        room: 房间信息
        airflow: 通风量 (立方米/小时)
        co2_generation: CO2产生率 (立方米/小时)，默认按人数计算
        outdoor_co2: 室外CO2浓度 (ppm)
    
    Returns:
        稳态CO2浓度 (ppm)
    """
    if airflow <= 0:
        return float('inf')
    
    # 计算CO2产生率
    if co2_generation is None:
        # 每人每小时产生约0.03立方米CO2
        co2_generation = room.occupants * CO2_PER_PERSON_HOURLY
    
    # 稳态浓度公式: C = C_out + G / Q * 10^6
    # C_out: 室外浓度(ppm), G: 产生率(m³/h), Q: 通风量(m³/h)
    steady_state_ppm = outdoor_co2 + (co2_generation / airflow) * 1_000_000
    
    return steady_state_ppm


def calculate_required_ventilation(
    room: RoomInfo,
    target_co2: float = CO2_GOOD_LIMIT,
    co2_generation: float = None,
    outdoor_co2: float = CO2_OUTDOOR
) -> float:
    """
    计算达到目标CO2浓度所需通风量
    
    Args:
        room: 房间信息
        target_co2: 目标CO2浓度 (ppm)
        co2_generation: CO2产生率 (立方米/小时)
        outdoor_co2: 室外CO2浓度 (ppm)
    
    Returns:
        所需通风量 (立方米/小时)
    """
    if co2_generation is None:
        co2_generation = room.occupants * CO2_PER_PERSON_HOURLY
    
    if target_co2 <= outdoor_co2:
        return float('inf')
    
    # Q = G / (C_target - C_out)
    delta_co2 = (target_co2 - outdoor_co2) / 1_000_000  # 转换为体积分数
    required_airflow = co2_generation / delta_co2
    
    return required_airflow


def predict_co2_decay(
    volume: float,
    initial_co2: float,
    airflow: float,
    time_minutes: float,
    outdoor_co2: float = CO2_OUTDOOR,
    co2_generation: float = 0
) -> CO2Prediction:
    """
    预测CO2浓度随时间的衰减
    
    Args:
        volume: 房间体积 (立方米)
        initial_co2: 初始CO2浓度 (ppm)
        airflow: 通风量 (立方米/小时)
        time_minutes: 预测时间 (分钟)
        outdoor_co2: 室外CO2浓度 (ppm)
        co2_generation: CO2产生率 (立方米/小时)
    
    Returns:
        CO2预测结果
    """
    ach = calculate_ach(volume, airflow)
    time_hours = time_minutes / 60
    
    # 指数衰减公式: C(t) = C_out + (C_0 - C_out) * e^(-n*t) + G*t/Q
    decay_factor = math.exp(-ach * time_hours)
    
    final_co2 = outdoor_co2 + (initial_co2 - outdoor_co2) * decay_factor
    if co2_generation > 0 and airflow > 0:
        final_co2 += (co2_generation / airflow) * (1 - decay_factor) * 1_000_000
    
    return CO2Prediction(
        initial_ppm=initial_co2,
        target_ppm=outdoor_co2,
        time_minutes=time_minutes,
        final_ppm=final_co2,
        ach_used=ach,
        reached_target=(final_co2 <= outdoor_co2 * 1.1)
    )


def calculate_ventilation_time(
    volume: float,
    initial_co2: float,
    target_co2: float,
    airflow: float,
    outdoor_co2: float = CO2_OUTDOOR
) -> float:
    """
    计算达到目标CO2浓度所需通风时间
    
    Args:
        volume: 房间体积 (立方米)
        initial_co2: 初始CO2浓度 (ppm)
        target_co2: 目标CO2浓度 (ppm)
        airflow: 通风量 (立方米/小时)
        outdoor_co2: 室外CO2浓度 (ppm)
    
    Returns:
        所需时间 (分钟)
    """
    if airflow <= 0:
        return float('inf')
    
    if target_co2 >= initial_co2:
        return 0
    
    if target_co2 < outdoor_co2:
        target_co2 = outdoor_co2
    
    ach = calculate_ach(volume, airflow)
    
    # t = -ln((C_target - C_out) / (C_0 - C_out)) / n
    ratio = (target_co2 - outdoor_co2) / (initial_co2 - outdoor_co2)
    
    if ratio <= 0 or ratio >= 1:
        return float('inf')
    
    time_hours = -math.log(ratio) / ach
    time_minutes = time_hours * 60
    
    return time_minutes


def get_air_quality_level(co2_ppm: float) -> AirQualityLevel:
    """
    根据CO2浓度判断空气质量等级
    
    Args:
        co2_ppm: CO2浓度 (ppm)
    
    Returns:
        空气质量等级
    """
    if co2_ppm < CO2_EXCELLENT_LIMIT:
        return AirQualityLevel.EXCELLENT
    elif co2_ppm < CO2_GOOD_LIMIT:
        return AirQualityLevel.GOOD
    elif co2_ppm < CO2_MODERATE_LIMIT:
        return AirQualityLevel.MODERATE
    elif co2_ppm < CO2_POOR_LIMIT:
        return AirQualityLevel.POOR
    else:
        return AirQualityLevel.VERY_POOR


def analyze_room_ventilation(
    room: RoomInfo,
    current_airflow: float = 0,
    room_type: str = "office",
    standard: str = "standard"
) -> VentilationResult:
    """
    分析房间通风情况
    
    Args:
        room: 房间信息
        current_airflow: 当前风量 (立方米/小时)，0表示需要计算
        room_type: 房间类型
        standard: 新风标准 ("minimal", "standard", "comfort", "premium")
    
    Returns:
        通风分析结果
    """
    notes = []
    
    # 获取标准换气次数
    standard_ach = STANDARD_ACH.get(room_type.lower(), 1.0)
    
    # 按人数计算所需新风量
    fresh_air_per_person = FRESH_AIR_PER_PERSON.get(standard, 30)
    airflow_by_occupants = room.occupants * fresh_air_per_person
    
    # 按换气次数计算所需新风量
    airflow_by_ach = calculate_airflow_for_ach(room.volume, standard_ach)
    
    # 取较大值作为所需风量
    required_airflow = max(airflow_by_occupants, airflow_by_ach)
    required_ach = calculate_ach(room.volume, required_airflow)
    
    # 推荐风量（增加20%余量）
    recommended_airflow = required_airflow * 1.2
    
    # 计算稳态CO2浓度
    co2_steady_state = calculate_co2_steady_state(room, recommended_airflow)
    
    # 判断通风类型
    if room.occupants == 0:
        vent_type = VentilationType.NATURAL
        notes.append("无人房间，自然通风即可")
    elif recommended_airflow > 500:
        vent_type = VentilationType.MECHANICAL
        notes.append("建议使用机械通风系统")
    else:
        vent_type = VentilationType.HYBRID
        notes.append("可采用自然通风与机械通风结合")
    
    # 判断空气质量
    quality_level = get_air_quality_level(co2_steady_state)
    
    # 添加建议
    if co2_steady_state > CO2_MODERATE_LIMIT:
        notes.append("警告：CO2浓度偏高，建议增加通风")
    elif co2_steady_state < CO2_GOOD_LIMIT:
        notes.append("通风良好，空气质量优秀")
    
    if room.occupants > 0:
        notes.append(f"每人新风量: {recommended_airflow / room.occupants:.1f} 立方米/小时")
    
    return VentilationResult(
        required_ach=required_ach,
        required_airflow=required_airflow,
        recommended_airflow=recommended_airflow,
        ventilation_type=vent_type,
        quality_level=quality_level,
        co2_steady_state=co2_steady_state,
        notes=notes
    )


def calculate_pollutant_decay(
    volume: float,
    initial_concentration: float,
    airflow: float,
    decay_rate: float = 0,
    time_hours: float = 1.0,
    outdoor_concentration: float = 0
) -> Dict[str, float]:
    """
    计算污染物浓度衰减
    
    Args:
        volume: 房间体积 (立方米)
        initial_concentration: 初始浓度
        airflow: 通风量 (立方米/小时)
        decay_rate: 自然衰减率 (1/小时)
        time_hours: 时间 (小时)
        outdoor_concentration: 室外浓度
    
    Returns:
        包含浓度信息的字典
    """
    ach = calculate_ach(volume, airflow)
    total_removal_rate = ach + decay_rate
    
    if total_removal_rate == 0:
        final_concentration = initial_concentration
    else:
        decay_factor = math.exp(-total_removal_rate * time_hours)
        final_concentration = outdoor_concentration + \
            (initial_concentration - outdoor_concentration) * decay_factor
    
    half_life = math.log(2) / total_removal_rate if total_removal_rate > 0 else float('inf')
    time_to_90_percent = math.log(10) / total_removal_rate if total_removal_rate > 0 else float('inf')
    
    return {
        "initial_concentration": initial_concentration,
        "final_concentration": final_concentration,
        "removal_rate": total_removal_rate,
        "half_life_hours": half_life,
        "time_to_90_percent_hours": time_to_90_percent,
        "concentration_removed": initial_concentration - final_concentration,
        "removal_percentage": (initial_concentration - final_concentration) / initial_concentration * 100 if initial_concentration > 0 else 0
    }


def calculate_natural_ventilation(
    opening_area: float,
    wind_speed: float,
    temperature_diff: float = 0,
    height: float = 2.0
) -> Dict[str, float]:
    """
    计算自然通风量
    
    Args:
        opening_area: 开口面积 (平方米)
        wind_speed: 风速 (米/秒)
        temperature_diff: 室内外温差 (摄氏度)
        height: 开口高度差 (米)
    
    Returns:
        包含通风量信息的字典
    """
    # 风压通风量
    # Q_wind = 0.6 * A * v
    wind_airflow = 0.6 * opening_area * wind_speed * 3600  # 转换为立方米/小时
    
    # 热压通风量（烟囱效应）
    # Q_stack = 0.43 * A * sqrt(h * ΔT)
    if temperature_diff > 0:
        stack_airflow = 0.43 * opening_area * math.sqrt(height * temperature_diff) * 3600
    else:
        stack_airflow = 0
    
    # 总通风量（取较大值或叠加）
    total_airflow = max(wind_airflow, stack_airflow)
    
    return {
        "wind_airflow": wind_airflow,
        "stack_airflow": stack_airflow,
        "total_airflow": total_airflow,
        "primary_driver": "wind" if wind_airflow > stack_airflow else "stack"
    }


def calculate_fresh_air_duct_size(
    airflow: float,
    air_velocity: float = 4.0
) -> Dict[str, float]:
    """
    计算新风管道尺寸
    
    Args:
        airflow: 风量 (立方米/小时)
        air_velocity: 风速 (米/秒)，一般4-6米/秒
    
    Returns:
        包含管道尺寸信息的字典
    """
    # Q = A * v => A = Q / v
    airflow_m3s = airflow / 3600  # 转换为立方米/秒
    area_m2 = airflow_m3s / air_velocity
    
    # 圆管直径
    diameter = math.sqrt(4 * area_m2 / math.pi) * 1000  # 转换为毫米
    
    # 方管边长（等面积）
    square_side = math.sqrt(area_m2) * 1000  # 转换为毫米
    
    # 推荐标准尺寸
    standard_diameters = [100, 125, 150, 160, 200, 250, 315, 355, 400]
    recommended_diameter = min([d for d in standard_diameters if d >= diameter] or [diameter])
    
    return {
        "area_m2": area_m2,
        "diameter_mm": diameter,
        "square_side_mm": square_side,
        "recommended_diameter_mm": recommended_diameter,
        "velocity_m_s": air_velocity
    }


def estimate_occupancy_from_co2(
    room: RoomInfo,
    current_co2: float,
    airflow: float,
    outdoor_co2: float = CO2_OUTDOOR
) -> int:
    """
    根据CO2浓度估算室内人数
    
    Args:
        room: 房间信息
        current_co2: 当前CO2浓度 (ppm)
        airflow: 通风量 (立方米/小时)
        outdoor_co2: 室外CO2浓度 (ppm)
    
    Returns:
        估算人数
    """
    if airflow <= 0 or current_co2 <= outdoor_co2:
        return 0
    
    # 稳态公式逆推: n = (C - C_out) * Q / (G_per_person)
    co2_contribution = (current_co2 - outdoor_co2) / 1_000_000  # 转换为体积分数
    co2_generation_rate = airflow * co2_contribution  # 立方米/小时
    
    estimated_occupancy = co2_generation_rate / CO2_PER_PERSON_HOURLY
    
    return max(0, round(estimated_occupancy))


def calculate_hvac_requirements(
    room: RoomInfo,
    outdoor_temp: float,
    indoor_temp_target: float,
    ventilation_rate: float,
    specific_heat: float = 1.005,  # 空气比热 (kJ/kg·K)
    air_density: float = 1.2  # 空气密度 (kg/m³)
) -> Dict[str, float]:
    """
    计算HVAC热负荷相关参数
    
    Args:
        room: 房间信息
        outdoor_temp: 室外温度 (°C)
        indoor_temp_target: 室内目标温度 (°C)
        ventilation_rate: 换气次数 (ACH)
        specific_heat: 空气比热 (kJ/kg·K)
        air_density: 空气密度 (kg/m³)
    
    Returns:
        包含HVAC参数的字典
    """
    # 通风热负荷 Q = ρ * V * n * c_p * ΔT / 3600 (kW)
    temp_diff = abs(indoor_temp_target - outdoor_temp)
    airflow = room.volume * ventilation_rate  # 立方米/小时
    
    # 通风热负荷 (kW)
    ventilation_heat_load = (air_density * airflow * specific_heat * temp_diff) / 3600
    
    # 制冷/制热需求
    is_cooling = outdoor_temp > indoor_temp_target
    
    return {
        "ventilation_heat_load_kw": ventilation_heat_load,
        "ventilation_heat_load_w": ventilation_heat_load * 1000,
        "airflow_m3h": airflow,
        "temp_difference": temp_diff,
        "mode": "cooling" if is_cooling else "heating",
        "btu_per_hour": ventilation_heat_load * 3412.14  # kW转BTU/h
    }


# 便捷函数
def quick_ventilation_check(
    room_length: float,
    room_width: float,
    room_height: float,
    occupants: int,
    room_type: str = "office"
) -> Dict:
    """
    快速通风检查
    
    Args:
        room_length: 房间长度 (米)
        room_width: 房间宽度 (米)
        room_height: 房间高度 (米)
        occupants: 人数
        room_type: 房间类型
    
    Returns:
        检查结果字典
    """
    room = RoomInfo(room_length, room_width, room_height, occupants)
    result = analyze_room_ventilation(room, room_type=room_type)
    
    return {
        "room_volume_m3": room.volume,
        "floor_area_m2": room.floor_area,
        "occupants": occupants,
        "required_ach": round(result.required_ach, 2),
        "required_airflow_m3h": round(result.required_airflow, 1),
        "recommended_airflow_m3h": round(result.recommended_airflow, 1),
        "co2_level_ppm": round(result.co2_steady_state, 0),
        "air_quality": result.quality_level.value,
        "ventilation_type": result.ventilation_type.value,
        "notes": result.notes
    }


if __name__ == "__main__":
    # 示例使用
    print("=== 室内通风计算工具示例 ===\n")
    
    # 创建房间信息
    room = RoomInfo(length=10, width=8, height=3, occupants=20)
    print(f"房间信息: {room.length}m x {room.width}m x {room.height}m")
    print(f"体积: {room.volume}m³, 面积: {room.floor_area}m², 人数: {room.occupants}\n")
    
    # 分析通风需求
    result = analyze_room_ventilation(room, room_type="office")
    print(f"所需换气次数: {result.required_ach} ACH")
    print(f"所需风量: {result.required_airflow:.1f} m³/h")
    print(f"推荐风量: {result.recommended_airflow:.1f} m³/h")
    print(f"通风类型: {result.ventilation_type.value}")
    print(f"稳态CO2浓度: {result.co2_steady_state:.0f} ppm")
    print(f"空气质量: {result.quality_level.value}")
    print(f"备注: {', '.join(result.notes)}\n")
    
    # CO2衰减预测
    print("=== CO2浓度衰减预测 ===")
    prediction = predict_co2_decay(
        volume=room.volume,
        initial_co2=1500,
        airflow=result.recommended_airflow,
        time_minutes=30
    )
    print(f"初始CO2: {prediction.initial_ppm} ppm")
    print(f"30分钟后: {prediction.final_ppm:.0f} ppm")
    print(f"换气次数: {prediction.ach_used:.2f} ACH\n")
    
    # 通风时间计算
    print("=== 通风时间计算 ===")
    time_to_good = calculate_ventilation_time(
        volume=room.volume,
        initial_co2=2000,
        target_co2=800,
        airflow=result.recommended_airflow
    )
    print(f"从2000ppm降至800ppm需要: {time_to_good:.1f} 分钟\n")
    
    # 自然通风计算
    print("=== 自然通风计算 ===")
    nat_vent = calculate_natural_ventilation(
        opening_area=2.0,
        wind_speed=2.0,
        temperature_diff=5
    )
    print(f"风压通风量: {nat_vent['wind_airflow']:.1f} m³/h")
    print(f"热压通风量: {nat_vent['stack_airflow']:.1f} m³/h")
    print(f"总通风量: {nat_vent['total_airflow']:.1f} m³/h")
    print(f"主要驱动: {nat_vent['primary_driver']}\n")
    
    # 管道尺寸计算
    print("=== 新风管道尺寸 ===")
    duct = calculate_fresh_air_duct_size(airflow=result.recommended_airflow)
    print(f"所需面积: {duct['area_m2']*1000000:.0f} mm²")
    print(f"圆管直径: {duct['diameter_mm']:.1f} mm")
    print(f"方管边长: {duct['square_side_mm']:.1f} mm")
    print(f"推荐标准直径: {duct['recommended_diameter_mm']} mm\n")
    
    # 快速检查
    print("=== 快速通风检查 ===")
    quick = quick_ventilation_check(10, 8, 3, 20, "office")
    for key, value in quick.items():
        if key != "notes":
            print(f"{key}: {value}")
    print(f"备注: {'; '.join(quick['notes'])}")