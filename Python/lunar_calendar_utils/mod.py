"""
农历日历工具模块 (Lunar Calendar Utils)
=======================================

提供农历与公历之间的转换，支持节气计算、传统节日查询、生肖干支计算等功能。

功能:
- 公历转农历
- 农历转公历
- 节气计算
- 传统节日查询
- 生肖计算
- 干支计算（天干地支）
- 农历月份名称
- 星座计算

作者: AllToolkit 自动化开发助手
日期: 2026-04-23
"""

from datetime import datetime, date, timedelta
from typing import Optional, Tuple, List, Dict
import math


# ==================== 基础数据 ====================

# 天干
TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 地支
DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 生肖
ZODIAC = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']

# 农历月份名称
LUNAR_MONTH_NAMES = {
    1: '正月', 2: '二月', 3: '三月', 4: '四月', 5: '五月', 6: '六月',
    7: '七月', 8: '八月', 9: '九月', 10: '十月', 11: '十一月', 12: '腊月'
}

# 农历日期名称
LUNAR_DAY_NAMES = {
    1: '初一', 2: '初二', 3: '初三', 4: '初四', 5: '初五',
    6: '初六', 7: '初七', 8: '初八', 9: '初九', 10: '初十',
    11: '十一', 12: '十二', 13: '十三', 14: '十四', 15: '十五',
    16: '十六', 17: '十七', 18: '十八', 19: '十九', 20: '二十',
    21: '廿一', 22: '廿二', 23: '廿三', 24: '廿四', 25: '廿五',
    26: '廿六', 27: '廿七', 28: '廿八', 29: '廿九', 30: '三十'
}

# 24节气名称
SOLAR_TERMS = [
    '小寒', '大寒', '立春', '雨水', '惊蛰', '春分',
    '清明', '谷雨', '立夏', '小满', '芒种', '夏至',
    '小暑', '大暑', '立秋', '处暑', '白露', '秋分',
    '寒露', '霜降', '立冬', '小雪', '大雪', '冬至'
]

# 传统节日（农历日期）
LUNAR_FESTIVALS = {
    (1, 1): '春节',
    (1, 15): '元宵节',
    (2, 2): '龙抬头',
    (5, 5): '端午节',
    (7, 7): '七夕节',
    (7, 15): '中元节',
    (8, 15): '中秋节',
    (9, 9): '重阳节',
    (12, 8): '腊八节',
    (12, 23): '小年',
    (12, 30): '除夕',
}

# 公历节日
SOLAR_FESTIVALS = {
    (1, 1): '元旦',
    (2, 14): '情人节',
    (3, 8): '妇女节',
    (3, 12): '植树节',
    (4, 1): '愚人节',
    (5, 1): '劳动节',
    (5, 4): '青年节',
    (6, 1): '儿童节',
    (7, 1): '建党节',
    (8, 1): '建军节',
    (9, 10): '教师节',
    (10, 1): '国庆节',
    (10, 31): '万圣节前夜',
    (11, 11): '光棍节',
    (12, 25): '圣诞节',
}


# ==================== 农历数据表 ====================
# 使用 1900-2100 年的农历数据（经典算法）
# 数据格式：
# - 16进制数中，第1-4位表示闰月月份（0表示无闰月）
# - 第5-16位表示12个月的大小（1为大月30天，0为小月29天）
# - 第17位表示闰月的大小（1为大月）

LUNAR_INFO = [
    0x04bd8, 0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0, 0x09ad0, 0x055d2,
    0x04ae0, 0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540, 0x0d6a0, 0x0ada2, 0x095b0, 0x14977,
    0x04970, 0x0a4b0, 0x0b4b5, 0x06a50, 0x06d40, 0x1ab54, 0x02b60, 0x09570, 0x052f2, 0x04970,
    0x06566, 0x0d4a0, 0x0ea50, 0x06e95, 0x05ad0, 0x02b60, 0x186e3, 0x092e0, 0x1c8d7, 0x0c950,
    0x0d4a0, 0x1d8a6, 0x0b550, 0x056a0, 0x1a5b4, 0x025d0, 0x092d0, 0x0d2b2, 0x0a950, 0x0b557,
    0x06ca0, 0x0b550, 0x15355, 0x04da0, 0x0a5b0, 0x14573, 0x052b0, 0x0a9a8, 0x0e950, 0x06aa0,
    0x0aea6, 0x0ab50, 0x04b60, 0x0aae4, 0x0a570, 0x05260, 0x0f263, 0x0d950, 0x05b57, 0x056a0,
    0x096d0, 0x04dd5, 0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250, 0x0d558, 0x0b540, 0x0b6a0, 0x195a6,
    0x095b0, 0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50, 0x06d40, 0x0af46, 0x0ab60, 0x09570,
    0x04af5, 0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58, 0x055c0, 0x0ab60, 0x096d5, 0x092e0,
    0x0c960, 0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0, 0x0abb7, 0x025d0, 0x092d0, 0x0cab5,
    0x0a950, 0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0, 0x0a5b0, 0x15176, 0x052b0, 0x0a930,
    0x07954, 0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6, 0x0a4e0, 0x0d260, 0x0ea65, 0x0d530,
    0x05aa0, 0x076a3, 0x096d0, 0x04afb, 0x04ad0, 0x0a4d0, 0x1d0b6, 0x0d250, 0x0d520, 0x0dd45,
    0x0b5a0, 0x056d0, 0x055b2, 0x049b0, 0x0a577, 0x0a4b0, 0x0aa50, 0x1b255, 0x06d20, 0x0ada0,
    0x14b63, 0x09370, 0x049f8, 0x04970, 0x064b0, 0x168a6, 0x0ea50, 0x06b20, 0x1a6c4, 0x0aae0,
    0x0a2e0, 0x0d2e3, 0x0c960, 0x0d557, 0x0d4a0, 0x0da50, 0x05d55, 0x056a0, 0x0a6d0, 0x055d4,
    0x052d0, 0x0a9b8, 0x0a950, 0x0b4a0, 0x0b6a6, 0x0ad50, 0x055a0, 0x0aba4, 0x0a5b0, 0x052b0,
    0x0b273, 0x06930, 0x07337, 0x06aa0, 0x0ad50, 0x14b55, 0x04b60, 0x0a570, 0x054e4, 0x0d160,
    0x0e968, 0x0d520, 0x0daa0, 0x16aa6, 0x056d0, 0x04ae0, 0x0a9d4, 0x0a2d0, 0x0d150, 0x0f252,
    0x0d520,
]


class LunarDate:
    """农历日期类"""
    
    def __init__(self, year: int, month: int, day: int, is_leap_month: bool = False):
        self.year = year
        self.month = month
        self.day = day
        self.is_leap_month = is_leap_month
    
    def __repr__(self) -> str:
        leap = '(闰)' if self.is_leap_month else ''
        return f"LunarDate({self.year}, {self.month}, {self.day}{leap})"
    
    def __str__(self) -> str:
        """返回中文字符串表示"""
        leap = '闰' if self.is_leap_month else ''
        month_name = LUNAR_MONTH_NAMES.get(self.month, f'{self.month}月')
        day_name = LUNAR_DAY_NAMES.get(self.day, f'{self.day}日')
        return f"农历{leap}{month_name}{day_name}"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, LunarDate):
            return False
        return (self.year == other.year and self.month == other.month and 
                self.day == other.day and self.is_leap_month == other.is_leap_month)
    
    def __hash__(self) -> int:
        return hash((self.year, self.month, self.day, self.is_leap_month))
    
    def get_ganzhi_year(self) -> str:
        """获取年干支"""
        return get_year_ganzhi(self.year)
    
    def get_zodiac(self) -> str:
        """获取生肖"""
        return get_zodiac(self.year)
    
    def get_festival(self) -> Optional[str]:
        """获取节日名称（如果有）"""
        return LUNAR_FESTIVALS.get((self.month, self.day))


# ==================== 核心转换函数 ====================

def _get_leap_month(year: int) -> int:
    """获取闰月月份（0表示无闰月）"""
    return LUNAR_INFO[year - 1900] & 0xf


def _get_leap_month_days(year: int) -> int:
    """获取闰月天数（0表示无闰月）"""
    leap_month = _get_leap_month(year)
    if leap_month == 0:
        return 0
    # 闰月大小：如果第17位是1，则为大月30天
    if LUNAR_INFO[year - 1900] & 0x10000:
        return 30
    return 29


def _get_lunar_month_days(year: int, month: int) -> int:
    """获取农历某月的天数（不包括闰月）"""
    # 检查第5-16位，月份从高位开始
    # 即第16位是正月，第15位是二月，依此类推
    if LUNAR_INFO[year - 1900] & (0x10000 >> month):
        return 30
    return 29


def _get_lunar_year_days(year: int) -> int:
    """获取农历年的总天数"""
    total = 0
    for month in range(1, 13):
        total += _get_lunar_month_days(year, month)
    total += _get_leap_month_days(year)
    return total


def solar_to_lunar(year: int, month: int, day: int) -> Optional[LunarDate]:
    """
    公历转农历
    
    Args:
        year: 公历年
        month: 公历月
        day: 公历日
    
    Returns:
        LunarDate 对象，如果转换失败返回 None
    """
    # 验证输入范围
    if not (1900 <= year <= 2100):
        return None
    
    try:
        solar_date = date(year, month, day)
    except ValueError:
        return None
    
    # 农历1900年1月1日对应公历1900年1月31日
    # 农历年的第一天
    base_date = date(1900, 1, 31)
    
    # 计算天数偏移
    offset = (solar_date - base_date).days
    if offset < 0:
        return None
    
    # 计算农历年
    lunar_year = 1900
    year_days = 0
    
    while lunar_year <= 2100 and offset >= 0:
        year_days = _get_lunar_year_days(lunar_year)
        offset -= year_days
        lunar_year += 1
    
    lunar_year -= 1
    offset += year_days
    
    if lunar_year > 2100:
        return None
    
    # 计算闰月
    leap_month = _get_leap_month(lunar_year)
    leap_days = _get_leap_month_days(lunar_year)
    
    # 计算农历月
    lunar_month = 1
    is_leap = False
    
    while lunar_month <= 12 and offset >= 0:
        # 正常月天数
        month_days = _get_lunar_month_days(lunar_year, lunar_month)
        
        # 如果有闰月且当前月正好是闰月前的那个月
        # 处理完正常月后，还要处理闰月
        if leap_month > 0 and lunar_month == leap_month and not is_leap:
            # 先处理正常月
            if offset < month_days:
                break
            offset -= month_days
            lunar_month += 1
            # 继续处理闰月（将is_leap设为True但lunar_month保持不变）
            is_leap = True
            month_days = leap_days
            if offset < month_days:
                lunar_month = leap_month  # 回退到闰月
                break
            offset -= month_days
            is_leap = False
        else:
            if offset < month_days:
                break
            offset -= month_days
            lunar_month += 1
    
    # 计算农历日
    lunar_day = offset + 1
    
    # 检查有效性
    if lunar_month > 12:
        lunar_month = 12
        lunar_day = _get_lunar_month_days(lunar_year, 12)
    
    return LunarDate(lunar_year, lunar_month, lunar_day, is_leap)


def lunar_to_solar(year: int, month: int, day: int, is_leap_month: bool = False) -> Optional[date]:
    """
    农历转公历
    
    Args:
        year: 农历年
        month: 农历月
        day: 农历日
        is_leap_month: 是否是闰月
    
    Returns:
        date 对象，如果转换失败返回 None
    """
    # 验证输入
    if not (1900 <= year <= 2100):
        return None
    
    if not (1 <= month <= 12):
        return None
    
    leap_month = _get_leap_month(year)
    
    # 闰月必须是存在的闰月
    if is_leap_month and month != leap_month:
        return None
    
    # 日期验证
    if is_leap_month:
        max_day = _get_leap_month_days(year)
    else:
        max_day = _get_lunar_month_days(year, month)
    
    if not (1 <= day <= max_day):
        return None
    
    # 农历1900年1月1日对应公历1900年1月31日
    base_date = date(1900, 1, 31)
    offset = 0
    
    # 累加年天数
    for y in range(1900, year):
        offset += _get_lunar_year_days(y)
    
    # 累加月天数
    for m in range(1, month):
        offset += _get_lunar_month_days(year, m)
        # 如果这个月是闰月前的月，需要加上闰月天数
        if leap_month > 0 and m == leap_month:
            offset += _get_leap_month_days(year)
    
    # 如果是闰月，加上正常月的天数
    if is_leap_month:
        offset += _get_lunar_month_days(year, month)
    
    # 加上日期偏移
    offset += day - 1
    
    return base_date + timedelta(days=offset)


# ==================== 干支计算 ====================

def get_year_ganzhi(year: int) -> str:
    """
    获取年份的干支
    
    Args:
        year: 年份
    
    Returns:
        干支字符串，如"甲子"
    """
    # 以1984年为甲子年（起点）
    offset = year - 1984
    gan_index = offset % 10
    zhi_index = offset % 12
    if gan_index < 0:
        gan_index += 10
    if zhi_index < 0:
        zhi_index += 12
    return TIAN_GAN[gan_index] + DI_ZHI[zhi_index]


def get_month_ganzhi(year: int, month: int) -> str:
    """
    获取月份的干支
    
    Args:
        year: 年份
        month: 月份（1-12）
    
    Returns:
        干支字符串
    """
    # 月干支计算（简化版）
    year_gan_index = (year - 1984) % 10
    if year_gan_index < 0:
        year_gan_index += 10
    
    month_gan_index = (year_gan_index * 2 + month - 1) % 10
    month_zhi_index = (month + 1) % 12
    
    return TIAN_GAN[month_gan_index] + DI_ZHI[month_zhi_index]


def get_day_ganzhi(year: int, month: int, day: int) -> str:
    """
    获取日期的干支
    
    Args:
        year: 年份
        month: 月份
        day: 日期
    
    Returns:
        干支字符串
    """
    # 以1900年1月1日为甲戌日
    base_date = date(1900, 1, 1)
    try:
        target_date = date(year, month, day)
    except ValueError:
        return ""
    
    offset = (target_date - base_date).days
    
    # 1900年1月1日：天干甲(0)，地支戌(10)
    gan_index = offset % 10
    zhi_index = (offset + 10) % 12
    
    return TIAN_GAN[gan_index] + DI_ZHI[zhi_index]


def get_hour_ganzhi(day_ganzhi: str, hour: int) -> str:
    """
    获取时辰的干支
    
    Args:
        day_ganzhi: 日干支
        hour: 小时（0-23）
    
    Returns:
        时辰干支
    """
    # 时辰地支对应
    zhi_map = [
        (23, 1), (1, 3), (3, 5), (5, 7), (7, 9), (9, 11),
        (11, 13), (13, 15), (15, 17), (17, 19), (19, 21), (21, 23)
    ]
    
    zhi_index = 0
    for i, (start, end) in enumerate(zhi_map):
        if start == 23:
            if hour >= 23 or hour < 1:
                zhi_index = i
                break
        else:
            if start <= hour < end:
                zhi_index = i
                break
    
    # 时干根据日干推算
    day_gan = day_ganzhi[0] if day_ganzhi else '甲'
    day_gan_index = TIAN_GAN.index(day_gan)
    
    hour_gan_index = (day_gan_index % 5 * 2 + zhi_index) % 10
    
    return TIAN_GAN[hour_gan_index] + DI_ZHI[zhi_index]


# ==================== 生肖计算 ====================

def get_zodiac(year: int) -> str:
    """
    获取生肖
    
    Args:
        year: 年份
    
    Returns:
        生肖字符串
    """
    # 1900年是鼠年
    zodiac_index = (year - 1900) % 12
    if zodiac_index < 0:
        zodiac_index += 12
    return ZODIAC[zodiac_index]


# ==================== 星座计算 ====================

def get_constellation(month: int, day: int) -> str:
    """
    获取星座
    
    Args:
        month: 月份（1-12）
        day: 日期
    
    Returns:
        星座名称
    """
    if not (1 <= month <= 12 and 1 <= day <= 31):
        return "未知"
    
    # 星座日期范围
    constellations = [
        (20, "水瓶座"), (19, "双鱼座"), (21, "白羊座"), (20, "金牛座"),
        (21, "双子座"), (22, "巨蟹座"), (23, "狮子座"), (23, "处女座"),
        (23, "天秤座"), (24, "天蝎座"), (23, "射手座"), (22, "摩羯座")
    ]
    
    if day < constellations[month - 1][0]:
        if month == 1:
            return "摩羯座"
        else:
            return constellations[month - 2][1]
    else:
        return constellations[month - 1][1]


# ==================== 节气计算 ====================

def get_solar_term_year(year: int) -> List[Tuple[str, date]]:
    """
    获取一年的24节气日期
    
    Args:
        year: 年份
    
    Returns:
        节气名称和日期的列表
    """
    # 节气基准日期（近似值）
    term_days = [
        (1, 6), (1, 20), (2, 4), (2, 19), (3, 6), (3, 21),
        (4, 5), (4, 20), (5, 6), (5, 21), (6, 6), (6, 21),
        (7, 7), (7, 23), (8, 8), (8, 23), (9, 8), (9, 23),
        (10, 8), (10, 24), (11, 8), (11, 22), (12, 7), (12, 22)
    ]
    
    result = []
    for i, (m, d) in enumerate(term_days):
        # 年份修正
        year_offset = (year - 1900) % 4
        adjusted_d = d + year_offset // 2
        
        # 确保日期有效
        max_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if m == 2 and (year % 400 == 0 or (year % 100 != 0 and year % 4 == 0)):
            max_days[1] = 29
        
        adjusted_d = min(adjusted_d, max_days[m - 1])
        
        result.append((SOLAR_TERMS[i], date(year, m, adjusted_d)))
    
    return result


def get_current_solar_term(year: int, month: int, day: int) -> Tuple[str, int]:
    """
    获取当前节气和距离下一个节气的天数
    
    Args:
        year: 年份
        month: 月份
        day: 日期
    
    Returns:
        (当前节气名称, 距离下一个节气天数)
    """
    try:
        target_date = date(year, month, day)
    except ValueError:
        return ("", 0)
    
    terms = get_solar_term_year(year)
    
    current_term = ""
    days_to_next = 0
    
    for i, (name, term_date) in enumerate(terms):
        if term_date <= target_date:
            current_term = name
        else:
            days_to_next = (term_date - target_date).days
            break
    
    return (current_term, days_to_next)


# ==================== 节日查询 ====================

def get_lunar_festival(year: int, month: int, day: int, is_leap: bool = False) -> Optional[str]:
    """
    获取农历节日
    
    Args:
        year: 农历年
        month: 农历月
        day: 农历日
        is_leap: 是否是闰月
    
    Returns:
        节日名称，如果不是节日返回 None
    """
    if is_leap:
        return None
    
    # 除夕是腊月最后一天
    if month == 12:
        last_day = _get_lunar_month_days(year, 12)
        if day == last_day:
            return "除夕"
    
    return LUNAR_FESTIVALS.get((month, day))


def get_solar_festival(month: int, day: int) -> Optional[str]:
    """
    获取公历节日
    
    Args:
        month: 月份
        day: 日期
    
    Returns:
        节日名称，如果不是节日返回 None
    """
    return SOLAR_FESTIVALS.get((month, day))


def get_all_festivals(year: int, month: int, day: int) -> List[str]:
    """
    获取所有节日（公历和农历）
    
    Args:
        year: 公历年
        month: 公历月
        day: 公历日
    
    Returns:
        节日名称列表
    """
    festivals = []
    
    solar_fest = get_solar_festival(month, day)
    if solar_fest:
        festivals.append(solar_fest)
    
    lunar = solar_to_lunar(year, month, day)
    if lunar:
        lunar_fest = get_lunar_festival(lunar.year, lunar.month, lunar.day, lunar.is_leap_month)
        if lunar_fest:
            festivals.append(lunar_fest)
    
    return festivals


# ==================== 辅助函数 ====================

def format_lunar_date(lunar_date: LunarDate) -> str:
    """
    格式化农历日期为中文
    
    Args:
        lunar_date: 农历日期对象
    
    Returns:
        格式化的中文日期字符串
    """
    year_ganzhi = get_year_ganzhi(lunar_date.year)
    zodiac = get_zodiac(lunar_date.year)
    
    result = f"{year_ganzhi}年（{zodiac}年）"
    
    if lunar_date.is_leap_month:
        result += " 闰"
    
    result += LUNAR_MONTH_NAMES.get(lunar_date.month, f"{lunar_date.month}月")
    result += LUNAR_DAY_NAMES.get(lunar_date.day, f"{lunar_date.day}日")
    
    return result


def get_lunar_info(year: int, month: int, day: int) -> Dict:
    """
    获取指定公历日期的农历信息
    
    Args:
        year: 公历年
        month: 公历月
        day: 公历日
    
    Returns:
        包含农历信息的字典
    """
    result = {
        'solar_date': f"{year}-{month:02d}-{day:02d}",
        'lunar_date': None,
        'year_ganzhi': None,
        'zodiac': None,
        'constellation': None,
        'solar_term': None,
        'festivals': [],
        'lunar_month_name': None,
        'lunar_day_name': None,
    }
    
    lunar = solar_to_lunar(year, month, day)
    if lunar:
        result['lunar_date'] = str(lunar)
        result['year_ganzhi'] = get_year_ganzhi(lunar.year)
        result['zodiac'] = get_zodiac(lunar.year)
        result['lunar_month_name'] = LUNAR_MONTH_NAMES.get(lunar.month)
        result['lunar_day_name'] = LUNAR_DAY_NAMES.get(lunar.day)
    
    result['constellation'] = get_constellation(month, day)
    
    term, _ = get_current_solar_term(year, month, day)
    result['solar_term'] = term
    
    result['festivals'] = get_all_festivals(year, month, day)
    
    return result


def is_leap_year_lunar(year: int) -> bool:
    """
    判断农历年是否有闰月
    
    Args:
        year: 农历年
    
    Returns:
        是否有闰月
    """
    return _get_leap_month(year) != 0


def get_leap_month(year: int) -> int:
    """
    获取闰月月份
    
    Args:
        year: 农历年
    
    Returns:
        闰月月份，0表示无闰月
    """
    return _get_leap_month(year)


def get_leap_month_days(year: int) -> int:
    """
    获取闰月天数
    
    Args:
        year: 农历年
    
    Returns:
        闰月天数，0表示无闰月
    """
    return _get_leap_month_days(year)


def get_lunar_month_days(year: int, month: int) -> int:
    """
    获取农历月天数
    
    Args:
        year: 农历年
        month: 农历月
    
    Returns:
        月天数
    """
    return _get_lunar_month_days(year, month)


def get_lunar_year_days(year: int) -> int:
    """
    获取农历年天数
    
    Args:
        year: 农历年
    
    Returns:
        年天数
    """
    return _get_lunar_year_days(year)


def get_chinese_age(birth_year: int, current_year: int) -> int:
    """
    计算虚岁（中国年龄）
    
    Args:
        birth_year: 出生年份
        current_year: 当前年份
    
    Returns:
        虚岁
    """
    return current_year - birth_year + 1


# ==================== 类封装 ====================

class LunarCalendar:
    """农历日历类，提供完整的农历信息"""
    
    def __init__(self, year: int, month: int = None, day: int = None):
        """
        初始化
        
        Args:
            year: 年份（公历）
            month: 月份（可选）
            day: 日期（可选）
        """
        self.solar_year = year
        self.solar_month = month
        self.solar_day = day
        
        self._lunar_date = None
        if month and day:
            self._lunar_date = solar_to_lunar(year, month, day)
    
    def get_lunar_date(self) -> Optional[LunarDate]:
        """获取农历日期"""
        return self._lunar_date
    
    def get_year_info(self) -> Dict:
        """获取年份信息"""
        return {
            'year': self.solar_year,
            'ganzhi': get_year_ganzhi(self.solar_year),
            'zodiac': get_zodiac(self.solar_year),
            'is_leap_year': is_leap_year_lunar(self.solar_year),
            'leap_month': get_leap_month(self.solar_year),
        }
    
    def get_solar_terms(self) -> List[Tuple[str, date]]:
        """获取一年所有节气"""
        return get_solar_term_year(self.solar_year)
    
    def convert_to_lunar(self, month: int, day: int) -> Optional[LunarDate]:
        """将公历日期转换为农历"""
        return solar_to_lunar(self.solar_year, month, day)
    
    def convert_to_solar(self, lunar_month: int, lunar_day: int, is_leap: bool = False) -> Optional[date]:
        """将农历日期转换为公历"""
        return lunar_to_solar(self.solar_year, lunar_month, lunar_day, is_leap)
    
    def get_month_calendar(self, month: int) -> List[Dict]:
        """
        获取某月的日历（包含公历和农历信息）
        
        Args:
            month: 公历月份
        
        Returns:
            日历列表
        """
        import calendar
        
        cal = calendar.monthcalendar(self.solar_year, month)
        result = []
        
        for week in cal:
            week_data = []
            for day in week:
                if day == 0:
                    week_data.append(None)
                else:
                    lunar = solar_to_lunar(self.solar_year, month, day)
                    festivals = get_all_festivals(self.solar_year, month, day)
                    week_data.append({
                        'solar': date(self.solar_year, month, day),
                        'lunar': lunar,
                        'festivals': festivals,
                    })
            result.append(week_data)
        
        return result


# ==================== 便捷函数 ====================

def today_lunar() -> Optional[LunarDate]:
    """获取今天的农历日期"""
    today = date.today()
    return solar_to_lunar(today.year, today.month, today.day)


def today_info() -> Dict:
    """获取今天的完整农历信息"""
    today = date.today()
    return get_lunar_info(today.year, today.month, today.day)


def quick_convert(solar_date: date) -> str:
    """快速转换公历为农历字符串"""
    lunar = solar_to_lunar(solar_date.year, solar_date.month, solar_date.day)
    if lunar:
        return format_lunar_date(lunar)
    return ""


if __name__ == "__main__":
    # 简单测试
    print("=" * 50)
    print("农历日历工具模块测试")
    print("=" * 50)
    
    # 今天的信息
    print("\n今天的农历信息:")
    info = today_info()
    for k, v in info.items():
        print(f"  {k}: {v}")
    
    # 公历转农历
    print("\n公历转农历测试:")
    lunar = solar_to_lunar(2024, 2, 10)
    print(f"  2024年2月10日 -> {lunar}")
    print(f"  格式化: {format_lunar_date(lunar)}")
    
    # 农历转公历
    print("\n农历转公历测试:")
    solar = lunar_to_solar(2024, 1, 1)
    print(f"  农历2024年正月初一 -> {solar}")
    
    # 节气
    print("\n2024年节气:")
    terms = get_solar_term_year(2024)
    for name, d in terms[:6]:
        print(f"  {name}: {d}")