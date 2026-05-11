"""
Fuel Efficiency Utils - 燃油效率计算工具
==========================================

提供各种燃油效率、油耗和碳排放计算功能，无需外部依赖。

功能列表:
- 油耗转换 (MPG ↔ L/100km)
- 燃油成本计算
- 行驶里程计算
- 碳排放计算
- 油箱续航里程
- 混合动力效率
- 燃油效率评级
- 多种燃油类型支持

作者: AllToolkit 自动化生成
日期: 2026-05-11
"""

from typing import Tuple, Dict, Any, Optional, List
from enum import Enum


class FuelType(Enum):
    """燃油类型枚举"""
    GASOLINE = "gasoline"          # 汽油
    DIESEL = "diesel"              # 柴油
    HYBRID = "hybrid"              # 混合动力
    ELECTRIC = "electric"          # 纯电动
    PLUG_IN_HYBRID = "plug_in_hybrid"  # 插电混动
    NATURAL_GAS = "natural_gas"    # 天然气
    E85 = "e85"                    # E85乙醇汽油


class FuelEfficiencyCalculator:
    """燃油效率计算器"""
    
    # 燃油特性常量
    FUEL_PROPERTIES = {
        FuelType.GASOLINE: {
            'density': 0.7489,           # kg/L
            'co2_per_liter': 2.31,       # kg CO2/L
            'energy_density': 34.2,      # MJ/L
            'name_cn': '汽油',
            'name_en': 'Gasoline'
        },
        FuelType.DIESEL: {
            'density': 0.832,
            'co2_per_liter': 2.68,
            'energy_density': 38.6,
            'name_cn': '柴油',
            'name_en': 'Diesel'
        },
        FuelType.HYBRID: {
            'density': 0.7489,
            'co2_per_liter': 2.31,
            'energy_density': 34.2,
            'name_cn': '混合动力',
            'name_en': 'Hybrid'
        },
        FuelType.PLUG_IN_HYBRID: {
            'density': 0.7489,
            'co2_per_liter': 2.31,
            'energy_density': 34.2,
            'name_cn': '插电混动',
            'name_en': 'Plug-in Hybrid'
        },
        FuelType.NATURAL_GAS: {
            'density': 0.00068,          # kg/L (气态)
            'co2_per_liter': 0.0019,     # kg CO2/L (气态)
            'energy_density': 0.038,     # MJ/L (气态)
            'name_cn': '天然气',
            'name_en': 'Natural Gas'
        },
        FuelType.E85: {
            'density': 0.78,
            'co2_per_liter': 1.62,       # 部分可再生，排放较低
            'energy_density': 25.2,
            'name_cn': 'E85乙醇汽油',
            'name_en': 'E85 Ethanol'
        },
        FuelType.ELECTRIC: {
            'density': 0,
            'co2_per_liter': 0,
            'energy_density': 0,
            'name_cn': '纯电动',
            'name_en': 'Electric'
        }
    }
    
    # 电网碳排放因子 (kg CO2/kWh)，因地区而异
    GRID_EMISSION_FACTORS = {
        'china': 0.5839,        # 中国平均
        'us': 0.417,            # 美国平均
        'eu': 0.255,            # 欧盟平均
        'world': 0.462,         # 世界平均
        'clean': 0.05,          # 清洁能源电网
        'dirty': 0.9            # 高碳电网
    }
    
    @staticmethod
    def mpg_to_lp100k(mpg: float, us_gallon: bool = True) -> float:
        """
        将 MPG (英里/加仑) 转换为 L/100km (升/百公里)
        
        Args:
            mpg: 英里每加仑
            us_gallon: True 使用美制加仑，False 使用英制加仑
            
        Returns:
            升每百公里
            
        Example:
            >>> round(FuelEfficiencyCalculator.mpg_to_lp100k(30), 1)
            7.8
            >>> round(FuelEfficiencyCalculator.mpg_to_lp100k(30, False), 1)
            9.4
        """
        if mpg <= 0:
            raise ValueError("MPG 必须大于 0")
        
        # 美制加仑 = 3.78541 升
        # 英制加仑 = 4.54609 升
        # 1 英里 = 1.60934 公里
        
        gallon_to_liter = 3.78541 if us_gallon else 4.54609
        mile_to_km = 1.60934
        
        # 转换公式: L/100km = 100 * (升/加仑) / (英里/加仑 * 公里/英里)
        #         = 100 * gallon_to_liter / (mpg * mile_to_km)
        lp100k = 100 * gallon_to_liter / (mpg * mile_to_km)
        
        return round(lp100k, 2)
    
    @staticmethod
    def lp100k_to_mpg(lp100k: float, us_gallon: bool = True) -> float:
        """
        将 L/100km (升/百公里) 转换为 MPG (英里/加仑)
        
        Args:
            lp100k: 升每百公里
            us_gallon: True 使用美制加仑，False 使用英制加仑
            
        Returns:
            英里每加仑
            
        Example:
            >>> round(FuelEfficiencyCalculator.lp100k_to_mpg(7.8), 1)
            30.2
        """
        if lp100k <= 0:
            raise ValueError("L/100km 必须大于 0")
        
        gallon_to_liter = 3.78541 if us_gallon else 4.54609
        mile_to_km = 1.60934
        
        mpg = 100 * gallon_to_liter / (lp100k * mile_to_km)
        
        return round(mpg, 1)
    
    @staticmethod
    def km_per_liter_to_lp100k(km_per_liter: float) -> float:
        """
        将 km/L (公里/升) 转换为 L/100km
        
        Args:
            km_per_liter: 公里每升
            
        Returns:
            升每百公里
            
        Example:
            >>> FuelEfficiencyCalculator.km_per_liter_to_lp100k(12.8)
            7.81
        """
        if km_per_liter <= 0:
            raise ValueError("km/L 必须大于 0")
        
        return round(100 / km_per_liter, 2)
    
    @staticmethod
    def lp100k_to_km_per_liter(lp100k: float) -> float:
        """
        将 L/100km 转换为 km/L
        
        Args:
            lp100k: 升每百公里
            
        Returns:
            公里每升
            
        Example:
            >>> round(FuelEfficiencyCalculator.lp100k_to_km_per_liter(7.8), 1)
            12.8
        """
        if lp100k <= 0:
            raise ValueError("L/100km 必须大于 0")
        
        return round(100 / lp100k, 2)
    
    @staticmethod
    def calculate_fuel_cost(
        distance: float,
        efficiency: float,
        fuel_price: float,
        efficiency_unit: str = 'lp100k',
        distance_unit: str = 'km'
    ) -> float:
        """
        计算燃油成本
        
        Args:
            distance: 行驶距离
            efficiency: 燃油效率
            fuel_price: 燃油价格 (每升或每加仑)
            efficiency_unit: 效率单位 ('lp100k', 'mpg', 'kmpl')
            distance_unit: 距离单位 ('km', 'mile')
            
        Returns:
            燃油成本
            
        Example:
            >>> round(FuelEfficiencyCalculator.calculate_fuel_cost(500, 8, 8.5), 1)
            340.0
        """
        # 标准化距离为公里
        if distance_unit == 'mile':
            distance_km = distance * 1.60934
        else:
            distance_km = distance
        
        # 标准化效率为 L/100km
        if efficiency_unit == 'mpg':
            lp100k = FuelEfficiencyCalculator.mpg_to_lp100k(efficiency)
        elif efficiency_unit == 'kmpl':
            lp100k = FuelEfficiencyCalculator.km_per_liter_to_lp100k(efficiency)
        else:
            lp100k = efficiency
        
        # 计算所需燃油量 (升)
        fuel_needed = distance_km * lp100k / 100
        
        # 计算成本
        cost = fuel_needed * fuel_price
        
        return round(cost, 2)
    
    @staticmethod
    def calculate_range(
        fuel_amount: float,
        efficiency: float,
        efficiency_unit: str = 'lp100k',
        fuel_unit: str = 'liter'
    ) -> float:
        """
        计算续航里程
        
        Args:
            fuel_amount: 燃油量
            efficiency: 燃油效率
            efficiency_unit: 效率单位 ('lp100k', 'mpg', 'kmpl')
            fuel_unit: 燃油单位 ('liter', 'us_gallon', 'uk_gallon')
            
        Returns:
            续航里程 (公里)
            
        Example:
            >>> FuelEfficiencyCalculator.calculate_range(50, 8)
            625.0
        """
        # 标准化燃油量为升
        if fuel_unit == 'us_gallon':
            fuel_liters = fuel_amount * 3.78541
        elif fuel_unit == 'uk_gallon':
            fuel_liters = fuel_amount * 4.54609
        else:
            fuel_liters = fuel_amount
        
        # 标准化效率为 L/100km
        if efficiency_unit == 'mpg':
            lp100k = FuelEfficiencyCalculator.mpg_to_lp100k(efficiency)
        elif efficiency_unit == 'kmpl':
            lp100k = FuelEfficiencyCalculator.km_per_liter_to_lp100k(efficiency)
        else:
            lp100k = efficiency
        
        # 计算续航里程
        range_km = fuel_liters / lp100k * 100
        
        return round(range_km, 1)
    
    @staticmethod
    def calculate_co2_emissions(
        distance: float,
        efficiency: float,
        fuel_type: FuelType = FuelType.GASOLINE,
        efficiency_unit: str = 'lp100k',
        distance_unit: str = 'km'
    ) -> float:
        """
        计算 CO2 排放量
        
        Args:
            distance: 行驶距离
            efficiency: 燃油效率
            fuel_type: 燃油类型
            efficiency_unit: 效率单位
            distance_unit: 距离单位
            
        Returns:
            CO2 排放量 (kg)
            
        Example:
            >>> round(FuelEfficiencyCalculator.calculate_co2_emissions(100, 8), 1)
            18.5
        """
        if fuel_type == FuelType.ELECTRIC:
            return 0.0  # 直接排放为 0
        
        # 标准化距离为公里
        if distance_unit == 'mile':
            distance_km = distance * 1.60934
        else:
            distance_km = distance
        
        # 标准化效率为 L/100km
        if efficiency_unit == 'mpg':
            lp100k = FuelEfficiencyCalculator.mpg_to_lp100k(efficiency)
        elif efficiency_unit == 'kmpl':
            lp100k = FuelEfficiencyCalculator.km_per_liter_to_lp100k(efficiency)
        else:
            lp100k = efficiency
        
        # 计算燃油消耗量 (升)
        fuel_consumed = distance_km * lp100k / 100
        
        # 获取燃油 CO2 排放因子
        co2_factor = FuelEfficiencyCalculator.FUEL_PROPERTIES[fuel_type]['co2_per_liter']
        
        # 计算 CO2 排放量
        co2_emissions = fuel_consumed * co2_factor
        
        return round(co2_emissions, 2)
    
    @staticmethod
    def calculate_electric_emissions(
        distance: float,
        efficiency: float,  # kWh/100km
        region: str = 'world'
    ) -> float:
        """
        计算电动汽车间接 CO2 排放量
        
        Args:
            distance: 行驶距离 (公里)
            efficiency: 能耗效率 (kWh/100km)
            region: 电网区域 ('china', 'us', 'eu', 'world', 'clean', 'dirty')
            
        Returns:
            CO2 排放量 (kg)
            
        Example:
            >>> round(FuelEfficiencyCalculator.calculate_electric_emissions(100, 15, 'china'), 1)
            8.8
        """
        # 计算耗电量 (kWh)
        energy_consumed = distance * efficiency / 100
        
        # 获取电网排放因子
        emission_factor = FuelEfficiencyCalculator.GRID_EMISSION_FACTORS.get(region, 0.462)
        
        # 计算排放量
        co2_emissions = energy_consumed * emission_factor
        
        return round(co2_emissions, 2)
    
    @staticmethod
    def calculate_annual_fuel_cost(
        annual_distance: float,
        efficiency: float,
        fuel_price: float,
        efficiency_unit: str = 'lp100k',
        distance_unit: str = 'km'
    ) -> Dict[str, Any]:
        """
        计算年度燃油成本
        
        Args:
            annual_distance: 年行驶里程
            efficiency: 燃油效率
            fuel_price: 燃油价格
            efficiency_unit: 效率单位
            distance_unit: 距离单位
            
        Returns:
            包含年度成本、月度成本、燃油消耗量的字典
            
        Example:
            >>> result = FuelEfficiencyCalculator.calculate_annual_fuel_cost(15000, 8, 8.5)
            >>> result['annual_cost']
            10200.0
        """
        annual_cost = FuelEfficiencyCalculator.calculate_fuel_cost(
            annual_distance, efficiency, fuel_price, efficiency_unit, distance_unit
        )
        
        # 标准化距离为公里
        if distance_unit == 'mile':
            distance_km = annual_distance * 1.60934
        else:
            distance_km = annual_distance
        
        # 标准化效率为 L/100km
        if efficiency_unit == 'mpg':
            lp100k = FuelEfficiencyCalculator.mpg_to_lp100k(efficiency)
        elif efficiency_unit == 'kmpl':
            lp100k = FuelEfficiencyCalculator.km_per_liter_to_lp100k(efficiency)
        else:
            lp100k = efficiency
        
        # 计算燃油消耗量
        fuel_consumed = distance_km * lp100k / 100
        
        return {
            'annual_cost': annual_cost,
            'monthly_cost': round(annual_cost / 12, 2),
            'weekly_cost': round(annual_cost / 52, 2),
            'daily_cost': round(annual_cost / 365, 2),
            'fuel_consumed_liters': round(fuel_consumed, 2),
            'fuel_consumed_gallons_us': round(fuel_consumed / 3.78541, 2)
        }
    
    @staticmethod
    def compare_vehicles(
        distance: float,
        efficiency1: float,
        efficiency2: float,
        fuel_price: float,
        efficiency_unit: str = 'lp100k',
        distance_unit: str = 'km'
    ) -> Dict[str, Any]:
        """
        比较两辆车的燃油成本
        
        Args:
            distance: 行驶距离
            efficiency1: 车辆1的燃油效率
            efficiency2: 车辆2的燃油效率
            fuel_price: 燃油价格
            efficiency_unit: 效率单位
            distance_unit: 距离单位
            
        Returns:
            包含两车成本对比的字典
            
        Example:
            >>> result = FuelEfficiencyCalculator.compare_vehicles(500, 10, 6, 8.5)
            >>> result['savings']
            170.0
        """
        cost1 = FuelEfficiencyCalculator.calculate_fuel_cost(
            distance, efficiency1, fuel_price, efficiency_unit, distance_unit
        )
        cost2 = FuelEfficiencyCalculator.calculate_fuel_cost(
            distance, efficiency2, fuel_price, efficiency_unit, distance_unit
        )
        
        savings = cost1 - cost2
        
        return {
            'vehicle1_cost': cost1,
            'vehicle2_cost': cost2,
            'savings': savings,
            'more_efficient': 'vehicle2' if savings > 0 else 'vehicle1',
            'percentage_improvement': round(abs(savings) / cost1 * 100, 1) if cost1 > 0 else 0
        }
    
    @staticmethod
    def efficiency_rating(
        efficiency: float,
        vehicle_type: str = 'car',
        efficiency_unit: str = 'lp100k'
    ) -> Tuple[str, str, str]:
        """
        评估燃油效率等级
        
        Args:
            efficiency: 燃油效率
            vehicle_type: 车辆类型 ('car', 'suv', 'truck', 'motorcycle')
            efficiency_unit: 效率单位
            
        Returns:
            (等级, 中文描述, 建议)
            
        Example:
            >>> FuelEfficiencyCalculator.efficiency_rating(5)
            ('A+', '卓越', '极低油耗，非常环保')
        """
        # 标准化为 L/100km
        if efficiency_unit == 'mpg':
            lp100k = FuelEfficiencyCalculator.mpg_to_lp100k(efficiency)
        elif efficiency_unit == 'kmpl':
            lp100k = FuelEfficiencyCalculator.km_per_liter_to_lp100k(efficiency)
        else:
            lp100k = efficiency
        
        # 根据车辆类型定义效率等级阈值
        thresholds = {
            'car': [
                (5, ('A+', '卓越', '极低油耗，非常环保')),
                (6, ('A', '优秀', '低油耗，经济实惠')),
                (7.5, ('B+', '良好+', '油耗较低')),
                (9, ('B', '良好', '油耗中等')),
                (11, ('C', '一般', '油耗偏高')),
                (13, ('D', '较差', '油耗较高，建议优化驾驶习惯')),
                (float('inf'), ('E', '高油耗', '油耗很高，建议更换车辆'))
            ],
            'suv': [
                (7, ('A+', '卓越', 'SUV中的省油王')),
                (8.5, ('A', '优秀', '低油耗SUV')),
                (10, ('B+', '良好+', '油耗较低')),
                (12, ('B', '良好', '油耗中等')),
                (14, ('C', '一般', '油耗偏高')),
                (16, ('D', '较差', '油耗较高')),
                (float('inf'), ('E', '高油耗', '油耗很高'))
            ],
            'truck': [
                (12, ('A+', '卓越', '卡车的省油典范')),
                (15, ('A', '优秀', '油耗较低')),
                (18, ('B+', '良好+', '油耗可接受')),
                (22, ('B', '良好', '油耗中等')),
                (26, ('C', '一般', '油耗偏高')),
                (30, ('D', '较差', '油耗较高')),
                (float('inf'), ('E', '高油耗', '油耗很高'))
            ],
            'motorcycle': [
                (2.5, ('A+', '卓越', '极低油耗')),
                (3, ('A', '优秀', '低油耗')),
                (3.5, ('B+', '良好+', '油耗较低')),
                (4, ('B', '良好', '油耗中等')),
                (4.5, ('C', '一般', '油耗偏高')),
                (5, ('D', '较差', '油耗较高')),
                (float('inf'), ('E', '高油耗', '摩托车中油耗很高'))
            ]
        }
        
        # 获取对应车辆类型的阈值
        threshold_list = thresholds.get(vehicle_type, thresholds['car'])
        
        # 查找对应等级
        for threshold, rating in threshold_list:
            if lp100k <= threshold:
                return rating
        
        return threshold_list[-1][1]  # 默认返回最低等级
    
    @staticmethod
    def calculate_break_even(
        efficient_car_cost: float,
        efficient_car_efficiency: float,
        inefficient_car_cost: float,
        inefficient_car_efficiency: float,
        fuel_price: float,
        efficiency_unit: str = 'lp100k'
    ) -> Dict[str, Any]:
        """
        计算省油车的回本里程
        
        当省油车价格较高但油耗低时，计算需要行驶多少公里才能省回差价。
        
        Args:
            efficient_car_cost: 省油车价格
            efficient_car_efficiency: 省油车油耗
            inefficient_car_cost: 普通车价格
            inefficient_car_efficiency: 普通车油耗
            fuel_price: 燃油价格
            efficiency_unit: 效率单位
            
        Returns:
            包含回本分析的字典
            
        Example:
            >>> result = FuelEfficiencyCalculator.calculate_break_even(200000, 5, 150000, 8, 8.5)
            >>> result['break_even_km'] > 0
            True
        """
        price_diff = efficient_car_cost - inefficient_car_cost
        
        # 标准化效率为 L/100km
        if efficiency_unit == 'mpg':
            eff_lp100k = FuelEfficiencyCalculator.mpg_to_lp100k(efficient_car_efficiency)
            ineff_lp100k = FuelEfficiencyCalculator.mpg_to_lp100k(inefficient_car_efficiency)
        elif efficiency_unit == 'kmpl':
            eff_lp100k = FuelEfficiencyCalculator.km_per_liter_to_lp100k(efficient_car_efficiency)
            ineff_lp100k = FuelEfficiencyCalculator.km_per_liter_to_lp100k(inefficient_car_efficiency)
        else:
            eff_lp100k = efficient_car_efficiency
            ineff_lp100k = inefficient_car_efficiency
        
        # 计算每公里节省的成本
        cost_per_km_efficient = eff_lp100k / 100 * fuel_price
        cost_per_km_inefficient = ineff_lp100k / 100 * fuel_price
        savings_per_km = cost_per_km_inefficient - cost_per_km_efficient
        
        if savings_per_km <= 0:
            # 省油车实际上不省油
            return {
                'price_difference': price_diff,
                'break_even_km': -1,
                'break_even_years': -1,
                'savings_per_km': savings_per_km,
                'message': '省油车的油耗不比普通车低，无法回本'
            }
        
        # 计算回本里程
        break_even_km = price_diff / savings_per_km
        
        # 假设每年行驶 15000 公里
        annual_distance = 15000
        break_even_years = break_even_km / annual_distance
        
        return {
            'price_difference': round(price_diff, 2),
            'break_even_km': round(break_even_km, 0),
            'break_even_years': round(break_even_years, 1),
            'savings_per_km': round(savings_per_km, 4),
            'message': f'需要行驶 {round(break_even_km, 0):,} 公里（约 {round(break_even_years, 1)} 年）才能省回差价'
        }
    
    @staticmethod
    def calculate_trip_fuel(
        distance: float,
        efficiency: float,
        fuel_price: float,
        passengers: int = 1,
        efficiency_unit: str = 'lp100k',
        distance_unit: str = 'km'
    ) -> Dict[str, Any]:
        """
        计算旅行燃油成本
        
        Args:
            distance: 行驶距离
            efficiency: 燃油效率
            fuel_price: 燃油价格
            passengers: 乘客人数（用于分摊成本）
            efficiency_unit: 效率单位
            distance_unit: 距离单位
            
        Returns:
            包含旅行燃油信息的字典
            
        Example:
            >>> result = FuelEfficiencyCalculator.calculate_trip_fuel(300, 8, 8.5, 4)
            >>> result['total_cost']
            204.0
        """
        total_cost = FuelEfficiencyCalculator.calculate_fuel_cost(
            distance, efficiency, fuel_price, efficiency_unit, distance_unit
        )
        
        # 标准化距离为公里
        if distance_unit == 'mile':
            distance_km = distance * 1.60934
        else:
            distance_km = distance
        
        # 标准化效率为 L/100km
        if efficiency_unit == 'mpg':
            lp100k = FuelEfficiencyCalculator.mpg_to_lp100k(efficiency)
        elif efficiency_unit == 'kmpl':
            lp100k = FuelEfficiencyCalculator.km_per_liter_to_km_per_liter(efficiency)
        else:
            lp100k = efficiency
        
        fuel_needed = distance_km * lp100k / 100
        
        return {
            'distance_km': round(distance_km, 1),
            'distance_miles': round(distance_km / 1.60934, 1),
            'efficiency_lp100k': lp100k,
            'fuel_needed_liters': round(fuel_needed, 2),
            'fuel_needed_gallons': round(fuel_needed / 3.78541, 2),
            'fuel_price': fuel_price,
            'total_cost': total_cost,
            'cost_per_km': round(total_cost / distance_km, 3),
            'cost_per_mile': round(total_cost / distance_km * 1.60934, 3),
            'cost_per_passenger': round(total_cost / passengers, 2) if passengers > 0 else total_cost
        }
    
    @staticmethod
    def full_efficiency_report(
        efficiency: float,
        annual_distance: float = 15000,
        fuel_price: float = 8.5,
        fuel_type: FuelType = FuelType.GASOLINE,
        vehicle_type: str = 'car',
        efficiency_unit: str = 'lp100k',
        distance_unit: str = 'km'
    ) -> Dict[str, Any]:
        """
        生成完整的燃油效率报告
        
        Args:
            efficiency: 燃油效率
            annual_distance: 年行驶里程
            fuel_price: 燃油价格
            fuel_type: 燃油类型
            vehicle_type: 车辆类型
            efficiency_unit: 效率单位
            distance_unit: 距离单位
            
        Returns:
            包含完整效率报告的字典
            
        Example:
            >>> report = FuelEfficiencyCalculator.full_efficiency_report(8)
            >>> 'annual_cost' in report
            True
        """
        # 标准化效率为 L/100km
        if efficiency_unit == 'mpg':
            lp100k = FuelEfficiencyCalculator.mpg_to_lp100k(efficiency)
        elif efficiency_unit == 'kmpl':
            lp100k = FuelEfficiencyCalculator.km_per_liter_to_km_per_liter(efficiency)
        else:
            lp100k = efficiency
        
        # 标准化距离为公里
        if distance_unit == 'mile':
            distance_km = annual_distance * 1.60934
        else:
            distance_km = annual_distance
        
        # 计算各种效率表示
        mpg_us = FuelEfficiencyCalculator.lp100k_to_mpg(lp100k, us_gallon=True)
        mpg_uk = FuelEfficiencyCalculator.lp100k_to_mpg(lp100k, us_gallon=False)
        kmpl = FuelEfficiencyCalculator.lp100k_to_km_per_liter(lp100k)
        
        # 计算年度成本
        annual_costs = FuelEfficiencyCalculator.calculate_annual_fuel_cost(
            distance_km, lp100k, fuel_price, 'lp100k', 'km'
        )
        
        # 计算碳排放
        co2_emissions = FuelEfficiencyCalculator.calculate_co2_emissions(
            distance_km, lp100k, fuel_type, 'lp100k', 'km'
        )
        
        # 效率评级
        rating = FuelEfficiencyCalculator.efficiency_rating(lp100k, vehicle_type, 'lp100k')
        
        # 燃油特性
        fuel_props = FuelEfficiencyCalculator.FUEL_PROPERTIES[fuel_type]
        
        return {
            'efficiency': {
                'lp100k': lp100k,
                'mpg_us': mpg_us,
                'mpg_uk': mpg_uk,
                'km_per_liter': kmpl
            },
            'annual_costs': annual_costs,
            'co2_emissions_kg': co2_emissions,
            'efficiency_rating': {
                'grade': rating[0],
                'description': rating[1],
                'suggestion': rating[2]
            },
            'fuel_info': {
                'type': fuel_type.value,
                'name_cn': fuel_props['name_cn'],
                'name_en': fuel_props['name_en'],
                'co2_per_liter': fuel_props['co2_per_liter']
            },
            'vehicle_type': vehicle_type,
            'assumptions': {
                'annual_distance_km': distance_km,
                'fuel_price': fuel_price
            }
        }


# 便捷函数
def mpg_to_lp100k(mpg: float, us_gallon: bool = True) -> float:
    """将 MPG 转换为 L/100km"""
    return FuelEfficiencyCalculator.mpg_to_lp100k(mpg, us_gallon)


def lp100k_to_mpg(lp100k: float, us_gallon: bool = True) -> float:
    """将 L/100km 转换为 MPG"""
    return FuelEfficiencyCalculator.lp100k_to_mpg(lp100k, us_gallon)


def calculate_fuel_cost(distance: float, efficiency: float, fuel_price: float,
                       efficiency_unit: str = 'lp100k') -> float:
    """计算燃油成本"""
    return FuelEfficiencyCalculator.calculate_fuel_cost(
        distance, efficiency, fuel_price, efficiency_unit
    )


def calculate_co2(distance: float, efficiency: float, 
                 fuel_type: FuelType = FuelType.GASOLINE,
                 efficiency_unit: str = 'lp100k') -> float:
    """计算 CO2 排放量"""
    return FuelEfficiencyCalculator.calculate_co2_emissions(
        distance, efficiency, fuel_type, efficiency_unit
    )


if __name__ == '__main__':
    print("=" * 60)
    print("Fuel Efficiency Utils - 燃油效率计算工具演示")
    print("=" * 60)
    
    # MPG 转换
    print("\n【单位转换】")
    print(f"30 MPG (美制) = {mpg_to_lp100k(30)} L/100km")
    print(f"30 MPG (英制) = {mpg_to_lp100k(30, False)} L/100km")
    print(f"8 L/100km = {lp100k_to_mpg(8)} MPG (美制)")
    print(f"8 L/100km = {lp100k_to_mpg(8, False)} MPG (英制)")
    
    # 燃油成本
    print("\n【燃油成本计算】")
    cost = calculate_fuel_cost(500, 8, 8.5)
    print(f"500公里，8L/100km，油价8.5元/升 = ¥{cost}")
    
    # 碳排放
    print("\n【碳排放计算】")
    co2 = calculate_co2(100, 8)
    print(f"100公里，8L/100km = {co2} kg CO2")
    
    # 效率评级
    print("\n【效率评级】")
    rating = FuelEfficiencyCalculator.efficiency_rating(5)
    print(f"5 L/100km: {rating[0]} - {rating[1]} - {rating[2]}")
    
    rating = FuelEfficiencyCalculator.efficiency_rating(12)
    print(f"12 L/100km: {rating[0]} - {rating[1]} - {rating[2]}")
    
    # 车辆对比
    print("\n【车辆对比】")
    comparison = FuelEfficiencyCalculator.compare_vehicles(10000, 10, 6, 8.5)
    print(f"年行驶10000公里对比:")
    print(f"  车辆A (10L/100km): ¥{comparison['vehicle1_cost']}")
    print(f"  车辆B (6L/100km): ¥{comparison['vehicle2_cost']}")
    print(f"  节省: ¥{comparison['savings']}")
    
    # 回本分析
    print("\n【回本分析】")
    breakeven = FuelEfficiencyCalculator.calculate_break_even(200000, 5, 150000, 8, 8.5)
    print(f"省油车差价: ¥{breakeven['price_difference']}")
    print(f"每公里节省: ¥{breakeven['savings_per_km']}")
    print(f"回本里程: {breakeven['break_even_km']:,} 公里")
    print(f"回本时间: {breakeven['break_even_years']} 年")
    
    # 完整报告
    print("\n【完整效率报告】")
    report = FuelEfficiencyCalculator.full_efficiency_report(8)
    print(f"效率: {report['efficiency']['lp100k']} L/100km")
    print(f"     {report['efficiency']['mpg_us']} MPG (美制)")
    print(f"     {report['efficiency']['km_per_liter']} km/L")
    print(f"年成本: ¥{report['annual_costs']['annual_cost']}")
    print(f"月成本: ¥{report['annual_costs']['monthly_cost']}")
    print(f"年碳排放: {report['co2_emissions_kg']} kg CO2")
    print(f"效率评级: {report['efficiency_rating']['grade']} - {report['efficiency_rating']['description']}")