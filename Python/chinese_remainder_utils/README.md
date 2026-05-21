# Chinese Remainder Utils

中国剩余定理计算工具，零依赖。

## 功能特性

- **中国剩余定理求解**: 解决同余方程组
- **模数计算**: 支持多个模数
- **验证结果**: 验证解的正确性
- **模逆计算**: 模逆元计算
- **扩展功能**: 模运算工具

## 快速开始

```python
from chinese_remainder_utils.mod import chinese_remainder_theorem

# 解同余方程组
# x ≡ 2 (mod 3)
# x ≡ 3 (mod 5)
# x ≡ 2 (mod 7)

result = chinese_remainder_theorem([2, 3, 2], [3, 5, 7])
print(result)  # 23

# 验证: 23 mod 3 = 2, 23 mod 5 = 3, 23 mod 7 = 2
```

## 使用示例

### 基础求解

```python
from chinese_remainder_utils.mod import crt

# 同余方程组求解
remainders = [1, 2, 3]
moduli = [2, 3, 5]

x = crt(remainders, moduli)
print(x)  # 23

# 验证
assert 23 % 2 == 1
assert 23 % 3 == 2
assert 23 % 5 == 3
```

### 多个解

```python
from chinese_remainder_utils.mod import crt_with_range

# 获取范围内的所有解
remainders = [1, 1]
moduli = [3, 4]

solutions = crt_with_range(remainders, moduli, min_val=0, max_val=100)
print(solutions)  # [1, 13, 25, 37, 49, 61, 73, 85, 97]
```

### 模逆元计算

```python
from chinese_remainder_utils.mod import mod_inverse

# 模逆元: a^-1 mod m
inverse = mod_inverse(3, 11)
print(inverse)  # 4 (因为 3 * 4 = 12 ≡ 1 (mod 11))

# 扩展欧几里得
from chinese_remainder_utils.mod import extended_gcd
gcd, x, y = extended_gcd(35, 15)
print(gcd, x, y)  # 5, 1, -2 (gcd = 35*1 + 15*(-2))
```

### GCD 和 LCM

```python
from chinese_remainder_utils.mod import gcd, lcm

# GCD（最大公约数）
print(gcd(12, 18))  # 6
print(gcd([12, 18, 24]))  # 6

# LCM（最小公倍数）
print(lcm(12, 18))  # 36
print(lcm([12, 18, 24]))  # 72
```

### 互质检查

```python
from chinese_remainder_utils.mod import are_coprime, check_moduli_coprime

# 两数互质检查
print(are_coprime(12, 25))  # True
print(are_coprime(12, 18))  # False

# 检查模数组是否互质
print(check_moduli_coprime([3, 5, 7]))  # True（CRT 有唯一解）
print(check_moduli_coprime([2, 4, 6]))  # False（可能无解或多解）
```

### 验证解

```python
from chinese_remainder_utils.mod import verify_solution

# 验证解是否满足所有同余条件
remainders = [2, 3, 2]
moduli = [3, 5, 7]
solution = 23

is_valid = verify_solution(solution, remainders, moduli)
print(is_valid)  # True
```

## API 参考

| 函数 | 说明 |
|------|------|
| `crt(remainders, moduli)` | 中国剩余定理求解 |
| `chinese_remainder_theorem(rem, mod)` | 同上 |
| `crt_with_range(rem, mod, min, max)` | 范围内所有解 |
| `mod_inverse(a, m)` | 模逆元 |
| `extended_gcd(a, b)` | 扩展欧几里得 |
| `gcd(a, b)` | 最大公约数 |
| `lcm(a, b)` | 最小公倍数 |
| `are_coprime(a, b)` | 互质检查 |
| `check_moduli_coprime(moduli)` | 模数互质检查 |
| `verify_solution(x, rem, mod)` | 解验证 |

## 中国剩余定理

给定同余方程组：
```
x ≡ a1 (mod m1)
x ≡ a2 (mod m2)
...
x ≡ an (mod mn)
```

若模数 m1, m2, ..., mn 两两互质，则存在唯一解：
```
x = Σ ai * Mi * yi (mod M)

其中:
- M = m1 * m2 * ... * mn
- Mi = M / mi
- yi = Mi^-1 mod mi
```

## 应用场景

- **密码学**: RSA 等加密算法
- **数论研究**: 同余方程求解
- **日期计算**: 周期问题
- **调度问题**: 时间冲突解决
- **竞赛编程**: 数论问题

---

**测试覆盖**: 完整测试套件，覆盖 CRT 求解、模逆、GCD/LCM 等