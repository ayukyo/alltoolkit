"""
Habit Tracker Utilities - 习惯追踪工具

提供完整的习惯追踪功能，包括：
- 习惯定义与管理
- 连续打卡（Streak）计算
- 完成率统计
- 目标进度追踪
- 最佳/最差时段分析
- 习惯推荐系统

零外部依赖，纯 Python 实现。
"""

from typing import List, Dict, Optional, Tuple, Set, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from enum import Enum
import json


def _parse_date(date_str: str) -> date:
    """解析日期字符串 (兼容 Python 3.6)"""
    return datetime.strptime(date_str, "%Y-%m-%d").date()


class FrequencyType(Enum):
    """习惯频率类型"""
    DAILY = "daily"  # 每天
    WEEKLY = "weekly"  # 每周
    MONTHLY = "monthly"  # 每月
    CUSTOM = "custom"  # 自定义


class DayOfWeek(Enum):
    """星期枚举"""
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


@dataclass
class HabitCompletion:
    """习惯完成记录"""
    date: date
    completed: bool
    value: Optional[float] = None  # 可选：完成数量/时间等
    note: Optional[str] = None  # 可选：备注
    mood: Optional[int] = None  # 可选：心情 1-5
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'date': self.date.isoformat(),
            'completed': self.completed,
            'value': self.value,
            'note': self.note,
            'mood': self.mood,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HabitCompletion':
        """从字典创建"""
        return cls(
            date=_parse_date(data['date']),
            completed=data['completed'],
            value=data.get('value'),
            note=data.get('note'),
            mood=data.get('mood'),
        )


@dataclass
class Habit:
    """习惯定义"""
    name: str
    description: str = ""
    frequency: FrequencyType = FrequencyType.DAILY
    target_days: List[int] = field(default_factory=list)  # 周几执行 (0-6)
    target_value: Optional[float] = None  # 目标值（如每天8杯水）
    color: str = "#4CAF50"  # 显示颜色
    icon: str = "✓"  # 图标
    created_at: date = field(default_factory=date.today)
    completions: Dict[date, HabitCompletion] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    priority: int = 1  # 优先级 1-5
    reminder_time: Optional[str] = None  # 提醒时间 "HH:MM"
    
    def __post_init__(self):
        """初始化后处理"""
        # 注意：空 target_days 表示每周习惯不执行任何日期
        # 如果用户想每天执行，需要显式设置 target_days = [0,1,2,3,4,5,6]
        pass
    
    def complete(self, 
                 target_date: Optional[date] = None,
                 value: Optional[float] = None,
                 note: Optional[str] = None,
                 mood: Optional[int] = None) -> HabitCompletion:
        """
        标记习惯为已完成
        
        Args:
            target_date: 目标日期，默认今天
            value: 完成值
            note: 备注
            mood: 心情
            
        Returns:
            完成记录
        """
        if target_date is None:
            target_date = date.today()
        
        completion = HabitCompletion(
            date=target_date,
            completed=True,
            value=value,
            note=note,
            mood=mood,
        )
        self.completions[target_date] = completion
        return completion
    
    def skip(self, 
             target_date: Optional[date] = None,
             note: Optional[str] = None) -> HabitCompletion:
        """
        标记习惯为跳过
        
        Args:
            target_date: 目标日期，默认今天
            note: 跳过原因
            
        Returns:
            完成记录
        """
        if target_date is None:
            target_date = date.today()
        
        completion = HabitCompletion(
            date=target_date,
            completed=False,
            note=note or "skipped",
        )
        self.completions[target_date] = completion
        return completion
    
    def is_due(self, target_date: Optional[date] = None) -> bool:
        """
        检查指定日期是否需要执行该习惯
        
        Args:
            target_date: 目标日期，默认今天
            
        Returns:
            是否需要执行
        """
        if target_date is None:
            target_date = date.today()
        
        if self.frequency == FrequencyType.DAILY:
            return True
        elif self.frequency == FrequencyType.WEEKLY:
            return target_date.weekday() in self.target_days
        elif self.frequency == FrequencyType.MONTHLY:
            # 月度习惯：每月特定日期执行
            return target_date.day in (self.target_days or [1])
        else:
            return True
    
    def is_completed(self, target_date: Optional[date] = None) -> bool:
        """
        检查指定日期是否已完成
        
        Args:
            target_date: 目标日期，默认今天
            
        Returns:
            是否已完成
        """
        if target_date is None:
            target_date = date.today()
        
        completion = self.completions.get(target_date)
        return completion.completed if completion else False
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'description': self.description,
            'frequency': self.frequency.value,
            'target_days': self.target_days,
            'target_value': self.target_value,
            'color': self.color,
            'icon': self.icon,
            'created_at': self.created_at.isoformat(),
            'completions': {d.isoformat(): c.to_dict() 
                          for d, c in self.completions.items()},
            'tags': self.tags,
            'priority': self.priority,
            'reminder_time': self.reminder_time,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Habit':
        """从字典创建"""
        habit = cls(
            name=data['name'],
            description=data.get('description', ''),
            frequency=FrequencyType(data.get('frequency', 'daily')),
            target_days=data.get('target_days', []),
            target_value=data.get('target_value'),
            color=data.get('color', '#4CAF50'),
            icon=data.get('icon', '✓'),
            created_at=_parse_date(data['created_at']),
            tags=data.get('tags', []),
            priority=data.get('priority', 1),
            reminder_time=data.get('reminder_time'),
        )
        
        # 恢复完成记录
        for date_str, comp_data in data.get('completions', {}).items():
            comp_date = _parse_date(date_str)
            habit.completions[comp_date] = HabitCompletion.from_dict(comp_data)
        
        return habit


@dataclass
class HabitStats:
    """习惯统计数据"""
    total_days: int = 0  # 总天数
    completed_days: int = 0  # 完成天数
    missed_days: int = 0  # 错过天数
    skipped_days: int = 0  # 跳过天数
    current_streak: int = 0  # 当前连续
    longest_streak: int = 0  # 最长连续
    completion_rate: float = 0.0  # 完成率
    best_day: Optional[str] = None  # 最佳星期
    worst_day: Optional[str] = None  # 最差星期
    average_mood: Optional[float] = None  # 平均心情
    total_value: float = 0.0  # 总完成值
    average_value: Optional[float] = None  # 平均完成值
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'total_days': self.total_days,
            'completed_days': self.completed_days,
            'missed_days': self.missed_days,
            'skipped_days': self.skipped_days,
            'current_streak': self.current_streak,
            'longest_streak': self.longest_streak,
            'completion_rate': round(self.completion_rate, 2),
            'best_day': self.best_day,
            'worst_day': self.worst_day,
            'average_mood': round(self.average_mood, 2) if self.average_mood else None,
            'total_value': self.total_value,
            'average_value': round(self.average_value, 2) if self.average_value else None,
        }


class HabitTracker:
    """
    习惯追踪器
    
    管理多个习惯，提供统计分析和报告功能。
    
    Example:
        >>> tracker = HabitTracker()
        >>> tracker.add_habit("跑步", "每天跑步30分钟")
        >>> tracker.complete_habit("跑步")
        >>> stats = tracker.get_stats("跑步")
        >>> print(f"当前连续: {stats.current_streak}天")
    """
    
    DAY_NAMES = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    DAY_NAMES_EN = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    def __init__(self):
        """初始化习惯追踪器"""
        self.habits: Dict[str, Habit] = {}
    
    def add_habit(self,
                  name: str,
                  description: str = "",
                  frequency: FrequencyType = FrequencyType.DAILY,
                  target_days: Optional[List[int]] = None,
                  target_value: Optional[float] = None,
                  color: str = "#4CAF50",
                  icon: str = "✓",
                  tags: Optional[List[str]] = None,
                  priority: int = 1) -> Habit:
        """
        添加新习惯
        
        Args:
            name: 习惯名称
            description: 习惯描述
            frequency: 频率类型
            target_days: 执行日期（周几）
            target_value: 目标值
            color: 显示颜色
            icon: 图标
            tags: 标签
            priority: 优先级
            
        Returns:
            创建的习惯对象
        """
        habit = Habit(
            name=name,
            description=description,
            frequency=frequency,
            target_days=target_days or [],
            target_value=target_value,
            color=color,
            icon=icon,
            tags=tags or [],
            priority=priority,
        )
        self.habits[name] = habit
        return habit
    
    def remove_habit(self, name: str) -> bool:
        """
        删除习惯
        
        Args:
            name: 习惯名称
            
        Returns:
            是否删除成功
        """
        if name in self.habits:
            del self.habits[name]
            return True
        return False
    
    def get_habit(self, name: str) -> Optional[Habit]:
        """
        获取习惯
        
        Args:
            name: 习惯名称
            
        Returns:
            习惯对象，不存在返回 None
        """
        return self.habits.get(name)
    
    def complete_habit(self,
                       name: str,
                       target_date: Optional[date] = None,
                       value: Optional[float] = None,
                       note: Optional[str] = None,
                       mood: Optional[int] = None) -> Optional[HabitCompletion]:
        """
        标记习惯为已完成
        
        Args:
            name: 习惯名称
            target_date: 目标日期
            value: 完成值
            note: 备注
            mood: 心情
            
        Returns:
            完成记录
        """
        habit = self.habits.get(name)
        if habit:
            return habit.complete(target_date, value, note, mood)
        return None
    
    def skip_habit(self,
                   name: str,
                   target_date: Optional[date] = None,
                   note: Optional[str] = None) -> Optional[HabitCompletion]:
        """
        标记习惯为跳过
        
        Args:
            name: 习惯名称
            target_date: 目标日期
            note: 跳过原因
            
        Returns:
            完成记录
        """
        habit = self.habits.get(name)
        if habit:
            return habit.skip(target_date, note)
        return None
    
    def calculate_streak(self, 
                         habit: Habit,
                         end_date: Optional[date] = None) -> Tuple[int, int]:
        """
        计算连续打卡天数
        
        Args:
            habit: 习惯对象
            end_date: 结束日期，默认今天
            
        Returns:
            (当前连续, 最长连续)
        """
        if end_date is None:
            end_date = date.today()
        
        # 获取所有需要执行的日期
        due_dates = self._get_due_dates(habit, end_date)
        
        if not due_dates:
            return 0, 0
        
        # 按日期排序
        due_dates.sort()
        
        # 计算当前连续
        current_streak = 0
        for d in reversed(due_dates):
            if habit.is_completed(d):
                current_streak += 1
            else:
                break
        
        # 计算最长连续
        longest_streak = 0
        temp_streak = 0
        for d in due_dates:
            if habit.is_completed(d):
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 0
        
        return current_streak, longest_streak
    
    def _get_due_dates(self, 
                        habit: Habit,
                        end_date: date,
                        start_date: Optional[date] = None) -> List[date]:
        """获取习惯需要执行的所有日期"""
        if start_date is None:
            # 考虑创建日期和最早完成记录
            start_date = habit.created_at
            if habit.completions:
                earliest_completion = min(habit.completions.keys())
                if earliest_completion < start_date:
                    start_date = earliest_completion
        
        due_dates = []
        current = start_date
        
        while current <= end_date:
            if habit.is_due(current):
                due_dates.append(current)
            current += timedelta(days=1)
        
        return due_dates
    
    def get_stats(self, 
                  name: str,
                  start_date: Optional[date] = None,
                  end_date: Optional[date] = None) -> Optional[HabitStats]:
        """
        获取习惯统计数据
        
        Args:
            name: 习惯名称
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            统计数据
        """
        habit = self.habits.get(name)
        if not habit:
            return None
        
        if end_date is None:
            end_date = date.today()
        
        if start_date is None:
            # 考虑创建日期和最早完成记录
            start_date = habit.created_at
            if habit.completions:
                earliest_completion = min(habit.completions.keys())
                if earliest_completion < start_date:
                    start_date = earliest_completion
        
        # 获取时间范围内的应执行日期
        due_dates = self._get_due_dates(habit, end_date, start_date)
        
        if not due_dates:
            return HabitStats()
        
        # 统计完成情况
        completed_days = 0
        missed_days = 0
        skipped_days = 0
        total_value = 0.0
        value_count = 0
        mood_sum = 0
        mood_count = 0
        
        # 按星期统计
        day_stats: Dict[int, Dict[str, int]] = {i: {'completed': 0, 'total': 0} 
                                                 for i in range(7)}
        
        for d in due_dates:
            day_of_week = d.weekday()
            day_stats[day_of_week]['total'] += 1
            
            completion = habit.completions.get(d)
            if completion:
                if completion.completed:
                    completed_days += 1
                    day_stats[day_of_week]['completed'] += 1
                    
                    if completion.value is not None:
                        total_value += completion.value
                        value_count += 1
                    
                    if completion.mood is not None:
                        mood_sum += completion.mood
                        mood_count += 1
                else:
                    skipped_days += 1
            else:
                missed_days += 1
        
        # 计算完成率
        total_due = len(due_dates)
        completion_rate = completed_days / total_due if total_due > 0 else 0.0
        
        # 计算连续天数
        current_streak, longest_streak = self.calculate_streak(habit, end_date)
        
        # 找最佳/最差星期
        best_day = None
        worst_day = None
        best_rate = -1
        worst_rate = 2.0
        
        for day_idx, stats in day_stats.items():
            if stats['total'] > 0:
                rate = stats['completed'] / stats['total']
                if rate > best_rate:
                    best_rate = rate
                    best_day = self.DAY_NAMES[day_idx]
                if rate < worst_rate:
                    worst_rate = rate
                    worst_day = self.DAY_NAMES[day_idx]
        
        return HabitStats(
            total_days=total_due,
            completed_days=completed_days,
            missed_days=missed_days,
            skipped_days=skipped_days,
            current_streak=current_streak,
            longest_streak=longest_streak,
            completion_rate=completion_rate,
            best_day=best_day,
            worst_day=worst_day,
            average_mood=mood_sum / mood_count if mood_count > 0 else None,
            total_value=total_value,
            average_value=total_value / value_count if value_count > 0 else None,
        )
    
    def get_weekly_report(self, 
                          name: str,
                          week_start: Optional[date] = None) -> Dict[str, Any]:
        """
        获取周报告
        
        Args:
            name: 习惯名称
            week_start: 周开始日期，默认本周
            
        Returns:
            周报告数据
        """
        habit = self.habits.get(name)
        if not habit:
            return {}
        
        if week_start is None:
            today = date.today()
            week_start = today - timedelta(days=today.weekday())
        
        week_end = week_start + timedelta(days=6)
        
        daily_status = []
        for i in range(7):
            d = week_start + timedelta(days=i)
            completion = habit.completions.get(d)
            daily_status.append({
                'date': d.isoformat(),
                'day_name': self.DAY_NAMES[i],
                'is_due': habit.is_due(d),
                'completed': completion.completed if completion else False,
                'value': completion.value if completion else None,
                'note': completion.note if completion else None,
            })
        
        stats = self.get_stats(name, week_start, week_end)
        
        return {
            'habit_name': name,
            'week_start': week_start.isoformat(),
            'week_end': week_end.isoformat(),
            'daily_status': daily_status,
            'stats': stats.to_dict() if stats else {},
        }
    
    def get_monthly_calendar(self,
                              name: str,
                              year: int,
                              month: int) -> Dict[str, Any]:
        """
        获取月度日历视图
        
        Args:
            name: 习惯名称
            year: 年份
            month: 月份
            
        Returns:
            月度日历数据
        """
        habit = self.habits.get(name)
        if not habit:
            return {}
        
        from calendar import monthrange
        _, days_in_month = monthrange(year, month)
        
        calendar_data = []
        for day in range(1, days_in_month + 1):
            d = date(year, month, day)
            completion = habit.completions.get(d)
            calendar_data.append({
                'date': d.isoformat(),
                'day': day,
                'day_of_week': d.weekday(),
                'day_name': self.DAY_NAMES[d.weekday()],
                'is_due': habit.is_due(d),
                'completed': completion.completed if completion else False,
                'value': completion.value if completion else None,
            })
        
        start_date = date(year, month, 1)
        end_date = date(year, month, days_in_month)
        stats = self.get_stats(name, start_date, end_date)
        
        return {
            'habit_name': name,
            'year': year,
            'month': month,
            'calendar': calendar_data,
            'stats': stats.to_dict() if stats else {},
        }
    
    def get_all_stats(self) -> Dict[str, HabitStats]:
        """获取所有习惯的统计数据"""
        return {name: self.get_stats(name) for name in self.habits}
    
    def get_today_habits(self) -> List[Habit]:
        """获取今天需要执行的习惯"""
        today = date.today()
        return [h for h in self.habits.values() if h.is_due(today)]
    
    def get_today_status(self) -> Dict[str, Dict[str, Any]]:
        """获取今日习惯状态"""
        today = date.today()
        result = {}
        
        for name, habit in self.habits.items():
            if habit.is_due(today):
                result[name] = {
                    'completed': habit.is_completed(today),
                    'value': None,
                    'note': None,
                }
                completion = habit.completions.get(today)
                if completion:
                    result[name]['value'] = completion.value
                    result[name]['note'] = completion.note
        
        return result
    
    def get_completion_heatmap(self,
                                name: str,
                                year: Optional[int] = None) -> Dict[str, Any]:
        """
        获取完成热力图数据
        
        Args:
            name: 习惯名称
            year: 年份，默认当前年
            
        Returns:
            热力图数据
        """
        habit = self.habits.get(name)
        if not habit:
            return {}
        
        if year is None:
            year = date.today().year
        
        heatmap = {}
        current = date(year, 1, 1)
        end = date(year, 12, 31)
        
        while current <= end:
            if habit.is_due(current):
                completion = habit.completions.get(current)
                heatmap[current.isoformat()] = {
                    'completed': completion.completed if completion else False,
                    'value': completion.value if completion else None,
                }
            current += timedelta(days=1)
        
        return {
            'habit_name': name,
            'year': year,
            'heatmap': heatmap,
        }
    
    def recommend_habits(self) -> List[Dict[str, Any]]:
        """
        基于现有习惯推荐新习惯
        
        Returns:
            推荐习惯列表
        """
        # 预定义的习惯推荐关系
        recommendations = {
            '跑步': [
                {'name': '拉伸', 'description': '跑步后拉伸', 'tags': ['运动', '恢复']},
                {'name': '喝水', 'description': '每天8杯水', 'tags': ['健康', '日常']},
            ],
            '冥想': [
                {'name': '早睡', 'description': '晚上10点前睡觉', 'tags': ['健康', '睡眠']},
                {'name': '写日记', 'description': '每天记录心情', 'tags': ['心理', '成长']},
            ],
            '阅读': [
                {'name': '笔记', 'description': '记录阅读笔记', 'tags': ['学习', '成长']},
                {'name': '分享', 'description': '分享读书心得', 'tags': ['社交', '学习']},
            ],
            '健身': [
                {'name': '蛋白摄入', 'description': '每餐保证蛋白质', 'tags': ['饮食', '健康']},
                {'name': '休息', 'description': '保证充足休息', 'tags': ['健康', '恢复']},
            ],
        }
        
        result = []
        existing_names = set(self.habits.keys())
        
        for habit_name, recs in recommendations.items():
            if habit_name in existing_names:
                for rec in recs:
                    if rec['name'] not in existing_names:
                        result.append(rec)
        
        # 通用推荐
        general_recs = [
            {'name': '早起', 'description': '每天早起', 'tags': ['生活', '效率']},
            {'name': '喝水', 'description': '每天8杯水', 'tags': ['健康', '日常']},
            {'name': '散步', 'description': '每天散步30分钟', 'tags': ['运动', '健康']},
            {'name': '感恩', 'description': '记录感恩的事', 'tags': ['心理', '成长']},
        ]
        
        for rec in general_recs:
            if rec['name'] not in existing_names and rec not in result:
                result.append(rec)
        
        return result[:5]  # 返回最多5个推荐
    
    def export_data(self) -> str:
        """导出数据为JSON字符串"""
        data = {
            'habits': {name: habit.to_dict() for name, habit in self.habits.items()},
            'exported_at': datetime.now().isoformat(),
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    def import_data(self, json_str: str) -> int:
        """
        从JSON字符串导入数据
        
        Args:
            json_str: JSON字符串
            
        Returns:
            导入的习惯数量
        """
        data = json.loads(json_str)
        count = 0
        
        for name, habit_data in data.get('habits', {}).items():
            if name not in self.habits:
                self.habits[name] = Habit.from_dict(habit_data)
                count += 1
        
        return count
    
    def save_to_file(self, filepath: str) -> None:
        """保存数据到文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.export_data())
    
    def load_from_file(self, filepath: str) -> int:
        """从文件加载数据"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return self.import_data(f.read())


class HabitUtils:
    """
    习惯追踪工具高级接口
    
    提供简化的静态方法。
    """
    
    @staticmethod
    def create_tracker() -> HabitTracker:
        """创建习惯追踪器"""
        return HabitTracker()
    
    @staticmethod
    def calculate_streak(completions: Dict[date, bool], 
                         end_date: Optional[date] = None) -> Tuple[int, int]:
        """
        计算连续打卡天数
        
        Args:
            completions: 完成记录 {日期: 是否完成}
            end_date: 结束日期
            
        Returns:
            (当前连续, 最长连续)
        """
        if end_date is None:
            end_date = date.today()
        
        # 获取所有日期并排序
        dates = sorted(completions.keys())
        
        if not dates:
            return 0, 0
        
        # 计算当前连续（从最后一天往前）
        current_streak = 0
        current = end_date
        
        # 只考虑有记录的日期
        while current in completions:
            if completions[current]:
                current_streak += 1
                current -= timedelta(days=1)
            else:
                break
        
        # 计算最长连续
        longest_streak = 0
        temp_streak = 0
        
        for d in dates:
            if completions.get(d, False):
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 0
        
        return current_streak, longest_streak
    
    @staticmethod
    def completion_rate(completions: Dict[date, bool],
                        start_date: Optional[date] = None,
                        end_date: Optional[date] = None) -> float:
        """
        计算完成率
        
        Args:
            completions: 完成记录
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            完成率 (0.0 - 1.0)
        """
        if not completions:
            return 0.0
        
        dates = sorted(completions.keys())
        
        if start_date is None:
            start_date = dates[0]
        if end_date is None:
            end_date = dates[-1]
        
        # 筛选范围内的日期
        filtered = {d: v for d, v in completions.items() 
                   if start_date <= d <= end_date}
        
        if not filtered:
            return 0.0
        
        completed = sum(1 for v in filtered.values() if v)
        return completed / len(filtered)


# 便捷函数
def create_habit(name: str, **kwargs) -> Habit:
    """创建习惯便捷函数"""
    return Habit(name=name, **kwargs)


def calculate_streak(completions: Dict[date, bool],
                     end_date: Optional[date] = None) -> Tuple[int, int]:
    """计算连续天数便捷函数"""
    return HabitUtils.calculate_streak(completions, end_date)


def completion_rate(completions: Dict[date, bool],
                    start_date: Optional[date] = None,
                    end_date: Optional[date] = None) -> float:
    """计算完成率便捷函数"""
    return HabitUtils.completion_rate(completions, start_date, end_date)


if __name__ == "__main__":
    # 简单演示
    print("=== 习惯追踪工具演示 ===")
    
    # 创建追踪器
    tracker = HabitTracker()
    
    # 添加习惯
    tracker.add_habit("跑步", "每天跑步30分钟", icon="🏃", color="#FF5722")
    tracker.add_habit("阅读", "每天阅读1小时", 
                      frequency=FrequencyType.DAILY, 
                      target_value=60,
                      icon="📚",
                      color="#2196F3")
    tracker.add_habit("冥想", "每周一三五冥想", 
                      frequency=FrequencyType.WEEKLY,
                      target_days=[0, 2, 4],  # 周一三五
                      icon="🧘",
                      color="#9C27B0")
    
    # 模拟一些完成记录
    today = date.today()
    
    # 标记今天完成
    tracker.complete_habit("跑步", value=30, mood=4, note="感觉不错！")
    tracker.complete_habit("阅读", value=65, mood=5)
    
    # 模拟过去几天
    for i in range(1, 8):
        d = today - timedelta(days=i)
        tracker.complete_habit("跑步", target_date=d, value=30)
        tracker.complete_habit("阅读", target_date=d, value=60)
        
        # 冥想只在周一三五
        if d.weekday() in [0, 2, 4]:
            tracker.complete_habit("冥想", target_date=d)
    
    # 获取统计
    print("\n--- 跑步统计 ---")
    stats = tracker.get_stats("跑步")
    print(f"当前连续: {stats.current_streak} 天")
    print(f"最长连续: {stats.longest_streak} 天")
    print(f"完成率: {stats.completion_rate * 100:.1f}%")
    print(f"最佳星期: {stats.best_day}")
    
    print("\n--- 今日状态 ---")
    today_status = tracker.get_today_status()
    for name, status in today_status.items():
        emoji = "✅" if status['completed'] else "⬜"
        print(f"{emoji} {name}: {'已完成' if status['completed'] else '待完成'}")
    
    print("\n--- 周报告 ---")
    report = tracker.get_weekly_report("跑步")
    for day in report['daily_status']:
        emoji = "✅" if day['completed'] else "⬜"
        if day['is_due']:
            print(f"{emoji} {day['day_name']} ({day['date']}): {'完成' if day['completed'] else '未完成'}")
    
    print("\n--- 推荐习惯 ---")
    recs = tracker.recommend_habits()
    for rec in recs[:3]:
        print(f"💡 {rec['name']}: {rec['description']}")
    
    # 导出数据
    print("\n--- 数据导出 ---")
    json_data = tracker.export_data()
    print(f"导出数据长度: {len(json_data)} 字符")