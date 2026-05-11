# Ohm's Law Utils - 欧姆定律计算工具 ⚡

电压、电流、电阻、功率计算工具。支持串联/并联电阻、分压器、功率计算。零外部依赖。

## 核心公式

- **欧姆定律**: V = I × R
- **功率公式**: P = V × I = I²R = V²/R
- **串联电阻**: R_total = R1 + R2 + ...
- **并联电阻**: 1/R_total = 1/R1 + 1/R2 + ...

## 功能

- **欧姆定律计算**: 根据任意两个参数计算其他参数
- **电阻计算**: 串联、并联、混合电路
- **分压器**: 电压分压计算
- **分流器**: 电流分流计算
- **功率计算**: AC/DC 功率、能耗、电池续航
- **电阻色环**: 4环/5环色码解码和编码

## 快速开始

### 欧姆定律计算

```python
from ohm_law_utils import OhmLawCalculator, calculate

# 从电压和电流计算
result = OhmLawCalculator.from_voltage_current(12.0, 3.0)
print(result.voltage)    # 12.0 V
print(result.current)    # 3.0 A
print(result.resistance) # 4.0 Ω
print(result.power)      # 36.0 W

# 从电压和电阻计算
result = OhmLawCalculator.from_voltage_resistance(12.0, 4.0)
print(result.current)    # 3.0 A

# 从功率和电流计算
result = OhmLawCalculator.from_current_power(3.0, 36.0)
print(result.voltage)    # 12.0 V

# 便捷函数
result = calculate(voltage=12, resistance=4)
print(result.current)    # 3.0 A
```

### 串联和并联电阻

```python
from ohm_law_utils import ResistorCalculator, series_resistance, parallel_resistance

# 串联电阻
total = ResistorCalculator.series([100, 200, 300])
print(total)  # 600 Ω

# 并联电阻
total = ResistorCalculator.parallel([100, 100])
print(total)  # 50 Ω (两个相同电阻并联 = 一半)

total = ResistorCalculator.parallel([100, 200])
print(total)  # 约 66.67 Ω

# 便捷函数
total = series_resistance(100, 200, 300)  # 600 Ω
total = parallel_resistance(100, 100)  # 50 Ω

# 混合电路: 串联 + 并联
# 10Ω + (20Ω||30Ω) + 40Ω
total = ResistorCalculator.mixed([10, [20, 30], 40])
print(total)  # 约 62 Ω
```

### 分压器计算

```python
from ohm_law_utils import VoltageDivider

# 12V 分压: R1=10kΩ, R2=2kΩ
vout = VoltageDivider.calculate(12, 10000, 2000)
print(vout)  # 2.0 V

# 相等电阻分压一半
vout = VoltageDivider.calculate(10, 100, 100)
print(vout)  # 5.0 V

# 查找合适的电阻组合
available = [1000, 2000, 4700, 10000, 22000]
combos = VoltageDivider.find_resistors(12, 3, available)
# 返回接近 3V 的电阻组合
```

### 分流器计算

```python
from ohm_law_utils import CurrentDivider

# 1A 总电流, 两个 100Ω 并联
i1, i2 = CurrentDivider.calculate(1.0, 100, 100)
print(i1, i2)  # 0.5A, 0.5A (各分一半)

# 不等电阻分流
i1, i2 = CurrentDivider.calculate(1.0, 100, 200)
print(i1, i2)  # 小电阻分到大电流
```

### 功率计算

```python
from ohm_law_utils import PowerCalculator

# AC 功率计算
result = PowerCalculator.ac_power(220, 10, 1.0)  # 220V, 10A, 功率因数=1
print(result['apparent_power'])  # 2200 VA
print(result['real_power'])      # 2200 W
print(result['reactive_power'])  # 0 VAR

# 功率因数 = 0.8 (滞后)
result = PowerCalculator.ac_power(220, 10, 0.8)
print(result['real_power'])      # 1760 W
print(result['reactive_power'])  # 1320 VAR

# 能耗成本计算
result = PowerCalculator.energy_cost(1000, 10, 0.5)  # 1000W, 10小时, 0.5元/kWh
print(result['energy_kwh'])  # 10 kWh
print(result['cost'])        # 5.0 元

# 电池续航
result = PowerCalculator.battery_life(3000, 500, 1.0)  # 3000mAh, 500mA
print(result['hours'])    # 6.0 小时
print(result['minutes'])  # 360 分钟
```

### 电阻色环解码/编码

```python
from ohm_law_utils import ResistorColorCode

# 解码 4 环电阻: 红-紫-黄-金
result = ResistorColorCode.decode_4band('red', 'violet', 'yellow', 'gold')
print(result['resistance'])  # 270000 Ω (270kΩ)
print(result['tolerance'])   # 5 %
print(result['range'])       # [256500, 283500] Ω

# 解码 5 环电阻
result = ResistorColorCode.decode_5band('red', 'red', 'black', 'orange', 'brown')
print(result['resistance'])  # 220000 Ω (220kΩ)
print(result['tolerance'])   # 1 %

# 编码电阻
colors = ResistorColorCode.encode(1000, 5)  # 1kΩ, 5%
print(colors)  # ['brown', 'black', 'red', 'gold']
```

## SI 前缀支持

```python
from ohm_law_utils import Prefix

# 常用前缀
Prefix.MILLI   # 1e-3 (m)
Prefix.MICRO   # 1e-6 (μ)
Prefix.KILO    # 1e3  (k)
Prefix.MEGA    # 1e6  (M)

# 格式化显示
from ohm_law_utils import OhmLawResult
formatted = OhmLawResult.format_value(12000, 'Ω')  # "12.0 kΩ"
```

## API 参考

### OhmLawCalculator

| 方法 | 描述 |
|------|------|
| `from_voltage_current(V, I)` | 从电压和电流计算 |
| `from_voltage_resistance(V, R)` | 从电压和电阻计算 |
| `from_current_resistance(I, R)` | 从电流和电阻计算 |
| `from_voltage_power(V, P)` | 从电压和功率计算 |
| `from_current_power(I, P)` | 从电流和功率计算 |
| `from_resistance_power(R, P)` | 从电阻和功率计算 |

### ResistorCalculator

| 方法 | 描述 |
|------|------|
| `series(resistors)` | 串联电阻计算 |
| `parallel(resistors)` | 并联电阻计算 |
| `mixed(config)` | 混合电路计算 |
| `find_combination(target, available, max_count, mode)` | 查找组合 |

### VoltageDivider / CurrentDivider

| 方法 | 描述 |
|------|------|
| `calculate(...)` | 分压/分流计算 |
| `find_resistors(...)` | 查找合适电阻 |

### PowerCalculator

| 方法 | 描述 |
|------|------|
| `ac_power(V, I, pf)` | AC 功率计算 |
| `energy_cost(W, hours, rate)` | 能耗成本 |
| `battery_life(capacity_mAh, current_mA, efficiency)` | 电池续航 |

### ResistorColorCode

| 方法 | 描述 |
|------|------|
| `decode_4band(...)` | 4 环解码 |
| `decode_5band(...)` | 5 环解码 |
| `encode(resistance, tolerance)` | 编码为色环 |

## 测试

```bash
python ohm_law_utils_test.py
```

**测试覆盖**: 44 个测试用例，100% 通过 ✅

---

*最后更新: 2026-05-12*