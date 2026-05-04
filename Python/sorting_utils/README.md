# sorting_utils - 排序算法工具模块

多语言支持的经典排序算法集合，零外部依赖。

## 功能特性

### 支持的排序算法

| 算法 | 时间复杂度 (平均) | 空间复杂度 | 稳定性 | 适用场景 |
|------|-------------------|------------|--------|----------|
| **quick_sort** | O(n log n) | O(log n) | ❌ | 通用排序，大数据集 |
| **merge_sort** | O(n log n) | O(n) | ✅ | 需要稳定排序 |
| **heap_sort** | O(n log n) | O(1) | ❌ | 内存受限场景 |
| **insertion_sort** | O(n²) | O(1) | ✅ | 小数据集，部分有序 |
| **selection_sort** | O(n²) | O(1) | ❌ | 小数据集，简单实现 |
| **bubble_sort** | O(n²) | O(1) | ✅ | 教学演示，已基本有序 |
| **shell_sort** | O(n^1.5) | O(1) | ❌ | 中等规模数据 |
| **counting_sort** | O(n + k) | O(k) | ✅ | 整数，值域有限 |
| **bucket_sort** | O(n + k) | O(n + k) | ✅ | 浮点数，均匀分布 |
| **radix_sort** | O(d × n) | O(n + k) | ✅ | 整数，多位数字 |
| **cocktail_sort** | O(n²) | O(1) | ✅ | 双向冒泡，教学 |
| **gnome_sort** | O(n²) | O(1) | ✅ | 简单实现，教学 |

### 核心特性

- ✅ **零外部依赖** - 仅使用 Python 标准库
- ✅ **通用类型支持** - 支持整数、浮点数、字符串、对象
- ✅ **自定义 key 函数** - 类似 `sorted()` 的 key 参数
- ✅ **升序/降序切换** - 通过 `reverse` 参数控制
- ✅ **原地排序选项** - 部分算法支持 `in_place` 参数
- ✅ **稳定排序保证** - 归并/插入/冒泡等保证稳定性
- ✅ **算法推荐系统** - 根据数据特性自动推荐最优算法

## 快速开始

### 基础用法

```python
from sorting_utils import quick_sort, merge_sort, counting_sort

# 基础排序
arr = [5, 2, 8, 1, 9, 3]
result = quick_sort(arr)
print(result)  # [1, 2, 3, 5, 8, 9]

# 降序排序
result = quick_sort(arr, reverse=True)
print(result)  # [9, 8, 5, 3, 2, 1]

# 使用 key 函数（按字符串长度排序）
words = ['apple', 'banana', 'cherry', 'date']
result = quick_sort(words, key=lambda x: len(x))
print(result)  # ['date', 'apple', 'banana', 'cherry']
```

### 高级用法

```python
from sorting_utils import (
    radix_sort,       # 整数专用，高效
    bucket_sort,      # 浮点数专用
    sort_by_custom,   # 自定义比较函数
    recommend_sort_algorithm,  # 算法推荐
    is_sorted,        # 检查是否已排序
)

# 大整数排序
large_numbers = [1234567890, 987654321, 1111111111]
result = radix_sort(large_numbers)

# 浮点数排序
floats = [0.5, 0.2, 0.8, 0.1, 0.9]
result = bucket_sort(floats)

# 自定义比较函数（奇数在前，偶数在后）
def custom_cmp(a, b):
    if a % 2 != b % 2:
        return -1 if a % 2 == 1 else 1
    return a - b

arr = [1, 2, 3, 4, 5, 6]
result = sort_by_custom(arr, custom_cmp)
print(result)  # [1, 3, 5, 2, 4, 6]

# 检查是否已排序
print(is_sorted([1, 2, 3, 4]))  # True
print(is_sorted([4, 3, 2, 1], reverse=True))  # True

# 自动推荐最优算法
algo = recommend_sort_algorithm(
    n=10000,
    is_integers=True,
    value_range=500,
    require_stable=True
)
print(algo)  # 'merge_sort'
```

### 原地排序

```python
from sorting_utils import quick_sort, insertion_sort

arr = [5, 2, 8, 1, 9, 3]

# 原地排序（修改原数组）
quick_sort(arr, in_place=True)
print(arr)  # [1, 2, 3, 5, 8, 9]

# 非原地排序（返回新数组）
arr2 = [5, 2, 8, 1, 9, 3]
result = insertion_sort(arr2)  # arr2 保持不变
```

## API 参考

### quick_sort(arr, key=None, reverse=False, in_place=False)

快速排序，平均 O(n log n)，最坏 O(n²)。

- **arr**: 待排序列表
- **key**: 提取比较键的函数
- **reverse**: 是否降序
- **in_place**: 是否原地排序

### merge_sort(arr, key=None, reverse=False, stable=True)

归并排序，稳定，O(n log n)。

- **stable**: 是否保持稳定性（相等元素保持原顺序）

### heap_sort(arr, key=None, reverse=False)

堆排序，O(n log n)，非稳定，内存效率高。

### insertion_sort(arr, key=None, reverse=False, in_place=False)

插入排序，O(n²)，稳定，小数据集高效。

### selection_sort(arr, key=None, reverse=False)

选择排序，O(n²)，非稳定。

### bubble_sort(arr, key=None, reverse=False, optimized=True)

冒泡排序，O(n²)，稳定。

- **optimized**: 使用优化版本（提前终止）

### shell_sort(arr, key=None, reverse=False, gaps=None)

希尔排序，O(n^1.5) ~ O(n²)。

- **gaps**: 自定义间隔序列（默认 Knuth 序列）

### counting_sort(arr, reverse=False, min_val=None, max_val=None)

计数排序，O(n + k)，仅适用于整数。

- **min_val/max_val**: 可选值域范围（自动检测）

### bucket_sort(arr, num_buckets=10, reverse=False, min_val=None, max_val=None)

桶排序，O(n + k)，适用于浮点数。

### radix_sort(arr, reverse=False, base=10)

基数排序，O(d × n)，适用于整数，自动处理负数。

- **base**: 进制基数（默认 10）

### tim_sort_like(arr, key=None, reverse=False)

类 TimSort 实现，结合插入和归并排序。

### cocktail_sort(arr, key=None, reverse=False)

鸡尾酒排序（双向冒泡），O(n²)。

### gnome_sort(arr, key=None, reverse=False)

侏儒排序，O(n²)，简单有趣。

### sort_by_custom(arr, comparator)

使用自定义比较函数排序。

- **comparator**: 返回负数/零/正数的比较函数

### is_sorted(arr, key=None, reverse=False)

检查列表是否已排序。

### get_sort_algorithm_complexity()

返回各算法复杂度信息字典。

### recommend_sort_algorithm(n, is_integers=False, value_range=None, require_stable=False)

根据数据特性推荐最优算法。

## 测试覆盖

模块包含 **100+ 测试用例**，覆盖：

- ✅ 基础排序功能
- ✅ 升序/降序切换
- ✅ key 函数支持
- ✅ 原地排序
- ✅ 空数组、单元素
- ✅ 已排序数组
- ✅ 全部相同元素
- ✅ 正负混合
- ✅ 大数组（1000+ 元素）
- ✅ 重复元素
- ✅ 稳定性验证
- ✅ 跨算法一致性
- ✅ 边界值（超大数、精度）
- ✅ 性能基准
- ✅ 异常处理

## 使用建议

### 选择合适算法

```python
# 小数据集 (< 50)
insertion_sort(arr)  # 最高效

# 大数据集，不要求稳定
quick_sort(arr)  # 通常最快

# 大数据集，要求稳定
merge_sort(arr)  # 保证稳定性

# 整数，值域有限
counting_sort(arr)  # O(n + k) 线性时间

# 整数，大值域
radix_sort(arr)  # O(d × n)

# 浮点数
bucket_sort(arr)  # 分布均匀时高效

# 让系统推荐
recommend_sort_algorithm(
    n=len(arr),
    is_integers=all(isinstance(x, int) for x in arr),
    value_range=max(arr) - min(arr) if arr else None
)
```

## 版本历史

- **v1.0.0** (2026-05-05): 首次发布，包含 12 种排序算法

## 许可证

MIT License

## 作者

AllToolkit 自动生成系统