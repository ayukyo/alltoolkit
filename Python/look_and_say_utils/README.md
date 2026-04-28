# Look and Say Utils - 外观数列工具集

外观数列（Look-and-Say sequence）是一个有趣的数学序列，每个项是对前一项的"外观描述"。

## 序列示例

```
1        → 起始
11       → 一个1
21       → 两个1
1211     → 一个2，一个1
111221   → 一个1，一个2，两个1
312211   → 三个1，两个2，一个1
...
```

## 核心功能

### 基本操作
- `next_term(term)` - 计算下一项
- `generate(n, start)` - 生成前n项
- `nth_term(n, start)` - 计算第n项
- `iterator(start)` - 无穷迭代器

### 长度分析
- `length_ratio(n)` - 相邻项长度比
- `conway_constant_approximation(n)` - 康威常数近似
- `estimate_nth_length(n)` - 估算第n项长度
- `analyze_growth(n)` - 增长分析

### 数字分析
- `digit_frequency(term)` - 数字频率
- `digit_distribution(n)` - 数字分布比例
- `count_unique_digits(n)` - 唯一数字数量
- `max_run_length(term)` - 最大连续长度

### 游程编码
- `run_length_encoding(s)` - 编码
- `from_run_length(encoded)` - 解码

### 验证与推导
- `is_valid_look_and_say_term(term)` - 有效性检查
- `reverse_step(term)` - 反向推导
- `split_into_elements(term)` - 元素分割

### 特殊功能
- `different_seed(seed, n)` - 不同种子生成
- `cosmological_decay(n)` - 康威宇宙学定理演示

## 使用示例

```python
from look_and_say_utils.mod import LookAndSayUtils, generate, nth_term

# 生成前10项
terms = generate(10)
for i, term in enumerate(terms):
    print(f"T({i}): {term}")

# 计算第15项
term15 = nth_term(15)
print(f"第15项长度: {len(term15)}")

# 康威常数近似
approx = LookAndSayUtils.conway_constant_approximation(20)
print(f"康威常数近似: {approx:.6f}")

# 不同种子
terms_22 = LookAndSayUtils.different_seed("22", 5)
print(f"种子22: {terms_22}")  # ['22', '22', '22', '22', '22'] - 不动点!
```

## 数学背景

### 康威常数
外观数列相邻项长度比趋近于常数 λ ≈ 1.303577，这个常数被称为康威常数，是多项式方程的唯一实根。

### 宇宙学定理
康威证明，无论从什么种子开始（除了22这个不动点），数列最终都会只包含数字1、2、3，并且特定的模式会稳定出现。

### 有趣性质
1. 种子"22"是不动点：22 → 22 → 22...
2. 数列只包含数字1、2、3（从标准种子开始）
3. 长度呈指数增长，增长率约为1.303577

## 零依赖

纯 Python 实现，无外部依赖。