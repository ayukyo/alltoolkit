"""
AQI (Air Quality Index) Utils - 空气质量指数计算工具

功能：
- 计算多种污染物的AQI (PM2.5, PM10, O3, CO, SO2, NO2)
- 支持中国标准和美国EPA标准
- 提供健康建议和活动推荐
- AQI等级分类和颜色代码
- 支持综合AQI计算（取最大值）
- 浓度与AQI双向转换
"""

from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import math


class AQILevel(Enum):
    """AQI等级枚举"""
    EXCELLENT = "优"          # 0-50
    GOOD = "良"               # 51-100
    LIGHT_POLLUTION = "轻度污染"  # 101-150
    MODERATE_POLLUTION = "中度污染"  # 151-200
    HEAVY_POLLUTION = "重度污染"  # 201-300
    SEVERE_POLLUTION = "严重污染"  # >300


class PollutantType(Enum):
    """污染物类型"""
    PM25 = "PM2.5"
    PM10 = "PM10"
    O3_1H = "O3_1h"      # 臭氧1小时平均
    O3_8H = "O3_8h"      # 臭氧8小时平均
    CO = "CO"            # 一氧化碳
    SO2 = "SO2"          # 二氧化硫
    NO2 = "NO2"          # 二氧化氮


@dataclass
class AQIResult:
    """AQI计算结果"""
    aqi: int                      # AQI值
    level: AQILevel                # 等级
    pollutant: PollutantType       # 主要污染物
    concentration: float           # 浓度值
    unit: str                     # 浓度单位
    color: str                    # 颜色代码 (hex)
    health_advice: str            # 健康建议
    activity_suggestion: str      # 活动建议


@dataclass
class ComprehensiveAQI:
    """综合AQI结果"""
    aqi: int                      # 综合AQI值（取最大）
    level: AQILevel               # 等级
    primary_pollutant: PollutantType  # 首要污染物
    all_results: Dict[str, AQIResult]  # 所有污染物结果
    color: str                    # 颜色代码
    health_advice: str            # 健康建议


# 中国标准 AQI 分级
AQI_BREAKPOINTS_CN = {
    # AQI范围: (0, 50, 100, 150, 200, 300, 400, 500)
    # 对应等级: 优, 良, 轻度污染, 中度污染, 重度污染, 严重污染
    PollutantType.PM25: [
        (0, 35, 0, 50),
        (35, 75, 50, 100),
        (75, 115, 100, 150),
        (115, 150, 150, 200),
        (150, 250, 200, 300),
        (250, 350, 300, 400),
        (350, 500, 400, 500),
    ],  # μg/m³
    PollutantType.PM10: [
        (0, 50, 0, 50),
        (50, 150, 50, 100),
        (150, 250, 100, 150),
        (250, 350, 150, 200),
        (350, 420, 200, 300),
        (420, 500, 300, 400),
        (500, 600, 400, 500),
    ],  # μg/m³
    PollutantType.O3_1H: [
        (0, 160, 0, 50),
        (160, 200, 50, 100),
        (200, 300, 100, 150),
        (300, 400, 150, 200),
        (400, 800, 200, 300),
        (800, 1000, 300, 400),
        (1000, 1200, 400, 500),
    ],  # μg/m³
    PollutantType.O3_8H: [
        (0, 100, 0, 50),
        (100, 160, 50, 100),
        (160, 215, 100, 150),
        (215, 265, 150, 200),
        (265, 800, 200, 300),
    ],  # μg/m³
    PollutantType.CO: [
        (0, 2, 0, 50),
        (2, 4, 50, 100),
        (4, 14, 100, 150),
        (14, 24, 150, 200),
        (24, 36, 200, 300),
        (36, 48, 300, 400),
        (48, 60, 400, 500),
    ],  # mg/m³
    PollutantType.SO2: [
        (0, 50, 0, 50),
        (50, 150, 50, 100),
        (150, 475, 100, 150),
        (475, 800, 150, 200),
        (800, 1600, 200, 300),
        (1600, 2100, 300, 400),
        (2100, 2620, 400, 500),
    ],  # μg/m³
    PollutantType.NO2: [
        (0, 40, 0, 50),
        (40, 80, 50, 100),
        (80, 180, 100, 150),
        (180, 280, 150, 200),
        (280, 565, 200, 300),
        (565, 750, 300, 400),
        (750, 940, 400, 500),
    ],  # μg/m³
}

# 美国 EPA 标准 AQI 分级
AQI_BREAKPOINTS_US = {
    PollutantType.PM25: [
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 350.4, 301, 400),
        (350.5, 500.4, 401, 500),
    ],  # μg/m³
    PollutantType.PM10: [
        (0, 54, 0, 50),
        (55, 154, 51, 100),
        (155, 254, 101, 150),
        (255, 354, 151, 200),
        (355, 424, 201, 300),
        (425, 504, 301, 400),
        (505, 604, 401, 500),
    ],  # μg/m³
    PollutantType.O3_1H: [
        (0, 54, 0, 50),
        (55, 124, 51, 100),
        (125, 164, 101, 150),
        (165, 204, 151, 200),
        (205, 404, 201, 300),
        (405, 504, 301, 400),
        (505, 604, 401, 500),
    ],  # ppb (parts per billion)
    PollutantType.O3_8H: [
        (0.0, 54, 0, 50),
        (55, 70, 51, 100),
        (71, 85, 101, 150),
        (86, 105, 151, 200),
        (106, 200, 201, 300),
    ],  # ppb
    PollutantType.CO: [
        (0.0, 4.4, 0, 50),
        (4.5, 9.4, 51, 100),
        (9.5, 12.4, 101, 150),
        (12.5, 15.4, 151, 200),
        (15.5, 30.4, 201, 300),
        (30.5, 40.4, 301, 400),
        (40.5, 50.4, 401, 500),
    ],  # ppm
    PollutantType.SO2: [
        (0, 35, 0, 50),
        (36, 75, 51, 100),
        (76, 185, 101, 150),
        (186, 304, 151, 200),
        (305, 604, 201, 300),
        (605, 804, 301, 400),
        (805, 1004, 401, 500),
    ],  # ppb
    PollutantType.NO2: [
        (0, 53, 0, 50),
        (54, 100, 51, 100),
        (101, 360, 101, 150),
        (361, 649, 151, 200),
        (650, 1249, 201, 300),
        (1250, 1649, 301, 400),
        (1650, 2049, 401, 500),
    ],  # ppb
}

# AQI 等级颜色 (hex)
AQI_COLORS = {
    AQILevel.EXCELLENT: "#00e400",        # 绿色
    AQILevel.GOOD: "#ffff00",              # 黄色
    AQILevel.LIGHT_POLLUTION: "#ff7e00",   # 橙色
    AQILevel.MODERATE_POLLUTION: "#ff0000", # 红色
    AQILevel.HEAVY_POLLUTION: "#99004c",   # 紫色
    AQILevel.SEVERE_POLLUTION: "#7e0023",  # 褐红色
}

# 健康建议
HEALTH_ADVICE = {
    AQILevel.EXCELLENT: "空气质量令人满意，基本无空气污染",
    AQILevel.GOOD: "空气质量可接受，但某些污染物可能对极少数异常敏感人群健康有较弱影响",
    AQILevel.LIGHT_POLLUTION: "易感人群症状有轻度加剧，健康人群出现刺激症状",
    AQILevel.MODERATE_POLLUTION: "进一步加剧易感人群症状，可能对健康人群心脏、呼吸系统有影响",
    AQILevel.HEAVY_POLLUTION: "心脏病和肺病患者症状显著加剧，运动耐受力降低，健康人群普遍出现症状",
    AQILevel.SEVERE_POLLUTION: "健康人群运动耐受力降低，有明显强烈症状，提前出现某些疾病",
}

# 活动建议
ACTIVITY_SUGGESTIONS = {
    AQILevel.EXCELLENT: "各类人群可正常活动，适合户外运动",
    AQILevel.GOOD: "极少数异常敏感人群应减少户外活动",
    AQILevel.LIGHT_POLLUTION: "儿童、老年人及心脏病、呼吸系统疾病患者应减少长时间、高强度的户外锻炼",
    AQILevel.MODERATE_POLLUTION: "儿童、老年人及心脏病、呼吸系统疾病患者避免长时间、高强度的户外锻炼，一般人群适量减少户外运动",
    AQILevel.HEAVY_POLLUTION: "儿童、老年人和心脏病、肺病患者应停留在室内，停止户外运动，一般人群减少户外运动",
    AQILevel.SEVERE_POLLUTION: "儿童、老年人和病人应当留在室内，避免体力消耗，一般人群应避免户外活动",
}

# 浓度单位
CONCENTRATION_UNITS = {
    PollutantType.PM25: "μg/m³",
    PollutantType.PM10: "μg/m³",
    PollutantType.O3_1H: "μg/m³",
    PollutantType.O3_8H: "μg/m³",
    PollutantType.CO: "mg/m³",
    PollutantType.SO2: "μg/m³",
    PollutantType.NO2: "μg/m³",
}


def get_aqi_level(aqi: int) -> AQILevel:
    """
    根据AQI值获取等级
    
    Args:
        aqi: AQI值
        
    Returns:
        AQILevel枚举值
    """
    if aqi <= 50:
        return AQILevel.EXCELLENT
    elif aqi <= 100:
        return AQILevel.GOOD
    elif aqi <= 150:
        return AQILevel.LIGHT_POLLUTION
    elif aqi <= 200:
        return AQILevel.MODERATE_POLLUTION
    elif aqi <= 300:
        return AQILevel.HEAVY_POLLUTION
    else:
        return AQILevel.SEVERE_POLLUTION


def calculate_aqi(
    concentration: float,
    pollutant: PollutantType,
    standard: str = "cn"
) -> AQIResult:
    """
    计算单个污染物的AQI值
    
    Args:
        concentration: 污染物浓度
        pollutant: 污染物类型
        standard: 标准类型，"cn"为中国标准，"us"为美国EPA标准
        
    Returns:
        AQIResult对象
    """
    # 选择断点表
    breakpoints = AQI_BREAKPOINTS_CN if standard == "cn" else AQI_BREAKPOINTS_US
    
    # 获取该污染物的断点
    if pollutant not in breakpoints:
        raise ValueError(f"不支持的污染物类型: {pollutant}")
    
    bp_list = breakpoints[pollutant]
    
    # 查找浓度所在的区间
    aqi_low, aqi_high = 0, 500
    conc_low, conc_high = 0, 0
    
    for bp in bp_list:
        c_low, c_high, i_low, i_high = bp
        if c_low <= concentration <= c_high:
            conc_low, conc_high = c_low, c_high
            aqi_low, aqi_high = i_low, i_high
            break
    else:
        # 超出范围，使用最后一个区间
        if concentration < bp_list[0][0]:
            # 低于最小值
            conc_low, conc_high = bp_list[0][0], bp_list[0][1]
            aqi_low, aqi_high = bp_list[0][2], bp_list[0][3]
        else:
            # 高于最大值
            conc_low, conc_high = bp_list[-1][0], bp_list[-1][1]
            aqi_low, aqi_high = bp_list[-1][2], bp_list[-1][3]
    
    # 使用线性插值计算AQI
    if conc_high == conc_low:
        aqi = aqi_low
    else:
        aqi = ((aqi_high - aqi_low) / (conc_high - conc_low)) * (concentration - conc_low) + aqi_low
    
    aqi = round(aqi)
    aqi = max(0, min(500, aqi))  # 限制在0-500范围内
    
    level = get_aqi_level(aqi)
    
    return AQIResult(
        aqi=aqi,
        level=level,
        pollutant=pollutant,
        concentration=concentration,
        unit=CONCENTRATION_UNITS.get(pollutant, "μg/m³"),
        color=AQI_COLORS[level],
        health_advice=HEALTH_ADVICE[level],
        activity_suggestion=ACTIVITY_SUGGESTIONS[level]
    )


def calculate_comprehensive_aqi(
    concentrations: Dict[str, float],
    standard: str = "cn"
) -> ComprehensiveAQI:
    """
    计算综合AQI（取各污染物AQI最大值）
    
    Args:
        concentrations: 污染物浓度字典，键为污染物名称（如"pm25", "pm10", "o3"）
        standard: 标准类型
        
    Returns:
        ComprehensiveAQI对象
    """
    # 污染物名称映射
    name_mapping = {
        "pm25": PollutantType.PM25,
        "pm2.5": PollutantType.PM25,
        "pm10": PollutantType.PM10,
        "o3": PollutantType.O3_1H,
        "o3_1h": PollutantType.O3_1H,
        "o3_8h": PollutantType.O3_8H,
        "co": PollutantType.CO,
        "so2": PollutantType.SO2,
        "no2": PollutantType.NO2,
    }
    
    results = {}
    max_aqi = 0
    primary_pollutant = None
    
    for name, conc in concentrations.items():
        name_lower = name.lower().replace(".", "")
        if name_lower not in name_mapping:
            continue
        
        pollutant = name_mapping[name_lower]
        result = calculate_aqi(conc, pollutant, standard)
        results[name] = result
        
        if result.aqi > max_aqi:
            max_aqi = result.aqi
            primary_pollutant = pollutant
    
    if not results:
        raise ValueError("未提供有效的污染物浓度数据")
    
    level = get_aqi_level(max_aqi)
    
    return ComprehensiveAQI(
        aqi=max_aqi,
        level=level,
        primary_pollutant=primary_pollutant,
        all_results=results,
        color=AQI_COLORS[level],
        health_advice=HEALTH_ADVICE[level]
    )


def aqi_to_concentration(
    aqi: int,
    pollutant: PollutantType,
    standard: str = "cn"
) -> float:
    """
    将AQI值转换为污染物浓度（返回区间中点）
    
    Args:
        aqi: AQI值 (0-500)
        pollutant: 污染物类型
        standard: 标准类型
        
    Returns:
        近似浓度值
    """
    breakpoints = AQI_BREAKPOINTS_CN if standard == "cn" else AQI_BREAKPOINTS_US
    
    if pollutant not in breakpoints:
        raise ValueError(f"不支持的污染物类型: {pollutant}")
    
    bp_list = breakpoints[pollutant]
    
    for c_low, c_high, i_low, i_high in bp_list:
        if i_low <= aqi <= i_high:
            # 反向线性插值
            if i_high == i_low:
                return c_low
            concentration = ((c_high - c_low) / (i_high - i_low)) * (aqi - i_low) + c_low
            return round(concentration, 2)
    
    # 超出范围
    if aqi < 0:
        return 0
    else:  # aqi > 500
        return bp_list[-1][1]


def get_health_recommendations(aqi: int) -> Dict[str, str]:
    """
    获取健康建议
    
    Args:
        aqi: AQI值
        
    Returns:
        包含各类建议的字典
    """
    level = get_aqi_level(aqi)
    
    recommendations = {
        "general": HEALTH_ADVICE[level],
        "activity": ACTIVITY_SUGGESTIONS[level],
        "sensitive_groups": _get_sensitive_groups_advice(level),
        "outdoor": _get_outdoor_advice(level),
        "mask": _get_mask_advice(level),
        "ventilation": _get_ventilation_advice(level),
    }
    
    return recommendations


def _get_sensitive_groups_advice(level: AQILevel) -> str:
    """获取敏感人群建议"""
    advice_map = {
        AQILevel.EXCELLENT: "敏感人群可正常户外活动",
        AQILevel.GOOD: "极少数对臭氧等异常敏感的人群应减少户外活动",
        AQILevel.LIGHT_POLLUTION: "儿童、老年人、心脏病及呼吸系统疾病患者应减少户外运动",
        AQILevel.MODERATE_POLLUTION: "敏感人群应避免户外运动，减少体力消耗",
        AQILevel.HEAVY_POLLUTION: "敏感人群应留在室内，必要时佩戴口罩",
        AQILevel.SEVERE_POLLUTION: "敏感人群应留在室内，关闭门窗，使用空气净化器",
    }
    return advice_map[level]


def _get_outdoor_advice(level: AQILevel) -> str:
    """获取户外活动建议"""
    advice_map = {
        AQILevel.EXCELLENT: "适合所有户外活动",
        AQILevel.GOOD: "适合户外活动，敏感人群注意身体反应",
        AQILevel.LIGHT_POLLUTION: "可进行户外活动，避免长时间剧烈运动",
        AQILevel.MODERATE_POLLUTION: "减少户外活动时间，避免剧烈运动",
        AQILevel.HEAVY_POLLUTION: "尽量减少户外活动，必要时佩戴防护口罩",
        AQILevel.SEVERE_POLLUTION: "避免户外活动，留在室内",
    }
    return advice_map[level]


def _get_mask_advice(level: AQILevel) -> str:
    """获取口罩佩戴建议"""
    advice_map = {
        AQILevel.EXCELLENT: "无需佩戴口罩",
        AQILevel.GOOD: "无需佩戴口罩",
        AQILevel.LIGHT_POLLUTION: "敏感人群外出可佩戴口罩",
        AQILevel.MODERATE_POLLUTION: "建议佩戴N95或KN95口罩",
        AQILevel.HEAVY_POLLUTION: "必须佩戴N95或KN95口罩",
        AQILevel.SEVERE_POLLUTION: "必须佩戴防护级别口罩，尽量不外出",
    }
    return advice_map[level]


def _get_ventilation_advice(level: AQILevel) -> str:
    """获取通风建议"""
    advice_map = {
        AQILevel.EXCELLENT: "可开窗通风，保持室内空气新鲜",
        AQILevel.GOOD: "可开窗通风，保持室内空气新鲜",
        AQILevel.LIGHT_POLLUTION: "可短时间开窗通风，避免长时间开窗",
        AQILevel.MODERATE_POLLUTION: "减少开窗时间，可使用空气净化器",
        AQILevel.HEAVY_POLLUTION: "关闭门窗，使用空气净化器",
        AQILevel.SEVERE_POLLUTION: "关闭门窗，使用空气净化器，避免通风",
    }
    return advice_map[level]


def compare_standards(concentration: float, pollutant: PollutantType) -> Dict[str, AQIResult]:
    """
    比较不同标准下的AQI计算结果
    
    Args:
        concentration: 污染物浓度
        pollutant: 污染物类型
        
    Returns:
        包含不同标准结果的字典
    """
    return {
        "cn": calculate_aqi(concentration, pollutant, "cn"),
        "us": calculate_aqi(concentration, pollutant, "us"),
    }


def get_pollutant_info(pollutant: PollutantType) -> Dict[str, str]:
    """
    获取污染物信息
    
    Args:
        pollutant: 污染物类型
        
    Returns:
        污染物信息字典
    """
    info = {
        PollutantType.PM25: {
            "name": "细颗粒物(PM2.5)",
            "description": "直径小于等于2.5微米的颗粒物，可深入肺泡，对健康影响最大",
            "source": "燃煤、机动车尾气、工业排放、扬尘等",
            "health_effect": "呼吸系统疾病、心血管疾病、肺癌等",
        },
        PollutantType.PM10: {
            "name": "可吸入颗粒物(PM10)",
            "description": "直径小于等于10微米的颗粒物，可进入呼吸道",
            "source": "扬尘、工业排放、花粉、真菌孢子等",
            "health_effect": "呼吸道刺激、哮喘、支气管炎等",
        },
        PollutantType.O3_1H: {
            "name": "臭氧(1小时平均)",
            "description": "光化学烟雾的主要成分，夏季午后浓度最高",
            "source": "氮氧化物和挥发性有机物在阳光作用下生成",
            "health_effect": "呼吸道刺激、肺功能下降、哮喘发作",
        },
        PollutantType.O3_8H: {
            "name": "臭氧(8小时平均)",
            "description": "臭氧8小时滑动平均浓度，更能反映日间暴露水平",
            "source": "氮氧化物和挥发性有机物在阳光作用下生成",
            "health_effect": "长期暴露可导致肺功能下降",
        },
        PollutantType.CO: {
            "name": "一氧化碳(CO)",
            "description": "无色无味气体，与血红蛋白结合影响氧气输送",
            "source": "机动车尾气、工业排放、不完全燃烧",
            "health_effect": "头痛、头晕、恶心、心脏病加重",
        },
        PollutantType.SO2: {
            "name": "二氧化硫(SO2)",
            "description": "刺激性气体，易溶于水形成酸雨",
            "source": "燃煤发电、工业排放、火山喷发",
            "health_effect": "呼吸道刺激、哮喘发作、肺功能下降",
        },
        PollutantType.NO2: {
            "name": "二氧化氮(NO2)",
            "description": "红棕色气体，有刺激性气味",
            "source": "机动车尾气、发电厂、工业锅炉",
            "health_effect": "呼吸道刺激、肺功能下降、易感染呼吸道疾病",
        },
    }
    
    return info.get(pollutant, {})


def calculate_aqi_range(
    concentration_low: float,
    concentration_high: float,
    pollutant: PollutantType,
    steps: int = 10,
    standard: str = "cn"
) -> List[Dict[str, float]]:
    """
    计算浓度范围内的AQI变化
    
    Args:
        concentration_low: 起始浓度
        concentration_high: 结束浓度
        pollutant: 污染物类型
        steps: 计算步数
        standard: 标准类型
        
    Returns:
        浓度和AQI的列表
    """
    if steps < 2:
        steps = 2
    
    step_size = (concentration_high - concentration_low) / (steps - 1)
    results = []
    
    for i in range(steps):
        conc = concentration_low + i * step_size
        result = calculate_aqi(conc, pollutant, standard)
        results.append({
            "concentration": round(conc, 2),
            "aqi": result.aqi,
            "level": result.level.value,
        })
    
    return results


def estimate_pm25_from_visibility(visibility_km: float) -> float:
    """
    根据能见度估算PM2.5浓度（粗略估算）
    
    Args:
        visibility_km: 能见度（公里）
        
    Returns:
        估算的PM2.5浓度 (μg/m³)
    """
    if visibility_km <= 0:
        return 500
    
    # 简化估算公式（仅供参考）
    # 高湿度条件下此公式不准确
    pm25 = 700 / visibility_km - 10
    return max(0, min(500, pm25))


def get_aqi_summary(aqi: int) -> str:
    """
    获取AQI摘要信息
    
    Args:
        aqi: AQI值
        
    Returns:
        摘要字符串
    """
    level = get_aqi_level(aqi)
    return f"AQI {aqi} - {level.value}"


# 便捷函数
def pm25_to_aqi(concentration: float, standard: str = "cn") -> int:
    """PM2.5浓度转AQI (便捷函数)"""
    return calculate_aqi(concentration, PollutantType.PM25, standard).aqi


def pm10_to_aqi(concentration: float, standard: str = "cn") -> int:
    """PM10浓度转AQI (便捷函数)"""
    return calculate_aqi(concentration, PollutantType.PM10, standard).aqi


def o3_to_aqi(concentration: float, standard: str = "cn") -> int:
    """臭氧浓度转AQI (便捷函数，使用1小时标准)"""
    return calculate_aqi(concentration, PollutantType.O3_1H, standard).aqi


def co_to_aqi(concentration: float, standard: str = "cn") -> int:
    """CO浓度转AQI (便捷函数)"""
    return calculate_aqi(concentration, PollutantType.CO, standard).aqi


def so2_to_aqi(concentration: float, standard: str = "cn") -> int:
    """SO2浓度转AQI (便捷函数)"""
    return calculate_aqi(concentration, PollutantType.SO2, standard).aqi


def no2_to_aqi(concentration: float, standard: str = "cn") -> int:
    """NO2浓度转AQI (便捷函数)"""
    return calculate_aqi(concentration, PollutantType.NO2, standard).aqi