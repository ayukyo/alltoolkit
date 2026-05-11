"""
Ohm's Law Utilities - 欧姆定律计算工具

提供电压、电流、电阻、功率的计算功能。
支持串联/并联电阻计算，电功率公式，以及分压/分流计算。

核心公式:
- V = I × R (电压 = 电流 × 电阻)
- P = V × I = I²R = V²/R (功率)
- 串联: R_total = R1 + R2 + ...
- 并联: 1/R_total = 1/R1 + 1/R2 + ...
"""

from typing import Union, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class Prefix(Enum):
    """SI前缀枚举"""
    PICO = 1e-12   # p
    NANO = 1e-9    # n
    MICRO = 1e-6   # μ
    MILLI = 1e-3   # m
    CENTI = 1e-2   # c
    DECI = 1e-1    # d
    BASE = 1       # (无前缀)
    DECA = 1e1     # da
    HECTO = 1e2    # h
    KILO = 1e3     # k
    MEGA = 1e6     # M
    GIGA = 1e9     # G
    TERA = 1e12    # T


@dataclass
class OhmLawResult:
    """欧姆定律计算结果"""
    voltage: float      # 电压 (V)
    current: float      # 电流 (A)
    resistance: float   # 电阻 (Ω)
    power: float        # 功率 (W)
    
    def to_dict(self) -> dict:
        return {
            'voltage': self.voltage,
            'current': self.current,
            'resistance': self.resistance,
            'power': self.power
        }
    
    def __str__(self) -> str:
        return (
            f"电压: {self.format_value(self.voltage, 'V')}\n"
            f"电流: {self.format_value(self.current, 'A')}\n"
            f"电阻: {self.format_value(self.resistance, 'Ω')}\n"
            f"功率: {self.format_value(self.power, 'W')}"
        )
    
    @staticmethod
    def format_value(value: float, unit: str) -> str:
        """格式化数值，使用合适的SI前缀"""
        prefixes = [
            (1e12, 'T'), (1e9, 'G'), (1e6, 'M'), (1e3, 'k'),
            (1, ''), (1e-3, 'm'), (1e-6, 'μ'), (1e-9, 'n'), (1e-12, 'p')
        ]
        
        abs_val = abs(value)
        for threshold, prefix in prefixes:
            if abs_val >= threshold or threshold == 1e-12:
                scaled = value / threshold
                if scaled == int(scaled):
                    return f"{int(scaled)} {prefix}{unit}"
                return f"{scaled:.4g} {prefix}{unit}"
        
        return f"{value} {unit}"


class OhmLawCalculator:
    """欧姆定律计算器"""
    
    @staticmethod
    def from_voltage_current(voltage: float, current: float) -> OhmLawResult:
        """
        根据电压和电流计算电阻和功率
        
        Args:
            voltage: 电压 (V)
            current: 电流 (A)
        
        Returns:
            OhmLawResult: 包含所有计算结果
        """
        if current == 0:
            raise ValueError("电流不能为零")
        
        resistance = voltage / current
        power = voltage * current
        
        return OhmLawResult(
            voltage=voltage,
            current=current,
            resistance=resistance,
            power=power
        )
    
    @staticmethod
    def from_voltage_resistance(voltage: float, resistance: float) -> OhmLawResult:
        """
        根据电压和电阻计算电流和功率
        
        Args:
            voltage: 电压 (V)
            resistance: 电阻 (Ω)
        
        Returns:
            OhmLawResult: 包含所有计算结果
        """
        if resistance == 0:
            raise ValueError("电阻不能为零")
        
        current = voltage / resistance
        power = voltage * current
        
        return OhmLawResult(
            voltage=voltage,
            current=current,
            resistance=resistance,
            power=power
        )
    
    @staticmethod
    def from_current_resistance(current: float, resistance: float) -> OhmLawResult:
        """
        根据电流和电阻计算电压和功率
        
        Args:
            current: 电流 (A)
            resistance: 电阻 (Ω)
        
        Returns:
            OhmLawResult: 包含所有计算结果
        """
        voltage = current * resistance
        power = current * current * resistance
        
        return OhmLawResult(
            voltage=voltage,
            current=current,
            resistance=resistance,
            power=power
        )
    
    @staticmethod
    def from_voltage_power(voltage: float, power: float) -> OhmLawResult:
        """
        根据电压和功率计算电流和电阻
        
        Args:
            voltage: 电压 (V)
            power: 功率 (W)
        
        Returns:
            OhmLawResult: 包含所有计算结果
        """
        if voltage == 0:
            raise ValueError("电压不能为零")
        
        current = power / voltage
        resistance = voltage * voltage / power
        
        return OhmLawResult(
            voltage=voltage,
            current=current,
            resistance=resistance,
            power=power
        )
    
    @staticmethod
    def from_current_power(current: float, power: float) -> OhmLawResult:
        """
        根据电流和功率计算电压和电阻
        
        Args:
            current: 电流 (A)
            power: 功率 (W)
        
        Returns:
            OhmLawResult: 包含所有计算结果
        """
        if current == 0:
            raise ValueError("电流不能为零")
        
        voltage = power / current
        resistance = power / (current * current)
        
        return OhmLawResult(
            voltage=voltage,
            current=current,
            resistance=resistance,
            power=power
        )
    
    @staticmethod
    def from_resistance_power(resistance: float, power: float) -> OhmLawResult:
        """
        根据电阻和功率计算电压和电流
        
        Args:
            resistance: 电阻 (Ω)
            power: 功率 (W)
        
        Returns:
            OhmLawResult: 包含所有计算结果
        """
        if resistance <= 0:
            raise ValueError("电阻必须大于零")
        if power < 0:
            raise ValueError("功率不能为负")
        
        current = (power / resistance) ** 0.5
        voltage = current * resistance
        
        return OhmLawResult(
            voltage=voltage,
            current=current,
            resistance=resistance,
            power=power
        )


class ResistorCalculator:
    """电阻计算器 - 串联和并联"""
    
    @staticmethod
    def series(resistances: List[float]) -> float:
        """
        计算串联电阻总阻值
        
        R_total = R1 + R2 + R3 + ...
        
        Args:
            resistances: 电阻值列表 (Ω)
        
        Returns:
            float: 总电阻值 (Ω)
        """
        if not resistances:
            raise ValueError("电阻列表不能为空")
        if any(r < 0 for r in resistances):
            raise ValueError("电阻值不能为负")
        
        return sum(resistances)
    
    @staticmethod
    def parallel(resistances: List[float]) -> float:
        """
        计算并联电阻总阻值
        
        1/R_total = 1/R1 + 1/R2 + 1/R3 + ...
        
        Args:
            resistances: 电阻值列表 (Ω)
        
        Returns:
            float: 总电阻值 (Ω)
        """
        if not resistances:
            raise ValueError("电阻列表不能为空")
        if any(r <= 0 for r in resistances):
            raise ValueError("并联电阻值必须大于零")
        
        reciprocal_sum = sum(1.0 / r for r in resistances)
        return 1.0 / reciprocal_sum
    
    @staticmethod
    def mixed(config: List[Union[float, List]]) -> float:
        """
        计算混合连接电阻
        
        支持嵌套列表表示并联，数值表示串联
        
        Example:
            [10, [20, 30], 40] 表示: 10Ω 串联 (20Ω||30Ω) 串联 40Ω
        
        Args:
            config: 混合连接配置
        
        Returns:
            float: 总电阻值 (Ω)
        """
        total = 0.0
        
        for item in config:
            if isinstance(item, list):
                # 并联部分
                total += ResistorCalculator.parallel(item)
            else:
                # 串联部分
                total += item
        
        return total
    
    @staticmethod
    def find_combination(target: float, available: List[float], 
                         max_count: int = 3, 
                         mode: str = 'series') -> List[Tuple[float, ...]]:
        """
        查找最接近目标阻值的电阻组合
        
        Args:
            target: 目标阻值 (Ω)
            available: 可用电阻值列表 (Ω)
            max_count: 最多使用电阻数量
            mode: 'series' 串联, 'parallel' 并联
        
        Returns:
            List[Tuple]: 可能的组合列表，按误差从小到大排序
        """
        from itertools import combinations_with_replacement
        
        results = []
        
        for count in range(1, max_count + 1):
            for combo in combinations_with_replacement(available, count):
                if mode == 'series':
                    total = sum(combo)
                else:
                    total = ResistorCalculator.parallel(list(combo))
                
                error = abs(total - target)
                results.append((combo, total, error))
        
        # 按误差排序
        results.sort(key=lambda x: x[2])
        
        return [(r[0], r[1]) for r in results[:10]]  # 返回前10个最佳组合


class VoltageDivider:
    """分压器计算器"""
    
    @staticmethod
    def calculate(vin: float, r1: float, r2: float) -> float:
        """
        计算分压器输出电压
        
        Vout = Vin × R2 / (R1 + R2)
        
        Args:
            vin: 输入电压 (V)
            r1: 上分压电阻 (Ω)
            r2: 下分压电阻 (Ω)
        
        Returns:
            float: 输出电压 (V)
        """
        if r1 + r2 == 0:
            raise ValueError("电阻之和不能为零")
        
        return vin * r2 / (r1 + r2)
    
    @staticmethod
    def find_resistors(vin: float, vout: float, 
                       available: List[float]) -> List[Tuple[float, float, float]]:
        """
        查找最佳分压电阻组合
        
        Args:
            vin: 输入电压 (V)
            vout: 期望输出电压 (V)
            available: 可用电阻值列表 (Ω)
        
        Returns:
            List[Tuple[R1, R2, 实际Vout]]: 最佳组合列表
        """
        if vout >= vin:
            raise ValueError("输出电压必须小于输入电压")
        
        results = []
        
        for r1 in available:
            for r2 in available:
                actual_vout = VoltageDivider.calculate(vin, r1, r2)
                error = abs(actual_vout - vout)
                results.append((r1, r2, actual_vout, error))
        
        results.sort(key=lambda x: x[3])
        
        return [(r[0], r[1], r[2]) for r in results[:10]]


class CurrentDivider:
    """分流器计算器"""
    
    @staticmethod
    def calculate(itotal: float, r1: float, r2: float) -> Tuple[float, float]:
        """
        计算分流器各支路电流
        
        I1 = Itotal × R2 / (R1 + R2)
        I2 = Itotal × R1 / (R1 + R2)
        
        Args:
            itotal: 总电流 (A)
            r1: 支路1电阻 (Ω)
            r2: 支路2电阻 (Ω)
        
        Returns:
            Tuple[float, float]: (I1, I2) 各支路电流 (A)
        """
        if r1 + r2 == 0:
            raise ValueError("电阻之和不能为零")
        if r1 == 0 and r2 == 0:
            raise ValueError("电阻不能同时为零")
        
        i1 = itotal * r2 / (r1 + r2)
        i2 = itotal * r1 / (r1 + r2)
        
        return (i1, i2)


class PowerCalculator:
    """电功率计算器"""
    
    @staticmethod
    def ac_power(voltage: float, current: float, 
                 power_factor: float = 1.0) -> dict:
        """
        计算交流电功率
        
        Args:
            voltage: 电压有效值 (V)
            current: 电流有效值 (A)
            power_factor: 功率因数 (0-1)
        
        Returns:
            dict: {
                'apparent_power': 视在功率 (VA),
                'real_power': 有功功率 (W),
                'reactive_power': 无功功率 (VAR)
            }
        """
        if not 0 <= power_factor <= 1:
            raise ValueError("功率因数必须在0到1之间")
        
        apparent_power = voltage * current  # S = V × I
        real_power = apparent_power * power_factor  # P = S × cos(φ)
        
        # Q = S × sin(φ) = S × √(1 - cos²φ)
        reactive_power = apparent_power * (1 - power_factor ** 2) ** 0.5
        
        return {
            'apparent_power': apparent_power,      # 视在功率 (VA)
            'real_power': real_power,              # 有功功率 (W)
            'reactive_power': reactive_power       # 无功功率 (VAR)
        }
    
    @staticmethod
    def energy_cost(power_watts: float, hours: float, 
                    rate_per_kwh: float) -> dict:
        """
        计算电能消耗和费用
        
        Args:
            power_watts: 功率 (W)
            hours: 使用时间 (小时)
            rate_per_kwh: 电价 (元/kWh)
        
        Returns:
            dict: {
                'energy_kwh': 消耗电能 (kWh),
                'cost': 费用 (元)
            }
        """
        energy_kwh = power_watts * hours / 1000
        cost = energy_kwh * rate_per_kwh
        
        return {
            'energy_kwh': energy_kwh,
            'cost': cost
        }
    
    @staticmethod
    def battery_life(battery_capacity_mah: float, 
                     current_ma: float,
                     efficiency: float = 1.0) -> dict:
        """
        计算电池续航时间
        
        Args:
            battery_capacity_mah: 电池容量 (mAh)
            current_ma: 工作电流 (mA)
            efficiency: 效率 (0-1)
        
        Returns:
            dict: {
                'hours': 续航时间 (小时),
                'minutes': 续航时间 (分钟)
            }
        """
        if current_ma <= 0:
            raise ValueError("电流必须大于零")
        if not 0 < efficiency <= 1:
            raise ValueError("效率必须在0到1之间")
        
        hours = battery_capacity_mah * efficiency / current_ma
        
        return {
            'hours': hours,
            'minutes': hours * 60
        }


class ResistorColorCode:
    """电阻色环计算器"""
    
    # 色环颜色对应的数值
    COLORS = {
        'black': 0,
        'brown': 1,
        'red': 2,
        'orange': 3,
        'yellow': 4,
        'green': 5,
        'blue': 6,
        'violet': 7,
        'gray': 8,
        'white': 9
    }
    
    # 色环颜色对应的误差
    TOLERANCE = {
        'brown': 1,
        'red': 2,
        'green': 0.5,
        'blue': 0.25,
        'violet': 0.1,
        'gold': 5,
        'silver': 10
    }
    
    # 色环颜色对应的温度系数
    TEMP_COEFF = {
        'brown': 100,
        'red': 50,
        'orange': 15,
        'yellow': 25
    }
    
    @staticmethod
    def decode_4band(band1: str, band2: str, band3: str, band4: str) -> dict:
        """
        解码4色环电阻
        
        Args:
            band1: 第一环颜色 (有效数字)
            band2: 第二环颜色 (有效数字)
            band3: 第三环颜色 (倍率)
            band4: 第四环颜色 (误差)
        
        Returns:
            dict: {
                'resistance': 电阻值 (Ω),
                'tolerance': 误差百分比 (%),
                'range': (最小值, 最大值)
            }
        """
        d1 = ResistorColorCode.COLORS.get(band1.lower())
        d2 = ResistorColorCode.COLORS.get(band2.lower())
        multiplier = 10 ** ResistorColorCode.COLORS.get(band3.lower(), 0)
        tolerance = ResistorColorCode.TOLERANCE.get(band4.lower(), 20)
        
        if d1 is None or d2 is None:
            raise ValueError("无效的色环颜色")
        
        resistance = (d1 * 10 + d2) * multiplier
        min_val = resistance * (1 - tolerance / 100)
        max_val = resistance * (1 + tolerance / 100)
        
        return {
            'resistance': resistance,
            'tolerance': tolerance,
            'range': (min_val, max_val)
        }
    
    @staticmethod
    def decode_5band(band1: str, band2: str, band3: str, 
                    band4: str, band5: str) -> dict:
        """
        解码5色环电阻
        
        Args:
            band1-3: 前三环颜色 (有效数字)
            band4: 第四环颜色 (倍率)
            band5: 第五环颜色 (误差)
        
        Returns:
            dict: {
                'resistance': 电阻值 (Ω),
                'tolerance': 误差百分比 (%),
                'range': (最小值, 最大值)
            }
        """
        d1 = ResistorColorCode.COLORS.get(band1.lower())
        d2 = ResistorColorCode.COLORS.get(band2.lower())
        d3 = ResistorColorCode.COLORS.get(band3.lower())
        multiplier = 10 ** ResistorColorCode.COLORS.get(band4.lower(), 0)
        tolerance = ResistorColorCode.TOLERANCE.get(band5.lower(), 20)
        
        if d1 is None or d2 is None or d3 is None:
            raise ValueError("无效的色环颜色")
        
        resistance = (d1 * 100 + d2 * 10 + d3) * multiplier
        min_val = resistance * (1 - tolerance / 100)
        max_val = resistance * (1 + tolerance / 100)
        
        return {
            'resistance': resistance,
            'tolerance': tolerance,
            'range': (min_val, max_val)
        }
    
    @staticmethod
    def encode(resistance: float, tolerance: int = 5) -> List[str]:
        """
        将电阻值编码为色环颜色
        
        Args:
            resistance: 电阻值 (Ω)
            tolerance: 误差百分比 (%)
        
        Returns:
            List[str]: 色环颜色列表
        """
        if resistance <= 0:
            raise ValueError("电阻值必须大于零")
        
        # 找到合适的倍率
        multiplier = 0
        value = resistance
        while value >= 100:
            value /= 10
            multiplier += 1
        while value < 10:
            value *= 10
            multiplier -= 1
        
        # 四舍五入到两位有效数字
        value = round(value)
        
        # 解析数字
        d1 = int(value // 10)
        d2 = int(value % 10)
        
        # 反向查找颜色
        color_to_num = ResistorColorCode.COLORS
        num_to_color = {v: k for k, v in color_to_num.items()}
        
        # 查找误差颜色
        tol_to_color = {v: k for k, v in ResistorColorCode.TOLERANCE.items()}
        tol_color = tol_to_color.get(tolerance, 'gold')
        
        return [
            num_to_color[d1],
            num_to_color[d2],
            num_to_color[multiplier],
            tol_color
        ]


# 便捷函数
def calculate(voltage: float = None, current: float = None, 
              resistance: float = None, power: float = None) -> OhmLawResult:
    """
    欧姆定律便捷计算函数
    
    只需提供任意两个参数，自动计算其他两个。
    
    Args:
        voltage: 电压 (V)
        current: 电流 (A)
        resistance: 电阻 (Ω)
        power: 功率 (W)
    
    Returns:
        OhmLawResult: 包含所有计算结果
    
    Example:
        >>> result = calculate(voltage=12, resistance=4)
        >>> print(result.current)  # 3.0 A
        >>> print(result.power)    # 36.0 W
    """
    params = {'voltage': voltage, 'current': current, 
              'resistance': resistance, 'power': power}
    provided = {k: v for k, v in params.items() if v is not None}
    
    if len(provided) != 2:
        raise ValueError("必须恰好提供两个参数")
    
    if 'voltage' in provided and 'current' in provided:
        return OhmLawCalculator.from_voltage_current(voltage, current)
    elif 'voltage' in provided and 'resistance' in provided:
        return OhmLawCalculator.from_voltage_resistance(voltage, resistance)
    elif 'current' in provided and 'resistance' in provided:
        return OhmLawCalculator.from_current_resistance(current, resistance)
    elif 'voltage' in provided and 'power' in provided:
        return OhmLawCalculator.from_voltage_power(voltage, power)
    elif 'current' in provided and 'power' in provided:
        return OhmLawCalculator.from_current_power(current, power)
    elif 'resistance' in provided and 'power' in provided:
        return OhmLawCalculator.from_resistance_power(resistance, power)
    else:
        raise ValueError("参数组合无效")


def series_resistance(*resistances: float) -> float:
    """计算串联电阻总阻值"""
    return ResistorCalculator.series(list(resistances))


def parallel_resistance(*resistances: float) -> float:
    """计算并联电阻总阻值"""
    return ResistorCalculator.parallel(list(resistances))


if __name__ == "__main__":
    # 演示用法
    print("=== 欧姆定律计算 ===")
    result = calculate(voltage=12, resistance=4)
    print(result)
    print()
    
    print("=== 串联电阻 ===")
    print(f"100Ω + 200Ω + 300Ω = {series_resistance(100, 200, 300)}Ω")
    
    print("=== 并联电阻 ===")
    print(f"100Ω || 100Ω = {parallel_resistance(100, 100)}Ω")
    print(f"100Ω || 200Ω = {parallel_resistance(100, 200):.2f}Ω")
    print()
    
    print("=== 分压器计算 ===")
    vout = VoltageDivider.calculate(12, 10000, 2000)
    print(f"Vin=12V, R1=10kΩ, R2=2kΩ → Vout={vout:.2f}V")
    print()
    
    print("=== 电能计算 ===")
    energy = PowerCalculator.energy_cost(1000, 24, 0.5)
    print(f"1000W 电器使用24小时，电价0.5元/kWh")
    print(f"消耗: {energy['energy_kwh']} kWh，费用: {energy['cost']} 元")
    print()
    
    print("=== 电池续航 ===")
    battery = PowerCalculator.battery_life(3000, 500, 0.9)
    print(f"3000mAh电池，500mA电流，90%效率")
    print(f"续航: {battery['hours']:.1f} 小时 ({battery['minutes']:.0f} 分钟)")
    print()
    
    print("=== 电阻色环解码 ===")
    colors = ResistorColorCode.decode_4band('red', 'violet', 'yellow', 'gold')
    print(f"红-紫-黄-金 → {colors['resistance']/1000:.0f}kΩ ±{colors['tolerance']}%")