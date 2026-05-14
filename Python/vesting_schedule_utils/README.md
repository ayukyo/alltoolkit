# Vesting Schedule Utils - 股权归属计划计算工具

AllToolkit 股权归属计划计算模块 - 零外部依赖，生产就绪。

## 📋 功能概览

本模块提供完整的股权归属计划计算功能，适用于股票期权、RSU等股权激励计划的管理和计算。

### 核心功能

- **多种归属类型**：线性、阶梯、Cliff、即时归属
- **灵活的归属频率**：按月、季度、半年、年度
- **Cliff期支持**：支持任意 Cliff 期和归属比例
- **归属状态计算**：实时计算已归属/未归属份额
- **归属日历生成**：生成年度归属事件日历
- **加速归属计算**：计算加速归属份额
- **价值估算**：根据股价估算归属价值
- **完整时间线**：生成可视化的归属时间线

## 🚀 快速开始

### 创建标准归属计划

```python
from vesting_schedule_utils.mod import create_standard_schedule, get_vesting_status
from datetime import date

# 创建标准4年归属计划（硅谷标准）
# 1年Cliff后归属25%，剩余75%按月归属36个月
schedule = create_standard_schedule(
    total_shares=10000,
    grant_date=date(2020, 1, 1),
    vesting_years=4,
    cliff_years=1,
    cliff_percentage=25.0
)

# 获取当前归属状态
status = get_vesting_status(schedule)
print(f"已归属: {status.vested_shares} 股 ({status.vested_percentage:.2f}%)")
print(f"下次归属: {status.next_vesting_date} - {status.next_vesting_shares} 股")
```

### 创建后置归属计划

```python
from vesting_schedule_utils.mod import create_backloaded_schedule

# 后置归属：逐年递增 10%, 20%, 30%, 40%
schedule = create_backloaded_schedule(
    total_shares=10000,
    grant_date=date(2020, 1, 1)
)

# 或自定义阶梯计划
schedule = create_backloaded_schedule(
    total_shares=10000,
    grant_date=date(2020, 1, 1),
    schedule=[(1, 15), (2, 25), (3, 35), (4, 25)]
)
```

### 获取归属状态

```python
from vesting_schedule_utils.mod import get_vesting_status
from datetime import date

status = get_vesting_status(schedule, date(2022, 1, 1))

print(f"已归属份额: {status.vested_shares}")
print(f"未归属份额: {status.unvested_shares}")
print(f"已归属比例: {status.vested_percentage}%")
print(f"下次归属日期: {status.next_vesting_date}")
print(f"是否完全归属: {status.is_fully_vested}")
print(f"剩余月数: {status.remaining_months}")
```

### 生成归属时间线

```python
from vesting_schedule_utils.mod import get_vesting_timeline

timeline = get_vesting_timeline(schedule)
print(timeline)
```

输出示例：
```
归属计划时间线
==================================================
授予日期: 2020-01-01
总份额: 10,000
归属类型: linear
归属周期: 48 个月
归属频率: monthly
Cliff期: 12 个月 (25.0%)

归属事件 (37 次):
--------------------------------------------------
2021-01-01: 2,500 股 (25.00%) [CLIFF] - Cliff归属（25.0%）
    累计: 2,500 股 (25.00%)
2021-02-01: 208 股 (2.08%) - 第1次归属
    累计: 2,708 股 (27.08%)
...
```

### 计算归属价值

```python
from vesting_schedule_utils.mod import estimate_vesting_value

# 每股价格10美元
value = estimate_vesting_value(schedule, price_per_share=10.0)

print(f"已归属价值: ${value['vested_value']}")
print(f"未归属价值: ${value['unvested_value']}")
print(f"总价值: ${value['total_value']}")
```

### 加速归属计算

```python
from vesting_schedule_utils.mod import calculate_accelerated_vesting

# 50%加速归属
shares, events = calculate_accelerated_vesting(
    schedule,
    acceleration_percentage=50.0
)

print(f"可加速归属: {shares} 股")
```

## 📖 API 参考

### 归属类型

| 类型 | 说明 |
|------|------|
| `LINEAR` | 线性归属 - 按固定频率平均归属 |
| `CLIFF` | Cliff归属 - Cliff期满一次性归属全部 |
| `GRADED` | 阶梯归属 - 按年度阶梯比例归属 |
| `IMMEDIATE` | 即时归属 - 授予时即刻归属 |

### 归属频率

| 频率 | 说明 |
|------|------|
| `MONTHLY` | 按月归属 |
| `QUARTERLY` | 按季度归属 |
| `SEMI_ANNUAL` | 每半年归属 |
| `ANNUALLY` | 每年归属 |

### 主要类

#### VestingSchedule

```python
VestingSchedule(
    total_shares: int,           # 总份额
    grant_date: date,            # 授予日期
    vesting_type: VestingType,   # 归属类型
    vesting_period_months: int,  # 归属周期（月）
    cliff_months: int = 0,       # Cliff期（月）
    cliff_percentage: float = 0.0,  # Cliff归属比例
    frequency: VestingFrequency = MONTHLY,
    graded_schedule: List = None  # 阶梯计划 [(年, 比例)]
)
```

#### VestingStatus

```python
VestingStatus(
    vested_shares: int,          # 已归属份额
    unvested_shares: int,        # 未归属份额
    vested_percentage: float,    # 已归属比例
    next_vesting_date: date,     # 下次归属日期
    next_vesting_shares: int,    # 下次归属份额
    remaining_months: int,       # 剩余月数
    is_fully_vested: bool,       # 完全归属标记
    vesting_events: List         # 归属事件列表
)
```

### 主要函数

| 函数 | 说明 |
|------|------|
| `create_standard_schedule()` | 创建标准4年归属计划 |
| `create_backloaded_schedule()` | 创建后置归属计划 |
| `calculate_vesting_schedule()` | 计算完整归属事件列表 |
| `get_vesting_status()` | 获取指定日期的归属状态 |
| `calculate_accelerated_vesting()` | 计算加速归属 |
| `generate_vesting_calendar()` | 生成年度归属日历 |
| `estimate_vesting_value()` | 估算归属价值 |
| `calculate_vesting_summary()` | 生成归属摘要 |
| `days_until_next_vesting()` | 距下次归属天数 |
| `get_vesting_timeline()` | 生成归属时间线文本 |
| `add_months()` | 日期加月份 |
| `months_between()` | 计算两日期间月数 |

## 📊 归属计划示例

### 标准硅谷归属计划

```python
# 4年归属，1年Cliff（25%），按月归属
schedule = VestingSchedule(
    total_shares=10000,
    grant_date=date(2020, 1, 1),
    vesting_type=VestingType.LINEAR,
    vesting_period_months=48,
    cliff_months=12,
    cliff_percentage=25.0,
    frequency=VestingFrequency.MONTHLY
)

# 归属事件：
# - 2021-01-01: 2500股 (25%) [Cliff]
# - 2021-02-01 ~ 2024-01-01: 约208股/月
```

### 季度归属计划

```python
# 4年归属，季度归属
schedule = VestingSchedule(
    total_shares=10000,
    grant_date=date(2020, 1, 1),
    vesting_type=VestingType.LINEAR,
    vesting_period_months=48,
    cliff_months=12,
    cliff_percentage=25.0,
    frequency=VestingFrequency.QUARTERLY
)

# 归属事件：
# - 2021-01-01: 2500股 (25%) [Cliff]
# - 每季度约625股（12个季度）
```

### 阶梯归属计划

```python
# 后置归属：10%, 20%, 30%, 40%
schedule = VestingSchedule(
    total_shares=10000,
    grant_date=date(2020, 1, 1),
    vesting_type=VestingType.GRADED,
    vesting_period_months=48,
    graded_schedule=[(1, 10), (2, 20), (3, 30), (4, 40)]
)

# 归属事件：
# - 2021-01-01: 1000股 (10%)
# - 2022-01-01: 2000股 (20%)
# - 2023-01-01: 3000股 (30%)
# - 2024-01-01: 4000股 (40%)
```

### 即时归属

```python
# 授予时即刻归属全部
schedule = VestingSchedule(
    total_shares=10000,
    grant_date=date(2020, 1, 1),
    vesting_type=VestingType.IMMEDIATE,
    vesting_period_months=0
)

# 状态：立即100%归属
```

## 🧪 测试

运行测试：

```bash
cd Python/vesting_schedule_utils
python vesting_schedule_utils_test.py
```

测试覆盖：
- 日期计算（月末处理、跨年）
- 各种归属类型（线性、阶梯、Cliff、即时）
- 归属频率（月、季度、半年、年）
- Cliff期计算
- 归属状态（各阶段）
- 加速归属
- 价值估算
- 边界值（最小/最大份额、极端日期）

## 💡 使用场景

1. **股权激励管理**：跟踪员工股权归属进度
2. **财务报告**：计算归属相关财务数据
3. **离职结算**：计算离职时的已归属份额
4. **激励设计**：设计不同归属方案
5. **投资分析**：估算股权价值

## 📝 注意事项

- 所有计算基于标准日历月，不考虑交易日调整
- 份额计算采用向下取整，最后归属处理余数
- Cliff期后归属按剩余周期平均分配
- 加速归属计算返回可加速份额，不修改原计划

---

**Last updated**: 2026-05-14
**License**: MIT