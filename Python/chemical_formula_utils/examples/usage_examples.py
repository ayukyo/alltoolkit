"""
Chemical Formula Utils 使用示例

展示化学式解析和处理的常见用法
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from chemical_formula_utils.mod import (
    ChemicalFormulaUtils,
    parse,
    get_elements,
    molar_mass,
    mass_percentages,
    is_valid,
    format_formula,
    empirical_formula
)


def example_basic_parsing():
    """基本解析示例"""
    print("=" * 50)
    print("示例1: 基本化学式解析")
    print("=" * 50)
    
    utils = ChemicalFormulaUtils()
    
    formulas = ["H2O", "NaCl", "CO2", "C6H12O6", "H2SO4"]
    
    for formula in formulas:
        result = utils.parse(formula)
        print(f"\n化学式: {formula}")
        print(f"  元素组成: {result.elements}")
        print(f"  是否有效: {result.is_valid}")


def example_molar_mass():
    """摩尔质量计算示例"""
    print("\n" + "=" * 50)
    print("示例2: 摩尔质量计算")
    print("=" * 50)
    
    utils = ChemicalFormulaUtils()
    
    compounds = [
        ("H2O", "水"),
        ("NaCl", "氯化钠(食盐)"),
        ("C6H12O6", "葡萄糖"),
        ("C2H5OH", "乙醇"),
        ("H2SO4", "硫酸"),
        ("CaCO3", "碳酸钙(石灰石)"),
        ("C9H8O4", "阿司匹林"),
        ("C8H10N4O2", "咖啡因"),
    ]
    
    print("\n化合物名称".ljust(20), "化学式".ljust(12), "摩尔质量(g/mol)")
    print("-" * 50)
    
    for formula, name in compounds:
        mass = utils.calculate_molar_mass(formula)
        print(f"{name.ljust(18)} {formula.ljust(12)} {mass:.4f}")


def example_mass_percentage():
    """质量百分比计算示例"""
    print("\n" + "=" * 50)
    print("示例3: 元素质量百分比")
    print("=" * 50)
    
    utils = ChemicalFormulaUtils()
    
    # 计算水中氢和氧的质量比
    formula = "H2O"
    percentages = utils.calculate_mass_percentages(formula)
    
    print(f"\n{formula} (水) 的元素质量百分比:")
    for element, percent in percentages.items():
        print(f"  {element}: {percent:.2f}%")
    
    # 葡萄糖
    formula = "C6H12O6"
    percentages = utils.calculate_mass_percentages(formula)
    
    print(f"\n{formula} (葡萄糖) 的元素质量百分比:")
    for element, percent in percentages.items():
        print(f"  {element}: {percent:.2f}%")
    
    # 硫酸
    formula = "H2SO4"
    percentages = utils.calculate_mass_percentages(formula)
    
    print(f"\n{formula} (硫酸) 的元素质量百分比:")
    for element, percent in percentages.items():
        print(f"  {element}: {percent:.2f}%")


def example_complex_formulas():
    """复杂化学式解析示例"""
    print("\n" + "=" * 50)
    print("示例4: 复杂化学式解析")
    print("=" * 50)
    
    utils = ChemicalFormulaUtils()
    
    formulas = [
        ("Ca(OH)2", "氢氧化钙(熟石灰)"),
        ("Al2(SO4)3", "硫酸铝"),
        ("CuSO4·5H2O", "五水硫酸铜(胆矾)"),
        ("K4[Fe(CN)6]", "亚铁氰化钾"),
        ("CH3COOH", "乙酸(醋酸)"),
        ("(NH4)2SO4", "硫酸铵"),
    ]
    
    for formula, name in formulas:
        result = utils.parse(formula)
        mass = utils.calculate_molar_mass(formula)
        
        print(f"\n{name} ({formula}):")
        print(f"  元素组成: {result.elements}")
        print(f"  摩尔质量: {mass:.4f} g/mol")


def example_empirical_formula():
    """最简式计算示例"""
    print("\n" + "=" * 50)
    print("示例5: 最简式(实验式)计算")
    print("=" * 50)
    
    utils = ChemicalFormulaUtils()
    
    compounds = [
        ("C6H12O6", "葡萄糖"),
        ("C2H2", "乙炔"),
        ("C2H4", "乙烯"),
        ("C4H10", "丁烷"),
        ("H2O2", "过氧化氢"),
    ]
    
    print("\n分子式".ljust(15), "最简式".ljust(10), "名称")
    print("-" * 45)
    
    for formula, name in compounds:
        empirical = utils.get_empirical_formula(formula)
        print(f"{formula.ljust(15)} {empirical.ljust(10)} {name}")


def example_formula_formatting():
    """化学式格式化示例"""
    print("\n" + "=" * 50)
    print("示例6: 化学式格式化")
    print("=" * 50)
    
    utils = ChemicalFormulaUtils()
    
    formulas = ["H2O", "H2SO4", "C6H12O6", "Ca(OH)2", "Al2(SO4)3"]
    
    print("\n原始格式".ljust(15), "下标格式")
    print("-" * 30)
    
    for formula in formulas:
        formatted = utils.format_formula(formula, use_subscripts=True)
        print(f"{formula.ljust(15)} {formatted}")


def example_compound_type():
    """化合物类型推断示例"""
    print("\n" + "=" * 50)
    print("示例7: 化合物类型推断")
    print("=" * 50)
    
    utils = ChemicalFormulaUtils()
    
    compounds = [
        "Fe", "O2", "He",
        "H2O", "CO2", "CaO",
        "HCl", "H2SO4", "HNO3",
        "NaOH", "Ca(OH)2",
        "NaCl", "CaCO3",
        "CH4", "C6H12O6", "C2H5OH"
    ]
    
    print("\n化学式".ljust(12), "类型")
    print("-" * 30)
    
    for formula in compounds:
        compound_type = utils.get_compound_type(formula)
        print(f"{formula.ljust(12)} {compound_type}")


def example_compare_formulas():
    """化学式比较示例"""
    print("\n" + "=" * 50)
    print("示例8: 化学式比较")
    print("=" * 50)
    
    utils = ChemicalFormulaUtils()
    
    comparisons = [
        ("H2O", "H2O"),
        ("H2O", "H2O2"),
        ("CH3COOH", "C2H4O2"),
        ("C6H12O6", "C12H22O11"),
    ]
    
    for f1, f2 in comparisons:
        result = utils.compare_formulas(f1, f2)
        print(f"\n比较: {f1} vs {f2}")
        print(f"  是否相等: {result['are_equal']}")
        if result['differences']:
            print(f"  差异元素: {result['differences']}")


def example_element_lookup():
    """元素信息查询示例"""
    print("\n" + "=" * 50)
    print("示例9: 元素信息查询")
    print("=" * 50)
    
    utils = ChemicalFormulaUtils()
    
    elements = ["H", "C", "O", "Fe", "Au", "Ag"]
    
    print("\n符号".ljust(6), "原子序数".ljust(10), "相对原子质量")
    print("-" * 35)
    
    for symbol in elements:
        elem = utils.get_element_info(symbol)
        if elem:
            print(f"{elem.symbol.ljust(6)} {str(elem.atomic_number).ljust(10)} {elem.atomic_mass:.4f}")
    
    # 按质量范围查找元素
    print("\n原子质量在 12-20 之间的元素:")
    elements_in_range = utils.find_elements_by_mass_range(12, 20)
    for elem in elements_in_range:
        print(f"  {elem.symbol}: {elem.atomic_mass:.4f}")


def example_balance_hint():
    """配平提示示例"""
    print("\n" + "=" * 50)
    print("示例10: 化学方程式配平分析")
    print("=" * 50)
    
    utils = ChemicalFormulaUtils()
    
    equations = [
        ("H2 + O2", "H2O"),
        ("Fe + O2", "Fe2O3"),
        ("CH4 + O2", "CO2 + H2O"),
    ]
    
    for reactants, products in equations:
        result = utils.balance_equation_hint(reactants, products)
        print(f"\n反应: {reactants} → {products}")
        print(f"  反应物元素: {result['reactant_elements']}")
        print(f"  生成物元素: {result['product_elements']}")
        print(f"  是否配平: {result['is_balanced']}")
        if result['unbalanced_elements']:
            print(f"  未平衡元素: {result['unbalanced_elements']}")


def example_convenience_functions():
    """便捷函数使用示例"""
    print("\n" + "=" * 50)
    print("示例11: 便捷函数")
    print("=" * 50)
    
    formula = "C6H12O6"
    
    print(f"\n化学式: {formula}")
    print(f"  元素组成: {get_elements(formula)}")
    print(f"  摩尔质量: {molar_mass(formula):.4f} g/mol")
    print(f"  质量百分比: {mass_percentages(formula)}")
    print(f"  是否有效: {is_valid(formula)}")
    print(f"  最简式: {empirical_formula(formula)}")
    print(f"  格式化: {format_formula(formula)}")


def main():
    """运行所有示例"""
    example_basic_parsing()
    example_molar_mass()
    example_mass_percentage()
    example_complex_formulas()
    example_empirical_formula()
    example_formula_formatting()
    example_compound_type()
    example_compare_formulas()
    example_element_lookup()
    example_balance_hint()
    example_convenience_functions()
    
    print("\n" + "=" * 50)
    print("所有示例运行完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()