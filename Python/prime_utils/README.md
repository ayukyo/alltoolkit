# Prime Number Utilities - 素数工具包

Python 实现的素数数学工具集，零外部依赖。

## 功能列表

| 函数 | 描述 |
|------|------|
| `is_prime(n)` | 使用 Miller-Rabin 算法判断素数（支持大数） |
| `is_prime_simple(n)` | 使用试除法判断素数（适合小数） |
| `generate_primes(limit)` | 使用埃拉托斯特尼筛法生成素数列表 |
| `prime_factors(n)` | 素因数分解，返回素数及指数 |
| `euler_phi(n)` | 计算欧拉函数 φ(n) |
| `gcd(a, b)` | 最大公约数 |
| `lcm(a, b)` | 最小公倍数 |
| `extended_gcd(a, b)` | 扩展欧几里得算法 |
| `mod_inverse(a, m)` | 模逆元（乘法逆元） |
| `next_prime(n)` | 下一个素数 |
| `prev_prime(n)` | 前一个素数 |
| `nth_prime(n)` | 第 n 个素数 |
| `count_primes(n)` | 素数计数函数 π(n) |
| `is_coprime(a, b)` | 判断两数是否互质 |
| `primes_up_to(n)` | 生成器版本的素数序列 |

## 安装使用

```python
from prime_utils import is_prime, generate_primes, prime_factors

# 判断素数
print(is_prime(17))  # True
print(is_prime(2**31 - 1))  # True（梅森素数）

# 生成素数
primes = generate_primes(100)
print(primes)  # [2, 3, 5, 7, 11, 13, 17, 19, ...]

# 素因数分解
print(prime_factors(60))  # [(2, 2), (3, 1), (5, 1)]
```

## 核心算法

### Miller-Rabin 素数测试

```python
from prime_utils import is_prime

# 小数（确定性测试）
print(is_prime(17))  # True

# 大数（概率性测试，确定性基）
print(is_prime(2**61 - 1))  # True（梅森素数）

# 卡迈克尔数（伪素数检测）
print(is_prime(561))  # False
```

### 素因数分解

```python
from prime_utils import prime_factors

# 分解质因数
print(prime_factors(123456789))
# [(3, 2), (3607, 1), (3803, 1)]
# 解释: 123456789 = 3² × 3607 × 3803
```

### RSA加密示例

```python
from prime_utils import euler_phi, mod_inverse, is_prime

# 选择两个素数
p, q = 61, 53

# 计算 n 和 φ(n)
n = p * q
phi = euler_phi(n)  # 3120

# 选择公钥指数并计算私钥
e = 17
d = mod_inverse(e, phi)  # 2753

# 加密解密
message = 42
encrypted = pow(message, e, n)
decrypted = pow(encrypted, d, n)
print(f"原始: {message}, 解密: {decrypted}")  # 42
```

## 运行测试

```bash
cd Python/prime_utils
python prime_utils_test.py
```

## 运行示例

```bash
cd Python/prime_utils
python examples.py
```

## 许可证

MIT License