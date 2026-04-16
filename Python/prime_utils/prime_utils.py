"""
Prime Number Utilities - 素数工具包实现

提供素数相关的数学计算功能，所有函数均为纯 Python 实现，无外部依赖。
"""

import random
from typing import List, Tuple, Optional, Generator


def is_prime_simple(n: int) -> bool:
    """
    使用简单试除法判断一个数是否为素数。
    适用于较小的数（n < 10^6），对于大数建议使用 is_prime()。
    
    Args:
        n: 要判断的正整数
        
    Returns:
        bool: 如果是素数返回 True，否则返回 False
        
    Examples:
        >>> is_prime_simple(17)
        True
        >>> is_prime_simple(18)
        False
        >>> is_prime_simple(1)
        False
        >>> is_prime_simple(2)
        True
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    if n < 9:
        return True
    if n % 3 == 0:
        return False
    
    # 只需检查到 sqrt(n)
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def _miller_rabin_test(n: int, a: int, d: int, r: int) -> bool:
    """
    Miller-Rabin 测试的核心实现。
    
    Args:
        n: 待测数
        a: 基数
        d: (n-1) = d * 2^r 中的 d
        r: (n-1) = d * 2^r 中的 r
        
    Returns:
        bool: 通过测试返回 True，否则返回 False
    """
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    
    for _ in range(r - 1):
        x = pow(x, 2, n)
        if x == n - 1:
            return True
        if x == 1:
            return False
    return False


def is_prime(n: int, k: int = 10) -> bool:
    """
    使用 Miller-Rabin 算法判断一个数是否为素数（概率性测试）。
    对于 n < 2^64，确定性测试保证正确。
    
    Args:
        n: 要判断的整数
        k: 测试轮数，默认10轮，错误概率 < 4^(-k)
        
    Returns:
        bool: 如果是素数返回 True，否则返回 False
        
    Examples:
        >>> is_prime(17)
        True
        >>> is_prime(561)  # Carmichael number
        False
        >>> is_prime(2**31 - 1)  # Mersenne prime
        True
        >>> is_prime(1)
        False
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    if n < 9:
        return True
    
    # 对于小数，使用确定性测试
    if n < 1000:
        return is_prime_simple(n)
    
    # 对于 n < 3,317,044,064,679,887,385,961,981，使用确定性基
    # 这样可以保证结果正确
    if n < 2047:
        bases = [2]
    elif n < 1373653:
        bases = [2, 3]
    elif n < 9080191:
        bases = [31, 73]
    elif n < 25326001:
        bases = [2, 3, 5]
    elif n < 3215031751:
        bases = [2, 3, 5, 7]
    elif n < 4759123141:
        bases = [2, 7, 61]
    elif n < 1122004669633:
        bases = [2, 13, 23, 1662803]
    elif n < 3474749660383:
        bases = [2, 3, 5, 7, 11, 13]
    elif n < 341550071728321:
        bases = [2, 3, 5, 7, 11, 13, 17]
    elif n < 3825123056546413051:
        bases = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    else:
        # 对于更大的数，使用随机基
        bases = [random.randint(2, n - 2) for _ in range(k)]
    
    # 分解 n-1 = d * 2^r
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    
    for a in bases:
        if a >= n:
            continue
        if not _miller_rabin_test(n, a, d, r):
            return False
    return True


def generate_primes(limit: int) -> List[int]:
    """
    使用埃拉托斯特尼筛法生成指定范围内所有素数。
    
    Args:
        limit: 上限（包含）
        
    Returns:
        List[int]: 小于等于 limit 的所有素数列表
        
    Examples:
        >>> generate_primes(20)
        [2, 3, 5, 7, 11, 13, 17, 19]
        >>> generate_primes(2)
        [2]
        >>> generate_primes(1)
        []
    """
    if limit < 2:
        return []
    
    # 使用位优化的筛法
    is_prime_arr = [True] * (limit + 1)
    is_prime_arr[0] = is_prime_arr[1] = False
    
    for i in range(2, int(limit ** 0.5) + 1):
        if is_prime_arr[i]:
            # 从 i*i 开始标记（更小的已经被之前的素数标记过了）
            for j in range(i * i, limit + 1, i):
                is_prime_arr[j] = False
    
    return [i for i in range(limit + 1) if is_prime_arr[i]]


def prime_factors(n: int) -> List[Tuple[int, int]]:
    """
    对一个数进行素因数分解。
    
    Args:
        n: 要分解的正整数
        
    Returns:
        List[Tuple[int, int]]: 素因子列表，每个元素为 (素数, 指数)
        
    Raises:
        ValueError: 如果 n < 1
        
    Examples:
        >>> prime_factors(60)
        [(2, 2), (3, 1), (5, 1)]  # 60 = 2^2 * 3 * 5
        >>> prime_factors(17)
        [(17, 1)]  # 17是素数
        >>> prime_factors(1)
        []
    """
    if n < 1:
        raise ValueError("n must be a positive integer")
    if n == 1:
        return []
    
    factors = []
    
    # 处理因子 2
    count = 0
    while n % 2 == 0:
        count += 1
        n //= 2
    if count > 0:
        factors.append((2, count))
    
    # 处理奇数因子
    i = 3
    while i * i <= n:
        count = 0
        while n % i == 0:
            count += 1
            n //= i
        if count > 0:
            factors.append((i, count))
        i += 2
    
    # 如果剩下的 n > 1，则它本身是素数
    if n > 1:
        factors.append((n, 1))
    
    return factors


def euler_phi(n: int) -> int:
    """
    计算欧拉函数 φ(n)，即小于 n 且与 n 互质的正整数个数。
    
    Args:
        n: 正整数
        
    Returns:
        int: 欧拉函数值
        
    Raises:
        ValueError: 如果 n < 1
        
    Examples:
        >>> euler_phi(1)
        1
        >>> euler_phi(9)  # 1,2,4,5,7,8 与 9 互质
        6
        >>> euler_phi(12)  # 1,5,7,11 与 12 互质
        4
        >>> euler_phi(17)  # 素数的欧拉函数值是 n-1
        16
    """
    if n < 1:
        raise ValueError("n must be a positive integer")
    if n == 1:
        return 1
    
    result = n
    factors = prime_factors(n)
    
    for p, _ in factors:
        result = result // p * (p - 1)
    
    return result


def gcd(a: int, b: int) -> int:
    """
    计算两个数的最大公约数（使用欧几里得算法）。
    
    Args:
        a: 第一个整数
        b: 第二个整数
        
    Returns:
        int: a 和 b 的最大公约数
        
    Examples:
        >>> gcd(48, 18)
        6
        >>> gcd(17, 13)
        1
        >>> gcd(-48, 18)
        6
        >>> gcd(0, 5)
        5
    """
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """
    计算两个数的最小公倍数。
    
    Args:
        a: 第一个整数
        b: 第二个整数
        
    Returns:
        int: a 和 b 的最小公倍数
        
    Raises:
        ValueError: 如果 a 或 b 为 0
        
    Examples:
        >>> lcm(12, 18)
        36
        >>> lcm(17, 13)
        221
        >>> lcm(4, 6)
        12
    """
    if a == 0 or b == 0:
        raise ValueError("lcm is not defined for zero")
    
    return abs(a * b) // gcd(a, b)


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    扩展欧几里得算法，求解 ax + by = gcd(a, b)。
    
    Args:
        a: 第一个整数
        b: 第二个整数
        
    Returns:
        Tuple[int, int, int]: (gcd, x, y)，其中 gcd = a*x + b*y
        
    Examples:
        >>> extended_gcd(35, 15)
        (5, 1, -2)  # 35*1 + 15*(-2) = 5
        >>> extended_gcd(17, 13)
        (1, -3, 4)  # 17*(-3) + 13*4 = 1
    """
    if b == 0:
        return a, 1, 0
    
    gcd_val, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    
    return gcd_val, x, y


def mod_inverse(a: int, m: int) -> Optional[int]:
    """
    计算 a 在模 m 下的乘法逆元。
    即找到 x 使得 ax ≡ 1 (mod m)。
    
    Args:
        a: 要求逆元的数
        m: 模数
        
    Returns:
        Optional[int]: 逆元，如果不存在则返回 None
        
    Examples:
        >>> mod_inverse(3, 11)
        4  # 因为 3*4 = 12 ≡ 1 (mod 11)
        >>> mod_inverse(6, 9)  # gcd(6,9)=3，不存在逆元
        None
    """
    if m <= 0:
        raise ValueError("modulus must be positive")
    
    g, x, _ = extended_gcd(a % m, m)
    
    if g != 1:
        return None  # 不存在逆元
    
    return x % m


def next_prime(n: int) -> int:
    """
    找到大于 n 的最小素数。
    
    Args:
        n: 起始数
        
    Returns:
        int: 大于 n 的最小素数
        
    Examples:
        >>> next_prime(10)
        11
        >>> next_prime(17)
        19
        >>> next_prime(1)
        2
    """
    if n < 2:
        return 2
    
    candidate = n + 1
    if candidate % 2 == 0:
        candidate += 1
    
    while not is_prime(candidate):
        candidate += 2
    
    return candidate


def prev_prime(n: int) -> Optional[int]:
    """
    找到小于 n 的最大素数。
    
    Args:
        n: 起始数
        
    Returns:
        Optional[int]: 小于 n 的最大素数，如果不存在则返回 None
        
    Examples:
        >>> prev_prime(10)
        7
        >>> prev_prime(3)
        2
        >>> prev_prime(2)
        None
    """
    if n <= 2:
        return None
    if n == 3:
        return 2
    
    candidate = n - 1
    if candidate % 2 == 0:
        candidate -= 1
    
    while candidate >= 2:
        if is_prime(candidate):
            return candidate
        candidate -= 2
    
    return None


def count_primes(n: int) -> int:
    """
    计算小于等于 n 的素数个数（素数计数函数 π(n)）。
    
    Args:
        n: 上限
        
    Returns:
        int: 素数个数
        
    Examples:
        >>> count_primes(10)
        4  # 2, 3, 5, 7
        >>> count_primes(100)
        25
        >>> count_primes(1)
        0
    """
    if n < 2:
        return 0
    
    return len(generate_primes(n))


def nth_prime(n: int) -> int:
    """
    返回第 n 个素数（从 1 开始计数）。
    
    Args:
        n: 序号（从1开始）
        
    Returns:
        int: 第 n 个素数
        
    Raises:
        ValueError: 如果 n < 1
        
    Examples:
        >>> nth_prime(1)
        2
        >>> nth_prime(5)
        11
        >>> nth_prime(100)
        541
    """
    if n < 1:
        raise ValueError("n must be a positive integer")
    
    # 估计上界（使用素数定理近似）
    if n < 6:
        upper = 15
    else:
        import math
        upper = int(n * (math.log(n) + math.log(math.log(n)))) + 10
    
    # 扩大上界以确保找到足够的素数
    primes = generate_primes(upper)
    
    while len(primes) < n:
        upper *= 2
        primes = generate_primes(upper)
    
    return primes[n - 1]


def is_coprime(a: int, b: int) -> bool:
    """
    判断两个数是否互质（最大公约数为1）。
    
    Args:
        a: 第一个整数
        b: 第二个整数
        
    Returns:
        bool: 如果互质返回 True，否则返回 False
        
    Examples:
        >>> is_coprime(15, 28)
        True
        >>> is_coprime(12, 18)
        False
        >>> is_coprime(17, 13)
        True
    """
    return gcd(a, b) == 1


def primes_up_to(n: int) -> Generator[int, None, None]:
    """
    生成器版本，逐个产生小于等于 n 的素数。
    适用于处理大范围时节省内存。
    
    Args:
        n: 上限
        
    Yields:
        int: 素数
        
    Examples:
        >>> list(primes_up_to(10))
        [2, 3, 5, 7]
    """
    if n < 2:
        return
    
    yield 2
    
    for candidate in range(3, n + 1, 2):
        if is_prime_simple(candidate):
            yield candidate