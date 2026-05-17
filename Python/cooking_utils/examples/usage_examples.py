#!/usr/bin/env python3
"""
Cooking Utils 使用示例

展示烹饪工具的各种功能。
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mod


def example_temperature():
    """温度转换示例"""
    print("\n=== 温度转换示例 ===")
    
    print("常见烘焙温度:")
    temps = mod.get_common_temperatures()
    for name, (c, f) in temps.items():
        print(f"  {name}: {c}°C = {f}°F")
    
    print("\n温度转换:")
    print(f"  180°C = {mod.celsius_to_fahrenheit(180)}°F")
    print(f"  350°F = {mod.fahrenheit_to_celsius(350)}°C")
    print(f"  -40°C = {mod.celsius_to_fahrenheit(-40)}°F (等温点)")


def example_weight():
    """重量转换示例"""
    print("\n=== 重量转换示例 ===")
    
    print("克 ↔ 盎司:")
    print(f"  500克 = {mod.grams_to_ounces(500):.2f}盎司")
    print(f"  8盎司 = {mod.ounces_to_grams(8):.2f}克")
    
    print("\n克 ↔ 磅:")
    print(f"  1000克 = {mod.grams_to_pounds(1000):.2f}磅")
    print(f"  2磅 = {mod.pounds_to_grams(2):.2f}克")
    
    print("\n千克 ↔ 磅:")
    print(f"  1千克 = {mod.kilograms_to_pounds(1):.2f}磅")


def example_volume():
    """容积转换示例"""
    print("\n=== 容积转换示例 ===")
    
    print("杯 ↔ 毫升:")
    print(f"  1杯 = {mod.cups_to_milliliters(1)}毫升")
    print(f"  0.5杯 = {mod.cups_to_milliliters(0.5)}毫升")
    
    print("\n汤匙 ↔ 毫升:")
    print(f"  2汤匙 = {mod.tablespoons_to_milliliters(2)}毫升")
    
    print("\n茶匙 ↔ 毫升:")
    print(f"  1茶匙 = {mod.teaspoons_to_milliliters(1)}毫升")
    print(f"  3茶匙 = {mod.teaspoons_to_milliliters(3)}毫升 (相当于1汤匙)")


def example_baking():
    """烘焙计算示例"""
    print("\n=== 烘焙计算示例 ===")
    
    print("烘焙蛋糕 (180°C):")
    cake_info = mod.calculate_baking_time(180, mod.TemperatureUnit.CELSIUS, "蛋糕")
    print(f"  烤箱温度: {cake_info['oven_temp_celsius']}°C / {cake_info['oven_temp_fahrenheit']}°F")
    print(f"  建议时间: {cake_info['min_time_minutes']}-{cake_info['max_time_minutes']}分钟")
    
    print("\n烤箱预热时间:")
    print(f"  100°C: {mod.get_oven_preheat_time(100)}分钟")
    print(f"  175°C: {mod.get_oven_preheat_time(175)}分钟")
    print(f"  250°C: {mod.get_oven_preheat_time(250)}分钟")


def example_food_storage():
    """食物保存示例"""
    print("\n=== 食物保存指南 ===")
    
    foods = ["生肉", "鸡蛋", "蔬菜", "面包", "米饭"]
    for food in foods:
        info = mod.get_food_storage_info(food)
        print(f"\n{food}:")
        if "冷藏" in info:
            print(f"  冷藏: {info['冷藏']}")
        if "冷冻" in info:
            print(f"  冷冻: {info['冷冻']}")
        if "注意事项" in info:
            print(f"  注意: {info['注意事项']}")


def example_substitutes():
    """食材替代示例"""
    print("\n=== 食材替代建议 ===")
    
    ingredients = ["鸡蛋", "黄油", "白糖"]
    for ing in ingredients:
        print(f"\n{ing}的替代:")
        subs = mod.get_ingredient_substitutes(ing)
        for sub in subs[:2]:  # 只显示前2个
            if "替代" in sub:
                print(f"  - {sub['替代']}: {sub['比例']}")


def example_cooking_terms():
    """烹饪术语示例"""
    print("\n=== 烹饪术语词典 ===")
    
    terms = ["焯水", "爆香", "勾芡", "收汁"]
    for term in terms:
        defn = mod.get_cooking_term_definition(term)
        print(f"{term}: {defn['定义']}")


def example_heat_levels():
    """火候控制示例"""
    print("\n=== 火候控制指南 ===")
    
    guide = mod.get_heat_level_guide()
    for level, info in guide.items():
        print(f"\n{level}:")
        print(f"  温度: {info['温度']}")
        print(f"  适用: {info['适用']}")
    
    print("\n火候推荐:")
    dishes = ["炒菜", "炖汤", "煎蛋", "炒青菜"]
    for dish in dishes:
        rec = mod.recommend_heat_level(dish)
        print(f"  {dish}: {rec['火候']} - {rec['说明']}")


def example_recipe_scaling():
    """食谱缩放示例"""
    print("\n=== 食谱缩放示例 ===")
    
    print("原食谱为2人份:")
    ingredients = {"面粉": 200, "糖": 100, "鸡蛋": 2, "牛奶": 120}
    
    print("\n缩放为4人份:")
    for name, amount in ingredients.items():
        scaled = mod.recipe_scale(amount, 2, 4)
        print(f"  {name}: {amount} -> {scaled}")
    
    print("\n缩放为3人份:")
    for name, amount in ingredients.items():
        scaled = mod.recipe_scale(amount, 2, 3)
        print(f"  {name}: {amount} -> {scaled}")


def example_water_ratio():
    """米水比例示例"""
    print("\n=== 米水比例计算 ===")
    
    rice_types = ["普通米", "糙米", "糯米", "香米"]
    for rice in rice_types:
        ratio = mod.calculate_cooking_water_ratio(rice)
        print(f"  {rice}: 水米比 {ratio['比例']} - {ratio['说明']}")


def example_quick_convert():
    """快速转换示例"""
    print("\n=== 快速转换示例 ===")
    
    print("一站式转换:")
    print(f"  180°C -> °F: {mod.quick_convert(180, 'temperature', 'celsius', 'fahrenheit')}")
    print(f"  500克 -> 磅: {mod.quick_convert(500, 'weight', 'gram', 'pound'):.2f}")
    print(f"  1杯 -> 毫升: {mod.quick_convert(1, 'volume', 'cup', 'milliliter')}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("Cooking Utils 使用示例")
    print("=" * 60)
    
    example_temperature()
    example_weight()
    example_volume()
    example_baking()
    example_food_storage()
    example_substitutes()
    example_cooking_terms()
    example_heat_levels()
    example_recipe_scaling()
    example_water_ratio()
    example_quick_convert()
    
    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()