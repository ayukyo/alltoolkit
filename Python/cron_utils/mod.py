"""
Cron Utilities - Cron 表达式解析和计算工具

提供完整的 Cron 表达式解析、验证和下次执行时间计算，包括：
- 标准 Cron 表达式解析（5字段）
- 扩展 Cron 表达式解析（6字段，含秒）
- Quartz Cron 表达式解析（7字段）
- 下次/多次执行时间计算
- Cron 表达式验证
- Cron 表达式描述生成（人类可读）
- 特殊表达式支持（@yearly, @monthly, @weekly, @daily, @hourly）

零外部依赖，纯 Python 实现。
"""

from typing import List, Optional, Tuple, Set, Dict, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import re


class CronFieldType(Enum):
    """Cron 字段类型"""
    SECOND = "second"
    MINUTE = "minute"
    HOUR = "hour"
    DAY_OF_MONTH = "day_of_month"
    MONTH = "month"
    DAY_OF_WEEK = "day_of_week"
    YEAR = "year"


@dataclass
class CronField:
    """Cron 字段定义"""
    name: str
    min_value: int
    max_value: int
    field_type: CronFieldType


# 字段定义
CRON_FIELDS = {
    CronFieldType.SECOND: CronField("second", 0, 59, CronFieldType.SECOND),
    CronFieldType.MINUTE: CronField("minute", 0, 59, CronFieldType.MINUTE),
    CronFieldType.HOUR: CronField("hour", 0, 23, CronFieldType.HOUR),
    CronFieldType.DAY_OF_MONTH: CronField("day_of_month", 1, 31, CronFieldType.DAY_OF_MONTH),
    CronFieldType.MONTH: CronField("month", 1, 12, CronFieldType.MONTH),
    CronFieldType.DAY_OF_WEEK: CronField("day_of_week", 0, 6, CronFieldType.DAY_OF_WEEK),
    CronFieldType.YEAR: CronField("year", 1970, 2099, CronFieldType.YEAR),
}

# 月份名称映射
MONTH_NAMES = {
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
    'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
    'january': 1, 'february': 2, 'march': 3, 'april': 4,
    'may': 5, 'june': 6, 'july': 7, 'august': 8,
    'september': 9, 'october': 10, 'november': 11, 'december': 12,
}

# 星期名称映射
DAY_NAMES = {
    'sun': 0, 'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5, 'sat': 6,
    'sunday': 0, 'monday': 1, 'tuesday': 2, 'wednesday': 3,
    'thursday': 4, 'friday': 5, 'saturday': 6,
}

# 特殊表达式
SPECIAL_EXPRESSIONS = {
    '@yearly': '0 0 0 1 1 *',
    '@annually': '0 0 0 1 1 *',
    '@monthly': '0 0 0 1 * *',
    '@weekly': '0 0 0 * * 0',
    '@daily': '0 0 0 * * *',
    '@midnight': '0 0 0 * * *',
    '@hourly': '0 0 * * * *',
    '@every_minute': '0 * * * * *',
    '@every_second': '* * * * * *',
}


class CronParseError(Exception):
    """Cron 解析错误"""
    pass


class CronExpression:
    """
    Cron 表达式类
    
    支持：
    - 标准 5 字段：分 时 日 月 周
    - 扩展 6 字段：秒 分 时 日 月 周
    - Quartz 7 字段：秒 分 时 日 月 周 年
    - 特殊表达式：@yearly, @monthly, @weekly, @daily, @hourly
    
    字段格式：
    - * : 任意值
    - */n : 每 n 个单位
    - n-m : 范围
    - n,m,x : 列表
    - n-m/s : 范围内每 s 个单位
    """
    
    def __init__(self, expression: str):
        """
        初始化 Cron 表达式
        
        Args:
            expression: Cron 表达式字符串
        """
        self.original_expression = expression
        self.normalized_expression: str = ""
        self.field_values: Dict[CronFieldType, Set[int]] = {}
        self.has_seconds: bool = False
        self.has_year: bool = False
        
        self._parse(expression)
    
    def _parse(self, expression: str) -> None:
        """解析 Cron 表达式"""
        # 处理特殊表达式
        expression = expression.strip().lower()
        if expression in SPECIAL_EXPRESSIONS:
            expression = SPECIAL_EXPRESSIONS[expression]
        
        self.normalized_expression = expression
        
        # 分割字段
        fields = expression.split()
        
        if len(fields) < 5:
            raise CronParseError(f"无效的 Cron 表达式：至少需要 5 个字段，得到 {len(fields)} 个")
        
        if len(fields) > 7:
            raise CronParseError(f"无效的 Cron 表达式：最多 7 个字段，得到 {len(fields)} 个")
        
        # 确定字段映射
        if len(fields) == 5:
            # 标准：分 时 日 月 周
            field_order = [
                CronFieldType.MINUTE,
                CronFieldType.HOUR,
                CronFieldType.DAY_OF_MONTH,
                CronFieldType.MONTH,
                CronFieldType.DAY_OF_WEEK,
            ]
            self.has_seconds = False
            self.has_year = False
        elif len(fields) == 6:
            # 扩展：秒 分 时 日 月 周
            field_order = [
                CronFieldType.SECOND,
                CronFieldType.MINUTE,
                CronFieldType.HOUR,
                CronFieldType.DAY_OF_MONTH,
                CronFieldType.MONTH,
                CronFieldType.DAY_OF_WEEK,
            ]
            self.has_seconds = True
            self.has_year = False
        else:
            # Quartz：秒 分 时 日 月 周 年
            field_order = [
                CronFieldType.SECOND,
                CronFieldType.MINUTE,
                CronFieldType.HOUR,
                CronFieldType.DAY_OF_MONTH,
                CronFieldType.MONTH,
                CronFieldType.DAY_OF_WEEK,
                CronFieldType.YEAR,
            ]
            self.has_seconds = True
            self.has_year = True
        
        # 解析每个字段
        for i, field_type in enumerate(field_order):
            self.field_values[field_type] = self._parse_field(fields[i], field_type)
    
    def _parse_field(self, field: str, field_type: CronFieldType) -> Set[int]:
        """
        解析单个字段
        
        Args:
            field: 字段字符串
            field_type: 字段类型
            
        Returns:
            包含所有可能值的集合
        """
        field_def = CRON_FIELDS[field_type]
        values: Set[int] = set()
        
        # 处理多个部分（逗号分隔）
        parts = field.split(',')
        
        for part in parts:
            part = part.strip()
            values.update(self._parse_part(part, field_def))
        
        return values
    
    def _parse_part(self, part: str, field_def: CronField) -> Set[int]:
        """解析字段的一部分"""
        values: Set[int] = set()
        
        # 处理 */n 或 n-m/s 形式
        step = 1
        if '/' in part:
            part, step_str = part.split('/', 1)
            try:
                step = int(step_str)
            except ValueError:
                raise CronParseError(f"无效的步长值：{step_str}")
        
        # 处理 *
        if part == '*':
            values.update(range(field_def.min_value, field_def.max_value + 1, step))
            return values
        
        # 处理范围 n-m
        if '-' in part:
            range_parts = part.split('-', 1)
            try:
                start = self._parse_value(range_parts[0], field_def)
                end = self._parse_value(range_parts[1], field_def)
            except ValueError as e:
                raise CronParseError(f"无效的范围值：{part}") from e
            
            if start > end:
                raise CronParseError(f"无效的范围：起始值 {start} 大于结束值 {end}")
            
            values.update(range(start, end + 1, step))
        else:
            # 单个值
            try:
                value = self._parse_value(part, field_def)
            except ValueError as e:
                raise CronParseError(f"无效的值：{part}") from e
            
            if step == 1:
                values.add(value)
            else:
                # n/s 形式：从 n 开始每 s 个
                values.update(range(value, field_def.max_value + 1, step))
        
        # 验证值范围
        for v in values:
            if v < field_def.min_value or v > field_def.max_value:
                raise CronParseError(
                    f"值 {v} 超出 {field_def.name} 的有效范围 "
                    f"({field_def.min_value}-{field_def.max_value})"
                )
        
        return values
    
    def _parse_value(self, value: str, field_def: CronField) -> int:
        """解析单个值（支持名称和数字）"""
        value = value.strip().lower()
        
        # 处理月份名称
        if field_def.field_type == CronFieldType.MONTH:
            if value in MONTH_NAMES:
                return MONTH_NAMES[value]
        
        # 处理星期名称
        if field_def.field_type == CronFieldType.DAY_OF_WEEK:
            if value in DAY_NAMES:
                return DAY_NAMES[value]
        
        # 数字
        try:
            return int(value)
        except ValueError:
            raise CronParseError(f"无法解析值：{value}")
    
    def matches(self, dt: datetime) -> bool:
        """
        检查给定时间是否匹配 Cron 表达式
        
        Args:
            dt: 要检查的时间
            
        Returns:
            是否匹配
        """
        # 秒（如果定义了）
        if self.has_seconds:
            if dt.second not in self.field_values[CronFieldType.SECOND]:
                return False
        
        # 分
        if dt.minute not in self.field_values[CronFieldType.MINUTE]:
            return False
        
        # 时
        if dt.hour not in self.field_values[CronFieldType.HOUR]:
            return False
        
        # 日
        if dt.day not in self.field_values[CronFieldType.DAY_OF_MONTH]:
            # 检查是否是 "周" 触发
            if 0 not in self.field_values[CronFieldType.DAY_OF_MONTH]:
                return False
        
        # 月
        if dt.month not in self.field_values[CronFieldType.MONTH]:
            return False
        
        # 周
        if dt.weekday() not in self._adjust_weekday(self.field_values[CronFieldType.DAY_OF_WEEK]):
            # 检查是否是 "日" 触发
            if 0 not in self.field_values[CronFieldType.DAY_OF_WEEK]:
                return False
        
        # 年（如果定义了）
        if self.has_year:
            if dt.year not in self.field_values[CronFieldType.YEAR]:
                return False
        
        # 检查日和周的冲突（如果两者都指定了具体值）
        dom_values = self.field_values[CronFieldType.DAY_OF_MONTH]
        dow_values = self.field_values[CronFieldType.DAY_OF_WEEK]
        
        # 如果日和周都指定了（不是 *），需要特殊处理
        # 这里采用 "OR" 逻辑：满足任一条件即可
        # 这是 Quartz 风格的处理方式
        
        return True
    
    def _adjust_weekday(self, values: Set[int]) -> Set[int]:
        """
        调整星期值（Python weekday: 0=周一，Cron: 0=周日）
        
        Python: Mon=0, Tue=1, ..., Sun=6
        Cron:   Sun=0, Mon=1, ..., Sat=6
        """
        result = set()
        for v in values:
            if v == 0:  # Cron 周日 -> Python 周日 (6)
                result.add(6)
            else:
                result.add(v - 1)  # Cron Mon(1) -> Python Mon(0)
        return result
    
    def get_next_run(self, from_time: Optional[datetime] = None, max_days: int = 366) -> Optional[datetime]:
        """
        计算下次执行时间
        
        使用高效算法，直接跳到下一个可能的匹配时间。
        
        Args:
            from_time: 起始时间（默认当前时间）
            max_days: 最大搜索天数（防止无限循环）
            
        Returns:
            下次执行时间，如果没有则返回 None
        """
        if from_time is None:
            from_time = datetime.now()
        
        # 从下一秒/分钟开始
        if self.has_seconds:
            current = from_time.replace(microsecond=0) + timedelta(seconds=1)
        else:
            current = from_time.replace(second=0, microsecond=0) + timedelta(minutes=1)
        
        end_date = from_time + timedelta(days=max_days)
        
        while current <= end_date:
            # 快速跳转到下一个匹配的时间
            next_time = self._find_next_match(current)
            if next_time and next_time <= end_date:
                return next_time
            
            # 如果没有找到匹配，跳到下一天
            current = current.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        
        return None
    
    def _find_next_match(self, start: datetime) -> Optional[datetime]:
        """
        从给定时间开始，找到当天或之后最近的匹配时间
        
        Args:
            start: 起始时间
            
        Returns:
            匹配时间，如果没有则返回 None
        """
        # 获取当天允许的小时和分钟值
        allowed_hours = sorted(self.field_values[CronFieldType.HOUR])
        allowed_minutes = sorted(self.field_values[CronFieldType.MINUTE])
        
        if self.has_seconds:
            allowed_seconds = sorted(self.field_values[CronFieldType.SECOND])
        
        # 检查当天是否是有效的日期
        if not self._is_valid_date(start):
            return None
        
        # 找到当天最近的有效时间
        current_hour = start.hour
        current_minute = start.minute
        current_second = start.second if self.has_seconds else 0
        
        # 找到第一个大于或等于当前值的有效小时
        for hour in allowed_hours:
            if hour > current_hour:
                # 使用该小时的第一个有效分钟
                minute = allowed_minutes[0]
                if self.has_seconds:
                    second = allowed_seconds[0]
                    return start.replace(hour=hour, minute=minute, second=second)
                return start.replace(hour=hour, minute=minute, second=0)
            
            if hour == current_hour:
                # 在当前小时内找第一个有效分钟
                for minute in allowed_minutes:
                    if minute > current_minute:
                        if self.has_seconds:
                            second = allowed_seconds[0]
                            return start.replace(hour=hour, minute=minute, second=second)
                        return start.replace(hour=hour, minute=minute, second=0)
                    
                    if minute == current_minute:
                        if self.has_seconds:
                            # 在当前分钟内找第一个有效秒
                            for second in allowed_seconds:
                                if second >= current_second:
                                    result = start.replace(hour=hour, minute=minute, second=second)
                                    if self.matches(result):
                                        return result
                        else:
                            # 已经是当前分钟，检查是否匹配
                            result = start.replace(hour=hour, minute=minute, second=0)
                            if self.matches(result):
                                return result
        
        # 当天没有找到，返回 None（外层会跳到下一天）
        return None
    
    def _is_valid_date(self, dt: datetime) -> bool:
        """
        检查给定日期是否符合 Cron 表达式的日和月字段
        
        Args:
            dt: 日期时间
            
        Returns:
            是否有效
        """
        # 检查月份
        if dt.month not in self.field_values[CronFieldType.MONTH]:
            return False
        
        # 检查日期或星期
        dom_values = self.field_values[CronFieldType.DAY_OF_MONTH]
        dow_values = self.field_values[CronFieldType.DAY_OF_WEEK]
        
        # 如果两者都是 '*'（所有值），则有效
        dom_is_all = len(dom_values) == 31
        dow_is_all = len(dow_values) == 7
        
        if dom_is_all and dow_is_all:
            return True
        
        # 如果只有日期被指定
        if not dow_is_all and dom_is_all:
            # 检查星期
            adjusted_dow = self._adjust_weekday(dow_values)
            return dt.weekday() in adjusted_dow
        
        # 如果只有星期被指定
        if dow_is_all and not dom_is_all:
            # 检查日期
            try:
                if dt.day in dom_values:
                    return True
            except ValueError:
                pass
            return False
        
        # 如果两者都被指定，使用 OR 逻辑
        adjusted_dow = self._adjust_weekday(dow_values)
        if dt.weekday() in adjusted_dow:
            return True
        
        if dt.day in dom_values:
            return True
        
        return False
    
    def get_next_runs(self, count: int = 10, from_time: Optional[datetime] = None) -> List[datetime]:
        """
        计算多次执行时间
        
        Args:
            count: 计算次数
            from_time: 起始时间
            
        Returns:
            执行时间列表
        """
        runs: List[datetime] = []
        current = from_time
        
        for _ in range(count):
            next_run = self.get_next_run(current)
            if next_run is None:
                break
            runs.append(next_run)
            current = next_run
        
        return runs
    
    def get_description(self) -> str:
        """
        生成人类可读的描述
        
        Returns:
            描述字符串
        """
        parts: List[str] = []
        
        # 秒
        if self.has_seconds:
            seconds = self.field_values[CronFieldType.SECOND]
            parts.append(self._describe_field(seconds, 0, 59, "秒"))
        
        # 分
        minutes = self.field_values[CronFieldType.MINUTE]
        parts.append(self._describe_field(minutes, 0, 59, "分"))
        
        # 时
        hours = self.field_values[CronFieldType.HOUR]
        parts.append(self._describe_field(hours, 0, 23, "时"))
        
        # 日
        days = self.field_values[CronFieldType.DAY_OF_MONTH]
        dom_desc = self._describe_field(days, 1, 31, "日")
        if dom_desc != "每日":
            parts.append(dom_desc)
        
        # 月
        months = self.field_values[CronFieldType.MONTH]
        month_desc = self._describe_field(months, 1, 12, "月")
        if month_desc != "每月":
            parts.append(month_desc)
        
        # 周
        dow = self.field_values[CronFieldType.DAY_OF_WEEK]
        if len(dow) < 7:  # 不是所有天
            dow_desc = self._describe_weekday(dow)
            parts.append(dow_desc)
        
        return " ".join(parts)
    
    def _describe_field(self, values: Set[int], min_val: int, max_val: int, unit: str) -> str:
        """生成字段描述"""
        if len(values) == max_val - min_val + 1:
            return f"每{unit}"
        
        sorted_values = sorted(values)
        
        # 连续值
        if len(sorted_values) == 1:
            return f"第{sorted_values[0]}{unit}"
        
        # 检查是否是连续范围
        if sorted_values[-1] - sorted_values[0] == len(sorted_values) - 1:
            return f"第{sorted_values[0]}到{sorted_values[-1]}{unit}"
        
        # 列表值
        return f"第{','.join(map(str, sorted_values))}{unit}"
    
    def _describe_weekday(self, values: Set[int]) -> str:
        """生成星期描述"""
        weekday_names = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
        sorted_values = sorted(values)
        names = [weekday_names[v] for v in sorted_values]
        return f"每周{','.join(names)}"
    
    def __str__(self) -> str:
        return self.normalized_expression
    
    def __repr__(self) -> str:
        return f"CronExpression('{self.original_expression}')"


class CronValidator:
    """Cron 表达式验证器"""
    
    @staticmethod
    def validate(expression: str) -> Tuple[bool, Optional[str]]:
        """
        验证 Cron 表达式
        
        Args:
            expression: Cron 表达式
            
        Returns:
            (是否有效, 错误信息)
        """
        try:
            CronExpression(expression)
            return True, None
        except CronParseError as e:
            return False, str(e)
    
    @staticmethod
    def is_valid(expression: str) -> bool:
        """快速验证"""
        return CronValidator.validate(expression)[0]


class CronCalculator:
    """Cron 时间计算器"""
    
    @staticmethod
    def next_run(expression: str, from_time: Optional[datetime] = None) -> Optional[datetime]:
        """
        计算下次执行时间
        
        Args:
            expression: Cron 表达式
            from_time: 起始时间
            
        Returns:
            下次执行时间
        """
        cron = CronExpression(expression)
        return cron.get_next_run(from_time)
    
    @staticmethod
    def next_runs(expression: str, count: int = 10, from_time: Optional[datetime] = None) -> List[datetime]:
        """
        计算多次执行时间
        
        Args:
            expression: Cron 表达式
            count: 次数
            from_time: 起始时间
            
        Returns:
            执行时间列表
        """
        cron = CronExpression(expression)
        return cron.get_next_runs(count, from_time)
    
    @staticmethod
    def time_until_next(expression: str, from_time: Optional[datetime] = None) -> Optional[timedelta]:
        """
        计算距离下次执行的时间
        
        Args:
            expression: Cron 表达式
            from_time: 起始时间
            
        Returns:
            时间差
        """
        next_run = CronCalculator.next_run(expression, from_time)
        if next_run is None:
            return None
        
        from_time = from_time or datetime.now()
        return next_run - from_time


class CronScheduler:
    """
    Cron 调度器
    
    用于管理多个 Cron 任务
    """
    
    def __init__(self):
        """初始化调度器"""
        self._jobs: Dict[str, CronExpression] = {}
    
    def add_job(self, name: str, expression: str) -> None:
        """
        添加任务
        
        Args:
            name: 任务名称
            expression: Cron 表达式
        """
        self._jobs[name] = CronExpression(expression)
    
    def remove_job(self, name: str) -> bool:
        """
        移除任务
        
        Args:
            name: 任务名称
            
        Returns:
            是否成功移除
        """
        if name in self._jobs:
            del self._jobs[name]
            return True
        return False
    
    def get_jobs(self) -> List[str]:
        """获取所有任务名称"""
        return list(self._jobs.keys())
    
    def get_next_run(self, name: str, from_time: Optional[datetime] = None) -> Optional[datetime]:
        """获取指定任务的下次执行时间"""
        if name not in self._jobs:
            return None
        return self._jobs[name].get_next_run(from_time)
    
    def get_due_jobs(self, at_time: Optional[datetime] = None) -> List[str]:
        """
        获取到时应执行的任务
        
        Args:
            at_time: 检查时间（默认当前时间）
            
        Returns:
            到时的任务名称列表
        """
        if at_time is None:
            at_time = datetime.now()
        
        due_jobs = []
        for name, cron in self._jobs.items():
            if cron.matches(at_time):
                due_jobs.append(name)
        
        return due_jobs
    
    def get_schedule(self, hours: int = 24, from_time: Optional[datetime] = None) -> Dict[str, List[datetime]]:
        """
        获取未来一段时间内的调度表
        
        Args:
            hours: 小时数
            from_time: 起始时间
            
        Returns:
            {任务名: 执行时间列表}
        """
        if from_time is None:
            from_time = datetime.now()
        
        end_time = from_time + timedelta(hours=hours)
        
        schedule: Dict[str, List[datetime]] = {}
        for name, cron in self._jobs.items():
            runs = []
            current = from_time
            while True:
                next_run = cron.get_next_run(current)
                if next_run is None or next_run > end_time:
                    break
                runs.append(next_run)
                current = next_run
            if runs:
                schedule[name] = runs
        
        return schedule


# 便捷函数
def parse(expression: str) -> CronExpression:
    """解析 Cron 表达式"""
    return CronExpression(expression)


def validate(expression: str) -> Tuple[bool, Optional[str]]:
    """验证 Cron 表达式"""
    return CronValidator.validate(expression)


def is_valid(expression: str) -> bool:
    """检查 Cron 表达式是否有效"""
    return CronValidator.is_valid(expression)


def next_run(expression: str, from_time: Optional[datetime] = None) -> Optional[datetime]:
    """计算下次执行时间"""
    return CronCalculator.next_run(expression, from_time)


def next_runs(expression: str, count: int = 10, from_time: Optional[datetime] = None) -> List[datetime]:
    """计算多次执行时间"""
    return CronCalculator.next_runs(expression, count, from_time)


def describe(expression: str) -> str:
    """生成人类可读描述"""
    return CronExpression(expression).get_description()


if __name__ == "__main__":
    # 演示
    print("=== Cron 工具演示 ===\n")
    
    # 测试各种表达式
    expressions = [
        "* * * * *",           # 每分钟
        "0 * * * *",           # 每小时
        "0 0 * * *",           # 每天午夜
        "0 9 * * 1-5",         # 工作日早上9点
        "0 0 1 * *",           # 每月1号
        "*/15 * * * *",        # 每15分钟
        "0 0 0 1 1 *",         # 每年1月1日（6字段）
        "@hourly",             # 每小时
        "@daily",              # 每天
        "0 30 14 * * *",       # 每天14:30（6字段）
    ]
    
    for expr in expressions:
        print(f"表达式: {expr}")
        
        try:
            cron = CronExpression(expr)
            print(f"  描述: {cron.get_description()}")
            print(f"  下次执行: {cron.get_next_run()}")
            
            # 显示接下来3次
            runs = cron.get_next_runs(3)
            if runs:
                print(f"  接下来3次: {[r.strftime('%Y-%m-%d %H:%M:%S') for r in runs]}")
        except CronParseError as e:
            print(f"  错误: {e}")
        
        print()