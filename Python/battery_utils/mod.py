"""
Battery Utils - 电池计算工具
==========================================

提供各种电池相关的计算功能，无需外部依赖。

功能列表:
- 充电时间估算
- 电池续航计算
- 电池健康度评估
- 电池循环次数计算
- 电池衰减模型
- 充电效率计算
- 电池寿命预测
- 功耗分析

作者: AllToolkit 自动化生成
日期: 2026-05-11
"""

from typing import Dict, Any, Tuple, List, Optional
from enum import Enum
from datetime import datetime, timedelta
import math


class BatteryType(Enum):
    """电池类型枚举"""
    LI_ION = "li_ion"              # 锂离子电池
    LI_PO = "li_po"                # 锂聚合物电池
    LI_FEPO4 = "li_fepo4"          # 磷酸铁锂电池
    NIMH = "nimh"                  # 镍氢电池
    NICD = "nicd"                  # 镍镉电池
    LEAD_ACID = "lead_acid"        # 铅酸电池
    ALKALINE = "alkaline"          # 碱性电池


class BatteryCalculator:
    """电池计算器"""
    
    # 电池特性常量
    BATTERY_PROPERTIES = {
        BatteryType.LI_ION: {
            'nominal_voltage': 3.7,           # 标称电压 (V)
            'energy_density': 250,            # 能量密度 (Wh/kg)
            'cycle_life': 500,                # 循环寿命 (次)
            'self_discharge_monthly': 2,      # 月自放电率 (%)
            'efficiency': 0.95,               # 充放电效率
            'optimal_temp_min': 15,            # 最佳温度范围
            'optimal_temp_max': 25,
            'name_cn': '锂离子电池',
            'name_en': 'Li-ion'
        },
        BatteryType.LI_PO: {
            'nominal_voltage': 3.7,
            'energy_density': 200,
            'cycle_life': 300,
            'self_discharge_monthly': 5,
            'efficiency': 0.90,
            'optimal_temp_min': 15,
            'optimal_temp_max': 25,
            'name_cn': '锂聚合物电池',
            'name_en': 'Li-Po'
        },
        BatteryType.LI_FEPO4: {
            'nominal_voltage': 3.2,
            'energy_density': 120,
            'cycle_life': 2000,
            'self_discharge_monthly': 3,
            'efficiency': 0.92,
            'optimal_temp_min': 0,
            'optimal_temp_max': 40,
            'name_cn': '磷酸铁锂电池',
            'name_en': 'LiFePO4'
        },
        BatteryType.NIMH: {
            'nominal_voltage': 1.2,
            'energy_density': 100,
            'cycle_life': 500,
            'self_discharge_monthly': 20,
            'efficiency': 0.70,
            'optimal_temp_min': 10,
            'optimal_temp_max': 30,
            'name_cn': '镍氢电池',
            'name_en': 'NiMH'
        },
        BatteryType.NICD: {
            'nominal_voltage': 1.2,
            'energy_density': 60,
            'cycle_life': 1000,
            'self_discharge_monthly': 15,
            'efficiency': 0.75,
            'optimal_temp_min': 10,
            'optimal_temp_max': 30,
            'name_cn': '镍镉电池',
            'name_en': 'NiCd'
        },
        BatteryType.LEAD_ACID: {
            'nominal_voltage': 2.0,
            'energy_density': 35,
            'cycle_life': 300,
            'self_discharge_monthly': 5,
            'efficiency': 0.80,
            'optimal_temp_min': 10,
            'optimal_temp_max': 25,
            'name_cn': '铅酸电池',
            'name_en': 'Lead Acid'
        },
        BatteryType.ALKALINE: {
            'nominal_voltage': 1.5,
            'energy_density': 150,
            'cycle_life': 0,                   # 不可充电
            'self_discharge_monthly': 0.5,
            'efficiency': 0.0,
            'optimal_temp_min': -20,
            'optimal_temp_max': 55,
            'name_cn': '碱性电池',
            'name_en': 'Alkaline'
        }
    }
    
    # 常见设备功耗参考 (W)
    DEVICE_POWER_CONSUMPTION = {
        'smartphone_idle': 0.5,
        'smartphone_active': 2,
        'smartphone_gaming': 5,
        'smartphone_video': 3,
        'laptop_idle': 10,
        'laptop_office': 30,
        'laptop_gaming': 80,
        'tablet_idle': 2,
        'tablet_active': 5,
        'smartwatch': 0.3,
        'bluetooth_headphones': 0.1,
        'wifi_router': 10,
        'led_bulb_10w': 10,
        'usb_fan': 2.5,
        'power_bank_5v': 5
    }
    
    @staticmethod
    def calculate_charge_time(
        capacity_mah: float,
        current_ma: float,
        efficiency: float = 0.85,
        current_charge_percent: float = 0
    ) -> Dict[str, Any]:
        """
        计算充电时间
        
        Args:
            capacity_mah: 电池容量 (mAh)
            current_ma: 充电电流 (mA)
            efficiency: 充电效率 (0-1)
            current_charge_percent: 当前电量百分比 (0-100)
            
        Returns:
            包含充电时间信息的字典
            
        Example:
            >>> result = BatteryCalculator.calculate_charge_time(3000, 1000)
            >>> result['hours'] > 0
            True
        """
        if capacity_mah <= 0 or current_ma <= 0:
            raise ValueError("电池容量和充电电流必须大于 0")
        
        if not 0 <= efficiency <= 1:
            raise ValueError("效率必须在 0-1 之间")
        
        if not 0 <= current_charge_percent <= 100:
            raise ValueError("当前电量百分比必须在 0-100 之间")
        
        # 计算需要充电的容量
        remaining_capacity = capacity_mah * (1 - current_charge_percent / 100)
        
        # 考虑充电效率的实际充电量
        effective_current = current_ma * efficiency
        
        # 计算充电时间 (小时)
        charge_time_hours = remaining_capacity / effective_current
        
        # 转换为时分秒
        hours = int(charge_time_hours)
        minutes = int((charge_time_hours - hours) * 60)
        seconds = int(((charge_time_hours - hours) * 60 - minutes) * 60)
        
        return {
            'total_hours': round(charge_time_hours, 2),
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds,
            'formatted': f"{hours}小时{minutes}分钟{seconds}秒",
            'remaining_capacity_mah': round(remaining_capacity, 2),
            'effective_current_ma': round(effective_current, 2)
        }
    
    @staticmethod
    def estimate_runtime(
        capacity_mah: float,
        voltage: float,
        power_consumption_w: float,
        efficiency: float = 0.85
    ) -> Dict[str, Any]:
        """
        估算电池续航时间
        
        Args:
            capacity_mah: 电池容量 (mAh)
            voltage: 电池电压 (V)
            power_consumption_w: 功耗 (W)
            efficiency: 放电效率 (0-1)
            
        Returns:
            包含续航时间信息的字典
            
        Example:
            >>> result = BatteryCalculator.estimate_runtime(3000, 3.7, 2)
            >>> result['hours'] > 0
            True
        """
        if power_consumption_w <= 0:
            raise ValueError("功耗必须大于 0")
        
        # 计算电池能量 (Wh)
        battery_energy_wh = capacity_mah / 1000 * voltage * efficiency
        
        # 计算续航时间 (小时)
        runtime_hours = battery_energy_wh / power_consumption_w
        
        hours = int(runtime_hours)
        minutes = int((runtime_hours - hours) * 60)
        
        return {
            'total_hours': round(runtime_hours, 2),
            'hours': hours,
            'minutes': minutes,
            'formatted': f"{hours}小时{minutes}分钟",
            'battery_energy_wh': round(battery_energy_wh, 2),
            'power_consumption_w': power_consumption_w
        }
    
    @staticmethod
    def calculate_battery_health(
        current_capacity_mah: float,
        original_capacity_mah: float,
        cycle_count: int,
        battery_type: BatteryType = BatteryType.LI_ION
    ) -> Dict[str, Any]:
        """
        计算电池健康度
        
        Args:
            current_capacity_mah: 当前电池容量 (mAh)
            original_capacity_mah: 原始电池容量 (mAh)
            cycle_count: 循环次数
            battery_type: 电池类型
            
        Returns:
            包含电池健康信息的字典
            
        Example:
            >>> result = BatteryCalculator.calculate_battery_health(2400, 3000, 200)
            >>> result['health_percent']
            80.0
        """
        if original_capacity_mah <= 0:
            raise ValueError("原始容量必须大于 0")
        
        # 计算容量健康度
        capacity_health = (current_capacity_mah / original_capacity_mah) * 100
        
        # 获取电池特性
        props = BatteryCalculator.BATTERY_PROPERTIES[battery_type]
        expected_cycle_life = props['cycle_life']
        
        # 计算循环健康度
        if expected_cycle_life > 0:
            cycle_health = max(0, 100 - (cycle_count / expected_cycle_life) * 100)
        else:
            cycle_health = 100  # 不可充电电池
        
        # 综合健康度 (容量占70%，循环占30%)
        overall_health = capacity_health * 0.7 + cycle_health * 0.3
        
        # 确定健康度等级
        if overall_health >= 90:
            grade = 'A'
            status = '优秀'
            suggestion = '电池状态良好，可正常使用'
        elif overall_health >= 80:
            grade = 'B'
            status = '良好'
            suggestion = '电池状态正常，注意保养'
        elif overall_health >= 70:
            grade = 'C'
            status = '一般'
            suggestion = '电池开始老化，建议减少深度放电'
        elif overall_health >= 60:
            grade = 'D'
            status = '较差'
            suggestion = '电池老化明显，建议更换'
        else:
            grade = 'E'
            status = '严重老化'
            suggestion = '电池严重老化，强烈建议更换'
        
        # 计算剩余寿命
        if expected_cycle_life > 0 and cycle_count < expected_cycle_life:
            remaining_cycles = expected_cycle_life - cycle_count
            remaining_life_percent = (remaining_cycles / expected_cycle_life) * 100
        else:
            remaining_cycles = 0
            remaining_life_percent = 0
        
        return {
            'capacity_health_percent': round(capacity_health, 1),
            'cycle_health_percent': round(cycle_health, 1),
            'overall_health_percent': round(overall_health, 1),
            'grade': grade,
            'status': status,
            'suggestion': suggestion,
            'cycle_count': cycle_count,
            'remaining_cycles': remaining_cycles,
            'remaining_life_percent': round(remaining_life_percent, 1),
            'battery_type': battery_type.value,
            'battery_name_cn': props['name_cn']
        }
    
    @staticmethod
    def calculate_cycle_count(
        total_charge_ah: float,
        battery_capacity_ah: float,
        depth_of_discharge: float = 0.8
    ) -> Dict[str, Any]:
        """
        计算等效循环次数
        
        Args:
            total_charge_ah: 累计充电量 (Ah)
            battery_capacity_ah: 电池容量 (Ah)
            depth_of_discharge: 平均放电深度 (0-1)
            
        Returns:
            包含循环次数信息的字典
            
        Example:
            >>> result = BatteryCalculator.calculate_cycle_count(100, 3)
            >>> result['full_cycles']
            33.333...
        """
        if battery_capacity_ah <= 0:
            raise ValueError("电池容量必须大于 0")
        
        if not 0 < depth_of_discharge <= 1:
            raise ValueError("放电深度必须在 0-1 之间")
        
        # 计算等效完整循环次数
        full_cycles = total_charge_ah / battery_capacity_ah
        
        # 考虑放电深度调整
        adjusted_cycles = full_cycles * depth_of_discharge
        
        return {
            'full_cycles': round(full_cycles, 2),
            'adjusted_cycles': round(adjusted_cycles, 2),
            'total_charge_ah': total_charge_ah,
            'battery_capacity_ah': battery_capacity_ah,
            'depth_of_discharge': depth_of_discharge
        }
    
    @staticmethod
    def model_degradation(
        years: float,
        battery_type: BatteryType = BatteryType.LI_ION,
        cycles_per_year: int = 365,
        temperature: float = 25
    ) -> Dict[str, Any]:
        """
        模拟电池衰减
        
        Args:
            years: 使用年限
            battery_type: 电池类型
            cycles_per_year: 每年循环次数
            temperature: 平均使用温度 (°C)
            
        Returns:
            包含衰减预测的字典
            
        Example:
            >>> result = BatteryCalculator.model_degradation(2)
            >>> result['remaining_capacity_percent'] < 100
            True
        """
        props = BatteryCalculator.BATTERY_PROPERTIES[battery_type]
        
        # 基础年衰减率
        base_annual_degradation = {
            BatteryType.LI_ION: 2.0,
            BatteryType.LI_PO: 3.0,
            BatteryType.LI_FEPO4: 1.0,
            BatteryType.NIMH: 4.0,
            BatteryType.NICD: 3.5,
            BatteryType.LEAD_ACID: 5.0,
            BatteryType.ALKALINE: 0
        }
        
        annual_rate = base_annual_degradation.get(battery_type, 2.0)
        
        # 温度修正 (每超过25°C增加10%衰减)
        if temperature > props['optimal_temp_max']:
            temp_factor = 1 + (temperature - props['optimal_temp_max']) * 0.05
        elif temperature < props['optimal_temp_min']:
            temp_factor = 1 + (props['optimal_temp_min'] - temperature) * 0.03
        else:
            temp_factor = 1.0
        
        adjusted_annual_rate = annual_rate * temp_factor
        
        # 循环衰减 (每500次循环约1-2%衰减，视电池类型)
        cycle_degradation_per_500 = {
            BatteryType.LI_ION: 2.0,
            BatteryType.LI_PO: 2.5,
            BatteryType.LI_FEPO4: 0.5,
            BatteryType.NIMH: 3.0,
            BatteryType.NICD: 1.5,
            BatteryType.LEAD_ACID: 4.0,
            BatteryType.ALKALINE: 0
        }
        
        cycle_rate = cycle_degradation_per_500.get(battery_type, 2.0)
        cycle_degradation = (cycles_per_year / 500) * cycle_rate
        
        # 总衰减
        total_degradation = (adjusted_annual_rate + cycle_degradation) * years
        
        # 剩余容量
        remaining_capacity = max(0, 100 - total_degradation)
        
        # 预测何时达到80%健康度
        degradation_per_year = adjusted_annual_rate + cycle_degradation
        if degradation_per_year > 0:
            years_to_80 = (100 - 80) / degradation_per_year
            years_to_70 = (100 - 70) / degradation_per_year
            years_to_60 = (100 - 60) / degradation_per_year
        else:
            years_to_80 = float('inf')
            years_to_70 = float('inf')
            years_to_60 = float('inf')
        
        return {
            'years': years,
            'remaining_capacity_percent': round(remaining_capacity, 1),
            'total_degradation_percent': round(total_degradation, 2),
            'annual_degradation_percent': round(adjusted_annual_rate + cycle_degradation, 2),
            'temp_factor': round(temp_factor, 2),
            'prediction': {
                'years_to_80_percent': round(years_to_80, 1) if years_to_80 != float('inf') else None,
                'years_to_70_percent': round(years_to_70, 1) if years_to_70 != float('inf') else None,
                'years_to_60_percent': round(years_to_60, 1) if years_to_60 != float('inf') else None
            },
            'battery_type': battery_type.value,
            'battery_name_cn': props['name_cn']
        }
    
    @staticmethod
    def calculate_charging_efficiency(
        input_energy_wh: float,
        battery_capacity_mah: float,
        voltage: float,
        final_charge_percent: float
    ) -> Dict[str, Any]:
        """
        计算充电效率
        
        Args:
            input_energy_wh: 输入能量 (Wh)
            battery_capacity_mah: 电池容量 (mAh)
            voltage: 电池电压 (V)
            final_charge_percent: 最终充电百分比 (0-100)
            
        Returns:
            包含充电效率信息的字典
            
        Example:
            >>> result = BatteryCalculator.calculate_charging_efficiency(15, 3000, 3.7, 100)
            >>> result['efficiency_percent'] > 0
            True
        """
        if input_energy_wh <= 0:
            raise ValueError("输入能量必须大于 0")
        
        # 计算电池实际获得的能量
        battery_energy_wh = battery_capacity_mah / 1000 * voltage * (final_charge_percent / 100)
        
        # 计算效率
        efficiency = (battery_energy_wh / input_energy_wh) * 100
        
        # 能量损失
        energy_loss = input_energy_wh - battery_energy_wh
        
        # 评估效率等级
        if efficiency >= 90:
            grade = 'A'
            status = '优秀'
        elif efficiency >= 80:
            grade = 'B'
            status = '良好'
        elif efficiency >= 70:
            grade = 'C'
            status = '一般'
        else:
            grade = 'D'
            status = '较差'
        
        return {
            'efficiency_percent': round(efficiency, 1),
            'grade': grade,
            'status': status,
            'input_energy_wh': input_energy_wh,
            'stored_energy_wh': round(battery_energy_wh, 2),
            'energy_loss_wh': round(energy_loss, 2),
            'energy_loss_percent': round(100 - efficiency, 1)
        }
    
    @staticmethod
    def analyze_power_consumption(
        capacity_mah: float,
        voltage: float,
        usage_pattern: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        分析功耗和续航
        
        Args:
            capacity_mah: 电池容量 (mAh)
            voltage: 电池电压 (V)
            usage_pattern: 使用模式字典，键为场景名，值为每天的小时数
                          例如: {'active': 4, 'idle': 20}
            
        Returns:
            包含功耗分析结果的字典
            
        Example:
            >>> pattern = {'active': 4, 'idle': 20}
            >>> result = BatteryCalculator.analyze_power_consumption(3000, 3.7, pattern)
            >>> 'total_runtime_hours' in result
            True
        """
        # 电池总能量 (Wh)
        total_energy_wh = capacity_mah / 1000 * voltage
        
        # 获取场景功耗
        device_power = BatteryCalculator.DEVICE_POWER_CONSUMPTION
        
        total_daily_consumption = 0
        scenario_analysis = {}
        
        for scenario, hours in usage_pattern.items():
            # 查找对应功耗，默认使用手机活跃功耗
            power_w = device_power.get(f'smartphone_{scenario}', 
                                       device_power.get(scenario, 2))
            
            consumption = power_w * hours
            total_daily_consumption += consumption
            
            scenario_analysis[scenario] = {
                'hours_per_day': hours,
                'power_w': power_w,
                'consumption_wh': round(consumption, 2)
            }
        
        # 计算续航天数
        if total_daily_consumption > 0:
            runtime_days = total_energy_wh / total_daily_consumption
            runtime_hours = runtime_days * 24
        else:
            runtime_days = float('inf')
            runtime_hours = float('inf')
        
        return {
            'battery_energy_wh': round(total_energy_wh, 2),
            'total_daily_consumption_wh': round(total_daily_consumption, 2),
            'runtime_days': round(runtime_days, 1) if runtime_days != float('inf') else None,
            'runtime_hours': round(runtime_hours, 1) if runtime_hours != float('inf') else None,
            'scenario_analysis': scenario_analysis,
            'average_hourly_consumption_w': round(total_daily_consumption / 24, 2)
        }
    
    @staticmethod
    def recommend_charger(
        capacity_mah: float,
        battery_type: BatteryType = BatteryType.LI_ION,
        fast_charge: bool = False
    ) -> Dict[str, Any]:
        """
        推荐充电器规格
        
        Args:
            capacity_mah: 电池容量 (mAh)
            battery_type: 电池类型
            fast_charge: 是否需要快充
            
        Returns:
            包含充电器推荐信息的字典
            
        Example:
            >>> result = BatteryCalculator.recommend_charger(3000)
            >>> result['recommended_current_ma'] > 0
            True
        """
        # 推荐充电倍率 (C-rate)
        if fast_charge:
            if battery_type == BatteryType.LI_ION:
                max_c_rate = 1.0  # 锂离子快充最大1C
            elif battery_type == BatteryType.LI_PO:
                max_c_rate = 2.0  # 锂聚合物可更高
            elif battery_type == BatteryType.LI_FEPO4:
                max_c_rate = 1.0
            else:
                max_c_rate = 0.5
        else:
            max_c_rate = 0.5  # 标充建议0.5C
        
        recommended_current_ma = capacity_mah * max_c_rate
        
        # 计算充电时间
        charge_time = BatteryCalculator.calculate_charge_time(
            capacity_mah, recommended_current_ma, 0.85, 0
        )
        
        # 推荐充电器功率
        voltage = BatteryCalculator.BATTERY_PROPERTIES[battery_type]['nominal_voltage']
        charger_power_w = recommended_current_ma / 1000 * voltage
        
        return {
            'battery_capacity_mah': capacity_mah,
            'recommended_current_ma': round(recommended_current_ma, 0),
            'recommended_power_w': round(charger_power_w, 1),
            'charge_rate_c': max_c_rate,
            'estimated_charge_time': charge_time['formatted'],
            'fast_charge': fast_charge,
            'battery_type': battery_type.value,
            'tips': [
                '使用原装充电器效果最佳',
                '避免在高温环境下充电',
                '不要让电池完全放电后再充电',
                '长期存放时保持50%电量'
            ]
        }
    
    @staticmethod
    def calculate_parallel_series(
        cells: int,
        cell_capacity_mah: float,
        cell_voltage: float,
        config: str = 'parallel'
    ) -> Dict[str, Any]:
        """
        计算电池组配置
        
        Args:
            cells: 电池数量
            cell_capacity_mah: 单体电池容量 (mAh)
            cell_voltage: 单体电池电压 (V)
            config: 配置方式 ('parallel' 并联, 'series' 串联, 'both' 混联)
            
        Returns:
            包含电池组规格的字典
            
        Example:
            >>> result = BatteryCalculator.calculate_parallel_series(2, 3000, 3.7, 'parallel')
            >>> result['total_capacity_mah']
            6000
        """
        if cells <= 0:
            raise ValueError("电池数量必须大于 0")
        
        if config == 'parallel':
            # 并联：容量相加，电压不变
            total_capacity = cell_capacity_mah * cells
            total_voltage = cell_voltage
            config_desc = '并联'
        elif config == 'series':
            # 串联：电压相加，容量不变
            total_capacity = cell_capacity_mah
            total_voltage = cell_voltage * cells
            config_desc = '串联'
        else:
            # 混联：假设一半串联一半并联
            series = cells // 2 if cells >= 2 else 1
            parallel = cells // 2 if cells >= 2 else 1
            total_capacity = cell_capacity_mah * parallel
            total_voltage = cell_voltage * series
            config_desc = '混联'
        
        # 计算总能量
        total_energy_wh = total_capacity / 1000 * total_voltage
        
        return {
            'cells': cells,
            'config': config,
            'config_description': config_desc,
            'cell_capacity_mah': cell_capacity_mah,
            'cell_voltage': cell_voltage,
            'total_capacity_mah': round(total_capacity, 0),
            'total_voltage': round(total_voltage, 2),
            'total_energy_wh': round(total_energy_wh, 2)
        }
    
    @staticmethod
    def battery_comparison(
        batteries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        比较多块电池
        
        Args:
            batteries: 电池列表，每个包含 capacity_mah, voltage, battery_type
            
        Returns:
            包含比较结果的字典
            
        Example:
            >>> batteries = [
            ...     {'name': 'A', 'capacity_mah': 3000, 'voltage': 3.7},
            ...     {'name': 'B', 'capacity_mah': 4000, 'voltage': 3.7}
            ... ]
            >>> result = BatteryCalculator.battery_comparison(batteries)
            >>> len(result['rankings']) == 2
            True
        """
        results = []
        
        for i, bat in enumerate(batteries):
            capacity = bat.get('capacity_mah', 0)
            voltage = bat.get('voltage', 3.7)
            name = bat.get('name', f'Battery {i+1}')
            
            energy_wh = capacity / 1000 * voltage
            
            results.append({
                'name': name,
                'capacity_mah': capacity,
                'voltage': voltage,
                'energy_wh': round(energy_wh, 2)
            })
        
        # 按能量排序
        rankings = sorted(results, key=lambda x: x['energy_wh'], reverse=True)
        
        # 计算相对容量
        max_energy = rankings[0]['energy_wh'] if rankings else 1
        for bat in rankings:
            bat['relative_capacity_percent'] = round(bat['energy_wh'] / max_energy * 100, 1) if max_energy > 0 else 0
        
        return {
            'rankings': rankings,
            'best': rankings[0] if rankings else None,
            'total_energy_wh': round(sum(b['energy_wh'] for b in results), 2),
            'average_energy_wh': round(sum(b['energy_wh'] for b in results) / len(results), 2) if results else 0
        }
    
    @staticmethod
    def full_battery_report(
        capacity_mah: float,
        voltage: float,
        battery_type: BatteryType = BatteryType.LI_ION,
        cycle_count: int = 0,
        current_capacity_mah: Optional[float] = None,
        average_power_w: float = 2.0
    ) -> Dict[str, Any]:
        """
        生成完整电池报告
        
        Args:
            capacity_mah: 电池容量 (mAh)
            voltage: 电池电压 (V)
            battery_type: 电池类型
            cycle_count: 循环次数
            current_capacity_mah: 当前实际容量 (mAh)，可选
            average_power_w: 平均功耗 (W)
            
        Returns:
            包含完整电池报告的字典
            
        Example:
            >>> report = BatteryCalculator.full_battery_report(3000, 3.7)
            >>> 'specs' in report
            True
        """
        props = BatteryCalculator.BATTERY_PROPERTIES[battery_type]
        
        # 基本规格
        energy_wh = capacity_mah / 1000 * voltage
        
        # 充电时间
        charger_recommend = BatteryCalculator.recommend_charger(capacity_mah, battery_type)
        fast_charger_recommend = BatteryCalculator.recommend_charger(capacity_mah, battery_type, True)
        
        # 续航估算
        runtime = BatteryCalculator.estimate_runtime(capacity_mah, voltage, average_power_w)
        
        # 健康度 (如果有当前容量)
        health = None
        if current_capacity_mah is not None:
            health = BatteryCalculator.calculate_battery_health(
                current_capacity_mah, capacity_mah, cycle_count, battery_type
            )
        
        # 衰减预测
        degradation_1yr = BatteryCalculator.model_degradation(1, battery_type)
        degradation_3yr = BatteryCalculator.model_degradation(3, battery_type)
        
        return {
            'specs': {
                'capacity_mah': capacity_mah,
                'voltage': voltage,
                'energy_wh': round(energy_wh, 2),
                'battery_type': battery_type.value,
                'battery_name_cn': props['name_cn'],
                'battery_name_en': props['name_en'],
                'nominal_voltage': props['nominal_voltage'],
                'expected_cycle_life': props['cycle_life'],
                'efficiency': props['efficiency']
            },
            'charging': {
                'standard': {
                    'recommended_current_ma': charger_recommend['recommended_current_ma'],
                    'estimated_time': charger_recommend['estimated_charge_time']
                },
                'fast_charge': {
                    'recommended_current_ma': fast_charger_recommend['recommended_current_ma'],
                    'estimated_time': fast_charger_recommend['estimated_charge_time']
                }
            },
            'runtime': runtime,
            'health': health,
            'degradation_forecast': {
                '1_year': degradation_1yr,
                '3_years': degradation_3yr
            },
            'tips': [
                f'建议充电电流: {int(charger_recommend["recommended_current_ma"])}mA',
                '避免完全放电，保持电量在20%-80%之间',
                f'最佳工作温度: {props["optimal_temp_min"]}-{props["optimal_temp_max"]}°C',
                f'预期循环寿命: {props["cycle_life"]}次'
            ]
        }


# 便捷函数
def calculate_charge_time(capacity_mah: float, current_ma: float) -> Dict[str, Any]:
    """计算充电时间"""
    return BatteryCalculator.calculate_charge_time(capacity_mah, current_ma)


def estimate_runtime(capacity_mah: float, voltage: float, power_w: float) -> float:
    """估算续航时间 (小时)"""
    result = BatteryCalculator.estimate_runtime(capacity_mah, voltage, power_w)
    return result['total_hours']


def calculate_battery_health(current: float, original: float, cycles: int = 0) -> float:
    """计算电池健康度百分比"""
    result = BatteryCalculator.calculate_battery_health(current, original, cycles)
    return result['overall_health_percent']


if __name__ == '__main__':
    print("=" * 60)
    print("Battery Utils - 电池计算工具演示")
    print("=" * 60)
    
    # 充电时间计算
    print("\n【充电时间计算】")
    result = calculate_charge_time(3000, 1000)
    print(f"3000mAh电池，1000mA充电电流")
    print(f"充电时间: {result['formatted']}")
    
    # 续航估算
    print("\n【续航估算】")
    runtime = estimate_runtime(3000, 3.7, 2)
    print(f"3000mAh, 3.7V电池，功耗2W")
    print(f"续航时间: {runtime}小时")
    
    # 电池健康度
    print("\n【电池健康度】")
    health = BatteryCalculator.calculate_battery_health(2400, 3000, 200)
    print(f"原容量3000mAh，现容量2400mAh，循环200次")
    print(f"健康度: {health['overall_health_percent']}%")
    print(f"等级: {health['grade']} - {health['status']}")
    print(f"建议: {health['suggestion']}")
    
    # 衰减预测
    print("\n【衰减预测】")
    deg = BatteryCalculator.model_degradation(2, BatteryType.LI_ION, 365, 25)
    print(f"使用2年后，锂离子电池剩余容量: {deg['remaining_capacity_percent']}%")
    print(f"年衰减率: {deg['annual_degradation_percent']}%")
    
    # 功耗分析
    print("\n【功耗分析】")
    pattern = {'active': 4, 'idle': 20}
    analysis = BatteryCalculator.analyze_power_consumption(3000, 3.7, pattern)
    print(f"使用模式: 活跃4小时, 待机20小时")
    print(f"日功耗: {analysis['total_daily_consumption_wh']}Wh")
    print(f"续航: {analysis['runtime_days']}天 ({analysis['runtime_hours']}小时)")
    
    # 充电器推荐
    print("\n【充电器推荐】")
    charger = BatteryCalculator.recommend_charger(3000, BatteryType.LI_ION, True)
    print(f"推荐电流: {charger['recommended_current_ma']}mA")
    print(f"预计充电时间: {charger['estimated_charge_time']}")
    
    # 完整报告
    print("\n【完整电池报告】")
    report = BatteryCalculator.full_battery_report(3000, 3.7, BatteryType.LI_ION, 100, 2800)
    print(f"容量: {report['specs']['capacity_mah']}mAh")
    print(f"能量: {report['specs']['energy_wh']}Wh")
    print(f"类型: {report['specs']['battery_name_cn']}")
    if report['health']:
        print(f"健康度: {report['health']['overall_health_percent']}%")
    print(f"标准充电时间: {report['charging']['standard']['estimated_time']}")
    print(f"快充时间: {report['charging']['fast_charge']['estimated_time']}")