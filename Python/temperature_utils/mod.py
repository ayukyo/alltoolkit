"""
Temperature Utils - 温度转换工具

零依赖的温度转换库，支持：
- 摄氏度(Celsius)、华氏度(Fahrenheit)、开尔文(Kelvin)、兰氏度(Rankine)
- 批量转换
- 温度范围验证
- 常见温度参考点
- 温度比较和运算

Author: AllToolkit
License: MIT
"""

from typing import Union, List, Tuple, Optional, Dict
from enum import Enum


class TemperatureUnit(Enum):
    """温度单位枚举"""
    CELSIUS = 'C'
    FAHRENHEIT = 'F'
    KELVIN = 'K'
    RANKINE = 'R'


# 单位别名映射
UNIT_ALIASES = {
    # 摄氏度
    'c': TemperatureUnit.CELSIUS,
    'celsius': TemperatureUnit.CELSIUS,
    '摄氏度': TemperatureUnit.CELSIUS,
    '℃': TemperatureUnit.CELSIUS,
    # 华氏度
    'f': TemperatureUnit.FAHRENHEIT,
    'fahrenheit': TemperatureUnit.FAHRENHEIT,
    '华氏度': TemperatureUnit.FAHRENHEIT,
    '℉': TemperatureUnit.FAHRENHEIT,
    # 开尔文
    'k': TemperatureUnit.KELVIN,
    'kelvin': TemperatureUnit.KELVIN,
    '开尔文': TemperatureUnit.KELVIN,
    '开': TemperatureUnit.KELVIN,
    # 兰氏度
    'r': TemperatureUnit.RANKINE,
    'rankine': TemperatureUnit.RANKINE,
    '兰氏度': TemperatureUnit.RANKINE,
    '兰金': TemperatureUnit.RANKINE,
}

# 绝对零度（各单位的最低温度）
ABSOLUTE_ZERO = {
    TemperatureUnit.CELSIUS: -273.15,
    TemperatureUnit.FAHRENHEIT: -459.67,
    TemperatureUnit.KELVIN: 0.0,
    TemperatureUnit.RANKINE: 0.0,
}

# 常见温度参考点
REFERENCE_POINTS = {
    'absolute_zero': {
        TemperatureUnit.CELSIUS: -273.15,
        TemperatureUnit.FAHRENHEIT: -459.67,
        TemperatureUnit.KELVIN: 0.0,
        TemperatureUnit.RANKINE: 0.0,
        'description': '绝对零度',
    },
    'liquid_nitrogen_boiling': {
        TemperatureUnit.CELSIUS: -195.8,
        TemperatureUnit.FAHRENHEIT: -320.4,
        TemperatureUnit.KELVIN: 77.35,
        TemperatureUnit.RANKINE: 139.23,
        'description': '液氮沸点',
    },
    'dry_ice_sublimation': {
        TemperatureUnit.CELSIUS: -78.5,
        TemperatureUnit.FAHRENHEIT: -109.3,
        TemperatureUnit.KELVIN: 194.65,
        TemperatureUnit.RANKINE: 350.37,
        'description': '干冰升华点',
    },
    'water_freezing': {
        TemperatureUnit.CELSIUS: 0.0,
        TemperatureUnit.FAHRENHEIT: 32.0,
        TemperatureUnit.KELVIN: 273.15,
        TemperatureUnit.RANKINE: 491.67,
        'description': '水冰点（标准大气压）',
    },
    'room_temperature': {
        TemperatureUnit.CELSIUS: 20.0,
        TemperatureUnit.FAHRENHEIT: 68.0,
        TemperatureUnit.KELVIN: 293.15,
        TemperatureUnit.RANKINE: 527.67,
        'description': '室温（标准）',
    },
    'human_body': {
        TemperatureUnit.CELSIUS: 37.0,
        TemperatureUnit.FAHRENHEIT: 98.6,
        TemperatureUnit.KELVIN: 310.15,
        TemperatureUnit.RANKINE: 558.27,
        'description': '人体正常温度',
    },
    'water_boiling': {
        TemperatureUnit.CELSIUS: 100.0,
        TemperatureUnit.FAHRENHEIT: 212.0,
        TemperatureUnit.KELVIN: 373.15,
        TemperatureUnit.RANKINE: 671.67,
        'description': '水沸点（标准大气压）',
    },
    'gold_melting': {
        TemperatureUnit.CELSIUS: 1064.0,
        TemperatureUnit.FAHRENHEIT: 1947.2,
        TemperatureUnit.KELVIN: 1337.15,
        TemperatureUnit.RANKINE: 2406.87,
        'description': '金熔点',
    },
    'sun_surface': {
        TemperatureUnit.CELSIUS: 5500.0,
        TemperatureUnit.FAHRENHEIT: 9932.0,
        TemperatureUnit.KELVIN: 5773.15,
        TemperatureUnit.RANKINE: 10391.67,
        'description': '太阳表面温度',
    },
}


class TemperatureError(Exception):
    """温度相关错误的基类"""
    pass


class InvalidTemperatureError(TemperatureError):
    """无效的温度值（低于绝对零度）"""
    pass


class InvalidUnitError(TemperatureError):
    """无效的温度单位"""
    pass


def _parse_unit(unit: Union[str, TemperatureUnit]) -> TemperatureUnit:
    """
    解析温度单位
    
    Args:
        unit: 单位字符串或枚举值
    
    Returns:
        TemperatureUnit 枚举值
    
    Raises:
        InvalidUnitError: 无效的单位
    """
    if isinstance(unit, TemperatureUnit):
        return unit
    
    if isinstance(unit, str):
        unit_lower = unit.lower().strip()
        if unit_lower in UNIT_ALIASES:
            return UNIT_ALIASES[unit_lower]
    
    raise InvalidUnitError(f"无效的温度单位: '{unit}'。支持的单位: C, F, K, R")


def _check_absolute_zero(value: float, unit: TemperatureUnit) -> None:
    """
    检查温度是否低于绝对零度
    
    Args:
        value: 温度值
        unit: 温度单位
    
    Raises:
        InvalidTemperatureError: 温度低于绝对零度
    """
    if value < ABSOLUTE_ZERO[unit]:
        raise InvalidTemperatureError(
            f"温度 {value}°{unit.value} 低于绝对零度 "
            f"({ABSOLUTE_ZERO[unit]}°{unit.value})"
        )


# ============== 核心转换函数 ==============

def celsius_to_fahrenheit(celsius: float) -> float:
    """摄氏度 → 华氏度"""
    return celsius * 9 / 5 + 32


def celsius_to_kelvin(celsius: float) -> float:
    """摄氏度 → 开尔文"""
    return celsius + 273.15


def celsius_to_rankine(celsius: float) -> float:
    """摄氏度 → 兰氏度"""
    return (celsius + 273.15) * 9 / 5


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """华氏度 → 摄氏度"""
    return (fahrenheit - 32) * 5 / 9


def fahrenheit_to_kelvin(fahrenheit: float) -> float:
    """华氏度 → 开尔文"""
    return (fahrenheit + 459.67) * 5 / 9


def fahrenheit_to_rankine(fahrenheit: float) -> float:
    """华氏度 → 兰氏度"""
    return fahrenheit + 459.67


def kelvin_to_celsius(kelvin: float) -> float:
    """开尔文 → 摄氏度"""
    return kelvin - 273.15


def kelvin_to_fahrenheit(kelvin: float) -> float:
    """开尔文 → 华氏度"""
    return kelvin * 9 / 5 - 459.67


def kelvin_to_rankine(kelvin: float) -> float:
    """开尔文 → 兰氏度"""
    return kelvin * 9 / 5


def rankine_to_celsius(rankine: float) -> float:
    """兰氏度 → 摄氏度"""
    return (rankine - 491.67) * 5 / 9


def rankine_to_fahrenheit(rankine: float) -> float:
    """兰氏度 → 华氏度"""
    return rankine - 459.67


def rankine_to_kelvin(rankine: float) -> float:
    """兰氏度 → 开尔文"""
    return rankine * 5 / 9


# 转换函数映射表
_CONVERSION_TABLE = {
    (TemperatureUnit.CELSIUS, TemperatureUnit.FAHRENHEIT): celsius_to_fahrenheit,
    (TemperatureUnit.CELSIUS, TemperatureUnit.KELVIN): celsius_to_kelvin,
    (TemperatureUnit.CELSIUS, TemperatureUnit.RANKINE): celsius_to_rankine,
    (TemperatureUnit.FAHRENHEIT, TemperatureUnit.CELSIUS): fahrenheit_to_celsius,
    (TemperatureUnit.FAHRENHEIT, TemperatureUnit.KELVIN): fahrenheit_to_kelvin,
    (TemperatureUnit.FAHRENHEIT, TemperatureUnit.RANKINE): fahrenheit_to_rankine,
    (TemperatureUnit.KELVIN, TemperatureUnit.CELSIUS): kelvin_to_celsius,
    (TemperatureUnit.KELVIN, TemperatureUnit.FAHRENHEIT): kelvin_to_fahrenheit,
    (TemperatureUnit.KELVIN, TemperatureUnit.RANKINE): kelvin_to_rankine,
    (TemperatureUnit.RANKINE, TemperatureUnit.CELSIUS): rankine_to_celsius,
    (TemperatureUnit.RANKINE, TemperatureUnit.FAHRENHEIT): rankine_to_fahrenheit,
    (TemperatureUnit.RANKINE, TemperatureUnit.KELVIN): rankine_to_kelvin,
}


def convert(
    value: float,
    from_unit: Union[str, TemperatureUnit],
    to_unit: Union[str, TemperatureUnit],
    check_valid: bool = True,
    precision: Optional[int] = None
) -> float:
    """
    温度单位转换
    
    Args:
        value: 温度值
        from_unit: 源单位
        to_unit: 目标单位
        check_valid: 是否检查温度有效性（低于绝对零度）
        precision: 保留小数位数，None 表示不处理
    
    Returns:
        转换后的温度值
    
    Raises:
        InvalidTemperatureError: 温度低于绝对零度
        InvalidUnitError: 无效的单位
    
    Examples:
        >>> convert(0, 'C', 'F')
        32.0
        >>> convert(100, 'C', 'K')
        373.15
        >>> convert(32, 'F', 'C')
        0.0
        >>> convert(0, 'K', 'C')
        -273.15
    """
    from_unit = _parse_unit(from_unit)
    to_unit = _parse_unit(to_unit)
    
    if check_valid:
        _check_absolute_zero(value, from_unit)
    
    # 相同单位直接返回
    if from_unit == to_unit:
        result = value
    else:
        converter = _CONVERSION_TABLE.get((from_unit, to_unit))
        if converter is None:
            raise InvalidUnitError(
                f"不支持从 {from_unit.value} 到 {to_unit.value} 的转换"
            )
        result = converter(value)
    
    if precision is not None:
        result = round(result, precision)
    
    return result


def convert_all(
    value: float,
    from_unit: Union[str, TemperatureUnit],
    precision: Optional[int] = None
) -> Dict[str, float]:
    """
    将温度转换为所有单位
    
    Args:
        value: 温度值
        from_unit: 源单位
        precision: 保留小数位数
    
    Returns:
        所有单位的温度字典
    
    Examples:
        >>> convert_all(0, 'C')
        {'celsius': 0.0, 'fahrenheit': 32.0, 'kelvin': 273.15, 'rankine': 491.67}
    """
    from_unit = _parse_unit(from_unit)
    
    result = {}
    for unit in TemperatureUnit:
        result[unit.name.lower()] = convert(value, from_unit, unit, precision=precision)
    
    return result


def batch_convert(
    values: List[float],
    from_unit: Union[str, TemperatureUnit],
    to_unit: Union[str, TemperatureUnit],
    skip_invalid: bool = False,
    precision: Optional[int] = None
) -> List[Tuple[float, Union[float, None], Union[str, None]]]:
    """
    批量温度转换
    
    Args:
        values: 温度值列表
        from_unit: 源单位
        to_unit: 目标单位
        skip_invalid: 是否跳过无效值
        precision: 保留小数位数
    
    Returns:
        列表，每项为 (原值, 结果, 错误信息)
    
    Examples:
        >>> batch_convert([0, 100, -273.15], 'C', 'F')
        [(0, 32.0, None), (100, 212.0, None), (-273.15, -459.67, None)]
    """
    results = []
    
    for value in values:
        try:
            converted = convert(value, from_unit, to_unit, precision=precision)
            results.append((value, converted, None))
        except Exception as e:
            if skip_invalid:
                results.append((value, None, str(e)))
            else:
                raise
    
    return results


# ============== 温度验证和检查函数 ==============

def is_valid_temperature(
    value: float,
    unit: Union[str, TemperatureUnit]
) -> bool:
    """
    检查温度值是否有效（不低于绝对零度）
    
    Args:
        value: 温度值
        unit: 温度单位
    
    Returns:
        是否有效
    
    Examples:
        >>> is_valid_temperature(0, 'K')
        True
        >>> is_valid_temperature(-1, 'K')
        False
    """
    unit = _parse_unit(unit)
    return value >= ABSOLUTE_ZERO[unit]


def is_above_freezing(
    value: float,
    unit: Union[str, TemperatureUnit] = TemperatureUnit.CELSIUS
) -> bool:
    """
    检查温度是否在冰点以上
    
    Args:
        value: 温度值
        unit: 温度单位
    
    Returns:
        是否在冰点以上
    
    Examples:
        >>> is_above_freezing(0, 'C')
        True
        >>> is_above_freezing(-1, 'C')
        False
    """
    celsius = convert(value, unit, TemperatureUnit.CELSIUS, check_valid=True)
    return celsius >= 0


def is_below_freezing(
    value: float,
    unit: Union[str, TemperatureUnit] = TemperatureUnit.CELSIUS
) -> bool:
    """
    检查温度是否在冰点以下
    
    Args:
        value: 温度值
        unit: 温度单位
    
    Returns:
        是否在冰点以下
    
    Examples:
        >>> is_below_freezing(-1, 'C')
        True
        >>> is_below_freezing(0, 'C')
        False
    """
    celsius = convert(value, unit, TemperatureUnit.CELSIUS, check_valid=True)
    return celsius < 0


def is_fever(
    value: float,
    unit: Union[str, TemperatureUnit] = TemperatureUnit.CELSIUS
) -> bool:
    """
    检查是否发烧（人体温度超过37.5°C）
    
    Args:
        value: 温度值
        unit: 温度单位
    
    Returns:
        是否发烧
    
    Examples:
        >>> is_fever(38, 'C')
        True
        >>> is_fever(37, 'C')
        False
    """
    celsius = convert(value, unit, TemperatureUnit.CELSIUS, check_valid=True)
    return celsius > 37.5


def is_hypothermia(
    value: float,
    unit: Union[str, TemperatureUnit] = TemperatureUnit.CELSIUS
) -> bool:
    """
    检查是否体温过低（低于35°C）
    
    Args:
        value: 温度值
        unit: 温度单位
    
    Returns:
        是否体温过低
    
    Examples:
        >>> is_hypothermia(34, 'C')
        True
        >>> is_hypothermia(36, 'C')
        False
    """
    celsius = convert(value, unit, TemperatureUnit.CELSIUS, check_valid=True)
    return celsius < 35


def get_temperature_category(
    value: float,
    unit: Union[str, TemperatureUnit] = TemperatureUnit.CELSIUS
) -> str:
    """
    获取温度类别
    
    Args:
        value: 温度值
        unit: 温度单位
    
    Returns:
        温度类别描述
    
    Examples:
        >>> get_temperature_category(-10, 'C')
        '极寒'
        >>> get_temperature_category(25, 'C')
        '舒适'
    """
    celsius = convert(value, unit, TemperatureUnit.CELSIUS, check_valid=True)
    
    if celsius < -30:
        return '极寒'
    elif celsius < -10:
        return '严寒'
    elif celsius < 0:
        return '寒冷'
    elif celsius < 10:
        return '凉爽'
    elif celsius < 20:
        return '温和'
    elif celsius < 26:
        return '舒适'
    elif celsius < 30:
        return '温暖'
    elif celsius < 35:
        return '炎热'
    elif celsius < 40:
        return '酷热'
    else:
        return '极热'


def get_temperature_description(
    value: float,
    unit: Union[str, TemperatureUnit] = TemperatureUnit.CELSIUS
) -> str:
    """
    获取温度描述（包含所有单位的值）
    
    Args:
        value: 温度值
        unit: 温度单位
    
    Returns:
        温度描述字符串
    
    Examples:
        >>> get_temperature_description(25, 'C')
        '25.0°C = 77.0°F = 298.15K = 536.67°R (舒适)'
    """
    unit = _parse_unit(unit)
    all_temps = convert_all(value, unit, precision=2)
    category = get_temperature_category(value, unit)
    
    return (
        f"{all_temps['celsius']}°C = "
        f"{all_temps['fahrenheit']}°F = "
        f"{all_temps['kelvin']}K = "
        f"{all_temps['rankine']}°R "
        f"({category})"
    )


# ============== 温度比较和运算 ==============

def compare(
    temp1: float,
    unit1: Union[str, TemperatureUnit],
    temp2: float,
    unit2: Union[str, TemperatureUnit]
) -> int:
    """
    比较两个温度
    
    Args:
        temp1: 第一个温度值
        unit1: 第一个温度单位
        temp2: 第二个温度值
        unit2: 第二个温度单位
    
    Returns:
        负数表示temp1<temp2，0表示相等，正数表示temp1>temp2
    
    Examples:
        >>> compare(0, 'C', 32, 'F')
        0
        >>> compare(100, 'C', 212, 'F')
        0
        >>> compare(0, 'C', 100, 'C')
        -100
    """
    k1 = convert(temp1, unit1, TemperatureUnit.KELVIN)
    k2 = convert(temp2, unit2, TemperatureUnit.KELVIN)
    
    if abs(k1 - k2) < 1e-10:  # 浮点数精度处理
        return 0
    return -1 if k1 < k2 else 1


def add(
    temp: float,
    unit: Union[str, TemperatureUnit],
    delta: float,
    delta_unit: Union[str, TemperatureUnit] = TemperatureUnit.CELSIUS,
    result_unit: Optional[Union[str, TemperatureUnit]] = None,
    precision: Optional[int] = None
) -> float:
    """
    温度加法（注意：温度差和温度值不同）
    
    Args:
        temp: 基础温度值
        unit: 基础温度单位
        delta: 温度变化量
        delta_unit: 温度变化单位（默认摄氏度）
        result_unit: 结果单位（默认与基础单位相同）
        precision: 保留小数位数
    
    Returns:
        结果温度
    
    Examples:
        >>> add(0, 'C', 10, 'C')
        10.0
        >>> add(32, 'F', 10, 'C')  # 10°C温差 ≈ 18°F温差
        50.0
    """
    unit = _parse_unit(unit)
    delta_unit = _parse_unit(delta_unit)
    result_unit = _parse_unit(result_unit) if result_unit else unit
    
    # 转换为开尔文进行计算
    kelvin = convert(temp, unit, TemperatureUnit.KELVIN)
    
    # 计算温差对应的开尔文值
    # 温差的转换需要特殊处理
    if delta_unit == TemperatureUnit.KELVIN:
        kelvin_delta = delta
    elif delta_unit == TemperatureUnit.CELSIUS:
        kelvin_delta = delta  # 1°C温差 = 1K温差
    elif delta_unit == TemperatureUnit.FAHRENHEIT:
        kelvin_delta = delta * 5 / 9  # 1°F温差 = 5/9 K温差
    elif delta_unit == TemperatureUnit.RANKINE:
        kelvin_delta = delta * 5 / 9  # 1°R温差 = 5/9 K温差
    else:
        raise InvalidUnitError(f"不支持的温差单位: {delta_unit}")
    
    result_kelvin = kelvin + kelvin_delta
    return convert(result_kelvin, TemperatureUnit.KELVIN, result_unit, precision=precision)


def subtract(
    temp: float,
    unit: Union[str, TemperatureUnit],
    delta: float,
    delta_unit: Union[str, TemperatureUnit] = TemperatureUnit.CELSIUS,
    result_unit: Optional[Union[str, TemperatureUnit]] = None,
    precision: Optional[int] = None
) -> float:
    """
    温度减法
    
    Args:
        temp: 基础温度值
        unit: 基础温度单位
        delta: 温度变化量
        delta_unit: 温度变化单位
        result_unit: 结果单位
        precision: 保留小数位数
    
    Returns:
        结果温度
    
    Examples:
        >>> subtract(10, 'C', 5, 'C')
        5.0
    """
    return add(temp, unit, -delta, delta_unit, result_unit, precision)


def difference(
    temp1: float,
    unit1: Union[str, TemperatureUnit],
    temp2: float,
    unit2: Union[str, TemperatureUnit],
    result_unit: Union[str, TemperatureUnit] = TemperatureUnit.CELSIUS
) -> float:
    """
    计算两个温度的差值
    
    Args:
        temp1: 第一个温度值
        unit1: 第一个温度单位
        temp2: 第二个温度值
        unit2: 第二个温度单位
        result_unit: 结果单位
    
    Returns:
        温度差值
    
    Examples:
        >>> difference(100, 'C', 0, 'C')
        100.0
        >>> difference(212, 'F', 32, 'F', 'C')
        100.0
    """
    k1 = convert(temp1, unit1, TemperatureUnit.KELVIN)
    k2 = convert(temp2, unit2, TemperatureUnit.KELVIN)
    delta_k = k1 - k2
    
    # 转换温差到目标单位
    result_unit = _parse_unit(result_unit)
    if result_unit == TemperatureUnit.KELVIN:
        return delta_k
    elif result_unit == TemperatureUnit.CELSIUS:
        return delta_k
    elif result_unit == TemperatureUnit.FAHRENHEIT:
        return delta_k * 9 / 5
    elif result_unit == TemperatureUnit.RANKINE:
        return delta_k * 9 / 5
    else:
        raise InvalidUnitError(f"不支持的结果单位: {result_unit}")


# ============== 温度范围函数 ==============

def in_range(
    value: float,
    unit: Union[str, TemperatureUnit],
    min_val: float,
    max_val: float,
    range_unit: Union[str, TemperatureUnit] = TemperatureUnit.CELSIUS
) -> bool:
    """
    检查温度是否在指定范围内
    
    Args:
        value: 温度值
        unit: 温度单位
        min_val: 最小值
        max_val: 最大值
        range_unit: 范围单位
    
    Returns:
        是否在范围内
    
    Examples:
        >>> in_range(25, 'C', 20, 30, 'C')
        True
        >>> in_range(15, 'C', 20, 30, 'C')
        False
    """
    celsius = convert(value, unit, TemperatureUnit.CELSIUS)
    min_celsius = convert(min_val, range_unit, TemperatureUnit.CELSIUS)
    max_celsius = convert(max_val, range_unit, TemperatureUnit.CELSIUS)
    
    return min_celsius <= celsius <= max_celsius


def get_reference_point(name: str) -> Dict:
    """
    获取温度参考点
    
    Args:
        name: 参考点名称
    
    Returns:
        参考点信息字典
    
    Raises:
        KeyError: 参考点不存在
    
    Examples:
        >>> get_reference_point('water_boiling')
        {'celsius': 100.0, 'fahrenheit': 212.0, ...}
    """
    if name not in REFERENCE_POINTS:
        available = ', '.join(REFERENCE_POINTS.keys())
        raise KeyError(f"参考点 '{name}' 不存在。可用的参考点: {available}")
    
    point = REFERENCE_POINTS[name]
    return {
        'celsius': point[TemperatureUnit.CELSIUS],
        'fahrenheit': point[TemperatureUnit.FAHRENHEIT],
        'kelvin': point[TemperatureUnit.KELVIN],
        'rankine': point[TemperatureUnit.RANKINE],
        'description': point['description'],
    }


def list_reference_points() -> List[Tuple[str, str, float]]:
    """
    列出所有温度参考点
    
    Returns:
        列表，每项为 (名称, 描述, 摄氏度值)
    
    Examples:
        >>> list_reference_points()
        [('absolute_zero', '绝对零度', -273.15), ...]
    """
    return [
        (name, REFERENCE_POINTS[name]['description'], 
         REFERENCE_POINTS[name][TemperatureUnit.CELSIUS])
        for name in REFERENCE_POINTS
    ]


def find_nearest_reference(
    value: float,
    unit: Union[str, TemperatureUnit] = TemperatureUnit.CELSIUS
) -> Tuple[str, str, float]:
    """
    找到最接近的参考点
    
    Args:
        value: 温度值
        unit: 温度单位
    
    Returns:
        (参考点名称, 描述, 与参考点的温差)
    
    Examples:
        >>> find_nearest_reference(37, 'C')
        ('human_body', '人体正常温度', 0.0)
    """
    unit = _parse_unit(unit)
    
    nearest_name = None
    nearest_diff = float('inf')
    
    for name, point in REFERENCE_POINTS.items():
        ref_val = point[unit]
        diff = abs(value - ref_val)
        if diff < nearest_diff:
            nearest_diff = diff
            nearest_name = name
    
    return (nearest_name, REFERENCE_POINTS[nearest_name]['description'], nearest_diff)


# ============== 格式化函数 ==============

def format_temperature(
    value: float,
    unit: Union[str, TemperatureUnit],
    precision: int = 1,
    include_unit: bool = True
) -> str:
    """
    格式化温度显示
    
    Args:
        value: 温度值
        unit: 温度单位
        precision: 小数位数
        include_unit: 是否包含单位符号
    
    Returns:
        格式化的温度字符串
    
    Examples:
        >>> format_temperature(36.5, 'C')
        '36.5°C'
        >>> format_temperature(36.5, 'C', precision=0)
        '37°C'
        >>> format_temperature(36.5, 'C', include_unit=False)
        '36.5'
    """
    unit = _parse_unit(unit)
    formatted = f"{value:.{precision}f}"
    
    if include_unit:
        symbols = {
            TemperatureUnit.CELSIUS: '°C',
            TemperatureUnit.FAHRENHEIT: '°F',
            TemperatureUnit.KELVIN: 'K',
            TemperatureUnit.RANKINE: '°R',
        }
        formatted += symbols[unit]
    
    return formatted


def parse_temperature(text: str) -> Tuple[float, TemperatureUnit]:
    """
    解析温度字符串
    
    Args:
        text: 温度字符串（如 "36.5°C", "100 F", "273.15K"）
    
    Returns:
        (温度值, 单位枚举)
    
    Raises:
        ValueError: 无法解析
    
    Examples:
        >>> parse_temperature("36.5°C")
        (36.5, <TemperatureUnit.CELSIUS: 'C'>)
        >>> parse_temperature("100 F")
        (100.0, <TemperatureUnit.FAHRENHEIT: 'F'>)
    """
    import re
    
    text = text.strip()
    
    # 匹配数字和单位
    match = re.match(r'^(-?\d+\.?\d*)\s*([℃CFKR°\u2103\u2109]?)\s*([CFKR]?).*$', text, re.IGNORECASE)
    
    if not match:
        raise ValueError(f"无法解析温度字符串: '{text}'")
    
    value = float(match.group(1))
    unit_char = match.group(2) or match.group(3)
    
    # 确定单位
    if unit_char in ['C', '℃', '°', '']:
        # 默认摄氏度，或明确指定
        unit = TemperatureUnit.CELSIUS
    elif unit_char in ['F', '℉']:
        unit = TemperatureUnit.FAHRENHEIT
    elif unit_char in ['K']:
        unit = TemperatureUnit.KELVIN
    elif unit_char in ['R']:
        unit = TemperatureUnit.RANKINE
    else:
        # 尝试从完整单位名解析
        unit = _parse_unit(unit_char)
    
    return (value, unit)


# 导出的公共API
__all__ = [
    # 枚举和常量
    'TemperatureUnit',
    'ABSOLUTE_ZERO',
    'REFERENCE_POINTS',
    # 异常
    'TemperatureError',
    'InvalidTemperatureError',
    'InvalidUnitError',
    # 核心转换
    'convert',
    'convert_all',
    'batch_convert',
    # 基础转换函数
    'celsius_to_fahrenheit',
    'celsius_to_kelvin',
    'celsius_to_rankine',
    'fahrenheit_to_celsius',
    'fahrenheit_to_kelvin',
    'fahrenheit_to_rankine',
    'kelvin_to_celsius',
    'kelvin_to_fahrenheit',
    'kelvin_to_rankine',
    'rankine_to_celsius',
    'rankine_to_fahrenheit',
    'rankine_to_kelvin',
    # 验证函数
    'is_valid_temperature',
    'is_above_freezing',
    'is_below_freezing',
    'is_fever',
    'is_hypothermia',
    'get_temperature_category',
    'get_temperature_description',
    # 比较和运算
    'compare',
    'add',
    'subtract',
    'difference',
    # 范围函数
    'in_range',
    'get_reference_point',
    'list_reference_points',
    'find_nearest_reference',
    # 格式化
    'format_temperature',
    'parse_temperature',
]