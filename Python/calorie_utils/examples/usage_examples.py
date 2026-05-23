"""
calorie_utils 使用示例

展示如何使用卡路里计算工具的各个功能。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    # BMR和TDEE
    calculate_bmr_mifflin,
    calculate_bmr_harris_benedict,
    calculate_bmr_katch_mcardle,
    calculate_bmr_from_body_fat,
    calculate_tdee,
    calculate_tdee_full,
    
    # 食物热量
    calculate_food_calories,
    calculate_meal_calories,
    search_food,
    list_all_foods,
    
    # 运动消耗
    calculate_exercise_calories,
    calculate_custom_exercise_calories,
    search_exercise,
    
    # 体重目标
    calculate_weight_goal_plan,
    calculate_weight_loss_calories,
    calculate_weight_gain_calories,
    
    # 宏量营养素
    calculate_macro_split,
    calculate_macro_calories,
    calculate_macro_percentages,
    
    # 工具
    bmi_calculate,
    ideal_body_weight,
    lean_body_mass_calculate,
    calorie_deficit_timeline,
    daily_water_intake,
    
    # 枚举
    Gender, ActivityLevel, Goal,
)


def example_bmr_tdee():
    """示例：计算BMR和TDEE"""
    print("=" * 50)
    print("示例1：BMR和TDEE计算")
    print("=" * 50)
    
    # 用户信息：男性，30岁，70kg，175cm
    weight = 70
    height = 175
    age = 30
    gender = Gender.MALE
    
    print(f"\n用户信息：{gender.value}, {age}岁, {weight}kg, {height}cm")
    
    # Mifflin-St Jeor公式（最准确）
    bmr_mifflin = calculate_bmr_mifflin(weight, height, age, gender)
    print(f"\nMifflin-St Jeor BMR: {bmr_mifflin:.1f} kcal/天")
    
    # Harris-Benedict公式
    bmr_harris = calculate_bmr_harris_benedict(weight, height, age, gender)
    print(f"Harris-Benedict BMR: {bmr_harris:.1f} kcal/天")
    
    # 假设体脂率20%，使用Katch-McArdle
    bmr_katch = calculate_bmr_from_body_fat(weight, 20, gender)
    print(f"Katch-McArdle BMR (20%体脂): {bmr_katch:.1f} kcal/天")
    
    # 不同活动水平的TDEE
    print("\n不同活动水平的TDEE：")
    for level in ActivityLevel:
        tdee = calculate_tdee(bmr_mifflin, level)
        print(f"  {level.value}: {tdee:.1f} kcal/天")
    
    # 完整计算
    result = calculate_tdee_full(weight, height, age, gender, ActivityLevel.MODERATE)
    print(f"\n完整TDEE计算结果：")
    for key, value in result.items():
        print(f"  {key}: {value}")


def example_food_calories():
    """示例：食物热量计算"""
    print("\n" + "=" * 50)
    print("示例2：食物热量计算")
    print("=" * 50)
    
    # 单个食物
    print("\n单个食物热量：")
    foods = [("rice_white_cooked", 200), ("chicken_breast", 150)]
    for key, grams in foods:
        result = calculate_food_calories(key, grams)
        if result:
            print(f"  {grams}g {key}: {result.calories:.1f} kcal, 蛋白质{result.protein:.1f}g")
    
    # 一餐计算
    print("\n计算一餐总热量：")
    meal_items = [
        ("rice_white_cooked", 200),   # 200g白米饭
        ("chicken_breast", 150),      # 150g鸡胸肉
        ("broccoli", 100),            # 100g西兰花
        ("tomato", 50),               # 50g番茄
    ]
    
    meal = calculate_meal_calories(meal_items)
    print(f"  总热量: {meal.calories:.1f} kcal")
    print(f"  蛋白质: {meal.protein:.1f} g")
    print(f"  碳水化合物: {meal.carbs:.1f} g")
    print(f"  脂肪: {meal.fat:.1f} g")
    
    # 搜索食物
    print("\n搜索'chicken'相关食物：")
    results = search_food("chicken")
    for food in results[:5]:
        print(f"  {food['key']}: {food['name']} ({food['calories']} kcal/100g)")


def example_exercise_calories():
    """示例：运动消耗计算"""
    print("\n" + "=" * 50)
    print("示例3：运动消耗计算")
    print("=" * 50)
    
    weight = 70  # kg
    
    print(f"\n体重：{weight}kg")
    
    # 不同运动的消耗
    exercises = [
        ("running_8kmh", 30),
        ("swimming_freestyle_moderate", 30),
        ("cycling_moderate", 60),
        ("weight_lifting_moderate", 45),
        ("yoga", 60),
    ]
    
    print("\n运动消耗：")
    total_calories = 0
    for key, duration in exercises:
        calories = calculate_exercise_calories(key, weight, duration)
        total_calories += calories
        info = search_exercise(key)[0] if search_exercise(key) else None
        name = info['name'] if info else key
        print(f"  {name} {duration}分钟: {calories:.1f} kcal")
    
    print(f"\n总消耗: {total_calories:.1f} kcal")
    
    # 自定义运动
    print("\n自定义MET运动：")
    custom_calories = calculate_custom_exercise_calories(12, weight, 30)  # MET=12
    print(f"  MET=12的运动 {weight}kg 30分钟: {custom_calories:.1f} kcal")


def example_weight_goal():
    """示例：体重目标计划"""
    print("\n" + "=" * 50)
    print("示例4：体重目标计划")
    print("=" * 50)
    
    # 减重计划
    print("\n减重计划：从80kg减到75kg")
    tdee = 2500
    
    # 默认速度（0.5kg/周）
    plan = calculate_weight_goal_plan(80, 75, tdee)
    print(f"  目标体重: {plan.target_weight} kg")
    print(f"  需减重: {abs(plan.weight_change)} kg")
    print(f"  达成周数: {plan.weeks_to_achieve} 周")
    print(f"  每日热量目标: {plan.daily_calorie_target} kcal")
    print(f"  每日热量缺口: {abs(plan.daily_deficit)} kcal")
    print(f"  宏量营养素分配:")
    print(f"    蛋白质: {plan.macro_split['protein']} g")
    print(f"    碳水: {plan.macro_split['carbs']} g")
    print(f"    脂肪: {plan.macro_split['fat']} g")
    
    # 减重热量计算
    print("\n减重热量需求：")
    for rate in [0.5, 0.75, 1.0]:
        result = calculate_weight_loss_calories(tdee, rate)
        print(f"  每周减{rate}kg: 每日摄入{result['daily_target']} kcal (缺口{result['daily_deficit']} kcal)")
    
    # 增重计划
    print("\n增重计划：从60kg增到65kg")
    plan_gain = calculate_weight_goal_plan(60, 65, 2000)
    print(f"  每日热量目标: {plan_gain.daily_calorie_target} kcal")
    print(f"  达成周数: {plan_gain.weeks_to_achieve} 周")


def example_macro_nutrients():
    """示例：宏量营养素分配"""
    print("\n" + "=" * 50)
    print("示例5：宏量营养素分配")
    print("=" * 50)
    
    calories = 2000
    
    print(f"\n总热量：{calories} kcal")
    
    # 不同目标的宏量分配
    for goal in Goal:
        macros = calculate_macro_split(calories, goal)
        print(f"\n{goal.value}目标：")
        print(f"  蛋白质: {macros['protein']} g ({macros['protein_pct']}%)")
        print(f"  碳水: {macros['carbs']} g ({macros['carbs_pct']}%)")
        print(f"  脂肪: {macros['fat']} g ({macros['fat_pct']}%)")
    
    # 从宏量计算热量
    print("\n从宏量计算热量：")
    calculated = calculate_macro_calories(150, 200, 67)
    print(f"  150g蛋白质 + 200g碳水 + 67g脂肪 = {calculated:.1f} kcal")
    
    # 计算占比
    print("\n宏量热量占比：")
    percentages = calculate_macro_percentages(150, 200, 67)
    print(f"  蛋白质占比: {percentages['protein_pct']}%")
    print(f"  碳水占比: {percentages['carbs_pct']}%")
    print(f"  脂肪占比: {percentages['fat_pct']}%")
    print(f"  总热量: {percentages['total_calories']} kcal")


def example_bmi_tools():
    """示例：BMI和理想体重"""
    print("\n" + "=" * 50)
    print("示例6：BMI和理想体重计算")
    print("=" * 50)
    
    weight = 70
    height = 175
    
    # BMI
    bmi_result = bmi_calculate(weight, height)
    print(f"\nBMI计算：{weight}kg, {height}cm")
    print(f"  BMI值: {bmi_result['bmi']}")
    print(f"  分类: {bmi_result['category_cn']}")
    print(f"  健康体重范围: {bmi_result['healthy_weight_range']['min']}-{bmi_result['healthy_weight_range']['max']} kg")
    
    # 不同BMI分类示例
    print("\n不同BMI分类示例（175cm）：")
    for w in [50, 70, 80, 100, 120]:
        bmi = bmi_calculate(w, height)
        print(f"  {w}kg: BMI={bmi['bmi']:.1f} ({bmi['category_cn']})")
    
    # 理想体重
    print(f"\n{height}cm男性的理想体重：")
    ideal = ideal_body_weight(height, Gender.MALE)
    print(f"  Devine公式: {ideal['devine']} kg")
    print(f"  Robinson公式: {ideal['robinson']} kg")
    print(f"  Miller公式: {ideal['miller']} kg")
    print(f"  Hamwi公式: {ideal['hamwi']} kg")
    print(f"  平均值: {ideal['average']} kg")
    
    # 理想体重（女性）
    print(f"\n{height}cm女性的理想体重：")
    ideal_f = ideal_body_weight(height, Gender.FEMALE)
    print(f"  Devine公式: {ideal_f['devine']} kg")
    print(f"  平均值: {ideal_f['average']} kg")


def example_lbm():
    """示例：瘦体重计算"""
    print("\n" + "=" * 50)
    print("示例7：瘦体重计算")
    print("=" * 50)
    
    weight = 70
    
    print(f"\n体重：{weight}kg")
    
    # 不同体脂率
    for body_fat in [10, 15, 20, 25, 30]:
        result = lean_body_mass_calculate(weight, body_fat)
        print(f"  体脂率{body_fat}%: 瘦体重{result['lean_body_mass']}kg, 脂肪{result['fat_mass']}kg")
    
    # 从瘦体重计算BMR
    print("\n基于瘦体重的BMR计算：")
    for body_fat in [10, 20, 30]:
        lbm = lean_body_mass_calculate(weight, body_fat)['lean_body_mass']
        bmr = calculate_bmr_katch_mcardle(lbm)
        print(f"  体脂率{body_fat}% (瘦体重{lbm}kg): BMR={bmr:.1f} kcal/天")


def example_timeline():
    """示例：减重时间线"""
    print("\n" + "=" * 50)
    print("示例8：减重时间线")
    print("=" * 50)
    
    current = 80
    target = 75
    
    print(f"\n从{current}kg减到{target}kg")
    
    # 不同热量缺口
    for deficit in [300, 500, 700, 1000]:
        timeline = calorie_deficit_timeline(current, target, deficit)
        print(f"\n每日缺口{deficit}kcal：")
        print(f"  总天数: {timeline['total_days']} 天")
        print(f"  总周数: {timeline['total_weeks']:.1f} 周")
        print(f"  每周减重: {timeline['weekly_loss']} kg")
    
    # 里程碑
    print("\n里程碑（每日缺口500kcal）：")
    timeline = calorie_deficit_timeline(current, target, 500)
    for milestone in timeline['milestones']:
        print(f"  {milestone['percent']}%: 第{milestone['days']}天, 体重{milestone['weight']}kg")


def example_water():
    """示例：饮水量计算"""
    print("\n" + "=" * 50)
    print("示例9：每日饮水量建议")
    print("=" * 50)
    
    weight = 70
    
    print(f"\n体重：{weight}kg")
    
    # 不同活动水平
    for level in ActivityLevel:
        water = daily_water_intake(weight, level)
        print(f"  {level.value}: {water['liters']} L ({water['glasses_250ml']}杯250ml)")
    
    # 不同体重
    print("\n不同体重建议饮水（中度活动）：")
    for w in [50, 70, 90, 110]:
        water = daily_water_intake(w, ActivityLevel.MODERATE)
        print(f"  {w}kg: {water['liters']} L")


def example_complete_day():
    """示例：完整的一天热量计算"""
    print("\n" + "=" * 50)
    print("示例10：完整的一天热量分析")
    print("=" * 50)
    
    # 用户信息
    weight, height, age, gender = 70, 175, 30, Gender.MALE
    activity_level = ActivityLevel.MODERATE
    
    print(f"\n用户：{gender.value}, {age}岁, {weight}kg, {height}cm, {activity_level.value}")
    
    # 计算TDEE
    result = calculate_tdee_full(weight, height, age, gender, activity_level)
    tdee = result['tdee']
    print(f"\n每日能量消耗(TDEE): {tdee:.1f} kcal")
    
    # 减重目标：每日缺口500kcal
    target_calories = int(tdee - 500)
    print(f"减重目标摄入: {target_calories} kcal")
    
    # 宏量分配
    macros = calculate_macro_split(target_calories, Goal.LOSE)
    print(f"\n宏量营养素目标：")
    print(f"  蛋白质: {macros['protein']} g")
    print(f"  碳水: {macros['carbs']} g")
    print(f"  脂肪: {macros['fat']} g")
    
    # 实际摄入
    print("\n实际摄入：")
    breakfast = calculate_meal_calories([
        ("oatmeal_cooked", 250),
        ("egg_whole", 100),
        ("milk_whole", 200),
    ])
    print(f"  早餐: {breakfast.calories:.1f} kcal")
    
    lunch = calculate_meal_calories([
        ("rice_white_cooked", 150),
        ("chicken_breast", 120),
        ("broccoli", 150),
        ("tomato", 100),
    ])
    print(f"  午餐: {lunch.calories:.1f} kcal")
    
    dinner = calculate_meal_calories([
        ("rice_white_cooked", 100),
        ("fish_salmon", 100),
        ("spinach", 150),
    ])
    print(f"  晚餐: {dinner.calories:.1f} kcal")
    
    total_intake = breakfast + lunch + dinner
    print(f"\n总摄入: {total_intake.calories:.1f} kcal")
    print(f"  蛋白质: {total_intake.protein:.1f} g")
    print(f"  碳水: {total_intake.carbs:.1f} g")
    print(f"  脂肪: {total_intake.fat:.1f} g")
    
    # 运动消耗
    print("\n运动消耗：")
    running = calculate_exercise_calories("running_8kmh", weight, 30)
    print(f"  跑步30分钟: {running:.1f} kcal")
    
    # 热量平衡
    net_calories = total_intake.calories - running
    print(f"\n热量平衡：")
    print(f"  摄入 - 运动 = {total_intake.calories:.1f} - {running:.1f} = {net_calories:.1f} kcal")
    print(f"  与TDEE差距: {tdee:.1f} - {net_calories:.1f} = {tdee - net_calories:.1f} kcal")
    
    if net_calories < tdee:
        print(f"  预期减重效果: {(tdee - net_calories) * 7 / 7700:.2f} kg/周")


def main():
    """运行所有示例"""
    example_bmr_tdee()
    example_food_calories()
    example_exercise_calories()
    example_weight_goal()
    example_macro_nutrients()
    example_bmi_tools()
    example_lbm()
    example_timeline()
    example_water()
    example_complete_day()
    
    print("\n" + "=" * 50)
    print("所有示例运行完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()