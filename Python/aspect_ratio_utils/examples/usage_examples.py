# -*- coding: utf-8 -*-
"""
Aspect Ratio Utilities 使用示例

展示宽高比计算工具的各种使用场景。

Author: AllToolkit
Version: 1.0.0
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from aspect_ratio_utils.mod import (
    AspectRatioPreset,
    Resolution,
    AspectRatio,
    simplify_ratio,
    calculate_aspect_ratio,
    is_same_ratio,
    scale_to_width,
    scale_to_height,
    scale_to_fit,
    scale_to_fill,
    calculate_crop,
    calculate_letterbox,
    find_common_resolutions,
    match_preset,
    get_resolution_name,
    calculate_print_size,
    get_optimal_resolution,
    COMMON_RESOLUTIONS,
)


def example_basic_ratio():
    """基础宽高比计算示例"""
    print("=" * 50)
    print("基础宽高比计算")
    print("=" * 50)
    
    # 简化宽高比
    print("\n1. 简化宽高比:")
    ratios = [
        (1920, 1080),
        (3840, 2160),
        (2560, 1440),
        (1080, 1920),
        (1000, 1000),
    ]
    
    for w, h in ratios:
        simplified = simplify_ratio(w, h)
        print(f"   {w}x{h} → {simplified[0]}:{simplified[1]}")
    
    # 使用 Resolution 类
    print("\n2. Resolution 类:")
    res = Resolution(1920, 1080)
    print(f"   分辨率: {res}")
    print(f"   像素数: {res.pixels}")
    print(f"   百万像素: {res.megapixels:.2f} MP")
    print(f"   宽高比: {res.aspect_ratio[0]}:{res.aspect_ratio[1]}")
    print(f"   方向: {res.orientation}")
    print(f"   名称: {get_resolution_name(res.width, res.height)}")
    print(f"   是否 HD: {res.is_hd}")
    print(f"   是否 Full HD: {res.is_full_hd}")
    print(f"   是否 4K: {res.is_4k}")


def example_aspect_ratio_class():
    """AspectRatio 类示例"""
    print("\n" + "=" * 50)
    print("AspectRatio 类使用")
    print("=" * 50)
    
    # 从不同方式创建
    print("\n1. 创建方式:")
    ratio1 = AspectRatio(16, 9)
    print(f"   直接创建: {ratio1}")
    
    ratio2 = AspectRatio.from_resolution(1920, 1080)
    print(f"   从分辨率创建: {ratio2}")
    
    ratio3 = AspectRatio.from_string("21:9")
    print(f"   从字符串创建: {ratio3}")
    
    ratio4 = AspectRatio.from_float(1.7778)
    print(f"   从浮点数创建: {ratio4} (≈16:9)")
    
    ratio5 = AspectRatio.from_preset(AspectRatioPreset.CINEMA_SCOPE)
    print(f"   从预设创建: {ratio5}")
    
    # 计算分辨率
    print("\n2. 根据比例计算分辨率:")
    ratio = AspectRatio(16, 9)
    res1 = ratio.get_resolution_for_width(1920)
    print(f"   16:9, 宽度1920 → {res1}")
    
    res2 = ratio.get_resolution_for_height(1080)
    print(f"   16:9, 高度1080 → {res2}")
    
    # 反向比例
    print("\n3. 反向比例:")
    wide = AspectRatio(16, 9)
    tall = wide.inverse
    print(f"   {wide} 的反向是 {tall}")


def example_scaling():
    """缩放示例"""
    print("\n" + "=" * 50)
    print("分辨率缩放")
    print("=" * 50)
    
    original = Resolution(1920, 1080)
    print(f"原始分辨率: {original}")
    
    # 缩放到指定宽度
    print("\n1. 缩放到指定宽度:")
    scaled1 = original.scale_to_width(3840)
    print(f"   缩放到宽度3840: {scaled1}")
    
    # 缩放到指定高度
    print("\n2. 缩放到指定高度:")
    scaled2 = original.scale_to_height(540)
    print(f"   缩放到高度540: {scaled2}")
    
    # 适应指定区域
    print("\n3. 缩放以适应区域:")
    scaled3 = original.scale_to_fit(1000, 1000)
    print(f"   适应1000x1000: {scaled3} (保持比例，不超出)")
    
    scaled4 = original.scale_to_fit(1920, 1920)
    print(f"   适应1920x1920: {scaled4}")
    
    # 填充指定区域
    print("\n4. 缩放以填充区域:")
    scaled5 = original.scale_to_fill(1000, 1000)
    print(f"   填充1000x1000: {scaled5} (保持比例，完全覆盖)")
    
    # 使用函数
    print("\n5. 使用函数缩放:")
    new_w, new_h = scale_to_width(1920, 1080, 960)
    print(f"   scale_to_width(1920, 1080, 960) → {new_w}x{new_h}")
    
    new_w, new_h = scale_to_fit(1920, 1080, 960, 540)
    print(f"   scale_to_fit(1920, 1080, 960, 540) → {new_w}x{new_h}")


def example_cropping():
    """裁剪计算示例"""
    print("\n" + "=" * 50)
    print("裁剪计算")
    print("=" * 50)
    
    # 1920x1080 裁剪到不同比例
    print("\n1. 1920x1080 裁剪到各种比例:")
    targets = ["1:1", "4:3", "21:9", "9:16"]
    
    for target in targets:
        crop = calculate_crop(1920, 1080, target)
        print(f"   到 {target}:")
        print(f"      区域: x={crop['x']}, y={crop['y']}, "
              f"{crop['width']}x{crop['height']}")
    
    # 正方形裁剪
    print("\n2. 1080x1920 (竖屏) 裁剪到 16:9:")
    crop = calculate_crop(1080, 1920, "16:9")
    print(f"   区域: x={crop['x']}, y={crop['y']}, "
          f"{crop['width']}x{crop['height']}")
    print(f"   被裁掉的高度: {1920 - crop['height']}px")
    
    # 使用 AspectRatio 对象
    print("\n3. 使用 AspectRatio 对象裁剪:")
    ratio = AspectRatio(21, 9)
    crop = calculate_crop(3840, 2160, ratio)
    print(f"   3840x2160 裁剪到 {ratio}:")
    print(f"   区域: x={crop['x']}, y={crop['y']}, "
          f"{crop['width']}x{crop['height']}")


def example_letterbox():
    """黑边计算示例"""
    print("\n" + "=" * 50)
    print("黑边 (Letterbox/Pillarbox) 计算")
    print("=" * 50)
    
    # 16:9 内容放入 4:3 容器
    print("\n1. 1920x1080 (16:9) 放入 1440x1080 (4:3) 容器:")
    result = calculate_letterbox(1920, 1080, 1440, 1080)
    print(f"   视频位置: ({result['video_x']}, {result['video_y']})")
    print(f"   视频尺寸: {result['video_width']}x{result['video_height']}")
    print(f"   左黑边: {result['left_bar']}px")
    print(f"   右黑边: {result['right_bar']}px")
    print(f"   类型: Pillarbox")
    
    # 4:3 内容放入 16:9 容器
    print("\n2. 1440x1080 (4:3) 放入 1920x1080 (16:9) 容器:")
    result = calculate_letterbox(1440, 1080, 1920, 1080)
    print(f"   视频位置: ({result['video_x']}, {result['video_y']})")
    print(f"   视频尺寸: {result['video_width']}x{result['video_height']}")
    print(f"   上黑边: {result['top_bar']}px")
    print(f"   下黑边: {result['bottom_bar']}px")
    print(f"   类型: Letterbox")
    
    # Instagram Story (9:16) 内容放入 TikTok (16:9) 容器
    print("\n3. 1080x1920 (Story) 放入 1920x1080 (横屏) 容器:")
    result = calculate_letterbox(1080, 1920, 1920, 1080)
    print(f"   视频尺寸: {result['video_width']}x{result['video_height']}")
    print(f"   左黑边: {result['left_bar']}px")
    print(f"   右黑边: {result['right_bar']}px")
    print(f"   上下黑边: {result['top_bar']}px / {result['bottom_bar']}px")


def example_presets():
    """预设宽高比示例"""
    print("\n" + "=" * 50)
    print("预设宽高比")
    print("=" * 50)
    
    print("\n常用预设宽高比:")
    for preset in [
        AspectRatioPreset.SQUARE,
        AspectRatioPreset.CLASSIC_FILM,
        AspectRatioPreset.WIDESCREEN,
        AspectRatioPreset.ULTRAWIDE,
        AspectRatioPreset.CINEMA_SCOPE,
        AspectRatioPreset.INSTAGRAM_STORY,
        AspectRatioPreset.IPHONE,
        AspectRatioPreset.GOLDEN_RATIO,
    ]:
        ratio = AspectRatio.from_string(preset.value)
        res = ratio.get_resolution_for_width(1920)
        print(f"   {preset.name}: {preset.value}")
        print(f"      1920px宽对应的分辨率: {res.width}x{res.height}")
    
    # 匹配预设
    print("\n2. 自动匹配预设:")
    resolutions = [(1920, 1080), (2560, 1080), (1080, 1080), (1024, 768)]
    for w, h in resolutions:
        preset = match_preset(w, h)
        name = preset.name if preset else "未知"
        print(f"   {w}x{h} → {name}")


def example_social_media():
    """社交媒体分辨率示例"""
    print("\n" + "=" * 50)
    print("社交媒体推荐分辨率")
    print("=" * 50)
    
    print("\n常用社交媒体分辨率:")
    for name, res in [
        ('instagram_square', COMMON_RESOLUTIONS['instagram_square']),
        ('instagram_portrait', COMMON_RESOLUTIONS['instagram_portrait']),
        ('instagram_story', COMMON_RESOLUTIONS['instagram_story']),
        ('youtube_thumbnail', COMMON_RESOLUTIONS['youtube_thumbnail']),
        ('twitter_card', COMMON_RESOLUTIONS['twitter_card']),
        ('facebook_cover', COMMON_RESOLUTIONS['facebook_cover']),
        ('linkedin_banner', COMMON_RESOLUTIONS['linkedin_banner']),
    ]:
        ratio = simplify_ratio(res.width, res.height)
        print(f"   {name}: {res} ({ratio[0]}:{ratio[1]})")
    
    # 从竖版照片适配到 Instagram Portrait
    print("\n2. 照片适配示例:")
    photo = Resolution(3000, 4000)  # 3:4 竖版照片
    target = COMMON_RESOLUTIONS['instagram_portrait']  # 4:5
    
    # 需要裁剪
    crop = calculate_crop(photo.width, photo.height, (4, 5))
    print(f"   原始照片: {photo}")
    print(f"   Instagram Portrait: {target}")
    print(f"   裁剪区域: {crop['width']}x{crop['height']}")
    print(f"   被裁掉: {photo.height - crop['height']}px")


def example_print():
    """打印尺寸计算示例"""
    print("\n" + "=" * 50)
    print("打印尺寸计算")
    print("=" * 50)
    
    print("\n常见打印 DPI:")
    dpis = [72, 150, 300, 600]
    for dpi in dpis:
        res = Resolution(3000, 2400)
        size = calculate_print_size(res.width, res.height, dpi)
        print(f"   {dpi} DPI:")
        print(f"      {res} 可打印 {size['inches'][0]}\" x {size['inches'][1]}\"")
        print(f"      即 {size['centimeters'][0]}cm x {size['centimeters'][1]}cm")
    
    # 计算所需像素
    print("\n2. 计算打印所需像素:")
    print("   想打印 8x10 英寸照片:")
    for dpi in [150, 300, 600]:
        width = int(8 * dpi)
        height = int(10 * dpi)
        print(f"      {dpi} DPI 需要 {width}x{height} = "
              f"{(width*height)/1000000:.2f} MP")


def example_optimal_resolution():
    """最优分辨率示例"""
    print("\n" + "=" * 50)
    print("最优分辨率计算")
    print("=" * 50)
    
    print("\n为不同宽高比计算最优分辨率:")
    ratios = ["16:9", "4:3", "21:9", "1:1", "9:16"]
    
    for ratio_str in ratios:
        res = get_optimal_resolution(ratio_str)
        ratio = simplify_ratio(res.width, res.height)
        print(f"   {ratio_str}:")
        print(f"      推荐: {res} ({ratio[0]}:{ratio[1]})")
        print(f"      像素: {res.megapixels:.2f} MP")


def example_resolution_parsing():
    """分辨率解析示例"""
    print("\n" + "=" * 50)
    print("分辨率字符串解析")
    print("=" * 50)
    
    print("\n从字符串创建 Resolution:")
    strings = ["1920x1080", "1920*1080", "1920:1080", "4K", "3840X2160"]
    
    # 自定义解析
    for s in strings:
        try:
            if s == "4K":
                res = COMMON_RESOLUTIONS['4k']
                print(f"   '{s}' → {res} (预定义)")
            else:
                res = Resolution.from_string(s)
                print(f"   '{s}' → {res}")
        except ValueError as e:
            print(f"   '{s}' → 解析失败")


def example_full_workflow():
    """完整工作流示例"""
    print("\n" + "=" * 50)
    print("完整工作流: 视频适配多个平台")
    print("=" * 50)
    
    # 原始视频
    source = Resolution(1920, 1080)
    print(f"\n原始视频: {source}")
    print(f"宽高比: {source.aspect_ratio[0]}:{source.aspect_ratio[1]}")
    
    # 适配到不同平台
    platforms = [
        ("YouTube (16:9)", "16:9", None),
        ("Instagram Feed (1:1)", "1:1", None),
        ("Instagram Story (9:16)", "9:16", None),
        ("Twitter Card (2:1)", "2:1", None),
    ]
    
    print("\n适配到各平台:")
    for platform, ratio, _ in platforms:
        crop = calculate_crop(source.width, source.height, ratio)
        target = AspectRatio.from_string(ratio).get_resolution_for_width(source.width)
        
        print(f"\n{platform}:")
        print(f"   目标比例: {ratio}")
        print(f"   需要裁剪区域: {crop['width']}x{crop['height']}")
        print(f"   裁剪偏移: x={crop['x']}, y={crop['y']}")
        
        # 计算缩放后的最终尺寸
        if crop['width'] > source.width:
            # 缩放后裁剪
            final = target
        else:
            # 直接裁剪
            final = Resolution(crop['width'], crop['height'])
        
        # 缩放到平台推荐尺寸
        if platform == "YouTube (16:9)":
            final = Resolution(1920, 1080)  # 不需要裁剪
        elif platform == "Instagram Feed (1:1)":
            final = Resolution(1080, 1080)
        elif platform == "Instagram Story (9:16)":
            final = Resolution(1080, 1920)
        elif platform == "Twitter Card (2:1)":
            final = Resolution(1200, 600)
        
        print(f"   输出尺寸: {final}")


def main():
    """运行所有示例"""
    example_basic_ratio()
    example_aspect_ratio_class()
    example_scaling()
    example_cropping()
    example_letterbox()
    example_presets()
    example_social_media()
    example_print()
    example_optimal_resolution()
    example_resolution_parsing()
    example_full_workflow()
    
    print("\n" + "=" * 50)
    print("所有示例完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()