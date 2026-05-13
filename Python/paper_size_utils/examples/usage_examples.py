"""
AllToolkit - Python Paper Size Utilities 使用示例

演示纸张尺寸工具模块的各种使用场景。

Author: AllToolkit
License: MIT
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    PaperSize, PaperSeries,
    get_paper_size, get_all_paper_sizes, get_paper_sizes_by_series,
    search_paper_sizes, list_available_papers, print_paper_info,
    mm_to_pixels, pixels_to_mm, inch_to_mm, mm_to_inch,
    calculate_pixels_for_paper, calculate_dpi_for_paper,
    find_paper_by_dimensions, find_paper_by_area, find_paper_by_aspect_ratio,
    calculate_iso_paper_size, scale_paper_to_fit, get_best_fit_paper,
    compare_paper_sizes, get_version
)


def example_basic_usage():
    """基本用法示例。"""
    print("\n=== 基本用法示例 ===\n")
    
    # 获取 A4 纸张信息
    a4 = get_paper_size("A4")
    print(f"A4 纸张尺寸: {a4.width_mm}×{a4.height_mm} mm")
    print(f"A4 纸张面积: {a4.area_mm2:.2f} mm² ({a4.area_cm2:.2f} cm²)")
    print(f"A4 宽高比: {a4.aspect_ratio:.4f}")
    print(f"A4 方向: {a4.get_orientation()}")
    
    # 获取 Letter 纸张信息
    letter = get_paper_size("Letter")
    print(f"\nLetter 纸张尺寸: {letter.width_mm:.2f}×{letter.height_mm:.2f} mm")
    print(f"Letter 纸张面积: {letter.area_inch2:.2f} inch²")
    print(f"Letter 描述: {letter.description}")
    
    # 获取名片尺寸
    card = get_paper_size("标准名片")
    print(f"\n标准名片尺寸: {card.width_mm}×{card.height_mm} mm")


def example_pixel_conversion():
    """像素转换示例。"""
    print("\n=== 像素转换示例 ===\n")
    
    # 计算 A4 在不同 DPI 下的像素尺寸
    a4 = get_paper_size("A4")
    
    print("A4 纸张在不同 DPI 下的像素尺寸:")
    for dpi in [72, 150, 300, 600]:
        width, height = a4.to_pixels(dpi)
        print(f"  {dpi} DPI: {width}×{height} px")
    
    # 印刷行业标准 DPI
    print("\n印刷行业常见 DPI 参考:")
    print("  网页显示: 72-96 DPI")
    print("  普通打印: 150-200 DPI")
    print("  高质量打印: 300 DPI")
    print("  专业印刷: 600+ DPI")
    
    # 单位转换
    print("\n单位转换示例:")
    pixels = mm_to_pixels(210, 300)
    print(f"  210mm @ 300 DPI = {pixels} px")
    
    mm = pixels_to_mm(2481, 300)
    print(f"  2481 px @ 300 DPI = {mm:.2f} mm")
    
    inch = mm_to_inch(210)
    print(f"  210mm = {inch:.4f} inch")
    
    mm = inch_to_mm(8.5)
    print(f"  8.5 inch = {mm:.2f} mm")


def example_paper_comparison():
    """纸张比较示例。"""
    print("\n=== 纸张比较示例 ===\n")
    
    # 比较 A4 和 Letter
    comparison = compare_paper_sizes("A4", "Letter")
    
    print("A4 与 Letter 比较:")
    print(f"  A4 尺寸: {comparison['paper1']['width_mm']}×{comparison['paper1']['height_mm']} mm")
    print(f"  Letter 尺寸: {comparison['paper2']['width_mm']}×{comparison['paper2']['height_mm']} mm")
    print(f"  宽度差异: {comparison['width_difference_mm']:.2f} mm")
    print(f"  高度差异: {comparison['height_difference_mm']:.2f} mm")
    print(f"  面积比例: {comparison['area_ratio']:.4f} (A4 是 Letter 的 {comparison['area_ratio']*100:.2f}%)")
    print(f"  较大者: {comparison['larger']}")
    
    # 比较 A 系列相邻纸张
    print("\nA 系列相邻纸张比较:")
    for n in range(0, 5):
        a_n = get_paper_size(f"A{n}")
        a_n_plus_1 = get_paper_size(f"A{n+1}")
        ratio = a_n.area_mm2 / a_n_plus_1.area_mm2
        print(f"  A{n} → A{n+1}: 面积比例 {ratio:.2f} (约 2 倍)")
    
    # ISO A 系列的宽高比一致性
    print("\nISO A 系列宽高比一致性:")
    ratios = []
    for n in range(0, 11):
        paper = get_paper_size(f"A{n}")
        ratios.append(paper.aspect_ratio)
    
    print(f"  所有 A 系列宽高比约为: {sum(ratios)/len(ratios):.4f} (√2 ≈ 0.7071)")


def example_find_paper():
    """纸张查找示例。"""
    print("\n=== 纸张查找示例 ===\n")
    
    # 按尺寸查找
    print("按尺寸查找纸张 (210×297mm):")
    papers = find_paper_by_dimensions(210, 297, "mm")
    for paper in papers:
        print(f"  找到: {paper.name} ({paper.width_mm}×{paper.height_mm}mm)")
    
    # 按面积查找
    print("\n按面积查找纸张 (约 62370 mm²):")
    papers = find_paper_by_area(62370, "mm2")
    for paper in papers:
        print(f"  找到: {paper.name} (面积 {paper.area_mm2:.0f} mm²)")
    
    # 按宽高比查找
    print("\n按宽高比查找纸张 (≈ 0.707, ISO A 系列特征):")
    papers = find_paper_by_aspect_ratio(0.707, tolerance=0.01)
    a_papers = [p for p in papers if p.series == PaperSeries.ISO_A]
    print(f"  找到 {len(a_papers)} 个 ISO A 系列纸张")
    
    # 最佳匹配纸张
    print("\n查找最佳匹配纸张:")
    paper = get_best_fit_paper(200, 280, "mm")
    if paper:
        print(f"  200×280mm 内容最佳匹配: {paper.name} ({paper.width_mm}×{paper.height_mm}mm)")
    
    paper = get_best_fit_paper(800, 1100, "mm")
    if paper:
        print(f"  800×1100mm 内容最佳匹配: {paper.name} ({paper.width_mm}×{paper.height_mm}mm)")


def example_iso_calculation():
    """ISO 纸张计算示例。"""
    print("\n=== ISO 纸张计算示例 ===\n")
    
    # 计算任意 ISO A 系列纸张
    print("计算任意 ISO A 系列纸张:")
    
    for n in [0, 4, 10, 15]:
        paper = calculate_iso_paper_size("A", n)
        print(f"  A{n}: {paper.width_mm:.4f}×{paper.height_mm:.4f} mm, 面积 {paper.area_mm2:.4f} mm²")
    
    # 计算 ISO B 系列
    print("\n计算 ISO B 系列纸张:")
    for n in [0, 5, 10]:
        paper = calculate_iso_paper_size("B", n)
        print(f"  B{n}: {paper.width_mm:.2f}×{paper.height_mm:.2f} mm")
    
    # 计算 ISO C 系列（信封）
    print("\n计算 ISO C 系列纸张（信封）:")
    for n in [4, 5, 6]:
        paper = calculate_iso_paper_size("C", n)
        print(f"  C{n}: {paper.width_mm:.2f}×{paper.height_mm:.2f} mm - {paper.description}")
    
    # 负号数（比 A0 大）
    print("\n负号数计算（比 A0 大的纸张）:")
    for n in [-1, -2]:
        paper = calculate_iso_paper_size("A", n)
        print(f"  A({n}): {paper.width_mm:.2f}×{paper.height_mm:.2f} mm")
    
    # 验证 ISO 规则
    print("\n验证 ISO A 系列规则:")
    a0 = get_paper_size("A0")
    print(f"  A0 面积: {a0.area_mm2:.0f} mm² ≈ 1 m² ({a0.area_mm2 / 1_000_000:.2f} m²)")
    
    # 验证宽高比
    sqrt2 = 1.41421356237
    print(f"  A0 宽高比: {a0.aspect_ratio:.4f}")
    print(f"  √2 倒数: {1/sqrt2:.4f}")
    print(f"  误差: {abs(a0.aspect_ratio - 1/sqrt2):.8f}")


def example_series_filter():
    """系列过滤示例。"""
    print("\n=== 系列过滤示例 ===\n")
    
    # 获取各系列纸张数量
    print("各系列纸张数量统计:")
    for series in PaperSeries:
        papers = get_paper_sizes_by_series(series)
        print(f"  {series.value}: {len(papers)} 种")
    
    # 列出 ISO A 系列
    print("\nISO A 系列纸张:")
    a_series = get_paper_sizes_by_series(PaperSeries.ISO_A)
    for name, paper in sorted(a_series.items()):
        print(f"  {name}: {paper.width_mm}×{paper.height_mm} mm")
    
    # 列出北美纸张
    print("\n北美常用纸张:")
    na_series = get_paper_sizes_by_series(PaperSeries.NORTH_AMERICAN)
    common = ["Letter", "Legal", "Tabloid", "Executive"]
    for name in common:
        if name in na_series:
            paper = na_series[name]
            print(f"  {paper.name}: {paper.width_inch:.2f}×{paper.height_inch:.2f} inch")


def example_search():
    """搜索示例。"""
    print("\n=== 搜索示例 ===\n")
    
    # 搜索关键词
    print("搜索 '信封':")
    envelopes = search_paper_sizes("信封")
    for paper in envelopes[:5]:
        print(f"  {paper.name}: {paper.width_mm}×{paper.height_mm} mm - {paper.description}")
    
    print("\n搜索 '海报':")
    posters = search_paper_sizes("海报")
    for paper in posters[:5]:
        print(f"  {paper.name}: {paper.description}")
    
    print("\n搜索 '照片':")
    photos = search_paper_sizes("照片")
    for paper in photos[:5]:
        print(f"  {paper.name}: {paper.width_mm}×{paper.height_mm} mm")


def example_photo_printing():
    """照片打印示例。"""
    print("\n=== 照片打印示例 ===\n")
    
    # 常见照片尺寸
    print("常见照片尺寸及其像素需求:")
    photo_sizes = ["2R", "3R", "4R", "5R", "8R"]
    
    for name in photo_sizes:
        photo = get_paper_size(name)
        if photo:
            width_300, height_300 = photo.to_pixels(300)
            width_150, height_150 = photo.to_pixels(150)
            
            print(f"\n{name} ({photo.description}):")
            print(f"  尺寸: {photo.width_inch:.2f}×{photo.height_inch:.2f} inch")
            print(f"  打印质量 (300 DPI): {width_300}×{height_300} px")
            print(f"  普通打印 (150 DPI): {width_150}×{height_150} px")
    
    # 照片 DPI 计算
    print("\n计算照片打印 DPI:")
    
    # 一张 1920×1080 的照片要打印到 4R (4×6 inch)
    dpi = calculate_dpi_for_paper("4R", 1920, 1080)
    print(f"  1920×1080 px 照片打印到 4R: 需要 {dpi:.2f} DPI")
    
    # 要达到 300 DPI 需要多少像素
    width, height = calculate_pixels_for_paper("4R", 300)
    print(f"  4R 照片 300 DPI 需要: {width}×{height} px")


def example_print_layout():
    """打印排版示例。"""
    print("\n=== 打印排版示例 ===\n")
    
    # 计算缩放比例
    print("计算纸张缩放比例:")
    
    # A5 内容缩放到 A4
    scale_w, scale_h = scale_paper_to_fit("A5", 210, 297, "mm")
    print(f"  A5 缩放到 A4: 宽度 {scale_w:.2f}x, 高度 {scale_h:.2f}x")
    
    # Letter 内容缩放到 A4
    letter = get_paper_size("Letter")
    scale_w, scale_h = scale_paper_to_fit("Letter", 210, 297, "mm")
    print(f"  Letter 缩放到 A4: 宽度 {scale_w:.4f}x, 高度 {scale_h:.4f}x")
    print(f"    (Letter 略宽略矮，需要缩放)")
    
    # 最佳纸张选择
    print("\n根据内容选择最佳纸张:")
    
    contents = [
        (150, 200, "名片设计稿"),
        (200, 280, "文档内容"),
        (400, 600, "海报设计"),
        (800, 1100, "大型图纸"),
    ]
    
    for width, height, desc in contents:
        paper = get_best_fit_paper(width, height, "mm")
        if paper:
            print(f"  {desc} ({width}×{height}mm): 推荐 {paper.name} ({paper.width_mm}×{paper.height_mm}mm)")


def example_print_info():
    """打印详细信息示例。"""
    print("\n=== 详细信息示例 ===\n")
    
    # 打印 A4 完整信息
    print("A4 纸张完整信息:")
    print(print_paper_info("A4"))
    
    print("\n" + "-"*50 + "\n")
    
    # 打印 Letter 完整信息
    print("Letter 纸张完整信息:")
    print(print_paper_info("Letter"))


def example_misc():
    """杂项示例。"""
    print("\n=== 杂项示例 ===\n")
    
    # 模块信息
    print(f"模块版本: {get_version()}")
    
    # 统计
    all_sizes = get_all_paper_sizes()
    print(f"共收录 {len(all_sizes)} 种纸张尺寸")
    
    papers = list_available_papers()
    print(f"可用纸张名称: {len(papers)} 个")
    
    # PaperSize 数据类功能
    print("\nPaperSize 数据类功能演示:")
    
    a4 = get_paper_size("A4")
    
    # 转换为字典
    d = a4.to_dict()
    print("A4 转为字典:")
    for key, value in d.items():
        print(f"  {key}: {value}")
    
    # 翻转
    flipped = a4.flip()
    print(f"\nA4 翻转后: {flipped.width_mm}×{flipped.height_mm} mm ({flipped.get_orientation()})")


def main():
    """运行所有示例。"""
    print("="*60)
    print("Paper Size Utilities 使用示例")
    print("="*60)
    
    example_basic_usage()
    example_pixel_conversion()
    example_paper_comparison()
    example_find_paper()
    example_iso_calculation()
    example_series_filter()
    example_search()
    example_photo_printing()
    example_print_layout()
    example_print_info()
    example_misc()
    
    print("\n" + "="*60)
    print("所有示例完成!")
    print("="*60)


if __name__ == '__main__':
    main()