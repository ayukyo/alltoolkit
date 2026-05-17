# Unit Converter Utils

多功能单位转换工具库 - 纯 Python 实现，零外部依赖

## 特性

- 🚀 **零依赖**: 纯 Python 标准库实现
- 📐 **多类型支持**: 长度、重量、温度、体积、面积、时间、速度、数据、压力、角度、功率
- 🔧 **灵活使用**: 支持自动类型检测、批量转换、全量转换
- 🎯 **高精度**: 使用 Decimal 进行精确计算
- 🧪 **完整测试**: 100+ 单元测试覆盖

## 支持的单位

### 长度 (Length)
`m`, `km`, `cm`, `mm`, `um`, `nm`, `mi`, `yd`, `ft`, `in`, `nmi`, `ly`, `au`, `pc`

### 重量 (Weight)
`kg`, `g`, `mg`, `ug`, `t`, `lb`, `oz`, `st`, `ct`, `jin`, `liang`

### 温度 (Temperature)
`C`, `F`, `K`

### 体积 (Volume)
`L`, `mL`, `m3`, `cm3`, `mm3`, `gal`, `gal_uk`, `qt`, `pt`, `cup`, `fl_oz`, `tbsp`, `tsp`, `bbl`

### 面积 (Area)
`m2`, `km2`, `cm2`, `mm2`, `ha`, `acre`, `ft2`, `in2`, `yd2`, `mu`, `qing`

### 时间 (Time)
`s`, `ms`, `us`, `ns`, `ps`, `min`, `h`, `d`, `w`, `mo`, `y`, `decade`, `century`

### 速度 (Speed)
`m/s`, `km/s`, `km/h`, `m/min`, `mph`, `knot`, `mach`, `c`

### 数据 (Data)
`B`, `KB`, `MB`, `GB`, `TB`, `PB`, `EB`, `KiB`, `MiB`, `GiB`, `TiB`, `PiB`, `bit`, `Kbit`, `Mbit`, `Gbit`

### 压力 (Pressure)
`Pa`, `kPa`, `MPa`, `GPa`, `bar`, `mbar`, `psi`, `atm`, `mmHg`, `inHg`, `Torr`, `kgf/cm2`

### 角度 (Angle)
`deg`, `rad`, `grad`, `arcmin`, `arcsec`, `turn`, `mrad`

### 功率 (Power)
`W`, `kW`, `MW`, `GW`, `mW`, `hp`, `hp_electric`, `BTU/h`, `kcal/h`, `ft_lbf/s`

## 安装

```bash
# 直接复制到项目中使用
cp -r unit_converter_utils /your/project/path/
```

## 快速开始

### 基础用法

```python
from unit_converter_utils import convert_length, convert_weight, convert_temperature

# 长度转换
print(convert_length(1000, 'm', 'km'))  # 1.0
print(convert_length(1, 'mi', 'km'))   # 1.609344

# 重量转换
print(convert_weight(1, 'kg', 'lb'))   # 2.204623
print(convert_weight(1, 'jin', 'kg'))  # 0.5 (市斤转千克)

# 温度转换
print(convert_temperature(0, 'C', 'F'))    # 32.0
print(convert_temperature(100, 'C', 'F'))  # 212.0
```

### 自动类型检测

```python
from unit_converter_utils import convert

# 自动识别单位类型
print(convert(1, 'kg', 'lb'))    # 重量
print(convert(100, 'km', 'mi'))  # 长度
print(convert(37, 'C', 'F'))      # 温度
print(convert(100, 'km/h', 'm/s'))  # 速度
```

### 使用 UnitConverter 类

```python
from unit_converter_utils import UnitConverter

# 创建转换器，设置精度
converter = UnitConverter(precision=4)

# 转换
result = converter.convert(1000, 'm', 'km', 'length')
print(result)  # 1.0

# 批量转换
conversions = [
    (100, 'km', 'mi'),
    (1, 'kg', 'lb'),
    (0, 'C', 'K'),
]
results = converter.batch_convert(conversions)
print(results)  # [62.1371, 2.2046, 273.15]

# 转换为所有同类型单位
all_units = converter.convert_all(1, 'kg', 'weight')
print(all_units['lb'])  # 2.2046
```

### 获取支持的单位

```python
from unit_converter_utils import UnitConverter

converter = UnitConverter()

# 获取所有支持的单位类型
units = converter.get_supported_units()
for category, unit_list in units.items():
    print(f"{category}: {unit_list}")

# 获取特定类型的单位
weight_units = converter.get_supported_units('weight')
print(weight_units)  # {'weight': ['kg', 'g', 'mg', ...]}
```

## 实用示例

### 国际旅行

```python
# 英里转公里
miles = 2800
km = convert_length(miles, 'mi', 'km')
print(f"{miles} 英里 = {km:.2f} 公里")

# 加仑转升
gallons = 15
liters = convert_volume(gallons, 'gal', 'L')
print(f"{gallons} 加仑 = {liters:.2f} 升")
```

### 烹饪食谱

```python
# 杯转毫升
cups = 2
ml = convert_volume(cups, 'cup', 'mL')
print(f"{cups} 杯 = {ml:.0f} mL")

# 华氏转摄氏
fahrenheit = 350
celsius = convert_temperature(fahrenheit, 'F', 'C')
print(f"{fahrenheit}°F = {celsius:.0f}°C")

# 磅转克
pounds = 1
grams = convert_weight(pounds, 'lb', 'g')
print(f"{pounds} 磅 = {grams:.0f} 克")
```

### 科技计算

```python
# 网络速度
mbps = 100
mb_per_sec = convert_data(mbps, 'Mbit', 'MB')
print(f"{mbps} Mbps = {mb_per_sec:.2f} MB/s (理论最大)")

# 存储容量
gb = 512
gib = convert_data(gb, 'GB', 'GiB')
print(f"{gb} GB = {gib:.2f} GiB (实际容量)")
```

## 运行测试

```bash
cd unit_converter_utils
python -m pytest test_converter.py -v

# 或使用 unittest
python test_converter.py
```

## 运行示例

```bash
cd unit_converter_utils
python examples.py
```

## API 参考

### 便捷函数

| 函数 | 说明 |
|------|------|
| `convert(value, from_unit, to_unit, category='auto')` | 通用转换函数 |
| `convert_length(value, from_unit, to_unit)` | 长度转换 |
| `convert_weight(value, from_unit, to_unit)` | 重量转换 |
| `convert_temperature(value, from_unit, to_unit)` | 温度转换 |
| `convert_volume(value, from_unit, to_unit)` | 体积转换 |
| `convert_area(value, from_unit, to_unit)` | 面积转换 |
| `convert_time(value, from_unit, to_unit)` | 时间转换 |
| `convert_speed(value, from_unit, to_unit)` | 速度转换 |
| `convert_data(value, from_unit, to_unit)` | 数据转换 |
| `convert_pressure(value, from_unit, to_unit)` | 压力转换 |
| `convert_angle(value, from_unit, to_unit)` | 角度转换 |

### UnitConverter 类

| 方法 | 说明 |
|------|------|
| `__init__(precision=6)` | 初始化，设置小数精度 |
| `convert(value, from_unit, to_unit, category='auto')` | 通用转换 |
| `convert_all(value, from_unit, category)` | 转换为所有同类型单位 |
| `batch_convert(conversions)` | 批量转换 |
| `get_supported_units(category=None)` | 获取支持的单位列表 |

## 许可证

MIT License

## 作者

AllToolkit 自动生成工具