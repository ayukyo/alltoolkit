# work_hours_utils - 工作时长计算工具

提供工作时间相关的计算功能，零外部依赖。

## 功能特性

- **工作时长计算** - 考虑午休时间的精确工作时长计算
- **加班时间计算** - 区分工作日/周末/节假日加班
- **周工作时间统计** - 按周汇总工作时间
- **弹性工作时间计算** - 支持弹性工作制
- **打卡记录分析** - 分析打卡数据生成工时报告
- **工时合规检查** - 检查是否符合劳动法规要求

## 主要类

### WorkDayType
工作日类型枚举：
- `WEEKDAY` - 普通工作日
- `WEEKEND` - 周末
- `HOLIDAY` - 法定节假日
- `REST_DAY` - 休息日（如调休）

### OvertimeType
加班类型枚举：
- `WEEKDAY_OVERTIME` - 工作日加班
- `WEEKEND_OVERTIME` - 周末加班
- `HOLIDAY_OVERTIME` - 法定节假日加班
- `NIGHT_OVERTIME` - 夜班加班

### TimeSlot
时间段类，支持跨天时间段计算。

### WorkShift
工作班次类，包含工作时间段。

### PunchRecord
打卡记录类，记录上班打卡时间。

### WorkHoursCalculator
主要计算器类，提供完整的工时计算功能。

## 使用示例

```python
from work_hours_utils import WorkHoursCalculator, WorkShift, TimeSlot
from datetime import time

# 创建标准班次
standard_shift = WorkShift(
    name="标准班次",
    work_periods=[
        TimeSlot(time(9, 0), time(12, 0)),   # 上午
        TimeSlot(time(13, 30), time(18, 0)), # 下午
    ]
)

# 创建计算器
calc = WorkHoursCalculator(standard_shift=standard_shift)

# 计算日工作时长
hours = calc.calculate_daily_hours(check_in=time(9, 0), check_out=time(18, 30))
print(f"工作时长: {hours} 小时")
```

## API 参考

### calculate_daily_hours()
计算每日工作时长。

### calculate_weekly_hours()
计算周工作时间。

### calculate_overtime()
计算加班时间，区分不同加班类型。

### check_compliance()
检查工时是否合规。

## 测试

运行测试：
```bash
python work_hours_utils/work_hours_utils_test.py
```

测试覆盖率：34 个测试用例，100% 通过。

---

*最后更新: 2026-05-26*