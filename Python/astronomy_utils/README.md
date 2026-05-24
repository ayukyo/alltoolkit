# astronomy_utils - 天文学工具

提供天文学计算功能：太阳系行星数据、星座数据、恒星数据、月相计算、儒略日转换、天体升起/落下时间、坐标转换等。

## 功能特性

- 🪐 **太阳系数据**: 包含8大行星、矮行星、太阳和月球的详细信息
- 🌌 **星座数据**: 黄道十二宫和北半球常见星座信息
- ⭐ **恒星数据**: 20颗最亮恒星的位置、距离、星等数据
- 🌙 **月相计算**: 计算任意日期的月相，预测下一个月相
- 📅 **儒略日转换**: 日期与儒略日的双向转换
- 🧭 **坐标转换**: 赤道坐标与地平坐标转换
- 🌅 **升起落下**: 计算天体在给定位置的升起、中天、落下时间
- 🚀 **距离计算**: 天文单位、光年、光传播时间等计算
- 📐 **角直径**: 计算天体的角直径

## 安装

```python
from astronomy_utils.mod import (
    get_planet, get_all_planets, get_constellation,
    calculate_moon_phase, get_star_info
)
```

## 快速开始

### 太阳系行星

```python
from mod import get_planet, get_all_planets

# 获取单个行星（支持中英文名）
mars = get_planet("火星")
print(mars.name_cn)        # "火星"
print(mars.moons)          # 2
print(mars.distance_au)    # 1.524

# 获取所有行星
planets = get_all_planets()
for planet in planets:
    print(f"{planet.name_cn}: {planet.moons}颗卫星")
```

### 星座数据

```python
from mod import get_constellation, get_zodiac_constellations

# 获取星座（支持中文名、英文名、缩写）
leo = get_constellation("狮子座")
print(leo.name)            # "Leo"
print(leo.brightest_star)  # "轩辕十四"

# 获取黄道十二宫
zodiac = get_zodiac_constellations()
for c in zodiac:
    print(f"{c.name_cn}: 最佳观测月份 {c.best_month}")
```

### 月相计算

```python
from mod import calculate_moon_phase
from datetime import datetime

# 计算当前月相
moon_age, phase_idx, name_cn, name_en = calculate_moon_phase()
print(f"月龄: {moon_age:.1f}天")
print(f"月相: {name_cn} ({name_en})")

# 计算特定日期的月相
dt = datetime(2024, 6, 15, 20, 0, 0)
moon_age, _, name_cn, _ = calculate_moon_phase(dt)
print(f"2024年6月15日: {name_cn}")
```

### 恒星数据

```python
from mod import get_star_info, StarData

# 获取恒星信息（支持中英文名）
sirius = get_star_info("天狼星")
print(sirius["magnitude"])     # -1.46
print(sirius["distance_ly"])   # 8.6光年
print(sirius["color"])         # "白色"

# 获取在给定纬度可见的恒星
visible_stars = StarData.get_visible_stars(39.9)  # 北京纬度
for star in visible_stars[:5]:
    print(f"{star['name_cn']}: 星等 {star['magnitude']}")
```

### 儒略日转换

```python
from mod import date_to_julian_day, julian_day_to_date
from datetime import datetime

# 日期转儒略日
dt = datetime(2024, 6, 15, 20, 0, 0)
jd = date_to_julian_day(dt)
print(f"儒略日: {jd}")

# 儒略日转日期
dt2 = julian_day_to_date(jd)
print(dt2)  # 2024-06-15 20:00:00
```

### 距离计算

```python
from mod import au_to_km, km_to_light_year, calculate_light_travel_time

# 天文单位转千米
distance_km = au_to_km(1.0)  # 地球到太阳
print(f"{distance_km:.1f} km")

# 千米转光年
ly = km_to_light_year(9.461e12)
print(f"{ly:.2f} 光年")

# 光传播时间（地球到太阳约8分20秒）
time = calculate_light_travel_time(149597870.7)
print(f"{time.total_seconds():.0f} 秒")
```

### 高级计算

```python
from mod import AstronomyCalculator, SolarSystemData, MoonPhaseCalculator
from datetime import datetime

# 赤道坐标转地平坐标
ra, dec = 101.29, -16.72  # 天狼星
latitude, longitude = 39.9, 116.4  # 北京
dt = datetime(2024, 6, 15, 20, 0, 0)

az, alt = AstronomyCalculator.equatorial_to_horizontal(ra, dec, latitude, longitude, dt)
print(f"方位角: {az:.1f}°, 高度角: {alt:.1f}°")

# 计算天体升起落下时间
times = AstronomyCalculator.calculate_rise_set_times(ra, dec, latitude, longitude, dt)
print(f"升起: {times.rise_time}")
print(f"中天: {times.transit_time}")
print(f"落下: {times.set_time}")

# 计算角直径
# 月球: 直径3474km, 距离384400km
angular = AstronomyCalculator.calculate_angular_diameter(3474, 384400)
print(f"月球角直径: {angular:.0f} 角秒")  # 约1800角秒

# 计算下一个满月
next_full = MoonPhaseCalculator.calculate_next_moon_phase(dt, 4)
print(f"下一个满月: {next_full}")
```

## API 参考

### 数据类

#### CelestialBody
天体数据类

| 属性 | 类型 | 说明 |
|------|------|------|
| `name` | str | 英文名 |
| `name_cn` | str | 中文名 |
| `body_type` | str | 类型 (planet, moon, star, dwarf_planet) |
| `mass_kg` | float | 质量 (千克) |
| `radius_km` | float | 半径 (千米) |
| `orbital_period_days` | float | 公转周期 (地球日) |
| `rotation_period_hours` | float | 自转周期 (小时) |
| `distance_au` | float | 与太阳平均距离 (天文单位) |
| `moons` | int | 卫星数量 |
| `magnitude` | float | 视星等 |
| `color` | str | 颜色描述 |

#### Constellation
星座数据类

| 属性 | 类型 | 说明 |
|------|------|------|
| `name` | str | 英文名 |
| `name_cn` | str | 中文名 |
| `abbreviation` | str | 缩写 |
| `area_sq_deg` | float | 面积 (平方度) |
| `brightest_star` | str | 最亮星 |
| `best_month` | int | 最佳观测月份 (1-12) |
| `description` | str | 描述 |

#### RiseSetTimes
升起落下时间类

| 属性 | 类型 | 说明 |
|------|------|------|
| `rise_time` | datetime | 升起时间 |
| `transit_time` | datetime | 中天时间 |
| `set_time` | datetime | 落下时间 |
| `is_circumpolar` | bool | 是否拱极星 |
| `is_never_rises` | bool | 是否永不升起 |

### 便捷函数

| 函数 | 说明 |
|------|------|
| `get_planet(name)` | 获取行星信息（支持中英文名） |
| `get_all_planets()` | 获取所有8大行星列表 |
| `get_constellation(name)` | 获取星座信息（支持中英文名和缩写） |
| `get_zodiac_constellations()` | 获取黄道十二宫列表 |
| `calculate_moon_phase(dt)` | 计算月相（dt可选，默认当前） |
| `get_star_info(name)` | 获取恒星信息（支持中英文名） |
| `date_to_julian_day(dt)` | 日期转儒略日 |
| `julian_day_to_date(jd)` | 儒略日转日期 |
| `au_to_km(au)` | 天文单位转千米 |
| `km_to_light_year(km)` | 千米转光年 |
| `calculate_light_travel_time(km)` | 计算光传播时间 |

### 计算类

#### AstronomyCalculator
天文学计算器

| 方法 | 说明 |
|------|------|
| `date_to_julian_day(dt)` | 日期转儒略日 |
| `julian_day_to_date(jd)` | 儒略日转日期 |
| `calculate_greenwich_sidereal_time(dt)` | 计算格林尼治恒星时 |
| `calculate_local_sidereal_time(dt, longitude)` | 计算本地恒星时 |
| `equatorial_to_horizontal(ra, dec, lat, lon, dt)` | 赤道坐标转地平坐标 |
| `calculate_rise_set_times(ra, dec, lat, lon, dt)` | 计算升起落下时间 |
| `calculate_distance_km(au)` | 天文单位转千米 |
| `calculate_distance_ly(km)` | 千米转光年 |
| `calculate_angular_diameter(diameter, distance)` | 计算角直径 |
| `calculate_light_travel_time(km)` | 计算光传播时间 |

#### MoonPhaseCalculator
月相计算器

| 方法 | 说明 |
|------|------|
| `calculate_moon_phase(dt)` | 计算月相，返回(月龄, 索引, 中文, 英文) |
| `calculate_next_moon_phase(dt, target_phase)` | 计算下一个特定月相日期 |
| `calculate_moon_distance(dt)` | 计算月球距离（简化） |

### 数据类

#### SolarSystemData
太阳系数据

- `SUN`: 太阳数据
- `MOON`: 月球数据
- `PLANETS`: 8大行星字典
- `DWARF_PLANETS`: 矮行星字典
- `get_all_planets()`: 获取所有行星
- `get_planet(name)`: 获取单个行星

#### ConstellationData
星座数据

- `ZODIAC`: 黄道十二宫字典
- `NORTHERN`: 北半球常见星座字典
- `get_zodiac()`: 获取黄道十二宫
- `get_constellation(name)`: 获取单个星座
- `get_constellation_by_month(month)`: 按月份获取星座

#### StarData
恒星数据

- `BRIGHT_STARS`: 20颗最亮恒星字典
- `get_star(name)`: 获取单个恒星
- `get_visible_stars(latitude)`: 获取给定纬度可见恒星

## 测试

```bash
python astronomy_utils_test.py
```

## 注意事项

- 行星位置计算为简化版本，精度有限；精确计算需要更复杂的轨道模型
- 升起落下时间计算基于简化算法，实际观测可能有几分钟误差
- 月相计算基于已知的参考新月日期，误差约1小时

## 许可证

MIT License