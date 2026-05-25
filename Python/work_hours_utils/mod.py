"""
工作时长计算工具模块

提供工作时间相关的计算功能：
- 工作时长计算（考虑午休时间）
- 加班时间计算
- 周工作时间统计
- 弹性工作时间计算
- 打卡记录分析
- 工时合规检查

零外部依赖，纯 Python 标准库实现。
"""

from datetime import datetime, time, timedelta, date
from typing import List, Dict, Tuple, Optional, NamedTuple
from enum import Enum
from dataclasses import dataclass
import math


class WorkDayType(Enum):
    """工作日类型"""
    WEEKDAY = "weekday"      # 普通工作日
    WEEKEND = "weekend"      # 周末
    HOLIDAY = "holiday"      # 法定节假日
    REST_DAY = "rest_day"   # 休息日（如调休）


class OvertimeType(Enum):
    """加班类型"""
    WEEKDAY_OVERTIME = "weekday_overtime"       # 工作日加班
    WEEKEND_OVERTIME = "weekend_overtime"       # 周末加班
    HOLIDAY_OVERTIME = "holiday_overtime"       # 法定节假日加班
    NIGHT_OVERTIME = "night_overtime"           # 夜班加班


@dataclass
class TimeSlot:
    """时间段"""
    start: time
    end: time
    
    def duration_hours(self) -> float:
        """计算时长（小时），支持跨天时间段"""
        start_minutes = self.start.hour * 60 + self.start.minute
        end_minutes = self.end.hour * 60 + self.end.minute
        
        # 处理跨天情况（如夜班 22:00 - 06:00）
        if end_minutes <= start_minutes:
            end_minutes += 24 * 60
        
        return (end_minutes - start_minutes) / 60
    
    def overlaps(self, other: 'TimeSlot') -> bool:
        """检查是否与另一个时间段重叠"""
        return (self.start < other.end and self.end > other.start)
    
    def contains(self, t: time) -> bool:
        """检查是否包含某个时间点"""
        return self.start <= t <= self.end


@dataclass
class WorkShift:
    """工作班次"""
    name: str
    work_periods: List[TimeSlot]
    is_night_shift: bool = False
    
    def total_work_hours(self) -> float:
        """计算总工作时长"""
        return sum(slot.duration_hours() for slot in self.work_periods)


@dataclass
class PunchRecord:
    """打卡记录"""
    date: date
    check_in: Optional[time] = None
    check_out: Optional[time] = None
    day_type: WorkDayType = WorkDayType.WEEKDAY
    
    def work_hours(self, break_periods: List[TimeSlot] = None) -> float:
        """计算工作时长"""
        if not self.check_in or not self.check_out:
            return 0.0
        
        start_minutes = self.check_in.hour * 60 + self.check_in.minute
        end_minutes = self.check_out.hour * 60 + self.check_out.minute
        
        total_minutes = end_minutes - start_minutes
        
        # 扣除休息时间
        if break_periods:
            for break_slot in break_periods:
                if self.check_in <= break_slot.start and self.check_out >= break_slot.end:
                    break_minutes = (break_slot.end.hour * 60 + break_slot.end.minute - 
                                   break_slot.start.hour * 60 - break_slot.start.minute)
                    total_minutes -= break_minutes
        
        return max(0, total_minutes / 60)


@dataclass
class OvertimeRecord:
    """加班记录"""
    date: date
    overtime_type: OvertimeType
    hours: float
    rate: float = 1.0  # 加班倍率


class WorkHoursCalculator:
    """工作时长计算器"""
    
    # 中国劳动法规定的标准工时
    STANDARD_DAILY_HOURS = 8.0
    STANDARD_WEEKLY_HOURS = 40.0
    STANDARD_WORK_DAYS = 5
    
    # 加班倍率（中国劳动法规定）
    OVERTIME_RATES = {
        OvertimeType.WEEKDAY_OVERTIME: 1.5,   # 工作日加班 1.5 倍
        OvertimeType.WEEKEND_OVERTIME: 2.0,    # 周末加班 2 倍（可调休）
        OvertimeType.HOLIDAY_OVERTIME: 3.0,    # 法定节假日加班 3 倍
        OvertimeType.NIGHT_OVERTIME: 2.0,      # 夜班加班
    }
    
    def __init__(
        self,
        standard_work_hours: float = 8.0,
        standard_weekly_hours: float = 40.0,
        break_periods: List[Tuple[time, time]] = None,
        night_shift_start: time = time(22, 0),
        night_shift_end: time = time(6, 0),
        flexible_hours: bool = False,
        core_hours: Tuple[time, time] = None,
    ):
        """
        初始化工作时长计算器
        
        Args:
            standard_work_hours: 标准日工作时长
            standard_weekly_hours: 标准周工作时长
            break_periods: 休息时间段列表 [(开始时间, 结束时间), ...]
            night_shift_start: 夜班开始时间
            night_shift_end: 夜班结束时间
            flexible_hours: 是否启用弹性工作时间
            core_hours: 核心工作时间（弹性工作制下必须在岗的时间）
        """
        self.standard_work_hours = standard_work_hours
        self.standard_weekly_hours = standard_weekly_hours
        self.break_periods = [
            TimeSlot(start, end) for start, end in (break_periods or [])
        ]
        self.night_shift_start = night_shift_start
        self.night_shift_end = night_shift_end
        self.flexible_hours = flexible_hours
        self.core_hours = TimeSlot(*core_hours) if core_hours else None
    
    def calculate_daily_hours(
        self,
        check_in: time,
        check_out: time,
        break_periods: List[Tuple[time, time]] = None
    ) -> Dict[str, float]:
        """
        计算日工作时长
        
        Args:
            check_in: 上班打卡时间
            check_out: 下班打卡时间
            break_periods: 额外休息时间（将合并到默认休息时间）
        
        Returns:
            包含各种时长信息的字典
        """
        check_in_minutes = check_in.hour * 60 + check_in.minute
        check_out_minutes = check_out.hour * 60 + check_out.minute
        
        # 处理跨天情况（如夜班）
        if check_out_minutes < check_in_minutes:
            check_out_minutes += 24 * 60
        
        total_minutes = check_out_minutes - check_in_minutes
        total_hours = total_minutes / 60
        
        # 计算休息时间
        all_breaks = list(self.break_periods)
        if break_periods:
            all_breaks.extend([TimeSlot(s, e) for s, e in break_periods])
        
        break_minutes = 0
        for break_slot in all_breaks:
            break_start_minutes = break_slot.start.hour * 60 + break_slot.start.minute
            break_end_minutes = break_slot.end.hour * 60 + break_slot.end.minute
            
            # 检查休息时间是否在工作时间范围内
            if check_in_minutes <= break_start_minutes and check_out_minutes >= break_end_minutes:
                break_minutes += break_end_minutes - break_start_minutes
        
        actual_work_hours = (total_minutes - break_minutes) / 60
        
        # 计算加班时长
        overtime_hours = max(0, actual_work_hours - self.standard_work_hours)
        
        # 计算夜班时长
        night_hours = self._calculate_night_hours(check_in, check_out)
        
        return {
            "total_hours": round(total_hours, 2),
            "break_hours": round(break_minutes / 60, 2),
            "actual_work_hours": round(actual_work_hours, 2),
            "overtime_hours": round(overtime_hours, 2),
            "night_hours": round(night_hours, 2),
            "standard_hours": self.standard_work_hours,
        }
    
    def _calculate_night_hours(self, check_in: time, check_out: time) -> float:
        """计算夜班时长"""
        check_in_minutes = check_in.hour * 60 + check_in.minute
        check_out_minutes = check_out.hour * 60 + check_out.minute
        
        night_start_minutes = self.night_shift_start.hour * 60 + self.night_shift_start.minute
        night_end_minutes = self.night_shift_end.hour * 60 + self.night_shift_end.minute
        
        night_minutes = 0
        
        # 计算夜班时段 1：22:00 - 24:00
        if check_out_minutes > check_in_minutes:
            # 正常情况（不跨天）
            if check_in_minutes < night_start_minutes and check_out_minutes > night_start_minutes:
                night_minutes += min(check_out_minutes, 24 * 60) - night_start_minutes
            elif check_in_minutes >= night_start_minutes:
                night_minutes += check_out_minutes - check_in_minutes
        else:
            # 跨天情况
            # 当天夜班时段
            if check_in_minutes < night_start_minutes:
                night_minutes += 24 * 60 - max(check_in_minutes, night_start_minutes)
            else:
                night_minutes += 24 * 60 - check_in_minutes
            # 次日夜班时段
            night_minutes += min(check_out_minutes, night_end_minutes)
        
        return max(0, night_minutes / 60)
    
    def calculate_weekly_hours(
        self,
        records: List[PunchRecord]
    ) -> Dict[str, any]:
        """
        计算周工作时长统计
        
        Args:
            records: 打卡记录列表
        
        Returns:
            周工作统计信息
        """
        total_work_hours = 0.0
        total_overtime_hours = 0.0
        total_night_hours = 0.0
        work_days = 0
        overtime_records: List[OvertimeRecord] = []
        
        for record in records:
            hours = record.work_hours(self.break_periods)
            total_work_hours += hours
            
            # 计算加班
            if hours > self.standard_work_hours:
                overtime = hours - self.standard_work_hours
                total_overtime_hours += overtime
                
                # 确定加班类型
                if record.day_type == WorkDayType.HOLIDAY:
                    overtime_type = OvertimeType.HOLIDAY_OVERTIME
                elif record.day_type == WorkDayType.WEEKEND:
                    overtime_type = OvertimeType.WEEKEND_OVERTIME
                else:
                    overtime_type = OvertimeType.WEEKDAY_OVERTIME
                
                overtime_records.append(OvertimeRecord(
                    date=record.date,
                    overtime_type=overtime_type,
                    hours=overtime,
                    rate=self.OVERTIME_RATES[overtime_type]
                ))
            
            if record.check_in and record.check_out:
                night_hours = self._calculate_night_hours(
                    record.check_in, record.check_out
                )
                total_night_hours += night_hours
                work_days += 1
        
        # 检查周工时合规性
        compliance = self.check_weekly_compliance(total_work_hours)
        
        return {
            "total_work_hours": round(total_work_hours, 2),
            "total_overtime_hours": round(total_overtime_hours, 2),
            "total_night_hours": round(total_night_hours, 2),
            "work_days": work_days,
            "average_daily_hours": round(total_work_hours / work_days, 2) if work_days > 0 else 0,
            "standard_weekly_hours": self.standard_weekly_hours,
            "overtime_records": overtime_records,
            "compliance": compliance,
        }
    
    def check_weekly_compliance(self, weekly_hours: float) -> Dict[str, any]:
        """
        检查周工时合规性
        
        Args:
            weekly_hours: 周总工作时长
        
        Returns:
            合规性检查结果
        """
        max_weekly_hours = 44.0  # 中国劳动法规定，每周最长44小时（含加班）
        max_overtime_hours = 36.0  # 每月加班上限
        
        overtime = max(0, weekly_hours - self.standard_weekly_hours)
        is_compliant = weekly_hours <= max_weekly_hours
        
        return {
            "is_compliant": is_compliant,
            "weekly_hours": round(weekly_hours, 2),
            "standard_hours": self.standard_weekly_hours,
            "overtime_hours": round(overtime, 2),
            "max_allowed_hours": max_weekly_hours,
            "exceeded_hours": round(max(0, weekly_hours - max_weekly_hours), 2),
            "warnings": self._generate_compliance_warnings(weekly_hours),
        }
    
    def _generate_compliance_warnings(self, weekly_hours: float) -> List[str]:
        """生成合规性警告"""
        warnings = []
        
        if weekly_hours > 44:
            warnings.append("⚠️ 周工作时长超过法定上限44小时")
        if weekly_hours > 48:
            warnings.append("⚠️ 周工作时长严重超标，建议调整")
        if weekly_hours > self.standard_weekly_hours + 10:
            warnings.append("⚠️ 本周加班时间过长，注意休息")
        
        return warnings
    
    def calculate_flexible_hours(
        self,
        check_in: time,
        check_out: time,
        core_hours_violation: bool = False
    ) -> Dict[str, any]:
        """
        计算弹性工作时长
        
        Args:
            check_in: 上班打卡时间
            check_out: 下班打卡时间
            core_hours_violation: 是否违反核心工作时间
        
        Returns:
            弹性工作时长计算结果
        """
        if not self.flexible_hours:
            return {"error": "未启用弹性工作制"}
        
        check_in_minutes = check_in.hour * 60 + check_in.minute
        check_out_minutes = check_out.hour * 60 + check_out.minute
        
        total_minutes = check_out_minutes - check_in_minutes
        
        # 扣除休息时间
        break_minutes = 0
        for break_slot in self.break_periods:
            break_minutes += (break_slot.end.hour * 60 + break_slot.end.minute - 
                            break_slot.start.hour * 60 - break_slot.start.minute)
        
        actual_minutes = total_minutes - break_minutes
        actual_hours = actual_minutes / 60
        
        # 计算与标准工时的差异
        hours_difference = actual_hours - self.standard_work_hours
        
        # 计算弹性额度
        flex_credit = hours_difference  # 正数表示加班，负数表示欠时
        
        result = {
            "actual_work_hours": round(actual_hours, 2),
            "standard_hours": self.standard_work_hours,
            "hours_difference": round(hours_difference, 2),
            "flex_credit": round(flex_credit, 2),
            "is_overtime": hours_difference > 0,
            "is_under_time": hours_difference < 0,
        }
        
        if self.core_hours:
            result["core_hours"] = {
                "start": self.core_hours.start.strftime("%H:%M"),
                "end": self.core_hours.end.strftime("%H:%M"),
                "violation": core_hours_violation,
            }
        
        return result
    
    def calculate_overtime_pay(
        self,
        overtime_records: List[OvertimeRecord],
        hourly_rate: float
    ) -> Dict[str, any]:
        """
        计算加班工资
        
        Args:
            overtime_records: 加班记录列表
            hourly_rate: 小时工资率
        
        Returns:
            加班工资计算结果
        """
        total_overtime_pay = 0.0
        breakdown = []
        
        for record in overtime_records:
            pay = record.hours * hourly_rate * record.rate
            total_overtime_pay += pay
            
            breakdown.append({
                "date": record.date.strftime("%Y-%m-%d"),
                "type": record.overtime_type.value,
                "hours": round(record.hours, 2),
                "rate": f"{record.rate}x",
                "pay": round(pay, 2),
            })
        
        return {
            "total_overtime_pay": round(total_overtime_pay, 2),
            "hourly_rate": hourly_rate,
            "total_overtime_hours": round(sum(r.hours for r in overtime_records), 2),
            "breakdown": breakdown,
        }


class ShiftScheduler:
    """排班调度器"""
    
    def __init__(self, shifts: List[WorkShift]):
        """
        初始化排班调度器
        
        Args:
            shifts: 可用班次列表
        """
        self.shifts = {shift.name: shift for shift in shifts}
    
    def assign_shift(
        self,
        employee_id: str,
        date: date,
        shift_name: str
    ) -> Dict[str, any]:
        """
        分配班次
        
        Args:
            employee_id: 员工ID
            date: 日期
            shift_name: 班次名称
        
        Returns:
            分配结果
        """
        if shift_name not in self.shifts:
            return {"error": f"未找到班次: {shift_name}"}
        
        shift = self.shifts[shift_name]
        
        return {
            "employee_id": employee_id,
            "date": date.strftime("%Y-%m-%d"),
            "shift": {
                "name": shift.name,
                "work_periods": [
                    {"start": p.start.strftime("%H:%M"), "end": p.end.strftime("%H:%M")}
                    for p in shift.work_periods
                ],
                "total_hours": round(shift.total_work_hours(), 2),
                "is_night_shift": shift.is_night_shift,
            },
        }
    
    def generate_weekly_schedule(
        self,
        employee_id: str,
        start_date: date,
        shift_pattern: List[str]
    ) -> List[Dict[str, any]]:
        """
        生成周排班表
        
        Args:
            employee_id: 员工ID
            start_date: 开始日期
            shift_pattern: 班次模式（7天的班次列表）
        
        Returns:
            周排班表
        """
        schedule = []
        
        for i, shift_name in enumerate(shift_pattern[:7]):
            current_date = start_date + timedelta(days=i)
            
            if shift_name.lower() in ["off", "rest", "休息"]:
                schedule.append({
                    "employee_id": employee_id,
                    "date": current_date.strftime("%Y-%m-%d"),
                    "day_of_week": current_date.strftime("%A"),
                    "shift": None,
                    "is_rest_day": True,
                })
            else:
                assignment = self.assign_shift(employee_id, current_date, shift_name)
                assignment["day_of_week"] = current_date.strftime("%A")
                assignment["is_rest_day"] = False
                schedule.append(assignment)
        
        return schedule
    
    def calculate_shift_statistics(
        self,
        schedule: List[Dict[str, any]]
    ) -> Dict[str, any]:
        """
        计算排班统计
        
        Args:
            schedule: 排班表
        
        Returns:
            排班统计信息
        """
        total_hours = 0.0
        night_shifts = 0
        work_days = 0
        rest_days = 0
        
        for day in schedule:
            if day.get("is_rest_day"):
                rest_days += 1
            else:
                work_days += 1
                if day.get("shift"):
                    total_hours += day["shift"]["total_hours"]
                    if day["shift"].get("is_night_shift"):
                        night_shifts += 1
        
        return {
            "total_work_hours": round(total_hours, 2),
            "work_days": work_days,
            "rest_days": rest_days,
            "night_shifts": night_shifts,
            "average_daily_hours": round(total_hours / work_days, 2) if work_days > 0 else 0,
        }


class TimeAttendanceAnalyzer:
    """考勤分析器"""
    
    def __init__(
        self,
        standard_start: time = time(9, 0),
        standard_end: time = time(18, 0),
        grace_minutes: int = 15,
        late_threshold_minutes: int = 30,
    ):
        """
        初始化考勤分析器
        
        Args:
            standard_start: 标准上班时间
            standard_end: 标准下班时间
            grace_minutes: 宽限时间（分钟）
            late_threshold_minutes: 迟到判定阈值（分钟）
        """
        self.standard_start = standard_start
        self.standard_end = standard_end
        self.grace_minutes = grace_minutes
        self.late_threshold_minutes = late_threshold_minutes
    
    def analyze_punch_record(
        self,
        record: PunchRecord
    ) -> Dict[str, any]:
        """
        分析单条打卡记录
        
        Args:
            record: 打卡记录
        
        Returns:
            分析结果
        """
        result = {
            "date": record.date.strftime("%Y-%m-%d"),
            "day_type": record.day_type.value,
            "check_in": record.check_in.strftime("%H:%M") if record.check_in else None,
            "check_out": record.check_out.strftime("%H:%M") if record.check_out else None,
        }
        
        # 如果是休息日或节假日，不做考勤分析
        if record.day_type in [WorkDayType.WEEKEND, WorkDayType.HOLIDAY, WorkDayType.REST_DAY]:
            result["is_work_day"] = False
            return result
        
        result["is_work_day"] = True
        
        # 检查打卡状态
        if not record.check_in:
            result["status"] = "absent"
            result["status_text"] = "缺勤"
            result["late_minutes"] = 0
            result["early_leave_minutes"] = 0
            return result
        
        # 计算迟到
        check_in_minutes = record.check_in.hour * 60 + record.check_in.minute
        standard_start_minutes = self.standard_start.hour * 60 + self.standard_start.minute
        
        late_minutes = max(0, check_in_minutes - standard_start_minutes)
        
        if late_minutes <= self.grace_minutes:
            late_minutes = 0
        
        result["late_minutes"] = late_minutes
        result["is_late"] = late_minutes > 0
        
        if late_minutes > self.late_threshold_minutes:
            result["status"] = "seriously_late"
            result["status_text"] = "严重迟到"
        elif late_minutes > 0:
            result["status"] = "late"
            result["status_text"] = "迟到"
        else:
            result["status"] = "normal"
            result["status_text"] = "正常"
        
        # 计算早退
        if record.check_out:
            check_out_minutes = record.check_out.hour * 60 + record.check_out.minute
            standard_end_minutes = self.standard_end.hour * 60 + self.standard_end.minute
            
            early_leave_minutes = max(0, standard_end_minutes - check_out_minutes)
            
            if early_leave_minutes > self.grace_minutes:
                result["early_leave_minutes"] = early_leave_minutes
                result["is_early_leave"] = True
                if result["status"] == "normal":
                    result["status"] = "early_leave"
                    result["status_text"] = "早退"
            else:
                result["early_leave_minutes"] = 0
                result["is_early_leave"] = False
        else:
            result["early_leave_minutes"] = 0
            result["is_early_leave"] = False
            if result["status"] == "normal":
                result["status"] = "missing_checkout"
                result["status_text"] = "缺卡"
        
        return result
    
    def analyze_period(
        self,
        records: List[PunchRecord]
    ) -> Dict[str, any]:
        """
        分析一段时间内的考勤情况
        
        Args:
            records: 打卡记录列表
        
        Returns:
            考勤统计报告
        """
        total_days = len(records)
        work_days = 0
        normal_days = 0
        late_days = 0
        early_leave_days = 0
        absent_days = 0
        missing_checkout_days = 0
        total_late_minutes = 0
        total_early_leave_minutes = 0
        
        details = []
        
        for record in records:
            analysis = self.analyze_punch_record(record)
            details.append(analysis)
            
            if analysis.get("is_work_day"):
                work_days += 1
                
                if analysis["status"] == "normal":
                    normal_days += 1
                elif analysis["status"] == "late":
                    late_days += 1
                    total_late_minutes += analysis["late_minutes"]
                elif analysis["status"] == "seriously_late":
                    late_days += 1
                    total_late_minutes += analysis["late_minutes"]
                elif analysis["status"] == "early_leave":
                    early_leave_days += 1
                    total_early_leave_minutes += analysis["early_leave_minutes"]
                elif analysis["status"] == "absent":
                    absent_days += 1
                elif analysis["status"] == "missing_checkout":
                    missing_checkout_days += 1
        
        attendance_rate = (normal_days + late_days + early_leave_days) / work_days * 100 if work_days > 0 else 0
        punctuality_rate = normal_days / work_days * 100 if work_days > 0 else 0
        
        return {
            "summary": {
                "total_days": total_days,
                "work_days": work_days,
                "normal_days": normal_days,
                "late_days": late_days,
                "early_leave_days": early_leave_days,
                "absent_days": absent_days,
                "missing_checkout_days": missing_checkout_days,
                "total_late_minutes": total_late_minutes,
                "total_early_leave_minutes": total_early_leave_minutes,
                "attendance_rate": round(attendance_rate, 2),
                "punctuality_rate": round(punctuality_rate, 2),
            },
            "details": details,
        }


# 预定义班次
STANDARD_DAY_SHIFT = WorkShift(
    name="标准白班",
    work_periods=[
        TimeSlot(time(9, 0), time(12, 0)),
        TimeSlot(time(13, 0), time(18, 0)),
    ],
    is_night_shift=False,
)

STANDARD_NIGHT_SHIFT = WorkShift(
    name="标准夜班",
    work_periods=[
        TimeSlot(time(22, 0), time(6, 0)),
    ],
    is_night_shift=True,
)

THREE_SHIFT_MORNING = WorkShift(
    name="早班",
    work_periods=[
        TimeSlot(time(6, 0), time(14, 0)),
    ],
    is_night_shift=False,
)

THREE_SHIFT_AFTERNOON = WorkShift(
    name="中班",
    work_periods=[
        TimeSlot(time(14, 0), time(22, 0)),
    ],
    is_night_shift=False,
)

THREE_SHIFT_NIGHT = WorkShift(
    name="晚班",
    work_periods=[
        TimeSlot(time(22, 0), time(6, 0)),
    ],
    is_night_shift=True,
)

# 默认休息时间
DEFAULT_BREAK_PERIODS = [
    (time(12, 0), time(13, 0)),   # 午休
    (time(18, 0), time(18, 30)),   # 晚休
]


def create_punch_record(
    date_str: str,
    check_in: str = None,
    check_out: str = None,
    day_type: str = "weekday"
) -> PunchRecord:
    """
    快捷创建打卡记录
    
    Args:
        date_str: 日期字符串 (YYYY-MM-DD)
        check_in: 上班打卡时间 (HH:MM)
        check_out: 下班打卡时间 (HH:MM)
        day_type: 工作日类型 (weekday/weekend/holiday/rest_day)
    
    Returns:
        PunchRecord 对象
    """
    day_type_map = {
        "weekday": WorkDayType.WEEKDAY,
        "weekend": WorkDayType.WEEKEND,
        "holiday": WorkDayType.HOLIDAY,
        "rest_day": WorkDayType.REST_DAY,
    }
    
    return PunchRecord(
        date=datetime.strptime(date_str, "%Y-%m-%d").date(),
        check_in=datetime.strptime(check_in, "%H:%M").time() if check_in else None,
        check_out=datetime.strptime(check_out, "%H:%M").time() if check_out else None,
        day_type=day_type_map.get(day_type, WorkDayType.WEEKDAY),
    )


if __name__ == "__main__":
    # 简单测试
    print("=== 工作时长计算器测试 ===\n")
    
    # 创建计算器
    calculator = WorkHoursCalculator(
        break_periods=[(time(12, 0), time(13, 0))]
    )
    
    # 测试日工作时长计算
    print("1. 日工作时长计算:")
    result = calculator.calculate_daily_hours(
        check_in=time(9, 0),
        check_out=time(19, 0)
    )
    for key, value in result.items():
        print(f"   {key}: {value}")
    
    print("\n2. 周工作时长统计:")
    records = [
        create_punch_record("2024-01-08", "09:00", "18:30"),
        create_punch_record("2024-01-09", "09:15", "19:00"),
        create_punch_record("2024-01-10", "09:00", "20:00"),
        create_punch_record("2024-01-11", "09:00", "18:00"),
        create_punch_record("2024-01-12", "09:00", "17:30"),
    ]
    weekly_result = calculator.calculate_weekly_hours(records)
    print(f"   总工作时长: {weekly_result['total_work_hours']} 小时")
    print(f"   加班时长: {weekly_result['total_overtime_hours']} 小时")
    print(f"   工作天数: {weekly_result['work_days']}")
    
    print("\n3. 加班工资计算:")
    overtime_pay = calculator.calculate_overtime_pay(
        weekly_result['overtime_records'],
        hourly_rate=50.0
    )
    print(f"   总加班工资: ¥{overtime_pay['total_overtime_pay']}")
    
    print("\n4. 考勤分析:")
    analyzer = TimeAttendanceAnalyzer()
    analysis = analyzer.analyze_period(records)
    print(f"   出勤率: {analysis['summary']['attendance_rate']}%")
    print(f"   准时率: {analysis['summary']['punctuality_rate']}%")
    print(f"   迟到天数: {analysis['summary']['late_days']}")
    
    print("\n测试完成!")