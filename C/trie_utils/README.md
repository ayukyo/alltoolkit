# Trie Utils - C 语言 Trie（前缀树）实现

一个高效的 Trie 数据结构实现，用于字符串存储和前缀操作。零外部依赖，纯 C 标准库实现。

## 功能特性

### 基本操作
- `trie_create()` - 创建新的 Trie
- `trie_destroy()` - 销毁 Trie 并释放内存
- `trie_clear()` - 清空 Trie 内容
- `trie_insert()` - 插入单词
- `trie_search()` - 搜索单词
- `trie_delete()` - 删除单词
- `trie_insert_batch()` - 批量插入单词

### 前缀操作
- `trie_starts_with()` - 检查是否有单词以给定前缀开头
- `trie_get_prefix_node()` - 获取前缀节点
- `trie_count_prefix()` - 计算以给定前缀开头的单词数
- `trie_longest_common_prefix()` - 计算最长公共前缀

### 自动补全
- `trie_get_words_with_prefix()` - 获取所有以给定前缀开头的单词
- `trie_get_all_words()` - 获取 Trie 中所有单词

### 模式匹配
- `trie_pattern_match()` - 支持 `?`（单字符）和 `*`（多字符）通配符匹配

### 迭代器支持
- `trie_iterator_init()` - 初始化迭代器
- `trie_iterator_next()` - 获取下一个单词
- `trie_iterator_has_next()` - 检查是否还有更多单词

### 工具函数
- `trie_size()` - 获取单词总数
- `trie_node_count()` - 获取节点总数
- `trie_is_empty()` - 检查是否为空
- `trie_memory_usage()` - 计算内存使用量
- `trie_print()` - 打印 Trie 内容（调试用）

## 文件结构

```
C/trie_utils/
├── trie.h              # 头文件（API 定义）
├── trie.c              # 实现文件
├── trie_test.c         # 单元测试（25+ 测试）
├── Makefile            # 构建配置
├── README.md           # 本文档
└── examples/           # 示例程序
    ├── basic_usage.c       # 基础用法示例
    ├── autocomplete.c      # 自动补全示例
    ├── spell_checker.c     # 拼写检查示例
    ├── word_frequency.c    # 词频统计示例
    └ iterator_demo.c       # 迭代器演示
```

## 构建与测试

```bash
# 构建对象文件
make all

# 运行单元测试
make test

# 构建所有示例
make examples

# 运行部分示例
make run_examples

# 清理构建产物
make clean
```

## 使用示例

### 基础用法

```c
#include "trie.h"

int main() {
    // 创建 Trie
    Trie *trie = trie_create();
    
    // 插入单词
    trie_insert(trie, "apple");
    trie_insert(trie, "application");
    trie_insert(trie, "banana");
    
    // 搜索
    if (trie_search(trie, "apple")) {
        printf("Found 'apple'!\n");
    }
    
    // 前缀检查
    printf("Words with 'app': %zu\n", trie_count_prefix(trie, "app"));
    
    // 自动补全
    TrieWordsResult result = trie_get_words_with_prefix(trie, "app", 10);
    for (size_t i = 0; i < result.count; i++) {
        printf("  %s\n", result.words[i]);
    }
    trie_free_words_result(&result);
    
    // 销毁
    trie_destroy(trie);
    return 0;
}
```

### 编译

```bash
# 单文件编译
gcc -Wall -O2 your_program.c trie.c -o your_program

# 使用对象文件
gcc -Wall -O2 trie.c -c -o trie.o
gcc -Wall -O2 your_program.c trie.o -o your_program
```

## API 参考

### 创建/销毁

| 函数 | 说明 |
|------|------|
| `Trie *trie_create(void)` | 创建新的空 Trie |
| `void trie_destroy(Trie *trie)` | 销毁 Trie |
| `void trie_clear(Trie *trie)` | 清空内容 |

### 基本操作

| 函数 | 说明 |
|------|------|
| `bool trie_insert(Trie *trie, const char *word)` | 插入单词 |
| `bool trie_search(const Trie *trie, const char *word)` | 搜索单词 |
| `bool trie_delete(Trie *trie, const char *word)` | 删除单词 |
| `size_t trie_insert_batch(Trie *trie, const char **words, size_t count)` | 批量插入 |

### 前缀操作

| 函数 | 说明 |
|------|------|
| `bool trie_starts_with(const Trie *trie, const char *prefix)` | 检查前缀是否存在 |
| `size_t trie_count_prefix(const Trie *trie, const char *prefix)` | 计算前缀单词数 |
| `size_t trie_longest_common_prefix(...)` | 最长公共前缀 |

### 自动补全

| 函数 | 说明 |
|------|------|
| `TrieWordsResult trie_get_words_with_prefix(...)` | 获取前缀单词 |
| `TrieWordsResult trie_get_all_words(const Trie *trie)` | 获取所有单词 |
| `void trie_free_words_result(TrieWordsResult *result)` | 释放结果 |

## 性能特性

- **插入**: O(m)，m 为单词长度
- **搜索**: O(m)
- **删除**: O(m)
- **前缀查询**: O(m) + 结果数量
- **内存**: 每节点约 128 字节（ASCII 范围）

## 测试覆盖

单元测试覆盖以下场景：
- 创建/销毁操作
- 单词插入（单个、多个、重复）
- 单词搜索（存在、不存在、前缀）
- 单词删除（叶节点、共享前缀）
- 前缀操作
- 自动补全功能
- 模式匹配（? 和 * 通配符）
- 迭代器遍历
- 边界情况处理（NULL、空字符串、长单词）
- 大量单词处理

## 许可证

MIT License

## 作者

AllToolkit 自动化生成

## 日期

2026-04-22