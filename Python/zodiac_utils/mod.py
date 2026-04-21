"""
Zodiac Utilities - 星座计算工具模块

提供西方星座和中国生肖的完整计算功能，包括星座判断、特性分析、兼容性计算等。
零依赖，仅使用 Python 标准库。

Author: AllToolkit
Version: 1.0.0
"""

from datetime import datetime, date
from typing import Optional, Union, List, Dict, Tuple, Any
from enum import Enum


class Element(Enum):
    """星座元素（四象）"""
    FIRE = "火象"
    EARTH = "土象"
    AIR = "风象"
    WATER = "水象"


class Quality(Enum):
    """星座属性（三方）"""
    CARDINAL = "基本宫"
    FIXED = "固定宫"
    MUTABLE = "变动宫"


class Zodiac:
    """星座枚举"""
    ARIES = "白羊座"
    TAURUS = "金牛座"
    GEMINI = "双子座"
    CANCER = "巨蟹座"
    LEO = "狮子座"
    VIRGO = "处女座"
    LIBRA = "天秤座"
    SCORPIO = "天蝎座"
    SAGITTARIUS = "射手座"
    CAPRICORN = "摩羯座"
    AQUARIUS = "水瓶座"
    PISCES = "双鱼座"


class ChineseZodiac:
    """中国生肖枚举"""
    RAT = "鼠"
    OX = "牛"
    TIGER = "虎"
    RABBIT = "兔"
    DRAGON = "龙"
    SNAKE = "蛇"
    HORSE = "马"
    GOAT = "羊"
    MONKEY = "猴"
    ROOSTER = "鸡"
    DOG = "狗"
    PIG = "猪"


# 星座数据：名称 -> (开始月日, 结束月日, 元素, 属性, 守护星, 幸运数字, 幸运颜色, 性格关键词)
_ZODIAC_DATA: Dict[str, Tuple[Tuple[int, int], Tuple[int, int], Element, Quality, str, List[int], List[str], List[str]]] = {
    Zodiac.ARIES: ((3, 21), (4, 19), Element.FIRE, Quality.CARDINAL, "火星", [1, 9], ["红色", "橙色"], ["热情", "勇敢", "直率", "冲动"]),
    Zodiac.TAURUS: ((4, 20), (5, 20), Element.EARTH, Quality.FIXED, "金星", [2, 6], ["绿色", "粉色"], ["稳重", "务实", "耐心", "固执"]),
    Zodiac.GEMINI: ((5, 21), (6, 21), Element.AIR, Quality.MUTABLE, "水星", [3, 5], ["黄色", "浅蓝"], ["聪明", "善变", "好奇", "机智"]),
    Zodiac.CANCER: ((6, 22), (7, 22), Element.WATER, Quality.CARDINAL, "月亮", [2, 7], ["银色", "白色"], ["敏感", "顾家", "温柔", "情绪化"]),
    Zodiac.LEO: ((7, 23), (8, 22), Element.FIRE, Quality.FIXED, "太阳", [1, 5], ["金色", "橙色"], ["自信", "慷慨", "领导力", "自负"]),
    Zodiac.VIRGO: ((8, 23), (9, 22), Element.EARTH, Quality.MUTABLE, "水星", [5, 6], ["灰色", "米色"], ["细心", "完美主义", "分析力", "挑剔"]),
    Zodiac.LIBRA: ((9, 23), (10, 23), Element.AIR, Quality.CARDINAL, "金星", [6, 9], ["粉色", "蓝色"], ["优雅", "公正", "社交力", "犹豫"]),
    Zodiac.SCORPIO: ((10, 24), (11, 22), Element.WATER, Quality.FIXED, "冥王星", [8, 0], ["深红", "黑色"], ["神秘", "洞察力", "专注", "记仇"]),
    Zodiac.SAGITTARIUS: ((11, 23), (12, 21), Element.FIRE, Quality.MUTABLE, "木星", [3, 9], ["紫色", "蓝色"], ["乐观", "自由", "冒险", "粗心"]),
    Zodiac.CAPRICORN: ((12, 22), (1, 19), Element.EARTH, Quality.CARDINAL, "土星", [4, 8], ["黑色", "棕色"], ["务实", "有责任感", "自律", "悲观"]),
    Zodiac.AQUARIUS: ((1, 20), (2, 18), Element.AIR, Quality.FIXED, "天王星", [4, 7], ["蓝色", "银色"], ["独立", "创新", "人道主义", "叛逆"]),
    Zodiac.PISCES: ((2, 19), (3, 20), Element.WATER, Quality.MUTABLE, "海王星", [7, 12], ["海蓝", "紫色"], ["浪漫", "富有同情心", "直觉强", "逃避"]),
}

# 中国生肖数据：地支对应
_CHINESE_ZODIAC_ORDER = [
    ChineseZodiac.RAT, ChineseZodiac.OX, ChineseZodiac.TIGER, ChineseZodiac.RABBIT,
    ChineseZodiac.DRAGON, ChineseZodiac.SNAKE, ChineseZodiac.HORSE, ChineseZodiac.GOAT,
    ChineseZodiac.MONKEY, ChineseZodiac.ROOSTER, ChineseZodiac.DOG, ChineseZodiac.PIG
]

# 五行数据
_WUXING = ["金", "木", "水", "火", "土"]

# 星座兼容性矩阵（基于元素和属性）
_COMPATIBILITY_MATRIX: Dict[str, Dict[str, int]] = {
    # 同元素：高兼容；同属性但有冲突：中等；其他：低
    Zodiac.ARIES: {Zodiac.LEO: 95, Zodiac.SAGITTARIUS: 95, Zodiac.GEMINI: 80, Zodiac.AQUARIUS: 85, Zodiac.LIBRA: 70},
    Zodiac.TAURUS: {Zodiac.VIRGO: 95, Zodiac.CAPRICORN: 95, Zodiac.CANCER: 85, Zodiac.PISCES: 90, Zodiac.SCORPIO: 70},
    Zodiac.GEMINI: {Zodiac.LIBRA: 95, Zodiac.AQUARIUS: 95, Zodiac.ARIES: 80, Zodiac.LEO: 85, Zodiac.SAGITTARIUS: 65},
    Zodiac.CANCER: {Zodiac.SCORPIO: 95, Zodiac.PISCES: 95, Zodiac.TAURUS: 85, Zodiac.VIRGO: 80, Zodiac.CAPRICORN: 65},
    Zodiac.LEO: {Zodiac.ARIES: 95, Zodiac.SAGITTARIUS: 95, Zodiac.GEMINI: 85, Zodiac.LIBRA: 80, Zodiac.AQUARIUS: 65},
    Zodiac.VIRGO: {Zodiac.TAURUS: 95, Zodiac.CAPRICORN: 95, Zodiac.CANCER: 80, Zodiac.SCORPIO: 85, Zodiac.PISCES: 65},
    Zodiac.LIBRA: {Zodiac.GEMINI: 95, Zodiac.AQUARIUS: 95, Zodiac.LEO: 80, Zodiac.SAGITTARIUS: 75, Zodiac.ARIES: 70},
    Zodiac.SCORPIO: {Zodiac.CANCER: 95, Zodiac.PISCES: 95, Zodiac.VIRGO: 85, Zodiac.CAPRICORN: 80, Zodiac.TAURUS: 70},
    Zodiac.SAGITTARIUS: {Zodiac.ARIES: 95, Zodiac.LEO: 95, Zodiac.LIBRA: 75, Zodiac.AQUARIUS: 80, Zodiac.GEMINI: 65},
    Zodiac.CAPRICORN: {Zodiac.TAURUS: 95, Zodiac.VIRGO: 95, Zodiac.SCORPIO: 80, Zodiac.PISCES: 75, Zodiac.CANCER: 65},
    Zodiac.AQUARIUS: {Zodiac.GEMINI: 95, Zodiac.LIBRA: 95, Zodiac.SAGITTARIUS: 80, Zodiac.ARIES: 85, Zodiac.LEO: 65},
    Zodiac.PISCES: {Zodiac.CANCER: 95, Zodiac.SCORPIO: 95, Zodiac.TAURUS: 90, Zodiac.CAPRICORN: 75, Zodiac.VIRGO: 65},
}


class ZodiacUtils:
    """星座工具类"""

    @staticmethod
    def get_zodiac(month: int, day: int) -> str:
        """
        根据月份和日期判断星座
        
        Args:
            month: 月份 (1-12)
            day: 日期 (1-31)
            
        Returns:
            星座名称
            
        Raises:
            ValueError: 无效的月份或日期
        """
        if not 1 <= month <= 12:
            raise ValueError(f"无效的月份: {month}")
        if not 1 <= day <= 31:
            raise ValueError(f"无效的日期: {day}")
        
        for zodiac, data in _ZODIAC_DATA.items():
            (start_month, start_day), (end_month, end_day) = data[0], data[1]
            
            # 处理跨年的情况（摩羯座）
            if start_month > end_month:
                if (month == start_month and day >= start_day) or \
                   (month == end_month and day <= end_day) or \
                   (month > start_month or month < end_month):
                    return zodiac
            else:
                if (month == start_month and day >= start_day) or \
                   (month == end_month and day <= end_day) or \
                   (start_month < month < end_month):
                    return zodiac
        
        raise ValueError(f"无法确定星座: {month}月{day}日")

    @staticmethod
    def get_zodiac_from_date(birth_date: Union[date, datetime, str, int, float]) -> str:
        """
        根据出生日期判断星座
        
        Args:
            birth_date: 出生日期，支持多种格式：
                       - date/datetime 对象
                       - 字符串 (YYYY-MM-DD 或 YYYY/MM/DD)
                       - 时间戳
            
        Returns:
            星座名称
        """
        if isinstance(birth_date, datetime):
            month, day = birth_date.month, birth_date.day
        elif isinstance(birth_date, date):
            month, day = birth_date.month, birth_date.day
        elif isinstance(birth_date, str):
            # 尝试解析日期字符串
            birth_date = birth_date.replace('/', '-')
            if ' ' in birth_date:
                birth_date = birth_date.split()[0]
            parts = birth_date.split('-')
            if len(parts) != 3:
                raise ValueError(f"无法解析日期字符串: {birth_date}")
            month, day = int(parts[1]), int(parts[2])
        elif isinstance(birth_date, (int, float)):
            # 时间戳
            dt = datetime.fromtimestamp(birth_date)
            month, day = dt.month, dt.day
        else:
            raise TypeError(f"不支持的日期类型: {type(birth_date)}")
        
        return ZodiacUtils.get_zodiac(month, day)

    @staticmethod
    def get_zodiac_info(zodiac: str) -> Dict[str, Any]:
        """
        获取星座详细信息
        
        Args:
            zodiac: 星座名称
            
        Returns:
            包含星座详细信息的字典
        """
        if zodiac not in _ZODIAC_DATA:
            raise ValueError(f"未知的星座: {zodiac}")
        
        data = _ZODIAC_DATA[zodiac]
        return {
            "name": zodiac,
            "date_range": f"{data[0][0]}月{data[0][1]}日 - {data[1][0]}月{data[1][1]}日",
            "element": data[2].value,
            "quality": data[3].value,
            "ruling_planet": data[4],
            "lucky_numbers": data[5],
            "lucky_colors": data[6],
            "personality_traits": data[7],
            "english_name": ZodiacUtils._get_english_name(zodiac),
            "symbol": ZodiacUtils._get_zodiac_symbol(zodiac),
        }

    @staticmethod
    def _get_english_name(zodiac: str) -> str:
        """获取星座英文名"""
        mapping = {
            Zodiac.ARIES: "Aries",
            Zodiac.TAURUS: "Taurus",
            Zodiac.GEMINI: "Gemini",
            Zodiac.CANCER: "Cancer",
            Zodiac.LEO: "Leo",
            Zodiac.VIRGO: "Virgo",
            Zodiac.LIBRA: "Libra",
            Zodiac.SCORPIO: "Scorpio",
            Zodiac.SAGITTARIUS: "Sagittarius",
            Zodiac.CAPRICORN: "Capricorn",
            Zodiac.AQUARIUS: "Aquarius",
            Zodiac.PISCES: "Pisces",
        }
        return mapping.get(zodiac, "Unknown")

    @staticmethod
    def _get_zodiac_symbol(zodiac: str) -> str:
        """获取星座符号"""
        mapping = {
            Zodiac.ARIES: "♈",
            Zodiac.TAURUS: "♉",
            Zodiac.GEMINI: "♊",
            Zodiac.CANCER: "♋",
            Zodiac.LEO: "♌",
            Zodiac.VIRGO: "♍",
            Zodiac.LIBRA: "♎",
            Zodiac.SCORPIO: "♏",
            Zodiac.SAGITTARIUS: "♐",
            Zodiac.CAPRICORN: "♑",
            Zodiac.AQUARIUS: "♒",
            Zodiac.PISCES: "♓",
        }
        return mapping.get(zodiac, "?")

    @staticmethod
    def get_element(zodiac: str) -> str:
        """获取星座元素"""
        if zodiac not in _ZODIAC_DATA:
            raise ValueError(f"未知的星座: {zodiac}")
        return _ZODIAC_DATA[zodiac][2].value

    @staticmethod
    def get_quality(zodiac: str) -> str:
        """获取星座属性"""
        if zodiac not in _ZODIAC_DATA:
            raise ValueError(f"未知的星座: {zodiac}")
        return _ZODIAC_DATA[zodiac][3].value

    @staticmethod
    def get_ruling_planet(zodiac: str) -> str:
        """获取星座守护星"""
        if zodiac not in _ZODIAC_DATA:
            raise ValueError(f"未知的星座: {zodiac}")
        return _ZODIAC_DATA[zodiac][4]

    @staticmethod
    def get_lucky_numbers(zodiac: str) -> List[int]:
        """获取星座幸运数字"""
        if zodiac not in _ZODIAC_DATA:
            raise ValueError(f"未知的星座: {zodiac}")
        return _ZODIAC_DATA[zodiac][5].copy()

    @staticmethod
    def get_lucky_colors(zodiac: str) -> List[str]:
        """获取星座幸运颜色"""
        if zodiac not in _ZODIAC_DATA:
            raise ValueError(f"未知的星座: {zodiac}")
        return _ZODIAC_DATA[zodiac][6].copy()

    @staticmethod
    def get_personality_traits(zodiac: str) -> List[str]:
        """获取星座性格特点"""
        if zodiac not in _ZODIAC_DATA:
            raise ValueError(f"未知的星座: {zodiac}")
        return _ZODIAC_DATA[zodiac][7].copy()

    @staticmethod
    def calculate_compatibility(zodiac1: str, zodiac2: str) -> Dict[str, Any]:
        """
        计算两个星座的兼容性
        
        Args:
            zodiac1: 第一个星座
            zodiac2: 第二个星座
            
        Returns:
            兼容性分析结果
        """
        if zodiac1 not in _ZODIAC_DATA or zodiac2 not in _ZODIAC_DATA:
            raise ValueError("未知的星座")
        
        # 检查是否有特定的兼容性数据
        if zodiac2 in _COMPATIBILITY_MATRIX.get(zodiac1, {}):
            score = _COMPATIBILITY_MATRIX[zodiac1][zodiac2]
        elif zodiac1 in _COMPATIBILITY_MATRIX.get(zodiac2, {}):
            score = _COMPATIBILITY_MATRIX[zodiac2][zodiac1]
        else:
            # 基于元素计算基础兼容性
            element1 = _ZODIAC_DATA[zodiac1][2]
            element2 = _ZODIAC_DATA[zodiac2][2]
            
            if element1 == element2:
                score = 85  # 同元素，高兼容
            elif (element1, element2) in [(Element.FIRE, Element.AIR), (Element.AIR, Element.FIRE),
                                          (Element.EARTH, Element.WATER), (Element.WATER, Element.EARTH)]:
                score = 75  # 相辅相成
            elif (element1, element2) in [(Element.FIRE, Element.WATER), (Element.WATER, Element.FIRE),
                                          (Element.EARTH, Element.AIR), (Element.AIR, Element.EARTH)]:
                score = 55  # 相克
            else:
                score = 65  # 中等
        
        # 生成描述
        if score >= 90:
            level = "非常契合"
            description = "天作之合，彼此理解深刻，相处和谐"
        elif score >= 80:
            level = "高度兼容"
            description = "性格互补，容易产生共鸣"
        elif score >= 70:
            level = "良好兼容"
            description = "有共同语言，需要适当磨合"
        elif score >= 60:
            level = "中等兼容"
            description = "存在差异，需要互相理解"
        else:
            level = "需要努力"
            description = "性格差异较大，需要更多包容"
        
        return {
            "zodiac1": zodiac1,
            "zodiac2": zodiac2,
            "score": score,
            "level": level,
            "description": description,
            "elements": {
                zodiac1: _ZODIAC_DATA[zodiac1][2].value,
                zodiac2: _ZODIAC_DATA[zodiac2][2].value,
            }
        }

    @staticmethod
    def get_all_zodiacs() -> List[str]:
        """获取所有星座名称列表"""
        return list(_ZODIAC_DATA.keys())

    @staticmethod
    def get_zodiacs_by_element(element: Union[Element, str]) -> List[str]:
        """
        获取指定元素的所有星座
        
        Args:
            element: 元素类型（火象、土象、风象、水象）
            
        Returns:
            该元素下的所有星座列表
        """
        if isinstance(element, str):
            element_map = {
                "火象": Element.FIRE,
                "火": Element.FIRE,
                "土象": Element.EARTH,
                "土": Element.EARTH,
                "风象": Element.AIR,
                "风": Element.AIR,
                "水象": Element.WATER,
                "水": Element.WATER,
            }
            element = element_map.get(element, element)
        
        return [zodiac for zodiac, data in _ZODIAC_DATA.items() if data[2] == element]

    @staticmethod
    def get_zodiacs_by_quality(quality: Union[Quality, str]) -> List[str]:
        """
        获取指定属性的所有星座
        
        Args:
            quality: 属性类型（基本宫、固定宫、变动宫）
            
        Returns:
            该属性下的所有星座列表
        """
        if isinstance(quality, str):
            quality_map = {
                "基本宫": Quality.CARDINAL,
                "基本": Quality.CARDINAL,
                "固定宫": Quality.FIXED,
                "固定": Quality.FIXED,
                "变动宫": Quality.MUTABLE,
                "变动": Quality.MUTABLE,
            }
            quality = quality_map.get(quality, quality)
        
        return [zodiac for zodiac, data in _ZODIAC_DATA.items() if data[3] == quality]

    @staticmethod
    def get_best_matches(zodiac: str, top_n: int = 3) -> List[Dict[str, Any]]:
        """
        获取最佳配对星座
        
        Args:
            zodiac: 星座名称
            top_n: 返回数量
            
        Returns:
            最佳配对星座列表
        """
        if zodiac not in _ZODIAC_DATA:
            raise ValueError(f"未知的星座: {zodiac}")
        
        # 获取该星座的兼容性数据
        compatibilities = _COMPATIBILITY_MATRIX.get(zodiac, {})
        
        # 排序
        sorted_matches = sorted(compatibilities.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {"zodiac": match_zodiac, "score": score}
            for match_zodiac, score in sorted_matches[:top_n]
        ]


class ChineseZodiacUtils:
    """中国生肖工具类"""

    @staticmethod
    def get_zodiac(year: int) -> str:
        """
        根据年份判断生肖
        
        Args:
            year: 年份
            
        Returns:
            生肖名称
        """
        if year < 1:
            raise ValueError(f"无效的年份: {year}")
        
        # 使用 (year - 4) % 12 来计算生肖
        # 2020年是鼠年，所以 2020 % 12 = 4, (2020 - 4) % 12 = 0
        index = (year - 4) % 12
        return _CHINESE_ZODIAC_ORDER[index]

    @staticmethod
    def get_zodiac_from_date(birth_date: Union[date, datetime, str, int, float]) -> str:
        """
        根据出生日期判断生肖
        
        注意：中国传统生肖以农历新年为界，此方法使用简化算法（公历年份）
        
        Args:
            birth_date: 出生日期
            
        Returns:
            生肖名称
        """
        if isinstance(birth_date, datetime):
            year = birth_date.year
        elif isinstance(birth_date, date):
            year = birth_date.year
        elif isinstance(birth_date, str):
            birth_date = birth_date.replace('/', '-')
            if ' ' in birth_date:
                birth_date = birth_date.split()[0]
            parts = birth_date.split('-')
            year = int(parts[0])
        elif isinstance(birth_date, (int, float)):
            dt = datetime.fromtimestamp(birth_date)
            year = dt.year
        else:
            raise TypeError(f"不支持的日期类型: {type(birth_date)}")
        
        return ChineseZodiacUtils.get_zodiac(year)

    @staticmethod
    def get_zodiac_year(zodiac: str) -> List[int]:
        """
        获取指定生肖的年份列表（近100年）
        
        Args:
            zodiac: 生肖名称
            
        Returns:
            年份列表
        """
        if zodiac not in _CHINESE_ZODIAC_ORDER:
            raise ValueError(f"未知的生肖: {zodiac}")
        
        current_year = datetime.now().year
        index = _CHINESE_ZODIAC_ORDER.index(zodiac)
        
        # 计算最近的一个该生肖年份
        base_year = 4 + index  # 2000年是龙年 (index=4)
        while base_year < current_year - 50:
            base_year += 12
        while base_year > current_year + 50:
            base_year -= 12
        
        # 生成年份列表
        years = []
        year = base_year
        while year <= current_year + 50:
            years.append(year)
            year += 12
        
        return years

    @staticmethod
    def get_wuxing(year: int) -> str:
        """
        根据年份获取五行
        
        Args:
            year: 年份
            
        Returns:
            五行属性（金、木、水、火、土）
        """
        if year < 1:
            raise ValueError(f"无效的年份: {year}")
        
        # 天干对应五行
        # 甲乙-木，丙丁-火，戊己-土，庚辛-金，壬癸-水
        tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        tiangan_wuxing = {
            "甲": "木", "乙": "木",
            "丙": "火", "丁": "火",
            "戊": "土", "己": "土",
            "庚": "金", "辛": "金",
            "壬": "水", "癸": "水",
        }
        
        # 计算天干
        tiangan_index = (year - 4) % 10
        gan = tiangan[tiangan_index]
        
        return tiangan_wuxing[gan]

    @staticmethod
    def get_benming_nian(year: int) -> Tuple[str, bool]:
        """
        判断某年是否是本命年
        
        Args:
            year: 年份
            
        Returns:
            (生肖名称, 是否本命年)
        """
        zodiac = ChineseZodiacUtils.get_zodiac(year)
        current_year = datetime.now().year
        current_zodiac = ChineseZodiacUtils.get_zodiac(current_year)
        
        is_benming = zodiac == current_zodiac
        return zodiac, is_benming

    @staticmethod
    def get_zodiac_info(zodiac: str) -> Dict[str, Any]:
        """
        获取生肖详细信息
        
        Args:
            zodiac: 生肖名称
            
        Returns:
            生肖详细信息
        """
        if zodiac not in _CHINESE_ZODIAC_ORDER:
            raise ValueError(f"未知的生肖: {zodiac}")
        
        # 生肖特性数据
        zodiac_traits = {
            ChineseZodiac.RAT: {
                "personality": ["聪明", "灵活", "机敏", "节俭"],
                "strengths": ["适应力强", "善于社交", "机智"],
                "weaknesses": ["多疑", "挑剔"],
                "best_matches": [ChineseZodiac.DRAGON, ChineseZodiac.MONKEY, ChineseZodiac.OX],
                "lucky_numbers": [2, 3],
                "lucky_colors": ["蓝色", "金色", "绿色"],
            },
            ChineseZodiac.OX: {
                "personality": ["勤劳", "踏实", "诚实", "守信"],
                "strengths": ["有耐心", "意志坚定", "可靠"],
                "weaknesses": ["固执", "缺乏灵活性"],
                "best_matches": [ChineseZodiac.RAT, ChineseZodiac.SNAKE, ChineseZodiac.ROOSTER],
                "lucky_numbers": [1, 9],
                "lucky_colors": ["白色", "黄色", "绿色"],
            },
            ChineseZodiac.TIGER: {
                "personality": ["勇敢", "自信", "独立", "果断"],
                "strengths": ["有领导力", "热情", "正义感"],
                "weaknesses": ["冲动", "自负"],
                "best_matches": [ChineseZodiac.HORSE, ChineseZodiac.DOG],
                "lucky_numbers": [1, 3, 4],
                "lucky_colors": ["蓝色", "灰色", "橙色"],
            },
            ChineseZodiac.RABBIT: {
                "personality": ["温柔", "善良", "优雅", "敏感"],
                "strengths": ["有艺术感", "善于交际", "善解人意"],
                "weaknesses": ["优柔寡断", "容易受伤"],
                "best_matches": [ChineseZodiac.GOAT, ChineseZodiac.PIG, ChineseZodiac.DOG],
                "lucky_numbers": [3, 4, 6],
                "lucky_colors": ["粉色", "紫色", "蓝色"],
            },
            ChineseZodiac.DRAGON: {
                "personality": ["自信", "勇敢", "有魅力", "理想主义"],
                "strengths": ["有抱负", "精力充沛", "慷慨"],
                "weaknesses": ["急躁", "傲慢"],
                "best_matches": [ChineseZodiac.RAT, ChineseZodiac.MONKEY, ChineseZodiac.ROOSTER],
                "lucky_numbers": [1, 6, 7],
                "lucky_colors": ["金色", "银色", "灰色"],
            },
            ChineseZodiac.SNAKE: {
                "personality": ["智慧", "神秘", "冷静", "优雅"],
                "strengths": ["洞察力强", "有魅力", "意志坚定"],
                "weaknesses": ["多疑", "嫉妒心"],
                "best_matches": [ChineseZodiac.OX, ChineseZodiac.ROOSTER],
                "lucky_numbers": [2, 8, 9],
                "lucky_colors": ["黑色", "红色", "黄色"],
            },
            ChineseZodiac.HORSE: {
                "personality": ["热情", "开朗", "独立", "自由"],
                "strengths": ["有活力", "善于社交", "聪明"],
                "weaknesses": ["急躁", "缺乏耐心"],
                "best_matches": [ChineseZodiac.TIGER, ChineseZodiac.GOAT, ChineseZodiac.DOG],
                "lucky_numbers": [2, 3, 7],
                "lucky_colors": ["黄色", "绿色"],
            },
            ChineseZodiac.GOAT: {
                "personality": ["温柔", "善良", "有创意", "敏感"],
                "strengths": ["有艺术天赋", "善解人意", "有耐心"],
                "weaknesses": ["优柔寡断", "悲观"],
                "best_matches": [ChineseZodiac.RABBIT, ChineseZodiac.HORSE, ChineseZodiac.PIG],
                "lucky_numbers": [2, 7],
                "lucky_colors": ["棕色", "红色", "紫色"],
            },
            ChineseZodiac.MONKEY: {
                "personality": ["聪明", "机灵", "好奇", "活泼"],
                "strengths": ["多才多艺", "幽默", "适应力强"],
                "weaknesses": ["狡猾", "缺乏耐心"],
                "best_matches": [ChineseZodiac.RAT, ChineseZodiac.DRAGON, ChineseZodiac.SNAKE],
                "lucky_numbers": [4, 9],
                "lucky_colors": ["白色", "蓝色", "金色"],
            },
            ChineseZodiac.ROOSTER: {
                "personality": ["勤奋", "准时", "诚实", "自信"],
                "strengths": ["有责任感", "勤劳", "善于观察"],
                "weaknesses": ["爱炫耀", "挑剔"],
                "best_matches": [ChineseZodiac.OX, ChineseZodiac.SNAKE, ChineseZodiac.DRAGON],
                "lucky_numbers": [5, 7, 8],
                "lucky_colors": ["金色", "棕色", "黄色"],
            },
            ChineseZodiac.DOG: {
                "personality": ["忠诚", "诚实", "可靠", "有正义感"],
                "strengths": ["值得信赖", "勇敢", "有责任心"],
                "weaknesses": ["固执", "担忧过多"],
                "best_matches": [ChineseZodiac.TIGER, ChineseZodiac.RABBIT, ChineseZodiac.HORSE],
                "lucky_numbers": [3, 4, 9],
                "lucky_colors": ["红色", "绿色", "紫色"],
            },
            ChineseZodiac.PIG: {
                "personality": ["善良", "宽容", "诚实", "乐观"],
                "strengths": ["慷慨", "有同情心", "勤奋"],
                "weaknesses": ["天真", "容易轻信"],
                "best_matches": [ChineseZodiac.RABBIT, ChineseZodiac.GOAT, ChineseZodiac.TIGER],
                "lucky_numbers": [2, 5, 8],
                "lucky_colors": ["黄色", "灰色", "棕色"],
            },
        }
        
        info = zodiac_traits[zodiac].copy()
        info["name"] = zodiac
        info["order"] = _CHINESE_ZODIAC_ORDER.index(zodiac) + 1
        
        return info

    @staticmethod
    def get_all_zodiacs() -> List[str]:
        """获取所有生肖名称列表"""
        return _CHINESE_ZODIAC_ORDER.copy()

    @staticmethod
    def calculate_compatibility(zodiac1: str, zodiac2: str) -> Dict[str, Any]:
        """
        计算两个生肖的兼容性
        
        Args:
            zodiac1: 第一个生肖
            zodiac2: 第二个生肖
            
        Returns:
            兼容性分析结果
        """
        if zodiac1 not in _CHINESE_ZODIAC_ORDER or zodiac2 not in _CHINESE_ZODIAC_ORDER:
            raise ValueError("未知的生肖")
        
        info1 = ChineseZodiacUtils.get_zodiac_info(zodiac1)
        info2 = ChineseZodiacUtils.get_zodiac_info(zodiac2)
        
        # 检查是否是最佳配对
        if zodiac2 in info1["best_matches"]:
            score = 95
            level = "天作之合"
            description = "六合生肖，非常般配"
        elif zodiac1 in info2["best_matches"]:
            score = 95
            level = "天作之合"
            description = "六合生肖，非常般配"
        else:
            # 基于位置差距计算
            index1 = _CHINESE_ZODIAC_ORDER.index(zodiac1)
            index2 = _CHINESE_ZODIAC_ORDER.index(zodiac2)
            gap = abs(index1 - index2)
            
            if gap == 6:
                score = 45
                level = "相冲"
                description = "生肖相冲，需要更多理解和包容"
            elif gap == 4 or gap == 8:
                score = 70
                level = "良好"
                description = "生肖相合，有良好的默契"
            else:
                score = 60
                level = "一般"
                description = "需要相互理解，慢慢磨合"
        
        return {
            "zodiac1": zodiac1,
            "zodiac2": zodiac2,
            "score": score,
            "level": level,
            "description": description,
        }

    @staticmethod
    def get_ganzhi(year: int) -> str:
        """
        获取年份的干支纪年
        
        Args:
            year: 年份
            
        Returns:
            干支（如"甲子"）
        """
        if year < 1:
            raise ValueError(f"无效的年份: {year}")
        
        tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        
        gan_index = (year - 4) % 10
        zhi_index = (year - 4) % 12
        
        return tiangan[gan_index] + dizhi[zhi_index]


# 便捷函数
def get_zodiac(month: int, day: int) -> str:
    """根据月份和日期判断星座"""
    return ZodiacUtils.get_zodiac(month, day)


def get_zodiac_from_date(birth_date: Union[date, datetime, str, int, float]) -> str:
    """根据出生日期判断星座"""
    return ZodiacUtils.get_zodiac_from_date(birth_date)


def get_chinese_zodiac(year: int) -> str:
    """根据年份判断生肖"""
    return ChineseZodiacUtils.get_zodiac(year)


def get_chinese_zodiac_from_date(birth_date: Union[date, datetime, str, int, float]) -> str:
    """根据出生日期判断生肖"""
    return ChineseZodiacUtils.get_zodiac_from_date(birth_date)


def calculate_zodiac_compatibility(zodiac1: str, zodiac2: str) -> Dict[str, Any]:
    """计算星座兼容性"""
    return ZodiacUtils.calculate_compatibility(zodiac1, zodiac2)


def calculate_chinese_zodiac_compatibility(zodiac1: str, zodiac2: str) -> Dict[str, Any]:
    """计算生肖兼容性"""
    return ChineseZodiacUtils.calculate_compatibility(zodiac1, zodiac2)