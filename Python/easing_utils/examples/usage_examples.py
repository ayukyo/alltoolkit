#!/usr/bin/env python3
"""
Easing Utilities - 使用示例

展示缓动函数的各种实际应用场景。
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from easing_utils.mod import (
    EasingType, EasingMode,
    ease, get_easing_function,
    interpolate, interpolate_list, interpolate_2d, interpolate_3d,
    generate_animation_frames, generate_animation_frames_2d,
    chain_easing, blend_easing,
    compare_easings, create_easing_curve,
    cubic_bezier, get_css_easing,
)


def example_01_basic_easing():
    """示例 1: 基本缓动函数使用"""
    print("=" * 60)
    print("示例 1: 基本缓动函数使用")
    print("=" * 60)
    
    # 直接调用缓动函数
    print("\n直接调用缓动函数:")
    print(f"  ease_out_quad(0.0) = {ease(0.0, 'quad', 'out'):.4f}")
    print(f"  ease_out_quad(0.25) = {ease(0.25, 'quad', 'out'):.4f}")
    print(f"  ease_out_quad(0.5) = {ease(0.5, 'quad', 'out'):.4f}")
    print(f"  ease_out_quad(0.75) = {ease(0.75, 'quad', 'out'):.4f}")
    print(f"  ease_out_quad(1.0) = {ease(1.0, 'quad', 'out'):.4f}")
    
    # 使用 ease 函数（推荐）
    print("\n使用 ease() 统一接口:")
    for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
        val = ease(t, EasingType.CUBIC, EasingMode.OUT)
        print(f"  ease({t}, 'cubic', 'out') = {val:.4f}")
    
    # 不同缓动类型对比
    print("\n不同缓动类型在 t=0.5 时的值:")
    result = compare_easings(0.5)
    for name, val in sorted(result.items()):
        print(f"  {name}: {val:.4f}")


def example_02_value_interpolation():
    """示例 2: 值插值"""
    print("\n" + "=" * 60)
    print("示例 2: 值插值")
    print("=" * 60)
    
    # 基本插值
    print("\n基本数值插值:")
    print(f"  线性插值: interpolate(0, 100, 0.5) = {interpolate(0, 100, 0.5)}")
    print(f"  quad_out: interpolate(0, 100, 0.5, 'quad', 'out') = {interpolate(0, 100, 0.5, 'quad', 'out')}")
    print(f"  cubic_in: interpolate(0, 100, 0.5, 'cubic', 'in') = {interpolate(0, 100, 0.5, 'cubic', 'in')}")
    
    # 动画帧序列
    print("\n生成动画帧序列 (0 → 100, 10帧, quad_out):")
    frames = generate_animation_frames(0, 100, 10, 'quad', 'out')
    for i, val in enumerate(frames):
        print(f"  帧 {i}: {val:.2f}")
    
    # 位置插值
    print("\n二维位置插值:")
    start = (0, 0)
    end = (200, 300)
    for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
        pos = interpolate_2d(start, end, t, 'quad', 'out')
        print(f"  t={t:.2f}: ({pos[0]:.2f}, {pos[1]:.2f})")


def example_03_animation_sequence():
    """示例 3: 动画序列生成"""
    print("\n" + "=" * 60)
    print("示例 3: 动画序列生成")
    print("=" * 60)
    
    # UI 元素入场动画
    print("\nUI 元素入场动画 (从底部滑入):")
    start_y = 500  # 开始位置（屏幕底部外）
    end_y = 100    # 目标位置
    
    frames = generate_animation_frames(start_y, end_y, 30, 'cubic', 'out')
    print(f"  生成 {len(frames)} 帧")
    print(f"  开始: y={frames[0]:.2f}")
    print(f"  中间: y={frames[15]:.2f}")
    print(f"  结束: y={frames[-1]:.2f}")
    
    # 弹跳效果
    print("\n弹跳效果 (球落下):")
    frames = generate_animation_frames(0, 100, 20, 'bounce', 'out')
    print(f"  位置变化:")
    for i, val in enumerate(frames):
        print(f"    帧 {i}: {val:.2f}")
    
    # 回弹效果
    print("\n回弹效果 (按钮点击):")
    frames = generate_animation_frames(1.0, 0.9, 5, 'back', 'out')
    for i, val in enumerate(frames):
        print(f"  帧 {i}: scale={val:.4f}")


def example_04_game_movement():
    """示例 4: 游戏中的移动"""
    print("\n" + "=" * 60)
    print("示例 4: 游戏中的移动")
    print("=" * 60)
    
    # 角色移动
    print("\n角色平滑移动:")
    character_start = (100, 200)
    character_target = (400, 300)
    
    # 使用不同的缓动效果
    easing_types = ['linear', 'quad', 'cubic', 'sine']
    
    for easing_type in easing_types:
        path = generate_animation_frames_2d(
            character_start, character_target, 10, easing_type, 'in_out'
        )
        print(f"\n  {easing_type} 缓动路径:")
        for i, pos in enumerate(path):
            print(f"    帧 {i}: ({pos[0]:.2f}, {pos[1]:.2f})")
    
    # 弹性跳跃
    print("\n弹性跳跃效果:")
    jump_path = generate_animation_frames_2d(
        (100, 0), (200, 0), 15, 'elastic', 'out'
    )
    for i, pos in enumerate(jump_path):
        print(f"  帧 {i}: x={pos[0]:.2f}, y={pos[1]:.2f}")


def example_05_chain_and_blend():
    """示例 5: 组合缓动"""
    print("\n" + "=" * 60)
    print("示例 5: 组合缓动")
    print("=" * 60)
    
    # 链式缓动
    print("\n链式缓动 - 复杂动画序列:")
    # 先快速减速，然后弹跳结束
    config = [
        (0.6, 'quart', 'out'),  # 前 60% 快速减速
        (0.4, 'bounce', 'out'), # 后 40% 弹跳
    ]
    
    print("  配置: 前60% quart_out + 后40% bounce_out")
    for t in [0.0, 0.3, 0.5, 0.7, 0.9, 1.0]:
        val = chain_easing(t, config)
        print(f"    t={t:.2f}: {val:.4f}")
    
    # 混合缓动
    print("\n混合缓动 - 中间过渡:")
    # 混合 quad 和 cubic
    for blend in [0.0, 0.25, 0.5, 0.75, 1.0]:
        val = blend_easing(0.5, 'quad', 'cubic', blend)
        print(f"  blend={blend:.2f}: {val:.4f}")


def example_06_css_compatibility():
    """示例 6: CSS 兼容性"""
    print("\n" + "=" * 60)
    print("示例 6: CSS 兼容性")
    print("=" * 60)
    
    # CSS 标准缓动
    print("\nCSS 标准缓动函数:")
    css_names = ['linear', 'ease', 'ease-in', 'ease-out', 'ease-in-out']
    
    for name in css_names:
        fn = get_css_easing(name)
        values = [fn(t) for t in [0.0, 0.25, 0.5, 0.75, 1.0]]
        print(f"  {name}: {values}")
    
    # 自定义 cubic-bezier
    print("\n自定义 cubic-bezier 曲线:")
    # 类似 iOS 的标准动画曲线
    ios_ease = cubic_bezier(0.25, 0.1, 0.25, 1.0)
    print("  iOS ease 曲线 (cubic-bezier(0.25, 0.1, 0.25, 1.0)):")
    for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
        print(f"    t={t:.2f}: {ios_ease(t):.4f}")


def example_07_animation_curve_analysis():
    """示例 7: 动画曲线分析"""
    print("\n" + "=" * 60)
    print("示例 7: 动画曲线分析")
    print("=" * 60)
    
    # 生成曲线数据
    print("\n生成缓动曲线数据 (可用于绘图):")
    curve = create_easing_curve('cubic', 'in_out', 20)
    print(f"  数据点: {len(curve)} 个")
    print("  前5个点:")
    for t, val in curve[:5]:
        print(f"    (t={t:.3f}, val={val:.4f})")
    
    # 极值分析
    print("\n极值分析 (超出 [0, 1] 范围):")
    from easing_utils.mod import get_easing_extremes
    
    for easing_type in ['back', 'elastic', 'linear', 'quad']:
        min_val, max_val = get_easing_extremes(easing_type, 'out')
        print(f"  {easing_type}_out: min={min_val:.4f}, max={max_val:.4f}")
        if min_val < 0 or max_val > 1:
            print(f"    ⚠️ 超出 [0, 1] 范围")


def example_08_practical_ui_animation():
    """示例 8: 实际 UI 动画应用"""
    print("\n" + "=" * 60)
    print("示例 8: 实际 UI 动画应用")
    print("=" * 60)
    
    # 模态框出现
    print("\n模态框淡入缩放动画:")
    opacity_frames = generate_animation_frames(0, 1, 10, 'quad', 'out')
    scale_frames = generate_animation_frames(0.8, 1.0, 10, 'back', 'out')
    
    print("  帧  | opacity | scale")
    print("  " + "-" * 30)
    for i in range(10):
        print(f"  {i:3d} | {opacity_frames[i]:.4f} | {scale_frames[i]:.4f}")
    
    # 滑动切换
    print("\n页面滑动切换:")
    slide_start = -100  # 左侧屏幕外
    slide_end = 0       # 正常位置
    
    frames = generate_animation_frames(slide_start, slide_end, 15, 'cubic', 'out')
    print(f"  位置变化 (帧 0, 5, 10, 14):")
    for i in [0, 5, 10, 14]:
        print(f"    帧 {i}: x={frames[i]:.2f}")
    
    # 进度条动画
    print("\n进度条平滑增长:")
    progress_frames = generate_animation_frames(0, 100, 20, 'quart', 'out')
    print(f"  进度值:")
    for i in [0, 5, 10, 15, 19]:
        print(f"    帧 {i}: {progress_frames[i]:.1f}%")


def example_09_visual_comparison():
    """示例 9: 可视化对比"""
    print("\n" + "=" * 60)
    print("示例 9: 可视化对比")
    print("=" * 60)
    
    # 简单文本可视化
    print("\n文本可视化缓动曲线:")
    
    easing_types = ['linear', 'quad', 'cubic', 'bounce', 'elastic']
    width = 50
    
    for easing_type in easing_types:
        print(f"\n  {easing_type} ease_out:")
        for t in range(0, 11):
            t_val = t / 10
            val = ease(t_val, easing_type, 'out')
            bar_pos = int(val * (width - 1))
            bar = '·' * bar_pos + '●' + '·' * (width - bar_pos - 1)
            print(f"    {t_val:.1f} |{bar}| {val:.2f}")


def example_10_advanced_usage():
    """示例 10: 高级用法"""
    print("\n" + "=" * 60)
    print("示例 10: 高级用法")
    print("=" * 60)
    
    # 获取缓动函数引用
    print("\n获取缓动函数引用（用于回调或配置）:")
    fn = get_easing_function('quad', 'out')
    print(f"  函数: {fn}")
    print(f"  fn(0.5) = {fn(0.5)}")
    
    # 列表插值（路径动画）
    print("\n路径动画（多点插值）:")
    waypoints = [0, 100, 50, 200, 150]
    
    for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
        pos = interpolate_list(waypoints, t, 'cubic', 'in_out')
        print(f"  t={t:.2f}: pos={pos:.2f}")
    
    # 序列重采样
    print("\n序列缓动重采样:")
    from easing_utils.mod import apply_easing_to_sequence
    
    original = [0, 10, 20, 30, 40, 50]
    resampled = apply_easing_to_sequence(original, 'quad', 'out')
    print(f"  原始序列: {original}")
    print(f"  重采样后: {[round(x, 2) for x in resampled]}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("Easing Utilities 使用示例")
    print("=" * 60)
    
    examples = [
        example_01_basic_easing,
        example_02_value_interpolation,
        example_03_animation_sequence,
        example_04_game_movement,
        example_05_chain_and_blend,
        example_06_css_compatibility,
        example_07_animation_curve_analysis,
        example_08_practical_ui_animation,
        example_09_visual_comparison,
        example_10_advanced_usage,
    ]
    
    for example in examples:
        example()
    
    print("\n" + "=" * 60)
    print("示例运行完成")
    print("=" * 60)


if __name__ == "__main__":
    main()