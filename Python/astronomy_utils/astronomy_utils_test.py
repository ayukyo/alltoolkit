"""
astronomy_utils 测试用例

Author: AllToolkit
Date: 2026-05-24
"""

import unittest
from datetime import datetime, timedelta
from mod import (
    SolarSystemData, ConstellationData, AstronomyCalculator,
    MoonPhaseCalculator, StarData, CelestialBody, Constellation,
    RiseSetTimes, get_planet, get_all_planets, get_constellation,
    get_zodiac_constellations, calculate_moon_phase, get_star_info,
    date_to_julian_day, julian_day_to_date, au_to_km, km_to_light_year,
    calculate_light_travel_time
)


class TestCelestialBody(unittest.TestCase):
    """测试 CelestialBody 数据类"""
    
    def test_to_dict(self):
        """测试转换为字典"""
        body = CelestialBody(
            name="Earth", name_cn="地球", body_type="planet",
            mass_kg=5.972e24, radius_km=6371,
            orbital_period_days=365.25, rotation_period_hours=23.93,
            distance_au=1.0, moons=1, magnitude=-3.99, color="蓝绿色"
        )
        result = body.to_dict()
        
        self.assertEqual(result["name"], "Earth")
        self.assertEqual(result["name_cn"], "地球")
        self.assertEqual(result["body_type"], "planet")
        self.assertEqual(result["mass_kg"], 5.972e24)
        self.assertEqual(result["radius_km"], 6371)
        self.assertEqual(result["distance_au"], 1.0)
        self.assertEqual(result["moons"], 1)


class TestConstellation(unittest.TestCase):
    """测试 Constellation 数据类"""
    
    def test_to_dict(self):
        """测试转换为字典"""
        c = Constellation(
            name="Leo", name_cn="狮子座", abbreviation="Leo",
            area_sq_deg=947, brightest_star="轩辕十四",
            best_month=4, description="黄道第五宫"
        )
        result = c.to_dict()
        
        self.assertEqual(result["name"], "Leo")
        self.assertEqual(result["name_cn"], "狮子座")
        self.assertEqual(result["abbreviation"], "Leo")
        self.assertEqual(result["area_sq_deg"], 947)


class TestSolarSystemData(unittest.TestCase):
    """测试太阳系数据"""
    
    def test_get_all_planets(self):
        """测试获取所有行星"""
        planets = SolarSystemData.get_all_planets()
        self.assertEqual(len(planets), 8)
        
        # 检查行星名称
        planet_names = [p.name for p in planets]
        self.assertIn("Mercury", planet_names)
        self.assertIn("Venus", planet_names)
        self.assertIn("Earth", planet_names)
        self.assertIn("Mars", planet_names)
        self.assertIn("Jupiter", planet_names)
        self.assertIn("Saturn", planet_names)
        self.assertIn("Uranus", planet_names)
        self.assertIn("Neptune", planet_names)
    
    def test_get_planet_by_english_name(self):
        """测试通过英文名获取行星"""
        planet = SolarSystemData.get_planet("Jupiter")
        self.assertIsNotNone(planet)
        self.assertEqual(planet.name_cn, "木星")
        self.assertEqual(planet.moons, 95)
    
    def test_get_planet_by_chinese_name(self):
        """测试通过中文名获取行星"""
        planet = SolarSystemData.get_planet("火星")
        self.assertIsNotNone(planet)
        self.assertEqual(planet.name, "Mars")
        self.assertEqual(planet.moons, 2)
    
    def test_get_planet_invalid(self):
        """测试获取无效行星"""
        planet = SolarSystemData.get_planet("Pluto")
        # Pluto 不在行星列表中（在矮行星列表）
        self.assertIsNone(planet)
    
    def test_sun_data(self):
        """测试太阳数据"""
        sun = SolarSystemData.SUN
        self.assertEqual(sun.name_cn, "太阳")
        self.assertEqual(sun.body_type, "star")
        self.assertEqual(sun.magnitude, -26.74)
    
    def test_moon_data(self):
        """测试月球数据"""
        moon = SolarSystemData.MOON
        self.assertEqual(moon.name_cn, "月球")
        self.assertEqual(moon.body_type, "moon")
        self.assertAlmostEqual(moon.orbital_period_days, 27.32, places=2)
    
    def test_dwarf_planets(self):
        """测试矮行星数据"""
        pluto = SolarSystemData.DWARF_PLANETS["Pluto"]
        self.assertEqual(pluto.name_cn, "冥王星")
        self.assertEqual(pluto.body_type, "dwarf_planet")
        self.assertEqual(pluto.moons, 5)


class TestConstellationData(unittest.TestCase):
    """测试星座数据"""
    
    def test_get_zodiac(self):
        """测试获取黄道十二宫"""
        zodiac = ConstellationData.get_zodiac()
        # 使用便捷函数
        zodiac = get_zodiac_constellations()
        self.assertEqual(len(zodiac), 12)
        
        # 检查星座名称
        names_cn = [c.name_cn for c in zodiac]
        self.assertIn("白羊座", names_cn)
        self.assertIn("狮子座", names_cn)
        self.assertIn("天蝎座", names_cn)
    
    def test_get_constellation_by_name(self):
        """测试通过名称获取星座"""
        c = ConstellationData.get_constellation("Leo")
        self.assertIsNotNone(c)
        self.assertEqual(c.name_cn, "狮子座")
        self.assertEqual(c.best_month, 4)
    
    def test_get_constellation_by_chinese_name(self):
        """测试通过中文名获取星座"""
        c = ConstellationData.get_constellation("猎户座")
        self.assertIsNotNone(c)
        self.assertEqual(c.name, "Orion")
    
    def test_get_constellation_by_abbreviation(self):
        """测试通过缩写获取星座"""
        c = ConstellationData.get_constellation("UMa")
        self.assertIsNotNone(c)
        self.assertEqual(c.name_cn, "大熊座")
    
    def test_get_constellation_by_month(self):
        """测试按月份获取星座"""
        constellations = ConstellationData.get_constellation_by_month(1)
        self.assertTrue(len(constellations) > 0)
        
        # 1月份最佳观测的星座应该包含猎户座和金牛座
        names_cn = [c.name_cn for c in constellations]
        self.assertIn("猎户座", names_cn)


class TestAstronomyCalculator(unittest.TestCase):
    """测试天文学计算器"""
    
    def test_date_to_julian_day(self):
        """测试日期转儒略日"""
        # J2000.0
        dt = datetime(2000, 1, 1, 12, 0, 0)
        jd = AstronomyCalculator.date_to_julian_day(dt)
        self.assertAlmostEqual(jd, 2451545.0, places=2)
        
        # 2024年某日
        dt2 = datetime(2024, 6, 15, 0, 0, 0)
        jd2 = AstronomyCalculator.date_to_julian_day(dt2)
        self.assertTrue(jd2 > 2451545.0)
    
    def test_julian_day_to_date(self):
        """测试儒略日转日期"""
        jd = 2451545.0  # J2000.0
        dt = AstronomyCalculator.julian_day_to_date(jd)
        self.assertEqual(dt.year, 2000)
        self.assertEqual(dt.month, 1)
        self.assertEqual(dt.day, 1)
        self.assertEqual(dt.hour, 12)
    
    def test_julian_day_roundtrip(self):
        """测试儒略日往返转换"""
        dt = datetime(2024, 5, 24, 18, 0, 0)
        jd = AstronomyCalculator.date_to_julian_day(dt)
        dt2 = AstronomyCalculator.julian_day_to_date(jd)
        
        # 允许微小误差
        diff = abs((dt - dt2).total_seconds())
        self.assertLess(diff, 1.0)
    
    def test_calculate_greenwich_sidereal_time(self):
        """测试格林尼治恒星时计算"""
        dt = datetime(2024, 6, 15, 0, 0, 0)
        gst = AstronomyCalculator.calculate_greenwich_sidereal_time(dt)
        
        # 恒星时应该在 0-360 度之间
        self.assertGreaterEqual(gst, 0)
        self.assertLess(gst, 360)
    
    def test_calculate_local_sidereal_time(self):
        """测试本地恒星时计算"""
        dt = datetime(2024, 6, 15, 0, 0, 0)
        longitude = 120.0  # 东经120度
        
        lst = AstronomyCalculator.calculate_local_sidereal_time(dt, longitude)
        self.assertGreaterEqual(lst, 0)
        self.assertLess(lst, 360)
    
    def test_equatorial_to_horizontal(self):
        """测试赤道坐标转地平坐标"""
        # 天狼星位置
        ra = 101.29  # 度
        dec = -16.72  # 度
        
        # 北京纬度
        latitude = 39.9
        longitude = 116.4
        
        dt = datetime(2024, 6, 15, 20, 0, 0)
        
        az, alt = AstronomyCalculator.equatorial_to_horizontal(ra, dec, latitude, longitude, dt)
        
        # 方位角和高度角应该在合理范围内
        self.assertGreaterEqual(az, 0)
        self.assertLess(az, 360)
        self.assertGreaterEqual(alt, -90)
        self.assertLessEqual(alt, 90)
    
    def test_calculate_distance_km(self):
        """测试天文单位转千米"""
        distance_km = AstronomyCalculator.calculate_distance_km(1.0)
        self.assertAlmostEqual(distance_km, 149597870.7, places=1)
        
        distance_km2 = AstronomyCalculator.calculate_distance_km(1.524)  # 火星
        self.assertAlmostEqual(distance_km2, 1.524 * 149597870.7, places=1)
    
    def test_calculate_distance_ly(self):
        """测试千米转光年"""
        # 1光年约为 9.461e12 km
        ly = AstronomyCalculator.calculate_distance_ly(9.461e12)
        self.assertAlmostEqual(ly, 1.0, places=2)
    
    def test_calculate_angular_diameter(self):
        """测试角直径计算"""
        # 月球直径约3474km，距离约384400km
        angular_diameter = AstronomyCalculator.calculate_angular_diameter(3474, 384400)
        
        # 月球角直径约为30角分（1800角秒）
        self.assertGreater(angular_diameter, 1500)
        self.assertLess(angular_diameter, 2000)
    
    def test_calculate_light_travel_time(self):
        """测试光传播时间计算"""
        # 地球到太阳的距离
        distance_km = 149597870.7
        time = AstronomyCalculator.calculate_light_travel_time(distance_km)
        
        # 应该约为8分20秒（500秒）
        self.assertGreater(time.total_seconds(), 480)
        self.assertLess(time.total_seconds(), 520)
    
    def test_calculate_rise_set_times(self):
        """测试升起落下时间计算"""
        # 天狼星
        ra = 101.29
        dec = -16.72
        
        # 北京
        latitude = 39.9
        longitude = 116.4
        
        dt = datetime(2024, 6, 15, 0, 0, 0)
        
        result = AstronomyCalculator.calculate_rise_set_times(ra, dec, latitude, longitude, dt)
        
        self.assertFalse(result.is_circumpolar)
        self.assertFalse(result.is_never_rises)
        self.assertIsNotNone(result.rise_time)
        self.assertIsNotNone(result.set_time)
        self.assertIsNotNone(result.transit_time)


class TestMoonPhaseCalculator(unittest.TestCase):
    """测试月相计算器"""
    
    def test_calculate_moon_phase(self):
        """测试月相计算"""
        # 使用已知新月日期
        dt = datetime(2000, 1, 6, 18, 14, 0)
        moon_age, phase_index, name_cn, name_en = MoonPhaseCalculator.calculate_moon_phase(dt)
        
        # 应该是新月
        self.assertAlmostEqual(moon_age, 0, places=1)
        self.assertEqual(phase_index, 0)
        self.assertEqual(name_cn, "新月")
    
    def test_calculate_moon_phase_full(self):
        """测试满月计算"""
        # 新月后约14.8天应该是满月
        dt = datetime(2000, 1, 21, 18, 14, 0)  # 新月后约15天
        moon_age, phase_index, name_cn, name_en = MoonPhaseCalculator.calculate_moon_phase(dt)
        
        # 应该接近满月
        self.assertGreater(moon_age, 13)
        self.assertLess(moon_age, 16)
    
    def test_calculate_moon_phase_quarter(self):
        """测试弦月计算"""
        # 新月后约7天应该是上弦月
        dt = datetime(2000, 1, 13, 18, 14, 0)
        moon_age, phase_index, name_cn, name_en = MoonPhaseCalculator.calculate_moon_phase(dt)
        
        self.assertGreater(moon_age, 6)
        self.assertLess(moon_age, 8)
    
    def test_calculate_next_moon_phase(self):
        """测试下一个月相计算"""
        dt = datetime(2024, 5, 24, 18, 0, 0)
        
        # 下一个满月
        next_full = MoonPhaseCalculator.calculate_next_moon_phase(dt, 4)
        self.assertIsNotNone(next_full)
        self.assertGreater(next_full, dt)
    
    def test_calculate_moon_distance(self):
        """测试月球距离计算"""
        dt = datetime(2024, 5, 24, 18, 0, 0)
        distance = MoonPhaseCalculator.calculate_moon_distance(dt)
        
        # 月球距离应该在356500-406700 km之间
        self.assertGreater(distance, 350000)
        self.assertLess(distance, 410000)
    
    def test_phase_names(self):
        """测试月相名称"""
        self.assertEqual(MoonPhaseCalculator.PHASES_CN[0], "新月")
        self.assertEqual(MoonPhaseCalculator.PHASES_CN[4], "满月")
        self.assertEqual(MoonPhaseCalculator.PHASES_EN[0], "New Moon")
        self.assertEqual(MoonPhaseCalculator.PHASES_EN[4], "Full Moon")


class TestStarData(unittest.TestCase):
    """测试恒星数据"""
    
    def test_get_star_by_english_name(self):
        """测试通过英文名获取恒星"""
        star = StarData.get_star("Sirius")
        self.assertIsNotNone(star)
        self.assertEqual(star["name_cn"], "天狼星")
        self.assertEqual(star["magnitude"], -1.46)
    
    def test_get_star_by_chinese_name(self):
        """测试通过中文名获取恒星"""
        star = StarData.get_star("天狼星")
        self.assertIsNotNone(star)
        self.assertEqual(star["name"], "Sirius")
    
    def test_get_star_invalid(self):
        """测试获取无效恒星"""
        star = StarData.get_star("不存在的星")
        self.assertIsNone(star)
    
    def test_get_visible_stars(self):
        """测试获取可见恒星"""
        # 北京纬度
        latitude = 39.9
        visible = StarData.get_visible_stars(latitude)
        
        # 应该能看到多颗恒星
        self.assertGreater(len(visible), 10)
        
        # 最亮的应该是天狼星
        self.assertEqual(visible[0]["name"], "Sirius")
    
    def test_bright_stars_data(self):
        """测试亮星数据完整性"""
        # 应该有20颗亮星
        self.assertEqual(len(StarData.BRIGHT_STARS), 20)
        
        # 检查数据完整性
        for star_name, data in StarData.BRIGHT_STARS.items():
            self.assertIn("name_cn", data)
            self.assertIn("ra", data)
            self.assertIn("dec", data)
            self.assertIn("magnitude", data)
            self.assertIn("constellation", data)
            self.assertIn("distance_ly", data)


class TestRiseSetTimes(unittest.TestCase):
    """测试升起落下时间数据类"""
    
    def test_to_dict(self):
        """测试转换为字典"""
        rise = datetime(2024, 6, 15, 8, 0, 0)
        transit = datetime(2024, 6, 15, 14, 0, 0)
        set_time = datetime(2024, 6, 15, 20, 0, 0)
        
        rst = RiseSetTimes(
            rise_time=rise,
            transit_time=transit,
            set_time=set_time,
            is_circumpolar=False,
            is_never_rises=False
        )
        
        result = rst.to_dict()
        self.assertEqual(result["rise_time"], rise.isoformat())
        self.assertEqual(result["transit_time"], transit.isoformat())
        self.assertEqual(result["set_time"], set_time.isoformat())
        self.assertFalse(result["is_circumpolar"])
        self.assertFalse(result["is_never_rises"])
    
    def test_circumpolar(self):
        """测试拱极星"""
        rst = RiseSetTimes(
            rise_time=None,
            transit_time=None,
            set_time=None,
            is_circumpolar=True,
            is_never_rises=False
        )
        
        self.assertTrue(rst.is_circumpolar)
        self.assertFalse(rst.is_never_rises)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_get_planet(self):
        """测试获取行星便捷函数"""
        planet = get_planet("木星")
        self.assertIsNotNone(planet)
        self.assertEqual(planet.name, "Jupiter")
    
    def test_get_all_planets(self):
        """测试获取所有行星便捷函数"""
        planets = get_all_planets()
        self.assertEqual(len(planets), 8)
    
    def test_get_constellation(self):
        """测试获取星座便捷函数"""
        c = get_constellation("天蝎座")
        self.assertIsNotNone(c)
        self.assertEqual(c.name, "Scorpius")
    
    def test_get_zodiac_constellations(self):
        """测试获取黄道十二宫便捷函数"""
        zodiac = get_zodiac_constellations()
        self.assertEqual(len(zodiac), 12)
    
    def test_calculate_moon_phase_default(self):
        """测试月相计算默认参数"""
        moon_age, phase_index, name_cn, name_en = calculate_moon_phase()
        
        self.assertGreaterEqual(moon_age, 0)
        self.assertLess(moon_age, 30)
        self.assertIn(phase_index, range(8))
    
    def test_get_star_info(self):
        """测试获取恒星信息便捷函数"""
        star = get_star_info("织女一")
        self.assertIsNotNone(star)
        self.assertEqual(star["name"], "Vega")
    
    def test_date_to_julian_day(self):
        """测试儒略日便捷函数"""
        dt = datetime(2000, 1, 1, 12, 0, 0)
        jd = date_to_julian_day(dt)
        self.assertAlmostEqual(jd, 2451545.0, places=2)
    
    def test_julian_day_to_date(self):
        """测试日期便捷函数"""
        jd = 2451545.0
        dt = julian_day_to_date(jd)
        self.assertEqual(dt.year, 2000)
    
    def test_au_to_km(self):
        """测试天文单位转千米便捷函数"""
        km = au_to_km(1.0)
        self.assertAlmostEqual(km, 149597870.7, places=1)
    
    def test_km_to_light_year(self):
        """测试千米转光年便捷函数"""
        ly = km_to_light_year(9.461e12)
        self.assertAlmostEqual(ly, 1.0, places=2)
    
    def test_calculate_light_travel_time(self):
        """测试光传播时间便捷函数"""
        time = calculate_light_travel_time(149597870.7)
        self.assertGreater(time.total_seconds(), 480)
        self.assertLess(time.total_seconds(), 520)


if __name__ == "__main__":
    unittest.main()