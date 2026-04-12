"""
AllToolkit - Image Utilities 基本使用示例

本文件展示 image_utils 模块的各种使用场景。

运行前请确保：
    pip install Pillow
"""

import sys
import os
import tempfile

# 添加父目录到路径以导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    get_image_info,
    convert_format,
    resize_image,
    scale_image,
    crop_image,
    center_crop,
    rotate_image,
    flip_image,
    compress_image,
    generate_thumbnail,
    add_watermark,
    add_image_watermark,
    merge_images,
    create_grid,
    batch_resize,
    batch_convert,
    is_pillow_available,
    get_supported_formats,
)


def create_test_image(color='red', size=(200, 200), filename=None):
    """创建测试图像（需要 Pillow）。"""
    if not is_pillow_available():
        print("⚠ 需要 Pillow 库创建测试图像")
        return None
    
    from PIL import Image
    
    img = Image.new('RGB', size, color=color)
    
    if filename:
        img.save(filename)
        return filename
    
    # 保存到临时文件
    fd, path = tempfile.mkstemp(suffix='.png')
    os.close(fd)
    img.save(path)
    return path


def example_1_basic_info():
    """示例 1: 获取图像信息"""
    print("=" * 60)
    print("示例 1: 获取图像信息")
    print("=" * 60)
    
    # 创建测试图像
    test_img = create_test_image('blue', (800, 600))
    if not test_img:
        return
    
    # 获取信息
    info = get_image_info(test_img)
    
    print(f"\n图像信息:")
    print(f"  尺寸：{info.width} x {info.height} 像素")
    print(f"  格式：{info.format}")
    print(f"  颜色模式：{info.mode}")
    print(f"  文件大小：{info.file_size} 字节")
    print(f"  透明通道：{'有' if info.has_alpha else '无'}")
    print(f"  位深度：{info.bit_depth}")
    
    # 转换为字典
    info_dict = info.to_dict()
    print(f"\n字典格式：{info_dict}")
    
    # 清理
    os.remove(test_img)
    print()


def example_2_format_conversion():
    """示例 2: 格式转换"""
    print("=" * 60)
    print("示例 2: 格式转换")
    print("=" * 60)
    
    if not is_pillow_available():
        print("⚠ 需要 Pillow 库")
        return
    
    # 创建 PNG 测试图像
    png_file = create_test_image('green', (300, 300))
    
    # 转换为 JPEG
    jpg_file = png_file.replace('.png', '.jpg')
    convert_format(png_file, 'JPEG', jpg_file, quality=90)
    print(f"✓ PNG → JPEG: {jpg_file}")
    
    # 转换为 WebP
    webp_file = png_file.replace('.png', '.webp')
    convert_format(png_file, 'WebP', webp_file, quality=85)
    print(f"✓ PNG → WebP: {webp_file}")
    
    # 比较文件大小
    png_size = os.path.getsize(png_file)
    jpg_size = os.path.getsize(jpg_file)
    webp_size = os.path.getsize(webp_file)
    
    print(f"\n文件大小比较:")
    print(f"  PNG:  {png_size} 字节")
    print(f"  JPEG: {jpg_size} 字节 ({jpg_size/png_size*100:.1f}%)")
    print(f"  WebP: {webp_size} 字节 ({webp_size/png_size*100:.1f}%)")
    
    # 清理
    for f in [png_file, jpg_file, webp_file]:
        if os.path.exists(f):
            os.remove(f)
    print()


def example_3_resize():
    """示例 3: 调整大小"""
    print("=" * 60)
    print("示例 3: 调整大小")
    print("=" * 60)
    
    if not is_pillow_available():
        print("⚠ 需要 Pillow 库")
        return
    
    # 创建大图像
    large_img = create_test_image('purple', (1000, 800))
    
    # 精确尺寸缩放
    resized = large_img.replace('.png', '_resized.png')
    resize_image(large_img, 400, 300, resized)
    info = get_image_info(resized)
    print(f"✓ 精确缩放：1000x800 → {info.width}x{info.height}")
    
    # 保持宽高比
    aspect = large_img.replace('.png', '_aspect.png')
    resize_image(large_img, 400, 400, aspect, maintain_aspect=True)
    info = get_image_info(aspect)
    print(f"✓ 保持宽高比：1000x800 → {info.width}x{info.height}")
    
    # 按比例缩放
    half = large_img.replace('.png', '_half.png')
    scale_image(large_img, 0.5, half)
    info = get_image_info(half)
    print(f"✓ 50% 缩放：1000x800 → {info.width}x{info.height}")
    
    # 清理
    for f in [large_img, resized, aspect, half]:
        if os.path.exists(f):
            os.remove(f)
    print()


def example_4_crop():
    """示例 4: 裁剪"""
    print("=" * 60)
    print("示例 4: 裁剪")
    print("=" * 60)
    
    if not is_pillow_available():
        print("⚠ 需要 Pillow 库")
        return
    
    # 创建测试图像
    img = create_test_image('orange', (500, 400))
    
    # 自定义区域裁剪
    cropped = img.replace('.png', '_cropped.png')
    crop_image(img, (50, 50, 250, 200), cropped)
    info = get_image_info(cropped)
    print(f"✓ 区域裁剪 (50,50,250,200): {info.width}x{info.height}")
    
    # 中心裁剪为正方形
    square = img.replace('.png', '_square.png')
    center_crop(img, 300, 300, square)
    info = get_image_info(square)
    print(f"✓ 中心裁剪：500x400 → {info.width}x{info.height}")
    
    # 清理
    for f in [img, cropped, square]:
        if os.path.exists(f):
            os.remove(f)
    print()


def example_5_rotate_flip():
    """示例 5: 旋转和翻转"""
    print("=" * 60)
    print("示例 5: 旋转和翻转")
    print("=" * 60)
    
    if not is_pillow_available():
        print("⚠ 需要 Pillow 库")
        return
    
    # 创建非正方形图像以便观察旋转效果
    img = create_test_image('cyan', (400, 200))
    
    # 旋转 90 度
    rotated_90 = img.replace('.png', '_rot90.png')
    rotate_image(img, 90, rotated_90)
    info = get_image_info(rotated_90)
    print(f"✓ 旋转 90°: 400x200 → {info.width}x{info.height}")
    
    # 旋转 45 度并扩展
    rotated_45 = img.replace('.png', '_rot45.png')
    rotate_image(img, 45, rotated_45, expand=True)
    info = get_image_info(rotated_45)
    print(f"✓ 旋转 45° (扩展): 400x200 → {info.width}x{info.height}")
    
    # 水平翻转
    flipped_h = img.replace('.png', '_flip_h.png')
    flip_image(img, 'horizontal', flipped_h)
    print(f"✓ 水平翻转：完成")
    
    # 垂直翻转
    flipped_v = img.replace('.png', '_flip_v.png')
    flip_image(img, 'vertical', flipped_v)
    print(f"✓ 垂直翻转：完成")
    
    # 清理
    for f in [img, rotated_90, rotated_45, flipped_h, flipped_v]:
        if os.path.exists(f):
            os.remove(f)
    print()


def example_6_compress():
    """示例 6: 压缩"""
    print("=" * 60)
    print("示例 6: 压缩")
    print("=" * 60)
    
    if not is_pillow_available():
        print("⚠ 需要 Pillow 库")
        return
    
    # 创建高质量 JPEG
    original = create_test_image('magenta', (1000, 800))
    from PIL import Image
    img = Image.open(original)
    high_quality = original.replace('.png', '_hq.jpg')
    img.save(high_quality, 'JPEG', quality=95)
    
    original_size = os.path.getsize(high_quality)
    
    # 降低质量压缩
    compressed_q = high_quality.replace('.jpg', '_q75.jpg')
    compress_image(high_quality, compressed_q, quality=75)
    size_q = os.path.getsize(compressed_q)
    print(f"✓ 质量压缩 (95→75): {original_size} → {size_q} 字节 ({size_q/original_size*100:.1f}%)")
    
    # 限制最大大小
    compressed_s = high_quality.replace('.jpg', '_max50k.jpg')
    compress_image(high_quality, compressed_s, max_size=50000)
    size_s = os.path.getsize(compressed_s)
    print(f"✓ 大小限制 (<50KB): {original_size} → {size_s} 字节")
    
    # 限制尺寸
    compressed_d = high_quality.replace('.jpg', '_small.jpg')
    compress_image(high_quality, compressed_d, max_dimensions=(400, 300))
    info = get_image_info(compressed_d)
    size_d = os.path.getsize(compressed_d)
    print(f"✓ 尺寸限制 (400x300): {info.width}x{info.height}, {size_d} 字节")
    
    # 清理
    for f in [original, high_quality, compressed_q, compressed_s, compressed_d]:
        if os.path.exists(f):
            os.remove(f)
    print()


def example_7_thumbnail():
    """示例 7: 缩略图"""
    print("=" * 60)
    print("示例 7: 缩略图生成")
    print("=" * 60)
    
    if not is_pillow_available():
        print("⚠ 需要 Pillow 库")
        return
    
    # 创建大图
    img = create_test_image('teal', (1920, 1080))
    
    # 生成缩略图
    thumb = img.replace('.png', '_thumb.png')
    generate_thumbnail(img, (200, 200), thumb)
    info = get_image_info(thumb)
    print(f"✓ 缩略图：1920x1080 → {info.width}x{info.height}")
    
    # 保持宽高比
    thumb_aspect = img.replace('.png', '_thumb_aspect.png')
    generate_thumbnail(img, (150, 150), thumb_aspect, maintain_aspect=True)
    info = get_image_info(thumb_aspect)
    print(f"✓ 缩略图 (保持比例): 1920x1080 → {info.width}x{info.height}")
    
    # 清理
    for f in [img, thumb, thumb_aspect]:
        if os.path.exists(f):
            os.remove(f)
    print()


def example_8_watermark():
    """示例 8: 水印"""
    print("=" * 60)
    print("示例 8: 添加水印")
    print("=" * 60)
    
    if not is_pillow_available():
        print("⚠ 需要 Pillow 库")
        return
    
    # 创建测试图像
    img = create_test_image('white', (600, 400))
    
    # 文字水印 - 不同位置
    positions = ['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center']
    
    for pos in positions:
        output = img.replace('.png', f'_wm_{pos}.png')
        add_watermark(img, '© 2024 Sample', output, position=pos,
                     font_size=20, color=(0, 0, 0, 180))
        print(f"✓ 文字水印 ({pos}): 完成")
    
    # 创建图片水印
    logo = create_test_image('red', (100, 100))
    watermarked = img.replace('.png', '_logo_wm.png')
    add_image_watermark(img, logo, watermarked, position='bottom-right',
                       opacity=0.7, scale=0.15)
    print(f"✓ 图片水印：完成")
    
    # 清理
    for f in [img, logo] + [f for f in os.listdir(os.path.dirname(img)) 
                            if f.startswith(os.path.basename(img).replace('.png', ''))]:
        path = os.path.join(os.path.dirname(img), f)
        if os.path.exists(path):
            os.remove(path)
    print()


def example_9_merge():
    """示例 9: 图像合并"""
    print("=" * 60)
    print("示例 9: 图像合并/拼接")
    print("=" * 60)
    
    if not is_pillow_available():
        print("⚠ 需要 Pillow 库")
        return
    
    # 创建测试图像
    colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta']
    images = []
    
    for i, color in enumerate(colors):
        img = create_test_image(color, (150, 100))
        images.append(img)
    
    # 水平拼接
    merged_h = images[0].replace('.png', '_merged_h.png')
    merge_images(images[:3], 'horizontal', merged_h)
    info = get_image_info(merged_h)
    print(f"✓ 水平拼接 (3 张): {info.width}x{info.height}")
    
    # 垂直拼接
    merged_v = images[0].replace('.png', '_merged_v.png')
    merge_images(images[3:], 'vertical', merged_v)
    info = get_image_info(merged_v)
    print(f"✓ 垂直拼接 (3 张): {info.width}x{info.height}")
    
    # 创建网格
    grid = images[0].replace('.png', '_grid.png')
    create_grid(images, cols=3, output_path=grid, gap=5)
    info = get_image_info(grid)
    print(f"✓ 网格布局 (2x3): {info.width}x{info.height}")
    
    # 清理
    for img in images:
        if os.path.exists(img):
            os.remove(img)
    for f in [merged_h, merged_v, grid]:
        if os.path.exists(f):
            os.remove(f)
    print()


def example_10_batch():
    """示例 10: 批量处理"""
    print("=" * 60)
    print("示例 10: 批量处理")
    print("=" * 60)
    
    if not is_pillow_available():
        print("⚠ 需要 Pillow 库")
        return
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    input_dir = os.path.join(temp_dir, 'input')
    output_dir = os.path.join(temp_dir, 'output')
    os.makedirs(input_dir)
    
    # 创建测试图像
    colors = ['red', 'green', 'blue', 'yellow', 'purple']
    for i, color in enumerate(colors):
        img = create_test_image(color, (800, 600), 
                               os.path.join(input_dir, f'image{i}.jpg'))
    
    print(f"✓ 创建 {len(colors)} 张测试图像")
    
    # 批量缩放
    result = batch_resize(input_dir, output_dir, 400, 300)
    print(f"\n✓ 批量缩放结果:")
    print(f"  成功：{result['processed']} 张")
    print(f"  失败：{result['failed']} 张")
    
    # 验证输出
    output_files = os.listdir(output_dir)
    print(f"  输出文件：{len(output_files)} 个")
    
    # 检查第一张
    if output_files:
        first = os.path.join(output_dir, output_files[0])
        info = get_image_info(first)
        print(f"  示例尺寸：{info.width}x{info.height}")
    
    # 批量转换
    convert_dir = os.path.join(temp_dir, 'converted')
    result = batch_convert(input_dir, convert_dir, 'png')
    print(f"\n✓ 批量转换结果 (JPG→PNG):")
    print(f"  成功：{result['processed']} 张")
    print(f"  失败：{result['failed']} 张")
    
    # 清理
    import shutil
    shutil.rmtree(temp_dir)
    print()


def example_11_module_info():
    """示例 11: 模块信息"""
    print("=" * 60)
    print("示例 11: 模块信息")
    print("=" * 60)
    
    # 版本
    from mod import get_version
    print(f"模块版本：{get_version()}")
    
    # Pillow 可用性
    print(f"Pillow 可用：{is_pillow_available()}")
    
    # 支持的格式
    formats = get_supported_formats()
    print(f"支持的格式 ({len(formats)} 种):")
    print(f"  {', '.join(formats)}")
    print()


def main():
    """运行所有示例。"""
    print("=" * 60)
    print("AllToolkit - Image Utilities 使用示例")
    print("=" * 60)
    print(f"Pillow 可用：{is_pillow_available()}")
    print(f"支持格式：{', '.join(get_supported_formats())}")
    print("=" * 60)
    print()
    
    # 运行示例
    example_1_basic_info()
    example_2_format_conversion()
    example_3_resize()
    example_4_crop()
    example_5_rotate_flip()
    example_6_compress()
    example_7_thumbnail()
    example_8_watermark()
    example_9_merge()
    example_10_batch()
    example_11_module_info()
    
    print("=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
