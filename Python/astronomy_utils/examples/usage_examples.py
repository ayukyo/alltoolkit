"""
astronomy_utils 使用示例

Author: AllToolkit
Date: 2026-05-24
"""

from datetime import datetime, timedelta
from mod import (
    get_planet, get_all_planets, get_constellation, get_zodiac_constellations,
    calculate_moon_phase, get_star_info, StarData, AstronomyCalculator,
    MoonPhaseCalculator, SolarSystemData, date_to_julian_day, julian_day_to_date,
    au_to_km, km_to_light_year, calculate_light_travel_time
)


def example_planets():
    """太阳系行星示例"""
    print("=== 太阳系行星 ===")
    
    # 获取所有行星
    planets = get_all_planets()
    print(f"\n太阳系8大行星:")
    for p in planets:
        print(f"  {p.name_cn} ({p.name}):")
        print(f"    - 质量: {p.mass_kg:.2e} kg")
        print(f"    - 半径: {p.radius_km:.1f} km")
        print(f"    - 距太阳: {p.distance_au:.3f} AU")
        print(f"    - 公转周期: {p.orbital_period_days:.1f} 天")
        print(f"    - 卫星数: {p.moons}")
        print(f"    - 星等: {p.magnitude}")
        print(f"    - 颜色: {p.color}")
    
    # 获取单个行星
    jupiter = get_planet("木星")
    print(f"\n木星详情:")
    print(f"  卫星数: {jupiter.moons}")
    print(f"  距太阳: {au_to_km(jupiter.distance_au):.1e} km")


def example_constellations():
    """星座示例"""
    print("\n=== 星座数据 ===")
    
    # 黄道十二宫
    zodiac = get_zodiac_constellations()
    print(f"\n黄道十二宫:")
    for c in zodiac:
        print(f"  {c.name_cn} ({c.abbreviation}): {c.description}")
    
    # 获取特定星座
    leo = get_constellation("狮子座")
    print(f"\n狮子座详情:")
    print(f"  英文名: {leo.name}")
    print(f"  缩写: {leo.abbreviation}")
    print(f"  面积: {leo.area_sq_deg} 平方度")
    print(f"  最亮星: {leo.brightest_star}")
    print(f"  最佳观测月份: {leo.best_month}月")
    
    # 按月份查询
    june_const = StarData.get_constellation_by_month(6)
    print(f"\n6月最佳观测星座:")
    for c in june_const:
        print(f"  {c.name_cn}")


def example_stars():
    """恒星示例"""
    print("\n=== 恒星数据 ===")
    
    # 最亮的恒星
    print(f"\n最亮的20颗恒星:")
    for name, data in StarData.BRIGHT_STARS.items():
        print(f"  {data['name_cn']} ({name}):")
        print(f"    星等: {data['magnitude']:.2f}")
        print(f"    距离: {data['distance_ly']} 光年")
        print(f"    颜色: {data['color']}")
    
    # 获取特定恒星
    sirius = get_star_info("天狼星")
    print(f"\n天狼星详情:")
    print(f"  赤经: {sirius['ra']:.2f}°")
    print(f"  赤纬: {sirius['dec']:.2f}°")
    print(f"  星等: {sirius['magnitude']}")
    print(f"  距离: {sirius['distance_ly']} 光年")
    
    # 北京可见恒星
    visible = StarData.get_visible_stars(39.9)  # 北京纬度
    print(f"\n北京可见恒星 (前10颗):")
    for star in visible[:10]:
        print(f"  {star['name_cn']}: 星等 {star['magnitude']}")


def example_moon_phase():
    """月相示例"""
    print("\n=== 月相计算 ===")
    
    # 当前月相
    moon_age, phase_idx, name_cn, name_en = calculate_moon_phase()
    print(f"\n当前月相:")
    print(f"  月龄: {moon_age:.1f} 天")
    print(f"  月相: {name_cn} ({name_en})")
    
    # 特定日期月相
    dates = [
        datetime(2024, 1, 1, 0, 0, 0),
        datetime(2024, 6, 15, 0, 0, 0),
        datetime(2024, 12, 25, 0, 0, 0),
    ]
    print(f"\n特定日期月相:")
    for dt in dates:
        age, _, cn, en = calculate_moon_phase(dt)
        print(f"  {dt.strftime('%Y-%m-%d')}: {cn} ({en}), 月龄 {age:.1f}天")
    
    # 下一个满月
    now = datetime.now()
    next_full = MoonPhaseCalculator.calculate_next_moon_phase(now, 4)
    print(f"\n下一个满月: {next_full.strftime('%Y-%m-%d %H:%M')}")
    
    # 下一个新月
    next_new = MoonPhaseCalculator.calculate_next_moon_phase(now, 0)
    print(f"下一个新月: {next_new.strftime('%Y-%m-%d %H:%M')}")
    
    # 月球距离
    distance = MoonPhaseCalculator.calculate_moon_distance(now)
    print(f"\n当前月球距离: {distance:.0f} km")


def example_julian_day():
    """儒略日示例"""
    print("\n=== 儒略日转换 ===")
    
    # 一些重要日期
    dates = [
        datetime(2000, 1, 1, 12, 0, 0),   # J2000.0
        datetime(2024, 6, 15, 0, 0, 0),
        datetime.now(),
    ]
    
    print(f"\n日期转儒略日:")
    for dt in dates:
        jd = date_to_julian_day(dt)
        print(f"  {dt.strftime('%Y-%m-%d %H:%M')}: JD {jd:.5f}")
    
    # 儒略日转日期
    jds = [2451545.0, 2440587.5]  # J2000.0, Unix epoch起点
    print(f"\n儒略日转日期:")
    for jd in jds:
        dt = julian_day_to_date(jd)
        print(f"  JD {jd:.1f}: {dt.strftime('%Y-%m-%d %H:%M')}")


def example_coordinates():
    """坐标转换示例"""
    print("\n=== 坐标转换 ===")
    
    # 天狼星的赤道坐标
    ra = 101.29
    dec = -16.72
    
    # 北京的位置
    latitude = 39.9
    longitude = 116.4
    
    # 当前时间
    dt = datetime.now()
    
    # 转换为地平坐标
    az, alt = AstronomyCalculator.equatorial_to_horizontal(ra, dec, latitude, longitude, dt)
    print(f"\n天狼星在北京的地平坐标:")
    print(f"  时间: {dt.strftime('%Y-%m-%d %H:%M')}")
    print(f"  方位角: {az:.1f}°")
    print(f"  高度角: {alt:.1f}°")
    
    # 恒星时
    gst = AstronomyCalculator.calculate_greenwich_sidereal_time(dt)
    lst = AstronomyCalculator.calculate_local_sidereal_time(dt, longitude)
    print(f"\n恒星时:")
    print(f"  格林尼治恒星时: {gst:.1f}°")
    print(f"  北京本地恒星时: {lst:.1f}°")


def example_rise_set():
    """升起落下示例"""
    print("\n=== 升起落下时间 ===")
    
    # 天狼星
    ra = 101.29
    dec = -16.72
    
    # 北京
    latitude = 39.9
    longitude = 116.4
    
    dt = datetime(2024, 6, 15, 0, 0, 0)
    
    result = AstronomyCalculator.calculate_rise_set_times(ra, dec, latitude, longitude, dt)
    
    print(f"\n天狼星在北京 (2024年6月15日):")
    if result.is_circumpolar:
        print("  拱极星，永不落下")
    elif result.is_never_rises:
        print("  永不升起")
    else:
        print(f"  升起: {result.rise_time.strftime('%H:%M')}")
        print(f"  中天: {result.transit_time.strftime('%H:%M')}")
        print(f"  落下: {result.set_time.strftime('%H:%M')}")


def example_distance():
    """距离计算示例"""
    print("\n=== 距离计算 ===")
    
    # 天文单位转千米
    earth_sun_km = au_to_km(1.0)
    mars_sun_km = au_to_km(1.524)
    print(f"\n行星距太阳:")
    print(f"  地球: {earth_sun_km:.1e} km = 1 AU")
    print(f"  火星: {mars_sun_km:.1e} km = 1.524 AU")
    
    # 光传播时间
    earth_sun_time = calculate_light_travel_time(earth_sun_km)
    print(f"\n光传播时间:")
    print(f"  地球到太阳: {earth_sun_time.total_seconds():.0f} 秒 ({earth_sun_time.total_seconds()/60:.1f} 分钟)")
    
    # 月球到地球
    moon_distance = 384400
    moon_time = calculate_light_travel_time(moon_distance)
    print(f"  月球到地球: {moon_time.total_seconds():.2f} 秒")
    
    # 角直径
    moon_angular = AstronomyCalculator.calculate_angular_diameter(3474, 384400)
    sun_angular = AstronomyCalculator.calculate_angular_diameter(696340, 149597870.7)
    print(f"\n角直径:")
    print(f"  月球: {moon_angular:.0f} 角秒 ({moon_angular/60:.1f} 角分)")
    print(f"  太阳: {sun_angular:.0f} 角秒 ({sun_angular/60:.1f} 角分)")
    
    # 光年转换
    nearest_star = 4.37  # 南门二距离（光年）
    nearest_km = nearest_star * 9.461e12
    nearest_ly = km_to_light_year(nearest_km)
    print(f"\n南门二:")
    print(f"  距离: {nearest_ly:.2f} 光年 = {nearest_km:.1e} km")


def example_full_demo():
    """综合演示"""
    print("\n=== 综合天文演示 ===")
    
    dt = datetime.now()
    print(f"当前时间: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 月相
    moon_age, _, name_cn, _ = calculate_moon_phase(dt)
    print(f"月相: {name_cn}, 月龄 {moon_age:.1f}天")
    
    # 儒略日
    jd = date_to_julian_day(dt)
    print(f"儒略日: JD {jd:.5f}")
    
    # 恒星时（北京）
    gst = AstronomyCalculator.calculate_greenwich_sidereal_time(dt)
    lst = AstronomyCalculator.calculate_local_sidereal_time(dt, 116.4)
    print(f"格林尼治恒星时: {gst:.1f}°, 北京本地恒星时: {lst:.1f}°")
    
    # 可见恒星
    visible = StarData.get_visible_stars(39.9)[:5]
    print(f"北京可见亮星: {', '.join([s['name_cn'] for s in visible])}")
    
    # 下一个满月
    next_full = MoonPhaseCalculator.calculate_next_moon_phase(dt, 4)
    print(f"下一个满月: {next_full.strftime('%Y-%m-%d')}")


if __name__ == "__main__":
    example_planets()
    example_constellations()
    example_stars()
    example_moon_phase()
    example_julian_day()
    example_coordinates()
    example_rise_set()
    example_distance()
    example_full_demo()