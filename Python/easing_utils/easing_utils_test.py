#!/usr/bin/env python3
"""
Easing Utilities - 测试模块

测试所有缓动函数、插值函数和工具函数。
"""

import sys
import os
import math

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # 枚举
    EasingType, EasingMode,
    
    # 辅助函数
    clamp, normalize_progress,
    
    # 核心函数
    linear,
    
    # Quad
    ease_in_quad, ease_out_quad, ease_in_out_quad, ease_out_in_quad,
    
    # Cubic
    ease_in_cubic, ease_out_cubic, ease_in_out_cubic, ease_out_in_cubic,
    
    # Quart
    ease_in_quart, ease_out_quart, ease_in_out_quart, ease_out_in_quart,
    
    # Quint
    ease_in_quint, ease_out_quint, ease_in_out_quint, ease_out_in_quint,
    
    # Sine
    ease_in_sine, ease_out_sine, ease_in_out_sine, ease_out_in_sine,
    
    # Expo
    ease_in_expo, ease_out_expo, ease_in_out_expo, ease_out_in_expo,
    
    # Circ
    ease_in_circ, ease_out_circ, ease_in_out_circ, ease_out_in_circ,
    
    # Elastic
    ease_in_elastic, ease_out_elastic, ease_in_out_elastic, ease_out_in_elastic,
    
    # Back
    ease_in_back, ease_out_back, ease_in_out_back, ease_out_in_back,
    
    # Bounce
    ease_in_bounce, ease_out_bounce, ease_in_out_bounce, ease_out_in_bounce,
    
    # 统一接口
    get_easing_function, ease,
    
    # 插值
    interpolate, interpolate_list, interpolate_2d, interpolate_3d,
    
    # 动画序列
    generate_animation_frames, generate_animation_frames_2d,
    
    # 组合
    chain_easing, blend_easing,
    
    # 分析
    get_easing_derivative, get_easing_extremes, compare_easings,
    
    # 便捷方法
    create_easing_curve, apply_easing_to_sequence,
    
    # CSS 兼容
    cubic_bezier, get_css_easing, CSS_EASING,
    
    # 常量
    PI, HALF_PI, TAU,
)


def test_basic_values():
    """测试基本值"""
    print("测试基本值...")
    
    # 所有缓动函数在 t=0 时应返回 0
    test_functions = [
        linear, ease_in_quad, ease_out_quad, ease_in_cubic, ease_out_cubic,
        ease_in_quart, ease_out_quart, ease_in_quint, ease_out_quint,
        ease_in_sine, ease_out_sine, ease_in_expo, ease_out_expo,
        ease_in_circ, ease_out_circ, ease_in_back, ease_out_back,
    ]
    
    for fn in test_functions:
        assert abs(fn(0) - 0) < 0.0001, f"{fn.__name__}(0) 应该是 0"
    
    # 所有缓动函数在 t=1 时应返回 1
    for fn in test_functions:
        assert abs(fn(1) - 1) < 0.0001, f"{fn.__name__}(1) 应该是 1"
    
    # 线性函数
    assert linear(0) == 0
    assert linear(0.5) == 0.5
    assert linear(1) == 1
    
    # 弹性函数边界
    assert ease_in_elastic(0) == 0
    assert ease_out_elastic(1) == 1
    
    # 弹跳函数边界
    assert ease_out_bounce(0) == 0
    assert ease_out_bounce(1) == 1
    
    print("✓ 基本值测试通过")


def test_quad_easing():
    """测试二次方缓动"""
    print("测试二次方缓动...")
    
    # ease_in_quad: 开始慢，结束快
    assert ease_in_quad(0.5) == 0.25
    
    # ease_out_quad: 开始快，结束慢
    assert ease_out_quad(0.5) == 0.75
    
    # ease_in_out_quad: 中间值
    mid = ease_in_out_quad(0.5)
    assert 0.4 < mid < 0.6
    
    # ease_out_in_quad: 中间值
    mid = ease_out_in_quad(0.5)
    assert 0.4 < mid < 0.6
    
    print("✓ 二次方缓动测试通过")


def test_cubic_easing():
    """测试三次方缓动"""
    print("测试三次方缓动...")
    
    # ease_in_cubic
    assert ease_in_cubic(0.5) == 0.125
    
    # ease_out_cubic
    assert ease_out_cubic(0.5) == 0.875
    
    # ease_in_out_cubic
    mid = ease_in_out_cubic(0.5)
    assert abs(mid - 0.5) < 0.01
    
    print("✓ 三次方缓动测试通过")


def test_quart_easing():
    """测试四次方缓动"""
    print("测试四次方缓动...")
    
    # ease_in_quart
    assert ease_in_quart(0.5) == 0.0625
    
    # ease_out_quart
    assert ease_out_quart(0.5) == 0.9375
    
    print("✓ 四次方缓动测试通过")


def test_quint_easing():
    """测试五次方缓动"""
    print("测试五次方缓动...")
    
    # ease_in_quint
    assert ease_in_quint(0.5) == 0.03125
    
    # ease_out_quint
    assert ease_out_quint(0.5) == 0.96875
    
    print("✓ 五次方缓动测试通过")


def test_sine_easing():
    """测试正弦缓动"""
    print("测试正弦缓动...")
    
    # ease_in_sine
    in_mid = ease_in_sine(0.5)
    assert 0.2 < in_mid < 0.3  # sin(π/4) / 2 ≈ 0.29
    
    # ease_out_sine
    out_mid = ease_out_sine(0.5)
    assert 0.7 < out_mid < 0.8  # sin(π/4) ≈ 0.71
    
    # ease_in_out_sine
    mid = ease_in_out_sine(0.5)
    assert abs(mid - 0.5) < 0.01
    
    print("✓ 正弦缓动测试通过")


def test_expo_easing():
    """测试指数缓动"""
    print("测试指数缓动...")
    
    # ease_in_expo: 开始非常慢
    assert ease_in_expo(0.1) < 0.1
    
    # ease_out_expo: 结束非常慢
    assert ease_out_expo(0.9) > 0.9
    
    # 边界条件
    assert ease_in_expo(0) == 0
    assert ease_out_expo(1) == 1
    
    print("✓ 指数缓动测试通过")


def test_circ_easing():
    """测试圆形缓动"""
    print("测试圆形缓动...")
    
    # ease_in_circ: 开始慢
    in_mid = ease_in_circ(0.5)
    assert 0.1 < in_mid < 0.2  # 1 - sqrt(1 - 0.25) ≈ 0.134
    
    # ease_out_circ: 结束慢
    out_mid = ease_out_circ(0.5)
    assert 0.8 < out_mid < 0.9  # sqrt(1 - 0.25) ≈ 0.866
    
    print("✓ 圆形缓动测试通过")


def test_elastic_easing():
    """测试弹性缓动"""
    print("测试弹性缓动...")
    
    # ease_out_elastic: 有弹性效果
    val = ease_out_elastic(0.5)
    # 弹性值可能超出 [0, 1] 范围
    assert -0.5 < val < 1.5
    
    # 边界
    assert ease_in_elastic(0) == 0
    assert ease_out_elastic(1) == 1
    
    print("✓ 弹性缓动测试通过")


def test_back_easing():
    """测试回弹缓动"""
    print("测试回弹缓动...")
    
    # ease_in_back: 开始有回退
    in_val = ease_in_back(0.1)
    assert in_val < 0  # 负值
    
    # ease_out_back: 结束有超出
    out_val = ease_out_back(0.9)
    assert out_val > 1  # 超出 1
    
    # 极值检查
    min_val, max_val = get_easing_extremes('back', 'out')
    assert min_val < 0 or max_val > 1  # 超出范围
    
    print("✓ 回弹缓动测试通过")


def test_bounce_easing():
    """测试弹跳缓动"""
    print("测试弹跳缓动...")
    
    # ease_out_bounce: 有弹跳效果
    val = ease_out_bounce(0.5)
    assert 0 < val < 1
    
    # 边界
    assert ease_in_bounce(0) == 0
    assert ease_out_bounce(1) == 1
    
    # 弹跳特征: 多个平台阶段
    # 在某些区间值变化很小
    assert ease_out_bounce(0.7) > ease_out_bounce(0.6)  # 递增
    
    print("✓ 弹跳缓动测试通过")


def test_get_easing_function():
    """测试获取缓动函数"""
    print("测试获取缓动函数...")
    
    # 使用枚举
    fn = get_easing_function(EasingType.QUAD, EasingMode.OUT)
    assert fn(0.5) == 0.75
    
    # 使用字符串
    fn = get_easing_function('quad', 'out')
    assert fn(0.5) == 0.75
    
    # 使用字符串（大写）
    fn = get_easing_function('QUAD', 'OUT')
    assert fn(0.5) == 0.75
    
    # 无效类型
    try:
        get_easing_function('invalid', 'out')
        assert False, "应该抛出异常"
    except ValueError:
        pass
    
    print("✓ 获取缓动函数测试通过")


def test_ease():
    """测试 ease 统一接口"""
    print("测试 ease 统一接口...")
    
    # 默认参数
    val = ease(0.5)
    assert 0 < val < 1
    
    # 指定类型和模式
    val = ease(0.5, 'cubic', 'in_out')
    assert abs(val - 0.5) < 0.01
    
    # 使用枚举
    val = ease(0.5, EasingType.QUAD, EasingMode.OUT)
    assert val == 0.75
    
    print("✓ ease 统一接口测试通过")


def test_interpolate():
    """测试插值函数"""
    print("测试插值函数...")
    
    # 基本插值
    val = interpolate(0, 100, 0.5)
    assert val == 50.0
    
    # 缓动插值
    val = interpolate(0, 100, 0.5, 'quad', 'out')
    assert val == 75.0
    
    # 反向插值
    val = interpolate(100, 0, 0.5)
    assert val == 50.0
    
    # 负值插值
    val = interpolate(-50, 50, 0.5)
    assert val == 0.0
    
    print("✓ 插值函数测试通过")


def test_interpolate_list():
    """测试列表插值"""
    print("测试列表插值...")
    
    # 三点插值
    val = interpolate_list([0, 50, 100], 0.5)
    assert val == 50.0
    
    # 起始点
    val = interpolate_list([0, 50, 100], 0)
    assert val == 0.0
    
    # 结束点
    val = interpolate_list([0, 50, 100], 1)
    assert val == 100.0
    
    # 单点
    val = interpolate_list([42], 0.5)
    assert val == 42.0
    
    print("✓ 列表插值测试通过")


def test_interpolate_2d():
    """测试二维插值"""
    print("测试二维插值...")
    
    # 基本插值
    point = interpolate_2d((0, 0), (100, 200), 0.5)
    assert point == (50.0, 100.0)
    
    # 缓动插值
    point = interpolate_2d((0, 0), (100, 200), 0.5, 'quad', 'out')
    assert point == (75.0, 150.0)
    
    print("✓ 二维插值测试通过")


def test_interpolate_3d():
    """测试三维插值"""
    print("测试三维插值...")
    
    # 基本插值
    point = interpolate_3d((0, 0, 0), (100, 200, 300), 0.5)
    assert point == (50.0, 100.0, 150.0)
    
    print("✓ 三维插值测试通过")


def test_generate_animation_frames():
    """测试动画帧生成"""
    print("测试动画帧生成...")
    
    # 基本生成
    frames = generate_animation_frames(0, 100, 5)
    assert len(frames) == 5
    assert frames[0] == 0.0
    assert frames[-1] == 100.0
    
    # 缓动生成
    frames = generate_animation_frames(0, 100, 5, 'quad', 'out')
    assert frames[0] == 0.0
    assert frames[-1] == 100.0
    # quad_out: t=0.25 -> ease(0.25, quad, out) = 0.4375 -> 43.75
    assert frames[1] == 43.75  # quad_out 的特性
    
    # 边界情况
    frames = generate_animation_frames(0, 100, 1)
    assert len(frames) == 1
    assert frames[0] == 0.0
    
    frames = generate_animation_frames(0, 100, 0)
    assert len(frames) == 0
    
    print("✓ 动画帧生成测试通过")


def test_generate_animation_frames_2d():
    """测试二维动画帧生成"""
    print("测试二维动画帧生成...")
    
    frames = generate_animation_frames_2d((0, 0), (100, 100), 3)
    assert len(frames) == 3
    assert frames[0] == (0.0, 0.0)
    assert frames[-1] == (100.0, 100.0)
    
    print("✓ 二维动画帧生成测试通过")


def test_chain_easing():
    """测试链式缓动"""
    print("测试链式缓动...")
    
    # 两种缓动组合
    val = chain_easing(0.25, [
        (0.5, 'quad', 'out'),
        (0.5, 'quad', 'in')
    ])
    # 前 50% 用 quad_out
    expected = ease(0.5, 'quad', 'out')  # 0.25 * 2 = 0.5
    assert abs(val - expected) < 0.0001
    
    val = chain_easing(0.75, [
        (0.5, 'quad', 'out'),
        (0.5, 'quad', 'in')
    ])
    # 后 50% 用 quad_in
    expected = ease(0.5, 'quad', 'in')  # (0.75 - 0.5) * 2 = 0.5
    assert abs(val - expected) < 0.0001
    
    print("✓ 链式缓动测试通过")


def test_blend_easing():
    """测试混合缓动"""
    print("测试混合缓动...")
    
    # 50% 混合
    val = blend_easing(0.5, 'quad', 'cubic', 0.5)
    expected = (ease(0.5, 'quad') + ease(0.5, 'cubic')) / 2
    assert abs(val - expected) < 0.0001
    
    # 完全使用第一个
    val = blend_easing(0.5, 'quad', 'cubic', 0.0)
    assert abs(val - ease(0.5, 'quad')) < 0.0001
    
    # 完全使用第二个
    val = blend_easing(0.5, 'quad', 'cubic', 1.0)
    assert abs(val - ease(0.5, 'cubic')) < 0.0001
    
    print("✓ 混合缓动测试通过")


def test_get_easing_derivative():
    """测试导数计算"""
    print("测试导数计算...")
    
    # 线性导数应约为 1
    deriv = get_easing_derivative('linear', 'in', 0.5)
    assert abs(deriv - 1.0) < 0.1
    
    # quad_out 在 t=0 附近导数较大
    deriv_start = get_easing_derivative('quad', 'out', 0.1)
    deriv_end = get_easing_derivative('quad', 'out', 0.9)
    # 结束时变化较慢
    assert deriv_start > deriv_end
    
    print("✓ 导数计算测试通过")


def test_get_easing_extremes():
    """测试极值获取"""
    print("测试极值获取...")
    
    # linear 应在 [0, 1]
    min_val, max_val = get_easing_extremes('linear')
    assert min_val == 0.0
    assert max_val == 1.0
    
    # back 超出范围
    min_val, max_val = get_easing_extremes('back', 'out')
    assert max_val > 1  # 超出
    
    # elastic 超出范围
    min_val, max_val = get_easing_extremes('elastic', 'out')
    assert max_val > 1  # 超出
    
    print("✓ 极值获取测试通过")


def test_compare_easings():
    """测试缓动比较"""
    print("测试缓动比较...")
    
    # 默认比较
    result = compare_easings(0.5)
    assert 'quad_out' in result
    assert 'cubic_out' in result
    
    # 所有值应在 [0, 1] 或略超出（弹性/回弹）
    for name, val in result.items():
        assert -1 <= val <= 2, f"{name} 的值 {val} 超出预期范围"
    
    # 多模式比较
    result = compare_easings(0.5, modes=['in', 'out'])
    assert 'quad_in' in result
    assert 'quad_out' in result
    
    print("✓ 缓动比较测试通过")


def test_create_easing_curve():
    """测试创建缓动曲线"""
    print("测试创建缓动曲线...")
    
    # 基本曲线
    curve = create_easing_curve('quad', 'out', 10)
    assert len(curve) == 11  # 0 到 10 共 11 个点
    assert curve[0] == (0.0, 0.0)
    assert curve[-1] == (1.0, 1.0)
    
    # 验证 x 坐标递增
    for i in range(len(curve) - 1):
        assert curve[i][0] < curve[i + 1][0]
    
    print("✓ 创建缓动曲线测试通过")


def test_apply_easing_to_sequence():
    """测试序列缓动"""
    print("测试序列缓动...")
    
    # 基本序列
    result = apply_easing_to_sequence([0, 10, 20, 30, 40, 50])
    assert len(result) == 6
    
    # 线性应保持不变
    result = apply_easing_to_sequence([0, 10, 20, 30, 40, 50], 'linear')
    for i, val in enumerate(result):
        assert abs(val - (i * 10)) < 0.1
    
    # 单元素
    result = apply_easing_to_sequence([42])
    assert result == [42.0]
    
    # 空列表
    result = apply_easing_to_sequence([])
    assert result == []
    
    print("✓ 序列缓动测试通过")


def test_cubic_bezier():
    """测试三次贝塞尔"""
    print("测试三次贝塞尔...")
    
    # 标准 ease
    ease_fn = cubic_bezier(0.25, 0.1, 0.25, 1.0)
    val = ease_fn(0.5)
    assert 0 < val < 1
    
    # 边界
    assert abs(ease_fn(0) - 0) < 0.01
    assert abs(ease_fn(1) - 1) < 0.01
    
    # linear: (0, 0, 1, 1)
    linear_fn = cubic_bezier(0, 0, 1, 1)
    assert abs(linear_fn(0.5) - 0.5) < 0.1
    
    print("✓ 三次贝塞尔测试通过")


def test_css_easing():
    """测试 CSS 缓动"""
    print("测试 CSS 缓动...")
    
    # 获取标准缓动
    linear_fn = get_css_easing('linear')
    assert linear_fn(0.5) == 0.5
    
    ease_fn = get_css_easing('ease')
    assert 0 < ease_fn(0.5) < 1
    
    # 所有 CSS 缓动
    for name in ['linear', 'ease', 'ease-in', 'ease-out', 'ease-in-out']:
        fn = get_css_easing(name)
        assert abs(fn(0) - 0) < 0.01
        assert abs(fn(1) - 1) < 0.01
    
    # 无效名称
    try:
        get_css_easing('invalid')
        assert False, "应该抛出异常"
    except ValueError:
        pass
    
    print("✓ CSS 缓动测试通过")


def test_clamp():
    """测试 clamp 函数"""
    print("测试 clamp 函数...")
    
    assert clamp(0.5) == 0.5
    assert clamp(-0.5) == 0.0
    assert clamp(1.5) == 1.0
    assert clamp(5, 0, 10) == 5
    assert clamp(-5, 0, 10) == 0
    assert clamp(15, 0, 10) == 10
    
    print("✓ clamp 函数测试通过")


def test_edge_cases():
    """测试边界情况"""
    print("测试边界情况...")
    
    # t < 0
    for fn in [ease_in_quad, ease_out_quad, ease_in_cubic]:
        val = fn(-0.1)
        # 取决于实现，可能 clamp 或保持
    
    # t > 1
    for fn in [ease_in_quad, ease_out_quad, ease_in_cubic]:
        val = fn(1.1)
        # 取决于实现
    
    # elastic 边界
    assert ease_in_elastic(0) == 0
    assert ease_in_elastic(1) == 1
    assert ease_out_elastic(0) == 0
    assert ease_out_elastic(1) == 1
    
    # expo 边界
    assert ease_in_expo(0) == 0
    assert ease_in_expo(1) == 1
    assert ease_out_expo(0) == 0
    assert ease_out_expo(1) == 1
    
    print("✓ 边界情况测试通过")


def test_all_easing_types():
    """测试所有缓动类型"""
    print("测试所有缓动类型...")
    
    for easing_type in EasingType:
        for mode in EasingMode:
            fn = get_easing_function(easing_type, mode)
            # 测试函数可调用
            val = fn(0.5)
            assert isinstance(val, float)
            
            # 测试统一接口
            val2 = ease(0.5, easing_type, mode)
            assert abs(val - val2) < 0.0001
    
    print("✓ 所有缓动类型测试通过")


def test_performance():
    """性能测试"""
    print("测试性能...")
    
    import time
    
    # 大量调用测试
    start = time.time()
    iterations = 10000
    
    for _ in range(iterations):
        ease(0.5, 'quad', 'out')
    
    elapsed = time.time() - start
    print(f"  {iterations} 次 ease() 调用耗时: {elapsed:.4f}s")
    print(f"  平均每次: {elapsed/iterations*1000:.4f}ms")
    
    # 应该在合理时间内完成
    assert elapsed < 1.0, "性能测试失败：耗时过长"
    
    print("✓ 性能测试通过")


def main():
    """运行所有测试"""
    print("=" * 60)
    print("Easing Utilities 测试套件")
    print("=" * 60)
    print()
    
    tests = [
        test_basic_values,
        test_quad_easing,
        test_cubic_easing,
        test_quart_easing,
        test_quint_easing,
        test_sine_easing,
        test_expo_easing,
        test_circ_easing,
        test_elastic_easing,
        test_back_easing,
        test_bounce_easing,
        test_get_easing_function,
        test_ease,
        test_interpolate,
        test_interpolate_list,
        test_interpolate_2d,
        test_interpolate_3d,
        test_generate_animation_frames,
        test_generate_animation_frames_2d,
        test_chain_easing,
        test_blend_easing,
        test_get_easing_derivative,
        test_get_easing_extremes,
        test_compare_easings,
        test_create_easing_curve,
        test_apply_easing_to_sequence,
        test_cubic_bezier,
        test_css_easing,
        test_clamp,
        test_edge_cases,
        test_all_easing_types,
        test_performance,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} 失败: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)