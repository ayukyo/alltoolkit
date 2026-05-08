"""
中国剩余定理工具使用示例

演示各种使用场景：
1. 孙子算经经典问题
2. 干支纪年计算
3. RSA解密加速
4. 实际应用场景
"""

import sys
sys.path.insert(0, '..')

from chinese_remainder_utils.mod import (
    chinese_remainder_theorem,
    crt_garner_method,
    is_solvable,
    all_solutions,
    ganzhi_year,
    year_from_ganzhi,
    rsa_decrypt_crt,
    extended_gcd,
    modular_inverse,
    solve_linear_congruence,
    count_solutions,
    ChineseRemainder
)


def example_1_sunzi_problem():
    """
    示例1：孙子算经经典问题
    
    "有物不知其数，三三数之剩二，五五数之剩三，七七数之剩二，问物几何？"
    """
    print("=" * 60)
    print("示例1：孙子算经经典问题")
    print("=" * 60)
    
    print("\n原题：有物不知其数，三三数之剩二，五五数之剩三，七七数之剩二，问物几何？")
    print("\n翻译：一个数除以3余2，除以5余3，除以7余2，求这个数。")
    
    # 方法1：标准CRT
    result = chinese_remainder_theorem([2, 3, 2], [3, 5, 7])
    print(f"\n方法1 - 标准CRT求解：")
    print(f"  最小正整数解: {result[0]}")
    print(f"  周期: {result[1]}")
    
    # 方法2：Garner方法
    x = crt_garner_method([2, 3, 2], [3, 5, 7])
    print(f"\n方法2 - Garner方法：")
    print(f"  最小正整数解: {x}")
    
    # 验证
    print(f"\n验证：")
    print(f"  {result[0]} ÷ 3 = {result[0] // 3} 余 {result[0] % 3}")
    print(f"  {result[0]} ÷ 5 = {result[0] // 5} 余 {result[0] % 5}")
    print(f"  {result[0]} ÷ 7 = {result[0] // 7} 余 {result[0] % 7}")
    
    # 找更多解
    solutions = all_solutions([2, 3, 2], [3, 5, 7], limit=10)
    print(f"\n前10个解: {solutions}")


def example_2_ganzhi_calendar():
    """
    示例2：干支纪年计算
    
    中国传统的干支纪年法实际上是中国剩余定理的应用。
    """
    print("\n" + "=" * 60)
    print("示例2：干支纪年计算")
    print("=" * 60)
    
    print("\n干支纪年原理：")
    print("  天干：甲乙丙丁戊己庚辛壬癸 (10个)")
    print("  地支：子丑寅卯辰巳午未申酉戌亥 (12个)")
    print("  周期：LCM(10, 12) = 60年")
    
    # 查看近年干支
    print("\n近年干支：")
    years = [1984, 2000, 2008, 2020, 2024, 2025, 2030]
    for year in years:
        gan, zhi = ganzhi_year(year)
        print(f"  {year}年: {gan}{zhi}年")
    
    # 从干支推年份
    print("\n从干支推算年份：")
    ganzhi_pairs = [('甲', '子'), ('庚', '辰'), ('甲', '辰'), ('丙', '申')]
    for gan, zhi in ganzhi_pairs:
        year = year_from_ganzhi(gan, zhi, 21)
        print(f"  {gan}{zhi}年: {year}年")


def example_3_rsa_acceleration():
    """
    示例3：RSA解密加速
    
    使用中国剩余定理可以显著加速RSA解密运算。
    """
    print("\n" + "=" * 60)
    print("示例3：RSA解密加速")
    print("=" * 60)
    
    print("\nRSA-CRT加速原理：")
    print("  1. 将 c^d mod n 分解为两个较小的模幂运算")
    print("  2. 分别计算 m1 = c^d mod p 和 m2 = c^d mod q")
    print("  3. 使用CRT合并结果")
    print("  4. 当p≈q≈√n时，效率提升约4倍")
    
    # 示例
    p, q = 61, 53
    n = p * q
    e, d = 17, 2753
    
    print(f"\n参数：")
    print(f"  p = {p}, q = {q}")
    print(f"  n = p × q = {n}")
    print(f"  公钥 e = {e}, 私钥 d = {d}")
    
    # 加密解密
    messages = [42, 123, 456, 789]
    print(f"\n加解密测试：")
    
    for m in messages:
        c = pow(m, e, n)
        decrypted = rsa_decrypt_crt(c, d, p, q)
        print(f"  明文: {m} → 密文: {c} → 解密: {decrypted} {'✓' if m == decrypted else '✗'}")


def example_4_extended_gcd_applications():
    """
    示例4：扩展欧几里得算法应用
    """
    print("\n" + "=" * 60)
    print("示例4：扩展欧几里得算法应用")
    print("=" * 60)
    
    # 求最大公约数和Bézout系数
    print("\n1. 求最大公约数和Bézout系数：")
    pairs = [(35, 15), (240, 46), (17, 13)]
    for a, b in pairs:
        gcd, x, y = extended_gcd(a, b)
        print(f"  gcd({a}, {b}) = {gcd}")
        print(f"  Bézout等式: {a} × {x} + {b} × {y} = {a*x + b*y}")
    
    # 求模逆元
    print("\n2. 求模逆元：")
    inverse_cases = [(3, 7), (7, 26), (17, 101)]
    for a, m in inverse_cases:
        inv = modular_inverse(a, m)
        print(f"  {a}^(-1) mod {m} = {inv}")
        print(f"  验证: {a} × {inv} mod {m} = {(a * inv) % m}")


def example_5_linear_congruence():
    """
    示例5：线性同余方程
    """
    print("\n" + "=" * 60)
    print("示例5：线性同余方程求解")
    print("=" * 60)
    
    equations = [
        (3, 6, 9),   # 3x ≡ 6 (mod 9)
        (5, 3, 7),   # 5x ≡ 3 (mod 7)
        (2, 3, 4),   # 2x ≡ 3 (mod 4) - 无解
    ]
    
    for a, b, m in equations:
        print(f"\n求解: {a}x ≡ {b} (mod {m})")
        solutions = solve_linear_congruence(a, b, m)
        if solutions:
            print(f"  解: {solutions}")
            for sol in solutions:
                print(f"  验证: {a} × {sol} mod {m} = {(a * sol) % m}")
        else:
            print(f"  无解 (因为 gcd({a},{m}) = {extended_gcd(a, m)[0]} 不整除 {b})")


def example_6_practical_applications():
    """
    示例6：实际应用场景
    """
    print("\n" + "=" * 60)
    print("示例6：实际应用场景")
    print("=" * 60)
    
    # 场景1：任务调度
    print("\n场景1 - 任务调度：")
    print("  任务A每3天执行，任务B每5天执行，任务C每7天执行")
    print("  如果今天都执行，下次都执行是什么时候？")
    result = chinese_remainder_theorem([0, 0, 0], [3, 5, 7])
    print(f"  答案: {result[0]} 天后 (即{result[1]}天周期)")
    
    # 场景2：计数问题
    print("\n场景2 - 计数问题：")
    print("  一个班级的学生，按3人一组剩1人，按5人一组剩2人，按7人一组剩3人")
    print("  问班级至少有多少人？")
    result = chinese_remainder_theorem([1, 2, 3], [3, 5, 7])
    print(f"  答案: 至少 {result[0]} 人")
    
    # 场景3：密码锁
    print("\n场景3 - 密码锁破解：")
    print("  一个密码锁，每次转动给出不同的余数提示...")
    print("  第1个齿轮转完显示余2（模3）")
    print("  第2个齿轮转完显示余3（模5）")
    print("  第3个齿轮转完显示余2（模7）")
    result = chinese_remainder_theorem([2, 3, 2], [3, 5, 7])
    print(f"  密码可能是: {all_solutions([2, 3, 2], [3, 5, 7], limit=5)}")
    print(f"  最小密码: {result[0]}")


def example_7_chinese_remainder_class():
    """
    示例7：使用ChineseRemainder类
    """
    print("\n" + "=" * 60)
    print("示例7：ChineseRemainder类（批量求解）")
    print("=" * 60)
    
    # 预计算，适用于多次求解相同模数的情况
    crt = ChineseRemainder([3, 5, 7])
    
    print("\n初始化求解器，模数为 [3, 5, 7]")
    print(f"解的周期: {crt.get_period()}")
    
    problems = [
        ([2, 3, 2], "孙子问题"),
        ([1, 2, 3], "简单例子"),
        ([0, 0, 0], "整除情况"),
        ([2, 1, 6], "另一组"),
    ]
    
    print("\n批量求解：")
    for remainders, desc in problems:
        solution = crt.solve(remainders)
        all_sols = crt.get_all_solutions(remainders, count=3)
        print(f"  {desc}: 余数{remainders} → 解{solution} (前3个: {all_sols})")


def example_8_counting_solutions():
    """
    示例8：解的计数
    """
    print("\n" + "=" * 60)
    print("示例8：解的计数")
    print("=" * 60)
    
    print("\n问题：在1到10000之间，满足以下条件的数有多少个？")
    print("  除以3余2，除以5余3，除以7余2")
    
    count = count_solutions([2, 3, 2], [3, 5, 7], 10000)
    print(f"  答案: {count} 个")
    
    # 验证
    solutions = all_solutions([2, 3, 2], [3, 5, 7], limit=count)
    in_range = [s for s in solutions if s <= 10000]
    print(f"  验证: 找到了 {len(in_range)} 个不超过10000的解")


def main():
    """运行所有示例"""
    example_1_sunzi_problem()
    example_2_ganzhi_calendar()
    example_3_rsa_acceleration()
    example_4_extended_gcd_applications()
    example_5_linear_congruence()
    example_6_practical_applications()
    example_7_chinese_remainder_class()
    example_8_counting_solutions()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()