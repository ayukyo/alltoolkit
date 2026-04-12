#!/usr/bin/env python3
"""
AllToolkit - Statistics Utils Demo

演示 statistics_utils 模块的各种功能。
运行：python examples/demo.py
"""

import sys
import os

# Add module to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    # 描述性统计
    mean, median, mode, variance, std_dev, quartiles, iqr,
    percentile, skewness, kurtosis, describe, summary,
    
    # 相关性与回归
    correlation, linear_regression, predict,
    
    # 标准化
    standardize, normalize_minmax,
    
    # 异常值检测
    detect_outliers_iqr, remove_outliers,
)


def print_section(title):
    """打印章节标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def demo_descriptive_statistics():
    """演示描述性统计"""
    print_section("描述性统计")
    
    # 示例数据：某班级 10 名学生的数学成绩
    scores = [78, 85, 92, 88, 76, 95, 89, 82, 91, 87]
    
    print(f"\n数据：{scores}")
    print(f"\n基础统计:")
    print(f"  均值 (Mean):     {mean(scores):.2f}")
    print(f"  中位数 (Median): {median(scores)}")
    print(f"  众数 (Mode):     {mode(scores)}")
    print(f"  方差 (Variance): {variance(scores):.2f}")
    print(f"  标准差 (Std Dev): {std_dev(scores):.2f}")
    
    q1, q2, q3 = quartiles(scores)
    print(f"\n分位数:")
    print(f"  Q1 (25%): {q1}")
    print(f"  Q2 (50%/中位数): {q2}")
    print(f"  Q3 (75%): {q3}")
    print(f"  IQR: {iqr(scores)}")
    
    print(f"\n百分位数:")
    print(f"  P10: {percentile(scores, 10):.2f}")
    print(f"  P90: {percentile(scores, 90):.2f}")
    
    print(f"\n分布特征:")
    print(f"  偏度 (Skewness):   {skewness(scores):.4f}")
    print(f"  峰度 (Kurtosis):   {kurtosis(scores):.4f}")
    
    print(f"\n综合统计报告:")
    print(summary(scores))


def demo_correlation_regression():
    """演示相关性与回归分析"""
    print_section("相关性与回归分析")
    
    # 示例数据：广告投入与销售额
    ad_spend = [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500]
    sales = [8000, 12000, 15000, 18000, 22000, 25000, 28000, 32000, 35000, 38000]
    
    print(f"\n广告投入 (千元): {ad_spend}")
    print(f"销售额 (千元):   {sales}")
    
    # 相关性
    corr = correlation(ad_spend, sales)
    print(f"\n皮尔逊相关系数：{corr:.4f}")
    print(f"解释：{'强正相关' if corr > 0.8 else '中等相关' if corr > 0.5 else '弱相关'}")
    
    # 线性回归
    reg = linear_regression(ad_spend, sales)
    print(f"\n线性回归结果:")
    print(f"  斜率 (Slope):     {reg['slope']:.4f}")
    print(f"  截距 (Intercept): {reg['intercept']:.2f}")
    print(f"  R²:              {reg['r_squared']:.4f}")
    print(f"  标准误差：        {reg['std_error']:.2f}")
    
    print(f"\n回归方程：销售额 = {reg['slope']:.4f} × 广告投入 + {reg['intercept']:.2f}")
    
    # 预测
    test_ad_spend = 6000
    predicted_sales = predict(reg, test_ad_spend)
    print(f"\n预测：广告投入 {test_ad_spend} 千元时，预计销售额为 {predicted_sales:.2f} 千元")


def demo_normalization():
    """演示数据标准化"""
    print_section("数据标准化")
    
    # 示例数据：不同量纲的特征
    height = [160, 165, 170, 175, 180, 185]  # cm
    weight = [55, 60, 65, 70, 75, 80]        # kg
    age = [20, 25, 30, 35, 40, 45]           # years
    
    print(f"\n原始数据:")
    print(f"  身高 (cm): {height}")
    print(f"  体重 (kg): {weight}")
    print(f"  年龄 (岁): {age}")
    
    # Z-score 标准化
    height_z = standardize(height)
    weight_z = standardize(weight)
    
    print(f"\nZ-score 标准化 (均值=0, 标准差=1):")
    print(f"  身高：{[f'{x:.3f}' for x in height_z]}")
    print(f"  体重：{[f'{x:.3f}' for x in weight_z]}")
    
    # Min-Max 归一化
    height_norm = normalize_minmax(height)
    print(f"\nMin-Max 归一化 [0, 1]:")
    print(f"  身高：{[f'{x:.3f}' for x in height_norm]}")
    
    # 自定义范围
    height_scaled = normalize_minmax(height, new_min=-1, new_max=1)
    print(f"\nMin-Max 归一化 [-1, 1]:")
    print(f"  身高：{[f'{x:.3f}' for x in height_scaled]}")


def demo_outlier_detection():
    """演示异常值检测"""
    print_section("异常值检测")
    
    # 示例数据：包含异常值的销售记录
    daily_sales = [1200, 1350, 1280, 1420, 1380, 15000, 1320, 1290, 1410, 1360]
    
    print(f"\n原始数据：{daily_sales}")
    print(f"\n原始统计:")
    print(summary(daily_sales))
    
    # IQR 方法检测
    outliers_iqr = detect_outliers_iqr(daily_sales)
    print(f"\nIQR 方法检测到的异常值:")
    for idx, val in outliers_iqr:
        print(f"  索引 {idx}: {val}")
    
    # 移除异常值
    clean_sales = remove_outliers(daily_sales, method='iqr')
    print(f"\n清理后数据：{clean_sales}")
    print(f"\n清理后统计:")
    print(summary(clean_sales))


def demo_real_world_analysis():
    """演示实际场景分析"""
    print_section("实际场景：A/B 测试分析")
    
    # A/B 测试数据：两组用户的转化率
    group_a = [0.12, 0.15, 0.14, 0.13, 0.16, 0.14, 0.15, 0.13, 0.14, 0.15]
    group_b = [0.18, 0.20, 0.19, 0.21, 0.17, 0.19, 0.20, 0.18, 0.19, 0.20]
    
    print(f"\nA 组转化率：{group_a}")
    print(f"B 组转化率：{group_b}")
    
    print(f"\nA 组统计:")
    print(f"  均值：{mean(group_a):.4f}")
    print(f"  标准差：{std_dev(group_a):.4f}")
    
    print(f"\nB 组统计:")
    print(f"  均值：{mean(group_b):.4f}")
    print(f"  标准差：{std_dev(group_b):.4f}")
    
    improvement = (mean(group_b) - mean(group_a)) / mean(group_a) * 100
    print(f"\nB 组相对 A 组提升：{improvement:.2f}%")


def main():
    """运行所有演示"""
    print("\n" + "📊" * 30)
    print("   AllToolkit - Statistics Utils 功能演示")
    print("📊" * 30)
    
    demo_descriptive_statistics()
    demo_correlation_regression()
    demo_normalization()
    demo_outlier_detection()
    demo_real_world_analysis()
    
    print_section("演示完成")
    print("\n✅ 所有功能演示完毕！")
    print("\n提示：运行 'python statistics_utils_test.py -v' 执行完整测试套件")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
