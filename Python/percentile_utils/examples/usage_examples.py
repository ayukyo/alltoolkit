"""
百分位数工具使用示例

演示 percentile_utils 模块的主要功能和使用方法
"""

from mod import (
    percentile,
    quartiles,
    percentile_rank,
    boxplot_stats,
    deciles,
    percentiles,
    grouped_percentile,
    percentile_summary,
    is_outlier,
    normalize_by_percentile,
    winsorize,
    InterpolationMethod
)


def example_basic_percentile():
    """示例1: 基本百分位数计算"""
    print("=" * 60)
    print("示例1: 基本百分位数计算")
    print("=" * 60)
    
    data = [15, 20, 35, 40, 50, 55, 60, 70, 85, 95]
    
    print(f"数据集: {data}")
    print(f"\n基本百分位数:")
    print(f"  P10 (第10百分位数): {percentile(data, 10)}")
    print(f"  P25 (第25百分位数/下四分位数): {percentile(data, 25)}")
    print(f"  P50 (第50百分位数/中位数): {percentile(data, 50)}")
    print(f"  P75 (第75百分位数/上四分位数): {percentile(data, 75)}")
    print(f"  P90 (第90百分位数): {percentile(data, 90)}")
    print()


def example_interpolation_methods():
    """示例2: 不同插值方法"""
    print("=" * 60)
    print("示例2: 不同插值方法对比")
    print("=" * 60)
    
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    p = 25
    
    print(f"数据集: {data}")
    print(f"计算 P{p}:\n")
    
    methods = [
        (InterpolationMethod.LINEAR, "线性插值 (默认, numpy风格)"),
        (InterpolationMethod.LOWER, "下界值 (取小于等于的最近值)"),
        (InterpolationMethod.HIGHER, "上界值 (取大于等于的最近值)"),
        (InterpolationMethod.NEAREST, "最近邻 (四舍五入)"),
        (InterpolationMethod.MIDPOINT, "中点值 (上下界平均)"),
        (InterpolationMethod.INCLUSIVE, "包含法 (Excel PERCENTILE.INC)"),
    ]
    
    for method, description in methods:
        result = percentile(data, p, method)
        print(f"  {method.value:10s}: {result:6.2f} - {description}")
    
    print("\n注意: exclusive 方法需要数据量较大，这里不做演示")
    print()


def example_quartiles():
    """示例3: 四分位数和 IQR"""
    print("=" * 60)
    print("示例3: 四分位数和四分位距 (IQR)")
    print("=" * 60)
    
    data = [12, 15, 17, 20, 24, 28, 30, 33, 37, 40, 45, 50, 55, 60, 65]
    
    print(f"数据集: {data}")
    
    qs = quartiles(data)
    
    print(f"\n四分位数统计:")
    print(f"  Q1 (下四分位数, P25): {qs['Q1']}")
    print(f"  Q2 (中位数, P50):     {qs['Q2']}")
    print(f"  Q3 (上四分位数, P75): {qs['Q3']}")
    print(f"  IQR (四分位距):       {qs['IQR']}")
    print(f"\n解读: 50% 的数据落在 {qs['Q1']} 到 {qs['Q3']} 之间")
    print()


def example_boxplot():
    """示例4: 箱线图统计"""
    print("=" * 60)
    print("示例4: 箱线图统计分析")
    print("=" * 60)
    
    # 正常数据 + 异常值
    data = [10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 
            26, 27, 28, 29, 30, 5, 50, 80]  # 后三个是异常值
    
    print(f"数据集: {data}")
    
    stats = boxplot_stats(data)
    
    print(f"\n箱线图统计:")
    print(f"  最小值:           {stats['min']}")
    print(f"  下四分位数 (Q1):  {stats['Q1']}")
    print(f"  中位数:           {stats['median']}")
    print(f"  上四分位数 (Q3):  {stats['Q3']}")
    print(f"  最大值:           {stats['max']}")
    print(f"  四分位距 (IQR):   {stats['IQR']}")
    print(f"  下须长:           {stats['lower_whisker']}")
    print(f"  上须长:           {stats['upper_whisker']}")
    print(f"  异常值下界:       {stats['lower_bound']:.2f}")
    print(f"  异常值上界:       {stats['upper_bound']:.2f}")
    print(f"  检测到的异常值:   {stats['outliers']}")
    print()


def example_percentile_rank():
    """示例5: 百分位排名"""
    print("=" * 60)
    print("示例5: 百分位排名计算")
    print("=" * 60)
    
    # 模拟考试分数
    scores = [55, 60, 65, 70, 72, 75, 78, 80, 82, 85, 88, 90, 92, 95, 98]
    
    print(f"考试分数分布: {scores}")
    print(f"\n分数排名查询:")
    
    test_scores = [65, 75, 85, 95]
    for score in test_scores:
        rank = percentile_rank(scores, score)
        print(f"  分数 {score:2d} 的百分位排名: {rank:5.1f}% (超过 {rank:.0f}% 的学生)")
    print()


def example_deciles():
    """示例6: 十分位数"""
    print("=" * 60)
    print("示例6: 十分位数划分")
    print("=" * 60)
    
    data = list(range(1, 101))  # 1-100
    
    print(f"数据集: 1 到 100 的整数")
    
    decs = deciles(data)
    
    print(f"\n十分位数 (将数据分为 10 等份):")
    for i, val in enumerate(decs):
        percentile_label = f"P{i * 10}"
        print(f"  D{i} = {percentile_label:4s} = {val:5.1f}")
    print()


def example_batch_percentiles():
    """示例7: 批量计算百分位数"""
    print("=" * 60)
    print("示例7: 批量百分位数计算")
    print("=" * 60)
    
    import random
    data = [random.randint(1, 1000) for _ in range(100)]
    data.sort()
    
    print(f"生成 100 个 1-1000 的随机数")
    
    # 计算常用百分位数
    percentile_list = [1, 5, 10, 25, 50, 75, 90, 95, 99]
    results = percentiles(data, percentile_list)
    
    print(f"\n批量百分位数结果:")
    for p in percentile_list:
        print(f"  P{p:2d} = {results[p]:6.1f}")
    print()


def example_grouped():
    """示例8: 分组百分位数"""
    print("=" * 60)
    print("示例8: 分组数据百分位数对比")
    print("=" * 60)
    
    # 模拟三个班级的成绩
    classes = {
        'A班': [85, 90, 88, 92, 87, 95, 89, 91, 86, 93],
        'B班': [70, 75, 72, 78, 80, 75, 77, 73, 79, 76],
        'C班': [60, 65, 62, 68, 70, 72, 65, 67, 63, 69]
    }
    
    print("三个班级的成绩分布:")
    for class_name, scores in classes.items():
        print(f"  {class_name}: {scores}")
    
    print(f"\n各班级 P50 (中位数) 对比:")
    results = grouped_percentile(classes, 50)
    for class_name, p50 in sorted(results.items(), key=lambda x: x[1], reverse=True):
        print(f"  {class_name}: {p50:.1f}")
    
    print(f"\n各班级 P75 (前25%门槛) 对比:")
    results = grouped_percentile(classes, 75)
    for class_name, p75 in sorted(results.items(), key=lambda x: x[1], reverse=True):
        print(f"  {class_name}: {p75:.1f}")
    print()


def example_summary():
    """示例9: 完整统计摘要"""
    print("=" * 60)
    print("示例9: 完整百分位数统计摘要")
    print("=" * 60)
    
    import random
    data = [random.gauss(100, 15) for _ in range(50)]  # 正态分布
    
    summary = percentile_summary(data)
    
    print(f"生成 50 个正态分布随机数 (均值=100, 标准差=15)")
    
    print(f"\n基本统计:")
    print(f"  样本数量:  {summary['count']}")
    print(f"  总和:      {summary['sum']:.2f}")
    print(f"  均值:      {summary['mean']:.2f}")
    print(f"  标准差:    {summary['std_dev']:.2f}")
    print(f"  方差:      {summary['variance']:.2f}")
    print(f"  范围:      {summary['range']:.2f}")
    print(f"  最小值:    {summary['min']:.2f}")
    print(f"  最大值:    {summary['max']:.2f}")
    
    print(f"\n四分位数:")
    print(f"  Q1 (25%): {summary['quartiles']['Q1']:.2f}")
    print(f"  Q2 (50%): {summary['quartiles']['Q2']:.2f}")
    print(f"  Q3 (75%): {summary['quartiles']['Q3']:.2f}")
    print(f"  IQR:      {summary['quartiles']['IQR']:.2f}")
    
    print(f"\n常用百分位数:")
    for p in [5, 10, 25, 50, 75, 90, 95]:
        print(f"  P{p:2d}: {summary['percentiles'][p]:.2f}")
    print()


def example_outlier_detection():
    """示例10: 异常值检测"""
    print("=" * 60)
    print("示例10: 异常值检测应用")
    print("=" * 60)
    
    # 模拟传感器读数
    sensor_data = [20.1, 20.3, 20.2, 20.4, 20.5, 20.3, 20.2, 
                   20.4, 20.3, 20.5, 35.0, 20.2, 20.3, 5.0]
    
    print(f"传感器读数: {sensor_data}")
    
    print(f"\n异常值检测结果 (1.5 × IQR 规则):")
    outliers = []
    for value in sensor_data:
        if is_outlier(value, sensor_data):
            outliers.append(value)
            print(f"  值 {value:5.1f} - 异常!")
        else:
            print(f"  值 {value:5.1f} - 正常")
    
    print(f"\n检测到的异常值: {outliers}")
    print()


def example_normalize():
    """示例11: 基于百分位数的归一化"""
    print("=" * 60)
    print("示例11: 基于百分位数的归一化")
    print("=" * 60)
    
    data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 1000]  # 含异常值
    
    print(f"原始数据: {data}")
    
    # 使用 Q1-Q3 范围归一化
    normalized = normalize_by_percentile(data, 25, 75)
    
    print(f"\n归一化后 (Q1-Q3 范围):")
    for original, norm in zip(data, normalized):
        print(f"  {original:4d} -> {norm:7.2f}")
    print()


def example_winsorize():
    """示例12: 缩尾处理"""
    print("=" * 60)
    print("示例12: 缩尾处理 (Winsorization)")
    print("=" * 60)
    
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100, 200, -50]
    
    print(f"原始数据: {data}")
    
    # 将低于 5% 和高于 95% 的值缩尾
    winsorized = winsorize(data, 5, 95)
    
    print(f"\n缩尾处理后 (P5-P95):")
    for original, win in zip(data, winsorized):
        if original != win:
            print(f"  {original:4d} -> {win:7.2f} (已缩尾)")
        else:
            print(f"  {original:4d} -> {win:7.2f}")
    print()


def example_performance_tips():
    """示例13: 性能优化技巧"""
    print("=" * 60)
    print("示例13: 性能优化技巧")
    print("=" * 60)
    
    import time
    import random
    
    # 生成大数据集
    data = [random.random() * 1000 for _ in range(100000)]
    
    print(f"数据集大小: {len(data)} 个随机数")
    
    # 方法1: 重复排序
    start = time.time()
    p1 = percentile(data, 25)
    p2 = percentile(data, 50)
    p3 = percentile(data, 75)
    time_unsorted = time.time() - start
    
    # 方法2: 预排序后复用
    start = time.time()
    sorted_data = sorted(data)
    p1 = percentile(sorted_data, 25, sorted_data=True)
    p2 = percentile(sorted_data, 50, sorted_data=True)
    p3 = percentile(sorted_data, 75, sorted_data=True)
    time_sorted = time.time() - start
    
    # 方法3: 使用批量计算
    start = time.time()
    results = percentiles(data, [25, 50, 75])
    time_batch = time.time() - start
    
    print(f"\n计算 P25, P50, P75 的时间对比:")
    print(f"  未优化 (重复排序): {time_unsorted:.4f} 秒")
    print(f"  预排序优化:        {time_sorted:.4f} 秒")
    print(f"  批量计算:          {time_batch:.4f} 秒")
    print(f"\n建议: 对于大数据集，使用 sorted_data=True 或批量计算函数")
    print()


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("百分位数工具模块 (percentile_utils) 使用示例")
    print("=" * 60 + "\n")
    
    example_basic_percentile()
    example_interpolation_methods()
    example_quartiles()
    example_boxplot()
    example_percentile_rank()
    example_deciles()
    example_batch_percentiles()
    example_grouped()
    example_summary()
    example_outlier_detection()
    example_normalize()
    example_winsorize()
    example_performance_tips()
    
    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()