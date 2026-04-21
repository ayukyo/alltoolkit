#!/usr/bin/env python3
"""
Solar Utils 使用示例

演示日出日落时间计算的各种应用场景
"""

from datetime import date, datetime, timedelta
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    get_sunrise,
    get_sunset,
    get_solar_noon,
    get_day_length,
    get_twilight_times,
    get_solar_position,
    get_golden_hour,
    get_solar_info,
    is_daylight,
    get_sun_phase,
    format_time
)


def example_basic_usage():
    """基本用法示例"""
    print("=" * 60)
    print("示例 1: 基本日出日落计算")
    print("=" * 60)
    
    # 北京坐标
    beijing_lat = 39.9042
    beijing_lon = 116.4074
    beijing_tz = 8.0
    
    today = date.today()
    
    print(f"\n📍 北京 ({beijing_lat}°N, {beijing_lon}°E) - {today}")
    
    sunrise = get_sunrise(beijing_lat, beijing_lon, today, beijing_tz)
    sunset = get_sunset(beijing_lat, beijing_lon, today, beijing_tz)
    
    print(f"🌅 日出时间: {format_time(sunrise)}")
    print(f"🌇 日落时间: {format_time(sunset)}")
    
    day_len = get_day_length(beijing_lat, beijing_lon, today, beijing_tz)
    if day_len:
        hours = day_len.total_seconds() / 3600
        print(f"⏱️ 白昼时长: {hours:.2f} 小时 ({int(hours)}时{int((hours - int(hours)) * 60)}分)")
    
    noon = get_solar_noon(beijing_lon, today, beijing_tz)
    print(f"☀️ 正午时间: {format_time(noon)}")


def example_multiple_cities():
    """多城市比较示例"""
    print("\n" + "=" * 60)
    print("示例 2: 多城市日出日落比较（2024年夏至）")
    print("=" * 60)
    
    cities = {
        '北京': (39.9042, 116.4074, 8.0),
        '上海': (31.2304, 121.4737, 8.0),
        '广州': (23.1291, 113.2644, 8.0),
        '新加坡': (1.3521, 103.8198, 8.0),
        '悉尼': (-33.8688, 151.2093, 10.0),  # 南半球
        '纽约': (40.7128, -74.0060, -5.0),
        '伦敦': (51.5074, -0.1278, 1.0),
    }
    
    d = date(2024, 6, 21)
    
    print(f"\n日期: {d} (北半球夏至)")
    print("-" * 60)
    
    for city, (lat, lon, tz) in cities.items():
        sunrise = get_sunrise(lat, lon, d, tz)
        sunset = get_sunset(lat, lon, d, tz)
        day_len = get_day_length(lat, lon, d, tz)
        
        print(f"\n{city}:")
        print(f"  日出: {format_time(sunrise, '%H:%M')}")
        print(f"  日落: {format_time(sunset, '%H:%M')}")
        if day_len:
            hours = day_len.total_seconds() / 3600
            print(f"  白昼: {hours:.1f} 小时")


def example_twilight_times():
    """曙暮光时间示例"""
    print("\n" + "=" * 60)
    print("示例 3: 曙暮光时间计算")
    print("=" * 60)
    
    beijing_lat = 39.9042
    beijing_lon = 116.4074
    beijing_tz = 8.0
    d = date(2024, 6, 21)
    
    print(f"\n📍 北京 - {d}")
    print("-" * 60)
    
    # 获取日出日落
    sunrise = get_sunrise(beijing_lat, beijing_lon, d, beijing_tz)
    sunset = get_sunset(beijing_lat, beijing_lon, d, beijing_tz)
    
    print(f"日出日落:")
    print(f"  🌅 日出: {format_time(sunrise, '%H:%M')}")
    print(f"  🌇 日落: {format_time(sunset, '%H:%M')}")
    
    # 三种曙暮光
    civil = get_twilight_times(beijing_lat, beijing_lon, d, beijing_tz, 'civil')
    nautical = get_twilight_times(beijing_lat, beijing_lon, d, beijing_tz, 'nautical')
    astronomical = get_twilight_times(beijing_lat, beijing_lon, d, beijing_tz, 'astronomical')
    
    print(f"\n曙暮光时间:")
    print(f"  🔸 民用曙暮光 (太阳在地平线下6°):")
    print(f"      开始: {format_time(civil['dawn'], '%H:%M')}")
    print(f"      结束: {format_time(civil['dusk'], '%H:%M')}")
    
    print(f"  🔹 航海曙暮光 (太阳在地平线下12°):")
    print(f"      开始: {format_time(nautical['dawn'], '%H:%M')}")
    print(f"      结束: {format_time(nautical['dusk'], '%H:%M')}")
    
    print(f"  🌌 天文曙暮光 (太阳在地平线下18°):")
    print(f"      开始: {format_time(astronomical['dawn'], '%H:%M')}")
    print(f"      结束: {format_time(astronomical['dusk'], '%H:%M')}")


def example_golden_hour():
    """黄金时刻示例（摄影）"""
    print("\n" + "=" * 60)
    print("示例 4: 黄金时刻计算（摄影最佳时段）")
    print("=" * 60)
    
    beijing_lat = 39.9042
    beijing_lon = 116.4074
    beijing_tz = 8.0
    d = date(2024, 6, 21)
    
    golden = get_golden_hour(beijing_lat, beijing_lon, d, beijing_tz)
    
    print(f"\n📍 北京 - {d}")
    print("-" * 60)
    
    print(f"\n📸 黄金时刻 (太阳高度角 2°-10°):")
    print(f"  早晨: {format_time(golden['morning_start'], '%H:%M')} - {format_time(golden['morning_end'], '%H:%M')}")
    print(f"  傍晚: {format_time(golden['evening_start'], '%H:%M')} - {format_time(golden['evening_end'], '%H:%M')}")
    
    print(f"\n💡 摄影建议:")
    print(f"  - 早晨黄金时刻光线柔和，适合拍摄风景和建筑")
    print(f"  - 傍晚黄金时刻色彩温暖，适合拍摄人像和剪影")


def example_solar_position():
    """太阳位置追踪示例"""
    print("\n" + "=" * 60)
    print("示例 5: 太阳位置追踪")
    print("=" * 60)
    
    beijing_lat = 39.9042
    beijing_lon = 116.4074
    beijing_tz = 8.0
    d = date(2024, 6, 21)
    
    print(f"\n📍 北京 - {d}")
    print("-" * 60)
    
    # 每小时追踪太阳位置
    hours = [6, 9, 12, 15, 18]
    
    print(f"\n太阳位置变化:")
    for hour in hours:
        dt = datetime(d.year, d.month, d.day, hour, 0)
        pos = get_solar_position(beijing_lat, beijing_lon, dt, beijing_tz)
        
        # 方位角描述
        azimuth = pos['azimuth']
        direction = ""
        if azimuth < 45 or azimuth >= 315:
            direction = "北"
        elif azimuth < 90:
            direction = "东北"
        elif azimuth < 135:
            direction = "东"
        elif azimuth < 180:
            direction = "东南"
        elif azimuth < 225:
            direction = "南"
        elif azimuth < 270:
            direction = "西南"
        elif azimuth < 315:
            direction = "西"
        
        altitude_str = f"+{pos['altitude']:.1f}°" if pos['altitude'] >= 0 else f"{pos['altitude']:.1f}°"
        
        print(f"  {hour}:00 - 方位角: {azimuth:.1f}° ({direction}), 高度角: {altitude_str}")


def example_seasonal_variation():
    """季节变化示例"""
    print("\n" + "=" * 60)
    print("示例 6: 全年白昼时长变化")
    print("=" * 60)
    
    beijing_lat = 39.9042
    beijing_lon = 116.4074
    beijing_tz = 8.0
    
    print(f"\n📍 北京 - 2024年白昼时长变化")
    print("-" * 60)
    
    # 每月15日
    months = [
        ('一月', 1, 15),
        ('二月', 2, 15),
        ('三月', 3, 15),
        ('四月', 4, 15),
        ('五月', 5, 15),
        ('六月', 6, 21),  # 夏至
        ('七月', 7, 15),
        ('八月', 8, 15),
        ('九月', 9, 15),
        ('十月', 10, 15),
        ('十一月', 11, 15),
        ('十二月', 12, 21),  # 冬至
    ]
    
    for name, month, day in months:
        d = date(2024, month, day)
        day_len = get_day_length(beijing_lat, beijing_lon, d, beijing_tz)
        
        if day_len:
            hours = day_len.total_seconds() / 3600
            sunrise = get_sunrise(beijing_lat, beijing_lon, d, beijing_tz)
            sunset = get_sunset(beijing_lat, beijing_lon, d, beijing_tz)
            
            print(f"  {name} ({month}/{day}):")
            print(f"    日出: {format_time(sunrise, '%H:%M')}, 日落: {format_time(sunset, '%H:%M')}, 白昼: {hours:.2f}小时")


def example_polar_regions():
    """极地地区示例"""
    print("\n" + "=" * 60)
    print("示例 7: 极地地区（极昼极夜）")
    print("=" * 60)
    
    # 北极圈附近
    print(f"\n📍 高纬度地区测试:")
    print("-" * 60)
    
    locations = [
        ('特隆赫姆 (挪威)', 63.4, 10.4, 1.0),
        ('摩尔曼斯克 (俄罗斯)', 68.97, 33.08, 3.0),
        ('特罗姆瑟 (挪威)', 69.65, 18.96, 1.0),
    ]
    
    # 夏至和冬至
    summer = date(2024, 6, 21)
    winter = date(2024, 12, 21)
    
    for name, lat, lon, tz in locations:
        print(f"\n{name} ({lat}°N):")
        
        # 夏至
        sunrise_summer = get_sunrise(lat, lon, summer, tz)
        sunset_summer = get_sunset(lat, lon, summer, tz)
        day_len_summer = get_day_length(lat, lon, summer, tz)
        
        print(f"  夏至:")
        if sunrise_summer and sunset_summer:
            hours = day_len_summer.total_seconds() / 3600 if day_len_summer else 0
            print(f"    白昼: {hours:.1f} 小时 (接近极昼)")
        else:
            print(f"    极昼 (太阳不落下)")
        
        # 冬至
        sunrise_winter = get_sunrise(lat, lon, winter, tz)
        sunset_winter = get_sunset(lat, lon, winter, tz)
        day_len_winter = get_day_length(lat, lon, winter, tz)
        
        print(f"  冬至:")
        if sunrise_winter is None:
            print(f"    极夜 (太阳不升起)")
        elif day_len_winter:
            hours = day_len_winter.total_seconds() / 3600
            print(f"    白昼: {hours:.1f} 小时")


def example_is_daylight_check():
    """白天判断示例"""
    print("\n" + "=" * 60)
    print("示例 8: 实时白天判断")
    print("=" * 60)
    
    beijing_lat = 39.9042
    beijing_lon = 116.4074
    beijing_tz = 8.0
    
    print(f"\n📍 北京 - 当前时间")
    print("-" * 60)
    
    now = datetime.now()
    is_day = is_daylight(beijing_lat, beijing_lon, now, beijing_tz)
    
    print(f"\n当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"是否白天: {'是 ☀️' if is_day else '否 🌙'}")
    
    # 模拟不同时间
    print(f"\n不同时间的白天状态:")
    test_times = ['06:00', '09:00', '12:00', '15:00', '18:00', '21:00', '00:00']
    
    sunrise = get_sunrise(beijing_lat, beijing_lon, now.date(), beijing_tz)
    sunset = get_sunset(beijing_lat, beijing_lon, now.date(), beijing_tz)
    
    for t in test_times:
        h, m = map(int, t.split(':'))
        dt = datetime(now.year, now.month, now.day, h, m)
        is_day = is_daylight(beijing_lat, beijing_lon, dt, beijing_tz)
        print(f"  {t}: {'白天 ☀️' if is_day else '夜晚 🌙'}")


def example_complete_info():
    """综合信息示例"""
    print("\n" + "=" * 60)
    print("示例 9: 完整太阳信息")
    print("=" * 60)
    
    beijing_lat = 39.9042
    beijing_lon = 116.4074
    beijing_tz = 8.0
    d = date(2024, 6, 21)
    
    info = get_solar_info(beijing_lat, beijing_lon, d, beijing_tz)
    
    print(f"\n📍 北京 - {d}")
    print("-" * 60)
    
    print(f"\n🌅 日出日落:")
    print(f"  日出: {format_time(info['sunrise'])}")
    print(f"  日落: {format_time(info['sunset'])}")
    print(f"  正午: {format_time(info['solar_noon'])}")
    print(f"  白昼时长: {info['day_length_hours']:.2f} 小时")
    
    print(f"\n🕐 曙暮光:")
    print(f"  民用: {format_time(info['civil_twilight']['dawn'])} - {format_time(info['civil_twilight']['dusk'])}")
    print(f"  航海: {format_time(info['nautical_twilight']['dawn'])} - {format_time(info['nautical_twilight']['dusk'])}")
    print(f"  天文: {format_time(info['astronomical_twilight']['dawn'])} - {format_time(info['astronomical_twilight']['dusk'])}")
    
    print(f"\n📸 黄金时刻:")
    gh = info['golden_hour']
    print(f"  早晨: {format_time(gh['morning_start'])} - {format_time(gh['morning_end'])}")
    print(f"  傍晚: {format_time(gh['evening_start'])} - {format_time(gh['evening_end'])}")
    
    print(f"\n📐 太阳参数:")
    print(f"  正午高度角: {info['solar_noon_altitude']:.1f}°")
    print(f"  太阳赤纬: {info['declination']:.4f}°")
    
    # 季节
    season = get_sun_phase(d, 'north')
    season_names = {'spring': '春季', 'summer': '夏季', 'autumn': '秋季', 'winter': '冬季'}
    print(f"\n🌸 季节: {season_names.get(season, season)}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("🌞 Solar Utils 使用示例集")
    print("=" * 60)
    
    example_basic_usage()
    example_multiple_cities()
    example_twilight_times()
    example_golden_hour()
    example_solar_position()
    example_seasonal_variation()
    example_polar_regions()
    example_is_daylight_check()
    example_complete_info()
    
    print("\n" + "=" * 60)
    print("✅ 所有示例完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()