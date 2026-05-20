"""
recipe_utils 使用示例

展示食谱缩放、单位转换、营养计算等功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Recipe,
    Ingredient,
    RecipeStep,
    UnitType,
    IngredientCategory,
    DifficultyLevel,
    MealType,
    scale_recipe,
    convert_unit,
    get_nutrition,
    get_substitutions,
    analyze_recipe,
    generate_shopping_list,
    parse_ingredient,
    estimate_recipe_cost,
    get_common_conversions,
    get_example_recipe,
    UnitConverter,
    NutritionCalculator,
    IngredientSubstitutor,
)


def example_basic_recipe_operations():
    """基础食谱操作示例"""
    print("=" * 50)
    print("基础食谱操作")
    print("=" * 50)
    
    # 获取示例食谱
    recipe = get_example_recipe()
    print(f"\n示例食谱: {recipe.name}")
    print(f"原份数: {recipe.servings}")
    
    # 打印配料
    print("\n配料列表:")
    for ing in recipe.ingredients:
        print(f"  - {ing.amount} {ing.unit.value} {ing.name}")
    
    # 缩放食谱到4人份
    scaled = scale_recipe(recipe, 4)
    print(f"\n缩放后份数: {scaled.servings}")
    print("缩放后配料:")
    for ing in scaled.ingredients:
        print(f"  - {ing.amount} {ing.unit.value} {ing.name}")


def example_unit_conversion():
    """单位转换示例"""
    print("\n" + "=" * 50)
    print("单位转换")
    print("=" * 50)
    
    # 体积转换
    print("\n体积转换:")
    result, success = convert_unit(1, UnitType.CUP, UnitType.MILLILITER)
    print(f"  1杯 = {result:.1f}毫升")
    
    result, success = convert_unit(3, UnitType.TABLESPOON, UnitType.TEASPOON)
    print(f"  3大匙 = {result:.0f}小匙")
    
    # 重量转换
    print("\n重量转换:")
    result, success = convert_unit(1, UnitType.POUND, UnitType.GRAM)
    print(f"  1磅 = {result:.1f}克")
    
    result, success = convert_unit(500, UnitType.GRAM, UnitType.OUNCE)
    print(f"  500克 = {result:.1f}盎司")
    
    # 体积到重量（需要食材密度）
    print("\n体积到重量转换（使用密度）:")
    result, success = convert_unit(1, UnitType.CUP, UnitType.GRAM, "面粉")
    print(f"  1杯面粉 = {result:.1f}克")
    
    # 温度转换
    print("\n温度转换:")
    temp = UnitConverter.convert_temperature(180, "celsius", "fahrenheit")
    print(f"  180°C = {temp:.0f}°F")
    
    temp = UnitConverter.convert_temperature(350, "fahrenheit", "celsius")
    print(f"  350°F = {temp:.1f}°C")
    
    # 常用转换对照
    print("\n常用转换对照:")
    conversions = get_common_conversions()
    for category, items in conversions.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  {item}")


def example_nutrition_calculation():
    """营养计算示例"""
    print("\n" + "=" * 50)
    print("营养计算")
    print("=" * 50)
    
    # 单个配料营养
    print("\n单个配料营养信息:")
    ing = Ingredient("鸡蛋", 100, UnitType.GRAM)
    nutrition = get_nutrition(ing)
    print(f"  100克鸡蛋:")
    print(f"    热量: {nutrition.calories} kcal")
    print(f"    蛋白质: {nutrition.protein} g")
    print(f"    碳水: {nutrition.carbs} g")
    print(f"    脂肪: {nutrition.fat} g")
    
    # 整份食谱营养
    print("\n整份食谱营养信息:")
    recipe = get_example_recipe()
    total_nutrition = NutritionCalculator.get_recipe_nutrition(recipe)
    per_serving = NutritionCalculator.get_nutrition_per_serving(recipe)
    
    print(f"  {recipe.name} (总份数{recipe.servings}):")
    print(f"    总热量: {total_nutrition.calories:.1f} kcal")
    print(f"    每份热量: {per_serving.calories:.1f} kcal")
    print(f"    每份蛋白质: {per_serving.protein:.1f} g")


def example_ingredient_substitution():
    """配料替代示例"""
    print("\n" + "=" * 50)
    print("配料替代建议")
    print("=" * 50)
    
    # 获取替代建议
    ingredients_to_check = ["鸡蛋", "牛奶", "黄油", "面粉"]
    
    for ingredient in ingredients_to_check:
        print(f"\n{ingredient}的替代品:")
        subs = get_substitutions(ingredient)
        for sub in subs:
            print(f"  - {sub['substitute']} (比例: {sub['ratio']})")
            print(f"    提示: {sub['note']}")
    
    # 素食替代品
    print("\n素食替代品:")
    vegan_alt = IngredientSubstitutor.find_vegan_alternative("鸡蛋")
    print(f"  鸡蛋 → {vegan_alt}")
    
    # 无麸质替代品
    print("\n无麸质替代品:")
    gf_alt = IngredientSubstitutor.find_gluten_free_alternative("面粉")
    print(f"  面粉 → {gf_alt}")


def example_shopping_list():
    """购物清单生成示例"""
    print("\n" + "=" * 50)
    print("购物清单生成")
    print("=" * 50)
    
    # 创建多个食谱
    recipe1 = get_example_recipe()
    recipe2 = Recipe(
        name="米饭",
        servings=4,
        ingredients=[
            Ingredient("米饭", 200, UnitType.GRAM),
            Ingredient("水", 400, UnitType.MILLILITER),
        ],
        steps=[RecipeStep(1, "煮饭")]
    )
    
    # 生成购物清单
    shopping_list = generate_shopping_list([recipe1, recipe2])
    
    print(f"\n总配料数: {shopping_list['total_ingredients']}")
    print("\n按类别分组:")
    for category, items in shopping_list["by_category"].items():
        print(f"\n{category}:")
        for item in items:
            amounts_str = ", ".join(
                f"{a['amount']}{a['unit']}" for a in item["amounts"]
            )
            print(f"  - {item['name']}: {amounts_str} (约{item['estimated_grams']}g)")


def example_recipe_analysis():
    """食谱分析示例"""
    print("\n" + "=" * 50)
    print("食谱分析")
    print("=" * 50)
    
    recipe = get_example_recipe()
    analysis = analyze_recipe(recipe)
    
    print(f"\n食谱: {analysis['recipe_name']}")
    print(f"份数: {analysis['servings']}")
    print(f"难度: {analysis['difficulty']}")
    print(f"餐食类型: {analysis['meal_type']}")
    
    print("\n每份营养:")
    nutrition = analysis['nutrition_per_serving']
    for key, value in nutrition.items():
        print(f"  {key}: {value}")
    
    print("\n健康评分:")
    health = analysis['health_score']
    print(f"  分数: {health['score']}")
    print(f"  等级: {health['grade']}")
    print(f"  亮点: {', '.join(health['highlights'])}")
    
    print("\n时间分析:")
    time_analysis = analysis['time_analysis']
    print(f"  准备时间: {time_analysis['prep_time']}分钟")
    print(f"  烹饪时间: {time_analysis['cook_time']}分钟")
    print(f"  总时间: {time_analysis['total_time']}分钟")
    print(f"  时间分类: {time_analysis['time_category']}")
    
    print("\n饮食兼容性:")
    for diet in analysis['compatible_diets']:
        print(f"  ✓ {diet}")
    
    print("\n成本估算:")
    cost = analysis['cost']
    print(f"  总成本: {cost['total_cost']}元")
    print(f"  每份成本: {cost['cost_per_serving']}元")


def example_cost_estimation():
    """成本估算示例"""
    print("\n" + "=" * 50)
    print("成本估算")
    print("=" * 50)
    
    recipe = get_example_recipe()
    cost = estimate_recipe_cost(recipe)
    
    print(f"\n食谱: {recipe.name}")
    print(f"总成本: {cost['total_cost']}元")
    print(f"每份成本: {cost['cost_per_serving']}元")
    
    print("\n各配料成本:")
    for ing_cost in cost['ingredient_costs']:
        print(f"  {ing_cost['name']}: {ing_cost['cost']}元 ({ing_cost['amount']}{ing_cost['unit']})")


def example_recipe_parsing():
    """食谱解析示例"""
    print("\n" + "=" * 50)
    print("配料文本解析")
    print("=" * 50)
    
    # 测试各种格式
    test_lines = [
        "100g 面粉",
        "2个鸡蛋",
        "1/2杯牛奶",
        "3大匙油",
        "500克牛肉",
    ]
    
    print("\n解析配料行:")
    for line in test_lines:
        ing = parse_ingredient(line)
        if ing:
            print(f"  '{line}' → {ing.amount} {ing.unit.value} {ing.name}")


def example_create_custom_recipe():
    """创建自定义食谱示例"""
    print("\n" + "=" * 50)
    print("创建自定义食谱")
    print("=" * 50)
    
    # 创建自定义食谱
    custom_recipe = Recipe(
        name="简单炒饭",
        servings=2,
        ingredients=[
            Ingredient("米饭", 300, UnitType.GRAM, IngredientCategory.GRAIN),
            Ingredient("鸡蛋", 2, UnitType.PIECE, IngredientCategory.PROTEIN),
            Ingredient("葱", 2, UnitType.PIECE, IngredientCategory.HERB),
            Ingredient("油", 2, UnitType.TABLESPOON, IngredientCategory.OIL),
            Ingredient("盐", 1, UnitType.TEASPOON, IngredientCategory.SPICE),
        ],
        steps=[
            RecipeStep(1, "米饭放凉备用", 0),
            RecipeStep(2, "鸡蛋打散炒熟", 3),
            RecipeStep(3, "加入米饭翻炒", 5),
            RecipeStep(4, "加盐调味，撒葱花", 1),
        ],
        prep_time_minutes=10,
        cook_time_minutes=10,
        difficulty=DifficultyLevel.EASY,
        meal_type=MealType.DINNER,
        tags=["快手菜", "家常菜", "主食"]
    )
    
    print(f"\n创建食谱: {custom_recipe.name}")
    print(f"份数: {custom_recipe.servings}")
    print(f"难度: {custom_recipe.difficulty.value}")
    print(f"总时间: {custom_recipe.total_time_minutes}分钟")
    
    print("\n配料:")
    for ing in custom_recipe.ingredients:
        print(f"  - {ing.amount} {ing.unit.value} {ing.name}")
    
    print("\n步骤:")
    for step in custom_recipe.steps:
        print(f"  {step.step_number}. {step.instruction} ({step.duration_minutes}分钟)")
    
    # 分析自定义食谱
    analysis = analyze_recipe(custom_recipe)
    print(f"\n健康评分: {analysis['health_score']['score']} ({analysis['health_score']['grade']})")
    print(f"每份热量: {analysis['nutrition_per_serving']['calories']} kcal")


if __name__ == "__main__":
    example_basic_recipe_operations()
    example_unit_conversion()
    example_nutrition_calculation()
    example_ingredient_substitution()
    example_shopping_list()
    example_recipe_analysis()
    example_cost_estimation()
    example_recipe_parsing()
    example_create_custom_recipe()
    
    print("\n" + "=" * 50)
    print("所有示例完成!")
    print("=" * 50)