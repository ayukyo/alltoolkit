"""
Origami Utils 使用示例

展示折纸工具的各种功能用法
"""

import sys
sys.path.insert(0, '..')

from mod import (
    OrigamiUtils,
    FoldType,
    PaperSize,
    Crease,
    CreasePattern,
    FoldStep,
    create_square_from_a4,
    classic_crane_creases,
    classic_frog_creases,
    classic_waterbomb_creases,
)


def example_paper_sizes():
    """示例：纸张尺寸"""
    print("=" * 50)
    print("纸张尺寸示例")
    print("=" * 50)
    
    # 获取标准纸张尺寸
    for paper in [PaperSize.A4, PaperSize.A3, PaperSize.SQUARE_15]:
        width, height = paper.value
        print(f"{paper.name}: {width}mm × {height}mm")
    
    # 判断是否正方形
    a4_width, a4_height = PaperSize.A4.value
    print(f"\nA4 是正方形吗？{OrigamiUtils.is_square(a4_width, a4_height)}")
    
    # 从 A4 创建正方形
    sq_width, sq_height = create_square_from_a4()
    print(f"从 A4裁剪的正方形: {sq_width}mm × {sq_height}mm")
    
    # 纸张几何属性
    print(f"\nA4 纸张属性:")
    print(f"  面积: {OrigamiUtils.paper_area(a4_width, a4_height)} mm²")
    print(f"  周长: {OrigamiUtils.paper_perimeter(a4_width, a4_height)} mm")
    print(f"  对角线长度: {OrigamiUtils.diagonal_length(a4_width, a4_height):.2f} mm")
    print(f"  宽高比: {OrigamiUtils.aspect_ratio(a4_width, a4_height):.4f}")
    print(f"  是否 A 系列: {OrigamiUtils.is_a_series(a4_width, a4_height)}")


def example_basic_creases():
    """示例：基础折痕"""
    print("\n" + "=" * 50)
    print("基础折痕示例")
    print("=" * 50)
    
    # 创建简单折痕
    crease = Crease((0, 0), (100, 100), FoldType.VALLEY)
    print(f"折痕长度: {crease.length:.2f}mm")
    print(f"折痕中点: {crease.midpoint}")
    print(f"折痕角度: {crease.angle:.2f}°")
    print(f"折叠类型: {crease.fold_type.value}")
    
    # 水平折痕（中线）
    horizontal = OrigamiUtils.fold_line_coordinate(100, 100, 'horizontal', 0.5)
    print(f"\n水平中线: {horizontal.start} → {horizontal.end}")
    
    # 垂直折痕（中线）
    vertical = OrigamiUtils.fold_line_coordinate(100, 100, 'vertical', 0.5)
    print(f"垂直中线: {vertical.start} → {vertical.end}")
    
    # 对角线折痕
    diag1 = OrigamiUtils.fold_line_coordinate(100, 100, 'diagonal')
    diag2 = OrigamiUtils.fold_line_coordinate(100, 100, 'diagonal2')
    print(f"对角线1: {diag1.start} → {diag1.end}")
    print(f"对角线2: {diag2.start} → {diag2.end}")


def example_divisions():
    """示例：等分折痕"""
    print("\n" + "=" * 50)
    print("等分折痕示例")
    print("=" * 50)
    
    # 三等分
    thirds = OrigamiUtils.divide_paper(150, 150, 3, 'horizontal')
    print(f"水平三等分: {len(thirds)} 条折痕")
    for c in thirds:
        print(f"  {c.start} → {c.end}")
    
    # 四等分
    quarters = OrigamiUtils.divide_paper(150, 150, 4, 'vertical')
    print(f"\n垂直四等分: {len(quarters)} 条折痕")
    for c in quarters:
        print(f"  {c.start} → {c.end}")
    
    # 网格折痕
    grid = OrigamiUtils.grid_creases(150, 150, 4, 4)
    print(f"\n4×4 网格: {len(grid)} 条折痕")


def example_base_patterns():
    """示例：基础折痕模式"""
    print("\n" + "=" * 50)
    print("经典基础折痕模式")
    print("=" * 50)
    
    # 水弹基础
    waterbomb = OrigamiUtils.waterbomb_base_creases(150, 150)
    print(f"\n水弹基础:")
    print(f"  折痕数: {len(waterbomb.creases)}")
    print(f"  总长度: {waterbomb.total_crease_length():.2f}mm")
    print(f"  复杂度: {waterbomb.complexity_score()}")
    
    # 初步基础
    preliminary = OrigamiUtils.preliminary_base_creases(150, 150)
    print(f"\n初步基础:")
    print(f"  折痕数: {len(preliminary.creases)}")
    valley = preliminary.get_creases_by_type(FoldType.VALLEY)
    mountain = preliminary.get_creases_by_type(FoldType.MOUNTAIN)
    print(f"  谷折: {len(valley)} 条, 山折: {len(mountain)} 条")
    
    # Blintz 折法
    blintz = OrigamiUtils.blintz_fold_creases(150, 150)
    print(f"\nBlintz 折法:")
    print(f"  折痕数: {len(blintz.creases)}")
    
    # 鸟基础（千纸鹤）
    bird = OrigamiUtils.bird_base_creases(150, 150)
    print(f"\n鸟基础（千纸鹤）:")
    print(f"  折痕数: {len(bird.creases)}")
    
    # 鱼基础
    fish = OrigamiUtils.fish_base_creases(150, 150)
    print(f"\n鱼基础:")
    print(f"  折痕数: {len(fish.creases)}")
    
    # 青蛙基础
    frog = OrigamiUtils.frog_base_creases(150, 150)
    print(f"\n青蛙基础:")
    print(f"  折痕数: {len(frog.creases)}")


def example_classic_models():
    """示例：经典折纸模型"""
    print("\n" + "=" * 50)
    print("经典折纸模型")
    print("=" * 50)
    
    # 千纸鹤
    crane = classic_crane_creases()
    print(f"\n千纸鹤:")
    print(f"  纸张: {crane.width}mm × {crane.height}mm")
    print(f"  折痕数: {len(crane.creases)}")
    
    # 青蛙
    frog = classic_frog_creases()
    print(f"\n跳跃青蛙:")
    print(f"  纸张: {frog.width}mm × {frog.height}mm")
    print(f"  折痕数: {len(frog.creases)}")
    
    # 水弹
    waterbomb = classic_waterbomb_creases()
    print(f"\n水弹:")
    print(f"  纸张: {waterbomb.width}mm × {waterbomb.height}mm")
    print(f"  折痕数: {len(waterbomb.creases)}")


def example_fold_physics():
    """示例：折叠物理计算"""
    print("\n" + "=" * 50)
    print("折叠物理计算")
    print("=" * 50)
    
    # 折叠角度
    print("折叠角度:")
    for layers in [1, 2, 3, 5, 10]:
        angle = OrigamiUtils.fold_angle(layers)
        print(f"  {layers} 层纸: {angle:.1f}°")
    
    # 折叠后厚度（假设纸张 0.1mm 厚）
    print("\n折叠后厚度（纸张 0.1mm 厚）:")
    initial = 0.1
    for folds in [1, 2, 3, 5, 7, 10]:
        thickness = OrigamiUtils.paper_thickness_after_fold(initial, folds)
        print(f"  折 {folds} 次: {thickness:.2f}mm")
    
    # 最大折叠次数
    print("\n最大折叠次数估算:")
    print(f"  A4 纸（210×297mm, 0.1mm厚）: {OrigamiUtils.max_folds(0.1, 297)} 次")
    print(f"  大报纸（300×500mm, 0.05mm厚）: {OrigamiUtils.max_folds(0.05, 500)} 次")


def example_special_folds():
    """示例：特殊折法"""
    print("\n" + "=" * 50)
    print("特殊折法")
    print("=" * 50)
    
    # 兔耳折法
    rabbit = OrigamiUtils.rabbit_ear_crease(150, 150)
    print(f"\n兔耳折法: {len(rabbit)} 条折痕")
    
    # 放射状折痕
    mito = OrigamiUtils.mito_creases(150, 150, 45)
    print(f"\n放射状折痕（每45°一条）: {len(mito)} 条")
    
    # 压折
    squash_tl = OrigamiUtils.squash_fold_creases(150, 150, 'tl')
    print(f"\n压折（左上角）: {len(squash_tl.creases)} 条折痕")
    
    # 内翻折
    inside = OrigamiUtils.reverse_fold_creases(150, 150, 'inside')
    print(f"\n内翻折: {len(inside.creases)} 条折痕")
    
    # 外翻折
    outside = OrigamiUtils.reverse_fold_creases(150, 150, 'outside')
    print(f"\n外翻折: {len(outside.creases)} 条折痕")
    
    # 花瓣折
    petal = OrigamiUtils.petal_fold_creases(150, 150)
    print(f"\n花瓣折: {len(petal.creases)} 条折痕")
    
    # 沉折
    sink = OrigamiUtils.sink_fold_creases(150, 150)
    print(f"\n沉折: {len(sink.creases)} 条折痕")


def example_fold_sequence():
    """示例：折叠步骤生成"""
    print("\n" + "=" * 50)
    print("折叠步骤生成")
    print("=" * 50)
    
    pattern = OrigamiUtils.bird_base_creases(150, 150)
    steps = OrigamiUtils.generate_fold_sequence(pattern)
    
    print(f"\n鸟基础折叠步骤:")
    for step in steps:
        print(f"\n步骤 {step.step_number}: {step.description}")
        print(f"  折痕数: {len(step.creases)}")
        if step.notes:
            print(f"  说明: {step.notes}")


def example_custom_pattern():
    """示例：自定义折痕模式"""
    print("\n" + "=" * 50)
    print("自定义折痕模式")
    print("=" * 50)
    
    # 创建自定义折痕
    creases = [
        # 对角线
        Crease((0, 0), (100, 100), FoldType.VALLEY),
        Crease((100, 0), (0, 100), FoldType.MOUNTAIN),
        # 中线
        Crease((0, 50), (100, 50), FoldType.VALLEY),
        Crease((50, 0), (50, 100), FoldType.MOUNTAIN),
        # 四角到中心
        Crease((0, 0), (50, 50), FoldType.VALLEY),
        Crease((100, 0), (50, 50), FoldType.VALLEY),
        Crease((100, 100), (50, 50), FoldType.VALLEY),
        Crease((0, 100), (50, 50), FoldType.VALLEY),
    ]
    
    pattern = CreasePattern(100, 100, creases)
    print(f"\n自定义模式:")
    print(f"  纸张: {pattern.width}mm × {pattern.height}mm")
    print(f"  折痕数: {len(pattern.creases)}")
    print(f"  总长度: {pattern.total_crease_length():.2f}mm")
    print(f"  复杂度: {pattern.complexity_score()}")
    
    # 按类型统计
    valley = pattern.get_creases_by_type(FoldType.VALLEY)
    mountain = pattern.get_creases_by_type(FoldType.MOUNTAIN)
    print(f"  谷折: {len(valley)} 条")
    print(f"  山折: {len(mountain)} 条")


def main():
    """运行所有示例"""
    example_paper_sizes()
    example_basic_creases()
    example_divisions()
    example_base_patterns()
    example_classic_models()
    example_fold_physics()
    example_special_folds()
    example_fold_sequence()
    example_custom_pattern()
    
    print("\n" + "=" * 50)
    print("示例完成！")
    print("=" * 50)


if __name__ == '__main__':
    main()