#!/usr/bin/env python3
"""
储蓄目标追踪工具 - 使用示例

演示：
- 创建储蓄目标
- 追踪进度
- 计算达成时间
- 复利计算
- 多目标管理
- 储蓄建议
"""

import sys
import os
from datetime import date, timedelta

# 添加父目录到路径
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from mod import (
    SavingsGoal,
    SavingsGoalManager,
    Frequency,
    GoalStatus,
    calculate_time_to_goal,
    calculate_required_savings,
    calculate_compound_interest,
    calculate_savings_with_regular_deposits,
    get_savings_recommendation,
    generate_progress_report,
    calculate_milestones,
    prioritize_goals,
    suggest_savings_allocation,
    create_goal,
)


def example_basic_goal():
    """示例1: 创建基本储蓄目标"""
    print("=" * 50)
    print("示例1: 创建基本储蓄目标")
    print("=" * 50)
    
    # 创建购车储蓄目标
    car_goal = create_goal(
        name="购车基金",
        target_amount=100000,
        current_amount=25000,
        description="计划购买一辆家用轿车"
    )
    
    print(f"目标名称: {car_goal.name}")
    print(f"目标金额: ¥{car_goal.target_amount:,.2f}")
    print(f"当前金额: ¥{car_goal.current_amount:,.2f}")
    print(f"完成进度: {car_goal.progress_percentage:.1f}%")
    print(f"剩余金额: ¥{car_goal.remaining_amount:,.2f}")
    print()


def example_goal_with_deadline():
    """示例2: 创建带截止日期的目标"""
    print("=" * 50)
    print("示例2: 创建带截止日期的目标")
    print("=" * 50)
    
    # 创建旅行储蓄目标，目标明年年底
    travel_goal = SavingsGoal(
        name="2027年旅行基金",
        target_amount=30000,
        current_amount=8000,
        target_date=date.today() + timedelta(days=365),
        category="travel",
        priority=3,
        description="计划去日本旅行"
    )
    
    print(f"目标名称: {travel_goal.name}")
    print(f"剩余天数: {travel_goal.days_remaining} 天")
    print(f"预期进度: {travel_goal.expected_progress:.1f}%")
    print(f"当前进度: {travel_goal.progress_percentage:.1f}%")
    print(f"状态: {travel_goal.status.value}")
    
    # 计算每月需要储蓄金额
    required = calculate_required_savings(
        travel_goal.target_amount,
        travel_goal.current_amount,
        travel_goal.target_date
    )
    print(f"每月需储蓄: ¥{required:,.2f}")
    print()


def example_with_interest():
    """示例3: 带利息的储蓄目标"""
    print("=" * 50)
    print("示例3: 带利息的储蓄目标")
    print("=" * 50)
    
    # 创建储蓄账户目标，带5%年利率
    savings_goal = SavingsGoal(
        name="高收益储蓄账户",
        target_amount=50000,
        current_amount=10000,
        start_date=date.today() - timedelta(days=180),
        target_date=date.today() + timedelta(days=365),
        interest_rate=0.05,  # 5% 年利率
        compounding_frequency=12  # 月复利
    )
    
    print(f"年利率: {savings_goal.interest_rate * 100:.1f}%")
    print(f"复利频率: 每月")
    
    # 计算预期利息收益
    projected = calculate_compound_interest(
        savings_goal.current_amount,
        savings_goal.interest_rate,
        (savings_goal.target_date - savings_goal.start_date).days / 365.25
    )
    interest = projected - savings_goal.current_amount
    print(f"预期利息收益: ¥{interest:,.2f}")
    
    # 比较无利息时所需储蓄
    required_no_interest = calculate_required_savings(
        savings_goal.target_amount,
        savings_goal.current_amount,
        savings_goal.target_date,
        interest_rate=0
    )
    required_with_interest = calculate_required_savings(
        savings_goal.target_amount,
        savings_goal.current_amount,
        savings_goal.target_date,
        interest_rate=0.05
    )
    
    print(f"无利息时每月需存: ¥{required_no_interest:,.2f}")
    print(f"有利息时每月需存: ¥{required_with_interest:,.2f}")
    print(f"利息节省: ¥{(required_no_interest - required_with_interest):,.2f}/月")
    print()


def example_calculate_time():
    """示例4: 计算达成时间"""
    print("=" * 50)
    print("示例4: 计算达成目标所需时间")
    print("=" * 50)
    
    # 目标10万元，已有2万元，每月存3000元
    periods = calculate_time_to_goal(
        target_amount=100000,
        current_amount=20000,
        savings_per_period=3000,
        frequency=Frequency.MONTHLY,
        interest_rate=0.03  # 3% 年利率
    )
    
    print(f"目标金额: ¥100,000")
    print(f"当前金额: ¥20,000")
    print(f"每月储蓄: ¥3,000")
    print(f"年利率: 3%")
    print(f"预计需要: {periods} 个月")
    
    # 如果每周存750（相同月储蓄额）
    periods_weekly = calculate_time_to_goal(
        target_amount=100000,
        current_amount=20000,
        savings_per_period=750,
        frequency=Frequency.WEEKLY,
        interest_rate=0.03
    )
    
    print(f"每周储蓄 ¥750，需要: {periods_weekly} 周 (约 {periods_weekly/4:.1f} 月)")
    print()


def example_multiple_goals():
    """示例5: 多目标管理"""
    print("=" * 50)
    print("示例5: 多目标管理")
    print("=" * 50)
    
    manager = SavingsGoalManager()
    
    # 创建多个目标
    manager.create_goal(
        name="购车基金",
        target_amount=100000,
        current_amount=30000,
        target_date=date.today() + timedelta(days=365),
        category="car",
        priority=5
    )
    
    manager.create_goal(
        name="旅行基金",
        target_amount=30000,
        current_amount=10000,
        target_date=date.today() + timedelta(days=180),
        category="travel",
        priority=3
    )
    
    manager.create_goal(
        name="应急储备",
        target_amount=50000,
        current_amount=15000,
        category="emergency",
        priority=4
    )
    
    manager.create_goal(
        name="已达成目标",
        target_amount=5000,
        current_amount=5000,
        category="completed"
    )
    
    print(f"总目标数: {len(manager.goals)}")
    print(f"总目标金额: ¥{manager.total_target:,.2f}")
    print(f"已储蓄总额: ¥{manager.total_saved:,.2f}")
    print(f"总体进度: {manager.overall_progress:.1f}%")
    print(f"已完成目标: {len(manager.completed_goals)}")
    print(f"进行中目标: {len(manager.active_goals)}")
    print()
    
    # 按优先级排序
    sorted_goals = prioritize_goals(manager.active_goals, method="priority")
    print("按优先级排序的目标:")
    for i, goal in enumerate(sorted_goals, 1):
        print(f"  {i}. {goal.name} (优先级:{goal.priority}) - {goal.progress_percentage:.1f}%")
    print()


def example_savings_allocation():
    """示例6: 储蓄分配建议"""
    print("=" * 50)
    print("示例6: 储蓄分配建议")
    print("=" * 50)
    
    manager = SavingsGoalManager()
    
    # 创建多个目标
    manager.create_goal(
        name="购车",
        target_amount=100000,
        current_amount=20000,
        target_date=date.today() + timedelta(days=365),
        priority=5
    )
    
    manager.create_goal(
        name="旅行",
        target_amount=30000,
        current_amount=5000,
        target_date=date.today() + timedelta(days=90),  # 紧急
        priority=3
    )
    
    manager.create_goal(
        name="应急储备",
        target_amount=50000,
        current_amount=10000,
        priority=4
    )
    
    # 每月可储蓄5000元，建议如何分配
    monthly_savings = 5000
    allocation = suggest_savings_allocation(manager.active_goals, monthly_savings)
    
    print(f"每月可储蓄: ¥{monthly_savings:,.2f}")
    print("建议分配:")
    for name, amount in allocation.items():
        print(f"  {name}: ¥{amount:,.2f}")
    print()
    
    # 计算验证
    total_allocated = sum(allocation.values())
    print(f"分配总额: ¥{total_allocated:,.2f}")
    print()


def example_progress_report():
    """示例7: 生成进度报告"""
    print("=" * 50)
    print("示例7: 生成进度报告")
    print("=" * 50)
    
    goal = SavingsGoal(
        name="购车基金",
        target_amount=100000,
        current_amount=35000,
        start_date=date.today() - timedelta(days=90),
        target_date=date.today() + timedelta(days=365),
        interest_rate=0.03,
        description="计划购买一辆家用轿车"
    )
    
    report = generate_progress_report(goal)
    print(report)
    print()


def example_savings_recommendation():
    """示例8: 储蓄建议"""
    print("=" * 50)
    print("示例8: 储蓄建议")
    print("=" * 50)
    
    # 月收入8000，月支出5000，目标存10万
    recommendation = get_savings_recommendation(
        target_amount=100000,
        current_amount=20000,
        target_date=date.today() + timedelta(days=365),
        monthly_income=8000,
        monthly_expenses=5000
    )
    
    print(f"剩余金额: ¥{recommendation['remaining_amount']:,.2f}")
    print(f"当前进度: {recommendation['progress_percentage']:.1f}%")
    print(f"状态: {recommendation['status']}")
    print(f"每月需储蓄: ¥{recommendation['monthly_required']:,.2f}")
    print(f"每月可储蓄: ¥{recommendation['available_monthly']:,.2f}")
    print("\n建议:")
    for suggestion in recommendation['suggestions']:
        print(f"  {suggestion}")
    print()


def example_milestones():
    """示例9: 里程碑计算"""
    print("=" * 50)
    print("示例9: 里程碑设置")
    print("=" * 50)
    
    # 为10万元目标设置里程碑
    milestones = calculate_milestones(100000, num_milestones=5)
    
    print("储蓄里程碑:")
    for percentage, amount in milestones:
        print(f"  {percentage:.0f}% 完成 → ¥{amount:,.2f}")
    
    # 检查当前进度对应里程碑
    current = 35000
    print(f"\n当前金额 ¥{current:,.2f}，已达成:")
    for percentage, amount in milestones:
        if current >= amount:
            print(f"  ✓ {percentage:.0f}% 里程碑")
        else:
            print(f"  ○ {percentage:.0f}% 里程碑 (还需 ¥{amount - current:,.2f})")
    print()


def example_compound_interest():
    """示例10: 复利计算"""
    print("=" * 50)
    print("示例10: 复利计算")
    print("=" * 50)
    
    # 比较10年储蓄的收益
    initial = 10000
    deposit = 500
    rate = 0.05
    years = 10
    
    # 无利息
    simple_total = initial + deposit * 12 * years
    print(f"简单储蓄（无利息）:")
    print(f"  本金 ¥{initial:,.2f} + 每月 ¥{deposit} × {years}年")
    print(f"  10年后总额: ¥{simple_total:,.2f}")
    
    # 有复利
    compound_total = calculate_savings_with_regular_deposits(
        initial, deposit, rate, years
    )
    print(f"\n复利储蓄（{rate*100:.1f}%年利率）:")
    print(f"  10年后总额: ¥{compound_total:,.2f}")
    print(f"  利息收益: ¥{compound_total - simple_total:,.2f}")
    
    # 比较不同复利频率
    print(f"\n不同复利频率的收益:")
    for freq, name in [(1, "年复利"), (4, "季复利"), (12, "月复利"), (365, "日复利")]:
        result = calculate_compound_interest(initial, rate, years, freq)
        print(f"  {name}: ¥{result:,.2f}")
    print()


def example_add_and_track():
    """示例11: 添加储蓄并追踪"""
    print("=" * 50)
    print("示例11: 添加储蓄并追踪")
    print("=" * 50)
    
    goal = SavingsGoal(
        name="购房首付",
        target_amount=300000,
        current_amount=50000,
        target_date=date.today() + timedelta(days=365*2),  # 2年
        interest_rate=0.04
    )
    
    print(f"初始状态:")
    print(f"  当前金额: ¥{goal.current_amount:,.2f}")
    print(f"  进度: {goal.progress_percentage:.1f}%")
    print(f"  状态: {goal.status.value}")
    print()
    
    # 模拟每月添加储蓄
    monthly_savings = [5000, 5000, 6000, 5000, 7000]
    print("每月储蓄记录:")
    for i, amount in enumerate(monthly_savings, 1):
        goal.add_savings(amount)
        print(f"  第{i}月: 存入 ¥{amount:,.2f} → 当前 ¥{goal.current_amount:,.2f} ({goal.progress_percentage:.1f}%)")
    
    print()
    print(f"储蓄后状态:")
    print(f"  当前金额: ¥{goal.current_amount:,.2f}")
    print(f"  进度: {goal.progress_percentage:.1f}%")
    print()


def run_all_examples():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("储蓄目标追踪工具 - 使用示例演示")
    print("=" * 60 + "\n")
    
    example_basic_goal()
    example_goal_with_deadline()
    example_with_interest()
    example_calculate_time()
    example_multiple_goals()
    example_savings_allocation()
    example_progress_report()
    example_savings_recommendation()
    example_milestones()
    example_compound_interest()
    example_add_and_track()
    
    print("=" * 60)
    print("所有示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()