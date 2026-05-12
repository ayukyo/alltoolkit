"""
Tipping Utils 使用示例

展示小费计算工具的各种使用场景
"""

import sys
import os

# 添加父目录的父目录到路径（Python 目录）
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tipping_utils import (
    Country,
    ServiceType,
    get_tip_recommendation,
    calculate_tip,
    calculate_tip_with_tax,
    split_bill,
    split_by_items,
    round_tip,
    suggest_tip,
    calculate_percentage,
    calculate_quick_tips,
    is_tipping_customary,
    get_countries_by_tipping_culture,
    calculate_tip_range,
    calculate_tip_with_rounding,
    format_tip_summary,
    calculate_shared_tip,
    tip,
    split,
)


def example_basic_tip():
    """基本小费计算示例"""
    print("=== 基本小费计算 ===\n")
    
    # 计算 18% 小费
    calc = calculate_tip(100.0, 18.0)
    print(f"账单: $100.00")
    print(f"小费 (18%): ${calc.tip_amount:.2f}")
    print(f"总计: ${calc.total:.2f}")
    
    print("\n--- 不同比例对比 ---")
    for percent in [10, 15, 18, 20, 25]:
        calc = calculate_tip(85.50, percent)
        print(f"{percent}%: 小费 ${calc.tip_amount:.2f}, 总计 ${calc.total:.2f}")


def example_with_tax():
    """含税小费计算示例"""
    print("\n=== 含税小费计算 ===\n")
    
    bill = 100.0
    tip_percent = 18.0
    tax_percent = 8.25  # 加州税率
    
    print(f"账单: ${bill:.2f}")
    print(f"税率: {tax_percent}%")
    print(f"小费: {tip_percent}%\n")
    
    # 在税前基础上计算小费
    calc1 = calculate_tip_with_tax(bill, tip_percent, tax_percent, tip_on_pre_tax=True)
    print("【税前计算小费】")
    print(f"  小费: ${calc1.tip_amount:.2f}")
    print(f"  税金: ${calc1.tax:.2f}")
    print(f"  总计: ${calc1.grand_total:.2f}")
    
    # 在税后基础上计算小费
    calc2 = calculate_tip_with_tax(bill, tip_percent, tax_percent, tip_on_pre_tax=False)
    print("\n【税后计算小费】")
    print(f"  小费: ${calc2.tip_amount:.2f}")
    print(f"  税金: ${calc2.tax:.2f}")
    print(f"  总计: ${calc2.grand_total:.2f}")


def example_split_bill():
    """账单分割示例"""
    print("\n=== 账单分割 ===\n")
    
    # 4人均分
    print("【均分账单】")
    result = split_bill(156.80, 4, tip_percent=18.0)
    print(f"账单: ${result.subtotal:.2f}")
    print(f"小费 (18%): ${result.tip:.2f}")
    print(f"总计: ${result.total:.2f}")
    print(f"每人: ${result.per_person:.2f}")
    
    # 不均等分摊
    print("\n【按消费分摊】")
    items = [
        ("张三", 68.50),
        ("李四", 45.30),
        ("王五", 43.00),
    ]
    split_result = split_by_items(items, tip_percent=18.0)
    print(f"总计: ${sum(p for _, p in items):.2f}, 小费 18%\n")
    for name, amount in split_result.items():
        print(f"  {name}: ${amount:.2f}")


def example_country_tips():
    """各国小费文化示例"""
    print("\n=== 各国小费文化 ===\n")
    
    countries = [
        (Country.USA, "美国"),
        (Country.JAPAN, "日本"),
        (Country.FRANCE, "法国"),
        (Country.CHINA, "中国"),
        (Country.UK, "英国"),
        (Country.AUSTRALIA, "澳大利亚"),
    ]
    
    bill = 100.0
    
    for country, name in countries:
        tip_amt, note = suggest_tip(bill, country, ServiceType.RESTAURANT, "good")
        is_customary = is_tipping_customary(country, ServiceType.RESTAURANT)
        
        print(f"【{name}】")
        print(f"  建议小费: ${tip_amt:.2f}")
        print(f"  期望小费: {'是' if is_customary else '否'}")
        print(f"  说明: {note}\n")


def example_service_types():
    """不同服务类型小费示例"""
    print("\n=== 不同服务类型小费 (美国) ===\n")
    
    services = [
        ServiceType.RESTAURANT,
        ServiceType.BAR,
        ServiceType.TAXI,
        ServiceType.DELIVERY,
        ServiceType.HAIR_SALON,
        ServiceType.HOTEL,
    ]
    
    bill = 50.0
    
    for service in services:
        rec = get_tip_recommendation(Country.USA, service)
        if rec:
            tip_amt = bill * rec.standard_percent / 100
            print(f"【{service.value}】")
            print(f"  标准小费: {rec.standard_percent}% (${tip_amt:.2f})")
            print(f"  范围: {rec.min_percent}% - {rec.max_percent}%")
            print(f"  说明: {rec.notes}\n")


def example_quick_tips():
    """快速小费参考示例"""
    print("\n=== 快速小费参考表 ===\n")
    
    bills = [20.0, 50.0, 100.0, 150.0]
    
    print(f"{'账单':>8} | {'10%':>8} | {'15%':>8} | {'18%':>8} | {'20%':>8} | {'25%':>8}")
    print("-" * 60)
    
    for bill in bills:
        quick = calculate_quick_tips(bill)
        tips = [quick[p].tip_amount for p in ["10%", "15%", "18%", "20%", "25%"]]
        print(f"${bill:>7.2f} | ${tips[0]:>7.2f} | ${tips[1]:>7.2f} | ${tips[2]:>7.2f} | ${tips[3]:>7.2f} | ${tips[4]:>7.2f}")


def example_rounding():
    """小费四舍五入示例"""
    print("\n=== 小费四舍五入 ===\n")
    
    bill = 47.83
    percent = 18.0
    raw_tip = bill * percent / 100
    
    print(f"账单: ${bill:.2f}, 小费率: {percent}%")
    print(f"原始小费: ${raw_tip:.2f}\n")
    
    methods = [
        ("nearest", "四舍五入"),
        ("up", "向上取整"),
        ("down", "向下取整"),
    ]
    
    for method, name in methods:
        rounded = round_tip(raw_tip, method, 0.50)
        total = bill + rounded
        print(f"【{name}到$0.50】")
        print(f"  小费: ${rounded:.2f}")
        print(f"  总计: ${total:.2f}\n")


def example_service_quality():
    """服务质量影响小费示例"""
    print("\n=== 服务质量影响小费 ===\n")
    
    bill = 100.0
    qualities = ["poor", "average", "good", "excellent"]
    quality_names = ["差", "一般", "好", "优秀"]
    
    print("美国餐厅小费建议:\n")
    
    for quality, name in zip(qualities, quality_names):
        tip_amt, note = suggest_tip(bill, Country.USA, ServiceType.RESTAURANT, quality)
        print(f"【{name}服务】小费: ${tip_amt:.2f}")


def example_tip_range():
    """小费范围示例"""
    print("\n=== 小费范围计算 ===\n")
    
    bill = 125.50
    min_tip, max_tip = calculate_tip_range(bill, 15.0, 25.0)
    
    print(f"账单: ${bill:.2f}")
    print(f"小费范围 (15%-25%): ${min_tip:.2f} - ${max_tip:.2f}")
    print(f"总计范围: ${bill + min_tip:.2f} - ${bill + max_tip:.2f}")


def example_format_summary():
    """格式化摘要示例"""
    print("\n=== 小费格式化摘要 ===\n")
    
    # 简单摘要
    print("【简单账单】")
    print(format_tip_summary(85.50, 18.0))
    
    print("\n【含额外税金】")
    print(format_tip_summary(85.50, 18.0, tax=7.05, tax_included=False))
    
    print("\n【含已含税金】")
    print(format_tip_summary(85.50, 18.0, tax=7.05, tax_included=True))
    
    print("\n【欧元】")
    print(format_tip_summary(85.50, 15.0, currency_symbol="€"))


def example_cultural_classification():
    """小费文化分类示例"""
    print("\n=== 小费文化分类 ===\n")
    
    classification = get_countries_by_tipping_culture()
    
    print("【强小费文化】(期望给 15%+ 小费)")
    strong = [c.value for c in classification["strong"]]
    print(f"  {', '.join(strong[:5])}...\n")
    
    print("【中等小费文化】(通常给 5-15%)")
    moderate = [c.value for c in classification["moderate"]]
    print(f"  {', '.join(moderate[:5])}...\n")
    
    print("【弱小费文化】(小费可选)")
    weak = [c.value for c in classification["weak"]]
    print(f"  {', '.join(weak[:5])}...\n")
    
    print("【无小费文化】(不给小费)")
    none = [c.value for c in classification["none"]]
    print(f"  {', '.join(none[:5])}...")


def example_convenience_functions():
    """便捷函数示例"""
    print("\n=== 便捷函数 ===\n")
    
    # 快速小费计算
    tip_amt, total = tip(100.0, 20.0)
    print(f"tip(100, 20%): 小费=${tip_amt:.2f}, 总计=${total:.2f}")
    
    # 默认 18%
    tip_amt, total = tip(100.0)
    print(f"tip(100): 小费=${tip_amt:.2f}, 总计=${total:.2f}")
    
    # 快速分割
    per_person = split(100.0, 4, 20.0)
    print(f"split(100, 4人, 20%): 每人=${per_person:.2f}")
    
    # 默认 18%
    per_person = split(100.0, 4)
    print(f"split(100, 4人): 每人=${per_person:.2f}")


def example_real_scenario():
    """真实场景示例"""
    print("\n=== 真实场景: 朋友聚餐 ===\n")
    
    # 场景: 4个朋友在洛杉矶餐厅聚餐
    print("场景: 4个朋友在洛杉矶餐厅聚餐")
    print("账单金额: $186.50")
    print("加州销售税: 9.5%\n")
    
    bill = 186.50
    tax_rate = 9.5
    
    # 每个人的消费
    individual_bills = [
        ("小明", 52.30),  # 主菜 + 饮料
        ("小红", 48.90),  # 主菜 + 甜点
        ("小刚", 45.80),  # 主菜
        ("小美", 39.50),  # 沙拉 + 汤
    ]
    
    total_individual = sum(b for _, b in individual_bills)
    print(f"个人消费:")
    for name, amount in individual_bills:
        print(f"  {name}: ${amount:.2f}")
    print(f"  总计: ${total_individual:.2f}\n")
    
    # 计算税金
    tax = bill * tax_rate / 100
    print(f"税金 (9.5%): ${tax:.2f}\n")
    
    # 建议小费
    tip_suggestion, note = suggest_tip(bill, Country.USA, ServiceType.RESTAURANT, "good")
    print(f"建议小费: ${tip_suggestion:.2f}")
    print(f"说明: {note}\n")
    
    # 均分方案
    print("【均分方案】")
    result = split_bill(bill, 4, tip_percent=18.0, tax=tax, tax_included=False)
    print(f"  小费 (18%): ${result.tip:.2f}")
    print(f"  总计: ${result.total:.2f}")
    print(f"  每人: ${result.per_person:.2f}\n")
    
    # 按消费比例分摊
    print("【按消费比例分摊】")
    items = [(name, amount) for name, amount in individual_bills]
    split_result = split_by_items(items, tip_percent=18.0, tax=tax, tax_included=False)
    
    print(f"  (含 18% 小费和 9.5% 税金)")
    for name, amount in individual_bills:
        total = split_result[name]
        print(f"  {name}: ${total:.2f} (消费 ${amount:.2f})")


def main():
    """运行所有示例"""
    example_basic_tip()
    example_with_tax()
    example_split_bill()
    example_country_tips()
    example_service_types()
    example_quick_tips()
    example_rounding()
    example_service_quality()
    example_tip_range()
    example_format_summary()
    example_cultural_classification()
    example_convenience_functions()
    example_real_scenario()
    
    print("\n" + "=" * 50)
    print("示例完成！")


if __name__ == "__main__":
    main()