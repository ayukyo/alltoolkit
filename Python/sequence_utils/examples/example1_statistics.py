"""
示例1：统计分析
演示基本统计功能的使用
"""

from sequence_utils import (
    mean, median, mode, variance, std_dev,
    quartiles, iqr, descriptive_stats
)

# 基本统计
data = [12, 15, 18, 22, 25, 28, 30, 33, 35, 40]

print("=== 基本统计示例 ===")
print(f"数据: {data}")
print(f"均值: {mean(data)}")
print(f"中位数: {median(data)}")
print(f"众数: {mode(data)}")

# 方差和标准差
print(f"\n总体方差: {variance(data, population=True)}")
print(f"样本方差: {variance(data, population=False)}")
print(f"总体标准差: {std_dev(data, population=True)}")
print(f"样本标准差: {std_dev(data, population=False)}")

# 四分位数
q1, q2, q3 = quartiles(data)
print(f"\n第一四分位数 (Q1): {q1}")
print(f"第二四分位数 (Q2/中位数): {q2}")
print(f"第三四分位数 (Q3): {q3}")
print(f"四分位距 (IQR): {iqr(data)}")

# 完整描述性统计
print("\n=== 完整描述性统计 ===")
stats = descriptive_stats(data)
for key, value in stats.items():
    if isinstance(value, list):
        print(f"{key}: {value}")
    else:
        print(f"{key}: {value:.4f}")