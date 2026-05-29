"""
示例2：序列生成器
演示各种序列生成功能
"""

from sequence_utils import (
    arange, linspace, logspace, geometric_sequence,
    fibonacci, tribonacci, lucas_numbers, prime_numbers,
    triangular_numbers, square_numbers, cube_numbers,
    factorial_sequence, golden_sequence
)

print("=== 序列生成器示例 ===")

# 等差数列
print("\n等差数列:")
print(f"arange(0, 10, 2): {arange(0, 10, 2)}")

# 等间隔数列
print("\n等间隔数列:")
print(f"linspace(0, 1, 5): {linspace(0, 1, 5)}")

# 对数等间隔数列
print("\n对数等间隔数列:")
print(f"logspace(0, 2, 5): {logspace(0, 2, 5)}")

# 等比数列
print("\n等比数列:")
print(f"geometric_sequence(1, 2, 5): {geometric_sequence(1, 2, 5)}")

# 斐波那契数列
print("\n斐波那契数列:")
print(f"fibonacci(10): {fibonacci(10)}")

# 三波那契数列
print("\n三波那契数列:")
print(f"tribonacci(10): {tribonacci(10)}")

# 卢卡斯数列
print("\n卢卡斯数列:")
print(f"lucas_numbers(10): {lucas_numbers(10)}")

# 质数
print("\n质数:")
print(f"prime_numbers(10): {prime_numbers(10)}")

# 三角形数
print("\n三角形数:")
print(f"triangular_numbers(5): {triangular_numbers(5)}")

# 平方数
print("\n平方数:")
print(f"square_numbers(5): {square_numbers(5)}")

# 立方数
print("\n立方数:")
print(f"cube_numbers(5): {cube_numbers(5)}")

# 阶乘数列
print("\n阶乘数列:")
print(f"factorial_sequence(5): {factorial_sequence(5)}")

# 黄金比例序列
print("\n黄金比例序列:")
print(f"golden_sequence(5): {golden_sequence(5)}")