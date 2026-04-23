# Lorem Ipsum 工具库

C 语言实现的 Lorem Ipsum 文本生成工具，零外部依赖。

## 功能特性

- 📝 **单词生成** - 生成指定数量的随机拉丁单词
- 📄 **句子生成** - 生成指定数量的完整句子
- 📑 **段落生成** - 生成指定数量的文本段落
- 🎯 **自定义参数** - 精确控制每句单词数和每段句子数
- 🔄 **可重复生成** - 支持固定随机种子
- 📖 **经典开头** - 提供标准 Lorem Ipsum 开头段落

## 快速开始

### 编译

```bash
# 编译测试
gcc -o test_lorem lorem_ipsum_utils.c lorem_ipsum_utils_test.c

# 运行测试
./test_lorem

# 编译示例
gcc -o example example.c lorem_ipsum_utils.c

# 运行示例
./example
```

## API 参考

### 基础生成函数

```c
#include "lorem_ipsum_utils.h"

// 生成指定数量的单词
size_t lorem_words(size_t count, char* buffer, size_t buffer_size);

// 生成指定数量的句子
size_t lorem_sentences(size_t count, char* buffer, size_t buffer_size);

// 生成指定数量的段落
size_t lorem_paragraphs(size_t count, char* buffer, size_t buffer_size);
```

### 自定义生成函数

```c
// 生成自定义句子（指定每句单词数范围）
size_t lorem_sentences_custom(size_t count, size_t min_words, size_t max_words,
                              char* buffer, size_t buffer_size);

// 生成自定义段落（指定每段句子数和每句单词数范围）
size_t lorem_paragraphs_custom(size_t count,
                                size_t min_sentences, size_t max_sentences,
                                size_t min_words, size_t max_words,
                                char* buffer, size_t buffer_size);
```

### 随机种子控制

```c
// 设置随机种子（用于可重复生成）
void lorem_set_seed(unsigned int seed);

// 重置为默认随机状态
void lorem_reset_seed(void);
```

### 工具函数

```c
// 获取单个随机单词
size_t lorem_single_word(char* buffer, size_t buffer_size);

// 获取经典 Lorem Ipsum 开头段落
size_t lorem_classic_start(char* buffer, size_t buffer_size);

// 计算生成指定内容所需的缓冲区大小
// type: 'w'=单词, 's'=句子, 'p'=段落
size_t lorem_estimate_buffer(char type, size_t count);
```

## 使用示例

### 生成单词

```c
char buffer[200];
lorem_words(10, buffer, sizeof(buffer));
// 输出: "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod"
```

### 生成句子

```c
char buffer[500];
lorem_sentences(3, buffer, sizeof(buffer));
// 输出: "Lorem ipsum dolor sit amet. Consectetur adipiscing elit sed do. 
//        Eiusmod tempor incididunt ut labore."
```

### 自定义句子

```c
char buffer[300];
// 生成 2 个句子，每句 4-6 个单词
lorem_sentences_custom(2, 4, 6, buffer, sizeof(buffer));
// 输出: "Lorem ipsum dolor sit. Amet consectetur adipiscing elit."
```

### 生成段落

```c
char buffer[2000];
lorem_paragraphs(2, buffer, sizeof(buffer));
// 输出两个段落，每段 3-7 句
```

### 可重复生成

```c
// 设置固定种子
lorem_set_seed(42);
char buf1[200];
lorem_words(10, buf1, sizeof(buf1));

// 再次设置相同种子
lorem_set_seed(42);
char buf2[200];
lorem_words(10, buf2, sizeof(buf2));

// buf1 和 buf2 内容完全相同
```

### 经典开头

```c
char buffer[500];
lorem_classic_start(buffer, sizeof(buffer));
// 输出标准 Lorem Ipsum 开头段落
```

## 缓冲区管理

所有生成函数都接受缓冲区和大小参数，确保不会发生缓冲区溢出：

```c
// 估算所需缓冲区大小
size_t needed = lorem_estimate_buffer('p', 5);  // 5 个段落
char* buffer = malloc(needed);
lorem_paragraphs(5, buffer, needed);
free(buffer);
```

## 设计特点

1. **零外部依赖** - 仅使用 C 标准库
2. **线程安全** - 每个线程可设置独立的随机种子
3. **内存高效** - 不做动态内存分配，完全由调用者管理
4. **缓冲区安全** - 所有函数都有缓冲区大小检查
5. **可预测输出** - 支持固定种子实现可重复生成

## 文件结构

```
lorem_ipsum_utils/
├── lorem_ipsum_utils.h      # 头文件
├── lorem_ipsum_utils.c      # 实现文件
├── lorem_ipsum_utils_test.c # 测试文件
├── example.c                # 示例程序
└── README.md                # 说明文档
```

## 许可证

MIT License