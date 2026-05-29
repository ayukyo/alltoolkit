# 储蓄目标追踪工具 (Savings Goal Utils)

帮助用户管理储蓄目标、追踪进度、预测达成时间、计算复利收益。

## 功能

- ✅ 创建和管理储蓄目标
- ✅ 追踪储蓄进度
- ✅ 计算达成目标所需时间
- ✅ 支持简单利息和复利计算
- ✅ 提供储蓄建议
- ✅ 生成进度报告
- ✅ 支持多目标管理
- ✅ 目标优先级排序
- ✅ 储蓄分配建议

## 安装

```bash
# 无需安装，直接导入使用
from savings_goal_utils.mod import SavingsGoal, SavingsGoalManager
```

## 快速开始

### 创建储蓄目标

```python
from savings_goal_utils.mod import SavingsGoal, create_goal
from datetime import date, timedelta

# 简单创建
goal = create_goal(
    name="购车基金",
    target_amount=100000,
    current_amount=25000
)

# 带截止日期
travel_goal = SavingsGoal(
    name="旅行基金",
    target_amount=30000,
    current_amount=8000,
    target_date=date.today() + timedelta(days=365),
    category="travel",
    priority=3
)
```

### 追踪进度

```python
# 查看进度
print(f"进度: {goal.progress_percentage:.1f}%")
print(f"剩余金额: ¥{goal.remaining_amount:,.2f}")
print(f"状态: {goal.status.value}")

# 添加储蓄
goal.add_savings(5000)

# 提取金额
goal.withdraw(1000)
```

### 计算达成时间

```python
from savings_goal_utils.mod import calculate_time_to_goal, Frequency

# 计算需要多少个月
months = calculate_time_to_goal(
    target_amount=100000,
    current_amount=20000,
    savings_per_period=3000,
    frequency=Frequency.MONTHLY,
    interest_rate=0.03  # 3%年利率
)
print(f"需要 {months} 个月")
```

### 计算所需储蓄

```python
from savings_goal_utils.mod import calculate_required_savings

# 计算每月需要储蓄多少
monthly_required = calculate_required_savings(
    target_amount=100000,
    current_amount=20000,
    target_date=date.today() + timedelta(days=365),
    interest_rate=0.05
)
print(f"每月需储蓄 ¥{monthly_required:,.2f}")
```

### 复利计算

```python
from savings_goal_utils.mod import calculate_compound_interest

# 计算复利收益
result = calculate_compound_interest(
    principal=10000,
    rate=0.05,  # 5%年利率
    years=5,
    compounding_frequency=12  # 月复利
)
print(f"5年后: ¥{result:,.2f}")
```

## 多目标管理

```python
from savings_goal_utils.mod import SavingsGoalManager

manager = SavingsGoalManager()

# 创建多个目标
manager.create_goal("购车", 100000, current_amount=30000, category="car", priority=5)
manager.create_goal("旅行", 30000, current_amount=10000, category="travel", priority=3)
manager.create_goal("应急储备", 50000, current_amount=15000, category="emergency", priority=4)

# 查看总体进度
print(f"总目标金额: ¥{manager.total_target:,.2f}")
print(f"已储蓄总额: ¥{manager.total_saved:,.2f}")
print(f"总体进度: {manager.overall_progress:.1f}%")

# 按优先级排序
sorted_goals = prioritize_goals(manager.active_goals, method="priority")

# 储蓄分配建议
allocation = suggest_savings_allocation(manager.active_goals, 5000)  # 每月5000
```

## 进度报告

```python
from savings_goal_utils.mod import generate_progress_report

report = generate_progress_report(goal)
print(report)

# 输出:
# ========================================
# 储蓄目标进度报告: 购车基金
# ========================================
# 目标金额: ¥100,000.00
# 当前金额: ¥35,000.00
# 剩余金额: ¥65,000.00
# 完成进度: 35.0%
# ...
```

## 储蓄建议

```python
from savings_goal_utils.mod import get_savings_recommendation

recommendation = get_savings_recommendation(
    target_amount=100000,
    current_amount=20000,
    target_date=date.today() + timedelta(days=365),
    monthly_income=8000,
    monthly_expenses=5000
)

print(f"状态: {recommendation['status']}")
for suggestion in recommendation['suggestions']:
    print(suggestion)
```

## API 参考

### SavingsGoal

| 属性 | 类型 | 说明 |
|------|------|------|
| `name` | str | 目标名称 |
| `target_amount` | float | 目标金额 |
| `current_amount` | float | 当前金额 |
| `target_date` | date | 目标日期（可选） |
| `interest_rate` | float | 年利率（小数形式） |
| `category` | str | 分类 |
| `priority` | int | 优先级（1-5） |

| 方法 | 说明 |
|------|------|
| `add_savings(amount)` | 添加储蓄 |
| `withdraw(amount)` | 提取金额 |
| `progress_percentage` | 进度百分比 |
| `remaining_amount` | 剩余金额 |
| `is_completed` | 是否已完成 |
| `status` | 当前状态 |

### 状态类型

- `NOT_STARTED` - 未开始
- `IN_PROGRESS` - 进行中
- `ON_TRACK` - 进度正常
- `AHEAD` - 进度超前
- `BEHIND` - 进度落后
- `COMPLETED` - 已完成
- `PAUSED` - 已暂停

### 储蓄频率

- `DAILY` - 每日
- `WEEKLY` - 每周
- `BIWEEKLY` - 每两周
- `MONTHLY` - 每月
- `QUARTERLY` - 每季度
- `YEARLY` - 每年

## 测试

```bash
python Python/savings_goal_utils/savings_goal_utils_test.py
```

## 许可证

MIT License