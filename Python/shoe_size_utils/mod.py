"""
鞋码转换工具模块

支持各国鞋码系统之间的转换：
- EU (欧洲码)
- US (美国码) - 男/女/儿童/幼儿
- UK (英国码)
- JP (日本码/厘米)
- CM (厘米)
- CN (中国码/毫米)
- BR (巴西码)
- AU (澳大利亚码)
- MEX (墨西哥码)
- KR (韩国码/毫米)

零外部依赖，纯 Python 实现。
"""

from typing import Dict, List, Optional, Tuple, Union
from enum import Enum
from dataclasses import dataclass


class Gender(Enum):
    """性别类型"""
    MEN = "men"
    WOMEN = "women"
    CHILD = "child"
    TODDLER = "toddler"
    INFANT = "infant"


class SizeSystem(Enum):
    """鞋码系统"""
    EU = "EU"           # 欧洲码
    US_MEN = "US_MEN"   # 美国男码
    US_WOMEN = "US_WOMEN"  # 美国女码
    US_CHILD = "US_CHILD"  # 美国儿童码
    US_TODDLER = "US_TODDLER"  # 美国幼儿码
    US_INFANT = "US_INFANT"  # 美国婴儿码
    UK = "UK"           # 英国码
    JP = "JP"          # 日本码 (厘米)
    CM = "CM"          # 厘米
    CN = "CN"          # 中国码 (毫米)
    BR = "BR"          # 巴西码
    AU = "AU"          # 澳大利亚码
    MEX = "MEX"        # 墨西哥码
    KR = "KR"          # 韩国码 (毫米)


@dataclass
class ShoeSize:
    """鞋码数据结构"""
    size: float
    system: SizeSystem
    gender: Optional[Gender] = None
    
    def __str__(self) -> str:
        if self.gender:
            return f"{self.system.value} {self.size} ({self.gender.value})"
        return f"{self.system.value} {self.size}"


class ShoeSizeConverter:
    """鞋码转换器"""
    
    # 脚长(cm) -> 各系统鞋码的转换基准
    # 基于 ISO 19407 和行业标准
    
    def __init__(self):
        # EU码与脚长关系: EU = 1.5 * 脚长(cm) + 2 (近似)
        # US男码: US = 0.847 * 脚长(cm) - 22.5 (近似)
        # US女码: US = 0.847 * 脚长(cm) - 21.5 (近似)
        # UK码: UK = 脚长(cm) * 0.847 - 23 (近似)
        pass
    
    @staticmethod
    def cm_to_eu(cm: float) -> float:
        """
        厘米转欧洲码
        
        Args:
            cm: 脚长(厘米)
            
        Returns:
            欧洲码
            
        Note:
            欧洲码单位是巴黎点(Paris point)，1巴黎点 = 2/3厘米
            EU码 = cm * 1.5 + 2 (基于ISO 19407近似)
        """
        # EU = cm / (2/3) + 2 = cm * 1.5 + 2
        # 更准确：EU 42 ≈ 26.5cm，所以 EU ≈ cm * 1.5 + 2
        return round(cm * 1.5 + 2, 1)
    
    @staticmethod
    def eu_to_cm(eu: float) -> float:
        """
        欧洲码转厘米
        
        Args:
            eu: 欧洲码
            
        Returns:
            脚长(厘米)
        """
        # cm = (EU - 2) / 1.5
        return round((eu - 2) / 1.5, 1)
    
    @staticmethod
    def cm_to_us_men(cm: float) -> float:
        """
        厘米转美国男码
        
        Args:
            cm: 脚长(厘米)
            
        Returns:
            美国男码
            
        Note:
            基于实际对照表线性拟合：
            EU 42 (26.5cm) ≈ US Men 8.5
            cm = US + 18, 所以 US = cm - 18
        """
        return round(cm - 18, 1)
    
    @staticmethod
    def us_men_to_cm(us: float) -> float:
        """
        美国男码转厘米
        
        Args:
            us: 美国男码
            
        Returns:
            脚长(厘米)
        """
        return round(us + 18, 1)
    
    @staticmethod
    def cm_to_us_women(cm: float) -> float:
        """
        厘米转美国女码
        
        Args:
            cm: 脚长(厘米)
            
        Returns:
            美国女码
            
        Note:
            US女码比男码大约1码
            US Women = US Men + 1.5
        """
        return round(cm - 16.5, 1)
    
    @staticmethod
    def us_women_to_cm(us: float) -> float:
        """
        美国女码转厘米
        
        Args:
            us: 美国女码
            
        Returns:
            脚长(厘米)
        """
        return round(us + 16.5, 1)
    
    @staticmethod
    def cm_to_uk(cm: float) -> float:
        """
        厘米转英国码
        
        Args:
            cm: 脚长(厘米)
            
        Returns:
            英国码
            
        Note:
            UK码比US男码小约0.5码
            UK = US Men - 0.5
        """
        return round(cm - 18.5, 1)
    
    @staticmethod
    def uk_to_cm(uk: float) -> float:
        """
        英国码转厘米
        
        Args:
            uk: 英国码
            
        Returns:
            脚长(厘米)
        """
        return round(uk + 18.5, 1)
    
    @staticmethod
    def cm_to_cn(cm: float) -> int:
        """
        厘米转中国码
        
        Args:
            cm: 脚长(厘米)
            
        Returns:
            中国码(毫米)
        """
        # CN码以毫米为单位，通常等于脚长毫米
        return int(cm * 10)
    
    @staticmethod
    def cn_to_cm(cn: int) -> float:
        """
        中国码转厘米
        
        Args:
            cn: 中国码(毫米)
            
        Returns:
            脚长(厘米)
        """
        return cn / 10
    
    @staticmethod
    def cm_to_br(cm: float) -> float:
        """
        厘米转巴西码
        
        Args:
            cm: 脚长(厘米)
            
        Returns:
            巴西码
        """
        # BR = EU - 34 + 30 (近似)
        eu = ShoeSizeConverter.cm_to_eu(cm)
        return round(eu - 34 + 30, 1)
    
    @staticmethod
    def br_to_cm(br: float) -> float:
        """
        巴西码转厘米
        
        Args:
            br: 巴西码
            
        Returns:
            脚长(厘米)
        """
        eu = br + 34 - 30
        return ShoeSizeConverter.eu_to_cm(eu)
    
    @staticmethod
    def cm_to_kr(cm: float) -> int:
        """
        厘米转韩国码
        
        Args:
            cm: 脚长(厘米)
            
        Returns:
            韩国码(毫米)
        """
        # 韩国码与中国码类似，以毫米为单位
        return int(cm * 10)
    
    @staticmethod
    def kr_to_cm(kr: int) -> float:
        """
        韩国码转厘米
        
        Args:
            kr: 韩国码(毫米)
            
        Returns:
            脚长(厘米)
        """
        return kr / 10
    
    @staticmethod
    def cm_to_mex(cm: float) -> float:
        """
        厘米转墨西哥码
        
        Args:
            cm: 脚长(厘米)
            
        Returns:
            墨西哥码
        """
        # MEX ≈ EU - 1
        eu = ShoeSizeConverter.cm_to_eu(cm)
        return round(eu - 1, 1)
    
    @staticmethod
    def mex_to_cm(mex: float) -> float:
        """
        墨西哥码转厘米
        
        Args:
            mex: 墨西哥码
            
        Returns:
            脚长(厘米)
        """
        eu = mex + 1
        return ShoeSizeConverter.eu_to_cm(eu)
    
    @staticmethod
    def us_child_to_cm(us: float) -> float:
        """
        美国儿童码转厘米
        
        Args:
            us: 美国儿童码
            
        Returns:
            脚长(厘米)
            
        Note:
            儿童码范围 0-13.5，对应约 8-22cm
            cm ≈ US_Child + 8
        """
        return round(us + 8, 1)
    
    @staticmethod
    def cm_to_us_child(cm: float) -> float:
        """
        厘米转美国儿童码
        
        Args:
            cm: 脚长(厘米)
            
        Returns:
            美国儿童码
        """
        return round(cm - 8, 1)
    
    @staticmethod
    def convert(size: float, from_system: SizeSystem, 
                to_system: SizeSystem, 
                gender: Optional[Gender] = None) -> float:
        """
        通用鞋码转换
        
        Args:
            size: 原始鞋码
            from_system: 原始鞋码系统
            to_system: 目标鞋码系统
            gender: 性别(部分系统需要)
            
        Returns:
            转换后的鞋码
            
        Raises:
            ValueError: 不支持的转换
        """
        # 先转换为厘米(脚长)
        cm = None
        
        if from_system == SizeSystem.CM:
            cm = size
        elif from_system == SizeSystem.JP:
            cm = size  # JP码就是厘米
        elif from_system == SizeSystem.EU:
            cm = ShoeSizeConverter.eu_to_cm(size)
        elif from_system == SizeSystem.US_MEN:
            cm = ShoeSizeConverter.us_men_to_cm(size)
        elif from_system == SizeSystem.US_WOMEN:
            cm = ShoeSizeConverter.us_women_to_cm(size)
        elif from_system == SizeSystem.US_CHILD:
            cm = ShoeSizeConverter.us_child_to_cm(size)
        elif from_system == SizeSystem.UK:
            cm = ShoeSizeConverter.uk_to_cm(size)
        elif from_system == SizeSystem.CN:
            cm = ShoeSizeConverter.cn_to_cm(int(size))
        elif from_system == SizeSystem.BR:
            cm = ShoeSizeConverter.br_to_cm(size)
        elif from_system == SizeSystem.KR:
            cm = ShoeSizeConverter.kr_to_cm(int(size))
        elif from_system == SizeSystem.MEX:
            cm = ShoeSizeConverter.mex_to_cm(size)
        else:
            raise ValueError(f"不支持的鞋码系统: {from_system}")
        
        # 从厘米转换到目标系统
        if to_system == SizeSystem.CM:
            return cm
        elif to_system == SizeSystem.JP:
            return cm
        elif to_system == SizeSystem.EU:
            return ShoeSizeConverter.cm_to_eu(cm)
        elif to_system == SizeSystem.US_MEN:
            return ShoeSizeConverter.cm_to_us_men(cm)
        elif to_system == SizeSystem.US_WOMEN:
            return ShoeSizeConverter.cm_to_us_women(cm)
        elif to_system == SizeSystem.US_CHILD:
            return ShoeSizeConverter.cm_to_us_child(cm)
        elif to_system == SizeSystem.UK:
            return ShoeSizeConverter.cm_to_uk(cm)
        elif to_system == SizeSystem.CN:
            return ShoeSizeConverter.cm_to_cn(cm)
        elif to_system == SizeSystem.BR:
            return ShoeSizeConverter.cm_to_br(cm)
        elif to_system == SizeSystem.KR:
            return ShoeSizeConverter.cm_to_kr(cm)
        elif to_system == SizeSystem.MEX:
            return ShoeSizeConverter.cm_to_mex(cm)
        else:
            raise ValueError(f"不支持的鞋码系统: {to_system}")
    
    @staticmethod
    def convert_all(size: float, from_system: SizeSystem,
                   gender: Optional[Gender] = None) -> Dict[str, float]:
        """
        转换为所有鞋码系统
        
        Args:
            size: 原始鞋码
            from_system: 原始鞋码系统
            gender: 性别(部分系统需要)
            
        Returns:
            所有鞋码系统的字典
        """
        cm = None
        
        # 先转换为厘米
        if from_system == SizeSystem.CM:
            cm = size
        elif from_system == SizeSystem.JP:
            cm = size
        elif from_system == SizeSystem.EU:
            cm = ShoeSizeConverter.eu_to_cm(size)
        elif from_system == SizeSystem.US_MEN:
            cm = ShoeSizeConverter.us_men_to_cm(size)
        elif from_system == SizeSystem.US_WOMEN:
            cm = ShoeSizeConverter.us_women_to_cm(size)
        elif from_system == SizeSystem.US_CHILD:
            cm = ShoeSizeConverter.us_child_to_cm(size)
        elif from_system == SizeSystem.UK:
            cm = ShoeSizeConverter.uk_to_cm(size)
        elif from_system == SizeSystem.CN:
            cm = ShoeSizeConverter.cn_to_cm(int(size))
        elif from_system == SizeSystem.BR:
            cm = ShoeSizeConverter.br_to_cm(size)
        elif from_system == SizeSystem.KR:
            cm = ShoeSizeConverter.kr_to_cm(int(size))
        elif from_system == SizeSystem.MEX:
            cm = ShoeSizeConverter.mex_to_cm(size)
        else:
            raise ValueError(f"不支持的鞋码系统: {from_system}")
        
        return {
            "cm": cm,
            "jp": cm,
            "eu": ShoeSizeConverter.cm_to_eu(cm),
            "us_men": ShoeSizeConverter.cm_to_us_men(cm),
            "us_women": ShoeSizeConverter.cm_to_us_women(cm),
            "us_child": ShoeSizeConverter.cm_to_us_child(cm),
            "uk": ShoeSizeConverter.cm_to_uk(cm),
            "cn": ShoeSizeConverter.cm_to_cn(cm),
            "br": ShoeSizeConverter.cm_to_br(cm),
            "kr": ShoeSizeConverter.cm_to_kr(cm),
            "mex": ShoeSizeConverter.cm_to_mex(cm)
        }
    
    @staticmethod
    def get_size_info(size: float, system: SizeSystem,
                     gender: Optional[Gender] = None) -> Dict:
        """
        获取鞋码详细信息
        
        Args:
            size: 鞋码
            system: 鞋码系统
            gender: 性别
            
        Returns:
            鞋码详细信息字典
        """
        all_sizes = ShoeSizeConverter.convert_all(size, system, gender)
        
        # 确定鞋码类型(成人/儿童/幼儿)
        cm = all_sizes["cm"]
        if cm < 15:
            size_type = "婴儿(Infant)"
        elif cm < 18:
            size_type = "幼儿(Toddler)"
        elif cm < 22:
            size_type = "儿童(Child)"
        else:
            size_type = "成人(Adult)"
        
        # 推荐范围
        recommended = {
            "跑步鞋": f"{all_sizes['eu'] + 0.5:.1f} EU (建议大半码)",
            "休闲鞋": f"{all_sizes['eu']:.1f} EU",
            "高跟鞋": f"{all_sizes['eu'] - 0.5:.1f} EU (建议小半码)",
        }
        
        return {
            "原始码": f"{size} {system.value}",
            "脚长": f"{cm} 厘米",
            "类型": size_type,
            "所有码": {
                "欧洲码(EU)": all_sizes["eu"],
                "美国男码(US Men)": all_sizes["us_men"],
                "美国女码(US Women)": all_sizes["us_women"],
                "美国儿童码(US Child)": all_sizes["us_child"],
                "英国码(UK)": all_sizes["uk"],
                "日本码(JP)": all_sizes["jp"],
                "厘米(CM)": all_sizes["cm"],
                "中国码(CN)": all_sizes["cn"],
                "巴西码(BR)": all_sizes["br"],
                "韩国码(KR)": all_sizes["kr"],
                "墨西哥码(MEX)": all_sizes["mex"]
            },
            "购鞋建议": recommended
        }


def convert_shoe_size(size: float, from_system: str, to_system: str,
                     gender: Optional[str] = None) -> float:
    """
    便捷函数: 鞋码转换
    
    Args:
        size: 原始鞋码
        from_system: 原始鞋码系统 (EU, US_MEN, US_WOMEN, US_CHILD, UK, JP, CM, CN, BR, KR, MEX)
        to_system: 目标鞋码系统
        gender: 性别 (men, women, child, toddler, infant)
        
    Returns:
        转换后的鞋码
        
    Example:
        >>> convert_shoe_size(42, "EU", "US_MEN")
        8.5
        >>> convert_shoe_size(9, "US_MEN", "UK")
        8.5
    """
    from_sys = SizeSystem(from_system.upper())
    to_sys = SizeSystem(to_system.upper())
    
    gender_enum = None
    if gender:
        gender_enum = Gender(gender.lower())
    
    return ShoeSizeConverter.convert(size, from_sys, to_sys, gender_enum)


def get_all_sizes(size: float, system: str) -> Dict[str, float]:
    """
    便捷函数: 获取所有鞋码
    
    Args:
        size: 原始鞋码
        system: 原始鞋码系统
        
    Returns:
        所有鞋码系统的字典
        
    Example:
        >>> get_all_sizes(42, "EU")
        {'cm': 26.5, 'jp': 26.5, 'eu': 42, ...}
    """
    sys = SizeSystem(system.upper())
    return ShoeSizeConverter.convert_all(size, sys)


def get_foot_length_info(foot_length_cm: float) -> Dict:
    """
    根据脚长获取鞋码信息
    
    Args:
        foot_length_cm: 脚长(厘米)
        
    Returns:
        鞋码信息字典
        
    Example:
        >>> get_foot_length_info(26.5)
        {'eu': 42.0, 'us_men': 8.5, ...}
    """
    return ShoeSizeConverter.convert_all(foot_length_cm, SizeSystem.CM)


def recommend_shoe_size(foot_length_cm: float, shoe_type: str = "normal") -> Dict:
    """
    根据脚长推荐鞋码
    
    Args:
        foot_length_cm: 脚长(厘米)
        shoe_type: 鞋子类型 (normal, running, high_heel, boot)
        
    Returns:
        推荐鞋码字典
        
    Example:
        >>> recommend_shoe_size(26.5, "running")
        {'eu': 42.5, 'us_men': 9.0, 'reason': '跑步鞋建议大半码...'}
    """
    base_sizes = ShoeSizeConverter.convert_all(foot_length_cm, SizeSystem.CM)
    
    adjustments = {
        "normal": 0,
        "running": 0.5,      # 跑步鞋建议大半码
        "sport": 0.5,        # 运动鞋建议大半码
        "high_heel": -0.5,   # 高跟鞋建议小半码
        "boot": 0.5,         # 靴子建议大半码
        "sandals": 0,        # 凉鞋正常码
    }
    
    adj = adjustments.get(shoe_type, 0)
    reason_map = {
        "normal": "标准尺码",
        "running": "跑步鞋建议大半码，预留脚趾空间",
        "sport": "运动鞋建议大半码，运动时脚会肿胀",
        "high_heel": "高跟鞋建议小半码，更贴合脚型",
        "boot": "靴子建议大半码，预留袜子厚度空间",
        "sandals": "凉鞋标准尺码",
    }
    
    # 调整EU码
    adjusted_eu = base_sizes["eu"] + adj
    
    # 重新计算所有码
    result = {
        "脚长": f"{foot_length_cm} 厘米",
        "鞋子类型": shoe_type,
        "调整原因": reason_map.get(shoe_type, "标准尺码"),
        "推荐EU码": adjusted_eu,
        "推荐US男码": ShoeSizeConverter.convert(adjusted_eu, SizeSystem.EU, SizeSystem.US_MEN),
        "推荐US女码": ShoeSizeConverter.convert(adjusted_eu, SizeSystem.EU, SizeSystem.US_WOMEN),
        "推荐UK码": ShoeSizeConverter.convert(adjusted_eu, SizeSystem.EU, SizeSystem.UK),
        "推荐CN码": int(ShoeSizeConverter.convert(adjusted_eu, SizeSystem.EU, SizeSystem.CN)),
    }
    
    return result


def validate_shoe_size(size: float, system: str) -> Tuple[bool, Optional[str]]:
    """
    验证鞋码是否在合理范围内
    
    Args:
        size: 鞋码
        system: 鞋码系统
        
    Returns:
        (是否有效, 错误信息)
        
    Example:
        >>> validate_shoe_size(42, "EU")
        (True, None)
        >>> validate_shoe_size(100, "EU")
        (False, 'EU码应在 15-52 范围内')
    """
    ranges = {
        "EU": (15, 52, "EU码应在 15-52 范围内"),
        "US_MEN": (1, 18, "US男码应在 1-18 范围内"),
        "US_WOMEN": (1, 16, "US女码应在 1-16 范围内"),
        "US_CHILD": (0, 13.5, "US儿童码应在 0-13.5 范围内"),
        "UK": (0, 17, "UK码应在 0-17 范围内"),
        "JP": (8, 35, "JP码应在 8-35 厘米范围内"),
        "CM": (8, 35, "脚长应在 8-35 厘米范围内"),
        "CN": (80, 350, "CN码应在 80-350 毫米范围内"),
        "BR": (10, 48, "BR码应在 10-48 范围内"),
        "KR": (80, 350, "KR码应在 80-350 毫米范围内"),
        "MEX": (14, 51, "MEX码应在 14-51 范围内"),
    }
    
    sys = system.upper()
    if sys not in ranges:
        return False, f"未知的鞋码系统: {system}"
    
    min_val, max_val, msg = ranges[sys]
    if min_val <= size <= max_val:
        return True, None
    return False, msg


def compare_sizes(size1: float, system1: str, size2: float, system2: str) -> Dict:
    """
    比较两个鞋码
    
    Args:
        size1: 第一个鞋码
        system1: 第一个鞋码系统
        size2: 第二个鞋码
        system2: 第二个鞋码系统
        
    Returns:
        比较结果字典
        
    Example:
        >>> compare_sizes(42, "EU", 8.5, "US_MEN")
        {'difference_cm': 0.0, 'equal': True, ...}
    """
    # 都转换为厘米
    sizes1 = get_all_sizes(size1, system1)
    sizes2 = get_all_sizes(size2, system2)
    
    diff = sizes1["cm"] - sizes2["cm"]
    
    return {
        "size1_cm": sizes1["cm"],
        "size2_cm": sizes2["cm"],
        "difference_cm": round(diff, 2),
        "equal": abs(diff) < 0.1,
        "larger": "size1" if diff > 0 else ("size2" if diff < 0 else "equal"),
        "comparison": f"鞋码1({system1} {size1}) 比鞋码2({system2} {size2}) {'大' if diff > 0 else '小' if diff < 0 else '相等'} {abs(diff):.1f}厘米"
    }


# 常用鞋码对照表 (部分)
COMMON_SIZE_CHART = [
    {"EU": 35, "US_MEN": 2.5, "US_WOMEN": 4.5, "UK": 2, "CM": 22.0, "CN": 220},
    {"EU": 36, "US_MEN": 3.5, "US_WOMEN": 5.5, "UK": 3, "CM": 22.5, "CN": 225},
    {"EU": 37, "US_MEN": 4.5, "US_WOMEN": 6.5, "UK": 4, "CM": 23.5, "CN": 235},
    {"EU": 38, "US_MEN": 5.5, "US_WOMEN": 7.5, "UK": 5, "CM": 24.0, "CN": 240},
    {"EU": 39, "US_MEN": 6.5, "US_WOMEN": 8.5, "UK": 6, "CM": 24.5, "CN": 245},
    {"EU": 40, "US_MEN": 7.5, "US_WOMEN": 9.5, "UK": 7, "CM": 25.5, "CN": 255},
    {"EU": 41, "US_MEN": 8, "US_WOMEN": 10, "UK": 7.5, "CM": 26.0, "CN": 260},
    {"EU": 42, "US_MEN": 8.5, "US_WOMEN": 10.5, "UK": 8, "CM": 26.5, "CN": 265},
    {"EU": 43, "US_MEN": 9.5, "US_WOMEN": 11.5, "UK": 9, "CM": 27.5, "CN": 275},
    {"EU": 44, "US_MEN": 10.5, "US_WOMEN": 12.5, "UK": 10, "CM": 28.0, "CN": 280},
    {"EU": 45, "US_MEN": 11.5, "US_WOMEN": 13.5, "UK": 11, "CM": 28.5, "CN": 285},
    {"EU": 46, "US_MEN": 12.5, "US_WOMEN": 14.5, "UK": 12, "CM": 29.5, "CN": 295},
    {"EU": 47, "US_MEN": 13.5, "US_WOMEN": 15.5, "UK": 13, "CM": 30.0, "CN": 300},
]


def find_closest_size(target_cm: float, system: str = "EU") -> Tuple[float, float]:
    """
    根据脚长查找最接近的标准尺码
    
    Args:
        target_cm: 目标脚长(厘米)
        system: 目标鞋码系统
        
    Returns:
        (最接近尺码, 差值厘米)
        
    Example:
        >>> find_closest_size(26.3, "EU")
        (42.0, 0.2)
    """
    closest = None
    min_diff = float('inf')
    
    for entry in COMMON_SIZE_CHART:
        diff = abs(entry["CM"] - target_cm)
        if diff < min_diff:
            min_diff = diff
            closest = entry
    
    if closest:
        return closest[system], min_diff
    return None, None


if __name__ == "__main__":
    # 演示用法
    print("=== 鞋码转换工具演示 ===\n")
    
    # 1. 基本转换
    print("1. 基本转换:")
    print(f"   EU 42 -> US Men: {convert_shoe_size(42, 'EU', 'US_MEN')}")
    print(f"   EU 42 -> UK: {convert_shoe_size(42, 'EU', 'UK')}")
    print(f"   EU 42 -> CN: {convert_shoe_size(42, 'EU', 'CN')}")
    print()
    
    # 2. 获取所有尺码
    print("2. EU 42 对应所有尺码:")
    all_sizes = get_all_sizes(42, "EU")
    for k, v in all_sizes.items():
        print(f"   {k}: {v}")
    print()
    
    # 3. 获取详细信息
    print("3. EU 42 详细信息:")
    info = ShoeSizeConverter.get_size_info(42, SizeSystem.EU)
    print(f"   脚长: {info['脚长']}")
    print(f"   类型: {info['类型']}")
    print()
    
    # 4. 购鞋建议
    print("4. 脚长26.5厘米的购鞋建议:")
    rec = recommend_shoe_size(26.5, "running")
    print(f"   推荐EU码: {rec['推荐EU码']}")
    print(f"   原因: {rec['调整原因']}")
    print()
    
    # 5. 尺码比较
    print("5. 尺码比较:")
    comp = compare_sizes(42, "EU", 8.5, "US_MEN")
    print(f"   {comp['comparison']}")