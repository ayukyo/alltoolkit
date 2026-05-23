"""
Color Utils 使用示例

展示颜色工具模块的各种用法。
"""

import sys
import os
# 添加 Python 目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Color,
    rgb_to_hsl,
    hsl_to_rgb,
    hex_to_rgb,
    rgb_to_hex,
    name_to_rgb,
    parse_color,
    generate_complementary,
    generate_analogous,
    generate_triadic,
    generate_split_complementary,
    generate_tetradic,
    generate_shades,
    generate_tints,
    generate_gradient,
    generate_monochromatic,
    generate_palette,
    random_color,
    random_pastel,
    random_vibrant,
    random_dark,
    random_light,
    blend_colors,
    get_color_suggestions,
)


def example_basic_color_creation():
    """示例1: 基本颜色创建"""
    print("=" * 50)
    print("示例1: 基本颜色创建")
    print("=" * 50)
    
    # RGB 创建
    color1 = Color(255, 128, 0)
    print(f"RGB 创建: {color1}")
    
    # 十六进制创建
    color2 = Color.from_hex('#ff8000')
    print(f"十六进制创建: {color2}")
    
    # HSL 创建 (色相, 饱和度, 亮度)
    color3 = Color.from_hsl(30, 100, 50)  # 橙色
    print(f"HSL 创建: {color3}")
    
    # HSV 创建 (色相, 饱和度, 明度)
    color4 = Color.from_hsv(120, 100, 100)  # 绿色
    print(f"HSV 创建: {color4}")
    
    # 颜色名称创建
    color5 = Color.from_name('coral')
    print(f"名称创建: {color5}")
    
    # 带透明度
    color6 = Color(255, 128, 0, 0.5)
    print(f"带透明度: {color6}")
    print(f"十六进制(含透明度): {color6.hex_with_alpha}")


def example_color_properties():
    """示例2: 颜色属性"""
    print("\n" + "=" * 50)
    print("示例2: 颜色属性")
    print("=" * 50)
    
    color = Color.from_hex('#ff8000')
    
    print(f"颜色: {color}")
    print(f"RGB: {color.rgb}")
    print(f"RGBA: {color.rgba}")
    print(f"HEX: {color.hex}")
    print(f"HSL: {color.hsl}")
    print(f"HSV: {color.hsv}")
    print(f"亮度: {color.luminance:.3f}")
    print(f"颜色名称: {color.name}")
    print(f"是否浅色: {color.is_light()}")
    print(f"是否深色: {color.is_dark()}")


def example_color_conversion():
    """示例3: 颜色格式转换"""
    print("\n" + "=" * 50)
    print("示例3: 颜色格式转换")
    print("=" * 50)
    
    # RGB <-> HSL
    r, g, b = 255, 128, 0
    h, s, l = rgb_to_hsl(r, g, b)
    print(f"RGB({r}, {g}, {b}) -> HSL({h:.1f}°, {s:.1f}%, {l:.1f}%)")
    
    r2, g2, b2 = hsl_to_rgb(h, s, l)
    print(f"HSL({h:.1f}°, {s:.1f}%, {l:.1f}%) -> RGB({r2}, {g2}, {b2})")
    
    # RGB <-> HEX
    hex_str = rgb_to_hex(255, 0, 0)
    print(f"RGB(255, 0, 0) -> HEX: {hex_str}")
    
    r, g, b, a = hex_to_rgb('#ff8000')
    print(f"HEX #ff8000 -> RGB({r}, {g}, {b}), alpha={a}")
    
    # 名称 <-> RGB
    r, g, b = name_to_rgb('coral')
    print(f"名称 'coral' -> RGB({r}, {g}, {b})")
    
    # 解析各种格式
    color1 = parse_color('#ff0000')
    color2 = parse_color('rgb(255, 0, 0)')
    color3 = parse_color('red')
    color4 = parse_color('hsl(0, 100%, 50%)')
    print(f"解析 #ff0000: {color1}")
    print(f"解析 rgb(255, 0, 0): {color2}")
    print(f"解析 'red': {color3}")
    print(f"解析 hsl(0, 100%, 50%): {color4}")


def example_color_operations():
    """示例4: 颜色操作"""
    print("\n" + "=" * 50)
    print("示例4: 颜色操作")
    print("=" * 50)
    
    color = Color.from_hex('#ff8000')
    
    # 增加亮度
    lighter = color.lighten(20)
    print(f"原色: {color.hex}")
    print(f"增加亮度 20%: {lighter.hex}")
    
    # 降低亮度
    darker = color.darken(20)
    print(f"降低亮度 20%: {darker.hex}")
    
    # 增加饱和度
    saturated = color.saturate(30)
    print(f"增加饱和度 30%: {saturated.hex}")
    
    # 降低饱和度
    desaturated = color.desaturate(30)
    print(f"降低饱和度 30%: {desaturated.hex}")
    
    # 灰度化
    gray = color.grayscale()
    print(f"灰度化: {gray.hex}")
    
    # 反色
    inverted = color.invert()
    print(f"反色: {inverted.hex}")
    
    # 色相旋转
    rotated = color.rotate_hue(60)
    print(f"色相旋转 60°: {rotated.hex}")
    
    # 互补色
    complement = color.complement()
    print(f"互补色: {complement.hex}")
    
    # 颜色混合
    blue = Color.from_hex('#0000ff')
    mixed = color.mix(blue, 0.5)
    print(f"与蓝色 50% 混合: {mixed.hex}")


def example_contrast_calculation():
    """示例5: 对比度计算"""
    print("\n" + "=" * 50)
    print("示例5: 对比度计算")
    print("=" * 50)
    
    # 黑白对比
    black = Color(0, 0, 0)
    white = Color(255, 255, 255)
    ratio = black.contrast_ratio(white)
    print(f"黑白对比度: {ratio:.1f}:1")
    
    # WCAG 合规性检查
    compliance = white.wcag_compliance(black)
    print(f"WCAG AA 正常文本: {'✓' if compliance['aa_normal'] else '✗'}")
    print(f"WCAG AA 大文本: {'✓' if compliance['aa_large'] else '✗'}")
    print(f"WCAG AAA 正常文本: {'✓' if compliance['aaa_normal'] else '✗'}")
    print(f"WCAG AAA 大文本: {'✓' if compliance['aaa_large'] else '✗'}")
    
    # 推荐文本颜色
    bg_color = Color(30, 30, 30)
    text_color = bg_color.text_color()
    print(f"\n深色背景 {bg_color.hex} 推荐文本颜色: {text_color.hex}")
    
    bg_color = Color(240, 240, 240)
    text_color = bg_color.text_color()
    print(f"浅色背景 {bg_color.hex} 推荐文本颜色: {text_color.hex}")


def example_palette_generation():
    """示例6: 调色板生成"""
    print("\n" + "=" * 50)
    print("示例6: 调色板生成")
    print("=" * 50)
    
    base_color = Color.from_hex('#ff6b6b')  # 红色
    
    # 互补色
    comp = generate_complementary(base_color)
    print(f"互补色: {[c.hex for c in comp]}")
    
    # 类似色
    anal = generate_analogous(base_color)
    print(f"类似色: {[c.hex for c in anal]}")
    
    # 三元组色
    tri = generate_triadic(base_color)
    print(f"三元组色: {[c.hex for c in tri]}")
    
    # 分裂互补色
    split = generate_split_complementary(base_color)
    print(f"分裂互补色: {[c.hex for c in split]}")
    
    # 四元组色
    tetra = generate_tetradic(base_color)
    print(f"四元组色: {[c.hex for c in tetra]}")
    
    # 单色调色板
    mono = generate_monochromatic(base_color, count=5)
    print(f"单色调色板: {[c.hex for c in mono]}")
    
    # 渐变
    start = Color.from_hex('#ff6b6b')
    end = Color.from_hex('#4ecdc4')
    gradient = generate_gradient(start, end, steps=5)
    print(f"渐变 (红到青): {[c.hex for c in gradient]}")
    
    # 深浅变化
    shades = generate_shades(base_color, count=5)
    print(f"深浅变化: {[c.hex for c in shades]}")
    
    # 浅色调变化
    tints = generate_tints(base_color, count=5)
    print(f"浅色调变化: {[c.hex for c in tints]}")


def example_random_colors():
    """示例7: 随机颜色生成"""
    print("\n" + "=" * 50)
    print("示例7: 随机颜色生成")
    print("=" * 50)
    
    # 随机颜色
    random_colors = [random_color() for _ in range(5)]
    print(f"随机颜色: {[c.hex for c in random_colors]}")
    
    # 柔和色
    pastels = [random_pastel() for _ in range(5)]
    print(f"柔和色: {[c.hex for c in pastels]}")
    
    # 鲜艳色
    vibrant = [random_vibrant() for _ in range(5)]
    print(f"鲜艳色: {[c.hex for c in vibrant]}")
    
    # 深色
    dark = [random_dark() for _ in range(5)]
    print(f"深色: {[c.hex for c in dark]}")
    
    # 浅色
    light = [random_light() for _ in range(5)]
    print(f"浅色: {[c.hex for c in light]}")
    
    # 指定色相的随机色
    blue_hue = [Color.random(hue=210) for _ in range(5)]
    print(f"蓝色系随机色: {[c.hex for c in blue_hue]}")


def example_blend_colors():
    """示例8: 多色混合"""
    print("\n" + "=" * 50)
    print("示例8: 多色混合")
    print("=" * 50)
    
    # 三色等权重混合
    red = Color(255, 0, 0)
    green = Color(0, 255, 0)
    blue = Color(0, 0, 255)
    
    blended = blend_colors([red, green, blue])
    print(f"红/绿/蓝 等权重混合: {blended.hex}")
    
    # 自定义权重混合
    colors = [red, green, blue]
    weights = [0.5, 0.3, 0.2]
    blended = blend_colors(colors, weights=weights)
    print(f"红(50%)/绿(30%)/蓝(20%) 混合: {blended.hex}")


def example_ui_color_suggestions():
    """示例9: UI 设计颜色建议"""
    print("\n" + "=" * 50)
    print("示例9: UI 设计颜色建议")
    print("=" * 50)
    
    primary_color = Color.from_hex('#3498db')  # 蓝色
    
    suggestions = get_color_suggestions(primary_color, 'ui')
    
    print(f"主色: {suggestions['original'].hex}")
    print(f"悬停色: {suggestions['hover'].hex}")
    print(f"激活色: {suggestions['active'].hex}")
    print(f"禁用色: {suggestions['disabled'].hex}")
    print(f"边框色: {suggestions['border'].hex}")
    print(f"文本色: {suggestions['text_on_bg'].hex}")
    print(f"浅色调: {suggestions['lighter'].hex}")
    print(f"深色调: {suggestions['darker'].hex}")


def example_design_palette():
    """示例10: 创建完整设计调色板"""
    print("\n" + "=" * 50)
    print("示例10: 创建完整设计调色板")
    print("=" * 50)
    
    # 主品牌色
    brand_color = Color.from_hex('#6c5ce7')
    
    # 生成各种调色板
    print("品牌调色板:")
    print("-" * 30)
    
    # 主色系列
    print(f"主色: {brand_color.hex}")
    print(f"浅主色: {brand_color.lighten(15).hex}")
    print(f"深主色: {brand_color.darken(15).hex}")
    
    # 强调色 (互补色)
    accent = brand_color.complement()
    print(f"强调色: {accent.hex}")
    
    # 成功/警告/错误色
    success = Color.from_hex('#00b894')
    warning = Color.from_hex('#fdcb6e')
    error = Color.from_hex('#e17055')
    print(f"成功色: {success.hex}")
    print(f"警告色: {warning.hex}")
    print(f"错误色: {error.hex}")
    
    # 灰度色阶
    gray_scale = [
        Color(255, 255, 255),  # 白
        Color(250, 250, 250),
        Color(245, 245, 245),
        Color(230, 230, 230),
        Color(200, 200, 200),
        Color(150, 150, 150),
        Color(100, 100, 100),
        Color(50, 50, 50),
        Color(0, 0, 0),        # 黑
    ]
    print(f"灰度色阶: {[c.hex for c in gray_scale]}")
    
    # 检查文本对比度
    print("\n文本对比度检查:")
    text_on_brand = brand_color.text_color()
    ratio = brand_color.contrast_ratio(text_on_brand)
    print(f"品牌背景上的文本对比度: {ratio:.1f}:1")


def example_html_color_output():
    """示例11: 生成 HTML 颜色展示"""
    print("\n" + "=" * 50)
    print("示例11: 生成 HTML 颜色展示代码")
    print("=" * 50)
    
    # 生成一个调色板并输出 HTML
    base_color = Color.from_name('coral')
    palette = generate_triadic(base_color)
    
    html = """
<div style="display: flex; gap: 10px;">
"""
    for color in palette:
        html += f"""  <div style="width: 100px; height: 100px; background-color: {color.hex}; border-radius: 8px;">
    <div style="color: {color.text_color().hex}; padding: 10px; font-size: 12px;">
      {color.hex}
    </div>
  </div>
"""
    html += "</div>"
    
    print(html)


def main():
    """运行所有示例"""
    example_basic_color_creation()
    example_color_properties()
    example_color_conversion()
    example_color_operations()
    example_contrast_calculation()
    example_palette_generation()
    example_random_colors()
    example_blend_colors()
    example_ui_color_suggestions()
    example_design_palette()
    example_html_color_output()
    
    print("\n" + "=" * 50)
    print("所有示例完成!")
    print("=" * 50)


if __name__ == '__main__':
    main()