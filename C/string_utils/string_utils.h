/**
 * @file string_utils.h
 * @brief C 语言字符串工具库
 * @author AllToolkit
 * @version 1.0.0
 * @date 2026-04-04
 */

#ifndef STRING_UTILS_H
#define STRING_UTILS_H

#include <stddef.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ==================== 类型定义 ==================== */

typedef struct {
    char** tokens;
    size_t count;
    size_t capacity;
} StringSplitResult;

/* ==================== 字符串修剪 ==================== */
char* str_trim_left(char* str);
char* str_trim_right(char* str);
char* str_trim(char* str);
char* str_trim_chars(char* str, const char* chars);

/* ==================== 字符串分割 ==================== */
StringSplitResult str_split(const char* str, const char* delimiter, size_t max_splits);
StringSplitResult str_split_char(const char* str, char delimiter, size_t max_splits);
void str_split_free(StringSplitResult* result);

/* ==================== 字符串替换 ==================== */
char* str_replace(const char* str, const char* old_sub, const char* new_sub);
char* str_replace_first(const char* str, const char* old_sub, const char* new_sub);
char* str_replace_n(const char* str, const char* old_sub, const char* new_sub, size_t n);

/* ==================== 字符串查找 ==================== */
size_t str_count(const char* str, const char* sub);
bool str_starts_with(const char* str, const char* prefix);
bool str_ends_with(const char* str, const char* suffix);

/* ==================== 大小写转换 ==================== */
char* str_to_upper(char* str);
char* str_to_lower(char* str);
char* str_to_upper_copy(const char* str);
char* str_to_lower_copy(const char* str);

/* ==================== 字符串复制和连接 ==================== */
size_t str_copy_safe(char* dest, const char* src, size_t dest_size);
size_t str_concat_safe(char* dest, const char* src, size_t dest_size);
char* str_repeat(const char* str, size_t n);
char* str_join_array(const char** strings, size_t count, const char* separator);

/* ==================== 字符串判断 ==================== */
bool str_is_blank(const char* str);
bool str_is_numeric(const char* str);
bool str_is_integer(const char* str);
bool str_is_float(const char* str);
bool str_is_alpha(const char* str);
bool str_is_alphanumeric(const char* str);

/* ==================== 子字符串 ==================== */
char* str_substring(const char* str, size_t start, size_t length);
char* str_left(const char* str, size_t n);
char* str_right(const char* str, size_t n);
char* str_drop_left(const char* str, size_t n);
char* str_drop_right(const char* str, size_t n);

/* ==================== 字符串清理 ==================== */
char* str_remove_whitespace(char* str);
char* str_remove_chars(char* str, const char* chars);
char* str_normalize_whitespace(char* str);

/* ==================== 辅助函数 ==================== */
bool str_is_whitespace(char c);

#ifdef __cplusplus
}
#endif

#endif /* STRING_UTILS_H */
