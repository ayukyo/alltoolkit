"""
Medication Utilities - 使用示例

演示药物剂量计算工具的各种用法。
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from medication_utils import (
    MedicationCalculator,
    MedicationInfo,
    DoseRange,
    DoseUnit,
    WeightUnit,
    Route,
    InfusionCalculator,
    HalfLifeCalculator,
    DoseConverter,
    RenalDoseAdjuster,
    DrugInteractionChecker,
    COMMON_MEDICATIONS,
    get_medication,
    calculate_dose
)


def example_basic_dose_calculation():
    """示例1: 基础剂量计算"""
    print("=" * 60)
    print("示例1: 基础剂量计算")
    print("=" * 60)
    
    # 获取对乙酰氨基酚信息
    paracetamol = get_medication("paracetamol")
    print(f"\n药物: {paracetamol.name}")
    print(f"标准剂量: {paracetamol.standard_dose_per_kg} {paracetamol.dose_unit.value}/kg")
    print(f"半衰期: {paracetamol.half_life_hours} 小时")
    
    # 创建计算器
    calculator = MedicationCalculator(paracetamol)
    
    # 计算70kg成人的剂量
    weight = 70
    dose = calculator.calculate_weight_based_dose(weight)
    print(f"\n{weight}kg 成人剂量: {dose} {paracetamol.dose_unit.value}")
    
    # 验证剂量
    validation = calculator.validate_dose(dose)
    print(f"剂量验证: {'通过' if validation['is_valid'] else '未通过'}")
    
    print()


def example_pediatric_dosing():
    """示例2: 儿童剂量计算（多种方法）"""
    print("=" * 60)
    print("示例2: 儿童剂量计算")
    print("=" * 60)
    
    ibuprofen = get_medication("ibuprofen")
    calculator = MedicationCalculator(ibuprofen)
    
    # 6岁儿童，20kg，110cm
    age_years = 6
    weight_kg = 20
    height_cm = 110
    
    print(f"\n儿童信息: {age_years}岁, {weight_kg}kg, {height_cm}cm")
    print(f"药物: {ibuprofen.name}\n")
    
    # Young规则（按年龄）
    young_dose = calculator.calculate_pediatric_dose_young(age_years)
    print(f"Young规则（按年龄）: {young_dose:.1f} {ibuprofen.dose_unit.value}")
    
    # Clark规则（按体重）
    clark_dose = calculator.calculate_pediatric_dose_clark(weight_kg, WeightUnit.KG)
    print(f"Clark规则（按体重）: {clark_dose:.1f} {ibuprofen.dose_unit.value}")
    
    # 体表面积法
    bsa_dose = calculator.calculate_pediatric_dose_body_surface(weight_kg, height_cm)
    print(f"体表面积法: {bsa_dose:.1f} {ibuprofen.dose_unit.value}")
    
    # 标准体重法
    weight_dose = calculator.calculate_weight_based_dose(weight_kg)
    print(f"体重法（标准）: {weight_dose:.1f} {ibuprofen.dose_unit.value}")
    
    print()


def example_infusion_calculation():
    """示例3: 输液计算"""
    print("=" * 60)
    print("示例3: 输液计算")
    print("=" * 60)
    
    # 场景: 1000ml生理盐水, 60分钟输完, 滴系数20
    volume = 1000  # ml
    time = 60  # 分钟
    drop_factor = 20
    
    drip_rate = InfusionCalculator.calculate_drip_rate(volume, time, drop_factor)
    print(f"\n输液量: {volume}ml")
    print(f"输液时间: {time}分钟")
    print(f"滴系数: {drop_factor} 滴/ml")
    print(f"计算滴速: {drip_rate:.1f} 滴/分钟")
    
    # 小儿输液场景
    print("\n--- 小儿输液场景 ---")
    pediatric_volume = 200  # ml
    pediatric_time = 120  # 分钟
    pediatric_drop_factor = 60  # 微滴
    
    pediatric_rate = InfusionCalculator.calculate_drip_rate(
        pediatric_volume, pediatric_time, pediatric_drop_factor
    )
    print(f"输液量: {pediatric_volume}ml")
    print(f"输液时间: {pediatric_time}分钟")
    print(f"滴系数: {pediatric_drop_factor} 滴/ml（微滴）")
    print(f"计算滴速: {pediatric_rate:.1f} 滴/分钟")
    
    # 计算所需体积
    print("\n--- 药物稀释计算 ---")
    dose_needed = 500  # mg
    concentration = 50  # mg/ml
    
    volume_needed = InfusionCalculator.calculate_volume(dose_needed, concentration)
    print(f"所需剂量: {dose_needed}mg")
    print(f"药物浓度: {concentration}mg/ml")
    print(f"需抽取体积: {volume_needed}ml")
    
    print()


def example_half_life_calculation():
    """示例4: 药物半衰期计算"""
    print("=" * 60)
    print("示例4: 药物半衰期计算")
    print("=" * 60)
    
    # 对乙酰氨基酚半衰期约2小时
    half_life = 2  # 小时
    initial_dose = 1000  # mg
    
    print(f"\n药物半衰期: {half_life}小时")
    print(f"初始剂量: {initial_dose}mg\n")
    
    # 计算不同时间点的剩余剂量
    print("时间点剩余剂量:")
    for hours in [2, 4, 6, 8, 12]:
        remaining = HalfLifeCalculator.calculate_remaining_dose(
            initial_dose, half_life, hours
        )
        print(f"  {hours}小时后: {remaining:.1f}mg ({remaining/initial_dose*100:.1f}%)")
    
    # 计算消除时间
    target = 50  # mg
    elimination_time = HalfLifeCalculator.calculate_time_to_eliminate(
        initial_dose, half_life, target
    )
    print(f"\n消除到 {target}mg 需要时间: {elimination_time:.1f}小时")
    
    # 估算稳态时间
    steady_state = HalfLifeCalculator.estimate_steady_state_time(half_life)
    print(f"达到稳态浓度时间: {steady_state}小时（约{steady_state/24:.1f}天）")
    
    # 计算给药间隔
    interval = HalfLifeCalculator.calculate_dosing_interval(half_life, 0.5)
    print(f"建议给药间隔: {interval:.1f}小时（峰谷比50%）")
    
    print()


def example_renal_dose_adjustment():
    """示例5: 肾功能剂量调整"""
    print("=" * 60)
    print("示例5: 肾功能剂量调整")
    print("=" * 60)
    
    # 计算肌酐清除率
    print("\n--- 肌酐清除率计算 ---")
    age = 65
    weight = 60  # kg
    scr = 1.5  # mg/dL
    is_female = True
    
    ccr = RenalDoseAdjuster.calculate_creatinine_clearance(
        age, weight, scr, is_female
    )
    print(f"患者: {age}岁, {weight}kg, 女性")
    print(f"血清肌酐: {scr} mg/dL")
    print(f"肌酐清除率: {ccr:.1f} mL/min")
    
    # 根据肾功能调整剂量
    print("\n--- 剂量调整 ---")
    standard_dose = 500  # mg
    
    for ccr_value in [95, 70, 45, 25, 10]:
        adjusted_dose, msg = RenalDoseAdjuster.adjust_dose_for_renal(
            standard_dose, ccr_value
        )
        print(f"Ccr {ccr_value} mL/min: {adjusted_dose:.0f}mg ({msg})")
    
    print()


def example_drug_interaction():
    """示例6: 药物相互作用检查"""
    print("=" * 60)
    print("示例6: 药物相互作用检查")
    print("=" * 60)
    
    # 单独检查两种药物
    print("\n--- 华法林 + 阿司匹林 ---")
    interaction = DrugInteractionChecker.check_interaction("warfarin", "aspirin")
    if interaction:
        print(f"严重程度: {interaction['severity']}")
        print(f"相互作用类型: {interaction['type']}")
        print(f"描述: {interaction['description']}")
    
    # 批量检查多种药物
    print("\n--- 批量检查药物相互作用 ---")
    medications = ["warfarin", "aspirin", "vitamin_k", "metformin"]
    print(f"药物列表: {', '.join(medications)}\n")
    
    interactions = DrugInteractionChecker.check_multiple_interactions(medications)
    
    if interactions:
        print(f"发现 {len(interactions)} 个潜在相互作用:\n")
        for i in interactions:
            print(f"  {i['drug1']} + {i['drug2']}")
            print(f"    严重程度: {i['severity']}")
            print(f"    描述: {i['description']}\n")
    else:
        print("未发现已知相互作用")
    
    print()


def example_dose_validation():
    """示例7: 剂量安全性验证"""
    print("=" * 60)
    print("示例7: 剂量安全性验证")
    print("=" * 60)
    
    # 自定义药物信息
    custom_med = MedicationInfo(
        name="Custom Antibiotic",
        standard_dose_per_kg=15,
        dose_unit=DoseUnit.MG,
        dose_range=DoseRange(10, 20, DoseUnit.MG),
        max_daily_dose=500,
        half_life_hours=8
    )
    
    calculator = MedicationCalculator(custom_med)
    
    print(f"\n药物: {custom_med.name}")
    print(f"剂量范围: {custom_med.dose_range.min_dose}-{custom_med.dose_range.max_dose} {custom_med.dose_unit.value}/kg")
    print(f"每日最大剂量: {custom_med.max_daily_dose} {custom_med.dose_unit.value}\n")
    
    # 测试不同剂量
    test_doses = [5, 15, 25, 600]
    
    for dose in test_doses:
        result = calculator.validate_dose(dose)
        status = "✓ 有效" if result["is_valid"] else "✗ 无效"
        print(f"剂量 {dose}mg: {status}")
        
        if result["errors"]:
            for error in result["errors"]:
                print(f"  错误: {error}")
        if result["warnings"]:
            for warning in result["warnings"]:
                print(f"  警告: {warning}")
    
    print()


def example_convenient_functions():
    """示例8: 便捷函数使用"""
    print("=" * 60)
    print("示例8: 便捷函数使用")
    print("=" * 60)
    
    # 使用便捷函数计算剂量
    print("\n--- 对乙酰氨基酚剂量计算 ---")
    result = calculate_dose("paracetamol", 70)
    
    if result["success"]:
        print(f"药物: {result['medication']}")
        print(f"体重: {result['weight_kg']}kg")
        print(f"计算剂量: {result['calculated_dose']} {result['unit']}")
        print(f"验证状态: {'通过' if result['is_valid'] else '未通过'}")
    
    # 使用磅作为体重单位
    print("\n--- 使用磅作为体重单位 ---")
    result = calculate_dose("ibuprofen", 154, WeightUnit.LB)
    
    if result["success"]:
        print(f"体重: {result['weight_kg']:.1f}kg (154lb)")
        print(f"计算剂量: {result['calculated_dose']:.1f} {result['unit']}")
    
    print()


def example_unit_conversion():
    """示例9: 单位转换"""
    print("=" * 60)
    print("示例9: 单位转换")
    print("=" * 60)
    
    print("\n--- 剂量单位转换 ---")
    print(f"1000mg = {DoseConverter.mg_to_g(1000)}g")
    print(f"1g = {DoseConverter.g_to_mg(1)}mg")
    print(f"1mg = {DoseConverter.mg_to_mcg(1)}mcg")
    print(f"1000mcg = {DoseConverter.mcg_to_mg(1000)}mg")
    
    print("\n--- 体重单位转换 ---")
    print(f"70kg = {DoseConverter.kg_to_lb(70):.2f}lb")
    print(f"154lb = {DoseConverter.lb_to_kg(154):.2f}kg")
    
    print("\n--- 通用剂量转换 ---")
    dose = DoseConverter.convert_dose(0.5, DoseUnit.G, DoseUnit.MG)
    print(f"0.5g = {dose}mg")
    
    dose = DoseConverter.convert_dose(500, DoseUnit.MG, DoseUnit.G)
    print(f"500mg = {dose}g")
    
    print()


def example_custom_medication():
    """示例10: 自定义药物计算"""
    print("=" * 60)
    print("示例10: 自定义药物计算")
    print("=" * 60)
    
    # 创建自定义药物
    custom_med = MedicationInfo(
        name="Experimental Drug X",
        standard_dose_per_kg=5,
        dose_unit=DoseUnit.MG,
        dose_range=DoseRange(2, 10, DoseUnit.MG),
        max_daily_dose=600,
        half_life_hours=12,
        routes=[Route.ORAL, Route.IV],
        bioavailability=0.75
    )
    
    calculator = MedicationCalculator(custom_med)
    
    print(f"\n自定义药物信息:")
    print(f"  名称: {custom_med.name}")
    print(f"  标准剂量: {custom_med.standard_dose_per_kg} {custom_med.dose_unit.value}/kg")
    print(f"  剂量范围: {custom_med.dose_range.min_dose}-{custom_med.dose_range.max_dose} {custom_med.dose_unit.value}/kg")
    print(f"  每日最大剂量: {custom_med.max_daily_dose} {custom_med.dose_unit.value}")
    print(f"  半衰期: {custom_med.half_life_hours} 小时")
    print(f"  生物利用度: {custom_med.bioavailability * 100}%")
    print(f"  给药途径: {', '.join([r.value for r in custom_med.routes])}")
    
    # 计算不同体重的剂量
    print("\n--- 不同体重的剂量计算 ---")
    weights = [50, 70, 90, 120]
    
    for w in weights:
        dose = calculator.calculate_weight_based_dose(w)
        validation = calculator.validate_dose(dose)
        status = "✓" if validation["is_valid"] else "✗"
        print(f"  {w}kg: {dose}mg {status}")
    
    print()


def main():
    """运行所有示例"""
    example_basic_dose_calculation()
    example_pediatric_dosing()
    example_infusion_calculation()
    example_half_life_calculation()
    example_renal_dose_adjustment()
    example_drug_interaction()
    example_dose_validation()
    example_convenient_functions()
    example_unit_conversion()
    example_custom_medication()
    
    print("=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()