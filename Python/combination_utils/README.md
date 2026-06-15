# Combination Utils 🔢

组合数学工具模块，提供排列、组合、卡特兰数、斯特林数等计算。

## 特性

- ✅ **组合数 C(n,k)** - 阶乘/乘法实现，避免大数溢出
- ✅ **排列数 P(n,k)** - 排列计算
- ✅ **全排列生成** - 字典序全排列
- ✅ **组合生成** - k 组合生成
- ✅ **卡特兰数** - 第 n 个卡特兰数
- ✅ **斯特林数** - 第一类/第二类
- ✅ **零依赖** - 仅使用 Python 标准库

## 快速开始

```python
from combination_utils import combination, permutation, catalan

# 组合数 C(5, 2) = 10
c = combination(5, 2)
print(c)  # 10

# 排列数 P(5, 2) = 20
p = permutation(5, 2)
print(p)  # 20

# 卡特兰数 C(4) = 14
cat = catalan(4)
print(cat)  # 14

# 全排列
from combination_utils import generate_permutations
perms = generate_permutations([1, 2, 3])
print(list(perms))  # [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
```

## API 参考

| 函数 | 说明 |
|------|------|
| `combination(n, k)` | 组合数 C(n,k) |
| `permutation(n, k)` | 排列数 P(n,k) |
| `generate_permutations(items)` | 全排列生成 |
| `generate_combinations(items, k)` | k 组合生成 |
| `power_set(items)` | 幂集生成 |
| `catalan(n)` | 卡特兰数 |
| `stirling_second(n, k)` | 第二类斯特林数 |
| `bell_number(n)` | 贝尔数 |
