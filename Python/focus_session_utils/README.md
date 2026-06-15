# Focus Session Utils 🎯

专注时间跟踪工具，支持番茄钟模式和专注数据分析。

## 特性

- ✅ **番茄钟** - 25/5 经典模式
- ✅ **会话追踪** - 记录专注时长
- ✅ **每日报告** - 统计每日专注情况
- ✅ **最佳时段** - 分析高效专注时段
- ✅ **零依赖** - 仅使用 Python 标准库

## 快速开始

```python
from focus_session_utils import FocusSession, FocusReport

# 创建会话
session = FocusSession(duration_minutes=25)
session.start()
session.complete()

# 获取报告
report = session.get_report()
print(f"专注时长: {report.total_minutes} 分钟")
print(f"完成率: {report.completion_rate}%")
```
