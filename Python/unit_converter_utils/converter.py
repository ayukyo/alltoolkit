"""
Unit Converter - 核心转换逻辑
"""

from typing import Union, Dict, Any
from decimal import Decimal, ROUND_HALF_UP


class UnitConverter:
    """单位转换器主类"""
    
    # 长度转换基准: 米 (m)
    LENGTH_UNITS = {
        'm': 1,
        'km': 1000,
        'cm': 0.01,
        'mm': 0.001,
        'um': 1e-6,  # 微米
        'nm': 1e-9,  # 纳米
        'mi': 1609.344,  # 英里
        'yd': 0.9144,    # 码
        'ft': 0.3048,    # 英尺
        'in': 0.0254,    # 英寸
        'nmi': 1852,     # 海里
        'ly': 9.461e15,  # 光年
        'au': 1.496e11,  # 天文单位
        'pc': 3.086e16,  # 秒差距
    }
    
    # 重量转换基准: 千克 (kg)
    WEIGHT_UNITS = {
        'kg': 1,
        'g': 0.001,
        'mg': 1e-6,
        'ug': 1e-9,      # 微克
        't': 1000,        # 公吨
        'lb': 0.45359237, # 磅
        'oz': 0.028349523125,  # 盎司
        'st': 6.35029318, # 英石
        'ct': 0.0002,     # 克拉
        'jin': 0.5,       # 市斤
        'liang': 0.05,    # 两
    }
    
    # 温度转换 (特殊处理)
    TEMPERATURE_UNITS = ['C', 'F', 'K']
    
    # 体积转换基准: 升 (L)
    VOLUME_UNITS = {
        'L': 1,
        'mL': 0.001,
        'm3': 1000,       # 立方米
        'cm3': 0.001,     # 立方厘米
        'mm3': 1e-6,      # 立方毫米
        'gal': 3.785411784,  # 美制加仑
        'gal_uk': 4.54609,    # 英制加仑
        'qt': 0.946352946,    # 夸脱
        'pt': 0.473176473,    # 品脱
        'cup': 0.2365882365,  # 杯
        'fl_oz': 0.029573529563,  # 液体盎司
        'tbsp': 0.014786764781,   # 汤勺
        'tsp': 0.0049289215938,   # 茶勺
        'bbl': 158.987,    # 桶 (石油)
    }
    
    # 面积转换基准: 平方米 (m2)
    AREA_UNITS = {
        'm2': 1,
        'km2': 1e6,
        'cm2': 1e-4,
        'mm2': 1e-6,
        'ha': 10000,       # 公顷
        'acre': 4046.8564224,
        'ft2': 0.09290304,
        'in2': 0.00064516,
        'yd2': 0.83612736,
        'mu': 666.6666667,  # 亩
        'qing': 6666.666667, # 顷
    }
    
    # 时间转换基准: 秒 (s)
    TIME_UNITS = {
        's': 1,
        'ms': 1e-3,
        'us': 1e-6,
        'ns': 1e-9,
        'ps': 1e-12,
        'min': 60,
        'h': 3600,
        'd': 86400,
        'w': 604800,
        'mo': 2629746,      # 平均月 (30.44天)
        'y': 31556952,      # 平均年 (365.24天)
        'decade': 315569520,
        'century': 3155695200,
    }
    
    # 速度转换基准: 米每秒 (m/s)
    SPEED_UNITS = {
        'm/s': 1,
        'km/s': 1000,
        'km/h': 1/3.6,
        'm/min': 1/60,
        'mph': 0.44704,      # 英里每小时
        'knot': 0.514444,    # 节
        'mach': 340.29,      # 马赫 (海平面, 15°C)
        'c': 299792458,      # 光速
    }
    
    # 数据转换基准: 字节 (B)
    DATA_UNITS = {
        'B': 1,
        'KB': 1000,
        'MB': 1e6,
        'GB': 1e9,
        'TB': 1e12,
        'PB': 1e15,
        'EB': 1e18,
        'KiB': 1024,
        'MiB': 1024**2,
        'GiB': 1024**3,
        'TiB': 1024**4,
        'PiB': 1024**5,
        'bit': 0.125,
        'Kbit': 125,
        'Mbit': 125000,
        'Gbit': 1.25e8,
    }
    
    # 压力转换基准: 帕斯卡 (Pa)
    PRESSURE_UNITS = {
        'Pa': 1,
        'kPa': 1000,
        'MPa': 1e6,
        'GPa': 1e9,
        'bar': 1e5,
        'mbar': 100,
        'psi': 6894.757293168,
        'atm': 101325,
        'mmHg': 133.322387415,
        'inHg': 3386.389,
        'Torr': 133.3223684211,
        'kgf/cm2': 98066.5,
    }
    
    # 角度转换基准: 度 (deg)
    ANGLE_UNITS = {
        'deg': 1,
        'rad': 57.295779513082,  # 180/π
        'grad': 0.9,              # 百分度
        'arcmin': 1/60,           # 角分
        'arcsec': 1/3600,         # 角秒
        'turn': 360,              # 圈
        'mrad': 0.057295779513,   # 毫弧度
    }
    
    # 功率转换基准: 瓦特 (W)
    POWER_UNITS = {
        'W': 1,
        'kW': 1000,
        'MW': 1e6,
        'GW': 1e9,
        'mW': 0.001,
        'hp': 745.699872,        # 马力 (公制)
        'hp_electric': 746,       # 电马力
        'BTU/h': 0.29307107,      # BTU每小时
        'kcal/h': 1.163,          # 千卡每小时
        'ft_lbf/s': 1.3558179,    # 英尺磅力每秒
    }
    
    def __init__(self, precision: int = 6):
        """
        初始化转换器
        
        Args:
            precision: 结果精度 (小数位数)
        """
        self.precision = precision
    
    def _convert_via_base(self, value: float, from_unit: str, to_unit: str, 
                          unit_dict: Dict[str, float]) -> float:
        """通过基准单位进行转换"""
        if from_unit not in unit_dict:
            raise ValueError(f"未知单位: {from_unit}")
        if to_unit not in unit_dict:
            raise ValueError(f"未知单位: {to_unit}")
        
        # 转换为基准单位，再转换为目标单位
        base_value = value * unit_dict[from_unit]
        result = base_value / unit_dict[to_unit]
        
        return self._round(result)
    
    def _convert_temperature(self, value: float, from_unit: str, to_unit: str) -> float:
        """温度转换 (特殊处理)"""
        from_unit = from_unit.upper()
        to_unit = to_unit.upper()
        
        if from_unit not in self.TEMPERATURE_UNITS:
            raise ValueError(f"未知温度单位: {from_unit}")
        if to_unit not in self.TEMPERATURE_UNITS:
            raise ValueError(f"未知温度单位: {to_unit}")
        
        # 先转换为开尔文
        if from_unit == 'C':
            kelvin = value + 273.15
        elif from_unit == 'F':
            kelvin = (value + 459.67) * 5/9
        else:  # K
            kelvin = value
        
        # 从开尔文转换为目标单位
        if to_unit == 'C':
            result = kelvin - 273.15
        elif to_unit == 'F':
            result = kelvin * 9/5 - 459.67
        else:  # K
            result = kelvin
        
        return self._round(result)
    
    def _round(self, value: float) -> float:
        """四舍五入到指定精度"""
        if self.precision <= 0:
            return round(value)
        return float(Decimal(str(value)).quantize(
            Decimal(10) ** -self.precision, rounding=ROUND_HALF_UP
        ))
    
    def convert(self, value: Union[int, float], from_unit: str, to_unit: str,
                category: str = 'auto') -> float:
        """
        通用单位转换
        
        Args:
            value: 要转换的值
            from_unit: 源单位
            to_unit: 目标单位
            category: 转换类型 ('length', 'weight', 'temperature', 'volume', 
                               'area', 'time', 'speed', 'data', 'pressure', 
                               'angle', 'power', 'auto')
        
        Returns:
            转换后的值
        """
        # 自动检测类型
        if category == 'auto':
            category = self._detect_category(from_unit, to_unit)
        
        converters = {
            'length': (self.LENGTH_UNITS, '_convert_via_base'),
            'weight': (self.WEIGHT_UNITS, '_convert_via_base'),
            'temperature': (None, '_convert_temperature'),
            'volume': (self.VOLUME_UNITS, '_convert_via_base'),
            'area': (self.AREA_UNITS, '_convert_via_base'),
            'time': (self.TIME_UNITS, '_convert_via_base'),
            'speed': (self.SPEED_UNITS, '_convert_via_base'),
            'data': (self.DATA_UNITS, '_convert_via_base'),
            'pressure': (self.PRESSURE_UNITS, '_convert_via_base'),
            'angle': (self.ANGLE_UNITS, '_convert_via_base'),
            'power': (self.POWER_UNITS, '_convert_via_base'),
        }
        
        if category not in converters:
            raise ValueError(f"未知的转换类型: {category}")
        
        unit_dict, method_name = converters[category]
        method = getattr(self, method_name)
        
        if method_name == '_convert_temperature':
            return method(float(value), from_unit, to_unit)
        else:
            return method(float(value), from_unit, to_unit, unit_dict)
    
    def _detect_category(self, from_unit: str, to_unit: str) -> str:
        """自动检测转换类型"""
        unit_categories = {
            'length': self.LENGTH_UNITS,
            'weight': self.WEIGHT_UNITS,
            'temperature': {u: 1 for u in self.TEMPERATURE_UNITS},
            'volume': self.VOLUME_UNITS,
            'area': self.AREA_UNITS,
            'time': self.TIME_UNITS,
            'speed': self.SPEED_UNITS,
            'data': self.DATA_UNITS,
            'pressure': self.PRESSURE_UNITS,
            'angle': self.ANGLE_UNITS,
            'power': self.POWER_UNITS,
        }
        
        from_unit_lower = from_unit.lower()
        to_unit_lower = to_unit.lower()
        
        for category, units in unit_categories.items():
            units_lower = {k.lower(): v for k, v in units.items()}
            if from_unit_lower in units_lower and to_unit_lower in units_lower:
                return category
        
        raise ValueError(f"无法确定单位 '{from_unit}' 和 '{to_unit}' 的转换类型")
    
    def get_supported_units(self, category: str = None) -> Dict[str, list]:
        """获取支持的单位列表"""
        all_units = {
            'length': list(self.LENGTH_UNITS.keys()),
            'weight': list(self.WEIGHT_UNITS.keys()),
            'temperature': self.TEMPERATURE_UNITS,
            'volume': list(self.VOLUME_UNITS.keys()),
            'area': list(self.AREA_UNITS.keys()),
            'time': list(self.TIME_UNITS.keys()),
            'speed': list(self.SPEED_UNITS.keys()),
            'data': list(self.DATA_UNITS.keys()),
            'pressure': list(self.PRESSURE_UNITS.keys()),
            'angle': list(self.ANGLE_UNITS.keys()),
            'power': list(self.POWER_UNITS.keys()),
        }
        
        if category:
            return {category: all_units.get(category, [])}
        return all_units
    
    def convert_length(self, value: float, from_unit: str, to_unit: str) -> float:
        """长度转换"""
        return self.convert(value, from_unit, to_unit, 'length')
    
    def convert_weight(self, value: float, from_unit: str, to_unit: str) -> float:
        """重量转换"""
        return self.convert(value, from_unit, to_unit, 'weight')
    
    def convert_temperature(self, value: float, from_unit: str, to_unit: str) -> float:
        """温度转换"""
        return self.convert(value, from_unit, to_unit, 'temperature')
    
    def convert_volume(self, value: float, from_unit: str, to_unit: str) -> float:
        """体积转换"""
        return self.convert(value, from_unit, to_unit, 'volume')
    
    def convert_area(self, value: float, from_unit: str, to_unit: str) -> float:
        """面积转换"""
        return self.convert(value, from_unit, to_unit, 'area')
    
    def convert_time(self, value: float, from_unit: str, to_unit: str) -> float:
        """时间转换"""
        return self.convert(value, from_unit, to_unit, 'time')
    
    def convert_speed(self, value: float, from_unit: str, to_unit: str) -> float:
        """速度转换"""
        return self.convert(value, from_unit, to_unit, 'speed')
    
    def convert_data(self, value: float, from_unit: str, to_unit: str) -> float:
        """数据转换"""
        return self.convert(value, from_unit, to_unit, 'data')
    
    def convert_pressure(self, value: float, from_unit: str, to_unit: str) -> float:
        """压力转换"""
        return self.convert(value, from_unit, to_unit, 'pressure')
    
    def convert_angle(self, value: float, from_unit: str, to_unit: str) -> float:
        """角度转换"""
        return self.convert(value, from_unit, to_unit, 'angle')
    
    def convert_power(self, value: float, from_unit: str, to_unit: str) -> float:
        """功率转换"""
        return self.convert(value, from_unit, to_unit, 'power')
    
    def batch_convert(self, conversions: list) -> list:
        """
        批量转换
        
        Args:
            conversions: 转换列表，每项为 (value, from_unit, to_unit, category?)
        
        Returns:
            转换结果列表
        """
        results = []
        for conv in conversions:
            if len(conv) == 3:
                value, from_unit, to_unit = conv
                category = 'auto'
            else:
                value, from_unit, to_unit, category = conv
            results.append(self.convert(value, from_unit, to_unit, category))
        return results
    
    def convert_all(self, value: float, from_unit: str, category: str) -> Dict[str, float]:
        """
        将一个值转换为同一类型的所有其他单位
        
        Args:
            value: 要转换的值
            from_unit: 源单位
            category: 转换类型
        
        Returns:
            所有目标单位及对应值的字典
        """
        if category == 'temperature':
            units = self.TEMPERATURE_UNITS
        else:
            unit_dicts = {
                'length': self.LENGTH_UNITS,
                'weight': self.WEIGHT_UNITS,
                'volume': self.VOLUME_UNITS,
                'area': self.AREA_UNITS,
                'time': self.TIME_UNITS,
                'speed': self.SPEED_UNITS,
                'data': self.DATA_UNITS,
                'pressure': self.PRESSURE_UNITS,
                'angle': self.ANGLE_UNITS,
                'power': self.POWER_UNITS,
            }
            units = list(unit_dicts.get(category, {}).keys())
        
        results = {}
        for to_unit in units:
            if to_unit.lower() != from_unit.lower():
                try:
                    results[to_unit] = self.convert(value, from_unit, to_unit, category)
                except:
                    pass
        return results


# 便捷函数
_converter = UnitConverter()

def convert(value: Union[int, float], from_unit: str, to_unit: str, 
            category: str = 'auto') -> float:
    """便捷转换函数"""
    return _converter.convert(value, from_unit, to_unit, category)

def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    """便捷长度转换"""
    return _converter.convert_length(value, from_unit, to_unit)

def convert_weight(value: float, from_unit: str, to_unit: str) -> float:
    """便捷重量转换"""
    return _converter.convert_weight(value, from_unit, to_unit)

def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """便捷温度转换"""
    return _converter.convert_temperature(value, from_unit, to_unit)

def convert_volume(value: float, from_unit: str, to_unit: str) -> float:
    """便捷体积转换"""
    return _converter.convert_volume(value, from_unit, to_unit)

def convert_area(value: float, from_unit: str, to_unit: str) -> float:
    """便捷面积转换"""
    return _converter.convert_area(value, from_unit, to_unit)

def convert_time(value: float, from_unit: str, to_unit: str) -> float:
    """便捷时间转换"""
    return _converter.convert_time(value, from_unit, to_unit)

def convert_speed(value: float, from_unit: str, to_unit: str) -> float:
    """便捷速度转换"""
    return _converter.convert_speed(value, from_unit, to_unit)

def convert_data(value: float, from_unit: str, to_unit: str) -> float:
    """便捷数据转换"""
    return _converter.convert_data(value, from_unit, to_unit)

def convert_pressure(value: float, from_unit: str, to_unit: str) -> float:
    """便捷压力转换"""
    return _converter.convert_pressure(value, from_unit, to_unit)

def convert_angle(value: float, from_unit: str, to_unit: str) -> float:
    """便捷角度转换"""
    return _converter.convert_angle(value, from_unit, to_unit)