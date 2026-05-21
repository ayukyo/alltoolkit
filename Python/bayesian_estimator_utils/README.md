# Bayesian Estimator Utils

贝叶斯估计器工具集，零依赖实现的贝叶斯统计和推断工具。

## 功能特性

- **Beta 分布**: 0-1 之间概率估计
- **朴素贝叶斯分类器**: 文本分类、多特征分类
- **贝叶斯平均**: 评分系统（如电影评分）
- **贝叶斯更新**: 在线学习、参数更新
- **贝叶斯假设检验**: A/B 测试分析

## 快速开始

```python
from bayesian_estimator_utils.mod import BetaDistribution, BayesianAverage

# Beta 分布估计成功率
beta = BetaDistribution(alpha=10, beta=5)  # 10 成功, 5 失败
print(f"期望成功率: {beta.mean}")  # 0.667
print(f"95% 置信区间: ({beta.lower_bound(0.95)}, {beta.upper_bound(0.95)})")
```

## 使用示例

### Beta 分布

```python
from bayesian_estimator_utils.mod import BetaDistribution

# 创建 Beta 分布（用于转化率估计）
beta = BetaDistribution(alpha=50, beta=100)  # 50 转化, 100 未转化

# 期望值
print(beta.mean)    # 0.333

# 标准差
print(beta.std_dev)  # 不确定性

# 众数
print(beta.mode)     # 最可能的值

# PDF（概率密度函数）
pdf = beta.pdf(0.35)

# 置信区间
lower = beta.lower_bound(0.95)
upper = beta.upper_bound(0.95)
```

### 贝叶斯平均（评分系统）

```python
from bayesian_estimator_utils.mod import BayesianAverage

# 创建贝叶斯平均评分器
# prior_mean: 先验平均评分（如 2.5）
# prior_weight: 先验权重（相当于多少个虚拟评分）
ba = BayesianAverage(prior_mean=2.5, prior_weight=5)

# 添加评分
ba.add_rating("电影A", [5, 5, 4, 5])  # 4 个高分
ba.add_rating("电影B", [3])           # 只有 1 个评分
ba.add_rating("电影C", [2, 2, 2, 2, 2])  # 5 个低分

# 获取贝叶斯平均评分（避免小样本偏差）
print(ba.get_bayesian_rating("电影A"))  # 较高
print(ba.get_bayesian_rating("电影B"))  # 接近先验（样本少）
print(ba.get_bayesian_rating("电影C"))  # 较低

# 排序（贝叶斯平均排序）
rankings = ba.rank_items()  # 按贝叶斯评分排序
```

### 朴素贝叶斯分类器

```python
from bayesian_estimator_utils.mod import NaiveBayesClassifier

# 创建分类器
clf = NaiveBayesClassifier()

# 训练数据
clf.train("spam", ["垃圾", "广告", "推销", "免费"])
clf.train("normal", ["正常", "朋友", "工作", "会议"])

# 预测
text = "这是一个垃圾邮件广告"
label = clf.predict(text)
print(label)  # "spam"

# 查看概率
probs = clf.predict_proba(text)
print(probs)  # {"spam": 0.85, "normal": 0.15}
```

### 贝叶斯更新（在线学习）

```python
from bayesian_estimator_utils.mod import BayesianUpdater

# 创建更新器（初始估计）
updater = BayesianUpdater(
    prior_alpha=1,  # 先验成功
    prior_beta=1    # 先验失败
)

# 观察数据并更新
updater.update(success=True)   # 观察成功
updater.update(success=False)  # 观察失败
updater.update(success=True)   # 再次成功

# 获取当前估计
print(updater.current_estimate())  # Beta 分布参数

# 批量更新
updater.batch_update([True, False, True, True, False])
```

### A/B 测试分析

```python
from bayesian_estimator_utils.mod import ABTestAnalyzer

# 创建 A/B 测试分析器
ab = ABTestAnalyzer()

# 添加数据
ab.add_variant("A", successes=100, trials=500)  # 转化率 20%
ab.add_variant("B", successes=150, trials=500)  # 转化率 30%

# 分析结果
result = ab.analyze()
print(f"B 比 A 奩的概率: {result.probability_b_better}")
print(f"B 的期望转化率: {result.expected_b}")
print(f"A 的期望转化率: {result.expected_a}")

# 推荐
print(f"推荐方案: {result.recommended_variant}")
```

## API 参考

### BetaDistribution

| 属性/方法 | 说明 |
|-----------|------|
| `alpha`, `beta` | 分布参数 |
| `mean` | 期望值 |
| `variance`, `std_dev` | 方差、标准差 |
| `mode` | 众数 |
| `pdf(x)` | 概率密度函数 |
| `lower_bound(confidence)` | 置信区间下界 |
| `upper_bound(confidence)` | 置信区间上界 |

### BayesianAverage

| 方法 | 说明 |
|------|------|
| `add_rating(item, ratings)` | 添加评分 |
| `get_bayesian_rating(item)` | 获取贝叶斯评分 |
| `rank_items()` | 按贝叶斯评分排序 |
| `get_all_ratings()` | 获取所有评分 |

### NaiveBayesClassifier

| 方法 | 说明 |
|------|------|
| `train(label, words)` | 训练分类 |
| `predict(text)` | 预测标签 |
| `predict_proba(text)` | 预测概率 |
| `reset()` | 重置分类器 |

### BayesianUpdater

| 方法 | 说明 |
|------|------|
| `update(success)` | 单次更新 |
| `batch_update(results)` | 批量更新 |
| `current_estimate()` | 当前 Beta 分布 |
| `confidence_interval(level)` | 置信区间 |

### ABTestAnalyzer

| 方法 | 说明 |
|------|------|
| `add_variant(name, successes, trials)` | 添加变体 |
| `analyze()` | 分析结果 |
| `recommend()` | 推荐方案 |

## 应用场景

- **A/B 测试**: 网页/产品变体效果对比
- **评分系统**: 避免小样本偏差的评分排名
- **文本分类**: 邮件分类、情感分析
- **转化率估计**: 广告效果、产品转化
- **异常检测**: 基于概率的异常判定

## 贝叶斯平均公式

```
贝叶斯评分 = (C × M + ΣR) / (C + N)

其中:
- C = 先验权重（虚拟评分数）
- M = 先验平均评分
- ΣR = 实际评分总和
- N = 实际评分数量
```

---

**测试覆盖**: 完整测试套件，覆盖 Beta 分布、朴素贝叶斯、贝叶斯平均、A/B 测试等