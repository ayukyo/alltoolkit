"""
Habit Chain Utils - 习惯链追踪工具

实现习惯链追踪功能，帮助用户追踪连续习惯形成的链条。
支持"不要断链"概念，计算最长连续天数、当前连续天数、
统计习惯完成率等功能。

零外部依赖，纯Python实现。
"""

from datetime import date, datetime, timedelta
from typing import Optional, List, Dict, Set, Tuple
from enum import Enum
import json


def _parse_iso_date(date_str: str) -> date:
    """解析ISO格式日期字符串，兼容Python 3.6"""
    return datetime.strptime(date_str, "%Y-%m-%d").date()


class HabitFrequency(Enum):
    """习惯频率类型"""
    DAILY = "daily"           # 每日
    WEEKDAYS = "weekdays"      # 工作日
    WEEKENDS = "weekends"      # 周末
    WEEKLY = "weekly"          # 每周
    CUSTOM = "custom"          # 自定义星期几


class HabitChain:
    """习惯链类 - 管理单个习惯的追踪"""
    
    def __init__(
        self,
        name: str,
        frequency: HabitFrequency = HabitFrequency.DAILY,
        custom_days: Optional[Set[int]] = None,  # 0=周一, 6=周日
        start_date: Optional[date] = None,
        color: str = "#4CAF50"
    ):
        """
        初始化习惯链
        
        Args:
            name: 习惯名称
            frequency: 频率类型
            custom_days: 自定义星期几 (0=周一, 6=周日)，仅当frequency=CUSTOM时使用
            start_date: 开始追踪日期，默认今天
            color: 显示颜色 (十六进制)
        """
        self.name = name
        self.frequency = frequency
        self.custom_days = custom_days or set()
        self.start_date = start_date or date.today()
        self.color = color
        self._completed_dates: Set[date] = set()
    
    def _should_track(self, d: date) -> bool:
        """检查某天是否应该追踪此习惯"""
        weekday = d.weekday()  # 0=周一, 6=周日
        
        if self.frequency == HabitFrequency.DAILY:
            return True
        elif self.frequency == HabitFrequency.WEEKDAYS:
            return weekday < 5  # 周一到周五
        elif self.frequency == HabitFrequency.WEEKENDS:
            return weekday >= 5  # 周六和周日
        elif self.frequency == HabitFrequency.WEEKLY:
            # 每周只需完成一次，每天都可以追踪
            return True
        elif self.frequency == HabitFrequency.CUSTOM:
            return weekday in self.custom_days
        return False
    
    def complete(self, d: Optional[date] = None) -> bool:
        """
        标记某天完成习惯
        
        Args:
            d: 日期，默认今天
            
        Returns:
            是否成功标记（如果在非追踪日会返回False）
        """
        d = d or date.today()
        if not self._should_track(d):
            return False
        self._completed_dates.add(d)
        return True
    
    def uncomplete(self, d: Optional[date] = None) -> bool:
        """
        取消某天的完成标记
        
        Args:
            d: 日期，默认今天
            
        Returns:
            是否成功取消
        """
        d = d or date.today()
        if d in self._completed_dates:
            self._completed_dates.remove(d)
            return True
        return False
    
    def is_completed(self, d: Optional[date] = None) -> bool:
        """检查某天是否完成"""
        d = d or date.today()
        return d in self._completed_dates
    
    def get_current_streak(self) -> int:
        """
        获取当前连续天数
        
        从今天往前数连续完成的追踪天数
        """
        streak = 0
        d = date.today()
        
        while True:
            if self._should_track(d):
                if d in self._completed_dates:
                    streak += 1
                else:
                    break
            d -= timedelta(days=1)
            
            # 防止无限循环，最多检查一年
            if d < self.start_date - timedelta(days=365):
                break
        
        return streak
    
    def get_longest_streak(self) -> int:
        """获取历史最长连续天数"""
        if not self._completed_dates:
            return 0
        
        sorted_dates = sorted(self._completed_dates)
        if not sorted_dates:
            return 0
        
        longest = 1
        current = 1
        
        for i in range(1, len(sorted_dates)):
            # 检查两个日期之间是否为连续的追踪日
            prev_date = sorted_dates[i-1]
            curr_date = sorted_dates[i]
            
            # 向前推进，检查是否有遗漏的追踪日
            check_date = prev_date + timedelta(days=1)
            consecutive = True
            
            while check_date < curr_date:
                if self._should_track(check_date):
                    consecutive = False
                    break
                check_date += timedelta(days=1)
            
            if consecutive:
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        
        return longest
    
    def get_completion_rate(self, days: int = 30) -> float:
        """
        获取最近N天的完成率
        
        Args:
            days: 统计天数
            
        Returns:
            完成率 (0.0 - 1.0)
        """
        if days <= 0:
            return 0.0
        
        end_date = date.today()
        start_date = end_date - timedelta(days=days-1)
        
        track_days = 0
        completed_days = 0
        
        d = start_date
        while d <= end_date:
            if self._should_track(d):
                track_days += 1
                if d in self._completed_dates:
                    completed_days += 1
            d += timedelta(days=1)
        
        if track_days == 0:
            return 0.0
        
        return completed_days / track_days
    
    def get_weekly_progress(self, week_start: Optional[date] = None) -> Dict:
        """
        获取某周的进度
        
        Args:
            week_start: 周开始日期，默认本周一
            
        Returns:
            周进度字典
        """
        if week_start is None:
            today = date.today()
            week_start = today - timedelta(days=today.weekday())
        
        week_end = week_start + timedelta(days=6)
        
        days = []
        completed = 0
        should_track = 0
        
        d = week_start
        while d <= week_end:
            should = self._should_track(d)
            done = d in self._completed_dates
            
            days.append({
                "date": d.isoformat(),
                "weekday": d.weekday(),
                "should_track": should,
                "completed": done
            })
            
            if should:
                should_track += 1
                if done:
                    completed += 1
            
            d += timedelta(days=1)
        
        return {
            "week_start": week_start.isoformat(),
            "week_end": week_end.isoformat(),
            "days": days,
            "completed": completed,
            "total_tracked_days": should_track,
            "rate": completed / should_track if should_track > 0 else 0.0
        }
    
    def get_stats(self) -> Dict:
        """获取习惯统计信息"""
        total_tracked = 0
        total_completed = 0
        
        d = self.start_date
        today = date.today()
        
        while d <= today:
            if self._should_track(d):
                total_tracked += 1
                if d in self._completed_dates:
                    total_completed += 1
            d += timedelta(days=1)
        
        return {
            "name": self.name,
            "frequency": self.frequency.value,
            "start_date": self.start_date.isoformat(),
            "color": self.color,
            "total_tracked_days": total_tracked,
            "total_completed_days": total_completed,
            "current_streak": self.get_current_streak(),
            "longest_streak": self.get_longest_streak(),
            "completion_rate": total_completed / total_tracked if total_tracked > 0 else 0.0,
            "last_30_days_rate": self.get_completion_rate(30),
            "is_completed_today": self.is_completed()
        }
    
    def get_calendar_heatmap(self, year: Optional[int] = None, month: Optional[int] = None) -> List[List[Dict]]:
        """
        获取日历热力图数据
        
        Args:
            year: 年份，默认当前年
            month: 月份，默认当前月
            
        Returns:
            按周分组的日历数据
        """
        today = date.today()
        year = year or today.year
        month = month or today.month
        
        # 获取月份第一天和最后一天
        first_day = date(year, month, 1)
        if month == 12:
            last_day = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = date(year, month + 1, 1) - timedelta(days=1)
        
        # 找到月份第一周的周一
        first_monday = first_day - timedelta(days=first_day.weekday())
        
        # 找到最后一天的周日
        last_sunday = last_day + timedelta(days=6 - last_day.weekday())
        
        # 生成周数据
        weeks = []
        current = first_monday
        
        while current <= last_sunday:
            week = []
            for i in range(7):
                day_data = {
                    "date": current.isoformat(),
                    "day": current.day,
                    "month": current.month,
                    "year": current.year,
                    "in_month": current.month == month,
                    "weekday": current.weekday(),
                    "should_track": self._should_track(current),
                    "completed": current in self._completed_dates,
                    "is_today": current == today,
                    "is_future": current > today
                }
                week.append(day_data)
                current += timedelta(days=1)
            weeks.append(week)
        
        return weeks
    
    def to_dict(self) -> Dict:
        """序列化为字典"""
        return {
            "name": self.name,
            "frequency": self.frequency.value,
            "custom_days": list(self.custom_days),
            "start_date": self.start_date.isoformat(),
            "color": self.color,
            "completed_dates": [d.isoformat() for d in sorted(self._completed_dates)]
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'HabitChain':
        """从字典反序列化"""
        chain = cls(
            name=data["name"],
            frequency=HabitFrequency(data["frequency"]),
            custom_days=set(data.get("custom_days", [])),
            start_date=_parse_iso_date(data["start_date"]),
            color=data.get("color", "#4CAF50")
        )
        
        for d_str in data.get("completed_dates", []):
            chain._completed_dates.add(_parse_iso_date(d_str))
        
        return chain


class HabitChainManager:
    """习惯链管理器 - 管理多个习惯"""
    
    def __init__(self):
        self._chains: Dict[str, HabitChain] = {}
    
    def add_chain(self, chain: HabitChain) -> bool:
        """添加习惯链"""
        if chain.name in self._chains:
            return False
        self._chains[chain.name] = chain
        return True
    
    def remove_chain(self, name: str) -> bool:
        """移除习惯链"""
        if name in self._chains:
            del self._chains[name]
            return True
        return False
    
    def get_chain(self, name: str) -> Optional[HabitChain]:
        """获取习惯链"""
        return self._chains.get(name)
    
    def complete(self, name: str, d: Optional[date] = None) -> bool:
        """标记某习惯完成"""
        chain = self._chains.get(name)
        if chain:
            return chain.complete(d)
        return False
    
    def uncomplete(self, name: str, d: Optional[date] = None) -> bool:
        """取消某习惯完成标记"""
        chain = self._chains.get(name)
        if chain:
            return chain.uncomplete(d)
        return False
    
    def get_all_stats(self) -> List[Dict]:
        """获取所有习惯的统计"""
        return [chain.get_stats() for chain in self._chains.values()]
    
    def get_today_overview(self) -> Dict:
        """获取今日概览"""
        today = date.today()
        habits = []
        completed = 0
        should_complete = 0
        
        for chain in self._chains.values():
            should = chain._should_track(today)
            done = chain.is_completed(today)
            
            habits.append({
                "name": chain.name,
                "color": chain.color,
                "should_track_today": should,
                "completed_today": done,
                "current_streak": chain.get_current_streak() if should else 0
            })
            
            if should:
                should_complete += 1
                if done:
                    completed += 1
        
        return {
            "date": today.isoformat(),
            "total_habits": len(self._chains),
            "habits_to_track_today": should_complete,
            "completed_today": completed,
            "completion_rate": completed / should_complete if should_complete > 0 else 0.0,
            "habits": sorted(habits, key=lambda x: (not x["should_track_today"], x["name"]))
        }
    
    def get_weekly_overview(self, week_start: Optional[date] = None) -> Dict:
        """获取周概览"""
        if week_start is None:
            today = date.today()
            week_start = today - timedelta(days=today.weekday())
        
        habits_weekly = {}
        
        for name, chain in self._chains.items():
            habits_weekly[name] = {
                "color": chain.color,
                "progress": chain.get_weekly_progress(week_start)
            }
        
        return {
            "week_start": week_start.isoformat(),
            "week_end": (week_start + timedelta(days=6)).isoformat(),
            "habits": habits_weekly
        }
    
    def get_leaderboard(self, by: str = "current_streak") -> List[Dict]:
        """
        获取排行榜
        
        Args:
            by: 排序字段 (current_streak, longest_streak, completion_rate)
        """
        stats = self.get_all_stats()
        
        valid_fields = {"current_streak", "longest_streak", "completion_rate", "last_30_days_rate"}
        if by not in valid_fields:
            by = "current_streak"
        
        return sorted(stats, key=lambda x: x.get(by, 0), reverse=True)
    
    def get_motivational_message(self) -> str:
        """获取激励消息"""
        today_overview = self.get_today_overview()
        
        total = today_overview["habits_to_track_today"]
        done = today_overview["completed_today"]
        
        if total == 0:
            return "今天没有需要追踪的习惯，休息一下也是好的！"
        
        if done == total:
            longest = max(
                (c.get_current_streak() for c in self._chains.values()),
                default=0
            )
            if longest > 30:
                return f"🎉 太棒了！你已经连续 {longest} 天，继续保持！"
            elif longest > 7:
                return f"💪 完美的一天！连续 {longest} 天不断链！"
            else:
                return "✅ 今日任务全部完成，你真棒！"
        
        if done > 0:
            remaining = total - done
            return f"已完成 {done}/{total} 个习惯，还有 {remaining} 个等你挑战！"
        
        # 检查是否有长链需要保护
        at_risk_chains = [
            c for c in self._chains.values()
            if c._should_track(date.today()) and c.get_current_streak() > 0
        ]
        
        if at_risk_chains:
            max_streak = max(c.get_current_streak() for c in at_risk_chains)
            return f"⚠️ 你有 {len(at_risk_chains)} 个习惯链可能断裂，最长 {max_streak} 天！加油！"
        
        return "新的一天开始了，开始你的习惯之旅吧！"
    
    def find_best_chain_day(self) -> Tuple[date, List[str]]:
        """
        找到最佳补链日（找到缺失最多习惯的日期）
        
        Returns:
            (日期, 该日缺失的习惯名列表)
        """
        today = date.today()
        best_date = today
        best_missing = []
        
        # 检查过去30天
        for i in range(30):
            check_date = today - timedelta(days=i+1)
            missing = []
            
            for name, chain in self._chains.items():
                if chain._should_track(check_date) and not chain.is_completed(check_date):
                    missing.append(name)
            
            if len(missing) > len(best_missing):
                best_missing = missing
                best_date = check_date
        
        return best_date, best_missing
    
    def to_json(self) -> str:
        """导出为JSON字符串"""
        data = {
            "chains": {name: chain.to_dict() for name, chain in self._chains.items()}
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'HabitChainManager':
        """从JSON字符串导入"""
        manager = cls()
        data = json.loads(json_str)
        
        for name, chain_data in data.get("chains", {}).items():
            chain = HabitChain.from_dict(chain_data)
            manager._chains[name] = chain
        
        return manager
    
    def save_to_file(self, filepath: str) -> bool:
        """保存到文件"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.to_json())
            return True
        except Exception:
            return False
    
    @classmethod
    def load_from_file(cls, filepath: str) -> Optional['HabitChainManager']:
        """从文件加载"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return cls.from_json(f.read())
        except Exception:
            return None


# 便捷函数
def create_daily_habit(name: str, color: str = "#4CAF50") -> HabitChain:
    """创建每日习惯"""
    return HabitChain(name, HabitFrequency.DAILY, color=color)


def create_weekday_habit(name: str, color: str = "#2196F3") -> HabitChain:
    """创建工作日习惯"""
    return HabitChain(name, HabitFrequency.WEEKDAYS, color=color)


def create_weekend_habit(name: str, color: str = "#FF9800") -> HabitChain:
    """创建周末习惯"""
    return HabitChain(name, HabitFrequency.WEEKENDS, color=color)


def create_custom_habit(name: str, days: Set[int], color: str = "#9C27B0") -> HabitChain:
    """
    创建自定义星期几习惯
    
    Args:
        name: 习惯名称
        days: 星期几集合 (0=周一, 6=周日)
        color: 颜色
    """
    return HabitChain(name, HabitFrequency.CUSTOM, custom_days=days, color=color)


def calculate_streak_milestone(streak: int) -> Dict:
    """
    计算连续天数里程碑
    
    Args:
        streak: 连续天数
        
    Returns:
        里程碑信息
    """
    milestones = [
        (7, "一周", "🎯"),
        (14, "两周", "🔥"),
        (21, "三周", "💪"),
        (30, "一个月", "🏆"),
        (60, "两个月", "⭐"),
        (90, "三个月", "🌟"),
        (100, "100天", "💎"),
        (180, "半年", "👑"),
        (365, "一年", "🏅"),
        (500, "500天", "🚀"),
        (1000, "1000天", "🌈"),
    ]
    
    current_milestone = None
    next_milestone = None
    progress_to_next = 0.0
    
    for i, (days, name, emoji) in enumerate(milestones):
        if streak >= days:
            current_milestone = {"days": days, "name": name, "emoji": emoji}
        else:
            next_milestone = {"days": days, "name": name, "emoji": emoji}
            if current_milestone:
                prev_days = milestones[i-1][0] if i > 0 else 0
            else:
                prev_days = 0
            progress_to_next = (streak - prev_days) / (days - prev_days)
            break
    
    if current_milestone and not next_milestone:
        progress_to_next = 1.0
    
    return {
        "current_streak": streak,
        "current_milestone": current_milestone,
        "next_milestone": next_milestone,
        "progress_to_next": min(progress_to_next, 1.0)
    }


def get_chain_health_score(chain: HabitChain) -> float:
    """
    计算习惯链健康分数 (0-100)
    
    基于以下因素：
    - 当前连续天数 (40%)
    - 最近30天完成率 (30%)
    - 总完成率 (20%)
    - 是否今天完成 (10%)
    """
    stats = chain.get_stats()
    
    # 连续天数得分 (最高40分)
    current_streak = stats["current_streak"]
    streak_score = min(current_streak * 2, 40)  # 每天2分，最多40分
    
    # 最近30天完成率得分 (最高30分)
    last_30_rate = stats["last_30_days_rate"]
    rate_30_score = last_30_rate * 30
    
    # 总完成率得分 (最高20分)
    total_rate = stats["completion_rate"]
    total_rate_score = total_rate * 20
    
    # 今日完成得分 (最高10分)
    today_score = 10 if stats["is_completed_today"] else 0
    
    return min(streak_score + rate_30_score + total_rate_score + today_score, 100.0)


if __name__ == "__main__":
    # 简单演示
    manager = HabitChainManager()
    
    # 创建几个习惯
    reading = create_daily_habit("阅读30分钟", "#4CAF50")
    exercise = create_weekday_habit("健身", "#2196F3")
    meditation = create_daily_habit("冥想", "#9C27B0")
    
    manager.add_chain(reading)
    manager.add_chain(exercise)
    manager.add_chain(meditation)
    
    # 模拟一些完成记录
    from datetime import timedelta
    today = date.today()
    
    # 阅读连续7天
    for i in range(7):
        reading.complete(today - timedelta(days=i))
    
    # 健身完成过去5个工作日
    for i in range(10):
        d = today - timedelta(days=i)
        if exercise._should_track(d):
            exercise.complete(d)
    
    # 冥想偶尔完成
    meditation.complete(today)
    meditation.complete(today - timedelta(days=2))
    
    print("=== 今日概览 ===")
    print(json.dumps(manager.get_today_overview(), indent=2, ensure_ascii=False))
    
    print("\n=== 习惯统计 ===")
    for stats in manager.get_all_stats():
        print(f"\n{stats['name']}:")
        print(f"  当前连续: {stats['current_streak']} 天")
        print(f"  最长连续: {stats['longest_streak']} 天")
        print(f"  完成率: {stats['completion_rate']*100:.1f}%")
        print(f"  最近30天: {stats['last_30_days_rate']*100:.1f}%")
    
    print(f"\n=== 激励消息 ===")
    print(manager.get_motivational_message())