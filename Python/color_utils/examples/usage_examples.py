"""
颜色工具使用示例

演示所有主要功能：
1. 创建颜色对象
2. 格式转换
3. 颜色混合
4. 对比度计算
5. 配色方案生成
6. 渐变创建
7. 随机颜色
8. 颜色名称
9. 文本颜色建议
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Color, parse_color,
    rgb_to_hsl, hsl_to_rgb,
    rgb_to_hsv, hsv_to_rgb,
    rgb_to_cmyk, cmyk_to_rgb,
    mix_colors, adjust_lightness, adjust_saturation,
    calculate_contrast_ratio, wcag_compliance,
    get_complement_color, get_analogous_colors, get_triadic_colors,
    get_split_complementary_colors, get_tetradic_colors,
    get_monochromatic_colors, get_shades, get_tints, get_tones,
    create_gradient, create_multi_gradient,
    random_color, random_pastel_color, random_vibrant_color,
    color_name_to_hex, hex_to_color_name,
    suggest_text_color,
    hex_to_rgb, rgb_to_hex,
)


def example_1_create_colors():
    """示例 1：创建颜色对象"""
    print("\n=== 示例 1：创建颜色对象 ===\n")
    
    # 从 HEX 创建
    red = Color.from_hex('#FF0000')
    print(f"从 HEX 创建: {red}")
    
    # 从 RGB 创建
    green = Color.from_rgb(0, 255, 0)
    print(f"从 RGB 创建: {green}")
    
    # 从 HSL 创建
    blue = Color.from_hsl(240, 100, 50)
    print(f"从 HSL 创建: {blue}")
    
    # 从 HSV 创建
    cyan = Color.from_hsv(180, 100, 100)
    print(f"从 HSV 创建: {cyan}")
    
    # 从 CMYK 创建
    yellow = Color.from_cmyk(0, 0, 100, 0)
    print(f"从 CMYK 创建: {yellow}")
    
    # 带透明度的颜色
    transparent_red = Color.from_hex('#FF000080')
    print(f"半透明红色: {transparent_red.hex_alpha}")
    
    # 通用解析
    color = parse_color('#4A90D9')
    print(f"通用解析: {color}")


def example_2_format_conversion():
    """示例 2：格式转换"""
    print("\n=== 示例 2：格式转换 ===\n")
    
    # 创建一个颜色
    color = Color.from_hex('#4A90D9')
    
    print(f"原始颜色: {color.hex}")
    print(f"\n格式转换结果:")
    print(f"  RGB:  {color.rgb}")
    print(f"  RGBA: {color.rgba}")
    print(f"  HSL:  {color.hsl} (色相, 饱和度%, 明度%)")
    print(f"  HSV:  {color.hsv} (色相, 饱和度%, 明度%)")
    print(f"  CMYK: {color.cmyk} (青%, 品红%, 黄%, 黑%)")
    
    # 亮度属性
    print(f"\n亮度: {color.luminance:.4f}")
    print(f"是浅色: {color.is_light}")
    print(f"是深色: {color.is_dark}")
    
    # 函数转换
    print("\n函数方式转换:")
    h, s, l = rgb_to_hsl(74, 144, 217)
    print(f"  RGB(74, 144, 217) -> HSL({h}, {s}%, {l}%)")
    
    r, g, b = hsl_to_rgb(210, 60, 57)
    print(f"  HSL(210, 60%, 57%) -> RGB({r}, {g}, {b})")


def example_3_color_mixing():
    """示例 3：颜色混合"""
    print("\n=== 示例 3：颜色混合 ===\n")
    
    red = Color.from_hex('#FF0000')
    blue = Color.from_hex('#0000FF')
    
    # 不同比例混合
    print("红 + 蓝 混合:")
    for ratio in [0.0, 0.25, 0.5, 0.75, 1.0]:
        mixed = mix_colors(red, blue, ratio)
        print(f"  {ratio:.2f}: {mixed.hex}")
    
    # 使用 Color 对象方法
    print("\n使用 Color 对象方法:")
    purple = red.mix(blue, 0.5)
    print(f"  red.mix(blue, 0.5) = {purple.hex}")
    
    # 混合多个颜色
    print("\n混合多个颜色 (创建渐变色):")
    gradient = create_gradient(red, blue, 5)
    for c in gradient:
        print(f"  {c.hex}")


def example_4_color_adjustment():
    """示例 4：颜色调整"""
    print("\n=== 示例 4：颜色调整 ===\n")
    
    color = Color.from_hex('#FF0000')
    
    # 调整明度
    print("明度调整:")
    for amount in [-0.4, -0.2, 0.0, 0.2, 0.4]:
        adjusted = adjust_lightness(color, amount)
        print(f"  {amount:+.1f}: {adjusted.hex}")
    
    # 调整饱和度
    print("\n饱和度调整:")
    for amount in [0.0, -0.25, -0.5, -0.75, -1.0]:
        adjusted = adjust_saturation(color, amount)
        print(f"  {amount:+.2f}: {adjusted.hex}")
    
    # 色相旋转
    print("\n色相旋转:")
    for degrees in [0, 30, 60, 90, 120, 180]:
        rotated = color.rotate_hue(degrees)
        print(f"  +{degrees}°: {rotated.hex}")
    
    # 使用 Color 对象方法
    print("\nColor 对象方法:")
    lighter = color.lighter(0.2)
    darker = color.darker(0.2)
    saturated = color.saturate(0.1)
    desaturated = color.desaturate(0.5)
    print(f"  lighter(0.2):    {lighter.hex}")
    print(f"  darker(0.2):     {darker.hex}")
    print(f"  saturate(0.1):   {saturated.hex}")
    print(f"  desaturate(0.5): {desaturated.hex}")


def example_5_contrast():
    """示例 5：对比度计算"""
    print("\n=== 示例 5：对比度计算 (WCAG) ===\n")
    
    # 黑白对比度
    black = Color.from_hex('#000000')
    white = Color.from_hex('#FFFFFF')
    
    ratio = calculate_contrast_ratio(black, white)
    print(f"黑白对比度: {ratio:.2f}:1")
    
    compliance = wcag_compliance(black, white)
    print(f"WCAG 合规性:")
    print(f"  AA 普通文本: {compliance['aa_normal']} (要求 >= 4.5:1)")
    print(f"  AA 大文本:   {compliance['aa_large']} (要求 >= 3:1)")
    print(f"  AAA 普通文本: {compliance['aaa_normal']} (要求 >= 7:1)")
    print(f"  AAA 大文本:   {compliance['aaa_large']} (要求 >= 4.5:1)")
    
    # 常见配色对比度
    print("\n常见配色对比度:")
    pairs = [
        ('#FF0000', '#FFFFFF', '红/白'),
        ('#FF0000', '#000000', '红/黑'),
        ('#4A90D9', '#FFFFFF', '蓝灰/白'),
        ('#4A90D9', '#000000', '蓝灰/黑'),
        ('#FFFF00', '#000000', '黄/黑'),
        ('#FFFF00', '#FFFFFF', '黄/白'),
    ]
    
    for hex1, hex2, name in pairs:
        c1 = Color.from_hex(hex1)
        c2 = Color.from_hex(hex2)
        ratio = calculate_contrast_ratio(c1, c2)
        compliance = wcag_compliance(c1, c2)
        aa = '✓' if compliance['aa_normal'] else '✗'
        print(f"  {name}: {ratio:.2f}:1 AA{aa}")


def example_6_color_schemes():
    """示例 6：配色方案生成"""
    print("\n=== 示例 6：配色方案 ===\n")
    
    base_color = Color.from_hex('#FF5733')  # 橙红色
    
    print(f"基础颜色: {base_color.hex}")
    
    # 互补色
    print(f"\n互补色 (180°):")
    complement = get_complement_color(base_color)
    print(f"  {complement.hex}")
    
    # 类似色
    print(f"\n类似色 (±30°):")
    analogous = get_analogous_colors(base_color)
    for i, c in enumerate(analogous):
        label = '原色' if i == 0 else ('左' if i == 1 else '右')
        print(f"  {label}: {c.hex}")
    
    # 三角色
    print(f"\n三角色 (±120°):")
    triadic = get_triadic_colors(base_color)
    for i, c in enumerate(triadic):
        label = '原色' if i == 0 else ('120°' if i == 1 else '240°')
        print(f"  {label}: {c.hex}")
    
    # 分裂互补色
    print(f"\n分裂互补色:")
    split = get_split_complementary_colors(base_color)
    for i, c in enumerate(split):
        label = '原色' if i == 0 else ('150°' if i == 1 else '210°')
        print(f"  {label}: {c.hex}")
    
    # 四角色
    print(f"\n四角色:")
    tetradic = get_tetradic_colors(base_color)
    for i, c in enumerate(tetradic):
        degrees = i * 90
        print(f"  {degrees}°: {c.hex}")
    
    # 单色配色
    print(f"\n单色配色 (同一色相):")
    mono = get_monochromatic_colors(base_color, 5)
    for c in mono:
        print(f"  {c.hex} (L={c.hsl[2]}%)")
    
    # 色阶 (混合黑色)
    print(f"\n色阶 Shades (混黑):")
    shades = get_shades(base_color, 5)
    for c in shades:
        print(f"  {c.hex}")
    
    # 色调 (混合白色)
    print(f"\n色调 Tints (混白):")
    tints = get_tints(base_color, 5)
    for c in tints:
        print(f"  {c.hex}")
    
    # 灰度色调 (混合灰色)
    print(f"\n灰度 Tones (混灰):")
    tones = get_tones(base_color, 5)
    for c in tones:
        print(f"  {c.hex}")


def example_7_gradients():
    """示例 7：渐变生成"""
    print("\n=== 示例 7：渐变生成 ===\n")
    
    # 简单渐变
    print("简单渐变 (红 -> 蓝):")
    red = Color.from_hex('#FF0000')
    blue = Color.from_hex('#0000FF')
    gradient = create_gradient(red, blue, 10)
    
    for c in gradient:
        print(f"  {c.hex}")
    
    # 多色渐变
    print("\n多色渐变 (红 -> 绿 -> 蓝):")
    green = Color.from_hex('#00FF00')
    multi_gradient = create_multi_gradient([red, green, blue], 11)
    
    for c in multi_gradient:
        print(f"  {c.hex}")
    
    # 阳光渐变
    print("\n阳光渐变 (橙 -> 黄 -> 绿 -> 蓝 -> 紫):")
    orange = Color.from_hex('#FF7F00')
    yellow = Color.from_hex('#FFFF00')
    blue = Color.from_hex('#0000FF')
    purple = Color.from_hex('#800080')
    rainbow = create_multi_gradient([orange, yellow, green, blue, purple], 21)
    
    # 只显示部分
    for i, c in enumerate(rainbow[::5]):
        print(f"  {c.hex}")


def example_8_random_colors():
    """示例 8：随机颜色"""
    print("\n=== 示例 8：随机颜色生成 ===\n")
    
    # 完全随机
    print("完全随机:")
    for _ in range(5):
        c = random_color()
        print(f"  {c.hex}")
    
    # 柔和色
    print("\n柔和色 (Pastel):")
    for _ in range(5):
        c = random_pastel_color()
        print(f"  {c.hex}")
    
    # 鲜艳色
    print("\n鲜艳色 (Vibrant):")
    for _ in range(5):
        c = random_vibrant_color()
        print(f"  {c.hex}")
    
    # 深色
    print("\n深色:")
    for _ in range(5):
        c = random_dark_color()
        print(f"  {c.hex}")
    
    # 浅色
    print("\n浅色:")
    for _ in range(5):
        c = random_light_color()
        print(f"  {c.hex}")
    
    # 限制色相范围
    print("\n暖色 (色相 0-60):")
    for _ in range(5):
        c = random_color(hue_range=(0, 60))
        print(f"  {c.hex} (H={c.hsl[0]}°)")


def example_9_color_names():
    """示例 9：颜色名称"""
    print("\n=== 示例 9：颜色名称 ===\n")
    
    # 名称转 HEX
    print("名称 -> HEX:")
    names = ['red', 'blue', 'green', 'yellow', 'purple', 'coral', 'turquoise']
    for name in names:
        hex_val = color_name_to_hex(name)
        print(f"  {name}: {hex_val}")
    
    # HEX 转名称
    print("\nHEX -> 名称:")
    hex_colors = ['#FF0000', '#00FF00', '#0000FF', '#FFA500', '#40E0D0', '#FF1493']
    for hex_val in hex_colors:
        name = hex_to_color_name(hex_val)
        print(f"  {hex_val}: {name}")
    
    # 接近的颜色名称
    print("\n接近的颜色:")
    similar = ['#FF0001', '#FE0000', '#FF0101']  # 接近红色
    for hex_val in similar:
        name = hex_to_color_name(hex_val)
        print(f"  {hex_val}: {name}")


def example_10_text_color():
    """示例 10：文本颜色建议"""
    print("\n=== 示例 10：文本颜色建议 ===\n")
    
    backgrounds = [
        '#000000',  # 黑色
        '#FFFFFF',  # 白色
        '#FF5733',  # 橙色
        '#4A90D9',  # 蓝灰
        '#00FF00',  # 绿色
        '#808080',  # 灰色
    ]
    
    print("背景色 -> 建议文本色:")
    for bg_hex in backgrounds:
        bg = Color.from_hex(bg_hex)
        text = suggest_text_color(bg)
        ratio = calculate_contrast_ratio(bg, text)
        print(f"  背景 {bg_hex} -> 文本 {text.hex} (对比度: {ratio:.2f}:1)")


def example_11_practical_usage():
    """示例 11：实际应用"""
    print("\n=== 示例 11：实际应用 ===\n")
    
    # 1. 生成品牌配色方案
    print("品牌配色方案生成:")
    brand_color = Color.from_hex('#4A90D9')  # 主色
    
    # 生成完整配色方案
    scheme = {
        'primary': brand_color,
        'secondary': brand_color.rotate_hue(30),
        'accent': get_complement_color(brand_color),
        'dark': brand_color.darker(0.3),
        'light': brand_color.lighter(0.3),
    }
    
    for name, color in scheme.items():
        print(f"  {name}: {color.hex}")
    
    # 2. 生成按钮配色
    print("\n按钮配色:")
    btn_color = Color.from_hex('#28A745')  # 绿色
    btn_styles = {
        'normal': btn_color,
        'hover': btn_color.lighter(0.1),
        'active': btn_color.darker(0.1),
        'disabled': btn_color.desaturate(0.7).lighter(0.2),
    }
    
    for state, color in btn_styles.items():
        print(f"  {state}: {color.hex}")
    
    # 3. 生成图表配色
    print("\n图表配色 (三角色方案):")
    chart_colors = get_triadic_colors(Color.from_hex('#FF5733'))
    for i, color in enumerate(chart_colors):
        print(f"  系列 {i+1}: {color.hex}")
    
    # 4. 检查文字可读性
    print("\n可读性检查:")
    background = Color.from_hex('#333333')
    text_colors = ['#FFFFFF', '#CCCCCC', '#999999', '#666666']
    
    for text_hex in text_colors:
        text = Color.from_hex(text_hex)
        compliance = wcag_compliance(background, text)
        ratio = compliance['contrast_ratio']
        aa = '✓' if compliance['aa_normal'] else '✗'
        aaa = '✓' if compliance['aaa_normal'] else '✗'
        print(f"  {text_hex}: {ratio:.2f}:1 AA{aa} AAA{aaa}")


def run_all_examples():
    """运行所有示例"""
    examples = [
        example_1_create_colors,
        example_2_format_conversion,
        example_3_color_mixing,
        example_4_color_adjustment,
        example_5_contrast,
        example_6_color_schemes,
        example_7_gradients,
        example_8_random_colors,
        example_9_color_names,
        example_10_text_color,
        example_11_practical_usage,
    ]
    
    print("\n" + "=" * 60)
    print("颜色工具使用示例")
    print("=" * 60)
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n错误: {example.__name__} - {e}")
    
    print("\n" + "=" * 60)
    print("示例完成")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()