"""
Solar Utils - 日出日落时间计算工具

提供零依赖的日出、日落、正午、曙暮光时间计算。
基于天文算法实现，精度可达分钟级别。

功能：
- 日出/日落时间计算
- 正午时间计算
- 曙暮光时间（民用、航海、天文）
- 太阳位置（方位角、高度角）
- 白昼时长计算
- 黄金时刻计算
- 支持任意日期和经纬度
"""

import math
from datetime import datetime, date, time, timedelta
from typing import Optional, Tuple, Dict, Any


# 常量定义
DEG_TO_RAD = math.pi / 180.0
RAD_TO_DEG = 180.0 / math.pi
MINUTES_PER_DAY = 1440.0
J2000 = 2451545.0  # J2000纪元儒略日

# 太阳参数
SUN_DECLINATION_COEFF = 0.0145  # 太阳赤纬变化系数

# 曙暮光角度定义（太阳在地平线下的角度）
TWILIGHT_CIVIL = 6.0      # 民用曙暮光：太阳在地平线下6度
TWILIGHT_NAUTICAL = 12.0  # 航海曙暮光：太阳在地平线下12度
TWILIGHT_ASTRONOMICAL = 18.0  # 天文曙暮光：太阳在地平线下18度

# 太阳视半径（用于日出日落计算）
SUN_RADIUS = 0.833  # 太阳视半径（度）

# 大气折射修正
ATMOSPHERIC_REFRACTION = 0.5667  # 大气折射修正（度）


def _julian_day(d: date) -> float:
    """
    计算儒略日
    
    Args:
        d: 日期对象
        
    Returns:
        儒略日数
    """
    year = d.year
    month = d.month
    day = d.day
    
    # 1月和2月视为上一年的13月和14月
    if month <= 2:
        year -= 1
        month += 12
    
    # 格里高利历修正
    a = year // 100
    b = 2 - a + a // 4
    
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b - 1524.5
    return jd


def _julian_century(jd: float) -> float:
    """
    计算从J2000纪元开始的儒略世纪数
    
    Args:
        jd: 儒略日
        
    Returns:
        儒略世纪数
    """
    return (jd - J2000) / 36525.0


def _solar_mean_anomaly(t: float) -> float:
    """
    计算太阳平近点角
    
    Args:
        t: 儒略世纪数
        
    Returns:
        太阳平近点角（弧度）
    """
    m = 357.52911 + 35999.05029 * t - 0.0001537 * t * t
    return (m % 360.0) * DEG_TO_RAD


def _solar_equation_of_center(t: float, m: float) -> float:
    """
    计算太阳中心差
    
    Args:
        t: 儒略世纪数
        m: 太阳平近点角（弧度）
        
    Returns:
        太阳中心差（度）
    """
    m_deg = m * RAD_TO_DEG
    c = (1.914602 - 0.004817 * t - 0.000014 * t * t) * math.sin(m)
    c += (0.019993 - 0.000101 * t) * math.sin(2 * m)
    c += 0.000289 * math.sin(3 * m)
    return c


def _solar_true_longitude(t: float) -> float:
    """
    计算太阳真黄经
    
    Args:
        t: 儒略世纪数
        
    Returns:
        太阳真黄经（度）
    """
    m = _solar_mean_anomaly(t)
    c = _solar_equation_of_center(t, m)
    
    # 太阳平黄经
    l0 = 280.46646 + 36000.76983 * t + 0.0003032 * t * t
    l0 = l0 % 360.0
    
    # 真黄经 = 平黄经 + 中心差
    true_long = l0 + c
    
    # 地球轨道离心率修正
    e = 0.016708634 - 0.000042037 * t - 0.0000001267 * t * t
    omega = 125.04 - 1934.136 * t
    
    # 最终修正
    true_long = true_long - 0.00569 - 0.00478 * math.sin(omega * DEG_TO_RAD)
    
    return true_long % 360.0


def _solar_apparent_longitude(t: float) -> float:
    """
    计算太阳视黄经（经过章动和光行差修正）
    
    Args:
        t: 儒略世纪数
        
    Returns:
        太阳视黄经（度）
    """
    true_long = _solar_true_longitude(t)
    
    # 章动修正
    omega = 125.04 - 1934.136 * t
    delta_psi = -0.00569 - 0.00478 * math.sin(omega * DEG_TO_RAD)
    
    return true_long + delta_psi


def _solar_declination(t: float) -> float:
    """
    计算太阳赤纬
    
    Args:
        t: 儒略世纪数
        
    Returns:
        太阳赤纬（度）
    """
    # 太阳视黄经
    lambda_sun = _solar_apparent_longitude(t) * DEG_TO_RAD
    
    # 黄赤交角
    epsilon = 23.439291 - 0.013004167 * t - 1.64e-7 * t * t + 5.04e-7 * t * t * t
    epsilon_rad = epsilon * DEG_TO_RAD
    
    # 太阳赤纬 = arcsin(sin(epsilon) * sin(lambda))
    declination = math.asin(math.sin(epsilon_rad) * math.sin(lambda_sun))
    
    return declination * RAD_TO_DEG


def _equation_of_time(t: float) -> float:
    """
    计算时差（太阳时与标准时的差异）
    
    Args:
        t: 儒略世纪数
        
    Returns:
        时差（分钟）
    """
    epsilon = 23.439291 - 0.013004167 * t
    epsilon_rad = epsilon * DEG_TO_RAD
    
    lambda_sun = _solar_apparent_longitude(t) * DEG_TO_RAD
    
    y = math.tan(epsilon_rad / 2) ** 2
    
    eot = y * math.sin(2 * lambda_sun)
    eot -= 2 * (0.016708634 - 0.000042037 * t) * math.sin(_solar_mean_anomaly(t))
    eot += 4 * (0.016708634 - 0.000042037 * t) * y * math.sin(_solar_mean_anomaly(t)) * math.cos(2 * lambda_sun)
    eot -= 0.5 * y * y * math.sin(4 * lambda_sun)
    eot -= 1.25 * (0.016708634 - 0.000042037 * t) ** 2 * math.sin(2 * _solar_mean_anomaly(t))
    
    # 转换为分钟
    eot_minutes = eot * RAD_TO_DEG * 4
    
    return eot_minutes


def _hour_angle(latitude: float, declination: float, altitude: float) -> Optional[float]:
    """
    计算时角
    
    Args:
        latitude: 纬度（度）
        declination: 太阳赤纬（度）
        altitude: 太阳高度角（度）
        
    Returns:
        时角（度），如果太阳不升起或不落下则返回 None
    """
    lat_rad = latitude * DEG_TO_RAD
    dec_rad = declination * DEG_TO_RAD
    alt_rad = altitude * DEG_TO_RAD
    
    # 时角公式
    cos_ha = (math.sin(alt_rad) - math.sin(lat_rad) * math.sin(dec_rad)) / \
             (math.cos(lat_rad) * math.cos(dec_rad))
    
    # 检查是否在有效范围内
    if cos_ha < -1:
        return 180.0  # 极昼
    elif cos_ha > 1:
        return None  # 极夜
    
    return math.acos(cos_ha) * RAD_TO_DEG


def _time_from_hour_angle(ha: float, longitude: float, eot: float, timezone: float) -> float:
    """
    从时角计算时间
    
    Args:
        ha: 时角（度），日出传入正值，日落传入负值
        longitude: 经度（度）
        eot: 时差（分钟）
        timezone: 时区（小时）
        
    Returns:
        时间（小时）
    """
    # 本地时间 = 12 ± 时角/15 + 时差/60 + (时区 - 经度/15)
    # 日出：时角为正（太阳还没到正午），使用 -时角/15
    # 日落：时角为负（太阳已过正午），使用 +时角/15
    
    local_time = 12 - ha / 15.0 + eot / 60.0 + (timezone - longitude / 15.0)
    
    # 处理跨越午夜的情况
    while local_time < 0:
        local_time += 24
    while local_time >= 24:
        local_time -= 24
        
    return local_time


def _decimal_to_time(decimal_hours: float) -> Tuple[int, int, int]:
    """
    将十进制小时转换为时分秒
    
    Args:
        decimal_hours: 十进制小时
        
    Returns:
        (小时, 分钟, 秒)
    """
    hours = int(decimal_hours)
    minutes_decimal = (decimal_hours - hours) * 60
    minutes = int(minutes_decimal)
    seconds = int((minutes_decimal - minutes) * 60)
    
    return (hours, minutes, seconds)


def _time_to_decimal(hours: int, minutes: int = 0, seconds: int = 0) -> float:
    """
    将时分秒转换为十进制小时
    
    Args:
        hours: 小时
        minutes: 分钟
        seconds: 秒
        
    Returns:
        十进制小时
    """
    return hours + minutes / 60.0 + seconds / 3600.0


# ============ 主要公共函数 ============

def get_sunrise(
    latitude: float,
    longitude: float,
    d: Optional[date] = None,
    timezone: float = 0.0,
    elevation: float = 0.0
) -> Optional[datetime]:
    """
    计算日出时间
    
    Args:
        latitude: 纬度（度），正为北纬
        longitude: 经度（度），正为东经
        d: 日期，默认为今天
        timezone: 时区（小时），东经为正
        elevation: 海拔高度（米），用于大气折射修正
        
    Returns:
        日出时间的datetime对象，如果极夜则返回None
        
    Example:
        >>> sunrise = get_sunrise(39.9042, 116.4074, date(2024, 6, 21), timezone=8)
        >>> print(sunrise.strftime('%H:%M'))
        04:46
    """
    if d is None:
        d = date.today()
    
    jd = _julian_day(d)
    t = _julian_century(jd)
    
    # 太阳赤纬和时差
    declination = _solar_declination(t)
    eot = _equation_of_time(t)
    
    # 日出时的太阳高度角（考虑太阳视半径和大气折射）
    altitude = -SUN_RADIUS - ATMOSPHERIC_REFRACTION
    
    # 海拔修正
    if elevation > 0:
        altitude += 2.076 * math.sqrt(elevation) / 60.0  # 地平线下降角
    
    # 计算时角
    ha = _hour_angle(latitude, declination, altitude)
    
    if ha is None:
        return None  # 极夜
    
    # 计算时间
    # 日出：时角为正，正午 - 时角/15
    sunrise_decimal = _time_from_hour_angle(ha, longitude, eot, timezone)
    
    hours, minutes, seconds = _decimal_to_time(sunrise_decimal)
    
    return datetime.combine(d, time(hours, minutes, seconds))


def get_sunset(
    latitude: float,
    longitude: float,
    d: Optional[date] = None,
    timezone: float = 0.0,
    elevation: float = 0.0
) -> Optional[datetime]:
    """
    计算日落时间
    
    Args:
        latitude: 纬度（度），正为北纬
        longitude: 经度（度），正为东经
        d: 日期，默认为今天
        timezone: 时区（小时），东经为正
        elevation: 海拔高度（米）
        
    Returns:
        日落时间的datetime对象，如果极夜则返回None
        
    Example:
        >>> sunset = get_sunset(39.9042, 116.4074, date(2024, 6, 21), timezone=8)
        >>> print(sunset.strftime('%H:%M'))
        19:46
    """
    if d is None:
        d = date.today()
    
    jd = _julian_day(d)
    t = _julian_century(jd)
    
    declination = _solar_declination(t)
    eot = _equation_of_time(t)
    
    altitude = -SUN_RADIUS - ATMOSPHERIC_REFRACTION
    
    if elevation > 0:
        altitude += 2.076 * math.sqrt(elevation) / 60.0
    
    ha = _hour_angle(latitude, declination, altitude)
    
    if ha is None:
        return None
    
    # 计算时间
    # 日落：时角为负（相对于日出），正午 + 时角/15
    sunset_decimal = _time_from_hour_angle(-ha, longitude, eot, timezone)
    
    hours, minutes, seconds = _decimal_to_time(sunset_decimal)
    
    return datetime.combine(d, time(hours, minutes, seconds))


def get_solar_noon(
    longitude: float,
    d: Optional[date] = None,
    timezone: float = 0.0
) -> datetime:
    """
    计算太阳正午时间（地方视午）
    
    Args:
        longitude: 经度（度），正为东经
        d: 日期，默认为今天
        timezone: 时区（小时），东经为正
        
    Returns:
        太阳正午时间的datetime对象
        
    Example:
        >>> noon = get_solar_noon(116.4074, date(2024, 6, 21), timezone=8)
        >>> print(noon.strftime('%H:%M'))
        12:16
    """
    if d is None:
        d = date.today()
    
    jd = _julian_day(d)
    t = _julian_century(jd)
    
    eot = _equation_of_time(t)
    
    # 正午 = 12 - 时差/60 - 经度修正
    noon_decimal = 12.0 - longitude / 15.0 + timezone + eot / 60.0
    
    # 处理跨越午夜
    while noon_decimal < 0:
        noon_decimal += 24
    while noon_decimal >= 24:
        noon_decimal -= 24
    
    hours, minutes, seconds = _decimal_to_time(noon_decimal)
    
    return datetime.combine(d, time(hours, minutes, seconds))


def get_day_length(
    latitude: float,
    longitude: float,
    d: Optional[date] = None,
    timezone: float = 0.0
) -> Optional[timedelta]:
    """
    计算白昼时长
    
    Args:
        latitude: 纬度（度）
        longitude: 经度（度）
        d: 日期，默认为今天
        timezone: 时区（小时）
        
    Returns:
        白昼时长的timedelta对象，极夜返回None
        
    Example:
        >>> length = get_day_length(39.9042, 116.4074, date(2024, 6, 21))
        >>> print(f"{length.seconds // 3600}小时{(length.seconds % 3600) // 60}分钟")
        15小时0分钟
    """
    sunrise = get_sunrise(latitude, longitude, d, timezone)
    sunset = get_sunset(latitude, longitude, d, timezone)
    
    if sunrise is None or sunset is None:
        return None
    
    return sunset - sunrise


def get_twilight_times(
    latitude: float,
    longitude: float,
    d: Optional[date] = None,
    timezone: float = 0.0,
    twilight_type: str = 'civil'
) -> Dict[str, Optional[datetime]]:
    """
    计算曙暮光时间
    
    Args:
        latitude: 纬度（度）
        longitude: 经度（度）
        d: 日期，默认为今天
        timezone: 时区（小时）
        twilight_type: 曙暮光类型，'civil'（民用）、'nautical'（航海）、'astronomical'（天文）
        
    Returns:
        包含开始和结束时间的字典：
        - dawn: 曙光开始
        - dusk: 暮光结束
        
    Example:
        >>> times = get_twilight_times(39.9042, 116.4074, date(2024, 6, 21), timezone=8, twilight_type='civil')
        >>> print(f"曙光开始: {times['dawn'].strftime('%H:%M')}")
        曙光开始: 04:12
    """
    if d is None:
        d = date.today()
    
    # 选择曙暮光角度
    twilight_angles = {
        'civil': TWILIGHT_CIVIL,
        'nautical': TWILIGHT_NAUTICAL,
        'astronomical': TWILIGHT_ASTRONOMICAL
    }
    
    if twilight_type not in twilight_angles:
        raise ValueError(f"Invalid twilight_type: {twilight_type}. Must be 'civil', 'nautical', or 'astronomical'")
    
    angle = twilight_angles[twilight_type]
    
    jd = _julian_day(d)
    t = _julian_century(jd)
    
    declination = _solar_declination(t)
    eot = _equation_of_time(t)
    
    # 曙暮光时太阳在地平线下的角度
    altitude = -angle
    
    ha = _hour_angle(latitude, declination, altitude)
    
    if ha is None:
        return {'dawn': None, 'dusk': None}
    
    # 曙光开始 = 日出前的曙暮光（早于日出）
    dawn_decimal = _time_from_hour_angle(ha, longitude, eot, timezone)
    # 暮光结束 = 日落后的曙暮光（晚于日落）
    dusk_decimal = _time_from_hour_angle(-ha, longitude, eot, timezone)
    
    dawn_h, dawn_m, dawn_s = _decimal_to_time(dawn_decimal)
    dusk_h, dusk_m, dusk_s = _decimal_to_time(dusk_decimal)
    
    return {
        'dawn': datetime.combine(d, time(dawn_h, dawn_m, dawn_s)),
        'dusk': datetime.combine(d, time(dusk_h, dusk_m, dusk_s))
    }


def get_solar_position(
    latitude: float,
    longitude: float,
    dt: Optional[datetime] = None,
    timezone: float = 0.0
) -> Dict[str, float]:
    """
    计算太阳位置（方位角和高度角）
    
    Args:
        latitude: 纬度（度）
        longitude: 经度（度）
        dt: 日期时间，默认为当前时间
        timezone: 时区（小时）
        
    Returns:
        包含方位角和高度角的字典：
        - azimuth: 方位角（度，正北为0，顺时针增加）
        - altitude: 高度角（度，地平线为0，正值表示在地平线以上）
        
    Example:
        >>> pos = get_solar_position(39.9042, 116.4074, datetime(2024, 6, 21, 12, 0), timezone=8)
        >>> print(f"方位角: {pos['azimuth']:.1f}°, 高度角: {pos['altitude']:.1f}°")
        方位角: 173.5°, 高度角: 73.6°
    """
    if dt is None:
        dt = datetime.now()
    
    d = dt.date()
    
    # 计算小数小时
    hour_decimal = dt.hour + dt.minute / 60.0 + dt.second / 3600.0
    
    jd = _julian_day(d) + (hour_decimal - timezone) / 24.0
    t = _julian_century(jd)
    
    # 太阳赤纬
    declination = _solar_declination(t) * DEG_TO_RAD
    
    # 时差
    eot = _equation_of_time(t)
    
    # 太阳时角
    # 太阳时 = 地方平时 + 时差
    solar_time = hour_decimal + eot / 60.0 + longitude / 15.0 - timezone
    hour_angle = (solar_time - 12) * 15.0  # 转换为度
    hour_angle_rad = hour_angle * DEG_TO_RAD
    
    lat_rad = latitude * DEG_TO_RAD
    
    # 计算高度角
    sin_alt = math.sin(lat_rad) * math.sin(declination) + \
              math.cos(lat_rad) * math.cos(declination) * math.cos(hour_angle_rad)
    altitude = math.asin(sin_alt) * RAD_TO_DEG
    
    # 计算方位角
    cos_az = (math.sin(declination) - math.sin(lat_rad) * sin_alt) / \
             (math.cos(lat_rad) * math.cos(altitude * DEG_TO_RAD))
    
    # 处理数值误差
    cos_az = max(-1, min(1, cos_az))
    azimuth = math.acos(cos_az) * RAD_TO_DEG
    
    # 根据时角修正方位角
    if hour_angle > 0:
        azimuth = 360 - azimuth
    
    return {
        'azimuth': round(azimuth, 2),
        'altitude': round(altitude, 2)
    }


def get_golden_hour(
    latitude: float,
    longitude: float,
    d: Optional[date] = None,
    timezone: float = 0.0
) -> Dict[str, Optional[datetime]]:
    """
    计算黄金时刻（摄影最佳时段）
    
    黄金时刻定义：太阳高度角在 2°-10° 之间
    
    Args:
        latitude: 纬度（度）
        longitude: 经度（度）
        d: 日期，默认为今天
        timezone: 时区（小时）
        
    Returns:
        包含早晚黄金时刻的字典：
        - morning_start: 早晨黄金时刻开始
        - morning_end: 早晨黄金时刻结束
        - evening_start: 傍晚黄金时刻开始
        - evening_end: 傍晚黄金时刻结束
        
    Example:
        >>> golden = get_golden_hour(39.9042, 116.4074, date(2024, 6, 21), timezone=8)
        >>> print(f"早晨黄金时刻: {golden['morning_start'].strftime('%H:%M')} - {golden['morning_end'].strftime('%H:%M')}")
    """
    if d is None:
        d = date.today()
    
    jd = _julian_day(d)
    t = _julian_century(jd)
    
    declination = _solar_declination(t)
    eot = _equation_of_time(t)
    
    # 黄金时刻的太阳高度角范围
    low_altitude = 2.0
    high_altitude = 10.0
    
    result = {
        'morning_start': None,
        'morning_end': None,
        'evening_start': None,
        'evening_end': None
    }
    
    # 计算早晨黄金时刻
    ha_low = _hour_angle(latitude, declination, low_altitude)
    ha_high = _hour_angle(latitude, declination, high_altitude)
    
    if ha_low is not None and ha_high is not None:
        # 早晨黄金时刻：太阳从低高度角(2°)升到高高度角(10°)
        # ha_low > ha_high，使用 -ha 来正确计算时间（减法变加法）
        morning_start_decimal = _time_from_hour_angle(-ha_low, longitude, eot, timezone)
        morning_end_decimal = _time_from_hour_angle(-ha_high, longitude, eot, timezone)
        
        h, m, s = _decimal_to_time(morning_start_decimal)
        result['morning_start'] = datetime.combine(d, time(h, m, s))
        
        h, m, s = _decimal_to_time(morning_end_decimal)
        result['morning_end'] = datetime.combine(d, time(h, m, s))
        
        # 傍晚黄金时刻：太阳从高高度角(10°)降到低高度角(2°)
        # 使用 -ha（日落方式），时间随太阳高度降低而推迟
        evening_start_decimal = _time_from_hour_angle(-ha_high, longitude, eot, timezone)
        evening_end_decimal = _time_from_hour_angle(-ha_low, longitude, eot, timezone)
        
        h, m, s = _decimal_to_time(evening_start_decimal)
        result['evening_start'] = datetime.combine(d, time(h, m, s))
        
        h, m, s = _decimal_to_time(evening_end_decimal)
        result['evening_end'] = datetime.combine(d, time(h, m, s))
    
    return result


def get_solar_info(
    latitude: float,
    longitude: float,
    d: Optional[date] = None,
    timezone: float = 0.0,
    elevation: float = 0.0
) -> Dict[str, Any]:
    """
    获取完整的太阳信息
    
    Args:
        latitude: 纬度（度）
        longitude: 经度（度）
        d: 日期，默认为今天
        timezone: 时区（小时）
        elevation: 海拔高度（米）
        
    Returns:
        包含所有太阳信息的字典
        
    Example:
        >>> info = get_solar_info(39.9042, 116.4074, date(2024, 6, 21), timezone=8)
        >>> print(f"日出: {info['sunrise'].strftime('%H:%M')}")
        >>> print(f"日落: {info['sunset'].strftime('%H:%M')}")
        >>> print(f"白昼时长: {info['day_length_hours']:.1f}小时")
    """
    if d is None:
        d = date.today()
    
    sunrise = get_sunrise(latitude, longitude, d, timezone, elevation)
    sunset = get_sunset(latitude, longitude, d, timezone, elevation)
    solar_noon = get_solar_noon(longitude, d, timezone)
    day_length = get_day_length(latitude, longitude, d, timezone)
    
    civil_twilight = get_twilight_times(latitude, longitude, d, timezone, 'civil')
    nautical_twilight = get_twilight_times(latitude, longitude, d, timezone, 'nautical')
    astronomical_twilight = get_twilight_times(latitude, longitude, d, timezone, 'astronomical')
    
    golden_hour = get_golden_hour(latitude, longitude, d, timezone)
    
    # 计算正午太阳高度角
    jd = _julian_day(d)
    t = _julian_century(jd)
    declination = _solar_declination(t)
    solar_altitude_noon = 90.0 - abs(latitude - declination)
    
    return {
        'date': d,
        'latitude': latitude,
        'longitude': longitude,
        'timezone': timezone,
        'sunrise': sunrise,
        'sunset': sunset,
        'solar_noon': solar_noon,
        'day_length': day_length,
        'day_length_hours': day_length.total_seconds() / 3600 if day_length else None,
        'civil_twilight': civil_twilight,
        'nautical_twilight': nautical_twilight,
        'astronomical_twilight': astronomical_twilight,
        'golden_hour': golden_hour,
        'solar_noon_altitude': round(solar_altitude_noon, 2),
        'declination': round(declination, 4)
    }


def is_daylight(
    latitude: float,
    longitude: float,
    dt: Optional[datetime] = None,
    timezone: float = 0.0
) -> bool:
    """
    判断指定时间是否为白天
    
    Args:
        latitude: 纬度（度）
        longitude: 经度（度）
        dt: 日期时间，默认为当前时间
        timezone: 时区（小时）
        
    Returns:
        True表示白天，False表示夜晚
        
    Example:
        >>> is_day = is_daylight(39.9042, 116.4074, datetime(2024, 6, 21, 14, 0), timezone=8)
        >>> print(is_day)
        True
    """
    if dt is None:
        dt = datetime.now()
    
    d = dt.date()
    sunrise = get_sunrise(latitude, longitude, d, timezone)
    sunset = get_sunset(latitude, longitude, d, timezone)
    
    if sunrise is None:
        return False  # 极夜
    
    if sunset is None:
        return True   # 极昼
    
    # 检查时间是否在日出和日落之间
    current_time = dt.time()
    sunrise_time = sunrise.time()
    sunset_time = sunset.time()
    
    return sunrise_time <= current_time <= sunset_time


def get_sun_phase(d: Optional[date] = None, hemisphere: str = 'north') -> str:
    """
    获取季节相位（基于太阳黄经）
    
    Args:
        d: 日期，默认为今天
        hemisphere: 半球，'north' 或 'south'
        
    Returns:
        季节名称：'spring', 'summer', 'autumn', 'winter'
        
    Example:
        >>> phase = get_sun_phase(date(2024, 6, 21), hemisphere='north')
        >>> print(phase)
        summer
    """
    if d is None:
        d = date.today()
    
    jd = _julian_day(d)
    t = _julian_century(jd)
    
    # 获取太阳黄经
    lambda_sun = _solar_apparent_longitude(t)
    
    # 根据黄经判断季节
    # 北半球：0-90°春季，90-180°夏季，180-270°秋季，270-360°冬季
    # 春分点约在黄经0°
    
    if hemisphere == 'north':
        if 0 <= lambda_sun < 90:
            return 'spring'
        elif 90 <= lambda_sun < 180:
            return 'summer'
        elif 180 <= lambda_sun < 270:
            return 'autumn'
        else:
            return 'winter'
    else:  # south
        if 0 <= lambda_sun < 90:
            return 'autumn'
        elif 90 <= lambda_sun < 180:
            return 'winter'
        elif 180 <= lambda_sun < 270:
            return 'spring'
        else:
            return 'summer'


def format_time(dt: Optional[datetime], fmt: str = '%H:%M:%S') -> str:
    """
    格式化时间输出
    
    Args:
        dt: datetime对象
        fmt: 格式字符串
        
    Returns:
        格式化的时间字符串，如果dt为None返回 'N/A'
        
    Example:
        >>> sunrise = get_sunrise(39.9042, 116.4074)
        >>> print(format_time(sunrise))
        06:23:45
    """
    if dt is None:
        return 'N/A'
    return dt.strftime(fmt)


if __name__ == '__main__':
    # 演示用法
    print("=" * 50)
    print("Solar Utils - 日出日落时间计算工具演示")
    print("=" * 50)
    
    # 北京坐标
    beijing_lat = 39.9042
    beijing_lon = 116.4074
    beijing_tz = 8.0
    
    today = date.today()
    
    print(f"\n📍 北京 ({beijing_lat}°N, {beijing_lon}°E) - {today}")
    print("-" * 50)
    
    # 获取完整信息
    info = get_solar_info(beijing_lat, beijing_lon, today, beijing_tz)
    
    print(f"🌅 日出时间: {format_time(info['sunrise'])}")
    print(f"🌇 日落时间: {format_time(info['sunset'])}")
    print(f"☀️ 正午时间: {format_time(info['solar_noon'])}")
    print(f"⏱️ 白昼时长: {info['day_length_hours']:.2f} 小时")
    print(f"📐 正午太阳高度角: {info['solar_noon_altitude']:.1f}°")
    print(f"🌍 太阳赤纬: {info['declination']:.4f}°")
    
    print(f"\n🕐 民用曙暮光: {format_time(info['civil_twilight']['dawn'])} - {format_time(info['civil_twilight']['dusk'])}")
    print(f"⚓ 航海曙暮光: {format_time(info['nautical_twilight']['dawn'])} - {format_time(info['nautical_twilight']['dusk'])}")
    print(f"🔭 天文曙暮光: {format_time(info['astronomical_twilight']['dawn'])} - {format_time(info['astronomical_twilight']['dusk'])}")
    
    print(f"\n📸 黄金时刻:")
    gh = info['golden_hour']
    print(f"   早晨: {format_time(gh['morning_start'])} - {format_time(gh['morning_end'])}")
    print(f"   傍晚: {format_time(gh['evening_start'])} - {format_time(gh['evening_end'])}")
    
    # 当前太阳位置
    now = datetime.now()
    pos = get_solar_position(beijing_lat, beijing_lon, now, beijing_tz)
    print(f"\n🌞 当前太阳位置 ({now.strftime('%H:%M')}):")
    print(f"   方位角: {pos['azimuth']:.1f}°")
    print(f"   高度角: {pos['altitude']:.1f}°")
    
    # 季节
    season = get_sun_phase(today, 'north')
    season_names = {'spring': '春季', 'summer': '夏季', 'autumn': '秋季', 'winter': '冬季'}
    print(f"\n🌸 当前季节: {season_names.get(season, season)}")
    
    print("\n" + "=" * 50)