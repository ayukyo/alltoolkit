"""
Histogram Utils 使用示例

演示各种直方图生成和分析场景

作者: AllToolkit 自动生成
日期: 2026-05-02
"""

import sys
sys.path.insert(0, '.')

from histogram_utils import (
    Histogram,
    create_histogram,
    frequency_table,
    ascii_histogram,
    text_histogram,
    generate_sample_data
)


def example_1_basic():
    """示例 1: 基础使用"""
    print("\n" + "=" * 60)
    print("示例 1: 基础直方图创建")
    print("=" * 60)
    
    # 简单数据
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # 创建直方图，指定分组数
    hist = Histogram(data, bins=5)
    
    print(f"\n数据: {data}")
    print(f"分组数: {hist.num_bins}")
    print(f"分组宽度: {hist.bin_width:.2f}")
    
    print("\n分组详情:")
    for bin in hist.bins:
        print(f"  [{bin.lower:.2f}, {bin.upper:.2f}): {bin.count} 个")


def example_2_auto_bins():
    """示例 2: 自动分组"""
    print("\n" + "=" * 60)
    print("示例 2: 自动分组计算")
    print("=" * 60)
    
    # 生成正态分布数据
    data = generate_sample_data(1000, 'normal', mean=50, std_dev=15)
    
    # 使用 Sturges 规则自动分组
    hist = Histogram(data)
    
    print(f"\n数据量: {len(data)}")
    print(f"自动分组数: {hist.num_bins} (Sturges 规则)")
    
    # 显示简化的直方图
    print("\n直方图 (前5组):")
    for i, bin in enumerate(hist.bins[:5]):
        bar = '█' * (bin.count // 10)
        print(f"  [{bin.lower:.1f}, {bin.upper:.1f}): {bin.count:4} | {bar}")


def example_3_statistics():
    """示例 3: 统计分析"""
    print("\n" + "=" * 60)
    print("示例 3: 统计分析")
    print("=" * 60)
    
    # 学生成绩数据
    scores = [85, 92, 78, 90, 88, 75, 82, 95, 89, 91, 
              80, 87, 83, 94, 79, 86, 81, 93, 77, 84]
    
    hist = Histogram(scores, bins=5)
    stats = hist.statistics()
    
    print(f"\n学生成绩分析 (n={stats['count']})")
    print(f"  最高分: {stats['max']}")
    print(f"  最低分: {stats['min']}")
    print(f"  平均分: {stats['mean']:.2f}")
    print(f"  中位数: {stats['median']:.2f}")
    print(f"  标准差: {stats['std_dev']:.2f}")
    print(f"  方差:   {stats['variance']:.2f}")
    
    print("\n成绩分布:")
    for bin in hist.bins:
        print(f"  {bin.lower:.0f}-{bin.upper:.0f}分: {bin.count} 人")


def example_4_cumulative():
    """示例 4: 累积频率"""
    print("\n" + "=" * 60)
    print("示例 4: 累积频率分析")
    print("=" * 60)
    
    # 产品重量数据
    weights = [100, 102, 105, 108, 110, 112, 115, 118, 120,
               101, 103, 106, 109, 111, 113, 116, 119, 121]
    
    hist = Histogram(weights, bins=6)
    
    print(f"\n产品重量分布 (单位: 克)")
    print("\n分组 | 计数 | 累积计数 | 累积频率")
    print("-" * 45)
    
    cum_counts = hist.cumulative_counts()
    cum_freqs = hist.cumulative_frequencies()
    
    for i, bin in enumerate(hist.bins):
        print(f"{bin.lower:.0f}-{bin.upper:.0f}g | {bin.count:3} | {cum_counts[i]:4} | {cum_freqs[i]*100:.1f}%")
    
    print(f"\n解读: {cum_freqs[-1]*100:.1f}% 的产品重量在 {hist.min_val:.0f}-{hist.max_val:.0f}g 范围内")


def example_5_custom_range():
    """示例 5: 自定义范围"""
    print("\n" + "=" * 60)
    print("示例 5: 自定义范围")
    print("=" * 60)
    
    # 实际数据范围 5-15
    data = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    
    # 自定义范围 0-20
    hist1 = Histogram(data, bins=10, range_min=0, range_max=20)
    
    # 使用实际数据范围
    hist2 = Histogram(data, bins=10)
    
    print(f"\n数据范围: 5-15")
    print(f"\n直方图 1 (自定义范围 0-20):")
    print(f"  分组宽度: {hist1.bin_width:.2f}")
    print(f"  空分组数: {sum(1 for b in hist1.bins if b.count == 0)}")
    
    print(f"\n直方图 2 (实际数据范围 5-15):")
    print(f"  分组宽度: {hist2.bin_width:.2f}")
    print(f"  空分组数: {sum(1 for b in hist2.bins if b.count == 0)}")


def example_6_bin_width():
    """示例 6: 指定分组宽度"""
    print("\n" + "=" * 60)
    print("示例 6: 指定分组宽度")
    print("=" * 60)
    
    # 年龄数据
    ages = [18, 22, 25, 28, 30, 35, 40, 45, 50, 55,
            20, 24, 27, 32, 38, 42, 48, 52, 58, 60]
    
    # 每 10 岁一组
    hist = Histogram(ages, bin_width=10)
    
    print(f"\n年龄分布 (按 10 岁分组)")
    print(f"数据范围: {hist.min_val}-{hist.max_val}")
    print(f"分组数: {hist.num_bins}")
    
    for bin in hist.bins:
        print(f"  {int(bin.lower)}-{int(bin.upper)}岁: {bin.count} 人")


def example_7_text_report():
    """示例 7: 完整文本报告"""
    print("\n" + "=" * 60)
    print("示例 7: 完整文本报告")
    print("=" * 60)
    
    # 生成模拟考试数据
    scores = generate_sample_data(50, 'normal', mean=75, std_dev=10)
    
    # 确保分数在 0-100 范围
    scores = [max(0, min(100, s)) for s in scores]
    
    hist = Histogram(scores, bins=10)
    
    print(hist.to_text())


def example_8_ascii_chart():
    """示例 8: ASCII 图表"""
    print("\n" + "=" * 60)
    print("示例 8: ASCII 直方图")
    print("=" * 60)
    
    # 生成数据
    data = generate_sample_data(200, 'normal', mean=50, std_dev=10)
    
    hist = Histogram(data, bins=10)
    
    print(hist.to_ascii_chart(height=8, width=40))


def example_9_dict_output():
    """示例 9: 字典输出"""
    print("\n" + "=" * 60)
    print("示例 9: 字典输出 (用于数据处理)")
    print("=" * 60)
    
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    hist = Histogram(data, bins=5)
    
    result = hist.to_dict()
    
    print(f"\n配置:")
    print(f"  分组数: {result['config']['num_bins']}")
    print(f"  分组宽度: {result['config']['bin_width']}")
    print(f"  范围: {result['config']['range']}")
    
    print(f"\n分组数据 (JSON 格式):")
    import json
    print(json.dumps(result['bins'], indent=2))


def example_10_distribution_comparison():
    """示例 10: 不同分布比较"""
    print("\n" + "=" * 60)
    print("示例 10: 不同分布比较")
    print("=" * 60)
    
    n = 500
    
    # 正态分布
    normal_data = generate_sample_data(n, 'normal', mean=50, std_dev=15)
    hist_normal = Histogram(normal_data, bins=10)
    
    # 均匀分布
    uniform_data = generate_sample_data(n, 'uniform', mean=50)
    hist_uniform = Histogram(uniform_data, bins=10)
    
    # 指数分布
    exp_data = generate_sample_data(n, 'exponential', mean=5)
    hist_exp = Histogram(exp_data, bins=10)
    
    print(f"\n正态分布 (μ=50, σ=15):")
    print(f"  实际均值: {hist_normal.statistics()['mean']:.2f}")
    print(f"  实际标准差: {hist_normal.statistics()['std_dev']:.2f}")
    print(f"  分布形状: 中间高，两边低 (钟形)")
    
    print(f"\n均匀分布 (range=0-100):")
    print(f"  实际均值: {hist_uniform.statistics()['mean']:.2f}")
    print(f"  实际标准差: {hist_uniform.statistics()['std_dev']:.2f}")
    print(f"  分布形状: 各分组计数相近")
    
    print(f"\n指数分布 (λ=0.2):")
    print(f"  实际均值: {hist_exp.statistics()['mean']:.2f}")
    print(f"  实际标准差: {hist_exp.statistics()['std_dev']:.2f}")
    print(f"  分布形状: 左侧高，右侧低")


def main():
    """运行所有示例"""
    print("Histogram Utils 使用示例集")
    print("=" * 60)
    
    examples = [
        example_1_basic,
        example_2_auto_bins,
        example_3_statistics,
        example_4_cumulative,
        example_5_custom_range,
        example_6_bin_width,
        example_7_text_report,
        example_8_ascii_chart,
        example_9_dict_output,
        example_10_distribution_comparison,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n示例执行出错: {e}")
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()