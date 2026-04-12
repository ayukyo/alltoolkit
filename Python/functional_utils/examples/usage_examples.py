# -*- coding: utf-8 -*-
"""
AllToolkit - Functional Programming Utilities 使用示例

展示各种函数式编程工具的实际应用场景。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    curry, curry_n, compose, compose_left, pipe,
    partial, partial_right, flip, memoize, memoize_with_ttl,
    Lazy, lazy, take, take_while, drop, drop_while, iterate,
    flatten, flatten_deep, chunk, sliding_window, mapcat,
    filter_map, reduce, reduce_right, scan, partition,
    group_by, unique, all_pred, any_pred, not_pred,
    eq, gt, lt, ge, le, cond, when, unless,
    identity, constantly, tap, noop, call_times, apply_to
)


# =============================================================================
# 示例 1: 柯里化 - 构建可复用的函数
# =============================================================================

def example_curry():
    """柯里化示例"""
    print("\n" + "="*60)
    print("示例 1: 柯里化 (Curry)")
    print("="*60)
    
    # 定义一个普通函数
    def create_greeting(greeting, punctuation, name):
        return f"{greeting}, {name}{punctuation}"
    
    # 柯里化
    curried_greet = curry(create_greeting)
    
    # 创建 specialized 函数
    say_hello = curried_greet("Hello")
    say_hello_exclaim = say_hello("!")
    
    # 使用
    print(f"say_hello_exclaim('Alice') = {say_hello_exclaim('Alice')}")
    print(f"say_hello_exclaim('Bob') = {say_hello_exclaim('Bob')}")
    
    # 也可以直接链式调用
    result = curried_greet("Hi")(".")("Charlie")
    print(f"curried_greet('Hi')('.')('Charlie') = {result}")
    
    # 使用装饰器语法
    @curry
    def multiply(a, b, c):
        return a * b * c
    
    double = multiply(2)
    double_and_triple = double(3)
    print(f"double_and_triple(4) = {double_and_triple(4)}")  # 2*3*4=24


# =============================================================================
# 示例 2: 函数管道 - 优雅的数据处理
# =============================================================================

def example_pipe():
    """函数管道示例"""
    print("\n" + "="*60)
    print("示例 2: 函数管道 (Pipe)")
    print("="*60)
    
    # 数据处理管道
    process_numbers = pipe(
        lambda x: range(1, x + 1),           # 生成 1 到 n
        lambda nums: filter(lambda n: n % 2 == 0, nums),  # 过滤偶数
        lambda nums: map(lambda n: n * 2, nums),  # 每个数乘以 2
        list,                                 # 转为列表
        lambda nums: sum(nums),               # 求和
    )
    
    result = process_numbers(10)
    print(f"process_numbers(10) = {result}")
    # 偶数：2,4,6,8,10 → 乘以 2：4,8,12,16,20 → 求和：60
    
    # 字符串处理管道
    process_text = pipe(
        str.lower,
        lambda s: s.replace(',', ''),
        lambda s: s.split(),
        lambda words: filter(lambda w: len(w) > 3, words),
        list,
    )
    
    text = "Hello, World, This, Is, A, Test"
    result = process_text(text)
    print(f"处理文本：'{text}'")
    print(f"结果：{result}")


# =============================================================================
# 示例 3: 记忆化 - 优化递归性能
# =============================================================================

def example_memoize():
    """记忆化示例"""
    print("\n" + "="*60)
    print("示例 3: 记忆化 (Memoize)")
    print("="*60)
    
    import time
    
    # 斐波那契数列
    @memoize
    def fibonacci(n):
        if n < 2:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    # 第一次计算
    start = time.time()
    result1 = fibonacci(30)
    time1 = time.time() - start
    
    # 第二次调用（缓存命中）
    start = time.time()
    result2 = fibonacci(30)
    time2 = time.time() - start
    
    print(f"fibonacci(30) = {result1}")
    print(f"第一次计算时间：{time1*1000:.2f}ms")
    print(f"第二次计算时间：{time2*1000:.2f}ms (缓存命中)")
    print(f"缓存大小：{fibonacci.cache_info()}")
    
    # 带 TTL 的记忆化
    call_count = 0
    
    @memoize_with_ttl(ttl_seconds=2)
    def get_current_time():
        nonlocal call_count
        call_count += 1
        return time.strftime("%H:%M:%S")
    
    print(f"\n带 TTL 的记忆化:")
    print(f"第一次调用：{get_current_time()} (调用次数：{call_count})")
    print(f"第二次调用：{get_current_time()} (调用次数：{call_count})")
    
    time.sleep(2.1)  # 等待过期
    print(f"过期后调用：{get_current_time()} (调用次数：{call_count})")


# =============================================================================
# 示例 4: 迭代器工具 - 高效处理序列
# =============================================================================

def example_iterators():
    """迭代器工具示例"""
    print("\n" + "="*60)
    print("示例 4: 迭代器工具 (Iterator Utilities)")
    print("="*60)
    
    numbers = list(range(1, 11))
    print(f"原始数据：{numbers}")
    
    # take - 取前 N 个
    print(f"take(3) = {take(3, numbers)}")
    
    # drop - 丢弃前 N 个
    print(f"drop(3) = {drop(3, numbers)}")
    
    # take_while - 取直到条件不满足
    print(f"take_while(x < 5) = {take_while(lambda x: x < 5, numbers)}")
    
    # chunk - 分块
    print(f"chunk(3) = {list(chunk(3, numbers))}")
    
    # sliding_window - 滑动窗口
    print(f"sliding_window(3) = {list(sliding_window(3, numbers))}")
    
    # iterate - 生成迭代序列
    print(f"iterate(x*2, 1, 6) = {list(iterate(lambda x: x * 2, 1, 6))}")
    
    # flatten - 展平
    nested = [[1, 2], [3, 4], [5, 6]]
    print(f"flatten({nested}) = {list(flatten(nested))}")
    
    # flatten_deep - 深度展平
    deeply_nested = [1, [2, [3, [4, [5]]]]]
    print(f"flatten_deep({deeply_nested}, depth=2) = {list(flatten_deep(deeply_nested, max_depth=2))}")


# =============================================================================
# 示例 5: 集合操作 - 函数式数据处理
# =============================================================================

def example_collections():
    """集合操作示例"""
    print("\n" + "="*60)
    print("示例 5: 集合操作 (Collection Operations)")
    print("="*60)
    
    # mapcat - map + flatten
    numbers = [1, 2, 3]
    result = mapcat(lambda x: [x, x * 2], numbers)
    print(f"mapcat(lambda x: [x, x*2], {numbers}) = {result}")
    
    # filter_map - filter + map
    def safe_int(x):
        try:
            return int(x)
        except ValueError:
            return None
    
    mixed = ['1', 'a', '2', 'b', '3']
    result = filter_map(safe_int, mixed)
    print(f"filter_map(safe_int, {mixed}) = {result}")
    
    # reduce - 归约
    numbers = [1, 2, 3, 4, 5]
    sum_result = reduce(lambda acc, x: acc + x, numbers)
    product_result = reduce(lambda acc, x: acc * x, numbers, 1)
    print(f"reduce(sum, {numbers}) = {sum_result}")
    print(f"reduce(product, {numbers}) = {product_result}")
    
    # scan - 累积
    running_sum = scan(lambda acc, x: acc + x, numbers)
    print(f"scan(sum, {numbers}) = {running_sum}")
    
    # partition - 分区
    evens, odds = partition(lambda x: x % 2 == 0, numbers)
    print(f"partition(is_even, {numbers}) = 偶数:{evens}, 奇数:{odds}")
    
    # group_by - 分组
    words = ['a', 'bb', 'ccc', 'dd', 'eee']
    grouped = group_by(len, words)
    print(f"group_by(len, {words}) = {grouped}")
    
    # unique - 去重
    with_duplicates = [1, 2, 2, 3, 1, 4, 3]
    result = unique(with_duplicates)
    print(f"unique({with_duplicates}) = {result}")


# =============================================================================
# 示例 6: 谓词逻辑 - 组合条件
# =============================================================================

def example_predicates():
    """谓词逻辑示例"""
    print("\n" + "="*60)
    print("示例 6: 谓词逻辑 (Predicate Logic)")
    print("="*60)
    
    numbers = list(range(1, 11))
    
    # 组合谓词
    is_positive = lambda x: x > 0
    is_even = lambda x: x % 2 == 0
    is_positive_even = all_pred(is_positive, is_even)
    
    result = list(filter(is_positive_even, numbers))
    print(f"all_pred(is_positive, is_even) 过滤 {numbers} = {result}")
    
    # 任一条件
    is_zero = lambda x: x == 0
    is_negative = lambda x: x < 0
    is_non_positive = any_pred(is_zero, is_negative)
    
    test_nums = [-3, -1, 0, 1, 3]
    result = list(filter(is_non_positive, test_nums))
    print(f"any_pred(is_zero, is_negative) 过滤 {test_nums} = {result}")
    
    # 取反
    is_odd = not_pred(is_even)
    result = list(filter(is_odd, numbers))
    print(f"not_pred(is_even) 过滤 {numbers} = {result}")
    
    # 内置比较谓词
    print(f"\n内置比较谓词:")
    print(f"  filter(eq(5), {numbers}) = {list(filter(eq(5), numbers))}")
    print(f"  filter(gt(5), {numbers}) = {list(filter(gt(5), numbers))}")
    print(f"  filter(lt(5), {numbers}) = {list(filter(lt(5), numbers))}")
    print(f"  filter(ge(5), {numbers}) = {list(filter(ge(5), numbers))}")
    print(f"  filter(le(5), {numbers}) = {list(filter(le(5), numbers))}")


# =============================================================================
# 示例 7: 条件执行 - 函数式条件语句
# =============================================================================

def example_conditionals():
    """条件执行示例"""
    print("\n" + "="*60)
    print("示例 7: 条件执行 (Conditional Execution)")
    print("="*60)
    
    # cond - 条件表达式
    classify_number = cond(
        (lambda x: x > 0, lambda x: f"{x} 是正数"),
        (lambda x: x < 0, lambda x: f"{x} 是负数"),
        (lambda x: True, lambda x: "零"),
    )
    
    print("cond 分类:")
    for num in [-5, 0, 5]:
        print(f"  {num} → {classify_number(num)}")
    
    # when - 条件执行
    print("\nwhen 示例:")
    log_positive = when(
        lambda x: x > 0,
        lambda x: f"记录正数：{x}"
    )
    
    for num in [-1, 0, 1]:
        result = log_positive(num)
        if result:
            print(f"  {num} → {result}")
        else:
            print(f"  {num} → (无输出)")
    
    # unless - 反向条件
    print("\nunless 示例:")
    log_non_positive = unless(
        lambda x: x > 0,
        lambda x: f"记录非正数：{x}"
    )
    
    for num in [-1, 0, 1]:
        result = log_non_positive(num)
        if result:
            print(f"  {num} → {result}")
        else:
            print(f"  {num} → (无输出)")


# =============================================================================
# 示例 8: 实用工具 - 辅助函数
# =============================================================================

def example_utilities():
    """实用工具示例"""
    print("\n" + "="*60)
    print("示例 8: 实用工具 (Utilities)")
    print("="*60)
    
    # identity - 恒等函数
    print(f"identity(42) = {identity(42)}")
    print(f"identity([1,2,3]) = {identity([1,2,3])}")
    
    # constantly - 常量函数
    always_true = constantly(True)
    print(f"\nconstantly(True)() = {always_true()}")
    print(f"constantly(True)(1,2,3) = {always_true(1, 2, 3)}")
    
    # tap - 调试辅助
    print("\ntap 调试管道:")
    result = pipe(
        lambda x: x * 2,
        tap(lambda x: print(f"  步骤 1 结果：{x}")),
        lambda x: x + 1,
        tap(lambda x: print(f"  步骤 2 结果：{x}")),
        lambda x: x ** 2,
    )(5)
    print(f"最终结果：{result}")
    
    # apply_to - 应用到多个函数
    print("\napply_to 示例:")
    value = 10
    results = apply_to(
        value,
        lambda x: x * 2,
        lambda x: x + 5,
        lambda x: x ** 2,
        lambda x: str(x) + "!"
    )
    print(f"apply_to({value}, [x*2, x+5, x**2, str(x)+'!']) = {results}")
    
    # call_times - 多次调用
    print("\ncall_times 示例:")
    counter = 0
    def increment():
        nonlocal counter
        counter += 1
        return counter
    
    results = call_times(5, increment)
    print(f"call_times(5, increment) = {results}")


# =============================================================================
# 示例 9: 综合示例 - 数据处理管道
# =============================================================================

def example_comprehensive():
    """综合示例"""
    print("\n" + "="*60)
    print("示例 9: 综合示例 - 用户数据处理")
    print("="*60)
    
    # 模拟用户数据
    users = [
        {'name': 'Alice', 'age': 25, 'score': 85},
        {'name': 'Bob', 'age': 30, 'score': 92},
        {'name': 'Charlie', 'age': 25, 'score': 78},
        {'name': 'Diana', 'age': 35, 'score': 95},
        {'name': 'Eve', 'age': 25, 'score': 88},
    ]
    
    # 构建数据处理管道
    process_users = pipe(
        # 过滤 30 岁以下的用户
        lambda users: list(filter(lambda u: u['age'] < 30, users)),
        # 提取姓名和分数
        mapcat(lambda u: [(u['name'], u['score'])]),
        # 按分数排序
        lambda pairs: sorted(pairs, key=lambda x: x[1], reverse=True),
        # 取前 3 名
        lambda pairs: take(3, pairs),
        # 格式化输出
        lambda top3: [f"{name}: {score}分" for name, score in top3],
    )
    
    result = process_users(users)
    print("30 岁以下用户分数排行榜 (前 3 名):")
    for item in result:
        print(f"  {item}")
    
    # 另一个管道：按年龄分组
    print("\n按年龄分组:")
    grouped = group_by(lambda u: u['age'], users)
    for age, group in sorted(grouped.items()):
        names = [u['name'] for u in group]
        print(f"  {age}岁：{', '.join(names)}")


# =============================================================================
# 示例 10: 惰性求值 - 延迟计算
# =============================================================================

def example_lazy():
    """惰性求值示例"""
    print("\n" + "="*60)
    print("示例 10: 惰性求值 (Lazy Evaluation)")
    print("="*60)
    
    computed = False
    
    def expensive_computation():
        nonlocal computed
        print("  [执行昂贵计算...]")
        computed = True
        return {'result': 42, 'data': list(range(1000))}
    
    # 创建惰性对象
    lazy_result = lazy(expensive_computation)
    print(f"创建后，computed = {computed}")
    
    # 访问值时才计算
    print("访问 .value:")
    result = lazy_result.value
    print(f"computed = {computed}, result = {result['result']}")
    
    # 再次访问不会重新计算
    print("再次访问 .value:")
    computed = False  # 重置标记
    result2 = lazy_result.value
    print(f"computed = {computed} (没有重新计算)")
    
    # 重置后可以重新计算
    print("调用 .reset() 后再次访问:")
    lazy_result.reset()
    result3 = lazy_result.value
    print(f"computed = {computed} (重新计算了)")


# =============================================================================
# 主程序
# =============================================================================

def main():
    """运行所有示例"""
    print("\n" + "="*60)
    print("  AllToolkit - Functional Programming Utilities")
    print("  函数式编程工具使用示例")
    print("="*60)
    
    examples = [
        example_curry,
        example_pipe,
        example_memoize,
        example_iterators,
        example_collections,
        example_predicates,
        example_conditionals,
        example_utilities,
        example_comprehensive,
        example_lazy,
    ]
    
    for example in examples:
        example()
    
    print("\n" + "="*60)
    print("  所有示例运行完成！")
    print("="*60)


if __name__ == '__main__':
    main()
