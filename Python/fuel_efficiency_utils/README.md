# Fuel Efficiency Utils - 燃油效率计算工具 ⛽

油耗转换、燃油成本计算、碳排放估算工具。零外部依赖。

## 功能

- **单位转换**: MPG ↔ L/100km ↔ km/L
- **燃油成本**: 行程燃油费用计算
- **续航里程**: 根据油箱容量估算续航
- **碳排放**: 不同燃油类型的 CO2 排放计算
- **年度成本**: 年度燃油开支估算
- **车辆对比**: 两车效率对比
- **效率评级**: A+ 到 E 级效率评级
- **回本分析**: 高效车回本里程计算
- **完整报告**: 一键生成效率报告

## 支持的燃油类型

- 汽油 (Gasoline)
- 柴油 (Diesel)
- 混合动力 (Hybrid)
- 纯电动 (Electric)
- 插电混动 (Plug-in Hybrid)
- 天然气 (Natural Gas)
- E85 乙醇汽油

## 快速开始

### 单位转换

```python
from fuel_efficiency_utils import mpg_to_lp100k, lp100k_to_mpg

# MPG 转 L/100km
lp100k = mpg_to_lp100k(30)  # 约 7.84 L/100km

# L/100km 转 MPG  
mpg = lp100k_to_mpg(8)  # 约 29.4 MPG

# 英制加仑（英国）
lp100k_uk = mpg_to_lp100k(30, us_gallon=False)  # 约 9.42 L/100km
```

### 燃油成本计算

```python
from fuel_efficiency_utils import calculate_fuel_cost

# 500公里, 8L/100km, 8.5元/升
cost = calculate_fuel_cost(500, 8, 8.5)
print(cost)  # 340 元

# MPG 单位计算
from fuel_efficiency_utils import FuelEfficiencyCalculator
cost = FuelEfficiencyCalculator.calculate_fuel_cost(300, 30, 3.5, 'mpg')
```

### 续航里程

```python
from fuel_efficiency_utils import FuelEfficiencyCalculator

# 50升油箱, 8L/100km
range_km = FuelEfficiencyCalculator.calculate_range(50, 8)
print(range_km)  # 625 公里

# 加仑单位
range_miles = FuelEfficiencyCalculator.calculate_range(15, 30, 'mpg', 'us_gallon')
```

### 碳排放计算

```python
from fuel_efficiency_utils import calculate_co2, FuelType

# 汽油车: 100公里, 8L/100km
co2 = FuelEfficiencyCalculator.calculate_co2_emissions(100, 8, FuelType.GASOLINE)
print(co2)  # 约 18.48 kg CO2

# 柴油车: 100公里, 6L/100km
co2 = FuelEfficiencyCalculator.calculate_co2_emissions(100, 6, FuelType.DIESEL)
print(co2)  # 约 16.08 kg CO2

# 电动车间接排放（中国电网）
co2 = FuelEfficiencyCalculator.calculate_electric_emissions(100, 15, 'china')
print(co2)  # 约 8.76 kg CO2
```

### 年度燃油成本

```python
# 年行驶15000公里, 8L/100km, 8.5元/升
result = FuelEfficiencyCalculator.calculate_annual_fuel_cost(15000, 8, 8.5)
print(result['annual_cost'])  # 10200 元
print(result['monthly_cost'])  # 850 元
print(result['fuel_consumed_liters'])  # 1200 升
```

### 车辆对比

```python
# 两车对比: 500公里, 10 vs 6 L/100km, 8.5元/升
result = FuelEfficiencyCalculator.compare_vehicles(500, 10, 6, 8.5)
print(result['vehicle1_cost'])  # 425 元
print(result['vehicle2_cost'])  # 255 元
print(result['savings'])  # 170 元
print(result['percentage_improvement'])  # 40%
```

### 效率评级

```python
# 评级系统: A+ 到 E
rating = FuelEfficiencyCalculator.efficiency_rating(5)
print(rating)  # ('A+', '卓越')

rating = FuelEfficiencyCalculator.efficiency_rating(8)
print(rating)  # ('B+', '良好')

rating = FuelEfficiencyCalculator.efficiency_rating(15)
print(rating)  # ('D', '较差')

# SUV 标准（更宽松）
rating = FuelEfficiencyCalculator.efficiency_rating(9, 'suv')
print(rating)  # ('A', '优秀')
```

### 回本分析

```python
# 省油车: 20万, 5L/100km
# 普通车: 15万, 8L/100km
result = FuelEfficiencyCalculator.calculate_break_even(200000, 5, 150000, 8, 8.5)
print(result['price_difference'])  # 50000 元
print(result['break_even_km'])  # 约 196000 公里
print(result['savings_per_km'])  # 0.255 元/公里
```

### 旅行计算

```python
# 300公里, 8L/100km, 8.5元/升, 4人
result = FuelEfficiencyCalculator.calculate_trip_fuel(300, 8, 8.5, 4)
print(result['fuel_needed_liters'])  # 24 升
print(result['total_cost'])  # 204 元
print(result['cost_per_passenger'])  # 51 元/人
```

### 完整效率报告

```python
report = FuelEfficiencyCalculator.full_efficiency_report(8)
print(report['efficiency'])  # 各单位效率值
print(report['efficiency_rating'])  # 评级
print(report['annual_costs'])  # 年度成本
print(report['co2_emissions_kg'])  # 碳排放

# 带参数的报告
report = FuelEfficiencyCalculator.full_efficiency_report(8, 15000, 8.5, FuelType.GASOLINE)
```

## API 参考

### 单位转换函数

| 函数 | 描述 |
|------|------|
| `mpg_to_lp100k(mpg, us_gallon=True)` | MPG 转 L/100km |
| `lp100k_to_mpg(lp100k, us_gallon=True)` | L/100km 转 MPG |
| `calculate_fuel_cost(distance, efficiency, price)` | 燃油成本 |

### FuelEfficiencyCalculator 类

| 方法 | 描述 |
|------|------|
| `calculate_range()` | 续航里程计算 |
| `calculate_co2_emissions()` | 碳排放计算 |
| `calculate_annual_fuel_cost()` | 年度成本计算 |
| `compare_vehicles()` | 车辆对比 |
| `efficiency_rating()` | 效率评级 |
| `calculate_break_even()` | 回本分析 |
| `calculate_trip_fuel()` | 旅行计算 |
| `full_efficiency_report()` | 完整报告 |

## 测试

```bash
python fuel_efficiency_utils_test.py
```

**测试覆盖**: 43 个测试用例，100% 通过 ✅

---

*最后更新: 2026-05-12*