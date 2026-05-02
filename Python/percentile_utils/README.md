# Percentile Utils - 百分位数计算工具

一个功能完整的百分位数计算工具模块，零外部依赖，纯 Python 实现。

## 核心功能

### 1. 基本百分位数计算
- `percentile(data, p, method)` - 计算第 p 百分位数
- 支持 7 种插值方法：
  - `LINEAR` - 线性插值（默认，与 numpy 一致）
  - `LOWER` - 取下界值
  - `HIGHER` - 取上界值
  - `NEAREST` - 最近邻
  - `MIDPOINT` - 中点值
  - `EXCLUSIVE` - Excel PERCENTILE.EXC 方法
  - `INCLUSIVE` - Excel PERCENTILE.INC 方法

### 2. 四分位数
- `quartiles(data)` - 计算 Q1, Q2, Q3, IQR

### 3. 百分位排名
- `percentile_rank(data, value)` - 计算某个值在数据集中的百分位排名

### 4. 箱线图统计
- `boxplot_stats(data)` - 完整的箱线图数据，包括异常值检测

### 5. 十分位数
- `deciles(data)` - 将数据分为 10 等份

### 6. 批量计算
- `percentiles(data, p_list)` - 一次计算多个百分位数
- `grouped_percentile(groups, p)` - 分组计算百分位数

### 7. 统计摘要
- `percentile_summary(data)` - 完整的百分位数统计摘要

### 8. 异常值处理
- `is_outlier(value, data)` - 判断是否为异常值
- `winsorize(data, lower, upper)` - 缩尾处理

### 9. 数据归一化
- `normalize_by_percentile(data)` - 基于 IQR 的归一化

## 使用示例

```python
from percentile_utils.mod import percentile, quartiles, boxplot_stats

# 基本百分位数
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
p50 = percentile(data, 50)  # 中位数
p25 = percentile(data, 25)  # 下四分位数

# 四分位数
qs = quartiles(data)
print(f"Q1={qs['Q1']}, Q2={qs['Q2']}, Q3={qs['Q3']}, IQR={qs['IQR']}")

# 箱线图统计（含异常值检测）
stats = boxplot_stats([1, 2, 3, 4, 5, 100])
print(f"异常值: {stats['outliers']}")
```

## 特性

- ✅ 零外部依赖
- ✅ 支持多种插值方法
- ✅ 完整的异常值检测
- ✅ 高性能优化（sorted_data 参数）
- ✅ 完善的错误处理
- ✅ 48 个单元测试覆盖

## 文件结构

```
percentile_utils/
├── mod.py              # 核心模块（16KB）
├── percentile_utils_test.py  # 测试文件（48个测试）
├── README.md           # 说明文档
└── examples/
    └── usage_examples.py  # 使用示例
```

## 作者

AllToolkit 自动生成
日期: 2026-05-02