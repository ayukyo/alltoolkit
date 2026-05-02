"""
Histogram Utils 测试文件

测试内容:
- 基础直方图创建
- 自动分组计算
- 手动分组设置
- 频率/密度计算
- 累积频率
- 统计信息
- 输出格式化
- 边界情况处理

作者: AllToolkit 自动生成
日期: 2026-05-02
"""

import sys
import math
sys.path.insert(0, '.')

from histogram_utils import (
    Histogram, HistogramBin,
    create_histogram, frequency_table,
    ascii_histogram, text_histogram,
    generate_sample_data
)


def test_basic_histogram():
    """测试基础直方图创建"""
    print("测试 1: 基础直方图创建")
    
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    hist = Histogram(data, bins=5)
    
    # 验证分组数量
    assert hist.num_bins == 5, f"分组数量应为 5, 实际为 {hist.num_bins}"
    
    # 验证范围
    assert hist.min_val == 1, f"最小值应为 1, 实际为 {hist.min_val}"
    assert hist.max_val == 10, f"最大值应为 10, 实际为 {hist.max_val}"
    
    # 验证总计数
    total = sum(bin.count for bin in hist.bins)
    assert total == 10, f"总计数应为 10, 实际为 {total}"
    
    print("  ✓ 基础直方图创建成功")


def test_auto_bins():
    """测试自动分组计算"""
    print("测试 2: 自动分组计算 (Sturges 规则)")
    
    # 100 个数据点，Sturges 规则: 1 + 3.322 * log10(100) ≈ 8
    data = list(range(1, 101))
    hist = Histogram(data)  # 不指定 bins
    
    expected_bins = int(math.ceil(1 + 3.322 * math.log10(100)))
    assert hist.num_bins == expected_bins, \
        f"自动分组数应为 {expected_bins}, 实际为 {hist.num_bins}"
    
    print(f"  ✓ 自动分组计算成功: {hist.num_bins} 组")


def test_manual_bin_width():
    """测试手动分组宽度"""
    print("测试 3: 手动分组宽度")
    
    data = [0, 5, 10, 15, 20, 25, 30]
    hist = Histogram(data, bin_width=10)
    
    # 范围 0-30, 宽度 10, 应有 3 组
    assert hist.num_bins == 3, f"分组数应为 3, 实际为 {hist.num_bins}"
    assert hist.bin_width == 10, f"分组宽度应为 10, 实际为 {hist.bin_width}"
    
    print("  ✓ 手动分组宽度设置成功")


def test_frequencies():
    """测试频率计算"""
    print("测试 4: 频率计算")
    
    data = [1, 1, 1, 2, 2, 3]  # 6 个数据点
    hist = Histogram(data, bins=3)
    
    frequencies = hist.frequencies()
    total_freq = sum(frequencies)
    
    assert abs(total_freq - 1.0) < 0.001, f"频率总和应为 1.0, 实际为 {total_freq}"
    
    # 验证每个频率在 0-1 范围内
    for freq in frequencies:
        assert 0 <= freq <= 1, f"频率 {freq} 超出范围"
    
    print(f"  ✓ 频率计算成功: {frequencies}")


def test_densities():
    """测试密度计算"""
    print("测试 5: 密度计算")
    
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    hist = Histogram(data, bins=5)
    
    densities = hist.densities()
    
    # 验证密度总和等于 1/bin_width (面积 = 1)
    area = sum(d * hist.bin_width for d in densities)
    assert abs(area - 1.0) < 0.01, f"密度面积应为 1.0, 实际为 {area}"
    
    print(f"  ✓ 密度计算成功, 面积: {area:.4f}")


def test_cumulative():
    """测试累积频率"""
    print("测试 6: 累积频率")
    
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    hist = Histogram(data, bins=5)
    
    cum_counts = hist.cumulative_counts()
    cum_freqs = hist.cumulative_frequencies()
    
    # 验证累积计数递增
    for i in range(1, len(cum_counts)):
        assert cum_counts[i] >= cum_counts[i-1], \
            f"累积计数应递增: {cum_counts}"
    
    # 验证最终累积频率为 1
    assert abs(cum_freqs[-1] - 1.0) < 0.01, \
        f"最终累积频率应为 1.0, 实际为 {cum_freqs[-1]}"
    
    print(f"  ✓ 累积频率计算成功: 最终 = {cum_freqs[-1]}")


def test_statistics():
    """测试统计信息"""
    print("测试 7: 统计信息")
    
    data = [1, 2, 3, 4, 5]
    hist = Histogram(data, bins=5)
    
    stats = hist.statistics()
    
    # 验证均值
    expected_mean = 3.0
    assert abs(stats['mean'] - expected_mean) < 0.01, \
        f"均值应为 {expected_mean}, 实际为 {stats['mean']}"
    
    # 验证中位数
    expected_median = 3.0
    assert abs(stats['median'] - expected_median) < 0.01, \
        f"中位数应为 {expected_median}, 实际为 {stats['median']}"
    
    # 验证计数
    assert stats['count'] == 5, f"计数应为 5, 实际为 {stats['count']}"
    
    print(f"  ✓ 统计信息正确: mean={stats['mean']}, median={stats['median']}")


def test_to_dict():
    """测试字典输出"""
    print("测试 8: 字典输出")
    
    data = [1, 2, 3, 4, 5]
    hist = Histogram(data, bins=3)
    
    result = hist.to_dict()
    
    # 验证结构
    assert 'bins' in result, "缺少 bins 字段"
    assert 'statistics' in result, "缺少 statistics 字段"
    assert 'config' in result, "缺少 config 字段"
    
    # 验证 bins 数据
    assert len(result['bins']) == 3, f"bins 数量应为 3"
    
    for bin_data in result['bins']:
        assert 'lower' in bin_data, "缺少 lower"
        assert 'upper' in bin_data, "缺少 upper"
        assert 'count' in bin_data, "缺少 count"
    
    print("  ✓ 字典输出格式正确")


def test_text_output():
    """测试文本输出"""
    print("测试 9: 文本输出")
    
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    hist = Histogram(data, bins=5)
    
    text = hist.to_text()
    
    # 验证包含关键信息
    assert "直方图统计报告" in text, "缺少标题"
    assert "数据统计" in text, "缺少统计信息"
    assert "分组数量" in text, "缺少分组信息"
    assert "█" in text, "缺少柱状图"
    
    print("  ✓ 文本输出格式正确")


def test_ascii_chart():
    """测试 ASCII 图输出"""
    print("测试 10: ASCII 图输出")
    
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    hist = Histogram(data, bins=5)
    
    chart = hist.to_ascii_chart(height=5, width=20)
    
    # 验证包含关键元素
    assert "│" in chart, "缺少分隔符"
    assert "└" in chart, "缺少 X轴"
    assert "█" in chart, "缺少柱状图符号"
    
    print("  ✓ ASCII 图输出格式正确")


def test_edge_cases():
    """测试边界情况"""
    print("测试 11: 边界情况")
    
    # 单一数据点
    hist1 = Histogram([5.0], bins=1)
    assert hist1.num_bins >= 1, "单一数据点应至少有 1 个分组"
    print("  ✓ 单一数据点处理正确")
    
    # 所有数据相同
    hist2 = Histogram([5, 5, 5, 5], bins=3)
    total = sum(bin.count for bin in hist2.bins)
    assert total == 4, "相同数据计数应正确"
    print("  ✓ 相同数据处理正确")
    
    # 范围边界值
    data = [0, 10]
    hist3 = Histogram(data, bins=2)
    assert hist3.min_val == 0, "最小值应为 0"
    assert hist3.max_val == 10, "最大值应为 10"
    print("  ✓ 范围边界处理正确")


def test_custom_range():
    """测试自定义范围"""
    print("测试 12: 自定义范围")
    
    data = [3, 4, 5, 6, 7]
    hist = Histogram(data, bins=5, range_min=0, range_max=10)
    
    assert hist.min_val == 0, f"自定义最小值应为 0, 实际为 {hist.min_val}"
    assert hist.max_val == 10, f"自定义最大值应为 10, 实际为 {hist.max_val}"
    
    print("  ✓ 自定义范围设置成功")


def test_sample_data_generation():
    """测试示例数据生成"""
    print("测试 13: 示例数据生成")
    
    # 正态分布
    normal_data = generate_sample_data(100, 'normal', mean=50, std_dev=10)
    assert len(normal_data) == 100, f"应生成 100 个数据, 实际 {len(normal_data)}"
    
    # 验证均值接近设定值
    avg = sum(normal_data) / len(normal_data)
    assert abs(avg - 50) < 15, f"正态分布均值偏离过大: {avg}"
    print(f"  ✓ 正态分布生成成功, 均值≈{avg:.2f}")
    
    # 均匀分布
    uniform_data = generate_sample_data(100, 'uniform', mean=50)
    assert len(uniform_data) == 100
    avg = sum(uniform_data) / len(uniform_data)
    assert abs(avg - 50) < 20, f"均匀分布均值偏离过大: {avg}"
    print(f"  ✓ 均匀分布生成成功, 均值≈{avg:.2f}")
    
    # 指数分布
    exp_data = generate_sample_data(100, 'exponential', mean=5)
    assert len(exp_data) == 100
    print(f"  ✓ 指数分布生成成功, 数量={len(exp_data)}")


def test_convenience_functions():
    """测试便捷函数"""
    print("测试 14: 便捷函数")
    
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # create_histogram
    hist = create_histogram(data, bins=5)
    assert hist.num_bins == 5
    print("  ✓ create_histogram 成功")
    
    # frequency_table
    table = frequency_table(data, bins=5)
    assert len(table) == 5
    assert all(isinstance(t, tuple) and len(t) == 3 for t in table)
    print("  ✓ frequency_table 成功")
    
    # ascii_histogram
    chart = ascii_histogram(data, bins=5)
    assert "█" in chart
    print("  ✓ ascii_histogram 成功")
    
    # text_histogram
    text = text_histogram(data, bins=5)
    assert "直方图" in text
    print("  ✓ text_histogram 成功")


def test_empty_data_error():
    """测试空数据错误处理"""
    print("测试 15: 空数据错误处理")
    
    try:
        Histogram([], bins=5)
        print("  ✗ 应抛出 ValueError")
        assert False
    except ValueError as e:
        assert "不能为空" in str(e)
        print("  ✓ 空数据正确抛出错误")


def test_histogram_bin():
    """测试 HistogramBin 类"""
    print("测试 16: HistogramBin 类")
    
    bin = HistogramBin(0, 10, 5)
    
    assert bin.lower == 0, "lower 应为 0"
    assert bin.upper == 10, "upper 应为 10"
    assert bin.count == 5, "count 应为 5"
    assert bin.width == 10, "width 应为 10"
    assert bin.midpoint == 5, "midpoint 应为 5"
    
    print("  ✓ HistogramBin 类属性正确")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Histogram Utils 测试套件")
    print("=" * 60)
    print()
    
    tests = [
        test_basic_histogram,
        test_auto_bins,
        test_manual_bin_width,
        test_frequencies,
        test_densities,
        test_cumulative,
        test_statistics,
        test_to_dict,
        test_text_output,
        test_ascii_chart,
        test_edge_cases,
        test_custom_range,
        test_sample_data_generation,
        test_convenience_functions,
        test_empty_data_error,
        test_histogram_bin,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ 测试失败: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ 异常: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)