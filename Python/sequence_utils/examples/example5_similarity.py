"""
示例5：序列相似度与相关分析
演示各种相似度度量方法
"""

from sequence_utils import (
    euclidean_distance, manhattan_distance,
    cosine_similarity, pearson_correlation,
    spearman_correlation, dtw_distance,
    autocorrelation, autocorrelation_function
)

print("=== 序列相似度示例 ===")

seq1 = [1, 2, 3, 4, 5]
seq2 = [1.1, 2.2, 3.1, 4.2, 5.1]
seq3 = [5, 4, 3, 2, 1]  # 与 seq1 反序

print(f"序列1: {seq1}")
print(f"序列2: {seq2}")
print(f"序列3: {seq3}")

print("\n=== 距离度量 ===")

print("\n欧几里得距离:")
print(f"seq1 - seq2: {euclidean_distance(seq1, seq2):.4f}")
print(f"seq1 - seq3: {euclidean_distance(seq1, seq3):.4f}")

print("\n曼哈顿距离:")
print(f"seq1 - seq2: {manhattan_distance(seq1, seq2):.4f}")
print(f"seq1 - seq3: {manhattan_distance(seq1, seq3):.4f}")

print("\n=== 相似度度量 ===")

print("\n余弦相似度:")
print(f"seq1 - seq2: {cosine_similarity(seq1, seq2):.4f}")
print(f"seq1 - seq3: {cosine_similarity(seq1, seq3):.4f}")

print("\n皮尔逊相关系数:")
print(f"seq1 - seq2: {pearson_correlation(seq1, seq2):.4f}")
print(f"seq1 - seq3: {pearson_correlation(seq1, seq3):.4f}")

print("\n斯皮尔曼相关系数:")
print(f"seq1 - seq2: {spearman_correlation(seq1, seq2):.4f}")
print(f"seq1 - seq3: {spearman_correlation(seq1, seq3):.4f}")

print("\n=== 动态时间规整 (DTW) ===")

# DTW 可以处理不同长度的序列
seq_short = [1, 2, 3, 4]
seq_long = [1, 1, 2, 2, 3, 3, 4, 4]

print(f"短序列: {seq_short}")
print(f"长序列: {seq_long}")
print(f"DTW 距离: {dtw_distance(seq_short, seq_long):.4f}")

print("\n=== 自相关分析 ===")

# 时间序列数据
time_series = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
print(f"时间序列: {time_series}")

print("\n自相关系数:")
print(f"lag=0: {autocorrelation(time_series, 0):.4f}")
print(f"lag=1: {autocorrelation(time_series, 1):.4f}")
print(f"lag=2: {autocorrelation(time_series, 2):.4f}")
print(f"lag=3: {autocorrelation(time_series, 3):.4f}")

print("\n自相关函数 (ACF):")
acf = autocorrelation_function(time_series, max_lag=5)
for i, val in enumerate(acf):
    print(f"lag={i}: {val:.4f}")