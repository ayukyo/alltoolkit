"""
One Rep Max Utilities - 使用示例

展示各种实际应用场景：
1. 基本1RM估算
2. 多公式对比
3. 训练计划生成
4. 进度追踪
5. 力量等级评估
"""

import sys
import os

# 路径设置
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from one_rep_max_utils.mod import (
    # 核心公式
    brzycki, epley, lander, lombardi, oconner, wathan, mayhew,
    # 综合计算
    calculate_1rm, calculate_all_formulas, average_1rm,
    # 反向计算
    calculate_weight_for_reps, calculate_percentage_weight,
    # 训练计划
    generate_rep_max_table, generate_percentage_table,
    estimate_reps_at_weight,
    # 进度追踪
    calculate_strength_level, calculate_wilks_score, compare_1rm,
    # 辅助功能
    round_to_plate, suggest_warmup_weights, validate_input,
    get_available_formulas, get_formula_description,
    # 类
    OneRepMaxCalculator,
)


def example_basic_calculation():
    """示例1: 基本1RM估算"""
    print("\n" + "="*60)
    print("示例1: 基本1RM估算")
    print("="*60)
    
    # 你卧推80kg做了8次，估算你的1RM
    weight = 80
    reps = 8
    
    print(f"\n训练数据: {weight}kg × {reps}次")
    
    # 使用默认公式（Brzycki）
    one_rm = calculate_1rm(weight, reps)
    print(f"\n估算1RM (Brzycki): {one_rm:.2f}kg")
    
    # 使用其他公式
    print("\n各公式估算结果:")
    all_results = calculate_all_formulas(weight, reps)
    for name, value in all_results.items():
        desc = get_formula_description(name)
        print(f"  {name:10s}: {value:.2f}kg - {desc}")
    
    # 平均值
    avg = average_1rm(weight, reps)
    print(f"\n所有公式平均: {avg:.2f}kg")


def example_training_plan():
    """示例2: 训练计划生成"""
    print("\n" + "="*60)
    print("示例2: 训练计划生成")
    print("="*60)
    
    # 你的深蹲1RM是150kg
    one_rm = 150
    
    print(f"\n假设深蹲1RM: {one_rm}kg")
    
    # 生成nRM表
    print("\nnRM训练表:")
    table = generate_rep_max_table(one_rm, max_reps=10)
    for reps, weight in table.items():
        rounded = round_to_plate(weight)
        print(f"  {reps}RM: {weight:.1f}kg → 实际可用: {rounded}kg")
    
    # 生成百分比表
    print("\n百分比训练表:")
    pct_table = generate_percentage_table(one_rm)
    for pct, weight in pct_table.items():
        print(f"  {pct}%: {weight:.1f}kg")


def example_weight_for_target_reps():
    """示例3: 根据目标次数计算训练重量"""
    print("\n" + "="*60)
    print("示例3: 计算目标次数的训练重量")
    print("="*60)
    
    # 你的卧推1RM是100kg，今天要做5×5训练
    one_rm = 100
    target_reps = 5
    
    print(f"\n假设卧推1RM: {one_rm}kg，目标: {target_reps}次")
    
    # 计算应该用的重量
    weight = calculate_weight_for_reps(one_rm, target_reps)
    rounded = round_to_plate(weight)
    
    print(f"\n建议使用重量: {weight:.2f}kg")
    print(f"实际可用杠铃片: {rounded}kg")
    
    # 估算可以做的次数
    test_weight = 80
    estimated_reps = estimate_reps_at_weight(one_rm, test_weight)
    print(f"\n如果用{test_weight}kg，预计可做: {estimated_reps}次")


def example_warmup_suggestion():
    """示例4: 热身组建议"""
    print("\n" + "="*60)
    print("示例4: 热身组建议")
    print("="*60)
    
    # 今天要硬拉180kg (1RM)，工作组是150kg
    one_rm = 180
    working_weight = 150
    
    print(f"\n硬拉1RM: {one_rm}kg，工作组: {working_weight}kg")
    
    # 获取热身建议
    warmup = suggest_warmup_weights(one_rm, working_weight)
    
    print("\n建议热身组:")
    for i, (weight, reps) in enumerate(warmup, 1):
        rounded = round_to_plate(weight)
        print(f"  第{i}组: {rounded}kg × {reps}次")


def example_progress_tracking():
    """示例5: 进度追踪"""
    print("\n" + "="*60)
    print("示例5: 进度追踪")
    print("="*60)
    
    # 过去一个月的训练记录
    sessions = [
        ("第1周", 80, 8),   # 80kg做8次
        ("第2周", 82, 8),   # 82kg做8次
        ("第3周", 85, 7),   # 85kg做7次
        ("第4周", 87, 6),   # 87kg做6次
    ]
    
    print("\n过去4周卧推训练记录:")
    
    one_rm_history = []
    for week, weight, reps in sessions:
        one_rm = calculate_1rm(weight, reps)
        one_rm_history.append(one_rm)
        print(f"  {week}: {weight}kg × {reps}次 → 估算1RM: {one_rm:.2f}kg")
    
    # 比较进步
    if len(one_rm_history) >= 2:
        progress = compare_1rm(one_rm_history[0], one_rm_history[-1])
        print(f"\n总体进步:")
        print(f"  1RM变化: {progress['change']:.2f}kg")
        print(f"  百分比: {progress['percentage']:.1f}%")


def example_strength_level():
    """示例6: 力量等级评估"""
    print("\n" + "="*60)
    print("示例6: 力量等级评估")
    print("="*60)
    
    # 一位训练者的数据
    exercises = {
        '卧推': ('bench_press', 100),
        '深蹲': ('squat', 140),
        '硬拉': ('deadlift', 180),
    }
    
    bodyweight = 80
    gender = 'male'
    
    print(f"\n训练者数据: {gender}，体重{bodyweight}kg")
    
    for name, (exercise, one_rm) in exercises.items():
        level = calculate_strength_level(one_rm, bodyweight, gender, exercise)
        ratio = one_rm / bodyweight
        wilks = calculate_wilks_score(one_rm, bodyweight, gender)
        
        print(f"\n{name} ({one_rm}kg):")
        print(f"  力量体重比: {ratio:.2f}")
        print(f"  力量等级: {level}")
        print(f"  Wilks得分: {wilks:.2f}")


def example_calculator_class():
    """示例7: 使用计算器类"""
    print("\n" + "="*60)
    print("示例7: 使用OneRepMaxCalculator类")
    print("="*60)
    
    # 创建计算器实例
    calc = OneRepMaxCalculator(formula='epley')
    
    print(f"\n创建计算器，使用Epley公式")
    
    # 计算1RM
    weight, reps = 100, 5
    one_rm = calc.calculate(weight, reps)
    print(f"\n{weight}kg × {reps}次 → 1RM: {one_rm:.2f}kg")
    
    # 生成训练表
    table = calc.generate_table(one_rm, max_reps=10)
    print(f"\n基于{one_rm:.2f}kg的nRM表:")
    for r, w in table.items():
        if r <= 6:
            print(f"  {r}RM: {w:.1f}kg")
    
    # 比较进步
    comparison = calc.compare(100, 110)
    print(f"\n进步分析: 100kg → 110kg")
    print(f"  增加: {comparison['change']}kg ({comparison['percentage']:.1f}%)")


def example_deload_calculation():
    """示例8: 减载计算"""
    print("\n" + "="*60)
    print("示例8: 减载计算")
    print("="*60)
    
    # 正常训练周期后的减载
    exercises = {
        '卧推': 100,
        '深蹲': 150,
        '硬拉': 180,
    }
    
    deload_percentage = 70  # 减载到70%
    
    print(f"\n减载周训练（{deload_percentage}%强度）:")
    
    for name, one_rm in exercises.items():
        deload_weight = calculate_percentage_weight(one_rm, deload_percentage)
        rounded = round_to_plate(deload_weight)
        
        # 估算这个重量能做多少次
        estimated_reps = estimate_reps_at_weight(one_rm, deload_weight)
        
        print(f"\n{name} (1RM: {one_rm}kg):")
        print(f"  减载重量: {deload_weight}kg → 可用: {rounded}kg")
        print(f"  这个重量预计可做: {estimated_reps}次")


def example_validation():
    """示例9: 输入验证"""
    print("\n" + "="*60)
    print("示例9: 输入验证")
    print("="*60)
    
    test_cases = [
        (100, 5, "正常"),
        (0, 5, "零重量"),
        (-10, 5, "负重量"),
        (100, 0, "零次数"),
        (100, 35, "过高次数"),
    ]
    
    print("\n验证测试:")
    for weight, reps, desc in test_cases:
        valid, msg = validate_input(weight, reps)
        status = "✓" if valid else "✗"
        print(f"  {status} {desc}: {weight}kg, {reps}次 - {msg if msg else 'OK'}")


def main():
    """运行所有示例"""
    print("\n" + "="*60)
    print("One Rep Max Utilities 使用示例")
    print("="*60)
    
    # 显示可用公式
    print("\n可用公式:")
    for formula in get_available_formulas():
        desc = get_formula_description(formula)
        print(f"  - {formula}: {desc}")
    
    # 运行所有示例
    example_basic_calculation()
    example_training_plan()
    example_weight_for_target_reps()
    example_warmup_suggestion()
    example_progress_tracking()
    example_strength_level()
    example_calculator_class()
    example_deload_calculation()
    example_validation()
    
    print("\n" + "="*60)
    print("示例完成!")
    print("="*60)


if __name__ == '__main__':
    main()