"""
Periodic Table Utilities - 化学元素周期表工具

A comprehensive toolkit for working with chemical elements and the periodic table.
Zero external dependencies - pure Python implementation.

Features:
- Query element information by atomic number, symbol, or name
- Calculate molecular weights for chemical formulas
- Find elements by period, group, or category
- Get electron configurations
- Support for all 118 known elements
"""

from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import re


class ElementCategory(Enum):
    """元素分类枚举"""
    ALKALI_METAL = "碱金属"
    ALKALINE_EARTH_METAL = "碱土金属"
    TRANSITION_METAL = "过渡金属"
    POST_TRANSITION_METAL = "后过渡金属"
    METALLOID = "准金属"
    NONMETAL = "非金属"
    HALOGEN = "卤素"
    NOBLE_GAS = "稀有气体"
    LANTHANIDE = "镧系元素"
    ACTINIDE = "锕系元素"
    UNKNOWN = "未知"


class ElementState(Enum):
    """元素状态枚举（常温常压下）"""
    SOLID = "固态"
    LIQUID = "液态"
    GAS = "气态"
    UNKNOWN = "未知"


@dataclass
class Element:
    """元素数据类"""
    atomic_number: int  # 原子序数
    symbol: str  # 元素符号
    name: str  # 元素名称（中文）
    name_en: str  # 元素名称（英文）
    atomic_mass: float  # 原子量
    category: ElementCategory  # 分类
    period: int  # 周期
    group: int  # 族（0表示镧系/锕系）
    electron_configuration: str  # 电子排布
    state: ElementState  # 常温状态
    melting_point: Optional[float] = None  # 熔点（开尔文）
    boiling_point: Optional[float] = None  # 沸点（开尔文）
    density: Optional[float] = None  # 密度（g/cm³）
    discovery_year: Optional[int] = None  # 发现年份
    discoverer: Optional[str] = None  # 发现者


# 完整的元素周期表数据
ELEMENTS: Dict[int, Element] = {
    1: Element(1, "H", "氢", "Hydrogen", 1.008, ElementCategory.NONMETAL, 1, 1, "1s1", ElementState.GAS, 14.01, 20.28, 0.00008988, 1766, "Henry Cavendish"),
    2: Element(2, "He", "氦", "Helium", 4.003, ElementCategory.NOBLE_GAS, 1, 18, "1s2", ElementState.GAS, 0.95, 4.22, 0.0001785, 1868, "Pierre Janssen"),
    3: Element(3, "Li", "锂", "Lithium", 6.941, ElementCategory.ALKALI_METAL, 2, 1, "[He]2s1", ElementState.SOLID, 453.69, 1615, 0.534, 1817, "Johan August Arfwedson"),
    4: Element(4, "Be", "铍", "Beryllium", 9.012, ElementCategory.ALKALINE_EARTH_METAL, 2, 2, "[He]2s2", ElementState.SOLID, 1560, 2742, 1.85, 1798, "Louis Nicolas Vauquelin"),
    5: Element(5, "B", "硼", "Boron", 10.81, ElementCategory.METALLOID, 2, 13, "[He]2s2 2p1", ElementState.SOLID, 2349, 4200, 2.34, 1808, "Joseph Louis Gay-Lussac"),
    6: Element(6, "C", "碳", "Carbon", 12.011, ElementCategory.NONMETAL, 2, 14, "[He]2s2 2p2", ElementState.SOLID, 3823, 4098, 2.267, None, "古代已知"),
    7: Element(7, "N", "氮", "Nitrogen", 14.007, ElementCategory.NONMETAL, 2, 15, "[He]2s2 2p3", ElementState.GAS, 63.15, 77.36, 0.0012506, 1772, "Daniel Rutherford"),
    8: Element(8, "O", "氧", "Oxygen", 15.999, ElementCategory.NONMETAL, 2, 16, "[He]2s2 2p4", ElementState.GAS, 54.36, 90.20, 0.001429, 1774, "Joseph Priestley"),
    9: Element(9, "F", "氟", "Fluorine", 18.998, ElementCategory.HALOGEN, 2, 17, "[He]2s2 2p5", ElementState.GAS, 53.53, 85.03, 0.001696, 1886, "Henri Moissan"),
    10: Element(10, "Ne", "氖", "Neon", 20.180, ElementCategory.NOBLE_GAS, 2, 18, "[He]2s2 2p6", ElementState.GAS, 24.56, 27.07, 0.0008999, 1898, "William Ramsay"),
    11: Element(11, "Na", "钠", "Sodium", 22.990, ElementCategory.ALKALI_METAL, 3, 1, "[Ne]3s1", ElementState.SOLID, 370.87, 1156, 0.971, 1807, "Humphry Davy"),
    12: Element(12, "Mg", "镁", "Magnesium", 24.305, ElementCategory.ALKALINE_EARTH_METAL, 3, 2, "[Ne]3s2", ElementState.SOLID, 923, 1363, 1.738, 1755, "Joseph Black"),
    13: Element(13, "Al", "铝", "Aluminum", 26.982, ElementCategory.POST_TRANSITION_METAL, 3, 13, "[Ne]3s2 3p1", ElementState.SOLID, 933.47, 2792, 2.698, 1825, "Hans Christian Ørsted"),
    14: Element(14, "Si", "硅", "Silicon", 28.086, ElementCategory.METALLOID, 3, 14, "[Ne]3s2 3p2", ElementState.SOLID, 1687, 3538, 2.3296, 1824, "Jöns Jacob Berzelius"),
    15: Element(15, "P", "磷", "Phosphorus", 30.974, ElementCategory.NONMETAL, 3, 15, "[Ne]3s2 3p3", ElementState.SOLID, 317.30, 553.65, 1.82, 1669, "Hennig Brand"),
    16: Element(16, "S", "硫", "Sulfur", 32.06, ElementCategory.NONMETAL, 3, 16, "[Ne]3s2 3p4", ElementState.SOLID, 388.36, 717.87, 2.067, None, "古代已知"),
    17: Element(17, "Cl", "氯", "Chlorine", 35.45, ElementCategory.HALOGEN, 3, 17, "[Ne]3s2 3p5", ElementState.GAS, 171.65, 239.11, 0.003214, 1774, "Carl Wilhelm Scheele"),
    18: Element(18, "Ar", "氩", "Argon", 39.948, ElementCategory.NOBLE_GAS, 3, 18, "[Ne]3s2 3p6", ElementState.GAS, 83.80, 87.30, 0.0017837, 1894, "Lord Rayleigh"),
    19: Element(19, "K", "钾", "Potassium", 39.098, ElementCategory.ALKALI_METAL, 4, 1, "[Ar]4s1", ElementState.SOLID, 336.53, 1032, 0.862, 1807, "Humphry Davy"),
    20: Element(20, "Ca", "钙", "Calcium", 40.078, ElementCategory.ALKALINE_EARTH_METAL, 4, 2, "[Ar]4s2", ElementState.SOLID, 1115, 1757, 1.54, 1808, "Humphry Davy"),
    21: Element(21, "Sc", "钪", "Scandium", 44.956, ElementCategory.TRANSITION_METAL, 4, 3, "[Ar]3d1 4s2", ElementState.SOLID, 1814, 3109, 2.989, 1879, "Lars Fredrik Nilson"),
    22: Element(22, "Ti", "钛", "Titanium", 47.867, ElementCategory.TRANSITION_METAL, 4, 4, "[Ar]3d2 4s2", ElementState.SOLID, 1941, 3560, 4.54, 1791, "William Gregor"),
    23: Element(23, "V", "钒", "Vanadium", 50.942, ElementCategory.TRANSITION_METAL, 4, 5, "[Ar]3d3 4s2", ElementState.SOLID, 2183, 3680, 6.11, 1801, "Andrés Manuel del Río"),
    24: Element(24, "Cr", "铬", "Chromium", 51.996, ElementCategory.TRANSITION_METAL, 4, 6, "[Ar]3d5 4s1", ElementState.SOLID, 2180, 2944, 7.15, 1794, "Louis Nicolas Vauquelin"),
    25: Element(25, "Mn", "锰", "Manganese", 54.938, ElementCategory.TRANSITION_METAL, 4, 7, "[Ar]3d5 4s2", ElementState.SOLID, 1519, 2334, 7.44, 1774, "Johan Gottlieb Gahn"),
    26: Element(26, "Fe", "铁", "Iron", 55.845, ElementCategory.TRANSITION_METAL, 4, 8, "[Ar]3d6 4s2", ElementState.SOLID, 1811, 3134, 7.874, None, "古代已知"),
    27: Element(27, "Co", "钴", "Cobalt", 58.933, ElementCategory.TRANSITION_METAL, 4, 9, "[Ar]3d7 4s2", ElementState.SOLID, 1768, 3200, 8.86, 1735, "Georg Brandt"),
    28: Element(28, "Ni", "镍", "Nickel", 58.693, ElementCategory.TRANSITION_METAL, 4, 10, "[Ar]3d8 4s2", ElementState.SOLID, 1728, 3186, 8.912, 1751, "Axel Fredrik Cronstedt"),
    29: Element(29, "Cu", "铜", "Copper", 63.546, ElementCategory.TRANSITION_METAL, 4, 11, "[Ar]3d10 4s1", ElementState.SOLID, 1357.77, 2835, 8.96, None, "古代已知"),
    30: Element(30, "Zn", "锌", "Zinc", 65.38, ElementCategory.TRANSITION_METAL, 4, 12, "[Ar]3d10 4s2", ElementState.SOLID, 692.88, 1180, 7.134, None, "古代已知"),
    31: Element(31, "Ga", "镓", "Gallium", 69.723, ElementCategory.POST_TRANSITION_METAL, 4, 13, "[Ar]3d10 4s2 4p1", ElementState.SOLID, 302.91, 2477, 5.907, 1875, "Lecoq de Boisbaudran"),
    32: Element(32, "Ge", "锗", "Germanium", 72.63, ElementCategory.METALLOID, 4, 14, "[Ar]3d10 4s2 4p2", ElementState.SOLID, 1211.40, 3106, 5.323, 1886, "Clemens Winkler"),
    33: Element(33, "As", "砷", "Arsenic", 74.922, ElementCategory.METALLOID, 4, 15, "[Ar]3d10 4s2 4p3", ElementState.SOLID, 1090, 887, 5.776, None, "古代已知"),
    34: Element(34, "Se", "硒", "Selenium", 78.971, ElementCategory.NONMETAL, 4, 16, "[Ar]3d10 4s2 4p4", ElementState.SOLID, 494, 958, 4.809, 1817, "Jöns Jacob Berzelius"),
    35: Element(35, "Br", "溴", "Bromine", 79.904, ElementCategory.HALOGEN, 4, 17, "[Ar]3d10 4s2 4p5", ElementState.LIQUID, 265.95, 332, 3.122, 1826, "Antoine Jérôme Balard"),
    36: Element(36, "Kr", "氪", "Krypton", 83.798, ElementCategory.NOBLE_GAS, 4, 18, "[Ar]3d10 4s2 4p6", ElementState.GAS, 115.79, 119.93, 0.003733, 1898, "William Ramsay"),
    37: Element(37, "Rb", "铷", "Rubidium", 85.468, ElementCategory.ALKALI_METAL, 5, 1, "[Kr]5s1", ElementState.SOLID, 312.46, 961, 1.532, 1861, "Robert Bunsen"),
    38: Element(38, "Sr", "锶", "Strontium", 87.62, ElementCategory.ALKALINE_EARTH_METAL, 5, 2, "[Kr]5s2", ElementState.SOLID, 1050, 1655, 2.64, 1790, "Adair Crawford"),
    39: Element(39, "Y", "钇", "Yttrium", 88.906, ElementCategory.TRANSITION_METAL, 5, 3, "[Kr]4d1 5s2", ElementState.SOLID, 1799, 3609, 4.469, 1794, "Johan Gadolin"),
    40: Element(40, "Zr", "锆", "Zirconium", 91.224, ElementCategory.TRANSITION_METAL, 5, 4, "[Kr]4d2 5s2", ElementState.SOLID, 2128, 4682, 6.506, 1789, "Martin Heinrich Klaproth"),
    41: Element(41, "Nb", "铌", "Niobium", 92.906, ElementCategory.TRANSITION_METAL, 5, 5, "[Kr]4d4 5s1", ElementState.SOLID, 2750, 5017, 8.57, 1801, "Charles Hatchett"),
    42: Element(42, "Mo", "钼", "Molybdenum", 95.95, ElementCategory.TRANSITION_METAL, 5, 6, "[Kr]4d5 5s1", ElementState.SOLID, 2896, 4912, 10.22, 1781, "Peter Jacob Hjelm"),
    43: Element(43, "Tc", "锝", "Technetium", 98.0, ElementCategory.TRANSITION_METAL, 5, 7, "[Kr]4d5 5s2", ElementState.SOLID, 2430, 4538, 11.5, 1937, "Carlo Perrier"),
    44: Element(44, "Ru", "钌", "Ruthenium", 101.07, ElementCategory.TRANSITION_METAL, 5, 8, "[Kr]4d7 5s1", ElementState.SOLID, 2607, 4423, 12.37, 1844, "Karl Ernst Claus"),
    45: Element(45, "Rh", "铑", "Rhodium", 102.91, ElementCategory.TRANSITION_METAL, 5, 9, "[Kr]4d8 5s1", ElementState.SOLID, 2237, 3968, 12.41, 1803, "William Hyde Wollaston"),
    46: Element(46, "Pd", "钯", "Palladium", 106.42, ElementCategory.TRANSITION_METAL, 5, 10, "[Kr]4d10", ElementState.SOLID, 1828.05, 3236, 12.02, 1802, "William Hyde Wollaston"),
    47: Element(47, "Ag", "银", "Silver", 107.87, ElementCategory.TRANSITION_METAL, 5, 11, "[Kr]4d10 5s1", ElementState.SOLID, 1234.93, 2435, 10.501, None, "古代已知"),
    48: Element(48, "Cd", "镉", "Cadmium", 112.41, ElementCategory.TRANSITION_METAL, 5, 12, "[Kr]4d10 5s2", ElementState.SOLID, 594.22, 1040, 8.69, 1817, "Karl Samuel Leberecht Hermann"),
    49: Element(49, "In", "铟", "Indium", 114.82, ElementCategory.POST_TRANSITION_METAL, 5, 13, "[Kr]4d10 5s2 5p1", ElementState.SOLID, 429.75, 2345, 7.31, 1863, "Ferdinand Reich"),
    50: Element(50, "Sn", "锡", "Tin", 118.71, ElementCategory.POST_TRANSITION_METAL, 5, 14, "[Kr]4d10 5s2 5p2", ElementState.SOLID, 505.08, 2875, 7.287, None, "古代已知"),
    51: Element(51, "Sb", "锑", "Antimony", 121.76, ElementCategory.METALLOID, 5, 15, "[Kr]4d10 5s2 5p3", ElementState.SOLID, 903.78, 1860, 6.685, None, "古代已知"),
    52: Element(52, "Te", "碲", "Tellurium", 127.60, ElementCategory.METALLOID, 5, 16, "[Kr]4d10 5s2 5p4", ElementState.SOLID, 722.66, 1261, 6.232, 1783, "Franz-Joseph Müller von Reichenstein"),
    53: Element(53, "I", "碘", "Iodine", 126.90, ElementCategory.HALOGEN, 5, 17, "[Kr]4d10 5s2 5p5", ElementState.SOLID, 386.85, 457.55, 4.93, 1811, "Bernard Courtois"),
    54: Element(54, "Xe", "氙", "Xenon", 131.29, ElementCategory.NOBLE_GAS, 5, 18, "[Kr]4d10 5s2 5p6", ElementState.GAS, 161.36, 165.03, 0.005887, 1898, "William Ramsay"),
    55: Element(55, "Cs", "铯", "Cesium", 132.91, ElementCategory.ALKALI_METAL, 6, 1, "[Xe]6s1", ElementState.SOLID, 301.59, 944, 1.873, 1860, "Robert Bunsen"),
    56: Element(56, "Ba", "钡", "Barium", 137.33, ElementCategory.ALKALINE_EARTH_METAL, 6, 2, "[Xe]6s2", ElementState.SOLID, 1000, 2170, 3.594, 1808, "Humphry Davy"),
    57: Element(57, "La", "镧", "Lanthanum", 138.91, ElementCategory.LANTHANIDE, 6, 0, "[Xe]5d1 6s2", ElementState.SOLID, 1193, 3737, 6.145, 1839, "Carl Gustaf Mosander"),
    58: Element(58, "Ce", "铈", "Cerium", 140.12, ElementCategory.LANTHANIDE, 6, 0, "[Xe]4f1 5d1 6s2", ElementState.SOLID, 1068, 3716, 6.77, 1803, "Jöns Jacob Berzelius"),
    59: Element(59, "Pr", "镨", "Praseodymium", 140.91, ElementCategory.LANTHANIDE, 6, 0, "[Xe]4f3 6s2", ElementState.SOLID, 1208, 3793, 6.773, 1885, "Carl Auer von Welsbach"),
    60: Element(60, "Nd", "钕", "Neodymium", 144.24, ElementCategory.LANTHANIDE, 6, 0, "[Xe]4f4 6s2", ElementState.SOLID, 1297, 3347, 7.007, 1885, "Carl Auer von Welsbach"),
    61: Element(61, "Pm", "钷", "Promethium", 145.0, ElementCategory.LANTHANIDE, 6, 0, "[Xe]4f5 6s2", ElementState.SOLID, 1315, 3273, 7.26, 1945, "Chien Shiung Wu"),
    62: Element(62, "Sm", "钐", "Samarium", 150.36, ElementCategory.LANTHANIDE, 6, 0, "[Xe]4f6 6s2", ElementState.SOLID, 1345, 2067, 7.52, 1879, "Lecoq de Boisbaudran"),
    63: Element(63, "Eu", "铕", "Europium", 151.96, ElementCategory.LANTHANIDE, 6, 0, "[Xe]4f7 6s2", ElementState.SOLID, 1099, 1802, 5.243, 1901, "Eugène-Anatole Demarçay"),
    64: Element(64, "Gd", "钆", "Gadolinium", 157.25, ElementCategory.LANTHANIDE, 6, 0, "[Xe]4f7 5d1 6s2", ElementState.SOLID, 1585, 3546, 7.895, 1880, "Jean Charles Galissard de Marignac"),
    65: Element(65, "Tb", "铽", "Terbium", 158.93, ElementCategory.LANTHANIDE, 6, 0, "[Xe]4f9 6s2", ElementState.SOLID, 1629, 3503, 8.229, 1843, "Carl Gustaf Mosander"),
    66: Element(66, "Dy", "镝", "Dysprosium", 162.50, ElementCategory.LANTHANIDE, 6, 0, "[Xe]4f10 6s2", ElementState.SOLID, 1680, 2840, 8.55, 1886, "Lecoq de Boisbaudran"),
    67: Element(67, "Ho", "钬", "Holmium", 164.93, ElementCategory.LANTHANIDE, 6, 0, "[Xe]4f11 6s2", ElementState.SOLID, 1734, 2993, 8.795, 1878, "Marc Delafontaine"),
    68: Element(68, "Er", "铒", "Erbium", 167.26, ElementCategory.LANTHANIDE, 6, 0, "[Xe]4f12 6s2", ElementState.SOLID, 1802, 3141, 9.066, 1843, "Carl Gustaf Mosander"),
    69: Element(69, "Tm", "铥", "Thulium", 168.93, ElementCategory.LANTHANIDE, 6, 0, "[Xe]4f13 6s2", ElementState.SOLID, 1818, 2223, 9.321, 1879, "Per Teodor Cleve"),
    70: Element(70, "Yb", "镱", "Ytterbium", 173.05, ElementCategory.LANTHANIDE, 6, 0, "[Xe]4f14 6s2", ElementState.SOLID, 1097, 1469, 6.965, 1878, "Jean Charles Galissard de Marignac"),
    71: Element(71, "Lu", "镥", "Lutetium", 174.97, ElementCategory.LANTHANIDE, 6, 0, "[Xe]4f14 5d1 6s2", ElementState.SOLID, 1925, 3675, 9.84, 1907, "Georges Urbain"),
    72: Element(72, "Hf", "铪", "Hafnium", 178.49, ElementCategory.TRANSITION_METAL, 6, 4, "[Xe]4f14 5d2 6s2", ElementState.SOLID, 2506, 4876, 13.31, 1923, "Dirk Coster"),
    73: Element(73, "Ta", "钽", "Tantalum", 180.95, ElementCategory.TRANSITION_METAL, 6, 5, "[Xe]4f14 5d3 6s2", ElementState.SOLID, 3290, 5731, 16.654, 1802, "Anders Gustaf Ekeberg"),
    74: Element(74, "W", "钨", "Tungsten", 183.84, ElementCategory.TRANSITION_METAL, 6, 6, "[Xe]4f14 5d4 6s2", ElementState.SOLID, 3695, 5828, 19.25, 1783, "Juan José Elhuyar"),
    75: Element(75, "Re", "铼", "Rhenium", 186.21, ElementCategory.TRANSITION_METAL, 6, 7, "[Xe]4f14 5d5 6s2", ElementState.SOLID, 3459, 5869, 21.02, 1925, "Masataka Ogawa"),
    76: Element(76, "Os", "锇", "Osmium", 190.23, ElementCategory.TRANSITION_METAL, 6, 8, "[Xe]4f14 5d6 6s2", ElementState.SOLID, 3306, 5285, 22.59, 1803, "Smithson Tennant"),
    77: Element(77, "Ir", "铱", "Iridium", 192.22, ElementCategory.TRANSITION_METAL, 6, 9, "[Xe]4f14 5d7 6s2", ElementState.SOLID, 2719, 4701, 22.56, 1803, "Smithson Tennant"),
    78: Element(78, "Pt", "铂", "Platinum", 195.08, ElementCategory.TRANSITION_METAL, 6, 10, "[Xe]4f14 5d9 6s1", ElementState.SOLID, 2041.55, 4098, 21.46, 1735, "Antonio de Ulloa"),
    79: Element(79, "Au", "金", "Gold", 196.97, ElementCategory.TRANSITION_METAL, 6, 11, "[Xe]4f14 5d10 6s1", ElementState.SOLID, 1337.33, 3129, 19.282, None, "古代已知"),
    80: Element(80, "Hg", "汞", "Mercury", 200.59, ElementCategory.TRANSITION_METAL, 6, 12, "[Xe]4f14 5d10 6s2", ElementState.LIQUID, 234.32, 629.88, 13.5336, None, "古代已知"),
    81: Element(81, "Tl", "铊", "Thallium", 204.38, ElementCategory.POST_TRANSITION_METAL, 6, 13, "[Xe]4f14 5d10 6s2 6p1", ElementState.SOLID, 577, 1746, 11.85, 1861, "William Crookes"),
    82: Element(82, "Pb", "铅", "Lead", 207.2, ElementCategory.POST_TRANSITION_METAL, 6, 14, "[Xe]4f14 5d10 6s2 6p2", ElementState.SOLID, 600.61, 2022, 11.342, None, "古代已知"),
    83: Element(83, "Bi", "铋", "Bismuth", 208.98, ElementCategory.POST_TRANSITION_METAL, 6, 15, "[Xe]4f14 5d10 6s2 6p3", ElementState.SOLID, 544.55, 1837, 9.807, 1753, "Claude François Geoffroy"),
    84: Element(84, "Po", "钋", "Polonium", 209.0, ElementCategory.METALLOID, 6, 16, "[Xe]4f14 5d10 6s2 6p4", ElementState.SOLID, 527, 1235, 9.32, 1898, "Pierre Curie"),
    85: Element(85, "At", "砹", "Astatine", 210.0, ElementCategory.HALOGEN, 6, 17, "[Xe]4f14 5d10 6s2 6p5", ElementState.SOLID, 575, 610, 7, 1940, "Dale R. Corson"),
    86: Element(86, "Rn", "氡", "Radon", 222.0, ElementCategory.NOBLE_GAS, 6, 18, "[Xe]4f14 5d10 6s2 6p6", ElementState.GAS, 202, 211.45, 0.00973, 1900, "Friedrich Ernst Dorn"),
    87: Element(87, "Fr", "钫", "Francium", 223.0, ElementCategory.ALKALI_METAL, 7, 1, "[Rn]7s1", ElementState.SOLID, 300, 950, 1.87, 1939, "Marguerite Perey"),
    88: Element(88, "Ra", "镭", "Radium", 226.0, ElementCategory.ALKALINE_EARTH_METAL, 7, 2, "[Rn]7s2", ElementState.SOLID, 973, 2010, 5.5, 1898, "Pierre Curie"),
    89: Element(89, "Ac", "锕", "Actinium", 227.0, ElementCategory.ACTINIDE, 7, 0, "[Rn]6d1 7s2", ElementState.SOLID, 1323, 3471, 10.07, 1899, "André-Louis Debierne"),
    90: Element(90, "Th", "钍", "Thorium", 232.04, ElementCategory.ACTINIDE, 7, 0, "[Rn]6d2 7s2", ElementState.SOLID, 2023, 5061, 11.72, 1829, "Jöns Jacob Berzelius"),
    91: Element(91, "Pa", "镤", "Protactinium", 231.04, ElementCategory.ACTINIDE, 7, 0, "[Rn]5f2 6d1 7s2", ElementState.SOLID, 1841, 4301, 15.37, 1913, "Kasimir Fajans"),
    92: Element(92, "U", "铀", "Uranium", 238.03, ElementCategory.ACTINIDE, 7, 0, "[Rn]5f3 6d1 7s2", ElementState.SOLID, 1405.3, 4404, 18.95, 1789, "Martin Heinrich Klaproth"),
    93: Element(93, "Np", "镎", "Neptunium", 237.0, ElementCategory.ACTINIDE, 7, 0, "[Rn]5f4 6d1 7s2", ElementState.SOLID, 912, 4447, 20.45, 1940, "Edwin McMillan"),
    94: Element(94, "Pu", "钚", "Plutonium", 244.0, ElementCategory.ACTINIDE, 7, 0, "[Rn]5f6 7s2", ElementState.SOLID, 912.5, 3501, 19.84, 1940, "Glenn T. Seaborg"),
    95: Element(95, "Am", "镅", "Americium", 243.0, ElementCategory.ACTINIDE, 7, 0, "[Rn]5f7 7s2", ElementState.SOLID, 1449, 2880, 13.69, 1944, "Glenn T. Seaborg"),
    96: Element(96, "Cm", "锔", "Curium", 247.0, ElementCategory.ACTINIDE, 7, 0, "[Rn]5f7 6d1 7s2", ElementState.SOLID, 1613, 3383, 13.51, 1944, "Glenn T. Seaborg"),
    97: Element(97, "Bk", "锫", "Berkelium", 247.0, ElementCategory.ACTINIDE, 7, 0, "[Rn]5f9 7s2", ElementState.SOLID, 1259, 2900, 14.79, 1949, "Stanley G. Thompson"),
    98: Element(98, "Cf", "锎", "Californium", 251.0, ElementCategory.ACTINIDE, 7, 0, "[Rn]5f10 7s2", ElementState.SOLID, 1173, 1743, 15.1, 1950, "Stanley G. Thompson"),
    99: Element(99, "Es", "锿", "Einsteinium", 252.0, ElementCategory.ACTINIDE, 7, 0, "[Rn]5f11 7s2", ElementState.SOLID, 1133, 1269, 8.84, 1952, "Albert Ghiorso"),
    100: Element(100, "Fm", "镄", "Fermium", 257.0, ElementCategory.ACTINIDE, 7, 0, "[Rn]5f12 7s2", ElementState.SOLID, 1800, None, None, 1952, "Albert Ghiorso"),
    101: Element(101, "Md", "钔", "Mendelevium", 258.0, ElementCategory.ACTINIDE, 7, 0, "[Rn]5f13 7s2", ElementState.SOLID, 1100, None, None, 1955, "Albert Ghiorso"),
    102: Element(102, "No", "锘", "Nobelium", 259.0, ElementCategory.ACTINIDE, 7, 0, "[Rn]5f14 7s2", ElementState.SOLID, 1100, None, None, 1958, "Albert Ghiorso"),
    103: Element(103, "Lr", "铹", "Lawrencium", 262.0, ElementCategory.ACTINIDE, 7, 0, "[Rn]5f14 7p1 7s2", ElementState.SOLID, 1900, None, None, 1961, "Albert Ghiorso"),
    104: Element(104, "Rf", "𬬻", "Rutherfordium", 267.0, ElementCategory.TRANSITION_METAL, 7, 4, "[Rn]5f14 6d2 7s2", ElementState.SOLID, 2400, 5800, 23.2, 1964, "Joint Institute for Nuclear Research"),
    105: Element(105, "Db", "𬭊", "Dubnium", 268.0, ElementCategory.TRANSITION_METAL, 7, 5, "[Rn]5f14 6d3 7s2", ElementState.SOLID, None, None, None, 1967, "Joint Institute for Nuclear Research"),
    106: Element(106, "Sg", "𬭳", "Seaborgium", 271.0, ElementCategory.TRANSITION_METAL, 7, 6, "[Rn]5f14 6d4 7s2", ElementState.SOLID, None, None, None, 1974, "Albert Ghiorso"),
    107: Element(107, "Bh", "𬭛", "Bohrium", 270.0, ElementCategory.TRANSITION_METAL, 7, 7, "[Rn]5f14 6d5 7s2", ElementState.SOLID, None, None, None, 1981, "Peter Armbruster"),
    108: Element(108, "Hs", "𬭶", "Hassium", 277.0, ElementCategory.TRANSITION_METAL, 7, 8, "[Rn]5f14 6d6 7s2", ElementState.SOLID, None, None, None, 1984, "Peter Armbruster"),
    109: Element(109, "Mt", "鿏", "Meitnerium", 276.0, ElementCategory.TRANSITION_METAL, 7, 9, "[Rn]5f14 6d7 7s2", ElementState.SOLID, None, None, None, 1982, "Peter Armbruster"),
    110: Element(110, "Ds", "𫟼", "Darmstadtium", 281.0, ElementCategory.TRANSITION_METAL, 7, 10, "[Rn]5f14 6d8 7s2", ElementState.SOLID, None, None, None, 1994, "Sigurd Hofmann"),
    111: Element(111, "Rg", "𬬭", "Roentgenium", 280.0, ElementCategory.TRANSITION_METAL, 7, 11, "[Rn]5f14 6d9 7s2", ElementState.SOLID, None, None, None, 1994, "Sigurd Hofmann"),
    112: Element(112, "Cn", "鿔", "Copernicium", 285.0, ElementCategory.TRANSITION_METAL, 7, 12, "[Rn]5f14 6d10 7s2", ElementState.SOLID, None, None, None, 1996, "Sigurd Hofmann"),
    113: Element(113, "Nh", "鿭", "Nihonium", 284.0, ElementCategory.POST_TRANSITION_METAL, 7, 13, "[Rn]5f14 6d10 7s2 7p1", ElementState.SOLID, None, None, None, 2003, "Kosuke Morita"),
    114: Element(114, "Fl", "𫓧", "Flerovium", 289.0, ElementCategory.POST_TRANSITION_METAL, 7, 14, "[Rn]5f14 6d10 7s2 7p2", ElementState.SOLID, None, None, None, 1998, "Yuri Oganessian"),
    115: Element(115, "Mc", "镆", "Moscovium", 288.0, ElementCategory.POST_TRANSITION_METAL, 7, 15, "[Rn]5f14 6d10 7s2 7p3", ElementState.SOLID, None, None, None, 2003, "Yuri Oganessian"),
    116: Element(116, "Lv", "𫟷", "Livermorium", 293.0, ElementCategory.POST_TRANSITION_METAL, 7, 16, "[Rn]5f14 6d10 7s2 7p4", ElementState.SOLID, None, None, None, 2000, "Yuri Oganessian"),
    117: Element(117, "Ts", "鿬", "Tennessine", 294.0, ElementCategory.HALOGEN, 7, 17, "[Rn]5f14 6d10 7s2 7p5", ElementState.SOLID, None, None, None, 2010, "Yuri Oganessian"),
    118: Element(118, "Og", "鿫", "Oganesson", 294.0, ElementCategory.NOBLE_GAS, 7, 18, "[Rn]5f14 6d10 7s2 7p6", ElementState.SOLID, None, None, None, 2002, "Yuri Oganessian"),
}

# 构建符号到原子序数的映射
SYMBOL_TO_NUMBER: Dict[str, int] = {e.symbol: n for n, e in ELEMENTS.items()}

# 构建名称到原子序数的映射（支持中英文）
NAME_TO_NUMBER: Dict[str, int] = {}
for n, e in ELEMENTS.items():
    NAME_TO_NUMBER[e.name.lower()] = n
    NAME_TO_NUMBER[e.name_en.lower()] = n


def get_element(query: Union[int, str]) -> Optional[Element]:
    """
    根据原子序数、符号或名称获取元素信息
    
    Args:
        query: 原子序数(int)、元素符号(str)或元素名称(str，支持中英文)
    
    Returns:
        Element对象，如果未找到则返回None
    
    Examples:
        >>> get_element(1)
        Element(atomic_number=1, symbol='H', name='氢', ...)
        >>> get_element('Fe')
        Element(atomic_number=26, symbol='Fe', name='铁', ...)
        >>> get_element('oxygen')
        Element(atomic_number=8, symbol='O', name='氧', ...)
        >>> get_element('碳')
        Element(atomic_number=6, symbol='C', name='碳', ...)
    """
    if isinstance(query, int):
        return ELEMENTS.get(query)
    
    query_str = str(query).strip()
    
    # 尝试符号匹配
    if query_str in SYMBOL_TO_NUMBER:
        return ELEMENTS[SYMBOL_TO_NUMBER[query_str]]
    
    # 尝试名称匹配
    query_lower = query_str.lower()
    if query_lower in NAME_TO_NUMBER:
        return ELEMENTS[NAME_TO_NUMBER[query_lower]]
    
    return None


def get_elements_by_period(period: int) -> List[Element]:
    """
    获取指定周期的所有元素
    
    Args:
        period: 周期号 (1-7)
    
    Returns:
        该周期的元素列表
    
    Examples:
        >>> len(get_elements_by_period(1))
        2
        >>> [e.symbol for e in get_elements_by_period(1)]
        ['H', 'He']
    """
    return [e for e in ELEMENTS.values() if e.period == period]


def get_elements_by_group(group: int) -> List[Element]:
    """
    获取指定族的所有元素
    
    Args:
        group: 族号 (1-18，0表示镧系/锕系)
    
    Returns:
        该族的元素列表
    
    Examples:
        >>> [e.symbol for e in get_elements_by_group(1)]
        ['Li', 'Na', 'K', 'Rb', 'Cs', 'Fr']
    """
    return [e for e in ELEMENTS.values() if e.group == group]


def get_elements_by_category(category: ElementCategory) -> List[Element]:
    """
    获取指定分类的所有元素
    
    Args:
        category: 元素分类
    
    Returns:
        该分类的元素列表
    
    Examples:
        >>> len(get_elements_by_category(ElementCategory.NOBLE_GAS))
        7
    """
    return [e for e in ELEMENTS.values() if e.category == category]


def search_elements(keyword: str) -> List[Element]:
    """
    搜索元素（按符号、名称匹配）
    
    Args:
        keyword: 搜索关键词
    
    Returns:
        匹配的元素列表
    
    Examples:
        >>> [e.symbol for e in search_elements('氧')]
        ['O']
        >>> [e.symbol for e in search_elements('gen')]
        ['H', 'O', 'N']
    """
    keyword_lower = keyword.lower()
    results = []
    for e in ELEMENTS.values():
        if (keyword_lower in e.symbol.lower() or
            keyword_lower in e.name or
            keyword_lower in e.name_en.lower()):
            results.append(e)
    return results


def calculate_molecular_weight(formula: str) -> Tuple[float, Dict[str, int]]:
    """
    计算分子量
    
    Args:
        formula: 化学式 (如 H2O, NaCl, C6H12O6)
    
    Returns:
        (分子量, {元素符号: 原子数})
    
    Raises:
        ValueError: 如果化学式格式错误或包含未知元素
    
    Examples:
        >>> calculate_molecular_weight('H2O')
        (18.015, {'H': 2, 'O': 1})
        >>> calculate_molecular_weight('NaCl')
        (58.443, {'Na': 1, 'Cl': 1})
    """
    # 解析化学式
    pattern = r'([A-Z][a-z]?)(\d*)'
    matches = re.findall(pattern, formula)
    
    if not matches or ''.join(sym + (num if num else '') for sym, num in matches) != formula:
        raise ValueError(f"无效的化学式格式: {formula}")
    
    composition: Dict[str, int] = {}
    total_mass = 0.0
    
    for symbol, count_str in matches:
        if not symbol:
            continue
        
        element = get_element(symbol)
        if element is None:
            raise ValueError(f"未知元素: {symbol}")
        
        count = int(count_str) if count_str else 1
        composition[symbol] = composition.get(symbol, 0) + count
        total_mass += element.atomic_mass * count
    
    return round(total_mass, 3), composition


def format_element_info(element: Element) -> str:
    """
    格式化元素信息为可读字符串
    
    Args:
        element: 元素对象
    
    Returns:
        格式化的元素信息字符串
    
    Examples:
        >>> print(format_element_info(get_element(79)))
        ╔══════════════════════════════╗
        ║           金 (Au)            ║
        ╠══════════════════════════════╣
        ║ 原子序数: 79                 ║
        ║ 英文名: Gold                 ║
        ║ 原子量: 196.97               ║
        ║ 分类: 过渡金属               ║
        ║ 周期: 6  族: 11             ║
        ║ 电子排布: [Xe]4f14 5d10 6s1  ║
        ║ 常温状态: 固态               ║
        ║ 密度: 19.282 g/cm³          ║
        ║ 熔点: 1337.33 K             ║
        ║ 沸点: 3129 K                ║
        ╚══════════════════════════════╝
    """
    lines = [
        "╔══════════════════════════════╗",
        f"║{element.name} ({element.symbol})".center(30) + "║",
        "╠══════════════════════════════╣",
        f"║ 原子序数: {element.atomic_number}".ljust(30) + "║",
        f"║ 英文名: {element.name_en}".ljust(30) + "║",
        f"║ 原子量: {element.atomic_mass}".ljust(30) + "║",
        f"║ 分类: {element.category.value}".ljust(30) + "║",
        f"║ 周期: {element.period}  族: {element.group if element.group else '镧系/锕系'}".ljust(30) + "║",
        f"║ 电子排布: {element.electron_configuration}".ljust(30) + "║",
        f"║ 常温状态: {element.state.value}".ljust(30) + "║",
    ]
    
    if element.density is not None:
        lines.append(f"║ 密度: {element.density} g/cm³".ljust(30) + "║")
    if element.melting_point is not None:
        lines.append(f"║ 熔点: {element.melting_point} K".ljust(30) + "║")
    if element.boiling_point is not None:
        lines.append(f"║ 沸点: {element.boiling_point} K".ljust(30) + "║")
    if element.discovery_year is not None:
        lines.append(f"║ 发现年份: {element.discovery_year}".ljust(30) + "║")
    if element.discoverer is not None:
        lines.append(f"║ 发现者: {element.discoverer}".ljust(30) + "║")
    
    lines.append("╚══════════════════════════════╝")
    return "\n".join(lines)


def get_periodic_table_text(compact: bool = True) -> str:
    """
    生成文本格式的元素周期表
    
    Args:
        compact: 是否使用紧凑格式
    
    Returns:
        文本格式的周期表
    
    Examples:
        >>> print(get_periodic_table_text())
        H  He                                                  H  He
        Li Be B  C  N  O  F  Ne                          Li Be B  C  N  O  F  Ne
        Na Mg Al Si P  S  Cl Ar                          Na Mg Al Si P  S  Cl Ar
        K  Ca Sc Ti V  Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr
        ...
    """
    if compact:
        # 紧凑格式
        lines = []
        for period in range(1, 8):
            row = []
            for group in range(1, 19):
                elements = [e for e in ELEMENTS.values() 
                           if e.period == period and e.group == group]
                if elements:
                    row.append(elements[0].symbol.ljust(2))
                else:
                    row.append("  ")
            # 处理镧系和锕系
            if period == 6:
                lines.append(" ".join(row[:2] + ["  "] * 10 + row[2:18]))
            elif period == 7:
                lines.append(" ".join(row[:2] + ["  "] * 10 + row[2:18]))
            else:
                lines.append(" ".join(row))
        
        # 添加镧系和锕系
        lanthanides = [e.symbol for e in sorted(
            [e for e in ELEMENTS.values() if e.category == ElementCategory.LANTHANIDE],
            key=lambda x: x.atomic_number)]
        actinides = [e.symbol for e in sorted(
            [e for e in ELEMENTS.values() if e.category == ElementCategory.ACTINIDE],
            key=lambda x: x.atomic_number)]
        
        lines.append("")
        lines.append("  " + " ".join([s.ljust(2) for s in lanthanides]))
        lines.append("  " + " ".join([s.ljust(2) for s in actinides]))
        
        return "\n".join(lines)
    else:
        # 详细格式
        return "详细周期表格式（此处省略，请使用 compact=True）"


def compare_elements(element1: Union[int, str], element2: Union[int, str]) -> Dict:
    """
    比较两个元素的属性
    
    Args:
        element1: 第一个元素（原子序数、符号或名称）
        element2: 第二个元素（原子序数、符号或名称）
    
    Returns:
        包含比较结果的字典
    
    Examples:
        >>> compare_elements('Fe', 'Cu')['原子量差异']
        8.125
    """
    e1 = get_element(element1)
    e2 = get_element(element2)
    
    if e1 is None or e2 is None:
        raise ValueError("无效的元素")
    
    result = {
        "元素1": f"{e1.name} ({e1.symbol})",
        "元素2": f"{e2.name} ({e2.symbol})",
        "原子序数差异": abs(e1.atomic_number - e2.atomic_number),
        "原子量差异": round(abs(e1.atomic_mass - e2.atomic_mass), 3),
        "同周期": e1.period == e2.period,
        "同族": e1.group == e2.group and e1.group != 0,
        "同类": e1.category == e2.category,
    }
    
    if e1.density and e2.density:
        result["密度比"] = round(e1.density / e2.density, 3)
    
    if e1.melting_point and e2.melting_point:
        result["熔点差异(K)"] = abs(e1.melting_point - e2.melting_point)
    
    return result


def get_element_neighbors(element: Union[int, str]) -> Dict[str, Optional[Element]]:
    """
    获取元素在周期表中的相邻元素
    
    Args:
        element: 元素（原子序数、符号或名称）
    
    Returns:
        包含相邻元素的字典
    
    Examples:
        >>> neighbors = get_element_neighbors('C')
        >>> neighbors['left'].symbol
        'B'
        >>> neighbors['right'].symbol
        'N'
    """
    e = get_element(element)
    if e is None:
        raise ValueError("无效的元素")
    
    neighbors = {
        "left": None,
        "right": None,
        "above": None,
        "below": None,
    }
    
    # 左侧元素
    left_elements = [el for el in ELEMENTS.values() 
                    if el.period == e.period and el.group == e.group - 1]
    if left_elements:
        neighbors["left"] = left_elements[0]
    
    # 右侧元素
    right_elements = [el for el in ELEMENTS.values() 
                     if el.period == e.period and el.group == e.group + 1]
    if right_elements:
        neighbors["right"] = right_elements[0]
    
    # 上方元素
    above_elements = [el for el in ELEMENTS.values() 
                     if el.period == e.period - 1 and el.group == e.group]
    if above_elements:
        neighbors["above"] = above_elements[0]
    
    # 下方元素
    below_elements = [el for el in ELEMENTS.values() 
                     if el.period == e.period + 1 and el.group == e.group]
    if below_elements:
        neighbors["below"] = below_elements[0]
    
    return neighbors


def get_common_compounds(element: Union[int, str]) -> List[str]:
    """
    获取元素的常见化合物
    
    Args:
        element: 元素（原子序数、符号或名称）
    
    Returns:
        常见化合物列表
    
    Examples:
        >>> get_common_compounds('Fe')[:3]
        ['Fe2O3', 'Fe3O4', 'FeSO4']
    """
    e = get_element(element)
    if e is None:
        return []
    
    # 常见化合物数据库（简化版）
    common_compounds = {
        "H": ["H2O", "H2", "HCl", "H2SO4", "HNO3", "NH3", "CH4", "H2O2"],
        "C": ["CO2", "CO", "CH4", "C6H12O6", "C2H5OH", "CaCO3", "NaHCO3"],
        "N": ["NH3", "N2", "NO", "NO2", "HNO3", "NH4Cl", "NH4NO3"],
        "O": ["H2O", "O2", "O3", "CO2", "SiO2", "H2O2"],
        "Na": ["NaCl", "NaOH", "Na2CO3", "NaHCO3", "Na2SO4", "NaNO3"],
        "Mg": ["MgO", "MgCl2", "MgSO4", "MgCO3", "Mg(OH)2"],
        "Al": ["Al2O3", "AlCl3", "Al2(SO4)3", "Al(OH)3"],
        "Si": ["SiO2", "SiC", "H2SiO3", "Na2SiO3"],
        "P": ["P2O5", "H3PO4", "Ca3(PO4)2", "Na3PO4"],
        "S": ["SO2", "SO3", "H2S", "H2SO4", "CaSO4"],
        "Cl": ["HCl", "NaCl", "KCl", "Cl2", "CaCl2", "FeCl3"],
        "K": ["KCl", "KOH", "K2CO3", "KNO3", "KMnO4"],
        "Ca": ["CaO", "CaCO3", "CaCl2", "CaSO4", "Ca(OH)2"],
        "Fe": ["Fe2O3", "Fe3O4", "FeSO4", "FeCl3", "Fe(OH)3"],
        "Cu": ["CuO", "Cu2O", "CuSO4", "CuCl2", "Cu(OH)2"],
        "Zn": ["ZnO", "ZnCl2", "ZnSO4", "Zn(OH)2"],
        "Ag": ["AgNO3", "AgCl", "Ag2O", "AgBr"],
        "Au": ["AuCl3", "HAuCl4"],
        "Ba": ["BaSO4", "BaCl2", "Ba(OH)2", "BaCO3"],
    }
    
    return common_compounds.get(e.symbol, [])


if __name__ == "__main__":
    # 示例用法
    print("=" * 50)
    print("化学元素周期表工具 - 示例")
    print("=" * 50)
    
    # 获取元素信息
    print("\n1. 查询元素信息:")
    element = get_element(79)
    print(format_element_info(element))
    
    # 计算分子量
    print("\n2. 计算分子量:")
    formulas = ["H2O", "NaCl", "C6H12O6", "H2SO4"]
    for formula in formulas:
        mass, composition = calculate_molecular_weight(formula)
        print(f"  {formula}: {mass} g/mol, 组成: {composition}")
    
    # 获取周期元素
    print("\n3. 第一周期元素:")
    period1 = get_elements_by_period(1)
    print(f"  {[e.symbol for e in period1]}")
    
    # 获取族元素
    print("\n4. 第一族（碱金属）:")
    group1 = get_elements_by_group(1)
    print(f"  {[e.symbol for e in group1]}")
    
    # 获取分类元素
    print("\n5. 稀有气体:")
    noble_gases = get_elements_by_category(ElementCategory.NOBLE_GAS)
    print(f"  {[e.symbol for e in noble_gases]}")
    
    # 比较元素
    print("\n6. 比较元素 (Fe vs Cu):")
    comparison = compare_elements("Fe", "Cu")
    for key, value in comparison.items():
        print(f"  {key}: {value}")
    
    # 获取相邻元素
    print("\n7. 碳的相邻元素:")
    neighbors = get_element_neighbors("C")
    for direction, elem in neighbors.items():
        if elem:
            print(f"  {direction}: {elem.name} ({elem.symbol})")
    
    # 获取常见化合物
    print("\n8. 铁的常见化合物:")
    compounds = get_common_compounds("Fe")
    print(f"  {compounds}")