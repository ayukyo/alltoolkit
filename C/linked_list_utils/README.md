# C Linked List Utils

C 语言双向链表工具库 - 零依赖，仅使用标准库。

## 功能特性

### 数据类型支持
- **整数链表** - `LIST_TYPE_INT` 存储 int 值
- **浮点链表** - `LIST_TYPE_DOUBLE` 存储 double 值
- **字符串链表** - `LIST_TYPE_STRING` 存储 char* (自动深拷贝)
- **指针链表** - `LIST_TYPE_POINTER` 存储 void* (不管理内存)
- **通用链表** - `LIST_TYPE_GENERIC` 存储任意类型 (用户自定义大小)

### 核心操作
- **头部操作** - push_front, pop_front, front
- **尾部操作** - push_back, pop_back, back
- **索引操作** - insert_at, remove_at, get_node, get_int/double/string/pointer
- **查找操作** - find_int/double/string/pointer, contains_int/string

### 高级功能
- **链表操作** - reverse, concat, clone, sort, unique
- **迭代器** - 正向/反向遍历
- **数组转换** - from_array, to_array
- **函数式** - foreach, filter, fold
- **打印调试** - print, print_int, print_string

## 快速开始

```c
#include "linked_list_utils.h"
#include <stdio.h>

int main() {
    // 创建整数链表
    LinkedList* list = list_create_int();
    
    // 添加元素
    list_push_back(list, 10);
    list_push_back(list, 20);
    list_push_front(list, 5);
    
    // 输出: [5, 10, 20]
    list_print_int(list);
    
    // 查找
    long idx = list_find_int(list, 10);
    printf("Index of 10: %ld\n", idx);  // 1
    
    // 排序和反转
    list_sort(list);      // [5, 10, 20]
    list_reverse(list);   // [20, 10, 5]
    
    // 清理
    list_destroy(list);
    
    return 0;
}
```

## 编译

```bash
# 编译库
gcc -c linked_list_utils.c -o linked_list_utils.o

# 编译示例
gcc linked_list_utils.c example.c -o example
./example

# 运行测试
gcc linked_list_utils.c linked_list_utils_test.c -o test
./test
```

## API 文档

### 创建和销毁

```c
LinkedList* list_create_int(void);                     // 创建整数链表
LinkedList* list_create_double(void);                  // 创建浮点链表
LinkedList* list_create_string(void);                  // 创建字符串链表
LinkedList* list_create_pointer(void);                 // 创建指针链表
LinkedList* list_create_generic(size_t size, void (*free)(void*)); // 创建通用链表
void list_destroy(LinkedList* list);                   // 销毁链表
void list_clear(LinkedList* list);                     // 清空链表
```

### 头部操作

```c
bool list_push_front(LinkedList* list, ...);  // 头部插入
bool list_pop_front(LinkedList* list);        // 头部移除
ListNode* list_front(LinkedList* list);       // 获取头部节点
```

### 尾部操作

```c
bool list_push_back(LinkedList* list, ...);   // 尾部插入
bool list_pop_back(LinkedList* list);         // 尾部移除
ListNode* list_back(LinkedList* list);        // 获取尾部节点
```

### 索引操作

```c
bool list_insert_at(LinkedList* list, size_t index, ...);  // 指定位置插入
bool list_remove_at(LinkedList* list, size_t index);       // 指定位置移除
ListNode* list_get_node(LinkedList* list, size_t index);   // 获取节点

// 类型安全的获取函数
bool list_get_int(LinkedList* list, size_t index, int* out);
bool list_get_double(LinkedList* list, size_t index, double* out);
bool list_get_string(LinkedList* list, size_t index, const char** out);
bool list_get_pointer(LinkedList* list, size_t index, void** out);
```

### 查找操作

```c
long list_find_int(LinkedList* list, int value);
long list_find_double(LinkedList* list, double value, double epsilon);
long list_find_string(LinkedList* list, const char* value);
long list_find_pointer(LinkedList* list, void* value);

bool list_contains_int(LinkedList* list, int value);
bool list_contains_string(LinkedList* list, const char* value);
```

### 删除操作

```c
bool list_remove_int(LinkedList* list, int value);      // 删除第一个匹配
bool list_remove_string(LinkedList* list, const char* value);
size_t list_remove_all_int(LinkedList* list, int value); // 删除所有匹配
```

### 信息查询

```c
size_t list_size(LinkedList* list);
bool list_is_empty(LinkedList* list);
ListType list_get_type(LinkedList* list);
```

### 链表操作

```c
void list_reverse(LinkedList* list);           // 反转
void list_concat(LinkedList* list, LinkedList* other);  // 连接
LinkedList* list_clone(LinkedList* list);      // 克隆
void list_sort(LinkedList* list);              // 排序 (仅整数)
void list_unique(LinkedList* list);            // 去重 (需已排序)
```

### 迭代器

```c
ListIterator list_iterator(LinkedList* list);            // 正向迭代器
ListIterator list_iterator_reverse(LinkedList* list);    // 反向迭代器
bool list_iterator_next(ListIterator* it);               // 移动到下一个
ListNode* list_iterator_get(ListIterator* it);           // 获取当前节点
int list_iterator_get_int(ListIterator* it);             // 获取当前整数
const char* list_iterator_get_string(ListIterator* it);  // 获取当前字符串
```

### 工具函数

```c
LinkedList* list_from_int_array(int* arr, size_t size);
LinkedList* list_from_string_array(const char** arr, size_t size);
int* list_to_int_array(LinkedList* list, size_t* out_size);

void list_foreach(LinkedList* list, void (*cb)(ListNode*, void*), void* data);
LinkedList* list_filter(LinkedList* list, bool (*pred)(ListNode*, void*), void* data);
bool list_fold_int(LinkedList* list, int init, int (*func)(int, int, void*), void* data, int* result);

void list_print(LinkedList* list);
void list_print_int(LinkedList* list);
void list_print_string(LinkedList* list);
```

## 使用示例

### 整数链表

```c
LinkedList* nums = list_create_int();

// 添加元素
list_push_back(nums, 30);
list_push_back(nums, 10);
list_push_back(nums, 20);

// 排序: [10, 20, 30]
list_sort(nums);

// 遍历
ListIterator it = list_iterator(nums);
while (it.current) {
    printf("%d ", list_iterator_get_int(&it));
    list_iterator_next(&it);
}

list_destroy(nums);
```

### 字符串链表

```c
LinkedList* words = list_create_string();

list_push_back(words, "Hello");
list_push_back(words, "World");
list_push_front(words, "Start");

// 输出: ["Start", "Hello", "World"]
list_print_string(words);

// 查找
long idx = list_find_string(words, "Hello");  // 返回 1

list_destroy(words);
```

### 数组转换

```c
int arr[] = {1, 2, 3, 4, 5};
LinkedList* list = list_from_int_array(arr, 5);

// 转回数组
size_t size;
int* out = list_to_int_array(list, &size);

for (size_t i = 0; i < size; i++) {
    printf("%d ", out[i]);
}
free(out);

list_destroy(list);
```

### 求和

```c
LinkedList* nums = list_create_int();
list_push_back(nums, 1);
list_push_back(nums, 2);
list_push_back(nums, 3);

int sum;
list_fold_int(nums, 0,
    [](int acc, int val, void*) -> int { return acc + val; },
    NULL, &sum);
printf("Sum: %d\n", sum);  // 6

list_destroy(nums);
```

## 设计特点

1. **类型安全** - 每种数据类型有专门的创建函数和操作
2. **内存管理** - 字符串自动深拷贝，销毁时自动释放
3. **性能优化** - 索引访问从最近的端点开始
4. **零依赖** - 仅使用 C 标准库
5. **丰富功能** - 排序、反转、克隆、迭代器、函数式操作

## 许可证

MIT License