"""
燃油消耗计算工具 (Fuel Consumption Utils)

提供汽车油耗相关的计算功能：
- MPG（英里每加仑）和 L/100km（升每百公里）转换
- 燃油成本估算
- 行程油耗计算
- 碳排放估算
- 油箱续航里程估算

零外部依赖，纯 Python 实现。
"""

from typing import Optional, Tuple
from dataclasses import dataclass


@dataclass
class FuelConsumptionResult:
    """燃油消耗计算结果"""
    mpg: float  # 英里每加仑
    liters_per_100km: float  # 升每百公里
    km_per_liter: float  # 公里每升


@dataclass
class TripFuelResult:
    """行程燃油消耗结果"""
    fuel_needed_liters: float  # 需要燃油（升）
    fuel_needed_gallons: float  # 需要燃油（加仑）
    estimated_cost_local: float  # 预估成本（本地货币）
    estimated_cost_usd: float  # 预估成本（美元）


@dataclass
class CarbonEmissionResult:
    """碳排放计算结果"""
    co2_kg: float  # CO2排放量（千克）
    co2_tons: float  # CO2排放量（吨）
    trees_needed: int  # 需要种植的树木数量来抵消


# 常量定义
MILES_TO_KM = 1.609344  # 英里转公里
KM_TO_MILES = 0.621371  # 公里转英里
GALLONS_TO_LITERS = 3.785411784  # 加仑转升
LITERS_TO_GALLONS = 0.264172  # 升转加仑

# 不同燃料的CO2排放因子 (kg CO2 per liter)
CO2_FACTORS = {
    'gasoline': 2.31,  # 汽油
    'diesel': 2.68,  # 柴油
    'ethanol_e85': 1.61,  # E85乙醇
    'biodiesel': 2.44,  # 生物柴油
}

# 每棵树每年吸收的CO2量 (kg)
TREE_CO2_ABSORPTION_PER_YEAR = 21.77


def mpg_to_liters_per_100km(mpg: float) -> float:
    """
    将 MPG（英里每加仑）转换为 L/100km（升每百公里）
    
    Args:
        mpg: 英里每加仑值
        
    Returns:
        升每百公里值
        
    Example:
        >>> mpg_to_liters_per_100km(30)
        7.84
    """
    if mpg <= 0:
        raise ValueError("MPG must be positive")
    
    # MPG -> L/100km: 235.215 / MPG
    return 235.215 / mpg


def liters_per_100km_to_mpg(liters_per_100km: float) -> float:
    """
    将 L/100km（升每百公里）转换为 MPG（英里每加仑）
    
    Args:
        liters_per_100km: 升每百公里值
        
    Returns:
        英里每加仑值
        
    Example:
        >>> liters_per_100km_to_mpg(8)
        29.40
    """
    if liters_per_100km <= 0:
        raise ValueError("Liters per 100km must be positive")
    
    return 235.215 / liters_per_100km


def km_per_liter_to_mpg(km_per_liter: float) -> float:
    """
    将公里每升转换为 MPG
    
    Args:
        km_per_liter: 公里每升值
        
    Returns:
        英里每加仑值
    """
    if km_per_liter <= 0:
        raise ValueError("Km per liter must be positive")
    
    # km/L -> MPG: km/L * KM_TO_MILES * LITERS_TO_GALLONS
    return km_per_liter * KM_TO_MILES / LITERS_TO_GALLONS


def mpg_to_km_per_liter(mpg: float) -> float:
    """
    将 MPG 转换为公里每升
    
    Args:
        mpg: 英里每加仑值
        
    Returns:
        公里每升值
    """
    if mpg <= 0:
        raise ValueError("MPG must be positive")
    
    return mpg * MILES_TO_KM * LITERS_TO_GALLONS


def calculate_consumption(
    distance_miles: Optional[float] = None,
    distance_km: Optional[float] = None,
    fuel_gallons: Optional[float] = None,
    fuel_liters: Optional[float] = None
) -> FuelConsumptionResult:
    """
    根据行程距离和燃油消耗计算油耗
    
    Args:
        distance_miles: 行程距离（英里）
        distance_km: 行程距离（公里）
        fuel_gallons: 燃油消耗（加仑）
        fuel_liters: 燃油消耗（升）
        
    Returns:
        FuelConsumptionResult 包含 MPG, L/100km, km/L
        
    Example:
        >>> result = calculate_consumption(distance_miles=300, fuel_gallons=10)
        >>> result.mpg
        30.0
    """
    # 确保至少有一种距离和燃油的单位
    if distance_miles is None and distance_km is None:
        raise ValueError("Must provide either distance_miles or distance_km")
    if fuel_gallons is None and fuel_liters is None:
        raise ValueError("Must provide either fuel_gallons or fuel_liters")
    
    # 转换到统一单位（公里和升）
    distance_km_val = distance_km if distance_km is not None else distance_miles * MILES_TO_KM
    fuel_liters_val = fuel_liters if fuel_liters is not None else fuel_gallons * GALLONS_TO_LITERS
    
    if distance_km_val <= 0 or fuel_liters_val <= 0:
        raise ValueError("Distance and fuel must be positive")
    
    # 计算各项指标
    km_per_liter = distance_km_val / fuel_liters_val
    liters_per_100km = 100 / km_per_liter
    mpg = km_per_liter_to_mpg(km_per_liter)
    
    return FuelConsumptionResult(
        mpg=round(mpg, 2),
        liters_per_100km=round(liters_per_100km, 2),
        km_per_liter=round(km_per_liter, 2)
    )


def calculate_trip_fuel(
    distance_km: float,
    consumption_liters_per_100km: float,
    fuel_price_per_liter: float = 7.5,
    usd_exchange_rate: float = 1.0
) -> TripFuelResult:
    """
    计算行程所需燃油和成本
    
    Args:
        distance_km: 行程距离（公里）
        consumption_liters_per_100km: 油耗（升/百公里）
        fuel_price_per_liter: 燃油单价（本地货币/升）
        usd_exchange_rate: 本地货币兑美元汇率
        
    Returns:
        TripFuelResult 包含燃油量和预估成本
        
    Example:
        >>> result = calculate_trip_fuel(500, 8, 7.5)
        >>> result.fuel_needed_liters
        40.0
    """
    if distance_km <= 0:
        raise ValueError("Distance must be positive")
    if consumption_liters_per_100km <= 0:
        raise ValueError("Consumption must be positive")
    
    fuel_needed_liters = distance_km * consumption_liters_per_100km / 100
    fuel_needed_gallons = fuel_needed_liters * LITERS_TO_GALLONS
    estimated_cost_local = fuel_needed_liters * fuel_price_per_liter
    estimated_cost_usd = estimated_cost_local / usd_exchange_rate
    
    return TripFuelResult(
        fuel_needed_liters=round(fuel_needed_liters, 2),
        fuel_needed_gallons=round(fuel_needed_gallons, 2),
        estimated_cost_local=round(estimated_cost_local, 2),
        estimated_cost_usd=round(estimated_cost_usd, 2)
    )


def calculate_carbon_emission(
    fuel_liters: float,
    fuel_type: str = 'gasoline'
) -> CarbonEmissionResult:
    """
    计算燃油消耗产生的碳排放
    
    Args:
        fuel_liters: 燃油消耗量（升）
        fuel_type: 燃油类型（gasoline, diesel, ethanol_e85, biodiesel）
        
    Returns:
        CarbonEmissionResult 包含CO2排放量和需要抵消的树木数
        
    Example:
        >>> result = calculate_carbon_emission(40, 'gasoline')
        >>> result.co2_kg
        92.4
    """
    if fuel_liters <= 0:
        raise ValueError("Fuel amount must be positive")
    
    fuel_type_lower = fuel_type.lower()
    if fuel_type_lower not in CO2_FACTORS:
        raise ValueError(f"Unknown fuel type: {fuel_type}. Supported: {list(CO2_FACTORS.keys())}")
    
    co2_factor = CO2_FACTORS[fuel_type_lower]
    co2_kg = fuel_liters * co2_factor
    co2_tons = co2_kg / 1000
    trees_needed = int(co2_kg / TREE_CO2_ABSORPTION_PER_YEAR) + 1
    
    return CarbonEmissionResult(
        co2_kg=round(co2_kg, 2),
        co2_tons=round(co2_tons, 4),
        trees_needed=trees_needed
    )


def estimate_range(
    tank_capacity_liters: float,
    consumption_liters_per_100km: float,
    current_fuel_percentage: float = 100
) -> Tuple[float, float]:
    """
    估算车辆续航里程
    
    Args:
        tank_capacity_liters: 油箱容量（升）
        consumption_liters_per_100km: 油耗（升/百公里）
        current_fuel_percentage: 当前油量百分比（0-100）
        
    Returns:
        (续航公里数, 续航英里数)
        
    Example:
        >>> km, miles = estimate_range(50, 8, 50)
        >>> km
        312.5
    """
    if tank_capacity_liters <= 0:
        raise ValueError("Tank capacity must be positive")
    if consumption_liters_per_100km <= 0:
        raise ValueError("Consumption must be positive")
    if current_fuel_percentage < 0 or current_fuel_percentage > 100:
        raise ValueError("Fuel percentage must be between 0 and 100")
    
    current_fuel_liters = tank_capacity_liters * current_fuel_percentage / 100
    range_km = current_fuel_liters * 100 / consumption_liters_per_100km
    range_miles = range_km * KM_TO_MILES
    
    return round(range_km, 2), round(range_miles, 2)


def compare_vehicles(
    vehicle1_consumption: float,
    vehicle2_consumption: float,
    annual_distance_km: float = 15000,
    fuel_price_per_liter: float = 7.5
) -> dict:
    """
    比较两辆车的年度燃油成本
    
    Args:
        vehicle1_consumption: 车辆1油耗（升/百公里）
        vehicle2_consumption: 车辆2油耗（升/百公里）
        annual_distance_km: 年度行驶里程（公里）
        fuel_price_per_liter: 燃油单价
        
    Returns:
        包含两辆车年度成本和节省金额的字典
        
    Example:
        >>> compare_vehicles(10, 7, 15000, 7.5)
        {'vehicle1_cost': 11250.0, 'vehicle2_cost': 7875.0, 'savings': 3375.0}
    """
    if vehicle1_consumption <= 0 or vehicle2_consumption <= 0:
        raise ValueError("Consumption values must be positive")
    
    fuel1 = annual_distance_km * vehicle1_consumption / 100
    fuel2 = annual_distance_km * vehicle2_consumption / 100
    
    cost1 = fuel1 * fuel_price_per_liter
    cost2 = fuel2 * fuel_price_per_liter
    
    savings = abs(cost1 - cost2)
    better_vehicle = 2 if vehicle2_consumption < vehicle1_consumption else 1
    
    return {
        'vehicle1_cost': round(cost1, 2),
        'vehicle1_fuel_liters': round(fuel1, 2),
        'vehicle2_cost': round(cost2, 2),
        'vehicle2_fuel_liters': round(fuel2, 2),
        'annual_savings': round(savings, 2),
        'better_vehicle': better_vehicle,
        'vehicle1_mpg': round(liters_per_100km_to_mpg(vehicle1_consumption), 2),
        'vehicle2_mpg': round(liters_per_100km_to_mpg(vehicle2_consumption), 2)
    }


def get_consumption_rating(liters_per_100km: float, vehicle_type: str = 'car') -> str:
    """
    根据油耗给出评级
    
    Args:
        liters_per_100km: 油耗（升/百公里）
        vehicle_type: 车辆类型（car, suv, truck）
        
    Returns:
        评级字符串（Excellent, Good, Average, Poor, Very Poor）
        
    Example:
        >>> get_consumption_rating(5)
        'Excellent'
    """
    if liters_per_100km <= 0:
        raise ValueError("Consumption must be positive")
    
    # 不同车型有不同的评级标准
    ratings = {
        'car': {
            'Excellent': 6,
            'Good': 8,
            'Average': 10,
            'Poor': 12,
        },
        'suv': {
            'Excellent': 8,
            'Good': 10,
            'Average': 12,
            'Poor': 14,
        },
        'truck': {
            'Excellent': 10,
            'Good': 12,
            'Average': 15,
            'Poor': 18,
        }
    }
    
    vehicle_type_lower = vehicle_type.lower()
    if vehicle_type_lower not in ratings:
        vehicle_type_lower = 'car'  # 默认使用轿车标准
    
    thresholds = ratings[vehicle_type_lower]
    
    if liters_per_100km <= thresholds['Excellent']:
        return 'Excellent ⭐⭐⭐⭐⭐'
    elif liters_per_100km <= thresholds['Good']:
        return 'Good ⭐⭐⭐⭐'
    elif liters_per_100km <= thresholds['Average']:
        return 'Average ⭐⭐⭐'
    elif liters_per_100km <= thresholds['Poor']:
        return 'Poor ⭐⭐'
    else:
        return 'Very Poor ⭐'


def format_consumption(result: FuelConsumptionResult) -> str:
    """
    格式化油耗结果为可读字符串
    
    Args:
        result: FuelConsumptionResult 对象
        
    Returns:
        格式化后的字符串
    """
    return (
        f"燃油消耗指标:\n"
        f"  MPG (英里/加仑): {result.mpg}\n"
        f"  L/100km (升/百公里): {result.liters_per_100km}\n"
        f"  km/L (公里/升): {result.km_per_liter}"
    )


# 便捷函数
def quick_mpg_convert(value: float, from_unit: str, to_unit: str) -> float:
    """
    快速油耗单位转换
    
    Args:
        value: 原始值
        from_unit: 原始单位（mpg, l100km, kml）
        to_unit: 目标单位（mpg, l100km, kml）
        
    Returns:
        转换后的值
        
    Example:
        >>> quick_mpg_convert(30, 'mpg', 'l100km')
        7.84
    """
    from_unit_lower = from_unit.lower()
    to_unit_lower = to_unit.lower()
    
    conversions = {
        ('mpg', 'l100km'): mpg_to_liters_per_100km,
        ('l100km', 'mpg'): liters_per_100km_to_mpg,
        ('mpg', 'kml'): mpg_to_km_per_liter,
        ('kml', 'mpg'): km_per_liter_to_mpg,
        ('l100km', 'kml'): lambda x: 100 / x,
        ('kml', 'l100km'): lambda x: 100 / x,
    }
    
    # 相同单位直接返回
    if from_unit_lower == to_unit_lower:
        return round(value, 2)
    
    key = (from_unit_lower, to_unit_lower)
    if key not in conversions:
        raise ValueError(f"Unsupported conversion: {from_unit} -> {to_unit}")
    
    return round(conversions[key](value), 2)


if __name__ == "__main__":
    # 演示用法
    print("=" * 60)
    print("燃油消耗计算工具演示")
    print("=" * 60)
    
    # 1. MPG 转换
    print("\n1. 单位转换:")
    mpg = 30
    l100km = mpg_to_liters_per_100km(mpg)
    print(f"   {mpg} MPG = {l100km} L/100km")
    
    # 2. 油耗计算
    print("\n2. 油耗计算:")
    result = calculate_consumption(distance_miles=300, fuel_gallons=10)
    print(format_consumption(result))
    
    # 3. 行程燃油估算
    print("\n3. 行程燃油估算:")
    trip = calculate_trip_fuel(distance_km=500, consumption_liters_per_100km=8, fuel_price_per_liter=7.5)
    print(f"   500公里行程需要: {trip.fuel_needed_liters} 升燃油")
    print(f"   预估成本: ¥{trip.estimated_cost_local}")
    
    # 4. 碳排放计算
    print("\n4. 碳排放计算:")
    carbon = calculate_carbon_emission(fuel_liters=40, fuel_type='gasoline')
    print(f"   40升汽油产生: {carbon.co2_kg} kg CO2")
    print(f"   需种植 {carbon.trees_needed} 棵树来抵消")
    
    # 5. 续航里程估算
    print("\n5. 续航里程估算:")
    tank = 50
    consumption = 8
    range_km, range_miles = estimate_range(tank, consumption, 50)
    print(f"   油箱{tank}升，油耗{consumption}L/100km，50%油量")
    print(f"   续航里程: {range_km} km ({range_miles} miles)")
    
    # 6. 车辆比较
    print("\n6. 车辆油耗比较:")
    comparison = compare_vehicles(10, 7, 15000, 7.5)
    print(f"   车辆1油耗10L/100km - 年度成本: ¥{comparison['vehicle1_cost']}")
    print(f"   车辆2油耗7L/100km - 年度成本: ¥{comparison['vehicle2_cost']}")
    print(f"   年节省: ¥{comparison['annual_savings']}")
    
    # 7. 油耗评级
    print("\n7. 油耗评级:")
    rating = get_consumption_rating(5, 'car')
    print(f"   5L/100km 评级: {rating}")