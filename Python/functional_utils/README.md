# AllToolkit - Functional Programming Utilities 🧩

**零依赖 Python 函数式编程工具库**

---

## 📖 概述

`functional_utils` 是一个功能完整的函数式编程工具模块，提供柯里化、函数组合、管道、偏函数、记忆化、惰性求值、迭代器工具等功能。完全使用 Python 标准库实现（functools, inspect, typing），无需任何外部依赖。

### 核心功能

- 🔀 **柯里化**: 将函数转换为柯里化形式，支持部分应用
- 🔗 **函数组合**: compose、pipe，从右到左或从左到右组合函数
- 📦 **偏函数**: partial、flip，固定部分参数或翻转参数顺序
- 💾 **记忆化**: memoize、memoize_with_ttl，缓存函数结果避免重复计算
- ⏱️ **惰性求值**: Lazy，延迟计算直到首次访问
- 🔄 **迭代器工具**: take、drop、chunk、sliding_window、flatten
- 📊 **集合操作**: mapcat、filter_map、reduce、scan、group_by、unique
- 🔍 **谓词逻辑**: all_pred、any_pred、not_pred、eq/gt/lt/ge/le
- 🎯 **条件执行**: cond、when、unless
- 🛠️ **实用工具**: identity、constantly、tap、noop

---

## 🚀 快速开始

### 安装

无需安装！直接复制 `mod.py` 到你的项目：

```bash
cp AllToolkit/Python/functional_utils/mod.py your_project/
```

### 基础使用

```python
from mod import *

# 柯里化
@curry
def add(a, b, c):
    return a + b + c

add_one_and_two = add(1, 2)
result = add_one_and_two(3)  # 6

# 函数组合/管道
def double(x): return x * 2
def add_one(x): return x + 1
def square(x): return x ** 2

result = pipe(double, add_one, square)(3)
# ((3 * 2) + 1) ** 2 = 49

# 记忆化
@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

fibonacci(10)  # 55（快速，有缓存）
```

---

## 📚 API 参考

### 柯里化 (Currying)

| 函数 | 描述 | 示例 |
|------|------|------|
| `curry(func)` | 将函数转换为柯里化形式 | `curry(add)(1)(2)(3)` |
| `curry_n(func, n)` | 固定元数的柯里化 | `curry_n(multiply, 3)(2)(3)(4)` |

### 函数组合 (Composition)

| 函数 | 描述 | 示例 |
|------|------|------|
| `compose(*funcs)` | 从右到左组合 | `compose(f, g, h)(x) = f(g(h(x)))` |
| `compose_left(*funcs)` | 从左到右组合 | `compose_left(f, g)(x) = g(f(x))` |
| `pipe(*funcs)` | 管道（同 compose_left） | `pipe(f, g, h)(x)` |

### 偏函数 (Partial Application)

| 函数 | 描述 | 示例 |
|------|------|------|
| `partial(func, *args)` | 绑定位置参数 | `partial(multiply, 2)(3, 4)` |
| `partial_right(func, *args)` | 从右侧绑定 | `partial_right(divide, 2)(10)` |
| `flip(func)` | 翻转前两个参数 | `flip(greet)("Alice", "Hello")` |

### 记忆化 (Memoization)

| 函数 | 描述 | 示例 |
|------|------|------|
| `memoize(func)` | 添加记忆化缓存 | `@memoize` |
| `memoize_with_ttl(ttl)` | 带过期时间的缓存 | `@memoize_with_ttl(60)` |

### 惰性求值 (Lazy Evaluation)

| 函数/类 | 描述 | 示例 |
|--------|------|------|
| `Lazy(factory)` | 惰性求值包装器 | `Lazy(lambda: expensive())` |
| `lazy(factory)` | 创建 Lazy 对象 | `lazy(expensive_computation)` |

### 迭代器工具 (Iterator Utilities)

| 函数 | 描述 | 示例 |
|------|------|------|
| `take(n, iterable)` | 取前 n 个元素 | `take(3, [1,2,3,4,5])` → `[1,2,3]` |
| `take_while(pred, iter)` | 取直到条件不满足 | `take_while(lambda x: x<5, ...)` |
| `drop(n, iterable)` | 丢弃前 n 个元素 | `drop(2, [1,2,3,4,5])` → `[3,4,5]` |
| `drop_while(pred, iter)` | 丢弃直到条件不满足 | `drop_while(lambda x: x<3, ...)` |
| `iterate(func, init, n)` | 生成迭代序列 | `iterate(lambda x: x*2, 1, 5)` |
| `flatten(nested)` | 展平一层嵌套 | `flatten([[1,2],[3,4]])` |
| `flatten_deep(nested, depth)` | 深度展平 | `flatten_deep([1,[2,[3]]], 2)` |
| `chunk(n, iterable)` | 分块 | `chunk(3, [1,2,3,4,5])` |
| `sliding_window(n, iter)` | 滑动窗口 | `sliding_window(3, [1,2,3,4,5])` |

### 集合操作 (Collection Operations)

| 函数 | 描述 | 示例 |
|------|------|------|
| `mapcat(func, iterable)` | map + flatten | `mapcat(lambda x: [x,x*2], [1,2,3])` |
| `filter_map(func, iterable)` | filter + map | `filter_map(safe_int, ['1','a','2'])` |
| `reduce(func, iterable, init)` | 归约/折叠 | `reduce(lambda a,x: a+x, [1,2,3])` |
| `reduce_right(func, iterable)` | 从右到左归约 | `reduce_right(...)` |
| `scan(func, iterable, init)` | 扫描/累积 | `scan(lambda a,x: a+x, [1,2,3,4])` |
| `partition(pred, iterable)` | 根据条件分组 | `partition(is_even, [1,2,3,4,5,6])` |
| `group_by(key_func, iterable)` | 按键分组 | `group_by(len, ['a','bb','ccc'])` |
| `unique(iterable, key)` | 去重 | `unique([1,2,2,3,1])` |

### 谓词逻辑 (Predicate Logic)

| 函数 | 描述 | 示例 |
|------|------|------|
| `all_pred(*preds)` | 所有谓词都为真 | `all_pred(is_positive, is_even)` |
| `any_pred(*preds)` | 任一谓词为真 | `any_pred(is_zero, is_negative)` |
| `not_pred(pred)` | 谓词取反 | `not_pred(is_even)` |
| `eq(value)` | 等于比较 | `eq(5)(5)` → `True` |
| `gt(value)` | 大于比较 | `gt(5)(10)` → `True` |
| `lt(value)` | 小于比较 | `lt(5)(3)` → `True` |
| `ge(value)` | 大于等于 | `ge(5)(5)` → `True` |
| `le(value)` | 小于等于 | `le(5)(4)` → `True` |

### 条件执行 (Conditional Execution)

| 函数 | 描述 | 示例 |
|------|------|------|
| `cond(*clauses)` | 条件表达式 | `cond((is_pos, to_pos), (is_neg, to_neg))` |
| `when(pred, func)` | 条件满足时执行 | `when(lambda x: x>0, log)` |
| `unless(pred, func)` | 条件不满足时执行 | `unless(lambda x: x>0, log)` |

### 实用工具 (Utilities)

| 函数 | 描述 | 示例 |
|------|------|------|
| `identity(x)` | 恒等函数 | `identity(5)` → `5` |
| `constantly(value)` | 常量函数 | `constantly(5)()` → `5` |
| `tap(func)` | 调试辅助 | `pipe(f, tap(print), g)` |
| `noop()` | 空操作 | `noop()` |
| `call_times(n, func)` | 调用 n 次 | `call_times(3, increment)` |
| `apply_to(value, *funcs)` | 应用到多个函数 | `apply_to(5, f, g, h)` |

---

## 💡 实用示例

### 1. 柯里化与部分应用

```python
from mod import curry, partial

# 柯里化
@curry
def multiply(a, b, c):
    return a * b * c

# 部分应用
double = multiply(2)
double_and_triple = double(3)
result = double_and_triple(4)  # 2 * 3 * 4 = 24

# 或者链式调用
result = multiply(2)(3)(4)  # 24
```

### 2. 函数管道

```python
from mod import pipe

# 数据处理管道
process_data = pipe(
    lambda x: [i for i in range(1, x + 1)],  # 生成序列
    lambda nums: filter(lambda n: n % 2 == 0, nums),  # 过滤偶数
    lambda nums: map(lambda n: n * 2, nums),  # 转换
    list,
    sum,  # 聚合
)

result = process_data(10)  # 60
# 偶数：2,4,6,8,10 → 乘以 2：4,8,12,16,20 → 求和：60
```

### 3. 记忆化优化递归

```python
from mod import memoize

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 第一次计算
print(fibonacci(20))  # 6765（需要计算）

# 第二次调用（缓存命中）
print(fibonacci(20))  # 6765（瞬间返回）

# 查看缓存信息
print(f"缓存大小：{fibonacci.cache_info()}")

# 清除缓存
fibonacci.cache_clear()
```

### 4. 惰性求值

```python
from mod import lazy

# 延迟昂贵计算
expensive_data = lazy(lambda: {
    'data': load_large_file(),
    'processed': process_data()
})

# 创建时不会执行
# 只有在访问 .value 时才计算
if need_data:
    result = expensive_data.value
```

### 5. 迭代器工具

```python
from mod import take, chunk, sliding_window, flatten

# 取前 N 个
first_three = take(3, [1, 2, 3, 4, 5])  # [1, 2, 3]

# 分块
chunks = list(chunk(2, [1, 2, 3, 4, 5]))  # [[1,2], [3,4], [5]]

# 滑动窗口
windows = list(sliding_window(3, [1, 2, 3, 4, 5]))
# [[1,2,3], [2,3,4], [3,4,5]]

# 展平
flat = list(flatten([[1, 2], [3, 4], [5]]))  # [1, 2, 3, 4, 5]
```

### 6. 集合操作

```python
from mod import group_by, partition, unique, scan

# 分组
words = ['a', 'bb', 'ccc', 'dd', 'eee']
grouped = group_by(len, words)
# {1: ['a'], 2: ['bb', 'dd'], 3: ['ccc', 'eee']}

# 分区
evens, odds = partition(lambda x: x % 2 == 0, [1, 2, 3, 4, 5, 6])
# evens = [2, 4, 6], odds = [1, 3, 5]

# 去重（保持顺序）
unique_items = unique([1, 2, 2, 3, 1, 4])  # [1, 2, 3, 4]

# 扫描/累积
running_sum = scan(lambda acc, x: acc + x, [1, 2, 3, 4])
# [1, 3, 6, 10]
```

### 7. 谓词组合

```python
from mod import all_pred, any_pred, not_pred, eq, gt, lt

# 组合谓词
is_positive_even = all_pred(
    lambda x: x > 0,
    lambda x: x % 2 == 0
)
is_positive_even(4)  # True
is_positive_even(3)  # False

# 使用内置谓词
from mod import eq, gt, lt

is_five = eq(5)
is_greater_than_10 = gt(10)
is_less_than_5 = lt(5)

# 取反
is_odd = not_pred(lambda x: x % 2 == 0)
```

### 8. 条件执行

```python
from mod import cond, when, unless

# cond 表达式
classify = cond(
    (lambda x: x > 0, lambda x: 'positive'),
    (lambda x: x < 0, lambda x: 'negative'),
    (lambda x: True, lambda x: 'zero'),
)

classify(5)   # 'positive'
classify(-3)  # 'negative'
classify(0)   # 'zero'

# when/unless
log_positive = when(
    lambda x: x > 0,
    lambda x: print(f"Positive: {x}")
)

log_positive(5)   # 打印 "Positive: 5"
log_positive(-3)  # 什么都不做
```

### 9. 调试管道

```python
from mod import pipe, tap

# 使用 tap 在管道中调试
result = pipe(
    lambda x: x * 2,
    tap(lambda x: print(f"After double: {x}")),
    lambda x: x + 1,
    tap(lambda x: print(f"After add: {x}")),
    lambda x: x ** 2,
)(5)

# 输出:
# After double: 10
# After add: 11
# result = 121
```

### 10. 综合示例：数据处理管道

```python
from mod import pipe, filter_map, group_by, take, curry

@curry
def process_user_data(users):
    return pipe(
        # 过滤有效邮箱
        filter_map(parse_email, users),
        # 按域名分组
        lambda emails: group_by(get_domain, emails),
        # 取前 5 个域名
        lambda grouped: take(5, grouped.items()),
        # 转换为字典
        dict,
    )(users)
```

---

## 🔧 高级用法

### 柯里化与组合结合

```python
from mod import curry, pipe

@curry
def add(a, b):
    return a + b

@curry
def multiply(a, b):
    return a * b

add_5 = add(5)
multiply_by_2 = multiply(2)

# 组合柯里化函数
process = pipe(add_5, multiply_by_2)
result = process(3)  # (3 + 5) * 2 = 16
```

### 带 TTL 的缓存

```python
from mod import memoize_with_ttl
import time

@memoize_with_ttl(ttl_seconds=60)  # 60 秒过期
def get_api_data(endpoint):
    return fetch_from_api(endpoint)

# 第一次调用 - 实际请求
data1 = get_api_data('/users')

# 60 秒内 - 使用缓存
data2 = get_api_data('/users')  # 缓存命中

# 60 秒后 - 重新请求
time.sleep(61)
data3 = get_api_data('/users')  # 新请求
```

### 深度展平

```python
from mod import flatten_deep

nested = [1, [2, [3, [4, [5]]]]]

# 完全展平
flat = list(flatten_deep(nested))  # [1, 2, 3, 4, 5]

# 限制深度
partial = list(flatten_deep(nested, max_depth=2))  # [1, 2, 3, [4, [5]]]
```

---

## 🧪 运行测试

```bash
cd AllToolkit/Python/functional_utils
python functional_utils_test.py
```

---

## 📝 注意事项

1. **零依赖**: 仅使用 Python 标准库（functools, inspect, typing），无需安装额外包
2. **Python 3.7+**: 需要 Python 3.7 或更高版本（使用 typing 模块）
3. **记忆化限制**: memoize 要求函数参数是可哈希的
4. **惰性求值**: Lazy 对象线程不安全，多线程环境需额外同步
5. **性能**: 柯里化和组合会引入少量开销，性能敏感场景需权衡

---

## 📄 License

MIT License - 自由使用、修改和分发
