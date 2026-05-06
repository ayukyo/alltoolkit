"""
Chemical Formula Utils - 化学公式解析和处理工具

功能:
- 解析化学式，提取元素及其原子数
- 计算分子量
- 验证化学式格式
- 格式化化学式输出
- 计算元素质量百分比
- 支持带括号的复杂化学式
- 支持水合物表示法 (如 CuSO4·5H2O)

零外部依赖，纯Python实现
"""

import re
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from functools import lru_cache


# 元素周期表数据 (符号: (原子序数, 相对原子质量))
ELEMENTS_DATA = {
    'H': (1, 1.00794), 'He': (2, 4.002602), 'Li': (3, 6.941), 'Be': (4, 9.012182),
    'B': (5, 10.811), 'C': (6, 12.0107), 'N': (7, 14.0067), 'O': (8, 15.9994),
    'F': (9, 18.9984032), 'Ne': (10, 20.1797), 'Na': (11, 22.98976928),
    'Mg': (12, 24.305), 'Al': (13, 26.9815386), 'Si': (14, 28.0855), 'P': (15, 30.973762),
    'S': (16, 32.065), 'Cl': (17, 35.453), 'Ar': (18, 39.948), 'K': (19, 39.0983),
    'Ca': (20, 40.078), 'Sc': (21, 44.955912), 'Ti': (22, 47.867), 'V': (23, 50.9415),
    'Cr': (24, 51.9961), 'Mn': (25, 54.938045), 'Fe': (26, 55.845), 'Co': (27, 58.933195),
    'Ni': (28, 58.6934), 'Cu': (29, 63.546), 'Zn': (30, 65.38), 'Ga': (31, 69.723),
    'Ge': (32, 72.63), 'As': (33, 74.9216), 'Se': (34, 78.96), 'Br': (35, 79.904),
    'Kr': (36, 83.798), 'Rb': (37, 85.4678), 'Sr': (38, 87.62), 'Y': (39, 88.90585),
    'Zr': (40, 91.224), 'Nb': (41, 92.90638), 'Mo': (42, 95.96), 'Tc': (43, 98),
    'Ru': (44, 101.07), 'Rh': (45, 102.9055), 'Pd': (46, 106.42), 'Ag': (47, 107.8682),
    'Cd': (48, 112.411), 'In': (49, 114.818), 'Sn': (50, 118.71), 'Sb': (51, 121.76),
    'Te': (52, 127.6), 'I': (53, 126.90447), 'Xe': (54, 131.293), 'Cs': (55, 132.9054519),
    'Ba': (56, 137.327), 'La': (57, 138.90547), 'Ce': (58, 140.116), 'Pr': (59, 140.90765),
    'Nd': (60, 144.242), 'Pm': (61, 145), 'Sm': (62, 150.36), 'Eu': (63, 151.964),
    'Gd': (64, 157.25), 'Tb': (65, 158.92535), 'Dy': (66, 162.5), 'Ho': (67, 164.93032),
    'Er': (68, 167.259), 'Tm': (69, 168.93421), 'Yb': (70, 173.054), 'Lu': (71, 174.9668),
    'Hf': (72, 178.49), 'Ta': (73, 180.94788), 'W': (74, 183.84), 'Re': (75, 186.207),
    'Os': (76, 190.23), 'Ir': (77, 192.217), 'Pt': (78, 195.084), 'Au': (79, 196.966569),
    'Hg': (80, 200.59), 'Tl': (81, 204.3833), 'Pb': (82, 207.2), 'Bi': (83, 208.9804),
    'Po': (84, 209), 'At': (85, 210), 'Rn': (86, 222), 'Fr': (87, 223), 'Ra': (88, 226),
    'Ac': (89, 227), 'Th': (90, 232.03806), 'Pa': (91, 231.03588), 'U': (92, 238.02891),
    'Np': (93, 237), 'Pu': (94, 244), 'Am': (95, 243), 'Cm': (96, 247),
    'Bk': (97, 247), 'Cf': (98, 251), 'Es': (99, 252), 'Fm': (100, 257),
    'Md': (101, 258), 'No': (102, 259), 'Lr': (103, 262), 'Rf': (104, 267),
    'Db': (105, 268), 'Sg': (106, 271), 'Bh': (107, 272), 'Hs': (108, 270),
    'Mt': (109, 276), 'Ds': (110, 281), 'Rg': (111, 280), 'Cn': (112, 285),
    'Nh': (113, 284), 'Fl': (114, 289), 'Mc': (115, 288), 'Lv': (116, 293),
    'Ts': (117, 294), 'Og': (118, 294)
}


@dataclass
class Element:
    """元素信息"""
    symbol: str
    atomic_number: int
    atomic_mass: float
    count: int = 1


@dataclass
class ParsedFormula:
    """解析后的化学式结果"""
    original: str
    elements: Dict[str, int]  # 元素符号 -> 原子数
    is_valid: bool
    error_message: Optional[str] = None
    
    def __repr__(self):
        if not self.is_valid:
            return f"ParsedFormula(invalid, error={self.error_message})"
        return f"ParsedFormula({self.original} -> {self.elements})"


class ChemicalFormulaParser:
    """化学式解析器"""
    
    # 元素符号正则: 大写字母 + 可选小写字母
    ELEMENT_PATTERN = re.compile(r'([A-Z][a-z]?)(\d*)')
    # 括号内容匹配
    GROUP_PATTERN = re.compile(r'\(([^()]*)\)(\d*)')
    # 方括号内容匹配 (配合物等)
    BRACKET_PATTERN = re.compile(r'\[([^\[\]]*)\](\d*)')
    # 水合物匹配 · 或 .
    HYDRATE_PATTERN = re.compile(r'[·•x](\d*)')
    # 电荷标记
    CHARGE_PATTERN = re.compile(r'[\^]?\d*[+-]$')
    
    def __init__(self):
        self.elements_data = ELEMENTS_DATA
    
    def parse(self, formula: str) -> ParsedFormula:
        """
        解析化学式，返回元素组成
        
        Args:
            formula: 化学式字符串，如 "H2O", "NaCl", "Ca(OH)2"
            
        Returns:
            ParsedFormula 对象
        """
        if not formula or not isinstance(formula, str):
            return ParsedFormula(
                original=formula or '',
                elements={},
                is_valid=False,
                error_message="公式不能为空"
            )
        
        # 去除空格和电荷标记
        clean_formula = formula.strip()
        clean_formula = self.CHARGE_PATTERN.sub('', clean_formula)
        
        # 处理水合物
        hydrate_parts = self._split_hydrate(clean_formula)
        
        all_elements = {}
        multiplier = 1
        
        for part in hydrate_parts:
            if ':' in part:
                # 格式: formula:count (水合物)
                base, count = part.rsplit(':', 1)
                try:
                    multiplier = int(count) if count else 1
                except ValueError:
                    multiplier = 1
                part = base
            
            # 处理方括号 (配合物)
            part, bracket_elements = self._process_brackets(part)
            if bracket_elements is None:
                return ParsedFormula(
                    original=formula,
                    elements={},
                    is_valid=False,
                    error_message="括号不匹配或格式错误"
                )
            
            # 处理圆括号
            part, paren_elements = self._process_parentheses(part)
            if paren_elements is None:
                return ParsedFormula(
                    original=formula,
                    elements={},
                    is_valid=False,
                    error_message="括号不匹配或格式错误"
                )
            
            # 解析剩余的简单元素
            simple_elements = self._parse_simple(part)
            if simple_elements is None:
                return ParsedFormula(
                    original=formula,
                    elements={},
                    is_valid=False,
                    error_message="无效的元素符号"
                )
            
            # 合并所有元素
            for elem_dict in [simple_elements, paren_elements, bracket_elements]:
                for elem, count in elem_dict.items():
                    if elem not in all_elements:
                        all_elements[elem] = 0
                    all_elements[elem] += count * multiplier
        
        # 验证所有元素
        for elem in all_elements:
            if elem not in self.elements_data:
                return ParsedFormula(
                    original=formula,
                    elements={},
                    is_valid=False,
                    error_message=f"未知元素: {elem}"
                )
        
        return ParsedFormula(
            original=formula,
            elements=all_elements,
            is_valid=True
        )
    
    def _split_hydrate(self, formula: str) -> List[str]:
        """分割水合物部分"""
        # 支持 · x · 等水合物表示
        parts = re.split(r'[·•x]', formula)
        result = []
        
        for i, part in enumerate(parts):
            if i > 0:
                # 检查是否有数字前缀 (如 5H2O)
                match = re.match(r'^(\d+)?(.+)$', part)
                if match:
                    count = match.group(1) or '1'
                    rest = match.group(2)
                    result.append(f"{rest}:{count}")
                else:
                    result.append(part)
            else:
                result.append(part)
        
        return result
    
    def _process_brackets(self, formula: str) -> Tuple[str, Dict[str, int]]:
        """处理方括号"""
        elements = {}
        
        while True:
            match = self.BRACKET_PATTERN.search(formula)
            if not match:
                break
            
            content = match.group(1)
            multiplier = int(match.group(2)) if match.group(2) else 1
            
            # 处理方括号内的圆括号
            inner_content, inner_paren_elements = self._process_parentheses(content)
            if inner_paren_elements is None:
                return formula, None
            
            inner_simple_elements = self._parse_simple(inner_content)
            if inner_simple_elements is None:
                return formula, None
            
            # 合并方括号内的所有元素
            for elem_dict in [inner_simple_elements, inner_paren_elements]:
                for elem, count in elem_dict.items():
                    elements[elem] = elements.get(elem, 0) + count * multiplier
            
            formula = formula[:match.start()] + formula[match.end():]
        
        return formula, elements
    
    def _process_parentheses(self, formula: str) -> Tuple[str, Dict[str, int]]:
        """处理圆括号"""
        elements = {}
        
        while True:
            match = self.GROUP_PATTERN.search(formula)
            if not match:
                break
            
            content = match.group(1)
            multiplier = int(match.group(2)) if match.group(2) else 1
            
            inner_elements = self._parse_simple(content)
            if inner_elements is None:
                return formula, None
            
            for elem, count in inner_elements.items():
                elements[elem] = elements.get(elem, 0) + count * multiplier
            
            formula = formula[:match.start()] + formula[match.end():]
        
        return formula, elements
    
    def _parse_simple(self, formula: str) -> Optional[Dict[str, int]]:
        """解析简单化学式 (无括号)"""
        elements = {}
        pos = 0
        
        while pos < len(formula):
            match = self.ELEMENT_PATTERN.match(formula, pos)
            if not match:
                # 检查是否还有未匹配的字符
                if pos < len(formula) and formula[pos] not in '()[]·•x':
                    return None
                break
            
            symbol = match.group(1)
            count_str = match.group(2)
            count = int(count_str) if count_str else 1
            
            if symbol not in self.elements_data:
                return None
            
            elements[symbol] = elements.get(symbol, 0) + count
            pos = match.end()
        
        return elements


class ChemicalFormulaUtils:
    """化学式工具类"""
    
    def __init__(self):
        self.parser = ChemicalFormulaParser()
        self.elements_data = ELEMENTS_DATA
    
    def parse(self, formula: str) -> ParsedFormula:
        """解析化学式"""
        return self.parser.parse(formula)
    
    def get_elements(self, formula: str) -> Dict[str, int]:
        """
        获取化学式中的所有元素及其原子数
        
        Args:
            formula: 化学式
            
        Returns:
            字典 {元素符号: 原子数}
        """
        result = self.parse(formula)
        return result.elements if result.is_valid else {}
    
    def get_element_count(self, formula: str, element: str) -> int:
        """
        获取化学式中指定元素的原子数
        
        Args:
            formula: 化学式
            element: 元素符号
            
        Returns:
            原子数，如果元素不存在返回0
        """
        elements = self.get_elements(formula)
        return elements.get(element, 0)
    
    def calculate_molar_mass(self, formula: str) -> float:
        """
        计算摩尔质量 (分子量)
        
        Args:
            formula: 化学式
            
        Returns:
            摩尔质量 (g/mol)，如果公式无效返回0
        """
        elements = self.get_elements(formula)
        if not elements:
            return 0.0
        
        total_mass = 0.0
        for symbol, count in elements.items():
            if symbol in self.elements_data:
                total_mass += self.elements_data[symbol][1] * count
        
        return round(total_mass, 4)
    
    def calculate_mass_percentages(self, formula: str) -> Dict[str, float]:
        """
        计算各元素的质量百分比
        
        Args:
            formula: 化学式
            
        Returns:
            字典 {元素符号: 质量百分比}
        """
        elements = self.get_elements(formula)
        if not elements:
            return {}
        
        total_mass = self.calculate_molar_mass(formula)
        if total_mass == 0:
            return {}
        
        percentages = {}
        for symbol, count in elements.items():
            if symbol in self.elements_data:
                element_mass = self.elements_data[symbol][1] * count
                percentages[symbol] = round((element_mass / total_mass) * 100, 4)
        
        return percentages
    
    def get_element_info(self, symbol: str) -> Optional[Element]:
        """
        获取元素信息
        
        Args:
            symbol: 元素符号
            
        Returns:
            Element 对象，如果元素不存在返回 None
        """
        symbol = symbol.capitalize()
        if symbol in self.elements_data:
            data = self.elements_data[symbol]
            return Element(
                symbol=symbol,
                atomic_number=data[0],
                atomic_mass=data[1]
            )
        return None
    
    def is_valid_formula(self, formula: str) -> bool:
        """
        验证化学式是否有效
        
        Args:
            formula: 化学式
            
        Returns:
            是否有效
        """
        return self.parse(formula).is_valid
    
    def format_formula(self, formula: str, use_subscripts: bool = True) -> str:
        """
        格式化化学式，将数字转换为下标
        
        Args:
            formula: 化学式
            use_subscripts: 是否使用Unicode下标
            
        Returns:
            格式化后的化学式
        """
        subscripts = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')
        
        if use_subscripts:
            result = re.sub(r'(\d+)', lambda m: m.group(1).translate(subscripts), formula)
        else:
            result = formula
        
        return result
    
    def get_empirical_formula(self, formula: str) -> str:
        """
        获取最简式 (实验式)
        
        Args:
            formula: 化学式
            
        Returns:
            最简式
        """
        elements = self.get_elements(formula)
        if not elements:
            return ""
        
        # 找到所有原子数的最大公约数
        counts = list(elements.values())
        gcd = self._gcd_list(counts)
        
        # 除以公约数得到最简比
        empirical = {}
        for symbol, count in sorted(elements.items()):
            empirical[symbol] = count // gcd
        
        return self._dict_to_formula(empirical)
    
    def _gcd(self, a: int, b: int) -> int:
        """计算最大公约数"""
        while b:
            a, b = b, a % b
        return a
    
    def _gcd_list(self, numbers: List[int]) -> int:
        """计算列表中所有数的最大公约数"""
        result = numbers[0]
        for num in numbers[1:]:
            result = self._gcd(result, num)
        return result
    
    def _dict_to_formula(self, elements: Dict[str, int]) -> str:
        """将元素字典转换为化学式字符串"""
        # 按照惯例排序: C, H, 然后其他元素按字母顺序
        order = ['C', 'H']
        sorted_elements = []
        
        for elem in order:
            if elem in elements:
                count = elements[elem]
                sorted_elements.append((elem, count))
        
        other_elements = [(k, v) for k, v in elements.items() if k not in order]
        other_elements.sort(key=lambda x: x[0])
        sorted_elements.extend(other_elements)
        
        formula = ""
        for symbol, count in sorted_elements:
            formula += symbol
            if count > 1:
                formula += str(count)
        
        return formula
    
    def compare_formulas(self, formula1: str, formula2: str) -> Dict[str, any]:
        """
        比较两个化学式
        
        Args:
            formula1: 第一个化学式
            formula2: 第二个化学式
            
        Returns:
            比较结果字典
        """
        elements1 = self.get_elements(formula1)
        elements2 = self.get_elements(formula2)
        
        all_elements = set(elements1.keys()) | set(elements2.keys())
        
        differences = {}
        for elem in all_elements:
            count1 = elements1.get(elem, 0)
            count2 = elements2.get(elem, 0)
            if count1 != count2:
                differences[elem] = {'formula1': count1, 'formula2': count2}
        
        return {
            'are_equal': not differences,
            'formula1_elements': elements1,
            'formula2_elements': elements2,
            'differences': differences,
            'unique_to_formula1': set(elements1.keys()) - set(elements2.keys()),
            'unique_to_formula2': set(elements2.keys()) - set(elements1.keys())
        }
    
    def find_elements_by_mass_range(self, min_mass: float, max_mass: float) -> List[Element]:
        """
        查找原子质量在指定范围内的元素
        
        Args:
            min_mass: 最小原子质量
            max_mass: 最大原子质量
            
        Returns:
            符合条件的元素列表
        """
        result = []
        for symbol, (atomic_num, atomic_mass) in self.elements_data.items():
            if min_mass <= atomic_mass <= max_mass:
                result.append(Element(
                    symbol=symbol,
                    atomic_number=atomic_num,
                    atomic_mass=atomic_mass
                ))
        
        return sorted(result, key=lambda x: x.atomic_mass)
    
    def get_compound_type(self, formula: str) -> str:
        """
        推断化合物类型
        
        Args:
            formula: 化学式
            
        Returns:
            化合物类型描述
        """
        elements = self.get_elements(formula)
        if not elements:
            return "未知"
        
        elem_set = set(elements.keys())
        
        # 简单元素
        if len(elem_set) == 1:
            elem = list(elem_set)[0]
            if elem in ['He', 'Ne', 'Ar', 'Kr', 'Xe', 'Rn']:
                return "稀有气体"
            elif elem in ['H', 'N', 'O', 'F', 'Cl', 'Br', 'I']:
                return "非金属单质"
            else:
                return "金属单质"
        
        # 氧化物
        if 'O' in elem_set and len(elem_set) == 2:
            other = (elem_set - {'O'}).pop()
            if other in ['H']:
                return "水"
            elif other in ['Na', 'K', 'Ca', 'Mg', 'Ba']:
                return "碱性氧化物"
            elif other in ['C', 'S', 'N', 'P']:
                return "酸性氧化物"
            else:
                return "氧化物"
        
        # 有机物简单判断 (优先于酸判断)
        if 'C' in elem_set and 'H' in elem_set:
            if 'O' in elem_set:
                if elements.get('C', 0) == 6 and elements.get('H', 0) == 12 and elements.get('O', 0) == 6:
                    return "糖类"
                elif elements.get('O', 0) == 2 and len(elem_set) == 3:
                    return "羧酸"
                else:
                    return "含氧有机物"
            return "有机物"
        
        # 酸
        if 'H' in elem_set and len(elem_set) <= 3:
            if 'O' in elem_set:
                return "含氧酸"
            else:
                return "无氧酸"
        
        # 碱
        if 'O' in elem_set and 'H' in elem_set:
            metals = {'Li', 'Na', 'K', 'Rb', 'Cs', 'Ca', 'Mg', 'Ba', 'Sr'}
            if elem_set - {'O', 'H'} & metals:
                return "碱"
        
        # 盐
        if len(elem_set) >= 2:
            metals = {'Li', 'Na', 'K', 'Rb', 'Cs', 'Ca', 'Mg', 'Ba', 'Sr', 
                     'Fe', 'Cu', 'Zn', 'Al', 'Ag', 'Pb', 'Hg', 'Sn'}
            nonmetals = {'Cl', 'Br', 'I', 'F', 'S', 'N', 'P', 'C'}
            
            has_metal = bool(elem_set & metals)
            has_nonmetal = bool(elem_set & nonmetals)
            
            if has_metal and 'O' in elem_set:
                return "含氧酸盐"
            elif has_metal and has_nonmetal:
                return "无氧酸盐"
        
        return "化合物"
    
    def balance_equation_hint(self, reactants: str, products: str) -> Dict[str, any]:
        """
        分析化学方程式配平
        
        Args:
            reactants: 反应物字符串 (如 "H2 + O2")
            products: 生成物字符串 (如 "H2O")
            
        Returns:
            配平提示和分析结果
        """
        # 解析反应物
        reactant_list = [r.strip() for r in reactants.split('+')]
        product_list = [p.strip() for p in products.split('+')]
        
        # 收集所有元素
        reactant_elements = {}
        product_elements = {}
        
        for r in reactant_list:
            elem = self.get_elements(r)
            for k, v in elem.items():
                reactant_elements[k] = reactant_elements.get(k, 0) + v
        
        for p in product_list:
            elem = self.get_elements(p)
            for k, v in elem.items():
                product_elements[k] = product_elements.get(k, 0) + v
        
        # 检查元素守恒
        all_elements = set(reactant_elements.keys()) | set(product_elements.keys())
        unbalanced = []
        
        for elem in all_elements:
            r_count = reactant_elements.get(elem, 0)
            p_count = product_elements.get(elem, 0)
            if r_count != p_count:
                unbalanced.append({
                    'element': elem,
                    'reactants': r_count,
                    'products': p_count
                })
        
        return {
            'reactants': reactant_list,
            'products': product_list,
            'reactant_elements': reactant_elements,
            'product_elements': product_elements,
            'is_balanced': not unbalanced,
            'unbalanced_elements': unbalanced
        }


# 创建默认实例
chemical_formula = ChemicalFormulaUtils()


# 便捷函数
def parse(formula: str) -> ParsedFormula:
    """解析化学式"""
    return chemical_formula.parse(formula)


def get_elements(formula: str) -> Dict[str, int]:
    """获取化学式中的元素组成"""
    return chemical_formula.get_elements(formula)


def molar_mass(formula: str) -> float:
    """计算摩尔质量"""
    return chemical_formula.calculate_molar_mass(formula)


def mass_percentages(formula: str) -> Dict[str, float]:
    """计算质量百分比"""
    return chemical_formula.calculate_mass_percentages(formula)


def is_valid(formula: str) -> bool:
    """验证化学式"""
    return chemical_formula.is_valid_formula(formula)


def format_formula(formula: str, use_subscripts: bool = True) -> str:
    """格式化化学式"""
    return chemical_formula.format_formula(formula, use_subscripts)


def empirical_formula(formula: str) -> str:
    """获取最简式"""
    return chemical_formula.get_empirical_formula(formula)


if __name__ == "__main__":
    # 简单测试
    utils = ChemicalFormulaUtils()
    
    test_formulas = [
        "H2O",
        "NaCl",
        "Ca(OH)2",
        "C6H12O6",
        "H2SO4",
        "CuSO4·5H2O",
        "CH3COOH",
        "K4[Fe(CN)6]"
    ]
    
    print("=== 化学式解析测试 ===\n")
    for formula in test_formulas:
        print(f"化学式: {formula}")
        result = utils.parse(formula)
        if result.is_valid:
            print(f"  元素: {result.elements}")
            print(f"  摩尔质量: {utils.calculate_molar_mass(formula)} g/mol")
            print(f"  质量百分比: {utils.calculate_mass_percentages(formula)}")
            print(f"  化合物类型: {utils.get_compound_type(formula)}")
        else:
            print(f"  错误: {result.error_message}")
        print()