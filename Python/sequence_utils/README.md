# Sequence Utilities - 序列分析工具模块

提供全面的序列分析和处理功能，零外部依赖，仅使用 Python 标准库。

## 功能概览

### 统计分析
- `mean(seq)` - 算术平均值
- `median(seq)` - 中位数
- `mode(seq)` - 众数
- `variance(seq, population=True)` - 方差（总体或样本）
- `std_dev(seq, population=True)` - 标准差
- `skewness(seq)` - 偏度（分布不对称性）
- `kurtosis(seq)` - 峰度（分布尖锐程度）
- `quantile(seq, q)` - 分位数
- `quartiles(seq)` - 四分位数 (Q1, Q2, Q3)
- `iqr(seq)` - 四分位距
- `range_value(seq)` - 极差
- `coefficient_of_variation(seq)` - 变异系数
- `descriptive_stats(seq)` - 完整描述性统计

### 序列变换
- `normalize(seq, method='minmax')` - 归一化（minmax 或 zscore）
- `standardize(seq)` - Z-score 标准化
- `differentiate(seq, n=1)` - 差分
- `cumulative_sum(seq)` - 累积和
- `cumulative_product(seq)` - 累积积
- `exponential_smoothing(seq, alpha)` - 指数平滑
- `moving_average(seq, window, weights)` - 移动平均
- `log_transform(seq, base)` - 对数变换
- `power_transform(seq, exponent)` - 幂变换
- `box_cox_transform(seq, lambda)` - Box-Cox 变换

### 序列生成器
- `arange(start, stop, step)` - 等差数列
- `linspace(start, stop, num)` - 等间隔数列
- `logspace(start, stop, num, base)` - 对数等间隔数列
- `geometric_sequence(start, ratio, length)` - 等比数列
- `fibonacci(n)` - 斐波那契数列
- `tribonacci(n)` - 三波那契数列
- `lucas_numbers(n)` - 卢卡斯数列
- `prime_numbers(n)` - 质数序列
- `triangular_numbers(n)` - 三角形数列
- `square_numbers(n)` - 平方数列
- `cube_numbers(n)` - 立方数列
- `factorial_sequence(n)` - 阶乘数列
- `golden_sequence(n)` - 黄金比例序列

### 滑动窗口操作
- `sliding_window(seq, window_size, step)` - 滑动窗口
- `rolling_max(seq, window)` - 滚动最大值
- `rolling_min(seq, window)` - 滚动最小值
- `rolling_sum(seq, window)` - 滚动求和
- `rolling_std(seq, window)` - 滚动标准差

### 插值与填充
- `linear_interpolate(x, y, x_new)` - 线性插值
- `fill_missing(seq, method)` - 填充缺失值（linear/forward/backward/mean/median）

### 重采样
- `downsample(seq, factor, method)` - 下采样
- `upsample(seq, factor, method)` - 上采样

### 序列操作
- `reverse(seq)` - 反转
- `shuffle(seq, seed)` - 随机打乱
- `sample(seq, n, replace, seed)` - 抽样
- `split(seq, ratio, shuffle_data, seed)` - 分割
- `chunk(seq, size)` - 分块
- `flatten(seqs)` - 展平嵌套序列
- `unique(seq, preserve_order)` - 唯一元素
- `difference(seq1, seq2)` - 差集
- `intersection(seq1, seq2)` - 交集
- `union(seq1, seq2)` - 并集

### 异常值检测
- `zscore_outliers(seq, threshold)` - Z-score 异常值检测
- `iqr_outliers(seq, k)` - IQR 异常值检测
- `remove_outliers(seq, method)` - 移除异常值

### 趋势与周期检测
- `is_monotonic(seq, strict)` - 是否单调
- `is_increasing(seq, strict)` - 是否递增
- `is_decreasing(seq, strict)` - 是否递减
- `trend_direction(seq)` - 趋势方向
- `find_peaks(seq, prominence)` - 查找峰值
- `find_valleys(seq, prominence)` - 查找谷值
- `detect_seasonality(seq, max_period)` - 检测周期性

### 自相关与滞后
- `autocorrelation(seq, lag)` - 自相关系数
- `autocorrelation_function(seq, max_lag)` - 自相关函数 (ACF)
- `lag(seq, n, fill)` - 滞后序列
- `lead(seq, n, fill)` - 领先序列

### 序列相似度
- `euclidean_distance(seq1, seq2)` - 欧几里得距离
- `manhattan_distance(seq1, seq2)` - 曼哈顿距离
- `cosine_similarity(seq1, seq2)` - 余弦相似度
- `pearson_correlation(seq1, seq2)` - 皮尔逊相关系数
- `spearman_correlation(seq1, seq2)` - 斯皮尔曼相关系数
- `dtw_distance(seq1, seq2)` - 动态时间规整距离

### 实用工具
- `apply(seq, func)` - 应用函数
- `filter_seq(seq, predicate)` - 过滤序列
- `reduce_seq(seq, func, initial)` - 归约序列
- `compose(*funcs)` - 函数组合

### 常量
- `GOLDEN_RATIO` - 黄金比例 (≈1.618)
- `EULER_NUMBER` - 自然常数 e
- `PI` - 圆周率 π

## 使用示例

```python
from sequence_utils import mean, median, fibonacci, moving_average

# 基本统计
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(f"均值: {mean(data)}")
print(f"中位数: {median(data)}")
print(f"四分位数: {quartiles(data)}")

# 生成斐波那契数列
fib = fibonacci(10)
print(f"斐波那契数列: {fib}")

# 移动平均
smoothed = moving_average(data, window=3)
print(f"移动平均: {smoothed}")

# 检测趋势
print(f"趋势方向: {trend_direction(data)}")

# 异常值检测
outlier_data = [1, 2, 3, 4, 5, 100]
print(f"IQR异常值索引: {iqr_outliers(outlier_data)}")

# 序列相似度
seq1 = [1, 2, 3, 4, 5]
seq2 = [1.1, 2.1, 3.1, 4.1, 5.1]
print(f"皮尔逊相关系数: {pearson_correlation(seq1, seq2)}")
```

## 特点

- **零依赖** - 仅使用 Python 标准库
- **类型安全** - 完整的类型标注
- **异常处理** - 清晰的错误提示
- **完整测试** - 覆盖所有功能

## 版本

1.0.0 - 初始版本

## 作者

AllToolkit