#!/usr/bin/env python3
"""
Solar Utils 测试套件

测试日出日落时间计算功能
"""

import unittest
import math
from datetime import date, datetime, timedelta
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solar_utils.mod import (
    _julian_day,
    _julian_century,
    _solar_mean_anomaly,
    _solar_declination,
    _equation_of_time,
    _hour_angle,
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
    format_time,
    TWILIGHT_CIVIL,
    TWILIGHT_NAUTICAL,
    TWILIGHT_ASTRONOMICAL
)


class TestJulianDay(unittest.TestCase):
    """儒略日计算测试"""
    
    def test_julian_day_known_dates(self):
        """测试已知日期的儒略日"""
        # J2000纪元
        jd = _julian_day(date(2000, 1, 1))
        self.assertAlmostEqual(jd, 2451544.5, places=1)
        
        # 2024年夏至
        jd = _julian_day(date(2024, 6, 21))
        self.assertAlmostEqual(jd, 2460482.5, places=1)
    
    def test_julian_day_consistency(self):
        """测试连续日期的儒略日差值为1"""
        d1 = date(2024, 1, 1)
        d2 = date(2024, 1, 2)
        jd1 = _julian_day(d1)
        jd2 = _julian_day(d2)
        self.assertAlmostEqual(jd2 - jd1, 1.0, places=3)
    
    def test_julian_day_year_transition(self):
        """测试跨年的儒略日"""
        jd_before = _julian_day(date(2023, 12, 31))
        jd_after = _julian_day(date(2024, 1, 1))
        self.assertAlmostEqual(jd_after - jd_before, 1.0, places=3)


class TestSolarDeclination(unittest.TestCase):
    """太阳赤纬计算测试"""
    
    def test_declination_range(self):
        """太阳赤纬应在 -23.45° 到 +23.45° 之间"""
        for month in range(1, 13):
            d = date(2024, month, 15)
            jd = _julian_day(d)
            t = _julian_century(jd)
            dec = _solar_declination(t)
            self.assertGreaterEqual(dec, -23.45)
            self.assertLessEqual(dec, 23.45)
    
    def test_declination_solstice(self):
        """测试至点的太阳赤纬"""
        # 夏至（北半球）太阳赤纬应接近 +23.44°
        jd_summer = _julian_day(date(2024, 6, 21))
        t_summer = _julian_century(jd_summer)
        dec_summer = _solar_declination(t_summer)
        self.assertGreater(dec_summer, 23.0)
        
        # 冬至（北半球）太阳赤纬应接近 -23.44°
        jd_winter = _julian_day(date(2024, 12, 21))
        t_winter = _julian_century(jd_winter)
        dec_winter = _solar_declination(t_winter)
        self.assertLess(dec_winter, -23.0)
    
    def test_declination_equinox(self):
        """测试分点的太阳赤纬应接近0°"""
        # 春分
        jd_spring = _julian_day(date(2024, 3, 20))
        t_spring = _julian_century(jd_spring)
        dec_spring = _solar_declination(t_spring)
        self.assertAlmostEqual(dec_spring, 0.0, delta=1.5)
        
        # 秋分
        jd_autumn = _julian_day(date(2024, 9, 22))
        t_autumn = _julian_century(jd_autumn)
        dec_autumn = _solar_declination(t_autumn)
        self.assertAlmostEqual(dec_autumn, 0.0, delta=1.5)


class TestEquationOfTime(unittest.TestCase):
    """时差计算测试"""
    
    def test_equation_of_time_range(self):
        """时差应在 -15 到 +20 分钟之间"""
        for month in range(1, 13):
            d = date(2024, month, 15)
            jd = _julian_day(d)
            t = _julian_century(jd)
            eot = _equation_of_time(t)
            self.assertGreaterEqual(eot, -15)
            self.assertLessEqual(eot, 20)
    
    def test_equation_of_time_extremes(self):
        """测试时差极值日期（约2月11日和11月3日）"""
        # 11月初时差最大（约+16分钟）
        jd_nov = _julian_day(date(2024, 11, 3))
        t_nov = _julian_century(jd_nov)
        eot_nov = _equation_of_time(t_nov)
        self.assertGreater(eot_nov, 14)
        
        # 2月中旬时差最小（约-14分钟）
        jd_feb = _julian_day(date(2024, 2, 11))
        t_feb = _julian_century(jd_feb)
        eot_feb = _equation_of_time(t_feb)
        self.assertLess(eot_feb, -12)


class TestSunriseSunset(unittest.TestCase):
    """日出日落计算测试"""
    
    def test_sunrise_sunset_beijing_summer(self):
        """测试北京夏至日出日落"""
        # 2024年夏至，北京
        sunrise = get_sunrise(39.9042, 116.4074, date(2024, 6, 21), timezone=8.0)
        sunset = get_sunset(39.9042, 116.4074, date(2024, 6, 21), timezone=8.0)
        
        self.assertIsNotNone(sunrise)
        self.assertIsNotNone(sunset)
        
        # 夏至北京日出约4:46，日落约19:46
        self.assertLess(sunrise.hour, 5)  # 日出在5点前
        self.assertGreaterEqual(sunset.hour, 19)  # 日落在19点或之后
    
    def test_sunrise_sunset_beijing_winter(self):
        """测试北京冬至日出日落"""
        # 2024年冬至，北京
        sunrise = get_sunrise(39.9042, 116.4074, date(2024, 12, 21), timezone=8.0)
        sunset = get_sunset(39.9042, 116.4074, date(2024, 12, 21), timezone=8.0)
        
        self.assertIsNotNone(sunrise)
        self.assertIsNotNone(sunset)
        
        # 冬至北京日出约7:33，日落约16:53
        self.assertGreaterEqual(sunrise.hour, 7)  # 日出在7点或之后
        self.assertLess(sunset.hour, 18)  # 日落在18点前
    
    def test_sunrise_sunset_equator(self):
        """测试赤道日出日落（全年约6:00/18:00）"""
        # 新加坡
        sunrise = get_sunrise(1.3521, 103.8198, date(2024, 6, 21), timezone=8.0)
        sunset = get_sunset(1.3521, 103.8198, date(2024, 6, 21), timezone=8.0)
        
        self.assertIsNotNone(sunrise)
        self.assertIsNotNone(sunset)
        
        # 赤道附近日出日落时间变化小
        self.assertGreater(sunrise.hour, 5)
        self.assertLessEqual(sunrise.hour, 7)
        self.assertGreaterEqual(sunset.hour, 17)
        self.assertLessEqual(sunset.hour, 19)
    
    def test_polar_day_night(self):
        """测试极昼极夜"""
        # 北极夏至（极昼）
        sunrise_arctic = get_sunrise(80.0, 0.0, date(2024, 6, 21), timezone=0.0)
        # 应该返回None或表示极昼
        # 或者日出时间很早，日落时间很晚
        
        # 北极冬至（极夜）
        sunrise_arctic_winter = get_sunrise(80.0, 0.0, date(2024, 12, 21), timezone=0.0)
        # 应该返回None（极夜）
        self.assertIsNone(sunrise_arctic_winter)
    
    def test_sunrise_before_sunset(self):
        """日出应该在日落之前"""
        for lat in [0, 30, 45, 60]:
            for month in [1, 4, 7, 10]:
                d = date(2024, month, 15)
                sunrise = get_sunrise(lat, 0.0, d, timezone=0.0)
                sunset = get_sunset(lat, 0.0, d, timezone=0.0)
                
                if sunrise and sunset:
                    self.assertLess(sunrise, sunset)


class TestSolarNoon(unittest.TestCase):
    """太阳正午计算测试"""
    
    def test_solar_noon_time(self):
        """正午时间应在12:00附近"""
        # 经度0°，时区0
        noon = get_solar_noon(0.0, date(2024, 6, 21), timezone=0.0)
        self.assertAlmostEqual(noon.hour + noon.minute/60.0, 12.0, delta=0.5)
    
    def test_solar_noon_longitude_correction(self):
        """测试经度修正"""
        # 东经120°（+8时区），正午应接近12:00
        noon_east = get_solar_noon(120.0, date(2024, 6, 21), timezone=8.0)
        self.assertAlmostEqual(noon_east.hour + noon_east.minute/60.0, 12.0, delta=0.5)
        
        # 西经120°（-8时区），正午也应接近12:00
        noon_west = get_solar_noon(-120.0, date(2024, 6, 21), timezone=-8.0)
        self.assertAlmostEqual(noon_west.hour + noon_west.minute/60.0, 12.0, delta=0.5)
    
    def test_solar_noon_equation_of_time(self):
        """测试时差对正午的影响"""
        # 11月初时差约+16分钟，正午会偏晚
        noon_nov = get_solar_noon(0.0, date(2024, 11, 3), timezone=0.0)
        
        # 2月中旬时差约-14分钟，正午会偏早
        noon_feb = get_solar_noon(0.0, date(2024, 2, 11), timezone=0.0)
        
        # 两者应该有约30分钟的差异
        diff = abs((noon_nov.hour * 60 + noon_nov.minute) - 
                   (noon_feb.hour * 60 + noon_feb.minute))
        self.assertGreater(diff, 20)


class TestDayLength(unittest.TestCase):
    """白昼时长计算测试"""
    
    def test_day_length_equator(self):
        """赤道白昼时长应接近12小时"""
        day_len = get_day_length(0.0, 0.0, date(2024, 6, 21))
        self.assertIsNotNone(day_len)
        hours = day_len.total_seconds() / 3600
        self.assertAlmostEqual(hours, 12.0, delta=0.3)
    
    def test_day_length_summer_vs_winter(self):
        """北半球夏至白昼应长于冬至"""
        day_summer = get_day_length(40.0, 0.0, date(2024, 6, 21))
        day_winter = get_day_length(40.0, 0.0, date(2024, 12, 21))
        
        self.assertIsNotNone(day_summer)
        self.assertIsNotNone(day_winter)
        
        self.assertGreater(day_summer, day_winter)
    
    def test_day_length_latitudinal_variation(self):
        """高纬度地区白昼时长变化更大"""
        # 低纬度
        variation_low = abs(
            get_day_length(20.0, 0.0, date(2024, 6, 21)).total_seconds() -
            get_day_length(20.0, 0.0, date(2024, 12, 21)).total_seconds()
        )
        
        # 高纬度
        variation_high = abs(
            get_day_length(60.0, 0.0, date(2024, 6, 21)).total_seconds() -
            get_day_length(60.0, 0.0, date(2024, 12, 21)).total_seconds()
        )
        
        self.assertGreater(variation_high, variation_low)
    
    def test_day_length_beijing_summer(self):
        """北京夏至白昼时长（约15小时）"""
        day_len = get_day_length(39.9042, 116.4074, date(2024, 6, 21), timezone=8.0)
        self.assertIsNotNone(day_len)
        hours = day_len.total_seconds() / 3600
        self.assertGreater(hours, 14.5)
        self.assertLess(hours, 15.5)


class TestTwilightTimes(unittest.TestCase):
    """曙暮光时间测试"""
    
    def test_twilight_order(self):
        """曙暮光时间顺序：天文 < 航海 < 民用 < 日出"""
        lat, lon = 40.0, 0.0
        d = date(2024, 6, 21)
        tz = 0.0
        
        civil = get_twilight_times(lat, lon, d, tz, 'civil')
        nautical = get_twilight_times(lat, lon, d, tz, 'nautical')
        astronomical = get_twilight_times(lat, lon, d, tz, 'astronomical')
        sunrise = get_sunrise(lat, lon, d, tz)
        sunset = get_sunset(lat, lon, d, tz)
        
        if all([civil['dawn'], nautical['dawn'], astronomical['dawn'], sunrise]):
            # 早晨：天文曙光最早，民用曙光最晚
            self.assertLess(astronomical['dawn'], nautical['dawn'])
            self.assertLess(nautical['dawn'], civil['dawn'])
            self.assertLess(civil['dawn'], sunrise)
        
        if all([civil['dusk'], nautical['dusk'], astronomical['dusk'], sunset]):
            # 傍晚：民用暮光最早，天文暮光最晚
            self.assertLess(sunset, civil['dusk'])
            self.assertLess(civil['dusk'], nautical['dusk'])
            self.assertLess(nautical['dusk'], astronomical['dusk'])
    
    def test_invalid_twilight_type(self):
        """测试无效曙暮光类型"""
        with self.assertRaises(ValueError):
            get_twilight_times(40.0, 0.0, date(2024, 6, 21), 0.0, 'invalid')


class TestSolarPosition(unittest.TestCase):
    """太阳位置计算测试"""
    
    def test_solar_noon_altitude(self):
        """正午太阳高度角应最大"""
        lat = 40.0
        lon = 0.0
        d = date(2024, 6, 21)
        
        # 正午
        noon = get_solar_noon(lon, d, 0.0)
        pos_noon = get_solar_position(lat, lon, noon, 0.0)
        
        # 上午9点
        pos_morning = get_solar_position(lat, lon, datetime(2024, 6, 21, 9, 0), 0.0)
        
        # 下午3点
        pos_afternoon = get_solar_position(lat, lon, datetime(2024, 6, 21, 15, 0), 0.0)
        
        # 正午高度角应大于上午和下午
        self.assertGreater(pos_noon['altitude'], pos_morning['altitude'])
        self.assertGreater(pos_noon['altitude'], pos_afternoon['altitude'])
    
    def test_azimuth_range(self):
        """方位角应在0-360度之间"""
        pos = get_solar_position(40.0, 0.0, datetime(2024, 6, 21, 12, 0), 0.0)
        self.assertGreaterEqual(pos['azimuth'], 0)
        self.assertLess(pos['azimuth'], 360)
    
    def test_altitude_range(self):
        """高度角应在-90到90度之间"""
        for hour in range(0, 24, 3):
            pos = get_solar_position(40.0, 0.0, datetime(2024, 6, 21, hour, 0), 0.0)
            self.assertGreaterEqual(pos['altitude'], -90)
            self.assertLessEqual(pos['altitude'], 90)
    
    def test_midnight_altitude(self):
        """午夜太阳高度角应为负值"""
        pos = get_solar_position(40.0, 0.0, datetime(2024, 6, 21, 0, 0), 0.0)
        self.assertLess(pos['altitude'], 0)


class TestGoldenHour(unittest.TestCase):
    """黄金时刻计算测试"""
    
    def test_golden_hour_order(self):
        """黄金时刻顺序：日出后和日落前"""
        lat = 40.0
        lon = 0.0
        d = date(2024, 6, 21)
        tz = 0.0
        
        golden = get_golden_hour(lat, lon, d, tz)
        sunrise = get_sunrise(lat, lon, d, tz)
        sunset = get_sunset(lat, lon, d, tz)
        
        if golden['morning_start'] and sunrise:
            # 早晨黄金时刻应在日出后
            self.assertGreater(golden['morning_start'], sunrise)
        
        if golden['evening_end'] and sunset:
            # 傍晚黄金时刻结束应在日落前
            self.assertLess(golden['evening_end'], sunset)
    
    def test_golden_hour_morning_before_evening(self):
        """早晨黄金时刻应早于傍晚黄金时刻"""
        golden = get_golden_hour(40.0, 0.0, date(2024, 6, 21), 0.0)
        
        if golden['morning_end'] and golden['evening_start']:
            # 早晨结束和傍晚开始可能有重叠（在太阳高度10°附近）
            # 允许一定重叠
            diff_seconds = (golden['evening_start'] - golden['morning_end']).total_seconds()
            # 早晨结束应该至少不晚于傍晚开始太多
            self.assertGreater(diff_seconds, -3600)  # 允许1小时重叠


class TestSolarInfo(unittest.TestCase):
    """太阳信息综合测试"""
    
    def test_solar_info_completeness(self):
        """测试返回信息完整性"""
        info = get_solar_info(39.9042, 116.4074, date(2024, 6, 21), 8.0)
        
        required_keys = [
            'date', 'latitude', 'longitude', 'timezone',
            'sunrise', 'sunset', 'solar_noon', 'day_length',
            'day_length_hours', 'civil_twilight', 'nautical_twilight',
            'astronomical_twilight', 'golden_hour', 'solar_noon_altitude',
            'declination'
        ]
        
        for key in required_keys:
            self.assertIn(key, info)
    
    def test_solar_info_consistency(self):
        """测试各时间值的一致性"""
        info = get_solar_info(39.9042, 116.4074, date(2024, 6, 21), 8.0)
        
        # 正午应在日出和日落之间
        if info['sunrise'] and info['sunset']:
            self.assertGreater(info['solar_noon'], info['sunrise'])
            self.assertLess(info['solar_noon'], info['sunset'])
        
        # 白昼时长与日出日落时间差一致
        if info['day_length']:
            expected = info['sunset'] - info['sunrise']
            self.assertAlmostEqual(
                info['day_length'].total_seconds(),
                expected.total_seconds(),
                delta=60
            )


class TestIsDaylight(unittest.TestCase):
    """白天判断测试"""
    
    def test_daylight_at_noon(self):
        """正午应该是白天"""
        dt = datetime(2024, 6, 21, 12, 0)
        self.assertTrue(is_daylight(40.0, 0.0, dt, 0.0))
    
    def test_night_at_midnight(self):
        """午夜应该是夜晚"""
        dt = datetime(2024, 6, 21, 0, 0)
        self.assertFalse(is_daylight(40.0, 0.0, dt, 0.0))
    
    def test_daylight_consistency_with_sunrise_sunset(self):
        """白天判断应与日出日落一致"""
        lat, lon = 40.0, 0.0
        d = date(2024, 6, 21)
        tz = 0.0
        
        sunrise = get_sunrise(lat, lon, d, tz)
        sunset = get_sunset(lat, lon, d, tz)
        
        if sunrise and sunset:
            # 日出后1小时
            dt_after_sunrise = sunrise + timedelta(hours=1)
            self.assertTrue(is_daylight(lat, lon, dt_after_sunrise, tz))
            
            # 日落前1小时
            dt_before_sunset = sunset - timedelta(hours=1)
            self.assertTrue(is_daylight(lat, lon, dt_before_sunset, tz))
            
            # 日出前1小时
            dt_before_sunrise = sunrise - timedelta(hours=1)
            self.assertFalse(is_daylight(lat, lon, dt_before_sunrise, tz))
            
            # 日落后1小时
            dt_after_sunset = sunset + timedelta(hours=1)
            self.assertFalse(is_daylight(lat, lon, dt_after_sunset, tz))


class TestSunPhase(unittest.TestCase):
    """季节相位测试"""
    
    def test_sun_phase_summer(self):
        """夏至应为夏季（北半球）"""
        phase = get_sun_phase(date(2024, 6, 21), 'north')
        self.assertEqual(phase, 'summer')
    
    def test_sun_phase_winter(self):
        """冬至应为冬季（北半球）"""
        # 使用12月22日，确保太阳黄经已进入冬季范围
        phase = get_sun_phase(date(2024, 12, 22), 'north')
        self.assertEqual(phase, 'winter')
    
    def test_sun_phase_spring(self):
        """春分附近应为春季"""
        phase = get_sun_phase(date(2024, 3, 25), 'north')
        self.assertEqual(phase, 'spring')
    
    def test_sun_phase_autumn(self):
        """秋分附近应为秋季"""
        phase = get_sun_phase(date(2024, 9, 25), 'north')
        self.assertEqual(phase, 'autumn')
    
    def test_sun_phase_south_hemisphere(self):
        """南半球季节应相反"""
        # 南半球夏至应为冬季（北半球夏季时南半球是冬季）
        phase = get_sun_phase(date(2024, 6, 21), 'south')
        self.assertEqual(phase, 'winter')
        
        # 南半球冬至应为夏季（北半球冬季时南半球是夏季）
        phase = get_sun_phase(date(2024, 12, 22), 'south')
        self.assertEqual(phase, 'summer')


class TestFormatTime(unittest.TestCase):
    """时间格式化测试"""
    
    def test_format_time_valid(self):
        """测试有效时间格式化"""
        dt = datetime(2024, 6, 21, 14, 30, 45)
        self.assertEqual(format_time(dt, '%H:%M:%S'), '14:30:45')
        self.assertEqual(format_time(dt, '%H:%M'), '14:30')
    
    def test_format_time_none(self):
        """测试None值格式化"""
        self.assertEqual(format_time(None), 'N/A')
    
    def test_format_time_default(self):
        """测试默认格式"""
        dt = datetime(2024, 6, 21, 14, 30, 45)
        self.assertEqual(format_time(dt), '14:30:45')


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_extreme_latitudes(self):
        """测试极端纬度"""
        # 赤道
        sunrise_eq = get_sunrise(0.0, 0.0, date(2024, 6, 21))
        self.assertIsNotNone(sunrise_eq)
        
        # 高纬度（非极昼极夜区）
        sunrise_high = get_sunrise(65.0, 0.0, date(2024, 6, 21))
        # 可能是极昼
        if sunrise_high:
            self.assertIsInstance(sunrise_high, datetime)
    
    def test_negative_longitude(self):
        """测试负经度"""
        # 纽约
        sunrise = get_sunrise(40.7128, -74.0060, date(2024, 6, 21), timezone=-5.0)
        self.assertIsNotNone(sunrise)
    
    def test_negative_latitude(self):
        """测试负纬度（南半球）"""
        # 悉尼
        sunrise = get_sunrise(-33.8688, 151.2093, date(2024, 6, 21), timezone=10.0)
        self.assertIsNotNone(sunrise)
    
    def test_date_at_year_boundary(self):
        """测试跨年日期"""
        sunrise = get_sunrise(40.0, 0.0, date(2023, 12, 31))
        self.assertIsNotNone(sunrise)
        
        sunrise = get_sunrise(40.0, 0.0, date(2024, 1, 1))
        self.assertIsNotNone(sunrise)
    
    def test_leap_year(self):
        """测试闰年"""
        # 2024是闰年
        sunrise = get_sunrise(40.0, 0.0, date(2024, 2, 29))
        self.assertIsNotNone(sunrise)
    
    def test_timezones(self):
        """测试不同时区"""
        for tz in [-12, -8, -5, 0, 1, 8, 12]:
            sunrise = get_sunrise(40.0, 0.0, date(2024, 6, 21), timezone=float(tz))
            self.assertIsNotNone(sunrise)


class TestAccuracyValidation(unittest.TestCase):
    """精度验证测试"""
    
    def test_beijing_sunrise_accuracy(self):
        """验证北京日出时间精度（与已知数据对比）"""
        # 2024年6月21日北京日出时间约为4:46
        sunrise = get_sunrise(39.9042, 116.4074, date(2024, 6, 21), timezone=8.0)
        self.assertIsNotNone(sunrise)
        
        expected_minutes = 4 * 60 + 46  # 4:46
        actual_minutes = sunrise.hour * 60 + sunrise.minute
        
        # 允许10分钟误差（天文计算精度有限）
        self.assertAlmostEqual(actual_minutes, expected_minutes, delta=10)
    
    def test_beijing_sunset_accuracy(self):
        """验证北京日落时间精度"""
        # 2024年6月21日北京日落时间约为19:46
        sunset = get_sunset(39.9042, 116.4074, date(2024, 6, 21), timezone=8.0)
        self.assertIsNotNone(sunset)
        
        expected_minutes = 19 * 60 + 46
        actual_minutes = sunset.hour * 60 + sunset.minute
        
        self.assertAlmostEqual(actual_minutes, expected_minutes, delta=5)
    
    def test_london_sunrise_accuracy(self):
        """验证伦敦日出时间精度"""
        # 2024年6月21日伦敦日出时间约为4:43
        sunrise = get_sunrise(51.5074, -0.1278, date(2024, 6, 21), timezone=1.0)
        self.assertIsNotNone(sunrise)
        
        expected_minutes = 4 * 60 + 43
        actual_minutes = sunrise.hour * 60 + sunrise.minute
        
        self.assertAlmostEqual(actual_minutes, expected_minutes, delta=10)


class TestConvenience(unittest.TestCase):
    """便捷性测试"""
    
    def test_default_date(self):
        """测试默认日期为今天"""
        from solar_utils.mod import get_sunrise
        # 不传日期应该使用今天
        sunrise = get_sunrise(40.0, 0.0)
        self.assertIsNotNone(sunrise)
        self.assertEqual(sunrise.date(), date.today())
    
    def test_default_timezone(self):
        """测试默认时区为0"""
        sunrise = get_sunrise(40.0, 0.0, date(2024, 6, 21))
        self.assertIsNotNone(sunrise)


if __name__ == '__main__':
    unittest.main(verbosity=2)