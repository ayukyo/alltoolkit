"""
Cocktail Utils 使用示例

演示鸡尾酒配方库的主要功能
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cocktail_utils.mod import (
    get_all_cocktails,
    get_cocktail_by_name,
    search_cocktails,
    get_cocktails_by_spirit,
    get_cocktails_by_flavor,
    get_random_cocktail,
    get_cocktails_by_abv_range,
    get_easy_cocktails,
    generate_shopping_list,
    format_shopping_list,
    calculate_abv,
    get_abv_description,
    convert_volume,
    format_recipe,
    suggest_similar_cocktails,
    get_iba_cocktails,
    estimate_drinks_for_party,
    get_pairing_suggestion,
    get_statistics,
    SpiritType,
    Flavor,
    GlassType,
)


def example_basic_search():
    """示例：基本搜索"""
    print("=" * 60)
    print("🍹 示例 1: 基本搜索")
    print("=" * 60)
    
    # 按名称搜索
    martini = get_cocktail_by_name("Martini")
    print(f"\n搜索 'Martini': {martini.name_zh}")
    
    # 中文搜索
    mojito = get_cocktail_by_name("莫吉托")
    print(f"搜索 '莫吉托': {mojito.name}")
    
    # 部分名称搜索
    results = search_cocktails("vodka")
    print(f"\n搜索 'vodka' 找到 {len(results)} 个鸡尾酒:")
    for c in results[:5]:
        print(f"  - {c.name_zh} ({c.name})")


def example_filter_by_spirit():
    """示例：按基酒筛选"""
    print("\n" + "=" * 60)
    print("🥃 示例 2: 按基酒筛选")
    print("=" * 60)
    
    # 烈酒统计
    for spirit in [SpiritType.VODKA, SpiritType.GIN, SpiritType.RUM, 
                   SpiritType.WHISKEY, SpiritType.TEQUILA]:
        results = get_cocktails_by_spirit(spirit)
        print(f"\n{spirit.value} 尾酒 ({len(results)} 个):")
        for c in results[:3]:
            print(f"  - {c.name_zh}")


def example_filter_by_flavor():
    """示例：按口味筛选"""
    print("\n" + "=" * 60)
    print("👅 示例 3: 按口味筛选")
    print("=" * 60)
    
    flavors = [Flavor.SWEET, Flavor.SOUR, Flavor.BITTER, Flavor.SPICY]
    for flavor in flavors:
        results = get_cocktails_by_flavor(flavor)
        print(f"\n{flavor.value} 口味 ({len(results)} 个):")
        for c in results[:2]:
            print(f"  - {c.name_zh}")


def example_random_cocktail():
    """示例：随机推荐"""
    print("\n" + "=" * 60)
    print("🎲 示例 4: 随机推荐")
    print("=" * 60)
    
    # 随机一个
    random_one = get_random_cocktail()
    print(f"\n今日推荐: {random_one.name_zh}")
    print(format_recipe(random_one))


def example_abv_range():
    """示例：按酒精度筛选"""
    print("\n" + "=" * 60)
    print("🍺 示例 5: 按酒精度筛选")
    print("=" * 60)
    
    # 低度鸡尾酒 (< 15%)
    low_abv = get_cocktails_by_abv_range(0, 15)
    print(f"\n低度鸡尾酒 (< 15%, {len(low_abv)} 个):")
    for c in low_abv[:3]:
        print(f"  - {c.name_zh}: {c.abv}%")
    
    # 高度鸡尾酒 (> 30%)
    high_abv = get_cocktails_by_abv_range(30, 50)
    print(f"\n高度鸡尾酒 (> 30%, {len(high_abv)} 个):")
    for c in high_abv[:3]:
        print(f"  - {c.name_zh}: {c.abv}% {get_abv_description(c.abv)}")


def example_shopping_list():
    """示例：购物清单"""
    print("\n" + "=" * 60)
    print("🛒 示例 6: 购物清单生成")
    print("=" * 60)
    
    # 为派对准备多种鸡尾酒
    cocktails = [
        get_cocktail_by_name("Mojito"),
        get_cocktail_by_name("Daiquiri"),
        get_cocktail_by_name("Piña Colada"),
    ]
    
    print("\n准备鸡尾酒:")
    for c in cocktails:
        print(f"  - {c.name_zh}")
    
    shopping = generate_shopping_list(cocktails)
    print(format_shopping_list(shopping, servings=5))


def example_volume_conversion():
    """示例：容量转换"""
    print("\n" + "=" * 60)
    print("📏 示例 7: 容量转换")
    print("=" * 60)
    
    # 常见转换
    conversions = [
        (60, "ml", "oz"),  # 标准烈酒量
        (1, "oz", "ml"),
        (1.5, "oz", "ml"),  # Jigger
        (1000, "ml", "l"),
        (15, "ml", "tsp"),
    ]
    
    print("\n常见容量转换:")
    for amount, from_unit, to_unit in conversions:
        result = convert_volume(amount, from_unit, to_unit)
        print(f"  {amount} {from_unit} = {result} {to_unit}")


def example_similar_cocktails():
    """示例：相似推荐"""
    print("\n" + "=" * 60)
    print("🎯 示例 8: 相似鸡尾酒推荐")
    print("=" * 60)
    
    cocktail = get_cocktail_by_name("Negroni")
    print(f"\n如果你喜欢 {cocktail.name_zh}，你可能也会喜欢:")
    
    similar = suggest_similar_cocktails(cocktail)
    for c, score in similar[:5]:
        print(f"  - {c.name_zh} (相似度: {score:.2f})")


def example_party_estimate():
    """示例：派对估算"""
    print("\n" + "=" * 60)
    print("🎉 示例 9: 派对估算")
    print("=" * 60)
    
    # 估算不同规模的派对
    parties = [
        (10, 2, "小型派对"),
        (50, 3, "中型派对"),
        (100, 4, "大型派对"),
    ]
    
    for people, hours, desc in parties:
        estimate = estimate_drinks_for_party(people, hours)
        print(f"\n{desc} ({people}人, {hours}小时):")
        print(f"  总饮品数: {estimate['total_drinks']}")
        print(f"  总容量: {estimate['total_liters']} 升")
        print(f"  建议准备 {estimate['suggested_cocktails']} 种不同鸡尾酒")


def example_pairing():
    """示例：菜品配对"""
    print("\n" + "=" * 60)
    print("🍽️ 示例 10: 菜品配对")
    print("=" * 60)
    
    dishes = ["seafood", "meat", "spicy", "dessert", "mexican"]
    for dish in dishes:
        results = get_pairing_suggestion(dish)
        print(f"\n{dish} 配对推荐 ({len(results)} 个):")
        for c in results[:3]:
            print(f"  - {c.name_zh}")


def example_statistics():
    """示例：数据库统计"""
    print("\n" + "=" * 60)
    print("📊 示例 11: 数据库统计")
    print("=" * 60)
    
    stats = get_statistics()
    
    print(f"\n总鸡尾酒数: {stats['total_cocktails']}")
    print(f"IBA 官方鸡尾酒: {stats['iba_cocktails']}")
    print(f"平均酒精度: {stats['avg_abv']}%")
    
    print("\n基酒分布:")
    for spirit, count in sorted(stats['spirits_distribution'].items(), 
                                 key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {spirit}: {count}")
    
    print("\n酒杯类型分布:")
    for glass, count in sorted(stats['glasses_distribution'].items(), 
                                key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {glass}: {count}")


def example_easy_cocktails():
    """示例：简单易做鸡尾酒"""
    print("\n" + "=" * 60)
    print("⭐ 示例 12: 简单易做鸡尾酒")
    print("=" * 60)
    
    easy = get_easy_cocktails()
    print(f"\n简单易做的鸡尾酒 ({len(easy)} 个, 难度 <= 2):")
    for c in easy[:5]:
        print(f"  - {c.name_zh} (难度: {'⭐' * c.difficulty})")


def example_recipe_format():
    """示例：完整配方"""
    print("\n" + "=" * 60)
    print("📝 示例 13: 完整配方格式")
    print("=" * 60)
    
    cocktail = get_cocktail_by_name("Margarita")
    print(format_recipe(cocktail))


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("🍹 Cocktail Utils 使用示例")
    print("=" * 60)
    
    example_basic_search()
    example_filter_by_spirit()
    example_filter_by_flavor()
    example_random_cocktail()
    example_abv_range()
    example_shopping_list()
    example_volume_conversion()
    example_similar_cocktails()
    example_party_estimate()
    example_pairing()
    example_statistics()
    example_easy_cocktails()
    example_recipe_format()
    
    print("\n" + "=" * 60)
    print("✅ 所有示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()