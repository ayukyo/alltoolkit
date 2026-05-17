"""
Coffee Utils 示例 - 基础用法

展示咖啡冲泡工具库的基本功能

运行方式: cd Python && python -m coffee_utils.examples.basic_usage
"""

import sys
import os
# 添加父目录到路径以便导入
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    CoffeeCalculator, CaffeineCalculator, BrewRecommender,
    BrewMethod, GrindSize, RoastLevel,
    calculate_ratio, estimate_caffeine, get_brew_recipe,
)


def main():
    print("=" * 60)
    print("Coffee Utils - 基础用法示例")
    print("=" * 60)
    
    # 1. 比例计算
    print("\n【1】比例计算")
    print("-" * 40)
    
    # 15g咖啡粉 + 225ml水
    ratio = calculate_ratio(15, 225)
    print(f"15g咖啡 + 225ml水 = 比例 {ratio}")
    
    # 根据水量计算咖啡粉量
    coffee_needed = CoffeeCalculator.calculate_coffee_for_water(300, "1:15")
    print(f"300ml水需要 {coffee_needed}g 咖啡粉")
    
    # 根据咖啡量计算水量
    water_needed = CoffeeCalculator.calculate_water_for_coffee(18, "1:2")
    print(f"18g咖啡粉(浓缩)需要 {water_needed}ml 水")
    
    # 2. 冲泡参数
    print("\n【2】V60 冲泡参数")
    print("-" * 40)
    
    recipe = get_brew_recipe("v60", cups=1)
    print(f"冲泡方式: {recipe['method']}")
    print(f"杯数: {recipe['cups']}")
    print(f"咖啡粉: {recipe['total_coffee_g']}g")
    print(f"水量: {recipe['total_water_ml']}ml")
    print(f"研磨度: {recipe['grind']}")
    print(f"比例: {recipe['ratio']}")
    print(f"温度: {recipe['temperature_c'][0]}-{recipe['temperature_c'][1]}°C")
    print(f"时间: {recipe['brew_time_seconds'][0]}-{recipe['brew_time_seconds'][1]}秒")
    print(f"闷蒸水量: {recipe['bloom_water_ml']}ml")
    
    # 3. 金杯标准检查
    print("\n【3】金杯标准检查")
    print("-" * 40)
    
    # 测试不同TDS值
    tds_values = [1.0, 1.2, 1.25, 1.35, 1.5]
    for tds in tds_values:
        extraction = CoffeeCalculator.calculate_extraction_yield(15, 225, tds)
        result = CoffeeCalculator.is_golden_cup(extraction, tds)
        status = "✓ 符合金杯标准" if result["is_golden_cup"] else "✗ 不符合"
        print(f"TDS {tds}%: 萃取率 {extraction}%, {status}")
    
    # 4. 研磨度详情
    print("\n【4】研磨度详细信息")
    print("-" * 40)
    
    grind = BrewRecommender.get_grind_recommendation(GrindSize.MEDIUM_FINE)
    print(f"研磨度: {grind.size.value}")
    print(f"描述: {grind.description}")
    print(f"粒径范围: {grind.particle_size_um[0]}-{grind.particle_size_um[1]}μm")
    print(f"筛网目数: {grind.mesh_size[0]}-{grind.mesh_size[1]}")
    
    # 5. 口味调整
    print("\n【5】根据口味偏好调整参数")
    print("-" * 40)
    
    base = BrewRecommender.get_brew_parameters(BrewMethod.POUR_OVER)
    print(f"标准参数: {base.coffee_grams}g 咖啡粉")
    
    stronger = BrewRecommender.adjust_for_taste(BrewMethod.POUR_OVER, "stronger")
    print(f"更浓参数: {stronger['coffee_grams']}g 咖啡粉")
    print(f"建议: {stronger['notes']}")
    
    weaker = BrewRecommender.adjust_for_taste(BrewMethod.POUR_OVER, "weaker")
    print(f"更淡参数: {weaker['coffee_grams']}g 咖啡粉")
    print(f"建议: {weaker['notes']}")
    
    # 6. 咖啡因估算
    print("\n【6】咖啡因含量估算")
    print("-" * 40)
    
    methods = ["pour_over", "espresso", "cold_brew", "french_press"]
    for method in methods:
        info = estimate_caffeine(15, method)
        print(f"{method}: {info.mg_per_cup}mg 咖啡因 ({info.sensitivity_level}敏感度)")
    
    # 7. 每日咖啡因限制
    print("\n【7】每日咖啡因摄入检查")
    print("-" * 40)
    
    consumed = 150  # 已摄入150mg
    result = CaffeineCalculator.daily_limit_check(consumed)
    print(f"已摄入: {result['consumed_mg']}mg")
    print(f"剩余可摄入: {result['remaining_mg']}mg")
    print(f"使用百分比: {result['percentage']}%")
    print(f"状态: {result['status']}")
    print(f"还能喝浓缩咖啡: {result['cups_remaining']['espresso']}杯")
    
    # 8. 闷蒸参数
    print("\n【8】闷蒸参数")
    print("-" * 40)
    
    coffee_amounts = [10, 15, 20, 25]
    for amount in coffee_amounts:
        bloom_water = CoffeeCalculator.calculate_bloom_water(amount)
        bloom_time = CoffeeCalculator.calculate_bloom_time(RoastLevel.MEDIUM)
        print(f"{amount}g咖啡粉 → 闷蒸水{bloom_water}ml, 时间{bloom_time}秒")


if __name__ == "__main__":
    main()