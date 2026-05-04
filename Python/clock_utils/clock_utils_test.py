"""
clock_utils 测试文件
测试世界时钟、秒表、计时器、倒计时等功能
"""

import unittest
import time
from datetime import datetime, timedelta, timezone
from mod import (
    WorldClock, Stopwatch, Timer, TimeFormatter, 
    TimeDifference, Countdown, AlarmClock, PomodoroTimer,
    ClockFormat, get_world_time, get_multiple_times,
    create_timer, create_stopwatch, format_duration, create_countdown
)


class TestWorldClock(unittest.TestCase):
    """测试世界时钟"""
    
    def test_create_clock(self):
        """测试创建时钟"""
        clock = WorldClock("Beijing")
        self.assertIsNotNone(clock)
        self.assertEqual(clock.city, "Beijing")
    
    def test_get_current_time(self):
        """测试获取当前时间"""
        clock = WorldClock("Beijing")
        now = clock.get_current_time()
        self.assertIsInstance(now, datetime)
    
    def test_get_time_str(self):
        """测试时间字符串格式"""
        clock = WorldClock("Beijing")
        
        # 24小时制
        time_24 = clock.get_time_str(ClockFormat.FORMAT_24H)
        self.assertRegex(time_24, r"^\d{2}:\d{2}:\d{2}$")
        
        # 12小时制
        time_12 = clock.get_time_str(ClockFormat.FORMAT_12H)
        self.assertRegex(time_12, r"^\d{2}:\d{2}:\d{2} (AM|PM)$")
    
    def test_get_full_time_str(self):
        """测试完整时间字符串"""
        clock = WorldClock("Beijing")
        full_time = clock.get_full_time_str()
        self.assertRegex(full_time, r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
    
    def test_get_multiple_times(self):
        """测试多城市时间"""
        clock = WorldClock("Beijing")
        cities = ["Beijing", "Tokyo", "NewYork", "London"]
        times = clock.get_multiple_times(cities)
        
        self.assertEqual(len(times), 4)
        for city in cities:
            self.assertIn(city, times)
            self.assertIsInstance(times[city], str)
    
    def test_list_cities(self):
        """测试列出城市"""
        cities = WorldClock.list_cities()
        self.assertIn("Beijing", cities)
        self.assertIn("Tokyo", cities)
        self.assertIn("NewYork", cities)
    
    def test_string_representation(self):
        """测试字符串表示"""
        clock = WorldClock("Beijing")
        s = str(clock)
        self.assertIn("Beijing", s)


class TestStopwatch(unittest.TestCase):
    """测试秒表"""
    
    def test_create_stopwatch(self):
        """测试创建秒表"""
        sw = Stopwatch()
        self.assertEqual(sw.elapsed, 0.0)
        self.assertFalse(sw.is_running)
    
    def test_start_stopwatch(self):
        """测试启动秒表"""
        sw = Stopwatch()
        result = sw.start()
        self.assertTrue(result)
        self.assertTrue(sw.is_running)
    
    def test_pause_stopwatch(self):
        """测试暂停秒表"""
        sw = Stopwatch()
        sw.start()
        time.sleep(0.05)
        result = sw.pause()
        self.assertTrue(result)
        self.assertFalse(sw.is_running)
    
    def test_elapsed_time(self):
        """测试计时"""
        sw = Stopwatch()
        sw.start()
        time.sleep(0.1)
        elapsed = sw.elapsed
        self.assertGreater(elapsed, 0.09)
        self.assertLess(elapsed, 0.2)
    
    def test_reset_stopwatch(self):
        """测试重置秒表"""
        sw = Stopwatch()
        sw.start()
        time.sleep(0.05)
        sw.reset()
        
        self.assertEqual(sw.elapsed, 0.0)
        self.assertFalse(sw.is_running)
        self.assertEqual(len(sw.laps), 0)
    
    def test_lap_functionality(self):
        """测试计次功能"""
        sw = Stopwatch()
        sw.start()
        time.sleep(0.05)
        lap1 = sw.lap()
        time.sleep(0.05)
        lap2 = sw.lap()
        
        self.assertEqual(lap1.lap_number, 1)
        self.assertEqual(lap2.lap_number, 2)
        self.assertEqual(len(sw.laps), 2)
        self.assertGreater(lap2.total_time, lap1.total_time)
    
    def test_best_worst_lap(self):
        """测试最快最慢计次"""
        sw = Stopwatch()
        sw.start()
        time.sleep(0.03)
        sw.lap()
        time.sleep(0.08)  # 较慢的计次
        sw.lap()
        time.sleep(0.02)  # 最快的计次
        sw.lap()
        
        best = sw.get_best_lap()
        worst = sw.get_worst_lap()
        avg = sw.get_average_lap()
        
        self.assertIsNotNone(best)
        self.assertIsNotNone(worst)
        self.assertIsNotNone(avg)
        self.assertEqual(best.lap_number, 3)  # 最快的是第三个
        self.assertEqual(worst.lap_number, 2)  # 最慢的是第二个
    
    def test_elapsed_str(self):
        """测试格式化时长"""
        sw = Stopwatch()
        self.assertEqual(sw.elapsed_str, "00:00:00")


class TestTimer(unittest.TestCase):
    """测试计时器"""
    
    def test_create_timer(self):
        """测试创建计时器"""
        timer = Timer(10)
        self.assertEqual(timer.duration, 10)
        self.assertFalse(timer.is_running)
        self.assertFalse(timer.is_completed)
    
    def test_create_from_minutes(self):
        """测试从分钟创建"""
        timer = Timer.from_minutes(5)
        self.assertEqual(timer.duration, 300)
    
    def test_create_from_hours(self):
        """测试从小时创建"""
        timer = Timer.from_hours(1)
        self.assertEqual(timer.duration, 3600)
    
    def test_create_from_parts(self):
        """测试从时分秒创建"""
        timer = Timer.from_time_parts(hours=1, minutes=30, seconds=45)
        self.assertEqual(timer.duration, 3600 + 1800 + 45)
    
    def test_timer_countdown(self):
        """测试倒计时"""
        timer = Timer(0.2)
        timer.start()
        
        time.sleep(0.05)
        self.assertGreater(timer.remaining, 0)
        self.assertLess(timer.remaining, 0.2)
        
        time.sleep(0.2)
        timer.check()
        self.assertTrue(timer.is_completed)
    
    def test_pause_resume(self):
        """测试暂停继续"""
        timer = Timer(1)
        timer.start()
        time.sleep(0.05)
        timer.pause()
        
        remaining1 = timer.remaining
        time.sleep(0.1)
        remaining2 = timer.remaining
        
        self.assertEqual(remaining1, remaining2)  # 暂停时剩余时间不变
    
    def test_reset(self):
        """测试重置"""
        timer = Timer(0.1)
        timer.start()
        time.sleep(0.15)
        timer.check()
        self.assertTrue(timer.is_completed)
        
        timer.reset()
        self.assertFalse(timer.is_completed)
        self.assertEqual(timer.remaining, 0.1)
    
    def test_progress(self):
        """测试进度"""
        timer = Timer(1)
        timer.start()
        time.sleep(0.1)
        
        progress = timer.progress
        self.assertGreater(progress, 0)
        self.assertLess(progress, 0.5)
    
    def test_progress_bar(self):
        """测试进度条"""
        timer = Timer(1)
        bar = timer.get_progress_bar(width=10)
        self.assertEqual(bar, "░░░░░░░░░░")
        
        timer.start()
        time.sleep(0.5)
        bar = timer.get_progress_bar(width=10)
        # 进度条应该有部分填充
        self.assertIn("█", bar)
    
    def test_callback(self):
        """测试回调函数"""
        callback_called = []
        
        def callback(t):
            callback_called.append(True)
        
        timer = Timer(0.1, callback=callback)
        timer.start()
        time.sleep(0.2)
        timer.check()
        
        self.assertEqual(len(callback_called), 1)


class TestTimeFormatter(unittest.TestCase):
    """测试时间格式化"""
    
    def test_format_duration_seconds(self):
        """测试格式化秒"""
        self.assertEqual(TimeFormatter.format_duration(30), "00:00:30")
        self.assertEqual(TimeFormatter.format_duration(0), "00:00:00")
    
    def test_format_duration_minutes(self):
        """测试格式化分钟"""
        self.assertEqual(TimeFormatter.format_duration(60), "00:01:00")
        self.assertEqual(TimeFormatter.format_duration(90), "00:01:30")
    
    def test_format_duration_hours(self):
        """测试格式化小时"""
        self.assertEqual(TimeFormatter.format_duration(3600), "01:00:00")
        self.assertEqual(TimeFormatter.format_duration(3661), "01:01:01")
    
    def test_format_duration_milliseconds(self):
        """测试毫秒显示"""
        result = TimeFormatter.format_duration(1.5, show_ms=True)
        self.assertIn("500", result)
    
    def test_format_relative_just_now(self):
        """测试相对时间 - 刚刚"""
        delta = timedelta(seconds=30)
        result = TimeFormatter.format_relative(delta)
        self.assertEqual(result, "刚刚")
    
    def test_format_relative_minutes(self):
        """测试相对时间 - 分钟"""
        delta = timedelta(minutes=5)
        result = TimeFormatter.format_relative(delta)
        self.assertEqual(result, "5分钟前")
        
        result = TimeFormatter.format_relative(-delta)
        self.assertEqual(result, "5分钟后")
    
    def test_format_relative_hours(self):
        """测试相对时间 - 小时"""
        delta = timedelta(hours=3)
        result = TimeFormatter.format_relative(delta)
        self.assertEqual(result, "3小时前")
    
    def test_format_relative_days(self):
        """测试相对时间 - 天"""
        delta = timedelta(days=5)
        result = TimeFormatter.format_relative(delta)
        self.assertEqual(result, "5天前")
    
    def test_format_countdown(self):
        """测试倒计时格式化"""
        target = datetime.now() + timedelta(days=1, hours=2, minutes=30)
        result = TimeFormatter.format_countdown(target)
        self.assertIn("1天", result)
        self.assertIn("2时", result)
    
    def test_format_countdown_expired(self):
        """测试已过期倒计时"""
        target = datetime.now() - timedelta(seconds=1)
        result = TimeFormatter.format_countdown(target)
        self.assertEqual(result, "已过期")
    
    def test_humanize_seconds(self):
        """测试人性化秒数"""
        self.assertEqual(TimeFormatter.humanize_seconds(0.5), "500毫秒")
        self.assertEqual(TimeFormatter.humanize_seconds(30), "30秒")
        self.assertEqual(TimeFormatter.humanize_seconds(90), "1分钟30秒")
        self.assertEqual(TimeFormatter.humanize_seconds(3661), "1小时1分钟1秒")
        self.assertEqual(TimeFormatter.humanize_seconds(90061), "1天1小时1分钟1秒")


class TestTimeDifference(unittest.TestCase):
    """测试时区差异"""
    
    def test_get_timezone_offset(self):
        """测试时区偏移"""
        offset = TimeDifference.get_timezone_offset("Beijing")
        self.assertEqual(offset, 8.0)  # UTC+8
        
        offset = TimeDifference.get_timezone_offset("UTC")
        self.assertEqual(offset, 0.0)
    
    def test_get_time_difference(self):
        """测试城市时差"""
        diff = TimeDifference.get_time_difference("Beijing", "Tokyo")
        self.assertEqual(diff, 1.0)  # 东京比北京快1小时
    
    def test_convert_time(self):
        """测试时间转换"""
        # 北京8点 = 东京9点
        hour, minute = TimeDifference.convert_time("Beijing", "Tokyo", 8, 0)
        self.assertEqual(hour, 9)
        self.assertEqual(minute, 0)
        
        # 北京20点 = 纽约当天7点（北京UTC+8，纽约UTC-5，差13小时）
        # 20 + 13 = 33 = 7 (第二天)
        hour, minute = TimeDifference.convert_time("Beijing", "NewYork", 20, 0)
        self.assertEqual(hour, 7)


class TestCountdown(unittest.TestCase):
    """测试倒计时"""
    
    def test_create_countdown(self):
        """测试创建倒计时"""
        target = datetime.now() + timedelta(hours=1)
        cd = Countdown(target)
        self.assertFalse(cd.is_expired)
        self.assertGreater(cd.total_seconds, 0)
    
    def test_countdown_to_date(self):
        """测试从日期创建"""
        cd = Countdown.to_date(2025, 12, 25)
        self.assertEqual(cd.target.year, 2025)
        self.assertEqual(cd.target.month, 12)
        self.assertEqual(cd.target.day, 25)
    
    def test_countdown_properties(self):
        """测试倒计时属性"""
        target = datetime.now() + timedelta(days=1, hours=2, minutes=30, seconds=15)
        cd = Countdown(target)
        
        self.assertEqual(cd.days, 1)
        # 小时、分钟、秒可能会有精度问题，所以只检查大致范围
        self.assertGreaterEqual(cd.hours, 1)
        self.assertGreaterEqual(cd.minutes, 0)
    
    def test_countdown_expired(self):
        """测试过期倒计时"""
        target = datetime.now() - timedelta(seconds=1)
        cd = Countdown(target)
        self.assertTrue(cd.is_expired)
        self.assertEqual(cd.total_seconds, 0)
    
    def test_get_detailed(self):
        """测试详细倒计时"""
        target = datetime.now() + timedelta(days=1)
        cd = Countdown(target)
        detailed = cd.get_detailed()
        
        self.assertIn("days", detailed)
        self.assertIn("hours", detailed)
        self.assertIn("minutes", detailed)
        self.assertIn("seconds", detailed)
        self.assertIn("total_seconds", detailed)


class TestAlarmClock(unittest.TestCase):
    """测试闹钟"""
    
    def test_add_remove_alarm(self):
        """测试添加和删除闹钟"""
        alarm = AlarmClock()
        target = datetime.now() + timedelta(hours=1)
        
        alarm.add_alarm("test", target)
        alarms = alarm.list_alarms()
        self.assertIn("test", alarms)
        
        result = alarm.remove_alarm("test")
        self.assertTrue(result)
        self.assertNotIn("test", alarm.list_alarms())
    
    def test_add_alarm_from_time(self):
        """测试从时间添加闹钟"""
        alarm = AlarmClock()
        
        # 添加未来时间的闹钟
        future_hour = (datetime.now().hour + 1) % 24
        result = alarm.add_alarm_from_time("future", future_hour)
        self.assertTrue(result)
        
        # 添加已过期时间（today_only=True）
        past_hour = (datetime.now().hour - 1) % 24
        result = alarm.add_alarm_from_time("past", past_hour, today_only=True)
        self.assertFalse(result)
    
    def test_check_alarm(self):
        """测试检查闹钟"""
        alarm = AlarmClock()
        
        # 添加一个立即触发的闹钟
        alarm.add_alarm("now", datetime.now() - timedelta(seconds=1))
        triggered = alarm.check()
        
        self.assertIn("now", triggered)
        self.assertTrue(alarm.is_triggered("now"))
    
    def test_snooze(self):
        """测试贪睡功能"""
        alarm = AlarmClock()
        alarm.add_alarm("test", datetime.now() - timedelta(seconds=1))
        alarm.check()  # 触发闹钟
        
        result = alarm.snooze("test", minutes=5)
        self.assertTrue(result)
        self.assertFalse(alarm.is_triggered("test"))
        
        remaining = alarm.get_remaining("test")
        self.assertIsNotNone(remaining)
        self.assertLessEqual(remaining.total_seconds(), 5 * 60 + 1)
    
    def test_list_pending(self):
        """测试列出待触发闹钟"""
        alarm = AlarmClock()
        future = datetime.now() + timedelta(hours=1)
        past = datetime.now() - timedelta(seconds=1)
        
        alarm.add_alarm("future", future)
        alarm.add_alarm("past", past)
        alarm.check()  # 触发过去的闹钟
        
        pending = alarm.list_pending()
        self.assertIn("future", pending)
        self.assertNotIn("past", pending)


class TestPomodoroTimer(unittest.TestCase):
    """测试番茄钟"""
    
    def test_create_pomodoro(self):
        """测试创建番茄钟"""
        pomo = PomodoroTimer()
        self.assertEqual(pomo.session_count, 0)
        self.assertEqual(pomo.current_phase, "工作")
    
    def test_start_pomodoro(self):
        """测试开始番茄钟"""
        pomo = PomodoroTimer(work_minutes=1)
        phase, duration = pomo.start()
        
        self.assertEqual(phase, "工作")
        self.assertEqual(duration, 60)
        self.assertTrue(pomo._running)
    
    def test_pause_resume(self):
        """测试暂停继续"""
        pomo = PomodoroTimer(work_minutes=1)
        pomo.start()
        
        pomo.pause()
        self.assertFalse(pomo._running)
        
        pomo.resume()
        self.assertTrue(pomo._running)
    
    def test_phase_transition(self):
        """测试阶段转换"""
        pomo = PomodoroTimer(work_minutes=0, short_break_minutes=0)
        pomo.start()
        
        time.sleep(0.05)
        completed = pomo.check()
        
        self.assertEqual(completed, "工作")
        self.assertEqual(pomo.session_count, 1)
        self.assertEqual(pomo.current_phase, "休息")
    
    def test_reset(self):
        """测试重置"""
        pomo = PomodoroTimer()
        pomo.start()
        pomo.reset()
        
        self.assertEqual(pomo.session_count, 0)
        self.assertEqual(pomo.current_phase, "工作")
        self.assertFalse(pomo._running)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_get_world_time(self):
        """测试获取世界时间"""
        time_str = get_world_time("Beijing")
        self.assertIsInstance(time_str, str)
        # 格式应该是 YYYY-MM-DD HH:MM:SS
        self.assertRegex(time_str, r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
    
    def test_get_multiple_times(self):
        """测试获取多城市时间"""
        times = get_multiple_times(["Beijing", "Tokyo"])
        self.assertEqual(len(times), 2)
    
    def test_create_timer_func(self):
        """测试创建计时器函数"""
        timer = create_timer(10, "Test")
        self.assertIsInstance(timer, Timer)
        self.assertEqual(timer.duration, 10)
    
    def test_create_stopwatch_func(self):
        """测试创建秒表函数"""
        sw = create_stopwatch()
        self.assertIsInstance(sw, Stopwatch)
    
    def test_format_duration_func(self):
        """测试格式化时长函数"""
        result = format_duration(3661)
        self.assertEqual(result, "01:01:01")
    
    def test_create_countdown_func(self):
        """测试创建倒计时函数"""
        target = datetime.now() + timedelta(hours=1)
        cd = create_countdown(target, "Test")
        self.assertIsInstance(cd, Countdown)


if __name__ == "__main__":
    unittest.main()