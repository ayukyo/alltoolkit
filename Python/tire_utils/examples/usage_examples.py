"""
Tire Utilities 使用示例

演示轮胎计算工具的各项功能
"""

import sys
sys.path.insert(0, '..')
from mod import (
    parse_tire_spec, calculate_dimensions, convert_pressure,
    parse_dot_code, get_tire_age, get_speed_rating_info, get_load_index_info,
    compare_tire_sizes, recommend_tire_pressure, evaluate_tire_wear,
    find_compatible_sizes, calculate_plus_sizing, tire_info
)
from datetime import datetime


def main():
    print("=" * 60)
    print("Tire Utilities 使用示例")
    print("=" * 60)
    
    # 1. 解析轮胎规格
    print("\n【1. 轮胎规格解析】")
    specs = [
        "225/50R17",
        "225/50R17 94V",
        "265/70R17",
        "P225/50R17",
        "LT265/70R17"
    ]
    
    for spec_str in specs:
        spec = parse_tire_spec(spec_str)
        if spec:
            print(f"  {spec_str} → {spec}")
            print(f"    断面宽度: {spec.width}mm, 扁平比: {spec.aspect_ratio}%")
            print(f"    轮辋直径: {spec.rim_diameter}英寸, 结构: {spec.construction}")
            if spec.load_index and spec.speed_rating:
                print(f"    载重指数: {spec.load_index}, 速度等级: {spec.speed_rating}")
        else:
            print(f"  {spec_str} → 解析失败")
    
    # 2. 计算轮胎尺寸
    print("\n【2. 轮胎尺寸计算】")
    spec = parse_tire_spec("225/50R17")
    dims = calculate_dimensions(spec)
    
    print(f"  轮胎规格: {spec}")
    print(f"  断面宽度: {dims.section_width_mm}mm")
    print(f"  断面高度: {dims.section_height_mm:.1f}mm")
    print(f"  外直径: {dims.overall_diameter_mm:.1f}mm ({dims.overall_diameter_inch:.2f}英寸)")
    print(f"  周长: {dims.circumference_mm:.1f}mm ({dims.circumference_inch:.1f}英寸)")
    print(f"  每公里转速: {dims.revolutions_per_km:.1f}次")
    print(f"  每英里转速: {dims.revolutions_per_mile:.1f}次")
    
    # 3. 胎压单位转换
    print("\n【3. 胎压单位转换】")
    
    pressures = [
        (32, 'psi', 'kpa'),
        (32, 'psi', 'bar'),
        (220, 'kpa', 'psi'),
        (2.5, 'bar', 'psi'),
        (35, 'psi', 'kg_cm2')
    ]
    
    for value, from_unit, to_unit in pressures:
        result = convert_pressure(value, from_unit, to_unit)
        print(f"  {value} {from_unit} = {result:.1f} {to_unit}")
    
    # 4. DOT 编码解析
    print("\n【4. DOT 编码解析】")
    dot_codes = [
        "DOT U2LL LMLR 3519",
        "2523",
        "5200"
    ]
    
    for dot in dot_codes:
        result = parse_dot_code(dot)
        if result:
            week, year = result
            print(f"  {dot} → 第{week}周, {year}年")
            
            # 计算轮胎年龄
            age = get_tire_age(dot, datetime(2025, 5, 25))
            print(f"    当前年龄: {age}年")
        else:
            print(f"  {dot} → 解析失败")
    
    # 5. 速度等级信息
    print("\n【5. 速度等级信息】")
    ratings = ['S', 'T', 'H', 'V', 'W', 'Y', 'ZR']
    
    for rating in ratings:
        info = get_speed_rating_info(rating)
        if info:
            print(f"  {rating}: 最高速度 {info['max_speed_kmh']}km/h ({info['max_speed_mph']}mph)")
            print(f"    适用: {info['description']}")
    
    # 6. 载重指数信息
    print("\n【6. 载重指数信息】")
    indices = [80, 94, 100, 120]
    
    for idx in indices:
        info = get_load_index_info(idx)
        if info:
            print(f"  {idx}: 最大载重 {info['max_load_kg']}kg ({info['max_load_lbs']}lbs)")
            print(f"    单轴承载力: {info['axle_capacity_kg']}kg")
    
    # 7. 胎压推荐
    print("\n【7. 胎压推荐】")
    
    for width in [195, 225, 255, 265]:
        rec = recommend_tire_pressure(width, 'sedan')
        print(f"  {width}mm宽度轿车推荐胎压:")
        print(f"    前轮: {rec['front_psi']}psi ({rec['front_kpa']}kpa)")
        print(f"    后轮: {rec['rear_psi']}psi ({rec['rear_kpa']}kpa)")
        print(f"    注意: {rec['note']}")
    
    # 8. 轮胎磨损评估
    print("\n【8. 轮胎磨损评估】")
    
    tread_depths = [8.0, 5.0, 3.5, 2.5, 1.5]
    
    for depth in tread_depths:
        result = evaluate_tire_wear(depth)
        print(f"  花纹深度 {depth}mm:")
        print(f"    磨损程度: {result['wear_percent']}%, 剩余: {result['remaining_percent']}%")
        print(f"    状态: {result['status']}")
        print(f"    建议: {result['recommendation']}")
        print(f"    估算剩余里程: {result['estimated_remaining_km']}km")
    
    # 9. 轮胎尺寸比较
    print("\n【9. 轮胎尺寸比较】")
    
    comparisons = [
        ("225/50R17", "235/50R17"),  # 更宽
        ("225/50R17", "225/55R17"),  # 更高扁平比
        ("225/50R17", "225/45R18"),  # Plus One
    ]
    
    for spec1_str, spec2_str in comparisons:
        spec1 = parse_tire_spec(spec1_str)
        spec2 = parse_tire_spec(spec2_str)
        diff = compare_tire_sizes(spec1, spec2)
        
        print(f"  {spec1_str} vs {spec2_str}:")
        print(f"    宽度差异: {diff['width_diff_percent']:.1f}%")
        print(f"    直径差异: {diff['diameter_diff_percent']:.1f}%")
        print(f"    周长差异: {diff['circumference_diff_percent']:.1f}%")
        print(f"    速度表误差: {diff['speedometer_error_percent']:.1f}%")
        print(f"    离地间隙变化: {diff['ground_clearance_diff_mm']:.1f}mm")
    
    # 10. 查找兼容尺寸
    print("\n【10. 查找兼容尺寸】")
    
    original = parse_tire_spec("225/50R17")
    compatible = find_compatible_sizes(original, tolerance_percent=2.0)
    
    print(f"  与 225/50R17 兼容的轮胎规格 (±2%直径差异):")
    for c_spec in compatible[:10]:
        c_dims = calculate_dimensions(c_spec)
        o_dims = calculate_dimensions(original)
        diff = abs(c_dims.overall_diameter_mm - o_dims.overall_diameter_mm) / o_dims.overall_diameter_mm * 100
        print(f"    {c_spec} - 直径差异: {diff:.1f}%")
    
    print(f"  共找到 {len(compatible)} 个兼容规格")
    
    # 11. Plus Sizing 计算
    print("\n【11. Plus Sizing 计算】")
    
    original = parse_tire_spec("225/50R17")
    print(f"  原规格: {original}")
    
    for new_rim in [18, 19]:
        options = calculate_plus_sizing(original, new_rim)
        print(f"\n  升级到 {new_rim}英寸轮辋的选项:")
        for opt in options[:5]:
            opt_dims = calculate_dimensions(opt)
            o_dims = calculate_dimensions(original)
            diff = abs(opt_dims.overall_diameter_mm - o_dims.overall_diameter_mm) / o_dims.overall_diameter_mm * 100
            print(f"    {opt} - 直径差异: {diff:.2f}%")
    
    # 12. 获取完整轮胎信息
    print("\n【12. 获取完整轮胎信息】")
    
    full_specs = ["225/50R17 94V", "265/70R17 113S", "275/35R20 102Y"]
    
    for spec_str in full_specs:
        info = tire_info(spec_str)
        if 'error' not in info:
            print(f"\n  【{info['spec']}】")
            print(f"  结构类型: {info['construction']}")
            print(f"  外直径: {info['dimensions']['overall_diameter_mm']}mm")
            print(f"  周长: {info['dimensions']['circumference_mm']}mm")
            print(f"  每公里转速: {info['dimensions']['revolutions_per_km']}次")
            
            if 'speed_rating' in info:
                print(f"  速度等级: {info['speed_rating']['rating']}")
                print(f"    最高速度: {info['speed_rating']['max_speed_kmh']}km/h")
                print(f"    适用类型: {info['speed_rating']['description']}")
            
            if 'load_index' in info:
                print(f"  载重指数: {info['load_index']['index']}")
                print(f"    最大载重: {info['load_index']['max_load_kg']}kg ({info['load_index']['max_load_lbs']}lbs)")
            
            if 'recommended_pressure' in info:
                print(f"  推荐胎压: 前轮 {info['recommended_pressure']['front_psi']}psi, 后轮 {info['recommended_pressure']['rear_psi']}psi")
    
    print("\n" + "=" * 60)
    print("示例演示完成")
    print("=" * 60)


if __name__ == '__main__':
    main()