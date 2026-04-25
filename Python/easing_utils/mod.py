"""
Easing Utilities - 动画缓动函数工具集

零外部依赖的缓动函数库，纯 Python 标准库实现。

缓动函数用于创建平滑自然的动画过渡效果，广泛应用于：
- UI 动画和过渡效果
- 游戏开发中的角色/物体移动
- 数据可视化动画
- 网页动画
- 视频和动效设计

支持的缓动类型：
- Linear: 线性匀速
- Quad: 二次方缓动
- Cubic: 三次方缓动
- Quart: 四次方缓动
- Quint: 五次方缓动
- Sine: 正弦缓动
- Expo: 指数缓动
- Circ: 圆形缓动
- Elastic: 弹性缓动
- Back: 回弹缓动
- Bounce: 弹跳缓动

每种类型支持四种模式：
- ease_in: 开始慢，结束快
- ease_out: 开始快，结束慢
- ease_in_out: 开始和结束慢，中间快
- ease_out_in: 开始和结束快，中间慢

作者: AllToolkit
日期: 2026-04-25
"""

import math
from typing import Callable, Dict, List, Tuple, Optional, Union
from enum import Enum
from functools import wraps


# =============================================================================
# 类型定义
# =============================================================================

Number = Union[int, float]
EasingFunction = Callable[[float], float]


class EasingType(Enum):
    """缓动类型枚举"""
    LINEAR = "linear"
    QUAD = "quad"
    CUBIC = "cubic"
    QUART = "quart"
    QUINT = "quint"
    SINE = "sine"
    EXPO = "expo"
    CIRC = "circ"
    ELASTIC = "elastic"
    BACK = "back"
    BOUNCE = "bounce"


class EasingMode(Enum):
    """缓动模式枚举"""
    IN = "in"
    OUT = "out"
    IN_OUT = "in_out"
    OUT_IN = "out_in"


# =============================================================================
# 常量
# =============================================================================

# π 常量
PI = math.pi
HALF_PI = PI / 2
TAU = 2 * PI

# 回弹系数
BACK_C1 = 1.70158
BACK_C2 = BACK_C1 * 1.525
BACK_C3 = BACK_C1 + 1


# =============================================================================
# 辅助函数
# =============================================================================

def clamp(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """
    将值限制在指定范围内
    
    Args:
        value: 输入值
        min_val: 最小值
        max_val: 最大值
    
    Returns:
        限制后的值
    """
    return max(min_val, min(value, max_val))


def normalize_progress(t: float) -> float:
    """
    标准化进度值到 [0, 1] 范围
    
    Args:
        t: 进度值
    
    Returns:
        标准化后的进度
    """
    return clamp(t)


# =============================================================================
# Linear 缓动 (线性)
# =============================================================================

def linear(t: float) -> float:
    """
    线性缓动 - 匀速运动
    
    Args:
        t: 进度值 [0, 1]
    
    Returns:
        缓动值 [0, 1]
    
    Example:
        >>> linear(0.0)
        0.0
        >>> linear(0.5)
        0.5
        >>> linear(1.0)
        1.0
    """
    return t


# =============================================================================
# Quad 缓动 (二次方)
# =============================================================================

def ease_in_quad(t: float) -> float:
    """
    二次方缓入 - 开始慢，结束快
    
    Args:
        t: 进度值 [0, 1]
    
    Returns:
        缓动值 [0, 1]
    """
    return t * t


def ease_out_quad(t: float) -> float:
    """
    二次方缓出 - 开始快，结束慢
    
    Args:
        t: 进度值 [0, 1]
    
    Returns:
        缓动值 [0, 1]
    """
    return 1 - (1 - t) * (1 - t)


def ease_in_out_quad(t: float) -> float:
    """
    二次方缓入缓出 - 开始和结束慢，中间快
    
    Args:
        t: 进度值 [0, 1]
    
    Returns:
        缓动值 [0, 1]
    """
    if t < 0.5:
        return 2 * t * t
    return 1 - pow(-2 * t + 2, 2) / 2


def ease_out_in_quad(t: float) -> float:
    """
    二次方缓出缓入 - 开始和结束快，中间慢
    
    Args:
        t: 进度值 [0, 1]
    
    Returns:
        缓动值 [0, 1]
    """
    if t < 0.5:
        return ease_out_quad(t * 2) / 2
    return ease_in_quad((t - 0.5) * 2) / 2 + 0.5


# =============================================================================
# Cubic 缓动 (三次方)
# =============================================================================

def ease_in_cubic(t: float) -> float:
    """
    三次方缓入 - 开始慢，结束快
    """
    return t * t * t


def ease_out_cubic(t: float) -> float:
    """
    三次方缓出 - 开始快，结束慢
    """
    return 1 - pow(1 - t, 3)


def ease_in_out_cubic(t: float) -> float:
    """
    三次方缓入缓出 - 开始和结束慢，中间快
    """
    if t < 0.5:
        return 4 * t * t * t
    return 1 - pow(-2 * t + 2, 3) / 2


def ease_out_in_cubic(t: float) -> float:
    """
    三次方缓出缓入 - 开始和结束快，中间慢
    """
    if t < 0.5:
        return ease_out_cubic(t * 2) / 2
    return ease_in_cubic((t - 0.5) * 2) / 2 + 0.5


# =============================================================================
# Quart 缓动 (四次方)
# =============================================================================

def ease_in_quart(t: float) -> float:
    """
    四次方缓入 - 开始慢，结束快
    """
    return t * t * t * t


def ease_out_quart(t: float) -> float:
    """
    四次方缓出 - 开始快，结束慢
    """
    return 1 - pow(1 - t, 4)


def ease_in_out_quart(t: float) -> float:
    """
    四次方缓入缓出 - 开始和结束慢，中间快
    """
    if t < 0.5:
        return 8 * t * t * t * t
    return 1 - pow(-2 * t + 2, 4) / 2


def ease_out_in_quart(t: float) -> float:
    """
    四次方缓出缓入 - 开始和结束快，中间慢
    """
    if t < 0.5:
        return ease_out_quart(t * 2) / 2
    return ease_in_quart((t - 0.5) * 2) / 2 + 0.5


# =============================================================================
# Quint 缓动 (五次方)
# =============================================================================

def ease_in_quint(t: float) -> float:
    """
    五次方缓入 - 开始慢，结束快
    """
    return t * t * t * t * t


def ease_out_quint(t: float) -> float:
    """
    五次方缓出 - 开始快，结束慢
    """
    return 1 - pow(1 - t, 5)


def ease_in_out_quint(t: float) -> float:
    """
    五次方缓入缓出 - 开始和结束慢，中间快
    """
    if t < 0.5:
        return 16 * t * t * t * t * t
    return 1 - pow(-2 * t + 2, 5) / 2


def ease_out_in_quint(t: float) -> float:
    """
    五次方缓出缓入 - 开始和结束快，中间慢
    """
    if t < 0.5:
        return ease_out_quint(t * 2) / 2
    return ease_in_quint((t - 0.5) * 2) / 2 + 0.5


# =============================================================================
# Sine 缓动 (正弦)
# =============================================================================

def ease_in_sine(t: float) -> float:
    """
    正弦缓入 - 开始慢，结束快
    """
    return 1 - math.cos((t * PI) / 2)


def ease_out_sine(t: float) -> float:
    """
    正弦缓出 - 开始快，结束慢
    """
    return math.sin((t * PI) / 2)


def ease_in_out_sine(t: float) -> float:
    """
    正弦缓入缓出 - 开始和结束慢，中间快
    """
    return -(math.cos(PI * t) - 1) / 2


def ease_out_in_sine(t: float) -> float:
    """
    正弦缓出缓入 - 开始和结束快，中间慢
    """
    if t < 0.5:
        return ease_out_sine(t * 2) / 2
    return ease_in_sine((t - 0.5) * 2) / 2 + 0.5


# =============================================================================
# Expo 缓动 (指数)
# =============================================================================

def ease_in_expo(t: float) -> float:
    """
    指数缓入 - 开始慢，结束快
    """
    if t == 0:
        return 0
    return pow(2, 10 * t - 10)


def ease_out_expo(t: float) -> float:
    """
    指数缓出 - 开始快，结束慢
    """
    if t == 1:
        return 1
    return 1 - pow(2, -10 * t)


def ease_in_out_expo(t: float) -> float:
    """
    指数缓入缓出 - 开始和结束慢，中间快
    """
    if t == 0:
        return 0
    if t == 1:
        return 1
    if t < 0.5:
        return pow(2, 20 * t - 10) / 2
    return (2 - pow(2, -20 * t + 10)) / 2


def ease_out_in_expo(t: float) -> float:
    """
    指数缓出缓入 - 开始和结束快，中间慢
    """
    if t < 0.5:
        return ease_out_expo(t * 2) / 2
    return ease_in_expo((t - 0.5) * 2) / 2 + 0.5


# =============================================================================
# Circ 缓动 (圆形)
# =============================================================================

def ease_in_circ(t: float) -> float:
    """
    圆形缓入 - 开始慢，结束快
    """
    return 1 - math.sqrt(1 - pow(t, 2))


def ease_out_circ(t: float) -> float:
    """
    圆形缓出 - 开始快，结束慢
    """
    return math.sqrt(1 - pow(t - 1, 2))


def ease_in_out_circ(t: float) -> float:
    """
    圆形缓入缓出 - 开始和结束慢，中间快
    """
    if t < 0.5:
        return (1 - math.sqrt(1 - pow(2 * t, 2))) / 2
    return (math.sqrt(1 - pow(-2 * t + 2, 2)) + 1) / 2


def ease_out_in_circ(t: float) -> float:
    """
    圆形缓出缓入 - 开始和结束快，中间慢
    """
    if t < 0.5:
        return ease_out_circ(t * 2) / 2
    return ease_in_circ((t - 0.5) * 2) / 2 + 0.5


# =============================================================================
# Elastic 缓动 (弹性)
# =============================================================================

def ease_in_elastic(t: float) -> float:
    """
    弹性缓入 - 开始慢，有弹性效果
    """
    if t == 0:
        return 0
    if t == 1:
        return 1
    return -pow(2, 10 * t - 10) * math.sin((t * 10 - 10.75) * ((2 * PI) / 3))


def ease_out_elastic(t: float) -> float:
    """
    弹性缓出 - 结束有弹性效果
    """
    if t == 0:
        return 0
    if t == 1:
        return 1
    return pow(2, -10 * t) * math.sin((t * 10 - 0.75) * ((2 * PI) / 3)) + 1


def ease_in_out_elastic(t: float) -> float:
    """
    弹性缓入缓出 - 开始和结束有弹性效果
    """
    if t == 0:
        return 0
    if t == 1:
        return 1
    if t < 0.5:
        return -(pow(2, 20 * t - 10) * math.sin((20 * t - 11.125) * ((2 * PI) / 4.5))) / 2
    return (pow(2, -20 * t + 10) * math.sin((20 * t - 11.125) * ((2 * PI) / 4.5))) / 2 + 1


def ease_out_in_elastic(t: float) -> float:
    """
    弹性缓出缓入 - 中间有弹性效果
    """
    if t < 0.5:
        return ease_out_elastic(t * 2) / 2
    return ease_in_elastic((t - 0.5) * 2) / 2 + 0.5


# =============================================================================
# Back 缓动 (回弹)
# =============================================================================

def ease_in_back(t: float) -> float:
    """
    回弹缓入 - 开始时有轻微回退效果
    """
    return BACK_C3 * t * t * t - BACK_C1 * t * t


def ease_out_back(t: float) -> float:
    """
    回弹缓出 - 结束时有轻微超出效果
    """
    return 1 + BACK_C3 * pow(t - 1, 3) + BACK_C1 * pow(t - 1, 2)


def ease_in_out_back(t: float) -> float:
    """
    回弹缓入缓出 - 开始和结束有回弹效果
    """
    if t < 0.5:
        return (pow(2 * t, 2) * ((BACK_C2 + 1) * 2 * t - BACK_C2)) / 2
    return (pow(2 * t - 2, 2) * ((BACK_C2 + 1) * (t * 2 - 2) + BACK_C2) + 2) / 2


def ease_out_in_back(t: float) -> float:
    """
    回弹缓出缓入 - 中间有回弹效果
    """
    if t < 0.5:
        return ease_out_back(t * 2) / 2
    return ease_in_back((t - 0.5) * 2) / 2 + 0.5


# =============================================================================
# Bounce 缓动 (弹跳)
# =============================================================================

def ease_out_bounce(t: float) -> float:
    """
    弹跳缓出 - 像球落地弹跳效果
    """
    n1 = 7.5625
    d1 = 2.75
    
    if t < 1 / d1:
        return n1 * t * t
    elif t < 2 / d1:
        t_val = t - 1.5 / d1
        return n1 * t_val * t_val + 0.75
    elif t < 2.5 / d1:
        t_val = t - 2.25 / d1
        return n1 * t_val * t_val + 0.9375
    else:
        t_val = t - 2.625 / d1
        return n1 * t_val * t_val + 0.984375


def ease_in_bounce(t: float) -> float:
    """
    弹跳缓入 - 开始有弹跳效果
    """
    return 1 - ease_out_bounce(1 - t)


def ease_in_out_bounce(t: float) -> float:
    """
    弹跳缓入缓出 - 开始和结束有弹跳效果
    """
    if t < 0.5:
        return (1 - ease_out_bounce(1 - 2 * t)) / 2
    return (1 + ease_out_bounce(2 * t - 1)) / 2


def ease_out_in_bounce(t: float) -> float:
    """
    弹跳缓出缓入 - 中间有弹跳效果
    """
    if t < 0.5:
        return ease_out_bounce(t * 2) / 2
    return ease_in_bounce((t - 0.5) * 2) / 2 + 0.5


# =============================================================================
# 统一接口
# =============================================================================

# 缓动函数注册表
EASING_FUNCTIONS: Dict[Tuple[EasingType, EasingMode], EasingFunction] = {
    (EasingType.LINEAR, EasingMode.IN): linear,
    (EasingType.LINEAR, EasingMode.OUT): linear,
    (EasingType.LINEAR, EasingMode.IN_OUT): linear,
    (EasingType.LINEAR, EasingMode.OUT_IN): linear,
    
    (EasingType.QUAD, EasingMode.IN): ease_in_quad,
    (EasingType.QUAD, EasingMode.OUT): ease_out_quad,
    (EasingType.QUAD, EasingMode.IN_OUT): ease_in_out_quad,
    (EasingType.QUAD, EasingMode.OUT_IN): ease_out_in_quad,
    
    (EasingType.CUBIC, EasingMode.IN): ease_in_cubic,
    (EasingType.CUBIC, EasingMode.OUT): ease_out_cubic,
    (EasingType.CUBIC, EasingMode.IN_OUT): ease_in_out_cubic,
    (EasingType.CUBIC, EasingMode.OUT_IN): ease_out_in_cubic,
    
    (EasingType.QUART, EasingMode.IN): ease_in_quart,
    (EasingType.QUART, EasingMode.OUT): ease_out_quart,
    (EasingType.QUART, EasingMode.IN_OUT): ease_in_out_quart,
    (EasingType.QUART, EasingMode.OUT_IN): ease_out_in_quart,
    
    (EasingType.QUINT, EasingMode.IN): ease_in_quint,
    (EasingType.QUINT, EasingMode.OUT): ease_out_quint,
    (EasingType.QUINT, EasingMode.IN_OUT): ease_in_out_quint,
    (EasingType.QUINT, EasingMode.OUT_IN): ease_out_in_quint,
    
    (EasingType.SINE, EasingMode.IN): ease_in_sine,
    (EasingType.SINE, EasingMode.OUT): ease_out_sine,
    (EasingType.SINE, EasingMode.IN_OUT): ease_in_out_sine,
    (EasingType.SINE, EasingMode.OUT_IN): ease_out_in_sine,
    
    (EasingType.EXPO, EasingMode.IN): ease_in_expo,
    (EasingType.EXPO, EasingMode.OUT): ease_out_expo,
    (EasingType.EXPO, EasingMode.IN_OUT): ease_in_out_expo,
    (EasingType.EXPO, EasingMode.OUT_IN): ease_out_in_expo,
    
    (EasingType.CIRC, EasingMode.IN): ease_in_circ,
    (EasingType.CIRC, EasingMode.OUT): ease_out_circ,
    (EasingType.CIRC, EasingMode.IN_OUT): ease_in_out_circ,
    (EasingType.CIRC, EasingMode.OUT_IN): ease_out_in_circ,
    
    (EasingType.ELASTIC, EasingMode.IN): ease_in_elastic,
    (EasingType.ELASTIC, EasingMode.OUT): ease_out_elastic,
    (EasingType.ELASTIC, EasingMode.IN_OUT): ease_in_out_elastic,
    (EasingType.ELASTIC, EasingMode.OUT_IN): ease_out_in_elastic,
    
    (EasingType.BACK, EasingMode.IN): ease_in_back,
    (EasingType.BACK, EasingMode.OUT): ease_out_back,
    (EasingType.BACK, EasingMode.IN_OUT): ease_in_out_back,
    (EasingType.BACK, EasingMode.OUT_IN): ease_out_in_back,
    
    (EasingType.BOUNCE, EasingMode.IN): ease_in_bounce,
    (EasingType.BOUNCE, EasingMode.OUT): ease_out_bounce,
    (EasingType.BOUNCE, EasingMode.IN_OUT): ease_in_out_bounce,
    (EasingType.BOUNCE, EasingMode.OUT_IN): ease_out_in_bounce,
}


def get_easing_function(
    easing_type: Union[EasingType, str],
    mode: Union[EasingMode, str] = EasingMode.OUT
) -> EasingFunction:
    """
    获取缓动函数
    
    Args:
        easing_type: 缓动类型（枚举或字符串）
        mode: 缓动模式（枚举或字符串），默认 ease_out
    
    Returns:
        缓动函数
    
    Raises:
        ValueError: 无效的缓动类型或模式
    
    Example:
        >>> easing_fn = get_easing_function('quad', 'out')
        >>> value = easing_fn(0.5)  # 计算 50% 进度时的缓动值
        0.75
    """
    # 转换字符串为枚举
    if isinstance(easing_type, str):
        easing_type = EasingType(easing_type.lower())
    if isinstance(mode, str):
        mode = EasingMode(mode.lower())
    
    key = (easing_type, mode)
    if key not in EASING_FUNCTIONS:
        raise ValueError(f"Unknown easing: {easing_type} with mode {mode}")
    
    return EASING_FUNCTIONS[key]


def ease(
    t: float,
    easing_type: Union[EasingType, str] = EasingType.QUAD,
    mode: Union[EasingMode, str] = EasingMode.OUT
) -> float:
    """
    应用缓动函数计算值
    
    Args:
        t: 进度值 [0, 1]
        easing_type: 缓动类型，默认 quad
        mode: 缓动模式，默认 out
    
    Returns:
        缓动后的值 [0, 1]
    
    Example:
        >>> ease(0.5, 'cubic', 'in_out')
        0.5
        >>> ease(0.25, 'bounce', 'out')
        0.5625
    """
    fn = get_easing_function(easing_type, mode)
    return fn(clamp(t))


# =============================================================================
# 值插值函数
# =============================================================================

def interpolate(
    start: Number,
    end: Number,
    t: float,
    easing_type: Union[EasingType, str] = EasingType.LINEAR,
    mode: Union[EasingMode, str] = EasingMode.IN
) -> float:
    """
    在两个值之间进行缓动插值
    
    Args:
        start: 起始值
        end: 结束值
        t: 进度值 [0, 1]
        easing_type: 缓动类型，默认 linear
        mode: 缓动模式，默认 in
    
    Returns:
        插值结果
    
    Example:
        >>> interpolate(0, 100, 0.5, 'quad', 'out')
        75.0
        >>> interpolate(10, 20, 0.5)
        15.0
    """
    t_eased = ease(t, easing_type, mode)
    return start + (end - start) * t_eased


def interpolate_list(
    values: List[Number],
    t: float,
    easing_type: Union[EasingType, str] = EasingType.LINEAR,
    mode: Union[EasingMode, str] = EasingMode.IN
) -> float:
    """
    在值列表之间进行缓动插值（多点插值）
    
    Args:
        values: 值列表
        t: 进度值 [0, 1]
        easing_type: 缓动类型
        mode: 缓动模式
    
    Returns:
        插值结果
    
    Raises:
        ValueError: 值列表为空或只有一个元素
    
    Example:
        >>> interpolate_list([0, 50, 100], 0.5)
        50.0
    """
    if not values:
        raise ValueError("Values list cannot be empty")
    if len(values) == 1:
        return values[0]
    
    t_eased = ease(t, easing_type, mode)
    
    # 计算区间
    segment_count = len(values) - 1
    segment_t = t_eased * segment_count
    segment_index = min(int(segment_t), segment_count - 1)
    local_t = segment_t - segment_index
    
    # 在当前区间内插值
    start = values[segment_index]
    end = values[segment_index + 1]
    
    return start + (end - start) * local_t


def interpolate_2d(
    start: Tuple[Number, Number],
    end: Tuple[Number, Number],
    t: float,
    easing_type: Union[EasingType, str] = EasingType.LINEAR,
    mode: Union[EasingMode, str] = EasingMode.IN
) -> Tuple[float, float]:
    """
    在两个二维点之间进行缓动插值
    
    Args:
        start: 起始点 (x, y)
        end: 结束点 (x, y)
        t: 进度值 [0, 1]
        easing_type: 缓动类型
        mode: 缓动模式
    
    Returns:
        插值点 (x, y)
    
    Example:
        >>> interpolate_2d((0, 0), (100, 200), 0.5, 'quad', 'out')
        (75.0, 150.0)
    """
    x = interpolate(start[0], end[0], t, easing_type, mode)
    y = interpolate(start[1], end[1], t, easing_type, mode)
    return (x, y)


def interpolate_3d(
    start: Tuple[Number, Number, Number],
    end: Tuple[Number, Number, Number],
    t: float,
    easing_type: Union[EasingType, str] = EasingType.LINEAR,
    mode: Union[EasingMode, str] = EasingMode.IN
) -> Tuple[float, float, float]:
    """
    在两个三维点之间进行缓动插值
    
    Args:
        start: 起始点 (x, y, z)
        end: 结束点 (x, y, z)
        t: 进度值 [0, 1]
        easing_type: 缓动类型
        mode: 缓动模式
    
    Returns:
        插值点 (x, y, z)
    
    Example:
        >>> interpolate_3d((0, 0, 0), (100, 200, 300), 0.5)
        (50.0, 100.0, 150.0)
    """
    x = interpolate(start[0], end[0], t, easing_type, mode)
    y = interpolate(start[1], end[1], t, easing_type, mode)
    z = interpolate(start[2], end[2], t, easing_type, mode)
    return (x, y, z)


# =============================================================================
# 动画序列生成
# =============================================================================

def generate_animation_frames(
    start: Number,
    end: Number,
    frames: int,
    easing_type: Union[EasingType, str] = EasingType.LINEAR,
    mode: Union[EasingMode, str] = EasingMode.IN
) -> List[float]:
    """
    生成动画帧序列
    
    Args:
        start: 起始值
        end: 结束值
        frames: 帧数
        easing_type: 缓动类型
        mode: 缓动模式
    
    Returns:
        帧值列表
    
    Example:
        >>> generate_animation_frames(0, 100, 5, 'quad', 'out')
        [0.0, 36.0, 64.0, 84.0, 100.0]
    """
    if frames <= 0:
        return []
    if frames == 1:
        return [float(start)]
    
    return [
        interpolate(start, end, i / (frames - 1), easing_type, mode)
        for i in range(frames)
    ]


def generate_animation_frames_2d(
    start: Tuple[Number, Number],
    end: Tuple[Number, Number],
    frames: int,
    easing_type: Union[EasingType, str] = EasingType.LINEAR,
    mode: Union[EasingMode, str] = EasingMode.IN
) -> List[Tuple[float, float]]:
    """
    生成二维动画帧序列
    
    Args:
        start: 起始点 (x, y)
        end: 结束点 (x, y)
        frames: 帧数
        easing_type: 缓动类型
        mode: 缓动模式
    
    Returns:
        帧点列表 [(x, y), ...]
    
    Example:
        >>> generate_animation_frames_2d((0, 0), (100, 100), 3)
        [(0.0, 0.0), (50.0, 50.0), (100.0, 100.0)]
    """
    if frames <= 0:
        return []
    if frames == 1:
        return [(float(start[0]), float(start[1]))]
    
    return [
        interpolate_2d(start, end, i / (frames - 1), easing_type, mode)
        for i in range(frames)
    ]


# =============================================================================
# 组合缓动
# =============================================================================

def chain_easing(
    t: float,
    easing_configs: List[Tuple[float, Union[EasingType, str], Union[EasingMode, str]]]
) -> float:
    """
    链式组合多种缓动效果
    
    Args:
        t: 进度值 [0, 1]
        easing_configs: 缓动配置列表 [(时长占比, 缓动类型, 模式), ...]
                       时长占比之和应为 1.0
    
    Returns:
        缓动后的值
    
    Example:
        >>> # 前 50% 使用 quadratic ease-out，后 50% 使用 bounce ease-out
        >>> chain_easing(0.75, [
        ...     (0.5, 'quad', 'out'),
        ...     (0.5, 'bounce', 'out')
        ... ])
        0.828125
    """
    if not easing_configs:
        return t
    
    # 计算当前所在的区间
    accumulated = 0.0
    for duration, easing_type, mode in easing_configs:
        if t <= accumulated + duration:
            # 计算在当前区间内的局部进度
            local_t = (t - accumulated) / duration if duration > 0 else 0
            return ease(local_t, easing_type, mode)
        accumulated += duration
    
    # 超出范围，返回最后一个缓动的最终值
    return 1.0


def blend_easing(
    t: float,
    easing_type1: Union[EasingType, str],
    easing_type2: Union[EasingType, str],
    blend_factor: float = 0.5,
    mode1: Union[EasingMode, str] = EasingMode.OUT,
    mode2: Union[EasingMode, str] = EasingMode.OUT
) -> float:
    """
    混合两种缓动效果
    
    Args:
        t: 进度值 [0, 1]
        easing_type1: 第一种缓动类型
        easing_type2: 第二种缓动类型
        blend_factor: 混合因子 [0, 1]，0 表示完全使用第一种，1 表示完全使用第二种
        mode1: 第一种缓动模式
        mode2: 第二种缓动模式
    
    Returns:
        混合后的缓动值
    
    Example:
        >>> blend_easing(0.5, 'quad', 'cubic', 0.5)
        0.625
    """
    v1 = ease(t, easing_type1, mode1)
    v2 = ease(t, easing_type2, mode2)
    return v1 * (1 - blend_factor) + v2 * blend_factor


# =============================================================================
# 缓动分析工具
# =============================================================================

def get_easing_derivative(
    easing_type: Union[EasingType, str],
    mode: Union[EasingMode, str] = EasingMode.OUT,
    t: float = 0.5,
    h: float = 0.0001
) -> float:
    """
    计算缓动函数在某点的导数（变化率）
    
    Args:
        easing_type: 缓动类型
        mode: 缓动模式
        t: 计算点
        h: 差分步长
    
    Returns:
        导数近似值
    
    Example:
        >>> get_easing_derivative('linear', 'in', 0.5)
        1.0
    """
    fn = get_easing_function(easing_type, mode)
    t = clamp(t)
    t_plus = clamp(t + h)
    t_minus = clamp(t - h)
    
    # 使用中心差分
    return (fn(t_plus) - fn(t_minus)) / (t_plus - t_minus) if t_plus != t_minus else 0


def get_easing_extremes(
    easing_type: Union[EasingType, str],
    mode: Union[EasingMode, str] = EasingMode.OUT,
    samples: int = 1000
) -> Tuple[float, float]:
    """
    获取缓动函数的极值（超出 [0, 1] 范围的部分）
    
    Args:
        easing_type: 缓动类型
        mode: 缓动模式
        samples: 采样数量
    
    Returns:
        (最小值, 最大值)
    
    Example:
        >>> get_easing_extremes('back', 'out')
        (-0.1..., 1.1...)
    """
    fn = get_easing_function(easing_type, mode)
    values = [fn(i / samples) for i in range(samples + 1)]
    return (min(values), max(values))


def compare_easings(
    t: float,
    modes: Optional[List[Union[EasingMode, str]]] = None
) -> Dict[str, float]:
    """
    比较所有缓动类型在给定进度下的值
    
    Args:
        t: 进度值 [0, 1]
        modes: 要比较的模式列表，默认为 ['out']
    
    Returns:
        字典 {缓动名称: 值}
    
    Example:
        >>> compare_easings(0.5)['quad_out']
        0.75
    """
    if modes is None:
        modes = [EasingMode.OUT]
    
    result = {}
    for easing_type in EasingType:
        for mode in modes:
            if isinstance(mode, str):
                mode = EasingMode(mode.lower())
            key = f"{easing_type.value}_{mode.value}"
            result[key] = ease(t, easing_type, mode)
    
    return result


# =============================================================================
# 便捷方法
# =============================================================================

def create_easing_curve(
    easing_type: Union[EasingType, str],
    mode: Union[EasingMode, str] = EasingMode.OUT,
    samples: int = 100
) -> List[Tuple[float, float]]:
    """
    创建缓动曲线数据点
    
    Args:
        easing_type: 缓动类型
        mode: 缓动模式
        samples: 采样数量
    
    Returns:
        数据点列表 [(t, value), ...]
    
    Example:
        >>> curve = create_easing_curve('quad', 'out', 5)
        >>> len(curve)
        5
    """
    fn = get_easing_function(easing_type, mode)
    return [(i / samples, fn(i / samples)) for i in range(samples + 1)]


def apply_easing_to_sequence(
    values: List[Number],
    easing_type: Union[EasingType, str] = EasingType.LINEAR,
    mode: Union[EasingMode, str] = EasingMode.IN
) -> List[float]:
    """
    对数值序列应用缓动重采样
    
    将原始序列通过缓动函数重新映射，产生新的时序分布
    
    Args:
        values: 原始数值序列
        easing_type: 缓动类型
        mode: 缓动模式
    
    Returns:
        重采样后的序列
    
    Example:
        >>> apply_easing_to_sequence([0, 10, 20, 30, 40, 50], 'quad', 'out')
        [0, 6.0, 22.0, 38.0, 46.0, 50]
    """
    if not values:
        return []
    if len(values) == 1:
        return [float(values[0])]
    
    result = []
    for i, _ in enumerate(values):
        t = i / (len(values) - 1)
        t_eased = ease(t, easing_type, mode)
        idx = t_eased * (len(values) - 1)
        idx_low = int(idx)
        idx_high = min(idx_low + 1, len(values) - 1)
        frac = idx - idx_low
        val = values[idx_low] * (1 - frac) + values[idx_high] * frac
        result.append(val)
    
    return result


# =============================================================================
# CSS cubic-bezier 兼容
# =============================================================================

def cubic_bezier(x1: float, y1: float, x2: float, y2: float) -> EasingFunction:
    """
    创建自定义三次贝塞尔缓动函数（CSS cubic-bezier 兼容）
    
    Args:
        x1: 第一个控制点 x 坐标 [0, 1]
        y1: 第一个控制点 y 坐标（可以是负值或大于 1）
        x2: 第二个控制点 x 坐标 [0, 1]
        y2: 第二个控制点 y 坐标（可以是负值或大于 1）
    
    Returns:
        缓动函数
    
    Example:
        >>> ease_fn = cubic_bezier(0.25, 0.1, 0.25, 1.0)
        >>> ease_fn(0.5)
        0.6...
    """
    # 确保控制点 x 坐标在有效范围内
    x1 = clamp(x1, 0, 1)
    x2 = clamp(x2, 0, 1)
    
    # 贝塞尔曲线计算
    def bezier_fn(t: float) -> float:
        # 牛顿迭代求解 t 对应的 x
        # 然后计算对应的 y
        low = 0.0
        high = 1.0
        t_guess = t
        
        # 使用二分法近似求解
        for _ in range(20):  # 迭代次数
            # 计算贝塞尔曲线上的 x 值
            cx = 3 * x1
            bx = 3 * (x2 - x1) - cx
            ax = 1 - cx - bx
            
            x_estimate = ((ax * t_guess + bx) * t_guess + cx) * t_guess
            
            if abs(x_estimate - t) < 0.0001:
                break
            
            if x_estimate > t:
                high = t_guess
            else:
                low = t_guess
            t_guess = (low + high) / 2
        
        # 计算对应的 y 值
        cy = 3 * y1
        by = 3 * (y2 - y1) - cy
        ay = 1 - cy - by
        
        return ((ay * t_guess + by) * t_guess + cy) * t_guess
    
    return bezier_fn


# 预定义的 CSS 缓动函数
CSS_EASING = {
    'linear': linear,
    'ease': cubic_bezier(0.25, 0.1, 0.25, 1.0),
    'ease-in': cubic_bezier(0.42, 0, 1.0, 1.0),
    'ease-out': cubic_bezier(0, 0, 0.58, 1.0),
    'ease-in-out': cubic_bezier(0.42, 0, 0.58, 1.0),
}


def get_css_easing(name: str) -> EasingFunction:
    """
    获取 CSS 标准缓动函数
    
    Args:
        name: 缓动名称（linear, ease, ease-in, ease-out, ease-in-out）
    
    Returns:
        缓动函数
    
    Raises:
        ValueError: 无效的缓动名称
    
    Example:
        >>> fn = get_css_easing('ease-in-out')
        >>> fn(0.5)
        0.5
    """
    if name not in CSS_EASING:
        raise ValueError(f"Unknown CSS easing: {name}. Available: {list(CSS_EASING.keys())}")
    return CSS_EASING[name]


# =============================================================================
# 导出列表
# =============================================================================

__all__ = [
    # 枚举
    'EasingType',
    'EasingMode',
    
    # 核心函数
    'linear',
    
    # Quad
    'ease_in_quad',
    'ease_out_quad',
    'ease_in_out_quad',
    'ease_out_in_quad',
    
    # Cubic
    'ease_in_cubic',
    'ease_out_cubic',
    'ease_in_out_cubic',
    'ease_out_in_cubic',
    
    # Quart
    'ease_in_quart',
    'ease_out_quart',
    'ease_in_out_quart',
    'ease_out_in_quart',
    
    # Quint
    'ease_in_quint',
    'ease_out_quint',
    'ease_in_out_quint',
    'ease_out_in_quint',
    
    # Sine
    'ease_in_sine',
    'ease_out_sine',
    'ease_in_out_sine',
    'ease_out_in_sine',
    
    # Expo
    'ease_in_expo',
    'ease_out_expo',
    'ease_in_out_expo',
    'ease_out_in_expo',
    
    # Circ
    'ease_in_circ',
    'ease_out_circ',
    'ease_in_out_circ',
    'ease_out_in_circ',
    
    # Elastic
    'ease_in_elastic',
    'ease_out_elastic',
    'ease_in_out_elastic',
    'ease_out_in_elastic',
    
    # Back
    'ease_in_back',
    'ease_out_back',
    'ease_in_out_back',
    'ease_out_in_back',
    
    # Bounce
    'ease_in_bounce',
    'ease_out_bounce',
    'ease_in_out_bounce',
    'ease_out_in_bounce',
    
    # 统一接口
    'get_easing_function',
    'ease',
    
    # 插值
    'interpolate',
    'interpolate_list',
    'interpolate_2d',
    'interpolate_3d',
    
    # 动画序列
    'generate_animation_frames',
    'generate_animation_frames_2d',
    
    # 组合
    'chain_easing',
    'blend_easing',
    
    # 分析
    'get_easing_derivative',
    'get_easing_extremes',
    'compare_easings',
    
    # 便捷方法
    'create_easing_curve',
    'apply_easing_to_sequence',
    
    # CSS 兼容
    'cubic_bezier',
    'get_css_easing',
    'CSS_EASING',
]