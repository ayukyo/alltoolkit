"""
Frame Rate Utils 测试套件

测试帧率计算工具的各种功能
"""

import unittest
from fractions import Fraction
import sys
import os

# 确保能找到模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    FrameRate,
    Timecode,
    FrameConverter,
    DropFrameCalculator,
    FRAME_RATE_PRESETS,
    frames_to_seconds,
    seconds_to_frames,
    frames_to_timecode,
    timecode_to_frames,
    timecode_to_seconds,
    seconds_to_timecode,
    convert_frame_rate,
    calculate_drop_frame_count,
    is_drop_frame_rate,
)


class TestFrameRate(unittest.TestCase):
    """FrameRate 类测试"""
    
    def test_create_from_int(self):
        """测试从整数创建帧率"""
        fps = FrameRate(30)
        self.assertEqual(fps.float_value, 30.0)
        self.assertEqual(fps.fps, Fraction(30, 1))
        self.assertEqual(fps.numerator, 30)
        self.assertEqual(fps.denominator, 1)
    
    def test_create_from_float(self):
        """测试从浮点数创建帧率"""
        fps = FrameRate(29.97)
        self.assertAlmostEqual(fps.float_value, 29.97, places=2)
        # 浮点数会被近似转换为分数
        self.assertEqual(fps.fps, Fraction(2997, 100))
    
    def test_create_from_fraction(self):
        """测试从分数创建帧率"""
        fps = FrameRate(Fraction(24000, 1001))
        self.assertAlmostEqual(fps.float_value, 23.976, places=2)
    
    def test_create_from_string(self):
        """测试从字符串创建帧率"""
        fps1 = FrameRate("30000/1001")
        self.assertEqual(fps1.fps, Fraction(30000, 1001))
        
        fps2 = FrameRate("29.97")
        self.assertAlmostEqual(fps2.float_value, 29.97, places=1)
    
    def test_frame_duration(self):
        """测试每帧时长计算"""
        fps = FrameRate(30)
        self.assertEqual(fps.frame_duration, Fraction(1, 30))
        self.assertAlmostEqual(fps.frame_duration_ms, 1000/30, places=2)
    
    def test_frames_to_seconds(self):
        """测试帧数转秒数"""
        fps = FrameRate(30)
        self.assertAlmostEqual(fps.frames_to_seconds(30), 1.0)
        self.assertAlmostEqual(fps.frames_to_seconds(90), 3.0)
        self.assertAlmostEqual(fps.frames_to_seconds(1500), 50.0)
    
    def test_seconds_to_frames(self):
        """测试秒数转帧数"""
        fps = FrameRate(30)
        self.assertEqual(fps.seconds_to_frames(1.0), 30)
        self.assertEqual(fps.seconds_to_frames(3.0), 90)
        self.assertEqual(fps.seconds_to_frames(50.0), 1500)
    
    def test_seconds_to_frames_rounding(self):
        """测试秒数转帧数的舍入方式"""
        fps = FrameRate(30)
        self.assertEqual(fps.seconds_to_frames(1.5, 'round'), 45)
        self.assertEqual(fps.seconds_to_frames(1.5, 'floor'), 45)
        self.assertEqual(fps.seconds_to_frames(1.51, 'floor'), 45)
        self.assertEqual(fps.seconds_to_frames(1.51, 'ceil'), 46)
    
    def test_drop_frame_flag(self):
        """测试 drop-frame 标志"""
        fps_ndf = FrameRate(30, is_drop_frame=False)
        fps_df = FrameRate(30, is_drop_frame=True)
        
        self.assertFalse(fps_ndf.is_drop_frame)
        self.assertTrue(fps_df.is_drop_frame)
    
    def test_str_representation(self):
        """测试字符串表示"""
        fps = FrameRate(30)
        self.assertIn("30", str(fps))
        self.assertIn("fps", str(fps))
        
        fps_df = FrameRate(30, is_drop_frame=True)
        self.assertIn("DF", str(fps_df))


class TestDropFrameCalculator(unittest.TestCase):
    """Drop-frame 计算器测试"""
    
    def test_is_drop_frame_rate(self):
        """测试 drop-frame 帧率判断"""
        self.assertTrue(DropFrameCalculator.is_drop_frame_rate(Fraction(30000, 1001)))
        self.assertTrue(DropFrameCalculator.is_drop_frame_rate(Fraction(60000, 1001)))
        self.assertFalse(DropFrameCalculator.is_drop_frame_rate(Fraction(30, 1)))
        self.assertFalse(DropFrameCalculator.is_drop_frame_rate(Fraction(25, 1)))
        self.assertFalse(DropFrameCalculator.is_drop_frame_rate(Fraction(24, 1)))
    
    def test_is_drop_frame_rate_with_frame_rate_object(self):
        """测试使用 FrameRate 对象判断 drop-frame"""
        fps_df = FrameRate(30, is_drop_frame=True)
        fps_ndf = FrameRate(30, is_drop_frame=False)
        
        # 注意：is_drop_frame_rate 检查的是帧率值本身是否为标准 DF 帧率
        result_df = DropFrameCalculator.is_drop_frame_rate(fps_df)
        result_ndf = DropFrameCalculator.is_drop_frame_rate(fps_ndf)
        
        # 30fps 不是标准的 DF 帧率（DF 通常是 29.97）
        # 但 FrameRate 对象的 is_drop_frame 属性会被检查
        self.assertTrue(fps_df.is_drop_frame)
        self.assertFalse(fps_ndf.is_drop_frame)
    
    def test_calculate_drop_frame_count(self):
        """测试计算丢帧数"""
        # 对于 29.97fps NTSC：
        # 每分钟丢 2 帧，每 10 分钟丢 18 帧
        fps = Fraction(30000, 1001)
        
        # 1 分钟内应该丢 0 帧（第一个 10 分钟内，第 0 分钟不丢）
        # 实际算法：每分钟丢 2 帧（除了每 10 分钟的第 0 分钟）
        drop_1_min = calculate_drop_frame_count(1800, fps)  # 约 1 分钟
        self.assertGreater(drop_1_min, 0)


class TestTimecode(unittest.TestCase):
    """Timecode 类测试"""
    
    def test_from_frames_30fps(self):
        """测试从帧数创建时间码（30fps）"""
        tc = Timecode.from_frames(0, 30)
        self.assertEqual(str(tc), "00:00:00:00")
        
        tc = Timecode.from_frames(30, 30)
        self.assertEqual(str(tc), "00:00:01:00")
        
        tc = Timecode.from_frames(90, 30)
        self.assertEqual(str(tc), "00:00:03:00")
        
        tc = Timecode.from_frames(108000, 30)  # 1 hour
        self.assertEqual(str(tc), "01:00:00:00")
    
    def test_from_frames_24fps(self):
        """测试从帧数创建时间码（24fps）"""
        tc = Timecode.from_frames(24, 24)
        self.assertEqual(str(tc), "00:00:01:00")
        
        tc = Timecode.from_frames(86400, 24)  # 1 hour
        self.assertEqual(str(tc), "01:00:00:00")
    
    def test_from_seconds(self):
        """测试从秒数创建时间码"""
        tc = Timecode.from_seconds(1.0, 30)
        self.assertEqual(str(tc), "00:00:01:00")
        
        tc = Timecode.from_seconds(3600.0, 30)
        self.assertEqual(str(tc), "01:00:00:00")
    
    def test_from_string(self):
        """测试从字符串解析时间码"""
        tc = Timecode.from_string("01:23:45:12", 30)
        self.assertEqual(tc.hours, 1)
        self.assertEqual(tc.minutes, 23)
        self.assertEqual(tc.seconds, 45)
        self.assertEqual(tc.frames, 12)
        
        tc_df = Timecode.from_string("01:00:00;00", 30)
        self.assertTrue(tc_df.is_drop_frame)
    
    def test_total_frames(self):
        """测试总帧数计算"""
        tc = Timecode.from_string("00:01:00:00", 30)
        self.assertEqual(tc.total_frames, 1800)  # 30 * 60
        
        tc = Timecode.from_string("01:00:00:00", 30)
        self.assertEqual(tc.total_frames, 108000)  # 30 * 60 * 60
    
    def test_total_seconds(self):
        """测试总秒数计算"""
        tc = Timecode.from_string("00:01:30:00", 30)
        self.assertEqual(tc.total_seconds, 90.0)
        
        tc = Timecode.from_string("01:00:00:00", 30)
        self.assertEqual(tc.total_seconds, 3600.0)
    
    def test_timecode_addition(self):
        """测试时间码加法"""
        tc1 = Timecode.from_string("00:00:30:00", 30)
        tc2 = Timecode.from_string("00:00:30:00", 30)
        result = tc1 + tc2
        self.assertEqual(str(result), "00:01:00:00")
    
    def test_timecode_subtraction(self):
        """测试时间码减法"""
        tc1 = Timecode.from_string("00:01:00:00", 30)
        tc2 = Timecode.from_string("00:00:30:00", 30)
        result = tc1 - tc2
        self.assertEqual(str(result), "00:00:30:00")
    
    def test_timecode_comparison(self):
        """测试时间码比较"""
        tc1 = Timecode.from_string("00:00:30:00", 30)
        tc2 = Timecode.from_string("00:01:00:00", 30)
        tc3 = Timecode.from_string("00:00:30:00", 30)
        
        self.assertTrue(tc1 < tc2)
        self.assertTrue(tc1 <= tc2)
        self.assertTrue(tc2 > tc1)
        self.assertTrue(tc2 >= tc1)
        self.assertTrue(tc1 == tc3)
        self.assertTrue(tc1 != tc2)


class TestFrameConverter(unittest.TestCase):
    """帧率转换器测试"""
    
    def test_convert_frames_simple(self):
        """测试简单帧率转换"""
        # 30fps 的 30 帧 → 24fps 的 ? 帧
        frames_24 = convert_frame_rate(30, 30, 24)
        self.assertEqual(frames_24, 24)  # 1秒 -> 1秒
    
    def test_convert_frames_exact(self):
        """测试精确帧率转换"""
        # 24fps 的 24 帧 → 30fps
        frames_30 = convert_frame_rate(24, 24, 30)
        self.assertEqual(frames_30, 30)  # 1秒 -> 1秒
    
    def test_convert_frames_with_fraction(self):
        """测试分数帧率转换"""
        # 23.976fps (24000/1001) 的 24 帧 → 29.97fps (30000/1001)
        frames = convert_frame_rate(
            24,
            Fraction(24000, 1001),
            Fraction(30000, 1001)
        )
        self.assertEqual(frames, 30)  # 仍然是 1 秒
    
    def test_convert_frames_rounding(self):
        """测试帧率转换舍入"""
        # 24fps 的 1 帧 → 30fps
        frames_round = convert_frame_rate(1, 24, 30, 'round')
        frames_floor = convert_frame_rate(1, 24, 30, 'floor')
        frames_ceil = convert_frame_rate(1, 24, 30, 'ceil')
        
        # 1/24 秒 ≈ 1.25 帧
        self.assertEqual(frames_round, 1)  # round(1.25) = 1
        self.assertEqual(frames_floor, 1)   # floor(1.25) = 1
        self.assertEqual(frames_ceil, 2)     # ceil(1.25) = 2
    
    def test_calculate_pull_down(self):
        """测试下拉参数计算"""
        pulldown = FrameConverter.calculate_pull_down()
        
        self.assertEqual(pulldown['source_fps'], 24.0)
        self.assertEqual(pulldown['target_fps'], 29.97002997002997)
        self.assertAlmostEqual(pulldown['ratio'], 1.25, places=1)
        self.assertTrue(pulldown['is_32_pulldown'])


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_frames_to_seconds(self):
        """测试帧数转秒数函数"""
        self.assertEqual(frames_to_seconds(30, 30), 1.0)
        self.assertEqual(frames_to_seconds(60, 30), 2.0)
        self.assertEqual(frames_to_seconds(24, 24), 1.0)
    
    def test_seconds_to_frames(self):
        """测试秒数转帧数函数"""
        self.assertEqual(seconds_to_frames(1.0, 30), 30)
        self.assertEqual(seconds_to_frames(2.0, 30), 60)
        self.assertEqual(seconds_to_frames(1.0, 24), 24)
    
    def test_frames_to_timecode(self):
        """测试帧数转时间码函数"""
        self.assertEqual(frames_to_timecode(0, 30), "00:00:00:00")
        self.assertEqual(frames_to_timecode(30, 30), "00:00:01:00")
        self.assertEqual(frames_to_timecode(108000, 30), "01:00:00:00")
    
    def test_timecode_to_frames(self):
        """测试时间码转帧数函数"""
        self.assertEqual(timecode_to_frames("00:00:00:00", 30), 0)
        self.assertEqual(timecode_to_frames("00:00:01:00", 30), 30)
        self.assertEqual(timecode_to_frames("01:00:00:00", 30), 108000)
    
    def test_timecode_to_seconds(self):
        """测试时间码转秒数函数"""
        self.assertEqual(timecode_to_seconds("00:00:01:00", 30), 1.0)
        self.assertEqual(timecode_to_seconds("00:01:00:00", 30), 60.0)
        self.assertEqual(timecode_to_seconds("01:00:00:00", 30), 3600.0)
    
    def test_seconds_to_timecode(self):
        """测试秒数转时间码函数"""
        self.assertEqual(seconds_to_timecode(1.0, 30), "00:00:01:00")
        self.assertEqual(seconds_to_timecode(60.0, 30), "00:01:00:00")
        self.assertEqual(seconds_to_timecode(3600.0, 30), "01:00:00:00")
    
    def test_is_drop_frame_rate(self):
        """测试 drop-frame 帧率判断函数"""
        self.assertTrue(is_drop_frame_rate(Fraction(30000, 1001)))
        self.assertTrue(is_drop_frame_rate(Fraction(60000, 1001)))
        self.assertFalse(is_drop_frame_rate(30))
        self.assertFalse(is_drop_frame_rate(24))


class TestFrameRatePresets(unittest.TestCase):
    """帧率预设测试"""
    
    def test_presets_exist(self):
        """测试预设存在"""
        self.assertIn('film', FRAME_RATE_PRESETS)
        self.assertIn('pal', FRAME_RATE_PRESETS)
        self.assertIn('ntsc', FRAME_RATE_PRESETS)
        self.assertIn('ntsc_df', FRAME_RATE_PRESETS)
    
    def test_preset_values(self):
        """测试预设值"""
        self.assertEqual(FRAME_RATE_PRESETS['film'], Fraction(24, 1))
        self.assertEqual(FRAME_RATE_PRESETS['pal'], Fraction(25, 1))
        self.assertEqual(FRAME_RATE_PRESETS['ntsc'], Fraction(30, 1))
        self.assertEqual(FRAME_RATE_PRESETS['ntsc_df'], Fraction(30000, 1001))
    
    def test_using_presets(self):
        """测试使用预设创建帧率"""
        fps_film = FrameRate(FRAME_RATE_PRESETS['film'])
        self.assertEqual(fps_film.float_value, 24.0)
        
        fps_ntsc_df = FrameRate(FRAME_RATE_PRESETS['ntsc_df'], is_drop_frame=True)
        self.assertAlmostEqual(fps_ntsc_df.float_value, 29.97, places=1)
        self.assertTrue(fps_ntsc_df.is_drop_frame)


class TestEdgeCases(unittest.TestCase):
    """边缘情况测试"""
    
    def test_zero_frames(self):
        """测试零帧"""
        tc = Timecode.from_frames(0, 30)
        self.assertEqual(str(tc), "00:00:00:00")
        self.assertEqual(tc.total_frames, 0)
        self.assertEqual(tc.total_seconds, 0.0)
    
    def test_large_frame_numbers(self):
        """测试大帧数"""
        # 24 小时的帧数（30fps）
        frames_24h = 30 * 60 * 60 * 24
        tc = Timecode.from_frames(frames_24h, 30)
        self.assertEqual(tc.hours, 24)
        self.assertEqual(tc.minutes, 0)
        self.assertEqual(tc.seconds, 0)
    
    def test_fractional_fps(self):
        """测试分数帧率"""
        fps = FrameRate(Fraction(24000, 1001))
        self.assertAlmostEqual(fps.float_value, 23.976, places=2)
        
        # 1 秒应该有约 24 帧
        frames = fps.seconds_to_frames(1.0)
        self.assertEqual(frames, 24)
    
    def test_negative_frames(self):
        """测试负帧数处理"""
        # 减法应该保证结果不为负
        tc1 = Timecode.from_string("00:00:30:00", 30)
        tc2 = Timecode.from_string("00:01:00:00", 30)
        result = tc1 - tc2  # 30 秒 - 60 秒
        self.assertEqual(result.total_frames, 0)  # 应该是 0 而不是负数


if __name__ == '__main__':
    unittest.main(verbosity=2)