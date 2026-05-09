"""
Periodic Table Utilities - 单元测试

Tests all core functionality of the periodic table utilities module.
"""

import sys
sys.path.insert(0, '.')

from mod import (
    get_element,
    get_elements_by_period,
    get_elements_by_group,
    get_elements_by_category,
    search_elements,
    calculate_molecular_weight,
    format_element_info,
    compare_elements,
    get_element_neighbors,
    get_common_compounds,
    ElementCategory,
    ElementState,
    ELEMENTS,
)


def test_get_element():
    """测试元素查询功能"""
    print("测试 get_element...")
    
    # 按原子序数查询
    e = get_element(1)
    assert e is not None
    assert e.symbol == "H"
    assert e.name == "氢"
    print("  ✓ 按原子序数查询成功")
    
    # 按符号查询
    e = get_element("Fe")
    assert e is not None
    assert e.atomic_number == 26
    assert e.name == "铁"
    print("  ✓ 按符号查询成功")
    
    # 按英文名查询
    e = get_element("oxygen")
    assert e is not None
    assert e.atomic_number == 8
    assert e.symbol == "O"
    print("  ✓ 按英文名查询成功")
    
    # 按中文名查询
    e = get_element("碳")
    assert e is not None
    assert e.atomic_number == 6
    assert e.symbol == "C"
    print("  ✓ 按中文名查询成功")
    
    # 查询不存在的元素
    e = get_element(999)
    assert e is None
    print("  ✓ 查询不存在的元素返回 None")
    
    e = get_element("NotExist")
    assert e is None
    print("  ✓ 查询不存在的符号返回 None")
    
    print("✅ get_element 测试通过\n")


def test_get_elements_by_period():
    """测试按周期获取元素"""
    print("测试 get_elements_by_period...")
    
    # 第一周期
    period1 = get_elements_by_period(1)
    assert len(period1) == 2
    assert set(e.symbol for e in period1) == {"H", "He"}
    print("  ✓ 第一周期有2个元素: H, He")
    
    # 第二周期
    period2 = get_elements_by_period(2)
    assert len(period2) == 8
    print(f"  ✓ 第二周期有{len(period2)}个元素")
    
    # 第三周期
    period3 = get_elements_by_period(3)
    assert len(period3) == 8
    print(f"  ✓ 第三周期有{len(period3)}个元素")
    
    # 第六周期
    period6 = get_elements_by_period(6)
    assert len(period6) == 32
    print(f"  ✓ 第六周期有{len(period6)}个元素（含镧系）")
    
    print("✅ get_elements_by_period 测试通过\n")


def test_get_elements_by_group():
    """测试按族获取元素"""
    print("测试 get_elements_by_group...")
    
    # 第一族（碱金属 + 氢）
    # 注意：氢在周期表中放在族1，但属于非金属
    group1 = get_elements_by_group(1)
    symbols = [e.symbol for e in group1]
    assert "Li" in symbols
    assert "Na" in symbols
    assert "K" in symbols
    assert "H" in symbols  # H在第一族位置
    print(f"  ✓ 第一族: {[e.symbol for e in group1]}")
    
    # 第18族（稀有气体）
    group18 = get_elements_by_group(18)
    symbols = [e.symbol for e in group18]
    assert "He" in symbols
    assert "Ne" in symbols
    assert "Ar" in symbols
    assert len(group18) == 7
    print(f"  ✓ 第18族（稀有气体）有{len(group18)}个元素")
    
    # 第17族（卤素）
    group17 = get_elements_by_group(17)
    symbols = [e.symbol for e in group17]
    assert "F" in symbols
    assert "Cl" in symbols
    assert "Br" in symbols
    assert "I" in symbols
    print(f"  ✓ 第17族（卤素）: {[e.symbol for e in group17]}")
    
    print("✅ get_elements_by_group 测试通过\n")


def test_get_elements_by_category():
    """测试按分类获取元素"""
    print("测试 get_elements_by_category...")
    
    # 稀有气体
    noble_gases = get_elements_by_category(ElementCategory.NOBLE_GAS)
    assert len(noble_gases) == 7
    symbols = [e.symbol for e in noble_gases]
    assert "He" in symbols
    assert "Ne" in symbols
    assert "Ar" in symbols
    print(f"  ✓ 稀有气体: {[e.symbol for e in noble_gases]}")
    
    # 碱金属
    alkali_metals = get_elements_by_category(ElementCategory.ALKALI_METAL)
    assert len(alkali_metals) == 6  # Li, Na, K, Rb, Cs, Fr
    symbols = [e.symbol for e in alkali_metals]
    assert "Li" in symbols
    assert "Na" in symbols
    print(f"  ✓ 碱金属: {[e.symbol for e in alkali_metals]}")
    
    # 镧系元素
    lanthanides = get_elements_by_category(ElementCategory.LANTHANIDE)
    assert len(lanthanides) == 15  # La-Lu
    print(f"  ✓ 镧系元素有{len(lanthanides)}个")
    
    # 锕系元素
    actinides = get_elements_by_category(ElementCategory.ACTINIDE)
    assert len(actinides) == 15  # Ac-Lr
    print(f"  ✓ 锕系元素有{len(actinides)}个")
    
    print("✅ get_elements_by_category 测试通过\n")


def test_search_elements():
    """测试元素搜索"""
    print("测试 search_elements...")
    
    # 搜索中文名
    results = search_elements("氧")
    symbols = [e.symbol for e in results]
    assert "O" in symbols  # 包含氧元素
    print(f"  ✓ 搜索'氧'找到: {symbols}")
    
    # 搜索英文名部分
    results = search_elements("gen")
    symbols = [e.symbol for e in results]
    assert "H" in symbols  # Hydrogen
    assert "O" in symbols  # Oxygen
    assert "N" in symbols  # Nitrogen
    print(f"  ✓ 搜索'gen'找到: {symbols}")
    
    # 搜索符号
    results = search_elements("Fe")
    symbols = [e.symbol for e in results]
    assert "Fe" in symbols  # 包含铁元素
    print(f"  ✓ 搜索'Fe'找到: {symbols}")
    
    print("✅ search_elements 测试通过\n")


def test_calculate_molecular_weight():
    """测试分子量计算"""
    print("测试 calculate_molecular_weight...")
    
    # H2O
    mass, composition = calculate_molecular_weight("H2O")
    assert mass == 18.015
    assert composition == {"H": 2, "O": 1}
    print(f"  ✓ H2O: {mass} g/mol, 组成: {composition}")
    
    # NaCl
    mass, composition = calculate_molecular_weight("NaCl")
    assert abs(mass - 58.44) < 0.01  # 允许小误差
    assert composition == {"Na": 1, "Cl": 1}
    print(f"  ✓ NaCl: {mass} g/mol, 组成: {composition}")
    
    # C6H12O6 (葡萄糖)
    mass, composition = calculate_molecular_weight("C6H12O6")
    assert composition == {"C": 6, "H": 12, "O": 6}
    print(f"  ✓ C6H12O6: {mass} g/mol, 组成: {composition}")
    
    # H2SO4 (硫酸)
    mass, composition = calculate_molecular_weight("H2SO4")
    assert composition == {"H": 2, "S": 1, "O": 4}
    print(f"  ✓ H2SO4: {mass} g/mol, 组成: {composition}")
    
    # 测试错误格式
    try:
        calculate_molecular_weight("Invalid")
        assert False, "应该抛出异常"
    except ValueError:
        print("  ✓ 无效化学式抛出异常")
    
    print("✅ calculate_molecular_weight 测试通过\n")


def test_format_element_info():
    """测试元素信息格式化"""
    print("测试 format_element_info...")
    
    e = get_element(79)  # 金
    info = format_element_info(e)
    assert "金" in info
    assert "Au" in info
    assert "79" in info
    assert "196.97" in info
    print("  ✓ 金元素信息格式化成功")
    print(info)
    
    print("✅ format_element_info 测试通过\n")


def test_compare_elements():
    """测试元素比较"""
    print("测试 compare_elements...")
    
    comparison = compare_elements("Fe", "Cu")
    
    assert "元素1" in comparison
    assert "元素2" in comparison
    assert comparison["同周期"] == True  # Fe和Cu都在第四周期
    assert comparison["原子序数差异"] == 3
    print(f"  ✓ Fe vs Cu: {comparison}")
    
    comparison = compare_elements("Na", "Cl")
    assert comparison["同周期"] == True  # 都在第三周期
    assert comparison["同族"] == False
    print(f"  ✓ Na vs Cl: 同周期但不同族")
    
    comparison = compare_elements("Li", "Na")
    assert comparison["同族"] == True  # 都是第一族碱金属
    assert comparison["同周期"] == False
    print(f"  ✓ Li vs Na: 同族但不同周期")
    
    print("✅ compare_elements 测试通过\n")


def test_get_element_neighbors():
    """测试获取相邻元素"""
    print("测试 get_element_neighbors...")
    
    # 碳的相邻元素
    neighbors = get_element_neighbors("C")
    
    assert neighbors["left"] is not None
    assert neighbors["left"].symbol == "B"
    print(f"  ✓ C的左侧是 B")
    
    assert neighbors["right"] is not None
    assert neighbors["right"].symbol == "N"
    print(f"  ✓ C的右侧是 N")
    
    # 碳在周期2族14，上方没有元素（周期1只有族1和族18）
    assert neighbors["above"] is None
    print(f"  ✓ C上方无元素")
    
    # 碳下方是硅
    assert neighbors["below"] is not None
    assert neighbors["below"].symbol == "Si"
    print(f"  ✓ C下方是 Si")
    
    print("✅ get_element_neighbors 测试通过\n")


def test_get_common_compounds():
    """测试获取常见化合物"""
    print("测试 get_common_compounds...")
    
    # 铁
    compounds = get_common_compounds("Fe")
    assert len(compounds) > 0
    assert "Fe2O3" in compounds
    assert "FeSO4" in compounds
    print(f"  ✓ Fe的常见化合物: {compounds}")
    
    # 氢
    compounds = get_common_compounds("H")
    assert "H2O" in compounds
    assert "H2" in compounds
    print(f"  ✓ H的常见化合物: {compounds}")
    
    # 金（较少）
    compounds = get_common_compounds("Au")
    print(f"  ✓ Au的常见化合物: {compounds}")
    
    print("✅ get_common_compounds 测试通过\n")


def test_element_data():
    """测试元素数据完整性"""
    print("测试元素数据完整性...")
    
    # 检查元素总数
    assert len(ELEMENTS) == 118
    print(f"  ✓ 元素总数: 118")
    
    # 检查原子序数连续性
    for i in range(1, 119):
        assert i in ELEMENTS
        assert ELEMENTS[i].atomic_number == i
    print("  ✓ 原子序数连续 1-118")
    
    # 检查必要属性
    for e in ELEMENTS.values():
        assert e.symbol is not None
        assert e.name is not None
        assert e.name_en is not None
        assert e.atomic_mass > 0
        assert e.period > 0
    print("  ✓ 所有元素具有必要属性")
    
    print("✅ 元素数据完整性测试通过\n")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Periodic Table Utilities - 单元测试")
    print("=" * 60)
    print()
    
    test_get_element()
    test_get_elements_by_period()
    test_get_elements_by_group()
    test_get_elements_by_category()
    test_search_elements()
    test_calculate_molecular_weight()
    test_format_element_info()
    test_compare_elements()
    test_get_element_neighbors()
    test_get_common_compounds()
    test_element_data()
    
    print("=" * 60)
    print("🎉 所有测试通过！")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()