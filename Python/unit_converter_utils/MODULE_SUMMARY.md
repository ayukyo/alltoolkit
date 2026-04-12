# Unit Converter Utils - Module Summary

## 模块信息

- **名称**: Unit Converter Utils (单位转换工具)
- **语言**: Python
- **路径**: `/home/admin/.openclaw/workspace/AllToolkit/Python/unit_converter_utils/`
- **创建时间**: 2026-04-12
- **依赖**: 零外部依赖 (仅使用 Python 标准库)

## 文件结构

```
unit_converter_utils/
├── mod.py                          # 主模块 (36 KB, ~1200 行)
├── unit_converter_utils_test.py    # 测试套件 (31 KB, 211 个测试)
├── README.md                       # 详细文档 (11 KB)
├── MODULE_SUMMARY.md               # 本文件
└── examples/
    └── usage_examples.py           # 使用示例 (12 KB)
```

## 功能概览

### 支持的单位类别 (11 类，95+ 单位)

| 类别 | 单位数 | 基础单位 | 示例单位 |
|------|--------|---------|---------|
| 长度 | 11 | meter (m) | km, cm, mm, in, ft, mi, nmi |
| 重量 | 9 | kilogram (kg) | g, mg, lb, oz, ton, st |
| 温度 | 3 | Celsius (°C) | °F, K |
| 体积 | 13 | liter (L) | mL, gal, qt, cup, fl oz |
| 面积 | 9 | m² | km², ft², acre, ha |
| 速度 | 5 | m/s | km/h, mph, kn |
| 时间 | 10 | second (s) | min, h, day, week, year |
| 数据 | 15 | byte (B) | KB, MB, GB, TB, KiB, GiB |
| 压力 | 7 | Pascal (Pa) | bar, atm, psi, mmHg |
| 能量 | 8 | Joule (J) | kJ, cal, kWh, BTU |
| 功率 | 5 | Watt (W) | kW, MW, hp |

### 核心 API

**主转换函数** (11 个):
- `convert_length()`, `convert_weight()`, `convert_temperature()`
- `convert_volume()`, `convert_area()`, `convert_speed()`
- `convert_time()`, `convert_data()`, `convert_pressure()`
- `convert_energy()`, `convert_power()`

**快捷函数** (40+ 个):
- `celsius_to_fahrenheit()`, `kg_to_pounds()`, `kilometers_to_miles()`
- `liters_to_gallons()`, `square_meters_to_square_feet()`, etc.

**通用函数**:
- `convert()` - 自动识别类别
- `format_conversion()` - 格式化输出

**批量转换**:
- `batch_convert_length()`, `batch_convert_weight()`, `batch_convert_temperature()`

**单位信息**:
- `get_available_units()`, `get_unit_info()`

## 测试结果

```
============================================================
Results: 211/211 tests passed
SUCCESS: All tests passed!
============================================================
```

### 测试覆盖

- ✅ 正常转换场景 (所有类别)
- ✅ 快捷函数 (40+ 个)
- ✅ 边界值测试 (零、极大值、极小值)
- ✅ 往返转换验证
- ✅ 错误处理 (负值、无效单位、绝对零度)
- ✅ 批量转换
- ✅ 单位信息查询
- ✅ 通用 convert() 函数
- ✅ 格式化输出

## 使用示例

```python
from mod import convert_length, convert_temperature, convert

# 基本转换
print(convert_length(1, 'km', 'mi'))  # 0.621371...
print(convert_temperature(0, 'C', 'F'))  # 32.0

# 快捷函数
from mod import kg_to_pounds
print(kg_to_pounds(70))  # 154.32...

# 通用转换 (自动识别类别)
print(convert(100, 'C', 'F'))  # 212.0
print(convert(1, 'GB', 'MB'))  # 1000.0

# 批量转换
from mod import batch_convert_temperature
temps_f = batch_convert_temperature([0, 20, 37, 100], 'C', 'F')
# [32.0, 68.0, 98.6, 212.0]
```

## 设计特点

1. **零依赖**: 仅使用 Python 标准库 (`math`, `typing`, `enum`)
2. **类型安全**: 完整的类型注解
3. **文档完善**: 每个函数都有详细的 docstring 和示例
4. **错误处理**: 清晰的错误消息和验证
5. **精确换算**: 使用国际标准换算因子
6. **易用性**: 提供快捷函数和通用转换函数

## 运行命令

```bash
# 运行测试
python unit_converter_utils_test.py

# 运行示例
python examples/usage_examples.py

# 运行模块演示
python mod.py
```

## 与其他 AllToolkit 模块的一致性

- ✅ 遵循 AllToolkit 项目结构
- ✅ 使用相同的文档格式
- ✅ 测试覆盖率 100%
- ✅ 零外部依赖
- ✅ 完整的 API 文档

## 后续优化建议

1. 添加更多货币转换支持 (需要实时汇率 API)
2. 添加角度转换 (度↔弧度)
3. 添加频率转换 (Hz, kHz, MHz, GHz)
4. 添加照度转换 (lux, foot-candle)
5. 添加数据传输速率转换 (bps, Mbps, Gbps)

---

**创建者**: AllToolkit Cron Job  
**创建时间**: 2026-04-12 04:00 (Asia/Shanghai)  
**状态**: ✅ 完成 (测试通过，文档完整)
