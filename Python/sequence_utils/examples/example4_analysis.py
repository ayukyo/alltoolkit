"""
示例4：异常值检测与趋势分析
演示异常值检测和趋势分析功能
"""

from sequence_utils import (
    zscore_outliers, iqr_outliers, remove_outliers,
    is_monotonic, is_increasing, trend_direction,
    find_peaks, find_valleys, detect_seasonality
)

print("=== 异常值检测示例 ===")

# 含异常值的数据
data_with_outliers = [10, 12, 15, 18, 20, 500, 22, 25, 28, -100, 30]
print(f"含异常值的数据: {data_with_outliers}")

# Z-score 检测
zscore_idx = zscore_outliers(data_with_outliers, threshold=2.0)
print(f"\nZ-score 异常值索引: {zscore_idx}")
print(f"异常值: {[data_with_outliers[i] for i in zscore_idx]}")

# IQR 检测
iqr_idx = iqr_outliers(data_with_outliers, k=1.5)
print(f"\nIQR 异常值索引: {iqr_idx}")
print(f"异常值: {[data_with_outliers[i] for i in iqr_idx]}")

# 移除异常值
cleaned = remove_outliers(data_with_outliers, method='iqr')
print(f"\n移除异常值后: {cleaned}")

print("\n=== 趋势分析示例 ===")

# 单调序列
monotonic_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(f"数据: {monotonic_data}")
print(f"是否单调: {is_monotonic(monotonic_data)}")
print(f"是否递增: {is_increasing(monotonic_data)}")
print(f"趋势方向: {trend_direction(monotonic_data)}")

# 非单调序列
non_monotonic = [1, 5, 3, 7, 2, 9, 4]
print(f"\n数据: {non_monotonic}")
print(f"是否单调: {is_monotonic(non_monotonic)}")
print(f"趋势方向: {trend_direction(non_monotonic)}")

print("\n=== 峰值和谷值检测 ===")

# 有峰值和谷值的数据
wave_data = [1, 5, 2, 8, 3, 10, 4, 7, 2]
print(f"数据: {wave_data}")

peaks = find_peaks(wave_data)
print(f"峰值索引: {peaks}")
print(f"峰值: {[wave_data[i] for i in peaks]}")

valleys = find_valleys(wave_data)
print(f"谷值索引: {valleys}")
print(f"谷值: {[wave_data[i] for i in valleys]}")

print("\n=== 周期性检测 ===")

# 周期性数据
seasonal_data = [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]
print(f"周期性数据: {seasonal_data}")
period = detect_seasonality(seasonal_data)
print(f"检测到的周期: {period}")

# 非周期性数据
random_data = [1, 5, 2, 8, 3, 7, 4, 6]
print(f"\n非周期性数据: {random_data}")
period2 = detect_seasonality(random_data)
print(f"检测到的周期: {period2}")