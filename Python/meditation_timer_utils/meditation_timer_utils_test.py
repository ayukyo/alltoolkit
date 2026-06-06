"""
Meditation Timer Utils 测试套件

测试覆盖：
1. MeditationTimer - 计时器功能
2. BreathingGuide - 呼吸指导功能
3. SessionRecorder - 会话记录功能
4. MeditationAssistant - 综合助手功能
5. MeditationBell - 铃声生成功能
"""

import unittest
import time
import os
import tempfile
import threading
from datetime import datetime, timedelta

from meditation_timer import (
    BreathingPattern,
    BreathingPhase,
    BreathingCycle,
    MeditationSession,
    MeditationStats,
    BreathingGuide,
    MeditationTimer,
    SessionRecorder,
    MeditationBell,
    MeditationAssistant,
    format_duration,
    quick_meditation,
    guided_breathing,
)


class TestBreathingPattern(unittest.TestCase):
    """测试呼吸模式"""
    
    def test_breathing_pattern_enum(self):
        """测试呼吸模式枚举"""
        self.assertEqual(BreathingPattern.RELAXING_4_7_8.value, "4-7-8 放松呼吸")
        self.assertEqual(BreathingPattern.BOX_BREATHING.value, "箱式呼吸")
        self.assertEqual(BreathingPattern.CALMING_4_6.value, "镇静呼吸")
    
    def test_breathing_phase(self):
        """测试呼吸阶段"""
        phase = BreathingPhase("inhale", 4.0, "吸气...")
        self.assertEqual(phase.name, "inhale")
        self.assertEqual(phase.duration, 4.0)
        self.assertEqual(phase.instruction, "吸气...")
    
    def test_breathing_cycle(self):
        """测试呼吸循环"""
        phases = [
            BreathingPhase("inhale", 4.0, "吸气"),
            BreathingPhase("exhale", 6.0, "呼气"),
        ]
        cycle = BreathingCycle("测试呼吸", phases)
        
        self.assertEqual(cycle.pattern_name, "测试呼吸")
        self.assertEqual(len(cycle.phases), 2)
        self.assertEqual(cycle.get_total_duration(), 10.0)


class TestMeditationSession(unittest.TestCase):
    """测试冥想会话记录"""
    
    def test_session_creation(self):
        """测试会话创建"""
        session = MeditationSession(
            start_time="2024-01-01T10:00:00",
            duration_seconds=300.0,
            breathing_pattern=BreathingPattern.BOX_BREATHING.value
        )
        
        self.assertEqual(session.start_time, "2024-01-01T10:00:00")
        self.assertEqual(session.duration_seconds, 300.0)
        self.assertEqual(session.breathing_pattern, "箱式呼吸")
        self.assertFalse(session.completed)
    
    def test_session_to_dict(self):
        """测试会话序列化"""
        session = MeditationSession(
            start_time="2024-01-01T10:00:00",
            end_time="2024-01-01T10:05:00",
            duration_seconds=300.0,
            completed=True,
            notes="感觉很好"
        )
        
        data = session.to_dict()
        self.assertIsInstance(data, dict)
        self.assertEqual(data["start_time"], "2024-01-01T10:00:00")
        self.assertEqual(data["duration_seconds"], 300.0)
        self.assertTrue(data["completed"])
    
    def test_session_from_dict(self):
        """测试会话反序列化"""
        data = {
            "start_time": "2024-01-01T10:00:00",
            "end_time": "2024-01-01T10:05:00",
            "duration_seconds": 300.0,
            "breathing_pattern": "箱式呼吸",
            "completed": True,
            "notes": ""
        }
        
        session = MeditationSession.from_dict(data)
        self.assertEqual(session.start_time, "2024-01-01T10:00:00")
        self.assertEqual(session.duration_seconds, 300.0)
        self.assertTrue(session.completed)


class TestBreathingGuide(unittest.TestCase):
    """测试呼吸指导器"""
    
    def test_get_available_patterns(self):
        """测试获取可用模式"""
        guide = BreathingGuide()
        patterns = guide.get_available_patterns()
        
        self.assertIsInstance(patterns, list)
        self.assertGreater(len(patterns), 0)
        
        # 检查所有模式都有必要字段
        for pattern in patterns:
            self.assertIn("type", pattern)
            self.assertIn("total_duration", pattern)
            self.assertIn("phases", pattern)
    
    def test_set_pattern(self):
        """测试设置呼吸模式"""
        guide = BreathingGuide()
        guide.set_pattern(BreathingPattern.RELAXING_4_7_8)
        
        self.assertEqual(guide.pattern, BreathingPattern.RELAXING_4_7_8)
        self.assertIsNotNone(guide.cycle)
    
    def test_breathing_cycle_durations(self):
        """测试各呼吸模式的时长"""
        guide = BreathingGuide()
        
        # 4-7-8 呼吸: 4+7+8=19秒
        guide.set_pattern(BreathingPattern.RELAXING_4_7_8)
        self.assertEqual(guide.cycle.get_total_duration(), 19.0)
        
        # 箱式呼吸: 4+4+4+4=16秒
        guide.set_pattern(BreathingPattern.BOX_BREATHING)
        self.assertEqual(guide.cycle.get_total_duration(), 16.0)
        
        # 镇静呼吸: 4+6=10秒
        guide.set_pattern(BreathingPattern.CALMING_4_6)
        self.assertEqual(guide.cycle.get_total_duration(), 10.0)
    
    def test_start_stop(self):
        """测试启动和停止"""
        guide = BreathingGuide()
        
        # 启动
        guide.start(0.1)  # 6秒
        self.assertTrue(guide.is_running())
        
        # 停止
        guide.stop()
        self.assertFalse(guide.is_running())


class TestMeditationTimer(unittest.TestCase):
    """测试冥想计时器"""
    
    def test_set_duration(self):
        """测试设置时长"""
        timer = MeditationTimer(duration_minutes=10.0)
        self.assertEqual(timer.duration_minutes, 10.0)
        self.assertEqual(timer.duration_seconds, 600.0)
        
        timer.set_duration(5.0)
        self.assertEqual(timer.duration_minutes, 5.0)
        self.assertEqual(timer.duration_seconds, 300.0)
    
    def test_set_duration_while_running(self):
        """测试运行时修改时长应报错"""
        timer = MeditationTimer(duration_minutes=1.0)
        timer.start()
        
        with self.assertRaises(RuntimeError):
            timer.set_duration(2.0)
        
        timer.stop()
    
    def test_start_stop(self):
        """测试开始和停止"""
        timer = MeditationTimer(duration_minutes=0.1)  # 6秒
        
        session = timer.start()
        self.assertTrue(timer.is_running())
        self.assertIsNotNone(session.start_time)
        
        time.sleep(0.5)
        
        session = timer.stop(completed=True)
        self.assertFalse(timer.is_running())
        self.assertTrue(session.completed)
        self.assertGreater(session.duration_seconds, 0)
    
    def test_pause_resume(self):
        """测试暂停和继续"""
        timer = MeditationTimer(duration_minutes=0.1)
        
        timer.start()
        time.sleep(0.2)
        
        timer.pause()
        self.assertTrue(timer.is_paused())
        
        paused_elapsed = timer._elapsed
        
        time.sleep(0.2)
        
        # 暂停期间时间不应增加
        self.assertAlmostEqual(timer._elapsed, paused_elapsed, places=1)
        
        timer.resume()
        self.assertFalse(timer.is_paused())
        
        timer.stop()
    
    def test_get_status(self):
        """测试获取状态"""
        timer = MeditationTimer(duration_minutes=1.0)
        
        status = timer.get_status()
        self.assertFalse(status["is_running"])
        self.assertEqual(status["remaining_seconds"], 60.0)
        self.assertEqual(status["progress_percent"], 0)
        
        timer.start()
        time.sleep(0.5)
        
        status = timer.get_status()
        self.assertTrue(status["is_running"])
        self.assertGreater(status["elapsed_seconds"], 0)
        self.assertLess(status["remaining_seconds"], 60.0)
        self.assertGreater(status["progress_percent"], 0)
        
        timer.stop()
    
    def test_callbacks(self):
        """测试回调函数"""
        tick_calls = []
        complete_calls = []
        
        def on_tick(elapsed, remaining):
            tick_calls.append((elapsed, remaining))
        
        def on_complete():
            complete_calls.append(True)
        
        timer = MeditationTimer(duration_minutes=0.05)  # 3秒
        timer.set_callbacks(on_tick=on_tick, on_complete=on_complete)
        
        timer.start()
        time.sleep(3.5)  # 等待完成
        
        self.assertGreater(len(tick_calls), 0)
        self.assertEqual(len(complete_calls), 1)


class TestSessionRecorder(unittest.TestCase):
    """测试会话记录器"""
    
    def setUp(self):
        """使用临时文件"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close()
        self.recorder = SessionRecorder(storage_path=self.temp_file.name)
    
    def tearDown(self):
        """清理临时文件"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_record_session(self):
        """测试记录会话"""
        session = MeditationSession(
            start_time="2024-01-01T10:00:00",
            end_time="2024-01-01T10:10:00",
            duration_seconds=600.0,
            completed=True
        )
        
        self.recorder.record_session(session)
        sessions = self.recorder.get_sessions()
        
        self.assertEqual(len(sessions), 1)
        self.assertEqual(sessions[0].duration_seconds, 600.0)
    
    def test_get_sessions_limit(self):
        """测试限制获取数量"""
        for i in range(5):
            session = MeditationSession(
                start_time=f"2024-01-0{i}T10:00:00",
                duration_seconds=300.0
            )
            self.recorder.record_session(session)
        
        sessions = self.recorder.get_sessions(limit=3)
        self.assertEqual(len(sessions), 3)
    
    def test_get_stats(self):
        """测试统计功能"""
        # 添加多个会话
        for i in range(3):
            session = MeditationSession(
                start_time=f"2024-01-{i+1:02d}T10:00:00",
                duration_seconds=600.0,
                completed=i < 2  # 前2个完成
            )
            self.recorder.record_session(session)
        
        stats = self.recorder.get_stats()
        
        self.assertEqual(stats.total_sessions, 3)
        self.assertEqual(stats.total_minutes, 30.0)  # 3 * 10分钟
        self.assertEqual(stats.completed_sessions, 2)
        self.assertEqual(stats.average_session_minutes, 10.0)
    
    def test_clear_sessions(self):
        """测试清空会话"""
        session = MeditationSession(
            start_time="2024-01-01T10:00:00",
            duration_seconds=300.0
        )
        self.recorder.record_session(session)
        
        self.assertEqual(len(self.recorder.get_sessions()), 1)
        
        self.recorder.clear_sessions()
        
        self.assertEqual(len(self.recorder.get_sessions()), 0)
    
    def test_persistence(self):
        """测试持久化"""
        session = MeditationSession(
            start_time="2024-01-01T10:00:00",
            duration_seconds=300.0,
            completed=True
        )
        
        self.recorder.record_session(session)
        
        # 创建新的记录器，应该能加载之前的记录
        new_recorder = SessionRecorder(storage_path=self.temp_file.name)
        sessions = new_recorder.get_sessions()
        
        self.assertEqual(len(sessions), 1)
        self.assertEqual(sessions[0].start_time, "2024-01-01T10:00:00")


class TestMeditationBell(unittest.TestCase):
    """测试冥想铃声"""
    
    def test_generate_bell_sound(self):
        """测试生成铃声"""
        samples = MeditationBell.generate_bell_sound(
            frequency=432.0,
            duration=1.0,
            sample_rate=44100
        )
        
        # 检查样本数量
        self.assertEqual(len(samples), 44100)
        
        # 检查样本范围
        for sample in samples[:100]:  # 只检查前100个
            self.assertGreaterEqual(sample, -32768)
            self.assertLessEqual(sample, 32767)
    
    def test_to_wav_bytes(self):
        """测试生成WAV字节"""
        samples = MeditationBell.generate_bell_sound(duration=0.5)
        wav_data = MeditationBell.to_wav_bytes(samples)
        
        # 检查WAV头
        self.assertEqual(wav_data[:4], b'RIFF')
        self.assertEqual(wav_data[8:12], b'WAVE')
        self.assertEqual(wav_data[12:16], b'fmt ')
        self.assertEqual(wav_data[36:40], b'data')
    
    def test_different_frequencies(self):
        """测试不同频率"""
        freq_432 = MeditationBell.generate_bell_sound(frequency=432.0, duration=0.1)
        freq_528 = MeditationBell.generate_bell_sound(frequency=528.0, duration=0.1)
        
        # 不同频率应产生不同的样本
        self.assertNotEqual(freq_432[:100], freq_528[:100])


class TestMeditationAssistant(unittest.TestCase):
    """测试冥想助手"""
    
    def setUp(self):
        """使用临时文件"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close()
        self.assistant = MeditationAssistant(storage_path=self.temp_file.name)
    
    def tearDown(self):
        """清理"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_set_timer_duration(self):
        """测试设置时长"""
        self.assistant.set_timer_duration(15.0)
        self.assertEqual(self.assistant.timer.duration_minutes, 15.0)
    
    def test_start_end_meditation(self):
        """测试开始和结束冥想"""
        self.assistant.set_timer_duration(0.05)  # 3秒
        
        session = self.assistant.start_meditation()
        self.assertTrue(self.assistant.timer.is_running())
        self.assertIsNotNone(session.start_time)
        
        time.sleep(0.5)
        
        session = self.assistant.end_meditation(completed=True)
        self.assertFalse(self.assistant.timer.is_running())
        self.assertTrue(session.completed)
        
        # 检查会话已记录
        sessions = self.assistant.get_session_history()
        self.assertEqual(len(sessions), 1)
    
    def test_start_meditation_with_breathing(self):
        """测试带呼吸模式的冥想"""
        self.assistant.set_timer_duration(0.05)
        
        session = self.assistant.start_meditation(
            breathing_pattern=BreathingPattern.BOX_BREATHING
        )
        
        self.assertEqual(session.breathing_pattern, "箱式呼吸")
        
        self.assistant.end_meditation()
    
    def test_get_stats(self):
        """测试获取统计"""
        # 添加几个会话
        for i in range(3):
            self.assistant.set_timer_duration(0.02)
            self.assistant.start_meditation()
            time.sleep(0.3)
            self.assistant.end_meditation(completed=True)
        
        stats = self.assistant.get_stats()
        self.assertEqual(stats.total_sessions, 3)
        self.assertEqual(stats.completed_sessions, 3)
    
    def test_get_current_status(self):
        """测试获取当前状态"""
        self.assistant.set_timer_duration(0.1)
        
        status = self.assistant.get_current_status()
        self.assertFalse(status["is_running"])
        
        self.assistant.start_meditation()
        time.sleep(0.3)
        
        status = self.assistant.get_current_status()
        self.assertTrue(status["is_running"])
        self.assertGreater(status["elapsed_seconds"], 0)
        
        self.assistant.end_meditation()
    
    def test_get_breathing_patterns(self):
        """测试获取呼吸模式"""
        patterns = self.assistant.get_breathing_patterns()
        
        self.assertIsInstance(patterns, list)
        self.assertGreater(len(patterns), 0)
    
    def test_generate_bell_wav(self):
        """测试生成铃声"""
        wav_data = MeditationAssistant.generate_bell_wav(
            frequency=432.0,
            duration=1.0
        )
        
        self.assertIsInstance(wav_data, bytes)
        self.assertGreater(len(wav_data), 0)
        self.assertEqual(wav_data[:4], b'RIFF')


class TestFormatDuration(unittest.TestCase):
    """测试时长格式化"""
    
    def test_seconds(self):
        """测试秒"""
        self.assertEqual(format_duration(30), "30.0秒")
        self.assertEqual(format_duration(59.5), "59.5秒")
    
    def test_minutes(self):
        """测试分钟"""
        self.assertEqual(format_duration(60), "1分钟")
        self.assertEqual(format_duration(120), "2分钟")
        self.assertEqual(format_duration(90), "1分30秒")
    
    def test_hours(self):
        """测试小时"""
        self.assertEqual(format_duration(3600), "1小时")
        self.assertEqual(format_duration(7200), "2小时")
        self.assertEqual(format_duration(3660), "1小时1分钟")


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def setUp(self):
        """使用临时文件"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close()
    
    def tearDown(self):
        """清理"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_full_meditation_flow(self):
        """测试完整冥想流程"""
        assistant = MeditationAssistant(storage_path=self.temp_file.name)
        
        # 设置时长
        assistant.set_timer_duration(0.1)  # 6秒
        
        # 开始冥想
        session = assistant.start_meditation(
            breathing_pattern=BreathingPattern.CALMING_4_6
        )
        
        self.assertIsNotNone(session.start_time)
        self.assertEqual(session.breathing_pattern, "镇静呼吸")
        
        # 等待计时器自然完成
        time.sleep(6.5)  # 等待超过设置的时长
        
        # 手动结束并记录（因为自然完成时需要调用 end_meditation）
        # 检查会话状态
        status = assistant.get_current_status()
        self.assertFalse(status["is_running"])
        
        # 记录会话
        assistant.recorder.record_session(assistant.timer._session)
        
        # 获取统计
        stats = assistant.get_stats()
        self.assertEqual(stats.total_sessions, 1)
    
    def test_concurrent_breathing_and_timer(self):
        """测试同时进行呼吸指导和计时"""
        assistant = MeditationAssistant(storage_path=self.temp_file.name)
        
        # 设置短时间
        assistant.set_timer_duration(0.05)
        
        # 启动呼吸指导
        phase_records = []
        
        def on_phase(phase, duration, instruction):
            phase_records.append(phase)
        
        assistant.start_breathing_guide(
            BreathingPattern.BOX_BREATHING,
            duration_minutes=0.05,
            callback=on_phase
        )
        
        # 同时启动冥想计时
        assistant.start_meditation()
        
        time.sleep(0.6)
        
        assistant.stop_breathing_guide()
        assistant.end_meditation()
        
        # 应该有一些呼吸阶段被记录
        self.assertGreater(len(phase_records), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)