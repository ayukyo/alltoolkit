"""
Sunrise/Sunset Calculator Utils
日出日落时间计算工具

纯 Python 实现，零外部依赖
基于 Jean Meeus 天文算法

功能:
- 计算日出、日落、正午时间
- 计算民用晨昏蒙影、航海晨昏蒙影、天文晨昏蒙影
- 计算黄金时刻（摄影最佳时间）
- 计算日照时长
- 计算太阳方位角和仰角
"""

import math
from datetime import datetime, date, time, timedelta
from typing import Tuple, Optional, Dict


def _to_julian_day(dt: datetime) -> float:
    """
    将 datetime 转换为儒略日 (Julian Day)
    
    Julian Day 是从公元前4713年1月1日正午开始的天数
    """
    year = dt.year
    month = dt.month
    day = dt.day + dt.hour / 24.0 + dt.minute / 1440.0 + dt.second / 86400.0
    
    if month <= 2:
        year -= 1
        month += 12
    
    A = int(year / 100)
    B = 2 - A + int(A / 4)
    
    JD = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5
    return JD


def _from_julian_day(jd: float, timezone_offset: float = 0) -> datetime:
    """
    将儒略日转换为 datetime
    """
    Z = int(jd + 0.5)
    F = jd + 0.5 - Z
    
    if Z < 2299161:
        A = Z
    else:
        alpha = int((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - int(alpha / 4)
    
    B = A + 1524
    C = int((B - 122.1) / 365.25)
    D = int(365.25 * C)
    E = int((B - D) / 30.6001)
    
    day = B - D - int(30.6001 * E) + F
    
    if E < 14:
        month = E - 1
    else:
        month = E - 13
    
    if month > 2:
        year = C - 4716
    else:
        year = C - 4715
    
    # 提取时分秒
    day_int = int(day)
    day_frac = day - day_int
    
    hours = day_frac * 24
    hour = int(hours)
    minutes = (hours - hour) * 60
    minute = int(minutes)
    seconds = (minutes - minute) * 60
    second = int(seconds)
    
    # 调整时区
    result = datetime(year, month, day_int, hour, minute, second)
    result = result + timedelta(hours=timezone_offset)
    
    return result


def _solar_mean_anomaly(jd: float) -> float:
    """计算太阳平均近点角 (degrees)"""
    M = (357.5296 + 0.98560028 * (jd - 2451545)) % 360
    return M


def _equation_of_center(M: float) -> float:
    """计算中心方程 (degrees)"""
    Mr = math.radians(M)
    C = (1.915 * math.sin(Mr) + 0.020 * math.sin(2 * Mr) + 0.0003 * math.sin(3 * Mr))
    return C


def _ecliptic_longitude(M: float, C: float) -> float:
    """计算黄道经度 (degrees)"""
    λ = (M + C + 180 + 102.9372) % 360
    return λ


def _solar_declination(λ: float) -> float:
    """计算太阳赤纬 (degrees)"""
    λr = math.radians(λ)
    δ = math.degrees(math.asin(math.sin(λr) * math.sin(math.radians(23.44))))
    return δ


def _equation_of_time(M: float, λ: float) -> float:
    """
    计算时差方程 (minutes)
    太阳时与本地时钟时间的差值
    
    使用更精确的公式
    """
    Mr = math.radians(M)
    e = 0.0167  # 地球轨道离心率
    ε = math.radians(23.44)  # 黄赤交角
    
    # 简化公式
    y = math.tan(ε / 2) ** 2
    EoT = 4 * math.degrees(
        y * math.sin(2 * λ) - 
        e * 2 * math.sin(M) + 
        4 * e * y * math.sin(M) * math.cos(2 * λ) -
        0.5 * y ** 2 * math.sin(4 * λ) -
        1.25 * e ** 2 * math.sin(2 * M)
    )
    return EoT


def _hour_angle(lat: float, dec: float, altitude: float = -0.833) -> float:
    """
    计算时角 (degrees)
    
    参数:
        lat: 纬度 (degrees)
        dec: 太阳赤纬 (degrees)
        altitude: 太阳高度角 (degrees), 默认 -0.833 (考虑大气折射的地平线)
    
    返回:
        时角 (degrees), 如果太阳不升起或不下落返回 None
    """
    lat_r = math.radians(lat)
    dec_r = math.radians(dec)
    alt_r = math.radians(altitude)
    
    cos_ω = (math.sin(alt_r) - math.sin(lat_r) * math.sin(dec_r)) / (math.cos(lat_r) * math.cos(dec_r))
    
    if cos_ω < -1:
        return None  # 太阳不落下（极昼）
    elif cos_ω > 1:
        return None  # 太阳不升起（极夜）
    
    ω = math.degrees(math.acos(cos_ω))
    return ω


def calculate_sunrise_sunset(
    latitude: float,
    longitude: float,
    target_date: date,
    timezone_offset: float = 0,
    altitude_deg: float = -0.833
) -> Optional[Dict[str, datetime]]:
    """
    计算日出日落时间
    
    参数:
        latitude: 纬度 (degrees, 北纬为正)
        longitude: 经度 (degrees, 东经为正)
        target_date: 目标日期
        timezone_offset: 时区偏移 (hours, 如北京时间为 +8)
        altitude_deg: 太阳高度角阈值 (degrees)
            -0.833: 标准日出日落 (考虑大气折射)
            -0.3: 太阳上边缘接触地平线
            -6: 民用晨昏蒙影
            -12: 航海晨昏蒙影
            -18: 天文晨昏蒙影
    
    返回:
        字典包含:
        - sunrise: 日出时间
        - sunset: 日落时间
        - solar_noon: 太阳正午
        - day_length: 日照时长 (秒)
        如果极昼或极夜返回 None
    """
    # 创建当天的 datetime (UTC noon)
    dt = datetime(target_date.year, target_date.month, target_date.day, 12, 0, 0)
    dt_utc = dt - timedelta(hours=timezone_offset)
    jd = _to_julian_day(dt_utc)
    
    # 计算太阳参数
    M = _solar_mean_anomaly(jd)
    C = _equation_of_center(M)
    λ = _ecliptic_longitude(M, C)
    δ = _solar_declination(λ)
    EoT = _equation_of_time(M, λ)
    
    # 计算时角
    ω = _hour_angle(latitude, δ, altitude_deg)
    
    if ω is None:
        return None
    
    # 计算日出、日落、正午时间
    # 太阳正午 = 12:00 - 时差方程 - 经度修正
    solar_noon_minutes = 720 - EoT - 4 * (longitude - timezone_offset * 15)
    
    # 日出时间 = 正午 - 时角
    sunrise_minutes = solar_noon_minutes - 4 * ω
    
    # 日落时间 = 正午 + 时角
    sunset_minutes = solar_noon_minutes + 4 * ω
    
    # 转换为 datetime
    base_date = datetime(target_date.year, target_date.month, target_date.day)
    
    sunrise = base_date + timedelta(minutes=sunrise_minutes)
    sunset = base_date + timedelta(minutes=sunset_minutes)
    solar_noon = base_date + timedelta(minutes=solar_noon_minutes)
    
    # 日照时长
    day_length_seconds = (sunset - sunrise).total_seconds()
    
    return {
        'sunrise': sunrise,
        'sunset': sunset,
        'solar_noon': solar_noon,
        'day_length': day_length_seconds,
        'sunrise_str': sunrise.strftime('%H:%M:%S'),
        'sunset_str': sunset.strftime('%H:%M:%S'),
        'solar_noon_str': solar_noon.strftime('%H:%M:%S'),
        'day_length_str': _format_duration(day_length_seconds)
    }


def calculate_civil_twilight(
    latitude: float,
    longitude: float,
    target_date: date,
    timezone_offset: float = 0
) -> Optional[Dict[str, datetime]]:
    """
    计算民用晨昏蒙影时间 (太阳高度 -6°)
    
    民用晨昏蒙影：太阳在地平线下 0° 到 6°
    此时地面物体仍清晰可见，适合户外活动
    """
    result = calculate_sunrise_sunset(latitude, longitude, target_date, timezone_offset, -6)
    if result:
        return {
            'dawn': result['sunrise'],
            'dusk': result['sunset'],
            'dawn_str': result['sunrise_str'],
            'dusk_str': result['sunset_str']
        }
    return None


def calculate_nautical_twilight(
    latitude: float,
    longitude: float,
    target_date: date,
    timezone_offset: float = 0
) -> Optional[Dict[str, datetime]]:
    """
    计算航海晨昏蒙影时间 (太阳高度 -12°)
    
    航海晨昏蒙影：太阳在地平线下 6° 到 12°
    此时地平线仍可见，适合航海观测
    """
    result = calculate_sunrise_sunset(latitude, longitude, target_date, timezone_offset, -12)
    if result:
        return {
            'dawn': result['sunrise'],
            'dusk': result['sunset'],
            'dawn_str': result['sunrise_str'],
            'dusk_str': result['sunset_str']
        }
    return None


def calculate_astronomical_twilight(
    latitude: float,
    longitude: float,
    target_date: date,
    timezone_offset: float = 0
) -> Optional[Dict[str, datetime]]:
    """
    计算天文晨昏蒙影时间 (太阳高度 -18°)
    
    天文晨昏蒙影：太阳在地平线下 12° 到 18°
    此时天空完全黑暗，适合天文观测
    """
    result = calculate_sunrise_sunset(latitude, longitude, target_date, timezone_offset, -18)
    if result:
        return {
            'dawn': result['sunrise'],
            'dusk': result['sunset'],
            'dawn_str': result['sunrise_str'],
            'dusk_str': result['sunset_str']
        }
    return None


def calculate_golden_hour(
    latitude: float,
    longitude: float,
    target_date: date,
    timezone_offset: float = 0
) -> Optional[Dict[str, datetime]]:
    """
    计算黄金时刻 (摄影最佳时间)
    
    黄金时刻：太阳高度在 0° 到 6° 之间
    早晨和傍晚的光线柔和、温暖，是摄影的黄金时间
    
    返回:
        morning_start: 早晨黄金时刻开始 (日出)
        morning_end: 早晨黄金时刻结束
        evening_start: 傍晚黄金时刻开始
        evening_end: 傍晚黄金时刻结束 (日落)
    """
    # 标准日出日落
    standard = calculate_sunrise_sunset(latitude, longitude, target_date, timezone_offset, -0.833)
    # 太阳高度 6°
    golden_end = calculate_sunrise_sunset(latitude, longitude, target_date, timezone_offset, 6)
    
    if standard is None or golden_end is None:
        return None
    
    base_date = datetime(target_date.year, target_date.month, target_date.day)
    
    return {
        'morning_start': standard['sunrise'],
        'morning_end': golden_end['sunrise'],
        'evening_start': golden_end['sunset'],
        'evening_end': standard['sunset'],
        'morning_start_str': standard['sunrise_str'],
        'morning_end_str': golden_end['sunrise_str'],
        'evening_start_str': golden_end['sunset_str'],
        'evening_end_str': standard['sunset_str']
    }


def calculate_blue_hour(
    latitude: float,
    longitude: float,
    target_date: date,
    timezone_offset: float = 0
) -> Optional[Dict[str, datetime]]:
    """
    计算蓝调时刻
    
    蓝调时刻：太阳在地平线下 4° 到 6°
    天空呈现深蓝色，城市灯光开始显现，适合城市夜景摄影
    
    返回:
        morning_start/end: 早晨蓝调时刻
        evening_start/end: 傍晚蓝调时刻
    """
    # 太阳高度 4°
    blue_outer = calculate_sunrise_sunset(latitude, longitude, target_date, timezone_offset, -4)
    # 太阳高度 6°
    blue_inner = calculate_sunrise_sunset(latitude, longitude, target_date, timezone_offset, -6)
    
    if blue_outer is None or blue_inner is None:
        return None
    
    return {
        'morning_start': blue_inner['sunrise'],
        'morning_end': blue_outer['sunrise'],
        'evening_start': blue_outer['sunset'],
        'evening_end': blue_inner['sunset'],
        'morning_start_str': blue_inner['sunrise_str'],
        'morning_end_str': blue_outer['sunrise_str'],
        'evening_start_str': blue_outer['sunset_str'],
        'evening_end_str': blue_inner['sunset_str']
    }


def calculate_solar_position(
    latitude: float,
    longitude: float,
    dt: datetime,
    timezone_offset: float = 0
) -> Dict[str, float]:
    """
    计算指定时刻的太阳位置
    
    参数:
        latitude: 纬度 (degrees)
        longitude: 经度 (degrees)
        dt: datetime 对象
        timezone_offset: 时区偏移 (hours)
    
    返回:
        altitude: 太阳高度角 (degrees, 0° 为地平线)
        azimuth: 太阳方位角 (degrees, 正北为 0°, 顺时针增加)
    """
    # 转换为 UTC
    dt_utc = dt - timedelta(hours=timezone_offset)
    jd = _to_julian_day(dt_utc)
    
    # 计算太阳参数
    n = jd - 2451545.0
    L = (280.460 + 0.9856474 * n) % 360  # 太阳平黄经
    g = (357.528 + 0.9856003 * n) % 360  # 太阳平近点角
    
    # 黄道经度
    λ = (L + 1.915 * math.sin(math.radians(g)) + 0.020 * math.sin(math.radians(2 * g))) % 360
    ε = 23.439 - 0.0000004 * n  # 黄赤交角
    
    # 赤经和赤纬
    λr = math.radians(λ)
    εr = math.radians(ε)
    
    # 纬
    δ = math.degrees(math.asin(math.sin(εr) * math.sin(λr)))
    
    # 经 (需要正确处理 atan2)
    α = math.degrees(math.atan2(math.cos(εr) * math.sin(λr), math.cos(λr)))
    if α < 0:
        α += 360  # 确保 α 在 0-360 范围内
    
    # 格林尼治恒星时（基于儒略日，已包含时间信息）
    θ0 = (280.460 + 360.9856474 * (jd - 2451545)) % 360
    
    # 本地恒星时（加上经度偏移）
    θ = (θ0 + longitude) % 360
    
    # 时角
    H = θ - α
    if H < -180:
        H += 360
    elif H > 180:
        H -= 360
    
    # 高度角和方位角
    lat_r = math.radians(latitude)
    H_r = math.radians(H)
    δ_r = math.radians(δ)
    
    # 高度角
    sin_alt = math.sin(lat_r) * math.sin(δ_r) + math.cos(lat_r) * math.cos(δ_r) * math.cos(H_r)
    alt = math.degrees(math.asin(sin_alt))
    alt_r = math.radians(alt)  # 高度角的弧度值
    
    # 方位角
    cos_az = (math.sin(δ_r) - math.sin(lat_r) * math.sin(alt_r)) / (math.cos(lat_r) * math.cos(alt_r))
    az = math.degrees(math.atan2(math.sin(H_r), cos_az))
    if az < 0:
        az += 360  # 确保方位角在 0-360 范围
    
    return {
        'altitude': alt,
        'azimuth': az,
        'declination': δ,
        'right_ascension': α
    }


def is_daylight(
    latitude: float,
    longitude: float,
    dt: datetime,
    timezone_offset: float = 0
) -> bool:
    """
    判断指定时刻是否为白天
    
    返回 True 如果太阳在地平线以上
    """
    pos = calculate_solar_position(latitude, longitude, dt, timezone_offset)
    return pos['altitude'] > -0.833  # 考虑大气折射


def calculate_day_length_year(
    latitude: float,
    year: int,
    timezone_offset: float = 0
) -> Dict[str, any]:
    """
    计算一年中最长和最短的日照时间
    
    返回:
        longest_day: 最长日照日期和时长
        shortest_day: 最短日照日期和时长
        equinox_dates: 春分秋分日期
        solstice_dates: 夏至冬至日期
    """
    from datetime import date as date_type
    
    longest = {'date': None, 'length': 0, 'length_str': ''}
    shortest = {'date': None, 'length': float('inf'), 'length_str': ''}
    
    # 遍历一年
    current = date_type(year, 1, 1)
    one_day = timedelta(days=1)
    
    while current.year == year:
        result = calculate_sunrise_sunset(latitude, 0, current, timezone_offset)
        if result:
            length = result['day_length']
            if length > longest['length']:
                longest = {
                    'date': current,
                    'length': length,
                    'length_str': result['day_length_str']
                }
            if length < shortest['length']:
                shortest = {
                    'date': current,
                    'length': length,
                    'length_str': result['day_length_str']
                }
        current += one_day
    
    return {
        'longest_day': longest,
        'shortest_day': shortest
    }


def _format_duration(seconds: float) -> str:
    """格式化时长为 HH:MM:SS"""
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def get_sun_times_summary(
    latitude: float,
    longitude: float,
    target_date: date,
    timezone_offset: float = 0
) -> Dict:
    """
    获取完整的太阳时间摘要
    
    一次性获取所有相关时间信息
    """
    result = {
        'date': target_date.isoformat(),
        'location': {
            'latitude': latitude,
            'longitude': longitude
        },
        'timezone_offset': timezone_offset
    }
    
    # 日出日落
    sun = calculate_sunrise_sunset(latitude, longitude, target_date, timezone_offset)
    if sun:
        result['sunrise'] = sun['sunrise_str']
        result['sunset'] = sun['sunset_str']
        result['solar_noon'] = sun['solar_noon_str']
        result['day_length'] = sun['day_length_str']
        result['day_length_seconds'] = sun['day_length']
    else:
        # 极昼或极夜
        pos = calculate_solar_position(latitude, longitude, datetime.combine(target_date, time(12)), timezone_offset)
        if pos['altitude'] > 0:
            result['status'] = 'polar_day'  # 极昼
        else:
            result['status'] = 'polar_night'  # 极夜
        return result
    
    # 晨昏蒙影
    civil = calculate_civil_twilight(latitude, longitude, target_date, timezone_offset)
    if civil:
        result['civil_twilight'] = {
            'dawn': civil['dawn_str'],
            'dusk': civil['dusk_str']
        }
    
    nautical = calculate_nautical_twilight(latitude, longitude, target_date, timezone_offset)
    if nautical:
        result['nautical_twilight'] = {
            'dawn': nautical['dawn_str'],
            'dusk': nautical['dusk_str']
        }
    
    astronomical = calculate_astronomical_twilight(latitude, longitude, target_date, timezone_offset)
    if astronomical:
        result['astronomical_twilight'] = {
            'dawn': astronomical['dawn_str'],
            'dusk': astronomical['dusk_str']
        }
    
    # 黄金时刻和蓝调时刻
    golden = calculate_golden_hour(latitude, longitude, target_date, timezone_offset)
    if golden:
        result['golden_hour'] = {
            'morning': f"{golden['morning_start_str']} - {golden['morning_end_str']}",
            'evening': f"{golden['evening_start_str']} - {golden['evening_end_str']}"
        }
    
    blue = calculate_blue_hour(latitude, longitude, target_date, timezone_offset)
    if blue:
        result['blue_hour'] = {
            'morning': f"{blue['morning_start_str']} - {blue['morning_end_str']}",
            'evening': f"{blue['evening_start_str']} - {blue['evening_end_str']}"
        }
    
    return result


# 常用城市坐标
CITIES = {
    'beijing': (39.9042, 116.4074, 8),
    'shanghai': (31.2304, 121.4737, 8),
    'guangzhou': (23.1291, 113.2644, 8),
    'shenzhen': (22.5431, 114.0579, 8),
    'hangzhou': (30.2741, 120.1551, 8),
    'chengdu': (30.5728, 104.0668, 8),
    'tokyo': (35.6762, 139.6503, 9),
    'new_york': (40.7128, -74.0060, -5),
    'london': (51.5074, -0.1278, 0),
    'paris': (48.8566, 2.3522, 1),
    'sydney': (-33.8688, 151.2093, 10),
    'moscow': (55.7558, 37.6173, 3),
    'dubai': (25.2048, 55.2708, 4),
    'singapore': (1.3521, 103.8198, 8),
    'hong_kong': (22.3193, 114.1694, 8),
}


def get_sun_times_for_city(
    city_name: str,
    target_date: Optional[date] = None
) -> Optional[Dict]:
    """
    根据城市名称获取太阳时间
    
    参数:
        city_name: 城市名称 (小写, 如 'beijing', 'tokyo')
        target_date: 目标日期，默认今天
    
    返回:
        太阳时间摘要字典
    """
    city_name = city_name.lower().replace(' ', '_')
    if city_name not in CITIES:
        return None
    
    lat, lon, tz = CITIES[city_name]
    if target_date is None:
        target_date = date.today()
    
    return get_sun_times_summary(lat, lon, target_date, tz)


if __name__ == '__main__':
    # 示例用法
    from datetime import date
    
    # 北京今天的日出日落时间
    today = date.today()
    
    print("=" * 60)
    print("日出日落时间计算器示例")
    print("=" * 60)
    
    # 北京
    print("\n📍 北京")
    summary = get_sun_times_for_city('beijing', today)
    if summary:
        print(f"  日出: {summary.get('sunrise', 'N/A')}")
        print(f"  日落: {summary.get('sunset', 'N/A')}")
        print(f"  正午: {summary.get('solar_noon', 'N/A')}")
        print(f"  日照时长: {summary.get('day_length', 'N/A')}")
        if 'golden_hour' in summary:
            print(f"  黄金时刻: 早晨 {summary['golden_hour']['morning']}")
            print(f"            傍晚 {summary['golden_hour']['evening']}")
    
    # 自定义坐标
    print("\n📍 上海 (自定义坐标)")
    lat, lon = 31.2304, 121.4737
    sun_times = calculate_sunrise_sunset(lat, lon, today, timezone_offset=8)
    if sun_times:
        print(f"  日出: {sun_times['sunrise_str']}")
        print(f"  日落: {sun_times['sunset_str']}")
        print(f"  日照时长: {sun_times['day_length_str']}")
    
    # 太阳当前位置
    print("\n📍 北京当前太阳位置")
    now = datetime.now()
    pos = calculate_solar_position(39.9042, 116.4074, now, 8)
    print(f"  高度角: {pos['altitude']:.2f}°")
    print(f"  方位角: {pos['azimuth']:.2f}°")
    print(f"  是否白天: {'是' if is_daylight(39.9042, 116.4074, now, 8) else '否'}")