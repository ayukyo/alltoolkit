"""
Clothing Size Utils - 国际服装尺码转换工具

提供服装尺码的国际标准转换功能，支持：
- 上装（上衣、夹克、毛衣等）
- 下装（裤子、裙子等）
- 鞋子
- 内衣（文胸）
- 配饰（帽子、手套、戒指等）

零外部依赖，纯 Python 实现。
"""

from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum


class SizeRegion(Enum):
    """尺码地区标准"""
    CN = "中国"      # 中国
    US = "美国"      # 美国
    EU = "欧洲"      # 欧洲
    UK = "英国"      # 英国
    JP = "日本"      # 日本
    KR = "韩国"      # 韩国
    AU = "澳洲"      # 澳大利亚
    IT = "意大利"    # 意大利
    FR = "法国"      # 法国
    DE = "德国"      # 德国


class ClothingType(Enum):
    """服装类型"""
    TOP = "上装"          # 上衣、T恤、衬衫、夹克等
    DRESS = "连衣裙"      # 连衣裙
    PANTS = "裤装"        # 裤子
    SKIRT = "裙装"        # 裙子
    SHOES = "鞋子"        # 鞋子
    BRA = "文胸"          # 文胸
    HAT = "帽子"          # 帽子
    GLOVES = "手套"       # 手套
    RING = "戒指"         # 戒指
    BELT = "腰带"         # 腰带
    SOCKS = "袜子"        # 袜子


@dataclass
class SizeInfo:
    """尺码信息"""
    label: str           # 尺码标签 (S/M/L/XL 或数字)
    bust_min: float      # 胸围最小值 (cm)
    bust_max: float      # 胸围最大值 (cm)
    waist_min: float     # 腰围最小值 (cm)
    waist_max: float     # 腰围最大值 (cm)
    hip_min: float       # 臀围最小值 (cm)
    hip_max: float       # 臀围最大值 (cm)
    description: str = "" # 额外描述


@dataclass
class ShoeSize:
    """鞋码信息"""
    cn: float           # 中国码
    us_men: float       # 美国男码
    us_women: float     # 美国女码
    uk: float           # 英国码
    eu: float           # 欧洲码
    jp: float           # 日本码
    cm: float           # 脚长 (cm)


# ==================== 上装尺码表 ====================
# 基于国际通用标准

TOP_SIZE_CN = {
    "XS": SizeInfo("XS", 76, 80, 60, 64, 82, 86, "特小号"),
    "S": SizeInfo("S", 80, 84, 64, 68, 86, 90, "小号"),
    "M": SizeInfo("M", 84, 88, 68, 72, 90, 94, "中号"),
    "L": SizeInfo("L", 88, 92, 72, 76, 94, 98, "大号"),
    "XL": SizeInfo("XL", 92, 96, 76, 80, 98, 102, "加大号"),
    "XXL": SizeInfo("XXL", 96, 100, 80, 84, 102, 106, "特大号"),
    "XXXL": SizeInfo("XXXL", 100, 104, 84, 88, 106, 110, "超大号"),
}

TOP_SIZE_US = {
    "XS": SizeInfo("XS", 78, 82, 62, 66, 84, 88, "US Extra Small"),
    "S": SizeInfo("S", 82, 86, 66, 70, 88, 92, "US Small"),
    "M": SizeInfo("M", 86, 90, 70, 74, 92, 96, "US Medium"),
    "L": SizeInfo("L", 90, 94, 74, 78, 96, 100, "US Large"),
    "XL": SizeInfo("XL", 94, 98, 78, 82, 100, 104, "US Extra Large"),
    "XXL": SizeInfo("XXL", 98, 102, 82, 86, 104, 108, "US 2X Large"),
}

TOP_SIZE_EU = {
    "XS": SizeInfo("34", 78, 82, 62, 66, 84, 88, "EU 34"),
    "S": SizeInfo("36", 82, 86, 66, 70, 88, 92, "EU 36"),
    "M": SizeInfo("38", 86, 90, 70, 74, 92, 96, "EU 38"),
    "L": SizeInfo("40", 90, 94, 74, 78, 96, 100, "EU 40"),
    "XL": SizeInfo("42", 94, 98, 78, 82, 100, 104, "EU 42"),
    "XXL": SizeInfo("44", 98, 102, 82, 86, 104, 108, "EU 44"),
    "XXXL": SizeInfo("46", 102, 106, 86, 90, 108, 112, "EU 46"),
}

TOP_SIZE_UK = {
    "XS": SizeInfo("6", 78, 82, 62, 66, 84, 88, "UK 6"),
    "S": SizeInfo("8", 82, 86, 66, 70, 88, 92, "UK 8"),
    "M": SizeInfo("10", 86, 90, 70, 74, 92, 96, "UK 10"),
    "L": SizeInfo("12", 90, 94, 74, 78, 96, 100, "UK 12"),
    "XL": SizeInfo("14", 94, 98, 78, 82, 100, 104, "UK 14"),
    "XXL": SizeInfo("16", 98, 102, 82, 86, 104, 108, "UK 16"),
}

# 上装尺码映射 (中国基准)
TOP_SIZE_MAPPING = {
    SizeRegion.CN: {"XS": "XS", "S": "S", "M": "M", "L": "L", "XL": "XL", "XXL": "XXL", "XXXL": "XXXL"},
    SizeRegion.US: {"XS": "XS", "S": "S", "M": "M", "L": "L", "XL": "XL", "XXL": "XXL"},
    SizeRegion.EU: {"XS": "34", "S": "36", "M": "38", "L": "40", "XL": "42", "XXL": "44", "XXXL": "46"},
    SizeRegion.UK: {"XS": "6", "S": "8", "M": "10", "L": "12", "XL": "14", "XXL": "16"},
    SizeRegion.JP: {"XS": "5", "S": "7", "M": "9", "L": "11", "XL": "13", "XXL": "15"},
    SizeRegion.KR: {"XS": "44", "S": "55", "M": "66", "L": "77", "XL": "88", "XXL": "99"},
}

# ==================== 下装尺码表 ====================

PANTS_SIZE_CN = {
    "S": SizeInfo("S", 74, 78, 60, 64, 84, 88, "小号"),
    "M": SizeInfo("M", 78, 82, 64, 68, 88, 92, "中号"),
    "L": SizeInfo("L", 82, 86, 68, 72, 92, 96, "大号"),
    "XL": SizeInfo("XL", 86, 90, 72, 76, 96, 100, "加大号"),
    "XXL": SizeInfo("XXL", 90, 94, 76, 80, 100, 104, "特大号"),
}

# 裤装尺码映射 (腰围为基准，单位cm)
PANTS_SIZE_MAPPING = {
    SizeRegion.CN: {64: "S", 68: "M", 72: "L", 76: "XL", 80: "XXL"},
    SizeRegion.US: {64: "0", 68: "2", 72: "4", 76: "6", 80: "8"},
    SizeRegion.EU: {64: "34", 68: "36", 72: "38", 76: "40", 80: "42"},
    SizeRegion.UK: {64: "4", 68: "6", 72: "8", 76: "10", 80: "12"},
    SizeRegion.JP: {64: "5", 68: "7", 72: "9", 76: "11", 80: "13"},
}

# ==================== 鞋码表 ====================
# 基于ISO 19407标准和常用对照

SHOE_SIZES: List[ShoeSize] = [
    # 女鞋尺码
    ShoeSize(cn=34, us_men=3.5, us_women=5, uk=2.5, eu=35, jp=21.5, cm=21.5),
    ShoeSize(cn=35, us_men=4, us_women=5.5, uk=3, eu=36, jp=22, cm=22),
    ShoeSize(cn=36, us_men=5, us_women=6.5, uk=4, eu=37, jp=23, cm=23),
    ShoeSize(cn=37, us_men=5.5, us_women=7, uk=4.5, eu=37.5, jp=23.5, cm=23.5),
    ShoeSize(cn=38, us_men=6, us_women=7.5, uk=5, eu=38, jp=24, cm=24),
    ShoeSize(cn=39, us_men=6.5, us_women=8, uk=5.5, eu=39, jp=24.5, cm=24.5),
    ShoeSize(cn=40, us_men=7, us_women=8.5, uk=6, eu=40, jp=25, cm=25),
    ShoeSize(cn=41, us_men=8, us_women=9.5, uk=7, eu=41, jp=26, cm=26),
    ShoeSize(cn=42, us_men=9, us_women=10.5, uk=8, eu=42, jp=27, cm=27),
    ShoeSize(cn=43, us_men=10, us_women=11.5, uk=9, eu=43, jp=28, cm=28),
    ShoeSize(cn=44, us_men=11, us_women=12.5, uk=10, eu=44, jp=29, cm=29),
    ShoeSize(cn=45, us_men=12, us_women=13.5, uk=11, eu=45, jp=30, cm=30),
    ShoeSize(cn=46, us_men=13, us_women=14.5, uk=12, eu=46, jp=31, cm=31),
]

# ==================== 文胸尺码表 ====================
# 下胸围(cm) + 罩杯 = 文胸尺码

BRA_BAND_SIZES = {
    65: ("60-65", "65"),
    70: ("65-70", "70"),
    75: ("70-75", "75"),
    80: ("75-80", "80"),
    85: ("80-85", "85"),
    90: ("85-90", "90"),
    95: ("90-95", "95"),
    100: ("95-100", "100"),
}

# 罩杯对应胸围差 (上胸围 - 下胸围)
CUP_SIZES = {
    "AA": (0, 10, "约10cm差"),
    "A": (10, 12.5, "约10-12.5cm差"),
    "B": (12.5, 15, "约12.5-15cm差"),
    "C": (15, 17.5, "约15-17.5cm差"),
    "D": (17.5, 20, "约17.5-20cm差"),
    "E": (20, 22.5, "约20-22.5cm差"),
    "F": (22.5, 25, "约22.5-25cm差"),
    "G": (25, 27.5, "约25-27.5cm差"),
    "H": (27.5, 30, "约27.5-30cm差"),
}

# 文胸尺码地区转换
BRA_SIZE_MAPPING = {
    SizeRegion.CN: "CN/JP",
    SizeRegion.US: "US",
    SizeRegion.UK: "UK",
    SizeRegion.EU: "EU",
    SizeRegion.AU: "AU",
}

# 不同地区的下胸围基准
BRA_BAND_REGION = {
    SizeRegion.CN: {65: 65, 70: 70, 75: 75, 80: 80, 85: 85, 90: 90, 95: 95},
    SizeRegion.US: {65: 30, 70: 32, 75: 34, 80: 36, 85: 38, 90: 40, 95: 42},
    SizeRegion.UK: {65: 30, 70: 32, 75: 34, 80: 36, 85: 38, 90: 40, 95: 42},
    SizeRegion.EU: {65: 65, 70: 70, 75: 75, 80: 80, 85: 85, 90: 90, 95: 95},
    SizeRegion.AU: {65: 8, 70: 10, 75: 12, 80: 14, 85: 16, 90: 18, 95: 20},
}

# 罩杯转换 (CN/JP为基准)
CUP_REGION_MAPPING = {
    SizeRegion.CN: {"A": "A", "B": "B", "C": "C", "D": "D", "E": "E", "F": "F", "G": "G", "H": "H"},
    SizeRegion.US: {"A": "A", "B": "B", "C": "C", "D": "D", "E": "DD", "F": "DDD", "G": "G", "H": "H"},
    SizeRegion.UK: {"A": "A", "B": "B", "C": "C", "D": "D", "E": "DD", "F": "E", "G": "F", "H": "FF"},
    SizeRegion.EU: {"A": "A", "B": "B", "C": "C", "D": "D", "E": "E", "F": "F", "G": "G", "H": "H"},
    SizeRegion.AU: {"A": "A", "B": "B", "C": "C", "D": "D", "E": "DD", "F": "E", "G": "F", "H": "G"},
}

# ==================== 配饰尺码表 ====================

# 帽子尺码 (头围cm)
HAT_SIZES = {
    SizeRegion.CN: {54: "S", 56: "M", 58: "L", 60: "XL"},
    SizeRegion.US: {54: "6-3/4", 56: "7", 58: "7-1/4", 60: "7-1/2"},
    SizeRegion.EU: {54: "XS", 56: "S", 58: "M", 60: "L"},
    SizeRegion.UK: {54: "6-5/8", 56: "6-7/8", 58: "7-1/8", 60: "7-3/8"},
}

# 戒指尺码 (内周长mm)
RING_SIZES = {
    SizeRegion.CN: {49: "10", 52: "12", 54: "14", 57: "16", 60: "18", 63: "20"},
    SizeRegion.US: {49: "5", 52: "6", 54: "7", 57: "8", 60: "9", 63: "10"},
    SizeRegion.EU: {49: "49", 52: "52", 54: "54", 57: "57", 60: "60", 63: "63"},
    SizeRegion.UK: {49: "J", 52: "L", 54: "N", 57: "P", 60: "R", 63: "T"},
}

# 手套尺码 (手掌周长cm)
GLOVE_SIZES = {
    SizeRegion.CN: {17: "S", 19: "M", 21: "L", 23: "XL"},
    SizeRegion.US: {17: "6.5", 19: "7.5", 21: "8.5", 23: "9.5"},
    SizeRegion.EU: {17: "6", 19: "7", 21: "8", 23: "9"},
    SizeRegion.UK: {17: "XS", 19: "S", 21: "M", 23: "L"},
}

# 腰带尺码 (腰围cm)
BELT_SIZES = {
    SizeRegion.CN: {65: "65", 70: "70", 75: "75", 80: "80", 85: "85", 90: "90"},
    SizeRegion.US: {65: "26", 70: "28", 75: "30", 80: "32", 85: "34", 90: "36"},
    SizeRegion.EU: {65: "65", 70: "70", 75: "75", 80: "80", 85: "85", 90: "90"},
    SizeRegion.UK: {65: "26", 70: "28", 75: "30", 80: "32", 85: "34", 90: "36"},
}


# ==================== 核心转换函数 ====================

def convert_top_size(size: str, from_region: SizeRegion, to_region: SizeRegion) -> Optional[str]:
    """
    转换上装尺码
    
    Args:
        size: 原始尺码 (如 "M", "38", "10")
        from_region: 原始地区标准
        to_region: 目标地区标准
    
    Returns:
        转换后的尺码，如果无法转换则返回 None
    
    Example:
        >>> convert_top_size("M", SizeRegion.CN, SizeRegion.EU)
        '38'
        >>> convert_top_size("38", SizeRegion.EU, SizeRegion.US)
        'M'
    """
    # 规范化输入
    size = size.upper().strip()
    
    # 构建反向映射
    from_mapping = TOP_SIZE_MAPPING.get(from_region, {})
    reverse_from = {v.upper(): k for k, v in from_mapping.items()}
    
    # 查找标准尺码
    standard_size = None
    for std, region_size in from_mapping.items():
        if region_size.upper() == size:
            standard_size = std
            break
    
    if standard_size is None:
        # 尝试反向查找
        standard_size = reverse_from.get(size)
    
    if standard_size is None:
        return None
    
    # 转换到目标地区
    to_mapping = TOP_SIZE_MAPPING.get(to_region, {})
    return to_mapping.get(standard_size)


def convert_pants_size(waist_cm: float, to_region: SizeRegion) -> Optional[str]:
    """
    根据腰围转换裤装尺码
    
    Args:
        waist_cm: 腰围 (厘米)
        to_region: 目标地区标准
    
    Returns:
        对应地区的尺码
    
    Example:
        >>> convert_pants_size(68, SizeRegion.US)
        '2'
        >>> convert_pants_size(72, SizeRegion.EU)
        '38'
    """
    mapping = PANTS_SIZE_MAPPING.get(to_region, {})
    
    # 找到最接近的尺码
    sizes = sorted(mapping.keys())
    for waist in sizes:
        if waist_cm <= waist:
            return mapping[waist]
    
    # 超出范围，返回最大尺码
    return mapping.get(sizes[-1])


def convert_shoe_size(
    size: float, 
    from_region: SizeRegion, 
    to_region: SizeRegion,
    gender: str = "unisex"
) -> Optional[float]:
    """
    转换鞋码
    
    Args:
        size: 原始鞋码
        from_region: 原始地区标准
        to_region: 目标地区标准
        gender: 性别 ("men", "women", "unisex")
    
    Returns:
        转换后的鞋码
    
    Example:
        >>> convert_shoe_size(38, SizeRegion.CN, SizeRegion.US, "women")
        7.5
        >>> convert_shoe_size(8, SizeRegion.US, SizeRegion.EU, "men")
        41
    """
    # 找到匹配的鞋码记录
    for shoe in SHOE_SIZES:
        match = False
        if from_region == SizeRegion.CN and shoe.cn == size:
            match = True
        elif from_region == SizeRegion.EU and shoe.eu == size:
            match = True
        elif from_region == SizeRegion.UK and shoe.uk == size:
            match = True
        elif from_region == SizeRegion.JP and shoe.jp == size:
            match = True
        elif from_region == SizeRegion.US:
            if gender == "men" and shoe.us_men == size:
                match = True
            elif gender == "women" and shoe.us_women == size:
                match = True
        
        if match:
            if to_region == SizeRegion.CN:
                return shoe.cn
            elif to_region == SizeRegion.EU:
                return shoe.eu
            elif to_region == SizeRegion.UK:
                return shoe.uk
            elif to_region == SizeRegion.JP:
                return shoe.jp
            elif to_region == SizeRegion.US:
                return shoe.us_women if gender == "women" else shoe.us_men
    
    return None


def convert_shoe_size_by_cm(foot_length_cm: float) -> Optional[float]:
    """
    根据脚长获取推荐的中国鞋码
    
    Args:
        foot_length_cm: 脚长 (厘米)
    
    Returns:
        推荐的中国鞋码
    
    Example:
        >>> convert_shoe_size_by_cm(25.0)
        40
    """
    for shoe in SHOE_SIZES:
        if foot_length_cm <= shoe.cm:
            return shoe.cn
    return None


def calculate_bra_size(
    underbust: float, 
    overbust: float,
    to_region: SizeRegion = SizeRegion.CN
) -> str:
    """
    计算文胸尺码
    
    Args:
        underbust: 下胸围 (厘米)
        overbust: 上胸围 (厘米)
        to_region: 目标地区标准
    
    Returns:
        文胸尺码 (如 "75B")
    
    Example:
        >>> calculate_bra_size(75, 88, SizeRegion.CN)
        '75B'
        >>> calculate_bra_size(75, 88, SizeRegion.US)
        '34B'
    """
    # 计算胸围差
    diff = overbust - underbust
    
    # 确定罩杯
    cup = "A"
    for cup_name, (min_diff, max_diff, _) in CUP_SIZES.items():
        if min_diff <= diff < max_diff:
            cup = cup_name
            break
    else:
        if diff >= 30:
            cup = "H"
        elif diff < 10:
            cup = "AA"
    
    # 确定下胸围尺码
    band = 70  # 默认
    for band_cm in sorted(BRA_BAND_SIZES.keys()):
        if underbust <= band_cm + 2.5:
            band = band_cm
            break
    else:
        band = 100  # 最大
    
    # 转换到目标地区
    band_mapping = BRA_BAND_REGION.get(to_region, BRA_BAND_REGION[SizeRegion.CN])
    cup_mapping = CUP_REGION_MAPPING.get(to_region, CUP_REGION_MAPPING[SizeRegion.CN])
    
    regional_band = band_mapping.get(band, band)
    regional_cup = cup_mapping.get(cup, cup)
    
    return f"{regional_band}{regional_cup}"


def recommend_size_by_measurements(
    bust: float,
    waist: float,
    hip: float,
    clothing_type: ClothingType = ClothingType.TOP,
    region: SizeRegion = SizeRegion.CN
) -> Dict[str, any]:
    """
    根据三围推荐服装尺码
    
    Args:
        bust: 胸围 (厘米)
        waist: 腰围 (厘米)
        hip: 臀围 (厘米)
        clothing_type: 服装类型
        region: 目标地区标准
    
    Returns:
        推荐尺码信息，包含尺码和详细数据
    
    Example:
        >>> recommend_size_by_measurements(88, 72, 94, ClothingType.TOP, SizeRegion.CN)
        {'size': 'L', 'bust_fit': True, 'waist_fit': True, ...}
    """
    result = {
        "size": None,
        "bust_fit": False,
        "waist_fit": False,
        "hip_fit": False,
        "recommendation": None,
        "measurements": {
            "bust": bust,
            "waist": waist,
            "hip": hip
        }
    }
    
    # 根据服装类型选择尺码表
    if clothing_type in [ClothingType.TOP, ClothingType.DRESS]:
        size_table = TOP_SIZE_CN
    elif clothing_type in [ClothingType.PANTS, ClothingType.SKIRT]:
        size_table = PANTS_SIZE_CN
    else:
        size_table = TOP_SIZE_CN
    
    # 查找匹配的尺码
    matched_sizes = []
    for size_label, size_info in size_table.items():
        bust_fit = size_info.bust_min <= bust <= size_info.bust_max
        waist_fit = size_info.waist_min <= waist <= size_info.waist_max
        hip_fit = size_info.hip_min <= hip <= size_info.hip_max
        
        if bust_fit or waist_fit or hip_fit:
            matched_sizes.append({
                "size": size_label,
                "bust_fit": bust_fit,
                "waist_fit": waist_fit,
                "hip_fit": hip_fit,
                "score": sum([bust_fit, waist_fit, hip_fit])
            })
    
    if matched_sizes:
        # 按匹配分数排序
        matched_sizes.sort(key=lambda x: (-x["score"], x["size"]))
        best = matched_sizes[0]
        result["size"] = best["size"]
        result["bust_fit"] = best["bust_fit"]
        result["waist_fit"] = best["waist_fit"]
        result["hip_fit"] = best["hip_fit"]
        
        if best["score"] == 3:
            result["recommendation"] = f"尺码 {best['size']} 完美适合"
        elif best["score"] == 2:
            result["recommendation"] = f"推荐尺码 {best['size']}，部分尺寸可能略紧或略松"
        else:
            result["recommendation"] = f"建议试穿 {best['size']} 或选择定制"
    
    return result


def get_size_chart(clothing_type: ClothingType, region: SizeRegion) -> Dict[str, Dict]:
    """
    获取指定类型和地区的尺码表
    
    Args:
        clothing_type: 服装类型
        region: 地区标准
    
    Returns:
        尺码表字典
    
    Example:
        >>> chart = get_size_chart(ClothingType.TOP, SizeRegion.CN)
        >>> 'M' in chart
        True
    """
    if clothing_type == ClothingType.SHOES:
        result = {}
        for shoe in SHOE_SIZES:
            result[str(int(shoe.cn))] = {
                "cn": shoe.cn,
                "us_men": shoe.us_men,
                "us_women": shoe.us_women,
                "uk": shoe.uk,
                "eu": shoe.eu,
                "jp": shoe.jp,
                "cm": shoe.cm
            }
        return result
    
    elif clothing_type == ClothingType.BRA:
        return {
            "bands": BRA_BAND_SIZES,
            "cups": CUP_SIZES
        }
    
    elif clothing_type in [ClothingType.TOP, ClothingType.DRESS]:
        return TOP_SIZE_MAPPING.get(region, TOP_SIZE_MAPPING[SizeRegion.CN])
    
    elif clothing_type in [ClothingType.PANTS, ClothingType.SKIRT]:
        return PANTS_SIZE_MAPPING.get(region, PANTS_SIZE_MAPPING[SizeRegion.CN])
    
    elif clothing_type == ClothingType.HAT:
        return HAT_SIZES.get(region, HAT_SIZES[SizeRegion.CN])
    
    elif clothing_type == ClothingType.RING:
        return RING_SIZES.get(region, RING_SIZES[SizeRegion.CN])
    
    elif clothing_type == ClothingType.GLOVES:
        return GLOVE_SIZES.get(region, GLOVE_SIZES[SizeRegion.CN])
    
    elif clothing_type == ClothingType.BELT:
        return BELT_SIZES.get(region, BELT_SIZES[SizeRegion.CN])
    
    return {}


def list_all_regions() -> List[str]:
    """列出所有支持的地区"""
    return [region.value for region in SizeRegion]


def list_all_clothing_types() -> List[str]:
    """列出所有支持的服装类型"""
    return [ct.value for ct in ClothingType]


def quick_size_guide(measurements: Dict[str, float]) -> Dict[str, str]:
    """
    快速尺码指南 - 根据测量值返回各类型服装的推荐尺码
    
    Args:
        measurements: 包含 bust, waist, hip, foot_length 等测量值
    
    Returns:
        各类型服装的推荐尺码
    
    Example:
        >>> quick_size_guide({"bust": 88, "waist": 72, "hip": 94, "foot_length": 25})
        {'top': 'L', 'pants': 'L', 'shoes': '40', 'bra': '75B'}
    """
    result = {}
    
    if "bust" in measurements and "waist" in measurements:
        top_rec = recommend_size_by_measurements(
            measurements.get("bust", 0),
            measurements.get("waist", 0),
            measurements.get("hip", 0),
            ClothingType.TOP
        )
        result["top"] = top_rec.get("size", "Unknown")
    
    if "waist" in measurements and "hip" in measurements:
        pants_rec = recommend_size_by_measurements(
            measurements.get("bust", 0),
            measurements.get("waist", 0),
            measurements.get("hip", 0),
            ClothingType.PANTS
        )
        result["pants"] = pants_rec.get("size", "Unknown")
    
    if "foot_length" in measurements:
        shoe_size = convert_shoe_size_by_cm(measurements["foot_length"])
        if shoe_size:
            result["shoes"] = str(int(shoe_size))
    
    if "underbust" in measurements and "overbust" in measurements:
        bra_size = calculate_bra_size(
            measurements["underbust"],
            measurements["overbust"]
        )
        result["bra"] = bra_size
    
    return result


if __name__ == "__main__":
    # 简单测试
    print("=== 上装尺码转换 ===")
    print(f"CN M -> EU: {convert_top_size('M', SizeRegion.CN, SizeRegion.EU)}")
    print(f"CN M -> US: {convert_top_size('M', SizeRegion.CN, SizeRegion.US)}")
    print(f"CN M -> UK: {convert_top_size('M', SizeRegion.CN, SizeRegion.UK)}")
    
    print("\n=== 裤装尺码转换 ===")
    print(f"腰围68cm -> US: {convert_pants_size(68, SizeRegion.US)}")
    print(f"腰围72cm -> EU: {convert_pants_size(72, SizeRegion.EU)}")
    
    print("\n=== 鞋码转换 ===")
    print(f"CN 38 -> US Women: {convert_shoe_size(38, SizeRegion.CN, SizeRegion.US, 'women')}")
    print(f"脚长25cm -> CN: {convert_shoe_size_by_cm(25)}")
    
    print("\n=== 文胸尺码计算 ===")
    print(f"下胸围75cm, 上胸围88cm: {calculate_bra_size(75, 88, SizeRegion.CN)}")
    print(f"下胸围75cm, 上胸围88cm (US): {calculate_bra_size(75, 88, SizeRegion.US)}")
    
    print("\n=== 尺码推荐 ===")
    rec = recommend_size_by_measurements(88, 72, 94, ClothingType.TOP, SizeRegion.CN)
    print(f"胸围88, 腰围72, 臀围94: {rec}")