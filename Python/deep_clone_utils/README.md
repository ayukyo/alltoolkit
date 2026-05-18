# Deep Clone Utils


AllToolkit - Python Deep Clone Utilities

A zero-dependency, production-ready deep cloning utility module.
Supports deep copying of complex nested data structures including
custom objects, circular references, and special Python types.

Author: AllToolkit
License: MIT


## 功能

### 类

- **CloneConfig**: Configuration options for deep cloning
  属性: preserve_singletons, copy_functions, copy_classes, copy_modules, max_depth, custom_handlers, memo

- **DeepClone**: Object-oriented interface for deep cloning
  方法: clone, __call__

- **CloneError**: Exception raised when cloning fails

### 函数

- **deep_clone(obj, config, depth)** - Deep clone an object recursively.
- **clone(obj, **kwargs)** - Shorthand for deep_clone with optional configuration.
- **shallow_clone(obj)** - Create a shallow copy of an object.
- **clone_with_depth(obj, max_depth)** - Deep clone with a maximum depth limit.
- **clone_without_functions(obj)** - Deep clone preserving function references.
- **clone_with_custom_handlers(obj, handlers)** - Deep clone with custom handlers for specific types.
- **is_deep_equal(a, b)** - Deep equality comparison for complex objects.
- **clone_structure(template, fill_value)** - Clone the structure of a nested object without values.

## 支持的类型

### 不可变类型 (直接返回)
- None, bool, int, float, complex, str, bytes
- type, range, slice, frozenset
- Ellipsis, NotImplemented

### 可变类型 (深度克隆)
- list, dict, set
- tuple (包含可变元素时)
- deque, OrderedDict, defaultdict, Counter
- namedtuple

### 特殊类型
- datetime, date, time, timedelta
- Decimal, Fraction
- re.Pattern (编译后的正则表达式)
- bytearray, memoryview

### 自定义对象
- 带 `__dict__` 的类实例
- 带 `__slots__` 的类实例
- 循环引用对象

## 使用示例

```python
from mod import deep_clone, clone, is_deep_equal

# 基础克隆
data = {'a': [1, 2, 3], 'b': {'c': 4}}
cloned = deep_clone(data)
cloned['a'].append(4)
print(data['a'])  # [1, 2, 3] - 原数据不变

# 快捷克隆
cloned = clone({'nested': {'value': 1}})

# 深度相等比较
assert is_deep_equal({'a': [1, 2]}, {'a': [1, 2]})

# 自定义深度限制
from mod import clone_with_depth
cloned = clone_with_depth(data, max_depth=10)

# 自定义类型处理器
class MyClass:
    def __init__(self, value):
        self.value = value

def my_handler(obj, config, depth):
    return MyClass(obj.value * 2)

from mod import clone_with_custom_handlers
cloned = clone_with_custom_handlers(MyClass(5), {MyClass: my_handler})
print(cloned.value)  # 10

# 克隆结构（不含值）
from mod import clone_structure
template = {'a': [1, 2], 'b': {'c': 3}}
empty = clone_structure(template, fill_value=0)
print(empty)  # {'a': [0, 0], 'b': {'c': 0}}

# 对象式接口
from mod import DeepClone
cloner = DeepClone(max_depth=100)
cloned = cloner({'data': [1, 2, 3]})
```

## 循环引用支持

```python
# 循环引用列表
lst = [1, 2, 3]
lst.append(lst)
cloned = deep_clone(lst)
assert cloned[3] is cloned  # 循环引用保留

# 循环引用字典
d = {'value': 1}
d['self'] = d
cloned = deep_clone(d)
assert cloned['self'] is cloned
```

## 自定义对象克隆

```python
class Person:
    def __init__(self, name, friends=None):
        self.name = name
        self.friends = friends or []
    
    def add_friend(self, friend):
        self.friends.append(friend)

alice = Person("Alice")
bob = Person("Bob")
alice.add_friend(bob)
bob.add_friend(alice)  # 循环引用

# 完整克隆，保留循环引用
cloned_alice = deep_clone(alice)
assert cloned_alice.name == "Alice"
assert cloned_alice.friends[0].name == "Bob"
assert cloned_alice.friends[0].friends[0] is cloned_alice
```

## 测试

运行测试：

```bash
python deep_clone_utils_test.py
```

或使用 pytest：

```bash
python -m pytest deep_clone_utils_test.py -v
```

## 文件结构

```
deep_clone_utils/
├── mod.py                    # 主模块
├── deep_clone_utils_test.py  # 测试文件
└── README.md                 # 本文档
```

---

**Last updated**: 2026-05-18