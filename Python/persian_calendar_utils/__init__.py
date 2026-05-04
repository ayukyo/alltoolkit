"""
Persian Calendar Utilities - 波斯历( Jalali )工具包

提供波斯历与公历之间的转换功能，包括：
- 日期转换（波斯历 <-> 公历）
- 儒略日转换
- 闰年判断
- 日期格式化（波斯语/英语）
- 月份和星期名称
- 日期计算（加减天数、天数差）

零外部依赖，纯 Python 实现。
"""

from .persian_calendar_utils import (
    is_leap_year_persian,
    days_in_persian_month,
    validate_persian_date,
    persian_to_jd,
    jd_to_persian,
    gregorian_to_jd,
    jd_to_gregorian,
    persian_to_gregorian,
    gregorian_to_persian,
    persian_from_date,
    persian_from_datetime,
    persian_to_date,
    format_persian_date,
    get_persian_month_name,
    get_persian_weekday_name,
    get_persian_weekday,
    persian_day_of_year,
    persian_days_in_year,
    persian_week_of_year,
    now_persian,
    persian_add_days,
    persian_diff_days,
    is_valid_persian_date,
    gregorian_year_to_persian_year,
    persian_year_to_gregorian_year,
    PERSIAN_MONTH_NAMES,
    PERSIAN_MONTH_NAMES_EN,
    PERSIAN_WEEKDAY_NAMES,
    PERSIAN_WEEKDAY_NAMES_EN,
)

__all__ = [
    "is_leap_year_persian",
    "days_in_persian_month",
    "validate_persian_date",
    "persian_to_jd",
    "jd_to_persian",
    "gregorian_to_jd",
    "jd_to_gregorian",
    "persian_to_gregorian",
    "gregorian_to_persian",
    "persian_from_date",
    "persian_from_datetime",
    "persian_to_date",
    "format_persian_date",
    "get_persian_month_name",
    "get_persian_weekday_name",
    "get_persian_weekday",
    "persian_day_of_year",
    "persian_days_in_year",
    "persian_week_of_year",
    "now_persian",
    "persian_add_days",
    "persian_diff_days",
    "is_valid_persian_date",
    "gregorian_year_to_persian_year",
    "persian_year_to_gregorian_year",
    "PERSIAN_MONTH_NAMES",
    "PERSIAN_MONTH_NAMES_EN",
    "PERSIAN_WEEKDAY_NAMES",
    "PERSIAN_WEEKDAY_NAMES_EN",
]

__version__ = "1.0.0"