# Moon Phase Utils

月相计算工具模块 - 提供完整的月相计算、照明百分比、相位名称等功能。

## 核心功能

### 基础计算
- `get_moon_age()` - 计算月龄（天数）
- `get_illumination()` - 计算照明百分比（0-100%）
- `get_phase_index()` - 获取相位索引（0-7）
- `get_phase_name()` - 获取相位名称（支持中英文）
- `get_moon_phase()` - 获取 MoonPhase 枚举值
- `is_major_phase()` - 检测是否为主要相位

### 主要相位计算
- `get_next_new_moon()` - 计算下一个新月日期
- `get_next_full_moon()` - 计算下一个满月日期
- `get_next_first_quarter()` - 计算下一个上弦月日期
- `get_next_last_quarter()` - 计算下一个下弦月日期

### 月历生成
- `get_moon_phases_in_month()` - 获取月内主要相位
- `get_moon_calendar()` - 生成本月月相日历

### 特殊现象检测
- `get_blue_moon_info()` - 蓝月检测（一个月内第二次满月）
- `is_super_moon()` - 超级月亮检测
- `calculate_moon_distance()` - 计算月球距离
- `get_lunar_eclipse_risk()` - 月食风险评估

### 其他功能
- `get_moon_rise_set()` - 月出/月落时间（近似值）
- `get_moon_info()` - 综合月相信息
- `get_moon_emoji()` - 月相 Emoji
- `print_moon_info()` - 打印格式化月相信息

## 月相索引说明

| 索引 | 英文名称 | 中文名称 | Emoji |
|------|----------|----------|-------|
| 0 | New Moon | 新月 | 🌑 |
| 1 | Waxing Crescent | 蛾眉月 | 🌒 |
| 2 | First Quarter | 上弦月 | 🌓 |
| 3 | Waxing Gibbous | 盈凸月 | 🌓 |
| 4 | Full Moon | 满月 | 🌕 |
| 5 | Waning Gibbous | 亏凸月 | 🌖 |
| 6 | Last Quarter | 下弦月 | 🌗 |
| 7 | Waning Crescent | 残月 | 🌘 |

## 使用示例

### 基础使用

```python
from moon_phase_utils import get_phase_name, get_moon_emoji, get_illumination

# 获取当前月相
print(f"当前月相: {get_phase_name()} {get_moon_emoji()}")
print(f"照明度: {get_illumination():.1f}%")
```

### 中文支持

```python
from moon_phase_utils import get_phase_name, get_moon_info

# 获取中文月相名称
print(f"月相: {get_phase_name(language='cn')}")

# 获取完整中文信息
info = get_moon_info(language="cn")
print(f"月相: {info['phase_name']}")
print(f"月龄: {info['moon_age_days']} 天")
```

### 计算未来相位

```python
from moon_phase_utils import get_next_full_moon, get_next_new_moon

# 下一个满月
full_moon = get_next_full_moon()
print(f"下一个满月: {full_moon.strftime('%Y-%m-%d')}")

# 下一个新月
new_moon = get_next_new_moon()
print(f"下一个新月: {new_moon.strftime('%Y-%m-%d')}")
```

### 生成月历

```python
from moon_phase_utils import get_moon_calendar

# 生成2024年7月月相日历
calendar = get_moon_calendar(2024, 7)
for day in calendar:
    print(f"{day['date']}: {day['phase_name']} ({day['illumination']:.0f}%)")
```

### 蓝月检测

```python
from moon_phase_utils import get_blue_moon_info

info = get_blue_moon_info(2024)
if info['has_blue_moon']:
    for bm in info['blue_moons']:
        print(f"蓝月出现在 {bm['month_name']}: {bm['blue_moon']}")
```

### 超级月亮检测

```python
from moon_phase_utils import is_super_moon, calculate_moon_distance

if is_super_moon():
    print("🌟 当前是超级月亮！")
    
distance = calculate_moon_distance()
print(f"月球距离: {distance:,.0f} km")
```

## 技术说明

### 计算方法

- 基于 J2000.0 天文参考历元（2000年1月6日新月）
- 使用平均朔望月周期（29.530588853 天）
- 照明计算基于相位角的余弦函数

### 精度

- 月龄计算精度：约 0.5 天误差
- 照明度精度：约 3% 误差
- 适用于一般用途，不适用于精确天文观测

### 注意事项

- `get_moon_rise_set()` 提供近似值，实际时间受观测位置影响
- `get_lunar_eclipse_risk()` 仅提供概率评估，非精确预测
- 超级月亮检测使用简化阈值（360,000 km）

## 运行测试

```bash
python moon_phase_utils_test.py
```

## 运行示例

```bash
python examples.py
```

## 零外部依赖

本模块仅使用 Python 标准库：
- `datetime` - 日期时间处理
- `math` - 数学计算
- `enum` - 枚举类型
- `typing` - 类型提示

## License

MIT License - AllToolkit