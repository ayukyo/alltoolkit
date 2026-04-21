# Solar Utils - 日出日落时间计算工具

**零依赖的天文计算模块，精确计算日出、日落、正午、曙暮光时间**

## ✨ 功能特性

- 🌅 **日出日落计算** - 基于经纬度和日期，精度可达分钟级
- ☀️ **太阳正午** - 计算地方视午时间
- 🕐 **曙暮光时间** - 民用、航海、天文三种类型
- 📐 **太阳位置** - 方位角和高度角计算
- 📊 **白昼时长** - 计算白天持续时间
- 📸 **黄金时刻** - 摄影最佳时段计算
- 🌍 **季节判断** - 基于太阳黄经的季节相位
- ⚡ **极昼极夜** - 自动处理极端情况

## 📦 零依赖

仅使用 Python 标准库：
- `math` - 数学运算
- `datetime` - 时间处理

## 🚀 快速开始

```python
from solar_utils.mod import get_sunrise, get_sunset, get_solar_info

# 计算北京日出时间
sunrise = get_sunrise(39.9042, 116.4074, date(2024, 6, 21), timezone=8.0)
print(sunrise.strftime('%H:%M'))  # 04:46

# 获取完整太阳信息
info = get_solar_info(39.9042, 116.4074, date(2024, 6, 21), timezone=8.0)
print(f"日出: {info['sunrise'].strftime('%H:%M')}")
print(f"日落: {info['sunset'].strftime('%H:%M')}")
print(f"白昼时长: {info['day_length_hours']:.2f} 小时")
```

## 📖 详细用法

### 日出日落计算

```python
from datetime import date
from solar_utils.mod import get_sunrise, get_sunset

# 基本用法
sunrise = get_sunrise(latitude, longitude, date_obj, timezone)
sunset = get_sunset(latitude, longitude, date_obj, timezone)

# 北京 2024年夏至
sunrise = get_sunrise(39.9042, 116.4074, date(2024, 6, 21), timezone=8.0)
# 返回: datetime(2024, 6, 21, 4, 46, xx)

# 参数说明：
# latitude - 纬度（度），正为北纬
# longitude - 经度（度），正为东经
# date_obj - 日期对象，默认为今天
# timezone - 时区（小时），东经为正，默认为0
# elevation - 海拔高度（米），可选
```

### 正午时间计算

```python
from solar_utils.mod import get_solar_noon

noon = get_solar_noon(longitude, date(2024, 6, 21), timezone=8.0)
print(noon.strftime('%H:%M'))  # 约 12:16（北京）
```

### 白昼时长计算

```python
from solar_utils.mod import get_day_length

day_len = get_day_length(39.9042, 116.4074, date(2024, 6, 21))
print(f"{day_len.total_seconds() / 3600:.1f} 小时")  # 约15小时
```

### 曙暮光时间

```python
from solar_utils.mod import get_twilight_times

# 民用曙暮光（太阳在地平线下6°）
civil = get_twilight_times(39.9042, 116.4074, date(2024, 6, 21), timezone=8.0, twilight_type='civil')

# 航海曙暮光（太阳在地平线下12°）
nautical = get_twilight_times(..., twilight_type='nautical')

# 天文曙暮光（太阳在地平线下18°）
astronomical = get_twilight_times(..., twilight_type='astronomical')

# 返回: {'dawn': datetime, 'dusk': datetime}
```

### 太阳位置计算

```python
from datetime import datetime
from solar_utils.mod import get_solar_position

pos = get_solar_position(39.9042, 116.4074, datetime(2024, 6, 21, 12, 0), timezone=8.0)
print(f"方位角: {pos['azimuth']:.1f}°")  # 正北为0°，顺时针增加
print(f"高度角: {pos['altitude']:.1f}°")  # 地平线为0°
```

### 黄金时刻计算

```python
from solar_utils.mod import get_golden_hour

golden = get_golden_hour(39.9042, 116.4074, date(2024, 6, 21), timezone=8.0)
print(f"早晨: {golden['morning_start'].strftime('%H:%M')} - {golden['morning_end'].strftime('%H:%M')}")
print(f"傍晚: {golden['evening_start'].strftime('%H:%M')} - {golden['evening_end'].strftime('%H:%M')}")
```

### 综合信息获取

```python
from solar_utils.mod import get_solar_info

info = get_solar_info(39.9042, 116.4074, date(2024, 6, 21), timezone=8.0)

# 返回完整信息：
# {
#   'sunrise': datetime,
#   'sunset': datetime,
#   'solar_noon': datetime,
#   'day_length': timedelta,
#   'day_length_hours': float,
#   'civil_twilight': {'dawn': datetime, 'dusk': datetime},
#   'nautical_twilight': {'dawn': datetime, 'dusk': datetime},
#   'astronomical_twilight': {'dawn': datetime, 'dusk': datetime},
#   'golden_hour': {...},
#   'solar_noon_altitude': float,  # 正午太阳高度角
#   'declination': float  # 太阳赤纬
# }
```

### 白天判断

```python
from solar_utils.mod import is_daylight

# 判断当前是否为白天
is_day = is_daylight(39.9042, 116.4074, datetime.now(), timezone=8.0)
print(is_day)  # True 或 False
```

### 季节判断

```python
from solar_utils.mod import get_sun_phase

# 北半球季节
season = get_sun_phase(date(2024, 6, 21), hemisphere='north')
print(season)  # 'summer'

# 南半球季节相反
season = get_sun_phase(date(2024, 6, 21), hemisphere='south')
print(season)  # 'winter'
```

## 🌍 世界城市坐标示例

| 城市 | 纬度 | 经度 | 时区 |
|------|------|------|------|
| 北京 | 39.9042 | 116.4074 | +8 |
| 上海 | 31.2304 | 121.4737 | +8 |
| 广州 | 23.1291 | 113.2644 | +8 |
| 东京 | 35.6762 | 139.6503 | +9 |
| 新加坡 | 1.3521 | 103.8198 | +8 |
| 悉尼 | -33.8688 | 151.2093 | +10 |
| 纽约 | 40.7128 | -74.0060 | -5 |
| 伦敦 | 51.5074 | -0.1278 | +0/+1 |

## 🧮 算法说明

### 计算方法

本模块采用 NOAA（美国国家海洋和大气管理局）推荐的简化天文算法：

1. **儒略日计算** - 将日期转换为儒略日
2. **太阳黄经** - 计算太阳在黄道上的位置
3. **太阳赤纬** - 从太阳黄经计算赤纬
4. **时差** - 计算真太阳时与平太阳时的差异
5. **时角** - 根据太阳高度角计算时角
6. **时间转换** - 从时角转换为本地时间

### 精度说明

- **日出日落时间**：精度约 ±2-5 分钟
- **太阳位置**：方位角精度约 ±1°，高度角精度约 ±0.5°
- **正午时间**：精度约 ±1 分钟

精度受以下因素影响：
- 大气折射（温度、气压）
- 观测海拔
- 太阳视半径变化

### 极端情况处理

- **极昼**：高纬度夏季，返回合理的日出日落时间或极昼状态
- **极夜**：高纬度冬季，返回 `None`
- **跨午夜**：自动处理日期跨越

## 🧪 测试覆盖

测试套件包含 80+ 测试用例，覆盖：

- ✅ 儒略日计算验证
- ✅ 太阳赤纬范围验证
- ✅ 时差极值验证
- ✅ 多城市日出日落精度验证
- ✅ 赤道地区测试
- ✅ 极地测试
- ✅ 曙暮光时间顺序验证
- ✅ 白昼时长验证
- ✅ 季节相位验证
- ✅ 边界值测试（极端经纬度、时区）
- ✅ 跨年、闰年测试

```bash
# 运行测试
python solar_utils_test.py
```

## 📚 参考资料本模块算法基于以下资料简化实现：

- NOAA Solar Calculator
- Jean Meeus - "Astronomical Algorithms"
- USNO (美国海军天文台) 数据

## 🔗 相关模块

- `datetime_utils` - 日期时间处理
- `time_zone_utils` - 时区转换
- `geo_utils` - 地理坐标计算

## 📄 许可证

MIT License

---

**最后更新**: 2026-04-21
**版本**: 1.0.0