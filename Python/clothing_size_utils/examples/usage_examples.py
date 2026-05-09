"""
Clothing Size Utils 使用示例
演示服装尺码转换的各种功能
"""

from mod import (
    SizeRegion, ClothingType,
    convert_top_size, convert_pants_size, convert_shoe_size,
    convert_shoe_size_by_cm, calculate_bra_size,
    recommend_size_by_measurements, get_size_chart,
    list_all_regions, list_all_clothing_types, quick_size_guide
)


def example_top_size_conversion():
    """上装尺码转换示例"""
    print("=" * 60)
    print("👕 上装尺码转换")
    print("=" * 60)
    
    # 中国码转其他地区
    sizes = ["XS", "S", "M", "L", "XL", "XXL"]
    print("\n中国上装尺码对照表:")
    print("-" * 50)
    print(f"{'CN':<6} {'EU':<6} {'US':<6} {'UK':<6} {'JP':<6} {'KR':<6}")
    print("-" * 50)
    
    for size in sizes:
        eu = convert_top_size(size, SizeRegion.CN, SizeRegion.EU) or "-"
        us = convert_top_size(size, SizeRegion.CN, SizeRegion.US) or "-"
        uk = convert_top_size(size, SizeRegion.CN, SizeRegion.UK) or "-"
        jp = convert_top_size(size, SizeRegion.CN, SizeRegion.JP) or "-"
        kr = convert_top_size(size, SizeRegion.CN, SizeRegion.KR) or "-"
        print(f"{size:<6} {eu:<6} {us:<6} {uk:<6} {jp:<6} {kr:<6}")
    
    print("\n示例:")
    print(f"  中国码 M → 欧洲码: {convert_top_size('M', SizeRegion.CN, SizeRegion.EU)}")
    print(f"  中国码 L → 英国码: {convert_top_size('L', SizeRegion.CN, SizeRegion.UK)}")
    print(f"  欧洲码 40 → 中国码: {convert_top_size('40', SizeRegion.EU, SizeRegion.CN)}")
    print(f"  英国码 10 → 美国码: {convert_top_size('10', SizeRegion.UK, SizeRegion.US)}")


def example_pants_size_conversion():
    """裤装尺码转换示例"""
    print("\n" + "=" * 60)
    print("👖 裤装尺码转换")
    print("=" * 60)
    
    print("\n根据腰围推荐尺码:")
    print("-" * 50)
    print(f"{'腰围(cm)':<10} {'CN':<6} {'US':<6} {'EU':<6} {'UK':<6} {'JP':<6}")
    print("-" * 50)
    
    waists = [60, 64, 68, 72, 76, 80]
    for waist in waists:
        cn = convert_pants_size(waist, SizeRegion.CN) or "-"
        us = convert_pants_size(waist, SizeRegion.US) or "-"
        eu = convert_pants_size(waist, SizeRegion.EU) or "-"
        uk = convert_pants_size(waist, SizeRegion.UK) or "-"
        jp = convert_pants_size(waist, SizeRegion.JP) or "-"
        print(f"{waist:<10} {cn:<6} {us:<6} {eu:<6} {uk:<6} {jp:<6}")


def example_shoe_size_conversion():
    """鞋码转换示例"""
    print("\n" + "=" * 60)
    print("👟 鞋码转换")
    print("=" * 60)
    
    print("\n中国鞋码对照表 (常见尺码):")
    print("-" * 70)
    print(f"{'CN':<6} {'EU':<6} {'US男':<8} {'US女':<8} {'UK':<6} {'JP':<6} {'脚长(cm)':<10}")
    print("-" * 70)
    
    cn_sizes = [36, 38, 40, 42, 44]
    for cn in cn_sizes:
        eu = convert_shoe_size(cn, SizeRegion.CN, SizeRegion.EU, "unisex") or "-"
        us_men = convert_shoe_size(cn, SizeRegion.CN, SizeRegion.US, "men") or "-"
        us_women = convert_shoe_size(cn, SizeRegion.CN, SizeRegion.US, "women") or "-"
        uk = convert_shoe_size(cn, SizeRegion.CN, SizeRegion.UK, "unisex") or "-"
        jp = convert_shoe_size(cn, SizeRegion.CN, SizeRegion.JP, "unisex") or "-"
        
        # 根据中国码估算脚长
        foot_length = cn - 2 if cn >= 34 else None
        fl_str = f"{foot_length}cm" if foot_length else "-"
        
        print(f"{cn:<6} {eu:<6} {us_men:<8} {us_women:<8} {uk:<6} {jp:<6} {fl_str:<10}")
    
    print("\n根据脚长选择鞋码:")
    foot_lengths = [23, 24, 25, 26, 27]
    for fl in foot_lengths:
        size = convert_shoe_size_by_cm(fl)
        print(f"  脚长 {fl}cm → 中国码 {size}")
    
    print("\n示例:")
    print(f"  中国码 38 → 美国女码: {convert_shoe_size(38, SizeRegion.CN, SizeRegion.US, 'women')}")
    print(f"  美国男码 9 → 中国码: {convert_shoe_size(9, SizeRegion.US, SizeRegion.CN, 'men')}")
    print(f"  欧洲码 42 → 英国码: {convert_shoe_size(42, SizeRegion.EU, SizeRegion.UK, 'unisex')}")


def example_bra_size_calculation():
    """文胸尺码计算示例"""
    print("\n" + "=" * 60)
    print("👙 文胸尺码计算")
    print("=" * 60)
    
    print("\n测量方法:")
    print("  1. 下胸围: 胸部下方水平测量")
    print("  2. 上胸围: 胸部最高点水平测量")
    print("  罩杯 = 上胸围 - 下胸围")
    
    print("\n罩杯对照表:")
    print("-" * 40)
    print(f"{'罩杯':<6} {'胸围差(cm)':<15} {'说明':<15}")
    print("-" * 40)
    from mod import CUP_SIZES
    for cup, (min_d, max_d, desc) in CUP_SIZES.items():
        diff_range = f"{min_d}-{max_d}" if max_d > min_d else f"≥{min_d}"
        print(f"{cup:<6} {diff_range:<15} {desc:<15}")
    
    print("\n计算示例:")
    # 不同地区的计算结果
    measurements = [
        (70, 82),  # 下胸围70, 上胸围82
        (75, 88),  # 下胸围75, 上胸围88
        (80, 99),  # 下胸围80, 上胸围99
    ]
    
    for underbust, overbust in measurements:
        diff = overbust - underbust
        print(f"\n  下胸围 {underbust}cm, 上胸围 {overbust}cm (差 {diff}cm):")
        print(f"    中国码: {calculate_bra_size(underbust, overbust, SizeRegion.CN)}")
        print(f"    美国码: {calculate_bra_size(underbust, overbust, SizeRegion.US)}")
        print(f"    英国码: {calculate_bra_size(underbust, overbust, SizeRegion.UK)}")


def example_size_recommendation():
    """尺码推荐示例"""
    print("\n" + "=" * 60)
    print("📊 根据三围推荐尺码")
    print("=" * 60)
    
    # 不同身材的推荐
    body_types = [
        {"name": "标准身材 S", "bust": 82, "waist": 66, "hip": 88},
        {"name": "标准身材 M", "bust": 86, "waist": 70, "hip": 92},
        {"name": "标准身材 L", "bust": 90, "waist": 74, "hip": 96},
        {"name": "梨形身材", "bust": 84, "waist": 68, "hip": 98},
        {"name": "苹果身材", "bust": 92, "waist": 80, "hip": 96},
    ]
    
    for body in body_types:
        print(f"\n{body['name']} (胸{body['bust']}/腰{body['waist']}/臀{body['hip']}):")
        
        # 上装推荐
        top_rec = recommend_size_by_measurements(
            body['bust'], body['waist'], body['hip'],
            ClothingType.TOP, SizeRegion.CN
        )
        print(f"  上装推荐: {top_rec['size']}")
        print(f"    胸围适合: {'✓' if top_rec['bust_fit'] else '✗'}")
        print(f"    腰围适合: {'✓' if top_rec['waist_fit'] else '✗'}")
        print(f"    臀围适合: {'✓' if top_rec['hip_fit'] else '✗'}")
        
        # 裤装推荐
        pants_rec = recommend_size_by_measurements(
            body['bust'], body['waist'], body['hip'],
            ClothingType.PANTS, SizeRegion.CN
        )
        print(f"  裤装推荐: {pants_rec['size']}")


def example_quick_guide():
    """快速尺码指南示例"""
    print("\n" + "=" * 60)
    print("⚡ 快速尺码指南")
    print("=" * 60)
    
    print("\n输入您的身体测量数据，一次性获取所有推荐尺码:")
    
    measurements = {
        "bust": 88,
        "waist": 72,
        "hip": 94,
        "foot_length": 25,
        "underbust": 75,
        "overbust": 88,
    }
    
    print("\n测量数据:")
    for key, value in measurements.items():
        print(f"  {key}: {value}cm")
    
    result = quick_size_guide(measurements)
    
    print("\n推荐尺码:")
    for clothing_type, size in result.items():
        type_names = {
            "top": "上装",
            "pants": "裤装",
            "shoes": "鞋子",
            "bra": "文胸"
        }
        print(f"  {type_names.get(clothing_type, clothing_type)}: {size}")


def example_accessories():
    """配饰尺码示例"""
    print("\n" + "=" * 60)
    print("🎀 配饰尺码")
    print("=" * 60)
    
    # 帽子
    print("\n帽子尺码对照表 (头围):")
    print("-" * 40)
    print(f"{'头围(cm)':<10} {'CN':<6} {'US':<10} {'EU':<6}")
    print("-" * 40)
    hat_chart = get_size_chart(ClothingType.HAT, SizeRegion.CN)
    for head_circumference, cn_size in sorted(hat_chart.items()):
        us = get_size_chart(ClothingType.HAT, SizeRegion.US).get(head_circumference, "-")
        eu = get_size_chart(ClothingType.HAT, SizeRegion.EU).get(head_circumference, "-")
        print(f"{head_circumference:<10} {cn_size:<6} {us:<10} {eu:<6}")
    
    # 戒指
    print("\n戒指尺码对照表 (内周长):")
    print("-" * 40)
    print(f"{'周长(mm)':<10} {'CN':<6} {'US':<6} {'EU':<6} {'UK':<6}")
    print("-" * 40)
    ring_chart = get_size_chart(ClothingType.RING, SizeRegion.CN)
    us_chart = get_size_chart(ClothingType.RING, SizeRegion.US)
    eu_chart = get_size_chart(ClothingType.RING, SizeRegion.EU)
    uk_chart = get_size_chart(ClothingType.RING, SizeRegion.UK)
    for circumference in sorted(ring_chart.keys()):
        cn = ring_chart.get(circumference, "-")
        us = us_chart.get(circumference, "-")
        eu = eu_chart.get(circumference, "-")
        uk = uk_chart.get(circumference, "-")
        print(f"{circumference:<10} {cn:<6} {us:<6} {eu:<6} {uk:<6}")
    
    # 手套
    print("\n手套尺码对照表 (手掌周长):")
    print("-" * 40)
    print(f"{'周长(cm)':<10} {'CN':<6} {'US':<6} {'EU':<6} {'UK':<6}")
    print("-" * 40)
    glove_chart = get_size_chart(ClothingType.GLOVES, SizeRegion.CN)
    us_chart = get_size_chart(ClothingType.GLOVES, SizeRegion.US)
    eu_chart = get_size_chart(ClothingType.GLOVES, SizeRegion.EU)
    uk_chart = get_size_chart(ClothingType.GLOVES, SizeRegion.UK)
    for circumference in sorted(glove_chart.keys()):
        cn = glove_chart.get(circumference, "-")
        us = us_chart.get(circumference, "-")
        eu = eu_chart.get(circumference, "-")
        uk = uk_chart.get(circumference, "-")
        print(f"{circumference:<10} {cn:<6} {us:<6} {eu:<6} {uk:<6}")


def example_supported_regions():
    """支持的地区"""
    print("\n" + "=" * 60)
    print("🌍 支持的地区标准")
    print("=" * 60)
    
    print("\n地区:")
    for i, region in enumerate(list_all_regions(), 1):
        print(f"  {i}. {region}")
    
    print("\n支持的服装类型:")
    for i, clothing_type in enumerate(list_all_clothing_types(), 1):
        print(f"  {i}. {clothing_type}")


def main():
    """运行所有示例"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "服装尺码转换工具示例" + " " * 15 + "║")
    print("╚" + "═" * 58 + "╝")
    
    example_top_size_conversion()
    example_pants_size_conversion()
    example_shoe_size_conversion()
    example_bra_size_calculation()
    example_size_recommendation()
    example_quick_guide()
    example_accessories()
    example_supported_regions()
    
    print("\n" + "=" * 60)
    print("示例完成!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()