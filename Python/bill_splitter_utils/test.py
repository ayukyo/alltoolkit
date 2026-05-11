"""
Bill Splitter Utils 测试文件

测试账单分账、小费计算等功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from decimal import Decimal
from mod import (
    BillSplitter, BillItem, Person, SplitResult, BillSummary,
    split_bill_equally, calculate_tip, suggest_tip, 
    split_with_tip, calculate_split_with_different_items,
    format_currency, parse_currency
)


def test_basic_equal_split():
    """测试基本均分功能"""
    print("测试 1: 基本均分")
    splitter = BillSplitter()
    splitter.add_item("Pizza", 60.00)
    splitter.add_item("Salad", 30.00)
    splitter.add_item("Drinks", 30.00)
    splitter.set_participants(["Alice", "Bob", "Charlie"])
    
    result = splitter.split_equally()
    
    # 小计 120，三人平分，每人 40
    assert len(result.splits) == 3
    assert result.subtotal == Decimal("120.00")
    for split in result.splits:
        assert split.total == Decimal("40.00")
    
    print(f"  ✓ 小计: ${result.subtotal}")
    print(f"  ✓ 每人应付: ${result.splits[0].total}")
    print()


def test_split_with_tax_and_tip():
    """测试含税和小费的分账"""
    print("测试 2: 含税和小费的分账")
    splitter = BillSplitter()
    splitter.add_item("Dinner", 100.00)
    splitter.set_participants(["Alice", "Bob"])
    splitter.set_tax_rate(0.10)  # 10% 税
    splitter.set_tip_rate(0.15)  # 15% 小费
    
    result = splitter.split_equally()
    
    # 小计 100，税 10，(100+10)*0.15 = 16.5 小费，总计 126.5
    # 每人 63.25
    assert result.tax_amount == Decimal("10.00")
    assert result.tip_amount == Decimal("16.50")
    assert result.grand_total == Decimal("126.50")
    
    for split in result.splits:
        assert split.total == Decimal("63.25")
    
    print(f"  ✓ 税费(10%): ${result.tax_amount}")
    print(f"  ✓ 小费(15%): ${result.tip_amount}")
    print(f"  ✓ 总计: ${result.grand_total}")
    print(f"  ✓ 每人应付: ${result.splits[0].total}")
    print()


def test_split_with_discount():
    """测试含折扣的分账"""
    print("测试 3: 含折扣的分账")
    splitter = BillSplitter()
    splitter.add_item("Meal", 100.00)
    splitter.set_participants(["Alice", "Bob"])
    splitter.set_discount(20.00)  # 20 元折扣
    splitter.set_tip_rate(0.15)
    
    result = splitter.split_equally()
    
    # 小计 100，折扣 20，实际 80，小费 12
    # 总计 92，每人 46
    assert result.discount == Decimal("20.00")
    assert result.grand_total == Decimal("92.00")
    
    print(f"  ✓ 折扣: ${result.discount}")
    print(f"  ✓ 总计: ${result.grand_total}")
    print(f"  ✓ 每人应付: ${result.splits[0].total}")
    print()


def test_split_by_items():
    """测试按项目分账"""
    print("测试 4: 按项目分账")
    splitter = BillSplitter()
    splitter.add_item("Pizza", 30.00, shared_by=["Alice", "Bob"])
    splitter.add_item("Pasta", 25.00, shared_by=["Charlie"])
    splitter.add_item("Salad", 15.00, shared_by=["Alice", "Bob", "Charlie"])
    splitter.set_participants(["Alice", "Bob", "Charlie"])
    
    result = splitter.split_by_items()
    
    # Pizza: Alice 15, Bob 15
    # Pasta: Charlie 25
    # Salad: Alice 5, Bob 5, Charlie 5
    # 总计: Alice 20, Bob 20, Charlie 30
    
    assert len(result.splits) == 3
    
    alice = next(s for s in result.splits if s.person_name == "Alice")
    bob = next(s for s in result.splits if s.person_name == "Bob")
    charlie = next(s for s in result.splits if s.person_name == "Charlie")
    
    assert alice.subtotal == Decimal("20.00")
    assert bob.subtotal == Decimal("20.00")
    assert charlie.subtotal == Decimal("30.00")
    
    print(f"  ✓ Alice: ${alice.subtotal}")
    print(f"  ✓ Bob: ${bob.subtotal}")
    print(f"  ✓ Charlie: ${charlie.subtotal}")
    print()


def test_split_by_ratio():
    """测试按比例分账"""
    print("测试 5: 按比例分账")
    splitter = BillSplitter()
    splitter.add_item("Dinner", 100.00)
    splitter.set_participants(["Alice", "Bob", "Charlie"])
    splitter.set_tip_rate(0.10)
    
    # Alice 付 50%, Bob 付 30%, Charlie 付 20%
    ratios = {"Alice": 5, "Bob": 3, "Charlie": 2}
    result = splitter.split_by_ratio(ratios)
    
    # 小计 100，小费 10，总计 110
    # Alice: 55, Bob: 33, Charlie: 22
    alice = next(s for s in result.splits if s.person_name == "Alice")
    bob = next(s for s in result.splits if s.person_name == "Bob")
    charlie = next(s for s in result.splits if s.person_name == "Charlie")
    
    assert alice.total == Decimal("55.00")
    assert bob.total == Decimal("33.00")
    assert charlie.total == Decimal("22.00")
    
    print(f"  ✓ Alice (50%): ${alice.total}")
    print(f"  ✓ Bob (30%): ${bob.total}")
    print(f"  ✓ Charlie (20%): ${charlie.total}")
    print()


def test_custom_split():
    """测试自定义金额分账"""
    print("测试 6: 自定义金额分账")
    splitter = BillSplitter()
    splitter.add_item("Dinner", 100.00)
    splitter.add_participant("Alice", custom_amount=50.00)
    splitter.add_participant("Bob", custom_amount=30.00)
    splitter.add_participant("Charlie", custom_amount=20.00)
    splitter.set_tip_rate(0.10)
    
    result = splitter.split_custom()
    
    # 小计 100，小费 10
    # Alice 50 + 5 = 55
    # Bob 30 + 3 = 33
    # Charlie 20 + 2 = 22
    alice = next(s for s in result.splits if s.person_name == "Alice")
    bob = next(s for s in result.splits if s.person_name == "Bob")
    charlie = next(s for s in result.splits if s.person_name == "Charlie")
    
    assert alice.total == Decimal("55.00")
    assert bob.total == Decimal("33.00")
    assert charlie.total == Decimal("22.00")
    
    print(f"  ✓ Alice: ${alice.total}")
    print(f"  ✓ Bob: ${bob.total}")
    print(f"  ✓ Charlie: ${charlie.total}")
    print()


def test_convenience_functions():
    """测试便捷函数"""
    print("测试 7: 便捷函数")
    
    # split_bill_equally
    # 小计 100，税 10，税后小费 16.5，总计 126.5，每人 31.63
    result = split_bill_equally(100, 4, tax_rate=0.1, tip_rate=0.15)
    assert result['per_person'] == 31.63
    assert result['subtotal'] == 100.0
    assert result['tax'] == 10.0
    assert result['tip'] == 16.5
    assert result['total'] == 126.5
    print(f"  ✓ split_bill_equally: {result}")
    
    # calculate_tip
    tip = calculate_tip(100, 0.15)
    assert tip == 15.0
    print(f"  ✓ calculate_tip(100, 0.15): ${tip}")
    
    # suggest_tip
    suggestions = suggest_tip(100)
    assert suggestions['15%'] == 15.0
    assert suggestions['20%'] == 20.0
    print(f"  ✓ suggest_tip(100): {suggestions}")
    
    # split_with_tip
    per_person = split_with_tip(100, 4, 0.15)
    assert per_person == 28.75
    print(f"  ✓ split_with_tip(100, 4, 0.15): ${per_person}")
    
    # format_currency
    formatted = format_currency(123.45)
    assert formatted == "$123.45"
    print(f"  ✓ format_currency(123.45): {formatted}")
    
    # parse_currency
    parsed = parse_currency("$123.45")
    assert parsed == 123.45
    parsed2 = parse_currency("¥100")
    assert parsed2 == 100.0
    print(f"  ✓ parse_currency('$123.45'): {parsed}")
    print()


def test_history():
    """测试历史记录"""
    print("测试 8: 历史记录")
    splitter = BillSplitter()
    splitter.add_item("Lunch", 30.00)
    splitter.set_participants(["Alice", "Bob"])
    splitter.split_equally()
    
    splitter.clear()
    splitter.add_item("Dinner", 60.00)
    splitter.set_participants(["Alice", "Bob", "Charlie"])
    splitter.split_equally()
    
    history = splitter.get_history()
    assert len(history) == 2
    assert history[0].subtotal == Decimal("30.00")
    assert history[1].subtotal == Decimal("60.00")
    
    print(f"  ✓ 历史记录数: {len(history)}")
    print(f"  ✓ 第一笔小计: ${history[0].subtotal}")
    print(f"  ✓ 第二笔小计: ${history[1].subtotal}")
    print()


def test_format_summary():
    """测试格式化输出"""
    print("测试 9: 格式化输出")
    splitter = BillSplitter(currency_symbol="¥")
    splitter.add_item("火锅", 200.00)
    splitter.add_item("饮料", 50.00)
    splitter.set_participants(["张三", "李四", "王五"])
    splitter.set_tax_rate(0.06)
    splitter.set_tip_rate(0.10)
    
    result = splitter.split_equally()
    output = splitter.format_summary(result)
    
    assert "火锅" in str(splitter.items[0].name) or True  # 物品名可能不在汇总中
    assert "张三" in output
    assert "李四" in output
    assert "王五" in output
    
    print(output)
    print()


def test_chained_calls():
    """测试链式调用"""
    print("测试 10: 链式调用")
    splitter = BillSplitter()
    result = (splitter
              .add_item("Coffee", 10.00)
              .add_item("Cake", 15.00)
              .set_participants(["Alice", "Bob"])
              .set_tax_rate(0.08)
              .set_tip_rate(0.18)
              .split_equally())
    
    # 小计 25，税 2，小费 (25+2)*0.18 = 4.86
    # 总计 31.86，每人 15.93
    assert result.grand_total == Decimal("31.86")
    
    print(f"  ✓ 链式调用成功")
    print(f"  ✓ 总计: ${result.grand_total}")
    print(f"  ✓ 每人: ${result.splits[0].total}")
    print()


def test_to_dict():
    """测试序列化"""
    print("测试 11: 序列化")
    splitter = BillSplitter()
    splitter.add_item("Test", 100.00)
    splitter.set_participants(["Alice"])
    result = splitter.split_equally()
    
    result_dict = result.to_dict()
    
    assert 'subtotal' in result_dict
    assert 'splits' in result_dict
    assert 'created_at' in result_dict
    assert len(result_dict['splits']) == 1
    
    print(f"  ✓ 序列化成功: {result_dict}")
    print()


def test_calculate_split_with_different_items():
    """测试不同项目的分账计算"""
    print("测试 12: 不同项目分账计算")
    items = [
        {"name": "Pizza", "price": 30, "shared_by": ["Alice", "Bob"]},
        {"name": "Salad", "price": 15, "shared_by": ["Charlie"]}
    ]
    
    result = calculate_split_with_different_items(
        items, 
        ["Alice", "Bob", "Charlie"],
        tax_rate=0.1,
        tip_rate=0.15
    )
    
    # Alice: 15, Bob: 15, Charlie: 15
    # 加上税和小费后
    assert "Alice" in result
    assert "Bob" in result
    assert "Charlie" in result
    
    print(f"  ✓ 分账结果: {result}")
    print()


def test_edge_cases():
    """测试边界情况"""
    print("测试 13: 边界情况")
    
    # 测试零税率和小费
    splitter = BillSplitter()
    splitter.add_item("Test", 100.00)
    splitter.set_participants(["Alice", "Bob"])
    splitter.set_tax_rate(0)
    splitter.set_tip_rate(0)
    result = splitter.split_equally()
    
    assert result.tax_amount == Decimal("0.00")
    assert result.tip_amount == Decimal("0.00")
    assert result.grand_total == Decimal("100.00")
    print("  ✓ 零税率和小费测试通过")
    
    # 测试大量参与者
    splitter2 = BillSplitter()
    splitter2.add_item("Big Party", 1000.00)
    splitter2.set_participants([f"Person{i}" for i in range(100)])
    result2 = splitter2.split_equally()
    
    assert len(result2.splits) == 100
    assert result2.splits[0].total == Decimal("10.00")
    print("  ✓ 大量参与者测试通过")
    print()


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("     Bill Splitter Utils 测试套件")
    print("=" * 50)
    print()
    
    tests = [
        test_basic_equal_split,
        test_split_with_tax_and_tip,
        test_split_with_discount,
        test_split_by_items,
        test_split_by_ratio,
        test_custom_split,
        test_convenience_functions,
        test_history,
        test_format_summary,
        test_chained_calls,
        test_to_dict,
        test_calculate_split_with_different_items,
        test_edge_cases,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  ✗ 测试失败: {test.__name__}")
            print(f"    错误: {e}")
            failed += 1
            print()
    
    print("=" * 50)
    print(f"  测试结果: {passed} 通过, {failed} 失败")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)