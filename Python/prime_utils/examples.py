"""
Prime Number Utilities - 使用示例

演示素数工具包的各种用法。
"""

import sys
import os
import time

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prime_utils import (
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


def print_section(title):
    """打印章节标题"""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print('='*50)


def demo_is_prime():
    """演示素数判断"""
    print_section("素数判断")
    
    # 小数判断
    numbers = [1, 2, 3, 4, 5, 17, 18, 19, 561]
    print("小数素数判断:")
    for n in numbers:
        result = "素数" if is_prime(n) else "合数"
        print(f"  {n}: {result}")
    
    # 大数判断（使用 Miller-Rabin）
    print("\n大数素数判断:")
    large_numbers = [
        (2**31 - 1, "梅森素数 M31"),
        (2**61 - 1, "梅森素数 M61"),
        (999999999989, "12位素数"),
        (561, "卡迈克尔数（伪素数）"),
    ]
    for n, desc in large_numbers:
        start = time.time()
        result = is_prime(n)
        elapsed = (time.time() - start) * 1000
        status = "素数✓" if result else "合数✗"
        print(f"  {n} ({desc}): {status} [{elapsed:.2f}ms]")


def demo_generate_primes():
    """演示素数生成"""
    print_section("素数生成（埃拉托斯特尼筛法）")
    
    # 生成小范围素数
    print("100以内的素数:")
    primes = generate_primes(100)
    print(f"  {primes}")
    print(f"  共 {len(primes)} 个")
    
    # 大范围素数统计
    print("\n素数统计:")
    limits = [100, 1000, 10000, 100000]
    for limit in limits:
        start = time.time()
        primes = generate_primes(limit)
        elapsed = (time.time() - start) * 1000
        print(f"  {limit:,} 以内: {len(primes)} 个素数 [{elapsed:.2f}ms]")


def demo_prime_factors():
    """演示素因数分解"""
    print_section("素因数分解")
    
    numbers = [60, 100, 1024, 123456789, 999999999989]
    
    for n in numbers:
        factors = prime_factors(n)
        factor_str = " × ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in factors)
        print(f"  {n:,} = {factor_str}")


def demo_euler_phi():
    """演示欧拉函数"""
    print_section("欧拉函数 φ(n)")
    
    print("欧拉函数值:")
    for n in range(1, 21):
        phi = euler_phi(n)
        print(f"  φ({n:2d}) = {phi:2d}  ", end="")
        if n % 5 == 0:
            print()
    
    print("\n素数的欧拉函数值（φ(p) = p-1）:")
    for p in generate_primes(20):
        print(f"  φ({p}) = {euler_phi(p)}")


def demo_gcd_lcm():
    """演示GCD和LCM"""
    print_section("最大公约数和最小公倍数")
    
    pairs = [(48, 18), (100, 25), (17, 13), (120, 45)]
    
    print("GCD 和 LCM:")
    for a, b in pairs:
        g = gcd(a, b)
        l = lcm(a, b)
        print(f"  gcd({a}, {b}) = {g}")
        print(f"  lcm({a}, {b}) = {l}")
        print(f"  验证: {a} × {b} = gcd × lcm = {g} × {l} = {g * l}")
        print()


def demo_extended_gcd():
    """演示扩展欧几里得算法"""
    print_section("扩展欧几里得算法")
    
    print("求解 ax + by = gcd(a,b):")
    pairs = [(35, 15), (17, 13), (120, 23)]
    
    for a, b in pairs:
        g, x, y = extended_gcd(a, b)
        print(f"  {a} × ({x}) + {b} × ({y}) = {g}")
        print(f"  验证: {a * x + b * y} = {g}")
        print()


def demo_mod_inverse():
    """演示模逆元"""
    print_section("模逆元（乘法逆元）")
    
    print("求 a 在模 m 下的逆元 x，使得 ax ≡ 1 (mod m):")
    
    pairs = [(3, 11), (7, 11), (5, 12)]
    for a, m in pairs:
        inv = mod_inverse(a, m)
        if inv:
            print(f"  {a}⁻¹ mod {m} = {inv}")
            print(f"  验证: {a} × {inv} = {a * inv} ≡ {a * inv % m} (mod {m})")
        else:
            print(f"  {a}⁻¹ mod {m} = 不存在（gcd({a},{m}) ≠ 1）")
        print()


def demo_adjacent_primes():
    """演示相邻素数"""
    print_section("相邻素数")
    
    print("找下一个素数:")
    for n in [10, 100, 1000, 10000]:
        p = next_prime(n)
        print(f"  大于 {n} 的最小素数: {p}")
    
    print("\n找前一个素数:")
    for n in [10, 100, 1000, 10000]:
        p = prev_prime(n)
        if p:
            print(f"  小于 {n} 的最大素数: {p}")


def demo_nth_prime():
    """演示第n个素数"""
    print_section("第 n 个素数")
    
    print("前10个素数:")
    for i in range(1, 11):
        print(f"  第 {i:2d} 个素数: {nth_prime(i)}")
    
    print("\n其他位置:")
    positions = [100, 500, 1000, 5000]
    for n in positions:
        start = time.time()
        p = nth_prime(n)
        elapsed = (time.time() - start) * 1000
        print(f"  第 {n:,} 个素数: {p:,} [{elapsed:.2f}ms]")


def demo_coprime():
    """演示互质判断"""
    print_section("互质判断")
    
    pairs = [(15, 28), (12, 18), (17, 13), (8, 9), (21, 22)]
    
    for a, b in pairs:
        g = gcd(a, b)
        coprime = is_coprime(a, b)
        status = "互质✓" if coprime else f"不互质（gcd={g}）"
        print(f"  ({a}, {b}): {status}")


def demo_rsa_example():
    """演示RSA加密中的素数应用"""
    print_section("RSA加密示例（演示用途）")
    
    # 选择两个素数
    p, q = 61, 53
    print(f"选择两个素数: p = {p}, q = {q}")
    
    # 计算n和φ(n)
    n = p * q
    phi = euler_phi(n)
    print(f"n = p × q = {n}")
    print(f"φ(n) = (p-1)(q-1) = {phi}")
    
    # 选择公钥指数e
    e = 17
    print(f"公钥指数 e = {e}")
    
    # 计算私钥d
    d = mod_inverse(e, phi)
    print(f"私钥指数 d = e⁻¹ mod φ(n) = {d}")
    print(f"验证: e × d mod φ(n) = {(e * d) % phi}")
    
    # 加密和解密
    message = 42
    encrypted = pow(message, e, n)
    decrypted = pow(encrypted, d, n)
    print(f"\n消息: {message}")
    print(f"加密: {message}^{e} mod {n} = {encrypted}")
    print(f"解密: {encrypted}^{d} mod {n} = {decrypted}")


def demo_generator():
    """演示生成器用法"""
    print_section("素数生成器（节省内存）")
    
    print("使用生成器处理大范围:")
    count = 0
    last_prime = None
    start = time.time()
    
    for p in primes_up_to(100000):
        count += 1
        last_prime = p
    
    elapsed = (time.time() - start) * 1000
    print(f"  100,000 以内有 {count} 个素数")
    print(f"  最大的素数是 {last_prime}")
    print(f"  耗时: {elapsed:.2f}ms")


def main():
    """运行所有示例"""
    print("\n" + "="*50)
    print("  Prime Number Utilities - 使用示例")
    print("="*50)
    
    demo_is_prime()
    demo_generate_primes()
    demo_prime_factors()
    demo_euler_phi()
    demo_gcd_lcm()
    demo_extended_gcd()
    demo_mod_inverse()
    demo_adjacent_primes()
    demo_nth_prime()
    demo_coprime()
    demo_rsa_example()
    demo_generator()
    
    print("\n" + "="*50)
    print("  示例演示完成！")
    print("="*50 + "\n")


if __name__ == "__main__":
    main()