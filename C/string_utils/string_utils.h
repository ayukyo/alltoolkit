/**
 * @file string_utils.h
 * @brief C语言通用字符串处理工具库
 * @author AllToolkit
 * @version 1.0.0
 * @date 2026-04-02
 *
 * 本库提供了一系列无依赖、可直接复用的C语言字符串处理函数。
 * 所有函数均使用标准C库，无需额外依赖。
 */

#ifndef STRING_UTILS_H
#define STRING_UTILS_H

#include <stddef.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief 去除字符串首尾的空白字符
 *
 * 原地修改字符串，去除开头的空格、制表符、换行符、回车符等空白字符，
 * 并在第一个非空白字符后的连续空白字符处截断字符串。
 *
 * @param str 待处理的字符串（会被修改）
 * @return char* 返回处理后的字符串指针（与输入相同）
 *
 * @note 该函数会修改原字符串，如需保留原字符串请先复制
 * @example
 *   char s[] = "  hello world  ";
 *   str_trim(s); // s 变为 "hello world"
 */
char* str_trim(char* str);

/**
 * @brief 去除字符串左侧的空白字符
 *
 * @param str 待处理的字符串（会被修改）
 * @return char* 返回处理后的字符串指针（与输入相同）
 */
char* str_trim_left(char* str);

/**
 * @brief 去除字符串右侧的空白字符
 *
 * @param str 待处理的字符串（会被修改）
 * @return char* 返回处理后的字符串指针（与输入相同）
 */
char* str_trim_right(char* str);

/**
 * @brief 将字符串转换为小写
 *
 * @param str 待处理的字符串（会被修改）
 * @return char* 返回处理后的字符串指针（与输入相同）
 */
char* str_to_lower(char* str);

/**
 * @brief 将字符串转换为大写
 *
 * @param str 待处理的字符串（会被修改）
 * @return char* 返回处理后的字符串指针（与输入相同）
 */
char* str_to_upper(char* str);

/**
 * @brief 反转字符串
 *
 * @param str 待反转的字符串（会被修改）
 * @return char* 返回处理后的字符串指针（与输入相同）
 */
char* str_reverse(char* str);

/**
 * @brief 检查字符串是否以指定前缀开头
 *
 * @param str 待检查的字符串
 * @param prefix 前缀字符串
 * @return bool 如果以prefix开头返回true，否则返回false
 */
bool str_starts_with(const char* str, const char* prefix);

/**
 * @brief 检查字符串是否以指定后缀结尾
 *
 * @param str 待检查的字符串
 * @param suffix 后缀字符串
 * @return bool 如果以suffix结尾返回true，否则返回false
 */
bool str_ends_with(const char* str, const char* suffix);

/**
 * @brief 计算字符串在目标字符串中出现的次数
 *
 * @param str 目标字符串
 * @param substr 要查找的子字符串
 * @return size_t 出现次数（不重叠匹配）
 */
size_t str_count(const char* str, const char* substr);

/**
 * @brief 安全的字符串复制函数
 *
 * 复制src到dest，最多复制max_len-1个字符，确保dest以'\0'结尾。
 * 比strncpy更安全，不会留下未终止的字符串。
 *
 * @param dest 目标缓冲区
 * @param src 源字符串
 * @param max_len 目标缓冲区大小（包括终止符）
 * @return size_t 实际复制的字符数（不包括终止符）
 */
size_t str_copy_safe(char* dest, const char* src, size_t max_len);

/**
 * @brief 判断字符是否为空白字符
 *
 * @param c 待判断的字符
 * @return bool 如果是空白字符返回true，否则返回false
 */
bool is_whitespace(char c);

#ifdef __cplusplus
}
#endif

#endif /* STRING_UTILS_H */
