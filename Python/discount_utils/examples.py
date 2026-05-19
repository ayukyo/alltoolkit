#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Discount Utilities Examples
==========================================
实际应用场景示例。
"""

from mod import (
    # Enums
    DiscountType, StackStrategy, TaxTiming,
    # Data classes
    Discount, TieredDiscount, BundleDiscount,
    # Functions
    apply_percentage_discount,
    apply_discount_with_strategy,
    apply_tiered_discount,
    suggest_upgrade_for_tier,
    apply_buy_x_get_y,
    calculate_free_items,
    calculate_bundle_savings,
    calculate_complete_breakdown,
    compare_prices,
    find_best_bulk_price,
    calculate_price_with_tax_and_discount,
    format_price,
    format_savings,
    analyze_price_history,
    is_good_deal,
    TAX_RATES,
)


def example_1_black_friday_sale():
    """
    场景1: 黑色星期五多重折扣
    
    商店在黑五期间有以下折扣：
    - 会员折扣: 10%
    - 黑五特惠: 25%
    - 优惠券: $10 (固定)
    
    如何计算最终价格？
    """
    print("\n=== 场景1: 黑色星期五多重折扣 ===")
    
    original_price = 200
    
    # 策略1: 顺序叠加折扣
    member_discount = Discount(DiscountType.PERCENTAGE, 10, '会员折扣')
    black_friday = Discount(DiscountType.PERCENTAGE, 25, '黑五特惠')
    coupon = Discount(DiscountType.FIXED, 10, '优惠券')
    
    # 先应用百分比折扣，再应用固定折扣
    price_after_percent = apply_discount_with_strategy(
        original_price,
        [member_discount, black_friday],
        StackStrategy.SEQUENTIAL
    )
    # 200 - 10% = 180, 180 - 25% = 135
    print(f"顺序折扣后: ${price_after_percent}")
    
    # 再减去固定折扣
    final_price = max(0, price_after_percent - coupon.value)
    print(f"应用优惠券后: ${final_price}")
    
    savings = original_price - final_price
    savings_percent = (savings / original_price) * 100
    print(f"总节省: ${savings} ({savings_percent:.1f}%)")


def example_2_bulk_purchase_tiered():
    """
    场景2: 批量采购阶梯折扣
    
    供应商提供阶梯折扣：
    - $1000+: 5%
    - $5000+: 10%
    - $10000+: 15%
    - $50000+: 20%
    
    采购经理想购买$8000的货物，如何计算折扣？
    """
    print("\n=== 场景2: 批量采购阶梯折扣 ===")
    
    tiers = TieredDiscount([
        (1000, 5),
        (5000, 10),
        (10000, 15),
        (50000, 20),
    ], '采购折扣')
    
    purchase_amount = 8000
    
    discounted = apply_tiered_discount(purchase_amount, tiers)
    print(f"原价: ${purchase_amount}")
    print(f"折扣后: ${discounted}")
    print(f"节省: ${purchase_amount - discounted}")
    
    # 建议: 加多少可以到下一档？
    suggestion = suggest_upgrade_for_tier(purchase_amount, tiers)
    if suggestion:
        additional, next_discount = suggestion
        additional_discount_amount = (purchase_amount + additional) * (next_discount / 100) - discounted
        print(f"\n建议: 增加 ${additional} 可达到 {next_discount}% 折扣档")
        print(f"额外节省: 约 ${additional_discount_amount}")
    
    # 如果是 $12000 的采购
    larger_purchase = 12000
    larger_discounted = apply_tiered_discount(larger_purchase, tiers)
    print(f"\n${larger_purchase} 采购折扣后: ${larger_discounted}")


def example_3_bundle_promotion():
    """
    场景3: 捆绑销售促销
    
    电子产品套餐：
    - 笔记本电脑: $800
    - 鼠标: $30
    - 键盘: $50
    - 转接头: $20
    
    套餐价: $880
    
    是否划算？
    """
    print("\n=== 场景3: 捆绑销售促销 ===")
    
    bundle = BundleDiscount([
        ('笔记本电脑', 800),
        ('鼠标', 30),
        ('键盘', 50),
        ('转接头', 20),
    ], 880, '开学季套餐')
    
    savings = calculate_bundle_savings(bundle)
    
    print(f"单独购买总价: ${savings['original_total']}")
    print(f"套餐价: ${savings['bundle_price']}")
    print(f"节省: ${savings['savings']} ({savings['savings_percent']}%)")
    
    if savings['savings_percent'] > 10:
        print("✅ 推荐购买套餐，节省超过10%")
    else:
        print("⚠️ 套餐折扣不大，考虑单独购买")


def example_4_buy2_get1_free():
    """
    场景4: 买二送一
    
    餐厅促销: 买2份主餐送1份免费
    主餐单价 $25
    
    顾客要买5份，如何计算？
    """
    print("\n=== 场景4: 买二送一 ===")
    
    unit_price = 25
    quantity = 5
    buy_x = 2
    get_y = 1
    
    # 常规计算 (无促销)
    regular_total = unit_price * quantity
    print(f"无促销总价: ${regular_total}")
    
    # 促销价格
    promo_total = apply_buy_x_get_y(unit_price, quantity, buy_x, get_y)
    print(f"促销总价: ${promo_total}")
    
    free_items = calculate_free_items(quantity, buy_x, get_y)
    print(f"免费获得: {free_items}份")
    print(f"实际付费: {quantity - free_items}份")
    
    savings = regular_total - promo_total
    print(f"节省: ${savings} ({(savings/regular_total)*100:.1f}%)")


def example_5_price_comparison():
    """
    场景5: 跨平台价格比较
    
    同一款手机在不同平台的价格：
    - 淘宝: $3999, 有5%优惠券
    - 京东: $3899, 无优惠券
    - 官网: $3999, 有会员价10%折扣
    
    哪个最便宜？
    """
    print("\n=== 场景5: 跨平台价格比较 ===")
    
    comparison = compare_prices([
        ('淘宝', 3999, 5),
        ('京东', 3899, 0),
        ('官网', 3999, 10),
    ])
    
    print(f"各平台价格对比:")
    for source, original, discount, final in comparison['all_options']:
        print(f"  {source}: 原价${original} 折扣{discount}% → ${final}")
    
    print(f"\n✅ 最优惠: {comparison['best_source']} 价格 ${comparison['best_price']}")
    print(f"   相比最贵平台 ({comparison['worst_source']}) 节省 ${comparison['savings_vs_worst']}")


def example_6_tax_calculation():
    """
    场景6: 含税价格计算
    
    美国加州销售，税率 7.25%
    商品原价 $100，折扣 20%
    
    税是在折扣前还是折扣后计算？
    """
    print("\n=== 场景6: 含税价格计算 ===")
    
    original_price = 100
    discount_percent = 20
    tax_rate = TAX_RATES['US_CA']  # 7.25%
    
    # 方式1: 折扣后计算税（美国常见）
    result_after = calculate_price_with_tax_and_discount(
        original_price, discount_percent, tax_rate, TaxTiming.AFTER_DISCOUNT
    )
    
    print("方式1: 先折扣，后加税")
    print(f"  原价: ${result_after['original']}")
    print(f"  折扣: -${result_after['discount_amount']}")
    print(f"  小计: ${result_after['subtotal']}")
    print(f"  税费: +${result_after['tax']:.2f}")
    print(f"  总计: ${result_after['final']:.2f}")
    
    # 方式2: 税前折扣
    result_before = calculate_price_with_tax_and_discount(
        original_price, discount_percent, tax_rate, TaxTiming.BEFORE_DISCOUNT
    )
    
    print("\n方式2: 先加税，后折扣")
    print(f"  原价含税: ${result_before['subtotal']}")
    print(f"  折扣后: ${result_before['final']:.2f}")


def example_7_price_history_analysis():
    """
    场景7: 价格历史分析
    
    用户想买一台相机，当前价格 $800
    过去几个月的价格走势：
    - 2024-01: $900
    - 2024-02: $850
    - 2024-03: $850
    - 2024-04: $780
    - 2024-05: $820
    
    现在是好时机吗？
    """
    print("\n=== 场景7: 价格历史分析 ===")
    
    current_price = 800
    history = [
        ('2024-01', 900),
        ('2024-02', 850),
        ('2024-03', 850),
        ('2024-04', 780),
        ('2024-05', 820),
    ]
    
    analysis = analyze_price_history(history)
    print(f"历史价格分析:")
    print(f"  最高价: ${analysis['highest']}")
    print(f"  最低价: ${analysis['lowest']}")
    print(f"  平均价: ${analysis['average']}")
    print(f"  波动范围: ${analysis['range']} ({analysis['range_percent']}%)")
    print(f"  趋势: {analysis['trend']}")
    
    deal_check = is_good_deal(current_price, history, threshold_percent=10)
    print(f"\n当前价格 $800 分析:")
    print(f"  相比平均: 节省 {deal_check['savings_vs_avg']}%")
    if deal_check['is_best_price']:
        print("  ✅ 这是历史最低价！强烈推荐购买")
    elif deal_check['is_good_deal']:
        print("  ✅ 这是好价格，值得购买")
    else:
        print("  ⚠️ 价格不算优惠，可以考虑等待")


def example_8_bulk_pricing():
    """
    场景8: 批量定价选择
    
    云服务提供商的存储定价：
    - 1TB: $100/月
    - 5TB: $400/月
    - 10TB: $700/月
    - 50TB: $3000/月
    
    哪个方案单价最便宜？
    """
    print("\n=== 场景8: 批量定价选择 ===")
    
    options = [
        (1, 100),
        (5, 400),
        (10, 700),
        (50, 3000),
    ]
    
    best = find_best_bulk_price(options)
    
    print("各方案单价:")
    for quantity, price in options:
        unit_price = price / quantity
        print(f"  {quantity}TB: ${price}/月 → ${unit_price}/TB/月")
    
    print(f"\n✅ 最优方案: {best[0]}TB 总价 ${best[1]} 单价 ${best[2]}/TB/月")


def main():
    """运行所有示例。"""
    print("=" * 60)
    print("折扣计算工具 - 实际应用场景示例")
    print("=" * 60)
    
    example_1_black_friday_sale()
    example_2_bulk_purchase_tiered()
    example_3_bundle_promotion()
    example_4_buy2_get1_free()
    example_5_price_comparison()
    example_6_tax_calculation()
    example_7_price_history_analysis()
    example_8_bulk_pricing()
    
    print("\n" + "=" * 60)
    print("更多功能请查看 README.md 和 mod.py")
    print("=" * 60)


if __name__ == '__main__':
    main()