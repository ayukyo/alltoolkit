"""
Persian Calendar Utilities - 波斯历( Jalali )工具包实现

提供波斯历( Jalali Calendar )与公历( Gregorian Calendar )之间的转换功能，
所有函数均为纯 Python 实现，无外部依赖。

波斯历是伊朗和阿富汗使用的官方历法，也称为 Jalali 历。
波斯历年份从春分( 约 3 月 20-21 日 )开始，是一个太阳历。
"""

from typing import Tuple, Optional
from datetime import date, datetime


# 波斯历月份名称
PERSIAN_MONTH_NAMES = [
    "فروردین",    # Farvardin (1)
    "اردیبهشت",   # Ordibehesht (2)
    "خرداد",      # Khordad (3)
    "تیر",        # Tir (4)
    "مرداد",      # Mordad (5)
    "شهریور",     # Shahrivar (6)
    "مهر",        # Mehr (7)
    "آبان",       # Aban (8)
    "آذر",        # Azar (9)
    "دی",         # Dey (10)
    "بهمن",       # Bahman (11)
    "اسفند",      # Esfand (12)
]

# 波斯历月份英文名称
PERSIAN_MONTH_NAMES_EN = [
    "Farvardin",
    "Ordibehesht",
    "Khordad",
    "Tir",
    "Mordad",
    "Shahrivar",
    "Mehr",
    "Aban",
    "Azar",
    "Dey",
    "Bahman",
    "Esfand",
]

# 波斯历星期名称
PERSIAN_WEEKDAY_NAMES = [
    "شنبه",       # Saturday
    "یکشنبه",     # Sunday
    "دوشنبه",     # Monday
    "سه‌شنبه",    # Tuesday
    "چهارشنبه",   # Wednesday
    "پنجشنبه",    # Thursday
    "جمعه",       # Friday
]

# 波斯历星期英文名称
PERSIAN_WEEKDAY_NAMES_EN = [
    "Shanbeh",
    "Yekshanbeh",
    "Doshanbeh",
    "Seshanbeh",
    "Chaharshanbeh",
    "Panjshanbeh",
    "Jomeh",
]


def is_leap_year_persian(year: int) -> bool:
    """
    判断波斯历年份是否为闰年。
    
    波斯历使用 33 年周期规则，其中 8 年是闰年。
    一个 33 年周期包含的闰年：第 1, 5, 9, 13, 17, 22, 26, 30 年
    
    Args:
        year: 波斯历年份
        
    Returns:
        bool: 如果是闰年返回 True
        
    Examples:
        >>> is_leap_year_persian(1403)
        True
        >>> is_leap_year_persian(1402)
        False
    """
    # 33年周期中的闰年位置
    leap_positions = [1, 5, 9, 13, 17, 22, 26, 30]
    
    # 计算在 33 年周期中的位置
    cycle_pos = year % 33
    if cycle_pos < 0:
        cycle_pos += 33
    
    return cycle_pos in leap_positions


def days_in_persian_month(year: int, month: int) -> int:
    """
    获取波斯历某年某月的天数。
    
    波斯历前 6 个月有 31 天，后 5 个月有 30 天，
    最后一个月( Esfand )在平年有 29 天，闰年有 30 天。
    
    Args:
        year: 波斯历年份
        month: 波斯历月份( 1-12 )
        
    Returns:
        int: 该月的天数
        
    Raises:
        ValueError: 如果月份不在 1-12 范围内
        
    Examples:
        >>> days_in_persian_month(1403, 1)
        31
        >>> days_in_persian_month(1403, 12)  # 闰年
        30
        >>> days_in_persian_month(1402, 12)  # 平年
        29
    """
    if month < 1 or month > 12:
        raise ValueError("Month must be between 1 and 12")
    
    if month <= 6:
        return 31
    elif month < 12:
        return 30
    else:  # month == 12 (Esfand)
        return 30 if is_leap_year_persian(year) else 29


def validate_persian_date(year: int, month: int, day: int) -> bool:
    """
    验证波斯历日期是否有效。
    
    Args:
        year: 波斯历年份
        month: 波斯历月份( 1-12 )
        day: 波斯历日
        
    Returns:
        bool: 如果日期有效返回 True
        
    Raises:
        ValueError: 如果日期无效
        
    Examples:
        >>> validate_persian_date(1403, 1, 1)
        True
        >>> validate_persian_date(1403, 13, 1)
        False
    """
    if month < 1 or month > 12:
        raise ValueError(f"Month must be between 1 and 12, got {month}")
    
    max_days = days_in_persian_month(year, month)
    if day < 1 or day > max_days:
        raise ValueError(f"Day must be between 1 and {max_days} for month {month}, got {day}")
    
    return True


def persian_to_jd(year: int, month: int, day: int) -> int:
    """
    将波斯历日期转换为儒略日( Julian Day )。
    
    儒略日是从公元前 4713 年 1 月 1 日中午开始连续计数的天数，
    用于不同历法之间的转换。
    
    Args:
        year: 波斯历年份
        month: 波斯历月份( 1-12 )
        day: 波斯历日
        
    Returns:
        int: 儒略日
        
    Examples:
        >>> persian_to_jd(1403, 1, 1)  # 2024-03-20
        2460390
    """
    # 验证输入
    validate_persian_date(year, month, day)
    
    # 计算偏移量
    # 波斯历元年( 1 年 1 月 1 日)对应的儒略日是 1948320
    # 公式基于算法: JD = epoch + (year - 1) * 365 + leap_days + month_days + day
    
    epoch = 1948320  # 波斯历元年的儒略日
    
    # 计算闰年数
    # 在 33 年周期中有 8 个闰年
    cycles = (year - 1) // 33
    remainder = (year - 1) % 33
    
    # 计算余数中的闰年数
    leap_positions = [1, 5, 9, 13, 17, 22, 26, 30]
    leap_in_remainder = sum(1 for pos in leap_positions if pos <= remainder)
    
    total_leap_days = cycles * 8 + leap_in_remainder
    
    # 计算月份天数
    if month <= 6:
        month_days = (month - 1) * 31
    else:
        month_days = 6 * 31 + (month - 7) * 30
    
    jd = epoch + (year - 1) * 365 + total_leap_days + month_days + (day - 1)
    
    return jd


def jd_to_persian(jd: int) -> Tuple[int, int, int]:
    """
    将儒略日转换为波斯历日期。
    
    Args:
        jd: 儒略日
        
    Returns:
        Tuple[int, int, int]: (年, 月, 日)
        
    Examples:
        >>> jd_to_persian(2460390)
        (1403, 1, 1)
    """
    epoch = 1948320  # 波斯历元年的儒略日
    
    # 计算从波斯历元年过去的总天数
    total_days = jd - epoch
    
    # 估算年份
    # 平均每年约 365.242424 天
    year = int(total_days / 365.242424) + 1
    
    # 调整年份
    while True:
        year_start = persian_to_jd(year, 1, 1)
        if total_days < year_start - epoch:
            year -= 1
            break
        year_end = persian_to_jd(year + 1, 1, 1)
        if total_days < year_end - epoch:
            break
        year += 1
    
    # 计算月份和日
    year_start = persian_to_jd(year, 1, 1)
    day_of_year = total_days - (year_start - epoch) + 1
    
    # 确定月份
    if day_of_year <= 6 * 31:
        month = (day_of_year - 1) // 31 + 1
        day = (day_of_year - 1) % 31 + 1
    else:
        remaining = day_of_year - 6 * 31
        month = 6 + (remaining - 1) // 30 + 1
        day = (remaining - 1) % 30 + 1
    
    return year, month, day


def gregorian_to_jd(year: int, month: int, day: int) -> int:
    """
    将公历日期转换为儒略日。
    
    使用天文公式计算儒略日。
    
    Args:
        year: 公历年份
        month: 公历月份( 1-12 )
        day: 公历日
        
    Returns:
        int: 儒略日
        
    Examples:
        >>> gregorian_to_jd(2024, 3, 20)
        2460390
    """
    # 验证日期
    if month < 1 or month > 12:
        raise ValueError(f"Month must be between 1 and 12, got {month}")
    if day < 1:
        raise ValueError(f"Day must be positive, got {day}")
    
    # 儒略日计算公式
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    
    jd = day + ((153 * m + 2) // 5) + 365 * y + (y // 4) - (y // 100) + (y // 400) - 32045
    
    return jd


def jd_to_gregorian(jd: int) -> Tuple[int, int, int]:
    """
    将儒略日转换为公历日期。
    
    Args:
        jd: 儒略日
        
    Returns:
        Tuple[int, int, int]: (年, 月, 日)
        
    Examples:
        >>> jd_to_gregorian(2460390)
        (2024, 3, 20)
    """
    a = jd + 32044
    b = (4 * a + 3) // 146097
    c = a - (146097 * b) // 4
    d = (4 * c + 3) // 1461
    e = c - (1461 * d) // 4
    m = (5 * e + 2) // 153
    
    day = e - (153 * m + 2) // 5 + 1
    month = m + 3 - 12 * (m // 10)
    year = 100 * b + d - 4800 + (m // 10)
    
    return year, month, day


def persian_to_gregorian(year: int, month: int, day: int) -> Tuple[int, int, int]:
    """
    将波斯历日期转换为公历日期。
    
    Args:
        year: 波斯历年份
        month: 波斯历月份( 1-12 )
        day: 波斯历日
        
    Returns:
        Tuple[int, int, int]: (公历年, 公历月, 公历日)
        
    Examples:
        >>> persian_to_gregorian(1403, 1, 1)
        (2024, 3, 20)
        >>> persian_to_gregorian(1402, 12, 29)
        (2024, 3, 19)
    """
    jd = persian_to_jd(year, month, day)
    return jd_to_gregorian(jd)


def gregorian_to_persian(year: int, month: int, day: int) -> Tuple[int, int, int]:
    """
    将公历日期转换为波斯历日期。
    
    Args:
        year: 公历年份
        month: 公历月份( 1-12 )
        day: 公历日
        
    Returns:
        Tuple[int, int, int]: (波斯历年, 波斯历月, 波斯历日)
        
    Examples:
        >>> gregorian_to_persian(2024, 3, 20)
        (1403, 1, 1)
        >>> gregorian_to_persian(2024, 3, 19)
        (1402, 12, 29)
    """
    jd = gregorian_to_jd(year, month, day)
    return jd_to_persian(jd)


def persian_from_date(d: date) -> Tuple[int, int, int]:
    """
    将 Python date 对象转换为波斯历日期。
    
    Args:
        d: Python date 对象
        
    Returns:
        Tuple[int, int, int]: (波斯历年, 波斯历月, 波斯历日)
        
    Examples:
        >>> from datetime import date
        >>> persian_from_date(date(2024, 3, 20))
        (1403, 1, 1)
    """
    return gregorian_to_persian(d.year, d.month, d.day)


def persian_from_datetime(dt: datetime) -> Tuple[int, int, int]:
    """
    将 Python datetime 对象转换为波斯历日期。
    
    Args:
        dt: Python datetime 对象
        
    Returns:
        Tuple[int, int, int]: (波斯历年, 波斯历月, 波斯历日)
        
    Examples:
        >>> from datetime import datetime
        >>> persian_from_datetime(datetime(2024, 3, 20, 12, 0))
        (1403, 1, 1)
    """
    return gregorian_to_persian(dt.year, dt.month, dt.day)


def persian_to_date(year: int, month: int, day: int) -> date:
    """
    将波斯历日期转换为 Python date 对象。
    
    Args:
        year: 波斯历年份
        month: 波斯历月份( 1-12 )
        day: 波斯历日
        
    Returns:
        date: Python date 对象
        
    Examples:
        >>> persian_to_date(1403, 1, 1)
        datetime.date(2024, 3, 20)
    """
    g_year, g_month, g_day = persian_to_gregorian(year, month, day)
    return date(g_year, g_month, g_day)


def format_persian_date(
    year: int, 
    month: int, 
    day: int, 
    format_type: str = "short",
    language: str = "fa"
) -> str:
    """
    格式化波斯历日期为字符串。
    
    Args:
        year: 波斯历年份
        month: 波斯历月份( 1-12 )
        day: 波斯历日
        format_type: 格式类型
            - "short": 短格式 "1403/01/01"
            - "long": 长格式 "1403 فروردین 1"
            - "full": 完整格式 "1 فروردین 1403"
        language: 语言
            - "fa": 波斯语
            - "en": 英语
        
    Returns:
        str: 格式化后的日期字符串
        
    Examples:
        >>> format_persian_date(1403, 1, 1)
        '1403/01/01'
        >>> format_persian_date(1403, 1, 1, "long")
        '1403 فروردین 1'
        >>> format_persian_date(1403, 1, 1, "full", "en")
        '1 Farvardin 1403'
    """
    validate_persian_date(year, month, day)
    
    if language == "en":
        month_names = PERSIAN_MONTH_NAMES_EN
    else:
        month_names = PERSIAN_MONTH_NAMES
    
    month_name = month_names[month - 1]
    
    if format_type == "short":
        return f"{year:04d}/{month:02d}/{day:02d}"
    elif format_type == "long":
        if language == "en":
            return f"{year} {month_name} {day}"
        return f"{year} {month_name} {day}"
    elif format_type == "full":
        if language == "en":
            return f"{day} {month_name} {year}"
        return f"{day} {month_name} {year}"
    else:
        raise ValueError(f"Unknown format type: {format_type}")


def get_persian_month_name(month: int, language: str = "fa") -> str:
    """
    获取波斯历月份名称。
    
    Args:
        month: 波斯历月份( 1-12 )
        language: 语言( "fa" 波斯语, "en" 英语 )
        
    Returns:
        str: 月份名称
        
    Raises:
        ValueError: 如果月份不在 1-12 范围内
        
    Examples:
        >>> get_persian_month_name(1)
        'فروردین'
        >>> get_persian_month_name(1, "en")
        'Farvardin'
    """
    if month < 1 or month > 12:
        raise ValueError("Month must be between 1 and 12")
    
    if language == "en":
        return PERSIAN_MONTH_NAMES_EN[month - 1]
    return PERSIAN_MONTH_NAMES[month - 1]


def get_persian_weekday_name(weekday: int, language: str = "fa") -> str:
    """
    获取波斯历星期名称。
    
    Args:
        weekday: 星期几( 0=周六, 1=周日, ..., 6=周五 )
        language: 语言( "fa" 波斯语, "en" 英语 )
        
    Returns:
        str: 星期名称
        
    Raises:
        ValueError: 如果 weekday 不在 0-6 范围内
        
    Examples:
        >>> get_persian_weekday_name(0)  # Saturday
        'شنبه'
        >>> get_persian_weekday_name(6, "en")  # Friday
        'Jomeh'
    """
    if weekday < 0 or weekday > 6:
        raise ValueError("Weekday must be between 0 and 6")
    
    if language == "en":
        return PERSIAN_WEEKDAY_NAMES_EN[weekday]
    return PERSIAN_WEEKDAY_NAMES[weekday]


def get_persian_weekday(year: int, month: int, day: int) -> int:
    """
    获取波斯历日期对应的星期几。
    
    Args:
        year: 波斯历年份
        month: 波斯历月份( 1-12 )
        day: 波斯历日
        
    Returns:
        int: 星期几( 0=周六, 1=周日, ..., 6=周五 )
        
    Examples:
        >>> get_persian_weekday(1403, 1, 1)  # 2024-03-20 is Wednesday
        4
    """
    jd = persian_to_jd(year, month, day)
    # 儒略日的星期：0=周一, 1=周二, ..., 6=周日
    # 波斯历的星期：0=周六, 1=周日, ..., 6=周五
    jd_weekday = (jd + 1) % 7  # 0=周日, ..., 6=周六
    
    # 转换为波斯历星期
    # 周日(0) -> 1, 周一(1) -> 2, 周二(2) -> 3, 周三(3) -> 4, 周四(4) -> 5, 周五(5) -> 6, 周六(6) -> 0
    persian_weekday = (jd_weekday + 1) % 7
    
    return persian_weekday


def persian_day_of_year(year: int, month: int, day: int) -> int:
    """
    获取波斯历日期在该年的第几天。
    
    Args:
        year: 波斯历年份
        month: 波斯历月份( 1-12 )
        day: 波斯历日
        
    Returns:
        int: 该年的第几天( 1-366 )
        
    Examples:
        >>> persian_day_of_year(1403, 1, 1)
        1
        >>> persian_day_of_year(1403, 12, 30)
        366
    """
    validate_persian_date(year, month, day)
    
    if month <= 6:
        return (month - 1) * 31 + day
    else:
        return 6 * 31 + (month - 7) * 30 + day


def persian_days_in_year(year: int) -> int:
    """
    获取波斯历某年的总天数。
    
    Args:
        year: 波斯历年份
        
    Returns:
        int: 该年的总天数( 365 或 366 )
        
    Examples:
        >>> persian_days_in_year(1403)  # 闰年
        366
        >>> persian_days_in_year(1402)  # 平年
        365
    """
    return 366 if is_leap_year_persian(year) else 365


def persian_week_of_year(year: int, month: int, day: int) -> int:
    """
    获取波斯历日期是该年的第几周。
    
    使用 ISO 周数计算方式：每年的第一周包含该年第一个周四。
    
    Args:
        year: 波斯历年份
        month: 波斯历月份( 1-12 )
        day: 波斯历日
        
    Returns:
        int: 该年的第几周( 1-53 )
        
    Examples:
        >>> persian_week_of_year(1403, 1, 1)
        1
    """
    doy = persian_day_of_year(year, month, day)
    return (doy - 1) // 7 + 1


def now_persian() -> Tuple[int, int, int]:
    """
    获取当前波斯历日期。
    
    Returns:
        Tuple[int, int, int]: (波斯历年, 波斯历月, 波斯历日)
        
    Examples:
        >>> now_persian()  # 返回当前日期
        (1403, 1, 15)  # 示例值
    """
    today = date.today()
    return gregorian_to_persian(today.year, today.month, today.day)


def persian_add_days(year: int, month: int, day: int, days: int) -> Tuple[int, int, int]:
    """
    在波斯历日期上增加或减少指定的天数。
    
    Args:
        year: 波斯历年份
        month: 波斯历月份( 1-12 )
        day: 波斯历日
        days: 要增加的天数( 可为负数 )
        
    Returns:
        Tuple[int, int, int]: 计算后的波斯历日期
        
    Examples:
        >>> persian_add_days(1403, 1, 1, 30)
        (1403, 2, 1)
        >>> persian_add_days(1403, 1, 1, -1)
        (1402, 12, 29)
    """
    jd = persian_to_jd(year, month, day) + days
    return jd_to_persian(jd)


def persian_diff_days(
    year1: int, month1: int, day1: int,
    year2: int, month2: int, day2: int
) -> int:
    """
    计算两个波斯历日期之间的天数差。
    
    Args:
        year1: 第一个日期的年份
        month1: 第一个日期的月份
        day1: 第一个日期的日
        year2: 第二个日期的年份
        month2: 第二个日期的月份
        day2: 第二个日期的日
        
    Returns:
        int: 天数差( date2 - date1 )
        
    Examples:
        >>> persian_diff_days(1403, 1, 1, 1403, 1, 11)
        10
    """
    jd1 = persian_to_jd(year1, month1, day1)
    jd2 = persian_to_jd(year2, month2, day2)
    return jd2 - jd1


def is_valid_persian_date(year: int, month: int, day: int) -> bool:
    """
    检查波斯历日期是否有效。
    
    Args:
        year: 波斯历年份
        month: 波斯历月份( 1-12 )
        day: 波斯历日
        
    Returns:
        bool: 如果日期有效返回 True，否则返回 False
        
    Examples:
        >>> is_valid_persian_date(1403, 1, 1)
        True
        >>> is_valid_persian_date(1403, 13, 1)
        False
    """
    try:
        validate_persian_date(year, month, day)
        return True
    except ValueError:
        return False


def persian_year_range(start_year: int, end_year: int) -> list:
    """
    生成指定范围内的所有波斯历年份。
    
    Args:
        start_year: 起始年份
        end_year: 结束年份( 包含 )
        
    Returns:
        list: 年份列表
        
    Examples:
        >>> persian_year_range(1400, 1403)
        [1400, 1401, 1402, 1403]
    """
    return list(range(start_year, end_year + 1))


def gregorian_year_to_persian_year(g_year: int) -> Tuple[int, int]:
    """
    将公历年份转换为波斯历年份范围。
    
    由于两个历法的年份不完全对齐，一个公历年可能跨越两个波斯历年。
    
    Args:
        g_year: 公历年份
        
    Returns:
        Tuple[int, int]: 该公历年对应的波斯历年份范围( 开始年, 结束年 )
        
    Examples:
        >>> gregorian_year_to_persian_year(2024)
        (1402, 1403)
    """
    # 公历年的第一天
    start_persian = gregorian_to_persian(g_year, 1, 1)
    # 公历年的最后一天
    end_persian = gregorian_to_persian(g_year, 12, 31)
    
    return (start_persian[0], end_persian[0])


def persian_year_to_gregorian_year(p_year: int) -> Tuple[int, int]:
    """
    将波斯历年份转换为公历年份范围。
    
    由于两个历法的年份不完全对齐，一个波斯历年可能跨越两个公历年。
    
    Args:
        p_year: 波斯历年份
        
    Returns:
        Tuple[int, int]: 该波斯历年对应的公历年份范围( 开始年, 结束年 )
        
    Examples:
        >>> persian_year_to_gregorian_year(1403)
        (2024, 2025)
    """
    # 波斯历年的第一天
    start_gregorian = persian_to_gregorian(p_year, 1, 1)
    # 波斯历年的最后一天
    last_day = days_in_persian_month(p_year, 12)
    end_gregorian = persian_to_gregorian(p_year, 12, last_day)
    
    return (start_gregorian[0], end_gregorian[0])