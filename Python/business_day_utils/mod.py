"""
Business Day Utils - 零依赖工作日计算工具库

提供完整的工作日计算功能，包括：
- 工作日判断（跳过周末）
- 节假日管理
- 工作日加减计算
- 计算两个日期之间的工作日数量
- 获取下一个/上一个工作日
- 批量工作日计算
- 自定义工作日定义（支持不同国家/地区）
"""

from typing import List, Set, Tuple, Optional, Callable
from datetime import datetime, date, timedelta
from dataclasses import dataclass, field
import calendar


class BusinessDayError(Exception):
    """工作日计算错误"""
    pass


@dataclass
class Holiday:
    """节假日定义"""
    name: str
    date: date
    is_recurring: bool = False  # 是否每年重复（如春节、国庆）
    description: str = ""
    
    def matches(self, check_date: date) -> bool:
        """检查日期是否匹配此节假日"""
        if self.is_recurring:
            return (check_date.month == self.date.month and 
                    check_date.day == self.date.day)
        return check_date == self.date


@dataclass
class BusinessDayConfig:
    """工作日配置"""
    # 工作日（0=周一, 6=周日）
    workdays: Set[int] = field(default_factory=lambda: {0, 1, 2, 3, 4})
    # 周末
    weekends: Set[int] = field(default_factory=lambda: {5, 6})
    # 节假日列表
    holidays: List[Holiday] = field(default_factory=list)
    # 调休工作日（原本是周末但需要上班的日子）
    adjusted_workdays: Set[date] = field(default_factory=set)
    # 自定义节假日判断函数
    custom_holiday_checker: Optional[Callable[[date], bool]] = None
    
    def add_holiday(self, name: str, holiday_date: date, 
                    is_recurring: bool = False, description: str = "") -> 'BusinessDayConfig':
        """添加节假日"""
        self.holidays.append(Holiday(name, holiday_date, is_recurring, description))
        return self
    
    def add_adjusted_workday(self, adj_date: date) -> 'BusinessDayConfig':
        """添加调休工作日"""
        self.adjusted_workdays.add(adj_date)
        return self
    
    def remove_holiday(self, name: str) -> 'BusinessDayConfig':
        """移除节假日"""
        self.holidays = [h for h in self.holidays if h.name != name]
        return self


class BusinessDayCalculator:
    """工作日计算器"""
    
    def __init__(self, config: Optional[BusinessDayConfig] = None):
        self.config = config or BusinessDayConfig()
    
    def is_weekend(self, check_date: date) -> bool:
        """判断是否为周末"""
        return check_date.weekday() in self.config.weekends
    
    def is_holiday(self, check_date: date) -> Tuple[bool, Optional[str]]:
        """
        判断是否为节假日
        返回: (是否为节假日, 节假日名称)
        """
        # 检查自定义节假日判断函数
        if self.config.custom_holiday_checker:
            if self.config.custom_holiday_checker(check_date):
                return True, "Custom Holiday"
        
        # 检查节假日列表
        for holiday in self.config.holidays:
            if holiday.matches(check_date):
                return True, holiday.name
        
        return False, None
    
    def is_adjusted_workday(self, check_date: date) -> bool:
        """判断是否为调休工作日"""
        return check_date in self.config.adjusted_workdays
    
    def is_business_day(self, check_date: date) -> bool:
        """判断是否为工作日"""
        # 调休工作日优先
        if self.is_adjusted_workday(check_date):
            return True
        
        # 节假日不是工作日
        is_hol, _ = self.is_holiday(check_date)
        if is_hol:
            return False
        
        # 检查是否为工作日
        return check_date.weekday() in self.config.workdays
    
    def add_business_days(self, start_date: date, days: int) -> date:
        """
        添加工作日
        days: 正数表示向后，负数表示向前
        """
        if days == 0:
            return start_date
        
        current = start_date
        direction = 1 if days > 0 else -1
        remaining = abs(days)
        
        while remaining > 0:
            current += timedelta(days=direction)
            if self.is_business_day(current):
                remaining -= 1
        
        return current
    
    def subtract_business_days(self, start_date: date, days: int) -> date:
        """
        减去工作日（等同于 add_business_days(start_date, -days)）
        """
        return self.add_business_days(start_date, -days)
    
    def business_days_between(self, start_date: date, end_date: date) -> int:
        """
        计算两个日期之间的工作日数量
        注意：不包含起始日期和结束日期
        
        优化：使用数学计算减少逐日迭代次数
        """
        if start_date > end_date:
            start_date, end_date = end_date, start_date
            negate = True
        else:
            negate = False
        
        # 计算总天数（不含首尾）
        total_days = (end_date - start_date).days - 1
        if total_days <= 0:
            return 0
        
        # 计算完整周数和剩余天数
        full_weeks = total_days // 7
        remaining_days = total_days % 7
        
        # 计算每个工作日在一周中出现的次数（用于快速估算）
        workdays_per_week = len(self.config.workdays)
        
        # 基础工作日数 = 完整周数 × 每周工作日数
        base_count = full_weeks * workdays_per_week
        
        # 处理剩余天数（逐日检查）
        current = start_date + timedelta(days=1 + full_weeks * 7)
        remaining_count = 0
        
        for _ in range(remaining_days):
            # 先检查是否为周末（快速判断）
            if current.weekday() in self.config.weekends:
                # 检查是否为调休工作日
                if self.is_adjusted_workday(current):
                    remaining_count += 1
            elif current.weekday() in self.config.workdays:
                # 检查是否为节假日
                is_hol, _ = self.is_holiday(current)
                if not is_hol:
                    remaining_count += 1
            current += timedelta(days=1)
        
        # 处理完整周期内的节假日和调休工作日
        # 需要检查完整周期内的特殊日期
        check_start = start_date + timedelta(days=1)
        check_end = start_date + timedelta(days=full_weeks * 7)
        
        adjustment = 0
        current_check = check_start
        while current_check <= check_end:
            weekday = current_check.weekday()
            if weekday in self.config.weekends:
                # 周末调休上班
                if self.is_adjusted_workday(current_check):
                    adjustment += 1
            elif weekday in self.config.workdays:
                # 工作日放假
                is_hol, _ = self.is_holiday(current_check)
                if is_hol:
                    adjustment -= 1
            current_check += timedelta(days=1)
        
        count = base_count + remaining_count + adjustment
        return -count if negate else count
    
    def business_days_inclusive(self, start_date: date, end_date: date) -> int:
        """
        计算两个日期之间的工作日数量（包含起始和结束日期）
        
        优化：使用数学计算减少逐日迭代次数
        """
        if start_date > end_date:
            start_date, end_date = end_date, start_date
            negate = True
        else:
            negate = False
        
        # 计算总天数（含首尾）
        total_days = (end_date - start_date).days + 1
        if total_days <= 0:
            return 0
        
        # 计算完整周数和剩余天数
        full_weeks = total_days // 7
        remaining_days = total_days % 7
        
        # 计算每个工作日在一周中出现的次数
        workdays_per_week = len(self.config.workdays)
        
        # 基础工作日数
        base_count = full_weeks * workdays_per_week
        
        # 处理剩余天数
        current = start_date + timedelta(days=full_weeks * 7)
        remaining_count = 0
        
        for _ in range(remaining_days):
            weekday = current.weekday()
            if weekday in self.config.weekends:
                if self.is_adjusted_workday(current):
                    remaining_count += 1
            elif weekday in self.config.workdays:
                is_hol, _ = self.is_holiday(current)
                if not is_hol:
                    remaining_count += 1
            current += timedelta(days=1)
        
        # 处理完整周期内的节假日和调休工作日
        check_start = start_date
        check_end = start_date + timedelta(days=full_weeks * 7 - 1)
        
        adjustment = 0
        current_check = check_start
        while current_check <= check_end:
            weekday = current_check.weekday()
            if weekday in self.config.weekends:
                if self.is_adjusted_workday(current_check):
                    adjustment += 1
            elif weekday in self.config.workdays:
                is_hol, _ = self.is_holiday(current_check)
                if is_hol:
                    adjustment -= 1
            current_check += timedelta(days=1)
        
        count = base_count + remaining_count + adjustment
        return -count if negate else count
    
    def next_business_day(self, from_date: date) -> date:
        """获取下一个工作日"""
        return self.add_business_days(from_date, 1)
    
    def previous_business_day(self, from_date: date) -> date:
        """获取上一个工作日"""
        return self.add_business_days(from_date, -1)
    
    def get_business_days_in_range(self, start_date: date, end_date: date) -> List[date]:
        """获取日期范围内的所有工作日"""
        if start_date > end_date:
            start_date, end_date = end_date, start_date
        
        business_days = []
        current = start_date
        
        while current <= end_date:
            if self.is_business_day(current):
                business_days.append(current)
            current += timedelta(days=1)
        
        return business_days
    
    def nth_business_day_of_month(self, year: int, month: int, n: int) -> Optional[date]:
        """
        获取某月的第n个工作日
        n: 1表示第一个工作日，-1表示最后一个工作日
        """
        if n == 0:
            return None
        
        if n > 0:
            # 正向查找
            current = date(year, month, 1)
            count = 0
            while current.month == month:
                if self.is_business_day(current):
                    count += 1
                    if count == n:
                        return current
                current += timedelta(days=1)
        else:
            # 反向查找
            _, last_day = calendar.monthrange(year, month)
            current = date(year, month, last_day)
            count = 0
            while current.month == month:
                if self.is_business_day(current):
                    count += 1
                    if count == -n:
                        return current
                current -= timedelta(days=1)
        
        return None
    
    def business_days_in_month(self, year: int, month: int) -> int:
        """计算某月的工作日数量"""
        _, last_day = calendar.monthrange(year, month)
        start = date(year, month, 1)
        end = date(year, month, last_day)
        return self.business_days_inclusive(start, end)
    
    def is_end_of_month_business_day(self, check_date: date) -> bool:
        """判断是否为月末最后一个工作日"""
        _, last_day = calendar.monthrange(check_date.year, check_date.month)
        end_of_month = date(check_date.year, check_date.month, last_day)
        
        # 从月末开始向前找最后一个工作日
        current = end_of_month
        while current.month == check_date.month:
            if self.is_business_day(current):
                return current == check_date
            current -= timedelta(days=1)
        
        return False
    
    def get_month_end_business_day(self, year: int, month: int) -> Optional[date]:
        """获取某月的最后一个工作日"""
        _, last_day = calendar.monthrange(year, month)
        current = date(year, month, last_day)
        
        while current.month == month:
            if self.is_business_day(current):
                return current
            current -= timedelta(days=1)
        
        return None
    
    def get_week_start_end(self, check_date: date) -> Tuple[date, date]:
        """
        获取某日期所在周的开始和结束日期（周一到周日）
        返回: (周一日期, 周日日期)
        """
        weekday = check_date.weekday()
        start = check_date - timedelta(days=weekday)
        end = start + timedelta(days=6)
        return start, end
    
    def business_days_in_week(self, check_date: date) -> List[date]:
        """获取某日期所在周的所有工作日"""
        start, end = self.get_week_start_end(check_date)
        return self.get_business_days_in_range(start, end)
    
    def get_next_n_business_days(self, start_date: date, n: int) -> List[date]:
        """获取接下来的n个工作日"""
        result = []
        current = start_date
        
        while len(result) < n:
            current += timedelta(days=1)
            if self.is_business_day(current):
                result.append(current)
        
        return result
    
    def get_previous_n_business_days(self, start_date: date, n: int) -> List[date]:
        """获取之前的n个工作日"""
        result = []
        current = start_date
        
        while len(result) < n:
            current -= timedelta(days=1)
            if self.is_business_day(current):
                result.append(current)
        
        return list(reversed(result))
    
    def find_next_business_day_matching(self, start_date: date, 
                                         condition: Callable[[date], bool]) -> Optional[date]:
        """
        查找下一个满足条件的工作日
        condition: 判断条件函数
        """
        current = start_date
        max_iterations = 365 * 2  # 最多查找两年
        iterations = 0
        
        while iterations < max_iterations:
            current += timedelta(days=1)
            if self.is_business_day(current) and condition(current):
                return current
            iterations += 1
        
        return None
    
    def get_holiday_info(self, check_date: date) -> Optional[Holiday]:
        """获取节假日信息"""
        for holiday in self.config.holidays:
            if holiday.matches(check_date):
                return holiday
        return None
    
    def list_holidays_in_range(self, start_date: date, end_date: date) -> List[Tuple[date, Holiday]]:
        """列出日期范围内的所有节假日"""
        if start_date > end_date:
            start_date, end_date = end_date, start_date
        
        holidays_in_range = []
        current = start_date
        
        while current <= end_date:
            holiday = self.get_holiday_info(current)
            if holiday:
                holidays_in_range.append((current, holiday))
            current += timedelta(days=1)
        
        return holidays_in_range


def create_china_holiday_calculator(year: int) -> BusinessDayCalculator:
    """
    创建中国节假日计算器（需要手动设置具体日期）
    注意：中国节假日每年不同，需要根据国务院公告设置
    """
    config = BusinessDayConfig()
    
    # 固定节假日（阳历）
    # 元旦
    config.add_holiday("元旦", date(year, 1, 1), is_recurring=True)
    # 劳动节
    config.add_holiday("劳动节", date(year, 5, 1), is_recurring=True)
    config.add_holiday("劳动节", date(year, 5, 2), is_recurring=True)
    config.add_holiday("劳动节", date(year, 5, 3), is_recurring=True)
    # 国庆节
    config.add_holiday("国庆节", date(year, 10, 1), is_recurring=True)
    config.add_holiday("国庆节", date(year, 10, 2), is_recurring=True)
    config.add_holiday("国庆节", date(year, 10, 3), is_recurring=True)
    
    # 注意：春节、清明、端午、中秋等农历节日需要根据具体年份设置
    # 建议使用 add_holiday 和 add_adjusted_workday 手动添加
    
    return BusinessDayCalculator(config)


def create_us_holiday_calculator(year: int) -> BusinessDayCalculator:
    """
    创建美国节假日计算器
    """
    config = BusinessDayConfig()
    
    # 固定日期节假日
    config.add_holiday("New Year's Day", date(year, 1, 1), is_recurring=True)
    config.add_holiday("Independence Day", date(year, 7, 4), is_recurring=True)
    config.add_holiday("Veterans Day", date(year, 11, 11), is_recurring=True)
    config.add_holiday("Christmas Day", date(year, 12, 25), is_recurring=True)
    
    # 计算浮动节假日
    # Martin Luther King Jr. Day - 1月第三个周一
    mlk_day = _nth_weekday_of_month(year, 1, 2, 3)  # 第3个周一
    config.add_holiday("MLK Day", mlk_day)
    
    # Presidents' Day - 2月第三个周一
    presidents_day = _nth_weekday_of_month(year, 2, 2, 3)
    config.add_holiday("Presidents' Day", presidents_day)
    
    # Memorial Day - 5月最后一个周一
    memorial_day = _last_weekday_of_month(year, 5, 2)
    config.add_holiday("Memorial Day", memorial_day)
    
    # Labor Day - 9月第一个周一
    labor_day = _nth_weekday_of_month(year, 9, 2, 1)
    config.add_holiday("Labor Day", labor_day)
    
    # Columbus Day - 10月第二个周一
    columbus_day = _nth_weekday_of_month(year, 10, 2, 2)
    config.add_holiday("Columbus Day", columbus_day)
    
    # Thanksgiving - 11月第四个周四
    thanksgiving = _nth_weekday_of_month(year, 11, 3, 4)
    config.add_holiday("Thanksgiving", thanksgiving)
    
    return BusinessDayCalculator(config)


def _nth_weekday_of_month(year: int, month: int, weekday: int, n: int) -> date:
    """
    计算某月第n个某星期几
    weekday: 0=周一, 6=周日
    n: 第几个（1-indexed）
    """
    first_day = date(year, month, 1)
    first_weekday = first_day.weekday()
    
    # 计算第一个目标weekday
    days_until_target = (weekday - first_weekday) % 7
    first_target = first_day + timedelta(days=days_until_target)
    
    # 加上 (n-1) 周
    return first_target + timedelta(weeks=n-1)


def _last_weekday_of_month(year: int, month: int, weekday: int) -> date:
    """
    计算某月最后一个某星期几
    weekday: 0=周一, 6=周日
    """
    _, last_day = calendar.monthrange(year, month)
    last_date = date(year, month, last_day)
    last_weekday = last_date.weekday()
    
    # 从月末往回找
    days_back = (last_weekday - weekday) % 7
    return last_date - timedelta(days=days_back)


# 便捷函数
def is_business_day(check_date: date, config: Optional[BusinessDayConfig] = None) -> bool:
    """判断是否为工作日（便捷函数）"""
    calc = BusinessDayCalculator(config)
    return calc.is_business_day(check_date)


def add_business_days(start_date: date, days: int, 
                      config: Optional[BusinessDayConfig] = None) -> date:
    """添加工作日（便捷函数）"""
    calc = BusinessDayCalculator(config)
    return calc.add_business_days(start_date, days)


def business_days_between(start_date: date, end_date: date,
                         config: Optional[BusinessDayConfig] = None) -> int:
    """计算工作日数量（便捷函数）"""
    calc = BusinessDayCalculator(config)
    return calc.business_days_between(start_date, end_date)


def next_business_day(from_date: date, config: Optional[BusinessDayConfig] = None) -> date:
    """获取下一个工作日（便捷函数）"""
    calc = BusinessDayCalculator(config)
    return calc.next_business_day(from_date)


def previous_business_day(from_date: date, config: Optional[BusinessDayConfig] = None) -> date:
    """获取上一个工作日（便捷函数）"""
    calc = BusinessDayCalculator(config)
    return calc.previous_business_day(from_date)