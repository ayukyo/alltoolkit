"""
Coffee Utils 示例 - 高级用法

展示咖啡冲泡工具库的高级功能：产地查询、烘焙分析、水质评估

运行方式: cd Python && python -m coffee_utils.examples.advanced_usage
"""

import sys
import os
# 添加父目录到路径以便导入
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    WaterQualityAnalyzer, RoastAnalyzer, OriginInfo,
    CoffeeOrigin, RoastLevel, CaffeineCalculator, BrewRecommender,
    BREW_PARAMETERS, COFFEE_ORIGINS,
)


def main():
    print("=" * 60)
    print("Coffee Utils - 高级用法示例")
    print("=" * 60)
    
    # 1. 产地信息查询
    print("\n【1】咖啡产地信息")
    print("-" * 40)
    
    origins = [CoffeeOrigin.ETHIOPIA, CoffeeOrigin.KENYA, CoffeeOrigin.BRAZIL]
    for origin in origins:
        info = OriginInfo.get_origin_info(origin)
        print(f"\n{info.name}:")
        print(f"  海拔范围: {info.altitude_range[0]}-{info.altitude_range[1]}m")
        print(f"  风味特征: {', '.join(info.flavor_notes)}")
        print(f"  酸度: {info.acidity}")
        print(f"  醇厚度: {info.body}")
        print(f"  处理方式: {', '.join(info.processing)}")
    
    # 2. 按风味搜索产地
    print("\n【2】按风味特征搜索产地")
    print("-" * 40)
    
    flavors = ["巧克力", "花香", "水果", "坚果"]
    for flavor in flavors:
        origins = OriginInfo.search_by_flavor(flavor)
        names = [COFFEE_ORIGINS[o].name for o in origins]
        print(f"{flavor}风味: {', '.join(names)}")
    
    # 3. 按酸度搜索
    print("\n【3】按酸度等级搜索产地")
    print("-" * 40)
    
    acidity_levels = ["高", "中", "低"]
    for level in acidity_levels:
        origins = OriginInfo.search_by_acidity(level)
        names = [COFFEE_ORIGINS[o].name for o in origins]
        print(f"{level}酸度: {', '.join(names)}")
    
    # 4. 烘焙程度分析
    print("\n【4】烘焙程度特性分析")
    print("-" * 40)
    
    roast_levels = [RoastLevel.LIGHT, RoastLevel.MEDIUM, RoastLevel.DARK]
    for level in roast_levels:
        chars = RoastAnalyzer.get_roast_characteristics(level)
        print(f"\n{level.value}:")
        print(f"  颜色: {chars['color']}")
        print(f"  表面: {chars['surface']}")
        print(f"  风味: {chars['flavor']}")
        print(f"  咖啡因: {chars['caffeine']}")
        print(f"  推荐水温: {chars['brew_temp'][0]}-{chars['brew_temp'][1]}°C")
        print(f"  风味笔记: {', '.join(chars['notes'][:4])}")
    
    # 5. 烘焙程度推荐产地
    print("\n【5】烘焙程度适合的产地")
    print("-" * 40)
    
    for level in [RoastLevel.LIGHT, RoastLevel.MEDIUM, RoastLevel.DARK]:
        origins = RoastAnalyzer.suggest_origin_for_roast(level)
        names = [COFFEE_ORIGINS[o].name for o in origins]
        print(f"{level.value}烘焙适合: {', '.join(names)}")
    
    # 6. 水质分析
    print("\n【6】水质评估")
    print("-" * 40)
    
    water_samples = [
        {"name": "理想水", "hardness": 100, "ph": 7.0, "alkalinity": 50},
        {"name": "软水", "hardness": 30, "ph": 6.5, "alkalinity": 30},
        {"name": "硬水", "hardness": 200, "ph": 8.0, "alkalinity": 100},
        {"name": "蒸馏水", "hardness": 5, "ph": 6.0, "alkalinity": 10},
    ]
    
    for sample in water_samples:
        result = WaterQualityAnalyzer.assess_water(
            sample["hardness"], 
            sample["ph"], 
            sample["alkalinity"]
        )
        print(f"\n{sample['name']} (硬度{sample['hardness']}ppm, pH{sample['ph']}):")
        print(f"  硬度: {result['hardness']['status']} - {result['hardness']['note']}")
        print(f"  pH: {result['ph']['status']} - {result['ph']['note']}")
        print(f"  整体: {result['overall']}")
        if result['suggestions']:
            print(f"  建议: {result['suggestions'][0]}")
    
    # 7. 镁含量影响
    print("\n【7】镁含量对咖啡的影响")
    print("-" * 40)
    
    hardness_values = [20, 50, 100, 150]
    for h in hardness_values:
        result = WaterQualityAnalyzer.magnesium_benefit(h)
        print(f"硬度{h}ppm: {result['magnesium_level']}")
        print(f"  效果: {result['effect']}")
        print(f"  建议: {result['recommendation']}")
    
    # 8. 咖啡因代谢计算
    print("\n【8】咖啡因代谢时间计算")
    print("-" * 40)
    
    print("假设咖啡因半衰期为5小时:")
    targets = [100, 75, 50, 25]
    current = 200  # 当前200mg
    for target in targets:
        hours = CaffeineCalculator.half_life_hours(current, target, 5.0)
        print(f"从{current}mg降到{target}mg需要 {hours} 小时")
    
    # 9. 所有冲泡方式参数汇总
    print("\n【9】所有冲泡方式参数汇总")
    print("-" * 40)
    
    for method, params in BREW_PARAMETERS.items():
        print(f"\n{method.value}:")
        print(f"  研磨: {params['grind'].value}")
        print(f"  比例: {params['ratio']}")
        print(f"  水温: {params['temperature'][0]}-{params['temperature'][1]}°C")
        print(f"  时间: {params['time'][0]}-{params['time'][1]}秒")
        print(f"  目标萃取率: {params['extraction'][0]}-{params['extraction'][1]}%")
        print(f"  目标TDS: {params['tds'][0]}-{params['tds'][1]}%")
    
    # 10. 按醇厚度搜索
    print("\n【10】按醇厚度搜索产地")
    print("-" * 40)
    
    body_levels = ["轻", "中等", "饱满"]
    for level in body_levels:
        origins = OriginInfo.search_by_body(level)
        names = [COFFEE_ORIGINS[o].name for o in origins]
        print(f"{level}醇厚度: {', '.join(names)}")


if __name__ == "__main__":
    main()