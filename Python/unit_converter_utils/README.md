# Unit Converter Utils - Python 单位转换工具模块

AllToolkit 的 Python 单位转换工具模块，提供全面的单位转换功能，零外部依赖。

## 📦 功能特性

### 长度/距离转换
- `convert_length()` - 通用长度转换
- `meters_to_feet()` / `feet_to_meters()` - 米↔英尺
- `kilometers_to_miles()` / `miles_to_kilometers()` - 公里↔英里
- `inches_to_centimeters()` / `centimeters_to_inches()` - 英寸↔厘米
- 支持单位：m, km, cm, mm, μm, nm, in, ft, yd, mi, nmi

### 重量/质量转换
- `convert_weight()` - 通用重量转换
- `kg_to_pounds()` / `pounds_to_kg()` - 千克↔磅
- `grams_to_ounces()` / `ounces_to_grams()` - 克↔盎司
- 支持单位：kg, g, mg, μg, lb, oz, ton, t (metric ton), st (stone)

### 温度转换
- `convert_temperature()` - 通用温度转换
- `celsius_to_fahrenheit()` / `fahrenheit_to_celsius()` - 摄氏↔华氏
- `celsius_to_kelvin()` / `kelvin_to_celsius()` - 摄氏↔开尔文
- `fahrenheit_to_kelvin()` / `kelvin_to_fahrenheit()` - 华氏↔开尔文
- 支持单位：°C, °F, K

### 体积转换
- `convert_volume()` - 通用体积转换
- `liters_to_gallons()` / `gallons_to_liters()` - 升↔加仑
- `milliliters_to_fluid_ounces()` / `fluid_ounces_to_milliliters()` - 毫升↔液量盎司
- 支持单位：L, mL, gal, qt, pt, cup, fl oz, tbsp, tsp, m³, cm³, in³, ft³

### 面积转换
- `convert_area()` - 通用面积转换
- `square_meters_to_square_feet()` / `square_feet_to_square_meters()` - 平方米↔平方英尺
- `acres_to_hectares()` / `hectares_to_acres()` - 英亩↔公顷
- 支持单位：m², km², cm², mm², ft², in², yd², acre, ha

### 速度转换
- `convert_speed()` - 通用速度转换
- `kmh_to_mph()` / `mph_to_kmh()` - 公里/小时↔英里/小时
- `ms_to_kmh()` - 米/秒→公里/小时
- `knots_to_kmh()` - 节→公里/小时
- 支持单位：m/s, km/h, mph, kn (knot), ft/s

### 时间转换
- `convert_time()` - 通用时间转换
- `hours_to_minutes()` - 小时→分钟
- `minutes_to_seconds()` - 分钟→秒
- `days_to_hours()` - 天→小时
- `weeks_to_days()` - 周→天
- `years_to_days()` - 年→天
- 支持单位：s, ms, μs, ns, min, h, day, week, month, year

### 数据存储转换
- `convert_data()` - 通用数据转换
- `gb_to_mb()` - GB→MB (十进制)
- `gib_to_mib()` - GiB→MiB (二进制)
- `tb_to_gb()` - TB→GB
- `bytes_to_bits()` / `bits_to_bytes()` - 字节↔位
- 支持单位：bit, B, KB, MB, GB, TB, PB, KiB, MiB, GiB, TiB, PiB, Kibit, Mibit, Gibit

### 压力转换
- `convert_pressure()` - 通用压力转换
- `atm_to_pascal()` - 大气压→帕斯卡
- `psi_to_bar()` / `bar_to_psi()` - PSI↔巴
- 支持单位：Pa, kPa, bar, atm, psi, mmHg, Torr

### 能量转换
- `convert_energy()` - 通用能量转换
- `kwh_to_joules()` - 千瓦时→焦耳
- `calories_to_joules()` - 卡路里→焦耳
- `btu_to_kwh()` - BTU→千瓦时
- 支持单位：J, kJ, cal, kcal, Wh, kWh, BTU, eV

### 功率转换
- `convert_power()` - 通用功率转换
- `hp_to_kw()` / `kw_to_hp()` - 马力↔千瓦
- `mw_to_kw()` - 兆瓦→千瓦
- 支持单位：W, kW, MW, hp, BTU/h

### 批量转换
- `batch_convert_length()` - 批量长度转换
- `batch_convert_weight()` - 批量重量转换
- `batch_convert_temperature()` - 批量温度转换

### 单位信息
- `get_available_units()` - 获取某类别的所有可用单位
- `get_unit_info()` - 获取特定单位的信息

### 通用函数
- `convert()` - 自动识别类别的通用转换函数
- `format_conversion()` - 转换并格式化为字符串

## 🚀 快速开始

### 安装

无需安装，直接使用：

```python
import sys
sys.path.insert(0, '/path/to/AllToolkit/Python/unit_converter_utils')
from mod import *
```

### 基本用法

```python
from mod import convert_length, convert_weight, convert_temperature

# 长度转换
print(convert_length(1, 'km', 'mi'))  # 0.6213711922373339
print(convert_length(100, 'm', 'ft'))  # 328.0839895013123

# 重量转换
print(convert_weight(1, 'kg', 'lb'))  # 2.2046226218487757
print(convert_weight(16, 'oz', 'g'))  # 453.59237

# 温度转换
print(convert_temperature(0, 'C', 'F'))  # 32.0
print(convert_temperature(100, 'C', 'F'))  # 212.0
print(convert_temperature(-40, 'F', 'C'))  # -40.0 (巧合点!)
```

### 快捷函数

```python
from mod import (
    celsius_to_fahrenheit, kg_to_pounds,
    kilometers_to_miles, liters_to_gallons
)

print(celsius_to_fahrenheit(25))  # 77.0
print(kg_to_pounds(70))  # 154.3235835294143
print(kilometers_to_miles(5))  # 3.1068559611866697
print(liters_to_gallons(10))  # 2.641720523581484
```

### 通用转换函数

```python
from mod import convert, format_conversion

# 自动识别类别
print(convert(100, 'C', 'F'))  # 212.0 (温度)
print(convert(1, 'km', 'mi'))  # 0.6213711922373339 (长度)
print(convert(1, 'kg', 'lb'))  # 2.2046226218487757 (重量)

# 格式化输出
print(format_conversion(1, 'mile', 'km', precision=2))  # "1.61 km"
print(format_conversion(100, 'C', 'F'))  # "212.0000 °F"
```

### 批量转换

```python
from mod import batch_convert_length, batch_convert_temperature

# 批量长度转换
distances_km = [1, 5, 10, 42.195]  # 马拉松距离
distances_mi = batch_convert_length(distances_km, 'km', 'mi')
print(distances_mi)  # [0.621..., 3.106..., 6.213..., 26.218...]

# 批量温度转换
temps_c = [0, 20, 37, 100]
temps_f = batch_convert_temperature(temps_c, 'C', 'F')
print(temps_f)  # [32.0, 68.0, 98.6, 212.0]
```

### 获取单位信息

```python
from mod import get_available_units, get_unit_info

# 获取所有长度单位
print(get_available_units('length'))
# ['m', 'km', 'cm', 'mm', 'μm', 'nm', 'in', 'ft', 'yd', 'mi', 'nmi']

# 获取单位信息
info = get_unit_info('km')
print(info)  # {'category': 'length', 'symbol': 'km', 'name': 'Kilometer'}
```

## 📊 转换精度

所有转换使用标准国际单位制 (SI) 换算因子：

| 转换 | 精确值 |
|------|--------|
| 1 inch | 2.54 cm (精确) |
| 1 foot | 0.3048 m (精确) |
| 1 mile | 1609.344 m (精确) |
| 1 lb | 0.45359237 kg (精确) |
| 1 gal (US) | 3.785411784 L (精确) |
| 0°C | 32°F, 273.15 K |
| 1 atm | 101325 Pa (精确) |

## 🧪 测试

运行测试套件：

```bash
cd /path/to/AllToolkit/Python/unit_converter_utils
python unit_converter_utils_test.py
```

测试覆盖：
- ✅ 正常转换场景
- ✅ 边界值（零、极大值、极小值）
- ✅ 往返转换验证
- ✅ 错误处理（负值、无效单位）
- ✅ 快捷函数
- ✅ 批量转换
- ✅ 单位信息查询

## 📝 完整 API 参考

### 主转换函数

```python
convert_length(value, from_unit, to_unit) -> float
convert_weight(value, from_unit, to_unit) -> float
convert_temperature(value, from_unit, to_unit) -> float
convert_volume(value, from_unit, to_unit) -> float
convert_area(value, from_unit, to_unit) -> float
convert_speed(value, from_unit, to_unit) -> float
convert_time(value, from_unit, to_unit) -> float
convert_data(value, from_unit, to_unit) -> float
convert_pressure(value, from_unit, to_unit) -> float
convert_energy(value, from_unit, to_unit) -> float
convert_power(value, from_unit, to_unit) -> float
```

### 快捷函数

```python
# 长度
meters_to_feet(meters) -> float
feet_to_meters(feet) -> float
kilometers_to_miles(km) -> float
miles_to_kilometers(miles) -> float
inches_to_centimeters(inches) -> float
centimeters_to_inches(cm) -> float

# 重量
kg_to_pounds(kg) -> float
pounds_to_kg(pounds) -> float
grams_to_ounces(grams) -> float
ounces_to_grams(ounces) -> float

# 温度
celsius_to_fahrenheit(celsius) -> float
fahrenheit_to_celsius(fahrenheit) -> float
celsius_to_kelvin(celsius) -> float
kelvin_to_celsius(kelvin) -> float
fahrenheit_to_kelvin(fahrenheit) -> float
kelvin_to_fahrenheit(kelvin) -> float

# 体积
liters_to_gallons(liters) -> float
gallons_to_liters(gallons) -> float
milliliters_to_fluid_ounces(ml) -> float
fluid_ounces_to_milliliters(fl_oz) -> float

# 面积
square_meters_to_square_feet(sq_m) -> float
square_feet_to_square_meters(sq_ft) -> float
acres_to_hectares(acres) -> float
hectares_to_acres(hectares) -> float

# 速度
kmh_to_mph(kmh) -> float
mph_to_kmh(mph) -> float
ms_to_kmh(ms) -> float
knots_to_kmh(knots) -> float

# 时间
hours_to_minutes(hours) -> float
minutes_to_seconds(minutes) -> float
days_to_hours(days) -> float
weeks_to_days(weeks) -> float
years_to_days(years) -> float

# 数据
gb_to_mb(gb) -> float
gib_to_mib(gib) -> float
tb_to_gb(tb) -> float
bytes_to_bits(bytes_val) -> float
bits_to_bytes(bits) -> float

# 压力
atm_to_pascal(atm) -> float
psi_to_bar(psi) -> float
bar_to_psi(bar) -> float

# 能量
kwh_to_joules(kwh) -> float
calories_to_joules(cal) -> float
btu_to_kwh(btu) -> float

# 功率
hp_to_kw(hp) -> float
kw_to_hp(kw) -> float
mw_to_kw(mw) -> float
```

### 批量转换

```python
batch_convert_length(values, from_unit, to_unit) -> List[float]
batch_convert_weight(values, from_unit, to_unit) -> List[float]
batch_convert_temperature(values, from_unit, to_unit) -> List[float]
```

### 单位信息

```python
get_available_units(category) -> List[str]
get_unit_info(unit) -> Optional[Dict]
```

### 通用函数

```python
convert(value, from_unit, to_unit) -> float
format_conversion(value, from_unit, to_unit, precision=4) -> str
```

## ⚠️ 错误处理

模块会在以下情况抛出 `ValueError`：

- 负值用于不允许的单位（重量、体积、面积、速度、时间、数据、压力、能量、功率）
- 温度低于绝对零度
- 无效的单位符号
- 跨类别转换（如长度→重量）

```python
try:
    convert_weight(-1, 'kg', 'g')  # ValueError: Weight cannot be negative
except ValueError as e:
    print(f"Error: {e}")

try:
    convert_temperature(-300, 'C', 'F')  # ValueError: Temperature below absolute zero
except ValueError as e:
    print(f"Error: {e}")

try:
    convert_length(1, 'invalid', 'm')  # ValueError: Unknown unit: invalid
except ValueError as e:
    print(f"Error: {e}")
```

## 📋 支持的单位类别

| 类别 | 单位数量 | 基础单位 |
|------|---------|---------|
| 长度 | 11 | meter (m) |
| 重量 | 9 | kilogram (kg) |
| 温度 | 3 | Celsius (°C) |
| 体积 | 13 | liter (L) |
| 面积 | 9 | square meter (m²) |
| 速度 | 5 | meter/second (m/s) |
| 时间 | 10 | second (s) |
| 数据 | 15 | byte (B) |
| 压力 | 7 | Pascal (Pa) |
| 能量 | 8 | Joule (J) |
| 功率 | 5 | Watt (W) |

**总计：95+ 个单位，11 个类别**

## 🔗 相关链接

- [AllToolkit 主项目](https://github.com/ayukyo/alltoolkit)
- [Python 模块列表](https://github.com/ayukyo/alltoolkit/tree/main/Python)
- [贡献指南](https://github.com/ayukyo/alltoolkit/docs/contributing.md)

---

**License**: MIT | **Author**: AllToolkit Contributors | **Zero Dependencies**: ✅
