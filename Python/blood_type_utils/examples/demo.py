#!/usr/bin/env python3
"""
Blood Type Utilities 使用示例

演示血型兼容性检测、遗传计算、分布统计等功能。

Author: AllToolkit
Version: 1.0.0
"""

import sys
import os

# 添加模块目录到路径
module_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, module_dir)

# 直接从当前目录导入
import importlib.util
spec = importlib.util.spec_from_file_location("blood_type_utils", os.path.join(module_dir, "mod.py"))
blood_type_utils = importlib.util.module_from_spec(spec)
sys.modules["blood_type_utils"] = blood_type_utils
spec.loader.exec_module(blood_type_utils)

# 使用导入的模块
BloodType = blood_type_utils.BloodType
ABOType = blood_type_utils.ABOType
RhFactor = blood_type_utils.RhFactor
BloodTypeUtils = blood_type_utils.BloodTypeUtils
parse_blood_type = blood_type_utils.parse_blood_type
can_donate = blood_type_utils.can_donate
get_compatible_donors = blood_type_utils.get_compatible_donors
get_compatible_recipients = blood_type_utils.get_compatible_recipients
child_blood_types = blood_type_utils.child_blood_types
get_blood_type_info = blood_type_utils.get_blood_type_info


def demo_compatibility():
    """演示血型兼容性"""
    print("=" * 60)
    print("血型兼容性检测示例")
    print("=" * 60)
    
    # 万能献血者
    print("\n🔴 万能献血者 (O-):")
    print("-" * 40)
    recipients = get_compatible_recipients(BloodType.O_NEGATIVE)
    print(f"O- 可以献血给 {len(recipients)} 种血型:")
    for r in sorted(recipients, key=lambda x: x.value):
        print(f"  ✓ {r.value}")
    
    # 万能受血者
    print("\n🟠 万能受血者 (AB+):")
    print("-" * 40)
    donors = get_compatible_donors(BloodType.AB_POSITIVE)
    print(f"AB+ 可以接受 {len(donors)} 种血型的献血:")
    for d in sorted(donors, key=lambda x: x.value):
        print(f"  ✓ {d.value}")
    
    # 特定血型示例
    print("\n🟡 A+ 血型兼容性:")
    print("-" * 40)
    print("可以献血给:")
    for r in BloodTypeUtils.get_compatible_recipients(BloodType.A_POSITIVE):
        print(f"  → {r.value}")
    print("可以接受:")
    for d in BloodTypeUtils.get_compatible_donors(BloodType.A_POSITIVE):
        print(f"  ← {d.value}")
    
    # 稀有血型限制
    print("\n🟢 O- 受血者的限制:")
    print("-" * 40)
    donors = get_compatible_donors(BloodType.O_NEGATIVE)
    print(f"O- 只能接受 {len(donors)} 种血型:")
    for d in donors:
        print(f"  ← {d.value} (唯一选择)")
    
    # 使用便捷函数
    print("\n🔵 便捷函数示例:")
    print("-" * 40)
    print(f"can_donate('O-', 'A+') = {can_donate('O-', 'A+')}")
    print(f"can_donate('A+', 'O-') = {can_donate('A+', 'O-')}")
    print(f"can_donate('B-', 'AB+') = {can_donate('B-', 'AB+')}")
    print(f"can_donate('AB+', 'B+') = {can_donate('AB+', 'B+')}")


def demo_inheritance():
    """演示血型遗传计算"""
    print("\n" + "=" * 60)
    print("血型遗传计算示例")
    print("=" * 60)
    
    # 各种父母组合
    combinations = [
        (BloodType.O_POSITIVE, BloodType.O_POSITIVE, "O+ × O+"),
        (BloodType.A_POSITIVE, BloodType.B_POSITIVE, "A+ × B+"),
        (BloodType.AB_POSITIVE, BloodType.O_POSITIVE, "AB+ × O+"),
        (BloodType.A_NEGATIVE, BloodType.A_NEGATIVE, "A- × A-"),
        (BloodType.B_POSITIVE, BloodType.O_NEGATIVE, "B+ × O-"),
    ]
    
    for p1, p2, title in combinations:
        print(f"\n🧬 {title}:")
        print("-" * 40)
        children = child_blood_types(p1, p2)
        for bt, prob in sorted(children.items(), key=lambda x: -x[1]):
            pct = f"{prob:.1f}%"
            bar = "█" * int(prob / 5) + "░" * (20 - int(prob / 5))
            print(f"  {bt.value:>4} {pct:>8} {bar}")
    
    # 父母关系验证
    print("\n🧪 父母关系验证:")
    print("-" * 40)
    print(f"O型父母能生AB型孩子吗? {BloodTypeUtils.can_be_parent(BloodType.O_POSITIVE, BloodType.AB_POSITIVE)}")
    print(f"AB型父母能生O型孩子吗? {BloodTypeUtils.can_be_parent(BloodType.AB_POSITIVE, BloodType.O_POSITIVE)}")
    print(f"A型父母能生O型孩子吗? {BloodTypeUtils.can_be_parent(BloodType.A_POSITIVE, BloodType.O_POSITIVE)}")
    
    # 查找可能的父母
    print("\n🔍 O- 孩子可能的父母组合:")
    print("-" * 40)
    parents = BloodTypeUtils.find_possible_parents(BloodType.O_NEGATIVE)
    print(f"共有 {len(parents)} 种组合:")
    for p1, p2 in parents[:5]:  # 只显示前5个
        print(f"  {p1.value} × {p2.value}")
    print(f"  ... 还有 {len(parents) - 5} 种组合")


def demo_distribution():
    """演示血型分布统计"""
    print("\n" + "=" * 60)
    print("血型分布统计示例")
    print("=" * 60)
    
    populations = ["global", "china", "usa"]
    population_names = {"global": "全球", "china": "中国", "usa": "美国"}
    
    for pop in populations:
        print(f"\n📊 {population_names[pop]}人群血型分布:")
        print("-" * 40)
        distribution = BloodTypeUtils.get_distribution_by_population(pop)
        
        for bt, pct in sorted(distribution.items(), key=lambda x: -x[1]):
            bar = "█" * int(pct / 2) + "░" * (50 - int(pct / 2))
            print(f"  {bt.value:>4} {pct:>5.1f}%  {bar}")
    
    # 稀有血型
    print("\n⚠️  全球稀有血型 (< 5%):")
    print("-" * 40)
    rare = BloodTypeUtils.get_rare_blood_types("global")
    for bt in sorted(rare, key=lambda x: BloodTypeUtils.get_population_percentage(x, "global"), reverse=True):
        pct = BloodTypeUtils.get_population_percentage(bt, "global")
        print(f"  {bt.value}: {pct}%")
    
    print("\n⚠️  中国稀有血型 (< 1%):")
    print("-" * 40)
    rare_china = BloodTypeUtils.get_rare_blood_types("china", threshold=1)
    for bt in sorted(rare_china, key=lambda x: BloodTypeUtils.get_population_percentage(x, "china"), reverse=True):
        pct = BloodTypeUtils.get_population_percentage(bt, "china")
        print(f"  {bt.value}: {pct}%")


def demo_detailed_info():
    """演示血型详细信息"""
    print("\n" + "=" * 60)
    print("血型详细信息示例")
    print("=" * 60)
    
    blood_types = [
        BloodType.O_NEGATIVE,
        BloodType.A_POSITIVE,
        BloodType.AB_POSITIVE,
    ]
    
    for bt in blood_types:
        print(f"\n🔬 {bt.value} 血型详情:")
        print("-" * 40)
        info = get_blood_type_info(bt)
        
        print(f"  ABO血型: {info.abo_type.value}")
        print(f"  Rh因子: {info.rh_factor.value}")
        print(f"  抗原: {', '.join(info.antigens) if info.antigens else '无'}")
        print(f"  抗体: {', '.join(info.antibodies) if info.antibodies else '无'}")
        print(f"  基因型: {', '.join(info.possible_genotypes)}")
        print(f"  全球占比: {info.population_percentage}%")
        print(f"  万能献血者: {'是' if info.is_universal_donor else '否'}")
        print(f"  万能受血者: {'是' if info.is_universal_recipient else '否'}")
    
    # 格式化显示
    print("\n📝 血型格式化显示:")
    print("-" * 40)
    for bt in [BloodType.A_POSITIVE, BloodType.O_NEGATIVE, BloodType.AB_POSITIVE]:
        print(f"  {bt.value}:")
        print(f"    简短格式: {BloodTypeUtils.format_blood_type(bt, 'short')}")
        print(f"    完整格式: {BloodTypeUtils.format_blood_type(bt, 'full')}")
        print(f"    中文格式: {BloodTypeUtils.format_blood_type(bt, 'chinese')}")


def demo_parsing():
    """演示血型解析"""
    print("\n" + "=" * 60)
    print("血型解析示例")
    print("=" * 60)
    
    test_inputs = [
        "A+", "a+", "A POSITIVE",
        "B-", "b-", "B NEGATIVE",
        "AB+", "ab+", "AB POSITIVE",
        "O-", "o-", "O NEGATIVE",
        "X+", "invalid", "",
    ]
    
    print("\n解析各种输入:")
    print("-" * 40)
    for input_str in test_inputs:
        result = parse_blood_type(input_str)
        if result:
            print(f"  '{input_str}' → {result.value}")
        else:
            print(f"  '{input_str}' → 无效")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("   🩸 Blood Type Utilities - 血型工具模块示例   ")
    print("=" * 60)
    
    demo_compatibility()
    demo_inheritance()
    demo_distribution()
    demo_detailed_info()
    demo_parsing()
    
    print("\n" + "=" * 60)
    print("   示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()