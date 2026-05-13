"""
Bill Splitter Utils 测试文件
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    BillSplitter, Person, BillItem, SplitResult, BillSummary,
    split_bill_equally, calculate_tip, suggest_tip, split_with_tip,
    calculate_split_with_different_items, format_currency, parse_currency
)
from decimal import Decimal


def test_bill_splitter_basic():
    """测试基本的账单分割功能"""
    print("测试基本的账单分割功能...")
    
    splitter = BillSplitter()
    splitter.add_item("Pizza", 30.00)
    splitter.add_item("Salad", 15.00)
    splitter.add_item("Drink", 10.00)
    splitter.set_participants(["Alice", "Bob", "Charlie"])
    
    summary = splitter.split_equally()
    
    # 总计应该是 55.00
    assert summary.subtotal == Decimal("55.00"), f"小计错误: {summary.subtotal}"
    
    # 每人应该付约 18.33
    per_person = summary.splits[0].total
    assert per_person > Decimal("18"), f"每人金额太低: {per_person}"
    
    print("✅ 基本账单分割测试通过")


def test_bill_splitter_with_tax_and_tip():
    """测试带税和小费的账单分割"""
    print("测试带税和小费的账单分割...")
    
    splitter = BillSplitter()
    splitter.add_item("Dinner", 100.00)
    splitter.set_participants(["Alice", "Bob"])
    splitter.set_tax_rate(0.10)  # 10% 税
    splitter.set_tip_rate(0.15)  # 15% 小费
    
    summary = splitter.split_equally()
    
    # 小计 = 100.00
    assert summary.subtotal == Decimal("100.00")
    
    # 税 = 10.00
    assert summary.tax_amount == Decimal("10.00"), f"税费错误: {summary.tax_amount}"
    
    # 小费 = (100 + 10) * 0.15 = 16.50
    assert summary.tip_amount == Decimal("16.50"), f"小费错误: {summary.tip_amount}"
    
    # 总计 = 100 + 10 + 16.50 = 126.50
    assert summary.grand_total == Decimal("126.50"), f"总计错误: {summary.grand_total}"
    
    # 每人 = 63.25
    assert summary.splits[0].total == Decimal("63.25"), f"每人金额错误: {summary.splits[0].total}"
    
    print("✅ 带税和小费测试通过")


def test_bill_splitter_with_discount():
    """测试带折扣的账单分割"""
    print("测试带折扣的账单分割...")
    
    splitter = BillSplitter()
    splitter.add_item("Meal", 50.00)
    splitter.set_participants(["Alice"])
    splitter.set_discount(10.00)  # 10元折扣
    
    summary = splitter.split_equally()
    
    # 折扣后小计应为 40.00
    assert summary.discount == Decimal("10.00")
    
    # 检查总计计算
    expected_total = Decimal("40.00")  # 50 - 10 = 40
    assert summary.grand_total == expected_total
    
    print("✅ 折扣测试通过")


def test_bill_splitter_by_items():
    """测试按项目分账"""
    print("测试按项目分账...")
    
    splitter = BillSplitter()
    splitter.add_item("Pizza", 30.00, shared_by=["Alice", "Bob"])
    splitter.add_item("Salad", 15.00, shared_by=["Charlie"])
    splitter.add_item("Drink", 10.00, shared_by=["Alice", "Bob", "Charlie"])
    splitter.set_participants(["Alice", "Bob", "Charlie"])
    
    summary = splitter.split_by_items()
    
    # Alice: Pizza(15) + Drink(3.33) = 18.33
    # Bob: Pizza(15) + Drink(3.33) = 18.33
    # Charlie: Salad(15) + Drink(3.33) = 18.33
    
    # 检查每人金额（允许 rounding 误差）
    for split in summary.splits:
        assert split.subtotal > Decimal("15"), f"{split.person_name}金额太低"
    
    print("✅ 按项目分账测试通过")


def test_bill_splitter_by_ratio():
    """测试按比例分账"""
    print("测试按比例分账...")
    
    splitter = BillSplitter()
    splitter.add_item("Total", 100.00)
    splitter.set_participants(["Alice", "Bob", "Charlie"])
    
    # Alice 付 50%, Bob 付 30%, Charlie 付 20%
    ratios = {"Alice": 0.5, "Bob": 0.3, "Charlie": 0.2}
    summary = splitter.split_by_ratio(ratios)
    
    # Alice 应付 50.00
    alice_split = [s for s in summary.splits if s.person_name == "Alice"][0]
    assert alice_split.subtotal == Decimal("50.00"), f"Alice金额错误: {alice_split.subtotal}"
    
    # Bob 应付 30.00
    bob_split = [s for s in summary.splits if s.person_name == "Bob"][0]
    assert bob_split.subtotal == Decimal("30.00"), f"Bob金额错误: {bob_split.subtotal}"
    
    # Charlie 应付 20.00
    charlie_split = [s for s in summary.splits if s.person_name == "Charlie"][0]
    assert charlie_split.subtotal == Decimal("20.00"), f"Charlie金额错误: {charlie_split.subtotal}"
    
    print("✅ 按比例分账测试通过")


def test_bill_splitter_custom():
    """测试自定义金额分账"""
    print("测试自定义金额分账...")
    
    splitter = BillSplitter()
    splitter.add_item("Total", 100.00)
    splitter.add_participant("Alice", custom_amount=60.00)
    splitter.add_participant("Bob", custom_amount=40.00)
    
    summary = splitter.split_custom()
    
    # Alice 应付 60（按比例加上税和小费，这里没有）
    alice_split = [s for s in summary.splits if s.person_name == "Alice"][0]
    assert alice_split.subtotal == Decimal("60.00")
    
    # Bob 应付 40
    bob_split = [s for s in summary.splits if s.person_name == "Bob"][0]
    assert bob_split.subtotal == Decimal("40.00")
    
    print("✅ 自定义金额分账测试通过")


def test_bill_splitter_chain_calls():
    """测试链式调用"""
    print("测试链式调用...")
    
    splitter = BillSplitter()
    result = splitter.add_item("A", 10).add_item("B", 20).set_participants(["X", "Y"]).set_tax_rate(0.1)
    
    # 验证返回的是 self
    assert result is splitter
    
    summary = splitter.split_equally()
    assert len(summary.splits) == 2
    
    print("✅ 式调用测试通过")


def test_bill_splitter_history():
    """测试历史记录"""
    print("测试历史记录...")
    
    splitter = BillSplitter()
    splitter.add_item("A", 10).set_participants(["X"])
    splitter.split_equally()
    
    splitter.clear()
    splitter.add_item("B", 20).set_participants(["Y"])
    splitter.split_equally()
    
    history = splitter.get_history()
    assert len(history) == 2, f"历史记录数量错误: {len(history)}"
    
    splitter.clear_history()
    assert len(splitter.get_history()) == 0
    
    print("✅ 历史记录测试通过")


def test_bill_splitter_format_summary():
    """测试格式化输出"""
    print("测试格式化输出...")
    
    splitter = BillSplitter(currency_symbol="¥")
    splitter.add_item("Dinner", 100).set_participants(["Alice", "Bob"])
    summary = splitter.split_equally()
    
    formatted = splitter.format_summary(summary)
    assert "¥" in formatted, f"货币符号未出现在输出中"
    assert "Alice" in formatted
    assert "Bob" in formatted
    
    print("✅ 格式化输出测试通过")


def test_split_bill_equally_function():
    """测试便捷函数 split_bill_equally"""
    print("测试 split_bill_equally 函数...")
    
    result = split_bill_equally(100, 4, tax_rate=0.1, tip_rate=0.15)
    
    # subtotal = 100.0
    assert result["subtotal"] == 100.0
    
    # tax = 10.0
    assert result["tax"] == 10.0
    
    # tip = (100 + 10) * 0.15 = 16.5
    assert result["tip"] == 16.5
    
    # total = 126.5
    assert result["total"] == 126.5
    
    # per_person = 31.625 -> 31.63 (rounded)
    assert result["per_person"] > 31.0
    
    print("✅ split_bill_equally 函数测试通过")


def test_calculate_tip_function():
    """测试小费计算函数"""
    print("测试 calculate_tip 函数...")
    
    tip = calculate_tip(100, 0.15)
    assert tip == 15.0
    
    tip = calculate_tip(50, 0.20)
    assert tip == 10.0
    
    print("✅ calculate_tip 函数测试通过")


def test_suggest_tip_function():
    """测试小费建议函数"""
    print("测试 suggest_tip 函数...")
    
    suggestions = suggest_tip(100)
    
    assert "15%" in suggestions
    assert suggestions["15%"] == 15.0
    assert suggestions["20%"] == 20.0
    
    print("✅ suggest_tip 函数测试通过")


def test_split_with_tip_function():
    """测试含小费人均计算"""
    print("测试 split_with_tip 函数...")
    
    per_person = split_with_tip(100, 4, 0.15)
    # 100 * 1.15 / 4 = 28.75
    assert per_person == 28.75
    
    print("✅ split_with_tip 函数测试通过")


def test_format_currency_function():
    """测试货币格式化"""
    print("测试 format_currency 函数...")
    
    formatted = format_currency(123.45)
    assert formatted == "$123.45"
    
    formatted = format_currency(100, symbol="¥")
    assert formatted == "¥100.00"
    
    print("✅ format_currency 函数测试通过")


def test_parse_currency_function():
    """测试货币解析"""
    print("测试 parse_currency 函数...")
    
    value = parse_currency("$123.45")
    assert value == 123.45
    
    value = parse_currency("¥100")
    assert value == 100.0
    
    value = parse_currency("€50.00")
    assert value == 50.0
    
    value = parse_currency("1,234.56")
    assert value == 1234.56
    
    print("✅ parse_currency 函数测试通过")


def test_calculate_split_with_different_items():
    """测试多项目分账便捷函数"""
    print("测试 calculate_split_with_different_items 函数...")
    
    items = [
        {"name": "Pizza", "price": 30, "shared_by": ["Alice", "Bob"]},
        {"name": "Salad", "price": 15, "shared_by": ["Charlie"]}
    ]
    
    result = calculate_split_with_different_items(
        items, 
        ["Alice", "Bob", "Charlie"]
    )
    
    # Alice: 15, Bob: 15, Charlie: 15
    assert result["Alice"] == 15.0
    assert result["Bob"] == 15.0
    assert result["Charlie"] == 15.0
    
    print("✅ calculate_split_with_different_items 函数测试通过")


def test_bill_splitter_edge_cases():
    """测试边界情况"""
    print("测试边界情况...")
    
    # 空参与者
    splitter = BillSplitter()
    splitter.add_item("A", 10)
    try:
        splitter.split_equally()
        assert False, "应该抛出异常"
    except ValueError as e:
        assert "没有参与者" in str(e)
    
    # 空项目
    splitter = BillSplitter()
    splitter.set_participants(["A"])
    try:
        splitter.split_equally()
        assert False, "应该抛出异常"
    except ValueError as e:
        assert "没有账单项目" in str(e)
    
    # 比例总和为零
    splitter = BillSplitter()
    splitter.add_item("A", 10).set_participants(["A", "B"])
    try:
        splitter.split_by_ratio({"A": 0, "B": 0})
        assert False, "应该抛出异常"
    except ValueError as e:
        assert "比例总和" in str(e)
    
    print("✅ 边界情况测试通过")


def test_bill_splitter_decimal_precision():
    """测试Decimal精度"""
    print("测试Decimal精度...")
    
    splitter = BillSplitter()
    splitter.add_item("A", 33.33)
    splitter.add_item("B", 33.33)
    splitter.add_item("C", 33.34)
    splitter.set_participants(["X", "Y", "Z"])
    
    summary = splitter.split_equally()
    
    # 总计应该是 100.00
    assert summary.subtotal == Decimal("100.00")
    
    print("✅ Decimal精度测试通过")


def test_split_result_to_dict():
    """测试SplitResult序列化"""
    print("测试SplitResult序列化...")
    
    result = SplitResult(
        person_name="Alice",
        subtotal=Decimal("50"),
        tax_amount=Decimal("5"),
        tip_amount=Decimal("7.5"),
        total=Decimal("62.5")
    )
    
    d = result.to_dict()
    assert d["person_name"] == "Alice"
    assert d["subtotal"] == "50"
    assert d["total"] == "62.5"
    
    print("✅ SplitResult序列化测试通过")


def test_bill_summary_to_dict():
    """测试BillSummary序列化"""
    print("测试BillSummary序列化...")
    
    summary = BillSummary(
        subtotal=Decimal("100"),
        tax_rate=Decimal("0.1"),
        tax_amount=Decimal("10"),
        tip_rate=Decimal("0.15"),
        tip_amount=Decimal("16.5"),
        discount=Decimal("0"),
        grand_total=Decimal("126.5"),
        splits=[]
    )
    
    d = summary.to_dict()
    assert d["subtotal"] == "100"
    assert "created_at" in d
    
    print("✅ BillSummary序列化测试通过")


def test_bill_splitter_currency_symbol():
    """测试自定义货币符号"""
    print("测试自定义货币符号...")
    
    # 不同货币符号
    symbols = ["$", "¥", "€", "£", "₹"]
    for symbol in symbols:
        splitter = BillSplitter(currency_symbol=symbol)
        splitter.add_item("A", 10).set_participants(["X"])
        summary = splitter.split_equally()
        formatted = splitter.format_summary(summary)
        assert symbol in formatted
    
    print("✅ 自定义货币符号测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("Bill Splitter Utils 测试套件")
    print("=" * 50)
    
    tests = [
        test_bill_splitter_basic,
        test_bill_splitter_with_tax_and_tip,
        test_bill_splitter_with_discount,
        test_bill_splitter_by_items,
        test_bill_splitter_by_ratio,
        test_bill_splitter_custom,
        test_bill_splitter_chain_calls,
        test_bill_splitter_history,
        test_bill_splitter_format_summary,
        test_split_bill_equally_function,
        test_calculate_tip_function,
        test_suggest_tip_function,
        test_split_with_tip_function,
        test_format_currency_function,
        test_parse_currency_function,
        test_calculate_split_with_different_items,
        test_bill_splitter_edge_cases,
        test_bill_splitter_decimal_precision,
        test_split_result_to_dict,
        test_bill_summary_to_dict,
        test_bill_splitter_currency_symbol,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} 失败: {e}")
            failed += 1
    
    print("=" * 50)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)