# Sunrise/Sunset Calculator Utils

日出日落时间计算工具 - 纯 Python 实现，零外部依赖

## 功能特性

- ✅ 计算日出、日落、太阳正午时间
- ✅ 计算民用/航海/天文晨昏蒙影时间
- ✅ 计算黄金时刻（摄影最佳时间）
- ✅ 计算蓝调时刻（城市夜景摄影时间）
- ✅ 计算日照时长
- ✅ 计算太阳方位角和仰角
- ✅ 判断当前是否为白天
- ✅ 支持 15 个常用城市坐标
- ✅ 支持任意经纬度坐标
- ✅ 支持时区偏移

## 安装

```bash
# 无需安装，直接导入使用
from sunrise_sunset_utils import calculate_sunrise_sunset
```

## 快速开始

### 1. 使用城市名称获取太阳时间

```python
from sunrise_sunset_utils import get_sun_times_for_city
from datetime import date

# 获取北京今天的太阳时间
summary = get_sun_times_for_city('beijing')
print(f"日出: {summary['sunrise']}")
print(f"日落: {summary['sunset']}")
print(f"日照时长: {summary['day_length']}")

# 获取特定日期
summary = get_sun_times_for_city('tokyo', date(2024, 12, 25))
```

### 2. 使用坐标计算

```python
from sunrise_sunset_utils import calculate_sunrise_sunset
from datetime import date

# 计算上海日出日落
lat, lon = 31.2304, 121.4737  # 上海坐标
tz_offset = 8  # 北京时间 UTC+8

result = calculate_sunrise_sunset(lat, lon, date.today(), tz_offset)
if result:
    print(f"日出: {result['sunrise_str']}")
    print(f"日落: {result['sunset_str']}")
    print(f"正午: {result['solar_noon_str']}")
    print(f"日照时长: {result['day_length_str']}")
```

### 3. 获取完整时间摘要

```python
from sunrise_sunset_utils import get_sun_times_summary
from datetime import date

summary = get_sun_times_summary(
    latitude=39.9042,   # 北京纬度
    longitude=116.4074, # 北京经度
    target_date=date.today(),
    timezone_offset=8   # UTC+8
)

# 包含所有时间信息
print(summary)
# {
#   'date': '2024-06-21',
#   'sunrise': '04:45:xx',
#   'sunset': '19:4x:xx',
#   'solar_noon': '12:xx:xx',
#   'day_length': '14:xx:xx',
#   'civil_twilight': {'dawn': '04:1x:xx', 'dusk': '20:1x:xx'},
#   'nautical_twilight': {'dawn': '03:3x:xx', 'dusk': '20:5x:xx'},
#   'astronomical_twilight': {'dawn': '02:5x:xx', 'dusk': '21:3x:xx'},
#   'golden_hour': {'morning': '04:45:xx - 05:4x:xx', 'evening': '18:4x:xx - 19:4x:xx'},
#   'blue_hour': {'morning': '04:1x:xx - 04:3x:xx', 'evening': '19:5x:xx - 20:1x:xx'}
# }
```

### 4. 计算太阳位置

```python
from sunrise_sunset_utils import calculate_solar_position, is_daylight
from datetime import datetime

# 获取当前太阳位置
now = datetime.now()
pos = calculate_solar_position(
    latitude=39.9042,
    longitude=116.4074,
    dt=now,
    timezone_offset=8
)

print(f"太阳高度角: {pos['altitude']:.2f}°")
print(f"太阳方位角: {pos['azimuth']:.2f}°")

# 判断是否为白天
if is_daylight(39.9042, 116.4074, now, 8):
    print("现在是白天")
else:
    print("现在是夜晚")
```

### 5. 摄影黄金时刻

```python
from sunrise_sunset_utils import calculate_golden_hour, calculate_blue_hour
from datetime import date

# 黄金时刻 - 柔和温暖的光线，适合人像和风景摄影
golden = calculate_golden_hour(39.9042, 116.4074, date.today(), 8)
print(f"早晨黄金时刻: {golden['morning_start_str']} - {golden['morning_end_str']}")
print(f"傍晚黄金时刻: {golden['evening_start_str']} - {golden['evening_end_str']}")

# 蓝调时刻 - 深蓝色天空，适合城市夜景
blue = calculate_blue_hour(39.9042, 116.4074, date.today(), 8)
print(f"早晨蓝调时刻: {blue['morning_start_str']} - {blue['morning_end_str']}")
print(f"傍晚蓝调时刻: {blue['evening_start_str']} - {blue['evening_end_str']}")
```

### 6. 晨昏蒙影时间

```python
from sunrise_sunset_utils import (
    calculate_civil_twilight,
    calculate_nautical_twilight,
    calculate_astronomical_twilight
)
from datetime import date

# 民用晨昏蒙影 (太阳在地平线下 0°-6°)
# 此时地面物体仍清晰可见，适合户外活动
civil = calculate_civil_twilight(39.9042, 116.4074, date.today(), 8)
print(f"民用晨光: {civil['dawn_str']}")
print(f"民用昏影: {civil['dusk_str']}")

# 航海晨昏蒙影 (太阳在地平线下 6°-12°)
# 此时地平线仍可见，适合航海观测
nautical = calculate_nautical_twilight(39.9042, 116.4074, date.today(), 8)

# 天文晨昏蒙影 (太阳在地平线下 12°-18°)
# 此时天空完全黑暗，适合天文观测
astro = calculate_astronomical_twilight(39.9042, 116.4074, date.today(), 8)
```

## 支持的城市

| 城市名称 | 代码 |
|---------|------|
| 北京 | beijing |
| 上海 | shanghai |
| 广州 | guangzhou |
| 深圳 | shenzhen |
| 杭州 | hangzhou |
| 成都 | chengdu |
| 东京 | tokyo |
| 纽约 | new_york |
| 伦敦 | london |
| 巴黎 | paris |
| 悉尼 | sydney |
| 莫斯科 | moscow |
| 迪拜 | dubai |
| 新加坡 | singapore |
| 香港 | hong_kong |

```python
from sunrise_sunset_utils import get_sun_times_for_city

# 使用城市代码
summary = get_sun_times_for_city('tokyo')
summary = get_sun_times_for_city('new_york')
summary = get_sun_times_for_city('london')
```

## API 参考

### 主要函数

#### `calculate_sunrise_sunset(latitude, longitude, target_date, timezone_offset, altitude_deg)`
计算日出日落时间。

**参数:**
- `latitude` (float): 纬度，北纬为正
- `longitude` (float): 经度，东经为正
- `target_date` (date): 目标日期
- `timezone_offset` (float): 时区偏移（小时），如北京时间为 8
- `altitude_deg` (float): 太阳高度角阈值，默认 -0.833（考虑大气折射的标准日出日落）

**返回:** 字典或 None（极昼/极夜）

#### `calculate_golden_hour(latitude, longitude, target_date, timezone_offset)`
计算黄金时刻。

#### `calculate_blue_hour(latitude, longitude, target_date, timezone_offset)`
计算蓝调时刻。

#### `calculate_solar_position(latitude, longitude, dt, timezone_offset)`
计算指定时刻的太阳位置。

**返回:**
- `altitude`: 太阳高度角（度）
- `azimuth`: 太阳方位角（度，正北为 0°）
- `declination`: 太阳赤纬
- `right_ascension`: 太阳赤经

#### `is_daylight(latitude, longitude, dt, timezone_offset)`
判断指定时刻是否为白天。

#### `get_sun_times_summary(latitude, longitude, target_date, timezone_offset)`
获取完整的太阳时间摘要。

#### `get_sun_times_for_city(city_name, target_date)`
根据城市名称获取太阳时间。

## 算法说明

本模块基于 Jean Meeus 的天文算法实现，使用以下公式：

1. **儒略日计算** - 将日期转换为儒略日
2. **太阳平均近点角** - 计算太阳位置
3. **黄道经度** - 太阳在黄道上的位置
4. **太阳赤纬** - 太阳在天球上的纬度
5. **时差方程** - 太阳时与本地时间的差值
6. **时角计算** - 太阳与当地子午线的角度

## 注意事项

1. **极昼极夜** - 在极地区域，夏季可能出现极昼（太阳不落下），冬季可能出现极夜（太阳不升起），此时函数返回 None。

2. **精度** - 计算精度约为 ±1 分钟，满足日常使用需求。对于天文研究等高精度需求，建议使用专业天文软件。

3. **时区** - 请确保传入正确的时区偏移，否则计算结果会有偏差。

## 运行测试

```bash
python sunrise_sunset_utils_test.py
```

## 许可证

MIT License