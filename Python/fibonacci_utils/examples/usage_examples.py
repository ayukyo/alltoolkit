"""
Fibonacci Utils 使用示例

演示斐波那契工具的各种功能
"""

import sys
sys.path.insert(0, '..')
from mod import FibonacciUtils, generate, nth, is_fibonacci, zeckendorf, golden_ratio


def print_section(title: str) -> None:
    """打印分隔线和标题"""
    print(f"\n{'=' * 50}")
    print(f"  {title}")
    print('=' * 50)


def main():
    print("\n" + "🧮 " * 20)
    print("     斐波那契工具集 - Fibonacci Utils")
    print("🧮 " * 20)
    
    # 1. 基本生成
    print_section("1. 基本斐波那契数列生成")
    fibs = FibonacciUtils.generate(15)
    print(f"前15个斐波那契数: {fibs}")
    print(f"使用便捷函数: {generate(15)}")
    
    # 2. 计算第N个斐波那契数
    print_section("2. 计算第N个斐波那契数")
    n = 20
    print(f"第{n}个斐波那契数 (迭代法): {FibonacciUtils.nth_iterative(n)}")
    print(f"第{n}个斐波那契数 (递归法): {FibonacciUtils.nth_recursive(n)}")
    print(f"第{n}个斐波那契数 (矩阵法): {FibonacciUtils.nth_matrix(n)}")
    print(f"第{n}个斐波那契数 (比内公式): {FibonacciUtils.nth_binet(n)}")
    print(f"使用便捷函数 nth({n}): {nth(n)}")
    
    # 3. 大数计算
    print_section("3. 大数计算")
    for n in [50, 100]:
        fib_n = FibonacciUtils.nth_matrix(n)
        digits = FibonacciUtils.count_digits(n)
        print(f"F({n}) = {fib_n}")
        print(f"    位数: {digits}")
    
    # 4. 判断斐波那契数
    print_section("4. 判断是否为斐波那契数")
    test_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 55, 56, 89, 144, 145]
    for num in test_numbers:
        is_fib = FibonacciUtils.is_fibonacci(num)
        status = "✅ 是" if is_fib else "❌ 否"
        print(f"{num:4d} -> {status}斐波那契数")
    
    # 5. 查找最近斐波那契数
    print_section("5. 查找最近的斐波那契数")
    test_values = [10, 50, 100, 200, 500, 1000]
    for val in test_values:
        nearest, idx = FibonacciUtils.nearest_fibonacci(val)
        diff = val - nearest
        direction = "低" if diff > 0 else "高" if diff < 0 else "精确"
        print(f"{val:4d} -> F({idx:2d}) = {nearest:4d} ({direction}{abs(diff)})")
    
    # 6. Zeckendorf表示
    print_section("6. Zeckendorf表示 (斐波那契分解)")
    test_nums = [1, 10, 50, 100, 256, 500, 1000]
    for num in test_nums:
        rep = FibonacciUtils.zeckendorf_representation(num)
        parts = FibonacciUtils.zeckendorf(num)
        print(f"{rep}")
        print(f"    分解: {parts}")
    
    # 7. 范围内斐波那契数
    print_section("7. 范围内的斐波那契数")
    ranges = [(0, 50), (50, 200), (100, 1000)]
    for start, end in ranges:
        fibs_in_range = FibonacciUtils.range(start, end)
        print(f"[{start}, {end}): {fibs_in_range}")
    
    # 8. 前N个斐波那契数之和
    print_section("8. 前N个斐波那契数之和")
    for n in [5, 10, 15, 20]:
        total = FibonacciUtils.sum_first_n(n)
        print(f"F(0) + F(1) + ... + F({n-1}) = {total}")
    
    # 9. 黄金比例
    print_section("9. 黄金比例近似")
    for precision in [5, 10, 20, 50, 100]:
        phi = FibonacciUtils.golden_ratio(precision)
        print(f"使用前{precision:3d}个斐波那契数: φ ≈ {phi:.15f}")
    print(f"真实黄金比例:           φ = {(1 + 5**0.5)/2:.15f}")
    
    # 10. 卢卡斯数列
    print_section("10. 卢卡斯数列")
    lucas_nums = [FibonacciUtils.lucas_number(i) for i in range(15)]
    print(f"前15个卢卡斯数: {lucas_nums}")
    
    # 11. 皮萨诺周期
    print_section("11. 皮萨诺周期 (模周期)")
    moduli = [2, 3, 5, 7, 10, 100]
    for m in moduli:
        period = FibonacciUtils.pisano_period(m)
        print(f"F(n) mod {m:3d} 的周期长度: {period}")
    
    # 12. 模运算
    print_section("12. 斐波那契模运算")
    n, m = 100, 7
    result = FibonacciUtils.nth_mod(n, m)
    print(f"F({n}) mod {m} = {result}")
    
    # 13. 斐波那契数的GCD
    print_section("13. 斐波那契数的最大公约数")
    pairs = [(6, 9), (12, 18), (8, 12), (15, 25)]
    for a, b in pairs:
        gcd_fib = FibonacciUtils.gcd_fibonacci(a, b)
        print(f"gcd(F({a}), F({b})) = F(gcd({a},{b})) = F({__import__('math').gcd(a,b)}) = {gcd_fib}")
    
    # 14. 迭代器使用
    print_section("14. 斐波那契迭代器")
    it = FibonacciUtils.fibonacci_iterator()
    first_10 = [next(it) for _ in range(10)]
    print(f"迭代器生成前10个: {first_10}")
    
    # 15. 查找索引
    print_section("15. 查找斐波那契数索引")
    test_fibs = [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
    for fib in test_fibs:
        idx = FibonacciUtils.find_index(fib)
        print(f"F({idx:2d}) = {fib}")
    
    print("\n" + "=" * 50)
    print("  所有示例演示完成!")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()