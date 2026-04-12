# AllToolkit - Python Statistics Utils 📊

**零依赖统计分析工具 - 功能完整的生产就绪工具**

---

## 📖 概述

`statistics_utils` 提供全面的统计分析功能，包括描述性统计、相关性分析、回归分析、数据标准化、异常值检测和分布函数。完全使用 Python 标准库实现，无需任何外部依赖。

---

## ✨ 特性

- **描述性统计** - 均值、中位数、众数、方差、标准差、偏度、峰度
- **分位数** - 四分位数、百分位数、IQR
- **相关性分析** - 皮尔逊相关系数、斯皮尔曼等级相关、协方差
- **回归分析** - 线性回归、预测
- **数据标准化** - Min-Max 归一化、Z-score 标准化、鲁棒缩放
- **异常值检测** - IQR 方法、Z-score 方法
- **分布函数** - 正态分布 PDF/CDF、卡方统计
- **频率分析** - 频数表、相对频率、累积频率
- **综合统计** - 一键生成完整统计报告

---

## 🚀 快速开始

### 基础使用

```python
from mod import mean, median, std_dev, variance

# 计算均值
data = [1, 2, 3, 4, 5]
print(mean(data))  # 3.0

# 计算中位数
print(median(data))  # 3

# 计算标准差
print(std_dev(data))  # 1.5811...

# 计算方差
print(variance(data))  # 2.5
```

### 综合统计报告

```python
from mod import describe, summary

data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

# 获取完整统计字典
stats = describe(data)
print(stats)
# {'count': 10, 'mean': 55.0, 'std_dev': 28.72..., 'min': 10, ...}

# 生成人类可读的摘要
print(summary(data))
# Count:  10
# Mean:   55.0000
# Std Dev: 28.7228
# Min:    10.0000
# P25:    32.5000
# P50:    55.0000
# P75:    77.5000
# Max:    100.0000
```

---

## 📚 API 参考

### 描述性统计

| 函数 | 描述 |
|------|------|
| `mean(data)` | 算术平均值 |
| `geometric_mean(data)` | 几何平均值（要求正值） |
| `harmonic_mean(data)` | 调和平均值（要求正值） |
| `median(data)` | 中位数 |
| `mode(data)` | 众数（返回列表，支持多众数） |
| `variance(data, population=False)` | 方差（样本/总体） |
| `std_dev(data, population=False)` | 标准差 |
| `quartiles(data)` | 返回 (Q1, Q2, Q3) |
| `iqr(data)` | 四分位距 |
| `percentile(data, p)` | 第 p 百分位数 |
| `range_value(data)` | 极差（最大值 - 最小值） |
| `coefficient_of_variation(data)` | 变异系数 |
| `skewness(data)` | 偏度 |
| `kurtosis(data)` | 峰度（超额峰度） |

### 相关性与回归

```python
from mod import correlation, linear_regression, predict

# 皮尔逊相关系数
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]
corr = correlation(x, y)  # 1.0（完全正相关）

# 斯皮尔曼等级相关
from mod import spearman_correlation
spearman = spearman_correlation(x, y)

# 线性回归
reg = linear_regression(x, y)
print(reg)
# {'slope': 2.0, 'intercept': 0.0, 'r_squared': 1.0, 'std_error': 0.0}

# 预测
predicted_y = predict(reg, 6)  # 12.0
```

### 数据标准化

```python
from mod import normalize_minmax, standardize, robust_scale

data = [10, 20, 30, 40, 50]

# Min-Max 归一化到 [0, 1]
normalized = normalize_minmax(data)  # [0.0, 0.25, 0.5, 0.75, 1.0]

# 归一化到自定义范围 [-1, 1]
normalized_custom = normalize_minmax(data, new_min=-1, new_max=1)

# Z-score 标准化（均值=0，标准差=1）
standardized = standardize(data)

# 鲁棒缩放（使用中位数和 IQR，对异常值不敏感）
robust = robust_scale(data)
```

### 异常值检测

```python
from mod import detect_outliers_iqr, detect_outliers_zscore, remove_outliers

data = [1, 2, 3, 4, 5, 100]  # 100 是异常值

# IQR 方法检测
outliers_iqr = detect_outliers_iqr(data)  # [(5, 100)]

# Z-score 方法检测
outliers_z = detect_outliers_zscore(data, threshold=3.0)

# 移除异常值
clean_data = remove_outliers(data, method='iqr')  # [1, 2, 3, 4, 5]
```

### 分布函数

```python
from mod import normal_pdf, normal_cdf, z_score

# 正态分布 PDF
pdf = normal_pdf(x=0, mu=0, sigma=1)  # 0.3989...

# 正态分布 CDF
cdf = normal_cdf(x=0, mu=0, sigma=1)  # 0.5

# Z-score 计算
z = z_score(x=85, mu=70, sigma=10)  # 1.5
```

### 频率分析

```python
from mod import frequency_table, relative_frequency, cumulative_frequency

data = ['a', 'b', 'a', 'c', 'a', 'b']

# 频数表
freq = frequency_table(data)  # {'a': 3, 'b': 2, 'c': 1}

# 相对频率
rel = relative_frequency(data)  # {'a': 0.5, 'b': 0.333..., 'c': 0.166...}

# 累积频率
cum_freq = cumulative_frequency([1, 2, 3, 4, 5], bins=3)
```

---

## 🧪 运行测试

```bash
cd /home/admin/.openclaw/workspace/AllToolkit/Python/statistics_utils
python statistics_utils_test.py -v
```

测试覆盖：
- ✅ 所有统计函数
- ✅ 边界情况（空数据、单值、异常值）
- ✅ 错误处理
- ✅ 数值精度验证

---

## 📝 使用示例

### 示例 1：学生成绩分析

```python
from mod import describe, correlation, linear_regression

# 学生成绩数据
math_scores = [85, 90, 78, 92, 88, 76, 95, 89, 82, 91]
english_scores = [88, 92, 80, 90, 85, 78, 93, 87, 84, 89]

# 描述性统计
print("数学成绩统计:")
print(summary(math_scores))

# 相关性分析
corr = correlation(math_scores, english_scores)
print(f"\n数学与英语成绩相关性：{corr:.4f}")

# 回归分析（用数学成绩预测英语成绩）
reg = linear_regression(math_scores, english_scores)
print(f"\n回归方程：英语 = {reg['slope']:.4f} × 数学 + {reg['intercept']:.4f}")
print(f"R² = {reg['r_squared']:.4f}")

# 预测
predicted = predict(reg, 80)
print(f"\n预测：数学 80 分的学生，英语约 {predicted:.1f} 分")
```

### 示例 2：异常值检测与处理

```python
from mod import detect_outliers_iqr, remove_outliers, describe

# 销售数据（包含异常值）
sales = [100, 120, 115, 130, 125, 5000, 118, 122, 128, 119]

print("原始数据统计:")
print(summary(sales))

# 检测异常值
outliers = detect_outliers_iqr(sales)
print(f"\n检测到的异常值：{outliers}")

# 移除异常值
clean_sales = remove_outliers(sales)
print("\n清理后数据统计:")
print(summary(clean_sales))
```

### 示例 3：数据标准化

```python
from mod import standardize, normalize_minmax

# 不同量纲的数据
height_cm = [160, 165, 170, 175, 180, 185]
weight_kg = [55, 60, 65, 70, 75, 80]

# Z-score 标准化
height_z = standardize(height_cm)
weight_z = standardize(weight_kg)

print(f"身高标准化：{[f'{x:.2f}' for x in height_z]}")
print(f"体重标准化：{[f'{x:.2f}' for x in weight_z]}")

# Min-Max 归一化
height_norm = normalize_minmax(height_cm)
print(f"身高等一化：{[f'{x:.2f}' for x in height_norm]}")
```

---

## ⚠️ 注意事项

1. **空数据处理**：所有函数在空数据上都会抛出 `EmptyDataError`
2. **样本 vs 总体**：`variance` 和 `std_dev` 默认计算样本统计量（除以 n-1）
3. **正值要求**：几何平均和调和平均要求所有值为正
4. **数值稳定性**：对于极大或极小值，可能存在浮点精度限制

---

## 📄 许可证

MIT License - 详见 AllToolkit 主项目许可证

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
