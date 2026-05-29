"""
示例3：序列变换与滑动窗口
演示变换操作和滑动窗口功能
"""

from sequence_utils import (
    normalize, standardize, differentiate,
    cumulative_sum, exponential_smoothing, moving_average,
    sliding_window, rolling_max, rolling_min, rolling_sum
)

data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

print("=== 序列变换示例 ===")
print(f"原始数据: {data}")

# 归一化
print("\n归一化 (minmax, 0-1范围):")
print(f"{normalize(data)}")

# 标准化
print("\n标准化 (zscore):")
print(f"{standardize(data)}")

# 差分
print("\n一阶差分:")
print(f"{differentiate(data)}")

print("\n二阶差分:")
print(f"{differentiate(data, 2)}")

# 累积和
print("\n累积和:")
print(f"{cumulative_sum(data)}")

# 指数平滑
print("\n指数平滑 (alpha=0.3):")
print(f"{exponential_smoothing(data, 0.3)}")

# 移动平均
print("\n移动平均 (window=3):")
print(f"{moving_average(data, 3)}")

# 加权移动平均
weights = [0.1, 0.3, 0.6]
print("\n加权移动平均 (window=3, weights=[0.1, 0.3, 0.6]):")
print(f"{moving_average(data, 3, weights=weights)}")

print("\n=== 滑动窗口示例 ===")

# 滑动窗口
print("\n滑动窗口 (window=3):")
windows = sliding_window(data, 3)
for i, w in enumerate(windows[:3]):  # 只显示前3个
    print(f"  窗口{i}: {w}")

# 滚动统计
print("\n滚动最大值 (window=3):")
print(f"{rolling_max(data, 3)}")

print("\n滚动最小值 (window=3):")
print(f"{rolling_min(data, 3)}")

print("\n滚动求和 (window=3):")
print(f"{rolling_sum(data, 3)}")