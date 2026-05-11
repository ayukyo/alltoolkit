"""
Sunrise/Sunset Calculator Utils
日出日落时间计算工具

基于 Jean Meeus 天文算法的纯 Python 实现，零外部依赖。
"""

from .sunrise_sunset_utils import (
    # 主要函数
    calculate_sunrise_sunset,
    calculate_civil_twilight,
    calculate_nautical_twilight,
    calculate_astronomical_twilight,
    calculate_golden_hour,
    calculate_blue_hour,
    calculate_solar_position,
    is_daylight,
    get_sun_times_summary,
    get_sun_times_for_city,
    calculate_day_length_year,
    # 常量
    CITIES,
    # 内部函数（高级用户）
    _to_julian_day,
    _from_julian_day,
    _solar_mean_anomaly,
    _equation_of_center,
    _ecliptic_longitude,
    _solar_declination,
    _equation_of_time,
    _hour_angle,
    _format_duration,
)

__all__ = [
    'calculate_sunrise_sunset',
    'calculate_civil_twilight',
    'calculate_nautical_twilight',
    'calculate_astronomical_twilight',
    'calculate_golden_hour',
    'calculate_blue_hour',
    'calculate_solar_position',
    'is_daylight',
    'get_sun_times_summary',
    'get_sun_times_for_city',
    'calculate_day_length_year',
    'CITIES',
]

__version__ = '1.0.0'
__author__ = 'AllToolkit'