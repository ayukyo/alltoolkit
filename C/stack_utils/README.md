# Stack Utils - C

通用栈数据结构实现，支持任意数据类型，零外部依赖。

## 功能特性

- **泛型支持** - 使用 `void*` 实现类型无关的栈
- **动态扩容** - 自动扩容，按需增长
- **内存高效** - 支持预分配和收缩
- **线程安全宏** - 为常用类型提供便捷宏
- **完整 API** - push、pop、peek、copy、reverse 等

## 文件结构

```
stack_utils/
├── stack.h          # 头文件，API 声明
├── stack.c          # 实现
├── test_stack.c     # 单元测试
├── example_stack.c  # 使用示例
├── Makefile         # 构建脚本
└── README.md        # 本文档
```

## 快速开始

### 编译

```bash
# 编译测试
make test

# 编译示例
make example

# 编译调试版本
make debug

# 运行测试
make run-test
```

### 基本用法

```c
#include "stack.h"

int main(void) {
    // 创建整数栈
    Stack *stack = stack_create_int();
    
    // 压栈
    stack_push_int(stack, 10);
    stack_push_int(stack, 20);
    stack_push_int(stack, 30);
    
    // 查看栈顶
    int top;
    stack_peek_int(stack, &top);  // top = 30
    
    // 弹栈 (LIFO 顺序)
    stack_pop_int(stack, &top);   // top = 30
    stack_pop_int(stack, &top);   // top = 20
    stack_pop_int(stack, &top);   // top = 10
    
    // 释放
    stack_free(&stack);
    return 0;
}
```

## API 参考

### 创建与销毁

| 函数 | 说明 |
|------|------|
| `Stack *stack_create(size_t elem_size, size_t initial_capacity)` | 创建栈 |
| `void stack_free(Stack **stack)` | 释放栈 |

### 基本操作

| 函数 | 说明 |
|------|------|
| `bool stack_push(Stack *stack, const void *elem)` | 压栈 |
| `bool stack_pop(Stack *stack, void *out)` | 弹栈 |
| `bool stack_peek(const Stack *stack, void *out)` | 查看栈顶 |
| `bool stack_is_empty(const Stack *stack)` | 是否为空 |
| `size_t stack_size(const Stack *stack)` | 元素数量 |

### 内存管理

| 函数 | 说明 |
|------|------|
| `size_t stack_capacity(const Stack *stack)` | 获取容量 |
| `void stack_clear(Stack *stack)` | 清空栈 |
| `bool stack_reserve(Stack *stack, size_t capacity)` | 预留容量 |
| `bool stack_shrink_to_fit(Stack *stack)` | 收缩到当前大小 |

### 高级操作

| 函数 | 说明 |
|------|------|
| `Stack *stack_copy(const Stack *stack)` | 深拷贝 |
| `void stack_reverse(Stack *stack)` | 反转栈 |
| `bool stack_at(const Stack *stack, size_t index, void *out)` | 按索引访问 |

### 便捷宏

```c
// 创建特定类型栈
stack_create_int()     // int 栈
stack_create_double()  // double 栈
stack_create_char()    // char 栈
stack_create_size()    // size_t 栈

// 类型安全操作
stack_push_int(s, 42)
stack_pop_int(s, &val)
stack_peek_int(s, &val)
```

## 使用场景

1. **表达式求值** - 后缀表达式计算
2. **括号匹配** - 语法分析
3. **撤销系统** - 操作历史管理
4. **字符串反转** - 字符处理
5. **深度优先搜索** - 图/树遍历
6. **函数调用栈** - 递归模拟

## 示例：括号匹配

```c
bool is_balanced(const char *expr) {
    Stack *stack = stack_create_char();
    
    for (size_t i = 0; expr[i]; i++) {
        char c = expr[i];
        if (c == '(' || c == '[' || c == '{') {
            stack_push_char(stack, c);
        } else if (c == ')' || c == ']' || c == '}') {
            if (stack_is_empty(stack)) {
                stack_free(&stack);
                return false;
            }
            char top;
            stack_pop_char(stack, &top);
            if (!matching(top, c)) {
                stack_free(&stack);
                return false;
            }
        }
    }
    
    bool balanced = stack_is_empty(stack);
    stack_free(&stack);
    return balanced;
}
```

## 性能特点

| 操作 | 时间复杂度 |
|------|------------|
| push | O(1) 均摊 |
| pop | O(1) |
| peek | O(1) |
| size | O(1) |
| capacity | O(1) |
| copy | O(n) |
| reverse | O(n) |

## 测试覆盖

- ✅ 创建/销毁
- ✅ 基本操作 (push/pop/peek)
- ✅ 空栈处理
- ✅ 容量管理
- ✅ 深拷贝
- ✅ 反转
- ✅ 索引访问
- ✅ 多种数据类型 (int/double/char/struct)
- ✅ 大规模数据 (10000 元素)
- ✅ NULL 参数处理

## 许可证

MIT License - AllToolkit

---
*作者: AllToolkit*  
*日期: 2026-04-22*