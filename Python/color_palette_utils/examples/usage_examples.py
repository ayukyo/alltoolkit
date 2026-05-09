"""
颜色调色板工具使用示例

展示各种调色板生成和使用方式。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from color_palette_utils.mod import (
    # 颜色空间转换
    hex_to_rgb, rgb_to_hex, rgb_to_hsl, hsl_to_rgb, hex_to_hsl, hsl_to_hex,
    # 颜色调整
    adjust_lightness, adjust_saturation, get_complementary,
    # 调色板生成
    generate_complementary_palette, generate_analogous_palette,
    generate_triadic_palette, generate_split_complementary_palette,
    generate_tetradic_palette, generate_pentadic_palette,
    generate_monochromatic_palette, generate_shades, generate_tints,
    generate_tones, generate_gradient, generate_multi_gradient,
    # 随机调色板
    random_color, random_palette, random_harmonious_palette,
    random_warm_palette, random_cool_palette, random_pastel_palette,
    # 导出
    palette_to_css_variables, palette_to_scss_variables,
    palette_to_json, palette_to_tailwind_config,
    # 对比度和可访问性
    get_contrast_ratio, meets_wcag_aa, meets_wcag_aaa,
    suggest_accessible_color,
    # 工具函数
    blend_colors, is_light_color, is_warm_color, color_temperature,
    get_color_name,
    # 类
    ColorPalette, create_palette,
)


def example_color_conversion():
    """颜色空间转换示例。"""
    print("\n" + "=" * 50)
    print("颜色空间转换示例")
    print("=" * 50)
    
    # 十六进制转 RGB
    hex_color = '#FF5733'
    rgb = hex_to_rgb(hex_color)
    print(f"\n十六进制 {hex_color} -> RGB: {rgb}")
    
    # RGB 转 HSL
    hsl = rgb_to_hsl(*rgb)
    print(f"RGB {rgb} -> HSL: 色相={hsl[0]}°, 饱和度={hsl[1]}%, 亮度={hsl[2]}%")
    
    # HSL 转十六进制
    back_to_hex = hsl_to_hex(*hsl)
    print(f"HSL {hsl} -> 十六进制: {back_to_hex}")
    
    # 快捷转换
    hsl_direct = hex_to_hsl('#3498DB')
    print(f"\n快捷: #3498DB -> HSL: 色相={hsl_direct[0]}°, 饱和度={hsl_direct[1]}%, 亮度={hsl_direct[2]}%")


def example_color_adjustment():
    """颜色调整示例。"""
    print("\n" + "=" * 50)
    print("颜色调整示例")
    print("=" * 50)
    
    base = '#FF5733'
    
    # 亮度调整
    lighter = adjust_lightness(base, 30)
    darker = adjust_lightness(base, -30)
    print(f"\n基础色: {base}")
    print(f"变亮 +30%: {lighter}")
    print(f"变暗 -30%: {darker}")
    
    # 饱和度调整
    more_saturated = adjust_saturation(base, 20)
    less_saturated = adjust_saturation(base, -20)
    print(f"\n增加饱和度 +20%: {more_saturated}")
    print(f"降低饱和度 -20%: {less_saturated}")
    
    # 互补色
    complementary = get_complementary(base)
    print(f"\n互补色: {complementary}")


def example_palette_generation():
    """调色板生成示例。"""
    print("\n" + "=" * 50)
    print("调色板生成示例")
    print("=" * 50)
    
    base = '#FF5733'
    
    # 互补色调色板
    complementary = generate_complementary_palette(base)
    print(f"\n互补色调色板 (2色): {complementary}")
    
    # 类似色调色板
    analogous = generate_analogous_palette(base)
    print(f"\n类似色调色板 (3色): {analogous}")
    
    # 三角色调色板
    triadic = generate_triadic_palette(base)
    print(f"\n三角色调色板 (3色): {triadic}")
    
    # 分裂互补色调色板
    split = generate_split_complementary_palette(base)
    print(f"\n分裂互补色调色板 (3色): {split}")
    
    # 四角色调色板
    tetradic = generate_tetradic_palette(base)
    print(f"\n四角色调色板 (4色): {tetradic}")
    
    # 五角色调色板
    pentadic = generate_pentadic_palette(base)
    print(f"\n五角色调色板 (5色): {pentadic}")
    
    # 单色调色板
    mono = generate_monochromatic_palette(base, 5)
    print(f"\n单色调色板 (5色): {mono}")


def example_shades_tints_tones():
    """阴影、着色、色调示例。"""
    print("\n" + "=" * 50)
    print("阴影、着色、色调示例")
    print("=" * 50)
    
    base = '#FF5733'
    
    # 阴影（变暗）
    shades = generate_shades(base, 5)
    print(f"\n基础色: {base}")
    print(f"阴影色 (5色): {shades}")
    
    # 着色（变亮）
    tints = generate_tints(base, 5)
    print(f"着色色 (5色): {tints}")
    
    # 色调（降低饱和度）
    tones = generate_tones(base, 5)
    print(f"色调色 (5色): {tones}")


def example_gradient():
    """渐变示例。"""
    print("\n" + "=" * 50)
    print("渐变示例")
    print("=" * 50)
    
    # 单段渐变
    gradient = generate_gradient('#FF5733', '#3498DB', 10)
    print(f"\n从 #FF5733 到 #3498DB 的 10 步渐变:")
    for i, color in enumerate(gradient):
        print(f"  第 {i+1} 步: {color}")
    
    # 多色渐变
    multi_gradient = generate_multi_gradient(['#FF5733', '#3498DB', '#2ECC71'], 4)
    print(f"\n多色渐变 (3个颜色，每段4步): {multi_gradient}")


def example_random_palettes():
    """随机调色板示例。"""
    print("\n" + "=" * 50)
    print("随机调色板示例")
    print("=" * 50)
    
    # 随机颜色
    print(f"\n单个随机颜色: {random_color()}")
    
    # 随机调色板
    print(f"\n随机调色板 (5色): {random_palette(5)}")
    
    # 随机和谐调色板
    for harmony_type in ['complementary', 'triadic', 'tetradic']:
        palette = random_harmonious_palette(harmony_type)
        print(f"\n{harmony_type} 和谐调色板: {palette}")
    
    # 暖色调调色板
    warm = random_warm_palette(5)
    print(f"\n暖色调调色板: {warm}")
    
    # 冷色调调色板
    cool = random_cool_palette(5)
    print(f"\n冷色调调色板: {cool}")
    
    # 柔和色调调色板
    pastel = random_pastel_palette(5)
    print(f"\n柔和色调调色板: {pastel}")


def example_palette_export():
    """调色板导出示例。"""
    print("\n" + "=" * 50)
    print("调色板导出示例")
    print("=" * 50)
    
    palette = ['#FF5733', '#3498DB', '#2ECC71', '#9B59B6', '#F1C40F']
    
    # CSS 变量
    css = palette_to_css_variables(palette, prefix='theme')
    print(f"\nCSS 变量导出:")
    print(css)
    
    # SCSS 变量
    scss = palette_to_scss_variables(palette, prefix='theme')
    print(f"\nSCSS 变量导出:")
    print(scss)
    
    # JSON
    json_data = palette_to_json(palette, 'ThemeColors', include_rgb=True)
    print(f"\nJSON 导出:")
    print(json_data)
    
    # Tailwind 配置
    tailwind = palette_to_tailwind_config(palette, 'theme')
    print(f"\nTailwind 配置导出:")
    print(tailwind)


def example_accessibility():
    """可访问性示例。"""
    print("\n" + "=" * 50)
    print("可访问性示例")
    print("=" * 50)
    
    # 对比度计算
    foreground = '#333333'
    background = '#FFFFFF'
    ratio = get_contrast_ratio(foreground, background)
    print(f"\n前景色 {foreground} 在背景色 {background} 上的对比度: {ratio:.2f}:1")
    
    # WCAG 标准检查
    meets_aa = meets_wcag_aa(foreground, background)
    meets_aaa = meets_wcag_aaa(foreground, background)
    print(f"满足 WCAG AA: {meets_aa}")
    print(f"满足 WCAG AAA: {meets_aaa}")
    
    # 不满足的情况
    light_fg = '#CCCCCC'
    ratio2 = get_contrast_ratio(light_fg, background)
    print(f"\n浅色前景 {light_fg} 对比度: {ratio2:.2f}:1")
    print(f"满足 WCAG AA: {meets_wcag_aa(light_fg, background)}")
    
    # 建议可访问颜色
    suggested = suggest_accessible_color(light_fg, background)
    suggested_ratio = get_contrast_ratio(suggested, background)
    print(f"\n建议颜色: {suggested} (对比度: {suggested_ratio:.2f}:1)")


def example_color_utilities():
    """颜色工具函数示例。"""
    print("\n" + "=" * 50)
    print("颜色工具函数示例")
    print("=" * 50)
    
    # 颜色混合
    blended = blend_colors('#FF5733', '#3498DB', 0.5)
    print(f"\n混合 #FF5733 和 #3498DB (50%): {blended}")
    
    # 明暗判断
    colors = ['#FFFFFF', '#EEEEEE', '#808080', '#333333', '#000000']
    print(f"\n明暗判断:")
    for color in colors:
        is_light = is_light_color(color)
        print(f"  {color}: {'浅色' if is_light else '深色'}")
    
    # 温度判断
    warm_colors = ['#FF0000', '#FFA500', '#FFFF00']
    cool_colors = ['#0000FF', '#00FFFF', '#008080']
    
    print(f"\n温度判断:")
    print("暖色:")
    for color in warm_colors:
        temp = color_temperature(color)
        print(f"  {color}: {temp}")
    print("冷色:")
    for color in cool_colors:
        temp = color_temperature(color)
        print(f"  {color}: {temp}")
    
    # 颜色名称
    named_colors = ['#FF0000', '#00FF00', '#0000FF', '#FFA500', '#800080']
    print(f"\n颜色名称:")
    for color in named_colors:
        name = get_color_name(color)
        print(f"  {color}: {name}")


def example_color_palette_class():
    """ColorPalette 类示例。"""
    print("\n" + "=" * 50)
    print("ColorPalette 类示例")
    print("=" * 50)
    
    # 从基础颜色创建
    palette = ColorPalette.from_base_color('#3498DB', 'triadic', 'MyTheme')
    print(f"\n从 #3498DB 创建三角调色板:")
    print(f"名称: {palette.name}")
    print(f"颜色: {palette.colors}")
    
    # 添加颜色
    palette.add_color('#F1C40F')
    print(f"\n添加 #F1C40F 后: {palette.colors}")
    
    # 导出
    print(f"\n导出为 CSS 变量:")
    print(palette.to_css('mytheme'))
    
    # 创建渐变调色板
    gradient_palette = ColorPalette.gradient('#FF5733', '#3498DB', 8, 'GradientTheme')
    print(f"\n渐变调色板: {gradient_palette.colors}")
    
    # 创建随机调色板
    random_palette = ColorPalette.random(5, 'RandomTheme')
    print(f"\n随机调色板: {random_palette.colors}")
    
    # 阴影扩展
    original = ColorPalette(['#3498DB'])
    with_shades = original.with_shades(3)
    print(f"\n原色 ['#3498DB'] + 阴影: {with_shades.colors}")
    
    # 着色扩展
    with_tints = original.with_tints(3)
    print(f"\n原色 ['#3498DB'] + 着色: {with_tints.colors}")


def example_complete_workflow():
    """完整工作流示例。"""
    print("\n" + "=" * 50)
    print("完整工作流示例 - 为网站创建调色板")
    print("=" * 50)
    
    # 1. 选择品牌色
    brand_color = '#E74C3C'  # 红色
    
    # 2. 生成和谐调色板
    harmony_palette = create_palette(brand_color, 'split_complementary')
    print(f"\n品牌色: {brand_color}")
    print(f"分裂互补色调色板: {harmony_palette.colors}")
    
    # 3. 生成阴影和着色变体
    full_palette = harmony_palette.with_shades(2).with_tints(2)
    print(f"\n完整调色板 (含阴影和着色): {full_palette.colors}")
    
    # 4. 导出为 CSS 变量
    print(f"\n导出为 CSS 变量 (用于网站):")
    css_vars = palette_to_css_variables(
        full_palette.colors, 
        prefix='color',
        variable_names=['primary', 'primary-shade-1', 'primary-shade-2', 
                        'primary-tint-1', 'primary-tint-2', 
                        'secondary', 'secondary-shade-1', 'secondary-shade-2',
                        'secondary-tint-1', 'secondary-tint-2',
                        'tertiary', 'tertiary-shade-1', 'tertiary-shade-2',
                        'tertiary-tint-1', 'tertiary-tint-2']
    )
    print(css_vars)
    
    # 5. 检查可访问性
    print(f"\n可访问性检查:")
    for color in harmony_palette.colors[:3]:
        white_ratio = get_contrast_ratio(color, '#FFFFFF')
        black_ratio = get_contrast_ratio(color, '#000000')
        print(f"  {color}:")
        print(f"    在白底上: {white_ratio:.2f}:1 (WCAG AA: {meets_wcag_aa(color, '#FFFFFF')})")
        print(f"    在黑底上: {black_ratio:.2f}:1 (WCAG AA: {meets_wcag_aa(color, '#000000')})")


def main():
    """运行所有示例。"""
    print("\n" + "=" * 60)
    print("颜色调色板工具使用示例")
    print("=" * 60)
    
    example_color_conversion()
    example_color_adjustment()
    example_palette_generation()
    example_shades_tints_tones()
    example_gradient()
    example_random_palettes()
    example_palette_export()
    example_accessibility()
    example_color_utilities()
    example_color_palette_class()
    example_complete_workflow()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()