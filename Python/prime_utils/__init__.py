"""
Prime Number Utilities - 素数工具包

提供素数相关的数学计算功能，包括：
- 素数检测 (Miller-Rabin 算法)
- 素数生成
- 素因数分解
- 欧拉函数
- 最大公约数/最小公倍数

零外部依赖，纯 Python 实现。
"""

from .prime_utils import (
    is_prime,
    is_prime_simple,
    generate_primes,
    prime_factors,
    euler_phi,
    gcd,
    lcm,
    next_prime,
    prev_prime,
    count_primes,
    nth_prime,
    is_coprime,
    extended_gcd,
    mod_inverse,
    primes_up_to,
)

__all__ = [
    "is_prime",
    "is_prime_simple",
    "generate_primes",
    "prime_factors",
    "euler_phi",
    "gcd",
    "lcm",
    "next_prime",
    "prev_prime",
    "count_primes",
    "nth_prime",
    "is_coprime",
    "extended_gcd",
    "mod_inverse",
    "primes_up_to",
]

__version__ = "1.0.0"