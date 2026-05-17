"""
Armstrong Number Utilities (阿姆斯特朗数工具)

阿姆斯特朗数（Armstrong Number），又称自恋数（Narcissistic Number）、
自幂数、水仙花数，是指一个 n 位数，其各位数字的 n 次方之和等于它本身。

例如：
- 153 = 1^3 + 5^3 + 3^3
- 9474 = 9^4 + 4^4 + 7^4 + 4^4
- 370 = 3^3 + 7^3 + 0^3

本模块还包含其他趣味数的检测和生成：
- 快乐数 (Happy Number)
- 卡普雷卡尔数 (Kaprekar Number)
- 完全数 (Perfect Number)
- 回文数 (Palindrome Number)
"""

from typing import List, Tuple, Optional, Generator


def is_armstrong(number: int) -> bool:
    """
    检测一个数是否为阿姆斯特朗数。
    
    阿姆斯特朗数是指一个 n 位数，其各位数字的 n 次方之和等于它本身。
    
    Args:
        number: 要检测的整数（非负）
        
    Returns:
        bool: 如果是阿姆斯特朗数返回 True，否则返回 False
        
    Examples:
        >>> is_armstrong(153)
        True
        >>> is_armstrong(9474)
        True
        >>> is_armstrong(154)
        False
    """
    if number < 0:
        return False
    
    digits = [int(d) for d in str(number)]
    n = len(digits)
    total = sum(d ** n for d in digits)
    
    return total == number


def get_armstrong_digits(number: int) -> Tuple[int, int, int]:
    """
    获取阿姆斯特朗数的位数、各位数字的幂和、以及差值。
    
    Args:
        number: 要分析的整数
        
    Returns:
        Tuple[int, int, int]: (位数, 幂和, 幂和与原数的差值)
        
    Examples:
        >>> get_armstrong_digits(153)
        (3, 153, 0)
        >>> get_armstrong_digits(154)
        (3, 190, 36)
    """
    if number < 0:
        return (0, 0, 0)
    
    digits = [int(d) for d in str(number)]
    n = len(digits)
    total = sum(d ** n for d in digits)
    
    return (n, total, total - number)


def find_armstrong_numbers(limit: int) -> List[int]:
    """
    查找指定范围内的所有阿姆斯特朗数。
    
    Args:
        limit: 上限（包含）
        
    Returns:
        List[int]: 范围内的所有阿姆斯特朗数列表
        
    Examples:
        >>> find_armstrong_numbers(200)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 153]
        >>> find_armstrong_numbers(10000)[:15]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371, 407, 1634]
    """
    result = []
    for num in range(limit + 1):
        if is_armstrong(num):
            result.append(num)
    return result


def generate_armstrong_numbers() -> Generator[int, None, None]:
    """
    无限生成阿姆斯特朗数的生成器。
    
    由于阿姆斯特朗数只有有限的 88 个（已知最大的是 115132219018763992565095597973971522401），
    该生成器将在生成完所有已知的阿姆斯特朗数后停止。
    
    Yields:
        int: 下一个阿姆斯特朗数
        
    Examples:
        >>> gen = generate_armstrong_numbers()
        >>> [next(gen) for _ in range(15)]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371, 407, 1634]
    """
    # 已知的所有阿姆斯特朗数
    known_armstrong = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
        153, 370, 371, 407,
        1634, 8208, 9474,
        54748, 92727, 93084,
        548834,
        1741725, 4210818, 9800817, 9926315,
        24678050, 24678051, 88593477,
        146511208, 472335975, 534494836, 912985153,
        4679307774,
        32164049650, 32164049651, 40028394225, 42678290603, 44708635679, 49388550606, 82693916578, 94204591914,
        28116440335967,
        4338281769391370, 4338281769391371,
        21897142587612075, 35641594208964132, 35875699062250035,
        1517841543307505039,
        3289582984443187032, 4498128791164624869, 4929273885928088826,
        63105425988599693916,
        128468643043731391252, 449177399146038697307,
        21887696841122916288858,
        27879694893054074471405, 27907865009977052567814, 28361281321319229463398, 35452590104031691935943,
        174088005938065293023722,
        188451485447897896036875, 239313664430041569350093,
        1550475334214501539088894, 1553242162892605526270993, 3706907995955475988644380, 3706907995955475988644381, 4422095118045580294627671,
        121204998563613372405438066, 121270696006801314328439376, 128851796696487777842012787, 174650464499531377631639254, 177265453171792792366489765,
        14607640612971980372614873089, 19008174136254279995012734740, 19008174136254279995012734741, 23866716435523975980390369295,
        1145037275765491025924292050346, 1927890457142960697580636236639, 2309092682616190307509695338915,
        17333509997782249308725103962772,
        186709961001538790100634132976990, 186709961001538790100634132976991,
        1122763285329372541592822900204593,
        12639369517103790328947807201478392, 12679937780272278566303885594196922, 1219167219625434121569735803609966019,
        12815792078366059955099770545296129367, 115132219018763992565095597973971522401
    ]
    
    for num in known_armstrong:
        yield num


def get_next_armstrong(number: int) -> Optional[int]:
    """
    获取大于给定数的最小阿姆斯特朗数。
    
    Args:
        number: 起始数
        
    Returns:
        Optional[int]: 下一个阿姆斯特朗数，如果不存在则返回 None
        
    Examples:
        >>> get_next_armstrong(150)
        153
        >>> get_next_armstrong(200)
        370
    """
    for arm in generate_armstrong_numbers():
        if arm > number:
            return arm
    return None


def count_armstrong_digits(number: int) -> int:
    """
    计算数字的位数。
    
    Args:
        number: 要计算的整数
        
    Returns:
        int: 数字的位数
        
    Examples:
        >>> count_armstrong_digits(153)
        3
        >>> count_armstrong_digits(9474)
        4
    """
    if number == 0:
        return 1
    count = 0
    n = abs(number)
    while n > 0:
        count += 1
        n //= 10
    return count


# ==================== 快乐数 (Happy Number) ====================

def sum_of_squares_of_digits(number: int) -> int:
    """
    计算一个数各位数字的平方和。
    
    Args:
        number: 要计算的整数
        
    Returns:
        int: 各位数字的平方和
        
    Examples:
        >>> sum_of_squares_of_digits(19)
        82  # 1^2 + 9^2 = 1 + 81 = 82
        >>> sum_of_squares_of_digits(100)
        1  # 1^2 + 0^2 + 0^2 = 1
    """
    total = 0
    n = abs(number)
    while n > 0:
        digit = n % 10
        total += digit * digit
        n //= 10
    return total


def is_happy(number: int) -> bool:
    """
    检测一个数是否为快乐数。
    
    快乐数定义：从任何正整数开始，将其各位数字的平方和替代该数，
    重复此过程，最终达到 1 的数为快乐数。
    
    Args:
        number: 要检测的整数
        
    Returns:
        bool: 如果是快乐数返回 True，否则返回 False
        
    Examples:
        >>> is_happy(19)
        True  # 19 → 82 → 68 → 100 → 1
        >>> is_happy(4)
        False  # 进入循环
    """
    if number <= 0:
        return False
    
    seen = set()
    while number != 1 and number not in seen:
        seen.add(number)
        number = sum_of_squares_of_digits(number)
    
    return number == 1


def get_happy_sequence(number: int) -> List[int]:
    """
    获取快乐数的变换序列。
    
    Args:
        number: 起始数
        
    Returns:
        List[int]: 变换序列（直到达到 1 或检测到循环）
        
    Examples:
        >>> get_happy_sequence(19)
        [19, 82, 68, 100, 1]
        >>> get_happy_sequence(4)[:8]
        [4, 16, 37, 58, 89, 145, 42, 20]
    """
    if number <= 0:
        return [number]
    
    sequence = [number]
    seen = {number}
    
    while number != 1:
        number = sum_of_squares_of_digits(number)
        if number in seen:
            sequence.append(number)
            break
        seen.add(number)
        sequence.append(number)
    
    return sequence


def find_happy_numbers(limit: int) -> List[int]:
    """
    查找指定范围内的所有快乐数。
    
    Args:
        limit: 上限（包含）
        
    Returns:
        List[int]: 范围内的所有快乐数列表
        
    Examples:
        >>> find_happy_numbers(20)
        [1, 7, 10, 13, 19]
    """
    return [num for num in range(1, limit + 1) if is_happy(num)]


# ==================== 卡普雷卡尔数 (Kaprekar Number) ====================

def is_kaprekar(number: int) -> bool:
    """
    检测一个数是否为卡普雷卡尔数。
    
    卡普雷卡尔数定义：一个非负整数，其平方数可以分为两部分，使得这两部分的和等于原数。
    
    例如：9 是卡普雷卡尔数，因为 9^2 = 81，8 + 1 = 9
         45 是卡普雷卡尔数，因为 45^2 = 2025，20 + 25 = 45
    
    注意：1 被视为卡普雷卡尔数，因为 1^2 = 1 = 0 + 1 = 1
    
    Args:
        number: 要检测的整数
        
    Returns:
        bool: 如果是卡普雷卡尔数返回 True，否则返回 False
        
    Examples:
        >>> is_kaprekar(9)
        True
        >>> is_kaprekar(45)
        True
        >>> is_kaprekar(297)
        True  # 297^2 = 88209, 88 + 209 = 297
        >>> is_kaprekar(10)
        False
    """
    if number < 1:
        return False
    
    # 特殊情况：1 是卡普雷卡尔数
    if number == 1:
        return True
    
    square = number * number
    square_str = str(square)
    
    for i in range(1, len(square_str)):
        left = int(square_str[:i]) if square_str[:i] else 0
        right = int(square_str[i:]) if square_str[i:] else 0
        
        # 右边部分不能为 0（按照某些定义）
        if right > 0 and left + right == number:
            return True
    
    return False


def find_kaprekar_numbers(limit: int) -> List[int]:
    """
    查找指定范围内的所有卡普雷卡尔数。
    
    Args:
        limit: 上限（包含）
        
    Returns:
        List[int]: 范围内的所有卡普雷卡尔数列表
        
    Examples:
        >>> find_kaprekar_numbers(100)
        [1, 9, 45, 55, 99]
    """
    return [num for num in range(1, limit + 1) if is_kaprekar(num)]


def kaprekar_routine(number: int, max_iterations: int = 100) -> Tuple[List[int], bool]:
    """
    执行卡普雷卡尔程序（将数字的各位按降序和升序排列后相减，重复直到达到 6174 或循环）。
    
    注意：此程序只适用于 4 位数（各位不全部相同）。
    6174 被称为卡普雷卡尔常数。
    
    Args:
        number: 起始的 4 位数
        max_iterations: 最大迭代次数
        
    Returns:
        Tuple[List[int], bool]: (变换序列, 是否达到 6174)
        
    Examples:
        >>> kaprekar_routine(3524)
        ([3524, 3087, 8352, 6174], True)
    """
    if number < 1000 or number > 9999:
        return ([number], False)
    
    # 检查是否所有数字相同
    digits = [int(d) for d in str(number)]
    if len(set(digits)) == 1:
        return ([number], False)
    
    sequence = [number]
    seen = {number}
    
    for _ in range(max_iterations):
        # 降序排列
        desc = int(''.join(sorted(str(number), reverse=True)))
        # 升序排列
        asc = int(''.join(sorted(str(number))))
        
        number = desc - asc
        
        if number in seen:
            sequence.append(number)
            return (sequence, number == 6174)
        
        seen.add(number)
        sequence.append(number)
        
        if number == 6174:
            return (sequence, True)
    
    return (sequence, False)


# ==================== 完全数 (Perfect Number) ====================

def get_proper_divisors(number: int) -> List[int]:
    """
    获取一个数的所有真约数（不包括自身）。
    
    Args:
        number: 要计算的正整数
        
    Returns:
        List[int]: 所有真约数列表
        
    Examples:
        >>> get_proper_divisors(28)
        [1, 2, 4, 7, 14]
        >>> get_proper_divisors(6)
        [1, 2, 3]
    """
    if number <= 1:
        return []
    
    divisors = [1]
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            divisors.append(i)
            if i != number // i:
                divisors.append(number // i)
    
    return sorted(divisors)


def is_perfect(number: int) -> bool:
    """
    检测一个数是否为完全数。
    
    完全数定义：一个数等于其所有真约数之和。
    例如：6 = 1 + 2 + 3，28 = 1 + 2 + 4 + 7 + 14
    
    Args:
        number: 要检测的整数
        
    Returns:
        bool: 如果是完全数返回 True，否则返回 False
        
    Examples:
        >>> is_perfect(6)
        True
        >>> is_perfect(28)
        True
        >>> is_perfect(12)
        False
    """
    if number <= 1:
        return False
    
    return sum(get_proper_divisors(number)) == number


def find_perfect_numbers(limit: int) -> List[int]:
    """
    查找指定范围内的所有完全数。
    
    Args:
        limit: 上限（包含）
        
    Returns:
        List[int]: 范围内的所有完全数列表
        
    Examples:
        >>> find_perfect_numbers(10000)
        [6, 28, 496, 8128]
    """
    return [num for num in range(2, limit + 1) if is_perfect(num)]


def is_abundant(number: int) -> bool:
    """
    检测一个数是否为盈数（Abundant Number）。
    
    盈数定义：一个数的真约数之和大于它本身。
    
    Args:
        number: 要检测的整数
        
    Returns:
        bool: 如果是盈数返回 True
        
    Examples:
        >>> is_abundant(12)
        True  # 1 + 2 + 3 + 4 + 6 = 16 > 12
    """
    if number <= 1:
        return False
    
    return sum(get_proper_divisors(number)) > number


def is_deficient(number: int) -> bool:
    """
    检测一个数是否为亏数（Deficient Number）。
    
    亏数定义：一个数的真约数之和小于它本身。
    
    Args:
        number: 要检测的整数
        
    Returns:
        bool: 如果是亏数返回 True
        
    Examples:
        >>> is_deficient(8)
        True  # 1 + 2 + 4 = 7 < 8
    """
    if number <= 1:
        return True
    
    return sum(get_proper_divisors(number)) < number


# ==================== 回文数 (Palindrome Number) ====================

def is_palindrome(number: int) -> bool:
    """
    检测一个数是否为回文数。
    
    回文数定义：正读和反读都相同的数。
    
    Args:
        number: 要检测的整数
        
    Returns:
        bool: 如果是回文数返回 True
        
    Examples:
        >>> is_palindrome(121)
        True
        >>> is_palindrome(12321)
        True
        >>> is_palindrome(123)
        False
    """
    if number < 0:
        return False
    
    s = str(number)
    return s == s[::-1]


def find_palindrome_numbers(limit: int) -> List[int]:
    """
    查找指定范围内的所有回文数。
    
    Args:
        limit: 上限（包含）
        
    Returns:
        List[int]: 范围内的所有回文数列表
        
    Examples:
        >>> find_palindrome_numbers(50)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33, 44]
    """
    return [num for num in range(limit + 1) if is_palindrome(num)]


def reverse_number(number: int) -> int:
    """
    返回一个数的数字反转。
    
    Args:
        number: 要反转的整数
        
    Returns:
        int: 反转后的数
        
    Examples:
        >>> reverse_number(123)
        321
        >>> reverse_number(100)
        1  # 前导零被忽略
    """
    negative = number < 0
    number = abs(number)
    reversed_num = 0
    
    while number > 0:
        reversed_num = reversed_num * 10 + number % 10
        number //= 10
    
    return -reversed_num if negative else reversed_num


def is_lychrel(number: int, max_iterations: int = 50) -> bool:
    """
    检测一个数是否为 Lychrel 数候选（经过多次反转相加仍不形成回文数）。
    
    大多数数经过反转相加几次后会成为回文数，但 Lychrel 数似乎永远不会。
    196 是最著名的 Lychrel 数候选。
    
    Args:
        number: 起始数
        max_iterations: 最大迭代次数
        
    Returns:
        bool: 如果在最大迭代次数内未形成回文数，返回 True
        
    Examples:
        >>> is_lychrel(196)
        True  # 已知的 Lychrel 数候选
        >>> is_lychrel(47)
        False  # 47 + 74 = 121，一次就成为回文
    """
    for _ in range(max_iterations):
        number = number + reverse_number(number)
        if is_palindrome(number):
            return False
    return True


def get_lychrel_sequence(number: int, max_iterations: int = 50) -> Tuple[List[int], bool]:
    """
    获取 Lychrel 变换序列。
    
    Args:
        number: 起始数
        max_iterations: 最大迭代次数
        
    Returns:
        Tuple[List[int], bool]: (变换序列, 是否找到回文数)
        
    Examples:
        >>> get_lychrel_sequence(47)
        ([47, 121], True)
    """
    sequence = [number]
    
    for _ in range(max_iterations):
        number = number + reverse_number(number)
        sequence.append(number)
        if is_palindrome(number):
            return (sequence, True)
    
    return (sequence, False)


# ==================== 综合功能 ====================

def analyze_number(number: int) -> dict:
    """
    全面分析一个数的各种趣味数属性。
    
    Args:
        number: 要分析的整数
        
    Returns:
        dict: 包含各种属性分析的字典
        
    Examples:
        >>> analyze_number(153)
        {'number': 153, 'is_armstrong': True, 'is_happy': False, 'is_kaprekar': False, 'is_perfect': False, 'is_palindrome': False, 'is_abundant': False, 'is_deficient': True, 'digits': 3, 'digit_sum': 9, 'proper_divisors': [1, 3, 9, 17, 51]}
    """
    result = {
        'number': number,
        'is_armstrong': is_armstrong(number),
        'is_happy': is_happy(number),
        'is_kaprekar': is_kaprekar(number),
        'is_perfect': is_perfect(number),
        'is_palindrome': is_palindrome(number),
        'is_abundant': is_abundant(number),
        'is_deficient': is_deficient(number),
        'digits': count_armstrong_digits(number),
        'digit_sum': sum(int(d) for d in str(abs(number))),
        'proper_divisors': get_proper_divisors(abs(number)) if number > 0 else []
    }
    
    return result


def find_special_numbers(limit: int, number_type: str = 'all') -> dict:
    """
    查找指定范围内的特殊数。
    
    Args:
        limit: 上限（包含）
        number_type: 数的类型，可选值：
            - 'all': 所有类型
            - 'armstrong': 阿姆斯特朗数
            - 'happy': 快乐数
            - 'kaprekar': 卡普雷卡尔数
            - 'perfect': 完全数
            - 'palindrome': 回文数
        
    Returns:
        dict: 包含指定类型特殊数的字典
        
    Examples:
        >>> find_special_numbers(100, 'armstrong')
        {'armstrong': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 153]  # 注意：153 > 100 所以不在范围内
        {'armstrong': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}
    """
    result = {}
    
    if number_type in ('all', 'armstrong'):
        result['armstrong'] = find_armstrong_numbers(limit)
    
    if number_type in ('all', 'happy'):
        result['happy'] = find_happy_numbers(limit)
    
    if number_type in ('all', 'kaprekar'):
        result['kaprekar'] = find_kaprekar_numbers(limit)
    
    if number_type in ('all', 'perfect'):
        result['perfect'] = find_perfect_numbers(limit)
    
    if number_type in ('all', 'palindrome'):
        result['palindrome'] = find_palindrome_numbers(limit)
    
    return result


# ==================== 工具函数 ====================

def is_narcissistic(number: int) -> bool:
    """
    is_armstrong 的别名。阿姆斯特朗数也称为自恋数。
    """
    return is_armstrong(number)


def is_pluperfect(number: int) -> bool:
    """
    is_armstrong 的别名。阿姆斯特朗数也称为完全数字不变数。
    """
    return is_armstrong(number)


def digital_root(number: int) -> int:
    """
    计算一个数的数字根（反复求数位之和直到只剩一位数）。
    
    Args:
        number: 要计算的整数
        
    Returns:
        int: 数字根（1-9之间的数，或 0 如果原数为 0）
        
    Examples:
        >>> digital_root(38)
        2  # 3 + 8 = 11, 1 + 1 = 2
        >>> digital_root(12345)
        6  # 1 + 2 + 3 + 4 + 5 = 15, 1 + 5 = 6
    """
    if number == 0:
        return 0
    
    # 数学方法：数字根等于 n mod 9，如果余数为 0 则为 9
    return 9 if number % 9 == 0 else number % 9


def is_harshad(number: int) -> bool:
    """
    检测一个数是否为 Harshad 数（能被其数位之和整除）。
    
    Args:
        number: 要检测的整数
        
    Returns:
        bool: 如果是 Harshad 数返回 True
        
    Examples:
        >>> is_harshad(18)
        True  # 18 / (1 + 8) = 18 / 9 = 2
        >>> is_harshad(21)
        True  # 21 / (2 + 1) = 21 / 3 = 7
    """
    if number <= 0:
        return False
    
    digit_sum = sum(int(d) for d in str(number))
    return number % digit_sum == 0


def find_harshad_numbers(limit: int) -> List[int]:
    """
    查找指定范围内的所有 Harshad 数。
    
    Args:
        limit: 上限（包含）
        
    Returns:
        List[int]: 范围内的所有 Harshad 数列表
        
    Examples:
        >>> find_harshad_numbers(25)
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 18, 20, 21, 24]
    """
    return [num for num in range(1, limit + 1) if is_harshad(num)]


if __name__ == '__main__':
    # 演示功能
    print("=" * 60)
    print("阿姆斯特朗数与趣味数工具演示")
    print("=" * 60)
    
    # 阿姆斯特朗数演示
    print("\n【阿姆斯特朗数】")
    print(f"153 是阿姆斯特朗数: {is_armstrong(153)}")
    print(f"153 的位数、幂和、差值: {get_armstrong_digits(153)}")
    print(f"10000 以内的阿姆斯特朗数: {find_armstrong_numbers(10000)}")
    
    # 快乐数演示
    print("\n【快乐数】")
    print(f"19 是快乐数: {is_happy(19)}")
    print(f"19 的变换序列: {get_happy_sequence(19)}")
    print(f"100 以内的快乐数: {find_happy_numbers(100)}")
    
    # 卡普雷卡尔数演示
    print("\n【卡普雷卡尔数】")
    print(f"45 是卡普雷卡尔数: {is_kaprekar(45)}")
    print(f"1000 以内的卡普雷卡尔数: {find_kaprekar_numbers(1000)}")
    print(f"卡普雷卡尔程序 (3524): {kaprekar_routine(3524)}")
    
    # 完全数演示
    print("\n【完全数】")
    print(f"28 是完全数: {is_perfect(28)}")
    print(f"28 的真约数: {get_proper_divisors(28)}")
    print(f"10000 以内的完全数: {find_perfect_numbers(10000)}")
    
    # 回文数演示
    print("\n【回文数】")
    print(f"12321 是回文数: {is_palindrome(12321)}")
    print(f"123 的反转: {reverse_number(123)}")
    print(f"196 是 Lychrel 数候选: {is_lychrel(196)}")
    
    # Harshad 数演示
    print("\n【Harshad 数】")
    print(f"18 是 Harshad 数: {is_harshad(18)}")
    print(f"100 以内的 Harshad 数: {find_harshad_numbers(100)}")
    
    # 综合分析
    print("\n【综合分析 153】")
    import json
    print(json.dumps(analyze_number(153), indent=2))