# Probability Distribution Utilities

概率分布与统计计算工具模块，零外部依赖，生产就绪。

## 特性

- **概率分布**: 正态分布、二项分布、泊松分布、指数分布、均匀分布
- **统计函数**: 均值、中位数、众数、方差、标准差、百分位数、偏度、峰度
- **置信区间**: Z 检验、T 检验、比例置信区间
- **假设检验**: Z 统计量、P 值计算、样本量估算
- **概率计算**: 贝叶斯定理、全概率公式、条件概率
- **随机抽样**: 从各种分布生成随机样本

## 安装

无需安装，直接导入使用：

```python
from probability_utils.mod import *
```

## 快速开始

### 基础统计分析

```python
from probability_utils.mod import mean, median, std_dev, percentile

data = [85, 92, 78, 90, 88, 95, 82, 79, 91, 87]

print(f"Mean: {mean(data)}")
print(f"Median: {median(data)}")
print(f"Std Dev: {std_dev(data)}")
print(f"90th percentile: {percentile(data, 90)}")
```

### 正态分布

```python
from probability_utils.mod import normal_cdf, normal_ppf, NormalDistribution

# IQ 分布 (μ=100, σ=15)
prob = normal_cdf(115, 100, 15) - normal_cdf(85, 100, 15)
print(f"IQ 85-115 概率: {prob:.2%}")

# 95 百分位 IQ
iq_95 = normal_ppf(0.95, 100, 15)
print(f"95 百分位 IQ: {iq_95}")

# 使用类
iq_dist = NormalDistribution(mean=100, std=15)
samples = iq_dist.samples(10)
```

### 二项分布

```python
from probability_utils.mod import binomial_pmf, binomial_cdf

# 10 次抛硬币，恰好 5 次正面
prob = binomial_pmf(5, 10, 0.5)
print(f"恰好 5 次正面概率: {prob:.4f}")

# 质检场景：10 件产品，20% 缺陷率
prob_defect = binomial_cdf(2, 10, 0.2)
print(f"最多 2 件缺陷概率: {prob_defect:.4f}")
```

### 泊松分布

```python
from probability_utils.mod import poisson_pmf, PoissonDistribution

# 每小时平均 5 名顾客
prob = poisson_pmf(3, 5)
print(f"恰好 3 名顾客概率: {prob:.4f}")

pois = PoissonDistribution(lambda_=5)
for k in range(8):
    print(f"P(X={k}): {pois.pmf(k):.4f}")
```

### 置信区间

```python
from probability_utils.mod import z_confidence_interval, proportion_confidence_interval

# 调查：样本均值 52，标准差 8，样本量 100
ci = z_confidence_interval(52, 8, 100, 0.95)
print(f"95% 置信区间: [{ci[0]:.2f}, {ci[1]:.2f}]")

# 比例置信区间：65/100 支持
ci_prop = proportion_confidence_interval(65, 100, 0.95)
print(f"支持率置信区间: [{ci_prop[0]:.3f}, {ci_prop[1]:.3f}]")
```

### 贝叶斯定理

```python
from probability_utils.mod import bayes_theorem

# 医学检测：患病率 1%，敏感性 99%，特异性 95%
prevalence = 0.01
sensitivity = 0.99
false_positive = 0.05

p_positive = sensitivity * prevalence + false_positive * (1 - prevalence)
p_disease = bayes_theorem(sensitivity, prevalence, p_positive)

print(f"阳性后患病概率: {p_disease:.2%}")
```

### 相关性分析

```python
from probability_utils.mod import correlation, covariance

study_hours = [2, 3, 4, 5, 6, 7, 8]
test_scores = [65, 70, 75, 78, 82, 85, 88]

r = correlation(study_hours, test_scores)
print(f"相关系数: {r:.4f}")  # 强正相关
```

## API 参考

### 基础统计函数

| 函数 | 描述 |
|------|------|
| `mean(data)` | 算术平均值 |
| `median(data)` | 中位数 |
| `mode(data)` | 众数 |
| `variance(data, population)` | 方差 |
| `std_dev(data, population)` | 标准差 |
| `percentile(data, p)` | 百分位数 |
| `quartiles(data)` | 四分位数 (Q1, Q2, Q3) |
| `iqr(data)` | 四分位距 |
| `skewness(data)` | 偏度 |
| `kurtosis(data)` | 峰度 |
| `geometric_mean(data)` | 几何平均 |
| `harmonic_mean(data)` | 调和平均 |

### 正态分布

| 函数 | 描述 |
|------|------|
| `normal_pdf(x, mean, std)` | 概率密度函数 |
| `normal_cdf(x, mean, std)` | 累积分布函数 |
| `normal_ppf(p, mean, std)` | 百分位点函数 (逆 CDF) |
| `z_score(x, mean, std)` | Z 分数 |
| `standardize(data)` | 标准化数据 |

### 二项分布

| 函数 | 描述 |
|------|------|
| `binomial_pmf(k, n, p)` | 概率质量函数 |
| `binomial_cdf(k, n, p)` | 累积分布函数 |
| `binomial_mean(n, p)` | 均值 = np |
| `binomial_variance(n, p)` | 方差 = np(1-p) |
| `combination(n, k)` | 组合数 C(n,k) |
| `permutation(n, k)` | 排列数 P(n,k) |

### 泊松分布

| 函数 | 描述 |
|------|------|
| `poisson_pmf(k, lambda)` | 概率质量函数 |
| `poisson_cdf(k, lambda)` | 累积分布函数 |
| `poisson_mean(lambda)` | 均值 = λ |
| `poisson_variance(lambda)` | 方差 = λ |

### 置信区间

| 函数 | 描述 |
|------|------|
| `z_confidence_interval(mean, std, n, confidence)` | Z 检验置信区间 |
| `t_confidence_interval(mean, std, n, confidence)` | T 检验置信区间 |
| `proportion_confidence_interval(successes, n, confidence)` | 比例置信区间 |

### 假设检验

| 函数 | 描述 |
|------|------|
| `z_test(sample_mean, pop_mean, pop_std, n)` | Z 检验 (返回 z, p) |
| `margin_of_error(std, n, confidence)` | 边际误差 |
| `sample_size_for_mean(std, margin, confidence)` | 估算样本量 |
| `sample_size_for_proportion(margin, confidence, p)` | 比例样本量 |

### 概率计算

| 函数 | 描述 |
|------|------|
| `bayes_theorem(p_b_given_a, p_a, p_b)` | 贝叶斯定理 |
| `total_probability(p_b_given_a_list, p_a_list)` | 全概率公式 |
| `probability_union(p_a, p_b, p_intersection)` | 联合概率 |
| `conditional_probability(p_a_given_b, p_b)` | 条件概率 |

### 随机抽样

| 函数 | 描述 |
|------|------|
| `random_normal(mean, std)` | 正态分布随机数 |
| `random_binomial(n, p)` | 二项分布随机数 |
| `random_poisson(lambda)` | 泊松分布随机数 |
| `random_exponential(lambda)` | 指数分布随机数 |
| `random_uniform(a, b)` | 均匀分布随机数 |

### 分布类

```python
# NormalDistribution
norm = NormalDistribution(mean=0, std=1)
norm.pdf(x)      # PDF
norm.cdf(x)      # CDF
norm.ppf(p)      # PPF
norm.sample()    # 随机样本
norm.samples(n)  # 多个样本

# BinomialDistribution
binom = BinomialDistribution(n=10, p=0.5)
binom.pmf(k)
binom.cdf(k)
binom.mean       # 属性
binom.variance

# PoissonDistribution
pois = PoissonDistribution(lambda_=5)

# ExponentialDistribution
exp = ExponentialDistribution(lambda_=0.5)

# UniformDistribution
unif = UniformDistribution(a=0, b=1)
```

## 测试

```bash
python Python/probability_utils/probability_utils_test.py
```

## 示例

```bash
python Python/probability_utils/examples/usage_examples.py
```

## 许可证

MIT License