# Combinatorics Utils


Combinatorics Utils - 组合数学工具集

提供完整的组合数学函数和生成器，包括：
- 排列（Permutations）
- 组合（Combinations）
- 笛卡尔积（Cartesian Product）
- 幂集（Power Set）
- 二项式系数（Binomial Coefficients）
- 阶乘（Factorial）
- 斯特林数（Stirling Numbers）
- 卡塔兰数（Catalan Numbers）
- 分拆数（Partition Numbers）
- 抽屉原理解析

零依赖，纯 Python 标准库实现。
支持大整数运算，内存高效生成器实现。


## 功能

### 函数

- **factorial(n**) - 计算阶乘 n!
- **factorial_range(n, k**) - 计算下降阶乘 n! / (n-k)! = n * (n-1) * ... * (n-k+1)
- **binomial(n, k**) - 计算二项式系数 C(n, k) = n! / (k! * (n-k)!)
- **multinomial(**) - 计算多项式系数
- **permutations(iterable, r**) - 生成排列（按字典序）
- **permutations_count(n, r**) - 计算排列数 P(n, r) = n! / (n-r)!
- **permutations_with_replacement(iterable, r**) - 生成可重复排列（有序，元素可重复使用）
- **combinations(iterable, r**) - 生成组合（按字典序）
- **combinations_count(n, r**) - 计算组合数 C(n, r) = n! / (r! * (n-r)!)
- **combinations_with_replacement(iterable, r**) - 生成可重复组合（无序，元素可重复使用）

... 共 38 个函数

## 使用示例

```python
from mod import factorial

# 使用 factorial
result = factorial()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
