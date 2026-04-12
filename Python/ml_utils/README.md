# AllToolkit - Python ML Utils 🧠

**零依赖机器学习工具 - 生产就绪**

---

## 📖 概述

`ml_utils` 提供功能完整的机器学习工具集，包括数据预处理、分类/回归评估指标、学习率调度器、距离度量和常用激活函数。完全使用 Python 标准库实现，无需任何外部依赖（如 NumPy、scikit-learn）。

---

## ✨ 特性

### 数据预处理
- **归一化** - Min-Max 缩放到 [0, 1]
- **标准化** - Z-score 标准化（零均值，单位方差）
- **数据集分割** - train_test_split 随机分割
- **交叉验证** - k 折交叉验证索引生成

### 分类评估指标
- **准确率** - accuracy_score
- **精确率** - precision_score（支持 binary/macro/micro/weighted）
- **召回率** - recall_score（支持 binary/macro/micro/weighted）
- **F1 分数** - f1_score
- **混淆矩阵** - 二分类和多分类支持
- **分类报告** - 完整的 per-class 指标

### 回归评估指标
- **均方误差** - MSE
- **均方根误差** - RMSE
- **平均绝对误差** - MAE
- **R² 分数** - 决定系数
- **平均绝对百分比误差** - MAPE

### 学习率调度器
- **StepLR** - 固定步长衰减
- **ExponentialLR** - 指数衰减
- **CosineAnnealingLR** - 余弦退火
- **ReduceLROnPlateau** - 指标不改善时衰减

### 距离度量
- **欧氏距离** - L2 距离
- **曼哈顿距离** - L1 距离
- **余弦相似度** - 向量夹角余弦
- **余弦距离** - 1 - 余弦相似度

### 激活函数
- **Softmax** - 多分类概率转换
- **Sigmoid** - 二分类概率转换
- **ReLU** - 线性整流单元

### 工具函数
- **One-Hot 编码** - 标签向量化
- **Argmax** - 最大值索引
- **交叉熵损失** - 分类损失计算
- **Memoize** - 函数结果缓存

---

## 🚀 快速开始

### 基础使用

```python
from mod import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_squared_error, r2_score,
    normalize, standardize,
    train_test_split,
)

# 分类评估
y_true = [1, 0, 1, 1, 0, 1, 0, 0]
y_pred = [1, 0, 1, 0, 0, 1, 1, 0]

print(f"Accuracy:  {accuracy_score(y_true, y_pred):.4f}")
print(f"Precision: {precision_score(y_true, y_pred):.4f}")
print(f"Recall:    {recall_score(y_true, y_pred):.4f}")
print(f"F1 Score:  {f1_score(y_true, y_pred):.4f}")

# 回归评估
y_true_reg = [3.0, -0.5, 2.0, 7.0]
y_pred_reg = [2.5, 0.0, 2.0, 8.0]

print(f"MSE:  {mean_squared_error(y_true_reg, y_pred_reg):.4f}")
print(f"RMSE: {root_mean_squared_error(y_true_reg, y_pred_reg):.4f}")
print(f"MAE:  {mean_absolute_error(y_true_reg, y_pred_reg):.4f}")
print(f"R²:   {r2_score(y_true_reg, y_pred_reg):.4f}")

# 数据预处理
data = [1.0, 2.0, 3.0, 4.0, 5.0]
normalized, min_v, max_v = normalize(data)
standardized, mean, std = standardize(data)

# 数据集分割
X = [[i] for i in range(100)]
y = list(range(100))
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

### 混淆矩阵

```python
from mod import confusion_matrix_binary, confusion_matrix_multiclass

# 二分类
y_true = [1, 0, 1, 1, 0, 0]
y_pred = [1, 0, 1, 0, 0, 1]

cm = confusion_matrix_binary(y_true, y_pred)
print(f"TN={cm.matrix[0][0]}, FP={cm.matrix[0][1]}")
print(f"FN={cm.matrix[1][0]}, TP={cm.matrix[1][1]}")

# 多分类
y_true = [0, 1, 2, 0, 1, 2]
y_pred = [0, 1, 1, 0, 2, 2]

cm = confusion_matrix_multiclass(y_true, y_pred)
for row in cm.matrix:
    print(row)
```

---

## 📚 API 参考

### 数据预处理

| 函数 | 描述 | 返回 |
|------|------|------|
| `normalize(vector, min_val, max_val)` | Min-Max 归一化 | `(normalized, min, max)` |
| `normalize_matrix(matrix, axis)` | 矩阵归一化 | `(normalized, mins, maxs)` |
| `standardize(vector, mean, std)` | Z-score 标准化 | `(standardized, mean, std)` |
| `standardize_matrix(matrix, axis)` | 矩阵标准化 | `(standardized, means, stds)` |
| `train_test_split(*arrays, test_size, random_state)` | 随机分割数据集 | `[train, test, ...]` |
| `k_fold_split(n_samples, k, random_state)` | K 折交叉验证 | `[(train_idx, test_idx), ...]` |

### 分类指标

| 函数 | 描述 | 返回 |
|------|------|------|
| `accuracy_score(y_true, y_pred)` | 准确率 | `float` |
| `precision_score(y_true, y_pred, pos_label, average)` | 精确率 | `float` |
| `recall_score(y_true, y_pred, pos_label, average)` | 召回率 | `float` |
| `f1_score(y_true, y_pred, pos_label, average)` | F1 分数 | `float` |
| `confusion_matrix_binary(y_true, y_pred, pos_label)` | 二分类混淆矩阵 | `ConfusionMatrix` |
| `confusion_matrix_multiclass(y_true, y_pred, labels)` | 多分类混淆矩阵 | `ConfusionMatrix` |
| `classification_report(y_true, y_pred, average)` | 分类报告 | `Dict[Label, ClassificationReport]` |

### 回归指标

| 函数 | 描述 | 返回 |
|------|------|------|
| `mean_squared_error(y_true, y_pred)` | 均方误差 | `float` |
| `root_mean_squared_error(y_true, y_pred)` | 均方根误差 | `float` |
| `mean_absolute_error(y_true, y_pred)` | 平均绝对误差 | `float` |
| `r2_score(y_true, y_pred)` | R² 分数 | `float` |
| `mean_absolute_percentage_error(y_true, y_pred)` | 平均绝对百分比误差 | `float` |

### 学习率调度器

| 类 | 描述 |
|------|------|
| `StepLR(initial_lr, step_size, gamma)` | 固定步长衰减 |
| `ExponentialLR(initial_lr, gamma)` | 指数衰减 |
| `CosineAnnealingLR(initial_lr, min_lr, max_epochs)` | 余弦退火 |
| `ReduceLROnPlateau(initial_lr, factor, patience, min_lr, mode)` | 指标不改善时衰减 |

### 距离度量

| 函数 | 描述 | 返回 |
|------|------|------|
| `euclidean_distance(a, b)` | 欧氏距离 | `float` |
| `manhattan_distance(a, b)` | 曼哈顿距离 | `float` |
| `cosine_similarity(a, b)` | 余弦相似度 | `float` |
| `cosine_distance(a, b)` | 余弦距离 | `float` |

### 激活函数

| 函数 | 描述 | 返回 |
|------|------|------|
| `softmax(logits)` | Softmax 归一化 | `Vector` |
| `sigmoid(x)` | Sigmoid 激活 | `float` 或 `Vector` |
| `relu(x)` | ReLU 激活 | `float` 或 `Vector` |

### 工具函数

| 函数 | 描述 | 返回 |
|------|------|------|
| `one_hot_encode(labels, num_classes)` | One-Hot 编码 | `Matrix` |
| `argmax(vector)` | 最大值索引 | `int` |
| `cross_entropy_loss(predictions, targets)` | 交叉熵损失 | `float` |
| `memoize(func)` | 缓存装饰器 | `Callable` |

---

## 🎯 使用场景

### 1. 模型评估

```python
from mod import accuracy_score, classification_report, confusion_matrix_binary

# 模型预测结果
y_true = [0, 0, 1, 1, 0, 1, 1, 1, 0, 0]
y_pred = [0, 0, 1, 0, 0, 1, 1, 1, 1, 0]

# 整体指标
print(f"Accuracy: {accuracy_score(y_true, y_pred):.4f}")

# 详细报告
report = classification_report(y_true, y_pred)
for label, metrics in report.items():
    print(f"Class {label}: P={metrics.precision:.3f}, R={metrics.recall:.3f}, F1={metrics.f1_score:.3f}")

# 混淆矩阵
cm = confusion_matrix_binary(y_true, y_pred)
print(f"TP={cm.matrix[1][1]}, FP={cm.matrix[0][1]}")
print(f"FN={cm.matrix[1][0]}, TN={cm.matrix[0][0]}")
```

### 2. 数据预处理管道

```python
from mod import train_test_split, normalize_matrix, standardize_matrix

# 原始数据
X = [[i, i*2, i*0.5] for i in range(1000)]
y = [i % 2 for i in range(1000)]

# 分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 标准化（使用训练集统计量）
X_train_std, means, stds = standardize_matrix(X_train, axis=0)

# 应用相同变换到测试集
X_test_std = []
for row in X_test:
    std_row = [(row[j] - means[j]) / stds[j] for j in range(len(row))]
    X_test_std.append(std_row)
```

### 3. 训练循环中的学习率调度

```python
from mod import StepLR, ReduceLROnPlateau

# StepLR 示例
scheduler = StepLR(initial_lr=0.1, step_size=30, gamma=0.1)

for epoch in range(100):
    lr = scheduler.step(epoch)
    print(f"Epoch {epoch}: LR = {lr:.6f}")
    # train_model(lr)

# ReduceLROnPlateau 示例
scheduler = ReduceLROnPlateau(initial_lr=0.01, factor=0.5, patience=5, mode='min')
best_loss = float('inf')

for epoch in range(100):
    train_loss = train_epoch()
    val_loss = validate()
    
    lr = scheduler.step(val_loss)
    
    if val_loss < best_loss:
        best_loss = val_loss
        print(f"Epoch {epoch}: New best! Loss={val_loss:.4f}, LR={lr:.6f}")
```

### 4. 交叉验证

```python
from mod import k_fold_split, accuracy_score

# 生成 K 折索引
folds = k_fold_split(n_samples=1000, k=5, random_state=42)

fold_scores = []
for fold_idx, (train_idx, test_idx) in enumerate(folds):
    # 使用索引分割数据
    X_train = [X[i] for i in train_idx]
    X_test = [X[i] for i in test_idx]
    y_train = [y[i] for i in train_idx]
    y_test = [y[i] for i in test_idx]
    
    # 训练和评估
    # model = train(X_train, y_train)
    # y_pred = model.predict(X_test)
    
    # 模拟预测
    y_pred = y_test  # 完美预测示例
    score = accuracy_score(y_test, y_pred)
    fold_scores.append(score)
    
    print(f"Fold {fold_idx + 1}: Accuracy = {score:.4f}")

print(f"Mean CV Score: {sum(fold_scores) / len(fold_scores):.4f}")
```

### 5. 距离度量用于 KNN

```python
from mod import euclidean_distance, manhattan_distance, cosine_similarity

# KNN 中的距离计算
query = [1.0, 2.0, 3.0]
data_points = [
    [1.1, 2.1, 3.1],
    [5.0, 6.0, 7.0],
    [1.0, 2.0, 2.9],
]

distances = []
for i, point in enumerate(data_points):
    dist = euclidean_distance(query, point)
    distances.append((i, dist))

# 按距离排序
distances.sort(key=lambda x: x[1])
print(f"Nearest neighbors: {[d[0] for d in distances[:3]]}")

# 文本相似度（余弦相似度）
vec1 = [1.0, 0.0, 1.0, 0.0]
vec2 = [1.0, 1.0, 0.0, 0.0]
similarity = cosine_similarity(vec1, vec2)
print(f"Cosine Similarity: {similarity:.4f}")
```

### 6. 激活函数用于神经网络

```python
from mod import softmax, sigmoid, relu, argmax

# 输出层：Softmax 转概率
logits = [2.0, 1.0, 0.1]
probabilities = softmax(logits)
predicted_class = argmax(probabilities)
print(f"Predicted class: {predicted_class}")
print(f"Probabilities: {[f'{p:.4f}' for p in probabilities]}")

# 隐藏层：ReLU 激活
hidden = [-1.0, 0.0, 2.0, 5.0]
activated = relu(hidden)
print(f"ReLU output: {activated}")

# 二分类：Sigmoid
logit = 3.0
prob = sigmoid(logit)
print(f"Sigmoid probability: {prob:.4f}")
```

### 7. 损失计算

```python
from mod import cross_entropy_loss, one_hot_encode

# 分类损失
predictions = [
    [0.9, 0.1, 0.0],
    [0.1, 0.8, 0.1],
    [0.2, 0.2, 0.6],
]
targets = [0, 1, 2]

loss = cross_entropy_loss(predictions, targets)
print(f"Cross-Entropy Loss: {loss:.4f}")

# One-Hot 编码
labels = [0, 1, 2, 0]
encoded = one_hot_encode(labels, num_classes=3)
print(f"One-Hot encoded: {encoded}")
```

---

## 🧪 运行测试

```bash
cd ml_utils
python ml_utils_test.py -v
```

### 测试覆盖

- ✅ 归一化和标准化
- ✅ 数据集分割和 K 折交叉验证
- ✅ 分类指标（准确率、精确率、召回率、F1）
- ✅ 混淆矩阵（二分类和多分类）
- ✅ 回归指标（MSE、RMSE、MAE、R²、MAPE）
- ✅ 学习率调度器
- ✅ 距离度量
- ✅ 激活函数
- ✅ 工具函数（One-Hot、Argmax、交叉熵、Memoize）
- ✅ 边界情况和错误处理
- ✅ 集成测试（完整 ML 管道）

---

## ⚠️ 注意事项

1. **零依赖**: 仅使用 Python 标准库，适合受限环境
2. **性能**: 对于大规模数据，建议使用 NumPy/scikit-learn
3. **数值稳定性**: Softmax 和交叉熵包含数值稳定处理
4. **浮点精度**: 所有比较使用适当容差
5. **空输入**: 大多数函数对空输入抛出 ValueError

---

## 📊 性能提示

### 推荐用法

```python
# ✅ 批量计算更高效
from mod import normalize_matrix

matrix = [[i, i*2] for i in range(1000)]
normalized, mins, maxs = normalize_matrix(matrix, axis=0)

# ❌ 避免逐行处理
normalized = []
for row in matrix:
    norm_row, _, _ = normalize(row)
    normalized.append(norm_row)
```

### 与 scikit-learn 对比

| 特性 | ml_utils | scikit-learn |
|------|----------|--------------|
| 依赖 | 无 | NumPy, SciPy |
| 安装 | 无需安装 | pip install |
| 性能 | 适合小数据 | 优化大数据 |
| 功能 | 核心功能 | 完整生态 |
| 适用场景 | 教学、受限环境、轻量应用 | 生产环境、大规模数据 |

---

## 📁 文件结构

```
ml_utils/
├── mod.py                      # 主要实现
├── ml_utils_test.py            # 测试套件 (100+ 测试用例)
├── README.md                   # 本文档
└── examples/
    ├── basic_usage.py          # 基础使用示例
    └── advanced_example.py     # 高级使用示例
```

---

## 💡 最佳实践

### 1. 保存预处理参数

```python
# 训练时
X_train_std, means, stds = standardize_matrix(X_train, axis=0)

# 保存参数
import json
with open('scaler_params.json', 'w') as f:
    json.dump({'means': means, 'stds': stds}, f)

# 推理时加载
with open('scaler_params.json', 'r') as f:
    params = json.load(f)
    means = params['means']
    stds = params['stds']

# 应用相同变换
X_test_std = []
for row in X_test:
    std_row = [(row[j] - means[j]) / stds[j] for j in range(len(row))]
    X_test_std.append(std_row)
```

### 2. 处理类别不平衡

```python
from mod import classification_report, f1_score

# 使用加权平均
y_true = [0, 0, 0, 0, 1]  # 不平衡
y_pred = [0, 0, 0, 1, 1]

# 宏平均（平等对待每个类）
f1_macro = f1_score(y_true, y_pred, average='macro')

# 加权平均（考虑支持度）
f1_weighted = f1_score(y_true, y_pred, average='weighted')

# 查看每类表现
report = classification_report(y_true, y_pred)
for label, metrics in report.items():
    print(f"Class {label}: support={metrics.support}, F1={metrics.f1_score:.3f}")
```

### 3. 学习率调度策略

```python
from mod import CosineAnnealingLR, ReduceLROnPlateau

# 策略 1: 余弦退火（适合固定训练轮次）
scheduler = CosineAnnealingLR(initial_lr=0.1, min_lr=0.001, max_epochs=100)

# 策略 2: 动态调整（适合不确定收敛时间）
scheduler = ReduceLROnPlateau(
    initial_lr=0.01,
    factor=0.5,
    patience=10,
    min_lr=1e-6,
    mode='min'
)
```

---

## 🔗 相关资源

- [scikit-learn metrics](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.metrics)
- [PyTorch optimizers](https://pytorch.org/docs/stable/optim.html)
- [Machine Learning Cheatsheet](https://ml-cheatsheet.readthedocs.io/)

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/ayukyo/alltoolkit
