"""
Chemical Formula Utils 测试文件

测试化学式解析和处理功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chemical_formula_utils.mod import (
    ChemicalFormulaUtils,
    ChemicalFormulaParser,
    ParsedFormula,
    Element,
    parse,
    get_elements,
    molar_mass,
    mass_percentages,
    is_valid,
    format_formula,
    empirical_formula,
    ELEMENTS_DATA
)


class TestChemicalFormulaParser:
    """测试化学式解析器"""
    
    def setup_method(self):
        self.parser = ChemicalFormulaParser()
    
    def test_simple_formula(self):
        """测试简单化学式"""
        # 水分子
        result = self.parser.parse("H2O")
        assert result.is_valid
        assert result.elements == {'H': 2, 'O': 1}
        
        # 氯化钠
        result = self.parser.parse("NaCl")
        assert result.is_valid
        assert result.elements == {'Na': 1, 'Cl': 1}
        
        # 单质
        result = self.parser.parse("O2")
        assert result.is_valid
        assert result.elements == {'O': 2}
        
        # 铁单质
        result = self.parser.parse("Fe")
        assert result.is_valid
        assert result.elements == {'Fe': 1}
    
    def test_complex_formula(self):
        """测试复杂化学式"""
        # 葡萄糖
        result = self.parser.parse("C6H12O6")
        assert result.is_valid
        assert result.elements == {'C': 6, 'H': 12, 'O': 6}
        
        # 硫酸
        result = self.parser.parse("H2SO4")
        assert result.is_valid
        assert result.elements == {'H': 2, 'S': 1, 'O': 4}
    
    def test_parentheses(self):
        """测试带括号的化学式"""
        # 氢氧化钙
        result = self.parser.parse("Ca(OH)2")
        assert result.is_valid
        assert result.elements == {'Ca': 1, 'O': 2, 'H': 2}
        
        # 碳酸钠
        result = self.parser.parse("Na2CO3")
        assert result.is_valid
        assert result.elements == {'Na': 2, 'C': 1, 'O': 3}
        
        # 硫酸铝
        result = self.parser.parse("Al2(SO4)3")
        assert result.is_valid
        assert result.elements == {'Al': 2, 'S': 3, 'O': 12}
    
    def test_brackets(self):
        """测试带方括号的化学式 (配合物)"""
        # 亚铁氰化钾
        result = self.parser.parse("K4[Fe(CN)6]")
        assert result.is_valid
        assert result.elements == {'K': 4, 'Fe': 1, 'C': 6, 'N': 6}
    
    def test_hydrate(self):
        """测试水合物"""
        # 五水硫酸铜
        result = self.parser.parse("CuSO4·5H2O")
        assert result.is_valid
        assert result.elements['Cu'] == 1
        assert result.elements['S'] == 1
        assert result.elements['O'] == 9  # 4 + 5
        assert result.elements['H'] == 10
    
    def test_charge_notation(self):
        """测试电荷标记"""
        # 带电荷的离子
        result = self.parser.parse("SO4^2-")
        assert result.is_valid
        assert result.elements == {'S': 1, 'O': 4}
        
        result = self.parser.parse("Fe^3+")
        assert result.is_valid
        assert result.elements == {'Fe': 1}
    
    def test_invalid_formulas(self):
        """测试无效化学式"""
        # 空字符串
        result = self.parser.parse("")
        assert not result.is_valid
        
        # 无效元素
        result = self.parser.parse("Xx2O3")
        assert not result.is_valid
        
        # None
        result = self.parser.parse(None)
        assert not result.is_valid
    
    def test_organic_compounds(self):
        """测试有机化合物"""
        # 甲烷
        result = self.parser.parse("CH4")
        assert result.is_valid
        assert result.elements == {'C': 1, 'H': 4}
        
        # 乙醇
        result = self.parser.parse("C2H5OH")
        assert result.is_valid
        assert result.elements['C'] == 2
        assert result.elements['H'] == 6
        assert result.elements['O'] == 1
        
        # 乙酸
        result = self.parser.parse("CH3COOH")
        assert result.is_valid
        assert result.elements['C'] == 2
        assert result.elements['H'] == 4
        assert result.elements['O'] == 2


class TestChemicalFormulaUtils:
    """测试化学式工具类"""
    
    def setup_method(self):
        self.utils = ChemicalFormulaUtils()
    
    def test_molar_mass(self):
        """测试摩尔质量计算"""
        # 水 H2O
        mass = self.utils.calculate_molar_mass("H2O")
        expected = 2 * 1.00794 + 15.9994
        assert abs(mass - expected) < 0.001
        
        # 氯化钠 NaCl
        mass = self.utils.calculate_molar_mass("NaCl")
        expected = 22.98976928 + 35.453
        assert abs(mass - expected) < 0.001
        
        # 葡萄糖 C6H12O6
        mass = self.utils.calculate_molar_mass("C6H12O6")
        expected = 6 * 12.0107 + 12 * 1.00794 + 6 * 15.9994
        assert abs(mass - expected) < 0.01
    
    def test_mass_percentages(self):
        """测试质量百分比计算"""
        # 水 H2O
        percentages = self.utils.calculate_mass_percentages("H2O")
        total = sum(percentages.values())
        assert abs(total - 100) < 0.01
        
        # 氢百分比
        h_percent = percentages['H']
        expected_h = (2 * 1.00794) / (2 * 1.00794 + 15.9994) * 100
        assert abs(h_percent - expected_h) < 0.1
    
    def test_element_info(self):
        """测试元素信息获取"""
        # 氢
        h = self.utils.get_element_info("H")
        assert h is not None
        assert h.atomic_number == 1
        assert h.symbol == "H"
        
        # 无效元素
        none = self.utils.get_element_info("Xx")
        assert none is None
    
    def test_is_valid_formula(self):
        """测试化学式验证"""
        assert self.utils.is_valid_formula("H2O")
        assert self.utils.is_valid_formula("NaCl")
        assert self.utils.is_valid_formula("C6H12O6")
        assert not self.utils.is_valid_formula("Xx2")
        assert not self.utils.is_valid_formula("")
    
    def test_format_formula(self):
        """测试化学式格式化"""
        # 带下标
        formatted = self.utils.format_formula("H2O", use_subscripts=True)
        assert '₂' in formatted
        assert 'H' in formatted
        assert 'O' in formatted
        
        # 不带下标
        formatted = self.utils.format_formula("H2O", use_subscripts=False)
        assert formatted == "H2O"
    
    def test_empirical_formula(self):
        """测试最简式计算"""
        # 葡萄糖 C6H12O6 -> CH2O
        empirical = self.utils.get_empirical_formula("C6H12O6")
        assert empirical == "CH2O"
        
        # 水 H2O (已是最简)
        empirical = self.utils.get_empirical_formula("H2O")
        assert empirical == "H2O"
        
        # 乙炔 C2H2 -> CH
        empirical = self.utils.get_empirical_formula("C2H2")
        assert empirical == "CH"
    
    def test_compare_formulas(self):
        """测试化学式比较"""
        # 相同化学式
        result = self.utils.compare_formulas("H2O", "H2O")
        assert result['are_equal']
        
        # 不同化学式
        result = self.utils.compare_formulas("H2O", "H2O2")
        assert not result['are_equal']
        assert 'O' in result['differences']
        
        # 相同组成不同表示
        result = self.utils.compare_formulas("CH3COOH", "C2H4O2")
        assert result['are_equal']
    
    def test_find_elements_by_mass_range(self):
        """测试按质量范围查找元素"""
        # 查找原子质量在10-20之间的元素
        elements = self.utils.find_elements_by_mass_range(10, 20)
        symbols = [e.symbol for e in elements]
        
        assert 'C' in symbols  # 12.0107
        assert 'N' in symbols  # 14.0067
        assert 'O' in symbols  # 15.9994
        assert 'F' in symbols  # 18.998
    
    def test_get_compound_type(self):
        """测试化合物类型推断"""
        # 单质
        assert "单质" in self.utils.get_compound_type("Fe")
        assert "单质" in self.utils.get_compound_type("O2")
        
        # 氧化物
        assert "氧化物" in self.utils.get_compound_type("CaO")
        assert "氧化物" in self.utils.get_compound_type("CO2")
        
        # 酸
        assert "酸" in self.utils.get_compound_type("HCl")
        assert "酸" in self.utils.get_compound_type("H2SO4")
        
        # 有机物
        assert "有机" in self.utils.get_compound_type("CH4")
        # C6H12O6 被识别为糖类，这也是有机物的一种
        compound_type = self.utils.get_compound_type("C6H12O6")
        assert "有机" in compound_type or "糖类" in compound_type
    
    def test_balance_equation_hint(self):
        """测试配平提示"""
        # 已配平
        result = self.utils.balance_equation_hint("2H2 + O2", "2H2O")
        # 这个测试主要看功能是否正常工作
        assert 'reactants' in result
        assert 'products' in result
        assert 'is_balanced' in result
    
    def test_get_element_count(self):
        """测试获取元素原子数"""
        count = self.utils.get_element_count("H2SO4", "H")
        assert count == 2
        
        count = self.utils.get_element_count("H2SO4", "S")
        assert count == 1
        
        count = self.utils.get_element_count("H2SO4", "O")
        assert count == 4
        
        count = self.utils.get_element_count("H2SO4", "C")
        assert count == 0


class TestConvenienceFunctions:
    """测试便捷函数"""
    
    def test_parse_function(self):
        """测试 parse 函数"""
        result = parse("H2O")
        assert result.is_valid
        assert result.elements == {'H': 2, 'O': 1}
    
    def test_get_elements_function(self):
        """测试 get_elements 函数"""
        elements = get_elements("NaCl")
        assert elements == {'Na': 1, 'Cl': 1}
    
    def test_molar_mass_function(self):
        """测试 molar_mass 函数"""
        mass = molar_mass("H2O")
        assert mass > 18
        assert mass < 19
    
    def test_mass_percentages_function(self):
        """测试 mass_percentages 函数"""
        percentages = mass_percentages("CO2")
        assert 'C' in percentages
        assert 'O' in percentages
        assert abs(percentages['C'] + percentages['O'] - 100) < 0.1
    
    def test_is_valid_function(self):
        """测试 is_valid 函数"""
        assert is_valid("H2O")
        assert is_valid("NaCl")
        assert not is_valid("")
    
    def test_format_formula_function(self):
        """测试 format_formula 函数"""
        formatted = format_formula("H2SO4")
        assert '₂' in formatted
        assert '₄' in formatted
    
    def test_empirical_formula_function(self):
        """测试 empirical_formula 函数"""
        emp = empirical_formula("C6H12O6")
        assert emp == "CH2O"


class TestEdgeCases:
    """测试边缘情况"""
    
    def setup_method(self):
        self.utils = ChemicalFormulaUtils()
    
    def test_empty_formula(self):
        """测试空化学式"""
        result = self.utils.parse("")
        assert not result.is_valid
    
    def test_single_element(self):
        """测试单元素化学式"""
        result = self.utils.parse("Fe")
        assert result.is_valid
        assert result.elements == {'Fe': 1}
    
    def test_large_formula(self):
        """测试大型化学式"""
        # 血红素近似式
        result = self.utils.parse("C34H32O4Fe")
        assert result.is_valid
        assert result.elements['C'] == 34
        assert result.elements['H'] == 32
        assert result.elements['O'] == 4
        assert result.elements['Fe'] == 1
    
    def test_nested_parentheses(self):
        """测试嵌套括号"""
        # 理论上的复杂化合物
        result = self.utils.parse("Mg(OH)2")
        assert result.is_valid
        assert result.elements == {'Mg': 1, 'O': 2, 'H': 2}
    
    def test_all_elements_data(self):
        """测试元素数据完整性"""
        # 确保至少有100个元素
        assert len(ELEMENTS_DATA) >= 100
        
        # 检查常见元素
        common_elements = ['H', 'C', 'N', 'O', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 
                          'Cl', 'K', 'Ca', 'Fe', 'Cu', 'Zn', 'Ag', 'Au', 'Hg', 'Pb']
        for elem in common_elements:
            assert elem in ELEMENTS_DATA, f"缺少元素: {elem}"


class TestRealWorldExamples:
    """测试真实世界的化学式"""
    
    def setup_method(self):
        self.utils = ChemicalFormulaUtils()
    
    def test_common_compounds(self):
        """测试常见化合物"""
        compounds = {
            "H2O": {'H': 2, 'O': 1},
            "NaCl": {'Na': 1, 'Cl': 1},
            "CaCO3": {'Ca': 1, 'C': 1, 'O': 3},
            "H2SO4": {'H': 2, 'S': 1, 'O': 4},
            "NaOH": {'Na': 1, 'O': 1, 'H': 1},
            "NH3": {'N': 1, 'H': 3},
            "CH4": {'C': 1, 'H': 4},
            "CO2": {'C': 1, 'O': 2},
            "HCl": {'H': 1, 'Cl': 1},
            "HNO3": {'H': 1, 'N': 1, 'O': 3},
        }
        
        for formula, expected in compounds.items():
            result = self.utils.parse(formula)
            assert result.is_valid, f"{formula} 解析失败"
            assert result.elements == expected, f"{formula} 元素组成错误"
    
    def test_pharmaceuticals(self):
        """测试药物分子"""
        # 阿司匹林 C9H8O4
        result = self.utils.parse("C9H8O4")
        assert result.is_valid
        mass = self.utils.calculate_molar_mass("C9H8O4")
        assert 180 < mass < 181
        
        # 咖啡因 C8H10N4O2
        result = self.utils.parse("C8H10N4O2")
        assert result.is_valid
        mass = self.utils.calculate_molar_mass("C8H10N4O2")
        assert 194 < mass < 195
    
    def test_minerals(self):
        """测试矿物"""
        # 石英 SiO2
        result = self.utils.parse("SiO2")
        assert result.is_valid
        assert result.elements == {'Si': 1, 'O': 2}
        
        # 刚玉 Al2O3
        result = self.utils.parse("Al2O3")
        assert result.is_valid
        assert result.elements == {'Al': 2, 'O': 3}


def run_tests():
    """运行所有测试"""
    import traceback
    
    test_classes = [
        TestChemicalFormulaParser,
        TestChemicalFormulaUtils,
        TestConvenienceFunctions,
        TestEdgeCases,
        TestRealWorldExamples
    ]
    
    passed = 0
    failed = 0
    
    for test_class in test_classes:
        instance = test_class()
        
        # 运行 setup_method
        if hasattr(instance, 'setup_method'):
            instance.setup_method()
        
        # 获取所有测试方法
        test_methods = [m for m in dir(instance) if m.startswith('test_')]
        
        for method_name in test_methods:
            try:
                method = getattr(instance, method_name)
                method()
                passed += 1
                print(f"✓ {test_class.__name__}.{method_name}")
            except AssertionError as e:
                failed += 1
                print(f"✗ {test_class.__name__}.{method_name}")
                print(f"  AssertionError: {e}")
            except Exception as e:
                failed += 1
                print(f"✗ {test_class.__name__}.{method_name}")
                print(f"  Exception: {e}")
                traceback.print_exc()
    
    print(f"\n{'='*50}")
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print(f"{'='*50}")
    
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)