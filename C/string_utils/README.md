# C String Utils

C 语言字符串工具库 - 零依赖，仅使用标准库。

## 功能特性

- **字符串修剪** - trim_left, trim_right, trim, trim_chars
- **字符串分割** - split, split_char (支持最大分割次数)
- **字符串替换** - replace, replace_first, replace_n
- **字符串查找** - count, starts_with, ends_with
- **大小写转换** - to_upper, to_lower (原地修改和复制版本)
- **安全复制/连接** - copy_safe, concat_safe (带边界检查)
- **字符串重复** - repeat
- **字符串连接** - join_array
- **字符串验证** - is_blank, is_numeric, is_integer, is_float, is_alpha, is_alphanumeric
- **子字符串** - substring, left, right, drop_left, drop_right
- **字符串清理** - remove_whitespace, remove_chars, normalize_whitespace

## 快速开始

```c
#include "string_utils.h"
#include <stdio.h>

int main() {
    // Trim
    char s[] = "  hello  ";
    str_trim(s);
    printf("%s\n", s);  // "hello"
    
    // Split
    StringSplitResult r = str_split("a,b,c", ",", 0);
    for (size_t i = 0; i < r.count; i++) {
        printf("%s\n", r.tokens[i]);
    }
    str_split_free(&r);
    
    // Replace
    char* result = str_replace("hello world", "world", "C");
    printf("%s\n", result);  // "hello C"
    free(result);
    
    return 0;
}
```

## 编译

```bash
# 编译库
gcc -c string_utils.c -o string_utils.o

# 编译示例
gcc string_utils.c example.c -o example
./example

# 运行测试
gcc string_utils.c string_utils_test.c -o test
./test
```

## API 文档

### 字符串修剪

```c
char* str_trim_left(char* str);                    // 去除左侧空白
char* str_trim_right(char* str);                   // 去除右侧空白
char* str_trim(char* str);                         // 去除两侧空白
char* str_trim_chars(char* str, const char* chars); // 去除指定字符
```

### 字符串分割

```c
StringSplitResult str_split(const char* str, const char* delimiter, size_t max_splits);
StringSplitResult str_split_char(const char* str, char delimiter, size_t max_splits);
void str_split_free(StringSplitResult* result);
```

### 字符串替换

```c
char* str_replace(const char* str, const char* old_sub, const char* new_sub);
char* str_replace_first(const char* str, const char* old_sub, const char* new_sub);
char* str_replace_n(const char* str, const char* old_sub, const char* new_sub, size_t n);
```

### 字符串查找

```c
size_t str_count(const char* str, const char* sub);
bool str_starts_with(const char* str, const char* prefix);
bool str_ends_with(const char* str, const char* suffix);
```

### 大小写转换

```c
char* str_to_upper(char* str);              // 原地修改
char* str_to_lower(char* str);              // 原地修改
char* str_to_upper_copy(const char* str);   // 返回新字符串
char* str_to_lower_copy(const char* str);   // 返回新字符串
```

### 安全复制/连接

```c
size_t str_copy_safe(char* dest, const char* src, size_t dest_size);
size_t str_concat_safe(char* dest, const char* src, size_t dest_size);
```

### 其他工具

```c
char* str_repeat(const char* str, size_t n);
char* str_join_array(const char** strings, size_t count, const char* separator);
bool str_is_blank(const char* str);
bool str_is_numeric(const char* str);
bool str_is_integer(const char* str);
bool str_is_float(const char* str);
bool str_is_alpha(const char* str);
bool str_is_alphanumeric(const char* str);
char* str_substring(const char* str, size_t start, size_t length);
char* str_left(const char* str, size_t n);
char* str_right(const char* str, size_t n);
char* str_drop_left(const char* str, size_t n);
char* str_drop_right(const char* str, size_t n);
char* str_remove_whitespace(char* str);
char* str_remove_chars(char* str, const char* chars);
char* str_normalize_whitespace(char* str);
```

## 许可证

MIT License
