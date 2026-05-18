"""
色盲模拟与辅助工具 - 使用示例

本示例展示如何使用 colorblind_utils 进行：
1. 色盲视觉模拟
2. 对比度检查
3. 颜色调整建议
4. 调色板生成
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    # 色盲模拟
    simulate_colorblindness, simulate_colorblindness_hex, simulate_all_types,
    # 颜色转换
    rgb_to_hex, hex_to_rgb, rgb_to_hsl,
    # 对比度
    contrast_ratio, wcag_compliance_level, is_colorblind_friendly,
    # 颜色调整
    adjust_for_colorblindness, suggest_colorblind_safe_alternatives,
    generate_colorblind_safe_palette,
    # 辅助
    get_colorblind_type_info, analyze_color_for_colorblindness,
    simulate_palette, check_palette_accessibility,
    # 色盲类型常量
    PROTANOPIA, DEUTERANOPIA, TRITANOPIA, ACHROMATOPSIA,
    PROTANOMALY, DEUTERANOMALY, TRITANOMALY,
    # 简写
    simulate, simulate_hex,
)


def print_separator(title=""):
    """打印分隔符"""
    if title:
        print(f"\n{'=' * 50}")
        print(f" {title}")
        print('=' * 50)
    else:
        print('-' * 50)


def example_1_basic_simulation():
    """示例1: 基本色盲模拟"""
    print_separator("示例1: 基本色盲模拟")
    
    # 模拟红色在不同色盲类型下的表现
    print("\n红色 (255, 0, 0) 在不同色盲类型下的表现:")
    
    for cb_type, info in get_colorblind_type_info().items():
        sim = simulate_colorblindness(255, 0, 0, cb_type)
        hex_color = rgb_to_hex(*sim)
        print(f"  {info['name']:6s}: RGB{str(sim):16s} HEX: {hex_color}")
    
    # 模拟绿色
    print("\n绿色 (0, 255, 0) 在不同色盲类型下的表现:")
    
    for cb_type, info in get_colorblind_type_info().items():
        sim = simulate_colorblindness(0, 255, 0, cb_type)
        hex_color = rgb_to_hex(*sim)
        print(f"  {info['name']:6s}: RGB{str(sim):16s} HEX: {hex_color}")


def example_2_hex_colors():
    """示例2: 使用十六进制颜色"""
    print_separator("示例2: 使用十六进制颜色")
    
    colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF"]
    
    print("\n十六进制颜色在绿色盲 (最常见) 下的模拟:")
    for hex_color in colors:
        sim_hex = simulate_hex(hex_color, DEUTERANOPIA)
        print(f"  {hex_color} → {sim_hex}")


def example_3_contrast_check():
    """示例3: 对比度检查"""
    print_separator("示例3: 对比度检查")
    
    # 常见前景/背景组合
    pairs = [
        ("黑色文字/白色背景", (0, 0, 0), (255, 255, 255)),
        ("红色文字/白色背景", (255, 0, 0), (255, 255, 255)),
        ("绿色文字/白色背景", (0, 255, 0), (255, 255, 255)),
        ("灰色文字/白色背景", (128, 128, 128), (255, 255, 255)),
        ("红色文字/绿色背景", (255, 0, 0), (0, 255, 0)),
    ]
    
    print("\n对比度检查 (WCAG 标准):")
    print("  - AA 级 (正常文本): ≥4.5")
    print("  - AA 级 (大文本): ≥3.0")
    print("  - AAA 级 (正常文本): ≥7.0")
    
    for name, fg, bg in pairs:
        contrast = contrast_ratio(fg, bg)
        compliance = wcag_compliance_level(contrast)
        
        status = "✓" if compliance["aa_normal"] else "✗"
        print(f"\n  {name}:")
        print(f"    对比度: {contrast:.2f}:1 {status}")
        print(f"    AA (正常): {compliance['aa_normal']}, AA (大文本): {compliance['aa_large']}")
        print(f"    AAA (正常): {compliance['aaa_normal']}")


def example_4_colorblind_friendliness():
    """示例4: 色盲友好检测"""
    print_separator("示例4: 色盲友好检测")
    
    pairs = [
        ("黑白", (0, 0, 0), (255, 255, 255)),
        ("红绿", (255, 0, 0), (0, 255, 0)),
        ("蓝黄", (0, 0, 255), (255, 255, 0)),
        ("橙青", (255, 165, 0), (0, 255, 255)),
    ]
    
    print("\n色盲友好检测 (对比度 ≥4.5):")
    for name, fg, bg in pairs:
        friendly = is_colorblind_friendly(fg, bg)
        status = "✓ 友好" if friendly else "✗ 不友好"
        print(f"  {name}: {status}")


def example_5_safe_palette():
    """示例5: 生成色盲安全调色板"""
    print_separator("示例5: 生成色盲安全调色板")
    
    palette = generate_colorblind_safe_palette(7)
    
    print("\n色盲安全调色板 (7色):")
    for i, color in enumerate(palette, 1):
        hex_color = rgb_to_hex(*color)
        print(f"  颜色 {i}: RGB{str(color):16s} HEX: {hex_color}")
    
    # 验证调色板在色盲模拟后的区分度
    print("\n验证调色板在绿色盲下的区分度:")
    sim_palette = simulate_palette(palette, DEUTERANOPIA)
    for i, (orig, sim) in enumerate(zip(palette, sim_palette), 1):
        print(f"  颜色 {i}: {rgb_to_hex(*orig)} → {rgb_to_hex(*sim)}")


def example_6_color_analysis():
    """示例6: 颜色全面分析"""
    print_separator("示例6: 颜色全面分析")
    
    # 分析红色
    analysis = analyze_color_for_colorblindness(255, 0, 0)
    
    print(f"\n分析颜色: {analysis['original']['hex']} (RGB{analysis['original']['rgb']})")
    print(f"HSL: {analysis['original']['hsl']}")
    
    print("\n模拟结果:")
    for cb_type, sim_data in analysis["simulations"].items():
        print(f"  {cb_type:15s}: {sim_data['hex']}")
    
    if analysis["issues"]:
        print("\n问题:")
        for issue in analysis["issues"]:
            print(f"  - {issue}")
    
    if analysis["recommendations"]:
        print("\n建议:")
        for rec in analysis["recommendations"]:
            print(f"  - {rec}")
    
    if analysis["safe_alternatives"]:
        print("\n安全替代色:")
        for alt in analysis["safe_alternatives"]:
            print(f"  - {alt['hex']}")


def example_7_palette_accessibility():
    """示例7: 调色板可访问性检查"""
    print_separator("示例7: 调色板可访问性检查")
    
    # 红绿灯配色 (可能有问题)
    traffic_light = [
        (255, 0, 0),     # 红
        (255, 255, 0),   # 黄
        (0, 255, 0),     # 绿
    ]
    
    print("\n检查红绿灯配色:")
    result = check_palette_accessibility(traffic_light, min_contrast=2.0)
    
    print(f"  检查的颜色对数: {result['pairs_checked']}")
    print(f"  安全的颜色对: {len(result['safe_pairs'])}")
    print(f"  有问题的颜色对: {len(result['problematic_pairs'])}")
    
    if result["issues"]:
        print("\n  问题详情:")
        for issue in result["issues"]:
            print(f"    - {issue}")


def example_8_real_world_use_case():
    """示例8: 实际应用场景"""
    print_separator("示例8: 实际应用场景")
    
    print("\n场景: 设计一个数据可视化图表")
    
    # 首先生成安全调色板
    palette = generate_colorblind_safe_palette(5)
    
    print("\n1. 使用色盲安全调色板:")
    for i, color in enumerate(palette, 1):
        print(f"   数据系列 {i}: {rgb_to_hex(*color)}")
    
    print("\n2. 验证文字对比度:")
    # 白色文字在调色板颜色上的对比度
    for i, bg in enumerate(palette, 1):
        contrast = contrast_ratio((255, 255, 255), bg)
        compliance = wcag_compliance_level(contrast)
        status = "✓" if compliance["aa_large"] else "✗"
        print(f"   白色文字在系列 {i} 背景: 对比度 {contrast:.2f}:1 {status}")
    
    print("\n3. 建议:")
    print("   - 使用图案/纹理辅助区分")
    print("   - 避免仅依赖颜色传达信息")
    print("   - 添加文字标签")


def example_9_all_simulations():
    """示例9: 一次性获取所有模拟结果"""
    print_separator("示例9: 一次性获取所有模拟结果")
    
    color = (255, 128, 0)  # 橙色
    print(f"\n原始颜色: RGB{color} HEX:{rgb_to_hex(*color)}")
    
    all_sims = simulate_all_types(*color)
    
    print("\n所有色盲类型模拟:")
    for cb_type, sim_color in all_sims.items():
        info = get_colorblind_type_info()[cb_type]
        print(f"  {info['name']:6s}: {rgb_to_hex(*sim_color)}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("     色盲模拟与辅助工具 (colorblind_utils) 使用示例")
    print("=" * 60)
    
    example_1_basic_simulation()
    example_2_hex_colors()
    example_3_contrast_check()
    example_4_colorblind_friendliness()
    example_5_safe_palette()
    example_6_color_analysis()
    example_7_palette_accessibility()
    example_8_real_world_use_case()
    example_9_all_simulations()
    
    print_separator()
    print("\n所有示例运行完成！")
    print("提示: 在实际项目中，建议使用 generate_colorblind_safe_palette()")
    print("     生成调色板，并使用 check_palette_accessibility() 验证。")


if __name__ == "__main__":
    main()