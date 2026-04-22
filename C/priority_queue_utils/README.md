# Priority Queue Utils - C

通用优先队列（最小堆）数据结构实现，支持任意数据类型，零外部依赖。

## 功能特性

- **泛型支持** - 使用 `void*` 实现类型无关的优先队列
- **最小堆** - 低优先级值先出队（priority 值越小越优先）
- **动态扩容** - 自动扩容，按需增长
- **内存高效** - 支持预分配和收缩
- **完整 API** - insert、extract、peek、merge、update 等
- **便捷宏** - 为常用类型提供便捷宏

## 文件结构

```
priority_queue_utils/
├── priority_queue.h          # 头文件，API 声明
├── priority_queue.c          # 实现
├── test_priority_queue.c     # 单元测试
├── example_priority_queue.c  # 使用示例
├── Makefile                  # 构建脚本
└── README.md                 # 本文档
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
#include "priority_queue.h"

int main(void) {
    // 创建整数优先队列
    PriorityQueue *pq = pq_create_int();
    
    // 插入元素（优先级值越小越优先）
    pq_insert_int(pq, 30, 3.0);
    pq_insert_int(pq, 10, 1.0);  // 最高优先级
    pq_insert_int(pq, 20, 2.0);
    
    // 查看队首
    int top;
    double priority;
    pq_peek_int(pq, &top, &priority);  // top = 10, priority = 1.0
    
    // 按优先级出队
    pq_extract_int(pq, &top, NULL);    // top = 10
    pq_extract_int(pq, &top, NULL);    // top = 20
    pq_extract_int(pq, &top, NULL);    // top = 30
    
    // 释放
    pq_free(&pq);
    return 0;
}
```

## API 参考

### 创建与销毁

| 函数 | 说明 |
|------|------|
| `PriorityQueue *pq_create(size_t elem_size, size_t initial_capacity)` | 创建优先队列 |
| `void pq_free(PriorityQueue **pq)` | 释放优先队列 |

### 基本操作

| 函数 | 说明 |
|------|------|
| `bool pq_insert(PriorityQueue *pq, const void *data, double priority)` | 插入元素 |
| `bool pq_extract_min(PriorityQueue *pq, void *out, double *out_priority)` | 提取最小优先级元素 |
| `bool pq_peek_min(const PriorityQueue *pq, void *out, double *out_priority)` | 查看队首 |
| `bool pq_is_empty(const PriorityQueue *pq)` | 是否为空 |
| `size_t pq_size(const PriorityQueue *pq)` | 元素数量 |

### 内存管理

| 函数 | 说明 |
|------|------|
| `size_t pq_capacity(const PriorityQueue *pq)` | 获取容量 |
| `void pq_clear(PriorityQueue *pq)` | 清空队列 |
| `bool pq_reserve(PriorityQueue *pq, size_t capacity)` | 预留容量 |
| `bool pq_shrink_to_fit(PriorityQueue *pq)` | 收缩到当前大小 |

### 高级操作

| 函数 | 说明 |
|------|------|
| `bool pq_contains_priority(const PriorityQueue *pq, double priority)` | 检查是否存在指定优先级 |
| `bool pq_update_priority(PriorityQueue *pq, const void *data, double new_priority, int (*cmp)(const void*, const void*))` | 更新元素优先级 |
| `bool pq_merge(PriorityQueue *pq, const PriorityQueue *other)` | 合合另一个队列 |
| `bool pq_get_sorted(const PriorityQueue *pq, void *out_data, double *out_priorities)` | 获取排序后的数据（不修改队列） |

### 便捷宏

```c
// 创建特定类型优先队列
pq_create_int()     // int 优先队列
pq_create_double()  // double 优先队列
pq_create_char()    // char 优先队列
pq_create_size()    // size_t 优先队列

// 类型安全操作
pq_insert_int(pq, 42, 1.0)
pq_extract_int(pq, &val, &pri)
pq_peek_int(pq, &val, &pri)
```

## 使用场景

1. **任务调度** - 按优先级执行任务
2. **Dijkstra 算法** - 最短路径计算
3. **A* 寻路** - 游戏路径规划
4. **事件模拟** - 按时间顺序处理事件
5. **急诊室分诊** - 按病情严重程度排序
6. **堆排序** - 高效排序算法

## 示例：任务调度器

```c
typedef struct {
    char name[32];
    int id;
} Task;

PriorityQueue *scheduler = pq_create(sizeof(Task), 0);

Task urgent = {"Fix Critical Bug", 1};
Task normal = {"Update Docs", 2};

pq_insert(scheduler, &urgent, 1.0);   // 高优先级
pq_insert(scheduler, &normal, 4.0);   // 低优先级

// 按优先级执行
while (!pq_is_empty(scheduler)) {
    Task task;
    pq_extract_min(scheduler, &task, NULL);
    printf("Executing: %s\n", task.name);
}
```

## 示例：动态更新优先级

```c
// 将某个任务的优先级提高（改为更小的值）
Task target = {"Update Docs", 2};
pq_update_priority(scheduler, &target, 0.5, cmp_task);

// 现在 "Update Docs" 会最先执行
```

## 性能特点

| 操作 | 时间复杂度 |
|------|------------|
| insert | O(log n) |
| extract_min | O(log n) |
| peek_min | O(1) |
| size | O(1) |
| capacity | O(1) |
| get_sorted | O(n log n) |
| merge | O(m log(n+m)) |

## 测试覆盖

- ✅ 创建/销毁
- ✅ 基本操作 (insert/extract/peek)
- ✅ 空队列处理
- ✅ 相同优先级元素
- ✅ 负优先级值
- ✅ 容量管理
- ✅ 优先级更新
- ✅ 队列合并
- ✅ 排序获取
- ✅ 多种数据类型 (int/double/char/struct)
- ✅ 大规模数据 (10000 元素)
- ✅ NULL 参数处理
- ✅ 堆属性稳定性验证

## 许可证

MIT License - AllToolkit

---
*作者: AllToolkit*  
*日期: 2026-04-23*