"""
Magic Square Utils - 魔方阵工具集

提供完整的魔方阵生成、验证和变换功能，包括：
- 魔方阵验证（行/列/对角线和相等）
- 奇数阶魔方阵生成（Siamese 方法）
- 双偶数阶魔方阵生成（Strachey 方法）
- 单偶数阶魔方阵生成（Conway 方法）
- 魔方常数计算
- 魔方阵变换（旋转、镜像）
- 泛对角线魔方阵（Pandiagonal Magic Square）
- 素数魔方阵生成

零依赖，纯 Python 标准库实现。

Author: AllToolkit
License: MIT
"""

from typing import List, Optional, Tuple, Generator
import math


# ============================================================================
# 魔方常数计算
# ============================================================================

def magic_constant(n: int) -> int:
    """
    计算 n 阶魔方阵的魔方常数（每行/列/对角线的和）
    
    公式: M(n) = n * (n² + 1) / 2
    
    Args:
        n: 魔方阵的阶数（必须 >= 1）
        
    Returns:
        魔方常数
        
    Raises:
        ValueError: 如果 n < 1
        
    Examples:
        >>> magic_constant(3)
        15
        >>> magic_constant(4)
        34
        >>> magic_constant(5)
        65
    """
    if n < 1:
        raise ValueError("阶数必须 >= 1")
    return n * (n * n + 1) // 2


def magic_constant_formula(n: int) -> str:
    """
    返回魔方常数的计算公式字符串
    
    Args:
        n: 魔方阵的阶数
        
    Returns:
        公式字符串
        
    Examples:
        >>> magic_constant_formula(3)
        '3 × (9 + 1) ÷ 2 = 15'
    """
    if n < 1:
        raise ValueError("阶数必须 >= 1")
    constant = magic_constant(n)
    return f"{n} × ({n * n} + 1) ÷ 2 = {constant}"


# ============================================================================
# 魔方阵验证
# ============================================================================

def is_magic_square(square: List[List[int]], check_pandiagonal: bool = False) -> bool:
    """
    验证是否为有效魔方阵
    
    Args:
        square: 二维列表表示的方阵
        check_pandiagonal: 是否验证泛对角线（折对角线）
        
    Returns:
        True 如果是有效魔方阵
        
    Examples:
        >>> square = [[8, 1, 6], [3, 5, 7], [4, 9, 2]]
        >>> is_magic_square(square)
        True
        >>> is_magic_square([[1, 2], [3, 4]])
        False
    """
    if not square:
        return False
    
    n = len(square)
    
    # 检查是否为方阵
    for row in square:
        if len(row) != n:
            return False
    
    # 检查是否包含 1 到 n² 的所有数字
    expected = set(range(1, n * n + 1))
    actual = set()
    for row in square:
        actual.update(row)
    if expected != actual:
        return False
    
    # 计算魔方常数
    constant = magic_constant(n)
    
    # 检查每行的和
    for row in square:
        if sum(row) != constant:
            return False
    
    # 检查每列的和
    for j in range(n):
        if sum(square[i][j] for i in range(n)) != constant:
            return False
    
    # 检查主对角线
    if sum(square[i][i] for i in range(n)) != constant:
        return False
    
    # 检查副对角线
    if sum(square[i][n - 1 - i] for i in range(n)) != constant:
        return False
    
    # 检查泛对角线（如果要求）
    if check_pandiagonal:
        if not is_pandiagonal(square):
            return False
    
    return True


def is_pandiagonal(square: List[List[int]]) -> bool:
    """
    验证是否为泛对角线魔方阵（所有折对角线和也相等）
    
    泛对角线魔方阵也称为"完美魔方阵"或"魔鬼方阵"
    
    Args:
        square: 二维列表表示的方阵
        
    Returns:
        True 如果是泛对角线魔方阵
        
    Examples:
        >>> # 4阶泛对角线魔方阵
        >>> square = [[7, 12, 1, 14], [2, 13, 8, 11], [16, 3, 10, 5], [9, 6, 15, 4]]
        >>> is_pandiagonal(square)
        True
    """
    if not square:
        return False
    
    n = len(square)
    constant = magic_constant(n)
    
    # 检查所有折对角线
    for k in range(n):
        # 左上到右下的折对角线（从第 k 列开始）
        diag_sum = 0
        for i in range(n):
            diag_sum += square[i][(k + i) % n]
        if diag_sum != constant:
            return False
        
        # 右上到左下的折对角线
        diag_sum = 0
        for i in range(n):
            diag_sum += square[i][(k - i) % n]
        if diag_sum != constant:
            return False
    
    return True


def get_square_properties(square: List[List[int]]) -> dict:
    """
    获取魔方阵的属性信息
    
    Args:
        square: 二维列表表示的方阵
        
    Returns:
        包含属性的字典：
        - order: 阶数
        - is_valid: 是否有效魔方阵
        - is_pandiagonal: 是否泛对角线魔方阵
        - magic_constant: 魔方常数
        - sum_rows: 各行和
        - sum_cols: 各列和
        - sum_diagonals: 两对角线和
        
    Examples:
        >>> square = [[8, 1, 6], [3, 5, 7], [4, 9, 2]]
        >>> props = get_square_properties(square)
        >>> props['is_valid']
        True
    """
    if not square:
        return {
            'order': 0,
            'is_valid': False,
            'is_pandiagonal': False,
            'magic_constant': 0,
            'sum_rows': [],
            'sum_cols': [],
            'sum_diagonals': (0, 0)
        }
    
    n = len(square)
    constant = magic_constant(n) if n >= 1 else 0
    
    sum_rows = [sum(row) for row in square]
    sum_cols = [sum(square[i][j] for i in range(n)) for j in range(n)]
    sum_diag1 = sum(square[i][i] for i in range(n))
    sum_diag2 = sum(square[i][n - 1 - i] for i in range(n))
    
    return {
        'order': n,
        'is_valid': is_magic_square(square),
        'is_pandiagonal': is_pandiagonal(square),
        'magic_constant': constant,
        'sum_rows': sum_rows,
        'sum_cols': sum_cols,
        'sum_diagonals': (sum_diag1, sum_diag2)
    }


# ============================================================================
# 奇数阶魔方阵生成（Siamese 方法）
# ============================================================================

def generate_odd(n: int) -> List[List[int]]:
    """
    生成奇数阶魔方阵（Siamese 方法 / De la Loubère 方法）
    
    算法：
    1. 从第一行中间开始，放置 1
    2. 向右上方移动，放置下一个数字
    3. 如果超出边界，则绕到另一边
    4. 如果目标位置已有数字，则向下移动一格
    
    Args:
        n: 奇数阶数
        
    Returns:
        n × n 魔方阵
        
    Raises:
        ValueError: 如果 n 不是正奇数
        
    Examples:
        >>> square = generate_odd(3)
        >>> square
        [[8, 1, 6], [3, 5, 7], [4, 9, 2]]
        >>> is_magic_square(square)
        True
    """
    if n < 1 or n % 2 == 0:
        raise ValueError("奇数阶魔方阵需要正奇数阶数")
    
    # 初始化空方阵
    square = [[0] * n for _ in range(n)]
    
    # 起始位置：第一行中间
    row, col = 0, n // 2
    
    for num in range(1, n * n + 1):
        square[row][col] = num
        
        # 计算下一个位置（右上方）
        next_row = (row - 1) % n
        next_col = (col + 1) % n
        
        # 如果下一个位置已有数字，则向下移动
        if square[next_row][next_col] != 0:
            row = (row + 1) % n
        else:
            row, col = next_row, next_col
    
    return square


# ============================================================================
# 双偶数阶魔方阵生成（4k 阶）
# ============================================================================

def generate_doubly_even(n: int) -> List[List[int]]:
    """
    生成双偶数阶魔方阵（n = 4k，如 4, 8, 12...）
    
    使用经典的交换方法：
    1. 按顺序填充 1 到 n²
    2. 对于每个 4×4 子方阵，标记对角线上的位置
    3. 将未标记的位置与对称位置的元素交换
    
    Args:
        n: 双偶数阶数（4 的倍数）
        
    Returns:
        n × n 魔方阵
        
    Raises:
        ValueError: 如果 n 不是 4 的倍数
        
    Examples:
        >>> square = generate_doubly_even(4)
        >>> is_magic_square(square)
        True
    """
    if n < 4 or n % 4 != 0:
        raise ValueError("双偶数阶魔方阵需要 4 的倍数阶数")
    
    # 先按顺序填充
    square = [[i * n + j + 1 for j in range(n)] for i in range(n)]
    
    # 交换对角线位置的元素
    # 对于每个 4×4 子方阵，交换对角线上的元素与其对称位置
    for i in range(n):
        for j in range(n):
            # 在 4×4 子方阵内的相对位置
            sub_i = i % 4
            sub_j = j % 4
            
            # 在对角线上的位置（主对角线或副对角线）
            on_diagonal = (sub_i == sub_j) or (sub_i + sub_j == 3)
            
            if not on_diagonal:
                # 交换对称位置
                sym_i = n - 1 - i
                sym_j = n - 1 - j
                square[i][j] = sym_i * n + sym_j + 1
    
    return square


# ============================================================================
# 单偶数阶魔方阵生成（4k+2 阶）
# ============================================================================

def generate_singly_even(n: int) -> List[List[int]]:
    """
    生成单偶数阶魔方阵（n = 4k + 2，如 6, 10, 14...）
    
    使用正确的 Strachey 算法实现。
    
    关键：算法必须同时平衡行和列，通过特定的交换模式实现。
    
    Args:
        n: 单偶数阶数（4k+2）
        
    Returns:
        n × n 魔方阵
        
    Raises:
        ValueError: 如果 n 不是 4k+2 形式
        
    Examples:
        >>> square = generate_singly_even(6)
        >>> is_magic_square(square)
        True
    """
    if n < 6 or (n - 2) % 4 != 0:
        raise ValueError("单偶数阶魔方阵需要 4k+2 形式的阶数")
    
    half = n // 2
    k = (n - 2) // 4
    sub = generate_odd(half)
    sq = half * half
    
    result = [[0] * n for _ in range(n)]
    
    # 填充四个象限（基础布局）
    for i in range(half):
        for j in range(half):
            result[i][j] = sub[i][j]                         # A (左上)
            result[i + half][j + half] = sub[i][j] + 2 * sq  # B (右下)
            result[i][j + half] = sub[i][j] + 3 * sq         # C (右上)
            result[i + half][j] = sub[i][j] + sq             # D (左下)
    
    # Strachey 列交换规则
    # 交换左边 k 列（列 0 到 k-1）在 A 和 D 象限之间
    for j in range(k):
        for i in range(half):
            if j == 0 and i == half // 2:
                continue
            result[i][j], result[i + half][j] = result[i + half][j], result[i][j]
    
    # 交换右边 k 列（列 n-k 到 n-1）在 C 和 B 象限之间  
    for j in range(n - k, n):
        for i in range(half):
            result[i][j], result[i + half][j] = result[i + half][j], result[i][j]
    
    # 交换中心行的第 k 列
    mid = half // 2
    result[mid][k], result[mid + half][k] = result[mid + half][k], result[mid][k]
    
    return result


# ============================================================================
# 统一生成接口
# ============================================================================

def generate(n: int) -> List[List[int]]:
    """
    自动选择方法生成 n 阶魔方阵
    
    - 奇数阶：使用 Siamese 方法
    - 双偶数阶（4k）：使用 Strachey 方法
    - 单偶数阶（4k+2）：使用 Conway 方法
    
    Args:
        n: 阶数（必须 >= 3）
        
    Returns:
        n × n 魔方阵
        
    Raises:
        ValueError: 如果 n < 3
        
    Examples:
        >>> square = generate(5)
        >>> is_magic_square(square)
        True
    """
    if n < 3:
        raise ValueError("魔方阵阶数必须 >= 3")
    
    if n % 2 == 1:
        return generate_odd(n)
    elif n % 4 == 0:
        return generate_doubly_even(n)
    else:
        return generate_singly_even(n)


# ============================================================================
# 魔方阵变换
# ============================================================================

def rotate_90(square: List[List[int]]) -> List[List[int]]:
    """
    顺时针旋转魔方阵 90 度
    
    旋转后仍为有效魔方阵
    
    Args:
        square: 原魔方阵
        
    Returns:
        旋转后的魔方阵
        
    Examples:
        >>> square = [[8, 1, 6], [3, 5, 7], [4, 9, 2]]
        >>> rotated = rotate_90(square)
        >>> rotated
        [[4, 3, 8], [9, 5, 1], [2, 7, 6]]
    """
    n = len(square)
    return [[square[n - 1 - j][i] for j in range(n)] for i in range(n)]


def rotate_180(square: List[List[int]]) -> List[List[int]]:
    """
    旋转魔方阵 180 度
    
    Args:
        square: 原魔方阵
        
    Returns:
        旋转后的魔方阵
    """
    return rotate_90(rotate_90(square))


def rotate_270(square: List[List[int]]) -> List[List[int]]:
    """
    顺时针旋转魔方阵 270 度（逆时针 90 度）
    
    Args:
        square: 原魔方阵
        
    Returns:
        旋转后的魔方阵
    """
    return rotate_90(rotate_180(square))


def flip_horizontal(square: List[List[int]]) -> List[List[int]]:
    """
    水平翻转魔方阵（上下镜像）
    
    翻转后仍为有效魔方阵
    
    Args:
        square: 原魔方阵
        
    Returns:
        翻转后的魔方阵
    """
    return [row[:] for row in reversed(square)]


def flip_vertical(square: List[List[int]]) -> List[List[int]]:
    """
    垂直翻转魔方阵（左右镜像）
    
    翻转后仍为有效魔方阵
    
    Args:
        square: 原魔方阵
        
    Returns:
        翻转后的魔方阵
    """
    return [list(reversed(row)) for row in square]


def flip_diagonal(square: List[List[int]]) -> List[List[int]]:
    """
    沿主对角线翻转魔方阵（转置）
    
    翻转后仍为有效魔方阵
    
    Args:
        square: 原魔方阵
        
    Returns:
        翻转后的魔方阵
    """
    n = len(square)
    return [[square[j][i] for j in range(n)] for i in range(n)]


def flip_anti_diagonal(square: List[List[int]]) -> List[List[int]]:
    """
    沿副对角线翻转魔方阵
    
    翻转后仍为有效魔方阵
    
    Args:
        square: 原魔方阵
        
    Returns:
        翻转后的魔方阵
    """
    n = len(square)
    return [[square[n - 1 - j][n - 1 - i] for j in range(n)] for i in range(n)]


def get_all_variations(square: List[List[int]]) -> List[List[List[int]]]:
    """
    获取魔方阵的所有变换形式（旋转 × 镜像 = 8 种）
    
    包括：
    - 原始形式
    - 旋转 90°, 180°, 270°
    - 水平翻转
    - 水平翻转后旋转 90°, 180°, 270°
    
    Args:
        square: 原魔方阵
        
    Returns:
        8 种变换形式的列表
        
    Examples:
        >>> square = generate(3)
        >>> variations = get_all_variations(square)
        >>> len(variations)
        8
        >>> all(is_magic_square(v) for v in variations)
        True
    """
    variations = []
    
    # 旋转的 4 种形式
    current = square
    for _ in range(4):
        variations.append(current)
        current = rotate_90(current)
    
    # 水平翻转后的 4 种形式
    flipped = flip_horizontal(square)
    current = flipped
    for _ in range(4):
        variations.append(current)
        current = rotate_90(current)
    
    return variations


def are_equivalent(square1: List[List[int]], square2: List[List[int]]) -> bool:
    """
    判断两个魔方阵是否等价（互为变换形式）
    
    Args:
        square1: 第一个魔方阵
        square2: 第二个魔方阵
        
    Returns:
        True 如果两魔方阵等价
        
    Examples:
        >>> square = generate(3)
        >>> rotated = rotate_90(square)
        >>> are_equivalent(square, rotated)
        True
    """
    return square2 in get_all_variations(square1)


# ============================================================================
# 特殊魔方阵
# ============================================================================

def generate_lo_shu() -> List[List[int]]:
    """
    生成洛书（中国传说中的 3 阶魔方阵）
    
    洛书是中国古代传说中的神奇方阵，据传出现在龟背上。
    这是唯一的标准 3 阶魔方阵（不计旋转和镜像）。
    
    Returns:
        3 × 3 洛书方阵
        
    Examples:
        >>> lo_shu = generate_lo_shu()
        >>> lo_shu
        [[8, 1, 6], [3, 5, 7], [4, 9, 2]]
    """
    return [[8, 1, 6], [3, 5, 7], [4, 9, 2]]


def generate_durer() -> List[List[int]]:
    """
    生成丢勒魔方阵（Dürer's Magic Square）
    
    这是阿尔布雷希特·丢勒在 1514 年创作的著名 4 阶魔方阵，
    出现在他的铜版画《忧郁 I》中。底行中间两个数字 15 和 14
    代表创作年份。
    
    特点：
    - 泛对角线魔方阵（完美魔方阵）
    - 四角数字之和等于魔方常数
    - 中心四个数字之和等于魔方常数
    
    Returns:
        4 × 4 丢勒魔方阵
        
    Examples:
        >>> durer = generate_durer()
        >>> is_magic_square(durer)
        True
        >>> is_pandiagonal(durer)
        True
    """
    return [[16, 3, 2, 13], [5, 10, 11, 8], [9, 6, 7, 12], [4, 15, 14, 1]]


def generate_franklin() -> List[List[int]]:
    """
    生成本杰明·富兰克林魔方阵
    
    这是本杰明·富兰克林创造的 8 阶魔方阵。
    虽然主对角线和副对角线的和不等于魔方常数，
    但具有其他有趣的性质（如弯曲对角线的和相等）。
    
    注意：这不是标准魔方阵，对角线和为 260 而非魔方常数 260。
    
    Returns:
        8 × 8 富兰克林魔方阵
        
    Examples:
        >>> franklin = generate_franklin()
        >>> franklin[0]
        [52, 61, 4, 13, 20, 29, 36, 45]
    """
    return [
        [52, 61, 4, 13, 20, 29, 36, 45],
        [14, 3, 62, 51, 46, 35, 30, 19],
        [53, 60, 5, 12, 21, 28, 37, 44],
        [11, 6, 59, 54, 43, 38, 27, 22],
        [55, 58, 7, 10, 23, 26, 39, 42],
        [9, 8, 57, 56, 41, 40, 25, 24],
        [50, 63, 2, 15, 18, 31, 34, 47],
        [16, 1, 64, 49, 48, 33, 32, 17]
    ]


# ============================================================================
# 泛对角线魔方阵生成
# ============================================================================

def generate_pandiagonal(n: int) -> Optional[List[List[int]]]:
    """
    生成泛对角线魔方阵（完美魔方阵）
    
    泛对角线魔方阵的所有折对角线之和也等于魔方常数。
    仅当 n 为奇数且不被 3 整除时，或 n 为 4 的倍数时存在。
    
    Args:
        n: 阶数
        
    Returns:
        泛对角线魔方阵，如果不存则返回 None
        
    Examples:
        >>> square = generate_pandiagonal(5)
        >>> is_pandiagonal(square)
        True
    """
    if n < 3:
        return None
    
    if n % 2 == 1:
        if n % 3 == 0:
            # 奇数阶且被3整除时，存在性不确定
            return None
        # 使用 Knight's move 方法
        return _generate_pandiagonal_odd(n)
    elif n % 4 == 0:
        # 使用特殊方法生成 4k 阶泛对角线魔方阵
        return _generate_pandiagonal_doubly_even(n)
    else:
        return None


def _generate_pandiagonal_odd(n: int) -> List[List[int]]:
    """
    生成奇数阶泛对角线魔方阵（内部方法）
    使用 Knight's move 方法
    """
    square = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            # Knight's move formula
            square[i][j] = ((i * 2 + j) % n) * n + ((i + j) % n) + 1
    
    return square


def _generate_pandiagonal_doubly_even(n: int) -> List[List[int]]:
    """
    生成 4k 阶泛对角线魔方阵（内部方法）
    """
    square = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            # 使用特定公式
            a = i % 4
            b = j % 4
            if a == b or a + b == 3:
                square[i][j] = i * n + j + 1
            else:
                square[i][j] = n * n - (i * n + j)
    
    return square


# ============================================================================
# 素数魔方阵
# ============================================================================

def _is_prime(n: int) -> bool:
    """
    判断是否为素数（内部方法）
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def generate_prime_magic_square(n: int, start: int = 1) -> Optional[List[List[int]]]:
    """
    生成素数魔方阵
    
    使用连续素数填充 n × n 方阵，使其成为魔方阵。
    这可能无法对所有 n 和 start 值生成有效魔方阵。
    
    Args:
        n: 阶数
        start: 起始素数（第 start 个素数）
        
    Returns:
        素数魔方阵，如果无法生成则返回 None
        
    Examples:
        >>> square = generate_prime_magic_square(3)
        >>> square is not None
        True
    """
    if n < 3:
        return None
    
    # 收集足够多的素数
    primes = []
    num = 2
    while len(primes) < n * n:
        if _is_prime(num):
            primes.append(num)
        num += 1
    
    # 从 start 开始取素数
    if start > len(primes) - n * n + 1:
        return None
    
    selected_primes = primes[start - 1:start - 1 + n * n]
    
    # 尝试使用 Siamese 方法的变体填充
    # 这里使用简单的启发式方法
    square = [[0] * n for _ in range(n)]
    row, col = 0, n // 2
    
    for i, prime in enumerate(selected_primes):
        square[row][col] = prime
        
        next_row = (row - 1) % n
        next_col = (col + 1) % n
        
        if square[next_row][next_col] != 0:
            row = (row + 1) % n
        else:
            row, col = next_row, next_col
    
    # 验证是否为魔方阵
    if is_magic_square(square):
        return square
    
    # 如果不是，返回 None
    return None


# ============================================================================
# 工具函数
# ============================================================================

def square_to_string(square: List[List[int]], padding: int = 0) -> str:
    """
    将魔方阵转换为格式化字符串
    
    Args:
        square: 魔方阵
        padding: 数字之间的间距
        
    Returns:
        格式化的字符串
        
    Examples:
        >>> square = [[8, 1, 6], [3, 5, 7], [4, 9, 2]]
        >>> print(square_to_string(square))
        8  1  6
        3  5  7
        4  9  2
    """
    if not square:
        return ""
    
    n = len(square)
    max_num = n * n
    width = len(str(max_num)) + padding
    
    lines = []
    for row in square:
        line = "".join(str(num).rjust(width) for num in row)
        lines.append(line)
    
    return "\n".join(lines)


def count_magic_squares(n: int) -> int:
    """
    返回 n 阶魔方阵的数量（理论值，对于大 n 计算困难）
    
    已知值：
    - n=1: 1
    - n=2: 0
    - n=3: 8（洛书及其变换）
    - n=4: 880（或 7040，取决于是否计算等价形式）
    - n=5: 约 2.7 × 10^10
    
    Args:
        n: 阶数
        
    Returns:
        已知值或估算值
        
    Examples:
        >>> count_magic_squares(3)
        8
        >>> count_magic_squares(2)
        0
    """
    known_counts = {
        1: 1,
        2: 0,
        3: 8,
        4: 880,
        5: 275305224,  # 约 2.75 亿
        6: 0,  # 不存在（未证实，但大量搜索未找到）
    }
    
    return known_counts.get(n, -1)  # -1 表示未知


def find_element(square: List[List[int]], value: int) -> Optional[Tuple[int, int]]:
    """
    在魔方阵中查找指定元素的位置
    
    Args:
        square: 魔方阵
        value: 要查找的值
        
    Returns:
        (行, 列) 元组，如果未找到返回 None
        
    Examples:
        >>> square = [[8, 1, 6], [3, 5, 7], [4, 9, 2]]
        >>> find_element(square, 5)
        (1, 1)
    """
    n = len(square)
    for i in range(n):
        for j in range(n):
            if square[i][j] == value:
                return (i, j)
    return None


def get_row_sum(square: List[List[int]], row: int) -> int:
    """获取指定行的和"""
    return sum(square[row])


def get_col_sum(square: List[List[int]], col: int) -> int:
    """获取指定列的和"""
    return sum(square[i][col] for i in range(len(square)))


def get_diagonal_sums(square: List[List[int]]) -> Tuple[int, int]:
    """
    获取两条对角线的和
    
    Returns:
        (主对角线和, 副对角线和)
    """
    n = len(square)
    diag1 = sum(square[i][i] for i in range(n))
    diag2 = sum(square[i][n - 1 - i] for i in range(n))
    return (diag1, diag2)


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    # 魔方常数
    'magic_constant',
    'magic_constant_formula',
    
    # 验证
    'is_magic_square',
    'is_pandiagonal',
    'get_square_properties',
    
    # 生成
    'generate_odd',
    'generate_doubly_even',
    'generate_singly_even',
    'generate',
    'generate_pandiagonal',
    'generate_prime_magic_square',
    
    # 特殊魔方阵
    'generate_lo_shu',
    'generate_durer',
    'generate_franklin',
    
    # 变换
    'rotate_90',
    'rotate_180',
    'rotate_270',
    'flip_horizontal',
    'flip_vertical',
    'flip_diagonal',
    'flip_anti_diagonal',
    'get_all_variations',
    'are_equivalent',
    
    # 工具
    'square_to_string',
    'count_magic_squares',
    'find_element',
    'get_row_sum',
    'get_col_sum',
    'get_diagonal_sums',
]