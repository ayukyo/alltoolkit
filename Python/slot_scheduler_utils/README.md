# slot_scheduler_utils - 时间槽调度工具

**零依赖的时间槽管理和预约调度工具库**

---

## 功能特性

- ✅ **时间槽创建与管理** - 支持单个和批量创建时间槽
- ✅ **预约与取消** - 完整的预约生命周期管理
- ✅ **冲突检测** - 自动检测和防止预约冲突
- ✅ **可用时间查询** - 查找空闲时间槽和连续空闲时段
- ✅ **批量操作** - 批量创建、清理过去时间槽
- ✅ **重复调度** - 支持每日、每周、每月重复规则
- ✅ **多资源支持** - 同时管理多个资源（会议室、场地等）
- ✅ **封锁机制** - 支持临时封锁时间槽（维护、例外）
- ✅ **数据导出导入** - 序列化和恢复调度状态
- ✅ **利用率统计** - 计算和可视化资源使用情况

---

## 快速开始

### 基本使用

```python
from slot_scheduler_utils import SlotScheduler
from datetime import datetime, date, time

# 创建调度器
scheduler = SlotScheduler(default_slot_duration=30)

# 创建时间槽
slot = scheduler.create_slot(
    start=datetime(2024, 1, 15, 10, 0),
    end=datetime(2024, 1, 15, 11, 0),
    resource_id="meeting_room_A"
)

# 预约时间槽
booking = scheduler.book_slot(
    slot_id=slot.slot_id,
    user_id="user_zhang",
    notes="产品评审会议"
)

print(f"预约成功: {booking.slot.start}")
```

### 批量创建时间槽

```python
# 为一周创建工作日时间槽
slots = scheduler.create_slots_from_schedule(
    resource_id="meeting_room_A",
    start_date=date(2024, 1, 15),
    end_date=date(2024, 1, 19),
    daily_start_time=time(9, 0),
    daily_end_time=time(18, 0),
    slot_duration=60,
    working_days=[0, 1, 2, 3, 4]  # 周一到周五
)
```

### 查找可用时间

```python
# 查找下一个可用时间槽
next_slot = scheduler.find_next_available(
    resource_id="meeting_room_A",
    after=datetime(2024, 1, 15, 10, 0)
)

# 查找指定时长的时间槽
available = scheduler.find_available_range(
    resource_id="meeting_room_A",
    start=datetime(2024, 1, 15, 9, 0),
    end=datetime(2024, 1, 15, 18, 0),
    duration_minutes=90
)
```

### 重复预约

```python
from slot_scheduler_utils import RecurrenceRule, RecurrenceType

# 每周一上午10点的会议
rule = RecurrenceRule(
    recurrence_type=RecurrenceType.WEEKLY,
    days_of_week=[0],  # 周一
    count=4
)

slots = scheduler.create_recurring_slots(
    base_start=datetime(2024, 1, 15, 10, 0),
    base_end=datetime(2024, 1, 15, 11, 0),
    resource_id="weekly_meeting",
    recurrence=rule
)
```

---

## API 参考

### TimeSlot（时间槽）

```python
@dataclass
class TimeSlot:
    start: datetime           # 开始时间
    end: datetime             # 结束时间
    resource_id: str          # 资源ID
    slot_id: str              # 时间槽唯一ID（自动生成）
    status: BookingStatus     # 状态（available/booked/blocked）
    metadata: Dict            # 元数据
```

**方法：**
- `duration` - 返回时长（timedelta）
- `duration_minutes` - 返回时长（分钟）
- `overlaps(other)` - 检查是否与另一时间槽重叠
- `contains(dt)` - 检查指定时间是否在时间槽内
- `to_dict()` - 转换为字典
- `from_dict(data)` - 从字典创建

### SlotScheduler（调度器）

**创建操作：**
- `create_slot()` - 创建单个时间槽
- `create_slots_from_schedule()` - 批量创建时间槽
- `create_recurring_slots()` - 创建重复时间槽

**预约操作：**
- `book_slot()` - 预约时间槽
- `cancel_booking()` - 取消预约
- `block_slot()` - 封锁时间槽
- `unblock_slot()` - 解除封锁

**查询操作：**
- `get_slot()` - 获取指定时间槽
- `get_slots_by_resource()` - 获取资源的时间槽
- `get_available_slots()` - 获取可用时间槽
- `find_next_available()` - 查找下一个可用时间槽
- `find_available_range()` - 查找指定范围内的可用时间槽
- `get_user_bookings()` - 获取用户预约

**检查操作：**
- `check_availability()` - 检查时间段可用性

**统计操作：**
- `get_schedule_summary()` - 获取某日调度摘要

**管理操作：**
- `delete_slot()` - 删除时间槽
- `clear_past_slots()` - 清理过去时间槽

**数据操作：**
- `to_dict()` - 导出数据
- `from_dict(data)` - 导入数据

### RecurrenceRule（重复规则）

```python
@dataclass
class RecurrenceRule:
    recurrence_type: RecurrenceType  # 重复类型
    interval: int = 1                # 间隔
    end_date: date = None            # 结束日期
    count: int = None                # 重复次数
    days_of_week: List[int] = None   # 星期几（0=周一）
    day_of_month: int = None         # 每月第几天
    exceptions: Set[date] = None     # 排除日期
```

**重复类型：**
- `NONE` - 无重复
- `DAILY` - 每日
- `WEEKLY` - 每周
- `MONTHLY` - 每月
- `YEARLY` - 每年

### 便捷函数

```python
# 创建每日时间槽
slots = create_daily_slots(
    resource_id="room",
    date=date(2024, 1, 15),
    start_time=time(9, 0),
    end_time=time(18, 0),
    slot_duration=60
)

# 查找连续空闲时间
free_periods = find_free_time(slots, min_duration_minutes=60)

# 计算利用率
stats = calculate_utilization(slots)
```

---

## 使用场景

### 1. 会议室预订系统

```python
scheduler = SlotScheduler()

# 创建会议室时间槽
scheduler.create_slots_from_schedule(
    resource_id="room_A",
    start_date=date.today(),
    end_date=date.today() + timedelta(days=7),
    daily_start_time=time(9, 0),
    daily_end_time=time(18, 0),
    slot_duration=60,
    working_days=[0, 1, 2, 3, 4]
)

# 用户预约
booking = scheduler.book_slot(
    slot_id=slot.slot_id,
    user_id="user_zhang",
    notes="产品评审"
)

# 查找可用时间
available = scheduler.get_available_slots("room_A")
```

### 2. 医生预约排班

```python
# 创建门诊时间槽
scheduler.create_slots_from_schedule(
    resource_id="doctor_wang",
    start_date=date.today(),
    end_date=date.today(),
    daily_start_time=time(8, 0),
    daily_end_time=time(12, 0),
    slot_duration=30,
    break_between_slots=5
)

# 患者预约
scheduler.book_slot(slot.slot_id, "patient_001", "头痛检查")

# 临时封锁（医生有事）
scheduler.block_slot(slot.slot_id, "外出急诊")
```

### 3. 体育场地管理

```python
# 多场地调度
for court in ["court_1", "court_2", "court_3"]:
    scheduler.create_slots_from_schedule(
        resource_id=court,
        start_date=date.today(),
        end_date=date.today(),
        daily_start_time=time(8, 0),
        daily_end_time=time(20, 0),
        slot_duration=60
    )

# 查找任意可用场地
for court in ["court_1", "court_2", "court_3"]:
    available, _ = scheduler.check_availability(
        court, 
        datetime.now(),
        datetime.now() + timedelta(hours=1)
    )
    if available:
        scheduler.book_slot(...)
        break
```

### 4. 每周例会

```python
rule = RecurrenceRule(
    recurrence_type=RecurrenceType.WEEKLY,
    days_of_week=[0],  # 周一
    count=12
)

slots = scheduler.create_recurring_slots(
    base_start=datetime(2024, 1, 15, 10, 0),
    base_end=datetime(2024, 1, 15, 11, 0),
    resource_id="weekly_meeting",
    recurrence=rule
)

# 预约整个系列
for slot in slots:
    scheduler.book_slot(slot.slot_id, "team_alpha")
```

---

## 测试覆盖

模块包含完整的测试套件：

- 时间槽创建与验证
- 重叠检测与边界条件
- 预约生命周期
- 冲突检测
- 重复规则验证
- 数据导出导入
- 边界值测试（极短/长时间槽、跨午夜等）

运行测试：

```bash
python slot_scheduler_utils_test.py
```

---

## 设计原则

1. **零依赖** - 仅使用 Python 标准库
2. **类型安全** - 使用 dataclass 和 Enum
3. **可序列化** - 支持导出导入
4. **用户冲突检测** - 同一用户不能有重叠预约
5. **灵活调度** - 支持多种重复规则

---

## 更新日志

- **2026-04-27** - 初始版本
  - 核心调度功能
  - 重复规则支持
  - 数据导出导入
  - 30+ 测试用例

---

## 许可证

MIT License