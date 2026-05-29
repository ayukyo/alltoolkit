"""
储蓄目标追踪工具 (Savings Goal Tracker)

提供储蓄目标管理、进度追踪、时间预测、复利计算等功能。
零依赖，仅使用 Python 标准库。

功能：
- 创建和管理储蓄目标
- 追踪储蓄进度
- 计算达成目标所需时间
- 支持简单利息和复利计算
- 提供储蓄建议
- 生成进度报告
- 支持多目标管理
"""

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict, Tuple, Union
from enum import Enum
import math


class GoalStatus(Enum):
    """目标状态"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    ON_TRACK = "on_track"
    BEHIND = "behind"
    AHEAD = "ahead"
    COMPLETED = "completed"
    PAUSED = "paused"


class Frequency(Enum):
    """储蓄频率"""
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


@dataclass
class SavingsGoal:
    """储蓄目标"""
    name: str
    target_amount: float
    current_amount: float = 0.0
    target_date: Optional[date] = None
    start_date: date = field(default_factory=date.today)
    description: str = ""
    category: str = "general"
    priority: int = 1  # 1-5, 5最高
    interest_rate: float = 0.0  # 年利率（小数形式，如 0.05 = 5%）
    compounding_frequency: int = 12  # 每年复利次数
    
    def __post_init__(self):
        if self.current_amount < 0:
            raise ValueError("当前金额不能为负数")
        if self.target_amount <= 0:
            raise ValueError("目标金额必须大于0")
        if self.target_date and self.target_date <= self.start_date:
            raise ValueError("目标日期必须晚于开始日期")
    
    @property
    def progress_percentage(self) -> float:
        """进度百分比"""
        return min(100.0, (self.current_amount / self.target_amount) * 100)
    
    @property
    def remaining_amount(self) -> float:
        """剩余金额"""
        return max(0.0, self.target_amount - self.current_amount)
    
    @property
    def is_completed(self) -> bool:
        """是否已完成"""
        return self.current_amount >= self.target_amount
    
    @property
    def days_elapsed(self) -> int:
        """已过天数"""
        return (date.today() - self.start_date).days
    
    @property
    def days_remaining(self) -> Optional[int]:
        """剩余天数（如果有目标日期）"""
        if self.target_date:
            return max(0, (self.target_date - date.today()).days)
        return None
    
    @property
    def total_days(self) -> Optional[int]:
        """总天数（如果有目标日期）"""
        if self.target_date:
            return (self.target_date - self.start_date).days
        return None
    
    @property
    def expected_progress(self) -> Optional[float]:
        """预期进度（基于时间）"""
        if self.target_date:
            total = self.total_days
            elapsed = self.days_elapsed
            if total and total > 0:
                return min(100.0, (elapsed / total) * 100)
        return None
    
    @property
    def status(self) -> GoalStatus:
        """获取目标状态"""
        if self.is_completed:
            return GoalStatus.COMPLETED
        
        expected = self.expected_progress
        if expected is None:
            if self.current_amount > 0:
                return GoalStatus.IN_PROGRESS
            return GoalStatus.NOT_STARTED
        
        actual = self.progress_percentage
        
        if actual >= expected + 10:
            return GoalStatus.AHEAD
        elif actual >= expected - 10:
            return GoalStatus.ON_TRACK
        else:
            return GoalStatus.BEHIND
    
    def add_savings(self, amount: float, apply_interest: bool = True) -> float:
        """
        添加储蓄
        
        Args:
            amount: 储蓄金额
            apply_interest: 是否应用利息
            
        Returns:
            更新后的当前金额
        """
        if amount < 0:
            raise ValueError("储蓄金额不能为负数")
        
        self.current_amount += amount
        
        if apply_interest and self.interest_rate > 0:
            # 应用复利（简化：假设每次添加时计算）
            days = self.days_elapsed
            if days > 0:
                years = days / 365.25
                n = self.compounding_frequency
                interest = self.current_amount * ((1 + self.interest_rate / n) ** (n * years) - 1)
                self.current_amount += interest
        
        return self.current_amount
    
    def withdraw(self, amount: float) -> float:
        """
        提取金额
        
        Args:
            amount: 提取金额
            
        Returns:
            更新后的当前金额
        """
        if amount < 0:
            raise ValueError("提取金额不能为负数")
        if amount > self.current_amount:
            raise ValueError("提取金额不能超过当前金额")
        
        self.current_amount -= amount
        return self.current_amount
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "name": self.name,
            "target_amount": self.target_amount,
            "current_amount": self.current_amount,
            "target_date": self.target_date.isoformat() if self.target_date else None,
            "start_date": self.start_date.isoformat(),
            "description": self.description,
            "category": self.category,
            "priority": self.priority,
            "interest_rate": self.interest_rate,
            "compounding_frequency": self.compounding_frequency,
        }


class SavingsGoalManager:
    """储蓄目标管理器"""
    
    def __init__(self):
        self.goals: List[SavingsGoal] = []
    
    def add_goal(self, goal: SavingsGoal) -> None:
        """添加目标"""
        self.goals.append(goal)
    
    def create_goal(
        self,
        name: str,
        target_amount: float,
        current_amount: float = 0.0,
        target_date: Optional[date] = None,
        **kwargs
    ) -> SavingsGoal:
        """创建并添加目标"""
        goal = SavingsGoal(
            name=name,
            target_amount=target_amount,
            current_amount=current_amount,
            target_date=target_date,
            **kwargs
        )
        self.add_goal(goal)
        return goal
    
    def remove_goal(self, name: str) -> bool:
        """移除目标"""
        for i, goal in enumerate(self.goals):
            if goal.name == name:
                self.goals.pop(i)
                return True
        return False
    
    def get_goal(self, name: str) -> Optional[SavingsGoal]:
        """获取目标"""
        for goal in self.goals:
            if goal.name == name:
                return goal
        return None
    
    def get_goals_by_status(self, status: GoalStatus) -> List[SavingsGoal]:
        """按状态获取目标"""
        return [g for g in self.goals if g.status == status]
    
    def get_goals_by_category(self, category: str) -> List[SavingsGoal]:
        """按类别获取目标"""
        return [g for g in self.goals if g.category == category]
    
    @property
    def total_target(self) -> float:
        """所有目标总金额"""
        return sum(g.target_amount for g in self.goals)
    
    @property
    def total_saved(self) -> float:
        """已储蓄总金额"""
        return sum(g.current_amount for g in self.goals)
    
    @property
    def total_remaining(self) -> float:
        """剩余总金额"""
        return sum(g.remaining_amount for g in self.goals)
    
    @property
    def overall_progress(self) -> float:
        """总体进度"""
        total_target = self.total_target
        if total_target == 0:
            return 0.0
        return (self.total_saved / total_target) * 100
    
    @property
    def completed_goals(self) -> List[SavingsGoal]:
        """已完成的目标"""
        return [g for g in self.goals if g.is_completed]
    
    @property
    def active_goals(self) -> List[SavingsGoal]:
        """进行中的目标"""
        return [g for g in self.goals if not g.is_completed]


def calculate_time_to_goal(
    target_amount: float,
    current_amount: float,
    savings_per_period: float,
    frequency: Frequency = Frequency.MONTHLY,
    interest_rate: float = 0.0,
    compounding_frequency: int = 12
) -> Optional[int]:
    """
    计算达成目标所需时间
    
    Args:
        target_amount: 目标金额
        current_amount: 当前金额
        savings_per_period: 每期储蓄金额
        frequency: 储蓄频率
        interest_rate: 年利率
        compounding_frequency: 每年复利次数
        
    Returns:
        所需周期数，如果无法达成返回 None
    """
    if savings_per_period <= 0:
        return None
    
    remaining = target_amount - current_amount
    if remaining <= 0:
        return 0
    
    if interest_rate <= 0:
        # 无利息，简单计算
        periods = math.ceil(remaining / savings_per_period)
        return periods
    
    # 有复利的情况
    # 使用数值方法求解
    r = interest_rate / compounding_frequency
    periods_per_year = {
        Frequency.DAILY: 365,
        Frequency.WEEKLY: 52,
        Frequency.BIWEEKLY: 26,
        Frequency.MONTHLY: 12,
        Frequency.QUARTERLY: 4,
        Frequency.YEARLY: 1,
    }
    
    periods_per_deposit = periods_per_year[frequency] / compounding_frequency
    
    # 简化计算：假设利息在每个复利周期末计算
    amount = current_amount
    periods = 0
    max_periods = 1000  # 防止无限循环
    
    while amount < target_amount and periods < max_periods:
        # 添加储蓄
        amount += savings_per_period
        periods += 1
        
        # 每个复利周期计算利息
        if periods % int(periods_per_deposit) == 0 and periods > 0:
            amount *= (1 + r)
    
    return periods if amount >= target_amount else None


def calculate_required_savings(
    target_amount: float,
    current_amount: float,
    target_date: date,
    start_date: date = None,
    frequency: Frequency = Frequency.MONTHLY,
    interest_rate: float = 0.0
) -> float:
    """
    计算达成目标所需的每期储蓄金额
    
    Args:
        target_amount: 目标金额
        current_amount: 当前金额
        target_date: 目标日期
        start_date: 开始日期
        frequency: 储蓄频率
        interest_rate: 年利率
        
    Returns:
        每期需要储蓄的金额
    """
    if start_date is None:
        start_date = date.today()
    
    remaining = target_amount - current_amount
    if remaining <= 0:
        return 0.0
    
    days = (target_date - start_date).days
    if days <= 0:
        raise ValueError("目标日期必须晚于开始日期")
    
    # 计算储蓄周期数
    periods_per_year = {
        Frequency.DAILY: 365,
        Frequency.WEEKLY: 52,
        Frequency.BIWEEKLY: 26,
        Frequency.MONTHLY: 12,
        Frequency.QUARTERLY: 4,
        Frequency.YEARLY: 1,
    }
    
    periods = (days / 365) * periods_per_year[frequency]
    
    if interest_rate <= 0:
        # 无利息
        return remaining / periods
    
    # 有复利，使用年金公式
    r = interest_rate / periods_per_year[frequency]
    
    if r == 0:
        return remaining / periods
    
    # 未来值公式：FV = PMT * [(1+r)^n - 1] / r
    # 求解 PMT
    factor = ((1 + r) ** periods - 1) / r
    if factor <= 0:
        return remaining / periods
    
    return remaining / factor


def calculate_compound_interest(
    principal: float,
    rate: float,
    years: float,
    compounding_frequency: int = 12
) -> float:
    """
    计算复利
    
    Args:
        principal: 本金
        rate: 年利率（小数形式）
        years: 年数
        compounding_frequency: 每年复利次数
        
    Returns:
        最终金额
    """
    return principal * (1 + rate / compounding_frequency) ** (compounding_frequency * years)


def calculate_savings_with_regular_deposits(
    initial: float,
    deposit: float,
    rate: float,
    years: float,
    deposits_per_year: int = 12,
    compounding_frequency: int = 12
) -> float:
    """
    计算定期存款的最终金额
    
    Args:
        initial: 初始金额
        deposit: 每期存款金额
        rate: 年利率
        years: 年数
        deposits_per_year: 每年存款次数
        compounding_frequency: 每年复利次数
        
    Returns:
        最终金额
    """
    # 初始金额的复利
    initial_growth = calculate_compound_interest(initial, rate, years, compounding_frequency)
    
    # 定期存款的未来值（年金）
    n = deposits_per_year * years
    r = rate / compounding_frequency
    periods_per_deposit = compounding_frequency / deposits_per_year
    
    # 简化计算
    if rate <= 0:
        return initial_growth + deposit * n
    
    # 使用年金终值公式
    annuity_factor = ((1 + r) ** (compounding_frequency * years) - 1) / r
    deposits_future = deposit * deposits_per_year / compounding_frequency * annuity_factor
    
    return initial_growth + deposits_future


def get_savings_recommendation(
    target_amount: float,
    current_amount: float,
    target_date: Optional[date] = None,
    monthly_income: Optional[float] = None,
    monthly_expenses: Optional[float] = None
) -> Dict:
    """
    获取储蓄建议
    
    Args:
        target_amount: 目标金额
        current_amount: 当前金额
        target_date: 目标日期
        monthly_income: 月收入
        monthly_expenses: 月支出
        
    Returns:
        储蓄建议
    """
    remaining = target_amount - current_amount
    recommendation = {
        "remaining_amount": remaining,
        "progress_percentage": (current_amount / target_amount) * 100 if target_amount > 0 else 0,
        "status": "on_track",
        "suggestions": [],
    }
    
    if remaining <= 0:
        recommendation["status"] = "completed"
        recommendation["suggestions"].append("恭喜！您已达成储蓄目标！")
        return recommendation
    
    if target_date:
        days = (target_date - date.today()).days
        if days <= 0:
            recommendation["status"] = "overdue"
            recommendation["suggestions"].append("目标日期已过，请调整目标或增加储蓄。")
            return recommendation
        
        monthly_required = remaining / (days / 30)
        recommendation["monthly_required"] = monthly_required
        recommendation["days_remaining"] = days
        
        if monthly_income and monthly_expenses:
            available = monthly_income - monthly_expenses
            recommendation["available_monthly"] = available
            
            if available >= monthly_required:
                recommendation["status"] = "achievable"
                recommendation["suggestions"].append(f"每月需储蓄 ¥{monthly_required:.2f}，您有能力达成。")
            else:
                gap = monthly_required - available
                recommendation["status"] = "challenging"
                recommendation["monthly_gap"] = gap
                recommendation["suggestions"].append(f"每月缺口 ¥{gap:.2f}，建议：")
                recommendation["suggestions"].append("  - 增加收入来源")
                recommendation["suggestions"].append("  - 减少非必要支出")
                recommendation["suggestions"].append("  - 延长目标期限")
        else:
            recommendation["suggestions"].append(f"每月需储蓄 ¥{monthly_required:.2f} 以按时达成目标。")
    else:
        recommendation["suggestions"].append("建议设置目标日期以获得更详细的储蓄建议。")
    
    # 通用建议
    if remaining > 0:
        recommendation["suggestions"].extend([
            "设立自动转账，每月固定储蓄",
            "使用高收益储蓄账户增加利息收入",
            "记录每笔储蓄，保持动力",
            "设定里程碑奖励自己",
        ])
    
    return recommendation


def generate_progress_report(goal: SavingsGoal) -> str:
    """
    生成进度报告
    
    Args:
        goal: 储蓄目标
        
    Returns:
        进度报告文本
    """
    lines = [
        f"{'=' * 40}",
        f"储蓄目标进度报告: {goal.name}",
        f"{'=' * 40}",
        f"",
        f"目标金额: ¥{goal.target_amount:,.2f}",
        f"当前金额: ¥{goal.current_amount:,.2f}",
        f"剩余金额: ¥{goal.remaining_amount:,.2f}",
        f"完成进度: {goal.progress_percentage:.1f}%",
        f"",
        f"开始日期: {goal.start_date}",
    ]
    
    if goal.target_date:
        lines.append(f"目标日期: {goal.target_date}")
        lines.append(f"剩余天数: {goal.days_remaining} 天")
        
        expected = goal.expected_progress
        if expected is not None:
            lines.append(f"预期进度: {expected:.1f}%")
    
    lines.append(f"当前状态: {goal.status.value}")
    
    if goal.interest_rate > 0:
        lines.append(f"")
        lines.append(f"年利率: {goal.interest_rate * 100:.2f}%")
        # 计算预期利息收益
        if goal.target_date:
            years = (goal.target_date - goal.start_date).days / 365.25
            projected = calculate_compound_interest(
                goal.current_amount, 
                goal.interest_rate, 
                years,
                goal.compounding_frequency
            )
            interest = projected - goal.current_amount
            lines.append(f"预期利息: ¥{interest:,.2f}")
    
    # 进度条
    lines.append(f"")
    lines.append(f"进度条:")
    bar_length = 30
    filled = int(bar_length * goal.progress_percentage / 100)
    bar = "█" * filled + "░" * (bar_length - filled)
    lines.append(f"[{bar}] {goal.progress_percentage:.1f}%")
    
    lines.append(f"{'=' * 40}")
    
    return "\n".join(lines)


def calculate_milestones(
    target_amount: float,
    num_milestones: int = 4
) -> List[Tuple[float, float]]:
    """
    计算里程碑
    
    Args:
        target_amount: 目标金额
        num_milestones: 里程碑数量
        
    Returns:
        里程碑列表 [(百分比, 金额), ...]
    """
    milestones = []
    for i in range(1, num_milestones + 1):
        percentage = (i / num_milestones) * 100
        amount = target_amount * i / num_milestones
        milestones.append((percentage, amount))
    return milestones


def prioritize_goals(
    goals: List[SavingsGoal],
    method: str = "priority"
) -> List[SavingsGoal]:
    """
    对目标进行优先级排序
    
    Args:
        goals: 目标列表
        method: 排序方法
            - deadline: 按截止日期排序
            - priority: 按优先级排序
            - progress: 按进度排序
            - amount: 按目标金额排序
            
    Returns:
        排序后的目标列表
    """
    sorted_goals = goals.copy()
    
    if method == "deadline":
        # 有截止日期的排前面，按日期升序
        sorted_goals.sort(key=lambda g: (g.target_date is None, g.target_date or date.max))
    elif method == "priority":
        # 按优先级降序
        sorted_goals.sort(key=lambda g: g.priority, reverse=True)
    elif method == "progress":
        # 按进度升序（最需要关注的排前面）
        sorted_goals.sort(key=lambda g: g.progress_percentage)
    elif method == "amount":
        # 按目标金额降序
        sorted_goals.sort(key=lambda g: g.target_amount, reverse=True)
    
    return sorted_goals


def suggest_savings_allocation(
    goals: List[SavingsGoal],
    total_monthly_savings: float
) -> Dict[str, float]:
    """
    建议储蓄分配
    
    Args:
        goals: 目标列表
        total_monthly_savings: 每月可储蓄总额
        
    Returns:
        每个目标的建议月储蓄金额
    """
    active_goals = [g for g in goals if not g.is_completed]
    
    if not active_goals:
        return {}
    
    allocation = {}
    remaining = total_monthly_savings
    
    # 首先处理有截止日期且紧迫的目标
    urgent_goals = [g for g in active_goals if g.target_date and g.days_remaining and g.days_remaining <= 90]
    
    for goal in urgent_goals:
        if remaining <= 0:
            break
        required = calculate_required_savings(
            goal.target_amount,
            goal.current_amount,
            goal.target_date
        )
        allocate = min(required, remaining)
        allocation[goal.name] = allocate
        remaining -= allocate
    
    # 剩余资金按优先级和剩余金额比例分配
    other_goals = [g for g in active_goals if g.name not in allocation]
    
    if other_goals and remaining > 0:
        # 按优先级加权
        total_weight = sum(g.priority * g.remaining_amount for g in other_goals)
        
        for goal in other_goals:
            if total_weight > 0:
                weight = goal.priority * goal.remaining_amount
                share = (weight / total_weight) * remaining
                allocation[goal.name] = allocation.get(goal.name, 0) + share
    
    return allocation


# 便捷函数
def create_goal(
    name: str,
    target_amount: float,
    current_amount: float = 0.0,
    target_date: Optional[date] = None,
    **kwargs
) -> SavingsGoal:
    """创建储蓄目标的便捷函数"""
    return SavingsGoal(
        name=name,
        target_amount=target_amount,
        current_amount=current_amount,
        target_date=target_date,
        **kwargs
    )