# AllToolkit - Python Time Zone Utils 🌍

**零依赖时区转换工具 - 功能完整的生产就绪工具**

---

## 📖 概述

`time_zone_utils` 提供全面的时区处理功能，包括时区转换、UTC 偏移计算、夏令时检测、时区列表查询和会议时间查找。完全使用 Python 标准库实现（datetime 和 zoneinfo 模块），无需任何外部依赖。

**要求**: Python 3.9+（需要 zoneinfo 模块支持）

---

## ✨ 特性

- **时区转换** - 支持全球所有 IANA 时区，处理夏令时自动调整
- **UTC 偏移计算** - 获取任意时区在特定时间的 UTC 偏移
- **夏令时检测** - 判断某时区在指定时间是否处于夏令时
- **时区信息查询** - 获取时区详细信息，包括当前时间、偏移、夏令时状态
- **会议时间查找** - 自动计算多个时区的工作时间交集
- **时差计算** - 计算两个时区之间的小时差
- **时间运算** - 在指定时区中添加/减去时间
- **日期比较** - 判断两个时间在某时区是否为同一天

---

## 🚀 快速开始

### 基础时区转换

```python
from mod import convert_time, convert_time_string
from datetime import datetime

# 转换 datetime 对象
dt = datetime(2026, 4, 10, 16, 0, 0)  # 下午 4 点上海时间
converted = convert_time(dt, "Asia/Shanghai", "UTC")
print(f"UTC 时间：{converted}")  # 08:00:00

# 转换时间字符串
time_str = convert_time_string("2026-04-10 16:00:00", "Asia/Shanghai", "UTC")
print(f"UTC 字符串：{time_str}")  # 2026-04-10 08:00:00

# 自定义格式
time_str = convert_time_string(
    "10/04/2026 16:00", "Asia/Shanghai", "UTC",
    format_str="%d/%m/%Y %H:%M"
)
print(f"自定义格式：{time_str}")  # 10/04/2026 08:00
```

### 获取 UTC 偏移

```python
from mod import get_utc_offset_hours, get_utc_offset
from datetime import datetime

# 获取当前偏移
offset = get_utc_offset_hours("Asia/Shanghai")
print(f"上海 UTC 偏移：{offset}")  # 8.0

# 获取特定日期的偏移（考虑夏令时）
jan_dt = datetime(2026, 1, 15)
jul_dt = datetime(2026, 7, 15)

offset_jan = get_utc_offset_hours("America/New_York", jan_dt)
offset_jul = get_utc_offset_hours("America/New_York", jul_dt)
print(f"纽约 1 月偏移：{offset_jan}")  # -5.0 (标准时间)
print(f"纽约 7 月偏移：{offset_jul}")  # -4.0 (夏令时)
```

### 夏令时检测

```python
from mod import is_dst, get_dst_info
from datetime import datetime

# 检测夏令时
print(is_dst("Asia/Shanghai", datetime(2026, 7, 15)))  # False (中国无夏令时)
print(is_dst("America/New_York", datetime(2026, 1, 15)))  # False (冬季)
print(is_dst("America/New_York", datetime(2026, 7, 15)))  # True (夏季)

# 获取完整 DST 信息
info = get_dst_info("America/New_York", 2026)
print(f"是否有夏令时：{info['has_dst']}")
print(f"标准时间偏移：{info['offset_std']}")
print(f"夏令时偏移：{info['offset_dst']}")
print(f"开始日期：{info['start_date']}")
print(f"结束日期：{info['end_date']}")
```

### 时区信息查询

```python
from mod import get_timezone_info, list_timezones, get_common_timezones

# 获取时区详细信息
info = get_timezone_info("Asia/Shanghai")
print(f"时区：{info['name']}")
print(f"当前时间：{info['current_time']}")
print(f"UTC 偏移：{info['utc_offset']}")
print(f"是否夏令时：{info['is_dst']}")

# 列出所有时区
all_timezones = list_timezones()
print(f"总时区数：{len(all_timezones)}")  # 500+

# 过滤时区
asia_timezones = list_timezones("Asia")
print(f"亚洲时区数：{len(asia_timezones)}")

# 常用时区
common = get_common_timezones()
print(f"中国时区：{common['China']}")  # Asia/Shanghai
print(f"纽约时区：{common['New York']}")  # America/New_York
```

### 会议时间查找

```python
from mod import find_meeting_times
from datetime import datetime

# 查找上海和伦敦的会议时间
times = find_meeting_times(
    ["Asia/Shanghai", "Europe/London"],
    work_start=9,  # 9 点上班
    work_end=18,   # 18 点下班
    date=datetime(2026, 4, 10)
)

print(f"找到 {len(times)} 个合适的会议时间:")
for slot in times[:3]:  # 显示前 3 个
    print(f"  UTC {slot['utc_time']}:")
    for tz, local_time in slot['times'].items():
        print(f"    {tz}: {local_time}")

# 查找纽约和东京的会议时间（时差大，选择少）
times = find_meeting_times(
    ["America/New_York", "Asia/Tokyo"],
    work_start=9, work_end=18
)
print(f"纽约 - 东京会议时间：{len(times)} 个")
```

### 时差计算

```python
from mod import time_difference_hours

# 计算时差
diff = time_difference_hours("UTC", "Asia/Shanghai")
print(f"上海比 UTC 快：{diff} 小时")  # 8.0

diff = time_difference_hours("America/New_York", "America/Los_Angeles")
print(f"纽约比洛杉矶快：{diff} 小时")  # 3.0

# 特殊时区（半小时偏移）
diff = time_difference_hours("UTC", "Asia/Kolkata")
print(f"印度比 UTC 快：{diff} 小时")  # 5.5

# 特殊时区（15 分钟偏移）
diff = time_difference_hours("UTC", "Asia/Kathmandu")
print(f"尼泊尔比 UTC 快：{diff} 小时")  # 5.75
```

### 当前时间查询

```python
from mod import now_in_timezone, format_for_timezone

# 获取当前时间
now_sh = now_in_timezone("Asia/Shanghai")
print(f"上海当前时间：{now_sh}")

now_ny = now_in_timezone("America/New_York")
print(f"纽约当前时间：{now_ny}")

# 格式化输出
from datetime import datetime
utc_dt = datetime(2026, 4, 10, 8, 0, 0, tzinfo=ZoneInfo("UTC"))
formatted = format_for_timezone(utc_dt, "Asia/Shanghai")
print(f"格式化时间：{formatted}")  # 2026-04-10 16:00:00

# 自定义格式
formatted = format_for_timezone(
    utc_dt, "Asia/Shanghai",
    format_str="%Y/%m/%d %H:%M %Z"
)
print(f"自定义格式：{formatted}")
```

### 时间解析和运算

```python
from mod import parse_timezone_aware, add_time_in_timezone, is_same_day
from datetime import datetime

# 解析带时区的时间
dt = parse_timezone_aware("2026-04-10 16:00:00", "Asia/Shanghai")
print(f"解析结果：{dt}")  # 带时区信息的 datetime

# 添加时间
dt = datetime(2026, 4, 10, 10, 0, 0)
new_dt = add_time_in_timezone(dt, "Asia/Shanghai", hours=5)
print(f"5 小时后：{new_dt}")  # 15:00:00

new_dt = add_time_in_timezone(dt, "Asia/Shanghai", days=3)
print(f"3 天后：{new_dt}")  # April 13

# 跨月计算
dt = datetime(2026, 4, 28, 10, 0, 0)
new_dt = add_time_in_timezone(dt, "Asia/Shanghai", days=5)
print(f"跨月结果：{new_dt}")  # May 3

# 判断是否同一天
dt1 = datetime(2026, 4, 10, 10, 0, 0, tzinfo=ZoneInfo("Asia/Shanghai"))
dt2 = datetime(2026, 4, 10, 20, 0, 0, tzinfo=ZoneInfo("Asia/Shanghai"))
print(f"是否同一天：{is_same_day(dt1, dt2, 'Asia/Shanghai')}")  # True

# 跨时区同一天判断
dt1 = datetime(2026, 4, 10, 23, 0, 0, tzinfo=ZoneInfo("UTC"))
dt2 = datetime(2026, 4, 11, 7, 0, 0, tzinfo=ZoneInfo("Asia/Shanghai"))
print(f"UTC 同一天：{is_same_day(dt1, dt2, 'UTC')}")  # False
```

---

## 📋 API 参考

### 异常类

| 异常 | 说明 |
|------|------|
| `TimeZoneError` | 时区操作基础异常 |
| `InvalidTimeZoneError` | 无效时区标识符 |
| `InvalidTimeError` | 无效时间值 |

### 核心函数

| 函数 | 说明 |
|------|------|
| `convert_time(dt, from_tz, to_tz)` | 转换 datetime 对象时区 |
| `convert_time_string(time_str, from_tz, to_tz, format_str)` | 转换时间字符串 |
| `get_utc_offset(timezone, dt)` | 获取 UTC 偏移 (timedelta) |
| `get_utc_offset_hours(timezone, dt)` | 获取 UTC 偏移 (小时) |
| `is_dst(timezone, dt)` | 检测夏令时 |
| `get_dst_info(timezone, year)` | 获取 DST 详细信息 |
| `list_timezones(filter_str)` | 列出所有时区 |
| `get_timezone_info(timezone)` | 获取时区详细信息 |
| `get_common_timezones()` | 获取常用时区字典 |
| `find_meeting_times(timezones, work_start, work_end, date)` | 查找会议时间 |
| `time_difference_hours(tz1, tz2, dt)` | 计算时差 |
| `now_in_timezone(timezone)` | 获取当前时间 |
| `format_for_timezone(dt, timezone, format_str)` | 格式化时间 |
| `parse_timezone_aware(time_str, timezone, format_str)` | 解析带时区时间 |
| `is_same_day(dt1, dt2, timezone)` | 判断是否同一天 |
| `add_time_in_timezone(dt, timezone, days, hours, minutes, seconds)` | 添加时间 |

---

## 🧪 测试

运行测试套件：

```bash
cd /home/admin/.openclaw/workspace/AllToolkit/Python/time_zone_utils
python time_zone_utils_test.py
```

### 测试覆盖

测试套件包含 **45+ 个测试用例**，覆盖：

- ✅ 基础时区转换
- ✅ 字符串时间转换
- ✅ UTC 偏移计算
- ✅ 夏令时检测（不同半球）
- ✅ DST 信息获取
- ✅ 时区列表和过滤
- ✅ 会议时间查找
- ✅ 时差计算
- ✅ 特殊时区（半小时、15 分钟偏移）
- ✅ 边界情况（午夜、年末、闰年）
- ✅ 错误处理（无效时区、无效时间）

---

## 🌐 支持的时区

支持所有 IANA 时区数据库中的时区（500+），包括：

### 亚洲
- `Asia/Shanghai` - 中国标准时间 (UTC+8)
- `Asia/Tokyo` - 日本标准时间 (UTC+9)
- `Asia/Seoul` - 韩国标准时间 (UTC+9)
- `Asia/Singapore` - 新加坡时间 (UTC+8)
- `Asia/Hong_Kong` - 香港时间 (UTC+8)
- `Asia/Taipei` - 台北时间 (UTC+8)
- `Asia/Kolkata` - 印度标准时间 (UTC+5:30)
- `Asia/Dubai` - 阿联酋时间 (UTC+4)
- `Asia/Bangkok` - 泰国时间 (UTC+7)

### 欧洲
- `Europe/London` - 英国时间 (UTC+0/UTC+1)
- `Europe/Paris` - 法国时间 (UTC+1/UTC+2)
- `Europe/Berlin` - 德国时间 (UTC+1/UTC+2)
- `Europe/Moscow` - 莫斯科时间 (UTC+3)

### 美洲
- `America/New_York` - 美国东部时间 (UTC-5/UTC-4)
- `America/Chicago` - 美国中部时间 (UTC-6/UTC-5)
- `America/Los_Angeles` - 美国太平洋时间 (UTC-8/UTC-7)
- `America/Toronto` - 加拿大东部时间 (UTC-5/UTC-4)
- `America/Sao_Paulo` - 巴西时间 (UTC-3)
- `America/Mexico_City` - 墨西哥时间 (UTC-6/UTC-5)

### 大洋洲
- `Australia/Sydney` - 悉尼时间 (UTC+10/UTC+11)
- `Australia/Melbourne` - 墨尔本时间 (UTC+10/UTC+11)
- `Pacific/Auckland` - 奥克兰时间 (UTC+12/UTC+13)

### 特殊时区
- `UTC` - 协调世界时
- `Asia/Kathmandu` - 尼泊尔时间 (UTC+5:45)
- `Pacific/Honolulu` - 夏威夷时间 (UTC-10)
- `Pacific/Chatham` - 查塔姆时间 (UTC+12:45/UTC+13:45)

---

## 💡 实用示例

### 示例 1：全球团队会议安排

```python
from mod import find_meeting_times, get_common_timezones
from datetime import datetime

# 全球团队时区
team_timezones = [
    "Asia/Shanghai",      # 中国团队
    "Europe/London",      # 英国团队
    "America/New_York",   # 美国东岸团队
]

# 查找合适的会议时间
times = find_meeting_times(
    team_timezones,
    work_start=9,
    work_end=18,
    date=datetime.now()
)

if times:
    print("找到以下会议时间:")
    for slot in times:
        print(f"\nUTC {slot['utc_time']}:")
        for tz, local_time in slot['times'].items():
            print(f"  {tz}: {local_time}")
else:
    print("没有合适的工作时间交集，考虑调整工作时间或使用录播")
```

### 示例 2：日志时间标准化

```python
from mod import format_for_timezone, parse_timezone_aware
from datetime import datetime

# 将不同地区的日志时间统一转换为 UTC
log_entries = [
    ("2026-04-10 16:00:00", "Asia/Shanghai"),
    ("2026-04-10 09:00:00", "Europe/London"),
    ("2026-04-10 04:00:00", "America/New_York"),
]

for time_str, tz in log_entries:
    dt = parse_timezone_aware(time_str, tz)
    utc_time = format_for_timezone(dt, "UTC", "%Y-%m-%d %H:%M:%S")
    print(f"{tz}: {time_str} -> UTC: {utc_time}")
```

### 示例 3：航班时间计算

```python
from mod import convert_time, add_time_in_timezone
from datetime import datetime

# 航班信息：上海飞往纽约，飞行时间 14 小时
departure = datetime(2026, 4, 10, 12, 0, 0)  # 中午 12 点上海起飞
flight_hours = 14

# 计算到达时间（上海时区）
arrival_sh = add_time_in_timezone(departure, "Asia/Shanghai", hours=flight_hours)

# 转换为纽约当地时间
arrival_ny = convert_time(arrival_sh, "Asia/Shanghai", "America/New_York")

print(f"起飞：上海 {departure.strftime('%Y-%m-%d %H:%M')}")
print(f"到达：纽约 {arrival_ny.strftime('%Y-%m-%d %H:%M')}")
```

### 示例 4：定时任务调度

```python
from mod import now_in_timezone, convert_time
from datetime import datetime

# 检查当前时间是否在执行窗口内（避免打扰用户）
def is_within_quiet_hours(user_timezone: str, quiet_start: int = 22, quiet_end: int = 8) -> bool:
    """检查用户时区是否处于安静时段"""
    now = now_in_timezone(user_timezone)
    hour = now.hour
    return hour >= quiet_start or hour < quiet_end

# 使用
if is_within_quiet_hours("Asia/Shanghai"):
    print("用户在休息，推迟通知")
else:
    print("可以发送通知")
```

---

## ⚠️ 注意事项

1. **Python 版本要求**: 需要 Python 3.9+（zoneinfo 模块在 3.9 引入）
2. **时区数据库**: 使用系统 IANA 时区数据库，确保系统时区数据是最新的
3. **夏令时规则**: 夏令时规则可能变化，建议使用最新系统更新
4. **历史时间**: 对于历史时间（如 1970 年前），时区规则可能不准确
5. **未来时间**: 未来夏令时规则可能调整，结果仅供参考

---

## 📄 许可证

MIT License

---

## 🔗 相关链接

- [IANA 时区数据库](https://www.iana.org/time-zones)
- [Python zoneinfo 文档](https://docs.python.org/3/library/zoneinfo.html)
- [世界时区地图](https://en.wikipedia.org/wiki/List_of_UTC_time_offsets)

---

**最后更新**: 2026-04-10
