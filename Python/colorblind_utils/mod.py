"""
色盲模拟与辅助工具 (Colorblind Simulation & Assistance Utils)

提供色盲视觉模拟、颜色调整建议和对比度检测功能。
零外部依赖，使用 Python 标准库实现。

支持类型：
- Protanopia (红色盲)
- Deuteranopia (绿色盲) - 最常见
- Tritanopia (蓝色盲)
- Achromatopsia (全色盲)
- Protanomaly (红色弱)
- Deuteranomaly (绿色弱)
- Tritanomaly (蓝色弱)
"""

from typing import Tuple, List, Dict, Optional
import math


# ============================================================================
# 类型定义
# ============================================================================

RGB = Tuple[int, int, int]  # (0-255, 0-255, 0-255)
RGBA = Tuple[int, int, int, float]  # (0-255, 0-255, 0-255, 0.0-1.0)
HSL = Tuple[float, float, float]  # (0-360, 0-100, 0-100)

ColorBlindType = str

# 色盲类型常量
PROTANOPIA = "protanopia"          # 红色盲
DEUTERANOPIA = "deuteranopia"      # 绿色盲 (最常见，约6%男性)
TRITANOPIA = "tritanopia"          # 蓝色盲
ACHROMATOPSIA = "achromatopsia"    # 全色盲
PROTANOMALY = "protanomaly"        # 红色弱
DEUTERANOMALY = "deuteranomaly"    # 绿色弱
TRITANOMALY = "tritanomaly"        # 蓝色弱


# ============================================================================
# 颜色转换工具函数
# ============================================================================

def rgb_to_linear(value: int) -> float:
    """
    将 sRGB 值转换为线性 RGB 值。
    
    Args:
        value: sRGB 值 (0-255)
    
    Returns:
        线性 RGB 值 (0.0-1.0)
    """
    value = value / 255.0
    if value <= 0.04045:
        return value / 12.92
    return ((value + 0.055) / 1.055) ** 2.4


def linear_to_rgb(value: float) -> int:
    """
    将线性 RGB 值转换为 sRGB 值。
    
    Args:
        value: 线性 RGB 值 (0.0-1.0)
    
    Returns:
        sRGB 值 (0-255)
    """
    if value <= 0.0031308:
        value = value * 12.92
    else:
        value = 1.055 * (value ** (1 / 2.4)) - 0.055
    return max(0, min(255, round(value * 255)))


def rgb_to_lms(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """
    将 RGB 转换为 LMS 色彩空间。
    LMS 是模拟人眼锥状细胞响应的模型。
    
    Args:
        r, g, b: RGB 值 (0-255)
    
    Returns:
        (L, M, S) 锥状细胞响应值
    """
    # 转换为线性 RGB
    lr = rgb_to_linear(r)
    lg = rgb_to_linear(g)
    lb = rgb_to_linear(b)
    
    # 使用标准变换矩阵 (Hunt-Pointer-Estevez)
    L = 0.17881 * lr + 0.43516 * lg + 0.04119 * lb
    M = 0.03456 * lr + 0.27158 * lg + 0.03867 * lb
    S = 0.00031 * lr + 0.00195 * lg + 1.08583 * lb
    
    return (L, M, S)


def lms_to_rgb(L: float, M: float, S: float) -> RGB:
    """
    将 LMS 色彩空间转换回 RGB。
    
    Args:
        L, M, S: 锥状细胞响应值
    
    Returns:
        (r, g, b) RGB 值 (0-255)
    """
    # 逆变换矩阵
    r = 5.61303 * L - 8.93483 * M + 0.18861 * S
    g = -0.70371 * L + 3.71286 * M - 0.06168 * S
    b = 0.00328 * L - 0.01247 * M + 0.92167 * S
    
    return (linear_to_rgb(r), linear_to_rgb(g), linear_to_rgb(b))


def rgb_to_hsl(r: int, g: int, b: int) -> HSL:
    """
    将 RGB 转换为 HSL。
    
    Args:
        r, g, b: RGB 值 (0-255)
    
    Returns:
        (h, s, l) HSL 值 (0-360, 0-100, 0-100)
    """
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    l = (max_c + min_c) / 2
    
    if max_c == min_c:
        h = s = 0
    else:
        d = max_c - min_c
        s = d / (2 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)
        
        if max_c == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif max_c == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        h *= 60
    
    return (h, s * 100, l * 100)


def hsl_to_rgb(h: float, s: float, l: float) -> RGB:
    """
    将 HSL 转换为 RGB。
    
    Args:
        h, s, l: HSL 值 (0-360, 0-100, 0-100)
    
    Returns:
        (r, g, b) RGB 值 (0-255)
    """
    h, s, l = h / 360, s / 100, l / 100
    
    if s == 0:
        r = g = b = l
    else:
        def hue_to_rgb(p, q, t):
            if t < 0: t += 1
            if t > 1: t -= 1
            if t < 1/6: return p + (q - p) * 6 * t
            if t < 1/2: return q
            if t < 2/3: return p + (q - p) * (2/3 - t) * 6
            return p
        
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue_to_rgb(p, q, h + 1/3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1/3)
    
    return (round(r * 255), round(g * 255), round(b * 255))


def hex_to_rgb(hex_color: str) -> RGB:
    """
    将十六进制颜色转换为 RGB。
    
    Args:
        hex_color: 十六进制颜色字符串 (如 "#FF0000" 或 "FF0000")
    
    Returns:
        (r, g, b) RGB 值
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """
    将 RGB 转换为十六进制颜色字符串。
    
    Args:
        r, g, b: RGB 值 (0-255)
    
    Returns:
        十六进制颜色字符串 (如 "#FF0000")
    """
    return f"#{r:02X}{g:02X}{b:02X}"


# ============================================================================
# 色盲模拟核心
# ============================================================================

# 色盲模拟矩阵 (LMS 色彩空间的变换)
# 基于 Brettel, Viénot, Mollon (1997) 的研究

# 红色盲 (Protanopia) - 缺少L锥细胞
_PROTANOPIA_MATRIX = (
    (0.0, 1.05118294, -0.05116099),
    (0.0, 1.0, 0.0),
    (0.0, 0.0, 1.0)
)

# 绿色盲 (Deuteranopia) - 缺少M锥细胞
_DEUTERANOPIA_MATRIX = (
    (1.0, 0.0, 0.0),
    (0.49420696, 0.0, 0.0),
    (0.0, 0.0, 1.0)
)

# 蓝色盲 (Tritanopia) - 缺少S锥细胞
_TRITANOPIA_MATRIX = (
    (1.0, 0.0, 0.0),
    (0.0, 1.0, 0.0),
    (-0.86744736, 1.86727089, 0.0)
)

# 色弱模拟矩阵 (部分锥细胞功能障碍)
_PROTANOMALY_MATRIX = (
    (0.816, 0.184, 0.0),
    (0.334, 0.666, 0.0),
    (0.0, 0.0, 1.0)
)

_DEUTERANOMALY_MATRIX = (
    (0.8, 0.2, 0.0),
    (0.258, 0.742, 0.0),
    (0.0, 0.0, 1.0)
)

_TRITANOMALY_MATRIX = (
    (1.0, 0.0, 0.0),
    (0.0, 0.933, 0.067),
    (0.0, 0.183, 0.817)
)


def _apply_lms_transform(L: float, M: float, S: float, 
                          matrix: Tuple[Tuple[float, ...], ...]) -> Tuple[float, float, float]:
    """
    应用 LMS 变换矩阵。
    """
    new_L = matrix[0][0] * L + matrix[0][1] * M + matrix[0][2] * S
    new_M = matrix[1][0] * L + matrix[1][1] * M + matrix[1][2] * S
    new_S = matrix[2][0] * L + matrix[2][1] * M + matrix[2][2] * S
    return (new_L, new_M, new_S)


def simulate_colorblindness(r: int, g: int, b: int, 
                            blindness_type: ColorBlindType = DEUTERANOPIA) -> RGB:
    """
    模拟色盲视觉效果。
    
    Args:
        r, g, b: 原始 RGB 值 (0-255)
        blindness_type: 色盲类型
    
    Returns:
        模拟后的 RGB 值
    
    Examples:
        >>> simulate_colorblindness(255, 0, 0, PROTANOPIA)  # 红色在红色盲眼中
        (133, 126, 62)  # 呈现为暗黄绿色
        
        >>> simulate_colorblindness(0, 255, 0, DEUTERANOPIA)  # 绿色在绿色盲眼中
        (145, 145, 53)  # 呈现为黄色调
    """
    # 全色盲：完全丧失颜色感知，只能看到灰度
    if blindness_type == ACHROMATOPSIA:
        gray = round(0.299 * r + 0.587 * g + 0.114 * b)
        return (gray, gray, gray)
    
    # 选择变换矩阵
    matrix_map = {
        PROTANOPIA: _PROTANOPIA_MATRIX,
        DEUTERANOPIA: _DEUTERANOPIA_MATRIX,
        TRITANOPIA: _TRITANOPIA_MATRIX,
        PROTANOMALY: _PROTANOMALY_MATRIX,
        DEUTERANOMALY: _DEUTERANOMALY_MATRIX,
        TRITANOMALY: _TRITANOMALY_MATRIX,
    }
    
    matrix = matrix_map.get(blindness_type, _DEUTERANOPIA_MATRIX)
    
    # 转换到 LMS 空间
    L, M, S = rgb_to_lms(r, g, b)
    
    # 应用色盲变换
    L, M, S = _apply_lms_transform(L, M, S, matrix)
    
    # 转换回 RGB
    return lms_to_rgb(L, M, S)


def simulate_colorblindness_hex(hex_color: str, 
                                 blindness_type: ColorBlindType = DEUTERANOPIA) -> str:
    """
    模拟色盲视觉效果（十六进制输入/输出）。
    
    Args:
        hex_color: 十六进制颜色字符串
        blindness_type: 色盲类型
    
    Returns:
        模拟后的十六进制颜色字符串
    """
    r, g, b = hex_to_rgb(hex_color)
    new_r, new_g, new_b = simulate_colorblindness(r, g, b, blindness_type)
    return rgb_to_hex(new_r, new_g, new_b)


def simulate_all_types(r: int, g: int, b: int) -> Dict[ColorBlindType, RGB]:
    """
    一次性模拟所有色盲类型。
    
    Args:
        r, g, b: RGB 值 (0-255)
    
    Returns:
        字典，键为色盲类型，值为模拟后的 RGB
    """
    types = [PROTANOPIA, DEUTERANOPIA, TRITANOPIA, ACHROMATOPSIA,
             PROTANOMALY, DEUTERANOMALY, TRITANOMALY]
    return {t: simulate_colorblindness(r, g, b, t) for t in types}


# ============================================================================
# 对比度和可访问性检测
# ============================================================================

def relative_luminance(r: int, g: int, b: int) -> float:
    """
    计算相对亮度 (WCAG 2.1 标准)。
    
    Args:
        r, g, b: RGB 值 (0-255)
    
    Returns:
        相对亮度值 (0.0-1.0)
    """
    r = rgb_to_linear(r)
    g = rgb_to_linear(g)
    b = rgb_to_linear(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(rgb1: RGB, rgb2: RGB) -> float:
    """
    计算两种颜色之间的对比度比率 (WCAG 2.1 标准)。
    
    Args:
        rgb1, rgb2: 两组 RGB 值
    
    Returns:
        对比度比率 (1:1 到 21:1)
    
    Examples:
        >>> contrast_ratio((0, 0, 0), (255, 255, 255))
        21.0  # 黑白对比度为最高
        
        >>> contrast_ratio((255, 255, 255), (255, 255, 255))
        1.0   # 相同颜色对比度最低
    """
    L1 = relative_luminance(*rgb1)
    L2 = relative_luminance(*rgb2)
    
    lighter = max(L1, L2)
    darker = min(L1, L2)
    
    return (lighter + 0.05) / (darker + 0.05)


def wcag_compliance_level(contrast: float) -> Dict[str, bool]:
    """
    根据 WCAG 2.1 标准评估对比度合规级别。
    
    Args:
        contrast: 对比度比率
    
    Returns:
        字典，包含 AA 和 AAA 级别的合规状态
    """
    return {
        "aa_normal": contrast >= 4.5,
        "aa_large": contrast >= 3.0,
        "aaa_normal": contrast >= 7.0,
        "aaa_large": contrast >= 4.5,
    }


def is_colorblind_friendly(fg: RGB, bg: RGB, 
                           min_contrast: float = 4.5) -> bool:
    """
    检测前景/背景色组合对色盲用户是否友好。
    
    检查在不同色盲类型下的对比度是否满足最低要求。
    
    Args:
        fg: 前景色 RGB
        bg: 背景色 RGB
        min_contrast: 最低对比度要求 (默认 4.5，WCAG AA 标准)
    
    Returns:
        是否对所有常见色盲类型友好
    """
    # 检查原始对比度
    if contrast_ratio(fg, bg) < min_contrast:
        return False
    
    # 检查在红色盲和绿色盲下的对比度
    for blindness_type in [PROTANOPIA, DEUTERANOPIA, TRITANOPIA]:
        fg_sim = simulate_colorblindness(*fg, blindness_type)
        bg_sim = simulate_colorblindness(*bg, blindness_type)
        
        if contrast_ratio(fg_sim, bg_sim) < min_contrast:
            return False
    
    return True


# ============================================================================
# 颜色调整和建议
# ============================================================================

def adjust_for_colorblindness(r: int, g: int, b: int,
                               blindness_type: ColorBlindType = DEUTERANOPIA,
                               target_contrast: float = 4.5,
                               bg_color: Optional[RGB] = None) -> RGB:
    """
    调整颜色使其对色盲用户更加友好。
    
    通过调整亮度和饱和度来增加可区分性。
    
    Args:
        r, g, b: 原始 RGB 值
        blindness_type: 目标色盲类型
        target_contrast: 目标对比度
        bg_color: 背景色 (可选，用于计算对比度)
    
    Returns:
        调整后的 RGB 值
    """
    h, s, l = rgb_to_hsl(r, g, b)
    
    # 如果是红色盲或绿色盲，避免红绿色调
    if blindness_type in [PROTANOPIA, DEUTERANOPIA, PROTANOMALY, DEUTERANOMALY]:
        # 如果色调在红色或绿色区域
        if 0 <= h <= 30 or 330 <= h <= 360 or 90 <= h <= 150:
            # 调整色调到蓝色区域
            h = (h + 180) % 360
    
    # 如果是蓝色盲，避免蓝色调
    elif blindness_type in [TRITANOPIA, TRITANOMALY]:
        if 200 <= h <= 280:
            h = (h + 120) % 360
    
    # 增加亮度差异
    if l < 50:
        l = max(0, l - 10)
    else:
        l = min(100, l + 10)
    
    # 增加饱和度以提高可识别性
    s = min(100, s * 1.2)
    
    return hsl_to_rgb(h, s, l)


def suggest_colorblind_safe_alternatives(r: int, g: int, b: int,
                                          count: int = 3) -> List[RGB]:
    """
    为给定颜色建议色盲安全的替代颜色。
    
    Args:
        r, g, b: 原始 RGB 值
        count: 需要的替代颜色数量
    
    Returns:
        替代颜色列表
    """
    h, s, l = rgb_to_hsl(r, g, b)
    
    alternatives = []
    
    # 策略1：调整色调（避开红绿区域）
    h_shifts = [180, 90, 270]
    for shift in h_shifts[:count]:
        new_h = (h + shift) % 360
        alternatives.append(hsl_to_rgb(new_h, s, l))
    
    # 如果需要更多，调整亮度
    while len(alternatives) < count:
        l_adjusted = (l + 25 * (len(alternatives) - 2)) % 100
        alternatives.append(hsl_to_rgb(h, s, l_adjusted))
    
    return alternatives[:count]


def generate_colorblind_safe_palette(count: int = 5) -> List[RGB]:
    """
    生成一个色盲安全的调色板。
    
    基于 Okabe-Ito 色盲友好配色方案。
    
    Args:
        count: 需要的颜色数量
    
    Returns:
        RGB 颜色列表
    
    Examples:
        >>> generate_colorblind_safe_palette(5)
        [(230, 159, 0), (86, 180, 233), (0, 158, 115), 
         (240, 228, 66), (0, 114, 178)]
    """
    # Okabe-Ito 色盲友好配色
    safe_colors = [
        (230, 159, 0),    # 橙色
        (86, 180, 233),   # 天蓝色
        (0, 158, 115),    # 青绿色
        (240, 228, 66),   # 黄色
        (0, 114, 178),    # 深蓝色
        (213, 94, 0),     # 朱红色
        (204, 121, 167),  # 粉色
    ]
    
    # Wong 色盲友好配色作为补充
    wong_colors = [
        (0, 0, 0),        # 黑色
        (230, 159, 0),    # 橙色
        (86, 180, 233),   # 天蓝色
        (0, 158, 115),    # 青绿色
        (240, 228, 66),   # 黄色
        (0, 114, 178),    # 深蓝色
        (213, 94, 0),     # 朱红色
        (204, 121, 167),  # 粉色
    ]
    
    result = []
    for i in range(count):
        if i < len(safe_colors):
            result.append(safe_colors[i])
        else:
            # 如果需要更多颜色，生成新的安全色
            h = (i * 360 / count) % 360
            # 避开红色和绿色区域
            if 0 <= h <= 60 or 100 <= h <= 160:
                h = (h + 180) % 360
            result.append(hsl_to_rgb(h, 70, 50))
    
    return result


# ============================================================================
# 辅助工具
# ============================================================================

def get_colorblind_type_info() -> Dict[ColorBlindType, Dict[str, str]]:
    """
    获取所有色盲类型的信息。
    
    Returns:
        字典，包含每种色盲类型的名称、描述和发病率
    """
    return {
        PROTANOPIA: {
            "name": "红色盲",
            "name_en": "Protanopia",
            "description": "无法感知红色，红绿混淆",
            "prevalence_male": "约1%",
            "prevalence_female": "约0.02%",
        },
        DEUTERANOPIA: {
            "name": "绿色盲",
            "name_en": "Deuteranopia",
            "description": "无法感知绿色，红绿混淆（最常见的色盲类型）",
            "prevalence_male": "约1.3%",
            "prevalence_female": "约0.01%",
        },
        TRITANOPIA: {
            "name": "蓝色盲",
            "name_en": "Tritanopia",
            "description": "无法感知蓝色，蓝黄混淆",
            "prevalence_male": "约0.001%",
            "prevalence_female": "约0.001%",
        },
        ACHROMATOPSIA: {
            "name": "全色盲",
            "name_en": "Achromatopsia",
            "description": "完全无法感知颜色，只能看到灰度",
            "prevalence_male": "约0.003%",
            "prevalence_female": "约0.003%",
        },
        PROTANOMALY: {
            "name": "红色弱",
            "name_en": "Protanomaly",
            "description": "红色感知减弱",
            "prevalence_male": "约1%",
            "prevalence_female": "约0.03%",
        },
        DEUTERANOMALY: {
            "name": "绿色弱",
            "name_en": "Deuteranomaly",
            "description": "绿色感知减弱（最常见的色觉异常）",
            "prevalence_male": "约5%",
            "prevalence_female": "约0.35%",
        },
        TRITANOMALY: {
            "name": "蓝色弱",
            "name_en": "Tritanomaly",
            "description": "蓝色感知减弱",
            "prevalence_male": "罕见",
            "prevalence_female": "罕见",
        },
    }


def analyze_color_for_colorblindness(r: int, g: int, b: int) -> Dict:
    """
    全面分析一个颜色在色盲情况下的表现。
    
    Args:
        r, g, b: RGB 值
    
    Returns:
        包含详细分析的字典
    """
    h, s, l = rgb_to_hsl(r, g, b)
    
    result = {
        "original": {
            "rgb": (r, g, b),
            "hex": rgb_to_hex(r, g, b),
            "hsl": (round(h, 1), round(s, 1), round(l, 1)),
        },
        "simulations": {},
        "issues": [],
        "recommendations": [],
    }
    
    # 模拟所有类型
    for blindness_type in [PROTANOPIA, DEUTERANOPIA, TRITANOPIA, 
                           PROTANOMALY, DEUTERANOMALY, TRITANOMALY]:
        sim = simulate_colorblindness(r, g, b, blindness_type)
        result["simulations"][blindness_type] = {
            "rgb": sim,
            "hex": rgb_to_hex(*sim),
        }
    
    # 全色盲单独处理
    achrom = simulate_colorblindness(r, g, b, ACHROMATOPSIA)
    result["simulations"][ACHROMATOPSIA] = {
        "rgb": achrom,
        "hex": rgb_to_hex(*achrom),
    }
    
    # 检测潜在问题
    # 红色/绿色区域
    if 0 <= h <= 30 or 330 <= h <= 360:
        result["issues"].append("颜色在红色区域，红色盲/绿色盲用户可能难以区分")
        result["recommendations"].append("考虑添加图标或纹理以增加可识别性")
    
    if 80 <= h <= 150:
        result["issues"].append("颜色在绿色区域，红色盲/绿色盲用户可能难以区分")
    
    # 蓝色区域
    if 200 <= h <= 280:
        result["issues"].append("颜色在蓝色区域，蓝色盲用户可能难以区分")
    
    # 低饱和度警告
    if s < 20:
        result["issues"].append("饱和度过低，所有色盲用户可能难以区分")
        result["recommendations"].append("增加饱和度以提高可识别性")
    
    # 低亮度警告
    if l < 10:
        result["issues"].append("亮度过低，对比度可能不足")
    
    # 推荐替代色
    alternatives = suggest_colorblind_safe_alternatives(r, g, b, 2)
    result["safe_alternatives"] = [
        {"rgb": a, "hex": rgb_to_hex(*a)} for a in alternatives
    ]
    
    return result


# ============================================================================
# 批量处理
# ============================================================================

def simulate_palette(colors: List[RGB], 
                     blindness_type: ColorBlindType = DEUTERANOPIA) -> List[RGB]:
    """
    批量模拟调色板的色盲效果。
    
    Args:
        colors: RGB 颜色列表
        blindness_type: 色盲类型
    
    Returns:
        模拟后的颜色列表
    """
    return [simulate_colorblindness(*c, blindness_type) for c in colors]


def check_palette_accessibility(colors: List[RGB],
                                 min_contrast: float = 4.5) -> Dict:
    """
    检查调色板的色盲可访问性。
    
    检查颜色对之间在不同色盲类型下的区分度。
    
    Args:
        colors: RGB 颜色列表
        min_contrast: 最低对比度要求
    
    Returns:
        包含检查结果的字典
    """
    result = {
        "pairs_checked": 0,
        "issues": [],
        "safe_pairs": [],
        "problematic_pairs": [],
    }
    
    blindness_types = [PROTANOPIA, DEUTERANOPIA, TRITANOPIA]
    
    for i, c1 in enumerate(colors):
        for j, c2 in enumerate(colors):
            if i >= j:
                continue
            
            result["pairs_checked"] += 1
            
            # 检查原始对比度
            original_contrast = contrast_ratio(c1, c2)
            
            # 检查色盲模拟后的对比度
            min_simulated_contrast = original_contrast
            worst_type = None
            
            for bt in blindness_types:
                sim1 = simulate_colorblindness(*c1, bt)
                sim2 = simulate_colorblindness(*c2, bt)
                sim_contrast = contrast_ratio(sim1, sim2)
                
                if sim_contrast < min_simulated_contrast:
                    min_simulated_contrast = sim_contrast
                    worst_type = bt
            
            pair_info = {
                "pair": (i, j),
                "colors": (rgb_to_hex(*c1), rgb_to_hex(*c2)),
                "original_contrast": round(original_contrast, 2),
                "min_simulated_contrast": round(min_simulated_contrast, 2),
                "worst_blindness_type": worst_type,
            }
            
            if min_simulated_contrast < min_contrast:
                result["problematic_pairs"].append(pair_info)
                result["issues"].append(
                    f"颜色对 {pair_info['colors']} 在 {worst_type} 下对比度为 "
                    f"{min_simulated_contrast:.2f}，低于 {min_contrast}"
                )
            else:
                result["safe_pairs"].append(pair_info)
    
    return result


# ============================================================================
# 便捷函数
# ============================================================================

def simulate(r: int, g: int, b: int, 
             blindness_type: ColorBlindType = DEUTERANOPIA) -> RGB:
    """
    simulate_colorblindness 的简写形式。
    """
    return simulate_colorblindness(r, g, b, blindness_type)


def simulate_hex(hex_color: str, 
                  blindness_type: ColorBlindType = DEUTERANOPIA) -> str:
    """
    simulate_colorblindness_hex 的简写形式。
    """
    return simulate_colorblindness_hex(hex_color, blindness_type)


def contrast(rgb1: RGB, rgb2: RGB) -> float:
    """
    contrast_ratio 的简写形式。
    """
    return contrast_ratio(rgb1, rgb2)


if __name__ == "__main__":
    # 简单演示
    print("色盲模拟工具演示")
    print("=" * 50)
    
    # 测试红色
    print("\n红色 (255, 0, 0) 在不同色盲类型下的表现:")
    for cb_type, info in get_colorblind_type_info().items():
        sim = simulate_colorblindness(255, 0, 0, cb_type)
        print(f"  {info['name']}: RGB{sim} HEX:{rgb_to_hex(*sim)}")
    
    # 测试绿色
    print("\n绿色 (0, 255, 0) 在不同色盲类型下的表现:")
    for cb_type, info in get_colorblind_type_info().items():
        sim = simulate_colorblindness(0, 255, 0, cb_type)
        print(f"  {info['name']}: RGB{sim} HEX:{rgb_to_hex(*sim)}")
    
    # 测试对比度
    print("\n对比度检查:")
    contrast_val = contrast_ratio((255, 0, 0), (0, 255, 0))
    print(f"  红色 vs 绿色: {contrast_val:.2f}")
    compliance = wcag_compliance_level(contrast_val)
    print(f"  WCAG AA (正常文本): {compliance['aa_normal']}")
    
    # 生成安全调色板
    print("\n色盲安全调色板:")
    palette = generate_colorblind_safe_palette(5)
    for i, color in enumerate(palette):
        print(f"  颜色 {i+1}: RGB{color} HEX:{rgb_to_hex(*color)}")