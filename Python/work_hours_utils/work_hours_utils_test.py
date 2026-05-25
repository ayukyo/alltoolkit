"""
工作时长计算工具测试

测试所有核心功能：
- 日工作时长计算
- 周工作时长统计
- 加班工资计算
- 弹性工作制
- 排班调度
- 考勤分析
"""

import unittest
from datetime import datetime, time, date, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    WorkHoursCalculator,
    WorkShift,
    TimeSlot,
    PunchRecord,
    WorkDayType,
    OvertimeType,
    ShiftScheduler,
    TimeAttendanceAnalyzer,
    create_punch_record,
    STANDARD_DAY_SHIFT,
    STANDARD_NIGHT_SHIFT,
    THREE_SHIFT_MORNING,
    THREE_SHIFT_AFTERNOON,
    THREE_SHIFT_NIGHT,
)


class TestTimeSlot(unittest.TestCase):
    """测试时间段"""
    
    def test_duration_hours(self):
        """测试时长计算"""
        slot = TimeSlot(time(9, 0), time(12, 0))
        self.assertEqual(slot.duration_hours(), 3.0)
        
        slot2 = TimeSlot(time(13, 30), time(18, 0))
        self.assertEqual(slot2.duration_hours(), 4.5)
    
    def test_overlaps(self):
        """测试重叠检测"""
        slot1 = TimeSlot(time(9, 0), time(12, 0))
        slot2 = TimeSlot(time(11, 0), time(14, 0))
        slot3 = TimeSlot(time(12, 0), time(15, 0))
        
        self.assertTrue(slot1.overlaps(slot2))
        self.assertFalse(slot1.overlaps(slot3))
    
    def test_contains(self):
        """测试包含检测"""
        slot = TimeSlot(time(9, 0), time(12, 0))
        
        self.assertTrue(slot.contains(time(10, 0)))
        self.assertTrue(slot.contains(time(9, 0)))
        self.assertTrue(slot.contains(time(12, 0)))
        self.assertFalse(slot.contains(time(8, 0)))
        self.assertFalse(slot.contains(time(13, 0)))


class TestWorkShift(unittest.TestCase):
    """测试工作班次"""
    
    def test_total_work_hours(self):
        """测试总工作时长"""
        shift = WorkShift(
            name="测试班次",
            work_periods=[
                TimeSlot(time(9, 0), time(12, 0)),
                TimeSlot(time(13, 0), time(18, 0)),
            ]
        )
        self.assertEqual(shift.total_work_hours(), 8.0)
    
    def test_standard_day_shift(self):
        """测试标准白班"""
        self.assertEqual(STANDARD_DAY_SHIFT.total_work_hours(), 8.0)
        self.assertFalse(STANDARD_DAY_SHIFT.is_night_shift)
    
    def test_standard_night_shift(self):
        """测试标准夜班"""
        hours = STANDARD_NIGHT_SHIFT.total_work_hours()
        # 夜班跨天，计算为正数
        self.assertEqual(hours, 8.0)
        self.assertTrue(STANDARD_NIGHT_SHIFT.is_night_shift)


class TestPunchRecord(unittest.TestCase):
    """测试打卡记录"""
    
    def test_work_hours_simple(self):
        """测试简单工作时长"""
        record = PunchRecord(
            date=date(2024, 1, 8),
            check_in=time(9, 0),
            check_out=time(17, 0)
        )
        self.assertEqual(record.work_hours(), 8.0)
    
    def test_work_hours_with_break(self):
        """测试带休息的工作时长"""
        record = PunchRecord(
            date=date(2024, 1, 8),
            check_in=time(9, 0),
            check_out=time(18, 0)
        )
        break_periods = [
            TimeSlot(time(12, 0), time(13, 0))
        ]
        self.assertEqual(record.work_hours(break_periods), 8.0)
    
    def test_work_hours_no_punch(self):
        """测试无打卡情况"""
        record = PunchRecord(
            date=date(2024, 1, 8),
            check_in=None,
            check_out=None
        )
        self.assertEqual(record.work_hours(), 0.0)


class TestWorkHoursCalculator(unittest.TestCase):
    """测试工作时长计算器"""
    
    def setUp(self):
        """初始化测试"""
        self.calculator = WorkHoursCalculator(
            break_periods=[(time(12, 0), time(13, 0))]
        )
    
    def test_calculate_daily_hours_normal(self):
        """测试正常日工作时长"""
        result = self.calculator.calculate_daily_hours(
            check_in=time(9, 0),
            check_out=time(18, 0)
        )
        
        self.assertEqual(result["total_hours"], 9.0)
        self.assertEqual(result["break_hours"], 1.0)
        self.assertEqual(result["actual_work_hours"], 8.0)
        self.assertEqual(result["overtime_hours"], 0.0)
    
    def test_calculate_daily_hours_overtime(self):
        """测试加班情况"""
        result = self.calculator.calculate_daily_hours(
            check_in=time(9, 0),
            check_out=time(21, 0)
        )
        
        self.assertEqual(result["total_hours"], 12.0)
        self.assertEqual(result["break_hours"], 1.0)
        self.assertEqual(result["actual_work_hours"], 11.0)
        self.assertEqual(result["overtime_hours"], 3.0)
    
    def test_calculate_daily_hours_partial_break(self):
        """测试部分休息时间"""
        # 只工作到中午12点，没有休息
        result = self.calculator.calculate_daily_hours(
            check_in=time(9, 0),
            check_out=time(12, 0)
        )
        
        self.assertEqual(result["total_hours"], 3.0)
        self.assertEqual(result["break_hours"], 0.0)
        self.assertEqual(result["actual_work_hours"], 3.0)
    
    def test_calculate_night_hours(self):
        """测试夜班时长计算"""
        result = self.calculator.calculate_daily_hours(
            check_in=time(22, 0),
            check_out=time(6, 0)
        )
        
        # 跨天工作，总共8小时
        self.assertEqual(result["total_hours"], 8.0)
        # 夜班时长应该是8小时
        self.assertEqual(result["night_hours"], 8.0)
    
    def test_calculate_weekly_hours(self):
        """测试周工作时长"""
        records = [
            create_punch_record("2024-01-08", "09:00", "18:00"),
            create_punch_record("2024-01-09", "09:00", "18:00"),
            create_punch_record("2024-01-10", "09:00", "18:00"),
            create_punch_record("2024-01-11", "09:00", "18:00"),
            create_punch_record("2024-01-12", "09:00", "18:00"),
        ]
        
        result = self.calculator.calculate_weekly_hours(records)
        
        self.assertEqual(result["total_work_hours"], 40.0)
        self.assertEqual(result["work_days"], 5)
        self.assertEqual(result["average_daily_hours"], 8.0)
    
    def test_calculate_weekly_hours_with_overtime(self):
        """测试带加班的周工作时长"""
        records = [
            create_punch_record("2024-01-08", "09:00", "18:00"),
            create_punch_record("2024-01-09", "09:00", "20:00"),  # 加班2小时
            create_punch_record("2024-01-10", "09:00", "18:00"),
            create_punch_record("2024-01-11", "09:00", "18:00"),
            create_punch_record("2024-01-12", "09:00", "18:00"),
        ]
        
        result = self.calculator.calculate_weekly_hours(records)
        
        self.assertEqual(result["total_work_hours"], 42.0)
        self.assertEqual(result["total_overtime_hours"], 2.0)
        self.assertEqual(len(result["overtime_records"]), 1)
    
    def test_check_weekly_compliance(self):
        """测试周工时合规检查"""
        # 合规情况
        result = self.calculator.check_weekly_compliance(40.0)
        self.assertTrue(result["is_compliant"])
        self.assertEqual(len(result["warnings"]), 0)
        
        # 超标情况
        result = self.calculator.check_weekly_compliance(50.0)
        self.assertFalse(result["is_compliant"])
        self.assertTrue(len(result["warnings"]) > 0)
    
    def test_calculate_flexible_hours(self):
        """测试弹性工作时长"""
        flex_calculator = WorkHoursCalculator(
            flexible_hours=True,
            core_hours=(time(10, 0), time(16, 0)),
            break_periods=[(time(12, 0), time(13, 0))]
        )
        
        result = flex_calculator.calculate_flexible_hours(
            check_in=time(8, 0),
            check_out=time(17, 0)
        )
        
        self.assertEqual(result["actual_work_hours"], 8.0)
        self.assertEqual(result["hours_difference"], 0.0)
    
    def test_calculate_overtime_pay(self):
        """测试加班工资计算"""
        overtime_records = [
            PunchRecord(
                date=date(2024, 1, 9),
                check_in=time(9, 0),
                check_out=time(20, 0),
                day_type=WorkDayType.WEEKDAY
            ),
            PunchRecord(
                date=date(2024, 1, 13),  # 周末
                check_in=time(9, 0),
                check_out=time(18, 0),
                day_type=WorkDayType.WEEKEND
            ),
        ]
        
        result = self.calculator.calculate_weekly_hours(overtime_records)
        overtime_pay = self.calculator.calculate_overtime_pay(
            result["overtime_records"],
            hourly_rate=100.0
        )
        
        # 应该计算加班工资
        self.assertTrue(overtime_pay["total_overtime_pay"] > 0)


class TestShiftScheduler(unittest.TestCase):
    """测试排班调度器"""
    
    def setUp(self):
        """初始化测试"""
        self.scheduler = ShiftScheduler([
            THREE_SHIFT_MORNING,
            THREE_SHIFT_AFTERNOON,
            THREE_SHIFT_NIGHT,
        ])
    
    def test_assign_shift(self):
        """测试分配班次"""
        result = self.scheduler.assign_shift(
            employee_id="EMP001",
            date=date(2024, 1, 8),
            shift_name="早班"
        )
        
        self.assertEqual(result["employee_id"], "EMP001")
        self.assertEqual(result["shift"]["name"], "早班")
        self.assertEqual(result["shift"]["total_hours"], 8.0)
        self.assertFalse(result["shift"]["is_night_shift"])
    
    def test_assign_shift_invalid(self):
        """测试无效班次"""
        result = self.scheduler.assign_shift(
            employee_id="EMP001",
            date=date(2024, 1, 8),
            shift_name="无效班次"
        )
        
        self.assertIn("error", result)
    
    def test_generate_weekly_schedule(self):
        """测试生成周排班表"""
        schedule = self.scheduler.generate_weekly_schedule(
            employee_id="EMP001",
            start_date=date(2024, 1, 8),
            shift_pattern=["早班", "中班", "晚班", "早班", "中班", "off", "off"]
        )
        
        self.assertEqual(len(schedule), 7)
        self.assertEqual(schedule[0]["shift"]["name"], "早班")
        self.assertEqual(schedule[5]["is_rest_day"], True)
        self.assertEqual(schedule[6]["is_rest_day"], True)
    
    def test_calculate_shift_statistics(self):
        """测试排班统计"""
        schedule = self.scheduler.generate_weekly_schedule(
            employee_id="EMP001",
            start_date=date(2024, 1, 8),
            shift_pattern=["早班", "中班", "晚班", "早班", "中班", "off", "off"]
        )
        
        stats = self.scheduler.calculate_shift_statistics(schedule)
        
        self.assertEqual(stats["work_days"], 5)
        self.assertEqual(stats["rest_days"], 2)
        self.assertEqual(stats["night_shifts"], 1)
        self.assertEqual(stats["total_work_hours"], 40.0)


class TestTimeAttendanceAnalyzer(unittest.TestCase):
    """测试考勤分析器"""
    
    def setUp(self):
        """初始化测试"""
        self.analyzer = TimeAttendanceAnalyzer(
            standard_start=time(9, 0),
            standard_end=time(18, 0),
            grace_minutes=15,
            late_threshold_minutes=30,
        )
    
    def test_analyze_normal_record(self):
        """测试正常打卡记录"""
        record = create_punch_record("2024-01-08", "09:00", "18:00")
        result = self.analyzer.analyze_punch_record(record)
        
        self.assertEqual(result["status"], "normal")
        self.assertEqual(result["late_minutes"], 0)
        self.assertFalse(result["is_late"])
    
    def test_analyze_late_record(self):
        """测试迟到记录"""
        record = create_punch_record("2024-01-08", "09:20", "18:00")
        result = self.analyzer.analyze_punch_record(record)
        
        self.assertEqual(result["status"], "late")
        self.assertEqual(result["late_minutes"], 20)
        self.assertTrue(result["is_late"])
    
    def test_analyze_seriously_late_record(self):
        """测试严重迟到记录"""
        record = create_punch_record("2024-01-08", "09:35", "18:00")
        result = self.analyzer.analyze_punch_record(record)
        
        self.assertEqual(result["status"], "seriously_late")
        self.assertEqual(result["late_minutes"], 35)
    
    def test_analyze_grace_period(self):
        """测试宽限时间"""
        record = create_punch_record("2024-01-08", "09:10", "18:00")
        result = self.analyzer.analyze_punch_record(record)
        
        self.assertEqual(result["status"], "normal")
        self.assertEqual(result["late_minutes"], 0)
    
    def test_analyze_early_leave(self):
        """测试早退记录"""
        record = create_punch_record("2024-01-08", "09:00", "17:30")
        result = self.analyzer.analyze_punch_record(record)
        
        self.assertEqual(result["status"], "early_leave")
        self.assertTrue(result["is_early_leave"])
        self.assertEqual(result["early_leave_minutes"], 30)
    
    def test_analyze_absent(self):
        """测试缺勤"""
        record = create_punch_record("2024-01-08", None, None)
        result = self.analyzer.analyze_punch_record(record)
        
        self.assertEqual(result["status"], "absent")
    
    def test_analyze_missing_checkout(self):
        """测试缺卡"""
        record = create_punch_record("2024-01-08", "09:00", None)
        result = self.analyzer.analyze_punch_record(record)
        
        self.assertEqual(result["status"], "missing_checkout")
    
    def test_analyze_weekend(self):
        """测试周末"""
        record = create_punch_record("2024-01-13", "09:00", "18:00", "weekend")
        result = self.analyzer.analyze_punch_record(record)
        
        self.assertFalse(result["is_work_day"])
    
    def test_analyze_period(self):
        """测试期间分析"""
        records = [
            create_punch_record("2024-01-08", "09:00", "18:00"),  # 正常
            create_punch_record("2024-01-09", "09:20", "18:00"),  # 迟到
            create_punch_record("2024-01-10", "09:00", "17:30"),  # 早退
            create_punch_record("2024-01-11", None, None),        # 缺勤
            create_punch_record("2024-01-12", "09:00", None),     # 缺卡
        ]
        
        result = self.analyzer.analyze_period(records)
        
        self.assertEqual(result["summary"]["total_days"], 5)
        self.assertEqual(result["summary"]["work_days"], 5)
        self.assertEqual(result["summary"]["normal_days"], 1)
        self.assertEqual(result["summary"]["late_days"], 1)
        self.assertEqual(result["summary"]["early_leave_days"], 1)
        self.assertEqual(result["summary"]["absent_days"], 1)
        self.assertEqual(result["summary"]["missing_checkout_days"], 1)
        
        # 出勤率 = (正常+迟到+早退)/工作日 = 3/5 = 60%
        self.assertEqual(result["summary"]["attendance_rate"], 60.0)
        # 准时率 = 正常/工作日 = 1/5 = 20%
        self.assertEqual(result["summary"]["punctuality_rate"], 20.0)


class TestCreatePunchRecord(unittest.TestCase):
    """测试快捷创建打卡记录"""
    
    def test_create_punch_record_full(self):
        """测试完整创建"""
        record = create_punch_record(
            "2024-01-08",
            "09:00",
            "18:00",
            "weekday"
        )
        
        self.assertEqual(record.date, date(2024, 1, 8))
        self.assertEqual(record.check_in, time(9, 0))
        self.assertEqual(record.check_out, time(18, 0))
        self.assertEqual(record.day_type, WorkDayType.WEEKDAY)
    
    def test_create_punch_record_partial(self):
        """测试部分创建"""
        record = create_punch_record("2024-01-08")
        
        self.assertEqual(record.date, date(2024, 1, 8))
        self.assertIsNone(record.check_in)
        self.assertIsNone(record.check_out)
    
    def test_create_punch_record_weekend(self):
        """测试周末创建"""
        record = create_punch_record(
            "2024-01-13",
            "09:00",
            "18:00",
            "weekend"
        )
        
        self.assertEqual(record.day_type, WorkDayType.WEEKEND)


if __name__ == "__main__":
    unittest.main(verbosity=2)