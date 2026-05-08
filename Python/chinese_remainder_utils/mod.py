"""
Chinese Remainder Theorem (CRT) Utils
中国剩余定理工具模块

中国剩余定理是数论中的重要定理，用于求解同余方程组。
经典问题："有物不知其数，三三数之剩二，五五数之剩三，七七数之剩二，问物几何？"

Features:
- 扩展欧几里得算法 (Extended Euclidean Algorithm)
- 模逆运算 (Modular Inverse)
- 中国剩余定理求解 (CRT Solver)
- 支持任意数量的同余方程
- 干支纪年计算应用
- RSA解密加速应用
"""

from typing import List, Tuple, Optional
import math


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    扩展欧几里得算法
    
    计算 gcd(a, b) 以及满足 ax + by = gcd(a, b) 的整数 x, y
    
    Args:
        a: 第一个整数
        b: 第二个整数
    
    Returns:
        (gcd, x, y) 其中 gcd 是最大公约数，x, y 满足 ax + by = gcd
    
    Examples:
        >>> extended_gcd(35, 15)
        (5, 1, -2)  # 35*1 + 15*(-2) = 5
        >>> extended_gcd(240, 46)
        (2, -9, 47)  # 240*(-9) + 46*47 = 2
    """
    if b == 0:
        return a, 1, 0
    
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    
    return gcd, x, y


def modular_inverse(a: int, m: int) -> Optional[int]:
    """
    计算模逆元
    
    找到 x 使得 ax ≡ 1 (mod m)
    
    Args:
        a: 要求逆元的数
        m: 模数
    
    Returns:
        a 模 m 的逆元，如果不存在则返回 None
    
    Examples:
        >>> modular_inverse(3, 7)
        5  # 因为 3*5 = 15 ≡ 1 (mod 7)
        >>> modular_inverse(2, 4)
        None  # gcd(2,4)=2≠1，逆元不存在
    """
    gcd, x, _ = extended_gcd(a, m)
    
    if gcd != 1:
        return None
    
    return (x % m + m) % m


def crt_two_equations(a1: int, m1: int, a2: int, m2: int) -> Optional[Tuple[int, int]]:
    """
    求解两个同余方程的方程组
    
    求解:
        x ≡ a1 (mod m1)
        x ≡ a2 (mod m2)
    
    Args:
        a1, m1: 第一个同余方程的参数
        a2, m2: 第二个同余方程的参数
    
    Returns:
        (x, M) 其中 x 是最小正整数解，M 是解的模数
        如果无解则返回 None
    
    Examples:
        >>> crt_two_equations(2, 3, 3, 5)
        (8, 15)  # x ≡ 8 (mod 15)
        >>> crt_two_equations(2, 4, 1, 2)
        None  # 无解
    """
    gcd, p, q = extended_gcd(m1, m2)
    
    # 检查是否有解
    if (a2 - a1) % gcd != 0:
        return None
    
    lcm = m1 * m2 // gcd
    x = (a1 + (a2 - a1) // gcd * p % (m2 // gcd) * m1) % lcm
    
    return x, lcm


def chinese_remainder_theorem(remainders: List[int], moduli: List[int]) -> Optional[Tuple[int, int]]:
    """
    中国剩余定理 - 求解同余方程组
    
    求解方程组:
        x ≡ remainders[i] (mod moduli[i])  for i = 0, 1, ..., n-1
    
    条件：模数两两互质时必有唯一解（模乘积意义下）
    
    Args:
        remainders: 余数列表 [a1, a2, ..., an]
        moduli: 模数列表 [m1, m2, ..., mn]
    
    Returns:
        (x, M) 其中 x 是最小正整数解（x < M），M 是所有模数的最小公倍数
        如果无解则返回 None
    
    Raises:
        ValueError: 如果输入列表长度不匹配或为空
    
    Examples:
        >>> chinese_remainder_theorem([2, 3, 2], [3, 5, 7])
        (23, 105)  # 孙子算经经典问题
        >>> chinese_remainder_theorem([1, 2, 3], [2, 3, 5])
        (23, 30)
    
    Note:
        经典问题："有物不知其数，三三数之剩二，五五数之剩三，七七数之剩二"
        答案：x = 23, M = 105
    """
    if len(remainders) != len(moduli):
        raise ValueError("余数列表和模数列表长度必须相同")
    
    if len(remainders) == 0:
        raise ValueError("输入列表不能为空")
    
    # 使用两两合并的方法
    x, M = remainders[0], moduli[0]
    
    for i in range(1, len(remainders)):
        result = crt_two_equations(x, M, remainders[i], moduli[i])
        if result is None:
            return None
        x, M = result
    
    return x, M


def crt_garner_method(remainders: List[int], moduli: List[int]) -> Optional[int]:
    """
    使用 Garner 方法求解 CRT
    
    Garner 方法是一种高效的 CRT 求解方法，适用于多次求解相同模数的情况。
    时间复杂度：预处理 O(n²)，查询 O(n)
    
    Args:
        remainders: 余数列表
        moduli: 模数列表（需要两两互质）
    
    Returns:
        最小正整数解，如果无解或模数不互质则返回 None
    
    Examples:
        >>> crt_garner_method([2, 3, 2], [3, 5, 7])
        23
    """
    if len(remainders) != len(moduli):
        raise ValueError("余数列表和模数列表长度必须相同")
    
    if len(remainders) == 0:
        raise ValueError("输入列表不能为空")
    
    n = len(remainders)
    
    # 验证模数两两互质
    for i in range(n):
        for j in range(i + 1, n):
            if math.gcd(moduli[i], moduli[j]) != 1:
                return None
    
    # 计算 M = m1 * m2 * ... * mn
    M = 1
    for m in moduli:
        M *= m
    
    # 计算 Mi 和 Mi的逆元
    result = 0
    for i in range(n):
        Mi = M // moduli[i]
        yi = modular_inverse(Mi, moduli[i])
        if yi is None:
            return None
        result = (result + remainders[i] * yi * Mi) % M
    
    return result


def is_solvable(remainders: List[int], moduli: List[int]) -> bool:
    """
    检查同余方程组是否有解
    
    条件：对于所有 i, j，满足 ai ≡ aj (mod gcd(mi, mj))
    
    Args:
        remainders: 余数列表
        moduli: 模数列表
    
    Returns:
        True 如果有解，False 如果无解
    
    Examples:
        >>> is_solvable([2, 4], [3, 6])
        True
        >>> is_solvable([2, 3], [4, 6])
        False  # gcd(4,6)=2, 但 2≠3 (mod 2)
    """
    if len(remainders) != len(moduli):
        return False
    
    n = len(remainders)
    for i in range(n):
        for j in range(i + 1, n):
            g = math.gcd(moduli[i], moduli[j])
            if (remainders[i] - remainders[j]) % g != 0:
                return False
    
    return True


def all_solutions(remainders: List[int], moduli: List[int], limit: int = 10) -> List[int]:
    """
    求同余方程组的所有解（限定范围内）
    
    Args:
        remainders: 余数列表
        moduli: 模数列表
        limit: 返回解的个数限制
    
    Returns:
        解列表（按升序排列）
    
    Examples:
        >>> all_solutions([2, 3], [3, 5], limit=5)
        [8, 23, 38, 53, 68]
    """
    result = chinese_remainder_theorem(remainders, moduli)
    if result is None:
        return []
    
    x, M = result
    solutions = []
    for i in range(limit):
        solutions.append(x + i * M)
    
    return solutions


# ============ 应用函数 ============

def ganzhi_year(year: int) -> Tuple[str, str]:
    """
    计算干支纪年（六十甲子）
    
    使用中国剩余定理计算给定年份的干支。
    
    Args:
        year: 公元纪年（如 2024）
    
    Returns:
        (天干, 地支) 元组
    
    Examples:
        >>> ganzhi_year(2024)
        ('甲', '辰')
        >>> ganzhi_year(1984)
        ('甲', '子')
        >>> ganzhi_year(2000)
        ('庚', '辰')
    
    Note:
        天干：甲乙丙丁戊己庚辛壬癸 (10个)
        地支：子丑寅卯辰巳午未申酉戌亥 (12个)
        干支周期：LCM(10, 12) = 60 年
    """
    tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 1984年是甲子年，作为基准
    # 天干：(year - 4) mod 10
    # 地支：(year - 4) mod 12
    # 这等价于求解 x ≡ (year-4) (mod 10) 和 x ≡ (year-4) (mod 12)
    
    offset = (year - 4) % 60  # 1984 = 甲子年
    
    gan_index = offset % 10
    zhi_index = offset % 12
    
    return tiangan[gan_index], dizhi[zhi_index]


def ganzhi_from_crt(year: int) -> Tuple[str, str]:
    """
    使用CRT方法计算干支（演示CRT应用）
    
    这是 ganzhi_year 的另一种实现，显式使用中国剩余定理。
    
    Args:
        year: 公元纪年
    
    Returns:
        (天干, 地支) 元组
    """
    tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 已知：某年是甲子年（天干=甲=0，地支=子=0）
    # 设该年相对于甲子年的偏移为 x
    # 则 x ≡ gan_offset (mod 10)
    #    x ≡ zhi_offset (mod 12)
    # 其中 gan_offset = (year - base_year) mod 10
    #      zhi_offset = (year - base_year) mod 12
    
    gan_offset = (year - 4) % 10  # 1984是甲子年，天干=0
    zhi_offset = (year - 4) % 12  # 1984是甲子年，地支=0
    
    # 使用CRT求解 x
    result = chinese_remainder_theorem([gan_offset, zhi_offset], [10, 12])
    if result is None:
        # 如果无解（这里不会发生，因为 gcd(10,12)=2，需要检查一致性）
        return tiangan[gan_offset], dizhi[zhi_offset]
    
    x, _ = result
    return tiangan[x % 10], dizhi[x % 12]


def year_from_ganzhi(gan: str, zhi: str, century: int = 21) -> int:
    """
    从干支推算年份
    
    Args:
        gan: 天干（甲乙丙丁戊己庚辛壬癸）
        zhi: 地支（子丑寅卯辰巳午未申酉戌亥）
        century: 世纪（默认21世纪，用于确定大致范围）
    
    Returns:
        该世纪内最接近的年份
    
    Examples:
        >>> year_from_ganzhi('甲', '子', 21)
        2044  # 21世纪内的甲子年
        >>> year_from_ganzhi('庚', '辰', 21)
        2000
    """
    tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    gan_index = tiangan.index(gan)
    zhi_index = dizhi.index(zhi)
    
    # 1984年是甲子年，天干索引=0，地支索引=0
    # 相对于1984年的偏移需要满足：
    # offset ≡ gan_index (mod 10)
    # offset ≡ zhi_index (mod 12)
    # 由于 gan_index 和 zhi_index 来自同一个 offset（周期60）
    # 需要验证一致性：gan_index ≡ zhi_index (mod 2)
    if (gan_index - zhi_index) % 2 != 0:
        raise ValueError(f"无效的干支组合: {gan}{zhi}（天干地支索引不一致）")
    
    # 计算 offset（使用中国剩余定理或直接查找）
    # 在60年周期内找到满足条件的 offset
    for offset in range(60):
        if offset % 10 == gan_index and offset % 12 == zhi_index:
            break
    
    # 计算在指定世纪内的年份
    base_year = (century - 1) * 100
    year = 1984 + offset
    
    # 找到该世纪内最接近的年份
    while year < base_year:
        year += 60
    while year >= base_year + 100:
        year -= 60
    
    return year


def rsa_decrypt_crt(c: int, d: int, p: int, q: int) -> int:
    """
    使用中国剩余定理加速 RSA 解密
    
    RSA解密通常需要计算 m = c^d mod n，其中 n = p * q
    使用CRT可以将计算分解为两个较小的模幂运算：
        m1 = c^d mod p
        m2 = c^d mod n
    然后用CRT合并结果。
    
    Args:
        c: 密文
        d: 私钥指数
        p: 第一个素因子
        q: 第二个素因子
    
    Returns:
        明文 m
    
    Examples:
        >>> # 简化示例（实际RSA参数更大）
        >>> p, q = 61, 53
        >>> n = p * q  # 3233
        >>> e, d = 17, 2753
        >>> m = 123  # 明文
        >>> c = pow(m, e, n)  # 加密
        >>> rsa_decrypt_crt(c, d, p, q)
        123
    
    Note:
        时间复杂度：O(log d * (log p² + log q²)) vs O(log d * log n²)
        当 p ≈ q ≈ √n 时，效率提升约4倍
    """
    # 计算 dp = d mod (p-1), dq = d mod (q-1)
    dp = d % (p - 1)
    dq = d % (q - 1)
    
    # 计算模幂
    m1 = pow(c % p, dp, p)
    m2 = pow(c % q, dq, q)
    
    # 使用CRT合并
    n = p * q
    q_inv = modular_inverse(q, p)
    
    h = (q_inv * (m1 - m2)) % p
    m = m2 + h * q
    
    return m % n


# ============ 辅助函数 ============

def lcm(a: int, b: int) -> int:
    """计算最小公倍数"""
    return abs(a * b) // math.gcd(a, b)


def lcm_list(numbers: List[int]) -> int:
    """计算多个数的最小公倍数"""
    result = 1
    for n in numbers:
        result = lcm(result, n)
    return result


def solve_linear_congruence(a: int, b: int, m: int) -> List[int]:
    """
    求解线性同余方程 ax ≡ b (mod m)
    
    Args:
        a: 系数
        b: 常数项
        m: 模数
    
    Returns:
        所有解的列表（按升序排列）
    
    Examples:
        >>> solve_linear_congruence(3, 6, 9)
        [2, 5, 8]  # x ≡ 2 (mod 3)
        >>> solve_linear_congruence(2, 3, 4)
        []  # 无解，因为 gcd(2,4)=2 不整除 3
    """
    g = math.gcd(a, m)
    
    if b % g != 0:
        return []
    
    # 化简
    a_reduced = a // g
    b_reduced = b // g
    m_reduced = m // g
    
    # 求 a_reduced 模 m_reduced 的逆
    inv = modular_inverse(a_reduced, m_reduced)
    if inv is None:
        return []
    
    # 基础解
    x0 = (inv * b_reduced) % m_reduced
    
    # 所有解
    solutions = []
    for i in range(g):
        solutions.append(x0 + i * m_reduced)
    
    return sorted(solutions)


def count_solutions(remainders: List[int], moduli: List[int], upper_bound: int) -> int:
    """
    计算在给定范围内解的个数
    
    Args:
        remainders: 余数列表
        moduli: 模数列表
        upper_bound: 上界（包含）
    
    Returns:
        解的个数
    
    Examples:
        >>> count_solutions([2, 3, 2], [3, 5, 7], 1000)
        10  # 105以内有1个解(23)，1000以内有约10个
    """
    result = chinese_remainder_theorem(remainders, moduli)
    if result is None:
        return 0
    
    x, M = result
    
    if x > upper_bound:
        return 0
    
    return 1 + (upper_bound - x) // M


# ============ 类定义 ============

class ChineseRemainder:
    """
    中国剩余定理求解器类
    
    支持预先计算和重复求解，适用于多次求解相同模数的情况。
    
    Examples:
        >>> crt = ChineseRemainder([3, 5, 7])
        >>> crt.solve([2, 3, 2])
        23
        >>> crt.solve([1, 2, 3])
        52
    """
    
    def __init__(self, moduli: List[int]):
        """
        初始化求解器
        
        Args:
            moduli: 模数列表
        """
        self.moduli = moduli
        self.n = len(moduli)
        
        # 计算 M = m1 * m2 * ... * mn
        self.M = 1
        for m in moduli:
            self.M *= m
        
        # 预计算 Mi 和 Mi的逆元
        self.Mi_list = []
        self.yi_list = []
        
        for i in range(self.n):
            Mi = self.M // moduli[i]
            yi = modular_inverse(Mi, moduli[i])
            self.Mi_list.append(Mi)
            self.yi_list.append(yi)
    
    def solve(self, remainders: List[int]) -> Optional[int]:
        """
        求解同余方程组
        
        Args:
            remainders: 余数列表
        
        Returns:
            最小正整数解，如果无解返回 None
        """
        if len(remainders) != self.n:
            raise ValueError(f"需要 {self.n} 个余数")
        
        # 检查是否有解（当模数不互质时）
        for i in range(self.n):
            for j in range(i + 1, self.n):
                g = math.gcd(self.moduli[i], self.moduli[j])
                if (remainders[i] - remainders[j]) % g != 0:
                    return None
        
        result = 0
        for i in range(self.n):
            if self.yi_list[i] is None:
                return None
            result = (result + remainders[i] * self.yi_list[i] * self.Mi_list[i]) % self.M
        
        return result
    
    def get_period(self) -> int:
        """获取解的周期（所有模数的最小公倍数）"""
        return self.M
    
    def get_all_solutions(self, remainders: List[int], count: int = 10) -> List[int]:
        """获取多个解"""
        x = self.solve(remainders)
        if x is None:
            return []
        
        solutions = []
        for i in range(count):
            solutions.append(x + i * self.M)
        
        return solutions


if __name__ == "__main__":
    # 演示使用
    print("=" * 60)
    print("中国剩余定理工具演示")
    print("=" * 60)
    
    # 经典问题
    print("\n【孙子算经经典问题】")
    print("有物不知其数，三三数之剩二，五五数之剩三，七七数之剩二，问物几何？")
    
    result = chinese_remainder_theorem([2, 3, 2], [3, 5, 7])
    print(f"答案: {result[0]} (周期: {result[1]})")
    
    # 干支纪年
    print("\n【干支纪年】")
    for year in [1984, 2000, 2024, 2025]:
        gan, zhi = ganzhi_year(year)
        print(f"{year}年: {gan}{zhi}年")
    
    # RSA加速演示
    print("\n【RSA解密加速演示】")
    p, q = 61, 53
    n = p * q
    e, d = 17, 2753
    m = 123
    c = pow(m, e, n)
    decrypted = rsa_decrypt_crt(c, d, p, q)
    print(f"明文: {m}, 密文: {c}, 解密: {decrypted}")
    
    print("\n" + "=" * 60)