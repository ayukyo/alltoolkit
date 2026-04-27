# Permutation Utils


Permutation Utils - 排列组合工具集

提供排列、组合的生成、计算、序号转换等功能。
零外部依赖，纯 Python 标准库实现。

功能:
- 排列生成 (全排列、部分排列)
- 组合生成 (n选k)
- 排列序号计算 (字典序转数字)
- 排列逆序计算 (数字转字典序)
- 组合序号计算
- 排列/组合迭代器 (惰性生成)
- 排列性质判断 (奇偶性、逆序对)


## 功能

### 类

- **PermutationUtils**: 排列工具类
  方法: permutations, all_permutations, permutation_count, permutation_rank, permutation_unrank ... (11 个方法)
- **CombinationUtils**: 组合工具类
  方法: combinations, combination_count, combination_rank, combination_unrank, all_subsets ... (6 个方法)
- **PermutationUtilsAdvanced**: 排列高级工具
  方法: random_permutation, random_combination, multiset_permutations, multiset_permutation_count, kth_permutation_with_duplicates ... (8 个方法)

### 函数

- **permutations(elements, k**) - 生成排列
- **combinations(elements, k**) - 生成组合
- **permutation_count(n, k**) - 计算排列数
- **combination_count(n, k**) - 计算组合数
- **factorial_val(n**) - 计算阶乘
- **permutations(elements, k**) - 生成排列
- **all_permutations(elements**) - 生成全排列（简写）
- **permutation_count(n, k**) - 计算排列数 P(n, k)
- **permutation_rank(perm, elements**) - 计算排列的字典序编号（从0开始）
- **permutation_unrank(rank, elements**) - 根据字典序编号生成排列

... 共 32 个函数

## 使用示例

```python
from mod import permutations

# 使用 permutations
result = permutations()
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
