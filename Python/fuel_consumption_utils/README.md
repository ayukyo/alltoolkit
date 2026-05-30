# Fuel Consumption Utils

燃油消耗计算工具模块，提供汽车油耗相关的计算功能。

## 功能

- **单位转换**: MPG（英里每加仑）和 L/100km（升每百公里）相互转换
- **油耗计算**: 根据行程距离和燃油消耗计算油耗指标
- **行程估算**: 计算行程所需燃油和预估成本
- **碳排放**: 估算燃油消耗产生的 CO2 排放量
- **续航估算**: 根据油箱容量和油耗估算续航里程
- **车辆比较**: 比较两辆车的年度燃油成本
- **油耗评级**: 根据油耗给出星级评价

## 安装

```bash
# 直接导入
from fuel_consumption_utils.mod import mpg_to_liters_per_100km

# 或使用便捷函数
from fuel_consumption_utils.mod import quick_mpg_convert
```

## 快速开始

```python
from fuel_consumption_utils.mod import (
    mpg_to_liters_per_100km,
    calculate_consumption,
    calculate_trip_fuel,
    estimate_range,
)

# MPG 转 L/100km
l100km = mpg_to_liters_per_100km(30)  # 7.84

# 计算油耗
result = calculate_consumption(distance_miles=300, fuel_gallons=10)
print(f"MPG: {result.mpg}")  # 30.0
print(f"L/100km: {result.liters_per_100km}")  # 7.84

# 计算行程燃油
trip = calculate_trip_fuel(distance_km=500, consumption_liters_per_100km=8)
print(f"需要燃油: {trip.fuel_needed_liters} 升")  # 40.0

# 估算续航里程
km, miles = estimate_range(tank_capacity_liters=50, consumption_liters_per_100km=8)
print(f"续航: {km} km / {miles} miles")
```

## API 参考

### 单位转换

| 函数 | 说明 |
|------|------|
| `mpg_to_liters_per_100km(mpg)` | MPG → L/100km |
| `liters_per_100km_to_mpg(l/100km)` | L/100km → MPG |
| `mpg_to_km_per_liter(mpg)` | MPG → km/L |
| `km_per_liter_to_mpg(kml)` | km/L → MPG |
| `quick_mpg_convert(value, from_unit, to_unit)` | 快速单位转换 |

### 油耗计算

| 函数 | 说明 |
|------|------|
| `calculate_consumption(distance_miles, fuel_gallons)` | 计算油耗指标 |
| `calculate_trip_fuel(distance_km, consumption_liters_per_100km, fuel_price_per_liter)` | 计算行程燃油成本 |

### 碳排放

| 函数 | 说明 |
|------|------|
| `calculate_carbon_emission(fuel_liters, fuel_type)` | 计算 CO2 排放量 |

### 续航估算

| 函数 | 说明 |
|------|------|
| `estimate_range(tank_capacity_liters, consumption_liters_per_100km, current_fuel_percentage)` | 估算续航里程 |

### 车辆比较

| 函数 | 说明 |
|------|------|
| `compare_vehicles(vehicle1_consumption, vehicle2_consumption, annual_distance_km, fuel_price_per_liter)` | 比较年度燃油成本 |

### 油耗评级

| 函数 | 说明 |
|------|------|
| `get_consumption_rating(liters_per_100km, vehicle_type)` | 获取油耗评级 |

## 支持的燃油类型

- `gasoline` - 汽油 (CO2: 2.31 kg/L)
- `diesel` - 柴油 (CO2: 2.68 kg/L)
- `ethanol_e85` - E85 乙醇 (CO2: 1.61 kg/L)
- `biodiesel` - 生物柴油 (CO2: 2.44 kg/L)

## 数据结构

### FuelConsumptionResult

```python
@dataclass
class FuelConsumptionResult:
    mpg: float                    # 英里每加仑
    liters_per_100km: float       # 升每百公里
    km_per_liter: float           # 公里每升
```

### TripFuelResult

```python
@dataclass
class TripFuelResult:
    fuel_needed_liters: float    # 需要燃油（升）
    fuel_needed_gallons: float    # 需要燃油（加仑）
    estimated_cost_local: float   # 预估成本（本地货币）
    estimated_cost_usd: float     # 预估成本（美元）
```

### CarbonEmissionResult

```python
@dataclass
class CarbonEmissionResult:
    co2_kg: float                 # CO2 排放量（千克）
    co2_tons: float              # CO2 排放量（吨）
    trees_needed: int            # 需要种植的树木数量来抵消
```

## 运行测试

```bash
python test_fuel_consumption_utils.py -v
```

## License

MIT License