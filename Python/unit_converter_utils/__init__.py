"""
Unit Converter Utils - 多功能单位转换工具库

支持转换类型:
- 长度 (Length): m, km, cm, mm, mi, yd, ft, in, nmi, ly
- 重量 (Weight): kg, g, mg, t, lb, oz, st
- 温度 (Temperature): C, F, K
- 体积 (Volume): L, mL, gal, qt, pt, cup, fl_oz, m3, cm3
- 面积 (Area): m2, km2, ha, acre, ft2, in2
- 时间 (Time): s, ms, us, ns, min, h, d, w, y
- 速度 (Speed): m/s, km/h, mph, knot, mach
- 数据 (Data): B, KB, MB, GB, TB, PB, KiB, MiB, GiB, TiB
- 压力 (Pressure): Pa, kPa, MPa, bar, psi, atm, mmHg
- 角度 (Angle): deg, rad, grad, arcmin, arcsec

零外部依赖，纯Python实现
"""

from .converter import UnitConverter, convert, convert_length, convert_weight
from .converter import convert_temperature, convert_volume, convert_area
from .converter import convert_time, convert_speed, convert_data, convert_pressure, convert_angle

__all__ = [
    'UnitConverter',
    'convert',
    'convert_length',
    'convert_weight',
    'convert_temperature',
    'convert_volume',
    'convert_area',
    'convert_time',
    'convert_speed',
    'convert_data',
    'convert_pressure',
    'convert_angle',
]

__version__ = '1.0.0'