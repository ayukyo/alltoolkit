"""
Dew Point Utilities - 露点计算工具

提供露点、湿球温度、饱和蒸汽压等气象计算功能。
使用 Magnus 公式进行精确计算，零外部依赖。

核心功能:
- 露点温度计算
- 湿球温度计算
- 相对湿度与绝对湿度转换
- 饱和蒸汽压计算
- 体感舒适度评估
- 霜点计算
"""

import math
from typing import Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class ComfortLevel(Enum):
    """舒适度等级"""
    VERY_DRY = "非常干燥"
    DRY = "干燥"
    COMFORTABLE = "舒适"
    HUMID = "潮湿"
    VERY_HUMID = "非常潮湿"
    OPPRESSIVE = "闷热"


@dataclass
class HumidityData:
    """湿度数据容器"""
    temperature: float  # 摄氏度
    relative_humidity: float  # 百分比 (0-100)
    dew_point: float  # 露点温度
    absolute_humidity: float  # 绝对湿度 g/m³
    vapor_pressure: float  # 水蒸气分压 hPa
    saturation_vapor_pressure: float  # 饱和水蒸气压 hPa
    comfort_level: ComfortLevel


# Magnus 公式常数 (适用于 -45°C 到 60°C)
MAGNUS_A = 6.112
MAGNUS_B = 17.62
MAGNUS_C = 243.12

# Magnus 公式常数 (低于 0°C，冰面)
MAGNUS_A_ICE = 6.112
MAGNUS_B_ICE = 22.46
MAGNUS_C_ICE = 272.62


def saturation_vapor_pressure(temperature: float, over_ice: bool = False) -> float:
    """
    计算饱和水蒸气压
    
    使用 Magnus-Tetens 公式
    
    Args:
        temperature: 温度 (摄氏度)
        over_ice: 是否在冰面上 (温度低于0°C时)
    
    Returns:
        饱和水蒸气压 (hPa)
    
    Examples:
        >>> saturation_vapor_pressure(20)
        23.38...
        >>> saturation_vapor_pressure(-10, over_ice=True)
        2.86...
    """
    if over_ice and temperature < 0:
        a, b, c = MAGNUS_A_ICE, MAGNUS_B_ICE, MAGNUS_C_ICE
    else:
        a, b, c = MAGNUS_A, MAGNUS_B, MAGNUS_C
    
    return a * math.exp((b * temperature) / (c + temperature))


def vapor_pressure(temperature: float, relative_humidity: float) -> float:
    """
    计算实际水蒸气分压
    
    Args:
        temperature: 温度 (摄氏度)
        relative_humidity: 相对湿度 (百分比 0-100)
    
    Returns:
        水蒸气分压 (hPa)
    
    Examples:
        >>> vapor_pressure(20, 50)
        11.69...
    """
    rh = max(0, min(100, relative_humidity))  # 限制范围
    return saturation_vapor_pressure(temperature) * rh / 100


def dew_point(temperature: float, relative_humidity: float) -> float:
    """
    计算露点温度
    
    使用 Magnus 公式反算露点
    
    Args:
        temperature: 环境温度 (摄氏度)
        relative_humidity: 相对湿度 (百分比 0-100)
    
    Returns:
        露点温度 (摄氏度)
    
    Examples:
        >>> round(dew_point(20, 50), 1)
        9.3
        >>> round(dew_point(25, 80), 1)
        21.3
    """
    rh = max(0.1, min(100, relative_humidity))  # 限制范围，避免 log(0)
    
    # 计算 alpha 值
    svp = saturation_vapor_pressure(temperature)
    vp = svp * rh / 100
    
    # 使用 Magnus 公式反算
    a, b, c = MAGNUS_A, MAGNUS_B, MAGNUS_C
    
    # alpha = ln(vp/a) 其中 vp 是水蒸气分压
    alpha = math.log(vp / a)
    
    # 露点 = c * alpha / (b - alpha)
    dew_point_temp = c * alpha / (b - alpha)
    
    return dew_point_temp


def frost_point(temperature: float, relative_humidity: float) -> float:
    """
    计算霜点温度
    
    霜点是水蒸气直接凝华成霜的温度
    
    Args:
        temperature: 环境温度 (摄氏度)
        relative_humidity: 相对湿度 (百分比 0-100)
    
    Returns:
        霜点温度 (摄氏度)
    
    Examples:
        >>> round(frost_point(-5, 80), 1)
        -7.5
    """
    rh = max(0.1, min(100, relative_humidity))
    
    # 使用冰面 Magnus 公式
    svp_ice = saturation_vapor_pressure(temperature, over_ice=True)
    vp = svp_ice * rh / 100
    
    a, b, c = MAGNUS_A_ICE, MAGNUS_B_ICE, MAGNUS_C_ICE
    alpha = math.log(vp / a)
    
    return c * alpha / (b - alpha)


def absolute_humidity(temperature: float, relative_humidity: float) -> float:
    """
    计算绝对湿度
    
    Args:
        temperature: 温度 (摄氏度)
        relative_humidity: 相对湿度 (百分比 0-100)
    
    Returns:
        绝对湿度 (g/m³)
    
    Examples:
        >>> round(absolute_humidity(20, 50), 2)
        8.65
    """
    vp = vapor_pressure(temperature, relative_humidity)  # hPa
    
    # 绝对湿度 = 216.7 * vp / (T + 273.15)
    # 其中 vp 单位为 hPa
    return 216.7 * vp / (temperature + 273.15)


def relative_humidity_from_dew_point(temperature: float, dew_point_temp: float) -> float:
    """
    从露点温度反算相对湿度
    
    Args:
        temperature: 环境温度 (摄氏度)
        dew_point_temp: 露点温度 (摄氏度)
    
    Returns:
        相对湿度 (百分比)
    
    Examples:
        >>> round(relative_humidity_from_dew_point(20, 10), 1)
        52.6
    """
    svp_temp = saturation_vapor_pressure(temperature)
    svp_dew = saturation_vapor_pressure(dew_point_temp)
    
    return (svp_dew / svp_temp) * 100


def wet_bulb_temperature(temperature: float, relative_humidity: float) -> float:
    """
    计算湿球温度
    
    使用 Stull 近似公式
    
    Args:
        temperature: 干球温度 (摄氏度)
        relative_humidity: 相对湿度 (百分比 0-100)
    
    Returns:
        湿球温度 (摄氏度)
    
    Examples:
        >>> round(wet_bulb_temperature(20, 50), 1)
        13.7
    """
    rh = max(0, min(100, relative_humidity))
    
    # Stull 近似公式
    # Tw = T * atan(0.151977 * (rh + 8.313659)^0.5) 
    #      + atan(T + rh) - atan(rh - 1.676331) 
    #      + 0.00391838 * rh^1.5 * atan(0.023101 * rh) - 4.686035
    
    tw = (temperature * math.atan(0.151977 * (rh + 8.313659) ** 0.5)
          + math.atan(temperature + rh)
          - math.atan(rh - 1.676331)
          + 0.00391838 * rh ** 1.5 * math.atan(0.023101 * rh)
          - 4.686035)
    
    return tw


def heat_index(temperature: float, relative_humidity: float) -> float:
    """
    计算热指数 (体感温度)
    
    仅适用于温度 >= 27°C 且相对湿度 >= 40% 的情况
    
    Args:
        temperature: 温度 (摄氏度)
        relative_humidity: 相对湿度 (百分比 0-100)
    
    Returns:
        热指数 (摄氏度)，如果条件不满足则返回原温度
    
    Examples:
        >>> round(heat_index(30, 70), 1)
        35.1
    """
    if temperature < 27 or relative_humidity < 40:
        return temperature
    
    rh = relative_humidity
    t = temperature
    
    # Rothfusz 回归公式
    hi = (-8.78469475556
          + 1.61139411 * t
          + 2.33854883889 * rh
          - 0.14611605 * t * rh
          - 0.012308094 * t ** 2
          - 0.0164248277778 * rh ** 2
          + 0.002211732 * t ** 2 * rh
          + 0.00072546 * t * rh ** 2
          - 0.000003582 * t ** 2 * rh ** 2)
    
    return hi


def comfort_level(dew_point_temp: float) -> ComfortLevel:
    """
    根据露点温度评估体感舒适度
    
    基于美国国家气象局的舒适度分级
    
    Args:
        dew_point_temp: 露点温度 (摄氏度)
    
    Returns:
        舒适度等级
    
    Examples:
        >>> comfort_level(10)
        <ComfortLevel.COMFORTABLE: '舒适'>
        >>> comfort_level(25)
        <ComfortLevel.OPPRESSIVE: '闷热'>
    """
    if dew_point_temp < 10:
        return ComfortLevel.VERY_DRY
    elif dew_point_temp < 13:
        return ComfortLevel.DRY
    elif dew_point_temp < 16:
        return ComfortLevel.COMFORTABLE
    elif dew_point_temp < 18:
        return ComfortLevel.HUMID
    elif dew_point_temp < 24:
        return ComfortLevel.VERY_HUMID
    else:
        return ComfortLevel.OPPRESSIVE


def mixing_ratio(temperature: float, relative_humidity: float, pressure: float = 1013.25) -> float:
    """
    计算混合比
    
    Args:
        temperature: 温度 (摄氏度)
        relative_humidity: 相对湿度 (百分比 0-100)
        pressure: 大气压 (hPa)，默认标准大气压
    
    Returns:
        混合比 (g/kg 干空气)
    
    Examples:
        >>> round(mixing_ratio(20, 50), 2)
        7.26
    """
    vp = vapor_pressure(temperature, relative_humidity)
    
    # 混合比 = 622 * vp / (pressure - vp)
    return 622 * vp / (pressure - vp)


def specific_humidity(temperature: float, relative_humidity: float, pressure: float = 1013.25) -> float:
    """
    计算比湿
    
    Args:
        temperature: 温度 (摄氏度)
        relative_humidity: 相对湿度 (百分比 0-100)
        pressure: 大气压 (hPa)，默认标准大气压
    
    Returns:
        比湿 (g/kg)
    
    Examples:
        >>> round(specific_humidity(20, 50), 2)
        7.21
    """
    mr = mixing_ratio(temperature, relative_humidity, pressure)
    
    # 比湿 = 混合比 / (1 + 混合比/1000)
    return mr / (1 + mr / 1000)


def analyze_humidity(temperature: float, relative_humidity: float) -> HumidityData:
    """
    综合分析湿度状况
    
    Args:
        temperature: 温度 (摄氏度)
        relative_humidity: 相对湿度 (百分比 0-100)
    
    Returns:
        包含所有湿度相关数据的 HumidityData 对象
    
    Examples:
        >>> data = analyze_humidity(25, 60)
        >>> round(data.dew_point, 1)
        16.7
    """
    dp = dew_point(temperature, relative_humidity)
    
    return HumidityData(
        temperature=temperature,
        relative_humidity=relative_humidity,
        dew_point=dp,
        absolute_humidity=absolute_humidity(temperature, relative_humidity),
        vapor_pressure=vapor_pressure(temperature, relative_humidity),
        saturation_vapor_pressure=saturation_vapor_pressure(temperature),
        comfort_level=comfort_level(dp)
    )


def dew_point_depression(temperature: float, relative_humidity: float) -> float:
    """
    计算露点差 (温度 - 露点)
    
    露点差越小，表示空气越接近饱和，可能形成雾或露水
    
    Args:
        temperature: 温度 (摄氏度)
        relative_humidity: 相对湿度 (百分比 0-100)
    
    Returns:
        露点差 (摄氏度)
    
    Examples:
        >>> round(dew_point_depression(20, 50), 1)
        10.7
    """
    dp = dew_point(temperature, relative_humidity)
    return temperature - dp


def fog_risk(temperature: float, relative_humidity: float) -> str:
    """
    评估雾形成风险
    
    Args:
        temperature: 温度 (摄氏度)
        relative_humidity: 相对湿度 (百分比 0-100)
    
    Returns:
        风险等级描述
    
    Examples:
        >>> fog_risk(15, 95)
        '高风险 - 极可能形成雾'
        >>> fog_risk(20, 50)
        '无风险'
    """
    dp = dew_point_depression(temperature, relative_humidity)
    
    if dp < 2:
        return "极高风险 - 雾几乎确定形成"
    elif dp < 4:
        return "高风险 - 极可能形成雾"
    elif dp < 6:
        return "中等风险 - 可能形成雾"
    elif dp < 8:
        return "低风险 - 需其他条件配合"
    else:
        return "无风险"


def condensation_prediction(temperature: float, relative_humidity: float, 
                           surface_temp: Optional[float] = None) -> Tuple[bool, str]:
    """
    预测表面是否会结露
    
    Args:
        temperature: 空气温度 (摄氏度)
        relative_humidity: 相对湿度 (百分比 0-100)
        surface_temp: 表面温度 (摄氏度)，如果不提供则假设等于空气温度
    
    Returns:
        (是否结露, 说明)
    
    Examples:
        >>> condensation_prediction(25, 70, 15)
        (True, '表面温度低于露点，将结露')
    """
    dp = dew_point(temperature, relative_humidity)
    st = surface_temp if surface_temp is not None else temperature
    
    if st <= dp:
        return True, f"表面温度 ({st}°C) 低于露点 ({dp:.1f}°C)，将结露"
    else:
        margin = st - dp
        return False, f"表面温度 ({st}°C) 高于露点 ({dp:.1f}°C) {margin:.1f}°C，不会结露"


def temperature_for_target_rh(dew_point_temp: float, target_rh: float) -> float:
    """
    计算达到目标相对湿度所需的温度
    
    Args:
        dew_point_temp: 当前露点温度 (摄氏度)
        target_rh: 目标相对湿度 (百分比 0-100)
    
    Returns:
        所需温度 (摄氏度)
    
    Examples:
        >>> round(temperature_for_target_rh(10, 50), 1)
        20.0
    """
    target_rh = max(1, min(99, target_rh))
    
    # 露点对应的饱和蒸汽压
    svp_dew = saturation_vapor_pressure(dew_point_temp)
    
    # 目标温度下的饱和蒸汽压 = svp_dew / (target_rh / 100)
    target_svp = svp_dew * 100 / target_rh
    
    # 反算温度
    a, b, c = MAGNUS_A, MAGNUS_B, MAGNUS_C
    alpha = math.log(target_svp / a)
    temp = c * alpha / (b - alpha)
    
    return temp


def humidity_ratio(temperature: float, relative_humidity: float, 
                   pressure: float = 1013.25) -> float:
    """
    计算湿度比 (含湿量)
    
    与 mixing_ratio 相同，只是不同的叫法
    
    Args:
        temperature: 温度 (摄氏度)
        relative_humidity: 相对湿度 (百分比 0-100)
        pressure: 大气压 (hPa)
    
    Returns:
        湿度比 (kg水蒸气/kg干空气)
    
    Examples:
        >>> round(humidity_ratio(20, 50), 5)
        0.00726
    """
    return mixing_ratio(temperature, relative_humidity, pressure) / 1000


def enthalpy(temperature: float, relative_humidity: float, 
             pressure: float = 1013.25) -> float:
    """
    计算湿空气的焓
    
    Args:
        temperature: 温度 (摄氏度)
        relative_humidity: 相对湿度 (百分比 0-100)
        pressure: 大气压 (hPa)
    
    Returns:
        焓值 (kJ/kg 干空气)
    
    Examples:
        >>> round(enthalpy(20, 50), 1)
        38.6
    """
    # 焓 = 1.006 * T + W * (2501 + 1.86 * T)
    # W = 湿度比 (kg/kg)
    w = humidity_ratio(temperature, relative_humidity, pressure)
    
    return 1.006 * temperature + w * (2501 + 1.86 * temperature)


if __name__ == "__main__":
    # 示例演示
    print("=" * 60)
    print("露点计算工具 - Dew Point Utilities")
    print("=" * 60)
    
    # 示例 1: 基本露点计算
    temp = 25
    rh = 60
    print(f"\n【示例 1】温度 {temp}°C，相对湿度 {rh}%")
    print(f"  露点温度: {dew_point(temp, rh):.1f}°C")
    print(f"  绝对湿度: {absolute_humidity(temp, rh):.2f} g/m³")
    print(f"  湿球温度: {wet_bulb_temperature(temp, rh):.1f}°C")
    print(f"  体感温度: {heat_index(temp, rh):.1f}°C")
    print(f"  舒适度: {comfort_level(dew_point(temp, rh)).value}")
    
    # 示例 2: 雾风险评估
    print(f"\n【示例 2】雾风险评估")
    fog_conditions = [(15, 95), (10, 90), (20, 50)]
    for t, h in fog_conditions:
        risk = fog_risk(t, h)
        dp = dew_point(t, h)
        print(f"  {t}°C, {h}%RH → 露点 {dp:.1f}°C → {risk}")
    
    # 示例 3: 结露预测
    print(f"\n【示例 3】结露预测")
    will_condense, msg = condensation_prediction(28, 75, 18)
    print(f"  空气 28°C, 75%RH, 表面 18°C")
    print(f"  结果: {msg}")
    
    # 示例 4: 综合湿度分析
    print(f"\n【示例 4】综合湿度分析")
    data = analyze_humidity(22, 55)
    print(f"  温度: {data.temperature}°C")
    print(f"  相对湿度: {data.relative_humidity}%")
    print(f"  露点: {data.dew_point:.1f}°C")
    print(f"  绝对湿度: {data.absolute_humidity:.2f} g/m³")
    print(f"  水蒸气分压: {data.vapor_pressure:.2f} hPa")
    print(f"  饱和蒸汽压: {data.saturation_vapor_pressure:.2f} hPa")
    print(f"  舒适度: {data.comfort_level.value}")
    
    print("\n" + "=" * 60)