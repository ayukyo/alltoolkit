"""
Vesting Schedule Utilities - 股权归属计划计算工具

A comprehensive vesting schedule calculator for stock options and RSUs.
零外部依赖，生产就绪。

Features:
    - 多种归属方式：线性、阶梯、即时
    - Cliff 期支持
    - 按月/季度/年归属
    - 已归属份额计算
    - 归属日历生成
    - 加速归属计算
    - 归属事件预测
"""

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import List, Dict, Optional, Tuple
from enum import Enum
import calendar


class VestingType(Enum):
    """归属类型"""
    LINEAR = "linear"          # 线性归属（按月/季度平均归属）
    CLIFF = "cliff"             # Cliff后一次性归属
    GRADED = "graded"           # 阶梯归属（逐年递增）
    IMMEDIATE = "immediate"     # 即时归属


class VestingFrequency(Enum):
    """归属频率"""
    MONTHLY = "monthly"         # 按月
    QUARTERLY = "quarterly"     # 按季度
    SEMI_ANNUAL = "semi_annual" # 每半年
    ANNUALLY = "annually"       # 每年


@dataclass
class VestingEvent:
    """单个归属事件"""
    date: date                          # 归属日期
    shares: int                         # 归属份额
    percentage: float                   # 归属比例（0-100）
    is_cliff: bool = False              # 是否为Cliff归属
    description: str = ""               # 描述


@dataclass
class VestingSchedule:
    """归属计划"""
    total_shares: int                           # 总份额
    grant_date: date                            # 授予日期
    vesting_type: VestingType                   # 归属类型
    vesting_period_months: int                  # 归属周期（月）
    cliff_months: int = 0                       # Cliff期（月）
    cliff_percentage: float = 0.0               # Cliff归属比例
    frequency: VestingFrequency = VestingFrequency.MONTHLY
    graded_schedule: List[Tuple[int, float]] = field(default_factory=list)  # 阶梯归属计划 [(年, 比例)]
    
    def __post_init__(self):
        """初始化后验证"""
        if self.vesting_period_months < 0:
            raise ValueError("归属周期不能为负数")
        if self.vesting_type != VestingType.IMMEDIATE and self.vesting_period_months <= 0:
            raise ValueError("归属周期必须大于0（即时归属除外）")
        if self.total_shares <= 0:
            raise ValueError("总份额必须大于0")
        if self.cliff_months < 0:
            raise ValueError("Cliff期不能为负数")
        if self.cliff_months >= self.vesting_period_months and self.vesting_type != VestingType.CLIFF and self.vesting_type != VestingType.IMMEDIATE:
            raise ValueError("Cliff期不能大于等于归属周期")


@dataclass
class VestingStatus:
    """归属状态"""
    vested_shares: int                          # 已归属份额
    unvested_shares: int                        # 未归属份额
    vested_percentage: float                    # 已归属比例
    next_vesting_date: Optional[date]           # 下次归属日期
    next_vesting_shares: int                    # 下次归属份额
    remaining_months: int                       # 剩余归属月数
    is_fully_vested: bool                       # 是否完全归属
    vesting_events: List[VestingEvent] = field(default_factory=list)


def calculate_vesting_schedule(schedule: VestingSchedule) -> List[VestingEvent]:
    """
    计算完整的归属事件列表
    
    Args:
        schedule: 归属计划
        
    Returns:
        归属事件列表
    """
    events = []
    
    if schedule.vesting_type == VestingType.IMMEDIATE:
        # 即时归属
        events.append(VestingEvent(
            date=schedule.grant_date,
            shares=schedule.total_shares,
            percentage=100.0,
            is_cliff=False,
            description="即时归属"
        ))
        return events
    
    elif schedule.vesting_type == VestingType.CLIFF:
        # Cliff后一次性归属
        cliff_date = add_months(schedule.grant_date, schedule.cliff_months)
        events.append(VestingEvent(
            date=cliff_date,
            shares=schedule.total_shares,
            percentage=100.0,
            is_cliff=True,
            description=f"Cliff期满归属（{schedule.cliff_months}个月）"
        ))
        return events
    
    elif schedule.vesting_type == VestingType.GRADED:
        # 阶梯归属
        return _calculate_graded_vesting(schedule)
    
    else:
        # 线性归属
        return _calculate_linear_vesting(schedule)


def _calculate_linear_vesting(schedule: VestingSchedule) -> List[VestingEvent]:
    """计算线性归属事件"""
    events = []
    
    # 如果有Cliff期
    if schedule.cliff_months > 0:
        cliff_date = add_months(schedule.grant_date, schedule.cliff_months)
        cliff_shares = int(schedule.total_shares * schedule.cliff_percentage / 100)
        
        if cliff_shares > 0:
            events.append(VestingEvent(
                date=cliff_date,
                shares=cliff_shares,
                percentage=schedule.cliff_percentage,
                is_cliff=True,
                description=f"Cliff归属（{schedule.cliff_percentage}%）"
            ))
    
    # 计算归属间隔
    if schedule.frequency == VestingFrequency.MONTHLY:
        interval = 1
    elif schedule.frequency == VestingFrequency.QUARTERLY:
        interval = 3
    elif schedule.frequency == VestingFrequency.SEMI_ANNUAL:
        interval = 6
    else:  # ANNUALLY
        interval = 12
    
    # 计算总归属次数
    total_intervals = schedule.vesting_period_months // interval
    
    # Cliff后的剩余份额
    cliff_shares = int(schedule.total_shares * schedule.cliff_percentage / 100) if schedule.cliff_months > 0 else 0
    remaining_shares = schedule.total_shares - cliff_shares
    remaining_percentage = 100.0 - schedule.cliff_percentage if schedule.cliff_months > 0 else 100.0
    
    # Cliff后的归属次数
    intervals_after_cliff = (schedule.vesting_period_months - schedule.cliff_months) // interval
    
    if intervals_after_cliff <= 0:
        return events
    
    # 每次归属的份额
    shares_per_interval = remaining_shares / intervals_after_cliff
    percentage_per_interval = remaining_percentage / intervals_after_cliff
    
    # 生成归属事件
    # 无Cliff时，第一次归属在授予日期后interval个月
    # 有Cliff时，第一次归属在Cliff日期后interval个月
    if schedule.cliff_months > 0:
        current_date = add_months(schedule.grant_date, schedule.cliff_months + interval)
    else:
        current_date = add_months(schedule.grant_date, interval)
    
    accumulated_shares = cliff_shares
    accumulated_percentage = schedule.cliff_percentage if schedule.cliff_months > 0 else 0.0
    
    for i in range(intervals_after_cliff):
        # 最后一次归属处理余数
        if i == intervals_after_cliff - 1:
            event_shares = schedule.total_shares - accumulated_shares
            event_percentage = 100.0 - accumulated_percentage
        else:
            event_shares = int(shares_per_interval)
            event_percentage = round(percentage_per_interval, 2)
            accumulated_shares += event_shares
            accumulated_percentage += event_percentage
        
        if event_shares > 0:
            events.append(VestingEvent(
                date=current_date,
                shares=event_shares,
                percentage=event_percentage,
                is_cliff=False,
                description=f"第{i+1}次归属"
            ))
        
        current_date = add_months(current_date, interval)
    
    return events


def _calculate_graded_vesting(schedule: VestingSchedule) -> List[VestingEvent]:
    """计算阶梯归属事件"""
    events = []
    
    if not schedule.graded_schedule:
        # 默认阶梯计划：25%, 25%, 25%, 25%
        schedule.graded_schedule = [(1, 25), (2, 25), (3, 25), (4, 25)]
    
    accumulated_shares = 0
    accumulated_percentage = 0.0
    
    for year, percentage in schedule.graded_schedule:
        vest_date = add_months(schedule.grant_date, year * 12)
        shares = int(schedule.total_shares * percentage / 100)
        
        # 最后一年处理余数
        if year == schedule.graded_schedule[-1][0]:
            shares = schedule.total_shares - accumulated_shares
            percentage = 100.0 - accumulated_percentage
        
        events.append(VestingEvent(
            date=vest_date,
            shares=shares,
            percentage=percentage,
            is_cliff=(year == 1 and schedule.cliff_months > 0),
            description=f"第{year}年归属（{percentage}%）"
        ))
        
        accumulated_shares += shares
        accumulated_percentage += percentage
    
    return events


def get_vesting_status(schedule: VestingSchedule, as_of_date: Optional[date] = None) -> VestingStatus:
    """
    获取指定日期的归属状态
    
    Args:
        schedule: 归属计划
        as_of_date: 计算日期，默认为今天
        
    Returns:
        归属状态
    """
    if as_of_date is None:
        as_of_date = date.today()
    
    events = calculate_vesting_schedule(schedule)
    
    vested_shares = 0
    vested_percentage = 0.0
    next_vesting_date = None
    next_vesting_shares = 0
    
    for event in events:
        if event.date <= as_of_date:
            vested_shares += event.shares
            vested_percentage += event.percentage
        else:
            if next_vesting_date is None:
                next_vesting_date = event.date
                next_vesting_shares = event.shares
    
    # 确保不超过总额
    vested_shares = min(vested_shares, schedule.total_shares)
    vested_percentage = min(round(vested_percentage, 2), 100.0)
    
    unvested_shares = schedule.total_shares - vested_shares
    is_fully_vested = vested_shares >= schedule.total_shares
    
    # 计算剩余月数
    vest_end_date = add_months(schedule.grant_date, schedule.vesting_period_months)
    if as_of_date >= vest_end_date:
        remaining_months = 0
    else:
        remaining_months = months_between(as_of_date, vest_end_date)
    
    return VestingStatus(
        vested_shares=vested_shares,
        unvested_shares=unvested_shares,
        vested_percentage=vested_percentage,
        next_vesting_date=next_vesting_date,
        next_vesting_shares=next_vesting_shares,
        remaining_months=remaining_months,
        is_fully_vested=is_fully_vested,
        vesting_events=events
    )


def add_months(start_date: date, months: int) -> date:
    """
    日期加月份（正确处理月末）
    
    Args:
        start_date: 起始日期
        months: 增加的月数
        
    Returns:
        新日期
    """
    if months == 0:
        return start_date
    
    year = start_date.year
    month = start_date.month + months
    
    # 处理年份进位
    while month > 12:
        year += 1
        month -= 12
    while month < 1:
        year -= 1
        month += 12
    
    # 处理月末
    day = start_date.day
    last_day = calendar.monthrange(year, month)[1]
    if day > last_day:
        day = last_day
    
    return date(year, month, day)


def months_between(start_date: date, end_date: date) -> int:
    """
    计算两个日期之间的月数
    
    Args:
        start_date: 起始日期
        end_date: 结束日期
        
    Returns:
        月数
    """
    if end_date <= start_date:
        return 0
    
    months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    
    # 如果结束日期的日小于起始日期的日，减去一个月
    if end_date.day < start_date.day:
        months -= 1
    
    return max(0, months)


def calculate_accelerated_vesting(
    schedule: VestingSchedule,
    acceleration_percentage: float,
    as_of_date: Optional[date] = None
) -> Tuple[int, List[VestingEvent]]:
    """
    计算加速归属
    
    Args:
        schedule: 归属计划
        acceleration_percentage: 加速比例（0-100）
        as_of_date: 计算日期，默认为今天
        
    Returns:
        (加速归属份额, 加速归属事件列表)
    """
    if as_of_date is None:
        as_of_date = date.today()
    
    status = get_vesting_status(schedule, as_of_date)
    
    # 计算可加速的份额
    accelerable_shares = status.unvested_shares
    accelerated_shares = int(accelerable_shares * acceleration_percentage / 100)
    
    # 生成加速归属事件
    events = []
    if accelerated_shares > 0:
        events.append(VestingEvent(
            date=as_of_date,
            shares=accelerated_shares,
            percentage=round(acceleration_percentage * status.unvested_shares / schedule.total_shares, 2),
            is_cliff=False,
            description=f"加速归属（{acceleration_percentage}%）"
        ))
    
    return accelerated_shares, events


def generate_vesting_calendar(
    schedule: VestingSchedule,
    year: Optional[int] = None
) -> Dict[int, List[VestingEvent]]:
    """
    生成指定年份的归属日历
    
    Args:
        schedule: 归属计划
        year: 年份，默认为当前年
        
    Returns:
        月份到归属事件的映射 {月份: [归属事件]}
    """
    if year is None:
        year = date.today().year
    
    events = calculate_vesting_schedule(schedule)
    calendar_events = {}
    
    for event in events:
        if event.date.year == year:
            month = event.date.month
            if month not in calendar_events:
                calendar_events[month] = []
            calendar_events[month].append(event)
    
    return calendar_events


def estimate_vesting_value(
    schedule: VestingSchedule,
    price_per_share: float,
    as_of_date: Optional[date] = None
) -> Dict[str, float]:
    """
    估算归属价值
    
    Args:
        schedule: 归属计划
        price_per_share: 每股价格
        as_of_date: 计算日期，默认为今天
        
    Returns:
        价值估算字典
    """
    status = get_vesting_status(schedule, as_of_date)
    
    vested_value = status.vested_shares * price_per_share
    unvested_value = status.unvested_shares * price_per_share
    total_value = schedule.total_shares * price_per_share
    
    return {
        "vested_value": vested_value,
        "unvested_value": unvested_value,
        "total_value": total_value,
        "price_per_share": price_per_share,
        "vested_shares": status.vested_shares,
        "unvested_shares": status.unvested_shares,
        "total_shares": schedule.total_shares,
        "vested_percentage": status.vested_percentage
    }


def create_standard_schedule(
    total_shares: int,
    grant_date: date,
    vesting_years: int = 4,
    cliff_years: int = 1,
    cliff_percentage: float = 25.0,
    frequency: VestingFrequency = VestingFrequency.MONTHLY
) -> VestingSchedule:
    """
    创建标准的4年归属计划（硅谷标准）
    
    Args:
        total_shares: 总份额
        grant_date: 授予日期
        vesting_years: 归属年限（默认4年）
        cliff_years: Cliff年限（默认1年）
        cliff_percentage: Cliff归属比例（默认25%）
        frequency: 归属频率（默认按月）
        
    Returns:
        归属计划
    """
    return VestingSchedule(
        total_shares=total_shares,
        grant_date=grant_date,
        vesting_type=VestingType.LINEAR,
        vesting_period_months=vesting_years * 12,
        cliff_months=cliff_years * 12,
        cliff_percentage=cliff_percentage,
        frequency=frequency
    )


def create_backloaded_schedule(
    total_shares: int,
    grant_date: date,
    schedule: List[Tuple[int, float]] = None
) -> VestingSchedule:
    """
    创建后置归属计划（逐年递增）
    
    Args:
        total_shares: 总份额
        grant_date: 授予日期
        schedule: 阶梯计划 [(年, 比例)]，默认为 10%, 20%, 30%, 40%
        
    Returns:
        归属计划
    """
    if schedule is None:
        schedule = [(1, 10), (2, 20), (3, 30), (4, 40)]
    
    total_years = max(year for year, _ in schedule)
    
    return VestingSchedule(
        total_shares=total_shares,
        grant_date=grant_date,
        vesting_type=VestingType.GRADED,
        vesting_period_months=total_years * 12,
        graded_schedule=schedule
    )


def calculate_vesting_summary(schedule: VestingSchedule, as_of_date: Optional[date] = None) -> Dict:
    """
    生成归属摘要报告
    
    Args:
        schedule: 归属计划
        as_of_date: 计算日期，默认为今天
        
    Returns:
        摘要字典
    """
    status = get_vesting_status(schedule, as_of_date)
    
    return {
        "grant_date": schedule.grant_date.isoformat(),
        "total_shares": schedule.total_shares,
        "vesting_type": schedule.vesting_type.value,
        "vesting_period_months": schedule.vesting_period_months,
        "cliff_months": schedule.cliff_months,
        "frequency": schedule.frequency.value,
        "as_of_date": (as_of_date or date.today()).isoformat(),
        "vested_shares": status.vested_shares,
        "unvested_shares": status.unvested_shares,
        "vested_percentage": status.vested_percentage,
        "next_vesting_date": status.next_vesting_date.isoformat() if status.next_vesting_date else None,
        "next_vesting_shares": status.next_vesting_shares,
        "remaining_months": status.remaining_months,
        "is_fully_vested": status.is_fully_vested,
        "total_events": len(status.vesting_events)
    }


def days_until_next_vesting(schedule: VestingSchedule, as_of_date: Optional[date] = None) -> int:
    """
    计算距离下次归属的天数
    
    Args:
        schedule: 归属计划
        as_of_date: 计算日期，默认为今天
        
    Returns:
        天数（如果已完全归属返回-1）
    """
    status = get_vesting_status(schedule, as_of_date)
    
    if status.is_fully_vested or status.next_vesting_date is None:
        return -1
    
    if as_of_date is None:
        as_of_date = date.today()
    
    return (status.next_vesting_date - as_of_date).days


def format_vesting_event(event: VestingEvent) -> str:
    """
    格式化归属事件为可读字符串
    
    Args:
        event: 归属事件
        
    Returns:
        格式化字符串
    """
    cliff_marker = " [CLIFF]" if event.is_cliff else ""
    return f"{event.date.strftime('%Y-%m-%d')}: {event.shares:,} 股 ({event.percentage:.2f}%){cliff_marker} - {event.description}"


def get_vesting_timeline(schedule: VestingSchedule) -> str:
    """
    生成归属时间线文本
    
    Args:
        schedule: 归属计划
        
    Returns:
        时间线文本
    """
    events = calculate_vesting_schedule(schedule)
    lines = [
        f"归属计划时间线",
        f"{'='*50}",
        f"授予日期: {schedule.grant_date}",
        f"总份额: {schedule.total_shares:,}",
        f"归属类型: {schedule.vesting_type.value}",
        f"归属周期: {schedule.vesting_period_months} 个月",
        f"归属频率: {schedule.frequency.value}",
    ]
    
    if schedule.cliff_months > 0:
        lines.append(f"Cliff期: {schedule.cliff_months} 个月 ({schedule.cliff_percentage}%)")
    
    lines.append(f"\n归属事件 ({len(events)} 次):")
    lines.append("-" * 50)
    
    accumulated_shares = 0
    accumulated_percentage = 0.0
    
    for event in events:
        accumulated_shares += event.shares
        accumulated_percentage += event.percentage
        lines.append(format_vesting_event(event))
        lines.append(f"    累计: {accumulated_shares:,} 股 ({accumulated_percentage:.2f}%)")
    
    return "\n".join(lines)