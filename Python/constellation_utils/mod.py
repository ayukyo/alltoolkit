"""
Constellation Utilities - 星座生肖工具

提供完整的星座和生肖相关功能，包括：
- 星座判断（根据生日）
- 星座信息查询（元素、守护星、特质）
- 星座配对分析
- 生肖计算
- 生肖配对分析
- 上升星座估算
- 星座运势生成（趣味性）

零外部依赖，纯 Python 实现。
"""

from typing import Tuple, Optional, Dict, List
from dataclasses import dataclass
from enum import Enum
from datetime import date
import random


class Element(Enum):
    """星座元素"""
    FIRE = "火象"      # 白羊、狮子、射手
    EARTH = "土象"     # 金牛、处女、摩羯
    AIR = "风象"       # 双子、天秤、水瓶
    WATER = "水象"     # 巨蟹、天蝎、双鱼


class Quality(Enum):
    """星座特质"""
    CARDINAL = "本位"     # 白羊、巨蟹、天秤、摩羯
    FIXED = "固定"        # 金牛、狮子、天蝎、水瓶
    MUTABLE = "变动"      # 双子、处女、射手、双鱼


class Zodiac(Enum):
    """十二星座"""
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


class ChineseZodiac(Enum):
    """十二生肖"""
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


@dataclass
class ConstellationInfo:
    """星座详细信息"""
    zodiac: Zodiac
    date_range: str
    element: Element
    quality: Quality
    ruling_planet: str
    lucky_numbers: List[int]
    lucky_colors: List[str]
    lucky_days: List[str]
    strengths: List[str]
    weaknesses: List[str]
    likes: List[str]
    dislikes: List[str]
    compatible_signs: List[Zodiac]


@dataclass
class ChineseZodiacInfo:
    """生肖详细信息"""
    zodiac: ChineseZodiac
    years: List[int]
    element: str
    yin_yang: str
    lucky_numbers: List[int]
    lucky_colors: List[str]
    lucky_directions: List[str]
    strengths: List[str]
    weaknesses: List[str]
    compatible_signs: List[ChineseZodiac]
    incompatible_signs: List[ChineseZodiac]


# 星座详细信息数据
CONSTELLATION_DATA: Dict[Zodiac, ConstellationInfo] = {
    Zodiac.ARIES: ConstellationInfo(
        zodiac=Zodiac.ARIES,
        date_range="3月21日 - 4月19日",
        element=Element.FIRE,
        quality=Quality.CARDINAL,
        ruling_planet="火星",
        lucky_numbers=[1, 8, 17],
        lucky_colors=["红色", "橙色"],
        lucky_days=["星期二", "星期六"],
        strengths=["勇敢", "自信", "热情", "领导力"],
        weaknesses=["冲动", "急躁", "固执"],
        likes=["挑战", "冒险", "运动"],
        dislikes=["等待", "无聊", "被控制"],
        compatible_signs=[Zodiac.LEO, Zodiac.SAGITTARIUS, Zodiac.GEMINI, Zodiac.AQUARIUS]
    ),
    Zodiac.TAURUS: ConstellationInfo(
        zodiac=Zodiac.TAURUS,
        date_range="4月20日 - 5月20日",
        element=Element.EARTH,
        quality=Quality.FIXED,
        ruling_planet="金星",
        lucky_numbers=[2, 6, 9, 15],
        lucky_colors=["绿色", "粉色"],
        lucky_days=["星期一", "星期五"],
        strengths=["可靠", "耐心", "务实", "忠诚"],
        weaknesses=["固执", "占有欲强", "懒散"],
        likes=["美食", "艺术", "舒适"],
        dislikes=["变化", "不稳定", "被催促"],
        compatible_signs=[Zodiac.VIRGO, Zodiac.CAPRICORN, Zodiac.CANCER, Zodiac.PISCES]
    ),
    Zodiac.GEMINI: ConstellationInfo(
        zodiac=Zodiac.GEMINI,
        date_range="5月21日 - 6月21日",
        element=Element.AIR,
        quality=Quality.MUTABLE,
        ruling_planet="水星",
        lucky_numbers=[5, 7, 14, 23],
        lucky_colors=["黄色", "浅蓝色"],
        lucky_days=["星期三", "星期日"],
        strengths=["机智", "灵活", "善于交流", "好奇心强"],
        weaknesses=["善变", "肤浅", "焦虑"],
        likes=["学习", "旅行", "社交"],
        dislikes=["无聊", "重复", "被限制"],
        compatible_signs=[Zodiac.LIBRA, Zodiac.AQUARIUS, Zodiac.ARIES, Zodiac.LEO]
    ),
    Zodiac.CANCER: ConstellationInfo(
        zodiac=Zodiac.CANCER,
        date_range="6月22日 - 7月22日",
        element=Element.WATER,
        quality=Quality.CARDINAL,
        ruling_planet="月亮",
        lucky_numbers=[2, 3, 15, 20],
        lucky_colors=["银白色", "海蓝色"],
        lucky_days=["星期一", "星期四"],
        strengths=["体贴", "忠诚", "直觉敏锐", "有同情心"],
        weaknesses=["情绪化", "敏感", "多疑"],
        likes=["家庭", "烹饪", "收藏"],
        dislikes=["批评", "被忽视", "冲突"],
        compatible_signs=[Zodiac.SCORPIO, Zodiac.PISCES, Zodiac.TAURUS, Zodiac.VIRGO]
    ),
    Zodiac.LEO: ConstellationInfo(
        zodiac=Zodiac.LEO,
        date_range="7月23日 - 8月22日",
        element=Element.FIRE,
        quality=Quality.FIXED,
        ruling_planet="太阳",
        lucky_numbers=[1, 3, 10, 19],
        lucky_colors=["金色", "橙色"],
        lucky_days=["星期日", "星期一"],
        strengths=["慷慨", "自信", "有魅力", "创造力强"],
        weaknesses=["自大", "固执", "爱面子"],
        likes=["表演", "被赞美", "奢华"],
        dislikes=["被忽视", "无聊", "失败"],
        compatible_signs=[Zodiac.ARIES, Zodiac.SAGITTARIUS, Zodiac.GEMINI, Zodiac.LIBRA]
    ),
    Zodiac.VIRGO: ConstellationInfo(
        zodiac=Zodiac.VIRGO,
        date_range="8月23日 - 9月22日",
        element=Element.EARTH,
        quality=Quality.MUTABLE,
        ruling_planet="水星",
        lucky_numbers=[5, 14, 15, 23],
        lucky_colors=["灰色", "米色", "深绿色"],
        lucky_days=["星期三", "星期六"],
        strengths=["细心", "分析能力强", "勤劳", "实际"],
        weaknesses=["过度挑剔", "焦虑", "完美主义"],
        likes=["整理", "健康", "阅读"],
        dislikes=["混乱", "粗鲁", "不靠谱"],
        compatible_signs=[Zodiac.TAURUS, Zodiac.CAPRICORN, Zodiac.CANCER, Zodiac.SCORPIO]
    ),
    Zodiac.LIBRA: ConstellationInfo(
        zodiac=Zodiac.LIBRA,
        date_range="9月23日 - 10月23日",
        element=Element.AIR,
        quality=Quality.CARDINAL,
        ruling_planet="金星",
        lucky_numbers=[4, 6, 13, 22],
        lucky_colors=["粉色", "淡蓝色"],
        lucky_days=["星期五", "星期六"],
        strengths=["公平", "外交", "优雅", "合作"],
        weaknesses=["犹豫不决", "逃避冲突", "依赖"],
        likes=["和谐", "美", "社交"],
        dislikes=["冲突", "不公", "孤独"],
        compatible_signs=[Zodiac.GEMINI, Zodiac.AQUARIUS, Zodiac.LEO, Zodiac.SAGITTARIUS]
    ),
    Zodiac.SCORPIO: ConstellationInfo(
        zodiac=Zodiac.SCORPIO,
        date_range="10月24日 - 11月22日",
        element=Element.WATER,
        quality=Quality.FIXED,
        ruling_planet="冥王星",
        lucky_numbers=[8, 11, 18, 22],
        lucky_colors=["深红色", "黑色"],
        lucky_days=["星期二", "星期四"],
        strengths=["专注", "坚定", "直觉敏锐", "有魅力"],
        weaknesses=["嫉妒", "固执", "记仇"],
        likes=["神秘", "深度", "权力"],
        dislikes=["背叛", "肤浅", "被质疑"],
        compatible_signs=[Zodiac.CANCER, Zodiac.PISCES, Zodiac.VIRGO, Zodiac.CAPRICORN]
    ),
    Zodiac.SAGITTARIUS: ConstellationInfo(
        zodiac=Zodiac.SAGITTARIUS,
        date_range="11月23日 - 12月21日",
        element=Element.FIRE,
        quality=Quality.MUTABLE,
        ruling_planet="木星",
        lucky_numbers=[3, 7, 9, 12],
        lucky_colors=["紫色", "深蓝色"],
        lucky_days=["星期四", "星期日"],
        strengths=["乐观", "爱自由", "慷慨", "幽默"],
        weaknesses=["不耐心", "过于直率", "承诺恐惧"],
        likes=["旅行", "哲学", "学习"],
        dislikes=["束缚", "细节", "被控制"],
        compatible_signs=[Zodiac.ARIES, Zodiac.LEO, Zodiac.LIBRA, Zodiac.AQUARIUS]
    ),
    Zodiac.CAPRICORN: ConstellationInfo(
        zodiac=Zodiac.CAPRICORN,
        date_range="12月22日 - 1月19日",
        element=Element.EARTH,
        quality=Quality.CARDINAL,
        ruling_planet="土星",
        lucky_numbers=[4, 8, 13, 22],
        lucky_colors=["棕色", "黑色"],
        lucky_days=["星期六", "星期日"],
        strengths=["负责", "自律", "实际", "有耐心"],
        weaknesses=["悲观", "固执", "过度工作"],
        likes=["成功", "传统", "成就"],
        dislikes=["失败", "轻浮", "被质疑"],
        compatible_signs=[Zodiac.TAURUS, Zodiac.VIRGO, Zodiac.SCORPIO, Zodiac.PISCES]
    ),
    Zodiac.AQUARIUS: ConstellationInfo(
        zodiac=Zodiac.AQUARIUS,
        date_range="1月20日 - 2月18日",
        element=Element.AIR,
        quality=Quality.FIXED,
        ruling_planet="天王星",
        lucky_numbers=[4, 7, 11, 22],
        lucky_colors=["天蓝色", "银色"],
        lucky_days=["星期六", "星期日"],
        strengths=["独立", "人道主义", "原创", "聪明"],
        weaknesses=["叛逆", "疏离", "固执己见"],
        likes=["创新", "社交", "自由"],
        dislikes=["限制", "传统", "被控制"],
        compatible_signs=[Zodiac.GEMINI, Zodiac.LIBRA, Zodiac.ARIES, Zodiac.SAGITTARIUS]
    ),
    Zodiac.PISCES: ConstellationInfo(
        zodiac=Zodiac.PISCES,
        date_range="2月19日 - 3月20日",
        element=Element.WATER,
        quality=Quality.MUTABLE,
        ruling_planet="海王星",
        lucky_numbers=[3, 9, 12, 15],
        lucky_colors=["海蓝色", "紫色"],
        lucky_days=["星期四", "星期一"],
        strengths=["有同情心", "艺术天赋", "直觉强", "温柔"],
        weaknesses=["逃避现实", "过于敏感", "意志薄弱"],
        likes=["艺术", "梦境", "独处"],
        dislikes=["批评", "残酷", "现实"],
        compatible_signs=[Zodiac.CANCER, Zodiac.SCORPIO, Zodiac.TAURUS, Zodiac.CAPRICORN]
    ),
}


# 生肖详细信息数据
CHINESE_ZODIAC_DATA: Dict[ChineseZodiac, ChineseZodiacInfo] = {
    ChineseZodiac.RAT: ChineseZodiacInfo(
        zodiac=ChineseZodiac.RAT,
        years=[2020, 2008, 1996, 1984, 1972, 1960, 1948],
        element="水",
        yin_yang="阳",
        lucky_numbers=[2, 3],
        lucky_colors=["蓝色", "金色", "绿色"],
        lucky_directions=["东南", "东北"],
        strengths=["聪明", "机智", "适应力强", "节俭"],
        weaknesses=["多疑", "挑剔", "贪心"],
        compatible_signs=[ChineseZodiac.OX, ChineseZodiac.DRAGON, ChineseZodiac.MONKEY],
        incompatible_signs=[ChineseZodiac.HORSE, ChineseZodiac.GOAT]
    ),
    ChineseZodiac.OX: ChineseZodiacInfo(
        zodiac=ChineseZodiac.OX,
        years=[2021, 2009, 1997, 1985, 1973, 1961, 1949],
        element="土",
        yin_yang="阴",
        lucky_numbers=[1, 9],
        lucky_colors=["白色", "黄色", "绿色"],
        lucky_directions=["北", "西南"],
        strengths=["勤劳", "可靠", "坚强", "有耐心"],
        weaknesses=["固执", "保守", "不善表达"],
        compatible_signs=[ChineseZodiac.RAT, ChineseZodiac.SNAKE, ChineseZodiac.ROOSTER],
        incompatible_signs=[ChineseZodiac.TIGER, ChineseZodiac.DRAGON, ChineseZodiac.HORSE]
    ),
    ChineseZodiac.TIGER: ChineseZodiacInfo(
        zodiac=ChineseZodiac.TIGER,
        years=[2022, 2010, 1998, 1986, 1974, 1962, 1950],
        element="木",
        yin_yang="阳",
        lucky_numbers=[1, 3, 4],
        lucky_colors=["蓝色", "灰色", "橙色"],
        lucky_directions=["南", "东", "东南"],
        strengths=["勇敢", "自信", "有魅力", "竞争心强"],
        weaknesses=["冲动", "固执", "傲慢"],
        compatible_signs=[ChineseZodiac.HORSE, ChineseZodiac.DOG],
        incompatible_signs=[ChineseZodiac.OX, ChineseZodiac.SNAKE, ChineseZodiac.MONKEY]
    ),
    ChineseZodiac.RABBIT: ChineseZodiacInfo(
        zodiac=ChineseZodiac.RABBIT,
        years=[2023, 2011, 1999, 1987, 1975, 1963, 1951],
        element="木",
        yin_yang="阴",
        lucky_numbers=[3, 4, 6],
        lucky_colors=["粉色", "紫色", "蓝色"],
        lucky_directions=["东", "南", "西北"],
        strengths=["温和", "优雅", "谨慎", "有同情心"],
        weaknesses=["胆小", "优柔寡断", "敏感"],
        compatible_signs=[ChineseZodiac.GOAT, ChineseZodiac.PIG, ChineseZodiac.DOG],
        incompatible_signs=[ChineseZodiac.RAT, ChineseZodiac.SNAKE, ChineseZodiac.MONKEY]
    ),
    ChineseZodiac.DRAGON: ChineseZodiacInfo(
        zodiac=ChineseZodiac.DRAGON,
        years=[2024, 2012, 2000, 1988, 1976, 1964, 1952],
        element="土",
        yin_yang="阳",
        lucky_numbers=[1, 6, 7],
        lucky_colors=["金色", "银色", "灰色"],
        lucky_directions=["东", "北", "西"],
        strengths=["自信", "聪明", "有野心", "热情"],
        weaknesses=["急躁", "傲慢", "不切实际"],
        compatible_signs=[ChineseZodiac.RAT, ChineseZodiac.MONKEY, ChineseZodiac.ROOSTER],
        incompatible_signs=[ChineseZodiac.OX, ChineseZodiac.DOG]
    ),
    ChineseZodiac.SNAKE: ChineseZodiacInfo(
        zodiac=ChineseZodiac.SNAKE,
        years=[2025, 2013, 2001, 1989, 1977, 1965, 1953],
        element="火",
        yin_yang="阴",
        lucky_numbers=[2, 8, 9],
        lucky_colors=["红色", "黄色", "黑色"],
        lucky_directions=["东", "西", "西南"],
        strengths=["智慧", "神秘", "有魅力", "直觉强"],
        weaknesses=["嫉妒", "多疑", "占有欲强"],
        compatible_signs=[ChineseZodiac.OX, ChineseZodiac.ROOSTER],
        incompatible_signs=[ChineseZodiac.TIGER, ChineseZodiac.RABBIT, ChineseZodiac.GOAT]
    ),
    ChineseZodiac.HORSE: ChineseZodiacInfo(
        zodiac=ChineseZodiac.HORSE,
        years=[2026, 2014, 2002, 1990, 1978, 1966, 1954],
        element="火",
        yin_yang="阳",
        lucky_numbers=[2, 3, 7],
        lucky_colors=["黄色", "绿色"],
        lucky_directions=["南", "西南"],
        strengths=["热情", "活泼", "独立", "有活力"],
        weaknesses=["冲动", "自私", "缺乏耐心"],
        compatible_signs=[ChineseZodiac.TIGER, ChineseZodiac.GOAT, ChineseZodiac.DOG],
        incompatible_signs=[ChineseZodiac.RAT, ChineseZodiac.OX, ChineseZodiac.ROOSTER]
    ),
    ChineseZodiac.GOAT: ChineseZodiacInfo(
        zodiac=ChineseZodiac.GOAT,
        years=[2027, 2015, 2003, 1991, 1979, 1967, 1955],
        element="土",
        yin_yang="阴",
        lucky_numbers=[2, 7],
        lucky_colors=["棕色", "红色", "紫色"],
        lucky_directions=["北", "西北", "西"],
        strengths=["温和", "有创造力", "善良", "有同情心"],
        weaknesses=["优柔寡断", "悲观", "敏感"],
        compatible_signs=[ChineseZodiac.RABBIT, ChineseZodiac.HORSE, ChineseZodiac.PIG],
        incompatible_signs=[ChineseZodiac.RAT, ChineseZodiac.OX, ChineseZodiac.DOG]
    ),
    ChineseZodiac.MONKEY: ChineseZodiacInfo(
        zodiac=ChineseZodiac.MONKEY,
        years=[2028, 2016, 2004, 1992, 1980, 1968, 1956],
        element="金",
        yin_yang="阳",
        lucky_numbers=[4, 9],
        lucky_colors=["白色", "蓝色", "金色"],
        lucky_directions=["北", "西北", "西"],
        strengths=["聪明", "机智", "好奇", "灵活"],
        weaknesses=["狡猾", "傲慢", "缺乏耐心"],
        compatible_signs=[ChineseZodiac.RAT, ChineseZodiac.DRAGON],
        incompatible_signs=[ChineseZodiac.TIGER, ChineseZodiac.PIG]
    ),
    ChineseZodiac.ROOSTER: ChineseZodiacInfo(
        zodiac=ChineseZodiac.ROOSTER,
        years=[2029, 2017, 2005, 1993, 1981, 1969, 1957],
        element="金",
        yin_yang="阴",
        lucky_numbers=[5, 7, 8],
        lucky_colors=["金色", "棕色", "黄色"],
        lucky_directions=["东南", "南"],
        strengths=["勤奋", "守时", "勇敢", "自信"],
        weaknesses=["傲慢", "多疑", "爱炫耀"],
        compatible_signs=[ChineseZodiac.OX, ChineseZodiac.SNAKE, ChineseZodiac.DRAGON],
        incompatible_signs=[ChineseZodiac.RAT, ChineseZodiac.RABBIT, ChineseZodiac.HORSE]
    ),
    ChineseZodiac.DOG: ChineseZodiacInfo(
        zodiac=ChineseZodiac.DOG,
        years=[2030, 2018, 2006, 1994, 1982, 1970, 1958],
        element="土",
        yin_yang="阳",
        lucky_numbers=[3, 4, 9],
        lucky_colors=["红色", "绿色", "紫色"],
        lucky_directions=["东", "东南", "南"],
        strengths=["忠诚", "诚实", "负责", "勇敢"],
        weaknesses=["敏感", "固执", "悲观"],
        compatible_signs=[ChineseZodiac.TIGER, ChineseZodiac.RABBIT, ChineseZodiac.HORSE],
        incompatible_signs=[ChineseZodiac.OX, ChineseZodiac.DRAGON, ChineseZodiac.GOAT]
    ),
    ChineseZodiac.PIG: ChineseZodiacInfo(
        zodiac=ChineseZodiac.PIG,
        years=[2031, 2019, 2007, 1995, 1983, 1971, 1959],
        element="水",
        yin_yang="阴",
        lucky_numbers=[2, 5, 8],
        lucky_colors=["黄色", "灰色", "棕色"],
        lucky_directions=["东南", "东"],
        strengths=["真诚", "慷慨", "有耐心", "善良"],
        weaknesses=["天真", "轻信", "懒惰"],
        compatible_signs=[ChineseZodiac.TIGER, ChineseZodiac.RABBIT, ChineseZodiac.GOAT],
        incompatible_signs=[ChineseZodiac.SNAKE, ChineseZodiac.MONKEY]
    ),
}


# 星座日期范围（月, 日）
_ZODIAC_DATES = [
    ((1, 20), (2, 18), Zodiac.AQUARIUS),
    ((2, 19), (3, 20), Zodiac.PISCES),
    ((3, 21), (4, 19), Zodiac.ARIES),
    ((4, 20), (5, 20), Zodiac.TAURUS),
    ((5, 21), (6, 21), Zodiac.GEMINI),
    ((6, 22), (7, 22), Zodiac.CANCER),
    ((7, 23), (8, 22), Zodiac.LEO),
    ((8, 23), (9, 22), Zodiac.VIRGO),
    ((9, 23), (10, 23), Zodiac.LIBRA),
    ((10, 24), (11, 22), Zodiac.SCORPIO),
    ((11, 23), (12, 21), Zodiac.SAGITTARIUS),
    ((12, 22), (1, 19), Zodiac.CAPRICORN),
]


def get_zodiac(month: int, day: int) -> Zodiac:
    """
    根据月份和日期判断星座
    
    Args:
        month: 月份 (1-12)
        day: 日期 (1-31)
    
    Returns:
        对应的 Zodiac 枚举值
    
    Raises:
        ValueError: 月份或日期无效
    """
    if not 1 <= month <= 12:
        raise ValueError(f"月份必须在 1-12 之间，当前: {month}")
    
    # 验证日期是否在有效范围内
    days_in_month = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if not 1 <= day <= days_in_month[month]:
        raise ValueError(f"{month}月的日期必须在 1-{days_in_month[month]} 之间，当前: {day}")
    
    for (start_m, start_d), (end_m, end_d), zodiac in _ZODIAC_DATES:
        if start_m > end_m:  # 跨年情况（摩羯座）
            if (month == start_m and day >= start_d) or (month == end_m and day <= end_d):
                return zodiac
        else:
            if (month == start_m and day >= start_d) or (month == end_m and day <= end_d) or \
               (start_m < month < end_m):
                return zodiac
    
    return Zodiac.CAPRICORN  # 默认返回摩羯座


def get_zodiac_from_date(birth_date: date) -> Zodiac:
    """
    根据出生日期判断星座
    
    Args:
        birth_date: 出生日期
    
    Returns:
        对应的 Zodiac 枚举值
    """
    return get_zodiac(birth_date.month, birth_date.day)


def get_zodiac_info(zodiac: Zodiac) -> ConstellationInfo:
    """
    获取星座详细信息
    
    Args:
        zodiac: 星座枚举值
    
    Returns:
        ConstellationInfo 对象
    """
    return CONSTELLATION_DATA[zodiac]


def get_element(zodiac: Zodiac) -> Element:
    """
    获取星座元素
    
    Args:
        zodiac: 星座枚举值
    
    Returns:
        Element 枚举值
    """
    return CONSTELLATION_DATA[zodiac].element


def get_quality(zodiac: Zodiac) -> Quality:
    """
    获取星座特质
    
    Args:
        zodiac: 星座枚举值
    
    Returns:
        Quality 枚举值
    """
    return CONSTELLATION_DATA[zodiac].quality


def get_ruling_planet(zodiac: Zodiac) -> str:
    """
    获取星座守护星
    
    Args:
        zodiac: 星座枚举值
    
    Returns:
        守护星名称
    """
    return CONSTELLATION_DATA[zodiac].ruling_planet


def calculate_compatibility(zodiac1: Zodiac, zodiac2: Zodiac) -> Dict[str, any]:
    """
    计算两个星座的配对指数
    
    Args:
        zodiac1: 第一个星座
        zodiac2: 第二个星座
    
    Returns:
        包含配对信息的字典
    """
    info1 = CONSTELLATION_DATA[zodiac1]
    info2 = CONSTELLATION_DATA[zodiac2]
    
    # 基础分数
    score = 50
    
    # 元素相同 +20
    if info1.element == info2.element:
        score += 20
    
    # 元素相配 (火-风, 土-水) +15
    harmonious_pairs = [
        (Element.FIRE, Element.AIR),
        (Element.AIR, Element.FIRE),
        (Element.EARTH, Element.WATER),
        (Element.WATER, Element.EARTH),
    ]
    if (info1.element, info2.element) in harmonious_pairs:
        score += 15
    
    # 相互在最佳配对列表中 +15
    if zodiac2 in info1.compatible_signs and zodiac1 in info2.compatible_signs:
        score += 15
    elif zodiac2 in info1.compatible_signs or zodiac1 in info2.compatible_signs:
        score += 8
    
    # 特质匹配
    if info1.quality == info2.quality:
        score += 5
    
    # 确保分数在 0-100 范围内
    score = max(0, min(100, score))
    
    # 生成描述
    if score >= 80:
        description = "天作之合！你们天生就有很强的默契和吸引力。"
    elif score >= 60:
        description = "良配佳偶！你们有很好的相容性，需要相互理解。"
    elif score >= 40:
        description = "中等配对，需要付出更多努力来维系关系。"
    else:
        description = "互补型配对，你们的差异可以带来成长机会。"
    
    return {
        "zodiac1": zodiac1.value,
        "zodiac2": zodiac2.value,
        "score": score,
        "description": description,
        "element_match": info1.element == info2.element,
        "compatible": zodiac2 in info1.compatible_signs,
    }


def get_chinese_zodiac(year: int) -> ChineseZodiac:
    """
    根据年份计算生肖
    
    Args:
        year: 出生年份
    
    Returns:
        ChineseZodiac 枚举值
    
    Raises:
        ValueError: 年份无效
    """
    if year < 1900 or year > 2100:
        raise ValueError(f"年份必须在 1900-2100 之间，当前: {year}")
    
    zodiac_order = [
        ChineseZodiac.RAT,
        ChineseZodiac.OX,
        ChineseZodiac.TIGER,
        ChineseZodiac.RABBIT,
        ChineseZodiac.DRAGON,
        ChineseZodiac.SNAKE,
        ChineseZodiac.HORSE,
        ChineseZodiac.GOAT,
        ChineseZodiac.MONKEY,
        ChineseZodiac.ROOSTER,
        ChineseZodiac.DOG,
        ChineseZodiac.PIG,
    ]
    
    # 2008年是鼠年
    base_year = 2008
    offset = (year - base_year) % 12
    if offset < 0:
        offset += 12
    
    return zodiac_order[offset]


def get_chinese_zodiac_info(zodiac: ChineseZodiac) -> ChineseZodiacInfo:
    """
    获取生肖详细信息
    
    Args:
        zodiac: 生肖枚举值
    
    Returns:
        ChineseZodiacInfo 对象
    """
    return CHINESE_ZODIAC_DATA[zodiac]


def calculate_chinese_compatibility(zodiac1: ChineseZodiac, zodiac2: ChineseZodiac) -> Dict[str, any]:
    """
    计算两个生肖的配对指数
    
    Args:
        zodiac1: 第一个生肖
        zodiac2: 第二个生肖
    
    Returns:
        包含配对信息的字典
    """
    info1 = CHINESE_ZODIAC_DATA[zodiac1]
    info2 = CHINESE_ZODIAC_DATA[zodiac2]
    
    # 基础分数
    score = 50
    
    # 相互最佳配对 +30
    if zodiac2 in info1.compatible_signs and zodiac1 in info2.compatible_signs:
        score += 30
    elif zodiac2 in info1.compatible_signs or zodiac1 in info2.compatible_signs:
        score += 15
    
    # 相冲 -25
    if zodiac2 in info1.incompatible_signs or zodiac1 in info2.incompatible_signs:
        score -= 25
    
    # 阴阳互补 +10
    if info1.yin_yang != info2.yin_yang:
        score += 10
    
    # 确保分数在 0-100 范围内
    score = max(0, min(100, score))
    
    # 生成描述
    if score >= 80:
        description = "六合之配！你们是天作之合，非常适合在一起。"
    elif score >= 60:
        description = "三合之配！你们有很好的相容性，可以相互扶持。"
    elif score >= 40:
        description = "中等配对，需要多沟通理解。"
    else:
        description = "相冲之配，你们的差异较大，需要更多的包容。"
    
    return {
        "zodiac1": zodiac1.value,
        "zodiac2": zodiac2.value,
        "score": score,
        "description": description,
        "compatible": zodiac2 in info1.compatible_signs,
        "incompatible": zodiac2 in info1.incompatible_signs,
    }


def estimate_rising_sign(birth_time: Tuple[int, int], zodiac: Zodiac) -> Zodiac:
    """
    估算上升星座（简化版，仅供娱乐参考）
    
        注意：这只是一个简化估算，真实上升星座需要精确出生时间和地点
    
    Args:
        birth_time: 出生时间 (小时, 分钟)，24小时制
        zodiac: 太阳星座
    
    Returns:
        估算的上升星座
    """
    hour, minute = birth_time
    
    if not 0 <= hour <= 23 or not 0 <= minute <= 59:
        raise ValueError(f"无效的时间: {hour}:{minute}")
    
    # 每个时辰对应一个星座
    # 大约每2小时变换一个星座
    time_to_rising = [
        Zodiac.CAPRICORN,   # 00:00-01:59
        Zodiac.AQUARIUS,    # 02:00-03:59
        Zodiac.PISCES,      # 04:00-05:59
        Zodiac.ARIES,       # 06:00-07:59
        Zodiac.TAURUS,      # 08:00-09:59
        Zodiac.GEMINI,      # 10:00-11:59
        Zodiac.CANCER,      # 12:00-13:59
        Zodiac.LEO,         # 14:00-15:59
        Zodiac.VIRGO,       # 16:00-17:59
        Zodiac.LIBRA,       # 18:00-19:59
        Zodiac.SCORPIO,     # 20:00-21:59
        Zodiac.SAGITTARIUS, # 22:00-23:59
    ]
    
    time_slot = (hour // 2)
    
    # 基于太阳星座进行偏移调整
    zodiac_offset = list(Zodiac).index(zodiac)
    rising_index = (time_slot + zodiac_offset) % 12
    
    return list(Zodiac)[rising_index]


def get_daily_horoscope(zodiac: Zodiac, seed: Optional[int] = None) -> Dict[str, str]:
    """
    生成每日运势（仅供娱乐）
    
    Args:
        zodiac: 星座
        seed: 随机种子（可选，用于生成可重复的运势）
    
    Returns:
        包含各项运势的字典
    """
    if seed is not None:
        random.seed(seed)
    
    # 运势等级
    levels = ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]
    
    # 各方面运势描述
    love_descriptions = [
        "今天适合与伴侣共度时光，单身者有机会遇到心仪对象。",
        "感情稳定，但要注意沟通方式。",
        "桃花运旺盛，可以多参加社交活动。",
        "感情方面需要更多的耐心和理解。",
        "单身者不宜急于表白，多观察了解为好。",
    ]
    
    career_descriptions = [
        "工作运势良好，适合展现个人能力。",
        "注意细节，避免小错误带来大麻烦。",
        "有机会获得领导的认可，把握机遇。",
        "团队合作是今天的关键词。",
        "适合学习新技能，提升自我价值。",
    ]
    
    wealth_descriptions = [
        "财运亨通，有意外之财的可能。",
        "理性消费，避免冲动购物。",
        "投资方面需要谨慎，不宜冒进。",
        "有贵人相助，财务状况向好。",
        "适合做长期理财规划。",
    ]
    
    health_descriptions = [
        "精力充沛，适合户外运动。",
        "注意作息规律，避免熬夜。",
        "饮食宜清淡，少食辛辣。",
        "适度放松，缓解压力。",
        "多喝水，保持良好的身体状态。",
    ]
    
    # 幸运颜色列表
    lucky_colors = [
        "红色", "橙色", "黄色", "绿色", "蓝色", 
        "紫色", "粉色", "白色", "黑色", "金色",
    ]
    
    # 幸运数字
    lucky_numbers = [str(random.randint(1, 9)) for _ in range(3)]
    
    return {
        "zodiac": zodiac.value,
        "overall": random.choice(levels),
        "love": {
            "level": random.choice(levels),
            "description": random.choice(love_descriptions),
        },
        "career": {
            "level": random.choice(levels),
            "description": random.choice(career_descriptions),
        },
        "wealth": {
            "level": random.choice(levels),
            "description": random.choice(wealth_descriptions),
        },
        "health": {
            "level": random.choice(levels),
            "description": random.choice(health_descriptions),
        },
        "lucky_color": random.choice(lucky_colors),
        "lucky_number": "、".join(lucky_numbers),
        "tip": random.choice([
            "保持乐观心态，好事自然来。",
            "今日宜静不宜动，多思考少行动。",
            "机会就在身边，抓住每一个可能。",
            "与其担心未来，不如把握当下。",
            "微笑是最好的名片，今天多笑笑吧。",
        ]),
    }


def get_all_zodiacs() -> List[Zodiac]:
    """
    获取所有星座列表
    
    Returns:
        包含所有 Zodiac 枚举值的列表
    """
    return list(Zodiac)


def get_all_chinese_zodiacs() -> List[ChineseZodiac]:
    """
    获取所有生肖列表
    
    Returns:
        包含所有 ChineseZodiac 枚举值的列表
    """
    return list(ChineseZodiac)


def get_zodiac_by_chinese_name(name: str) -> Optional[Zodiac]:
    """
    根据中文名称获取星座
    
    Args:
        name: 星座中文名称（如"白羊座"）
    
    Returns:
        Zodiac 枚举值，如果未找到返回 None
    """
    for zodiac in Zodiac:
        if zodiac.value == name:
            return zodiac
    return None


def get_chinese_zodiac_by_name(name: str) -> Optional[ChineseZodiac]:
    """
    根据中文名称获取生肖
    
    Args:
        name: 生肖中文名称（如"龙"）
    
    Returns:
        ChineseZodiac 枚举值，如果未找到返回 None
    """
    for zodiac in ChineseZodiac:
        if zodiac.value == name:
            return zodiac
    return None


def get_element_relationship(element1: Element, element2: Element) -> str:
    """
    获取两个元素之间的关系
    
    Args:
        element1: 第一个元素
        element2: 第二个元素
    
    Returns:
        关系描述字符串
    """
    # 元素相生相克关系
    generating = {
        Element.FIRE: Element.EARTH,   # 火生土
        Element.EARTH: Element.METAL if hasattr(Element, 'METAL') else Element.AIR,   # 土生金（简化为土生风）
        Element.AIR: Element.WATER,    # 风生水
        Element.WATER: Element.WOOD if hasattr(Element, 'WOOD') else Element.FIRE,   # 水生木（简化为水生火）
    }
    
    # 相同元素
    if element1 == element2:
        return "同元素，性格特质相似，容易理解对方。"
    
    # 和谐配对
    harmonious = [
        (Element.FIRE, Element.AIR),
        (Element.AIR, Element.FIRE),
        (Element.EARTH, Element.WATER),
        (Element.WATER, Element.EARTH),
    ]
    
    if (element1, element2) in harmonious:
        return "元素和谐，相互促进，是理想的组合。"
    
    # 冲突配对
    conflicting = [
        (Element.FIRE, Element.WATER),
        (Element.WATER, Element.FIRE),
        (Element.EARTH, Element.AIR),
        (Element.AIR, Element.EARTH),
    ]
    
    if (element1, element2) in conflicting:
        return "元素相冲，性格差异大，需要多加磨合。"
    
    return "元素中性，需要相互理解才能和谐相处。"


def calculate_triple_harmony(zodiac: Zodiac) -> List[Zodiac]:
    """
    计算三合星座
    
    三合星座是每四个星座组成一组，彼此相容度最高
    
    Args:
        zodiac: 目标星座
    
    Returns:
        三合星座列表（包含自身）
    """
    # 三合星座分组
    trines = [
        [Zodiac.ARIES, Zodiac.LEO, Zodiac.SAGITTARIUS],      # 火象三合
        [Zodiac.TAURUS, Zodiac.VIRGO, Zodiac.CAPRICORN],    # 土象三合
        [Zodiac.GEMINI, Zodiac.LIBRA, Zodiac.AQUARIUS],     # 风象三合
        [Zodiac.CANCER, Zodiac.SCORPIO, Zodiac.PISCES],     # 水象三合
    ]
    
    for trine in trines:
        if zodiac in trine:
            return trine
    
    return [zodiac]


def calculate_six_harm(zodiac: Zodiac) -> Optional[Zodiac]:
    """
    计算六害星座
    
    六害星座之间存在一定的冲突
    
    Args:
        zodiac: 目标星座
    
    Returns:
        六害星座，如果没有则返回 None
    """
    # 六害配对（基于西方星座简化版本）
    six_harms = {
        Zodiac.ARIES: Zodiac.CANCER,
        Zodiac.TAURUS: Zodiac.LEO,
        Zodiac.GEMINI: Zodiac.VIRGO,
        Zodiac.CANCER: Zodiac.ARIES,
        Zodiac.LEO: Zodiac.TAURUS,
        Zodiac.VIRGO: Zodiac.GEMINI,
        Zodiac.LIBRA: Zodiac.CAPRICORN,
        Zodiac.SCORPIO: Zodiac.AQUARIUS,
        Zodiac.SAGITTARIUS: Zodiac.PISCES,
        Zodiac.CAPRICORN: Zodiac.LIBRA,
        Zodiac.AQUARIUS: Zodiac.SCORPIO,
        Zodiac.PISCES: Zodiac.SAGITTARIUS,
    }
    
    return six_harms.get(zodiac)