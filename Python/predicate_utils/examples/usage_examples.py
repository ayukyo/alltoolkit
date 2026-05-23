# -*- coding: utf-8 -*-
"""
Predicate Utilities 使用示例

展示谓词构建与组合的各种用法。

Author: AllToolkit
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/AllToolkit/Python')

from predicate_utils.mod import (
    # 构建器函数
    eq, ne, lt, le, gt, ge, between, in_, not_in,
    isinstance_of, starts_with, ends_with, contains, matches,
    length, divisible_by, contains_all, contains_any,
    has_key, key_value, attr, item, predicate,
    all_of, any_of, none_of, exactly, at_least, at_most,
    implies,
    
    # 常用谓词实例
    is_none, is_not_none, is_empty, is_not_empty,
    is_positive, is_negative, is_zero, is_even, is_odd,
    is_integer, is_finite, is_nan,
    is_alnum, is_alpha, is_digit, is_lower, is_upper,
)


def example_basic_comparison():
    """基础比较谓词示例"""
    print("=" * 50)
    print("1. 基础比较谓词")
    print("=" * 50)
    
    # 等于
    p = eq(42)
    print(f"eq(42)(42) = {p(42)}")  # True
    print(f"eq(42)(41) = {p(41)}")  # False
    
    # 大于/小于
    print(f"gt(10)(15) = {gt(10)(15)}")  # True
    print(f"lt(10)(5) = {lt(10)(5)}")    # True
    
    # 区间
    p = between(1, 100)
    print(f"between(1, 100)(50) = {p(50)}")  # True
    print(f"between(1, 100)(0) = {p(0)}")    # False
    
    # 包含于集合
    p = in_(['apple', 'banana', 'orange'])
    print(f"in_(['apple', 'banana'])(apple) = {p('apple')}")  # True
    
    print()


def example_logical_combination():
    """逻辑组合示例"""
    print("=" * 50)
    print("2. 逻辑组合谓词")
    print("=" * 50)
    
    # AND 组合
    p = gt(0) & lt(100)
    print(f"gt(0) & lt(100)(50) = {p(50)}")  # True
    print(f"gt(0) & lt(100)(150) = {p(150)}")  # False
    
    # OR 组合
    p = lt(0) | gt(100)
    print(f"lt(0) | gt(100)(-5) = {p(-5)}")   # True
    print(f"lt(0) | gt(100)(50) = {p(50)}")   # False
    
    # NOT 组合
    p = ~eq(5)
    print(f"~eq(5)(5) = {p(5)}")    # False
    print(f"~eq(5)(10) = {p(10)}")  # True
    
    # XOR 组合
    p = is_even ^ is_positive
    print(f"is_even ^ is_positive(1) = {p(1)}")   # True (奇数正数)
    print(f"is_even ^ is_positive(2) = {p(2)}")   # False (偶数正数)
    print(f"is_even ^ is_positive(-2) = {p(-2)}")  # True (偶数负数)
    
    # 复杂组合
    p = (gt(0) & lt(50)) | (gt(100) & lt(200))
    print(f"复合区间检查(25) = {p(25)}")   # True
    print(f"复合区间检查(75) = {p(75)}")   # False
    print(f"复合区间检查(150) = {p(150)}") # True
    
    print()


def example_quantified_combination():
    """量化组合示例"""
    print("=" * 50)
    print("3. 量化组合谓词")
    print("=" * 50)
    
    # 所有条件都满足
    p = all_of(is_positive, is_even, divisible_by(4))
    print(f"all_of(正数,偶数,被4整除)(8) = {p(8)}")   # True
    print(f"all_of(正数,偶数,被4整除)(6) = {p(6)}")   # False (不被4整除)
    
    # 任一条件满足
    p = any_of(eq('a'), eq('b'), eq('c'))
    print(f"any_of(在a,b,c中)(a) = {p('a')}")  # True
    print(f"any_of(在a,b,c中)(d) = {p('d')}")  # False
    
    # 所有条件都不满足
    p = none_of(eq(1), eq(2), eq(3))
    print(f"none_of(不在1,2,3中)(4) = {p(4)}")  # True
    print(f"none_of(不在1,2,3中)(2) = {p(2)}")  # False
    
    # 恰好 N 个满足
    p = exactly(2, gt(0), gt(5), gt(10))
    print(f"exactly(2个大于)(8) = {p(8)}")   # True (gt0=True, gt5=True, gt10=False)
    print(f"exactly(2个大于)(15) = {p(15)}")  # False (3个都满足)
    
    # 至少 N 个满足
    p = at_least(2, is_alpha, is_digit, is_lower)
    print(f"at_least(2个满足)(abc) = {p('abc')}")  # True (字母+小写)
    print(f"at_least(2个满足)(ABC) = {p('ABC')}")  # False (只有字母)
    
    # 最多 N 个满足
    p = at_most(1, gt(0), gt(5), gt(10))
    print(f"at_most(1个满足)(3) = {p(3)}")   # True (只有gt0)
    print(f"at_most(1个满足)(8) = {p(8)}")   # False (gt0和gt5)
    
    print()


def example_string_predicates():
    """字符串谓词示例"""
    print("=" * 50)
    print("4. 字符串谓词")
    print("=" * 50)
    
    # 开头/结尾
    print(f"starts_with('Hello')(Hello World) = {starts_with('Hello')('Hello World')}")  # True
    print(f"ends_with('.py')(script.py) = {ends_with('.py')('script.py')}")  # True
    
    # 包含
    print(f"contains('Python')(I love Python) = {contains('Python')('I love Python')}")  # True
    
    # 正则匹配
    email_pattern = matches(r'^[\w.-]+@[\w.-]+\.\w+$')
    print(f"邮箱格式(user@example.com) = {email_pattern('user@example.com')}")  # True
    print(f"邮箱格式(invalid) = {email_pattern('invalid')}")  # False
    
    # 长度检查
    p = length(min_len=8, max_len=20)
    print(f"长度8-20(password123) = {p('password123')}")  # True
    print(f"长度8-20(short) = {p('short')}")  # False
    
    # 字符类型
    print(f"is_alpha(abc) = {is_alpha('abc')}")   # True
    print(f"is_digit(123) = {is_digit('123')}")   # True
    print(f"is_lower(hello) = {is_lower('hello')}")  # True
    print(f"is_upper(HELLO) = {is_upper('HELLO')}")  # True
    
    print()


def example_number_predicates():
    """数值谓词示例"""
    print("=" * 50)
    print("5. 数值谓词")
    print("=" * 50)
    
    # 正负零
    print(f"is_positive(42) = {is_positive(42)}")   # True
    print(f"is_negative(-42) = {is_negative(-42)}") # True
    print(f"is_zero(0) = {is_zero(0)}")             # True
    
    # 奇偶
    print(f"is_even(4) = {is_even(4)}")  # True
    print(f"is_odd(5) = {is_odd(5)}")    # True
    
    # 整除
    p = divisible_by(3)
    print(f"divisible_by(3)(9) = {p(9)}")  # True
    print(f"divisible_by(3)(10) = {p(10)}")  # False
    
    # 数值类型
    print(f"is_integer(5) = {is_integer(5)}")       # True
    print(f"is_integer(5.0) = {is_integer(5.0)}")   # True (5.0是整数)
    print(f"is_integer(5.5) = {is_integer(5.5)}")   # False
    
    print()


def example_type_predicates():
    """类型谓词示例"""
    print("=" * 50)
    print("6. 类型谓词")
    print("=" * 50)
    
    # None 检查
    print(f"is_none(None) = {is_none(None)}")  # True
    print(f"is_not_none(0) = {is_not_none(0)}")  # True
    
    # 实例类型
    p = isinstance_of(int)
    print(f"isinstance_of(int)(42) = {p(42)}")  # True
    print(f"isinstance_of(int)(42.0) = {p(42.0)}")  # False
    
    # 多类型
    p = isinstance_of((int, float))
    print(f"isinstance_of(int|float)(42) = {p(42)}")    # True
    print(f"isinstance_of(int|float)(42.0) = {p(42.0)}")  # True
    
    print()


def example_collection_predicates():
    """集合谓词示例"""
    print("=" * 50)
    print("7. 集合谓词")
    print("=" * 50)
    
    # 包含元素
    p = contains_all([1, 2])
    print(f"contains_all([1,2])([1,2,3]) = {p([1, 2, 3])}")  # True
    
    p = contains_any(['a', 'b'])
    print(f"contains_any(['a','b'])(['a','c']) = {p(['a', 'c'])}")  # True
    
    # 空检查
    print(f"is_empty([]) = {is_empty([])}")  # True
    print(f"is_empty(None) = {is_empty(None)}")  # True
    print(f"is_not_empty([1]) = {is_not_empty([1])}")  # True
    
    print()


def example_dict_predicates():
    """字典谓词示例"""
    print("=" * 50)
    print("8. 字典谓词")
    print("=" * 50)
    
    user = {'name': 'John', 'age': 25, 'email': 'john@example.com'}
    
    # 键检查
    print(f"has_key('name')(user) = {has_key('name')(user)}")  # True
    
    # 键值检查
    p = key_value('age', ge(18))
    print(f"age >= 18(user) = {p(user)}")  # True
    
    p = key_value('email', matches(r'.*@.*\.com'))
    print(f"邮箱格式检查(user) = {p(user)}")  # True
    
    print()


def example_filter_operations():
    """过滤操作示例"""
    print("=" * 50)
    print("9. 过滤操作")
    print("=" * 50)
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # 过滤偶数
    even_numbers = is_even.filter(numbers)
    print(f"偶数: {even_numbers}")
    
    # 过滤正数
    values = [-5, -2, 0, 3, 7, 12]
    positive_values = is_positive.filter(values)
    print(f"正数: {positive_values}")
    
    # 区间过滤
    scores = [45, 65, 78, 92, 35, 88, 72]
    passing_scores = between(60, 100).filter(scores)
    print(f"及格分数: {passing_scores}")
    
    # 统计
    print(f"偶数数量: {is_even.count(numbers)}")
    
    # 查找第一个
    first_gt_5 = gt(5).first(numbers)
    print(f"第一个大于5的数: {first_gt_5}")
    
    # 检查是否满足
    print(f"是否有大于8的数: {gt(8).any(numbers)}")
    print(f"是否都大于0: {gt(0).all(numbers)}")
    
    # 反向过滤
    odd_numbers = is_even.reject(numbers)
    print(f"奇数: {odd_numbers}")
    
    print()


def example_custom_predicate():
    """自定义谓词示例"""
    print("=" * 50)
    print("10. 自定义谓词")
    print("=" * 50)
    
    # 使用 lambda
    is_palindrome = predicate(lambda s: s == s[::-1], "是回文")
    print(f"是回文(radar) = {is_palindrome('radar')}")  # True
    print(f"是回文(hello) = {is_palindrome('hello')}")  # False
    
    # 使用函数
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    prime_predicate = predicate(is_prime, "是质数")
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    primes = prime_predicate.filter(numbers)
    print(f"质数: {primes}")
    
    print()


def example_complex_validation():
    """复杂验证示例"""
    print("=" * 50)
    print("11. 复杂验证场景")
    print("=" * 50)
    
    # 用户数据验证
    users = [
        {'name': 'Alice', 'age': 25, 'email': 'alice@example.com', 'active': True},
        {'name': '', 'age': 30, 'email': 'bob@example.com', 'active': True},
        {'name': 'Charlie', 'age': 15, 'email': 'charlie@example.com', 'active': False},
        {'name': 'Diana', 'age': 28, 'email': 'invalid-email', 'active': True},
    ]
    
    # 有效用户：名字非空，年龄>=18，邮箱格式正确，已激活
    valid_user_predicate = all_of(
        key_value('name', length(min_len=1)),
        key_value('age', ge(18)),
        key_value('email', matches(r'^[\w.-]+@[\w.-]+\.\w+$')),
        key_value('active', eq(True))
    )
    
    valid_users = valid_user_predicate.filter(users)
    print(f"有效用户数: {len(valid_users)}")
    for user in valid_users:
        print(f"  - {user['name']} ({user['email']})")
    
    # 产品价格验证
    products = [
        {'name': 'Laptop', 'price': 999.99, 'stock': 50, 'category': 'electronics'},
        {'name': 'Mouse', 'price': -10, 'stock': 100, 'category': 'electronics'},
        {'name': 'Keyboard', 'price': 49.99, 'stock': 0, 'category': 'electronics'},
    ]
    
    # 有效产品：价格正数，有库存
    valid_product_predicate = all_of(
        key_value('price', is_positive),
        key_value('stock', gt(0))
    )
    
    valid_products = valid_product_predicate.filter(products)
    print(f"\n有效产品数: {len(valid_products)}")
    for product in valid_products:
        print(f"  - {product['name']}: $${product['price']}")
    
    print()


def example_rule_engine():
    """规则引擎示例"""
    print("=" * 50)
    print("12. 简单规则引擎")
    print("=" * 50)
    
    # 订单处理规则
    orders = [
        {'amount': 5000, 'customer_type': 'vip', 'items': 3},
        {'amount': 100, 'customer_type': 'normal', 'items': 1},
        {'amount': 2000, 'customer_type': 'vip', 'items': 10},
        {'amount': 3000, 'customer_type': 'normal', 'items': 5},
    ]
    
    # VIP客户订单 >= 1000 需要审批
    vip_approval_rule = all_of(
        key_value('customer_type', eq('vip')),
        key_value('amount', ge(1000))
    )
    
    # 普通客户订单 >= 3000 需要审批
    normal_approval_rule = all_of(
        key_value('customer_type', eq('normal')),
        key_value('amount', ge(3000))
    )
    
    # 综合审批规则
    needs_approval = vip_approval_rule | normal_approval_rule
    
    approval_orders = needs_approval.filter(orders)
    print(f"需要审批的订单数: {len(approval_orders)}")
    for order in approval_orders:
        print(f"  - {order['customer_type']}: ¥{order['amount']}, {order['items']}件")
    
    # 蕴涵规则：如果是VIP，则订单金额应该 >= 500（业务约束检查）
    vip_min_amount_rule = implies(
        key_value('customer_type', eq('vip')),
        key_value('amount', ge(500))
    )
    
    # 检查是否所有订单都满足业务约束
    print(f"\n所有订单都满足VIP最小金额约束: {vip_min_amount_rule.all(orders)}")
    
    print()


def main():
    """运行所有示例"""
    example_basic_comparison()
    example_logical_combination()
    example_quantified_combination()
    example_string_predicates()
    example_number_predicates()
    example_type_predicates()
    example_collection_predicates()
    example_dict_predicates()
    example_filter_operations()
    example_custom_predicate()
    example_complex_validation()
    example_rule_engine()
    
    print("=" * 50)
    print("所有示例完成!")
    print("=" * 50)


if __name__ == '__main__':
    main()