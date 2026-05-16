"""
节拍器工具模块测试

测试 metronome_utils 模块的所有功能，
覆盖 BPM 计算、节拍生成、速度标记、拍号处理等。

作者: AllToolkit
日期: 2026-05-17
"""

import sys
import time
import unittest
from pathlib import Path

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent))

from mod import (
    Metronome,
    TimeSignature,
    TempoMarking,
    Subdivision,
    Beat,
    PracticeSession,
    bpm_to_ms,
    bpm_to_seconds,
    ms_to_bpm,
    seconds_to_bpm,
    get_tempo_marking,
    get_bpm_range_for_tempo,
    calculate_measures,
    calculate_duration,
    adjust_bpm_for_exercise,
    get_subdivision_name,
    calculate_delay_time,
    calculate_reverb_pre_delay,
    time_signature_to_string,
    parse_time_signature,
    get_time_signature_info,
    generate_rhythm_pattern,
    suggest_bpm_for_genre,
    create_practice_routine,
    calculate_polymetric_bpm,
    get_metronome_exercise
)


class TestBPMConversion(unittest.TestCase):
    """BPM 转换测试"""
    
    def test_bpm_to_ms_basic(self):
        """测试基本 BPM 到毫秒转换"""
        # 60 BPM = 1秒 = 1000毫秒
        self.assertEqual(bpm_to_ms(60), 1000.0)
        
        # 120 BPM = 0.5秒 = 500毫秒
        self.assertEqual(bpm_to_ms(120), 500.0)
        
        # 30 BPM = 2秒 = 2000毫秒
        self.assertEqual(bpm_to_ms(30), 2000.0)
        
    def test_bpm_to_ms_edge_cases(self):
        """测试边界值"""
        # 极高 BPM
        self.assertAlmostEqual(bpm_to_ms(250), 240.0, places=1)
        
        # 极低 BPM
        self.assertAlmostEqual(bpm_to_ms(20), 3000.0, places=1)
        
    def test_bpm_to_ms_invalid(self):
        """测试无效输入"""
        with self.assertRaises(ValueError):
            bpm_to_ms(0)
            
        with self.assertRaises(ValueError):
            bpm_to_ms(-10)
            
    def test_bpm_to_seconds_basic(self):
        """测试 BPM 到秒转换"""
        self.assertEqual(bpm_to_seconds(60), 1.0)
        self.assertEqual(bpm_to_seconds(120), 0.5)
        self.assertEqual(bpm_to_seconds(30), 2.0)
        
    def test_ms_to_bpm_basic(self):
        """测试毫秒到 BPM 转换"""
        self.assertEqual(ms_to_bpm(1000), 60)
        self.assertEqual(ms_to_bpm(500), 120)
        self.assertEqual(ms_to_bpm(2000), 30)
        
    def test_seconds_to_bpm_basic(self):
        """测试秒到 BPM 转换"""
        self.assertEqual(seconds_to_bpm(1.0), 60)
        self.assertEqual(seconds_to_bpm(0.5), 120)
        self.assertEqual(seconds_to_bpm(2.0), 30)
        
    def test_conversion_roundtrip(self):
        """测试转换往返"""
        for bpm in [40, 60, 90, 120, 150, 200]:
            ms = bpm_to_ms(bpm)
            converted_bpm = ms_to_bpm(ms)
            self.assertEqual(converted_bpm, bpm)


class TestTempoMarking(unittest.TestCase):
    """速度标记测试"""
    
    def test_get_tempo_marking_basic(self):
        """测试基本速度标记获取"""
        # Largo 范围
        italian, chinese = get_tempo_marking(50)
        self.assertEqual(italian, "Largo")
        
        # Moderato 范围
        italian, chinese = get_tempo_marking(110)
        self.assertEqual(italian, "Moderato")
        
        # Allegro 范围
        italian, chinese = get_tempo_marking(140)
        self.assertEqual(italian, "Allegro")
        
        # Presto 范围
        italian, chinese = get_tempo_marking(190)
        self.assertEqual(italian, "Presto")
        
    def test_get_tempo_marking_edge_cases(self):
        """测试边界速度标记"""
        # 极慢
        italian, chinese = get_tempo_marking(15)
        self.assertEqual(italian, "Larghissimo")
        
        # 极快
        italian, chinese = get_tempo_marking(250)
        self.assertEqual(italian, "Prestissimo")
        
    def test_get_bpm_range_for_tempo(self):
        """测试从速度标记获取 BPM 范围"""
        # 意大利语
        min_bpm, max_bpm = get_bpm_range_for_tempo("Allegro")
        self.assertEqual(min_bpm, 120)
        self.assertEqual(max_bpm, 168)
        
        # 中文
        min_bpm, max_bpm = get_bpm_range_for_tempo("快板")
        self.assertEqual(min_bpm, 120)
        self.assertEqual(max_bpm, 168)
        
    def test_get_bpm_range_unknown(self):
        """测试未知速度标记"""
        min_bpm, max_bpm = get_bpm_range_for_tempo("未知标记")
        self.assertEqual(min_bpm, 108)  # 默认中速
        self.assertEqual(max_bpm, 120)


class TestTimeSignature(unittest.TestCase):
    """拍号测试"""
    
    def test_parse_time_signature_basic(self):
        """测试拍号解析"""
        beats, unit = parse_time_signature("4/4")
        self.assertEqual(beats, 4)
        self.assertEqual(unit, 4)
        
        beats, unit = parse_time_signature("6/8")
        self.assertEqual(beats, 6)
        self.assertEqual(unit, 8)
        
    def test_parse_time_signature_with_spaces(self):
        """测试带空格的拍号"""
        beats, unit = parse_time_signature(" 4 / 4 ")
        self.assertEqual(beats, 4)
        self.assertEqual(unit, 4)
        
    def test_parse_time_signature_invalid(self):
        """测试无效拍号"""
        # 返回默认值
        beats, unit = parse_time_signature("invalid")
        self.assertEqual(beats, 4)
        self.assertEqual(unit, 4)
        
    def test_time_signature_to_string(self):
        """测试拍号转字符串"""
        self.assertEqual(time_signature_to_string(4, 4), "4/4")
        self.assertEqual(time_signature_to_string(6, 8), "6/8")
        self.assertEqual(time_signature_to_string(3, 4), "3/4")
        
    def test_get_time_signature_info_simple(self):
        """测试简单拍号信息"""
        info = get_time_signature_info(4, 4)
        self.assertEqual(info['beats'], 4)
        self.assertEqual(info['beat_unit'], 4)
        self.assertFalse(info['is_compound'])
        self.assertEqual(info['downbeats'], [1, 3])
        
    def test_get_time_signature_info_compound(self):
        """测试复合拍号信息"""
        info = get_time_signature_info(6, 8)
        self.assertEqual(info['beats'], 6)
        self.assertEqual(info['beat_unit'], 8)
        self.assertTrue(info['is_compound'])
        self.assertEqual(info['beat_divisions'], 3)
        
    def test_get_time_signature_info_asymmetric(self):
        """测试不对称拍号"""
        info = get_time_signature_info(5, 4)
        self.assertEqual(info['beats'], 5)
        self.assertEqual(info['beat_unit'], 4)
        self.assertFalse(info['is_compound'])
        self.assertIn('不对称', info['name'])


class TestDurationCalculation(unittest.TestCase):
    """时长计算测试"""
    
    def test_calculate_measures_basic(self):
        """测试小节数计算"""
        # 60 BPM，60秒，4/4拍 = 60拍 = 15小节
        measures = calculate_measures(60, 60, 4)
        self.assertEqual(measures, 15.0)
        
        # 120 BPM，30秒 = 60拍 = 15小节
        measures = calculate_measures(120, 30, 4)
        self.assertEqual(measures, 15.0)
        
    def test_calculate_duration_basic(self):
        """测试时长计算"""
        # 60 BPM，10小节，4/4拍 = 40拍 = 40秒
        duration = calculate_duration(60, 10, 4)
        self.assertEqual(duration, 40.0)
        
        # 120 BPM，10小节 = 40拍 = 20秒
        duration = calculate_duration(120, 10, 4)
        self.assertEqual(duration, 20.0)
        
    def test_calculation_roundtrip(self):
        """测试计算往返"""
        bpm = 100
        measures = 12
        beats_per_measure = 4
        
        duration = calculate_duration(bpm, measures, beats_per_measure)
        calculated_measures = calculate_measures(bpm, duration, beats_per_measure)
        
        # 使用近似比较处理浮点数精度问题
        self.assertAlmostEqual(calculated_measures, measures, places=5)
        
    def test_calculate_zero(self):
        """测试零值"""
        self.assertEqual(calculate_measures(0, 60), 0.0)
        self.assertEqual(calculate_duration(0, 10), 0.0)
        self.assertEqual(calculate_measures(60, 0), 0.0)
        self.assertEqual(calculate_duration(60, 0), 0.0)


class TestSubdivision(unittest.TestCase):
    """细分测试"""
    
    def test_get_subdivision_name_basic(self):
        """测试细分名称获取"""
        self.assertEqual(get_subdivision_name(1), "四分音符")
        self.assertEqual(get_subdivision_name(2), "八分音符")
        self.assertEqual(get_subdivision_name(3), "三连音")
        self.assertEqual(get_subdivision_name(4), "十六分音符")
        self.assertEqual(get_subdivision_name(6), "六连音")
        self.assertEqual(get_subdivision_name(8), "三十二分音符")
        
    def test_get_subdivision_name_extended(self):
        """测试扩展细分名称"""
        self.assertEqual(get_subdivision_name(5), "五连音")
        self.assertEqual(get_subdivision_name(7), "七连音")
        self.assertEqual(get_subdivision_name(12), "十二连音")
        
    def test_get_subdivision_name_unknown(self):
        """测试未知细分"""
        self.assertEqual(get_subdivision_name(11), "11连音")


class TestDelayCalculation(unittest.TestCase):
    """延迟时间计算测试"""
    
    def test_calculate_delay_time_basic(self):
        """测试基本延迟时间"""
        # 60 BPM，四分音符 = 1000ms
        delay = calculate_delay_time(60, 'quarter')
        self.assertEqual(delay, 1000.0)
        
        # 120 BPM，八分音符 = 250ms
        delay = calculate_delay_time(120, 'eighth')
        self.assertEqual(delay, 250.0)
        
    def test_calculate_delay_time_various_notes(self):
        """测试各种音符时值"""
        quarter_delay = calculate_delay_time(120, 'quarter')
        
        # 全音符 = 4倍
        self.assertEqual(calculate_delay_time(120, 'whole'), quarter_delay * 4)
        
        # 二分音符 = 2倍
        self.assertEqual(calculate_delay_time(120, 'half'), quarter_delay * 2)
        
        # 十六分音符 = 1/4
        self.assertEqual(calculate_delay_time(120, 'sixteenth'), quarter_delay * 0.25)
        
    def test_calculate_delay_time_dotted(self):
        """测试附点音符"""
        quarter_delay = calculate_delay_time(120, 'quarter')
        
        # 附点二分音符 = 3倍
        self.assertEqual(calculate_delay_time(120, 'dotted_half'), quarter_delay * 3)
        
        # 附点四分音符 = 1.5倍
        self.assertEqual(calculate_delay_time(120, 'dotted_quarter'), quarter_delay * 1.5)
        
        # 附点八分音符 = 0.75倍
        self.assertEqual(calculate_delay_time(120, 'dotted_eighth'), quarter_delay * 0.75)
        
    def test_calculate_delay_time_triplet(self):
        """测试三连音"""
        quarter_delay = calculate_delay_time(120, 'quarter')
        
        # 三连音八分音符 = 1/3
        self.assertEqual(calculate_delay_time(120, 'triplet_eighth'), quarter_delay / 3)
        
    def test_calculate_reverb_pre_delay(self):
        """测试混响预延迟"""
        # 默认使用八分音符
        delay = calculate_reverb_pre_delay(120)
        self.assertEqual(delay, 250.0)
        
        # 指定音符时值
        delay = calculate_reverb_pre_delay(120, 'quarter')
        self.assertEqual(delay, 500.0)


class TestRhythmPattern(unittest.TestCase):
    """节奏模式测试"""
    
    def test_generate_rhythm_pattern_basic(self):
        """测试基本节奏模式生成"""
        pattern = [1, 1, 0, 1]  # 强 弱 休止 弱
        result = generate_rhythm_pattern(120, pattern, 1)
        
        self.assertEqual(len(result), 4)
        
        # 检查时间
        self.assertEqual(result[0]['time_ms'], 0)
        self.assertEqual(result[1]['time_ms'], 125)  # 500/4
        self.assertEqual(result[2]['time_ms'], 250)
        self.assertEqual(result[3]['time_ms'], 375)
        
        # 检查发声状态
        self.assertTrue(result[0]['has_note'])
        self.assertTrue(result[1]['has_note'])
        self.assertFalse(result[2]['has_note'])
        self.assertTrue(result[3]['has_note'])
        
    def test_generate_rhythm_pattern_multiple_measures(self):
        """测试多小节节奏模式"""
        pattern = [1, 0]  # 两个位置
        result = generate_rhythm_pattern(60, pattern, 2)
        
        self.assertEqual(len(result), 4)  # 2小节 * 2位置
        
        # 检查小节数
        self.assertEqual(result[0]['measure'], 1)
        self.assertEqual(result[2]['measure'], 2)
        
    def test_generate_rhythm_pattern_empty(self):
        """测试空模式"""
        result = generate_rhythm_pattern(120, [], 1)
        self.assertEqual(len(result), 0)


class TestGenreBPM(unittest.TestCase):
    """音乐风格 BPM 测试"""
    
    def test_suggest_bpm_for_genre_common(self):
        """测试常见风格"""
        result = suggest_bpm_for_genre('rock')
        self.assertEqual(result['min_bpm'], 110)
        self.assertEqual(result['max_bpm'], 140)
        self.assertEqual(result['genre'], '摇滚')
        
        result = suggest_bpm_for_genre('jazz')
        self.assertEqual(result['min_bpm'], 100)
        self.assertEqual(result['max_bpm'], 150)
        
    def test_suggest_bpm_for_genre_dance(self):
        """测试舞曲风格"""
        result = suggest_bpm_for_genre('house')
        self.assertEqual(result['min_bpm'], 120)
        self.assertEqual(result['max_bpm'], 130)
        
        result = suggest_bpm_for_genre('dubstep')
        self.assertEqual(result['min_bpm'], 140)
        self.assertEqual(result['max_bpm'], 150)
        
    def test_suggest_bpm_for_genre_classical(self):
        """测试古典风格"""
        result = suggest_bpm_for_genre('waltz')
        self.assertEqual(result['min_bpm'], 84)
        self.assertEqual(result['max_bpm'], 120)
        
    def test_suggest_bpm_for_genre_unknown(self):
        """测试未知风格"""
        result = suggest_bpm_for_genre('unknown_genre')
        self.assertEqual(result['min_bpm'], 60)
        self.assertEqual(result['max_bpm'], 200)
        self.assertEqual(result['suggested_bpm'], 120)


class TestPracticeRoutine(unittest.TestCase):
    """练习计划测试"""
    
    def test_create_practice_routine_basic(self):
        """测试基本练习计划"""
        routine = create_practice_routine(120, 60, 5, 'medium')
        
        # 应包含多个步骤
        self.assertTrue(len(routine) > 1)
        
        # 检查第一个和最后一个步骤
        self.assertEqual(routine[0]['bpm'], 60)
        self.assertEqual(routine[-1]['bpm'], 120)
        self.assertTrue(routine[0]['is_start'])
        self.assertTrue(routine[-1]['is_target'])
        
    def test_create_practice_routine_easy(self):
        """测试简单难度"""
        routine = create_practice_routine(100, 80, 3, 'easy')
        
        # 每次增加 5 BPM
        for i in range(1, len(routine)):
            diff = routine[i]['bpm'] - routine[i-1]['bpm']
            self.assertEqual(diff, 5)
            
    def test_create_practice_routine_hard(self):
        """测试困难难度"""
        routine = create_practice_routine(150, 100, 5, 'hard')
        
        # 每次增加 15 BPM（最后一步可能不同以达到目标）
        for i in range(1, len(routine) - 1):  # 不检查最后一步
            diff = routine[i]['bpm'] - routine[i-1]['bpm']
            self.assertEqual(diff, 15)
        
        # 最后一步应该达到目标
        self.assertEqual(routine[-1]['bpm'], 150)
            
    def test_create_practice_routine_same_bpm(self):
        """测试相同 BPM"""
        routine = create_practice_routine(100, 100)
        self.assertEqual(len(routine), 1)
        self.assertEqual(routine[0]['bpm'], 100)


class TestPolymetricBPM(unittest.TestCase):
    """多节奏 BPM 测试"""
    
    def test_calculate_polymetric_bpm_basic(self):
        """测试基本多节奏计算"""
        result = calculate_polymetric_bpm(60, 90)
        
        # 应有同步间隔
        self.assertGreater(result['sync_interval_seconds'], 0)
        
        # 应有拍数信息
        self.assertEqual(len(result['sync_interval_beats']), 2)
        
    def test_calculate_polymetric_bpm_same(self):
        """测试相同 BPM"""
        result = calculate_polymetric_bpm(120, 120)
        
        # 同步间隔应该是 1拍
        self.assertEqual(result['sync_interval_seconds'], 0.5)


class TestMetronomeExercise(unittest.TestCase):
    """节拍器练习测试"""
    
    def test_get_metronome_exercise_basic(self):
        """测试基础练习"""
        exercise = get_metronome_exercise('basic')
        
        self.assertEqual(exercise['name'], '基础节拍练习')
        self.assertEqual(exercise['difficulty'], '初级')
        self.assertIn('instructions', exercise)
        
    def test_get_metronome_exercise_subdivision(self):
        """测试细分练习"""
        exercise = get_metronome_exercise('subdivision')
        
        self.assertEqual(exercise['name'], '细分练习')
        self.assertEqual(exercise['difficulty'], '中级')
        
    def test_get_metronome_exercise_polyrhythm(self):
        """测试多节奏练习"""
        exercise = get_metronome_exercise('polyrhythm')
        
        self.assertEqual(exercise['name'], '多节奏练习')
        self.assertEqual(exercise['difficulty'], '高级')
        
    def test_get_metronome_exercise_unknown(self):
        """测试未知练习类型"""
        exercise = get_metronome_exercise('unknown')
        
        # 返回基础练习
        self.assertEqual(exercise['name'], '基础节拍练习')


class TestMetronomeClass(unittest.TestCase):
    """节拍器类测试"""
    
    def test_metronome_init(self):
        """测试初始化"""
        metronome = Metronome(bpm=120)
        
        self.assertEqual(metronome.bpm, 120)
        self.assertEqual(metronome.time_signature, TimeSignature.FOUR_FOUR)
        self.assertFalse(metronome.is_running)
        
    def test_metronome_bpm_limits(self):
        """测试 BPM 限制"""
        # 过低自动调整
        metronome = Metronome(bpm=10)
        self.assertEqual(metronome.bpm, 20)  # 最低限制
        
        # 过高自动调整
        metronome = Metronome(bpm=300)
        self.assertEqual(metronome.bpm, 250)  # 最高限制
        
    def test_metronome_set_bpm(self):
        """测试设置 BPM"""
        metronome = Metronome(bpm=100)
        metronome.bpm = 150
        self.assertEqual(metronome.bpm, 150)
        
        # 设置超出范围
        metronome.bpm = 500
        self.assertEqual(metronome.bpm, 250)
        
    def test_metronome_beat_duration(self):
        """测试拍时长计算"""
        metronome = Metronome(bpm=60)
        
        self.assertEqual(metronome.get_beat_duration_seconds(), 1.0)
        self.assertEqual(metronome.get_beat_duration_ms(), 1000.0)
        
    def test_metronome_measure_duration(self):
        """测试小节时长"""
        metronome = Metronome(bpm=60)
        
        # 4/4拍，1拍1秒，小节4秒
        self.assertEqual(metronome.get_measure_duration_seconds(), 4.0)
        self.assertEqual(metronome.get_measure_duration_ms(), 4000.0)
        
    def test_metronome_subdivision_duration(self):
        """测试细分时长"""
        metronome = Metronome(bpm=60, subdivision=Subdivision.EIGHTH)
        
        # 八分音符细分，每份500ms
        self.assertEqual(metronome.get_subdivision_duration_ms(), 500.0)
        
    def test_metronome_beats_per_measure(self):
        """测试每小节拍数"""
        metronome = Metronome(time_signature=TimeSignature.THREE_FOUR)
        self.assertEqual(metronome.beats_per_measure, 3)
        
        metronome.time_signature = TimeSignature.SIX_EIGHT
        self.assertEqual(metronome.beats_per_measure, 6)
        
    def test_metronome_downbeats(self):
        """测试强拍位置"""
        # 4/4拍，强拍在1和3
        metronome = Metronome(time_signature=TimeSignature.FOUR_FOUR)
        downbeats = metronome.get_downbeats()
        self.assertEqual(downbeats, [1, 3])
        
        # 6/8拍（复合拍号），强拍在1
        metronome.time_signature = TimeSignature.SIX_EIGHT
        downbeats = metronome.get_downbeats()
        self.assertEqual(downbeats, [1])
        
        # 12/8拍，强拍在1, 4, 7
        metronome.time_signature = TimeSignature.TWELVE_EIGHT
        downbeats = metronome.get_downbeats()
        self.assertEqual(downbeats, [1, 4, 7])
        
    def test_metronome_is_downbeat(self):
        """测试强拍判断"""
        metronome = Metronome(time_signature=TimeSignature.FOUR_FOUR)
        
        self.assertTrue(metronome.is_downbeat(1))
        self.assertFalse(metronome.is_downbeat(2))
        self.assertTrue(metronome.is_downbeat(3))
        self.assertFalse(metronome.is_downbeat(4))
        
    def test_metronome_generate_beats(self):
        """测试节拍生成"""
        metronome = Metronome(bpm=120, time_signature=TimeSignature.FOUR_FOUR)
        beats = metronome.generate_beats(2)  # 2小节
        
        # 应生成8拍
        self.assertEqual(len(beats), 8)
        
        # 检查节拍属性
        self.assertEqual(beats[0].position, 1)
        self.assertTrue(beats[0].is_downbeat)
        
        self.assertEqual(beats[1].position, 2)
        self.assertFalse(beats[1].is_downbeat)
        
    def test_metronome_generate_subdivisions(self):
        """测试细分生成"""
        metronome = Metronome(
            bpm=120,
            subdivision=Subdivision.SIXTEENTH
        )
        subdivisions = metronome.generate_subdivisions(2)
        
        # 2拍 * 4细分 = 8个细分
        self.assertEqual(len(subdivisions), 8)
        
        # 检查细分属性
        self.assertTrue(subdivisions[0]['is_first_subdivision'])
        self.assertFalse(subdivisions[1]['is_first_subdivision'])
        
    def test_metronome_current_beat(self):
        """测试当前拍位置"""
        metronome = Metronome(bpm=120)
        self.assertEqual(metronome.current_beat, 0)
        
    def test_metronome_practice_session(self):
        """测试练习会话信息"""
        metronome = Metronome(bpm=100)
        session = metronome.get_practice_session()
        
        self.assertEqual(session.bpm, 100)
        self.assertEqual(session.beats_played, 0)
        self.assertEqual(session.measures_completed, 0)


class TestAdjustBPM(unittest.TestCase):
    """BPM 递进测试"""
    
    def test_adjust_bpm_increasing(self):
        """测试 BPM 递增"""
        result = adjust_bpm_for_exercise(60, 120, 'medium')
        
        # 应从60递增到120，每次+10
        self.assertEqual(result[0], 60)
        self.assertTrue(120 in result)
        
    def test_adjust_bpm_decreasing(self):
        """测试 BPM 递减"""
        result = adjust_bpm_for_exercise(120, 60, 'medium')
        
        # 应从120递减到60
        self.assertEqual(result[0], 120)
        self.assertTrue(60 in result)
        
    def test_adjust_bpm_same(self):
        """测试相同 BPM"""
        result = adjust_bpm_for_exercise(100, 100)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 100)


class TestTempoMarkingEnum(unittest.TestCase):
    """速度标记枚举测试"""
    
    def test_tempo_marking_properties(self):
        """测试枚举属性"""
        marking = TempoMarking.ALLEGRO
        
        self.assertEqual(marking.italian, "Allegro")
        self.assertEqual(marking.min_bpm, 120)
        self.assertEqual(marking.max_bpm, 168)


class TestSubdivisionEnum(unittest.TestCase):
    """细分枚举测试"""
    
    def test_subdivision_properties(self):
        """测试细分属性"""
        sub = Subdivision.SIXTEENTH
        
        self.assertEqual(sub.divisions, 4)
        self.assertEqual(sub.name, "十六分音符")


class TestTimeSignatureEnum(unittest.TestCase):
    """拍号枚举测试"""
    
    def test_time_signature_values(self):
        """测试拍号值"""
        ts = TimeSignature.FOUR_FOUR
        self.assertEqual(ts.value, (4, 4))
        
        ts = TimeSignature.SIX_EIGHT
        self.assertEqual(ts.value, (6, 8))


class TestBeatDataClass(unittest.TestCase):
    """Beat 数据类测试"""
    
    def test_beat_creation(self):
        """测试 Beat 创建"""
        beat = Beat(
            position=1,
            is_downbeat=True,
            is_accent=True,
            beat_type='downbeat',
            time_ms=0.0
        )
        
        self.assertEqual(beat.position, 1)
        self.assertTrue(beat.is_downbeat)
        self.assertTrue(beat.is_accent)
        self.assertEqual(beat.beat_type, 'downbeat')
        self.assertEqual(beat.time_ms, 0.0)


class TestPracticeSessionDataClass(unittest.TestCase):
    """PracticeSession 数据类测试"""
    
    def test_practice_session_creation(self):
        """测试 PracticeSession 创建"""
        session = PracticeSession(
            bpm=120,
            time_signature=TimeSignature.FOUR_FOUR,
            duration_seconds=300.0,
            beats_played=600,
            measures_completed=150,
            subdivision=Subdivision.QUARTER
        )
        
        self.assertEqual(session.bpm, 120)
        self.assertEqual(session.duration_seconds, 300.0)
        self.assertEqual(session.beats_played, 600)


class TestEdgeCases(unittest.TestCase):
    """边界值测试"""
    
    def test_extremely_high_bpm(self):
        """测试极高 BPM"""
        self.assertAlmostEqual(bpm_to_ms(250), 240.0, places=1)
        italian, _ = get_tempo_marking(250)
        self.assertEqual(italian, "Prestissimo")
        
    def test_extremely_low_bpm(self):
        """测试极低 BPM"""
        self.assertAlmostEqual(bpm_to_ms(20), 3000.0, places=1)
        italian, _ = get_tempo_marking(20)
        self.assertEqual(italian, "Larghissimo")
        
    def test_fractional_bpm(self):
        """测试小数 BPM"""
        delay = calculate_delay_time(120.5, 'quarter')
        self.assertGreater(delay, 0)
        
    def test_large_pattern(self):
        """测试大节奏模式"""
        pattern = [1] * 100  # 100个位置
        result = generate_rhythm_pattern(120, pattern, 1)
        self.assertEqual(len(result), 100)
        
    def test_negative_duration(self):
        """测试负时长"""
        # 应返回 0
        measures = calculate_measures(60, -10)
        self.assertEqual(measures, 0.0)


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)