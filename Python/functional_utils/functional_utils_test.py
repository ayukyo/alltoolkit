# -*- coding: utf-8 -*-
"""
AllToolkit - Functional Programming Utilities 测试套件

测试所有函数式编程工具函数的功能。
"""

import sys
import os
import time

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import *


# =============================================================================
# 测试工具函数
# =============================================================================

def print_section(title: str):
    """打印测试章节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def print_test(name: str, passed: bool, details: str = ''):
    """打印测试结果"""
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"  {status}: {name}")
    if details:
        print(f"         {details}")
    return passed


# =============================================================================
# 测试用例：柯里化
# =============================================================================

def test_curry():
    """测试柯里化"""
    print_section("测试柯里化 (Curry)")
    
    all_passed = True
    
    # 测试基本柯里化
    def add(a, b, c):
        return a + b + c
    
    curried_add = curry(add)
    
    # 完全柯里化
    result = curried_add(1)(2)(3)
    passed = result == 6
    all_passed &= print_test("完全柯里化", passed, f"curried_add(1)(2)(3) = {result}")
    
    # 部分应用
    add_one_and_two = curried_add(1, 2)
    result = add_one_and_two(3)
    passed = result == 6
    all_passed &= print_test("部分应用", passed, f"curried_add(1, 2)(3) = {result}")
    
    # 混合参数
    result = curried_add(1)(2, 3)
    passed = result == 6
    all_passed &= print_test("混合参数", passed, f"curried_add(1)(2, 3) = {result}")
    
    # 测试带默认值的函数
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}!"
    
    curried_greet = curry(greet)
    # 带默认值时，只需提供一个参数即可调用
    result = curried_greet("Alice")
    passed = result == "Hello, Alice!"
    all_passed &= print_test("带默认值", passed, f"结果：{result}")
    
    return all_passed


def test_curry_n():
    """测试固定元数柯里化"""
    print_section("测试固定元数柯里化 (Curry N)")
    
    all_passed = True
    
    def multiply(a, b, c):
        return a * b * c
    
    curried = curry_n(multiply, 3)
    result = curried(2)(3)(4)
    passed = result == 24
    all_passed &= print_test("固定元数柯里化", passed, f"curry_n(multiply, 3)(2)(3)(4) = {result}")
    
    return all_passed


# =============================================================================
# 测试用例：函数组合
# =============================================================================

def test_compose():
    """测试函数组合"""
    print_section("测试函数组合 (Compose)")
    
    all_passed = True
    
    def double(x):
        return x * 2
    
    def add_one(x):
        return x + 1
    
    def square(x):
        return x ** 2
    
    # compose(f, g, h)(x) = f(g(h(x)))
    result = compose(square, add_one, double)(3)
    # double(3) = 6, add_one(6) = 7, square(7) = 49
    passed = result == 49
    all_passed &= print_test("从右到左组合", passed, f"compose(square, add_one, double)(3) = {result}")
    
    # 空组合
    identity_result = compose()(5)
    passed = identity_result == 5
    all_passed &= print_test("空组合（恒等）", passed, f"compose()(5) = {identity_result}")
    
    return all_passed


def test_compose_left():
    """测试从左到右组合"""
    print_section("测试从左到右组合 (Compose Left)")
    
    all_passed = True
    
    def double(x):
        return x * 2
    
    def add_one(x):
        return x + 1
    
    # compose_left(f, g)(x) = g(f(x))
    result = compose_left(double, add_one)(3)
    # double(3) = 6, add_one(6) = 7
    passed = result == 7
    all_passed &= print_test("从左到右组合", passed, f"compose_left(double, add_one)(3) = {result}")
    
    return all_passed


def test_pipe():
    """测试管道"""
    print_section("测试管道 (Pipe)")
    
    all_passed = True
    
    result = pipe(
        lambda x: x * 2,
        lambda x: x + 1,
        lambda x: x ** 2
    )(3)
    # ((3 * 2) + 1) ** 2 = 49
    passed = result == 49
    all_passed &= print_test("管道操作", passed, f"pipe(...)(3) = {result}")
    
    return all_passed


# =============================================================================
# 测试用例：偏函数
# =============================================================================

def test_partial():
    """测试偏函数"""
    print_section("测试偏函数 (Partial)")
    
    all_passed = True
    
    def multiply(a, b, c):
        return a * b * c
    
    # 绑定第一个参数
    double = partial(multiply, 2)
    result = double(3, 4)
    passed = result == 24
    all_passed &= print_test("绑定位置参数", passed, f"partial(multiply, 2)(3, 4) = {result}")
    
    # 绑定关键字参数
    multiply_by_10 = partial(multiply, c=10)
    result = multiply_by_10(2, 3)
    passed = result == 60
    all_passed &= print_test("绑定关键字参数", passed, f"partial(multiply, c=10)(2, 3) = {result}")
    
    return all_passed


def test_partial_right():
    """测试右侧偏函数"""
    print_section("测试右侧偏函数 (Partial Right)")
    
    all_passed = True
    
    def divide(a, b):
        return a / b
    
    # 从右侧绑定
    divide_by_2 = partial_right(divide, 2)
    result = divide_by_2(10)
    passed = result == 5.0
    all_passed &= print_test("右侧绑定", passed, f"partial_right(divide, 2)(10) = {result}")
    
    return all_passed


def test_flip():
    """测试参数翻转"""
    print_section("测试参数翻转 (Flip)")
    
    all_passed = True
    
    def greet(greeting, name):
        return f"{greeting}, {name}!"
    
    flipped = flip(greet)
    result = flipped("Alice", "Hello")
    passed = result == "Hello, Alice!"
    all_passed &= print_test("翻转参数", passed, f"flip(greet)('Alice', 'Hello') = '{result}'")
    
    return all_passed


# =============================================================================
# 测试用例：记忆化
# =============================================================================

def test_memoize():
    """测试记忆化"""
    print_section("测试记忆化 (Memoize)")
    
    all_passed = True
    
    call_count = 0
    
    @memoize
    def fibonacci(n):
        nonlocal call_count
        call_count += 1
        if n < 2:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    # 第一次计算
    result1 = fibonacci(10)
    first_call_count = call_count
    passed = result1 == 55
    all_passed &= print_test("斐波那契计算", passed, f"fibonacci(10) = {result1}")
    
    # 第二次调用应该使用缓存
    call_count = 0
    result2 = fibonacci(10)
    passed = result2 == 55 and call_count == 0
    all_passed &= print_test("缓存命中", passed, f"第二次调用，新增计算次数：{call_count}")
    
    # 测试 cache_info
    passed = fibonacci.cache_info() > 0
    all_passed &= print_test("缓存信息", passed, f"缓存大小：{fibonacci.cache_info()}")
    
    # 测试 cache_clear
    fibonacci.cache_clear()
    passed = fibonacci.cache_info() == 0
    all_passed &= print_test("清除缓存", passed, f"清除后缓存大小：{fibonacci.cache_info()}")
    
    return all_passed


def test_memoize_with_ttl():
    """测试带 TTL 的记忆化"""
    print_section("测试带 TTL 的记忆化 (Memoize with TTL)")
    
    all_passed = True
    
    call_count = 0
    
    @memoize_with_ttl(1)  # 1 秒过期
    def get_timestamp():
        nonlocal call_count
        call_count += 1
        return time.time()
    
    # 第一次调用
    ts1 = get_timestamp()
    first_count = call_count
    passed = first_count == 1
    all_passed &= print_test("首次调用", passed, f"调用次数：{first_count}")
    
    # 立即再次调用，应该使用缓存
    call_count = 0
    ts2 = get_timestamp()
    passed = call_count == 0 and ts1 == ts2
    all_passed &= print_test("缓存命中", passed, f"调用次数：{call_count}")
    
    # 等待过期
    time.sleep(1.1)
    call_count = 0
    ts3 = get_timestamp()
    passed = call_count == 1
    all_passed &= print_test("缓存过期", passed, f"过期后调用次数：{call_count}")
    
    return all_passed


# =============================================================================
# 测试用例：惰性求值
# =============================================================================

def test_lazy():
    """测试惰性求值"""
    print_section("测试惰性求值 (Lazy)")
    
    all_passed = True
    
    computed = False
    
    def expensive_computation():
        nonlocal computed
        computed = True
        return 42
    
    lazy_val = lazy(expensive_computation)
    
    # 创建时不应计算
    passed = not computed
    all_passed &= print_test("延迟计算", passed, f"创建时已计算：{computed}")
    
    # 访问值时才计算
    result = lazy_val.value
    passed = computed and result == 42
    all_passed &= print_test("访问时计算", passed, f"结果：{result}, 已计算：{computed}")
    
    # 再次访问不应重新计算
    computed = False
    result2 = lazy_val.value
    passed = not computed and result2 == 42
    all_passed &= print_test("缓存结果", passed, f"再次访问：{result2}")
    
    # 测试 reset
    lazy_val.reset()
    passed = not lazy_val._computed
    all_passed &= print_test("重置缓存", passed, f"重置后已计算：{lazy_val._computed}")
    
    return all_passed


# =============================================================================
# 测试用例：迭代器工具
# =============================================================================

def test_take():
    """测试 take"""
    print_section("测试 Take")
    
    all_passed = True
    
    result = take(3, [1, 2, 3, 4, 5])
    passed = result == [1, 2, 3]
    all_passed &= print_test("take(3, ...)", passed, f"结果：{result}")
    
    result = take(10, [1, 2, 3])
    passed = result == [1, 2, 3]
    all_passed &= print_test("take 超过长度", passed, f"结果：{result}")
    
    return all_passed


def test_take_while():
    """测试 take_while"""
    print_section("测试 Take While")
    
    all_passed = True
    
    result = take_while(lambda x: x < 5, [1, 2, 3, 6, 7])
    passed = result == [1, 2, 3]
    all_passed &= print_test("take_while", passed, f"结果：{result}")
    
    return all_passed


def test_drop():
    """测试 drop"""
    print_section("测试 Drop")
    
    all_passed = True
    
    result = drop(2, [1, 2, 3, 4, 5])
    passed = result == [3, 4, 5]
    all_passed &= print_test("drop(2, ...)", passed, f"结果：{result}")
    
    return all_passed


def test_drop_while():
    """测试 drop_while"""
    print_section("测试 Drop While")
    
    all_passed = True
    
    result = drop_while(lambda x: x < 3, [1, 2, 3, 4, 5])
    passed = result == [3, 4, 5]
    all_passed &= print_test("drop_while", passed, f"结果：{result}")
    
    return all_passed


def test_iterate():
    """测试 iterate"""
    print_section("测试 Iterate")
    
    all_passed = True
    
    result = list(iterate(lambda x: x * 2, 1, 5))
    passed = result == [1, 2, 4, 8, 16]
    all_passed &= print_test("iterate", passed, f"结果：{result}")
    
    return all_passed


def test_flatten():
    """测试 flatten"""
    print_section("测试 Flatten")
    
    all_passed = True
    
    result = list(flatten([[1, 2], [3, 4], [5]]))
    passed = result == [1, 2, 3, 4, 5]
    all_passed &= print_test("flatten", passed, f"结果：{result}")
    
    result = list(flatten_deep([1, [2, [3, [4]]]], max_depth=2))
    # depth=0: [1, [2, [3, [4]]]]
    # depth=1: 1, [2, [3, [4]]] -> 展开第一层
    # depth=2: 1, 2, [3, [4]] -> 展开第二层，停止
    passed = result == [1, 2, [3, [4]]]
    all_passed &= print_test("flatten_deep", passed, f"结果：{result}")
    
    return all_passed


def test_chunk():
    """测试 chunk"""
    print_section("测试 Chunk")
    
    all_passed = True
    
    result = list(chunk(3, [1, 2, 3, 4, 5, 6, 7]))
    passed = result == [[1, 2, 3], [4, 5, 6], [7]]
    all_passed &= print_test("chunk", passed, f"结果：{result}")
    
    return all_passed


def test_sliding_window():
    """测试 sliding_window"""
    print_section("测试 Sliding Window")
    
    all_passed = True
    
    result = list(sliding_window(3, [1, 2, 3, 4, 5]))
    passed = result == [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
    all_passed &= print_test("sliding_window", passed, f"结果：{result}")
    
    return all_passed


# =============================================================================
# 测试用例：集合操作
# =============================================================================

def test_mapcat():
    """测试 mapcat"""
    print_section("测试 Mapcat")
    
    all_passed = True
    
    result = mapcat(lambda x: [x, x * 2], [1, 2, 3])
    passed = result == [1, 2, 2, 4, 3, 6]
    all_passed &= print_test("mapcat", passed, f"结果：{result}")
    
    return all_passed


def test_filter_map():
    """测试 filter_map"""
    print_section("测试 Filter Map")
    
    all_passed = True
    
    def safe_int(x):
        try:
            return int(x)
        except ValueError:
            return None
    
    result = filter_map(safe_int, ['1', 'a', '2', 'b', '3'])
    passed = result == [1, 2, 3]
    all_passed &= print_test("filter_map", passed, f"结果：{result}")
    
    return all_passed


def test_reduce():
    """测试 reduce"""
    print_section("测试 Reduce")
    
    all_passed = True
    
    result = reduce(lambda acc, x: acc + x, [1, 2, 3, 4, 5])
    passed = result == 15
    all_passed &= print_test("reduce 求和", passed, f"结果：{result}")
    
    result = reduce(lambda acc, x: acc * 10 + x, [1, 2, 3], 0)
    passed = result == 123
    all_passed &= print_test("reduce 组合数字", passed, f"结果：{result}")
    
    return all_passed


def test_reduce_right():
    """测试 reduce_right"""
    print_section("测试 Reduce Right")
    
    all_passed = True
    
    result = reduce_right(lambda x, acc: str(x) + acc, [1, 2, 3], '')
    passed = result == '123'
    all_passed &= print_test("reduce_right", passed, f"结果：{result}")
    
    return all_passed


def test_scan():
    """测试 scan"""
    print_section("测试 Scan")
    
    all_passed = True
    
    result = scan(lambda acc, x: acc + x, [1, 2, 3, 4])
    passed = result == [1, 3, 6, 10]
    all_passed &= print_test("scan 累积", passed, f"结果：{result}")
    
    result = scan(lambda acc, x: acc + x, [1, 2, 3, 4], 0)
    passed = result == [0, 1, 3, 6, 10]
    all_passed &= print_test("scan 带初始值", passed, f"结果：{result}")
    
    return all_passed


def test_partition():
    """测试 partition"""
    print_section("测试 Partition")
    
    all_passed = True
    
    truthy, falsy = partition(lambda x: x % 2 == 0, [1, 2, 3, 4, 5, 6])
    passed = truthy == [2, 4, 6] and falsy == [1, 3, 5]
    all_passed &= print_test("partition", passed, f"偶数：{truthy}, 奇数：{falsy}")
    
    return all_passed


def test_group_by():
    """测试 group_by"""
    print_section("测试 Group By")
    
    all_passed = True
    
    result = group_by(len, ['a', 'bb', 'ccc', 'dd'])
    passed = result == {1: ['a'], 2: ['bb', 'dd'], 3: ['ccc']}
    all_passed &= print_test("group_by", passed, f"结果：{result}")
    
    return all_passed


def test_unique():
    """测试 unique"""
    print_section("测试 Unique")
    
    all_passed = True
    
    result = unique([1, 2, 2, 3, 1, 4])
    passed = result == [1, 2, 3, 4]
    all_passed &= print_test("unique 去重", passed, f"结果：{result}")
    
    result = unique(['a', 'A', 'b', 'B'], key=str.lower)
    passed = result == ['a', 'b']
    all_passed &= print_test("unique 带 key", passed, f"结果：{result}")
    
    return all_passed


# =============================================================================
# 测试用例：谓词逻辑
# =============================================================================

def test_all_pred():
    """测试 all_pred"""
    print_section("测试 All Pred")
    
    all_passed = True
    
    is_positive = lambda x: x > 0
    is_even = lambda x: x % 2 == 0
    check = all_pred(is_positive, is_even)
    
    passed = check(4) == True
    all_passed &= print_test("all_pred(4)", passed, f"4 是正偶数：{check(4)}")
    
    passed = check(3) == False
    all_passed &= print_test("all_pred(3)", passed, f"3 不是偶数：{check(3)}")
    
    return all_passed


def test_any_pred():
    """测试 any_pred"""
    print_section("测试 Any Pred")
    
    all_passed = True
    
    is_zero = lambda x: x == 0
    is_negative = lambda x: x < 0
    check = any_pred(is_zero, is_negative)
    
    passed = check(-5) == True
    all_passed &= print_test("any_pred(-5)", passed, f"-5 是负数：{check(-5)}")
    
    passed = check(5) == False
    all_passed &= print_test("any_pred(5)", passed, f"5 既不是零也不是负数：{check(5)}")
    
    return all_passed


def test_not_pred():
    """测试 not_pred"""
    print_section("测试 Not Pred")
    
    all_passed = True
    
    is_even = lambda x: x % 2 == 0
    is_odd = not_pred(is_even)
    
    passed = is_odd(3) == True
    all_passed &= print_test("not_pred(3)", passed, f"3 是奇数：{is_odd(3)}")
    
    passed = is_odd(4) == False
    all_passed &= print_test("not_pred(4)", passed, f"4 不是奇数：{is_odd(4)}")
    
    return all_passed


def test_comparison_preds():
    """测试比较谓词"""
    print_section("测试比较谓词")
    
    all_passed = True
    
    passed = eq(5)(5) == True and eq(5)(3) == False
    all_passed &= print_test("eq(5)", passed)
    
    passed = gt(5)(10) == True and gt(5)(3) == False
    all_passed &= print_test("gt(5)", passed)
    
    passed = lt(5)(3) == True and lt(5)(10) == False
    all_passed &= print_test("lt(5)", passed)
    
    passed = ge(5)(5) == True and ge(5)(6) == True and ge(5)(4) == False
    all_passed &= print_test("ge(5)", passed)
    
    passed = le(5)(5) == True and le(5)(4) == True and le(5)(6) == False
    all_passed &= print_test("le(5)", passed)
    
    return all_passed


# =============================================================================
# 测试用例：条件执行
# =============================================================================

def test_cond():
    """测试 cond"""
    print_section("测试 Cond")
    
    all_passed = True
    
    classify = cond(
        (lambda x: x > 0, lambda x: 'positive'),
        (lambda x: x < 0, lambda x: 'negative'),
        (lambda x: True, lambda x: 'zero'),
    )
    
    passed = classify(5) == 'positive'
    all_passed &= print_test("cond(5)", passed, f"结果：{classify(5)}")
    
    passed = classify(-3) == 'negative'
    all_passed &= print_test("cond(-3)", passed, f"结果：{classify(-3)}")
    
    passed = classify(0) == 'zero'
    all_passed &= print_test("cond(0)", passed, f"结果：{classify(0)}")
    
    return all_passed


def test_when():
    """测试 when"""
    print_section("测试 When")
    
    all_passed = True
    
    log_positive = when(lambda x: x > 0, lambda x: f"{x} is positive")
    
    passed = log_positive(5) == '5 is positive'
    all_passed &= print_test("when(5)", passed, f"结果：{log_positive(5)}")
    
    passed = log_positive(-3) is None
    all_passed &= print_test("when(-3)", passed, f"结果：{log_positive(-3)}")
    
    return all_passed


def test_unless():
    """测试 unless"""
    print_section("测试 Unless")
    
    all_passed = True
    
    log_non_positive = unless(lambda x: x > 0, lambda x: f"{x} is not positive")
    
    passed = log_non_positive(-3) == '-3 is not positive'
    all_passed &= print_test("unless(-3)", passed, f"结果：{log_non_positive(-3)}")
    
    passed = log_non_positive(5) is None
    all_passed &= print_test("unless(5)", passed, f"结果：{log_non_positive(5)}")
    
    return all_passed


# =============================================================================
# 测试用例：实用工具
# =============================================================================

def test_identity():
    """测试 identity"""
    print_section("测试 Identity")
    
    all_passed = True
    
    passed = identity(5) == 5
    all_passed &= print_test("identity(5)", passed)
    
    obj = {'key': 'value'}
    passed = identity(obj) is obj
    all_passed &= print_test("identity(对象)", passed)
    
    return all_passed


def test_constantly():
    """测试 constantly"""
    print_section("测试 Constantly")
    
    all_passed = True
    
    always_five = constantly(5)
    
    passed = always_five() == 5
    all_passed &= print_test("constantly()()", passed)
    
    passed = always_five(1, 2, 3, a=4) == 5
    all_passed &= print_test("constantly(带参数)", passed)
    
    return all_passed


def test_tap():
    """测试 tap"""
    print_section("测试 Tap")
    
    all_passed = True
    
    tapped_value = None
    
    def tap_func(x):
        nonlocal tapped_value
        tapped_value = x
    
    result = pipe(
        lambda x: x * 2,
        tap(tap_func),
        lambda x: x + 1,
    )(5)
    
    passed = result == 11 and tapped_value == 10
    all_passed &= print_test("tap 副作用", passed, f"结果：{result}, 捕获值：{tapped_value}")
    
    return all_passed


def test_noop():
    """测试 noop"""
    print_section("测试 Noop")
    
    all_passed = True
    
    result = noop()
    passed = result is None
    all_passed &= print_test("noop()", passed)
    
    result = noop(1, 2, 3, a=4)
    passed = result is None
    all_passed &= print_test("noop(带参数)", passed)
    
    return all_passed


def test_call_times():
    """测试 call_times"""
    print_section("测试 Call Times")
    
    all_passed = True
    
    counter = 0
    
    def increment():
        nonlocal counter
        counter += 1
        return counter
    
    result = call_times(3, increment)
    passed = result == [1, 2, 3]
    all_passed &= print_test("call_times", passed, f"结果：{result}")
    
    return all_passed


def test_apply_to():
    """测试 apply_to"""
    print_section("测试 Apply To")
    
    all_passed = True
    
    result = apply_to(5, lambda x: x * 2, lambda x: x + 1, lambda x: x ** 2)
    passed = result == [10, 6, 25]
    all_passed &= print_test("apply_to", passed, f"结果：{result}")
    
    return all_passed


# =============================================================================
# 测试用例：综合测试
# =============================================================================

def test_function_pipeline():
    """测试函数管道组合"""
    print_section("测试函数管道组合")
    
    all_passed = True
    
    # 创建一个数据处理管道
    process = pipe(
        lambda x: [i for i in range(1, x + 1)],  # 生成 1 到 x 的数字
        lambda nums: filter(lambda n: n % 2 == 0, nums),  # 过滤偶数
        lambda nums: map(lambda n: n * 2, nums),  # 每个数乘以 2
        list,
        lambda nums: sum(nums),  # 求和
    )
    
    result = process(10)
    # 偶数：2, 4, 6, 8, 10
    # 乘以 2：4, 8, 12, 16, 20
    # 求和：60
    passed = result == 60
    all_passed &= print_test("数据处理管道", passed, f"结果：{result}")
    
    return all_passed


def test_curried_composition():
    """测试柯里化与组合"""
    print_section("测试柯里化与组合")
    
    all_passed = True
    
    @curry
    def add(a, b):
        return a + b
    
    @curry
    def multiply(a, b):
        return a * b
    
    add_5 = add(5)
    multiply_by_2 = multiply(2)
    
    # 组合：先加 5，再乘以 2
    process = pipe(add_5, multiply_by_2)
    result = process(3)
    # (3 + 5) * 2 = 16
    passed = result == 16
    all_passed &= print_test("柯里化 + 管道", passed, f"结果：{result}")
    
    return all_passed


def test_memoized_composition():
    """测试记忆化与组合"""
    print_section("测试记忆化与组合")
    
    all_passed = True
    
    call_count = 0
    
    @memoize
    def expensive_square(x):
        nonlocal call_count
        call_count += 1
        time.sleep(0.001)  # 模拟耗时
        return x * x
    
    # 组合中使用记忆化函数
    process = pipe(
        lambda x: expensive_square(x),
        lambda x: expensive_square(x),  # 同样的输入会命中缓存
    )
    
    result = process(5)
    first_count = call_count
    
    # 再次调用
    call_count = 0
    result2 = process(5)
    
    passed = result == 625 and result2 == 625 and first_count == 2 and call_count == 0
    all_passed &= print_test("记忆化组合", passed, 
                            f"结果：{result}, 首次调用次数：{first_count}, 二次调用次数：{call_count}")
    
    return all_passed


# =============================================================================
# 主测试运行器
# =============================================================================

def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("  AllToolkit - Functional Programming Utilities 测试套件")
    print("  函数式编程工具完整功能测试")
    print("="*60)
    
    tests = [
        ("柯里化", test_curry),
        ("固定元数柯里化", test_curry_n),
        ("函数组合", test_compose),
        ("从左到右组合", test_compose_left),
        ("管道", test_pipe),
        ("偏函数", test_partial),
        ("右侧偏函数", test_partial_right),
        ("参数翻转", test_flip),
        ("记忆化", test_memoize),
        ("带 TTL 记忆化", test_memoize_with_ttl),
        ("惰性求值", test_lazy),
        ("Take", test_take),
        ("Take While", test_take_while),
        ("Drop", test_drop),
        ("Drop While", test_drop_while),
        ("Iterate", test_iterate),
        ("Flatten", test_flatten),
        ("Chunk", test_chunk),
        ("Sliding Window", test_sliding_window),
        ("Mapcat", test_mapcat),
        ("Filter Map", test_filter_map),
        ("Reduce", test_reduce),
        ("Reduce Right", test_reduce_right),
        ("Scan", test_scan),
        ("Partition", test_partition),
        ("Group By", test_group_by),
        ("Unique", test_unique),
        ("All Pred", test_all_pred),
        ("Any Pred", test_any_pred),
        ("Not Pred", test_not_pred),
        ("比较谓词", test_comparison_preds),
        ("Cond", test_cond),
        ("When", test_when),
        ("Unless", test_unless),
        ("Identity", test_identity),
        ("Constantly", test_constantly),
        ("Tap", test_tap),
        ("Noop", test_noop),
        ("Call Times", test_call_times),
        ("Apply To", test_apply_to),
        ("函数管道组合", test_function_pipeline),
        ("柯里化与组合", test_curried_composition),
        ("记忆化与组合", test_memoized_composition),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n  ✗ EXCEPTION in {name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # 汇总结果
    print_section("测试结果汇总")
    
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    
    for name, passed in results:
        status = "✓" if passed else "✗"
        print(f"  {status} {name}")
    
    print(f"\n  总计：{passed_count}/{total_count} 通过")
    
    if passed_count == total_count:
        print("\n  🎉 所有测试通过！")
    else:
        print(f"\n  ⚠️  {total_count - passed_count} 个测试失败")
    
    return passed_count == total_count


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
