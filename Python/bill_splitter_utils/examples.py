"""
Bill Splitter Utils 使用示例

展示账单分账、小费计算等功能的使用方法
"""

from mod import (
    BillSplitter,
    split_bill_equally,
    calculate_tip,
    suggest_tip,
    split_with_tip,
    format_currency,
    parse_currency,
    calculate_split_with_different_items
)


def example_basic_split():
    """
    示例 1: 基本均分
    
    三个人聚餐，账单总额 120 元，均分
    """
    print("=" * 50)
    print("示例 1: 基本均分")
    print("=" * 50)
    
    splitter = BillSplitter(currency_symbol="¥")
    splitter.add_item("火锅", 60.00)
    splitter.add_item("饮料", 30.00)
    splitter.add_item("小菜", 30.00)
    splitter.set_participants(["张三", "李四", "王五"])
    
    result = splitter.split_equally()
    print(splitter.format_summary(result))


def example_with_tax_and_tip():
    """
    示例 2: 含税和小费的分账
    
    餐厅用餐，需要加税和小费
    """
    print("=" * 50)
    print("示例 2: 含税和小费")
    print("=" * 50)
    
    splitter = BillSplitter(currency_symbol="$")
    splitter.add_item("Steak", 45.00)
    splitter.add_item("Wine", 30.00)
    splitter.add_item("Dessert", 15.00)
    splitter.set_participants(["Alice", "Bob"])
    splitter.set_tax_rate(0.10)   # 10% 税
    splitter.set_tip_rate(0.18)   # 18% 小费
    
    result = splitter.split_equally()
    print(splitter.format_summary(result))


def example_with_discount():
    """
    示例 3: 含折扣的分账
    
    使用优惠券后的分账
    """
    print("=" * 50)
    print("示例 3: 含折扣")
    print("=" * 50)
    
    splitter = BillSplitter(currency_symbol="¥")
    splitter.add_item("套餐A", 100.00)
    splitter.add_item("套餐B", 80.00)
    splitter.set_participants(["小明", "小红"])
    splitter.set_discount(30.00)   # 30 元折扣
    splitter.set_tip_rate(0.10)
    
    result = splitter.split_equally()
    print(splitter.format_summary(result))


def example_split_by_items():
    """
    示例 4: 按项目分账
    
    每个人点了不同的菜品，按各自消费分账
    """
    print("=" * 50)
    print("示例 4: 按项目分账")
    print("=" * 50)
    
    splitter = BillSplitter(currency_symbol="¥")
    # Pizza 两个人分享
    splitter.add_item("Pizza", 60.00, shared_by=["Alice", "Bob"])
    # Pasta 只有 Charlie 吃
    splitter.add_item("Pasta", 40.00, shared_by=["Charlie"])
    # Salad 三个人都吃
    splitter.add_item("Salad", 30.00, shared_by=["Alice", "Bob", "Charlie"])
    
    splitter.set_participants(["Alice", "Bob", "Charlie"])
    splitter.set_tip_rate(0.10)
    
    result = splitter.split_by_items()
    print(splitter.format_summary(result))
    
    # 验证计算
    print("\n计算明细:")
    print("Pizza (¥60): Alice ¥30 + Bob ¥30")
    print("Pasta (¥40): Charlie ¥40")
    print("Salad (¥30): Alice ¥10 + Bob ¥10 + Charlie ¥10")
    print("小计: Alice ¥40, Bob ¥40, Charlie ¥50")


def example_split_by_ratio():
    """
    示例 5: 按比例分账
    
    根据收入比例或其他规则分账
    """
    print("=" * 50)
    print("示例 5: 按比例分账")
    print("=" * 50)
    
    splitter = BillSplitter(currency_symbol="¥")
    splitter.add_item("聚餐费用", 500.00)
    splitter.set_participants(["老板", "员工A", "员工B"])
    splitter.set_tip_rate(0.10)
    
    # 老板付 60%，员工A 付 25%，员工B 付 15%
    ratios = {"老板": 60, "员工A": 25, "员工B": 15}
    result = splitter.split_by_ratio(ratios)
    print(splitter.format_summary(result))


def example_quick_functions():
    """
    示例 6: 快捷函数
    
    使用便捷函数快速计算
    """
    print("=" * 50)
    print("示例 6: 快捷函数")
    print("=" * 50)
    
    # 快速均分
    print("\n6人聚餐，账单 ¥600:")
    result = split_bill_equally(600, 6, tax_rate=0.06, tip_rate=0.10)
    print(f"  小计: ¥{result['subtotal']}")
    print(f"  税费(6%): ¥{result['tax']}")
    print(f"  小费(10%): ¥{result['tip']}")
    print(f"  总计: ¥{result['total']}")
    print(f"  每人: ¥{result['per_person']}")
    
    # 计算小费
    print("\n账单 ¥100 的小费建议:")
    suggestions = suggest_tip(100)
    for rate, tip in suggestions.items():
        print(f"  {rate}: ¥{tip}")
    
    # 含小费的人均金额
    print("\n账单 ¥200，4人，小费 15%:")
    per_person = split_with_tip(200, 4, 0.15)
    print(f"  每人应付: ¥{per_person}")


def example_different_items():
    """
    示例 7: 不同项目分账计算
    
    使用便捷函数快速分账
    """
    print("=" * 50)
    print("示例 7: 不同项目分账计算")
    print("=" * 50)
    
    items = [
        {"name": "Beer", "price": 50, "shared_by": ["张三", "李四"]},
        {"name": "Juice", "price": 20, "shared_by": ["王五"]},
        {"name": "Snacks", "price": 30, "shared_by": ["张三", "李四", "王五"]}
    ]
    
    result = calculate_split_with_different_items(
        items,
        ["张三", "李四", "王五"],
        tax_rate=0.06,
        tip_rate=0.10
    )
    
    print("分账结果:")
    for name, amount in result.items():
        print(f"  {name}: ¥{amount:.2f}")


def example_currency_formatting():
    """
    示例 8: 货币格式化和解析
    """
    print("=" * 50)
    print("示例 8: 货币格式化和解析")
    print("=" * 50)
    
    # 格式化
    amounts = [123.45, 1000.00, 0.99]
    for amount in amounts:
        print(f"  {amount} -> {format_currency(amount, '¥')}")
    
    # 解析
    currencies = ["¥123.45", "$100", "€50.00", "¥1,000"]
    print("\n解析货币字符串:")
    for currency in currencies:
        print(f"  '{currency}' -> {parse_currency(currency)}")


def example_chained_calls():
    """
    示例 9: 链式调用
    
    使用链式调用简化代码
    """
    print("=" * 50)
    print("示例 9: 式调用")
    print("=" * 50)
    
    result = (BillSplitter(currency_symbol="¥")
              .add_item("午餐", 50.00)
              .add_item("咖啡", 20.00)
              .set_participants(["甲", "乙", "丙"])
              .set_tax_rate(0.06)
              .set_tip_rate(0.10)
              .split_equally())
    
    print(f"总计: ¥{result.grand_total}")
    for split in result.splits:
        print(f"{split.person_name}: ¥{split.total}")


def main():
    """运行所有示例"""
    print("\n")
    print("█" * 50)
    print("  Bill Splitter Utils 使用示例")
    print("█" * 50)
    print("\n")
    
    example_basic_split()
    example_with_tax_and_tip()
    example_with_discount()
    example_split_by_items()
    example_split_by_ratio()
    example_quick_functions()
    example_different_items()
    example_currency_formatting()
    example_chained_calls()
    
    print("\n")
    print("█" * 50)
    print("  所有示例完成!")
    print("█" * 50)


if __name__ == "__main__":
    main()