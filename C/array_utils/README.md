# array_utils - C 语言数组工具库

一个功能完整、零外部依赖的 C 语言数组操作工具库，提供排序、搜索、统计等常用数组操作。

## 功能特性

### 排序算法
- `array_bubble_sort()` - 冒泡排序
- `array_selection_sort()` - 选择排序
- `array_insertion_sort()` - 插入排序
- `array_quick_sort()` - 快速排序（非递归实现，避免栈溢出）
- `array_merge_sort()` - 归并排序

### 搜索算法
- `array_linear_search()` - 线性搜索
- `array_binary_search()` - 二分搜索（数组需已排序）

### 数组操作
- `array_reverse()` - 反转数组
- `array_slice()` - 数组切片复制
- `array_merge()` - 合并两个数组
- `array_unique_sorted()` - 原地去重（已排序数组）
- `array_fill()` - 数组填充
- `array_copy()` - 数组复制

### 统计函数（整型数组）
- `array_int_min()` - 最小值
- `array_int_max()` - 最大值
- `array_int_sum()` - 总和
- `array_int_avg()` - 平均值

### 统计函数（浮点型数组）
- `array_double_min()` - 最小值
- `array_double_max()` - 最大值
- `array_double_sum()` - 总和
- `array_double_avg()` - 平均值

### 数组判断
- `array_is_sorted()` - 检查是否已排序
- `array_contains()` - 检查是否包含元素
- `array_count_element()` - 统计元素出现次数

### 预定义比较函数
- `compare_int()` / `compare_int_desc()` - 整型比较
- `compare_double()` / `compare_double_desc()` - 浮点型比较
- `compare_char()` / `compare_char_desc()` - 字符比较
- `compare_string()` - 字符串比较

## 编译

### 编译测试程序

```bash
gcc -Wall -Wextra -o test array_utils.c array_utils_test.c
./test
```

### 编译示例程序

```bash
gcc -Wall -Wextra -o example array_utils.c example.c
./example
```

## 使用示例

### 基本排序

```c
#include "array_utils.h"

int main() {
    int arr[] = {64, 34, 25, 12, 22, 11, 90};
    size_t count = sizeof(arr) / sizeof(arr[0]);
    
    // 快速排序（升序）
    array_quick_sort(arr, count, sizeof(int), compare_int);
    
    // 快速排序（降序）
    array_quick_sort(arr, count, sizeof(int), compare_int_desc);
    
    return 0;
}
```

### 搜索元素

```c
#include "array_utils.h"

int main() {
    int arr[] = {11, 12, 22, 25, 34, 64, 90};
    size_t count = sizeof(arr) / sizeof(arr[0]);
    
    // 线性搜索
    int target = 22;
    size_t idx = array_linear_search(arr, count, sizeof(int), &target, compare_int);
    
    // 二分搜索（数组必须已排序）
    target = 64;
    idx = array_binary_search(arr, count, sizeof(int), &target, compare_int);
    
    return 0;
}
```

### 数组操作

```c
#include "array_utils.h"

int main() {
    // 反转数组
    int arr[] = {1, 2, 3, 4, 5};
    array_reverse(arr, 5, sizeof(int));
    // arr 现在是 {5, 4, 3, 2, 1}
    
    // 数组切片
    int source[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    int* slice = (int*)array_slice(source, 10, sizeof(int), 2, 4, NULL);
    // slice 是 {3, 4, 5, 6}
    free(slice);
    
    // 合并数组
    int a[] = {1, 2, 3};
    int b[] = {4, 5, 6};
    int* merged = (int*)array_merge(a, 3, b, 3, sizeof(int), NULL);
    // merged 是 {1, 2, 3, 4, 5, 6}
    free(merged);
    
    return 0;
}
```

### 统计计算

```c
#include "array_utils.h"

int main() {
    int arr[] = {3, 1, 4, 1, 5, 9, 2, 6, 5, 3};
    size_t count = sizeof(arr) / sizeof(arr[0]);
    
    int min = array_int_min(arr, count);        // 1
    int max = array_int_max(arr, count);        // 9
    long long sum = array_int_sum(arr, count);  // 39
    double avg = array_int_avg(arr, count);     // 3.9
    
    return 0;
}
```

### 自定义比较函数

```c
#include "array_utils.h"

typedef struct {
    int age;
    const char* name;
} Person;

// 按年龄比较
int compare_person(const void* a, const void* b) {
    const Person* pa = (const Person*)a;
    const Person* pb = (const Person*)b;
    return (pa->age > pb->age) - (pa->age < pb->age);
}

int main() {
    Person people[] = {
        {25, "Alice"},
        {30, "Bob"},
        {20, "Charlie"}
    };
    size_t count = sizeof(people) / sizeof(people[0]);
    
    array_quick_sort(people, count, sizeof(Person), compare_person);
    
    return 0;
}
```

## API 参考

### 比较函数类型

```c
typedef int (*CompareFunc)(const void* a, const void* b);
```

比较函数应返回：
- `< 0` 如果 `a < b`
- `= 0` 如果 `a == b`
- `> 0` 如果 `a > b`

### 时间复杂度

| 算法 | 平均时间 | 最坏时间 | 空间 | 稳定性 |
|------|----------|----------|------|--------|
| 冒泡排序 | O(n²) | O(n²) | O(1) | 稳定 |
| 选择排序 | O(n²) | O(n²) | O(1) | 不稳定 |
| 插入排序 | O(n²) | O(n²) | O(1) | 稳定 |
| 快速排序 | O(n log n) | O(n²) | O(log n) | 不稳定 |
| 归并排序 | O(n log n) | O(n log n) | O(n) | 稳定 |
| 线性搜索 | O(n) | O(n) | O(1) | - |
| 二分搜索 | O(log n) | O(log n) | O(1) | - |

## 注意事项

1. **内存管理**：`array_slice()` 和 `array_merge()` 函数会自动分配内存，调用者负责释放。
2. **线程安全**：所有函数都是线程安全的，可以并发调用。
3. **空指针检查**：所有函数都会检查空指针输入，避免崩溃。
4. **快速排序**：使用非递归实现，避免大数组导致的栈溢出。

## 许可证

MIT License

## 作者

AllToolkit

## 版本历史

- v1.0.0 (2026-04-25) - 初始版本