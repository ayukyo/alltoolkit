"""
数学工具模块使用示例
"""

from math_utils import MathUtils


def example_basic_operations():
    """基础运算示例"""
    print("=" * 50)
    print("基础运算示例")
    print("=" * 50)
    
    # 阶乘
    print(f"5! = {MathUtils.factorial(5)}")
    print(f"10! = {MathUtils.factorial(10)}")
    
    # 斐波那契数列
    print(f"\n第 10 个斐波那契数: {MathUtils.fibonacci(10)}")
    print(f"前 15 个斐波那契数: {MathUtils.fibonacci_sequence(15)}")
    
    # 最大公约数和最小公倍数
    print(f"\ngcd(48, 18) = {MathUtils.gcd(48, 18)}")
    print(f"gcd(48, 18, 12) = {MathUtils.gcd(48, 18, 12)}")
    print(f"lcm(4, 6) = {MathUtils.lcm(4, 6)}")
    print(f"lcm(4, 6, 8) = {MathUtils.lcm(4, 6, 8)}")
    
    # 幂运算和根
    print(f"\n2^10 = {MathUtils.power(2, 10)}")
    print(f"sqrt(16) = {MathUtils.sqrt(16)}")
    print(f"cbrt(27) = {MathUtils.cbrt(27)}")
    print(f"4th root of 16 = {MathUtils.root(16, 4)}")
    
    # 符号和绝对值
    print(f"\nabs(-5) = {MathUtils.abs(-5)}")
    print(f"sign(-10) = {MathUtils.sign(-10)}")
    print(f"sign(0) = {MathUtils.sign(0)}")
    print(f"sign(10) = {MathUtils.sign(10)}")


def example_number_theory():
    """数论示例"""
    print("\n" + "=" * 50)
    print("数论示例")
    print("=" * 50)
    
    # 素数检测
    primes = [n for n in range(2, 50) if MathUtils.is_prime(n)]
    print(f"50 以内的素数: {primes}")
    
    # 使用筛法生成素数
    print(f"\n使用筛法生成 50 以内的素数: {MathUtils.primes_up_to(50)}")
    
    # 质因数分解
    numbers = [60, 84, 100, 97]
    for n in numbers:
        print(f"{n} 的质因数分解: {MathUtils.prime_factors(n)}")
    
    # 因数
    print(f"\n12 的所有因数: {MathUtils.divisors(12)}")
    print(f"12 的因数个数: {MathUtils.count_divisors(12)}")
    
    # 欧拉函数
    print(f"\nφ(9) = {MathUtils.euler_totient(9)}")
    print(f"φ(10) = {MathUtils.euler_totient(10)}")
    
    # 完全数
    perfects = [n for n in range(1, 10000) if MathUtils.is_perfect_number(n)]
    print(f"\n10000 以内的完全数: {perfects}")


def example_geometry():
    """几何计算示例"""
    print("\n" + "=" * 50)
    print("几何计算示例")
    print("=" * 50)
    
    # 距离计算
    print(f"点 (0,0) 到点 (3,4) 的距离: {MathUtils.distance_2d((0, 0), (3, 4))}")
    print(f"点 (0,0,0) 到点 (1,2,2) 的距离: {MathUtils.distance_3d((0, 0, 0), (1, 2, 2))}")
    
    # 圆和球
    print(f"\n半径为 1 的圆面积: {MathUtils.circle_area(1):.4f}")
    print(f"半径为 1 的圆周长: {MathUtils.circle_circumference(1):.4f}")
    print(f"半径为 1 的球体积: {MathUtils.sphere_volume(1):.4f}")
    print(f"半径为 1 的球表面积: {MathUtils.sphere_surface_area(1):.4f}")
    
    # 矩形和三角形
    print(f"\n矩形 (5 x 3) 面积: {MathUtils.rectangle_area(5, 3)}")
    print(f"三角形 (底=6, 高=4) 面积: {MathUtils.triangle_area(6, 4)}")
    print(f"三角形 (边长 3,4,5) 面积 (海伦公式): {MathUtils.triangle_area_heron(3, 4, 5)}")
    
    # 圆柱和圆锥
    print(f"\n圆柱体 (半径=3, 高=5) 体积: {MathUtils.cylinder_volume(3, 5):.4f}")
    print(f"圆锥体 (半径=3, 高=5) 体积: {MathUtils.cone_volume(3, 5):.4f}")
    
    # 向量夹角
    angle = MathUtils.angle_between_vectors((1, 0), (0, 1))
    print(f"\n向量 (1,0) 和 (0,1) 的夹角: {angle:.4f} 弧度 ({angle * 180 / 3.14159:.2f}°)")


def example_statistics():
    """统计示例"""
    print("\n" + "=" * 50)
    print("统计示例")
    print("=" * 50)
    
    data = [12, 15, 18, 22, 25, 28, 30, 33, 35, 40]
    
    print(f"数据: {data}")
    print(f"平均值: {MathUtils.mean(data):.2f}")
    print(f"中位数: {MathUtils.median(data):.2f}")
    print(f"众数: {MathUtils.mode(data)}")
    print(f"方差: {MathUtils.variance(data):.2f}")
    print(f"标准差: {MathUtils.standard_deviation(data):.2f}")
    print(f"极差: {MathUtils.range_value(data)}")
    
    # 百分位数
    print(f"\n第 25 百分位数: {MathUtils.percentile(data, 25):.2f}")
    print(f"第 50 百分位数: {MathUtils.percentile(data, 50):.2f}")
    print(f"第 75 百分位数: {MathUtils.percentile(data, 75):.2f}")
    
    # 四分位数
    q1, q2, q3 = MathUtils.quartiles(data)
    print(f"\n四分位数: Q1={q1:.2f}, Q2={q2:.2f}, Q3={q3:.2f}")
    print(f"四分位距 (IQR): {MathUtils.iqr(data):.2f}")
    
    # 相关性分析
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y1 = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]  # 完全正相关
    y2 = [20, 18, 16, 14, 12, 10, 8, 6, 4, 2]  # 完全负相关
    y3 = [5, 3, 8, 1, 9, 2, 7, 4, 6, 10]  # 无相关
    
    print(f"\n相关性分析:")
    print(f"x 与 y1 (正相关): {MathUtils.correlation(x, y1):.4f}")
    print(f"x 与 y2 (负相关): {MathUtils.correlation(x, y2):.4f}")
    print(f"x 与 y3 (无相关): {MathUtils.correlation(x, y3):.4f}")


def example_numeric_operations():
    """数值处理示例"""
    print("\n" + "=" * 50)
    print("数值处理示例")
    print("=" * 50)
    
    pi = 3.14159265358979
    
    # 四舍五入
    print(f"圆周率: {pi}")
    print(f"四舍五入到 2 位小数: {MathUtils.round_to(pi, 2)}")
    print(f"四舍五入到 4 位小数: {MathUtils.round_to(pi, 4)}")
    
    # 向上/向下取整
    print(f"\n向上取整 3.14 到 1 位小数: {MathUtils.round_up(3.14, 1)}")
    print(f"向下取整 3.19 到 1 位小数: {MathUtils.round_down(3.19, 1)}")
    print(f"截断 3.14159 到 2 位小数: {MathUtils.truncate(3.14159, 2)}")
    
    # 范围限制
    print(f"\nclamp(10, 0, 5) = {MathUtils.clamp(10, 0, 5)}")
    print(f"clamp(-1, 0, 5) = {MathUtils.clamp(-1, 0, 5)}")
    print(f"clamp(3, 0, 5) = {MathUtils.clamp(3, 0, 5)}")
    
    # 百分比计算
    print(f"\n25 是 200 的 {MathUtils.percentage(25, 200)}%")
    print(f"从 100 到 150 的百分比变化: {MathUtils.percentage_change(100, 150)}%")
    print(f"从 100 到 80 的百分比变化: {MathUtils.percentage_change(100, 80)}%")
    print(f"比率 0.75 转百分比: {MathUtils.ratio_to_percentage(0.75)}%")


def example_vectors():
    """向量运算示例"""
    print("\n" + "=" * 50)
    print("向量运算示例")
    print("=" * 50)
    
    v1 = (1, 2, 3)
    v2 = (4, 5, 6)
    
    print(f"向量 v1 = {v1}")
    print(f"向量 v2 = {v2}")
    print(f"v1 + v2 = {MathUtils.vector_add(v1, v2)}")
    print(f"v1 - v2 = {MathUtils.vector_subtract(v1, v2)}")
    print(f"v1 * 2 = {MathUtils.vector_scale(v1, 2)}")
    print(f"v1 · v2 = {MathUtils.vector_dot(v1, v2)}")
    print(f"v1 × v2 = {MathUtils.vector_cross_3d(v1, v2)}")
    print(f"|v1| = {MathUtils.vector_magnitude(v1):.4f}")
    print(f"|v2| = {MathUtils.vector_magnitude(v2):.4f}")
    
    # 归一化
    normalized = MathUtils.vector_normalize(v1)
    print(f"v1 归一化 = {normalized}")
    print(f"归一化后模长 = {MathUtils.vector_magnitude(normalized):.4f}")


def example_sequences():
    """序列生成示例"""
    print("\n" + "=" * 50)
    print("序列生成示例")
    print("=" * 50)
    
    # 等差数列
    print("等差数列 (首项=1, 公差=2, 10项):")
    seq = MathUtils.arithmetic_sequence(1, 2, 10)
    print(f"序列: {seq}")
    print(f"前 10 项和: {MathUtils.arithmetic_sum(1, 2, 10)}")
    
    # 等比数列
    print("\n等比数列 (首项=1, 公比=2, 10项):")
    seq = MathUtils.geometric_sequence(1, 2, 10)
    print(f"序列: {seq}")
    print(f"前 10 项和: {MathUtils.geometric_sum(1, 2, 10)}")
    
    # 浮点数范围
    print("\n浮点数范围 (0 到 1, 步长 0.2):")
    print(f"{MathUtils.range_float(0, 1, 0.2)}")
    
    # 等间距数列
    print("\n等间距数列 (0 到 10, 6 个点):")
    print(f"{MathUtils.linspace(0, 10, 6)}")


def example_numeric_checks():
    """数值检查示例"""
    print("\n" + "=" * 50)
    print("数值检查示例")
    print("=" * 50)
    
    # 奇偶数
    print(f"2 是偶数: {MathUtils.is_even(2)}")
    print(f"3 是奇数: {MathUtils.is_odd(3)}")
    
    # 幂次
    print(f"\n8 是 2 的幂次: {MathUtils.is_power_of(8, 2)}")
    print(f"10 是 2 的幂次: {MathUtils.is_power_of(10, 2)}")
    
    # 完全平方/立方数
    print(f"\n16 是完全平方数: {MathUtils.is_perfect_square(16)}")
    print(f"27 是完全立方数: {MathUtils.is_perfect_cube(27)}")
    
    # 阿姆斯特朗数
    armstrong_nums = [n for n in range(1, 1000) if MathUtils.is_armstrong(n)]
    print(f"\n1000 以内的阿姆斯特朗数: {armstrong_nums}")
    
    # 回文数
    palindromes = [n for n in range(10, 200) if MathUtils.is_palindrome_number(n)]
    print(f"\n200 以内的回文数: {palindromes}")


def example_random():
    """随机函数示例"""
    print("\n" + "=" * 50)
    print("随机函数示例")
    print("=" * 50)
    
    # 随机整数
    print(f"随机整数 (1-100): {[MathUtils.random_int(1, 100) for _ in range(5)]}")
    
    # 随机浮点数
    print(f"随机浮点数 (0-1): {[round(MathUtils.random_float(), 4) for _ in range(5)]}")
    
    # 随机选择
    items = ['苹果', '香蕉', '橙子', '葡萄', '西瓜']
    print(f"从 {items} 中随机选择: {MathUtils.random_choice(items)}")
    
    # 随机抽样
    print(f"随机抽样 3 个: {MathUtils.random_sample(items, 3)}")
    
    # 打乱列表
    numbers = [1, 2, 3, 4, 5]
    print(f"原列表: {numbers}")
    print(f"打乱后: {MathUtils.shuffle(numbers)}")
    print(f"原列表不变: {numbers}")


if __name__ == '__main__':
    example_basic_operations()
    example_number_theory()
    example_geometry()
    example_statistics()
    example_numeric_operations()
    example_vectors()
    example_sequences()
    example_numeric_checks()
    example_random()
    
    print("\n" + "=" * 50)
    print("所有示例运行完成!")
    print("=" * 50)